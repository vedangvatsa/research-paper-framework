"""Retrospective reanalysis. No network calls and no modification of raw inputs."""

import argparse
import hashlib
import html
import importlib.metadata
import io
import json
import math
import os
import platform
import re
import unicodedata
import zipfile
from concurrent.futures import ProcessPoolExecutor
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd
from lexicalrichness import LexicalRichness
from nltk.tabdata import PunktDecoder
from nltk.tokenize.punkt import PunktParameters, PunktSentenceTokenizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import average_precision_score, confusion_matrix, roc_auc_score
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from threadpoolctl import threadpool_limits

from audit_recovered_data import sha256


PAPER = Path(__file__).resolve().parents[1]
FEATURES = ["mean_sent_len", "sent_len_cv", "hedge_density", "booster_density",
            "self_mention_density", "connector_density", "lexical_diversity_mtld",
            "first_word_connector_ratio"]
LENGTHS = ["word_count", "sentence_count"]
HEDGES = set("may might possibly suggest suggests suggested suggesting appear appears appeared appearing seem seems seemed seeming maybe perhaps probable probably likely unlikely plausible plausibly tentative tentatively indicate indicates indicated indicating".split())
BOOSTERS = set("clearly obviously demonstrate demonstrates demonstrated demonstrating prove proves proved proving establish establishes established establishing definitely show shows showed showing certainly certain undeniably undeniable always never evident evidently indeed".split())
SELF_MENTIONS = set("i we our my us me ours".split())
CONNECTORS = {tuple(s.split()) for s in ["however", "nevertheless", "nonetheless", "conversely", "instead", "contrastingly", "therefore", "consequently", "thus", "hence", "accordingly", "as a result", "furthermore", "moreover", "in addition", "additionally", "besides", "also"]}
WORD = re.compile(r"[^\W\d_]+(?:['\u2019][^\W\d_]+)*", re.UNICODE)
TOKENIZER = None


def clean_text(text):
    return " ".join(unicodedata.normalize("NFKC", html.unescape(str(text))).split())


def normalize(text):
    return " ".join(WORD.findall(clean_text(text).casefold()))


def text_hash(text):
    return hashlib.sha256(normalize(text).encode()).hexdigest()


def valid_source_id(value):
    # OpenAlex has genuine short numeric work IDs inherited from MAG.
    return re.fullmatch(r"https://openalex\.org/W\d+", str(value)) is not None


def load_tokenizer(archive):
    """Load only the four non-executable English parameter tables from NLTK."""
    decoder, params = PunktDecoder(), PunktParameters()
    with zipfile.ZipFile(archive) as resource:
        def stream(name):
            return io.StringIO(resource.read("punkt_tab/english/" + name).decode("utf-8"))
        params.collocations = set(decoder.tab2tups(stream("collocations.tab")))
        params.sent_starters = decoder.txt2set(stream("sent_starters.txt"))
        params.abbrev_types = decoder.txt2set(stream("abbrev_types.txt"))
        params.ortho_context = decoder.tab2intdict(stream("ortho_context.tab"))
    return PunktSentenceTokenizer(params)


def init_worker(archive):
    global TOKENIZER
    TOKENIZER = load_tokenizer(archive)


def count_connectors(words):
    total, i = 0, 0
    while i < len(words):
        match = next((n for n in (3, 2, 1) if tuple(words[i:i+n]) in CONNECTORS), 0)
        total += bool(match)
        i += match or 1
    return total


def extract_features(text, tokenizer):
    text = clean_text(text)
    tokens = WORD.findall(text)
    words = [word.casefold() for word in tokens]
    if not words:
        raise ValueError("no_word_tokens")
    sentences = [WORD.findall(s) for s in tokenizer.tokenize(text)]
    sentences = [s for s in sentences if s]
    if not sentences:
        raise ValueError("no_sentences")
    lengths = np.asarray([len(s) for s in sentences], dtype=float)
    mtld = float(LexicalRichness(" ".join(words), preprocessor=None, tokenizer=str.split).mtld(threshold=0.72))
    if not math.isfinite(mtld) or mtld <= 0:
        raise ValueError("invalid_mtld")
    lower_sents = [[w.casefold() for w in s] for s in sentences]
    openers = sum(any(tuple(s[:n]) in CONNECTORS for n in (1, 2, 3)) for s in lower_sents)
    # US, WE and similar abbreviations are not pronouns. I is retained as a
    # possible first-person pronoun; contextual ambiguity remains documented.
    self_count = sum(w.casefold() in SELF_MENTIONS and (not w.isupper() or w == "I") for w in tokens)
    n = len(words)
    return {
        "word_count": n, "sentence_count": len(sentences),
        "mean_sent_len": float(lengths.mean()),
        "sent_len_cv": float(lengths.std(ddof=0) / lengths.mean()),
        "hedge_density": 1000 * sum(w in HEDGES for w in words) / n,
        "booster_density": 1000 * sum(w in BOOSTERS for w in words) / n,
        "self_mention_density": 1000 * self_count / n,
        "connector_density": 1000 * sum(count_connectors(s) for s in lower_sents) / n,
        "lexical_diversity_mtld": mtld,
        "first_word_connector_ratio": openers / len(sentences),
    }


def extract_pair(record):
    oid, human, generated = record
    try:
        return oid, extract_features(human, TOKENIZER), extract_features(generated, TOKENIZER), None
    except (ValueError, ZeroDivisionError) as error:
        return oid, None, None, type(error).__name__ + ": " + str(error)


def group_pairs(frame):
    """Connected components of source ID, normalized title and either text hash."""
    parent = list(range(len(frame)))

    def root(i):
        while parent[i] != i:
            parent[i] = parent[parent[i]]
            i = parent[i]
        return i

    seen = {}
    for i, row in enumerate(frame.itertuples(index=False)):
        keys = [("id", row.openalex_id), ("title", normalize(row.title)),
                ("text", row.human_hash), ("text", row.ai_hash)]
        for key in keys:
            if key[1]:
                if key in seen:
                    a, b = root(i), root(seen[key])
                    parent[max(a, b)] = min(a, b)
                else:
                    seen[key] = i
    names = {}
    for i, oid in enumerate(frame["openalex_id"]):
        r = root(i)
        names[r] = min(oid, names.get(r, oid))
    return [names[root(i)] for i in range(len(frame))]


def fold_for_group(group):
    return int(hashlib.sha256(("42:" + group).encode()).hexdigest()[:16], 16) % 5


def validate_splits(frame):
    for col in ("pair_id", "group_id", "title_hash", "text_hash"):
        if frame.groupby(col)["fold"].nunique().gt(1).any():
            raise ValueError(f"Related {col} crosses folds")
    if not set(frame["label"]) == {0, 1} or set(frame["fold"]) != set(range(5)):
        raise ValueError("Both classes and all five folds are required")
    for _, group in frame.groupby("pair_id"):
        if len(group) != 2 or set(group["label"]) != {0, 1}:
            raise ValueError("Every pair must contain one record of each class")


def write_json(path, value):
    path.write_text(json.dumps(value, indent=2, allow_nan=False) + "\n")


def extraction(args):
    output = args.output
    if (output / "features.csv.gz").exists():
        raise ValueError("Feature output already exists. Use --stage evaluate or a fresh output directory.")
    pairs = pd.read_csv(args.pairs, keep_default_na=False)
    human = pd.read_csv(args.human, keep_default_na=False)
    if human.openalex_id.duplicated().any() or pairs.openalex_id.duplicated().any():
        raise ValueError("Duplicate source IDs need resolution before joining")
    pairs = pairs.merge(human, on="openalex_id", how="left", suffixes=("", "_source"), validate="one_to_one", indicator=True)
    original_count = len(pairs)
    exclusions = []
    stages = []

    def exclude(mask, reason):
        nonlocal pairs
        exclusions.extend({"pair_id": oid, "reason": reason} for oid in pairs.loc[mask, "openalex_id"])
        stages.append({"reason": reason, "removed_pairs": int(mask.sum())})
        pairs = pairs.loc[~mask].copy()

    exclude(~pairs.openalex_id.map(valid_source_id), "invalid_source_id")
    exclude(pairs["_merge"].ne("both"), "missing_source_record")
    exclude(pairs.title_source.str.strip().eq("") | pairs.title.str.strip().eq(""), "missing_source_title")
    exclude(pairs.title.map(clean_text).ne(pairs.title_source.map(clean_text)), "source_title_mismatch")
    exclude(pairs.human_abstract.ne(pairs.abstract), "source_text_mismatch")
    years = pd.to_numeric(pairs.year, errors="coerce")
    source_years = pd.to_numeric(pairs.year_source, errors="coerce")
    exclude(years.isna() | years.gt(2021) | years.ne(source_years), "invalid_or_mismatched_year")
    # Observed before corrected evaluation. Its stored abstract describes an
    # Indigenous language-learning study, rather than the named 2006 methods paper.
    exclude(pairs.openalex_id.eq("https://openalex.org/W1979290264"), "documented_title_content_conflict")
    pairs["human_hash"] = pairs.human_abstract.map(text_hash)
    pairs["ai_hash"] = pairs.ai_abstract.map(text_hash)
    shared = set(pairs.human_hash) & set(pairs.ai_hash)
    exclude(pairs.human_hash.isin(shared) | pairs.ai_hash.isin(shared), "cross_class_duplicate")
    pairs = pairs.sort_values("openalex_id").reset_index(drop=True)
    exclude(pairs.human_hash.duplicated() | pairs.ai_hash.duplicated(), "normalized_duplicate")
    pairs = pairs.reset_index(drop=True)
    pairs["group_id"] = group_pairs(pairs)
    counts_h = pairs.human_abstract.map(lambda s: len(WORD.findall(clean_text(s))))
    counts_a = pairs.ai_abstract.map(lambda s: len(WORD.findall(clean_text(s))))
    exclude(counts_h.lt(100) | counts_a.lt(100), "under_100_words")
    rows, failures, short_sentence = [], 0, 0
    metadata = pairs.set_index("openalex_id")
    tasks = list(pairs[["openalex_id", "human_abstract", "ai_abstract"]].itertuples(index=False, name=None))
    with ProcessPoolExecutor(max_workers=args.workers, initializer=init_worker,
                             initargs=(str(args.punkt_archive),)) as executor:
        for i, (oid, h, a, error) in enumerate(executor.map(extract_pair, tasks, chunksize=100), 1):
            if error:
                failures += 1
                exclusions.append({"pair_id": oid, "reason": "feature_failure", "detail": error})
                continue
            if min(h["sentence_count"], a["sentence_count"]) < 2:
                short_sentence += 1
                exclusions.append({"pair_id": oid, "reason": "fewer_than_two_sentences"})
                continue
            meta = metadata.loc[oid]
            for label, feats in ((0, h), (1, a)):
                rows.append({"pair_id": oid, "group_id": meta.group_id,
                             "title_hash": text_hash(meta.title), "year": int(float(meta.year)),
                             "text_hash": meta.human_hash if label == 0 else meta.ai_hash,
                             "label": label, "fold": fold_for_group(meta.group_id), **feats})
            if i % 10000 == 0:
                print(f"Extracted {i:,}/{len(tasks):,} candidate pairs", flush=True)
    stages.extend([{"reason": "feature_failure", "removed_pairs": failures},
                   {"reason": "fewer_than_two_sentences", "removed_pairs": short_sentence}])
    frame = pd.DataFrame(rows)
    validate_splits(frame)
    assert original_count == len(frame) // 2 + len(exclusions)
    frame.to_csv(output / "features.csv.gz", index=False, compression={"method": "gzip", "mtime": 0})
    pd.DataFrame(exclusions).to_csv(output / "exclusions.csv", index=False)
    environment = {name: importlib.metadata.version(name) for name in ["numpy", "pandas", "scipy", "scikit-learn", "lexicalrichness", "nltk"]}
    manifest = {"created_utc": datetime.now(timezone.utc).isoformat(), "retrospective": True,
                "input_pairs": original_count, "included_pairs": len(frame) // 2,
                "included_texts": len(frame), "groups": int(frame.group_id.nunique()),
                "exclusion_stages": stages, "seed": 42, "fold_rule": "sha256('42:' + group_id)[:16] modulo 5",
                "features": FEATURES, "min_words": 100, "min_sentences": 2,
                "word_pattern": WORD.pattern, "mtld_threshold": .72,
                "python": platform.python_version(), "packages": environment,
                "inputs": {"pairs_sha256": sha256(args.pairs), "human_sha256": sha256(args.human),
                           "punkt_archive_sha256": sha256(args.punkt_archive)},
                "analysis_code_sha256": sha256(Path(__file__)),
                "features_sha256": sha256(output / "features.csv.gz"),
                "fold_text_counts": {str(k): int(v) for k, v in frame.fold.value_counts().sort_index().items()},
                "known_limits": ["No per-output provider response metadata or generation date",
                                 "Sampling probabilities cannot be reconstructed",
                                 "Source abstracts not individually verified against all publishers",
                                 "No fresh external test set", "Approximate near-duplicates not exhaustively detected",
                                 "No validated language or discipline labels retained"]}
    write_json(output / "manifest.json", manifest)
    print(json.dumps({k: manifest[k] for k in ["included_pairs", "groups", "exclusion_stages"]}, indent=2), flush=True)


def cluster_bootstrap(sums, sizes, repeats=1000):
    rng = np.random.default_rng(42)
    samples = []
    for start in range(0, repeats, 16):
        indices = rng.integers(0, len(sizes), size=(min(16, repeats-start), len(sizes)))
        samples.append(sums[indices].sum(axis=1) / sizes[indices].sum(axis=1)[:, None])
    return np.concatenate(samples)


def descriptives(frame, output):
    human = frame[frame.label == 0].set_index("pair_id").sort_index()
    ai = frame[frame.label == 1].set_index("pair_id").sort_index()
    assert human.index.equals(ai.index)
    delta = ai[FEATURES] - human[FEATURES]
    delta["group_id"] = human.group_id
    grouped = delta.groupby("group_id")[FEATURES]
    draws = cluster_bootstrap(grouped.sum().to_numpy(), grouped.size().to_numpy())
    low, high = np.quantile(draws, [.025, .975], axis=0)
    rows = []
    for j, feature in enumerate(FEATURES):
        h, a = human[feature].to_numpy(), ai[feature].to_numpy()
        rows.append({"feature": feature, "human_mean": h.mean(), "human_sd": h.std(ddof=1),
                     "ai_mean": a.mean(), "ai_sd": a.std(ddof=1),
                     "paired_mean_difference": (a-h).mean(), "difference_ci_low": low[j], "difference_ci_high": high[j],
                     "pooled_cohens_d": (a.mean()-h.mean()) / np.sqrt((h.var(ddof=1)+a.var(ddof=1))/2)})
    pd.DataFrame(rows).to_csv(output / "feature_comparisons.csv", index=False)
    description = {}
    for label, subset in (("published", human), ("generated", ai)):
        description[label] = {col: {str(k): float(v) for k, v in subset[col].quantile([0, .25, .5, .75, 1]).items()}
                              for col in LENGTHS}
    write_json(output / "length_summary.json", description)


def ratios(counts):
    tn, fp, fn, tp = np.moveaxis(np.asarray(counts, dtype=float), -1, 0)
    with np.errstate(divide="ignore", invalid="ignore"):
        return np.stack([(tn+tp)/(tn+fp+fn+tp), tp/(tp+fp), tp/(tp+fn),
                         2*tp/(2*tp+fp+fn), fp/(tn+fp), tn/(tn+fp)], axis=-1)


METRICS = ["accuracy", "precision", "recall", "f1", "false_positive_rate", "specificity"]


def evaluate_model(frame, columns, kind, name, jobs, output):
    values, y = frame[columns].to_numpy(), frame.label.to_numpy()
    probs = np.full(len(frame), np.nan)
    importance, fold_results = [], []
    for fold in range(5):
        train, test = frame.fold.to_numpy() != fold, frame.fold.to_numpy() == fold
        model = (make_pipeline(StandardScaler(), LogisticRegression(max_iter=1000, random_state=42))
                 if kind == "logistic" else RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=jobs))
        with threadpool_limits(limits=1):
            model.fit(values[train], y[train])
            p = model.predict_proba(values[test])[:, 1]
        probs[test] = p
        # sklearn's binary predict uses the first class for an exact tie.
        counts = confusion_matrix(y[test], p > .5, labels=[0, 1]).ravel()
        fold_results.append({"fold": fold, "texts": int(test.sum()),
                             **dict(zip(METRICS, ratios(counts))), "roc_auc": roc_auc_score(y[test], p)})
        if kind != "logistic":
            importance.append(model.feature_importances_)
        print(f"{name} fold {fold+1}: accuracy={ratios(counts)[0]:.4f}", flush=True)
    if not np.isfinite(probs).all():
        raise ValueError("Missing or nonfinite predictions")
    predictions = frame[["pair_id", "group_id", "label", "fold"]].copy()
    predictions["probability"] = probs
    predictions["prediction"] = (probs > .5).astype(int)
    predictions.to_csv(output / f"predictions_{name}.csv.gz", index=False, compression={"method": "gzip", "mtime": 0})
    counts = confusion_matrix(y, probs > .5, labels=[0, 1]).ravel()
    per_group = np.zeros((frame.group_id.nunique(), 4))
    group_codes = pd.factorize(frame.group_id, sort=True)[0]
    cells = y * 2 + (probs > .5).astype(int)
    np.add.at(per_group, (group_codes, cells), 1)
    draws = cluster_bootstrap(per_group, np.ones(len(per_group)))
    ci_low, ci_high = np.quantile(ratios(draws), [.025, .975], axis=0)
    result = {"name": name, "features": columns, "texts": len(frame), "pairs": frame.pair_id.nunique(),
              "confusion_matrix": counts.reshape(2, 2).tolist(),
              **{key: float(value) for key, value in zip(METRICS, ratios(counts))},
              "roc_auc": float(roc_auc_score(y, probs)),
              "average_precision": float(average_precision_score(y, probs)),
              "conditional_group_bootstrap_95ci": {key: [float(lo), float(hi)] for key, lo, hi in zip(METRICS, ci_low, ci_high)},
              "folds": fold_results}
    if importance:
        result["mean_gini_importance"] = dict(zip(columns, np.asarray(importance).mean(axis=0).tolist()))
    write_json(output / f"metrics_{name}.json", result)
    return result


def evaluation(args):
    frame = pd.read_csv(args.output / "features.csv.gz")
    validate_splits(frame)
    manifest = json.loads((args.output / "manifest.json").read_text())
    if manifest["features_sha256"] != sha256(args.output / "features.csv.gz"):
        raise ValueError("Feature table changed after extraction")
    descriptives(frame, args.output)
    cases = [("forest_eight", FEATURES, "forest", frame),
             ("logistic_eight", FEATURES, "logistic", frame),
             ("forest_length", LENGTHS, "forest", frame),
             ("forest_mtld", ["lexical_diversity_mtld"], "forest", frame),
             ("forest_sentence_cv", ["sent_len_cv"], "forest", frame),
             ("forest_without_mtld", [f for f in FEATURES if f != "lexical_diversity_mtld"], "forest", frame)]
    eligible = frame.groupby("pair_id")["word_count"].agg(["min", "max"])
    common_ids = eligible.index[(eligible["min"] >= 150) & (eligible["max"] <= 250)]
    common = frame[frame.pair_id.isin(common_ids)].copy()
    cases.append(("forest_common_length", FEATURES, "forest", common))
    results = []
    for name, columns, kind, subset in cases:
        path = args.output / f"metrics_{name}.json"
        if path.exists():
            raise ValueError(f"Refusing to replace existing model results: {path}")
        results.append(evaluate_model(subset, columns, kind, name, args.workers, args.output))
    write_json(args.output / "evaluation.json", {
        "retrospective": True, "threshold": "probability > 0.5; ties classified as published",
        "interval_scope": "1000 source-group bootstrap draws of fixed out-of-fold predictions; no model refitting",
        "analysis_code_sha256": sha256(Path(__file__)), "models": results,
    })


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--pairs", type=Path, default=PAPER / "data/metadata/synthetic_abstracts_openai.csv")
    parser.add_argument("--human", type=Path, default=PAPER / "data/metadata/openalex_human_abstracts.csv")
    parser.add_argument("--punkt-archive", type=Path, required=True)
    parser.add_argument("--output", type=Path, default=PAPER / "results/correction_20261005/revision2")
    parser.add_argument("--workers", type=int, default=min(8, os.cpu_count() or 1))
    parser.add_argument("--stage", choices=["extract", "evaluate", "all"], default="all")
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    if args.stage in ("extract", "all"):
        extraction(args)
    if args.stage in ("evaluate", "all"):
        evaluation(args)


if __name__ == "__main__":
    main()

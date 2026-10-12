"""Post hoc checks for explicit reviewer objections; primary results stay frozen."""

import hashlib
import importlib.metadata
import json
import shutil
from concurrent.futures import ProcessPoolExecutor
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd
from datasketch import MinHash, MinHashLSH
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import average_precision_score, confusion_matrix, roc_auc_score
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from threadpoolctl import threadpool_limits

from audit_recovered_data import sha256
from audit_text_quality import shingles, signature
from corrected_analysis import FEATURES, LENGTHS, METRICS, cluster_bootstrap, ratios
from regroup_confirmed_duplicates import merged_groups


PAPER = Path(__file__).resolve().parents[1]
BASE = PAPER / "results/full_verification_20261005"
OUT = PAPER / "results/defensibility_20261006"


def write_json(path, content):
    path.write_text(json.dumps(content, indent=2, allow_nan=False) + "\n")


def threshold_curve(y, score):
    """All distinct strict-greater-than decisions, including both constant rules."""
    y, score = np.asarray(y, dtype=int), np.asarray(score, dtype=float)
    assert set(y) == {0, 1} and np.isfinite(score).all()
    order = np.argsort(-score, kind="stable")
    ordered, target = score[order], y[order]
    starts = np.r_[0, np.flatnonzero(np.diff(ordered) != 0) + 1]
    cumulative = np.r_[0, np.cumsum(target)]
    indices = np.r_[starts, len(y)]
    tp, fp = cumulative[indices], indices-cumulative[indices]
    positive, negative = y.sum(), len(y)-y.sum()
    thresholds = np.r_[ordered[starts], np.nextafter(ordered[-1], -np.inf)]
    return pd.DataFrame({"threshold": thresholds, "tpr": tp/positive, "fpr": fp/negative,
                         "accuracy": (tp+negative-fp)/len(y),
                         "balanced_accuracy": .5*(tp/positive + 1-fp/negative)})


def choose_threshold(y, score, mode):
    if mode == "default":
        return .5
    if mode in ("fpr_01", "fpr_05"):
        target = .01 if mode == "fpr_01" else .05
        return float(np.quantile(np.asarray(score)[np.asarray(y) == 0], 1-target, method="higher"))
    curve = threshold_curve(y, score)
    if mode != "best_balanced_accuracy":
        raise ValueError(mode)
    return float(curve.loc[curve.balanced_accuracy.idxmax(), "threshold"])


def score_metrics(y, p, threshold=.5):
    cm = confusion_matrix(y, np.asarray(p) > threshold, labels=[0, 1])
    values = ratios(cm.ravel())
    return {"texts": len(y), "confusion_matrix": cm.tolist(),
            **{name: float(value) if np.isfinite(value) else None for name, value in zip(METRICS, values)},
            "roc_auc": float(roc_auc_score(y, p)), "average_precision": float(average_precision_score(y, p))}


def load_predictions(path, frame):
    pred = pd.read_csv(path)
    assert not pred.duplicated(["pair_id", "label"]).any()
    joined = frame[["pair_id", "label"]].merge(pred, on=["pair_id", "label"], how="left", validate="one_to_one", sort=False)
    assert joined.probability.notna().all() and len(joined) == len(frame)
    return joined.probability.to_numpy()


def external_groups(frame):
    path = OUT / "external_groups.csv"
    if path.exists():
        return pd.read_csv(path).set_index("pair_id").group_id.to_dict()
    raw = pd.read_csv(BASE / "external/research_abstracts-final.csv", keep_default_na=False)
    texts = [raw.iloc[int(r.pair_id.split(":")[1])]["real_abstract" if r.label == 0 else "generated_abstract"]
             for r in frame.itertuples(index=False)]
    lsh = MinHashLSH(threshold=.8, num_perm=128)
    matches = []
    with ProcessPoolExecutor(max_workers=4) as executor:
        for i, (values, count) in enumerate(executor.map(signature, texts, chunksize=100)):
            if not count:
                continue
            mh = MinHash(num_perm=128, seed=42, hashvalues=values)
            candidates = lsh.query(mh)
            if candidates:
                left = shingles(texts[i])
                for j in candidates:
                    right = shingles(texts[j])
                    overlap = len(left & right) / len(left | right)
                    if overlap >= .85:
                        matches.append({"left_id": frame.iloc[i].pair_id, "right_id": frame.iloc[j].pair_id,
                                        "left_label": int(frame.iloc[i].label), "right_label": int(frame.iloc[j].label),
                                        "jaccard": overlap})
            lsh.insert(i, mh)
    links = pd.DataFrame(matches, columns=["left_id", "right_id", "left_label", "right_label", "jaccard"])
    links.to_csv(OUT / "external_near_duplicates.csv", index=False)
    groups = merged_groups(frame, links)
    pd.DataFrame({"pair_id": list(groups), "group_id": list(groups.values())}).to_csv(path, index=False)
    write_json(OUT / "external_group_audit.json", {"pairs": len(groups), "groups": len(set(groups.values())),
               "confirmed_links": len(links), "candidate_search": "MinHash 128, seed 42, LSH 0.8; exact Jaccard >= 0.85",
               "exhaustive": False, "labels_and_scores_unchanged": True})
    return groups


def bootstrap_external(frame, probabilities):
    y = frame.label.to_numpy()
    codes, groups = pd.factorize(frame.group_id, sort=True)
    rng = np.random.default_rng(42)
    draws = {name: [] for name in probabilities}
    auc_draws = {name: [] for name in probabilities}
    for _ in range(1000):
        counts = np.bincount(rng.integers(0, len(groups), len(groups)), minlength=len(groups))
        weights = counts[codes]
        for name, p in probabilities.items():
            cm = confusion_matrix(y, p > .5, labels=[0, 1], sample_weight=weights).ravel()
            draws[name].append(ratios(cm))
            auc_draws[name].append(roc_auc_score(y, p, sample_weight=weights))
    intervals = {}
    for name in probabilities:
        samples = np.c_[np.asarray(draws[name]), auc_draws[name]]
        lower, upper = np.nanquantile(samples, [.025, .975], axis=0)
        intervals[name] = {metric: [float(lo), float(hi)] for metric, lo, hi in zip(METRICS + ["roc_auc"], lower, upper)}
    comparisons = {}
    for metric, col in (("accuracy", 0), ("recall", 2), ("false_positive_rate", 4)):
        diff = (np.asarray(draws["logistic"] )[:, col] - np.asarray(draws["forest"])[:, col]) * 100
        point = (score_metrics(y, probabilities["logistic"])[metric] - score_metrics(y, probabilities["forest"])[metric]) * 100
        comparisons[metric + "_difference_pp"] = {"estimate": point, "ci": np.quantile(diff, [.025, .975]).tolist()}
    diff_auc = np.asarray(auc_draws["logistic"]) - np.asarray(auc_draws["forest"])
    comparisons["roc_auc_difference"] = {"estimate": float(roc_auc_score(y, probabilities["logistic"])-roc_auc_score(y, probabilities["forest"])),
                                          "ci": np.quantile(diff_auc, [.025, .975]).tolist()}
    return {"model_intervals": intervals, "logistic_minus_forest": comparisons,
            "resamples": 1000, "unit": "external source group", "conditional_on_fixed_scores": True}


def refit(train, test, seed, kind, name):
    model = (RandomForestClassifier(n_estimators=100, random_state=seed, n_jobs=8) if kind == "forest"
             else make_pipeline(StandardScaler(), LogisticRegression(max_iter=1000, random_state=42)))
    with threadpool_limits(limits=1):
        model.fit(train[FEATURES].to_numpy(), train.label.to_numpy())
        p = model.predict_proba(test[FEATURES].to_numpy())[:, 1]
    pred = test[["pair_id", "group_id", "label"]].copy()
    pred["probability"] = p
    pred["prediction"] = (p > .5).astype(int)
    pred.to_csv(OUT / f"predictions_{name}.csv.gz", index=False, compression={"method": "gzip", "mtime": 0})
    return {"name": name, "training_texts": len(train), "seed": seed, **score_metrics(test.label.to_numpy(), p)}, p


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    if (OUT / "diagnostics.json").exists():
        raise ValueError("Completed diagnostics exist; do not replace post hoc results")
    archive = OUT / "previous_draft"
    if not archive.exists():
        archive.mkdir()
        for filename in ("linguistic_markers_paper.md", "linguistic_markers_paper.pdf", "RESEARCH_STATUS.md"):
            shutil.copy2(PAPER / filename, archive / filename)
    source = pd.read_csv(BASE / "revision4/features.csv.gz")
    external = pd.read_csv(BASE / "external/features.csv.gz")
    group_map = external_groups(external)
    external.group_id = external.pair_id.map(group_map)
    source_scores, external_scores = {}, {}
    for name, artifact in (("forest", "forest_eight"), ("logistic", "logistic_eight"), ("length", "forest_length")):
        source_scores[name] = load_predictions(BASE / f"revision4/predictions_{artifact}.csv.gz", source)
        external_scores[name] = load_predictions(BASE / f"external/predictions_{artifact}_external.csv.gz", external)
    thresholds, oracles, roc_points = [], [], []
    for name in ("forest", "logistic", "length"):
        for rule in ("default", "best_balanced_accuracy", "fpr_01", "fpr_05"):
            t = choose_threshold(source.label.to_numpy(), source_scores[name], rule)
            thresholds.append({"model": name, "rule": rule, "threshold": t,
                               "source": score_metrics(source.label.to_numpy(), source_scores[name], t),
                               "external": score_metrics(external.label.to_numpy(), external_scores[name], t)})
        curve = threshold_curve(external.label.to_numpy(), external_scores[name])
        best = curve.loc[curve.balanced_accuracy.idxmax()]
        oracles.append({"model": name, **best.to_dict(), "uses_external_labels": True, "deployment_estimate": False})
        for limit in (.01, .05):
            selected = curve[curve.fpr <= limit]
            point = selected.loc[selected.tpr.idxmax()]
            roc_points.append({"model": name, "fpr_limit": limit, **point.to_dict(), "uses_external_labels": True})
    paired = bootstrap_external(external, {name: external_scores[name] for name in ("forest", "logistic")})
    internal_delta = pd.DataFrame({"group": source.group_id,
                                  "delta": ((source_scores["logistic"] > .5) == source.label).astype(int)
                                  - ((source_scores["forest"] > .5) == source.label).astype(int)})
    grouped = internal_delta.groupby("group").delta
    internal_boot = cluster_bootstrap(grouped.sum().to_numpy()[:, None], grouped.size().to_numpy()).ravel()*100
    paired["internal_logistic_minus_forest_accuracy_pp"] = {
        "estimate": float(internal_delta.delta.mean()*100), "ci": np.quantile(internal_boot, [.025, .975]).tolist()}
    subsets = []
    for low, high in ((150, 250), (100, 500)):
        for name, frame, scores in (("local", source, source_scores), ("external", external, external_scores)):
            counts = frame.groupby("pair_id").word_count.agg(["min", "max"])
            ids = counts.index[(counts["min"] >= low) & (counts["max"] <= high)]
            mask = frame.pair_id.isin(ids).to_numpy()
            for model_name in ("forest", "logistic", "length"):
                subsets.append({"corpus": name, "minimum_words": low, "maximum_words": high,
                                "pairs": len(ids), "model": model_name,
                                **score_metrics(frame.label.to_numpy()[mask], scores[model_name][mask])})
    repetitions = []
    for seed in (7, 42, 2026):
        result, p = refit(source, external, seed, "forest", f"forest_seed_{seed}")
        if seed == 42:
            difference = float(np.max(np.abs(p-external_scores["forest"])))
            assert difference < 1e-12, difference
            result["maximum_difference_from_frozen_scores"] = difference
        repetitions.append(result)
        print(f"Seed {seed}: accuracy={result['accuracy']:.4f}, recall={result['recall']:.4f}", flush=True)
    strict = pd.read_csv(BASE / "source_consistency_final/features.csv.gz")
    clean_training = []
    for kind in ("forest", "logistic"):
        result, _ = refit(strict, external, 42, kind, kind + "_source_consistent_training")
        clean_training.append(result)
        print(f"Source-consistent {kind}: accuracy={result['accuracy']:.4f}, recall={result['recall']:.4f}", flush=True)
    result = {"completed_utc": datetime.now(timezone.utc).isoformat(), "post_hoc": True,
              "source_thresholds": thresholds, "external_test_label_oracles": oracles,
              "external_empirical_roc_points": roc_points, "paired_bootstrap": paired,
              "length_restrictions": subsets, "forest_seed_checks": repetitions,
              "source_consistent_training": clean_training,
              "external_group_count": len(set(group_map.values())),
              "hashes": {"code": sha256(Path(__file__)), "protocol": sha256(PAPER / "defensibility_protocol.md"),
                         "source_features": sha256(BASE / "revision4/features.csv.gz"),
                         "external_features": sha256(BASE / "external/features.csv.gz"),
                         "source_consistent_features": sha256(BASE / "source_consistency_final/features.csv.gz")},
              "packages": {name: importlib.metadata.version(name) for name in ("numpy", "pandas", "scikit-learn", "datasketch")}}
    write_json(OUT / "diagnostics.json", result)
    print(json.dumps({"oracles": oracles, "roc_points": roc_points, "paired": paired,
                      "length_restrictions": subsets}, indent=2))


if __name__ == "__main__":
    main()

"""Frozen-model transfer test on the revision-pinned independent abstract corpus."""

import argparse
import json
from concurrent.futures import ProcessPoolExecutor
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
from corrected_analysis import (FEATURES, LENGTHS, METRICS, cluster_bootstrap, extract_pair,
                                group_pairs, init_worker, normalize, ratios, text_hash)


PAPER = Path(__file__).resolve().parents[1]
FOLLOWUP = PAPER / "results/full_verification_20261005"
EXTERNAL = FOLLOWUP / "external"


def prepare(archive, workers):
    output = EXTERNAL / "features.csv.gz"
    if output.exists():
        return pd.read_csv(output)
    external = pd.read_csv(EXTERNAL / "research_abstracts-final.csv", keep_default_na=False)
    local_path = PAPER / "data/metadata/synthetic_abstracts_openai.csv"
    local = pd.read_csv(local_path, keep_default_na=False)
    local_texts = local.human_abstract.tolist() + local.ai_abstract.tolist()
    local_titles = set(local.title.map(normalize))
    local_hashes = {text_hash(text) for text in local_texts}
    manifest = json.loads((FOLLOWUP / "minhash_manifest.json").read_text())
    assert sha256(local_path) == manifest["input_sha256"]
    assert sha256(FOLLOWUP / "local_minhash_signatures.npz") == manifest["signature_sha256"]
    with np.load(FOLLOWUP / "local_minhash_signatures.npz", allow_pickle=False) as saved:
        signatures, counts = saved["signatures"], saved["shingle_counts"]
    lsh = MinHashLSH(threshold=.8, num_perm=128)
    for i, values in enumerate(signatures):
        if counts[i] > 0:
            lsh.insert(i, MinHash(num_perm=128, seed=42, hashvalues=values))
    rows, exclusions, seen_human, seen_ai = [], [], set(), set()
    for i, row in enumerate(external.itertuples(index=False)):
        oid = f"external:{i:05d}"
        texts = [row.real_abstract, row.generated_abstract]
        hashes = [text_hash(text) for text in texts]
        reason = None
        if not row.title.strip() or any(not text.strip() for text in texts):
            reason = "missing_text_or_title"
        elif normalize(row.title) in local_titles:
            reason = "title_overlap_with_original_local_collection"
        elif any(h in local_hashes for h in hashes):
            reason = "normalized_text_overlap_with_original_local_collection"
        elif hashes[0] == hashes[1]:
            reason = "identical_texts_within_external_pair"
        elif hashes[0] in seen_human or hashes[1] in seen_ai:
            reason = "normalized_duplicate_in_external_collection"
        if not reason:
            for text in texts:
                values, count = signature(text)
                if count == 0:
                    continue
                candidates = lsh.query(MinHash(num_perm=128, seed=42, hashvalues=values))
                if candidates:
                    external_shingles = shingles(text)
                    for j in candidates:
                        local_shingles = shingles(local_texts[j])
                        score = len(external_shingles & local_shingles) / len(external_shingles | local_shingles)
                        if score >= .85:
                            reason = "confirmed_near_overlap_with_original_local_collection"
                            break
                if reason:
                    break
        if reason:
            exclusions.append({"pair_id": oid, "reason": reason})
        else:
            seen_human.add(hashes[0])
            seen_ai.add(hashes[1])
            rows.append({"openalex_id": oid, "title": row.title, "human_abstract": texts[0],
                         "ai_abstract": texts[1], "human_hash": hashes[0], "ai_hash": hashes[1]})
        if (i+1) % 2000 == 0:
            print(f"External overlap checks: {i+1:,}/{len(external):,}", flush=True)
    pairs = pd.DataFrame(rows)
    pairs["group_id"] = group_pairs(pairs)
    # Remove cross-class exact copies across different external pairs as well.
    shared = set(pairs.human_hash) & set(pairs.ai_hash)
    conflict = pairs.human_hash.isin(shared) | pairs.ai_hash.isin(shared)
    exclusions.extend({"pair_id": oid, "reason": "cross_class_copy_in_external_collection"}
                      for oid in pairs.loc[conflict, "openalex_id"])
    pairs = pairs.loc[~conflict].copy()
    meta = pairs.set_index("openalex_id")
    tasks = list(pairs[["openalex_id", "human_abstract", "ai_abstract"]].itertuples(index=False, name=None))
    features = []
    with ProcessPoolExecutor(max_workers=workers, initializer=init_worker, initargs=(str(archive),)) as executor:
        for oid, h, a, error in executor.map(extract_pair, tasks, chunksize=100):
            if error:
                exclusions.append({"pair_id": oid, "reason": "feature_failure", "detail": error})
            elif min(h["word_count"], a["word_count"]) < 100:
                exclusions.append({"pair_id": oid, "reason": "under_100_words"})
            elif min(h["sentence_count"], a["sentence_count"]) < 2:
                exclusions.append({"pair_id": oid, "reason": "fewer_than_two_sentences"})
            else:
                for label, feats in ((0, h), (1, a)):
                    features.append({"pair_id": oid, "group_id": meta.loc[oid, "group_id"],
                                     "label": label, "text_hash": meta.loc[oid, "human_hash" if label == 0 else "ai_hash"],
                                     **feats})
    frame = pd.DataFrame(features)
    assert len(frame) // 2 + len(exclusions) == len(external)
    assert set(frame.text_hash).isdisjoint(local_hashes)
    frame.to_csv(output, index=False, compression={"method": "gzip", "mtime": 0})
    pd.DataFrame(exclusions).to_csv(EXTERNAL / "exclusions.csv", index=False)
    (EXTERNAL / "eligibility.json").write_text(json.dumps({
        "input_pairs": len(external), "included_pairs": len(frame) // 2, "included_texts": len(frame),
        "groups": int(frame.group_id.nunique()), "exclusion_counts": pd.Series([e["reason"] for e in exclusions]).value_counts().to_dict(),
        "features_sha256": sha256(output), "original_local_input_sha256": sha256(local_path),
        "external_input_sha256": sha256(EXTERNAL / "research_abstracts-final.csv"),
        "near_overlap_rule": "MinHash 128 permutations, seed 42, LSH 0.8, exact word-five-gram Jaccard at least 0.85",
        "limits": "Candidate near-overlap search is not exhaustive. External source labels and model configuration come from the dataset author."
    }, indent=2) + "\n")
    return frame


def score_model(train, test, columns, kind, name):
    model = (make_pipeline(StandardScaler(), LogisticRegression(max_iter=1000, random_state=42))
             if kind == "logistic" else RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=8))
    with threadpool_limits(limits=1):
        model.fit(train[columns].to_numpy(), train.label.to_numpy())
        p = model.predict_proba(test[columns].to_numpy())[:, 1]
    y = test.label.to_numpy()
    predicted = (p > .5).astype(int)
    cm = confusion_matrix(y, predicted, labels=[0, 1])
    per_group = np.zeros((test.group_id.nunique(), 4))
    np.add.at(per_group, (pd.factorize(test.group_id, sort=True)[0], y*2+predicted), 1)
    boot = cluster_bootstrap(per_group, np.ones(len(per_group)))
    low, high = np.nanquantile(ratios(boot), [.025, .975], axis=0)
    result = {"name": name, "features": columns, "training_texts": len(train), "test_texts": len(test),
              "confusion_matrix": cm.tolist(), **dict(zip(METRICS, ratios(cm.ravel()))),
              "roc_auc": roc_auc_score(y, p), "average_precision": average_precision_score(y, p),
              "conditional_group_bootstrap_95ci": {key: [float(lo), float(hi)] for key, lo, hi in zip(METRICS, low, high)}}
    predictions = test[["pair_id", "group_id", "label"]].copy()
    predictions["probability"] = p
    predictions["prediction"] = predicted
    predictions.to_csv(EXTERNAL / f"predictions_{name}.csv.gz", index=False, compression={"method": "gzip", "mtime": 0})
    print(json.dumps(result, indent=2), flush=True)
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--punkt-archive", type=Path, required=True)
    parser.add_argument("--workers", type=int, default=4)
    parser.add_argument("--prepare-only", action="store_true")
    args = parser.parse_args()
    if (EXTERNAL / "evaluation.json").exists():
        raise ValueError("External test already scored; do not overwrite or retune")
    test = prepare(args.punkt_archive, args.workers)
    if args.prepare_only:
        print((EXTERNAL / "eligibility.json").read_text())
        return
    train_path = FOLLOWUP / "revision3/features.csv.gz"
    train = pd.read_csv(train_path)
    models = [score_model(train, test, columns, kind, name) for name, columns, kind in (
        ("forest_eight_external", FEATURES, "forest"), ("forest_length_external", LENGTHS, "forest"),
        ("logistic_eight_external", FEATURES, "logistic"))]
    result = {"dataset_revision": "07857e2a97571ab553421ed645ef470bef6fa05c",
              "training_features_sha256": sha256(train_path), "external_features_sha256": sha256(EXTERNAL / "features.csv.gz"),
              "code_sha256": sha256(Path(__file__)), "threshold": "Generated if score > 0.5; no external tuning",
              "models": models,
              "scope": "Transfer to one independently assembled public dataset using its author's labels, not authentication of every author or deployment validation"}
    (EXTERNAL / "evaluation.json").write_text(json.dumps(result, indent=2, allow_nan=False) + "\n")


if __name__ == "__main__":
    main()

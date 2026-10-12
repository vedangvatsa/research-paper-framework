"""Preserve measured features and join all confirmed near-duplicate source groups."""

import json
import shutil
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd

from audit_recovered_data import sha256
from corrected_analysis import FEATURES, fold_for_group, validate_splits


PAPER = Path(__file__).resolve().parents[1]
PREVIOUS = PAPER / "results/correction_20261005/revision2"
OUTPUT = PAPER / "results/full_verification_20261005/revision4"


def merged_groups(frame, matches):
    mapping = frame.drop_duplicates("pair_id").set_index("pair_id").group_id.to_dict()
    parent = {group: group for group in mapping.values()}

    def root(key):
        while parent[key] != key:
            parent[key] = parent[parent[key]]
            key = parent[key]
        return key

    for row in matches.itertuples(index=False):
        a, b = root(mapping[row.left_id]), root(mapping[row.right_id])
        parent[max(a, b)] = min(a, b)
    return {pair: root(group) for pair, group in mapping.items()}


def main():
    OUTPUT.mkdir(parents=True, exist_ok=True)
    if (OUTPUT / "features.csv.gz").exists():
        raise ValueError("Final revision already exists")
    previous_draft = PAPER / "results/full_verification_20261005/revision3"
    for name in ("linguistic_markers_paper.md", "linguistic_markers_paper.pdf"):
        target = previous_draft / name
        if not target.exists():
            shutil.copy2(PAPER / name, target)
    frame = pd.read_csv(PREVIOUS / "features.csv.gz")
    manifest = json.loads((PREVIOUS / "manifest.json").read_text())
    assert sha256(PREVIOUS / "features.csv.gz") == manifest["features_sha256"]
    near_path = PAPER / "results/full_verification_20261005/near_duplicates_all_labels.csv"
    matches = pd.read_csv(near_path)
    assert matches.jaccard.ge(.85).all()
    identity_path = PAPER / "results/full_verification_20261005/source_identity_edges.csv"
    identities = pd.read_csv(identity_path)
    all_edges = pd.concat([matches[["left_id", "right_id"]], identities[["left_id", "right_id"]]], ignore_index=True)
    new_groups = merged_groups(frame, all_edges)
    corrected = frame.copy()
    corrected["group_id"] = corrected.pair_id.map(new_groups)
    corrected["fold"] = corrected.group_id.map(fold_for_group)
    validate_splits(corrected)
    fold_map = corrected.drop_duplicates("pair_id").set_index("pair_id").fold.to_dict()
    assert all(fold_map[r.left_id] == fold_map[r.right_id] for r in all_edges.itertuples(index=False))
    assert np.array_equal(frame[FEATURES].to_numpy(), corrected[FEATURES].to_numpy())
    assert np.array_equal(frame.label.to_numpy(), corrected.label.to_numpy())
    corrected.to_csv(OUTPUT / "features.csv.gz", index=False, compression={"method": "gzip", "mtime": 0})
    report = {"previous_groups": int(frame.group_id.nunique()), "new_groups": int(corrected.group_id.nunique()),
              "source_pairs_changing_fold": int(frame.fold.ne(corrected.fold).sum() // 2),
              "near_duplicate_edges": len(matches), "confirmed_edges_crossing_new_folds": 0,
              "source_identity_edges": len(identities), "source_identity_edges_sha256": sha256(identity_path),
              "previous_features_sha256": sha256(PREVIOUS / "features.csv.gz"),
              "near_duplicate_edges_sha256": sha256(near_path), "feature_values_unchanged": True,
              "regrouping_code_sha256": sha256(Path(__file__))}
    manifest.update({"created_utc": datetime.now(timezone.utc).isoformat(),
                     "groups": report["new_groups"], "features_sha256": sha256(OUTPUT / "features.csv.gz"),
                     "regrouping": report,
                     "fold_text_counts": {str(k): int(v) for k, v in corrected.fold.value_counts().sort_index().items()}})
    manifest["known_limits"] = ["No per-output generation logs", "Sampling probabilities not recovered",
                                "Current-index audit is not independent publisher authentication",
                                "MinHash near-duplicate candidate search is not exhaustive",
                                "Author background and authorship labels are not independently verified"]
    (OUTPUT / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    (OUTPUT / "regrouping.json").write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()

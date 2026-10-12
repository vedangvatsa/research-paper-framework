"""Independently check saved predictions, summaries, accounting and manuscript."""

import json
import re
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.metrics import (accuracy_score, average_precision_score, confusion_matrix,
                             f1_score, precision_score, recall_score, roc_auc_score)

from audit_recovered_data import sha256
from corrected_analysis import FEATURES, fold_for_group, validate_splits
from prepare_corrected_results import feature_table, flow_table, model_table


PAPER = Path(__file__).resolve().parents[1]
RESULTS = PAPER / "results/full_verification_20261005/revision4"


def main():
    manifest = json.loads((RESULTS / "manifest.json").read_text())
    evaluation = json.loads((RESULTS / "evaluation.json").read_text())
    audit = json.loads((PAPER / "results/correction_20261005/source_audit_v2.json").read_text())
    for record in audit["inputs"]:
        assert sha256(PAPER / record["path"]) == record["sha256"], record["path"]
    assert sha256(RESULTS / "features.csv.gz") == manifest["features_sha256"]
    assert sha256(PAPER / "scripts/corrected_analysis.py") == evaluation["analysis_code_sha256"]
    frame = pd.read_csv(RESULTS / "features.csv.gz")
    excluded = pd.read_csv(RESULTS / "exclusions.csv")
    assert excluded.pair_id.is_unique
    assert not set(excluded.pair_id) & set(frame.pair_id)
    assert len(frame) == manifest["included_texts"] == 2 * manifest["included_pairs"]
    assert len(excluded) + manifest["included_pairs"] == manifest["input_pairs"]
    assert sum(s["removed_pairs"] for s in manifest["exclusion_stages"]) == len(excluded)
    assert np.isfinite(frame[FEATURES].to_numpy()).all()
    assert frame.word_count.min() >= 100 and frame.sentence_count.min() >= 2
    assert frame.lexical_diversity_mtld.min() > 0
    validate_splits(frame)
    assert frame.fold.eq(frame.group_id.map(fold_for_group)).all()
    near = pd.read_csv(RESULTS.parent / "near_duplicates_all_labels.csv")
    fold_map = frame.drop_duplicates("pair_id").set_index("pair_id").fold.to_dict()
    assert all(fold_map[r.left_id] == fold_map[r.right_id] for r in near.itertuples(index=False))
    identities = pd.read_csv(RESULTS.parent / "source_identity_edges.csv")
    assert all(fold_map[r.left_id] == fold_map[r.right_id] for r in identities.itertuples(index=False))

    statistics = pd.read_csv(RESULTS / "feature_comparisons.csv")
    h = frame[frame.label == 0].set_index("pair_id").sort_index()
    a = frame[frame.label == 1].set_index("pair_id").sort_index()
    for row in statistics.to_dict("records"):
        feature = row["feature"]
        for key, value in {"human_mean": h[feature].mean(), "ai_mean": a[feature].mean(),
                           "human_sd": h[feature].std(ddof=1), "ai_sd": a[feature].std(ddof=1),
                           "paired_mean_difference": (a[feature]-h[feature]).mean()}.items():
            assert np.isclose(row[key], value, rtol=0, atol=1e-10), (feature, key)

    keys = ["pair_id", "label"]
    for model in evaluation["models"]:
        name = model["name"]
        predictions = pd.read_csv(RESULTS / f"predictions_{name}.csv.gz", float_precision="round_trip")
        assert not predictions.duplicated(keys).any()
        joined = predictions.merge(frame[keys + ["fold", "group_id", "word_count"]], on=keys,
                                   validate="one_to_one", how="left", suffixes=("", "_source"))
        assert joined.fold.eq(joined.fold_source).all()
        assert joined.group_id.eq(joined.group_id_source).all()
        assert len(joined) == model["texts"]
        if name == "forest_common_length":
            counts = frame.groupby("pair_id").word_count.agg(["min", "max"])
            eligible = set(counts.index[(counts["min"] >= 150) & (counts["max"] <= 250)])
            assert set(joined.pair_id) == eligible
            assert joined.word_count.between(150, 250).all()
        else:
            assert len(joined) == len(frame)
        y, p, predicted = joined.label, joined.probability, joined.prediction
        assert np.isfinite(p).all() and p.between(0, 1).all()
        assert np.array_equal(predicted, (p > .5).astype(int))
        cm = confusion_matrix(y, predicted, labels=[0, 1])
        assert cm.tolist() == model["confusion_matrix"]
        values = {"accuracy": accuracy_score(y, predicted), "precision": precision_score(y, predicted),
                  "recall": recall_score(y, predicted), "f1": f1_score(y, predicted),
                  "roc_auc": roc_auc_score(y, p), "average_precision": average_precision_score(y, p),
                  "false_positive_rate": cm[0, 1]/cm[0].sum(), "specificity": cm[0, 0]/cm[0].sum()}
        for key, value in values.items():
            assert np.isclose(model[key], value, rtol=0, atol=1e-12), (name, key)
        print(f"Verified {name}: {len(joined):,} predictions, accuracy {values['accuracy']:.8f}")

    manuscript = (PAPER / "linguistic_markers_paper.md").read_text()
    assert flow_table(manifest) in manuscript
    assert feature_table(statistics) in manuscript
    assert model_table(evaluation["models"]) in manuscript
    main_model = next(m for m in evaluation["models"] if m["name"] == "forest_eight")
    for metric in ("precision", "recall"):
        assert f"{metric} is {100*main_model[metric]:.2f}%" in manuscript
    assert f"F1 is {main_model['f1']:.4f}" in manuscript
    assert f"average precision is {main_model['average_precision']:.4f}" in manuscript
    assert f"contains {manifest['groups']:,} groups" in manuscript
    tn, fp, fn, tp = np.array(main_model["confusion_matrix"]).ravel()
    assert f"{tn:,} published texts and {tp:,} generated texts" in manuscript
    assert f"{fp:,} published texts as generated and misses {fn:,}" in manuscript
    assert f"about {100*main_model['recall']:.0f} generated texts and {9900*main_model['false_positive_rate']:.0f} published texts" in manuscript
    body, references = manuscript.split("## 8. References", 1)
    cited = {int(n) for group in re.findall(r"\[(\d+(?:,\s*\d+)*)\]", body) for n in re.findall(r"\d+", group)}
    listed = {int(n) for n in re.findall(r"^\[(\d+)\]", references, re.M)}
    assert cited == listed == set(range(1, 16))
    assert len(re.findall(r"https://[^)]+", references)) == len(listed)
    images = re.findall(r"!\[[^\]]*\]\(([^)]+)\)", manuscript)
    assert len(images) == 4 and all((PAPER / image).is_file() for image in images)
    abstract = body.split("## Abstract", 1)[1].split("_**Keywords**_", 1)[0]
    assert len(abstract.split()) <= 250
    for value in ("74,513", "149,026", "95.99%", "0.9916", "3.60%", "90.38%", "53.89%", "11.73%", "68.91%"):
        assert value in abstract, value
    assert not any(value in manuscript for value in ("95.69%", "October 2024", "2403.19074", "CBO9781139524599"))

    report = {"input_hashes_unchanged": True, "included_pairs": manifest["included_pairs"],
              "excluded_pairs": len(excluded), "source_groups_disjoint": True,
              "confirmed_near_duplicate_edges_checked": len(near),
              "models_verified": len(evaluation["models"]), "manuscript_tables_match": True,
              "references_cited_and_linked": len(listed), "figure_files_present": len(images),
              "abstract_words": len(abstract.split())}
    (RESULTS / "verification.json").write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()

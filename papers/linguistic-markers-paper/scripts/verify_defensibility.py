"""Independently verify diagnostic claims from the retained scores and labels."""

import json
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.metrics import (accuracy_score, average_precision_score, confusion_matrix,
                             precision_score, recall_score, roc_auc_score, roc_curve)

from audit_recovered_data import sha256
from prepare_defensibility_results import paired_table, sensitivity_table, threshold_table


PAPER = Path(__file__).resolve().parents[1]
BASE = PAPER / "results/full_verification_20261005"
OUT = PAPER / "results/defensibility_20261006"


def metrics(y, score, threshold):
    prediction = score > threshold
    cm = confusion_matrix(y, prediction, labels=[0, 1])
    return {"accuracy": accuracy_score(y, prediction), "recall": recall_score(y, prediction),
            "precision": precision_score(y, prediction, zero_division=0),
            "false_positive_rate": cm[0, 1]/cm[0].sum(), "roc_auc": roc_auc_score(y, score),
            "average_precision": average_precision_score(y, score), "cm": cm.tolist()}


def assert_metrics(expected, actual):
    for key in ("accuracy", "recall", "false_positive_rate", "roc_auc", "average_precision"):
        assert np.isclose(expected[key], actual[key], rtol=0, atol=1e-11), key
    assert expected["confusion_matrix"] == actual["cm"]


def main():
    data = json.loads((OUT / "diagnostics.json").read_text())
    assert data["post_hoc"] is True
    for key, path in (("code", PAPER / "scripts/defensibility_checks.py"),
                      ("protocol", PAPER / "defensibility_protocol.md"),
                      ("source_features", BASE / "revision4/features.csv.gz"),
                      ("external_features", BASE / "external/features.csv.gz"),
                      ("source_consistent_features", BASE / "source_consistency_final/features.csv.gz")):
        assert data["hashes"][key] == sha256(path), key
    source = pd.read_csv(BASE / "revision4/features.csv.gz")
    external = pd.read_csv(BASE / "external/features.csv.gz")
    model_names = {"forest": "forest_eight", "logistic": "logistic_eight", "length": "forest_length"}
    scores = {}
    for corpus, frame in (("local", source), ("external", external)):
        for short, name in model_names.items():
            path = BASE / (f"revision4/predictions_{name}.csv.gz" if corpus == "local" else f"external/predictions_{name}_external.csv.gz")
            pred = pd.read_csv(path)
            joined = frame[["pair_id", "label"]].merge(pred, on=["pair_id", "label"], validate="one_to_one", how="left")
            assert joined.probability.notna().all()
            scores[corpus, short] = joined.probability.to_numpy()
    for row in data["source_thresholds"]:
        for corpus, frame, label in (("local", source, "source"), ("external", external, "external")):
            assert_metrics(row[label], metrics(frame.label.to_numpy(), scores[corpus, row["model"]], row["threshold"]))
        if row["rule"] == "fpr_01":
            assert row["source"]["false_positive_rate"] <= .01
        if row["rule"] == "fpr_05":
            assert row["source"]["false_positive_rate"] <= .05
        if row["rule"] == "best_balanced_accuracy":
            fpr, tpr, _ = roc_curve(source.label, scores["local", row["model"]], drop_intermediate=False)
            assert np.isclose(row["source"]["accuracy"], np.max((1-fpr+tpr)/2), rtol=0, atol=1e-12)
    for row in data["external_test_label_oracles"]:
        fpr, tpr, _ = roc_curve(external.label, scores["external", row["model"]], drop_intermediate=False)
        assert np.isclose(row["balanced_accuracy"], np.max((1-fpr+tpr)/2), rtol=0, atol=1e-12)
        direct = metrics(external.label.to_numpy(), scores["external", row["model"]], row["threshold"])
        assert np.isclose(row["accuracy"], direct["accuracy"], rtol=0, atol=1e-12)
        assert row["uses_external_labels"] and not row["deployment_estimate"]
    for row in data["external_empirical_roc_points"]:
        fpr, tpr, _ = roc_curve(external.label, scores["external", row["model"]], drop_intermediate=False)
        assert np.isclose(row["tpr"], tpr[fpr <= row["fpr_limit"]].max(), rtol=0, atol=1e-12)
    for row in data["length_restrictions"]:
        frame = source if row["corpus"] == "local" else external
        lengths = frame.groupby("pair_id").word_count.agg(["min", "max"])
        ids = lengths.index[(lengths["min"] >= row["minimum_words"]) & (lengths["max"] <= row["maximum_words"])]
        mask = frame.pair_id.isin(ids).to_numpy()
        assert len(ids) == row["pairs"]
        assert_metrics(row, metrics(frame.label.to_numpy()[mask], scores[row["corpus"], row["model"]][mask], .5))
    for row in data["forest_seed_checks"] + data["source_consistent_training"]:
        pred = pd.read_csv(OUT / f"predictions_{row['name']}.csv.gz")
        assert_metrics(row, metrics(pred.label.to_numpy(), pred.probability.to_numpy(), .5))
    reproduced = pd.read_csv(OUT / "predictions_forest_seed_42.csv.gz")
    assert np.allclose(reproduced.probability.to_numpy(), scores["external", "forest"], rtol=0, atol=1e-12)
    groups = pd.read_csv(OUT / "external_groups.csv").set_index("pair_id").group_id.to_dict()
    edges = pd.read_csv(OUT / "external_near_duplicates.csv")
    assert all(groups[r.left_id] == groups[r.right_id] for r in edges.itertuples(index=False))
    assert len(set(groups.values())) == data["external_group_count"]
    paired = data["paired_bootstrap"]["logistic_minus_forest"]
    rf = metrics(external.label.to_numpy(), scores["external", "forest"], .5)
    lr = metrics(external.label.to_numpy(), scores["external", "logistic"], .5)
    for key, name, factor in (("accuracy_difference_pp", "accuracy", 100), ("recall_difference_pp", "recall", 100),
                              ("false_positive_rate_difference_pp", "false_positive_rate", 100), ("roc_auc_difference", "roc_auc", 1)):
        assert np.isclose(paired[key]["estimate"], factor*(lr[name]-rf[name]), rtol=0, atol=1e-12)
    same = json.loads((OUT / "same_model/evaluation.json").read_text())
    assert same["hashes"]["code"] == sha256(PAPER / "scripts/same_model_transfer.py")
    assert same["hashes"]["protocol"] == sha256(PAPER / "same_model_protocol.md")
    for row in same["rows"]:
        pred = pd.read_csv(OUT / f"same_model/predictions_fold_{row['fold']}.csv.gz")
        assert_metrics(row["external"], metrics(pred.label.to_numpy(), pred.probability.to_numpy(), .5))
        mask = source.fold.eq(row["fold"]).to_numpy()
        assert_metrics(row["source"], metrics(source.label.to_numpy()[mask], scores["local", "forest"][mask], .5))
        assert row["maximum_source_reproduction_difference"] < 1e-12
    manuscript = (PAPER / "linguistic_markers_paper.md").read_text()
    for table in (threshold_table(data), sensitivity_table(data), paired_table(data)):
        assert table in manuscript
    report = {"source_threshold_conditions_verified": len(data["source_thresholds"]),
              "test_label_oracles_verified_with_independent_roc": 3, "length_conditions_verified": len(data["length_restrictions"]),
              "new_fit_prediction_sets_verified": 5, "seed_42_frozen_scores_reproduced": True,
              "external_groups": len(set(groups.values())), "external_confirmed_links": len(edges),
              "paired_point_differences_verified": True, "diagnostic_tables_match_manuscript": True}
    report["same_fitted_model_comparisons_verified"] = len(same["rows"])
    (OUT / "verification.json").write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()

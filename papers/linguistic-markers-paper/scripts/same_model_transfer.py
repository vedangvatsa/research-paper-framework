"""Compare source and external outcomes for each identical fitted fold model."""

import json
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from threadpoolctl import threadpool_limits

from audit_recovered_data import sha256
from corrected_analysis import FEATURES
from defensibility_checks import load_predictions, score_metrics


PAPER = Path(__file__).resolve().parents[1]
BASE = PAPER / "results/full_verification_20261005"
OUT = PAPER / "results/defensibility_20261006/same_model"


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    if (OUT / "evaluation.json").exists():
        raise ValueError("Completed same-model check exists")
    source = pd.read_csv(BASE / "revision4/features.csv.gz")
    external = pd.read_csv(BASE / "external/features.csv.gz")
    saved = load_predictions(BASE / "revision4/predictions_forest_eight.csv.gz", source)
    rows = []
    for fold in range(5):
        train, test = source.fold.ne(fold).to_numpy(), source.fold.eq(fold).to_numpy()
        forest = RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=8)
        with threadpool_limits(limits=1):
            forest.fit(source.loc[train, FEATURES].to_numpy(), source.loc[train, "label"].to_numpy())
            source_p = forest.predict_proba(source.loc[test, FEATURES].to_numpy())[:, 1]
            external_p = forest.predict_proba(external[FEATURES].to_numpy())[:, 1]
        maximum_difference = float(np.max(np.abs(source_p-saved[test])))
        assert maximum_difference < 1e-12
        pred = external[["pair_id", "group_id", "label"]].copy()
        pred["probability"] = external_p
        pred["prediction"] = (external_p > .5).astype(int)
        pred.to_csv(OUT / f"predictions_fold_{fold}.csv.gz", index=False, compression={"method": "gzip", "mtime": 0})
        row = {"fold": fold, "training_texts": int(train.sum()), "source_heldout_texts": int(test.sum()),
               "maximum_source_reproduction_difference": maximum_difference,
               "source": score_metrics(source.loc[test, "label"].to_numpy(), source_p),
               "external": score_metrics(external.label.to_numpy(), external_p)}
        rows.append(row)
        print(json.dumps({"fold": fold, "source_accuracy": row["source"]["accuracy"],
                          "external_accuracy": row["external"]["accuracy"],
                          "external_recall": row["external"]["recall"]}), flush=True)
    (OUT / "evaluation.json").write_text(json.dumps({
        "post_hoc": True, "same_fitted_model_for_both_evaluations": True,
        "folds_are_not_independent_replications": True, "threshold": .5, "rows": rows,
        "hashes": {"code": sha256(Path(__file__)), "protocol": sha256(PAPER / "same_model_protocol.md"),
                   "source_features": sha256(BASE / "revision4/features.csv.gz"),
                   "external_features": sha256(BASE / "external/features.csv.gz")}
    }, indent=2) + "\n")


if __name__ == "__main__":
    main()

"""Evaluate frozen models on the prespecified current-source-consistent subset."""

import json
from pathlib import Path

import pandas as pd

from audit_recovered_data import sha256
from corrected_analysis import FEATURES, LENGTHS, evaluate_model, validate_splits


PAPER = Path(__file__).resolve().parents[1]
FOLLOWUP = PAPER / "results/full_verification_20261005"


def main():
    checks = pd.read_csv(FOLLOWUP / "source_checks_resolved.csv.gz", low_memory=False)
    selection = checks.source_consistent.map(lambda value: str(value).lower() == "true")
    allowed = set(checks.loc[selection, "source_id"])
    frame = pd.read_csv(FOLLOWUP / "revision4/features.csv.gz")
    subset = frame[frame.pair_id.isin(allowed)].copy()
    expected = json.loads((FOLLOWUP / "source_summary_resolved.json").read_text())["revision2"]["source_consistent"]
    assert subset.pair_id.nunique() == expected
    validate_splits(subset)
    output = FOLLOWUP / "source_consistency_final"
    output.mkdir(exist_ok=True)
    if (output / "evaluation.json").exists():
        raise ValueError("Refusing to replace completed source sensitivity results")
    subset.to_csv(output / "features.csv.gz", index=False, compression={"method": "gzip", "mtime": 0})
    models = []
    for name, features in (("forest_eight_sourceconsistent", FEATURES), ("forest_length_sourceconsistent", LENGTHS)):
        models.append(evaluate_model(subset, features, "forest", name, 8, output))
    result = {"subset_pairs": subset.pair_id.nunique(), "subset_texts": len(subset),
              "features_sha256": sha256(output / "features.csv.gz"),
              "selection_source_sha256": sha256(FOLLOWUP / "source_checks_resolved.csv.gz"),
              "source_index_snapshot": "5 October 2026", "models": models,
              "interpretation": "Retrospective sensitivity to current-index consistency; not independent publisher authentication"}
    (output / "evaluation.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({"pairs": result["subset_pairs"], "models": [
        {key: m[key] for key in ("name", "accuracy", "roc_auc", "false_positive_rate")} for m in models]}, indent=2))


if __name__ == "__main__":
    main()

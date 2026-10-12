"""Format the additional, explicitly post hoc manuscript results."""

import json
from pathlib import Path


PAPER = Path(__file__).resolve().parents[1]
ROOT = PAPER / "results/defensibility_20261006"


def threshold_table(data):
    labels = {"default": "Fixed default", "best_balanced_accuracy": "Best source balanced accuracy",
              "fpr_01": "Source false positives at most 1%", "fpr_05": "Source false positives at most 5%"}
    lines = ["| Source rule | Threshold | Source FPR | External accuracy | External recall | External FPR |",
             "| --- | ---: | ---: | ---: | ---: | ---: |"]
    for row in data["source_thresholds"]:
        if row["model"] != "forest":
            continue
        ext = row["external"]
        lines.append(f"| {labels[row['rule']]} | {row['threshold']:.2f} | {100*row['source']['false_positive_rate']:.2f}% | {100*ext['accuracy']:.2f}% | {100*ext['recall']:.2f}% | {100*ext['false_positive_rate']:.2f}% |")
    return "\n".join(lines)


def sensitivity_table(data):
    rows = []
    by_seed = {row["seed"]: row for row in data["forest_seed_checks"]}
    for seed in (42, 7, 2026):
        rows.append((f"Full source, seed {seed}", by_seed[seed]["training_texts"]//2, by_seed[seed]))
    clean = next(row for row in data["source_consistent_training"] if row["name"].startswith("forest"))
    rows.append(("Source-consistent training", clean["training_texts"]//2, clean))
    for row in data["length_restrictions"]:
        if row["model"] == "forest" and row["corpus"] == "external":
            rows.append((f"Fixed scores, {row['minimum_words']}-{row['maximum_words']} words", 74513, row))
    lines = ["| Forest check | Training pairs | External pairs | Accuracy | Recall | ROC AUC |",
             "| --- | ---: | ---: | ---: | ---: | ---: |"]
    for name, training, row in rows:
        lines.append(f"| {name} | {training:,} | {row['texts']//2:,} | {100*row['accuracy']:.2f}% | {100*row['recall']:.2f}% | {row['roc_auc']:.4f} |")
    return "\n".join(lines)


def paired_table(data):
    paired = data["paired_bootstrap"]
    rows = [("Internal accuracy (percentage points)", paired["internal_logistic_minus_forest_accuracy_pp"], 2)]
    for label, key, digits in [
        ("External accuracy (percentage points)", "accuracy_difference_pp", 2),
        ("External recall (percentage points)", "recall_difference_pp", 2),
        ("External false-positive rate (percentage points)", "false_positive_rate_difference_pp", 2),
        ("External ROC AUC", "roc_auc_difference", 4),
    ]:
        rows.append((label, paired["logistic_minus_forest"][key], digits))
    lines = ["| Logistic minus forest | Difference | Conditional 95% interval |", "| --- | ---: | ---: |"]
    for label, row, digits in rows:
        lines.append(f"| {label} | {row['estimate']:.{digits}f} | [{row['ci'][0]:.{digits}f}, {row['ci'][1]:.{digits}f}] |")
    return "\n".join(lines)


def main():
    data = json.loads((ROOT / "diagnostics.json").read_text())
    tables = "\n\n".join([threshold_table(data), sensitivity_table(data), paired_table(data)]) + "\n"
    (ROOT / "manuscript_tables.md").write_text(tables)
    print(tables)
    for result in data["source_consistent_training"]:
        print(result["name"], {k: result[k] for k in ("accuracy", "recall", "false_positive_rate", "roc_auc")})


if __name__ == "__main__":
    main()

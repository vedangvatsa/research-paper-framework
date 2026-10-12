"""Generate manuscript tables and figures from the saved corrected run."""

import json
import hashlib
import shutil
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.metrics import precision_recall_curve, roc_curve


PAPER = Path(__file__).resolve().parents[1]
FOLLOWUP = PAPER / "results/full_verification_20261005"
RESULTS = FOLLOWUP / "revision4"
LABELS = {
    "mean_sent_len": "Mean sentence length", "sent_len_cv": "Sentence-length CV",
    "hedge_density": "Hedge matches", "booster_density": "Booster matches",
    "self_mention_density": "Self-mention matches", "connector_density": "Connector matches",
    "lexical_diversity_mtld": "Lexical diversity (MTLD)",
    "first_word_connector_ratio": "Connector opener ratio",
}
MODELS = {"forest_eight": "Forest, eight features", "logistic_eight": "Logistic, eight features",
          "forest_length": "Forest, length only", "forest_mtld": "Forest, MTLD only",
          "forest_sentence_cv": "Forest, sentence CV only", "forest_without_mtld": "Forest, seven without MTLD",
          "forest_common_length": "Forest, common-length subset"}


def flow_table(manifest):
    labels = {"missing_source_title": "Missing source title",
              "documented_title_content_conflict": "Documented title-content conflict",
              "normalized_duplicate": "Normalized duplicate text",
              "under_100_words": "Fewer than 100 words in either text",
              "fewer_than_two_sentences": "Fewer than two sentences in either text"}
    remaining = manifest["input_pairs"]
    lines = ["| Stage | Pairs removed | Pairs remaining |", "| --- | ---: | ---: |",
             f"| Original paired records | 0 | {remaining:,} |"]
    for step in manifest["exclusion_stages"]:
        if not step["removed_pairs"]:
            continue
        remaining -= step["removed_pairs"]
        lines.append(f"| {labels[step['reason']]} | {step['removed_pairs']:,} | {remaining:,} |")
    assert remaining == manifest["included_pairs"]
    return "\n".join(lines)


def model_table(models):
    lines = ["| Model | Texts | Accuracy | ROC AUC | False-positive rate |",
             "| --- | ---: | ---: | ---: | ---: |"]
    for row in models:
        lines.append(f"| {MODELS[row['name']]} | {row['texts']:,} | {100*row['accuracy']:.2f}% | {row['roc_auc']:.4f} | {100*row['false_positive_rate']:.2f}% |")
    return "\n".join(lines)


def feature_table(stats):
    lines = ["| Feature | Published mean (SD) | Generated mean (SD) | Difference, 95% interval |",
             "| --- | ---: | ---: | ---: |"]
    for row in stats.to_dict("records"):
        decimals = 3 if row["feature"] in ("sent_len_cv", "first_word_connector_ratio") else 2
        lines.append(f"| {LABELS[row['feature']]} | {row['human_mean']:.{decimals}f} ({row['human_sd']:.{decimals}f}) | {row['ai_mean']:.{decimals}f} ({row['ai_sd']:.{decimals}f}) | {row['paired_mean_difference']:.{decimals}f} [{row['difference_ci_low']:.{decimals}f}, {row['difference_ci_high']:.{decimals}f}] |")
    return "\n".join(lines)


def source_table(summary):
    labels = [("Current record retrieved", "retrieved"), ("Title agrees after normalization", "title_agrees"),
              ("Publication year agrees", "year_agrees"), ("Abstract agrees after text cleaning", "abstract_exact_clean_match"),
              ("Current language is English", "current_language"), ("Current type is article", "current_type"),
              ("Meets all source-consistency conditions", "source_consistent"), ("Current record unresolved", "unresolved")]
    lines = ["| Check | All 100,000 records | Retained 74,513 records |", "| --- | ---: | ---: |"]
    for label, key in labels:
        values = []
        for scope in ("all", "revision2"):
            item = summary[scope]
            value = (item["status_counts"][key] if key in ("retrieved", "unresolved") else
                     item[key]["en"] if key == "current_language" else
                     item[key]["article"] if key == "current_type" else item[key])
            values.append(f"{value:,}")
        lines.append(f"| {label} | {values[0]} | {values[1]} |")
    return "\n".join(lines)


def external_table(models):
    lines = ["| Model | Accuracy | Generated-text recall | False-positive rate | ROC AUC |",
             "| --- | ---: | ---: | ---: | ---: |"]
    for model in models:
        name = MODELS[model["name"].removesuffix("_external")]
        lines.append(f"| {name} | {100*model['accuracy']:.2f}% | {100*model['recall']:.2f}% | {100*model['false_positive_rate']:.2f}% | {model['roc_auc']:.4f} |")
    return "\n".join(lines)


def main():
    archive = FOLLOWUP / "pre_followup_draft"
    if not (archive / "manifest.json").exists():
        archive.mkdir(exist_ok=True)
        hashes = {}
        for name in ("linguistic_markers_paper.md", "linguistic_markers_paper.pdf", "RESEARCH_STATUS.md", "README.md"):
            if (archive / name).exists():
                raise ValueError("Incomplete pre-follow-up archive needs inspection")
            shutil.copy2(PAPER / name, archive / name)
            hashes[name] = hashlib.sha256((archive / name).read_bytes()).hexdigest()
        (archive / "manifest.json").write_text(json.dumps(hashes, indent=2) + "\n")
    shutil.copy2(PAPER / "results/correction_20261005/revision2/exclusions.csv", RESULTS / "exclusions.csv")
    figures = RESULTS / "figures"
    figures.mkdir(exist_ok=True)
    evaluation = json.loads((RESULTS / "evaluation.json").read_text())
    models = evaluation["models"]
    stats = pd.read_csv(RESULTS / "feature_comparisons.csv")
    frame = pd.read_csv(RESULTS / "features.csv.gz")
    source = json.loads((FOLLOWUP / "source_summary_resolved.json").read_text())
    external = json.loads((FOLLOWUP / "external/evaluation.json").read_text())["models"]
    manifest = json.loads((RESULTS / "manifest.json").read_text())
    (RESULTS / "manuscript_tables.md").write_text("\n\n".join([
        flow_table(manifest), feature_table(stats), model_table(models), source_table(source), external_table(external)]) + "\n")
    plt.rcParams.update({"font.size": 14, "axes.spines.top": False, "axes.spines.right": False,
                         "savefig.dpi": 220, "figure.constrained_layout.use": True})

    fig, axes = plt.subplots(1, 2, figsize=(10, 3.6))
    for label, color, name in ((0, "#2563eb", "Published"), (1, "#e76f25", "Generated")):
        for ax, column, xlabel in zip(axes, ["word_count", "sentence_count"], ["Words per text", "Sentences per text"]):
            values, counts = np.unique(frame.loc[frame.label == label, column].to_numpy(), return_counts=True)
            # An empirical CDF is right-continuous and constant between values.
            limits = (100, 600) if column == "word_count" else (2, 25)
            endpoints = (min(limits[0], values[0]-1), max(limits[1], values[-1]))
            ax.step(np.r_[endpoints[0], values, endpoints[1]], np.r_[0, np.cumsum(counts)/counts.sum(), 1],
                    where="post", color=color, label=name)
            ax.set_xlabel(xlabel)
            ax.set_ylabel("Cumulative share")
    axes[0].set_xlim(100, 600)
    axes[1].set_xlim(2, 25)
    axes[0].legend(frameon=False)
    fig.savefig(figures / "fig1_lengths.png", bbox_inches="tight")
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(9, 4.8))
    selected = list(reversed(models))
    ys = np.arange(len(selected))
    points = np.array([m["accuracy"]*100 for m in selected])
    lower = np.array([m["conditional_group_bootstrap_95ci"]["accuracy"][0]*100 for m in selected])
    upper = np.array([m["conditional_group_bootstrap_95ci"]["accuracy"][1]*100 for m in selected])
    ax.errorbar(points, ys, xerr=np.vstack([points-lower, upper-points]), fmt="o", color="#2563eb", capsize=3)
    ax.set_yticks(ys, [MODELS[m["name"]] for m in selected])
    ax.set_xlabel("Out-of-fold accuracy (%)")
    ax.set_xlim(75, 100)
    ax.grid(axis="x", alpha=.2)
    fig.savefig(figures / "fig2_comparisons.png", bbox_inches="tight")
    plt.close(fig)

    fig, axes = plt.subplots(1, 2, figsize=(10, 4))
    for name, folder, color, label in (
        ("forest_eight", RESULTS, "#2563eb", "Forest: internal"),
        ("forest_eight_external", FOLLOWUP / "external", "#e76f25", "Forest: external"),
        ("logistic_eight_external", FOLLOWUP / "external", "#555555", "Logistic: external"),
    ):
        pred = pd.read_csv(folder / f"predictions_{name}.csv.gz", float_precision="round_trip")
        fpr, tpr, _ = roc_curve(pred.label, pred.probability)
        precision, recall, _ = precision_recall_curve(pred.label, pred.probability)
        axes[0].plot(fpr, tpr, color=color, label=label)
        axes[1].plot(recall, precision, color=color)
    axes[0].plot([0, 1], [0, 1], "--", color="grey", linewidth=.8)
    axes[0].set(xlabel="False-positive rate", ylabel="Recall", xlim=(0, 1), ylim=(0, 1.01))
    axes[1].set(xlabel="Recall", ylabel="Precision", xlim=(0, 1), ylim=(0, 1.01))
    axes[0].legend(loc="lower right", fontsize=9, frameon=False)
    fig.savefig(figures / "fig3_curves.png", bbox_inches="tight")
    plt.close(fig)

    main_model = next(m for m in models if m["name"] == "forest_eight")
    cm = np.asarray(main_model["confusion_matrix"])
    fig, ax = plt.subplots(figsize=(5.8, 4.8))
    ax.imshow(cm, cmap="Blues")
    ax.set_xticks([0, 1], ["Published", "Generated"])
    ax.set_yticks([0, 1], ["Published", "Generated"])
    ax.set_xlabel("Predicted label")
    ax.set_ylabel("Recorded label")
    for i in range(2):
        for j in range(2):
            ax.text(j, i, f"{cm[i,j]:,}\n{100*cm[i,j]/cm[i].sum():.2f}% of row",
                    ha="center", va="center", color="white" if i == j else "black", fontsize=15)
    fig.savefig(figures / "fig4_confusion.png", bbox_inches="tight")
    plt.close(fig)
    print((RESULTS / "manuscript_tables.md").read_text())


if __name__ == "__main__":
    main()

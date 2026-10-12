"""Audit recovered study inputs without running collection or generation code."""

import argparse
import hashlib
import json
import re
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd


PAPER = Path(__file__).resolve().parents[1]


def sha256(path):
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def file_record(path):
    return {"path": str(path.relative_to(PAPER)), "bytes": path.stat().st_size,
            "sha256": sha256(path)}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if args.output.exists():
        raise SystemExit(f"Refusing to overwrite audit: {args.output}")

    human_path = PAPER / "data/metadata/openalex_human_abstracts.csv"
    paired_path = PAPER / "data/metadata/synthetic_abstracts_openai.csv"
    features_path = PAPER / "data/features/corpus_features.csv"
    human = pd.read_csv(human_path, keep_default_na=False)
    pairs = pd.read_csv(paired_path, keep_default_na=False)
    features = pd.read_csv(features_path)
    report = {"audited_at_utc": datetime.now(timezone.utc).isoformat(),
              "inputs": [file_record(p) for p in (human_path, paired_path, features_path)],
              "human_rows": len(human), "paired_rows": len(pairs),
              "feature_rows": len(features), "human_columns": list(human.columns),
              "paired_columns": list(pairs.columns), "feature_columns": list(features.columns)}

    for name, frame in (("human", human), ("paired", pairs)):
        years = pd.to_numeric(frame["year"], errors="coerce")
        report[name] = {
            "unique_ids": int(frame["openalex_id"].nunique()),
            "duplicate_ids": int(frame["openalex_id"].duplicated().sum()),
            "missing_titles": int(frame["title"].str.strip().eq("").sum()),
            "id_shape_failures": int((~frame["openalex_id"].str.fullmatch(r"https://openalex\.org/W\d+")).sum()),
            "ids_with_fewer_than_seven_digits": int(frame["openalex_id"].str.fullmatch(r"https://openalex\.org/W\d{1,6}").sum()),
            "year_counts": {str(k): int(v) for k, v in years.value_counts(dropna=False).sort_index().items()},
            "missing_year": int(years.isna().sum()),
            "post2021_rows": int((years > 2021).sum()),
        }

    joined = pairs.merge(human, on="openalex_id", how="left", suffixes=("_pair", "_source"), indicator=True)
    report["source_join"] = {
        "joined_rows": len(joined),
        "matched_ids": int(joined["_merge"].eq("both").sum()),
        "title_mismatches": int((joined["title_pair"] != joined["title_source"]).sum()),
        "year_mismatches": int((joined["year_pair"] != joined["year_source"]).sum()),
        "text_mismatches": int((joined["human_abstract"] != joined["abstract"]).sum()),
    }

    length_report = {}
    for col in ("human_abstract", "ai_abstract"):
        text = pairs[col].astype(str)
        counts = text.map(lambda s: len(re.findall(r"\b[a-zA-Z]+\b", s)))
        length_report[col] = {
            "empty": int(text.str.strip().eq("").sum()),
            "exact_duplicates": int(text.duplicated().sum()),
            "at_most_100_characters": int(text.str.strip().str.len().le(100).sum()),
            "under_100_regex_words": int(counts.lt(100).sum()),
            "word_quantiles": {str(k): float(v) for k, v in counts.quantile([0, .01, .25, .5, .75, .99, 1]).items()},
            "missing_terminal_punctuation": int(text.map(lambda s: re.search(r'[.!?][\s\"\u201d\u2019\)]*$', s.strip()) is None).sum()),
        }
    report["text_audit"] = length_report
    report["identical_within_pair"] = int(pairs["human_abstract"].eq(pairs["ai_abstract"]).sum())
    report["cross_class_exact_texts"] = len(set(pairs["human_abstract"]) & set(pairs["ai_abstract"]))
    legacy = pairs[(pairs["human_abstract"].str.strip().str.len() > 100)
                   & (pairs["ai_abstract"].str.strip().str.len() > 100)].drop_duplicates("human_abstract")
    report["historical_cleaning_pairs"] = len(legacy)
    report["historical_expected_feature_rows"] = 2 * len(legacy)
    report["feature_label_counts"] = {str(k): int(v) for k, v in features["label"].value_counts().items()}
    report["feature_nonfinite_values"] = int((~np.isfinite(features.to_numpy())).sum())
    report["feature_zero_mtld"] = int(features["lexical_diversity_mtld"].eq(0).sum())
    report["feature_one_or_fewer_sentences"] = int(features["sentence_count"].le(1).sum())

    saved_stats = pd.read_csv(PAPER / "results/tables/statistical_comparisons.csv")
    comparisons = []
    for _, row in saved_stats.iterrows():
        feature = row["Feature"]
        h = features.loc[features["label"] == 0, feature].to_numpy()
        a = features.loc[features["label"] == 1, feature].to_numpy()
        derived = {"Human Mean": float(np.mean(h)), "Human SD": float(np.std(h)),
                   "AI Mean": float(np.mean(a)), "AI SD": float(np.std(a))}
        comparisons.append({"feature": feature, "derived": derived,
                            "matches_saved_to_4dp": {key: round(value, 4) == round(float(row[key]), 4)
                                                      for key, value in derived.items()}})
    report["saved_feature_summary_comparison"] = comparisons
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2, allow_nan=False) + "\n")
    print(json.dumps(report, indent=2, allow_nan=False))


if __name__ == "__main__":
    main()

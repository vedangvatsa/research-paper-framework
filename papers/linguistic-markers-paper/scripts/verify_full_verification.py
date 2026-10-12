"""Check source-audit accounting, test-set independence and follow-up predictions."""

import gzip
import json
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.metrics import (accuracy_score, average_precision_score, confusion_matrix,
                             f1_score, precision_score, recall_score, roc_auc_score)

from audit_recovered_data import sha256
from corrected_analysis import FEATURES, LENGTHS, normalize, text_hash
from prepare_corrected_results import external_table, source_table


PAPER = Path(__file__).resolve().parents[1]
ROOT = PAPER / "results/full_verification_20261005"


def truth(series):
    return series.map(lambda value: str(value).lower() == "true")


def verify_models(folder, test_features, models):
    for model in models:
        pred = pd.read_csv(folder / f"predictions_{model['name']}.csv.gz", float_precision="round_trip")
        assert not pred.duplicated(["pair_id", "label"]).any()
        joined = pred.merge(test_features, on=["pair_id", "label"], how="left", suffixes=("", "_feature"), validate="one_to_one")
        assert joined.group_id.eq(joined.group_id_feature).all()
        assert len(pred) == len(test_features)
        assert pred.probability.between(0, 1).all()
        assert pred.prediction.eq(pred.probability.gt(.5).astype(int)).all()
        y, p, predicted = pred.label, pred.probability, pred.prediction
        cm = confusion_matrix(y, predicted, labels=[0, 1])
        assert cm.tolist() == model["confusion_matrix"]
        calculated = {"accuracy": accuracy_score(y, predicted), "precision": precision_score(y, predicted),
                      "recall": recall_score(y, predicted), "f1": f1_score(y, predicted),
                      "roc_auc": roc_auc_score(y, p), "average_precision": average_precision_score(y, p),
                      "false_positive_rate": cm[0, 1]/cm[0].sum(), "specificity": cm[0, 0]/cm[0].sum()}
        for key, value in calculated.items():
            assert np.isclose(model[key], value, rtol=0, atol=1e-12), (model["name"], key)
        print(f"Verified {model['name']}: {len(pred):,} predictions")


def main():
    source = pd.read_csv(ROOT / "source_checks_resolved.csv.gz", low_memory=False)
    summary = json.loads((ROOT / "source_summary_resolved.json").read_text())
    raw_source_path = PAPER / "data/metadata/openalex_human_abstracts.csv"
    assert sha256(raw_source_path) == summary["source_input_sha256"]
    original = pd.read_csv(raw_source_path, keep_default_na=False)
    assert len(source) == 100000 and source.source_id.is_unique
    assert set(source.source_id) == set(original.openalex_id)
    retained = pd.read_csv(ROOT / "revision4/features.csv.gz")
    previous = pd.read_csv(PAPER / "results/correction_20261005/revision2/features.csv.gz")
    assert np.array_equal(previous[FEATURES].to_numpy(), retained[FEATURES].to_numpy())
    assert previous.pair_id.equals(retained.pair_id) and previous.label.equals(retained.label)
    assert truth(source.in_revision2).sum() == retained.pair_id.nunique()
    recalculated_consistent = (truth(source.title_agrees) & truth(source.year_agrees)
                              & truth(source.abstract_exact_clean_match) & source.current_language.eq("en")
                              & source.current_type.eq("article") & source.current_retracted.map(lambda v: str(v).lower() == "false"))
    assert recalculated_consistent.equals(truth(source.source_consistent))
    for label, subset in (("all", source), ("revision2", source[truth(source.in_revision2)])):
        assert subset.source_status.value_counts().to_dict() == summary[label]["status_counts"]
        for col in ("title_agrees", "doi_agrees", "year_agrees", "current_has_abstract", "abstract_exact_clean_match", "abstract_word_sequence_match", "source_consistent", "current_retracted"):
            assert int(truth(subset[col]).sum()) == summary[label][col], (label, col)

    # The independent CSV summary is linked back to cached requests by the
    # response hashes. Every claimed retrieval must have a stored response.
    response_hashes = set()
    cached_records = 0
    for path in (ROOT / "openalex_cache").glob("*.json.gz"):
        with gzip.open(path, "rt") as stream:
            entry = json.load(stream)
        if entry.get("status") == 200:
            response_hashes.add(entry["response_sha256"])
            cached_records += 1 if entry["singleton"] else len(entry["data"]["results"])
    claimed = source[source.source_status.eq("retrieved")]
    assert set(claimed.response_sha256) <= response_hashes

    strict_path = ROOT / "source_consistency_final"
    strict = pd.read_csv(strict_path / "features.csv.gz")
    strict_ids = set(source.loc[recalculated_consistent, "source_id"]) & set(retained.pair_id)
    assert set(strict.pair_id) == strict_ids
    strict_models = json.loads((strict_path / "evaluation.json").read_text())["models"]
    verify_models(strict_path, strict, strict_models)

    external_path = ROOT / "external"
    external = pd.read_csv(external_path / "features.csv.gz")
    excluded = pd.read_csv(external_path / "exclusions.csv")
    eligibility = json.loads((external_path / "eligibility.json").read_text())
    download = json.loads((external_path / "download_manifest.json").read_text())
    for name, record in download["files"].items():
        assert sha256(external_path / name) == record["sha256"]
    raw_external = pd.read_csv(external_path / "research_abstracts-final.csv", keep_default_na=False)
    local = pd.read_csv(PAPER / "data/metadata/synthetic_abstracts_openai.csv", keep_default_na=False)
    assert len(external) == eligibility["included_texts"]
    assert len(external) // 2 + len(excluded) == len(raw_external) == 10000
    assert external.word_count.ge(100).all() and external.sentence_count.ge(2).all()
    assert not set(external.pair_id) & set(excluded.pair_id)
    local_hashes = {text_hash(t) for col in ("human_abstract", "ai_abstract") for t in local[col]}
    assert set(external.text_hash).isdisjoint(local_hashes)
    local_titles = set(local.title.map(normalize))
    for row in external.itertuples(index=False):
        raw_row = raw_external.iloc[int(row.pair_id.split(":")[1])]
        text = raw_row.real_abstract if row.label == 0 else raw_row.generated_abstract
        assert text_hash(text) == row.text_hash, (row.pair_id, row.label)
        assert normalize(raw_row.title) not in local_titles
    external_results = json.loads((external_path / "evaluation.json").read_text())
    assert external_results["training_features_sha256"] == sha256(ROOT / "revision3/features.csv.gz")
    external_training = pd.read_csv(ROOT / "revision3/features.csv.gz")
    assert np.array_equal(external_training[FEATURES + LENGTHS].to_numpy(), retained[FEATURES + LENGTHS].to_numpy())
    assert external_training.label.equals(retained.label)
    assert external_results["external_features_sha256"] == sha256(external_path / "features.csv.gz")
    verify_models(external_path, external, external_results["models"])
    manuscript = (PAPER / "linguistic_markers_paper.md").read_text()
    assert source_table(summary) in manuscript
    assert external_table(external_results["models"]) in manuscript
    types = summary["revision2"]["current_type"]
    assert f"{types['conference-paper']:,} records now typed as conference papers" in manuscript
    assert f"{types['book-review']:,} typed as book reviews" in manuscript
    assert f"{summary['revision2']['current_retracted']} retained works as retracted" in manuscript
    quality = json.loads((ROOT / "text_quality_all_labels_summary.json").read_text())
    assert f"{quality['published']['non_english_score_at_least_0_9']:,} published texts and {quality['generated']['non_english_score_at_least_0_9']:,} generated texts as non-English" in manuscript
    external_forest = external_results["models"][0]
    tn, fp, fn, tp = np.array(external_forest["confusion_matrix"]).ravel()
    assert f"{tn:,} of {tn+fp:,} external published texts" in manuscript
    assert f"{tp:,} of {tp+fn:,} generated texts" in manuscript
    assert f"{fn:,} generated texts and wrongly flags {fp:,} published texts" in manuscript
    for label, name in ((0, "published"), (1, "generated")):
        low, median, high = external.loc[external.label.eq(label), "word_count"].quantile([.25, .5, .75])
        assert (f"{name} texts have a median of {median:.0f} words and an interquartile range of "
                f"{low:.0f}-{high:.0f}") in manuscript
    report = {"source_ids_accounted_for": len(source), "retrieved_source_responses_linked": len(claimed),
              "unresolved_source_statuses": source.loc[source.source_status.ne("retrieved"), "fetch_status"].astype(str).value_counts().to_dict(),
              "source_consistent_pairs": len(strict_ids), "followup_prediction_sets_verified": 5,
              "external_pairs": len(external)//2, "external_label_to_raw_text_hashes_verified": len(external),
              "external_exact_title_and_text_overlap": 0,
              "near_duplicate_feature_values_unchanged": True, "manuscript_followup_tables_match": True}
    (ROOT / "verification.json").write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()

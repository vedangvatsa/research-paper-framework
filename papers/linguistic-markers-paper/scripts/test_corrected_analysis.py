"""Known-answer tests for the scientific measurement and split rules."""

import os

import numpy as np
import pandas as pd
import pytest

from corrected_analysis import (cluster_bootstrap, count_connectors, extract_features,
                                fold_for_group, group_pairs, load_tokenizer, ratios,
                                valid_source_id, validate_splits)


class SentenceFixture:
    def tokenize(self, text):
        return [s for s in text.split(".") if s.strip()]


def test_multiword_connectors_are_counted_once():
    assert count_connectors("in addition we tested samples as a result we changed methods".split()) == 2
    assert count_connectors("additional results are reported".split()) == 0


def test_features_use_phrases_and_do_not_count_us_as_a_pronoun():
    result = extract_features("In addition, US laboratories tested samples. As a result, we compared results.", SentenceFixture())
    assert result["sentence_count"] == 2
    assert result["first_word_connector_ratio"] == 1
    assert result["connector_density"] == pytest.approx(2000 / result["word_count"])
    assert result["self_mention_density"] == pytest.approx(1000 / result["word_count"])


def test_empty_text_is_not_a_valid_zero_feature_record():
    with pytest.raises(ValueError):
        extract_features("123 !!!", SentenceFixture())


def test_related_groups_are_transitive_across_titles_and_texts():
    pairs = pd.DataFrame([
        {"openalex_id": "a", "title": "Shared Title", "human_hash": "h1", "ai_hash": "a1"},
        {"openalex_id": "b", "title": "shared title", "human_hash": "h2", "ai_hash": "a2"},
        {"openalex_id": "c", "title": "Third Title", "human_hash": "h2", "ai_hash": "a3"},
        {"openalex_id": "d", "title": "Fourth Title", "human_hash": "h4", "ai_hash": "a4"},
    ])
    groups = group_pairs(pairs)
    assert groups[:3] == ["a", "a", "a"]
    assert groups[3] == "d"
    assert len({fold_for_group(g) for g in groups[:3]}) == 1


def test_validation_rejects_a_source_pair_crossing_folds():
    frame = pd.DataFrame({"pair_id": ["a", "a"], "group_id": ["a", "a"],
                          "title_hash": ["t", "t"], "text_hash": ["h", "g"],
                          "label": [0, 1], "fold": [0, 1]})
    with pytest.raises(ValueError, match="crosses folds"):
        validate_splits(frame)


def test_metrics_use_the_human_denominator_for_false_alarms():
    metrics = ratios(np.array([19218, 782, 943, 19057]))
    assert metrics[0] == pytest.approx(38275 / 40000)
    assert metrics[4] == pytest.approx(782 / 20000)
    assert metrics[2] == pytest.approx(19057 / 20000)


def test_short_openalex_ids_are_not_excluded_by_length():
    assert valid_source_id("https://openalex.org/W852874")
    assert valid_source_id("https://openalex.org/W226145")
    assert not valid_source_id("https://example.com/W852874")
    assert not valid_source_id("https://openalex.org/not-a-work")


def test_group_bootstrap_resamples_groups_with_their_sizes():
    draws = cluster_bootstrap(np.array([[2.0], [6.0]]), np.array([1, 3]), repeats=100)
    assert np.allclose(draws, 2)


def test_real_punkt_handles_abbreviation_and_decimal():
    path = os.environ.get("PUNKT_ARCHIVE")
    if not path:
        pytest.skip("Set PUNKT_ARCHIVE for the real tokenizer-resource test")
    tokenizer = load_tokenizer(path)
    text = "Dr. Smith measured 3.14 units in the samples. The samples were measured again."
    assert tokenizer.tokenize(text) == [
        "Dr. Smith measured 3.14 units in the samples.",
        "The samples were measured again.",
    ]

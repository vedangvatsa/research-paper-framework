"""Known-answer checks for source matching and the additional grouping audit."""

from types import SimpleNamespace

import pandas as pd
import pytest

from audit_all_sources import compare, invert
from audit_text_quality import shingles, signature
from check_source_identities import valid_doi_identity
from regroup_confirmed_duplicates import merged_groups


def test_inverted_abstract_respects_positions():
    assert invert({"test": [2], "This": [0], "is": [1]}) == "This is test"
    with pytest.raises(ValueError):
        invert({"first": [0], "second": [0]})


def test_source_match_keeps_numerical_findings_distinct():
    row = SimpleNamespace(openalex_id="https://openalex.org/W1", title="Study", doi="", year=2020,
                          abstract="There were 10 participants.")
    current = {"id": row.openalex_id, "title": "Study", "publication_year": 2020, "language": "en",
               "type": "article", "is_retracted": False,
               "abstract_inverted_index": {"There": [0], "were": [1], "20": [2], "participants.": [3]}}
    result = compare(row, current, {"status": 200})
    assert result["title_agrees"]
    assert not result["abstract_exact_clean_match"]
    assert not result["source_consistent"]


def test_unavailable_source_is_not_a_failed_factual_match():
    row = SimpleNamespace(openalex_id="https://openalex.org/W1")
    result = compare(row, None, {"status": 403})
    assert result["source_status"] == "unresolved"
    assert "source_consistent" not in result


def test_five_gram_candidate_and_exact_sets_agree_on_copy():
    text = "One two three four five six seven eight nine"
    assert len(shingles(text)) == 5
    first, count = signature(text)
    second, _ = signature(text.upper())
    assert count == 5
    assert (first == second).all()


def test_near_duplicate_edges_merge_preexisting_groups_transitively():
    frame = pd.DataFrame({"pair_id": ["a", "b", "c", "d"], "group_id": ["a", "b", "b", "d"]})
    edges = pd.DataFrame({"left_id": ["a", "c"], "right_id": ["b", "d"]})
    assert set(merged_groups(frame, edges).values()) == {"a"}


def test_bare_doi_resolver_is_not_a_shared_work_identity():
    assert not valid_doi_identity("https://doi.org/")
    assert not valid_doi_identity("")
    assert not valid_doi_identity(None)
    assert valid_doi_identity("https://doi.org/10.1088/1674-1137/38/9/090001")

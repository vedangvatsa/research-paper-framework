"""Known-answer checks for strict thresholds and score-independent selection."""

import numpy as np
import pytest

from defensibility_checks import choose_threshold, score_metrics, threshold_curve


def test_threshold_curve_matches_direct_predictions_including_ties():
    y = np.array([0, 1, 0, 1, 1, 0])
    scores = np.array([0, .2, .5, .5, .8, 1])
    curve = threshold_curve(y, scores)
    for row in curve.itertuples(index=False):
        metrics = score_metrics(y, scores, row.threshold)
        assert row.accuracy == pytest.approx(metrics["accuracy"])
        assert row.fpr == pytest.approx(metrics["false_positive_rate"])
        assert row.tpr == pytest.approx(metrics["recall"])
    assert curve.iloc[0].tpr == 0 and curve.iloc[0].fpr == 0
    assert curve.iloc[-1].tpr == 1 and curve.iloc[-1].fpr == 1


def test_source_fpr_quantile_respects_strict_ties():
    y = np.array([0]*100 + [1]*100)
    scores = np.r_[np.repeat([.1, .8, .9], [95, 4, 1]), np.full(100, .85)]
    for mode, target in (("fpr_01", .01), ("fpr_05", .05)):
        threshold = choose_threshold(y, scores, mode)
        assert score_metrics(y, scores, threshold)["false_positive_rate"] <= target


def test_tied_optimum_chooses_more_conservative_threshold():
    y = np.array([0, 1, 0, 1])
    scores = np.array([.2, .2, .8, .8])
    assert choose_threshold(y, scores, "best_balanced_accuracy") == .8

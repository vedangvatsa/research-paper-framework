"""A CSV parsing regression that matters for tie-sensitive ranking metrics."""

from sklearn.metrics import roc_auc_score

from reproduce_scores import read_scores


def test_saved_score_order_survives_csv_round_trip():
    raw = (b"label,probability,prediction\n"
           b"0,0.12345678901234561,0\n"
           b"1,0.12345678901234568,0\n")
    frame = read_scores(raw)
    assert frame.probability.nunique() == 2
    assert frame.probability.iloc[0] == float("0.12345678901234561")
    assert frame.probability.iloc[1] == float("0.12345678901234568")
    assert roc_auc_score(frame.label, frame.probability) == 1.0

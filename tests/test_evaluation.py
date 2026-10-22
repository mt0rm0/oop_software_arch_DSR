import pytest

from churn.evaluation import ConfusionMatrix, RetentionCost


@pytest.fixture
def cm() -> ConfusionMatrix:
    #           y_true: 0  0  0  0  1  1  1  1
    #           y_pred: 0  0  0  1  0  1  1  1
    return ConfusionMatrix.from_predictions([0, 0, 0, 0, 1, 1, 1, 1], [0, 0, 0, 1, 0, 1, 1, 1])


def test_counts(cm):
    assert (cm.tn, cm.fp, cm.fn, cm.tp) == (3, 1, 1, 3)
    assert cm.n == 8


def test_metrics(cm):
    assert cm.precision == pytest.approx(0.75)
    assert cm.recall == pytest.approx(0.75)
    assert cm.f1 == pytest.approx(0.75)
    assert cm.accuracy == pytest.approx(0.75)


def test_metrics_without_positive_predictions_are_zero_not_an_error():
    cm = ConfusionMatrix.from_predictions([0, 1], [0, 0])
    assert cm.precision == 0.0
    assert cm.f1 == 0.0


def test_shape_mismatch_is_rejected():
    with pytest.raises(ValueError, match="shape"):
        ConfusionMatrix.from_predictions([0, 1, 1], [0, 1])


def test_unpacking_matches_sklearn_order(cm):
    tn, fp, fn, tp = cm
    assert (tn, fp, fn, tp) == (3, 1, 1, 3)


def test_adding_pools_counts(cm):
    total = cm + cm
    assert total == ConfusionMatrix(tn=6, fp=2, fn=2, tp=6)


def test_sum_over_folds(cm):
    assert sum([cm, cm, cm]) == ConfusionMatrix(tn=9, fp=3, fn=3, tp=9)


def test_adding_something_else_fails(cm):
    with pytest.raises(TypeError):
        cm + 1


def test_retention_cost_is_callable_like_a_metric():
    cost = RetentionCost(offer_cost=10, customer_value=100, acceptance_rate=0.5)
    #   one TP: 10 offer + 50 expected loss; one FP: 10 offer; one FN: 100 lost
    assert cost([1, 0, 1], [1, 1, 0]) == pytest.approx(170)


def test_flagging_nobody_costs_every_churner():
    cost = RetentionCost(customer_value=100)
    assert cost([1, 0, 1], [0, 0, 0]) == cost.do_nothing([1, 0, 1]) == 200

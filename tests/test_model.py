import numpy as np
import pytest
from sklearn.dummy import DummyClassifier

from churn.config import ExperimentConfig
from churn.data import clean_customers, split_features_target
from churn.errors import NotFittedError, SchemaError
from churn.model import ChurnModel


@pytest.fixture(scope="module")
def telco_xy(telco_raw):
    return split_features_target(clean_customers(telco_raw))


@pytest.fixture(scope="module")
def fitted_model(telco_xy):
    X, y = telco_xy
    return ChurnModel().fit(X, y)


def test_predict_before_fit_raises(telco_xy):
    X, _ = telco_xy
    with pytest.raises(NotFittedError):
        ChurnModel().predict(X)


def test_predictions_are_binary_and_aligned(fitted_model, telco_xy):
    X, _ = telco_xy
    preds = fitted_model.predict(X.head(50))
    assert preds.shape == (50,)
    assert set(np.unique(preds)) <= {0, 1}


def test_probabilities_are_probabilities(fitted_model, telco_xy):
    X, _ = telco_xy
    proba = fitted_model.predict_proba(X)
    assert ((proba >= 0) & (proba <= 1)).all()


def test_score_of_a_customer_does_not_depend_on_the_batch(fitted_model, telco_xy):
    """The bug from the warm-up notebook must be impossible here."""
    X, _ = telco_xy
    two_year_only = X[X["Contract"] == "Two year"].head(20)
    in_full_batch = fitted_model.predict_proba(X)[X.index.get_indexer(two_year_only.index)]
    alone = fitted_model.predict_proba(two_year_only)
    np.testing.assert_allclose(alone, in_full_batch)


def test_missing_feature_column_is_reported(fitted_model, telco_xy):
    X, _ = telco_xy
    with pytest.raises(SchemaError, match="Contract"):
        fitted_model.predict(X.drop(columns=["Contract"]))


def test_lower_threshold_flags_more_customers(fitted_model, telco_xy):
    X, _ = telco_xy
    fitted_model.threshold = 0.5
    strict = fitted_model.predict(X).sum()
    fitted_model.threshold = 0.2
    lenient = fitted_model.predict(X).sum()
    fitted_model.threshold = 0.5
    assert lenient > strict


@pytest.mark.parametrize("bad", [0, 1, 1.5, -0.1])
def test_threshold_must_be_a_probability(bad):
    with pytest.raises(ValueError):
        ChurnModel().threshold = bad


def test_any_probabilistic_estimator_can_be_plugged_in(telco_xy):
    X, y = telco_xy
    model = ChurnModel(estimator=DummyClassifier(strategy="prior")).fit(X, y)
    assert model.predict_proba(X.head(3)) == pytest.approx([y.mean()] * 3)


def test_save_and_load_roundtrip(fitted_model, telco_xy, tmp_path):
    X, _ = telco_xy
    path = fitted_model.save(tmp_path / "model.joblib")
    reloaded = ChurnModel.load(path)
    np.testing.assert_array_equal(reloaded.predict(X), fitted_model.predict(X))


def test_random_forest_config(telco_xy):
    X, y = telco_xy
    config = ExperimentConfig(model="random_forest", model_params={"n_estimators": 20})
    model = ChurnModel(config).fit(X.head(500), y.head(500))
    assert "RandomForest" in repr(model)

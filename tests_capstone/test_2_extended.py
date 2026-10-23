"""If you finish early: configuration, errors as a family, and a model that is actually useful.

The contract (in addition to test_1_essentials.py):
    churn_capstone.config.ExperimentConfig     dataclass with test_size and random_state
    churn_capstone.errors.ChurnError           base class of all your exceptions
    churn_capstone.errors.NotFittedError       raised when predicting before fit
    ChurnModel(config)                         accepts a config
"""

import pytest
from sklearn.metrics import f1_score
from sklearn.model_selection import train_test_split


@pytest.fixture
def X_y(get, data_path):
    customers = get("data", "load_customers")(data_path)
    return customers.drop(columns=["Churn"]), customers["Churn"]


def test_config_has_sensible_defaults(get):
    config = get("config", "ExperimentConfig")()
    assert 0 < config.test_size < 1
    assert isinstance(config.random_state, int)


@pytest.mark.parametrize("bad_test_size", [0, 1, 1.5, -0.2])
def test_invalid_test_size_is_rejected_at_creation(get, bad_test_size):
    with pytest.raises(ValueError):
        get("config", "ExperimentConfig")(test_size=bad_test_size)


def test_all_errors_share_a_base_class(get):
    ChurnError = get("errors", "ChurnError")
    assert issubclass(get("errors", "SchemaError"), ChurnError)
    assert issubclass(get("errors", "NotFittedError"), ChurnError)


def test_predict_before_fit_raises_not_fitted_error(get, X_y):
    X, _ = X_y
    with pytest.raises(get("errors", "NotFittedError")):
        get("model", "ChurnModel")().predict(X)


def test_model_accepts_a_config(get, X_y):
    X, y = X_y
    config = get("config", "ExperimentConfig")()
    model = get("model", "ChurnModel")(config).fit(X, y)
    assert len(model.predict(X.head(5))) == 5


def test_model_is_useful_on_unseen_customers(get, X_y):
    """Predicting "nobody churns" scores F1 = 0. A reasonable model reaches about 0.6."""
    X, y = X_y
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=0, stratify=y
    )
    model = get("model", "ChurnModel")().fit(X_train, y_train)
    assert f1_score(y_test, model.predict(X_test)) > 0.5

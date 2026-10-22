"""Core: everybody should get these green.

The contract:
    churn_capstone.data.load_customers(path)  -> cleaned DataFrame
    churn_capstone.errors.SchemaError          raised for missing columns
    churn_capstone.model.ChurnModel()          with fit(X, y) and predict(X)
"""

import numpy as np
import pandas as pd
import pytest


@pytest.fixture
def customers(get, data_path):
    return get("data", "load_customers")(data_path)


@pytest.fixture
def X_y(customers):
    return customers.drop(columns=["Churn"]), customers["Churn"]


def test_load_returns_every_customer(customers):
    assert len(customers) == 7043


def test_total_charges_is_numeric_without_gaps(customers):
    assert customers["TotalCharges"].dtype.kind == "f"
    assert customers["TotalCharges"].notna().all()


def test_churn_is_zero_or_one(customers):
    assert set(customers["Churn"].unique()) == {0, 1}


def test_customer_id_is_not_a_feature(customers):
    assert "customerID" not in customers.columns


def test_missing_column_raises_schema_error(get, raw, write_csv):
    SchemaError = get("errors", "SchemaError")
    path = write_csv(raw.drop(columns=["tenure"]))
    with pytest.raises(SchemaError):
        get("data", "load_customers")(path)


def test_fit_returns_the_model_itself(get, X_y):
    X, y = X_y
    model = get("model", "ChurnModel")()
    assert model.fit(X, y) is model


def test_predict_returns_one_label_per_customer(get, X_y):
    X, y = X_y
    model = get("model", "ChurnModel")().fit(X, y)
    preds = np.asarray(model.predict(X.head(100)))
    assert preds.shape == (100,)
    assert set(np.unique(preds)) <= {0, 1}


def test_prediction_does_not_depend_on_who_else_is_in_the_batch(get, X_y):
    """The warm-up notebook's hidden bug: re-encoding each new batch."""
    X, y = X_y
    model = get("model", "ChurnModel")().fit(X, y)
    two_year = X[X["Contract"] == "Two year"].head(30)
    month_to_month = X[X["Contract"] == "Month-to-month"].head(30)

    alone = np.asarray(model.predict(two_year))
    mixed = np.asarray(model.predict(pd.concat([two_year, month_to_month])))[: len(two_year)]
    np.testing.assert_array_equal(alone, mixed)

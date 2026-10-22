"""Challenge: robustness and persistence.

The contract (in addition to stretch):
    churn_capstone.errors.DataQualityError     raised for unusable values
    model.save(path) / ChurnModel.load(path)   round trip
"""

import numpy as np
import pytest


@pytest.fixture
def X_y(get, data_path):
    customers = get("data", "load_customers")(data_path)
    return customers.drop(columns=["Churn"]), customers["Churn"]


def test_blank_total_charges_for_an_existing_customer_is_a_quality_error(get, raw, write_csv):
    broken = raw.copy()
    long_term = broken.index[broken["tenure"] > 12][0]
    broken.loc[long_term, "TotalCharges"] = " "
    with pytest.raises(get("errors", "DataQualityError")):
        get("data", "load_customers")(write_csv(broken))


def test_unseen_category_does_not_crash_prediction(get, X_y):
    X, y = X_y
    model = get("model", "ChurnModel")().fit(X, y)
    new_customer = X.head(1).copy()
    new_customer["Contract"] = "Three year"  # a product launched after training
    preds = np.asarray(model.predict(new_customer))
    assert preds.shape == (1,)


def test_save_and_load_give_identical_predictions(get, X_y, tmp_path):
    X, y = X_y
    ChurnModel = get("model", "ChurnModel")
    model = ChurnModel().fit(X, y)
    path = tmp_path / "model.joblib"
    model.save(path)
    reloaded = ChurnModel.load(path)
    np.testing.assert_array_equal(np.asarray(reloaded.predict(X)), np.asarray(model.predict(X)))

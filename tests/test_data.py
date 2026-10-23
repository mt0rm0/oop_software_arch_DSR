import pandas as pd
import pytest

from churn.data import InMemoryLoader, clean_customers, load_customers, split_features_target
from churn.errors import DataQualityError, SchemaError


def test_clean_sets_customer_id_as_index(raw_customers):
    df = clean_customers(raw_customers)
    assert df.index.name == "customerID"
    assert "customerID" not in df.columns


def test_blank_total_charges_of_new_customer_becomes_zero(raw_customers):
    df = clean_customers(raw_customers)
    assert df.loc["A-2", "TotalCharges"] == 0.0
    assert df["TotalCharges"].dtype == float


def test_blank_total_charges_of_existing_customer_is_an_error(raw_customers):
    raw_customers.loc[0, "TotalCharges"] = " "  # tenure 1, so this is a real data problem
    with pytest.raises(DataQualityError, match="TotalCharges"):
        clean_customers(raw_customers)


def test_churn_becomes_binary(raw_customers):
    df = clean_customers(raw_customers)
    assert df["Churn"].tolist() == [1, 0, 0, 0, 1, 0]


def test_unexpected_churn_label_is_an_error(raw_customers):
    raw_customers.loc[0, "Churn"] = "Maybe"
    with pytest.raises(DataQualityError, match="Maybe"):
        clean_customers(raw_customers)


def test_missing_column_raises_schema_error_listing_it(raw_customers):
    with pytest.raises(SchemaError) as excinfo:
        clean_customers(raw_customers.drop(columns=["tenure"]))
    assert excinfo.value.missing_columns == ["tenure"]


def test_cleaning_does_not_modify_the_input(raw_customers):
    before = raw_customers.copy()
    clean_customers(raw_customers)
    pd.testing.assert_frame_equal(raw_customers, before)


def test_scoring_batches_without_target_are_allowed(raw_customers):
    df = clean_customers(raw_customers.drop(columns=["Churn"]))
    assert "Churn" not in df.columns


def test_in_memory_loader_gives_same_result_as_cleaning(raw_customers):
    pd.testing.assert_frame_equal(
        InMemoryLoader(raw_customers).load(), clean_customers(raw_customers)
    )


def test_real_dataset_loads_cleanly(data_path):
    df = load_customers(data_path)
    assert len(df) == 7043
    assert df["TotalCharges"].notna().all()
    assert set(df["Churn"].unique()) == {0, 1}


def test_split_features_target(raw_customers):
    X, y = split_features_target(clean_customers(raw_customers))
    assert "Churn" not in X.columns
    assert len(X) == len(y) == 6

"""Tests for the churn package.

Students add tests here during notebook 11 (Testing with pytest)
and the capstone (notebook 12).
"""

import pandas as pd


# --- The function under test ---
def calculate_class_balance(y: pd.Series) -> dict:
    """Return class counts and proportions."""
    counts = y.value_counts()
    props = y.value_counts(normalize=True)
    return {"counts": counts.to_dict(), "proportions": props.to_dict()}


def test_class_balance_basic():
    # Setting up
    y = pd.Series([0, 0, 0, 1, 1])

    # Making the experiment
    result = calculate_class_balance(y)

    # Comparing
    assert result["counts"][0] == 3
    assert result["counts"][1] == 2
    assert result["proportions"][0] == 0.7
    # assert abs(result["proportions"][0] - 0.6) < 1e-9


def test_class_balance_equal():
    y = pd.Series([0, 1, 0, 1])
    result = calculate_class_balance(y)
    assert result["proportions"][0] == result["proportions"][1]


def test_class_balance_all_same_class():
    y = pd.Series([1, 1, 1])
    result = calculate_class_balance(y)
    assert result["proportions"][1] == 1.0
    assert 0 not in result["counts"]

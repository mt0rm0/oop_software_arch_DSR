"""Shared fixtures. pytest discovers this file automatically."""

from pathlib import Path

import pandas as pd
import pytest

DATA_PATH = Path(__file__).resolve().parents[1] / "data" / "raw" / "telco_churn.csv"


@pytest.fixture
def raw_customers() -> pd.DataFrame:
    """Six hand-written customers in the raw export format, including the tricky cases."""
    return pd.DataFrame(
        {
            "customerID": ["A-1", "A-2", "A-3", "A-4", "A-5", "A-6"],
            "SeniorCitizen": [0, 1, 0, 0, 1, 0],
            "tenure": [1, 0, 45, 12, 3, 70],
            "Contract": [
                "Month-to-month",
                "Month-to-month",
                "Two year",
                "One year",
                "Month-to-month",
                "Two year",
            ],
            "InternetService": ["Fiber optic", "DSL", "No", "DSL", "Fiber optic", "DSL"],
            "PaymentMethod": [
                "Electronic check",
                "Mailed check",
                "Bank transfer (automatic)",
                "Credit card (automatic)",
                "Electronic check",
                "Bank transfer (automatic)",
            ],
            "PaperlessBilling": ["Yes", "No", "No", "Yes", "Yes", "No"],
            "OnlineSecurity": ["No", "No", "No internet service", "Yes", "No", "Yes"],
            "TechSupport": ["No", "Yes", "No internet service", "No", "No", "Yes"],
            "MonthlyCharges": [70.7, 25.0, 19.9, 55.3, 89.1, 60.0],
            # exported as text; blank for the customer who joined this month
            "TotalCharges": ["70.7", " ", "895.5", "663.6", "267.3", "4200.0"],
            "Churn": ["Yes", "No", "No", "No", "Yes", "No"],
        }
    )


@pytest.fixture(scope="session")
def data_path() -> Path:
    return DATA_PATH


@pytest.fixture(scope="session")
def telco_raw() -> pd.DataFrame:
    """The real dataset, read once per test session."""
    return pd.read_csv(DATA_PATH)

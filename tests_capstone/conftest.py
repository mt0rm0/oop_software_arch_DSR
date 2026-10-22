"""Acceptance tests for the capstone package.

Run them with:

    uv run pytest tests_capstone                 # everything
    uv run pytest tests_capstone/test_1_core.py  # one level at a time

They test your package `churn_capstone`. Trainers can check that the tests are
achievable by running them against the reference solution:

    CAPSTONE_PACKAGE=churn uv run pytest tests_capstone
"""

import importlib
import os
from pathlib import Path
from types import ModuleType

import pandas as pd
import pytest

PACKAGE = os.environ.get("CAPSTONE_PACKAGE", "churn_capstone")
DATA_PATH = Path(__file__).resolve().parents[1] / "data" / "raw" / "telco_churn.csv"


def _module(name: str) -> ModuleType:
    try:
        return importlib.import_module(f"{PACKAGE}.{name}")
    except ModuleNotFoundError as exc:
        if exc.name != f"{PACKAGE}.{name}":
            raise
    # outside the except block, so pytest shows only this message
    pytest.fail(f"Create the module src/{PACKAGE}/{name}.py", pytrace=False)


def _attr(module: str, name: str):
    mod = _module(module)
    if not hasattr(mod, name):
        pytest.fail(f"{PACKAGE}.{module} has no '{name}' yet", pytrace=False)
    return getattr(mod, name)


@pytest.fixture
def get():
    """get("model", "ChurnModel") returns that object or fails with a helpful message."""
    return _attr


@pytest.fixture(scope="session")
def data_path() -> Path:
    return DATA_PATH


@pytest.fixture(scope="session")
def raw() -> pd.DataFrame:
    return pd.read_csv(DATA_PATH)


@pytest.fixture
def write_csv(tmp_path):
    """Write a DataFrame to a temporary CSV and return its path."""

    def _write(df: pd.DataFrame) -> Path:
        path = tmp_path / "customers.csv"
        df.to_csv(path, index=False)
        return path

    return _write

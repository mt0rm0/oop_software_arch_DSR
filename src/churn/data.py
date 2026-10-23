"""Data access layer: load the raw customer table and make it safe to use.

Nothing in here knows about models. The rest of the package asks a *loader* for
a clean DataFrame and does not care whether it came from a CSV file, a database
or a test fixture.
"""

from __future__ import annotations

import logging
from collections.abc import Iterable
from pathlib import Path
from typing import Protocol

import pandas as pd

from churn.errors import DataQualityError, SchemaError

logger = logging.getLogger(__name__)

ID_COLUMN = "customerID"
TARGET_COLUMN = "Churn"
REQUIRED_COLUMNS = (ID_COLUMN, "tenure", "MonthlyCharges", "TotalCharges", "Contract")


class CustomerLoader(Protocol):
    """Anything that can provide a clean customer table."""

    def load(self) -> pd.DataFrame: ...


def validate_schema(df: pd.DataFrame, required: Iterable[str] = REQUIRED_COLUMNS) -> None:
    """Raise SchemaError if any required column is missing."""
    missing = [col for col in required if col not in df.columns]
    if missing:
        raise SchemaError(missing)


def clean_customers(raw: pd.DataFrame) -> pd.DataFrame:
    """Turn the raw export into a table with correct types.

    - ``customerID`` becomes the index.
    - ``TotalCharges`` is exported as text and is blank for customers who joined
      this month (tenure 0). They have not been billed yet, so the correct value
      is 0, not "missing".
    - ``Churn`` (if present) becomes 1/0, so metrics can be computed directly.

    Raises:
        SchemaError: If required columns are missing.
        DataQualityError: If TotalCharges is blank for a customer with tenure > 0
            or Churn contains values other than "Yes"/"No".
    """
    validate_schema(raw)
    df = raw.copy().set_index(ID_COLUMN)

    total = pd.to_numeric(df["TotalCharges"].astype(str).str.strip(), errors="coerce")
    new_customers = df["tenure"] == 0
    unexplained = total.isna() & ~new_customers
    if unexplained.any():
        raise DataQualityError(
            f"TotalCharges is missing or not numeric for {int(unexplained.sum())} "
            f"customers with tenure > 0, e.g. {list(df.index[unexplained][:3])}"
        )
    df["TotalCharges"] = total.fillna(0.0)
    if new_customers.any():
        logger.debug("Set TotalCharges=0 for %d new customers", int(new_customers.sum()))

    if TARGET_COLUMN in df.columns:
        unknown = set(df[TARGET_COLUMN].unique()) - {"Yes", "No"}
        if unknown:
            raise DataQualityError(f"Unexpected values in {TARGET_COLUMN}: {sorted(unknown)}")
        df[TARGET_COLUMN] = (df[TARGET_COLUMN] == "Yes").astype(int)

    return df


class CSVCustomerLoader:
    """Load customers from a CSV export."""

    def __init__(self, path: str | Path) -> None:
        self.path = Path(path)

    def load(self) -> pd.DataFrame:
        logger.info("Loading customers from %s", self.path)
        df = clean_customers(pd.read_csv(self.path))
        logger.info("Loaded %d customers", len(df))
        return df

    def __repr__(self) -> str:
        return f"CSVCustomerLoader(path={str(self.path)!r})"


class InMemoryLoader:
    """Serve an existing DataFrame. Handy in tests and notebooks."""

    def __init__(self, raw: pd.DataFrame) -> None:
        self._raw = raw

    def load(self) -> pd.DataFrame:
        return clean_customers(self._raw)

    def __repr__(self) -> str:
        return f"InMemoryLoader(rows={len(self._raw)})"


def load_customers(path: str | Path) -> pd.DataFrame:
    """Shortcut for ``CSVCustomerLoader(path).load()``."""
    return CSVCustomerLoader(path).load()


def split_features_target(
    df: pd.DataFrame, target: str = TARGET_COLUMN
) -> tuple[pd.DataFrame, pd.Series]:
    """Separate the label column from the features."""
    validate_schema(df, [target])
    return df.drop(columns=[target]), df[target]

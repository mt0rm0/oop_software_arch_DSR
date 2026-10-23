"""Preprocessing steps that learn from training data and replay on new data.

Every step follows the same contract (the Transformer ABC): ``fit`` learns
parameters from the training data only, ``transform`` applies exactly those
parameters to any later batch. This is what the warm-up notebook got wrong: it
re-fitted its LabelEncoder on each new batch, so the same customer could be
encoded differently depending on who else was in the file.

scikit-learn ships production-grade versions of these (OneHotEncoder,
StandardScaler, ColumnTransformer, Pipeline). We keep small hand-written ones
because the point of the workshop is to understand how such classes are built.
"""

from __future__ import annotations

import logging
from abc import ABC, abstractmethod
from collections.abc import Sequence
from typing import Self

import pandas as pd

from churn.errors import NotFittedError

logger = logging.getLogger(__name__)


class Transformer(ABC):
    """Contract for a preprocessing step.

    Subclasses implement ``_fit`` and ``_transform``. The public ``fit`` and
    ``transform`` methods add the bookkeeping every step needs (fitted flag,
    clear error when used too early), so subclasses cannot forget it.
    """

    def __init__(self) -> None:
        self._fitted = False

    @property
    def is_fitted(self) -> bool:
        return self._fitted

    def fit(self, X: pd.DataFrame) -> Self:
        self._fit(X)
        self._fitted = True
        return self

    def transform(self, X: pd.DataFrame) -> pd.DataFrame:
        if not self._fitted:
            raise NotFittedError(f"{type(self).__name__} must be fitted before transform()")
        return self._transform(X)

    def fit_transform(self, X: pd.DataFrame) -> pd.DataFrame:
        return self.fit(X).transform(X)

    @abstractmethod
    def _fit(self, X: pd.DataFrame) -> None:
        """Learn parameters from training data."""

    @abstractmethod
    def _transform(self, X: pd.DataFrame) -> pd.DataFrame:
        """Apply the learned parameters. Must not modify X in place."""

    def __repr__(self) -> str:
        state = "fitted" if self._fitted else "not fitted"
        return f"{type(self).__name__}({state})"


class OneHotEncoder(Transformer):
    """One column per category seen during fit.

    The output always has the same columns in the same order, no matter which
    categories appear in the batch being transformed. A category that was never
    seen during fit is encoded as all zeros and logged as a warning.
    """

    def __init__(self, columns: Sequence[str]) -> None:
        super().__init__()
        self.columns = list(columns)
        self._categories: dict[str, list[str]] = {}

    @property
    def categories(self) -> dict[str, list[str]]:
        """Categories learned per column (a copy, so callers cannot corrupt the encoder)."""
        return {col: list(cats) for col, cats in self._categories.items()}

    @property
    def output_columns(self) -> list[str]:
        return [f"{col}={cat}" for col, cats in self._categories.items() for cat in cats]

    def _fit(self, X: pd.DataFrame) -> None:
        self._categories = {col: sorted(X[col].astype(str).unique()) for col in self.columns}

    def _transform(self, X: pd.DataFrame) -> pd.DataFrame:
        out = X.drop(columns=self.columns)
        for col, cats in self._categories.items():
            values = X[col].astype(str)
            unseen = ~values.isin(cats)
            if unseen.any():
                logger.warning(
                    "%s: %d rows with unseen categories %s, encoded as all zeros",
                    col,
                    int(unseen.sum()),
                    sorted(values[unseen].unique()),
                )
            for cat in cats:
                out[f"{col}={cat}"] = (values == cat).astype(int)
        return out


class Standardizer(Transformer):
    """Scale numeric columns to mean 0 and standard deviation 1 (training statistics)."""

    def __init__(self, columns: Sequence[str]) -> None:
        super().__init__()
        self.columns = list(columns)
        self._mean = pd.Series(dtype=float)
        self._std = pd.Series(dtype=float)

    def _fit(self, X: pd.DataFrame) -> None:
        self._mean = X[self.columns].mean()
        # a constant column would divide by zero; leave it centred but unscaled
        self._std = X[self.columns].std().replace(0, 1.0)

    def _transform(self, X: pd.DataFrame) -> pd.DataFrame:
        scaled = {col: (X[col] - self._mean[col]) / self._std[col] for col in self.columns}
        return X.assign(**scaled)


class FeaturePipeline(Transformer):
    """Run several transformers in sequence and keep only the model inputs.

    A FeaturePipeline is itself a Transformer, so it can be used anywhere a single
    step can (the Composite pattern).
    """

    def __init__(self, steps: Sequence[Transformer], keep: Sequence[str] | None = None) -> None:
        super().__init__()
        self.steps = list(steps)
        self.keep = list(keep) if keep is not None else None
        self._output_columns: list[str] = []

    @property
    def output_columns(self) -> list[str]:
        return list(self._output_columns)

    def _fit(self, X: pd.DataFrame) -> None:
        current = self._select(X)
        for step in self.steps:
            current = step.fit_transform(current)
        self._output_columns = list(current.columns)

    def _transform(self, X: pd.DataFrame) -> pd.DataFrame:
        current = self._select(X)
        for step in self.steps:
            current = step.transform(current)
        return current[self._output_columns]

    def _select(self, X: pd.DataFrame) -> pd.DataFrame:
        return X[self.keep] if self.keep is not None else X

    def __repr__(self) -> str:
        inner = ", ".join(repr(step) for step in self.steps)
        return f"FeaturePipeline([{inner}])"

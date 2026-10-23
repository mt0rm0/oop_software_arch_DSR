"""The churn model: preprocessing + estimator + decision threshold.

ChurnModel *has* a feature pipeline and *has* an estimator (composition) instead
of inheriting from either. That keeps each piece replaceable: any object with
``fit``/``predict_proba`` works as the estimator, including scikit-learn models.
"""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Any, Protocol, Self

import joblib
import numpy as np
import numpy.typing as npt
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression

from churn.config import ExperimentConfig
from churn.errors import ConfigError, NotFittedError, SchemaError
from churn.features import FeaturePipeline, OneHotEncoder, Standardizer

logger = logging.getLogger(__name__)


class ProbabilisticClassifier(Protocol):
    """Structural type for the estimator inside ChurnModel (sklearn classifiers fit)."""

    def fit(self, X: Any, y: Any) -> Any: ...

    def predict_proba(self, X: Any) -> npt.NDArray[np.float64]: ...


def build_estimator(
    name: str, params: dict[str, Any], random_state: int
) -> ProbabilisticClassifier:
    """Create an unfitted estimator from its config name."""
    if name == "logistic_regression":
        return LogisticRegression(max_iter=1000, random_state=random_state, **params)
    if name == "random_forest":
        return RandomForestClassifier(random_state=random_state, **params)
    raise ConfigError(f"Unknown model {name!r}")


def build_features(config: ExperimentConfig) -> FeaturePipeline:
    return FeaturePipeline(
        steps=[
            OneHotEncoder(config.categorical_features),
            Standardizer(config.numeric_features),
        ],
        keep=list(config.features),
    )


class ChurnModel:
    """Predict which customers are likely to cancel their contract.

    Example:
        >>> model = ChurnModel().fit(X_train, y_train)      # doctest: +SKIP
        >>> flagged = model.predict(next_month_customers)   # doctest: +SKIP
    """

    def __init__(
        self,
        config: ExperimentConfig | None = None,
        estimator: ProbabilisticClassifier | None = None,
    ) -> None:
        self.config = config or ExperimentConfig()
        self._features = build_features(self.config)
        self._estimator = estimator or build_estimator(
            self.config.model, self.config.model_params, self.config.random_state
        )
        self._threshold = self.config.threshold
        self._fitted = False

    @property
    def threshold(self) -> float:
        return self._threshold

    @threshold.setter
    def threshold(self, value: float) -> None:
        # Changing the threshold after training is legitimate (it is a business decision),
        # but it must stay a probability.
        if not 0 < value < 1:
            raise ValueError(f"threshold must be between 0 and 1, got {value}")
        self._threshold = value

    @property
    def is_fitted(self) -> bool:
        return self._fitted

    @property
    def feature_names(self) -> list[str]:
        """Model input columns after preprocessing (available after fit)."""
        self._require_fitted()
        return self._features.output_columns

    def fit(self, X: pd.DataFrame, y: pd.Series) -> Self:
        self._check_columns(X)
        logger.info("Fitting %s on %d customers", type(self._estimator).__name__, len(X))
        X_model = self._features.fit_transform(X)
        self._estimator.fit(X_model, np.asarray(y))
        self._fitted = True
        return self

    def predict_proba(self, X: pd.DataFrame) -> npt.NDArray[np.float64]:
        """Probability of churn for each customer."""
        self._require_fitted()
        self._check_columns(X)
        X_model = self._features.transform(X)
        return self._estimator.predict_proba(X_model)[:, 1]

    def predict(self, X: pd.DataFrame) -> npt.NDArray[np.int_]:
        """1 for customers whose churn probability reaches the threshold, else 0."""
        return (self.predict_proba(X) >= self._threshold).astype(int)

    def save(self, path: str | Path) -> Path:
        self._require_fitted()
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)
        joblib.dump(self, path)
        logger.info("Saved model to %s", path)
        return path

    @classmethod
    def load(cls, path: str | Path) -> ChurnModel:
        obj = joblib.load(path)
        if not isinstance(obj, cls):
            raise TypeError(f"{path} does not contain a {cls.__name__}")
        return obj

    def _require_fitted(self) -> None:
        if not self._fitted:
            raise NotFittedError("ChurnModel must be fitted before it can predict")

    def _check_columns(self, X: pd.DataFrame) -> None:
        missing = [col for col in self.config.features if col not in X.columns]
        if missing:
            raise SchemaError(missing)

    def __repr__(self) -> str:
        state = "fitted" if self._fitted else "not fitted"
        return (
            f"ChurnModel(estimator={type(self._estimator).__name__}, "
            f"threshold={self._threshold}, {state})"
        )

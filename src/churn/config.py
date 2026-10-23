"""Experiment configuration.

A frozen dataclass replaces the loose constants and magic numbers of the warm-up
notebook. Validation happens once, when the object is created, so a typo in a
config file fails immediately instead of halfway through training.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from churn.errors import ConfigError

SUPPORTED_MODELS = ("logistic_regression", "random_forest")


@dataclass(frozen=True)
class ExperimentConfig:
    """Everything needed to reproduce one training run.

    Attributes:
        data_path: CSV file with the raw customer table.
        numeric_features: Columns used as numbers.
        categorical_features: Columns one-hot encoded before training.
        target: Name of the label column (1 = customer churned).
        test_size: Fraction of customers held out for evaluation.
        random_state: Seed for the split and the estimator.
        model: Estimator family, one of SUPPORTED_MODELS.
        model_params: Extra keyword arguments passed to the estimator.
        threshold: Churn probability above which a customer is flagged.
    """

    data_path: Path = Path("data/raw/telco_churn.csv")
    numeric_features: tuple[str, ...] = (
        "tenure",
        "MonthlyCharges",
        "TotalCharges",
        "SeniorCitizen",
    )
    categorical_features: tuple[str, ...] = (
        "Contract",
        "InternetService",
        "PaymentMethod",
        "PaperlessBilling",
        "OnlineSecurity",
        "TechSupport",
    )
    target: str = "Churn"
    test_size: float = 0.2
    random_state: int = 42
    model: str = "logistic_regression"
    model_params: dict[str, Any] = field(default_factory=dict)
    threshold: float = 0.5

    def __post_init__(self) -> None:
        # frozen=True blocks normal assignment, so normalise through object.__setattr__
        object.__setattr__(self, "data_path", Path(self.data_path))
        object.__setattr__(self, "numeric_features", tuple(self.numeric_features))
        object.__setattr__(self, "categorical_features", tuple(self.categorical_features))

        if not 0 < self.test_size < 1:
            raise ConfigError(f"test_size must be between 0 and 1, got {self.test_size}")
        if not 0 < self.threshold < 1:
            raise ConfigError(f"threshold must be between 0 and 1, got {self.threshold}")
        if self.model not in SUPPORTED_MODELS:
            raise ConfigError(f"model must be one of {SUPPORTED_MODELS}, got {self.model!r}")
        overlap = set(self.numeric_features) & set(self.categorical_features)
        if overlap:
            raise ConfigError(f"Columns listed as both numeric and categorical: {sorted(overlap)}")
        if self.target in self.features:
            raise ConfigError(f"The target {self.target!r} must not be used as a feature")

    @property
    def features(self) -> tuple[str, ...]:
        """All input columns, numeric first."""
        return self.numeric_features + self.categorical_features

    @classmethod
    def from_json(cls, path: str | Path) -> ExperimentConfig:
        """Create a config from a JSON file. Unknown keys raise ConfigError."""
        raw = json.loads(Path(path).read_text())
        try:
            return cls(**raw)
        except TypeError as exc:  # unexpected keyword argument, i.e. a typo in the file
            raise ConfigError(f"Invalid config file {path}: {exc}") from exc

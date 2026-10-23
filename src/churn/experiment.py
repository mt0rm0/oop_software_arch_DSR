"""Application layer: wire data, model and evaluation into one reproducible run."""

from __future__ import annotations

import logging
from dataclasses import dataclass

from sklearn.metrics import roc_auc_score
from sklearn.model_selection import train_test_split

from churn.config import ExperimentConfig
from churn.data import CSVCustomerLoader, CustomerLoader, split_features_target
from churn.evaluation import ConfusionMatrix, RetentionCost
from churn.model import ChurnModel

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class ExperimentResult:
    """Holdout metrics of one run."""

    confusion: ConfusionMatrix
    roc_auc: float
    cost: float
    cost_do_nothing: float

    @property
    def savings(self) -> float:
        """Money saved compared with not running any retention campaign."""
        return self.cost_do_nothing - self.cost

    def summary(self) -> str:
        cm = self.confusion
        return (
            f"precision={cm.precision:.2f} recall={cm.recall:.2f} f1={cm.f1:.2f} "
            f"roc_auc={self.roc_auc:.3f} savings={self.savings:,.0f}"
        )


def run_experiment(
    config: ExperimentConfig,
    loader: CustomerLoader | None = None,
    cost: RetentionCost | None = None,
) -> tuple[ChurnModel, ExperimentResult]:
    """Train on a stratified split of the data and evaluate on the holdout.

    Args:
        config: What to train and how.
        loader: Where the customers come from. Defaults to the CSV in the config;
            tests pass an InMemoryLoader instead (dependency injection).
        cost: Business cost model used for the savings figure.
    """
    loader = loader or CSVCustomerLoader(config.data_path)
    cost = cost or RetentionCost()

    customers = loader.load()
    X, y = split_features_target(customers, config.target)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=config.test_size, random_state=config.random_state, stratify=y
    )

    model = ChurnModel(config).fit(X_train, y_train)
    y_pred = model.predict(X_test)

    result = ExperimentResult(
        confusion=ConfusionMatrix.from_predictions(y_test, y_pred),
        roc_auc=float(roc_auc_score(y_test, model.predict_proba(X_test))),
        cost=cost(y_test, y_pred),
        cost_do_nothing=cost.do_nothing(y_test),
    )
    logger.info("Holdout: %s", result.summary())
    return model, result

"""Evaluate churn predictions in statistical and in business terms."""

from __future__ import annotations

from collections.abc import Iterator
from dataclasses import dataclass

import numpy as np
import numpy.typing as npt


@dataclass(frozen=True)
class ConfusionMatrix:
    """Counts of a binary classifier's hits and misses (1 = churn).

    Two matrices can be added: the result is the pooled matrix, e.g. over all
    cross-validation folds or over several monthly scoring batches.
    """

    tn: int
    fp: int
    fn: int
    tp: int

    @classmethod
    def from_predictions(cls, y_true: npt.ArrayLike, y_pred: npt.ArrayLike) -> ConfusionMatrix:
        t = np.asarray(y_true).astype(int)
        p = np.asarray(y_pred).astype(int)
        if t.shape != p.shape:
            raise ValueError(f"y_true and y_pred differ in shape: {t.shape} vs {p.shape}")
        return cls(
            tn=int(((t == 0) & (p == 0)).sum()),
            fp=int(((t == 0) & (p == 1)).sum()),
            fn=int(((t == 1) & (p == 0)).sum()),
            tp=int(((t == 1) & (p == 1)).sum()),
        )

    @property
    def n(self) -> int:
        return self.tn + self.fp + self.fn + self.tp

    @property
    def accuracy(self) -> float:
        return _safe_div(self.tp + self.tn, self.n)

    @property
    def precision(self) -> float:
        """Of the customers we flagged, how many really churned?"""
        return _safe_div(self.tp, self.tp + self.fp)

    @property
    def recall(self) -> float:
        """Of the customers who churned, how many did we flag?"""
        return _safe_div(self.tp, self.tp + self.fn)

    @property
    def f1(self) -> float:
        return _safe_div(2 * self.precision * self.recall, self.precision + self.recall)

    def __add__(self, other: object) -> ConfusionMatrix:
        if not isinstance(other, ConfusionMatrix):
            return NotImplemented
        return ConfusionMatrix(
            self.tn + other.tn, self.fp + other.fp, self.fn + other.fn, self.tp + other.tp
        )

    def __radd__(self, other: object) -> ConfusionMatrix:
        # sum() starts from 0, so 0 + matrix must work
        if other == 0:
            return self
        return self.__add__(other)

    def __iter__(self) -> Iterator[int]:
        """Allow ``tn, fp, fn, tp = cm`` (same order as sklearn's confusion_matrix().ravel())."""
        return iter((self.tn, self.fp, self.fn, self.tp))

    def __str__(self) -> str:
        return (
            f"              pred=0  pred=1\n"
            f"actual=0  {self.tn:>8} {self.fp:>7}\n"
            f"actual=1  {self.fn:>8} {self.tp:>7}"
        )


@dataclass(frozen=True)
class RetentionCost:
    """Money lost to churn when a retention team acts on the model's flags.

    Every flagged customer receives an offer that costs ``offer_cost``. A churner
    who receives the offer stays with probability ``acceptance_rate``. Every
    churner who leaves costs ``customer_value`` (the margin we would have earned
    over the next year).

    The default figures are illustrative assumptions, not facts about the
    dataset. Plug in your own business numbers.
    """

    offer_cost: float = 50.0
    customer_value: float = 600.0
    acceptance_rate: float = 0.3

    def __call__(self, y_true: npt.ArrayLike, y_pred: npt.ArrayLike) -> float:
        tn, fp, fn, tp = ConfusionMatrix.from_predictions(y_true, y_pred)
        offers = (tp + fp) * self.offer_cost
        lost_despite_offer = tp * (1 - self.acceptance_rate) * self.customer_value
        lost_unflagged = fn * self.customer_value
        return float(offers + lost_despite_offer + lost_unflagged)

    def do_nothing(self, y_true: npt.ArrayLike) -> float:
        """Cost if nobody gets an offer: every churner is lost."""
        return float(np.asarray(y_true).astype(int).sum() * self.customer_value)


def _safe_div(num: float, den: float) -> float:
    return num / den if den else 0.0

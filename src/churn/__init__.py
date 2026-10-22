"""churn: reference implementation of the workshop's churn prediction project.

This is the "after" picture of notebook 00 (the warm-up). Each module shows one
idea from the workshop:

    config.py      dataclass with validation (notebook 07)
    errors.py      custom exception hierarchy (notebook 09)
    data.py        data access layer, Protocol, dependency injection (08, 05)
    features.py    ABC, inheritance, encapsulation, composite (02, 04)
    model.py       composition, properties, persistence (08, 04)
    evaluation.py  dunder methods, callable objects (03)
    experiment.py  application layer (08)
    __main__.py    command line entry point and logging setup (09, 11)

Read it after you have tried the capstone (notebook 12) yourself.
"""

from churn.config import ExperimentConfig
from churn.data import CSVCustomerLoader, InMemoryLoader, load_customers
from churn.errors import ChurnError
from churn.evaluation import ConfusionMatrix, RetentionCost
from churn.experiment import ExperimentResult, run_experiment
from churn.model import ChurnModel

__version__ = "1.0.0"

__all__ = [
    "ChurnError",
    "ChurnModel",
    "ConfusionMatrix",
    "CSVCustomerLoader",
    "ExperimentConfig",
    "ExperimentResult",
    "InMemoryLoader",
    "RetentionCost",
    "load_customers",
    "run_experiment",
]

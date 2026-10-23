"""Exceptions raised by the churn package.

All of them inherit from ChurnError, so a caller can handle "anything that went
wrong inside churn" with a single ``except ChurnError`` while still being able to
react to specific problems (for example a missing column) individually.
"""


class ChurnError(Exception):
    """Base class for every error raised by this package."""


class ConfigError(ChurnError, ValueError):
    """An experiment configuration is invalid.

    Also a ValueError, so code that only knows about built-in exceptions still
    catches it.
    """


class DataValidationError(ChurnError):
    """Input data does not meet the expectations of the pipeline."""


class SchemaError(DataValidationError):
    """Required columns are missing from a DataFrame."""

    def __init__(self, missing_columns: list[str]) -> None:
        self.missing_columns = missing_columns
        super().__init__(f"Missing required columns: {missing_columns}")


class DataQualityError(DataValidationError):
    """Values are present but not usable (wrong type, out of range, too many gaps)."""


class NotFittedError(ChurnError, RuntimeError):
    """A model or transformer was used before ``fit()`` was called."""

import json

import pytest

from churn.config import ExperimentConfig
from churn.errors import ConfigError


def test_defaults_are_valid():
    config = ExperimentConfig()
    assert config.test_size == 0.2
    assert "Contract" in config.features


@pytest.mark.parametrize(
    "kwargs",
    [
        {"test_size": 0.0},
        {"test_size": 1.5},
        {"threshold": 1.0},
        {"model": "xgboost"},
        {"numeric_features": ("tenure",), "categorical_features": ("tenure",)},
        {"categorical_features": ("Churn",)},
    ],
)
def test_invalid_values_are_rejected(kwargs):
    with pytest.raises(ConfigError):
        ExperimentConfig(**kwargs)


def test_config_error_is_also_a_value_error():
    with pytest.raises(ValueError):
        ExperimentConfig(test_size=2)


def test_config_is_immutable():
    config = ExperimentConfig()
    with pytest.raises(AttributeError):
        config.test_size = 0.5


def test_lists_are_normalised_to_tuples():
    config = ExperimentConfig(numeric_features=["tenure"], categorical_features=["Contract"])
    assert config.features == ("tenure", "Contract")


def test_from_json(tmp_path):
    path = tmp_path / "config.json"
    path.write_text(json.dumps({"model": "random_forest", "threshold": 0.3}))
    config = ExperimentConfig.from_json(path)
    assert config.model == "random_forest"
    assert config.threshold == 0.3


def test_typo_in_json_is_reported(tmp_path):
    path = tmp_path / "config.json"
    path.write_text(json.dumps({"tresh0ld": 0.3}))
    with pytest.raises(ConfigError, match="tresh0ld"):
        ExperimentConfig.from_json(path)

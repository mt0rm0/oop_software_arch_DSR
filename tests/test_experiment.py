"""End-to-end tests: the whole pipeline, with the data source injected."""

import pytest

from churn.__main__ import main
from churn.config import ExperimentConfig
from churn.data import InMemoryLoader
from churn.experiment import run_experiment


@pytest.fixture(scope="module")
def result(telco_raw):
    _, result = run_experiment(ExperimentConfig(), loader=InMemoryLoader(telco_raw))
    return result


def test_model_is_clearly_better_than_chance(result):
    assert result.roc_auc > 0.75


def test_model_finds_most_churners_at_default_threshold(result):
    # threshold 0.5 on a 27% churn rate: we expect to catch at least half of the churners
    assert result.confusion.recall > 0.5


def test_holdout_has_the_configured_size(result, telco_raw):
    assert result.confusion.n == pytest.approx(0.2 * len(telco_raw), abs=1)


def test_runs_are_reproducible(telco_raw):
    loader = InMemoryLoader(telco_raw)
    _, first = run_experiment(ExperimentConfig(), loader=loader)
    _, second = run_experiment(ExperimentConfig(), loader=loader)
    assert first == second


def test_cli_end_to_end(tmp_path, capsys, data_path):
    config = tmp_path / "config.json"
    config.write_text(f'{{"data_path": "{data_path}", "threshold": 0.3}}')
    exit_code = main(["--config", str(config), "--save", str(tmp_path / "m.joblib")])
    assert exit_code == 0
    assert "roc_auc" in capsys.readouterr().out
    assert (tmp_path / "m.joblib").exists()


def test_cli_reports_bad_config_without_crashing(tmp_path):
    config = tmp_path / "config.json"
    config.write_text('{"test_size": 3}')
    assert main(["--config", str(config)]) == 1

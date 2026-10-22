import pandas as pd
import pytest

from churn.errors import NotFittedError
from churn.features import FeaturePipeline, OneHotEncoder, Standardizer, Transformer


@pytest.fixture
def contracts() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "Contract": ["Month-to-month", "One year", "Two year", "Month-to-month"],
            "tenure": [1, 20, 50, 3],
        }
    )


def test_transformer_is_abstract():
    with pytest.raises(TypeError):
        Transformer()


def test_one_hot_creates_one_column_per_category(contracts):
    out = OneHotEncoder(["Contract"]).fit_transform(contracts)
    assert out.columns.tolist() == [
        "tenure",
        "Contract=Month-to-month",
        "Contract=One year",
        "Contract=Two year",
    ]
    assert out["Contract=Month-to-month"].tolist() == [1, 0, 0, 1]


def test_one_hot_columns_do_not_depend_on_the_batch(contracts):
    """The warm-up bug: a batch with fewer categories must not change the encoding."""
    encoder = OneHotEncoder(["Contract"]).fit(contracts)
    single_category_batch = contracts[contracts["Contract"] == "Two year"]
    out = encoder.transform(single_category_batch)
    assert out.columns.tolist() == encoder.transform(contracts).columns.tolist()
    assert out.iloc[0]["Contract=Two year"] == 1


def test_unseen_category_is_all_zeros_and_logged(contracts, caplog):
    encoder = OneHotEncoder(["Contract"]).fit(contracts)
    out = encoder.transform(pd.DataFrame({"Contract": ["Three year"], "tenure": [5]}))
    assert out.filter(like="Contract=").sum(axis=1).tolist() == [0]
    assert "Three year" in caplog.text


def test_learned_categories_cannot_be_changed_from_outside(contracts):
    encoder = OneHotEncoder(["Contract"]).fit(contracts)
    encoder.categories["Contract"].append("Hacked")
    assert "Hacked" not in encoder.categories["Contract"]


@pytest.mark.parametrize("step", [OneHotEncoder(["Contract"]), Standardizer(["tenure"])])
def test_transform_before_fit_raises(step, contracts):
    with pytest.raises(NotFittedError):
        step.transform(contracts)


def test_standardizer_uses_training_statistics_only(contracts):
    scaler = Standardizer(["tenure"]).fit(contracts)
    train_out = scaler.transform(contracts)
    assert train_out["tenure"].mean() == pytest.approx(0.0)
    assert train_out["tenure"].std() == pytest.approx(1.0)

    new_batch = pd.DataFrame({"Contract": ["One year"], "tenure": [contracts["tenure"].mean()]})
    assert scaler.transform(new_batch)["tenure"].iloc[0] == pytest.approx(0.0)


def test_standardizer_handles_constant_column():
    X = pd.DataFrame({"tenure": [5, 5, 5]})
    assert Standardizer(["tenure"]).fit_transform(X)["tenure"].tolist() == [0.0, 0.0, 0.0]


def test_transform_does_not_modify_input(contracts):
    before = contracts.copy()
    FeaturePipeline([OneHotEncoder(["Contract"]), Standardizer(["tenure"])]).fit_transform(
        contracts
    )
    pd.testing.assert_frame_equal(contracts, before)


def test_pipeline_keeps_only_requested_columns(contracts):
    contracts["notes"] = "irrelevant"
    pipeline = FeaturePipeline([OneHotEncoder(["Contract"])], keep=["Contract", "tenure"])
    out = pipeline.fit_transform(contracts)
    assert "notes" not in out.columns
    assert pipeline.output_columns == out.columns.tolist()


def test_pipeline_is_a_transformer():
    assert isinstance(FeaturePipeline([]), Transformer)

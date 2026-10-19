# IndustrialSense AI - ML Baseline Tests

from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

from src.ml_baseline import create_baseline_pipeline


def test_create_baseline_pipeline():
    """Verify the expected ML pipeline structure."""

    model = create_baseline_pipeline()

    assert isinstance(model, Pipeline)

    assert list(model.named_steps) == [
        "scaler",
        "classifier",
    ]

    assert isinstance(
        model.named_steps["scaler"],
        StandardScaler,
    )

    assert isinstance(
        model.named_steps["classifier"],
        LogisticRegression,
    )

    assert model.named_steps["classifier"].max_iter == 1000
    assert model.named_steps["classifier"].random_state == 42
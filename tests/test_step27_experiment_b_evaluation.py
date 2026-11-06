import pytest

from run_step27_experiment_b_evaluation import validate_evaluation_records


def valid_records():
    """Synthetic records for the frozen Evaluation split."""
    return [
        {"recording_id": 100, "label": 0},
        {"recording_id": 121, "label": 1},
    ]


def test_valid_evaluation_records():
    validate_evaluation_records(valid_records())


def test_reject_empty_evaluation():
    with pytest.raises(ValueError, match="Empty evaluation"):
        validate_evaluation_records([])


def test_reject_missing_ball_fault():
    records = [{"recording_id": 100, "label": 0}]

    with pytest.raises(ValueError, match="frozen protocol"):
        validate_evaluation_records(records)


def test_reject_incorrect_label():
    records = valid_records()
    records[1]["label"] = 0

    with pytest.raises(ValueError, match="incorrect label"):
        validate_evaluation_records(records)


def test_reject_wrong_recording():
    records = valid_records()
    records[1]["recording_id"] = 108

    with pytest.raises(ValueError, match="frozen protocol"):
        validate_evaluation_records(records)


def test_reject_unsupported_extra_recording():
    records = valid_records()
    records.append({"recording_id": 122, "label": 1})

    with pytest.raises(ValueError, match="frozen protocol"):
        validate_evaluation_records(records)

from unittest.mock import patch
import run_step27_experiment_b_evaluation as runner


def test_evaluation_fits_training_only():
    """Verify frozen evaluation never fits on evaluation data."""

    train = [
        {
            "recording_id": 97,
            "split": "train",
            "label": 0,
            "mean": 0.1,
            "std": 0.1,
            "rms": 0.1,
        },
        {
            "recording_id": 105,
            "split": "train",
            "label": 1,
            "mean": 0.3,
            "std": 0.3,
            "rms": 0.3,
        },
    ]

    evaluation = [
        {
            "recording_id": 100,
            "split": "test",
            "label": 0,
            "mean": 0.2,
            "std": 0.2,
            "rms": 0.2,
        },
        {
            "recording_id": 121,
            "split": "test",
            "label": 1,
            "mean": 0.4,
            "std": 0.4,
            "rms": 0.4,
        },
    ]

    class FakeModel:
        def __init__(self):
            self.fit_calls = []
            self.predict_calls = []

        def fit(self, X, y):
            self.fit_calls.append((X, y))
            return self

        def predict(self, X):
            self.predict_calls.append(X)
            return [0, 1]

    fake_model = FakeModel()
    accessed_files = []

    def fake_import(path):
        accessed_files.append(path.name)

        if path.name == "train.csv":
            return train

        if path.name == "test.csv":
            return evaluation

        raise AssertionError(f"Unexpected CSV: {path}")

    with (
        patch.object(
            runner,
            "import_features_from_csv",
            side_effect=fake_import,
        ),
        patch.object(
            runner,
            "create_baseline_pipeline",
            return_value=fake_model,
        ),
        patch.object(runner, "validate_held_out_fault_split"),
        patch.object(runner, "validate_evaluation_records"),
        patch(
            "run_step27_experiment_b.validate_experiment_b_records"
        ),
    ):
        runner.main()

    assert accessed_files == ["train.csv", "test.csv"]

    assert len(fake_model.fit_calls) == 1

    fitted_X, fitted_y = fake_model.fit_calls[0]

    assert fitted_X == [
        [0.1, 0.1, 0.1],
        [0.3, 0.3, 0.3],
    ]
    assert fitted_y == [0, 1]

    assert fake_model.predict_calls == [
        [
            [0.2, 0.2, 0.2],
            [0.4, 0.4, 0.4],
        ]
    ]
import pytest

from run_step27_experiment_b import validate_experiment_b_records
from src.held_out_fault_split import HELD_OUT_FAULT_SPLIT
from src.cwru_metadata import CWRU_RECORDING_METADATA


def make_valid_records(split_name):
    """Create one valid synthetic record per frozen recording ID."""
    return [
        {
            "recording_id": recording_id,
            "label": CWRU_RECORDING_METADATA[recording_id]["label"],
        }
        for ids in HELD_OUT_FAULT_SPLIT[split_name].values()
        for recording_id in ids
    ]


def test_valid_training_records():
    records = make_valid_records("train")
    validate_experiment_b_records(records, "train")


def test_valid_validation_records():
    records = make_valid_records("validation")
    validate_experiment_b_records(records, "validation")


def test_reject_incorrect_label():
    records = make_valid_records("train")
    records[0]["label"] = 1 - records[0]["label"]

    with pytest.raises(ValueError, match="incorrect label"):
        validate_experiment_b_records(records, "train")


def test_reject_missing_recording():
    records = make_valid_records("train")
    records.pop()

    with pytest.raises(ValueError, match="frozen protocol"):
        validate_experiment_b_records(records, "train")


def test_reject_ball_fault_recording():
    records = make_valid_records("train")
    records.append({"recording_id": 118, "label": 1})

    with pytest.raises(ValueError, match="frozen protocol"):
        validate_experiment_b_records(records, "train")


def test_reject_unsupported_split():
    records = make_valid_records("train")

    with pytest.raises(ValueError, match="Unsupported split"):
        validate_experiment_b_records(records, "evaluation")


def test_reject_empty_dataset():
    with pytest.raises(ValueError, match="Empty dataset"):
        validate_experiment_b_records([], "train")

from unittest.mock import patch
import run_step27_experiment_b as runner


def test_training_uses_only_train_and_validation():
    """Verify model fitting and data access without real CSV files."""

    class FakeModel:
        def __init__(self):
            self.fit_calls = []
            self.predict_calls = []

        def fit(self, X, y):
            self.fit_calls.append((X, y))
            return self

        def predict(self, X):
            self.predict_calls.append(X)
            return [0] * len(X)

    fake_model = FakeModel()
    accessed_files = []

    def fake_import(path):
        accessed_files.append(path.name)

        if path.name == "train.csv":
            return [
                {
                    "recording_id": 97,
                    "split": "train",
                    "label": 0,
                    "mean": 0.1,
                    "std": 0.1,
                    "rms": 0.1,
                }
            ]

        if path.name == "validation.csv":
            return [
                {
                    "recording_id": 99,
                    "split": "validation",
                    "label": 0,
                    "mean": 0.2,
                    "std": 0.2,
                    "rms": 0.2,
                }
            ]

        raise AssertionError(f"Unexpected CSV access: {path}")

    with (
        patch.object(runner, "import_features_from_csv",
                     side_effect=fake_import),
        patch.object(runner, "create_baseline_pipeline",
                     return_value=fake_model),
        patch.object(runner, "validate_experiment_b_records"),
        patch.object(runner, "validate_held_out_fault_split"),
    ):
        runner.main()

    assert accessed_files == ["train.csv", "validation.csv"]
    assert len(fake_model.fit_calls) == 1

    fitted_X, fitted_y = fake_model.fit_calls[0]

    assert fitted_X == [[0.1, 0.1, 0.1]]
    assert fitted_y == [0]

    assert fake_model.predict_calls == [
        [[0.1, 0.1, 0.1]],
        [[0.2, 0.2, 0.2]],
    ]
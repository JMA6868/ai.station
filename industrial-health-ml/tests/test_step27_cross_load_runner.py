import pytest

from run_step27_cross_load import (
    validate_cross_load_records,
    evaluate_per_recording,
)

from src.cross_load_split import CROSS_LOAD_SPLIT
from src.cwru_metadata import CWRU_RECORDING_METADATA


def make_valid_records(split_name):
    """Create one valid sample per expected recording."""
    return [
        {
            "recording_id": recording_id,
            "label": CWRU_RECORDING_METADATA[recording_id]["label"],
        }
        for ids in CROSS_LOAD_SPLIT[split_name].values()
        for recording_id in ids
    ]


def test_valid_train_records():
    records = make_valid_records("train")
    validate_cross_load_records(records, "train")


def test_valid_validation_records():
    records = make_valid_records("validation")
    validate_cross_load_records(records, "validation")


def test_reject_incorrect_label():
    records = make_valid_records("train")
    records[0]["label"] = 1 - records[0]["label"]

    with pytest.raises(ValueError, match="incorrect label"):
        validate_cross_load_records(records, "train")


def test_reject_missing_recording():
    records = make_valid_records("train")
    records.pop()

    with pytest.raises(ValueError, match="recording IDs"):
        validate_cross_load_records(records, "train")


def test_reject_wrong_load_recording():
    records = make_valid_records("validation")

    # Replace a 2 HP recording with a 3 HP recording.
    records[0]["recording_id"] = 100
    records[0]["label"] = CWRU_RECORDING_METADATA[100]["label"]

    with pytest.raises(ValueError, match="recording IDs"):
        validate_cross_load_records(records, "validation")


def test_reject_unsupported_split():
    records = make_valid_records("train")

    with pytest.raises(ValueError, match="Unsupported split"):
        validate_cross_load_records(records, "evaluation")

def test_evaluate_per_recording():
    """Verify per-recording accuracy calculations."""

    records = [
        {"recording_id": 99, "label": 0},
        {"recording_id": 99, "label": 0},
        {"recording_id": 99, "label": 0},
        {"recording_id": 107, "label": 1},
        {"recording_id": 107, "label": 1},
    ]

    predictions = [0, 0, 1, 1, 0]

    results = evaluate_per_recording(records, predictions)

    assert results[99]["total"] == 3
    assert results[99]["correct"] == 2
    assert results[99]["accuracy"] == pytest.approx(2 / 3)

    assert results[107]["total"] == 2
    assert results[107]["correct"] == 1
    assert results[107]["accuracy"] == pytest.approx(0.5)


def test_evaluate_per_recording_rejects_length_mismatch():
    """Reject records and predictions with different lengths."""

    records = [{"recording_id": 99, "label": 0}]
    predictions = [0, 0]

    with pytest.raises(ValueError, match="equal lengths"):
        evaluate_per_recording(records, predictions)


def test_evaluate_per_recording_rejects_empty_input():
    """Reject empty evaluation datasets."""

    with pytest.raises(ValueError, match="empty records"):
        evaluate_per_recording([], [])
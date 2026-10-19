import pytest

from run_ml_baseline import (
    validate_dataset_split,
    validate_recording_isolation,
)

from run_ml_baseline import validate_recording_isolation


def test_recording_isolation_accepts_disjoint_ids():
    """Accept separate recording IDs for training and validation."""

    train = [
        {"recording_id": 97},
        {"recording_id": 98},
    ]

    validation = [
        {"recording_id": 99},
        {"recording_id": 107},
    ]

    train_ids, validation_ids = validate_recording_isolation(
        train, validation
    )

    assert train_ids == {97, 98}
    assert validation_ids == {99, 107}


def test_recording_isolation_rejects_overlap():
    """Reject the same recording appearing in both splits."""

    train = [
        {"recording_id": 97},
        {"recording_id": 98},
    ]

    validation = [
        {"recording_id": 98},
        {"recording_id": 107},
    ]

    with pytest.raises(ValueError, match="must not overlap"):
        validate_recording_isolation(train, validation)

def test_dataset_split_accepts_correct_records():
    """Accept records with the expected split."""

    records = [
        {"split": "train"},
        {"split": "train"},
    ]

    validate_dataset_split(records, "train")


def test_dataset_split_rejects_wrong_split():
    """Reject records assigned to the wrong split."""

    records = [
        {"split": "train"},
        {"split": "validation"},
    ]

    with pytest.raises(ValueError, match="Invalid dataset split"):
        validate_dataset_split(records, "train")


def test_dataset_split_rejects_empty_dataset():
    """Reject a dataset containing no records."""

    with pytest.raises(ValueError, match="Empty dataset"):
        validate_dataset_split([], "train")
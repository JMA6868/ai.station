import pytest

from run_step27_cross_load import validate_cross_load_records
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
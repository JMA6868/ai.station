import pytest

from src.feature_validation import validate_feature_record


@pytest.fixture
def valid_record():
    """Create a valid, typed feature record."""
    return {
        "recording_id": 97,
        "split": "train",
        "label": 0,
        "start_index": 0,
        "end_index": 1199,
        "mean": 0.01,
        "std": 0.07,
        "rms": 0.08,
    }


def test_accept_valid_record(valid_record):
    """A valid feature record should not raise an error."""
    assert validate_feature_record(valid_record) is None


@pytest.mark.parametrize(
    "field,invalid_value,expected_error",
    [
        ("split", "unknown", "Invalid split"),
        ("label", 9, "Invalid label"),
        ("recording_id", 0, "Invalid metadata"),
        ("start_index", -1, "Invalid metadata"),
        ("end_index", -1, "Invalid metadata"),
        ("rms", float("nan"), "Non-finite feature"),
        ("std", float("inf"), "Non-finite feature"),
        ("label", "0", "Invalid integer field"),
    ],
)
def test_reject_invalid_record(
    valid_record, field, invalid_value, expected_error
):
    """Reject invalid feature values and metadata."""
    valid_record[field] = invalid_value

    with pytest.raises(ValueError, match=expected_error):
        validate_feature_record(valid_record)


def test_reject_missing_column(valid_record):
    """Reject records missing a required column."""
    del valid_record["rms"]

    with pytest.raises(ValueError, match="Invalid feature record schema"):
        validate_feature_record(valid_record)
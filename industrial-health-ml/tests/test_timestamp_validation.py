import pytest

from src.timestamp_validation import validate_timestamps


def test_continuous_timestamps():
    assert validate_timestamps([0, 1, 2, 3], 1.0) == []


def test_missing_interval():
    assert validate_timestamps([0, 1, 2, 8, 9], 1.0) == [3]


def test_duplicate_timestamp():
    assert validate_timestamps([0, 1, 1, 2], 1.0) == [2]


def test_backward_timestamp():
    assert validate_timestamps([0, 1, 0.5, 2], 1.0) == [2, 3]


def test_floating_point_tolerance():
    assert validate_timestamps([0.0, 0.1, 0.2, 0.3], 0.1) == []


def test_invalid_interval():
    with pytest.raises(ValueError):
        validate_timestamps([0, 1, 2], 0)


def test_single_timestamp():
    assert validate_timestamps([5.0], 1.0) == []
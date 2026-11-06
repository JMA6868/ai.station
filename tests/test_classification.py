import pytest

from src.classification import predict_fault


def test_below_threshold_is_normal():
    assert predict_fault(0.07, 0.18) == 0


def test_above_threshold_is_fault():
    assert predict_fault(0.29, 0.18) == 1


def test_equal_to_threshold_is_normal():
    assert predict_fault(0.18, 0.18) == 0


def test_just_above_threshold_is_fault():
    assert predict_fault(0.180001, 0.18) == 1


def test_zero_rms_is_normal():
    assert predict_fault(0.0, 0.18) == 0


@pytest.mark.parametrize(
    "rms, threshold, expected",
    [
        (0.05, 0.10, 0),
        (0.15, 0.10, 1),
        (0.10, 0.10, 0),
    ],
)
def test_different_thresholds(rms, threshold, expected):
    assert predict_fault(rms, threshold) == expected
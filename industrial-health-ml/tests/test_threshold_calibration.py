import pytest

from src.threshold_calibration import calculate_percentile_threshold


def test_percentile_threshold_p99():
    values = [1.0, 2.0, 3.0, 4.0, 5.0]

    result = calculate_percentile_threshold(values, 99)

    assert result == pytest.approx(4.96)


def test_percentile_threshold_empty_values():
    with pytest.raises(ValueError):
        calculate_percentile_threshold([], 99)


def test_percentile_threshold_nan():
    with pytest.raises(ValueError):
        calculate_percentile_threshold(
            [0.1, float("nan")],
            99,
        )


def test_percentile_threshold_infinity():
    with pytest.raises(ValueError):
        calculate_percentile_threshold(
            [0.1, float("inf")],
            99,
        )


def test_percentile_threshold_invalid_percentile():
    with pytest.raises(ValueError):
        calculate_percentile_threshold(
            [0.1, 0.2, 0.3],
            101,
        )


def test_percentile_threshold_p0():
    result = calculate_percentile_threshold(
        [1.0, 2.0, 3.0],
        0,
    )

    assert result == pytest.approx(1.0)


def test_percentile_threshold_p100():
    result = calculate_percentile_threshold(
        [1.0, 2.0, 3.0],
        100,
    )

    assert result == pytest.approx(3.0)


def test_percentile_threshold_rejects_2d_input():
    with pytest.raises(ValueError, match="nonempty 1D"):
        calculate_percentile_threshold(
            [[1.0, 2.0], [3.0, 4.0]],
            99,
        )

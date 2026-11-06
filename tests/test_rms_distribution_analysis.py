"""Tests for CWRU RMS distribution analysis."""

import numpy as np
import pytest

from src.rms_distribution_analysis import (
    summarize_rms_distribution,
)


def test_rms_distribution_statistics():
    values = np.array([1.0, 2.0, 3.0, 4.0, 5.0])

    result = summarize_rms_distribution(values)

    assert result["window_count"] == 5
    assert result["min"] == 1.0
    assert result["median"] == 3.0
    assert result["max"] == 5.0

    assert result["p1"] == pytest.approx(
        np.percentile(values, 1)
    )
    assert result["p99"] == pytest.approx(
        np.percentile(values, 99)
    )


def test_single_rms_value():
    result = summarize_rms_distribution([0.25])

    assert result["window_count"] == 1
    assert result["min"] == 0.25
    assert result["p1"] == 0.25
    assert result["median"] == 0.25
    assert result["p99"] == 0.25
    assert result["max"] == 0.25


@pytest.mark.parametrize(
    "values",
    [
        [],
        [[1.0, 2.0]],
        [1.0, float("nan")],
        [1.0, float("inf")],
    ],
)
def test_invalid_rms_values(values):
    with pytest.raises(ValueError):
        summarize_rms_distribution(values)

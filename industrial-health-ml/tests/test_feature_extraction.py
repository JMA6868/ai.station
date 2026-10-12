import math
import pytest

from src.feature_extraction import calculate_features


def test_basic_features():
    result = calculate_features([1, 2, 3, 4, 5])

    assert result["mean"] == pytest.approx(3.0)
    assert result["std"] == pytest.approx(math.sqrt(2))
    assert result["rms"] == pytest.approx(math.sqrt(11))


def test_constant_signal():
    result = calculate_features([3, 3, 3, 3, 3])

    assert result["mean"] == pytest.approx(3.0)
    assert result["std"] == pytest.approx(0.0)
    assert result["rms"] == pytest.approx(3.0)


def test_zero_signal():
    result = calculate_features([0, 0, 0])

    assert result["mean"] == pytest.approx(0.0)
    assert result["std"] == pytest.approx(0.0)
    assert result["rms"] == pytest.approx(0.0)


def test_empty_signal():
    with pytest.raises(ValueError):
        calculate_features([])
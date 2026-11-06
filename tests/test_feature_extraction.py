import math
import pytest

from src.feature_extraction import calculate_features, extract_window_features


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
 
def test_window_count():
    values = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

    results = extract_window_features(values, window_size=4, step=2)

    assert len(results) == 4


def test_window_positions():
    values = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

    results = extract_window_features(values, window_size=4, step=2)

    assert [r["start_index"] for r in results] == [0, 2, 4, 6]
    assert [r["end_index"] for r in results] == [3, 5, 7, 9]


def test_window_statistics():
    values = [1, 2, 3, 4, 5, 6]

    results = extract_window_features(values, window_size=4, step=2)

    assert results[0]["mean"] == pytest.approx(2.5)
    assert results[1]["mean"] == pytest.approx(4.5)


def test_invalid_window_parameters():
    with pytest.raises(ValueError):
        extract_window_features([1, 2, 3], window_size=0, step=1)

    with pytest.raises(ValueError):
        extract_window_features([1, 2, 3], window_size=2, step=0)


def test_short_signal():
    values = [1, 2]

    results = extract_window_features(values, window_size=4, step=2)

    assert results == []

def test_window_step_three():
    values = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

    results = extract_window_features(
        values,
        window_size=4,
        step=3
    )

    assert len(results) == 3
    assert [r["start_index"] for r in results] == [0, 3, 6] 
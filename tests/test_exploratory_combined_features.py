import math

import pytest

from src.exploratory_combined_features import calculate_combined_features


def test_combined_features_known_values():
    result = calculate_combined_features([3.0, 4.0])

    assert result["rms"] == pytest.approx(math.sqrt(12.5))
    assert result["crest_factor"] == pytest.approx(
        4.0 / math.sqrt(12.5)
    )


def test_combined_features_preserves_existing_statistics():
    result = calculate_combined_features([1.0, 2.0, 3.0])

    assert set(result) == {"mean", "std", "rms", "crest_factor"}
    assert result["mean"] == pytest.approx(2.0)
    assert result["std"] == pytest.approx(math.sqrt(2.0 / 3.0))


def test_combined_features_rejects_empty_signal():
    with pytest.raises(ValueError):
        calculate_combined_features([])


def test_combined_features_rejects_zero_rms():
    with pytest.raises(ValueError):
        calculate_combined_features([0.0, 0.0])

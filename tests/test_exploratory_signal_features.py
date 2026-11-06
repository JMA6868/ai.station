import math

import pytest

from src.exploratory_signal_features import calculate_crest_factor


def test_crest_factor_known_values():
    signal = [3.0, 4.0]

    expected_rms = math.sqrt((3.0**2 + 4.0**2) / 2)
    expected_crest = 4.0 / expected_rms

    assert calculate_crest_factor(signal) == pytest.approx(
        expected_crest
    )


@pytest.mark.parametrize("scale", [0.5, 1.0, 1.2, 2.0, -2.0])
def test_crest_factor_amplitude_invariance(scale):
    signal = [0.2, -0.4, 0.1, 0.8, -0.3]

    original = calculate_crest_factor(signal)
    scaled = calculate_crest_factor([x * scale for x in signal])

    assert scaled == pytest.approx(original)


def test_crest_factor_empty_signal():
    with pytest.raises(ValueError, match="empty"):
        calculate_crest_factor([])


def test_crest_factor_zero_signal():
    with pytest.raises(ValueError, match="zero-RMS"):
        calculate_crest_factor([0.0, 0.0, 0.0])

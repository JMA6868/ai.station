"""Tests for sampling-rate harmonization."""

import numpy as np

from src.signal_resampling import resample_signal


def test_downsample_48k_to_12k_preserves_duration():
    source_rate = 48000
    target_rate = 12000
    duration_seconds = 1.0

    time = np.arange(source_rate) / source_rate
    signal = np.sin(2 * np.pi * 100 * time)

    result = resample_signal(
        signal,
        source_rate_hz=source_rate,
        target_rate_hz=target_rate,
    )

    assert len(result) == int(duration_seconds * target_rate)
    assert np.isfinite(result).all()


def test_downsampling_preserves_low_frequency_and_rejects_aliasing():
    source_rate = 48000
    target_rate = 12000
    time = np.arange(source_rate) / source_rate

    low_frequency = np.sin(2 * np.pi * 1000 * time)
    high_frequency = np.sin(2 * np.pi * 10000 * time)

    low_result = resample_signal(
        low_frequency,
        source_rate_hz=source_rate,
        target_rate_hz=target_rate,
    )

    high_result = resample_signal(
        high_frequency,
        source_rate_hz=source_rate,
        target_rate_hz=target_rate,
    )

    # Ignore filter boundary transients.
    low_center = low_result[100:-100]
    high_center = high_result[100:-100]

    low_rms = np.sqrt(np.mean(low_center ** 2))
    high_rms = np.sqrt(np.mean(high_center ** 2))

    assert 0.65 < low_rms < 0.75
    assert high_rms < 0.02


def test_same_sampling_rate_preserves_signal_without_sharing_memory():
    signal = np.array([0.1, -0.5, 0.8, 1.2])

    result = resample_signal(
        signal,
        source_rate_hz=12000,
        target_rate_hz=12000,
    )

    np.testing.assert_array_equal(result, signal)
    assert not np.shares_memory(result, signal)


def test_invalid_resampling_inputs():
    import pytest

    valid_signal = np.array([0.1, 0.2, 0.3])

    invalid_cases = [
        (valid_signal, 0, 12000),
        (valid_signal, 48000, -12000),
        (np.array([]), 48000, 12000),
        (np.array([1.0, np.nan]), 48000, 12000),
        (np.array([[1.0, 2.0]]), 48000, 12000),
    ]

    for signal, source_rate, target_rate in invalid_cases:
        with pytest.raises(ValueError):
            resample_signal(
                signal,
                source_rate_hz=source_rate,
                target_rate_hz=target_rate,
            )

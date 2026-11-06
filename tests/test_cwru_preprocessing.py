"""Tests for CWRU sampling-rate harmonization."""

import numpy as np

from src.cwru_preprocessing import load_harmonized_cwru_signal


def test_normal_48k_is_downsampled_to_12k():
    signal = load_harmonized_cwru_signal(
        "data/raw/cwru/97.mat",
        source_rate_hz=48000,
    )

    assert signal.ndim == 1
    assert len(signal) == 60985
    assert np.isfinite(signal).all()


def test_fault_12k_preserves_original_signal():
    signal = load_harmonized_cwru_signal(
        "data/raw/cwru/105.mat",
        source_rate_hz=12000,
    )

    assert signal.ndim == 1
    assert len(signal) == 121265
    assert np.isfinite(signal).all()


def test_normal_recording_rejects_incorrect_source_rate():
    import pytest

    with pytest.raises(ValueError, match="sampling rate"):
        load_harmonized_cwru_signal(
            "data/raw/cwru/97.mat",
            source_rate_hz=12000,
        )


def test_12k_fault_rejects_incorrect_source_rate():
    import pytest

    with pytest.raises(ValueError, match="sampling rate"):
        load_harmonized_cwru_signal(
            "data/raw/cwru/105.mat",
            source_rate_hz=48000,
        )


def test_unknown_recording_rejects_unverified_sampling_rate():
    import pytest

    with pytest.raises(ValueError, match="Unknown CWRU recording"):
        load_harmonized_cwru_signal(
            "data/raw/cwru/999.mat",
            source_rate_hz=12000,
        )

"""Tests for CWRU 0.028-inch special MAT signal names."""

import numpy as np
import pytest

from src import cwru_loader


SPECIAL_MAPPING = {
    3001: 56,
    3002: 57,
    3003: 58,
    3004: 59,
    3005: 48,
    3006: 49,
    3007: 50,
    3008: 51,
}


@pytest.mark.parametrize(
    "recording_id,signal_number",
    SPECIAL_MAPPING.items(),
)
def test_special_signal_mapping(
    monkeypatch, recording_id, signal_number
):
    """Load the verified DE signal for each special file."""
    expected_key = f"X{signal_number:03d}_DE_time"
    expected_signal = np.array([[1.0], [2.0], [3.0]])

    def fake_loadmat(path):
        return {expected_key: expected_signal}

    monkeypatch.setattr(cwru_loader, "loadmat", fake_loadmat)

    result = cwru_loader.load_cwru_de_signal(
        f"data/raw/cwru/{recording_id}.mat"
    )

    np.testing.assert_array_equal(
        result,
        [1.0, 2.0, 3.0],
    )


def test_special_mapping_rejects_wrong_signal(monkeypatch):
    """Do not silently accept an unexpected DE signal."""
    monkeypatch.setattr(
        cwru_loader,
        "loadmat",
        lambda path: {"X999_DE_time": np.array([[1.0]])},
    )

    with pytest.raises(ValueError, match="Expected signal"):
        cwru_loader.load_cwru_de_signal(
            "data/raw/cwru/3001.mat"
        )


def test_original_signal_mapping_unchanged(monkeypatch):
    """Ordinary CWRU files retain their original signal mapping."""
    monkeypatch.setattr(
        cwru_loader,
        "loadmat",
        lambda path: {"X105_DE_time": np.array([[2.0], [4.0]])},
    )

    result = cwru_loader.load_cwru_de_signal(
        "data/raw/cwru/105.mat"
    )

    np.testing.assert_array_equal(result, [2.0, 4.0])

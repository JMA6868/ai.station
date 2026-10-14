from pathlib import Path

import numpy as np
from scipy.io import loadmat

from src.cwru_loader import load_cwru_de_signal


def test_load_correct_signal_from_99():
    """Ensure 99.mat loads X099 rather than X098."""

    project_root = Path(__file__).resolve().parents[1]
    file_path = project_root / "data/raw/cwru/99.mat"

    actual = load_cwru_de_signal(file_path)

    data = loadmat(file_path)
    expected = data["X099_DE_time"].flatten()
    wrong_signal = data["X098_DE_time"].flatten()

    assert np.array_equal(actual, expected)
    assert not np.array_equal(actual, wrong_signal)

import pytest
from scipy.io import savemat


@pytest.mark.parametrize("invalid_value", [
    np.nan,
    np.inf,
    -np.inf,
])
def test_reject_nonfinite_signal(tmp_path, invalid_value):
    """Reject signals containing NaN or Infinity."""

    file_path = tmp_path / "123.mat"

    signal = np.array([
        [0.1],
        [invalid_value],
        [-0.2],
    ])

    savemat(file_path, {
        "X123_DE_time": signal
    })

    with pytest.raises(ValueError, match="NaN or Infinity"):
        load_cwru_de_signal(file_path)

def test_reject_missing_signal(tmp_path):
    """Reject a MAT file without the expected DE signal."""

    file_path = tmp_path / "123.mat"

    savemat(file_path, {
        "X122_DE_time": np.array([[0.1], [0.2]])
    })

    with pytest.raises(ValueError, match="Expected signal"):
        load_cwru_de_signal(file_path)


def test_reject_empty_signal(tmp_path):
    """Reject a DE signal containing zero samples."""

    file_path = tmp_path / "123.mat"

    savemat(file_path, {
        "X123_DE_time": np.empty((0, 1))
    })

    with pytest.raises(ValueError, match="Signal cannot be empty"):
        load_cwru_de_signal(file_path)    
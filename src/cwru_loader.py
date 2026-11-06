# IndustrialSense AI - CWRU Data Loader

from pathlib import Path

import numpy as np
from scipy.io import loadmat


def load_cwru_de_signal(file_path):
    """Load the matching Drive End signal from a CWRU MAT file."""

    path = Path(file_path)

    # Extract experiment number from filename.
    experiment_number = int(path.stem)

    # Most CWRU filenames match their internal signal identifiers.
    # Official 0.028-inch fault files 3001-3008 are exceptions.
    special_signal_numbers = {
        3001: 56,
        3002: 57,
        3003: 58,
        3004: 59,
        3005: 48,
        3006: 49,
        3007: 50,
        3008: 51,
    }

    signal_number = special_signal_numbers.get(
        experiment_number,
        experiment_number,
    )
    signal_key = f"X{signal_number:03d}_DE_time"

    data = loadmat(path)

    if signal_key not in data:
        raise ValueError(
            f"Expected signal '{signal_key}' not found in {path.name}"
        )

    signal = np.asarray(data[signal_key]).flatten()

    if signal.size == 0:
        raise ValueError("Signal cannot be empty")

    if not np.isfinite(signal).all():
        raise ValueError("Signal contains NaN or Infinity")

    return signal
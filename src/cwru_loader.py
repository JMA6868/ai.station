# IndustrialSense AI - CWRU Data Loader

from pathlib import Path

import numpy as np
from scipy.io import loadmat


def load_cwru_de_signal(file_path):
    """Load the matching Drive End signal from a CWRU MAT file."""

    path = Path(file_path)

    # Extract experiment number from filename.
    experiment_number = int(path.stem)

    # Example: 99.mat -> X099_DE_time
    signal_key = f"X{experiment_number:03d}_DE_time"

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
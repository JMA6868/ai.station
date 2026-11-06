"""Threshold calibration utilities for Stage 1 anomaly detection."""

import numpy as np


def calculate_percentile_threshold(values, percentile):
    """Calculate a percentile threshold from calibration values."""

    data = np.asarray(values, dtype=float)

    if data.ndim != 1 or data.size == 0:
        raise ValueError(
            "Calibration values must be a nonempty 1D sequence"
        )

    if not np.all(np.isfinite(data)):
        raise ValueError(
            "Calibration values must all be finite"
        )

    if not np.isfinite(percentile) or not 0 <= percentile <= 100:
        raise ValueError(
            "Percentile must be between 0 and 100"
        )

    return float(np.percentile(data, percentile))

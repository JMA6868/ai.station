"""Sampling-rate harmonization for vibration signals."""

import math

import numpy as np
from scipy.signal import resample_poly


def resample_signal(signal, source_rate_hz, target_rate_hz):
    """Resample a 1D signal using polyphase filtering."""
    if (
        not isinstance(source_rate_hz, int)
        or not isinstance(target_rate_hz, int)
        or source_rate_hz <= 0
        or target_rate_hz <= 0
    ):
        raise ValueError("Sampling rates must be positive integers")

    values = np.asarray(signal, dtype=float)

    if values.ndim != 1 or values.size == 0:
        raise ValueError("Signal must be a nonempty 1D array")

    if not np.isfinite(values).all():
        raise ValueError("Signal contains NaN or Infinity")

    if source_rate_hz == target_rate_hz:
        return values.copy()

    divisor = math.gcd(source_rate_hz, target_rate_hz)

    up = target_rate_hz // divisor
    down = source_rate_hz // divisor

    return resample_poly(values, up, down)

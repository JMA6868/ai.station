"""Per-recording RMS distribution analysis for CWRU Stage 1."""

from pathlib import Path

import numpy as np

from src.cwru_preprocessing import load_harmonized_cwru_signal
from src.feature_extraction import extract_window_features
from src.harmonized_stage1_evaluation import WINDOW_SIZE, STEP


NORMAL_IDS = {97, 98, 99, 100}


def get_recording_rms_values(recording_id):
    """Extract harmonized window RMS values for one recording."""
    source_rate_hz = 48000 if recording_id in NORMAL_IDS else 12000

    signal = load_harmonized_cwru_signal(
        Path(f"data/raw/cwru/{recording_id}.mat"),
        source_rate_hz=source_rate_hz,
    )

    features = extract_window_features(
        signal,
        window_size=WINDOW_SIZE,
        step=STEP,
    )

    rms_values = np.array(
        [feature["rms"] for feature in features],
        dtype=float,
    )

    if rms_values.size == 0:
        raise ValueError("No valid RMS windows")

    if not np.isfinite(rms_values).all():
        raise ValueError("Non-finite RMS values")

    return rms_values


def summarize_rms_distribution(rms_values):
    """Summarize the RMS distribution without changing thresholds."""
    values = np.asarray(rms_values, dtype=float)

    if values.ndim != 1 or values.size == 0:
        raise ValueError("RMS values must be a nonempty 1D array")

    if not np.isfinite(values).all():
        raise ValueError("RMS values must be finite")

    return {
        "window_count": int(values.size),
        "min": float(np.min(values)),
        "p1": float(np.percentile(values, 1)),
        "median": float(np.median(values)),
        "p99": float(np.percentile(values, 99)),
        "max": float(np.max(values)),
    }

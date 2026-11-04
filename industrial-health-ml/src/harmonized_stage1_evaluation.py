"""Sampling-rate-harmonized Stage 1 evaluation."""

from pathlib import Path

from src.cwru_preprocessing import load_harmonized_cwru_signal
from src.feature_extraction import extract_window_features
from src.threshold_calibration import calculate_percentile_threshold


TRAIN_IDS = (97, 98)

WINDOW_SIZE = 1200
STEP = 600
PERCENTILE = 99


def calibrate_harmonized_rms_threshold():
    """Calibrate RMS P99 using harmonized Normal training data."""
    training_rms = []

    for recording_id in TRAIN_IDS:
        signal = load_harmonized_cwru_signal(
            Path(f"data/raw/cwru/{recording_id}.mat"),
            source_rate_hz=48000,
        )

        features = extract_window_features(
            signal,
            window_size=WINDOW_SIZE,
            step=STEP,
        )

        training_rms.extend(
            feature["rms"] for feature in features
        )

    if not training_rms:
        raise ValueError("No Normal training windows available")

    return calculate_percentile_threshold(
        training_rms,
        PERCENTILE,
    )


def evaluate_rms_recording(recording_id, rms_threshold):
    """Evaluate a CWRU recording using harmonized RMS features."""
    from src.recording_anomaly_decision import classify_recording

    normal_ids = {97, 98, 99, 100}
    source_rate_hz = 48000 if recording_id in normal_ids else 12000

    signal = load_harmonized_cwru_signal(
        Path(f"data/raw/cwru/{recording_id}.mat"),
        source_rate_hz=source_rate_hz,
    )

    features = extract_window_features(
        signal,
        window_size=WINDOW_SIZE,
        step=STEP,
    )

    if not features:
        raise ValueError("Recording has no valid windows")

    anomalous_windows = sum(
        feature["rms"] > rms_threshold
        for feature in features
    )

    total_windows = len(features)

    return {
        "recording_id": recording_id,
        "total_windows": total_windows,
        "anomalous_windows": anomalous_windows,
        "anomaly_rate": anomalous_windows / total_windows,
        "detected": classify_recording(
            anomalous_windows,
            total_windows,
        ),
    }

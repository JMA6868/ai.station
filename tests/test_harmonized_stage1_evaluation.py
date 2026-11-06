"""Tests for harmonized Stage 1 evaluation."""

import numpy as np

from src.harmonized_stage1_evaluation import (
    calibrate_harmonized_rms_threshold,
)


def test_harmonized_rms_threshold_is_valid_and_reproducible():
    first = calibrate_harmonized_rms_threshold()
    second = calibrate_harmonized_rms_threshold()

    assert np.isfinite(first)
    assert first > 0
    assert first == second


def test_harmonized_training_uses_expected_windows():
    from src.cwru_preprocessing import load_harmonized_cwru_signal
    from src.feature_extraction import extract_window_features

    expected_counts = {97: 100, 98: 200}
    total = 0

    for recording_id, expected in expected_counts.items():
        signal = load_harmonized_cwru_signal(
            f"data/raw/cwru/{recording_id}.mat",
            source_rate_hz=48000,
        )

        features = extract_window_features(
            signal,
            window_size=1200,
            step=600,
        )

        assert len(features) == expected
        total += len(features)

    assert total == 300


def test_harmonized_threshold_matches_training_rms_p99():
    from src.cwru_preprocessing import load_harmonized_cwru_signal
    from src.feature_extraction import extract_window_features

    rms_values = []

    for recording_id in (97, 98):
        signal = load_harmonized_cwru_signal(
            f"data/raw/cwru/{recording_id}.mat",
            source_rate_hz=48000,
        )

        features = extract_window_features(
            signal,
            window_size=1200,
            step=600,
        )

        rms_values.extend(feature["rms"] for feature in features)

    expected = float(np.percentile(rms_values, 99))
    actual = calibrate_harmonized_rms_threshold()

    assert len(rms_values) == 300
    assert np.isclose(actual, expected, rtol=1e-12, atol=0)


def test_harmonized_recording_evaluation_uses_frozen_rules():
    from src.harmonized_stage1_evaluation import evaluate_rms_recording

    result = evaluate_rms_recording(
        recording_id=99,
        rms_threshold=calibrate_harmonized_rms_threshold(),
    )

    assert result["recording_id"] == 99
    assert result["total_windows"] > 0
    assert 0 <= result["anomalous_windows"] <= result["total_windows"]
    assert result["anomaly_rate"] == (
        result["anomalous_windows"] / result["total_windows"]
    )
    assert result["detected"] == (result["anomaly_rate"] > 0.05)


def test_harmonized_recording_decision_boundary():
    from src.recording_anomaly_decision import classify_recording

    assert classify_recording(5, 100) is False
    assert classify_recording(6, 100) is True
    assert classify_recording(0, 100) is False
    assert classify_recording(100, 100) is True

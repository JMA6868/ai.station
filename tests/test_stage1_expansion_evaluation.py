from unittest.mock import patch

import pytest

from src.stage1_expansion_evaluation import evaluate_recording


def test_stage1_evaluation_with_synthetic_features():
    features = (
        [(0.20, 2.0)] * 4
        + [(0.01, 5.0)] * 3
        + [(0.01, 2.0)] * 93
    )

    with patch(
        "src.stage1_expansion_evaluation.get_window_features",
        return_value=features,
    ):
        result = evaluate_recording(
            recording_id=999,
            rms_threshold=0.10,
            cf_threshold=4.0,
        )

    assert result["total_windows"] == 100

    assert result["rms_alarms"] == 4
    assert result["rms_rate"] == pytest.approx(0.04)
    assert result["rms_detected"] is False

    assert result["dual_alarms"] == 7
    assert result["dual_rate"] == pytest.approx(0.07)
    assert result["dual_detected"] is True


def test_stage1_evaluation_rejects_empty_recording():
    with patch(
        "src.stage1_expansion_evaluation.get_window_features",
        return_value=[],
    ):
        with pytest.raises(ValueError, match="no valid windows"):
            evaluate_recording(
                recording_id=999,
                rms_threshold=0.10,
                cf_threshold=4.0,
            )

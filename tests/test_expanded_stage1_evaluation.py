"""Tests for the expanded Stage 1 RMS evaluation."""

import pytest

from src import expanded_stage1_evaluation as expanded


def test_evaluation_recording_ids():
    normal_ids = expanded.NORMAL_EVAL_IDS
    fault_ids = expanded.FAULT_EVAL_IDS

    assert normal_ids == (99, 100)
    assert len(fault_ids) == 17
    assert len(normal_ids + fault_ids) == 19
    assert len(set(normal_ids + fault_ids)) == 19
    assert set(normal_ids).isdisjoint(fault_ids)


def test_recording_metadata():
    normal = expanded.get_recording_metadata(99)
    fault = expanded.get_recording_metadata(144)

    assert normal["label"] == 0
    assert normal["load_hp"] == 2

    assert fault["label"] == 1
    assert fault["condition"] == "outer_race_3"

    with pytest.raises(ValueError, match="Unknown recording ID"):
        expanded.get_recording_metadata(999)


def test_batch_evaluation_uses_frozen_threshold(monkeypatch):
    calls = []

    def fake_evaluation(recording_id, threshold):
        calls.append((recording_id, threshold))
        return {
            "recording_id": recording_id,
            "total_windows": 100,
            "anomalous_windows": 0,
            "anomaly_rate": 0.0,
            "detected": False,
        }

    monkeypatch.setattr(
        expanded,
        "evaluate_rms_recording",
        fake_evaluation,
    )

    results = expanded.evaluate_expanded_stage1()

    expected_ids = (
        expanded.NORMAL_EVAL_IDS + expanded.FAULT_EVAL_IDS
    )

    assert len(results) == 19
    assert [result["recording_id"] for result in results] == list(expected_ids)

    assert all(
        threshold == expanded.FROZEN_RMS_THRESHOLD
        for _, threshold in calls
    )

    assert expanded.FROZEN_RMS_THRESHOLD == 0.07467624803042527
    assert all("condition" in result for result in results)
    assert all("load_hp" in result for result in results)

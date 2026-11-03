import pytest

from src.recording_anomaly_decision import classify_recording


@pytest.mark.parametrize(
    "anomalous, total, expected",
    [
        (4, 100, False),
        (5, 100, False),
        (6, 100, True),
    ],
)
def test_recording_decision(anomalous, total, expected):
    result = classify_recording(anomalous, total)

    assert result == expected


@pytest.mark.parametrize(
    "anomalous, total",
    [
        (0, 0),
        (-1, 100),
        (101, 100),
        (5.5, 100),
        (True, 100),
    ],
)
def test_recording_decision_invalid_counts(anomalous, total):
    with pytest.raises(ValueError):
        classify_recording(anomalous, total)

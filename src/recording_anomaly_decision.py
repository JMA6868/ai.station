"""Recording-level decision for Stage 1 anomaly detection."""


def classify_recording(anomalous, total):
    """Classify a recording using the frozen 5% anomaly-rate cutoff."""

    if (
        not isinstance(anomalous, int)
        or isinstance(anomalous, bool)
        or not isinstance(total, int)
        or isinstance(total, bool)
    ):
        raise ValueError("Window counts must be integers")

    if total <= 0:
        raise ValueError("Total windows must be positive")

    if anomalous < 0 or anomalous > total:
        raise ValueError("Invalid anomalous window count")

    return anomalous / total > 0.05

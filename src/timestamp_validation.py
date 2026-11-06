import math


def validate_timestamps(timestamps, expected_interval, tolerance=1e-6):
    """Return indices where timestamp continuity is broken."""

    if expected_interval <= 0:
        raise ValueError("Expected interval must be positive")

    if tolerance < 0:
        raise ValueError("Tolerance cannot be negative")

    invalid_indices = []

    for i in range(1, len(timestamps)):
        previous = timestamps[i - 1]
        current = timestamps[i]

        if not math.isfinite(previous) or not math.isfinite(current):
            invalid_indices.append(i)
            continue

        interval = current - previous

        if not math.isclose(
            interval,
            expected_interval,
            rel_tol=0.0,
            abs_tol=tolerance
        ):
            invalid_indices.append(i)

    return invalid_indices
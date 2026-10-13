
import csv
import math

from src.sensor_analysis import validate_sensor_value
from src.feature_extraction import calculate_features
from src.timestamp_validation import validate_timestamps


def process_sensor_csv(
    csv_path, window_size, step, expected_interval=1.0
):
    """Extract features from valid, continuous sensor windows."""

    if window_size <= 0 or step <= 0:
        raise ValueError("Window size and step must be positive")

    if not math.isfinite(expected_interval) or expected_interval <= 0:
        raise ValueError("Expected interval must be finite and positive")

    readings = []
    timestamps = []

    with open(csv_path, "r", newline="", encoding="utf-8-sig") as file:
        reader = csv.DictReader(file)

        if not reader.fieldnames or not {"timestamp", "vibration"}.issubset(
            reader.fieldnames
        ):
            raise ValueError("CSV must contain timestamp and vibration columns")

        for row in reader:
            readings.append(validate_sensor_value(row["vibration"]))

            try:
                timestamp = float(row["timestamp"])
            except (ValueError, TypeError):
                timestamp = float("nan")

            timestamps.append(timestamp)

    # Indices of samples whose preceding interval is invalid
    invalid_intervals = set(
        validate_timestamps(timestamps, expected_interval)
    )

    results = []

    for start in range(0, len(readings) - window_size + 1, step):
        end = start + window_size
        window = readings[start:end]

        if any(value is None for value in window):
            continue

        # A window of samples start...end-1 contains
        # intervals ending at start+1...end-1.
        if any(i in invalid_intervals for i in range(start + 1, end)):
            continue

        if not all(math.isfinite(t) for t in timestamps[start:end]):
            continue

        features = calculate_features(window)
        features["start_index"] = start
        features["end_index"] = end - 1
        results.append(features)

    return results

def process_sensor_csv_with_report(
    csv_path, window_size, step, expected_interval=1.0
):
    """Return window features and a data quality report."""

    from src.data_quality import generate_quality_report

    # Reuse the existing validated pipeline
    features = process_sensor_csv(
        csv_path, window_size, step, expected_interval
    )

    # Read data again to collect quality statistics
    readings = []
    timestamps = []

    with open(csv_path, "r", newline="", encoding="utf-8-sig") as file:
        reader = csv.DictReader(file)

        for row in reader:
            readings.append(validate_sensor_value(row["vibration"]))

            try:
                timestamp = float(row["timestamp"])
            except (ValueError, TypeError):
                timestamp = float("nan")

            timestamps.append(timestamp)

    invalid_measurements = sum(
        value is None for value in readings
    )

    # Count unique indices associated with invalid timestamps
    timestamp_indices = set(
        validate_timestamps(timestamps, expected_interval)
    )

    # Also count non-finite timestamps, including the first row
    timestamp_indices.update(
        i for i, t in enumerate(timestamps)
        if not math.isfinite(t)
    )

    total_windows = len(
        range(0, len(readings) - window_size + 1, step)
    )

    report = generate_quality_report(
        total_samples=len(readings),
        invalid_measurements=invalid_measurements,
        timestamp_issues=len(timestamp_indices),
        total_windows=total_windows,
        valid_windows=len(features)
    )

    return features, report

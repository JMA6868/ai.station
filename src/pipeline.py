import csv
import math

from src.sensor_analysis import validate_sensor_value
from src.feature_extraction import calculate_features
from src.timestamp_validation import validate_timestamps
from src.data_quality import generate_quality_report


def _process_csv(csv_path, window_size, step, expected_interval):
    """Shared processing logic. Read CSV only once."""

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

    invalid_intervals = set(
        validate_timestamps(timestamps, expected_interval)
    )

    invalid_intervals.update(
        i for i, timestamp in enumerate(timestamps)
        if not math.isfinite(timestamp)
    )

    features = []
    total_windows = 0

    for start in range(0, len(readings) - window_size + 1, step):
        total_windows += 1

        end = start + window_size
        window = readings[start:end]

        if any(value is None for value in window):
            continue

        if any(i in invalid_intervals for i in range(start + 1, end)):
            continue

        if not all(math.isfinite(t) for t in timestamps[start:end]):
            continue

        result = calculate_features(window)
        result["start_index"] = start
        result["end_index"] = end - 1
        features.append(result)

    report = generate_quality_report(
        total_samples=len(readings),
        invalid_measurements=sum(v is None for v in readings),
        timestamp_issues=len(invalid_intervals),
        total_windows=total_windows,
        valid_windows=len(features)
    )

    return features, report


def process_sensor_csv(
    csv_path, window_size, step, expected_interval=1.0
):
    """Backward-compatible interface returning features only."""

    features, _ = _process_csv(
        csv_path, window_size, step, expected_interval
    )
    return features


def process_sensor_csv_with_report(
    csv_path, window_size, step, expected_interval=1.0
):
    """Return features and quality report."""

    return _process_csv(
        csv_path, window_size, step, expected_interval
    )
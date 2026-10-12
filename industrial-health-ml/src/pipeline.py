import csv

from src.sensor_analysis import validate_sensor_value
from src.feature_extraction import calculate_features


def process_sensor_csv(csv_path, window_size, step):
    """Read, validate, and extract features from CSV data."""

    if window_size <= 0 or step <= 0:
        raise ValueError("Window size and step must be positive")

    readings = []

    with open(csv_path, "r", newline="", encoding="utf-8-sig") as file:
        reader = csv.DictReader(file)

        if not reader.fieldnames or not {"timestamp", "vibration"}.issubset(
            reader.fieldnames
        ):
            raise ValueError("CSV must contain timestamp and vibration columns")

        for row in reader:
            # Keep invalid readings as None to preserve positions
            value = validate_sensor_value(row["vibration"])
            readings.append(value)

    results = []

    for start in range(0, len(readings) - window_size + 1, step):
        window = readings[start:start + window_size]

        # Skip windows containing invalid measurements
        if any(value is None for value in window):
            continue

        features = calculate_features(window)
        features["start_index"] = start
        features["end_index"] = start + window_size - 1
        results.append(features)

    return results
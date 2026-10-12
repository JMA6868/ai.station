# IndustrialSense AI - Statistical Feature Extraction

import math


def calculate_features(values):
    """Calculate mean, population std, and RMS."""

    if len(values) == 0:
        raise ValueError("Sensor data cannot be empty")

    n = len(values)

    # Mean
    mean = sum(values) / n

    # Population standard deviation
    variance = sum((x - mean) ** 2 for x in values) / n
    std = math.sqrt(variance)

    # Root Mean Square
    rms = math.sqrt(sum(x ** 2 for x in values) / n)

    return {
        "mean": mean,
        "std": std,
        "rms": rms
    }

def extract_window_features(values, window_size, step):
    """Extract statistical features from sliding windows."""

    if window_size <= 0 or step <= 0:
        raise ValueError("Window size and step must be positive")

    results = []

    for start in range(0, len(values) - window_size + 1, step):
        window = values[start:start + window_size]

        features = calculate_features(window)

        features["start_index"] = start
        features["end_index"] = start + window_size - 1

        results.append(features)

    return results

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
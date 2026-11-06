# IndustrialSense AI - Exploratory Signal Features

import math


def calculate_crest_factor(values):
    """Calculate peak absolute amplitude divided by RMS."""

    if len(values) == 0:
        raise ValueError("Signal cannot be empty")

    rms = math.sqrt(
        sum(float(x) ** 2 for x in values) / len(values)
    )

    if rms == 0:
        raise ValueError(
            "Crest Factor is undefined for a zero-RMS signal"
        )

    peak = max(abs(float(x)) for x in values)

    return peak / rms

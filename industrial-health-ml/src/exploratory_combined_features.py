"""Exploratory combined vibration features."""

from src.feature_extraction import calculate_features
from src.exploratory_signal_features import calculate_crest_factor


def calculate_combined_features(values):
    """Calculate existing statistics and exploratory crest factor."""

    features = calculate_features(values)

    features["crest_factor"] = calculate_crest_factor(values)

    return features

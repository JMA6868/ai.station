"""Exploratory dual-threshold anomaly detector."""


def is_anomaly(rms, crest_factor, rms_threshold, cf_threshold):
    """Flag an anomaly when RMS or Crest Factor exceeds its threshold."""

    if rms_threshold < 0 or cf_threshold < 0:
        raise ValueError("Thresholds cannot be negative")

    return rms > rms_threshold or crest_factor > cf_threshold

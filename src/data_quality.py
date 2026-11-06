# IndustrialSense AI - Data Quality Reporting


def generate_quality_report(
    total_samples,
    invalid_measurements,
    timestamp_issues,
    total_windows,
    valid_windows
):
    """Create a summary of sensor data quality."""

    if total_samples < 0 or total_windows < 0:
        raise ValueError("Counts cannot be negative")

    if not 0 <= invalid_measurements <= total_samples:
        raise ValueError("Invalid measurement count")

    if not 0 <= timestamp_issues <= total_samples:
        raise ValueError("Invalid timestamp issue count")

    if not 0 <= valid_windows <= total_windows:
        raise ValueError("Invalid window count")

    skipped_windows = total_windows - valid_windows

    if total_samples == 0:
        invalid_rate = 0.0
    else:
        invalid_rate = invalid_measurements / total_samples

    if total_windows == 0:
        window_valid_rate = 0.0
    else:
        window_valid_rate = valid_windows / total_windows

    return {
        "total_samples": total_samples,
        "invalid_measurements": invalid_measurements,
        "timestamp_issues": timestamp_issues,
        "total_windows": total_windows,
        "valid_windows": valid_windows,
        "skipped_windows": skipped_windows,
        "invalid_rate": invalid_rate,
        "window_valid_rate": window_valid_rate
    }
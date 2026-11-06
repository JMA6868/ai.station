# Sensor analysis functions

def detect_anomaly(value, threshold):
    """Return True if the sensor value exceeds the threshold."""
    return value > threshold

def validate_sensor_value(raw_value):
    """Convert a raw sensor reading to a valid number."""

    if raw_value is None or raw_value.strip() == "":
        return None

    try:
        value = float(raw_value)
    except ValueError:
        return None

    if not 0 <= value <= 100:
        return None

    return value

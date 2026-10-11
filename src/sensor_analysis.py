# Sensor analysis functions

def detect_anomaly(value, threshold):
    """Return True if the sensor value exceeds the threshold."""
    return value > threshold

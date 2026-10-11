
from src.sensor_analysis import detect_anomaly


def test_abnormal_value():
    assert detect_anomaly(4.8, 3.0) is True


def test_normal_value():
    assert detect_anomaly(1.5, 3.0) is False


def test_equal_threshold():
    assert detect_anomaly(3.0, 3.0) is False

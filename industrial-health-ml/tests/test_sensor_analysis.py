from src.sensor_analysis import detect_anomaly, validate_sensor_value


def test_abnormal_value():
    assert detect_anomaly(4.8, 3.0) is True


def test_normal_value():
    assert detect_anomaly(1.5, 3.0) is False


def test_equal_threshold():
    assert detect_anomaly(3.0, 3.0) is False


def test_valid_sensor_value():
    assert validate_sensor_value("4.8") == 4.8


def test_missing_sensor_value():
    assert validate_sensor_value("") is None


def test_invalid_sensor_value():
    assert validate_sensor_value("error") is None


def test_out_of_range_value():
    assert validate_sensor_value("-999") is None


def test_boundary_values():
    assert validate_sensor_value("0") == 0.0
    assert validate_sensor_value("100") == 100.0
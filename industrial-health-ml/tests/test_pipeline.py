
import pytest

from src.pipeline import process_sensor_csv


def test_pipeline_with_invalid_values(tmp_path):
    csv_file = tmp_path / "sensor_test.csv"

    csv_file.write_text(
        "timestamp,vibration\n"
        "0,1.2\n"
        "1,1.5\n"
        "2,\n"
        "3,error\n"
        "4,-999\n"
        "5,1.3\n"
        "6,4.8\n"
        "7,1.5\n"
        "8,1.4\n"
        "9,1.3\n"
    )

    results = process_sensor_csv(
        csv_file, window_size=4, step=2
    )

    assert len(results) == 1
    assert results[0]["start_index"] == 6
    assert results[0]["end_index"] == 9
    assert results[0]["mean"] == pytest.approx(2.25)


def test_pipeline_all_valid(tmp_path):
    csv_file = tmp_path / "sensor_valid.csv"

    csv_file.write_text(
        "timestamp,vibration\n"
        "0,1.0\n"
        "1,2.0\n"
        "2,3.0\n"
        "3,4.0\n"
        "4,5.0\n"
        "5,6.0\n"
    )

    results = process_sensor_csv(
        csv_file, window_size=3, step=1
    )

    assert len(results) == 4
    assert results[0]["mean"] == pytest.approx(2.0)
    assert results[-1]["mean"] == pytest.approx(5.0)


def test_pipeline_invalid_header(tmp_path):
    csv_file = tmp_path / "bad_header.csv"

    csv_file.write_text(
        "time,signal\n"
        "0,1.2\n"
    )

    with pytest.raises(ValueError):
        process_sensor_csv(
            csv_file, window_size=2, step=1
        )
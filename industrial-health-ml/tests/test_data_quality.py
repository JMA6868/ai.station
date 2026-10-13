import pytest

from src.data_quality import generate_quality_report


def test_basic_quality_report():
    report = generate_quality_report(10, 3, 0, 4, 1)

    assert report["total_samples"] == 10
    assert report["skipped_windows"] == 3
    assert report["invalid_rate"] == pytest.approx(0.3)
    assert report["window_valid_rate"] == pytest.approx(0.25)


def test_perfect_data_quality():
    report = generate_quality_report(10, 0, 0, 4, 4)

    assert report["skipped_windows"] == 0
    assert report["invalid_rate"] == 0.0
    assert report["window_valid_rate"] == 1.0


def test_empty_dataset():
    report = generate_quality_report(0, 0, 0, 0, 0)

    assert report["invalid_rate"] == 0.0
    assert report["window_valid_rate"] == 0.0


def test_invalid_counts():
    with pytest.raises(ValueError):
        generate_quality_report(10, 11, 0, 4, 1)

    with pytest.raises(ValueError):
        generate_quality_report(10, 0, 0, 4, 5)
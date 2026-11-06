import csv
import math
import pytest

from src.feature_export import export_features_to_csv
from src.feature_schema import CSV_COLUMNS


def test_export_features_to_csv(tmp_path):
    """Verify CSV columns, rows, and split metadata."""

    records = [
        {
            "recording_id": 97,
            "label": 0,
            "start_index": 0,
            "end_index": 1199,
            "mean": 0.01,
            "std": 0.07,
            "rms": 0.071,
        },
        {
            "recording_id": 105,
            "label": 1,
            "start_index": 600,
            "end_index": 1799,
            "mean": 0.02,
            "std": 0.29,
            "rms": 0.291,
        },
    ]

    output_path = tmp_path / "train.csv"

    export_features_to_csv(records, "train", output_path)

    with open(output_path, newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        rows = list(reader)

        assert tuple(reader.fieldnames) == CSV_COLUMNS

    assert len(rows) == 2

    assert rows[0]["recording_id"] == "97"
    assert rows[0]["split"] == "train"
    assert rows[0]["label"] == "0"
    assert float(rows[0]["rms"]) == 0.071

    assert rows[1]["recording_id"] == "105"
    assert rows[1]["split"] == "train"
    assert rows[1]["label"] == "1"
    assert float(rows[1]["rms"]) == 0.291


def test_csv_round_trip(tmp_path):
    """Verify feature values survive CSV export and reload."""

    records = [
        {
            "recording_id": 97,
            "label": 0,
            "start_index": 0,
            "end_index": 1199,
            "mean": 0.012345678901234,
            "std": 0.072345678901234,
            "rms": 0.073456789012345,
        }
    ]

    output_path = tmp_path / "train.csv"

    export_features_to_csv(records, "train", output_path)

    with open(output_path, newline="", encoding="utf-8") as file:
        reloaded = list(csv.DictReader(file))

    assert len(reloaded) == 1

    saved = reloaded[0]
    original = records[0]

    assert saved["split"] == "train"

    for column in ("recording_id", "label", "start_index", "end_index"):
        assert int(saved[column]) == original[column]

    for column in ("mean", "std", "rms"):
        assert math.isclose(
            float(saved[column]),
            original[column],
            rel_tol=1e-12,
            abs_tol=1e-12,
        )
def test_export_rejects_invalid_label(tmp_path):
    """Exporter must reject records with invalid labels."""

    records = [
        {
            "recording_id": 97,
            "label": 9,  # Invalid: only 0 and 1 are allowed
            "start_index": 0,
            "end_index": 1199,
            "mean": 0.01,
            "std": 0.07,
            "rms": 0.08,
        }
    ]

    output_path = tmp_path / "invalid.csv"

    with pytest.raises(ValueError, match="Invalid label"):
        export_features_to_csv(
            records,
            "train",
            output_path,
        )

def test_invalid_record_does_not_create_csv(tmp_path):
    """An invalid dataset must not leave a partial CSV."""

    records = [
        {
            "recording_id": 97,
            "label": 0,
            "start_index": 0,
            "end_index": 1199,
            "mean": 0.01,
            "std": 0.07,
            "rms": 0.08,
        },
        {
            "recording_id": 97,
            "label": 9,
            "start_index": 600,
            "end_index": 1799,
            "mean": 0.02,
            "std": 0.08,
            "rms": 0.09,
        },
    ]

    output_path = tmp_path / "partial.csv"

    with pytest.raises(ValueError, match="Invalid label"):
        export_features_to_csv(records, "train", output_path)

    assert not output_path.exists()
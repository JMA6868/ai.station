# IndustrialSense AI - Feature CSV Import Tests
import pytest
import csv

from src.feature_schema import CSV_COLUMNS
from src.feature_export import export_features_to_csv
from src.feature_import import import_features_from_csv


def test_import_restores_data_types(tmp_path):
    """Verify CSV import restores correct Python types."""

    original = [
        {
            "recording_id": 97,
            "label": 0,
            "start_index": 0,
            "end_index": 1199,
            "mean": 0.012345,
            "std": 0.072345,
            "rms": 0.073456,
        }
    ]

    file_path = tmp_path / "train.csv"

    export_features_to_csv(
        original,
        split_name="train",
        output_path=file_path,
    )

    imported = import_features_from_csv(file_path)

    assert len(imported) == 1

    row = imported[0]

    assert row["recording_id"] == 97
    assert row["split"] == "train"
    assert row["label"] == 0
    assert row["start_index"] == 0
    assert row["end_index"] == 1199

    assert row["mean"] == original[0]["mean"]
    assert row["std"] == original[0]["std"]
    assert row["rms"] == original[0]["rms"]

    assert type(row["recording_id"]) is int
    assert type(row["label"]) is int
    assert type(row["mean"]) is float
    assert type(row["std"]) is float
    assert type(row["rms"]) is float

    import pytest


def test_reject_invalid_csv_schema(tmp_path):
    """Reject CSV files with missing required columns."""

    file_path = tmp_path / "invalid.csv"

    file_path.write_text(
        "recording_id,split,label,mean,std\n"
        "97,train,0,0.01,0.07\n",
        encoding="utf-8",
    )

    with pytest.raises(
        ValueError,
        match="CSV schema does not match expected columns"
    ):
        import_features_from_csv(file_path)

@pytest.mark.parametrize(
    "invalid_value",
    ["nan", "inf", "-inf"],
)
def test_reject_nonfinite_features(tmp_path, invalid_value):
    """Reject NaN and Infinity in feature columns."""

    file_path = tmp_path / "invalid_features.csv"

    file_path.write_text(
        "recording_id,split,label,start_index,end_index,mean,std,rms\n"
        f"97,train,0,0,1199,0.01,0.07,{invalid_value}\n",
        encoding="utf-8",
    )

    with pytest.raises(
        ValueError,
        match="Non-finite feature"
    ):
        import_features_from_csv(file_path)

@pytest.mark.parametrize(
    "field,invalid_value,expected_error",
    [
        ("split", "unknown", "Invalid split"),
        ("label", "9", "Invalid label"),
        ("recording_id", "0", "Invalid metadata"),
        ("start_index", "-1", "Invalid metadata"),
        ("end_index", "-1", "Invalid metadata"),
    ],
)
def test_reject_invalid_metadata(
    tmp_path, field, invalid_value, expected_error
):
    """Reject invalid split, label, and window metadata."""

    row = {
        "recording_id": "97",
        "split": "train",
        "label": "0",
        "start_index": "0",
        "end_index": "1199",
        "mean": "0.01",
        "std": "0.07",
        "rms": "0.08",
    }

    row[field] = invalid_value

    file_path = tmp_path / "invalid_metadata.csv"

    with open(file_path, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=CSV_COLUMNS)
        writer.writeheader()
        writer.writerow(row)

    with pytest.raises(ValueError, match=expected_error):
        import_features_from_csv(file_path)
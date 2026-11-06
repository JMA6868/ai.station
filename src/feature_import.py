# IndustrialSense AI - Feature Dataset CSV Importer

import csv
from pathlib import Path

from src.feature_schema import CSV_COLUMNS
from src.feature_validation import validate_feature_record


def import_features_from_csv(file_path):
    """Load a feature CSV and restore Python data types."""

    file_path = Path(file_path)
    records = []

    with open(file_path, "r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        if tuple(reader.fieldnames or ()) != CSV_COLUMNS:
            raise ValueError("CSV schema does not match expected columns")

        for row_number, row in enumerate(reader, start=2):
            try:
                record = {
                    "recording_id": int(row["recording_id"]),
                    "split": row["split"],
                    "label": int(row["label"]),
                    "start_index": int(row["start_index"]),
                    "end_index": int(row["end_index"]),
                    "mean": float(row["mean"]),
                    "std": float(row["std"]),
                    "rms": float(row["rms"]),
                }
            except (ValueError, TypeError, KeyError) as error:
                raise ValueError(
                    f"Invalid data at CSV row {row_number}"
                ) from error

            try:
                validate_feature_record(record)
            except ValueError as error:
                raise ValueError(
                    f"{error} at CSV row {row_number}"
                ) from error
            
            records.append(record)

    return records

# IndustrialSense AI - Feature Record Validation

import math

from src.feature_schema import CSV_COLUMNS, FEATURE_COLUMNS


VALID_SPLITS = {"train", "validation", "test"}


def validate_feature_record(record):
    """Validate one typed feature record."""

    if set(record) != set(CSV_COLUMNS):
        raise ValueError("Invalid feature record schema")

    if record["split"] not in VALID_SPLITS:
        raise ValueError("Invalid split")

    integer_fields = (
        "recording_id",
        "label",
        "start_index",
        "end_index",
    )

    for field in integer_fields:
        if type(record[field]) is not int:
            raise ValueError(f"Invalid integer field: {field}")

    if record["label"] not in {0, 1}:
        raise ValueError("Invalid label")

    if (
        record["recording_id"] <= 0
        or record["start_index"] < 0
        or record["end_index"] < record["start_index"]
    ):
        raise ValueError("Invalid metadata")

    for field in FEATURE_COLUMNS:
        value = record[field]

        if not isinstance(value, (int, float)):
            raise ValueError(f"Invalid feature type: {field}")

        if not math.isfinite(value):
            raise ValueError("Non-finite feature")
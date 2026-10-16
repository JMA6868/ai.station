# IndustrialSense AI - Feature Dataset CSV Exporter

import csv
from pathlib import Path
from src.feature_validation import validate_feature_record
from src.feature_schema import CSV_COLUMNS


def export_features_to_csv(records, split_name, output_path):
    """Export window-level features to a structured CSV file."""

    if split_name not in {"train", "validation", "test"}:
        raise ValueError(f"Unknown split: {split_name}")

    if not records:
        raise ValueError("Cannot export an empty dataset")

        # Phase 1: Prepare and validate all records before writing.
    validated_rows = []

    for record in records:
        row = {
            **record,
            "split": split_name,
            "mean": float(record["mean"]),
            "std": float(record["std"]),
            "rms": float(record["rms"]),
        }

        validate_feature_record(row)
        validated_rows.append(row)

    # Phase 2: Write only after all records pass validation.
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(
            file,
            fieldnames=CSV_COLUMNS,
            extrasaction="raise",
        )

        writer.writeheader()
        writer.writerows(validated_rows)

    return output_path
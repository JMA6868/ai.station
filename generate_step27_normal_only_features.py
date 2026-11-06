# IndustrialSense AI - Step 27.11 Normal-only Feature Generator

from pathlib import Path

from src.evaluation_dataset import build_evaluation_dataset
from src.feature_export import export_features_to_csv
from src.normal_only_split import (
    NORMAL_ONLY_SPLIT,
    validate_normal_only_split,
)


OUTPUT_DIR = Path("data/processed/step27_normal_only")

EXPECTED_WINDOWS = {
    "train": 1210,
    "validation": 807,
}

EXPECTED_RECORDING_IDS = {
    "train": {97, 98},
    "validation": {99},
}


def generate_normal_only_features():
    """Generate exploratory Normal-only feature datasets."""

    validate_normal_only_split()

    for split_name in ("train", "validation"):
        records = build_evaluation_dataset(
            split_name=split_name,
            dataset_split=NORMAL_ONLY_SPLIT,
        )

        actual_ids = {
            record["recording_id"]
            for record in records
        }

        if actual_ids != EXPECTED_RECORDING_IDS[split_name]:
            raise ValueError(
                f"{split_name}: unexpected recording IDs"
            )

        if len(records) != EXPECTED_WINDOWS[split_name]:
            raise ValueError(
                f"{split_name}: unexpected window count"
            )

        if any(record["label"] != 0 for record in records):
            raise ValueError(
                f"{split_name}: found non-Normal labels"
            )

        output_path = OUTPUT_DIR / f"{split_name}.csv"

        export_features_to_csv(
            records=records,
            split_name=split_name,
            output_path=output_path,
        )

        print(
            f"{split_name}: "
            f"{len(records)} windows, "
            f"recordings={sorted(actual_ids)}, "
            f"saved={output_path}"
        )


if __name__ == "__main__":
    generate_normal_only_features()

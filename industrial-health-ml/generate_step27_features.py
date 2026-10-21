# IndustrialSense AI - Step 27 Feature Dataset Generator

from pathlib import Path

from src.cross_load_split import (
    CROSS_LOAD_SPLIT,
    validate_cross_load_split,
)
from src.evaluation_dataset import build_evaluation_dataset
from src.feature_export import export_features_to_csv
from src.evaluation_config import WINDOW_SIZE, WINDOW_STEP


OUTPUT_DIR = Path(__file__).resolve().parent / "data" / "processed" / "step27"

SPLIT_EXPORT_NAMES = {
    "train": "train",
    "validation": "validation",
    "evaluation": "test",
}


def generate_step27_features():
    """Generate separate CSV feature datasets for Experiment A."""

    validate_cross_load_split()

    for split_name, export_name in SPLIT_EXPORT_NAMES.items():
        print(f"Processing {split_name}...")

        records = build_evaluation_dataset(
            split_name,
            window_size=WINDOW_SIZE,
            step=WINDOW_STEP,
            dataset_split=CROSS_LOAD_SPLIT,
        )

        output_path = OUTPUT_DIR / f"{export_name}.csv"

        export_features_to_csv(
            records,
            split_name=export_name,
            output_path=output_path,
        )

        print(
            f"  Records: {len(records)}"
        )
        print(
            f"  Output: {output_path}"
        )

    print("\nStep 27 Feature Dataset Generation: COMPLETED")


if __name__ == "__main__":
    generate_step27_features()
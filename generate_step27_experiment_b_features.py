# IndustrialSense AI - Step 27 Experiment B Feature Generator

from pathlib import Path

from src.held_out_fault_split import (
    HELD_OUT_FAULT_SPLIT,
    validate_held_out_fault_split,
)
from src.evaluation_dataset import build_evaluation_dataset
from src.feature_export import export_features_to_csv
from src.evaluation_config import WINDOW_SIZE, WINDOW_STEP


OUTPUT_DIR = (
    Path(__file__).resolve().parent
    / "data"
    / "processed"
    / "step27_experiment_b"
)

SPLIT_EXPORT_NAMES = {
    "train": "train",
    "validation": "validation",
    "evaluation": "test",
}


def generate_experiment_b_features():
    """Generate feature datasets for the held-out Ball Fault experiment."""

    validate_held_out_fault_split()

    for split_name, export_name in SPLIT_EXPORT_NAMES.items():
        print(f"Processing {split_name}...")

        records = build_evaluation_dataset(
            split_name,
            window_size=WINDOW_SIZE,
            step=WINDOW_STEP,
            dataset_split=HELD_OUT_FAULT_SPLIT,
        )

        output_path = OUTPUT_DIR / f"{export_name}.csv"

        export_features_to_csv(
            records,
            split_name=export_name,
            output_path=output_path,
        )

        print(f"  Records: {len(records)}")
        print(f"  Output: {output_path}")

    print(
        "\nStep 27 Experiment B Feature Generation: COMPLETED"
    )


if __name__ == "__main__":
    generate_experiment_b_features()
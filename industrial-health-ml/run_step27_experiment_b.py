# IndustrialSense AI - Step 27 Experiment B Training / Validation

from pathlib import Path

from run_ml_baseline import (
    make_xy,
    validate_dataset_split,
    validate_recording_isolation,
)
from run_step27_cross_load import evaluate_per_recording

from src.cwru_metadata import CWRU_RECORDING_METADATA
from src.held_out_fault_split import (
    HELD_OUT_FAULT_SPLIT,
    EXPECTED_LOADS,
    validate_held_out_fault_split,
)
from src.feature_import import import_features_from_csv
from src.feature_schema import FEATURE_COLUMNS
from src.ml_baseline import create_baseline_pipeline
from src.ml_evaluation import evaluate_classifier


DATA_DIR = (
    Path(__file__).resolve().parent
    / "data"
    / "processed"
    / "step27_experiment_b"
)


def validate_experiment_b_records(records, split_name):
    """Validate train/validation data against frozen Experiment B."""

    if split_name not in ("train", "validation"):
        raise ValueError(f"Unsupported split: {split_name}")

    if not records:
        raise ValueError(f"Empty dataset: {split_name}")

    expected_ids = {
        recording_id
        for ids in HELD_OUT_FAULT_SPLIT[split_name].values()
        for recording_id in ids
    }

    actual_ids = {row["recording_id"] for row in records}

    if actual_ids != expected_ids:
        raise ValueError(
            f"{split_name}: recording IDs differ from frozen protocol"
        )

    for row in records:
        recording_id = row["recording_id"]
        metadata = CWRU_RECORDING_METADATA[recording_id]

        if row["label"] != metadata["label"]:
            raise ValueError(
                f"Recording {recording_id}: incorrect label"
            )

        if metadata["load_hp"] not in EXPECTED_LOADS[split_name]:
            raise ValueError(
                f"Recording {recording_id}: incorrect motor load"
            )

        if metadata["condition"] == "ball":
            raise ValueError(
                "Ball Fault cannot enter training or validation"
            )


def main():
    """Train without Ball Fault and validate on 2 HP."""

    validate_held_out_fault_split()

    # Read only Training and Validation data.
    train = import_features_from_csv(DATA_DIR / "train.csv")
    validation = import_features_from_csv(
        DATA_DIR / "validation.csv"
    )

    validate_dataset_split(train, "train")
    validate_dataset_split(validation, "validation")

    validate_experiment_b_records(train, "train")
    validate_experiment_b_records(validation, "validation")

    train_ids, val_ids = validate_recording_isolation(
        train, validation
    )

    X_train, y_train = make_xy(train)
    X_val, y_val = make_xy(validation)

    model = create_baseline_pipeline()

    # Fit scaler and classifier on Training data only.
    model.fit(X_train, y_train)

    train_pred = model.predict(X_train)
    val_pred = model.predict(X_val)

    train_metrics = evaluate_classifier(y_train, train_pred)
    val_metrics = evaluate_classifier(y_val, val_pred)

    print("IndustrialSense AI - Experiment B Baseline")
    print("Features:", FEATURE_COLUMNS)
    print("Training recordings:", sorted(train_ids))
    print("Validation recordings:", sorted(val_ids))

    for name, count, metrics in (
        ("Training", len(y_train), train_metrics),
        ("Validation", len(y_val), val_metrics),
    ):
        print(f"\n{name} - {count} windows")
        for metric, value in metrics.items():
            print(f"{metric}: {value}")

    per_recording = evaluate_per_recording(
        validation,
        val_pred,
    )

    print("\nValidation - Per-recording Results")

    for recording_id, result in per_recording.items():
        metadata = CWRU_RECORDING_METADATA[recording_id]

        print(
            f"ID={recording_id}, "
            f"Condition={metadata['condition']}, "
            f"Load={metadata['load_hp']} HP, "
            f"Windows={result['total']}, "
            f"Correct={result['correct']}, "
            f"Accuracy={result['accuracy']:.4f}"
        )

    print("\nExperiment B Train/Validation: COMPLETED")


if __name__ == "__main__":
    main()
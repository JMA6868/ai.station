# IndustrialSense AI - Step 27 Cross-load ML Baseline

from pathlib import Path

from run_ml_baseline import (
    make_xy,
    validate_dataset_split,
    validate_recording_isolation,
)
from src.feature_import import import_features_from_csv
from src.feature_schema import FEATURE_COLUMNS
from src.ml_baseline import create_baseline_pipeline
from src.ml_evaluation import evaluate_classifier
from src.cross_load_split import (
    CROSS_LOAD_SPLIT,
    validate_cross_load_split,
)

from src.cwru_metadata import CWRU_RECORDING_METADATA

DATA_DIR = (
    Path(__file__).resolve().parent
    / "data"
    / "processed"
    / "step27"
)

def validate_cross_load_records(records, split_name):
    """Validate recording IDs, labels and loads against protocol."""

    expected_ids = {
        recording_id
        for ids in CROSS_LOAD_SPLIT[split_name].values()
        for recording_id in ids
    }

    expected_loads = {
        "train": {0, 1},
        "validation": {2},
    }

    if split_name not in expected_loads:
        raise ValueError(f"Unsupported split: {split_name}")

    actual_ids = {row["recording_id"] for row in records}

    if actual_ids != expected_ids:
        raise ValueError(
            f"{split_name}: recording IDs do not match protocol"
        )

    for row in records:
        recording_id = row["recording_id"]
        metadata = CWRU_RECORDING_METADATA[recording_id]

        if row["label"] != metadata["label"]:
            raise ValueError(
                f"Recording {recording_id}: incorrect label"
            )

        if metadata["load_hp"] not in expected_loads[split_name]:
            raise ValueError(
                f"Recording {recording_id}: incorrect motor load"
            )

from collections import defaultdict


def evaluate_per_recording(records, predictions):
    """Evaluate classification accuracy for each recording."""

    if len(records) != len(predictions):
        raise ValueError(
            "Records and predictions must have equal lengths"
        )

    if not records:
        raise ValueError("Cannot evaluate empty records")

    grouped = defaultdict(lambda: {"total": 0, "correct": 0})

    for row, predicted_label in zip(records, predictions):
        recording_id = row["recording_id"]
        actual_label = row["label"]

        grouped[recording_id]["total"] += 1

        if actual_label == predicted_label:
            grouped[recording_id]["correct"] += 1

    results = {}

    for recording_id in sorted(grouped):
        total = grouped[recording_id]["total"]
        correct = grouped[recording_id]["correct"]

        results[recording_id] = {
            "total": total,
            "correct": correct,
            "accuracy": correct / total,
        }

    return results

def main():
    """Train on 0-1 HP and validate on 2 HP."""

    validate_cross_load_split()

    train = import_features_from_csv(DATA_DIR / "train.csv")
    validation = import_features_from_csv(
        DATA_DIR / "validation.csv"
    )

    validate_dataset_split(train, "train")
    validate_dataset_split(validation, "validation")
    validate_cross_load_records(train, "train")
    validate_cross_load_records(validation, "validation")

    train_ids, val_ids = validate_recording_isolation(
        train, validation
    )

    # Verify recording identities against the frozen protocol.
    expected_train = set(
        CROSS_LOAD_SPLIT["train"][0]
        + CROSS_LOAD_SPLIT["train"][1]
    )
    expected_val = set(
        CROSS_LOAD_SPLIT["validation"][0]
        + CROSS_LOAD_SPLIT["validation"][1]
    )

    if train_ids != expected_train or val_ids != expected_val:
        raise ValueError(
            "Recording IDs do not match frozen Step 27 split"
        )

    X_train, y_train = make_xy(train)
    X_val, y_val = make_xy(validation)

    model = create_baseline_pipeline()

    # Both scaler and classifier are fitted on training only.
    model.fit(X_train, y_train)

    train_pred = model.predict(X_train)
    val_pred = model.predict(X_val)

    train_metrics = evaluate_classifier(y_train, train_pred)
    val_metrics = evaluate_classifier(y_val, val_pred)

    print("IndustrialSense AI - Step 27 Cross-load Baseline")
    print("Features:", FEATURE_COLUMNS)
    print("Train recordings:", sorted(train_ids))
    print("Validation recordings:", sorted(val_ids))

    for name, count, metrics in (
        ("Training", len(y_train), train_metrics),
        ("Validation", len(y_val), val_metrics),
    ):
        print(f"\n{name} - {count} windows")
        for metric, value in metrics.items():
            print(f"{metric}: {value}")

    # Per-recording validation analysis.
    per_recording = evaluate_per_recording(
        validation,
        val_pred,
    )

    print("\nValidation - Per-recording Results")

    for recording_id, metrics in per_recording.items():
        metadata = CWRU_RECORDING_METADATA[recording_id]

        print(
            f"ID={recording_id}, "
            f"Condition={metadata['condition']}, "
            f"Load={metadata['load_hp']} HP, "
            f"Windows={metrics['total']}, "
            f"Correct={metrics['correct']}, "
            f"Accuracy={metrics['accuracy']:.4f}"
        )

    print("\nStep 27 Cross-load Train/Validation: COMPLETED")


if __name__ == "__main__":
    main()
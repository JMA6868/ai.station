# IndustrialSense AI - Reproducible ML Baseline Runner

from pathlib import Path

from src.feature_import import import_features_from_csv
from src.feature_schema import FEATURE_COLUMNS, TARGET_COLUMN
from src.ml_baseline import create_baseline_pipeline
from src.ml_evaluation import evaluate_classifier


DATA_DIR = Path(__file__).resolve().parent / "data" / "processed"


def make_xy(records):
    """Separate feature inputs X and target labels y."""
    X = [
        [row[column] for column in FEATURE_COLUMNS]
        for row in records
    ]
    y = [row[TARGET_COLUMN] for row in records]
    return X, y

def validate_dataset_split(records, expected_split):
    """Verify every record belongs to the expected dataset split."""

    if not records:
        raise ValueError(f"Empty dataset: {expected_split}")

    for row in records:
        if row["split"] != expected_split:
            raise ValueError(
                f"Invalid dataset split: expected {expected_split}"
            )

def validate_recording_isolation(train, validation):
    """Reject overlapping recordings across dataset splits."""

    train_ids = {row["recording_id"] for row in train}
    validation_ids = {row["recording_id"] for row in validation}

    if not train_ids.isdisjoint(validation_ids):
        raise ValueError(
            "Training and validation recordings must not overlap"
        )

    return train_ids, validation_ids

def main():
    """Train on training data and evaluate on validation data."""

    train = import_features_from_csv(DATA_DIR / "train.csv")
    validation = import_features_from_csv(
        DATA_DIR / "validation.csv"
    )

    # Verify split metadata and recording isolation.
    validate_dataset_split(train, "train")
    validate_dataset_split(validation, "validation")

    train_ids, validation_ids = validate_recording_isolation(
        train, validation
    )

    X_train, y_train = make_xy(train)
    X_val, y_val = make_xy(validation)

    model = create_baseline_pipeline()

    # Fit the complete pipeline using training data only.
    model.fit(X_train, y_train)

    # Evaluate training fit and independent validation.
    train_metrics = evaluate_classifier(
        y_train, model.predict(X_train)
    )
    val_metrics = evaluate_classifier(
        y_val, model.predict(X_val)
    )

    print("IndustrialSense AI - ML Baseline")
    print("Features:", FEATURE_COLUMNS)
    print("Train recordings:", sorted(train_ids))
    print("Validation recordings:", sorted(validation_ids))

    for name, count, metrics in (
        ("Training", len(y_train), train_metrics),
        ("Validation", len(y_val), val_metrics),
    ):
        print(f"\n{name} - {count} windows")
        for metric, value in metrics.items():
            print(f"{metric}: {value}")

    print("\nML baseline runner: COMPLETED")


if __name__ == "__main__":
    main()

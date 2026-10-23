# IndustrialSense AI - Step 27 Frozen Cross-load Evaluation

from pathlib import Path

from run_ml_baseline import (
    make_xy,
    validate_dataset_split,
    validate_recording_isolation,
)
from run_step27_cross_load import (
    evaluate_per_recording,
    validate_cross_load_records,
)
from src.cross_load_split import (
    CROSS_LOAD_SPLIT,
    validate_cross_load_split,
)
from src.cwru_metadata import CWRU_RECORDING_METADATA
from src.feature_import import import_features_from_csv
from src.feature_schema import FEATURE_COLUMNS
from src.ml_baseline import create_baseline_pipeline
from src.ml_evaluation import evaluate_classifier


DATA_DIR = (
    Path(__file__).resolve().parent
    / "data"
    / "processed"
    / "step27"
)


def main():
    """Evaluate frozen baseline on the 3 HP dataset."""

    validate_cross_load_split()

    train = import_features_from_csv(DATA_DIR / "train.csv")
    evaluation = import_features_from_csv(DATA_DIR / "test.csv")

    validate_dataset_split(train, "train")
    validate_dataset_split(evaluation, "test")

    # Evaluation is named "test" in the existing CSV schema.
    validate_cross_load_records(train, "train")

    expected_ids = {
        recording_id
        for ids in CROSS_LOAD_SPLIT["evaluation"].values()
        for recording_id in ids
    }

    actual_ids = {
        row["recording_id"]
        for row in evaluation
    }

    if actual_ids != expected_ids:
        raise ValueError(
            "Evaluation recordings do not match frozen protocol"
        )

    for row in evaluation:
        metadata = CWRU_RECORDING_METADATA[row["recording_id"]]

        if row["label"] != metadata["label"]:
            raise ValueError("Incorrect evaluation label")

        if metadata["load_hp"] != 3:
            raise ValueError("Incorrect evaluation motor load")

    train_ids, eval_ids = validate_recording_isolation(
        train,
        evaluation,
    )

    X_train, y_train = make_xy(train)
    X_eval, y_eval = make_xy(evaluation)

    model = create_baseline_pipeline()

    # Fit StandardScaler and classifier on 0-1 HP only.
    model.fit(X_train, y_train)

    # Frozen evaluation: no fitting on 3 HP.
    eval_pred = model.predict(X_eval)

    metrics = evaluate_classifier(y_eval, eval_pred)
    per_recording = evaluate_per_recording(
        evaluation,
        eval_pred,
    )

    print("IndustrialSense AI - Step 27 Frozen Evaluation")
    print("Features:", FEATURE_COLUMNS)
    print("Training recordings:", sorted(train_ids))
    print("Evaluation recordings:", sorted(eval_ids))

    print("\nEvaluation - Overall Metrics")
    for metric, value in metrics.items():
        print(f"{metric}: {value}")

    print("\nEvaluation - Per-recording Results")

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

    print("\nStep 27 Frozen Evaluation: COMPLETED")


if __name__ == "__main__":
    main()
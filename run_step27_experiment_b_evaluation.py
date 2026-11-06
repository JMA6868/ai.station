# IndustrialSense AI - Step 27 Experiment B Frozen Evaluation

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


def validate_evaluation_records(records):
    """Validate the frozen Normal and Ball Fault evaluation recordings."""

    if not records:
        raise ValueError("Empty evaluation dataset")

    expected_ids = {
        recording_id
        for ids in HELD_OUT_FAULT_SPLIT["evaluation"].values()
        for recording_id in ids
    }

    actual_ids = {row["recording_id"] for row in records}

    if actual_ids != expected_ids:
        raise ValueError(
            "Evaluation recording IDs differ from frozen protocol"
        )

    for row in records:
        recording_id = row["recording_id"]
        metadata = CWRU_RECORDING_METADATA[recording_id]

        if row["label"] != metadata["label"]:
            raise ValueError(
                f"Recording {recording_id}: incorrect label"
            )

        if metadata["load_hp"] not in EXPECTED_LOADS["evaluation"]:
            raise ValueError(
                f"Recording {recording_id}: incorrect motor load"
            )

    ball_ids = {
        rid for rid in actual_ids
        if CWRU_RECORDING_METADATA[rid]["condition"] == "ball"
    }

    if ball_ids != {121}:
        raise ValueError(
            "Held-out Ball Fault recording does not match protocol"
        )


def main():
    """Evaluate the frozen model on Normal 100 and Ball Fault 121."""

    validate_held_out_fault_split()

    train = import_features_from_csv(DATA_DIR / "train.csv")
    evaluation = import_features_from_csv(DATA_DIR / "test.csv")

    validate_dataset_split(train, "train")
    validate_dataset_split(evaluation, "test")

    # Import locally to reuse the Experiment B training checks.
    from run_step27_experiment_b import validate_experiment_b_records

    validate_experiment_b_records(train, "train")
    validate_evaluation_records(evaluation)

    train_ids, eval_ids = validate_recording_isolation(
        train, evaluation
    )

    X_train, y_train = make_xy(train)
    X_eval, y_eval = make_xy(evaluation)

    model = create_baseline_pipeline()

    # Fit only on Training: Normal, Inner Race, Outer Race.
    model.fit(X_train, y_train)

    # Frozen evaluation: no fitting on Ball Fault data.
    eval_pred = model.predict(X_eval)

    metrics = evaluate_classifier(y_eval, eval_pred)
    per_recording = evaluate_per_recording(
        evaluation, eval_pred
    )

    print("IndustrialSense AI - Experiment B Frozen Evaluation")
    print("Features:", FEATURE_COLUMNS)
    print("Training recordings:", sorted(train_ids))
    print("Evaluation recordings:", sorted(eval_ids))

    print("\nEvaluation - Overall Metrics")

    for metric, value in metrics.items():
        print(f"{metric}: {value}")

    print("\nEvaluation - Per-recording Results")

    for recording_id, result in per_recording.items():
        metadata = CWRU_RECORDING_METADATA[recording_id]

        metric_name = (
            "Specificity"
            if metadata["label"] == 0
            else "Recall"
        )

        print(
            f"ID={recording_id}, "
            f"Condition={metadata['condition']}, "
            f"Load={metadata['load_hp']} HP, "
            f"Windows={result['total']}, "
            f"Correct={result['correct']}, "
            f"{metric_name}={result['accuracy']:.4f}"
        )

    print("\nExperiment B Frozen Evaluation: COMPLETED")


if __name__ == "__main__":
    main()
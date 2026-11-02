"""Multiclass fault diagnosis evaluation utilities."""

from sklearn.metrics import (
    accuracy_score,
    confusion_matrix,
    f1_score,
    recall_score,
)


FAULT_LABELS = (0, 1, 2)


def evaluate_multiclass_classifier(y_true, y_pred):
    """Evaluate predictions for three known fault classes."""

    if len(y_true) == 0:
        raise ValueError("Cannot evaluate an empty dataset")

    if len(y_true) != len(y_pred):
        raise ValueError(
            "True and predicted labels must have equal lengths"
        )

    if any(label not in FAULT_LABELS for label in y_true):
        raise ValueError("Invalid true fault label")

    if any(label not in FAULT_LABELS for label in y_pred):
        raise ValueError("Invalid predicted fault label")

    matrix = confusion_matrix(
        y_true,
        y_pred,
        labels=list(FAULT_LABELS),
    )

    return {
        "confusion_matrix": matrix.tolist(),
        "class_support": {
            label: int(matrix[index].sum())
            for index, label in enumerate(FAULT_LABELS)
        },
        "accuracy": float(accuracy_score(y_true, y_pred)),
        "macro_f1": float(
            f1_score(
                y_true, y_pred,
                labels=list(FAULT_LABELS),
                average="macro",
                zero_division=0,
            )
        ),
        "per_class_recall": {
            label: float(score)
            for label, score in zip(
                FAULT_LABELS,
                recall_score(
                    y_true, y_pred,
                    labels=list(FAULT_LABELS),
                    average=None,
                    zero_division=0,
                ),
            )
        },
    }

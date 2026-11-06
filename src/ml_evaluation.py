# IndustrialSense AI - ML Classification Evaluation

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
)


def evaluate_classifier(y_true, y_pred):
    """Calculate binary classification metrics."""

    if len(y_true) == 0:
        raise ValueError("Cannot evaluate an empty dataset")

    if len(y_true) != len(y_pred):
        raise ValueError("True and predicted labels must have equal lengths")
    valid_labels = {0, 1}

    if (
        any(label not in valid_labels for label in y_true)
        or any(label not in valid_labels for label in y_pred)
    ):
        raise ValueError("Invalid binary label: expected 0 or 1")

    tn, fp, fn, tp = confusion_matrix(
        y_true,
        y_pred,
        labels=[0, 1],
    ).ravel()

    specificity = (
        tn / (tn + fp)
        if (tn + fp) > 0
        else 0.0
    )

    sensitivity = (
        tp / (tp + fn)
        if (tp + fn) > 0
        else 0.0
    )

    balanced_accuracy = (sensitivity + specificity) / 2

    return {
        "accuracy": float(accuracy_score(y_true, y_pred)),
        "precision": float(
            precision_score(y_true, y_pred, zero_division=0)
        ),
        "recall": float(
            recall_score(y_true, y_pred, zero_division=0)
        ),
        "f1": float(
            f1_score(y_true, y_pred, zero_division=0)
        ),
        "tn": int(tn),
        "fp": int(fp),
        "fn": int(fn),
        "tp": int(tp),
        "specificity": float(specificity),
        "balanced_accuracy": float(balanced_accuracy),
    }
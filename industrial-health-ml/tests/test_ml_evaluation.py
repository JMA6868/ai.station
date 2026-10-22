# IndustrialSense AI - ML Evaluation Tests

import pytest

from src.ml_evaluation import evaluate_classifier


def test_perfect_classification():
    """Verify metrics when all predictions are correct."""

    y_true = [0, 0, 1, 1]
    y_pred = [0, 0, 1, 1]

    result = evaluate_classifier(y_true, y_pred)

    assert result["tn"] == 2
    assert result["fp"] == 0
    assert result["fn"] == 0
    assert result["tp"] == 2

    assert result["accuracy"] == 1.0
    assert result["precision"] == 1.0
    assert result["recall"] == 1.0
    assert result["f1"] == 1.0


def test_imperfect_classification():
    """Verify metrics with false positives and negatives."""

    y_true = [0, 0, 0, 1, 1, 1]
    y_pred = [0, 1, 0, 1, 0, 1]

    result = evaluate_classifier(y_true, y_pred)

    assert result["tn"] == 2
    assert result["fp"] == 1
    assert result["fn"] == 1
    assert result["tp"] == 2

    assert result["accuracy"] == pytest.approx(4 / 6)
    assert result["precision"] == pytest.approx(2 / 3)
    assert result["recall"] == pytest.approx(2 / 3)
    assert result["f1"] == pytest.approx(2 / 3)

def test_reject_empty_dataset():
    """Reject evaluation without observations."""

    with pytest.raises(ValueError, match="empty dataset"):
        evaluate_classifier([], [])


def test_reject_mismatched_lengths():
    """Reject unequal true and predicted label counts."""

    with pytest.raises(ValueError, match="equal lengths"):
        evaluate_classifier([0, 1], [0])

@pytest.mark.parametrize(
    "y_true,y_pred",
    [
        ([0, 2, 1], [0, 1, 1]),
        ([0, 1, 1], [0, 2, 1]),
    ],
)
def test_reject_invalid_binary_labels(y_true, y_pred):
    """Reject labels outside the binary classification schema."""

    with pytest.raises(ValueError, match="Invalid binary label"):
        evaluate_classifier(y_true, y_pred)

def test_specificity_and_balanced_accuracy():
    """Verify metrics when normal and fault detection differ."""

    # TN=3, FP=1, FN=2, TP=2
    y_true = [0, 0, 0, 0, 1, 1, 1, 1]
    y_pred = [0, 0, 0, 1, 0, 0, 1, 1]

    result = evaluate_classifier(y_true, y_pred)

    assert result["tn"] == 3
    assert result["fp"] == 1
    assert result["fn"] == 2
    assert result["tp"] == 2

    assert result["specificity"] == pytest.approx(0.75)
    assert result["recall"] == pytest.approx(0.50)
    assert result["balanced_accuracy"] == pytest.approx(0.625)


def test_specificity_with_no_normal_samples():
    """Check the current convention for missing normal samples."""

    y_true = [1, 1, 1]
    y_pred = [1, 1, 0]

    result = evaluate_classifier(y_true, y_pred)

    assert result["specificity"] == 0.0
    assert result["recall"] == pytest.approx(2 / 3)
    assert result["balanced_accuracy"] == pytest.approx(1 / 3)
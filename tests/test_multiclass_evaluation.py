import pytest

from src.multiclass_evaluation import evaluate_multiclass_classifier


def test_multiclass_confusion_matrix():
    y_true = [0, 0, 1, 1, 2, 2]
    y_pred = [0, 1, 1, 1, 2, 0]

    result = evaluate_multiclass_classifier(y_true, y_pred)

    assert result["confusion_matrix"] == [
        [1, 1, 0],
        [0, 2, 0],
        [1, 0, 1],
    ]


def test_multiclass_accuracy():
    result = evaluate_multiclass_classifier(
        [0, 0, 1, 1, 2, 2],
        [0, 1, 1, 1, 2, 0],
    )

    assert result["accuracy"] == pytest.approx(4 / 6)


def test_multiclass_empty_input():
    with pytest.raises(ValueError, match="empty dataset"):
        evaluate_multiclass_classifier([], [])


def test_multiclass_mismatched_lengths():
    with pytest.raises(ValueError, match="equal lengths"):
        evaluate_multiclass_classifier(
            [0, 1, 2],
            [0, 1],
        )


def test_multiclass_invalid_true_label():
    with pytest.raises(ValueError, match="Invalid true fault label"):
        evaluate_multiclass_classifier(
            [0, 1, 3],
            [0, 1, 2],
        )


def test_multiclass_invalid_predicted_label():
    with pytest.raises(ValueError, match="Invalid predicted fault label"):
        evaluate_multiclass_classifier(
            [0, 1, 2],
            [0, 1, 3],
        )


def test_multiclass_macro_f1():
    result = evaluate_multiclass_classifier(
        [0, 0, 1, 1, 2, 2],
        [0, 1, 1, 1, 2, 0],
    )

    assert result["macro_f1"] == pytest.approx(
        (0.5 + 0.8 + 2 / 3) / 3
    )


def test_multiclass_per_class_recall():
    result = evaluate_multiclass_classifier(
        [0, 0, 1, 1, 2, 2],
        [0, 1, 1, 1, 2, 0],
    )

    assert result["per_class_recall"] == {
        0: pytest.approx(0.5),
        1: pytest.approx(1.0),
        2: pytest.approx(0.5),
    }


def test_multiclass_missing_fault_class():
    result = evaluate_multiclass_classifier(
        [0, 0, 1, 1],
        [0, 1, 1, 1],
    )

    assert result["confusion_matrix"] == [
        [1, 1, 0],
        [0, 2, 0],
        [0, 0, 0],
    ]

    assert result["per_class_recall"][2] == 0.0
    assert result["accuracy"] == pytest.approx(0.75)


def test_multiclass_class_support():
    result = evaluate_multiclass_classifier(
        [0, 0, 1, 1, 2, 2],
        [0, 1, 1, 1, 2, 0],
    )

    assert result["class_support"] == {
        0: 2,
        1: 2,
        2: 2,
    }


def test_multiclass_missing_class_support():
    result = evaluate_multiclass_classifier(
        [0, 0, 1, 1],
        [0, 1, 1, 1],
    )

    assert result["class_support"] == {
        0: 2,
        1: 2,
        2: 0,
    }

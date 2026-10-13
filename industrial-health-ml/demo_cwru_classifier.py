from pathlib import Path

import numpy as np
from scipy.io import loadmat

from src.classification import predict_fault
from src.feature_extraction import extract_window_features


DATA_DIR = Path(__file__).resolve().parent / "data" / "raw" / "cwru"

WINDOW_SIZE = 1200
STEP = 600
THRESHOLD = 0.18


def load_signal(filename):
    data = loadmat(DATA_DIR / filename)
    keys = [key for key in data if key.endswith("_DE_time")]

    if len(keys) != 1:
        raise ValueError("Expected exactly one drive-end signal")

    return np.asarray(data[keys[0]]).flatten()


true_labels = []
predictions = []

for filename, label in [
    ("97.mat", 0),
    ("105.mat", 1)
]:
    signal = load_signal(filename)

    windows = extract_window_features(
        signal.tolist(),
        window_size=WINDOW_SIZE,
        step=STEP
    )

    for window in windows:
        prediction = predict_fault(window["rms"], THRESHOLD)

        true_labels.append(label)
        predictions.append(prediction)

# Confusion matrix
tp = sum(t == 1 and p == 1 for t, p in zip(true_labels, predictions))
tn = sum(t == 0 and p == 0 for t, p in zip(true_labels, predictions))
fp = sum(t == 0 and p == 1 for t, p in zip(true_labels, predictions))
fn = sum(t == 1 and p == 0 for t, p in zip(true_labels, predictions))

total = len(true_labels)
accuracy = (tp + tn) / total

precision = tp / (tp + fp) if tp + fp else 0.0
recall = tp / (tp + fn) if tp + fn else 0.0
f1 = (
    2 * precision * recall / (precision + recall)
    if precision + recall else 0.0
)

print("=== Exploratory RMS Classifier ===")
print("Threshold:", THRESHOLD)
print("Total windows:", total)
print("TP:", tp)
print("TN:", tn)
print("FP:", fp)
print("FN:", fn)

print(f"Accuracy: {accuracy:.3f}")
print(f"Precision: {precision:.3f}")
print(f"Recall: {recall:.3f}")
print(f"F1 Score: {f1:.3f}")

print("\nWarning: These are in-sample descriptive metrics,")
print("not independent test-set performance.")
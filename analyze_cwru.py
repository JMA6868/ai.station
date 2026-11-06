from pathlib import Path

import numpy as np
from scipy.io import loadmat

from src.feature_extraction import extract_window_features


DATA_DIR = Path(__file__).resolve().parent / "data" / "raw" / "cwru"

FS = 12000
WINDOW_SIZE = 1200  # 0.1 second
STEP = 600          # 50% overlap


def load_signal(filename):
    data = loadmat(DATA_DIR / filename)

    keys = [key for key in data if key.endswith("_DE_time")]

    if len(keys) != 1:
        raise ValueError(f"Unexpected DE signal keys: {keys}")

    return np.asarray(data[keys[0]]).flatten()


for filename, label in [
    ("97.mat", "Normal"),
    ("105.mat", "Inner Race Fault"),
]:
    signal = load_signal(filename)

    # Use a list for compatibility with our existing code
    features = extract_window_features(
        signal.tolist(),
        window_size=WINDOW_SIZE,
        step=STEP,
    )

    rms_values = [item["rms"] for item in features]
    std_values = [item["std"] for item in features]

    print(f"\n=== {label} ===")
    print("Signal samples:", len(signal))
    print("Number of windows:", len(features))
    print("Average window RMS:", np.mean(rms_values))
    print("Average window Std:", np.mean(std_values))
    print("Maximum window RMS:", np.max(rms_values))
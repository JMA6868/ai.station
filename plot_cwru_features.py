from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from scipy.io import loadmat

from src.feature_extraction import extract_window_features


DATA_DIR = Path(__file__).resolve().parent / "data" / "raw" / "cwru"

FS = 12000
WINDOW_SIZE = 1200
STEP = 600


def load_signal(filename):
    data = loadmat(DATA_DIR / filename)

    keys = [key for key in data if key.endswith("_DE_time")]

    if len(keys) != 1:
        raise ValueError(f"Unexpected DE signal keys: {keys}")

    return np.asarray(data[keys[0]]).flatten()


def get_rms_trend(filename):
    signal = load_signal(filename)

    features = extract_window_features(
        signal.tolist(),
        window_size=WINDOW_SIZE,
        step=STEP
    )

    # Window center time, in seconds
    times = np.array([
        (f["start_index"] + (WINDOW_SIZE - 1) / 2) / FS
        for f in features
    ])

    rms_values = np.array([
        f["rms"] for f in features
    ])

    return times, rms_values


normal_time, normal_rms = get_rms_trend("97.mat")
fault_time, fault_rms = get_rms_trend("105.mat")

fig, axes = plt.subplots(2, 1, figsize=(12, 7))

axes[0].plot(normal_time, normal_rms)
axes[0].set_title("Normal Bearing - Window RMS")
axes[0].set_ylabel("RMS Acceleration (g)")
axes[0].grid(True)

axes[1].plot(fault_time, fault_rms)
axes[1].set_title("Inner Race Fault - Window RMS")
axes[1].set_xlabel("Time (seconds)")
axes[1].set_ylabel("RMS Acceleration (g)")
axes[1].grid(True)

# Use comparable vertical axes
upper = max(normal_rms.max(), fault_rms.max()) * 1.1

axes[0].set_ylim(0, upper)
axes[1].set_ylim(0, upper)

plt.tight_layout()
plt.savefig("cwru_rms_trend.png", dpi=150)
plt.show()

print("Normal RMS range:", normal_rms.min(), normal_rms.max())
print("Fault RMS range:", fault_rms.min(), fault_rms.max())
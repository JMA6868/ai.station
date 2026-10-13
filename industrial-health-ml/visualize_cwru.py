from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from scipy.io import loadmat


DATA_DIR = Path(__file__).resolve().parent / "data" / "raw" / "cwru"
FS = 12000


def load_vibration(filename):
    data = loadmat(DATA_DIR / filename)

    keys = [key for key in data if key.endswith("_DE_time")]

    if len(keys) != 1:
        raise ValueError(f"Expected one DE signal in {filename}")

    return np.asarray(data[keys[0]]).flatten()


normal = load_vibration("97.mat")
fault = load_vibration("105.mat")

# Display the first 0.1 second of each signal
duration = 0.1
n_samples = int(FS * duration)

normal_segment = normal[:n_samples]
fault_segment = fault[:n_samples]

time = np.arange(n_samples) / FS

# Plot in separate axes with the same vertical scale
limit = max(
    np.max(np.abs(normal_segment)),
    np.max(np.abs(fault_segment))
) * 1.1

fig, axes = plt.subplots(2, 1, figsize=(12, 7), sharex=True)

axes[0].plot(time, normal_segment)
axes[0].set_title("Normal Bearing - 97.mat")
axes[0].set_ylabel("Acceleration (g)")
axes[0].set_ylim(-limit, limit)
axes[0].grid(True)

axes[1].plot(time, fault_segment)
axes[1].set_title("Inner Race Fault - 105.mat")
axes[1].set_xlabel("Time (seconds)")
axes[1].set_ylabel("Acceleration (g)")
axes[1].set_ylim(-limit, limit)
axes[1].grid(True)

plt.tight_layout()
plt.savefig("cwru_waveforms.png", dpi=150)
plt.show()
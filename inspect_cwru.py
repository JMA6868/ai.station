from pathlib import Path
from scipy.io import loadmat
import numpy as np

# Location of the downloaded dataset
data_dir = Path(__file__).resolve().parent / "data" / "raw" / "cwru"

files = ["97.mat", "105.mat"]

for filename in files:
    file_path = data_dir / filename

    print(f"\n=== Inspecting {filename} ===")

    # Read MATLAB file
    data = loadmat(file_path)

    # Show available MATLAB variables
    print("Keys:", list(data.keys()))

    # Find drive-end vibration signal
    de_keys = [
        key for key in data
        if key.endswith("_DE_time")
    ]

    if not de_keys:
        raise ValueError(f"No drive-end signal found in {filename}")

    # Extract vibration data as a 1D array
    signal = np.asarray(data[de_keys[0]]).flatten()

    # CWRU selected files use 12 kHz sampling
    sampling_rate = 12000

    print("Signal key:", de_keys[0])
    print("Signal shape:", signal.shape)
    print("Number of samples:", len(signal))
    print("Sampling rate:", sampling_rate, "Hz")
    print("Duration:", len(signal) / sampling_rate, "seconds")
    print("First 10 values:", signal[:10])
    print("Mean:", np.mean(signal))
    print("Std:", np.std(signal))
    print("RMS:", np.sqrt(np.mean(signal ** 2)))
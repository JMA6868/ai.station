from src.feature_extraction import extract_window_features

vibration_data = [1.2, 1.5, 1.3, 1.4, 1.6, 1.3, 4.8, 1.5, 1.4, 1.3]

results = extract_window_features(
    vibration_data,
    window_size=4,
    step=2
)

for i, features in enumerate(results, start=1):
    print(f"Window {i}")
    print(f"  Samples: {features['start_index']} to {features['end_index']}")
    print(f"  Mean: {features['mean']:.3f}")
    print(f"  Std: {features['std']:.3f}")
    print(f"  RMS: {features['rms']:.3f}")
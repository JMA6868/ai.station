from pathlib import Path

from src.pipeline import process_sensor_csv


project_root = Path(__file__).resolve().parent
csv_path = project_root / "data" / "vibration_sample.csv"

results = process_sensor_csv(
    csv_path,
    window_size=4,
    step=2
)

print("Valid windows:", len(results))

for features in results:
    print(
        f"Window {features['start_index']}-{features['end_index']}: "
        f"Mean={features['mean']:.3f}, "
        f"Std={features['std']:.3f}, "
        f"RMS={features['rms']:.3f}"
    )
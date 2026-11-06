from pathlib import Path

from src.pipeline import process_sensor_csv_with_report


project_root = Path(__file__).resolve().parent
csv_path = project_root / "data" / "vibration_sample.csv"

features, report = process_sensor_csv_with_report(
    csv_path,
    window_size=4,
    step=2,
    expected_interval=1.0
)

print("=== Data Quality Report ===")

for key, value in report.items():
    print(f"{key}: {value}")

print("\n=== Extracted Features ===")

for window in features:
    print(
        f"Window {window['start_index']}-{window['end_index']}: "
        f"Mean={window['mean']:.3f}, "
        f"Std={window['std']:.3f}, "
        f"RMS={window['rms']:.3f}"
    )
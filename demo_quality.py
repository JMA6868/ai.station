from src.data_quality import generate_quality_report

report = generate_quality_report(
    total_samples=10,
    invalid_measurements=3,
    timestamp_issues=0,
    total_windows=4,
    valid_windows=1
)

for key, value in report.items():
    print(f"{key}: {value}")

# IndustrialSense AI - M1
# Step 10: Read vibration data from CSV

import csv
from pathlib import Path
from sensor_analysis import detect_anomaly

# Locate the project folder
project_root = Path(__file__).resolve().parent.parent
csv_path = project_root / "data" / "vibration_sample.csv"

threshold = 3.0

# Read sensor measurements
with open(csv_path, "r", newline="") as file:
    reader = csv.DictReader(file)

    print("CSV column names:", reader.fieldnames)

    for row in reader:
        timestamp = float(row["timestamp"])
        vibration = float(row["vibration"])

        if detect_anomaly(vibration, threshold):
            print(f"Time {timestamp}: WARNING - {vibration}")
        else:
            print(f"Time {timestamp}: Normal - {vibration}")


# IndustrialSense AI - Milestone 1
# Step 7: Modular sensor analysis

from sensor_analysis import detect_anomaly

vibration_data = [1.2, 1.5, 1.3, 1.4, 1.6, 1.3, 4.8, 1.5, 1.4, 1.3]

threshold = 3.0

for vibration in vibration_data:
    result = detect_anomaly(vibration, threshold)

    if result:
        print("WARNING: Abnormal vibration:", vibration)
    else:
        print("Normal vibration:", vibration)

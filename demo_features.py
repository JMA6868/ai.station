from src.feature_extraction import calculate_features

samples = [1, 2, 3, 4, 5]

features = calculate_features(samples)

print("Mean:", features["mean"])
print("Standard deviation:", features["std"])
print("RMS:", features["rms"])
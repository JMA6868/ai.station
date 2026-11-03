"""Frozen Stage 1 evaluation on expanded CWRU fault recordings."""

from pathlib import Path

from src.cwru_loader import load_cwru_de_signal
from src.feature_extraction import extract_window_features
from src.exploratory_signal_features import calculate_crest_factor
from src.exploratory_dual_threshold import is_anomaly
from src.threshold_calibration import calculate_percentile_threshold
from src.recording_anomaly_decision import classify_recording


TRAIN_IDS = (97, 98)
EVALUATION_IDS = (144, 156, 169, 185, 197)

WINDOW_SIZE = 1200
STEP = 600
PERCENTILE = 99


def get_window_features(recording_id):
    """Extract RMS and Crest Factor using the frozen window settings."""
    signal = load_cwru_de_signal(
        Path(f"data/raw/cwru/{recording_id}.mat")
    )

    rms_features = extract_window_features(
        signal,
        window_size=WINDOW_SIZE,
        step=STEP,
    )

    crest_factors = [
        calculate_crest_factor(signal[start:start + WINDOW_SIZE])
        for start in range(0, len(signal) - WINDOW_SIZE + 1, STEP)
    ]

    if len(rms_features) != len(crest_factors):
        raise ValueError("RMS and CF window counts do not match")

    return [
        (feature["rms"], cf)
        for feature, cf in zip(rms_features, crest_factors)
    ]


def calibrate_thresholds():
    """Calibrate both thresholds using Normal 97 and 98 only."""
    training_features = [
        features
        for recording_id in TRAIN_IDS
        for features in get_window_features(recording_id)
    ]

    rms_threshold = calculate_percentile_threshold(
        [rms for rms, _ in training_features],
        PERCENTILE,
    )

    cf_threshold = calculate_percentile_threshold(
        [cf for _, cf in training_features],
        PERCENTILE,
    )

    return rms_threshold, cf_threshold


def evaluate_recording(recording_id, rms_threshold, cf_threshold):
    """Evaluate one fault recording with both frozen baselines."""
    features = get_window_features(recording_id)

    if not features:
        raise ValueError("Recording has no valid windows")

    rms_alarms = sum(
        rms > rms_threshold
        for rms, _ in features
    )

    dual_alarms = sum(
        is_anomaly(rms, cf, rms_threshold, cf_threshold)
        for rms, cf in features
    )

    total = len(features)

    return {
        "recording_id": recording_id,
        "total_windows": total,
        "rms_alarms": rms_alarms,
        "rms_rate": rms_alarms / total,
        "rms_detected": classify_recording(rms_alarms, total),
        "dual_alarms": dual_alarms,
        "dual_rate": dual_alarms / total,
        "dual_detected": classify_recording(dual_alarms, total),
    }


def main():
    rms_threshold, cf_threshold = calibrate_thresholds()

    print(f"RMS P99: {rms_threshold:.9f}")
    print(f"CF P99:  {cf_threshold:.9f}")

    results = []

    for recording_id in EVALUATION_IDS:
        result = evaluate_recording(
            recording_id,
            rms_threshold,
            cf_threshold,
        )
        results.append(result)

        print(
            f"{recording_id}: "
            f"windows={result['total_windows']}, "
            f"RMS={result['rms_alarms']} "
            f"({result['rms_rate']:.2%}), "
            f"Dual={result['dual_alarms']} "
            f"({result['dual_rate']:.2%}), "
            f"RMS_detected={result['rms_detected']}, "
            f"Dual_detected={result['dual_detected']}"
        )

    rms_coverage = sum(r["rms_detected"] for r in results)
    dual_coverage = sum(r["dual_detected"] for r in results)

    print(f"RMS recording detection: {rms_coverage}/{len(results)}")
    print(f"Dual recording detection: {dual_coverage}/{len(results)}")


if __name__ == "__main__":
    main()

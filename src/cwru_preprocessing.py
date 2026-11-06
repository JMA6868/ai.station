"""CWRU signal loading with sampling-rate harmonization."""

from pathlib import Path

from src.cwru_loader import load_cwru_de_signal
from src.signal_resampling import resample_signal


TARGET_SAMPLE_RATE_HZ = 12000


def load_harmonized_cwru_signal(file_path, source_rate_hz):
    """Load a CWRU DE signal and harmonize its sampling rate."""
    recording_id = int(Path(file_path).stem)

    if recording_id in (97, 98, 99, 100):
        if source_rate_hz != 48000:
            raise ValueError(
                "Incorrect sampling rate for CWRU Normal recording"
            )

    known_12k_fault_ids = {
        105, 106, 107, 108,
        118, 119, 120, 121,
        130, 131, 132, 133,
        144, 156, 169, 185, 197,
    }

    if recording_id in known_12k_fault_ids:
        if source_rate_hz != 12000:
            raise ValueError(
                "Incorrect sampling rate for CWRU 12k fault recording"
            )

    known_normal_ids = {97, 98, 99, 100}

    if (
        recording_id not in known_normal_ids
        and recording_id not in known_12k_fault_ids
    ):
        raise ValueError(
            f"Unknown CWRU recording: {recording_id}. "
            "Sampling rate metadata has not been verified."
        )

    signal = load_cwru_de_signal(file_path)

    return resample_signal(
        signal,
        source_rate_hz=source_rate_hz,
        target_rate_hz=TARGET_SAMPLE_RATE_HZ,
    )

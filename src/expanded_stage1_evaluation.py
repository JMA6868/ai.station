"""Expanded descriptive CWRU Stage 1 RMS evaluation."""

from src.cwru_metadata import CWRU_RECORDING_METADATA
from src.cwru_expansion_metadata import CWRU_EXPANSION_METADATA
from src.harmonized_stage1_evaluation import evaluate_rms_recording


FROZEN_RMS_THRESHOLD = 0.07467624803042527

NORMAL_EVAL_IDS = (99, 100)

FAULT_EVAL_IDS = (
    105, 106, 107, 108,
    118, 119, 120, 121,
    130, 131, 132, 133,
    144, 156, 169, 185, 197,
)


def get_recording_metadata(recording_id):
    """Read existing metadata without modifying frozen experiments."""
    if recording_id in CWRU_RECORDING_METADATA:
        return CWRU_RECORDING_METADATA[recording_id]

    if recording_id in CWRU_EXPANSION_METADATA:
        return CWRU_EXPANSION_METADATA[recording_id]

    raise ValueError(f"Unknown recording ID: {recording_id}")


def evaluate_expanded_stage1():
    """Evaluate the frozen baseline on the predefined recordings."""
    results = []

    for recording_id in NORMAL_EVAL_IDS + FAULT_EVAL_IDS:
        metadata = get_recording_metadata(recording_id)

        evaluation = evaluate_rms_recording(
            recording_id,
            FROZEN_RMS_THRESHOLD,
        )

        results.append({
            **evaluation,
            "label": metadata["label"],
            "condition": metadata["condition"],
            "load_hp": metadata["load_hp"],
            "fault_diameter_in": metadata["fault_diameter_in"],
        })

    return results

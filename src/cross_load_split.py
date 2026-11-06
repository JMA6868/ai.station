# IndustrialSense AI - Step 27 Cross-load Dataset Split

from src.cwru_metadata import CWRU_RECORDING_METADATA


CROSS_LOAD_SPLIT = {
    "train": {
        0: [97, 98],
        1: [105, 106, 118, 119, 130, 131],
    },
    "validation": {
        0: [99],
        1: [107, 120, 132],
    },
    "evaluation": {
        0: [100],
        1: [108, 121, 133],
    },
}


def validate_cross_load_split():
    """Validate recording isolation, labels, and motor loads."""

    expected_loads = {
        "train": {0, 1},
        "validation": {2},
        "evaluation": {3},
    }

    all_ids = []

    for split_name, label_groups in CROSS_LOAD_SPLIT.items():
        for label, recording_ids in label_groups.items():
            for recording_id in recording_ids:
                if recording_id not in CWRU_RECORDING_METADATA:
                    raise ValueError(
                        f"Missing metadata for recording {recording_id}"
                    )

                metadata = CWRU_RECORDING_METADATA[recording_id]

                if metadata["label"] != label:
                    raise ValueError(
                        f"Incorrect label for recording {recording_id}"
                    )

                if metadata["load_hp"] not in expected_loads[split_name]:
                    raise ValueError(
                        f"Incorrect load for recording {recording_id}"
                    )

                all_ids.append(recording_id)

    if len(all_ids) != len(set(all_ids)):
        raise ValueError("Recording IDs overlap across splits")

    if set(all_ids) != set(CWRU_RECORDING_METADATA):
        raise ValueError("Cross-load split does not cover all recordings")

    return True
# IndustrialSense AI - Step 27.11 Normal-only Exploratory Split

from src.cwru_metadata import CWRU_RECORDING_METADATA


NORMAL_ONLY_SPLIT = {
    "train": {
        0: [97, 98],
    },
    "validation": {
        0: [99],
    },
}


EXPECTED_LOADS = {
    "train": {0, 1},
    "validation": {2},
}


FROZEN_EXPERIMENT_B_EVALUATION_IDS = {100, 121}


def validate_normal_only_split():
    """Validate the exploratory normal-only recording assignments."""

    all_ids = []

    for split_name, labels in NORMAL_ONLY_SPLIT.items():
        for label, recording_ids in labels.items():
            if label != 0:
                raise ValueError("Normal-only split must use label 0")

            for recording_id in recording_ids:
                metadata = CWRU_RECORDING_METADATA[recording_id]

                if metadata["label"] != 0:
                    raise ValueError(
                        f"Recording {recording_id} is not Normal"
                    )

                if metadata["condition"] != "normal":
                    raise ValueError(
                        f"Incorrect condition for recording {recording_id}"
                    )

                if metadata["load_hp"] not in EXPECTED_LOADS[split_name]:
                    raise ValueError(
                        f"Incorrect load for recording {recording_id}"
                    )

                all_ids.append(recording_id)

    if len(all_ids) != len(set(all_ids)):
        raise ValueError(
            "Recording IDs overlap across normal-only splits"
        )

    if set(all_ids) & FROZEN_EXPERIMENT_B_EVALUATION_IDS:
        raise ValueError(
            "Previously evaluated recordings cannot enter "
            "normal-only Training or Validation"
        )
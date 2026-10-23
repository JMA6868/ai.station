# IndustrialSense AI - Step 27 Experiment B Split

from src.cwru_metadata import CWRU_RECORDING_METADATA


HELD_OUT_FAULT_SPLIT = {
    "train": {
        0: [97, 98],
        1: [105, 106, 130, 131],
    },
    "validation": {
        0: [99],
        1: [107, 132],
    },
    "evaluation": {
        0: [100],
        1: [121],
    },
}


EXPECTED_LOADS = {
    "train": {0, 1},
    "validation": {2},
    "evaluation": {3},
}


FROZEN_RECORDING_IDS = {
    "train": {97, 98, 105, 106, 130, 131},
    "validation": {99, 107, 132},
    "evaluation": {100, 121},
}

def validate_held_out_fault_split():
    """Validate frozen Experiment B recording assignments."""

    all_ids = []

    for split_name, labels in HELD_OUT_FAULT_SPLIT.items():
        for label, recording_ids in labels.items():
            for recording_id in recording_ids:
                metadata = CWRU_RECORDING_METADATA[recording_id]

                if metadata["label"] != label:
                    raise ValueError(
                        f"Incorrect label for recording {recording_id}"
                    )

                if metadata["load_hp"] not in EXPECTED_LOADS[split_name]:
                    raise ValueError(
                        f"Incorrect load for recording {recording_id}"
                    )

                if split_name in ("train", "validation"):
                    if metadata["condition"] == "ball":
                        raise ValueError(
                            "Ball Fault must be excluded from "
                            "training and validation"
                        )

                all_ids.append(recording_id)

    if len(all_ids) != len(set(all_ids)):
        raise ValueError(
            "Recording IDs overlap across Experiment B splits"
        )

    expected_evaluation = {100, 121}

    actual_evaluation = {
        recording_id
        for ids in HELD_OUT_FAULT_SPLIT["evaluation"].values()
        for recording_id in ids
    }

    if actual_evaluation != expected_evaluation:
        raise ValueError(
            "Evaluation recordings do not match frozen protocol"
        )

    for split_name, expected_ids in FROZEN_RECORDING_IDS.items():
        actual_ids = {
            recording_id
            for ids in HELD_OUT_FAULT_SPLIT[split_name].values()
            for recording_id in ids
        }

        if actual_ids != expected_ids:
            raise ValueError(
                f"{split_name}: recording IDs differ from frozen protocol"
            )
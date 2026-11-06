from src.cwru_metadata import (
    CWRU_RECORDING_METADATA,
    APPROX_RPM_BY_LOAD,
)
from src.dataset_split import DATASET_SPLIT


def test_metadata_matches_dataset_split():
    """Every existing recording has matching metadata and label."""

    recording_ids = []

    for split_name, label_groups in DATASET_SPLIT.items():
        for label, ids in label_groups.items():
            for recording_id in ids:
                assert recording_id in CWRU_RECORDING_METADATA

                metadata = CWRU_RECORDING_METADATA[recording_id]

                assert metadata["label"] == label
                recording_ids.append(recording_id)

    assert len(recording_ids) == len(set(recording_ids))
    assert set(recording_ids).issubset(CWRU_RECORDING_METADATA)


def test_normal_recordings_have_no_fault_diameter():
    """Normal recordings must not have a fault diameter."""

    for metadata in CWRU_RECORDING_METADATA.values():
        if metadata["label"] == 0:
            assert metadata["condition"] == "normal"
            assert metadata["fault_diameter_in"] is None


def test_fault_recordings_have_expected_condition():
    """Validate the supported fault conditions and diameter."""

    valid_fault_conditions = {
        "inner_race",
        "ball",
        "outer_race_6",
    }

    for metadata in CWRU_RECORDING_METADATA.values():
        if metadata["label"] == 1:
            assert metadata["condition"] in valid_fault_conditions
            assert metadata["fault_diameter_in"] == 0.007


def test_loads_have_reference_rpm():
    """Every recording load must have an approximate RPM reference."""

    for metadata in CWRU_RECORDING_METADATA.values():
        assert metadata["load_hp"] in APPROX_RPM_BY_LOAD

def test_expanded_metadata_recordings():
    """Verify all 16 expected CWRU recording IDs."""

    expected_ids = {
        97, 98, 99, 100,
        105, 106, 107, 108,
        118, 119, 120, 121,
        130, 131, 132, 133,
    }

    assert set(CWRU_RECORDING_METADATA) == expected_ids

def test_expanded_fault_conditions():
    """Verify the new fault types and motor loads."""

    expected_groups = {
        "normal": {97, 98, 99, 100},
        "inner_race": {105, 106, 107, 108},
        "ball": {118, 119, 120, 121},
        "outer_race_6": {130, 131, 132, 133},
    }

    for condition, expected_ids in expected_groups.items():
        actual_ids = {
            recording_id
            for recording_id, metadata in CWRU_RECORDING_METADATA.items()
            if metadata["condition"] == condition
        }

        assert actual_ids == expected_ids

        actual_loads = {
            CWRU_RECORDING_METADATA[recording_id]["load_hp"]
            for recording_id in actual_ids
        }

        assert actual_loads == {0, 1, 2, 3}
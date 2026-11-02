from src.cwru_metadata import CWRU_RECORDING_METADATA
from src.cwru_expansion_metadata import CWRU_EXPANSION_METADATA


def test_expansion_recording_ids():
    expected_ids = {144, 156, 169, 185, 197}
    assert set(CWRU_EXPANSION_METADATA) == expected_ids


def test_expansion_conditions():
    expected = {
        144: ("outer_race_3", 0.007),
        156: ("outer_race_12", 0.007),
        169: ("inner_race", 0.014),
        185: ("ball", 0.014),
        197: ("outer_race_6", 0.014),
    }

    for recording_id, (condition, diameter) in expected.items():
        metadata = CWRU_EXPANSION_METADATA[recording_id]

        assert metadata["condition"] == condition
        assert metadata["fault_diameter_in"] == diameter


def test_expansion_labels_and_loads():
    for metadata in CWRU_EXPANSION_METADATA.values():
        assert metadata["label"] == 1
        assert metadata["load_hp"] == 0


def test_physical_identity_remains_unknown():
    for metadata in CWRU_EXPANSION_METADATA.values():
        assert metadata["bearing_id"] is None
        assert metadata["defect_instance_id"] is None


def test_expansion_does_not_overlap_existing_metadata():
    existing_ids = set(CWRU_RECORDING_METADATA)
    expansion_ids = set(CWRU_EXPANSION_METADATA)

    assert existing_ids.isdisjoint(expansion_ids)

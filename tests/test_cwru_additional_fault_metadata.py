"""Tests for additional CWRU fault metadata."""

from collections import Counter

from src.cwru_additional_fault_metadata import (
    CWRU_ADDITIONAL_FAULT_METADATA as METADATA,
)
from src.cwru_metadata import CWRU_RECORDING_METADATA
from src.cwru_expansion_metadata import CWRU_EXPANSION_METADATA


def test_recording_ids_and_no_overlap():
    expected = set(range(209, 213))
    expected |= set(range(222, 226))
    expected |= set(range(234, 238))
    expected |= set(range(246, 250))
    expected |= set(range(258, 262))
    expected |= set(range(3001, 3009))

    assert set(METADATA) == expected
    assert len(METADATA) == 28

    assert not set(METADATA) & set(CWRU_RECORDING_METADATA)
    assert not set(METADATA) & set(CWRU_EXPANSION_METADATA)


def test_fault_diameter_and_load_distribution():
    diameters = Counter(
        item["fault_diameter_in"]
        for item in METADATA.values()
    )
    loads = Counter(
        item["load_hp"]
        for item in METADATA.values()
    )

    assert diameters == {0.021: 20, 0.028: 8}
    assert loads == {0: 7, 1: 7, 2: 7, 3: 7}


def test_recording_metadata_fields():
    assert METADATA[209]["condition"] == "inner_race"
    assert METADATA[209]["load_hp"] == 0

    assert METADATA[261]["condition"] == "outer_race_12"
    assert METADATA[261]["load_hp"] == 3

    assert METADATA[3008]["condition"] == "ball"
    assert METADATA[3008]["load_hp"] == 3

    for item in METADATA.values():
        assert item["label"] == 1
        assert item["source_rate_hz"] == 12000
        assert item["bearing_id"] is None
        assert item["defect_instance_id"] is None

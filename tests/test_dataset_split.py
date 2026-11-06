# Tests for recording-level dataset separation

from src.dataset_split import DATASET_SPLIT


def test_no_recording_overlap():
    """Ensure recording IDs do not overlap across splits."""

    split_ids = {}

    for split_name, labels in DATASET_SPLIT.items():
        ids = [
            recording_id
            for recording_ids in labels.values()
            for recording_id in recording_ids
        ]

        assert len(ids) == len(set(ids))
        split_ids[split_name] = set(ids)

    assert split_ids["train"].isdisjoint(split_ids["validation"])
    assert split_ids["train"].isdisjoint(split_ids["test"])
    assert split_ids["validation"].isdisjoint(split_ids["test"])


def test_each_split_has_both_classes():
    """Ensure every split contains Normal and Fault recordings."""

    for labels in DATASET_SPLIT.values():
        assert set(labels.keys()) == {0, 1}
        assert len(labels[0]) > 0
        assert len(labels[1]) > 0
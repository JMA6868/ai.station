import pytest

from src.cross_load_split import (
    CROSS_LOAD_SPLIT,
    validate_cross_load_split,
)


def test_valid_cross_load_split():
    """The frozen Step 27 split should pass validation."""
    assert validate_cross_load_split() is True


def test_recording_isolation():
    """No recording may appear in multiple splits."""

    split_ids = {}

    for split_name, label_groups in CROSS_LOAD_SPLIT.items():
        split_ids[split_name] = {
            recording_id
            for ids in label_groups.values()
            for recording_id in ids
        }

    assert split_ids["train"].isdisjoint(split_ids["validation"])
    assert split_ids["train"].isdisjoint(split_ids["evaluation"])
    assert split_ids["validation"].isdisjoint(split_ids["evaluation"])


def test_reject_overlapping_recordings(monkeypatch):
    """Reject a recording reused across splits."""

    from src import cross_load_split

    invalid_split = {
        split: {
            label: ids.copy()
            for label, ids in groups.items()
        }
        for split, groups in CROSS_LOAD_SPLIT.items()
    }

    invalid_split["validation"][1].append(105)

    monkeypatch.setattr(
        cross_load_split,
        "CROSS_LOAD_SPLIT",
        invalid_split,
    )

    with pytest.raises(ValueError):
        validate_cross_load_split()


def test_reject_incorrect_label(monkeypatch):
    """Reject a recording assigned to the wrong class."""

    from src import cross_load_split

    invalid_split = {
        split: {
            label: ids.copy()
            for label, ids in groups.items()
        }
        for split, groups in CROSS_LOAD_SPLIT.items()
    }

    invalid_split["train"][0].remove(97)
    invalid_split["train"][1].append(97)

    monkeypatch.setattr(
        cross_load_split,
        "CROSS_LOAD_SPLIT",
        invalid_split,
    )

    with pytest.raises(ValueError, match="Incorrect label"):
        validate_cross_load_split()


def test_reject_incorrect_load(monkeypatch):
    """Reject a recording assigned to the wrong load group."""

    from src import cross_load_split

    invalid_split = {
        split: {
            label: ids.copy()
            for label, ids in groups.items()
        }
        for split, groups in CROSS_LOAD_SPLIT.items()
    }

    invalid_split["train"][0].remove(97)
    invalid_split["validation"][0].append(97)

    monkeypatch.setattr(
        cross_load_split,
        "CROSS_LOAD_SPLIT",
        invalid_split,
    )

    with pytest.raises(ValueError, match="Incorrect load"):
        validate_cross_load_split()


def test_reject_missing_recording(monkeypatch):
    """Reject an incomplete dataset split."""

    from src import cross_load_split

    invalid_split = {
        split: {
            label: ids.copy()
            for label, ids in groups.items()
        }
        for split, groups in CROSS_LOAD_SPLIT.items()
    }

    invalid_split["train"][0].remove(97)

    monkeypatch.setattr(
        cross_load_split,
        "CROSS_LOAD_SPLIT",
        invalid_split,
    )

    with pytest.raises(ValueError, match="does not cover all recordings"):
        validate_cross_load_split()
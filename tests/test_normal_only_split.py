# IndustrialSense AI - Step 27.11 Normal-only Split Tests

import pytest

from src.normal_only_split import (
    NORMAL_ONLY_SPLIT,
    validate_normal_only_split,
)


def test_valid_normal_only_split():
    validate_normal_only_split()

    assert NORMAL_ONLY_SPLIT == {
        "train": {0: [97, 98]},
        "validation": {0: [99]},
    }


def test_reject_fault_label(monkeypatch):
    invalid_split = {
        "train": {1: [97, 98]},
        "validation": {0: [99]},
    }

    monkeypatch.setattr(
        "src.normal_only_split.NORMAL_ONLY_SPLIT",
        invalid_split,
    )

    with pytest.raises(ValueError, match="label 0"):
        validate_normal_only_split()


def test_reject_fault_recording(monkeypatch):
    invalid_split = {
        "train": {0: [105, 98]},
        "validation": {0: [99]},
    }

    monkeypatch.setattr(
        "src.normal_only_split.NORMAL_ONLY_SPLIT",
        invalid_split,
    )

    with pytest.raises(ValueError, match="not Normal"):
        validate_normal_only_split()


def test_reject_incorrect_load(monkeypatch):
    invalid_split = {
        "train": {0: [97, 99]},
        "validation": {0: [98]},
    }

    monkeypatch.setattr(
        "src.normal_only_split.NORMAL_ONLY_SPLIT",
        invalid_split,
    )

    with pytest.raises(ValueError, match="Incorrect load"):
        validate_normal_only_split()


def test_reject_recording_overlap(monkeypatch):
    invalid_split = {
        "train": {0: [97, 97, 98]},
        "validation": {0: [99]},
    }

    monkeypatch.setattr(
        "src.normal_only_split.NORMAL_ONLY_SPLIT",
        invalid_split,
    )

    with pytest.raises(ValueError, match="overlap"):
        validate_normal_only_split()


def test_reject_previously_evaluated_recording(monkeypatch):
    monkeypatch.setattr(
        "src.normal_only_split.FROZEN_EXPERIMENT_B_EVALUATION_IDS",
        {99, 100, 121},
    )

    with pytest.raises(ValueError, match="Previously evaluated"):
        validate_normal_only_split()

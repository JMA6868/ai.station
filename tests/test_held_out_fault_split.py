import pytest

from src.held_out_fault_split import (
    HELD_OUT_FAULT_SPLIT,
    validate_held_out_fault_split,
)


def test_frozen_split_is_valid():
    """The original frozen split must pass."""
    validate_held_out_fault_split()


def test_reject_incorrect_recording_id():
    """Reject a recording assignment outside the frozen protocol."""

    original = HELD_OUT_FAULT_SPLIT["train"][0][:]

    try:
        HELD_OUT_FAULT_SPLIT["train"][0] = [97]

        with pytest.raises(ValueError, match="frozen protocol"):
            validate_held_out_fault_split()
    finally:
        HELD_OUT_FAULT_SPLIT["train"][0] = original


def test_reject_ball_fault_in_training():
    """Ball Fault must never enter the training split."""

    original = HELD_OUT_FAULT_SPLIT["train"][1][:]

    try:
        HELD_OUT_FAULT_SPLIT["train"][1] = original + [118]

        with pytest.raises(ValueError, match="Ball Fault"):
            validate_held_out_fault_split()
    finally:
        HELD_OUT_FAULT_SPLIT["train"][1] = original


def test_reject_ball_fault_in_validation():
    """Ball Fault must never enter validation."""

    original = HELD_OUT_FAULT_SPLIT["validation"][1][:]

    try:
        HELD_OUT_FAULT_SPLIT["validation"][1] = original + [120]

        with pytest.raises(ValueError, match="Ball Fault"):
            validate_held_out_fault_split()
    finally:
        HELD_OUT_FAULT_SPLIT["validation"][1] = original


def test_reject_duplicate_recording():
    """Reject recording IDs repeated across splits."""

    original = HELD_OUT_FAULT_SPLIT["train"][0][:]

    try:
        HELD_OUT_FAULT_SPLIT["train"][0] = original + [97]

        with pytest.raises(ValueError, match="overlap"):
            validate_held_out_fault_split()
    finally:
        HELD_OUT_FAULT_SPLIT["train"][0] = original


def test_reject_incorrect_motor_load():
    """Reject recordings assigned to the wrong motor load."""

    original = HELD_OUT_FAULT_SPLIT["validation"][0][:]

    try:
        HELD_OUT_FAULT_SPLIT["validation"][0] = [98]

        with pytest.raises(ValueError, match="Incorrect load"):
            validate_held_out_fault_split()
    finally:
        HELD_OUT_FAULT_SPLIT["validation"][0] = original
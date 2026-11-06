"""Tests for newly supported CWRU 12 kHz recordings."""

import pytest

from src import cwru_preprocessing as preprocessing


def test_new_12k_recordings_are_accepted(monkeypatch):
    calls = []

    def fake_loader(path):
        calls.append(("load", str(path)))
        return [1.0, 2.0, 3.0]

    def fake_resampler(signal, source_rate_hz, target_rate_hz):
        calls.append(("resample", source_rate_hz, target_rate_hz))
        return signal

    monkeypatch.setattr(
        preprocessing, "load_cwru_de_signal", fake_loader
    )
    monkeypatch.setattr(
        preprocessing, "resample_signal", fake_resampler
    )

    for recording_id in (209, 261, 3001, 3008):
        preprocessing.load_harmonized_cwru_signal(
            f"data/raw/cwru/{recording_id}.mat",
            source_rate_hz=12000,
        )

    assert len([c for c in calls if c[0] == "load"]) == 4
    assert all(
        c == ("resample", 12000, 12000)
        for c in calls if c[0] == "resample"
    )


def test_new_recordings_reject_incorrect_sample_rate():
    for recording_id in (209, 261, 3001, 3008):
        with pytest.raises(
            ValueError,
            match="Incorrect sampling rate",
        ):
            preprocessing.load_harmonized_cwru_signal(
                f"data/raw/cwru/{recording_id}.mat",
                source_rate_hz=48000,
            )


def test_unknown_recordings_remain_rejected():
    with pytest.raises(
        ValueError,
        match="Unknown CWRU recording",
    ):
        preprocessing.load_harmonized_cwru_signal(
            "data/raw/cwru/9999.mat",
            source_rate_hz=12000,
        )

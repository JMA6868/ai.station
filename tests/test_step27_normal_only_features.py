
# IndustrialSense AI - Step 27.11 Normal-only Feature Generator Tests

from collections import Counter

import pytest

import generate_step27_normal_only_features as generator
from src.feature_import import import_features_from_csv


def test_normal_only_feature_generation(monkeypatch, tmp_path):
    """Verify successful generation and CSV contents."""

    monkeypatch.setattr(
        generator,
        "OUTPUT_DIR",
        tmp_path,
    )

    expected_ids = {
        "train": [97, 98],
        "validation": [99],
    }

    def fake_builder(split_name, dataset_split):
        assert dataset_split == generator.NORMAL_ONLY_SPLIT

        records = []

        for recording_id in expected_ids[split_name]:
            count = {
                97: 405,
                98: 805,
                99: 807,
            }[recording_id]

            for i in range(count):
                records.append({
                    "recording_id": recording_id,
                    "label": 0,
                    "start_index": i * 600,
                    "end_index": i * 600 + 1200,
                    "mean": 0.01,
                    "std": 0.07,
                    "rms": 0.071,
                })

        return records

    monkeypatch.setattr(
        generator,
        "build_evaluation_dataset",
        fake_builder,
    )

    generator.generate_normal_only_features()

    for split_name, ids in expected_ids.items():
        records = import_features_from_csv(
            tmp_path / f"{split_name}.csv"
        )

        counts = Counter(
            record["recording_id"] for record in records
        )

        assert set(counts) == set(ids)
        assert len(records) == generator.EXPECTED_WINDOWS[split_name]
        assert all(record["label"] == 0 for record in records)
        assert all(record["split"] == split_name for record in records)


def test_reject_incorrect_window_count(monkeypatch, tmp_path):
    """Reject wrong window counts when recording IDs are valid."""

    monkeypatch.setattr(
        generator,
        "OUTPUT_DIR",
        tmp_path,
    )

    def fake_builder(split_name, dataset_split):
        assert split_name == "train"
        assert dataset_split == generator.NORMAL_ONLY_SPLIT

        return [
            {
                "recording_id": recording_id,
                "label": 0,
                "start_index": 0,
                "end_index": 1200,
                "mean": 0.01,
                "std": 0.07,
                "rms": 0.071,
            }
            for recording_id in (97, 98)
        ]

    monkeypatch.setattr(
        generator,
        "build_evaluation_dataset",
        fake_builder,
    )

    with pytest.raises(ValueError, match="unexpected window count"):
        generator.generate_normal_only_features()

    assert not (tmp_path / "train.csv").exists()
    assert not (tmp_path / "validation.csv").exists()

def test_reject_incorrect_recording_ids(monkeypatch, tmp_path):
    """Reject unexpected recording IDs even with correct window count."""

    monkeypatch.setattr(generator, "OUTPUT_DIR", tmp_path)

    def fake_builder(split_name, dataset_split):
        assert split_name == "train"
        assert dataset_split == generator.NORMAL_ONLY_SPLIT

        return [
            {
                "recording_id": 97,
                "label": 0,
                "start_index": i * 600,
                "end_index": i * 600 + 1200,
                "mean": 0.01,
                "std": 0.07,
                "rms": 0.071,
            }
            for i in range(1210)
        ]

    monkeypatch.setattr(
        generator,
        "build_evaluation_dataset",
        fake_builder,
    )

    with pytest.raises(ValueError, match="unexpected recording IDs"):
        generator.generate_normal_only_features()

    assert not (tmp_path / "train.csv").exists()
    assert not (tmp_path / "validation.csv").exists()

def test_reject_non_normal_label(monkeypatch, tmp_path):
    """Reject non-Normal labels with otherwise valid data."""

    monkeypatch.setattr(generator, "OUTPUT_DIR", tmp_path)

    def fake_builder(split_name, dataset_split):
        assert split_name == "train"
        assert dataset_split == generator.NORMAL_ONLY_SPLIT

        records = []

        for recording_id, count in ((97, 405), (98, 805)):
            for i in range(count):
                records.append({
                    "recording_id": recording_id,
                    "label": 0,
                    "start_index": i * 600,
                    "end_index": i * 600 + 1200,
                    "mean": 0.01,
                    "std": 0.07,
                    "rms": 0.071,
                })

        # Introduce one incorrect label.
        records[0]["label"] = 1

        return records

    monkeypatch.setattr(
        generator,
        "build_evaluation_dataset",
        fake_builder,
    )

    with pytest.raises(ValueError, match="found non-Normal labels"):
        generator.generate_normal_only_features()

    assert not (tmp_path / "train.csv").exists()
    assert not (tmp_path / "validation.csv").exists()

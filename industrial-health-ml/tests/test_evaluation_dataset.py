# IndustrialSense AI - Evaluation Dataset Tests

from collections import Counter

from src.cwru_loader import load_cwru_de_signal
from src.dataset_split import DATASET_SPLIT
from src.evaluation_dataset import build_evaluation_dataset


def test_training_window_counts():
    """Verify window counts for every training recording."""

    window_size = 1200
    step = 600

    records = build_evaluation_dataset("train")
    counts = Counter(row["recording_id"] for row in records)

    for recording_ids in DATASET_SPLIT["train"].values():
        for recording_id in recording_ids:
            signal = load_cwru_de_signal(
                f"data/raw/cwru/{recording_id}.mat"
            )

            expected = max(
                0,
                (len(signal) - window_size) // step + 1
            )

            assert counts[recording_id] == expected


def test_training_labels_and_recording_ids():
    """Verify each window has its correct label and origin."""

    records = build_evaluation_dataset("train")

    expected_labels = {
        recording_id: label
        for label, recording_ids in DATASET_SPLIT["train"].items()
        for recording_id in recording_ids
    }

    assert len(records) > 0

    for row in records:
        assert row["recording_id"] in expected_labels
        assert row["label"] == expected_labels[row["recording_id"]]

        assert {
            "mean", "std", "rms",
            "start_index", "end_index"
        }.issubset(row.keys())

        assert row["end_index"] - row["start_index"] + 1 == 1200
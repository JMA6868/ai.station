from src import evaluation_dataset


def test_default_dataset_split(monkeypatch):
    """Default behavior must remain compatible with Step 26."""

    loaded_paths = []

    def fake_loader(path):
        loaded_paths.append(path.name)
        return [1.0, 2.0, 3.0]

    def fake_features(signal, window_size, step):
        return [
            {
                "mean": 2.0,
                "std": 0.8165,
                "rms": 2.1602,
                "start_index": 0,
                "end_index": 2,
            }
        ]

    monkeypatch.setattr(
        evaluation_dataset,
        "load_cwru_de_signal",
        fake_loader,
    )
    monkeypatch.setattr(
        evaluation_dataset,
        "extract_window_features",
        fake_features,
    )

    records = evaluation_dataset.build_evaluation_dataset("validation")

    assert set(loaded_paths) == {"99.mat", "107.mat"}
    assert len(records) == 2
    assert {row["label"] for row in records} == {0, 1}


def test_custom_dataset_split(monkeypatch):
    """Accept an explicitly supplied recording split."""

    loaded_paths = []

    def fake_loader(path):
        loaded_paths.append(path.name)
        return [1.0, 2.0, 3.0]

    def fake_features(signal, window_size, step):
        return [
            {
                "mean": 2.0,
                "std": 0.8165,
                "rms": 2.1602,
                "start_index": 0,
                "end_index": 2,
            }
        ]

    monkeypatch.setattr(
        evaluation_dataset,
        "load_cwru_de_signal",
        fake_loader,
    )
    monkeypatch.setattr(
        evaluation_dataset,
        "extract_window_features",
        fake_features,
    )

    custom_split = {
        "validation": {
            0: [99],
            1: [120, 132],
        }
    }

    records = evaluation_dataset.build_evaluation_dataset(
        "validation",
        dataset_split=custom_split,
    )

    assert set(loaded_paths) == {
        "99.mat",
        "120.mat",
        "132.mat",
    }

    assert len(records) == 3
    assert {row["recording_id"] for row in records} == {99, 120, 132}
    assert {row["label"] for row in records} == {0, 1}
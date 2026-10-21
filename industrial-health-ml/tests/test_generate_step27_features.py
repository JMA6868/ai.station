from pathlib import Path

import generate_step27_features as generator


def test_step27_split_export_names():
    """Verify the explicit evaluation-to-test mapping."""

    assert generator.SPLIT_EXPORT_NAMES == {
        "train": "train",
        "validation": "validation",
        "evaluation": "test",
    }


def test_generator_uses_correct_splits_and_paths(monkeypatch, tmp_path):
    """Verify dataset generation without accessing real CWRU files."""

    calls = {
        "build": [],
        "export": [],
        "validated": 0,
    }

    def fake_validate():
        calls["validated"] += 1
        return True

    def fake_build(
        split_name,
        window_size,
        step,
        dataset_split,
    ):
        calls["build"].append(
            (split_name, window_size, step, dataset_split)
        )

        return [{"recording_id": 97, "label": 0}]

    def fake_export(records, split_name, output_path):
        calls["export"].append(
            (records, split_name, Path(output_path))
        )

    monkeypatch.setattr(
        generator,
        "validate_cross_load_split",
        fake_validate,
    )
    monkeypatch.setattr(
        generator,
        "build_evaluation_dataset",
        fake_build,
    )
    monkeypatch.setattr(
        generator,
        "export_features_to_csv",
        fake_export,
    )
    monkeypatch.setattr(
        generator,
        "OUTPUT_DIR",
        tmp_path,
    )

    generator.generate_step27_features()

    assert calls["validated"] == 1

    assert [call[0] for call in calls["build"]] == [
        "train",
        "validation",
        "evaluation",
    ]

    assert all(
        call[3] is generator.CROSS_LOAD_SPLIT
        for call in calls["build"]
    )

    assert all(
        call[1] == generator.WINDOW_SIZE
        and call[2] == generator.WINDOW_STEP
        for call in calls["build"]
    )

    assert [
        (call[1], call[2].name)
        for call in calls["export"]
    ] == [
        ("train", "train.csv"),
        ("validation", "validation.csv"),
        ("test", "test.csv"),
    ]

    assert all(
        call[2].parent == tmp_path
        for call in calls["export"]
    )
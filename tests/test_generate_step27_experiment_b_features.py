from pathlib import Path
from unittest.mock import patch

import generate_step27_experiment_b_features as generator
from src.held_out_fault_split import HELD_OUT_FAULT_SPLIT


def test_experiment_b_output_directory():
    """Experiment B must use a separate output directory."""

    assert generator.OUTPUT_DIR.name == "step27_experiment_b"
    assert generator.OUTPUT_DIR != (
        Path(generator.__file__).resolve().parent
        / "data" / "processed" / "step27"
    )


def test_experiment_b_generator_uses_frozen_split():
    """Verify all three splits and output paths without writing CSVs."""

    build_calls = []
    export_calls = []

    def fake_build(split_name, **kwargs):
        build_calls.append((split_name, kwargs))
        return [{"recording_id": 97, "label": 0}]

    def fake_export(records, split_name, output_path):
        export_calls.append((split_name, output_path))

    with (
        patch.object(generator, "build_evaluation_dataset",
                     side_effect=fake_build),
        patch.object(generator, "export_features_to_csv",
                     side_effect=fake_export),
    ):
        generator.generate_experiment_b_features()

    assert len(build_calls) == 3
    assert len(export_calls) == 3

    for split_name, kwargs in build_calls:
        assert kwargs["dataset_split"] is HELD_OUT_FAULT_SPLIT

    assert [name for name, _ in export_calls] == [
        "train", "validation", "test"
    ]

    assert all(
        path.parent == generator.OUTPUT_DIR
        for _, path in export_calls
    )
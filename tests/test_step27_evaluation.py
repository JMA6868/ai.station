from unittest.mock import patch

import run_step27_evaluation as runner


def test_evaluation_fits_training_only():
    """Ensure evaluation data is never used in model.fit()."""

    train_records = [
        {"recording_id": 97, "split": "train",
         "label": 0, "mean": 0.1, "std": 0.1, "rms": 0.1},
        {"recording_id": 105, "split": "train",
         "label": 1, "mean": 0.3, "std": 0.3, "rms": 0.3},
    ]

    eval_records = [
        {"recording_id": 100, "split": "test",
         "label": 0, "mean": 0.2, "std": 0.2, "rms": 0.2},
        {"recording_id": 108, "split": "test",
         "label": 1, "mean": 0.4, "std": 0.4, "rms": 0.4},
    ]

    class FakeModel:
        def __init__(self):
            self.fit_calls = []
            self.predict_calls = []

        def fit(self, X, y):
            self.fit_calls.append((X, y))
            return self

        def predict(self, X):
            self.predict_calls.append(X)
            return [0, 1]

    fake_model = FakeModel()

    def fake_import(path):
        if path.name == "train.csv":
            return train_records
        if path.name == "test.csv":
            return eval_records
        raise AssertionError(f"Unexpected CSV: {path}")

    with (
        patch.object(runner, "import_features_from_csv",
                     side_effect=fake_import),
        patch.object(runner, "create_baseline_pipeline",
                     return_value=fake_model),
        patch.object(runner, "validate_cross_load_records"),
        patch.object(runner, "validate_cross_load_split"),
        patch.object(runner, "validate_recording_isolation",
                     return_value=({97, 105}, {100, 108})),
    ):
        # This test isolates model fitting/prediction behavior.
        # The frozen recording-list checks are separately verified.
        expected_ids = {
            recording_id
            for ids in runner.CROSS_LOAD_SPLIT["evaluation"].values()
            for recording_id in ids
        }
        # Use a temporary split matching the tiny synthetic dataset.
        with patch.dict(
            runner.CROSS_LOAD_SPLIT,
            {"evaluation": {0: [100], 1: [108]}},
        ):
            runner.main()

    assert len(fake_model.fit_calls) == 1

    fitted_X, fitted_y = fake_model.fit_calls[0]
    assert fitted_X == [
        [0.1, 0.1, 0.1],
        [0.3, 0.3, 0.3],
    ]
    assert fitted_y == [0, 1]

    assert fake_model.predict_calls == [
        [[0.2, 0.2, 0.2], [0.4, 0.4, 0.4]]
    ]
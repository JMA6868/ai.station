# IndustrialSense AI - Evaluation Dataset Builder

from pathlib import Path

from src.cwru_loader import load_cwru_de_signal
from src.dataset_split import DATASET_SPLIT
from src.feature_extraction import extract_window_features

def build_evaluation_dataset(
    split_name,
    data_dir="data/raw/cwru",
    window_size=1200,
    step=600,
    dataset_split=None,
):
    
    """Build window features from a specified recording split."""

    if dataset_split is None:
        dataset_split = DATASET_SPLIT

    if split_name not in dataset_split:
        raise ValueError(f"Unknown dataset split: {split_name}")

    data_dir = Path(data_dir)
    records = []

    for label, recording_ids in dataset_split[split_name].items():
        for recording_id in recording_ids:

            file_path = data_dir / f"{recording_id}.mat"

            signal = load_cwru_de_signal(file_path)

            windows = extract_window_features(
                signal,
                window_size=window_size,
                step=step,
            )

            for window in windows:
                records.append({
                    "recording_id": recording_id,
                    "label": label,
                    **window,
                })

    return records
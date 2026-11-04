# Step 27.12 — Harmonized Stage 1 Evaluation Protocol

## Status

Pre-registered design. Evaluation not yet executed.

## Objective

Compare the frozen Stage 1 RMS baseline against a new
sampling-rate-harmonized evaluation.

Determine whether the large Normal/Fault RMS separation
persists after harmonizing sampling rates.

## Dataset Scope

CWRU only.

## Preprocessing

Target sample rate: 12000 Hz.

Normal 97-100:
- Original rate: 48000 Hz.
- Downsample to 12000 Hz using polyphase filtering.

Selected 12 kHz Drive End faults:
- Preserve original 12000 Hz signals.

Window size: 1200 samples.
Window step: 600 samples.

## Recording Roles

Normal training: 97, 98.
Normal validation: 99.
Normal evaluation: 100.

Fault evaluation: 144, 156, 169, 185, 197.

All listed recordings have been involved in prior research.
This is a controlled preprocessing comparison,
not an independent untouched holdout evaluation.

## RMS Baseline

Calibrate RMS threshold using only Normal training
recordings 97 and 98 after harmonization.

Threshold percentile: P99.

Window anomaly rule:
RMS > training P99 threshold.

Recording anomaly rule:
Anomalous window fraction > 0.05.

## Required Reporting

- Original and harmonized RMS thresholds.
- Per-recording RMS distributions.
- Normal validation and evaluation false-alarm rates.
- Fault recording detection rates.
- Window counts and recording-level outcomes.
- Comparison with frozen original results.
- Limitations from previously evaluated recordings.

## Scientific Boundaries

Do not tune the threshold using evaluation recordings.
Do not overwrite frozen historical results.
Do not claim industrial-grade or independent generalization.
Do not infer physical-bearing independence from file IDs.

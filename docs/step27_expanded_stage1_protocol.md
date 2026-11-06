# Step 27.12-11P — Expanded CWRU Stage 1 Evaluation Protocol

## Status

Prospective design documented before expanded evaluation.

## Objective

Evaluate the frozen harmonized RMS P99 baseline across
all 17 locally available CWRU fault recordings.

This is a retrospective, descriptive expansion study,
not an independent untouched holdout evaluation.

## Dataset

CWRU only.

Normal training:
97, 98

Normal validation/evaluation:
99, 100

Fault evaluation:
105, 106, 107, 108,
118, 119, 120, 121,
130, 131, 132, 133,
144, 156, 169, 185, 197

All recordings have been involved in previous research.
Evaluation outcomes must not be used to retune the baseline.

## Frozen Configuration

Target sampling rate: 12000 Hz
Window size: 1200 samples
Window step: 600 samples

Normal training recordings: 97, 98
RMS threshold percentile: P99

Frozen harmonized RMS threshold:
0.07467624803042527

Window anomaly rule:
RMS > frozen threshold

Recording anomaly rule:
Anomalous window fraction > 0.05

## Required Reporting

1. Per-recording window counts.
2. Per-recording anomalous window counts.
3. Per-recording anomaly fractions.
4. Recording-level Normal/Fault decisions.
5. False alarms for Normal recordings 99 and 100.
6. Fault detection rates by fault condition.
7. Fault detection rates by fault diameter.
8. Fault detection rates by motor load.
9. Overall recording-level detection summary.
10. Explicit limitations and prior data usage.

Report window-level outcomes descriptively.
Do not treat overlapping windows as independent samples.

## Scientific Boundaries

- Do not change frozen thresholds after seeing results.
- Do not overwrite previous experiment results.
- Do not describe previously used recordings as untouched.
- Physical-bearing independence remains unverified.
- Do not claim cross-bearing or industrial generalization.
- Results apply only to the evaluated CWRU conditions.
- Additional official CWRU recordings require separate
  metadata verification and evaluation planning.

## Future Model Comparison

Use this experiment as a descriptive RMS reference.

Traditional ML and deep learning comparisons require
separately documented training, validation, and evaluation
roles, with leakage-aware model selection.

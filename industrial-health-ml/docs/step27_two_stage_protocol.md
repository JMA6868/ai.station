# Step 27.12 — Two-Stage Detection and Diagnosis Protocol

## Status

Protocol design in progress.

No new model training or evaluation has been performed.

## System Objective

Build a two-stage industrial equipment health monitoring system.

Stage 1 — Anomaly Detection:
- Determine whether equipment behavior is Normal or Abnormal.
- Normal: pass and continue monitoring.
- Abnormal: forward to Stage 2.

Stage 2 — Fault Diagnosis:
- Identify Inner Race, Outer Race, or Ball Fault.
- Support Unknown or Uncertain Fault when evidence is insufficient.
- Do not force every anomaly into a known fault category.

## Available CWRU Data

Existing recordings: 16.
New expansion recordings: 5.
Total local recordings: 21.

All five expansion recordings have passed signal-integrity checks.

## Experimental Integrity

- Preserve frozen Experiment A/B results.
- Do not assume recording-level separation implies bearing independence.
- Do not treat previously examined recordings as untouched test data.
- Separate model training, threshold calibration, and evaluation.
- Account for correlated overlapping windows.
- Do not claim cross-equipment generalization without supporting evidence.
- Avoid evaluating a detector on data used to select its parameters.

## Open Design Decisions

- Define Stage 1 training and evaluation recordings.
- Define Stage 2 known fault labels and unknown fault handling.
- Investigate physical-bearing and defect-instance independence.
- Determine how to obtain independent Normal evaluation data.
- Establish recording-level and end-to-end evaluation metrics.
- Freeze the protocol before model training or final evaluation.

## Current Status

Data inventory completed.
Two-stage experimental design not yet finalized.

## Two-Stage Dataset Design Principles

### Stage 1 — Normal-only Anomaly Detection

- Train the anomaly detector using designated Normal recordings.
- Calibrate thresholds using training data only.
- Evaluate both normal false alarms and fault detection.
- Do not assume that additional fault recordings provide
  independent Normal evaluation data.
- Treat previously examined recordings as exploratory.

### Stage 2 — Known-Fault Diagnosis

- Train using designated known fault types.
- Initially distinguish Inner Race, Outer Race, and Ball Fault.
- Keep fault severity and position as metadata.
- Do not mix overlapping windows from the same recording
  across training and evaluation datasets.
- Investigate whether recordings share defect instances.

### Unknown-Fault Handling

- Allow Stage 2 to abstain from a diagnosis.
- Do not force every abnormal recording into a known class.
- Define rejection criteria using permitted training and
  calibration data before evaluating unknown faults.
- Do not claim reliable unknown-fault detection until
  independently evaluated.

### End-to-End Evaluation

- Evaluate Stage 1 and Stage 2 separately.
- Also evaluate the complete two-stage pipeline.
- A Stage 1 missed anomaly cannot reach Stage 2.
- Report window-level and recording-level results.
- Distinguish exploratory results from independent tests.

No new recording split has been finalized at this stage.

## Recording Usage History

All original 16 CWRU recordings have participated in
Experiment A or Experiment B.

| Recording IDs | Condition | Experiment A | Experiment B |
|---|---|---|---|
| 97, 98 | Normal | Train | Train |
| 99 | Normal | Validation | Validation |
| 100 | Normal | Evaluation | Evaluation |
| 105, 106 | Inner Race | Train | Train |
| 107 | Inner Race | Validation | Validation |
| 108 | Inner Race | Evaluation | Not used |
| 118, 119 | Ball | Train | Not used |
| 120 | Ball | Validation | Not used |
| 121 | Ball | Evaluation | Evaluation |
| 130, 131 | Outer Race 6:00 | Train | Train |
| 132 | Outer Race 6:00 | Validation | Validation |
| 133 | Outer Race 6:00 | Evaluation | Not used |
| 144, 156 | Outer Race 3:00 / 12:00 | Not used | Not used |
| 169, 185, 197 | 0.014-inch Fault | Not used | Not used |

## Data Reuse Restrictions

- Original 16 recordings are previously used research data.
- New recordings 144, 156, 169, 185, and 197 have passed
  signal-integrity checks but have not been model-evaluated.
- Signal-integrity inspection does not constitute model evaluation.
- New recording roles must be fixed before inspecting predictions.
- Physical-bearing and defect-instance independence remain unknown.
- New fault recordings do not provide independent Normal data.
- Any future evaluation must explicitly state its independence level.

No new two-stage training or evaluation split has been finalized.

## Proposed Dataset Split Strategy

Status: Design only. No split finalized.

### Stage 1 — Anomaly Detection

- Reuse previously examined Normal recordings for
  exploratory model development only.
- Keep the existing RMS baseline as a reference.
- Use expansion fault recordings to investigate
  detection under new fault conditions.
- Do not claim independent Normal/Fault evaluation
  without suitable independent Normal recordings.

### Stage 2 — Fault Diagnosis

- Initially distinguish Inner Race, Outer Race, and Ball.
- Treat fault diameter and Outer Race position as
  potential distribution-shift variables.
- Separate previously used data from new recordings.
- Define known-fault versus unknown-fault experiments
  before inspecting model predictions.
- Preserve an explicit Unknown/Abstain output.

### Split Integrity

- Do not randomly split overlapping signal windows.
- Group recordings sharing a physical bearing or defect
  instance whenever that relationship is known.
- Mark physical identities as unknown when unverified.
- Do not report recording-level isolation as proof of
  physical-bearing independence.
- Reserve evaluation data before model selection.
- Any analysis on previously examined recordings
  must be labeled exploratory.

No model evaluation has been conducted under this protocol.

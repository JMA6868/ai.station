# Step 27.11L — Combined Anomaly Detection Protocol

## Status

Protocol design in progress.

No combined anomaly detection model has been trained or evaluated.

## Research Question

Can RMS and Crest Factor provide complementary information
for normal-only vibration anomaly detection?

## Available Data

Training:
- Normal Recording 97 (0 HP)
- Normal Recording 98 (1 HP)

Exploratory validation:
- Normal Recording 99 (2 HP)

Previously evaluated:
- Normal Recording 100 (3 HP)
- Ball Fault Recording 121 (3 HP)

Previously evaluated recordings must not be treated as
fresh independent test data.

## Features

- RMS
- Crest Factor

Window size: 1200 samples.
Step size: 600 samples.
Overlap: 50%.

## Baseline

Existing normal-only RMS P99 detector.

Training-derived RMS threshold:
0.078705085

## Proposed Comparison

Compare the RMS-only baseline with a combined-feature
anomaly detector.

The combined method, threshold selection, and evaluation
metrics must be specified before fitting or testing.

## Evaluation Principles

1. Split by recording, not by overlapping windows.
2. Never fit scalers or thresholds on evaluation recordings.
3. Do not modify frozen Experiment A/B results.
4. Label previously examined data as exploratory.
5. Report false-positive behavior and detection sensitivity separately.
6. Avoid claims of cross-bearing generalization.
7. Treat overlapping windows as correlated observations.

## Current Limitations

Only two Normal recordings are available for training.

Normal Recording 99 and Ball Fault Recording 121 have
already been examined during exploratory analysis.

A genuinely independent evaluation will require new,
previously unseen recordings or a new dataset with a
documented separation protocol.

## Candidate Detector — Dual Threshold

Proposed exploratory method:

1. Use the existing training-derived RMS P99 threshold.
2. Compute a Crest Factor P99 threshold using Normal
   Training Recordings 97 and 98 only.
3. Flag a window when either condition holds:

   RMS > RMS_P99 OR Crest_Factor > CF_P99

4. Compare RMS-only and Dual-Threshold flags on the
   training recordings before exploratory validation.

Important:

- A P99 threshold for each individual feature does not
  guarantee a combined false-positive rate of 1%.
- Thresholds must be derived from training data only.
- Threshold choices are exploratory and must be documented
  before applying the detector to additional recordings.
- Recording 99 has already been examined; results from it
  are exploratory rather than independent validation.
- Recording 121 must not be presented as a new test set.

This candidate method has not yet been implemented.

## Training-Only Threshold Calibration Results

Status: Completed — exploratory training calibration.

Data:
- Normal Recording 97: 405 windows
- Normal Recording 98: 805 windows
- Total: 1210 normal training windows

Thresholds:
- RMS P99: 0.078705085
- Crest Factor P99: 3.951375434

Detection rule:
- RMS > RMS_P99 OR Crest Factor > CF_P99

Training alarm counts:

| Recording | Windows | RMS-only | Dual-Threshold |
|---|---:|---:|---:|
| 97 | 405 | 12 | 16 |
| 98 | 805 | 1 | 9 |
| Total | 1210 | 13 | 25 |

Overall training alarm rates:
- RMS-only: 13/1210 = 1.0744%
- Dual-Threshold: 25/1210 = 2.0661%
- Additional Dual-Threshold alarms: 12 windows

Interpretation:

The Dual-Threshold OR rule increased the number of alarms
on normal training data.

These in-sample results do not establish operational
false-positive rates or improved fault detection.

Overlapping windows are correlated observations.

No independent evaluation was performed during calibration.

Thresholds must remain fixed during subsequent exploratory
comparisons; previously evaluated data must not be treated
as new independent test data.

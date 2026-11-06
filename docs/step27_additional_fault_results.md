# Step 27.12-11Q — Additional CWRU Fault Evaluation Results

## Status

Completed descriptive evaluation of 28 additional
CWRU 12 kHz Drive End fault recordings.

## Protocol and Data

Protocol:
docs/step27_additional_fault_evaluation_protocol.md

Source inventory:
docs/step27_additional_cwru_inventory.csv

Per-recording results:
docs/step27_additional_fault_results.csv

## Frozen Configuration

Target sampling rate: 12000 Hz
Window size: 1200 samples
Window step: 600 samples

RMS P99 threshold: 0.07467624803042527

Window anomaly criterion:
RMS > frozen threshold

Recording anomaly criterion:
Anomalous window fraction > 0.05

The threshold was not recalibrated.

## Overall Results

Fault recordings evaluated: 28
Fault recordings detected: 28
Missed fault recordings: 0

Total fault windows: 5643
Anomalous fault windows: 5643

All evaluated fault windows exceeded the frozen
RMS threshold.

## Detection by Fault Diameter

| Diameter (in) | Detected | Total |
|---|---:|---:|
| 0.021 | 20 | 20 |
| 0.028 | 8 | 8 |

## Detection by Fault Condition

| Condition | Detected | Total |
|---|---:|---:|
| Inner Race | 8 | 8 |
| Ball | 8 | 8 |
| Outer Race 6 o'clock | 4 | 4 |
| Outer Race 3 o'clock | 4 | 4 |
| Outer Race 12 o'clock | 4 | 4 |

## Detection by Motor Load

| Load (HP) | Detected | Total |
|---|---:|---:|
| 0 | 7 | 7 |
| 1 | 7 | 7 |
| 2 | 7 | 7 |
| 3 | 7 | 7 |

## Comparison With Previous Evaluation

Previous descriptive Fault evaluation:
17/17 detected.

Additional Fault evaluation:
28/28 detected.

Combined descriptive coverage:
45/45 Fault recordings detected.

Previously evaluated Normal recordings:
99 and 100, with 0/2 recording-level false alarms.

Normal recordings 97 and 98 were used for
RMS threshold calibration.

## Interpretation

The frozen harmonized RMS P99 baseline detected
all 28 additional CWRU fault recordings.

The observed separation is strong for the
evaluated CWRU fault conditions.

These results do not establish independent
cross-bearing or industrial generalization.

## Scientific Limitations

- Physical-bearing independence remains unverified.
- The evaluation adds Fault recordings only.
- Normal false-alarm robustness was not newly tested.
- Previously evaluated recordings are not untouched holdouts.
- Overlapping windows are not independent observations.
- Fault severity and load conditions are not equally represented
  across every fault category.
- Recording-level metrics are based on the evaluated recordings.
- No threshold retuning was performed.

## Next Research Priority

Investigate the magnitude and possible causes
of Normal/Fault RMS separation.

Assess remaining CWRU condition coverage and
Normal-data limitations.

Plan leakage-aware comparisons between the frozen
RMS baseline, traditional ML and deep learning.

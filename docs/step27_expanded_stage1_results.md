# Step 27.12-11P — Expanded Stage 1 RMS Results

## Status

Completed descriptive evaluation of 19 CWRU recordings.

## Protocol

docs/step27_expanded_stage1_protocol.md

## Frozen Configuration

Target sample rate: 12000 Hz
Window size: 1200
Window step: 600

RMS P99 threshold: 0.07467624803042527
Recording anomaly criterion: fraction > 0.05

Training Normal IDs: 97, 98
Evaluation Normal IDs: 99, 100

## Recording-Level Results

Normal false alarms: 0/2
Fault detections: 17/17
Recording-level correct decisions: 19/19

All evaluated fault windows were flagged anomalous.
All evaluated Normal windows were below the threshold.

## Detection by Fault Condition

| Condition | Detected | Total |
|---|---:|---:|
| Inner Race | 5 | 5 |
| Ball | 5 | 5 |
| Outer Race 6 o'clock | 5 | 5 |
| Outer Race 3 o'clock | 1 | 1 |
| Outer Race 12 o'clock | 1 | 1 |

## Detection by Fault Diameter

| Diameter (in) | Detected | Total |
|---|---:|---:|
| 0.007 | 14 | 14 |
| 0.014 | 3 | 3 |

## Detection by Motor Load

| Load (HP) | Detected | Total |
|---|---:|---:|
| 0 | 8 | 8 |
| 1 | 3 | 3 |
| 2 | 3 | 3 |
| 3 | 3 | 3 |

## Interpretation

The frozen harmonized RMS baseline detected every fault
recording in this descriptive expansion evaluation.

The result demonstrates strong RMS separation for the
specific CWRU recordings and conditions evaluated.

It does not establish independent model generalization.

## Scientific Limitations

- All recordings had been involved in previous research.
- This is not a newly untouched holdout test.
- Physical-bearing independence remains unverified.
- Only two Normal recordings were evaluated.
- Evaluated fault diameters were 0.007 and 0.014 in.
- Fault coverage across loads and conditions is uneven.
- Overlapping windows are not independent observations.
- The frozen RMS threshold was not retuned.
- Previous experimental results remain unchanged.

## Next Research Priority

Expand to additional official CWRU fault conditions,
especially 0.021 and 0.028 in where available.

Preserve the frozen baseline and document new recordings
before evaluating their outcomes.

Plan leakage-aware comparisons with traditional ML
and deep learning models.

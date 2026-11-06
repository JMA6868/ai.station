# Harmonized Stage 1 — First Evaluation Results

## Protocol

docs/step27_harmonized_stage1_protocol.md

## Frozen Configuration

Target sampling rate: 12000 Hz
Window size: 1200
Window step: 600
Normal training: 97, 98
RMS threshold percentile: P99
Recording anomaly criterion: fraction > 0.05

## Threshold

Harmonized RMS P99:
0.07467624803042527

## Evaluation Results

| ID | Class | Windows | Anomalous | Rate | Detected |
|---|---|---:|---:|---:|---|
| 99 | Normal | 201 | 0 | 0.00% | False |
| 100 | Normal | 201 | 0 | 0.00% | False |
| 144 | Fault | 202 | 202 | 100.00% | True |
| 156 | Fault | 202 | 202 | 100.00% | True |
| 169 | Fault | 202 | 202 | 100.00% | True |
| 185 | Fault | 202 | 202 | 100.00% | True |
| 197 | Fault | 202 | 202 | 100.00% | True |

## Summary

Normal recording false alarms: 0/2
Fault recording detections: 5/5
Fault anomalous windows: 1010/1010

## Comparison With Original Baseline

Original RMS P99: approximately 0.078705085
Harmonized RMS P99: 0.07467624803042527

Original expansion fault anomalous windows: 1004/1010
Harmonized expansion fault anomalous windows: 1010/1010

Original expansion recording detections: 5/5
Harmonized expansion recording detections: 5/5

## Limitations

- These recordings were previously used in project research.
- This is a controlled preprocessing comparison.
- Results are not from a newly untouched test set.
- Physical-bearing independence remains unverified.
- The evaluated Normal and Fault recordings are limited.
- A perfect result on these recordings does not establish
  generalization across the complete CWRU dataset.
- Threshold and window-duration changes are confounded;
  the observed differences cannot be attributed to one alone.
- Frozen historical results remain unchanged.

## Next Research Priority

Expand the evaluation design to additional CWRU conditions
without using evaluation results to tune the current baseline.

Compare RMS against traditional ML and deep learning only
under clearly documented, leakage-aware evaluation protocols.

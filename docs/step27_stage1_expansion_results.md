# Step 27.12 — Stage 1 Expansion Fault Evaluation Results

## Experiment Status

First evaluation completed under the frozen Stage 1 protocol.

Protocol:
- docs/step27_two_stage_protocol.md

Evaluation code commit:
- 39c4557

Raw evaluation log:
- docs/step27_stage1_expansion_first_evaluation.log

## Experimental Configuration

Normal calibration recordings:
- 97, 98

Fault evaluation recordings:
- 144, 156, 169, 185, 197

Window size: 1200 samples
Step: 600 samples

Thresholds:
- RMS P99: 0.078705085
- Crest Factor P99: 3.951375434

The implementation recalculates thresholds from Normal
recordings using full floating-point precision.

Baseline A:
- RMS-only

Baseline B:
- RMS OR Crest Factor

Recording-level decision:
- Abnormal when anomaly_rate > 0.05

No threshold adjustments were made after evaluation.

## First Evaluation Results

| Recording | Total Windows | RMS Alarms | RMS Rate | Dual Alarms | Dual Rate |
|---|---:|---:|---:|---:|---:|
| 144 | 202 | 202 | 100.00% | 202 | 100.00% |
| 156 | 202 | 202 | 100.00% | 202 | 100.00% |
| 169 | 202 | 202 | 100.00% | 202 | 100.00% |
| 185 | 202 | 196 | 97.03% | 197 | 97.52% |
| 197 | 202 | 202 | 100.00% | 202 | 100.00% |

Total windows: 1010
RMS anomalous windows: 1004
Dual anomalous windows: 1005

Recording-level fault detection:
- RMS-only: 5/5
- RMS plus Crest Factor: 5/5

## Key Findings

1. Both frozen baselines flagged all five expansion fault
   recordings as abnormal at the recording level.

2. RMS-only identified 1004 of 1010 fault windows.

3. RMS plus Crest Factor identified 1005 of 1010 fault windows.

4. Crest Factor added one anomalous window on Recording 185.

5. Crest Factor did not improve recording-level detection
   coverage in this evaluation.

## Scientific Limitations

- All five evaluation recordings contain known fault conditions.
- No new independent Normal recording was evaluated.
- Independent normal false-alarm performance is unknown.
- Physical-bearing and defect-instance independence
  have not been established.
- Overlapping windows are correlated.
- The five recordings do not establish broad
  cross-equipment or cross-bearing generalization.
- These results do not establish complete system accuracy.
- Stage 2 fault diagnosis was not evaluated in this experiment.

## Research Interpretation

The frozen RMS baseline was sufficient to flag all five
specified expansion fault recordings.

Adding Crest Factor produced minimal incremental window-level
detection and no additional recording-level detections.

The results support further investigation of challenging
fault conditions, independent Normal recordings, and the
two-stage fault diagnosis architecture.

The frozen evaluation results must not be retroactively
altered through threshold tuning.

# Step 27.11 — Normal-only Anomaly Detection Research Protocol

## Status

Exploratory Research Protocol — Planning.

No new anomaly detection model has been trained or evaluated.

## Research Question

Can a model trained only on Normal vibration recordings
identify deviations associated with fault conditions that
were not represented during training?

## Dataset

CWRU 12 kHz Drive End vibration signals.

Window size: 1200 samples.
Step size: 600 samples.
Overlap: 50%.

Initial features:
- Mean
- Standard deviation
- RMS

## Planned Development Data

Normal-only training:
- Recording 97: Normal, 0 HP
- Recording 98: Normal, 1 HP

Normal validation:
- Recording 99: Normal, 2 HP

Known-fault diagnostics:
- Recordings 105, 106, 107: Inner Race
- Recordings 130, 131, 132: Outer Race

Previously evaluated or explored recordings:
- 100, 108, 121, 133

Other CWRU recordings must not automatically be treated
as independent untouched final-test data.

## Candidate Methods

1. RMS-based anomaly scoring.
2. Statistical distance from the Normal feature distribution.
3. Potential later comparison with one-class methods.

Methods must be evaluated individually with documented
development decisions.

## Evaluation Principles

- Keep Experiment A and Experiment B frozen.
- Do not reuse previously evaluated recordings as fresh holdouts.
- Fit all learned preprocessing and parameters on training data.
- Select operating thresholds using an explicitly defined
  development procedure, not a designated final test set.
- Report false alarms and fault detection separately.
- Report results per recording and per fault condition.
- Acknowledge correlations among overlapping windows.
- Do not claim physical bearing independence without evidence.
- Clearly label all current CWRU follow-up results as exploratory.

## Success Criteria for Planning

- Research question and development datasets documented.
- Candidate methods defined without fitting a model.
- Evaluation limitations explicitly identified.
- Frozen Experiment A/B results preserved.

## Initial RMS Baseline — Pre-validation Decision

Status: Exploratory candidate selected before inspecting
Normal Validation recording 99 for this baseline.

Anomaly score: Window RMS.

Candidate threshold: P99 of the pooled Normal Training RMS values
from recordings 97 and 98.

Observed training P99: approximately 0.078705.

Decision rule:
- RMS > threshold: Anomaly
- RMS <= threshold: Normal

Training-only diagnostics:
- Recording 97: 12/405 windows flagged (2.9630%).
- Recording 98: 1/805 windows flagged (0.1242%).

This choice is a simple initial baseline, not an optimized
threshold or a guaranteed 1% false-positive-rate detector.

The threshold will not be revised in response to the first
Normal Validation result. Any revised method must be documented
as a separate exploratory experiment.

Evaluation limitations:
- Window-level flags are correlated due to overlapping windows.
- Different recording conditions may have different RMS distributions.
- Normal Validation recording 99 has not yet been inspected for
  this baseline.
- Previously evaluated fault recordings are not untouched tests.
- No independent physical-bearing generalization is claimed.

## Initial RMS Baseline — First Normal Validation Results

Status: Completed — Exploratory Normal Validation.

The initial threshold was selected using Normal Training
recordings 97 and 98 before inspecting this validation result.

Method:
- Anomaly score: Window RMS.
- Threshold: Training RMS P99 = 0.078705085.
- Decision rule: RMS > threshold indicates Anomaly.

Normal Validation:
- Recording: 99.
- Operating load: 2 HP.
- Windows: 807.
- Flagged anomalous: 0.
- Window-level flag rate: 0.0000%.
- Mean RMS: 0.064281.
- Maximum RMS: 0.072400.

Interpretation:

All Normal Validation windows remained below the initial
Training-derived P99 threshold.

This result demonstrates zero flagged windows on this
specific Normal recording. It does not establish a general
zero false-positive rate across independent bearings,
machines, or industrial operating conditions.

The threshold was not revised after observing these results.

Limitations:
- Only one Normal Validation recording was examined.
- Overlapping windows are correlated.
- The result does not measure unknown-fault detection.
- The validation result is now known and must not be
  represented as an untouched future evaluation.

## Initial RMS Baseline — Known-Fault Diagnostics

Status: Completed — Exploratory Diagnostics.

The Training-derived RMS P99 threshold remained unchanged:

Threshold: 0.078705085.

Exploratory known-fault results:

| Recording | Condition | Windows | Flagged | Detection Rate |
|---|---|---:|---:|---:|
| 105 | Inner Race | 201 | 201 | 100% |
| 106 | Inner Race | 202 | 202 | 100% |
| 130 | Outer Race | 202 | 202 | 100% |
| 131 | Outer Race | 203 | 203 | 100% |

Total: 808/808 known-fault windows flagged.

Interpretation:

The Normal-derived RMS threshold successfully flagged all
windows from the selected known-fault recordings.

The threshold was not adjusted using these fault recordings.

Limitations:

- These recordings have been used in previous experiments.
- This is an exploratory diagnostic result, not an independent test.
- Overlapping windows are correlated.
- Fault detection on unseen fault types remains unverified
  for this Normal-only baseline.
- No physical bearing independence is established.
## Initial RMS Baseline — Post-evaluation Ball Fault Analysis

Status: Completed — Post-evaluation Exploratory Analysis.

Method:
- Normal-only RMS anomaly detection.
- Threshold: Training P99 = 0.078705085.
- Decision rule: RMS > threshold indicates Anomaly.
- Threshold unchanged after Normal Validation and Known-Fault Diagnostics.

Previously evaluated recordings:

| Recording | Condition | Windows | Flagged | Flag Rate |
|---|---|---:|---:|---:|
| 100 | Normal | 808 | 0 | 0% |
| 121 | Ball Fault | 201 | 201 | 100% |

Comparison with Experiment B:

- Logistic Regression correctly identified 0/201 Ball Fault windows.
- Normal-only RMS Detector flagged 201/201 Ball Fault windows.
- Both methods correctly identified all 808 Normal windows.

Interpretation:

The Normal-only RMS threshold flagged the held-out Ball Fault
recording that the earlier supervised classifier failed to detect.

This supports further investigation of normal-state anomaly
detection for fault types absent from supervised training.

Limitations:

- This analysis uses previously evaluated recordings.
- Recording 121 was examined before this experiment.
- The result is exploratory, not a new independent test.
- The two methods answer different questions: anomaly detection
  versus supervised binary classification.
- The comparison does not establish general superiority.
- Overlapping windows are correlated.
- No independent physical-bearing generalization is established.
- Additional independent datasets are needed before making
  robust unknown-fault detection claims.
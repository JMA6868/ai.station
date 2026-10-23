# Step 27 — Expanded CWRU Evaluation Protocol

## Objective

Evaluate binary fault detection under expanded CWRU fault conditions,
with attention to fault-type generalization and data leakage.

## Available Data

- Normal: recordings 97–100
- Inner Race Fault (0.007 inch): recordings 105–108
- Ball Fault (0.007 inch): recordings 118–121
- Outer Race Fault @ 6:00 (0.007 inch): recordings 130–133
- Motor loads: 0, 1, 2, 3 HP

## Historical Data Usage

Step 26 has already evaluated recordings 100 and 108 as its final holdout.
These recordings must not be described as untouched test data in Step 27.

New recordings 118–121 and 130–133 have undergone descriptive
signal inspection, but not model-based prediction evaluation.

## Proposed Experiment A — Cross-Load Evaluation

Evaluate generalization to different operating loads.

Status: Protocol frozen. See "Frozen Experiment A — Cross-load Engineering Benchmark" below.

## Proposed Experiment B — Held-Out Fault Condition

Train using selected fault conditions and evaluate detection of
a fault condition excluded from training.

Status: Planning.

## Important Constraints

- Split data at recording level or at a stronger independence level.
- Never split overlapping windows randomly across Train and Test.
- Investigate shared bearing and defect-instance identities.
- Ensure evaluation includes appropriate Normal samples.
- Do not interpret window-level performance as independent-bearing
  generalization.
- Freeze model-selection rules before final evaluation.
- Keep Step 26 experimental results unchanged.

## Preliminary Cross-load Split Design

Primary task: Binary fault classification.

- Training loads: 0 HP and 1 HP.
- Validation load: 2 HP.
- Evaluation load: 3 HP.
- Include Normal, Inner Race, Ball, and Outer Race conditions.
- Use complete recordings as the split unit.
- Do not randomly divide overlapping windows across splits.

Important:
- Recordings 100 and 108 were evaluated in Step 26.
- The proposed 3 HP evaluation is not a fully untouched holdout.
- This protocol assesses load-condition generalization, not
  independent-bearing generalization.
- This preliminary split was subsequently frozen under
  "Frozen Experiment A — Cross-load Engineering Benchmark" below.

## Historical Exposure Audit

The proposed Cross-load Evaluation uses 16 recordings.

### Training — 0 and 1 HP
- Previously used in Step 26 Training: 97, 98, 105, 106
- Newly added in Step 27: 118, 119, 130, 131

### Validation — 2 HP
- Previously used in Step 26 Validation: 99, 107
- Newly added in Step 27: 120, 132

### Evaluation — 3 HP
- Previously used in Step 26 Holdout: 100, 108
- Newly added in Step 27: 121, 133

### Interpretation

- Recording IDs are disjoint across the proposed Step 27 splits.
- Training and evaluation loads are different.
- Physical-bearing and defect-instance independence are not established.
- Step 27 Evaluation is not a fully untouched final test.
- The primary experiment should be reported as a cross-load
  engineering evaluation rather than independent-bearing validation.
- The final evaluation protocol must be frozen before model fitting
  and evaluation.

## Frozen Experiment A — Cross-load Engineering Benchmark

Status: Protocol frozen before Step 27 model training.

### Dataset Splits

- Training: 0 and 1 HP
- Validation: 2 HP
- Evaluation: 3 HP
- Split unit: complete recording
- Task: binary classification (Normal=0, Fault=1)

### Model Configuration

- Model: LogisticRegression
- Preprocessing: StandardScaler
- Features: mean, std, rms
- Window size: 1200 samples
- Window step: 600 samples
- Classification threshold: 0.5
- Fit preprocessing and classifier using Training only.

### Evaluation Metrics

- Primary: Recall, Specificity, Balanced Accuracy
- Secondary: Precision, F1, Accuracy
- Report overall and per-recording performance.
- Report detection recall separately for each fault type.

### Scientific Limitations

- Recording-level separation does not guarantee bearing independence.
- Different loads may share physical defect instances.
- Step 26 previously evaluated recordings 100 and 108.
- This experiment is a cross-load engineering benchmark,
  not an untouched independent-bearing evaluation.
- Do not change the model configuration after viewing
  Evaluation results.

## Experiment A — Training and Validation Results

Status: Training and Validation completed.
Evaluation (3 HP) not yet executed.

### Implementation

- Runner: run_step27_cross_load.py
- Model: StandardScaler + LogisticRegression
- Features: mean, std, rms
- Window size: 1200 samples
- Window step: 600 samples
- Classification threshold: 0.5
- Model configuration unchanged from frozen protocol.
- StandardScaler and classifier fitted on Training data only.

### Training Results — 0 and 1 HP

- Recordings: 97, 98, 105, 106, 118, 119, 130, 131
- Total windows: 2422
- Normal windows: 1210
- Fault windows: 1212

Metrics:

- Accuracy: 1.0000
- Precision: 1.0000
- Recall: 1.0000
- F1: 1.0000
- Specificity: 1.0000
- Balanced Accuracy: 1.0000
- Confusion Matrix: TN=1210, FP=0, FN=0, TP=1212

### Validation Results — 2 HP

- Recordings: 99, 107, 120, 132
- Total windows: 1411
- Normal windows: 807
- Fault windows: 604

Metrics:

- Accuracy: 1.0000
- Precision: 1.0000
- Recall: 1.0000
- F1: 1.0000
- Specificity: 1.0000
- Balanced Accuracy: 1.0000
- Confusion Matrix: TN=807, FP=0, FN=0, TP=604

### Per-recording Validation Results

| Recording | Condition | Windows | Correct | Accuracy |
|---|---|---:|---:|---:|
| 99 | Normal | 807 | 807 | 1.0000 |
| 107 | Inner Race Fault | 202 | 202 | 1.0000 |
| 120 | Ball Fault | 201 | 201 | 1.0000 |
| 132 | Outer Race Fault @ 6:00 | 201 | 201 | 1.0000 |

For the Normal recording, per-recording accuracy corresponds
to Specificity.

For each Fault recording, per-recording accuracy corresponds
to Recall.

### Automated Testing

- Full regression suite: 120 passed.
- Dataset integrity and recording isolation checks passed.
- Per-recording reporting tests passed.

### Interpretation and Limitations

- The frozen baseline achieved perfect window-level classification
  on the specified 2 HP Validation recordings.
- These results support cross-load performance within the selected
  CWRU recordings.
- Overlapping windows are not independent observations.
- Recording-level isolation does not establish independent-bearing
  or independent-defect-instance generalization.
- The features std and rms may capture similar amplitude-related
  information; perfect accuracy does not establish that the model
  learned fault-specific physical signatures.
- Only one Normal recording is included in the 2 HP Validation set.
- Real-world deployment performance has not been established.

### Pre-evaluation Checkpoint

- Training and Validation analysis completed before 3 HP Evaluation.
- No 3 HP Evaluation predictions have been generated in Step 27.
- Model configuration, features, preprocessing, windowing,
  and classification threshold remain frozen.
- Do not tune the model based on 3 HP Evaluation results.
- Report 3 HP results even if performance decreases.
- Record that recordings 100 and 108 were previously evaluated
  in Step 26; the benchmark is not a pristine final holdout.

## Decisions Pending

- Design Experiment B for held-out fault-type generalization.
- Determine how to obtain independent Normal evaluation recordings.
- Investigate physical-bearing and defect-instance independence.
- Determine whether an additional public bearing dataset is needed
  for stronger independent-equipment generalization testing.
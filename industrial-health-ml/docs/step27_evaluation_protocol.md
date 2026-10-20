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

Status: Planning.

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
- The split remains provisional until explicitly frozen.

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

## Decisions Pending

- Selection of the primary evaluation protocol.
- Selection of Train, Validation, and Test recordings.
- Method for obtaining independent Normal evaluation data.
- Definition of evaluation metrics and reporting units.
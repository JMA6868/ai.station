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

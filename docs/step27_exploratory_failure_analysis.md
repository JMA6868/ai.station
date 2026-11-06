# Step 27 — Experiment B Exploratory Failure Analysis

## Status

Exploratory / Post-evaluation Analysis.

This analysis was performed after the Experiment B frozen evaluation.
It does not modify the frozen protocol, model configuration, or evaluation results.

## Frozen Evaluation Reference

- Evaluation recordings: 100 (Normal), 121 (held-out Ball Fault)
- Accuracy: 0.800792864222002
- Ball Fault Recall: 0.0
- Normal Specificity: 1.0
- Balanced Accuracy: 0.5
- Confusion matrix: TN=808, FP=0, FN=201, TP=0

## 1. RMS Distribution

| Recording | Condition | Mean RMS | RMS Range |
|---|---|---:|---|
| 100 | Normal | 0.065823 | 0.058151–0.074234 |
| 121 | Ball Fault | 0.153508 | 0.134232–0.169985 |

Training Inner Race recordings 105 and 106 had mean RMS values
of 0.291421 and 0.292819, respectively.

Training Outer Race recordings 130 and 131 had mean RMS values
of 0.668864 and 0.591659, respectively.

The held-out Ball Fault recording has higher RMS than Normal,
but substantially lower RMS than the fault types used for training.

## 2. Fault Probability

| Metric | Normal 100 | Ball Fault 121 |
|---|---:|---:|
| Mean probability | 0.003508 | 0.293836 |
| Minimum probability | 0.001679 | 0.140158 |
| Maximum probability | 0.008710 | 0.443154 |
| Windows predicted Fault | 0 | 0 |

All 201 Ball Fault windows received fault probabilities below
the frozen classification threshold of 0.5.

However, all Ball Fault scores were higher than all Normal scores
within these two evaluation recordings.

## 3. Logistic Regression Coefficients

The frozen pipeline uses StandardScaler followed by Logistic Regression.

| Feature | Training Mean | Training Scale | Coefficient |
|---|---:|---:|---:|
| mean | 0.012180 | 0.005421 | -0.611834 |
| std | 0.225243 | 0.221524 | 4.834767 |
| rms | 0.226043 | 0.221110 | 4.823769 |

Intercept: 1.351155.

## 4. Decision Score Decomposition

| Component | Normal 100 | Ball Fault 121 |
|---|---:|---:|
| Mean contribution | -0.031298 | 0.901159 |
| STD contribution | -3.506058 | -1.566886 |
| RMS contribution | -3.495384 | -1.582428 |
| Intercept | 1.351155 | 1.351155 |
| Average decision score | -5.681585 | -0.897000 |

Positive scores correspond to Fault and negative scores to Normal.

The average Ball Fault decision score is higher than the Normal
score, but remains below zero.

## 5. Interpretation

The evidence supports the hypothesis that the classifier learned
a decision boundary strongly influenced by vibration amplitude
features from the known fault classes.

The held-out Ball Fault recording showed an intermediate vibration
amplitude. Its decision scores increased relative to Normal but
did not cross the frozen classification boundary.

This is a model-specific explanation of the observed predictions,
not proof of a physical causal mechanism.

STD and RMS are correlated features, so their individual coefficients
must not be interpreted as independent physical effects.

## 6. Limitations

- The analysis is exploratory and was performed after evaluation.
- Recording 121 is no longer an untouched holdout for future tuning.
- Experiment A and Experiment B used different training compositions,
  so their performance difference cannot be attributed solely to
  excluding Ball Fault recordings.
- Overlapping windows are correlated observations.
- CWRU recording-level separation does not establish independence
  of physical bearings or real-world deployment generalization.
- Predicted probabilities are not established as calibrated probabilities.
- No threshold or model changes are justified as independent test
  improvements using these same evaluation recordings.

## 7. Next Research Direction

Investigate alternative fault detection approaches and feature
representations under explicitly documented exploratory protocols.

Any new generalization claim requires appropriately independent
evaluation data and a newly frozen evaluation protocol.

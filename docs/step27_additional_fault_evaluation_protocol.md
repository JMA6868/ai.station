# Step 27.12-11Q — Additional CWRU Fault Evaluation Protocol

## Status

Protocol documented before evaluating the 28 additional recordings.

## Objective

Evaluate the frozen harmonized Stage 1 RMS baseline
on 28 additional CWRU 12 kHz Drive End fault recordings.

Focus on fault diameters 0.021 and 0.028 inches,
across available fault conditions and motor loads.

## Dataset

CWRU Bearing Data Center only.

Source inventory:
docs/step27_additional_cwru_inventory.csv

Normal training:
97, 98

Previously evaluated Normal recordings:
99, 100

Previously evaluated Fault recordings:
105-108, 118-121, 130-133, 144, 156, 169, 185, 197

Additional Fault evaluation:
209-212, 222-225, 234-237, 246-249, 258-261,
3001-3008

Additional recordings: 28
- 0.021 in: 20
- 0.028 in: 8

## Frozen Configuration

Target sample rate: 12000 Hz
Window size: 1200 samples
Window step: 600 samples

Frozen RMS P99 threshold:
0.07467624803042527

Window anomaly rule:
RMS > frozen threshold

Recording anomaly rule:
Anomalous window fraction > 0.05

No recalibration or threshold tuning is permitted
using the additional evaluation recordings.

## Required Reporting

1. Per-recording window counts.
2. Per-recording anomalous window counts.
3. Per-recording anomaly fractions.
4. Recording-level Fault detection outcomes.
5. Detection rates by fault condition.
6. Detection rates by fault diameter.
7. Detection rates by motor load.
8. Missed recordings, if any.
9. Comparison with earlier descriptive RMS results.
10. Explicit limitations and data-use history.

## Scientific Boundaries

- File selection was fixed before RMS evaluation.
- Additional recordings have not yet been evaluated
  by this project's frozen RMS baseline.
- No claim of untouched physical-bearing independence.
- No claim of independent cross-bearing generalization.
- Only fault recordings are added in this phase.
- Normal false-alarm robustness is not newly evaluated.
- Overlapping windows are not independent observations.
- Previous experimental results remain unchanged.
- Results apply only to the CWRU conditions evaluated.

## Next Research Direction

Evaluate the frozen RMS baseline without modifications.

After recording results, assess the remaining CWRU
coverage gaps and plan leakage-aware ML comparisons.

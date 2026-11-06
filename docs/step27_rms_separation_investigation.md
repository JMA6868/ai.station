# Step 27.12-11R — Normal/Fault RMS Separation Investigation

## Status

Descriptive RMS distribution and amplitude-sensitivity investigation.

The frozen Stage 1 RMS threshold and recording-level decision rule were
not modified.

## Dataset

- 4 Normal CWRU recordings: 97, 98, 99, 100
- 45 Fault CWRU recordings
- 49 recordings analyzed in total
- Harmonized sampling rate: 12 kHz
- Window size: 1200 samples
- Step size: 600 samples

Normal recordings 97 and 98 were used for threshold calibration.
Normal recordings 99 and 100 were used for prior evaluation.

## Frozen Detection Rule

- Window anomaly: RMS > 0.07467624803042527
- Recording anomaly: anomaly fraction > 0.05

## RMS Separation

- Maximum Normal window RMS: 0.074948803 (recording 97)
- Minimum Fault window RMS: 0.074981158 (recording 185)
- Separation gap: 0.000032355
- Boundary ratio: approximately 1.000432

The observed window RMS ranges do not overlap, but their closest
boundaries are separated by a very small margin.

The maximum Normal value is from a calibration recording, not an
independent holdout recording.

## Boundary Recording Investigation

| Recording | Class | Above Threshold | Anomaly Fraction |
|---|---|---:|---:|
| 97 | Normal calibration | 3/100 | 3.0% |
| 99 | Normal evaluation | 0/201 | 0.0% |
| 100 | Normal evaluation | 0/201 | 0.0% |
| 185 | Fault | 202/202 | 100.0% |
| 197 | Fault | 202/202 | 100.0% |

The frozen recording-level decision threshold explains why recording
97 remains Normal despite three windows exceeding the RMS threshold.

## Amplitude Sensitivity

Uniform positive amplitude scaling was investigated mathematically
using RMS(scale * signal) = scale * RMS(signal).

For a recording with N windows, detection requires at least
floor(0.05 * N) + 1 anomalous windows.

The critical scale is determined by the corresponding descending-order
RMS statistic. Detection requires scale strictly greater than the
critical scale.

### Selected Recordings

| Recording | Critical Scale | Critical Amplitude Reduction |
|---|---:|---:|
| 185 | 0.302330 | 69.77% |
| 197 | 0.696096 | 30.39% |
| 224 | 0.648981 | 35.10% |
| 225 | 0.601351 | 39.86% |
| 3008 | 0.029574 | 97.04% |

Across 45 Fault recordings:

- Most amplitude-sensitive: 197
- Least amplitude-sensitive: 3008
- Median critical scale: 0.177701

These values represent idealized mathematical sensitivity, not
measured real-world robustness.

## Fault Type and Diameter

Critical scale varies substantially across fault types and diameters.

Examples of median critical scale:

| Diameter | Fault Type | Recording Count | Median Critical Scale |
|---|---|---:|---:|
| 0.007 | Ball | 4 | 0.487693 |
| 0.021 | Ball | 4 | 0.476004 |
| 0.028 | Ball | 4 | 0.031566 |
| 0.007 | Inner race | 4 | 0.245925 |
| 0.021 | Inner race | 4 | 0.146544 |
| 0.028 | Inner race | 4 | 0.084836 |

These observations do not establish a universal monotonic relationship
between fault diameter and detection margin.

## Motor Load

Ten complete 0–3 HP fault groups were analyzed, covering 40 Fault
recordings.

The largest within-group critical-scale range was observed for
0.021-inch Ball Fault: approximately 0.3069.

### 0.021-inch Ball Fault Detail

| Recording | Load HP | Median RMS | P95 RMS | P95/P50 | Critical Scale |
|---|---:|---:|---:|---:|---:|
| 222 | 0 | 0.120422 | 0.217818 | 1.809 | 0.342116 |
| 223 | 1 | 0.109016 | 0.212962 | 1.953 | 0.350656 |
| 224 | 2 | 0.106535 | 0.115053 | 1.080 | 0.648981 |
| 225 | 3 | 0.117680 | 0.124175 | 1.055 | 0.601351 |

The upper RMS tail differs considerably across these recordings.
The data do not establish motor load as the causal explanation.

## Scientific Limitations

1. Results are descriptive for the available CWRU recordings.
2. Normal and Fault acquisition conditions may differ.
3. Normal recordings originated at 48 kHz and were harmonized to 12 kHz,
   while all 45 evaluated Fault recordings originated at 12 kHz.
4. The analysis does not demonstrate independent physical-bearing
   generalization.
5. Overlapping windows are correlated and must not be treated as
   independent test subjects.
6. The frozen threshold was calibrated using Normal 97 and 98.
7. Amplitude scaling is a mathematical sensitivity analysis, not an
   independent experimental validation.
8. Causal interpretations of fault type, diameter, or load are not
   supported by these observational comparisons.

## Next Investigation

Investigate CWRU acquisition and preprocessing differences that may
contribute to the large RMS separation, particularly sampling rate,
sensor configuration, measurement scale, and recording conditions.

Preserve the frozen baseline and all historical evaluation results.

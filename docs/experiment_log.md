# IndustrialSense AI — Experiment Log

## Experiment 001 — CWRU Vibration Analysis

### Dataset
- Source: CWRU Bearing Data Center
- Normal: 97.mat
- Inner race fault: 105.mat
- Signal: Drive-end vibration
- Sampling rate: 12000 Hz

### Window Configuration
- Window size: 1200 samples
- Step: 600 samples
- Overlap: 50%

### Results
| Feature | Normal | Fault |
|---|---:|---:|
| Windows | 405 | 201 |
| Avg RMS | 0.073719 | 0.291421 |
| Avg Std | 0.072625 | 0.291109 |
| Max RMS | 0.082824 | 0.304349 |

### Observations
- Fault RMS is approximately 3.95 times normal RMS.
- Window RMS appears relatively stable within each file.
- Window RMS ranges are clearly separated in these two recordings.

### Limitations
- Only two source recordings examined.
- Faults are artificially introduced.
- No independent classifier evaluation performed.
- Overlapping windows are correlated.
# Step 27.12 — CWRU Dataset Expansion Inventory

## Purpose

Identify additional CWRU 12 kHz Drive-End recordings
for exploratory fault detection and generalization research.

Existing experiments A/B must remain unchanged.

## Current Local Dataset

16 MAT files:

- Normal: 97, 98, 99, 100
- Inner Race 0.007 in: 105, 106, 107, 108
- Ball 0.007 in: 118, 119, 120, 121
- Outer Race 6:00 0.007 in: 130, 131, 132, 133

## Candidate Expansion Recordings

| ID | Condition | Fault Diameter | Load | Local Status |
|---|---|---|---|---|
| 144 | Outer Race 3:00 | 0.007 in | 0 HP | Not downloaded |
| 156 | Outer Race 12:00 | 0.007 in | 0 HP | Not downloaded |
| 169 | Inner Race | 0.014 in | 0 HP | Not downloaded |
| 185 | Ball | 0.014 in | 0 HP | Not downloaded |
| 197 | Outer Race 6:00 | 0.014 in | 0 HP | Not downloaded |

## Research Requirements

- Confirm recording metadata against the official CWRU directory.
- Verify signal keys and sampling configuration after download.
- Do not assume different recordings use independent bearings.
- Do not mix the new data into frozen Experiment A/B splits.
- Define the experimental protocol before model evaluation.
- Keep original MAT files outside Git version control.

## Current Status

Inventory planning only.

No additional recordings have been downloaded or evaluated.

## Official Source

https://engineering.case.edu/bearingdatacenter/12k-drive-end-bearing-fault-data

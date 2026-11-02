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

## Official Metadata Verification

Status: Recording IDs and published conditions verified.

Source:
https://engineering.case.edu/bearingdatacenter/12k-drive-end-bearing-fault-data

Verified candidate recordings:

| ID | Official Dataset Entry | Verification |
|---|---|---|
| 144 | OR007@3_0 | Confirmed |
| 156 | OR007@12_0 | Confirmed |
| 169 | IR014_0 | Confirmed |
| 185 | B014_0 | Confirmed |
| 197 | OR014@6_0 | Confirmed |

All five recordings are listed under the official
12 kHz Drive-End Bearing Fault Data category.

Physical-bearing and defect-instance identities remain
unverified. Distinct recording IDs must not be interpreted
as proof of independent physical bearings.

MAT signal keys and actual signal contents have not yet
been verified locally.

No new recordings have been downloaded or evaluated.

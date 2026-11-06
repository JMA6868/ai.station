# Step 27.12 — Dataset Suitability and Robustness Readiness Audit

## Status

In Progress — audit planning.

## Primary Project Deliverable

Stage 1: Robust Industrial Anomaly Detection.

The system must reliably distinguish Normal from Abnormal
equipment behavior across relevant operating conditions.

Stage 2 fault diagnosis is optional and currently deferred.
Abnormal conditions may be investigated by engineers or
other diagnostic methods.

## Audit Objectives

1. Assess the adequacy of existing CWRU recordings.
2. Distinguish window counts from independent experiments.
3. Assess Normal operating-condition diversity.
4. Investigate physical-bearing and defect-instance independence.
5. Evaluate suitability for traditional ML and deep learning.
6. Identify missing data for robust anomaly detection.
7. Compare potential supplementary industrial datasets.
8. Define evidence needed for Stage 1 delivery readiness.

## Current Evidence

- 21 locally available CWRU recordings.
- 4 Normal recordings: 97, 98, 99, 100.
- 17 Fault recordings.
- Training Normal recordings: 97 and 98.
- Frozen Stage 1 expansion evaluation completed.
- Five specified fault recordings detected by both baselines.
- Independent Normal generalization remains unverified.
- Physical-bearing independence remains unverified.

## Scientific Boundaries

- Many overlapping windows do not imply many independent runs.
- Successful training does not establish model generalization.
- Deep learning cannot compensate for missing operating conditions.
- Previously evaluated recordings are not untouched test data.
- Frozen experimental results must remain unchanged.

## Pending Audit

Detailed data inventory, dataset independence assessment,
deep-learning feasibility, supplementary dataset comparison,
and robustness evaluation requirements.

No new model training is authorized by this audit.

## Full CWRU Dataset Audit Scope

The audit covers the complete official CWRU Bearing Data Center
dataset, not only the 21 recordings currently downloaded.

Official source:
https://engineering.case.edu/bearingdatacenter/download-data-file

Dataset categories:
1. Normal Baseline Data
2. 12 kHz Drive End Bearing Fault Data
3. 48 kHz Drive End Bearing Fault Data
4. 12 kHz Fan End Bearing Fault Data

Audit requirements:
- Inventory every officially listed recording.
- Record sampling rate, fault type, fault size, fault position,
  operating load, approximate RPM, and available channels.
- Mark missing or unavailable recording combinations.
- Compare official inventory against locally downloaded files.
- Investigate bearing and defect-instance independence.
- Evaluate normal-data adequacy separately from fault-data volume.
- Assess suitability for traditional ML and deep learning.
- Identify data gaps affecting robust Stage 1 delivery.

Do not assume additional recordings are independent experiments.
Do not download the entire dataset before evaluating its relevance.
Do not modify frozen Experiment A/B or Stage 1 evaluation results.

Status: Full official dataset inventory pending.

## Preliminary Official CWRU Inventory

Source: CWRU Bearing Data Center official data pages.

| Dataset Category | Listed File Links |
|---|---:|
| Normal Baseline | 4 |
| 12 kHz Drive End Fault | 60 |
| 48 kHz Drive End Fault | 52 |
| 12 kHz Fan End Fault | 45 |
| Total | 161 |

Local inventory:
- 21 downloaded recordings.
- 4 Normal Baseline recordings.
- 17 Drive End fault recordings.

Important:
- Counts represent links listed in the official catalog.
- They do not represent independent bearings or experiments.
- File accessibility and detailed metadata require verification.
- Physical-bearing and defect-instance identities remain unknown.
- Normal data diversity is a critical Stage 1 research concern.
- Deep-learning suitability has not yet been established.

Status: Preliminary inventory completed.
Detailed recording-level audit pending.

## Normal Baseline Data Audit

Official CWRU Normal Baseline recordings:
- 97: 0 HP
- 98: 1 HP
- 99: 2 HP
- 100: 3 HP

Audit questions:
- Confirm original sampling rate and available sensor channels.
- Confirm actual signal duration for each recording.
- Determine whether recordings share the same physical bearing.
- Determine whether multiple independent healthy bearings exist.
- Evaluate load and RPM diversity.
- Assess suitability for Normal-only deep learning.
- Determine whether independent Normal evaluation is possible.

Current concern:
Four Normal recordings may provide many signal windows,
but not enough independent healthy operating conditions
to establish industrial robustness.

Status: Pending detailed verification.

### Verified Normal Operating Conditions

Official source:
https://engineering.case.edu/bearingdatacenter/normal-baseline-data

| Recording | Load (HP) | Approx. RPM |
|---|---:|---:|
| 97 | 0 | 1797 |
| 98 | 1 | 1772 |
| 99 | 2 | 1750 |
| 100 | 3 | 1730 |

Findings:
- Four Normal Baseline files are officially listed.
- Motor load and speed vary together.
- Independent healthy-bearing count is not established.
- Sampling rate, channels and signal duration require verification.
- These four files alone cannot establish industrial robustness.

Next: Investigate physical-bearing independence and
normal-data acquisition details.

## Stage 1 Sampling-Rate Consistency Audit

Status: Confirmed preprocessing inconsistency.

Evidence:
- Official CWRU Normal Baseline sampling rate: 48 kHz.
- Selected Drive End fault recordings: 12 kHz.
- src/cwru_loader.py loads raw DE signals without resampling.
- src/feature_extraction.py uses sample-count windows.
- src/stage1_expansion_evaluation.py uses 1200-sample windows
  and 600-sample steps without resampling.

Physical window duration:
- Normal 48 kHz: 25 ms.
- Fault 12 kHz: 100 ms.

Scientific implications:
- Window durations differ by a factor of four.
- Sampling conditions may confound comparisons.
- Existing 5/5 fault detection remains a valid recorded result,
  but does not establish sampling-rate-independent performance.
- Sampling-rate mismatch has not been proven to cause the
  observed Normal/Fault RMS separation.
- Frozen experiments and thresholds must remain unchanged.

Required follow-up:
1. Define a common target sampling rate.
2. Design anti-aliased resampling and preprocessing checks.
3. Recalibrate thresholds using harmonized training data.
4. Re-evaluate using a separately documented protocol.
5. Compare results against the frozen original baseline.

Do not overwrite or reinterpret the original frozen results.

## Physical Bearing Independence Audit

Official source:
https://engineering.case.edu/bearingdatacenter/apparatus-and-procedures

Verified apparatus information:
- Test stand uses a 2 HP motor.
- Faults were introduced using electrical discharge machining.
- Fault diameters include 0.007, 0.014, 0.021,
  0.028 and 0.040 inches.
- SKF bearings were used for smaller fault diameters.
- NTN equivalent bearings were used for larger faults.
- Accelerometers measured drive-end and fan-end vibration.

Unverified independence questions:
- Do Normal recordings 97-100 share one physical bearing?
- Do different loads share the same fault-bearing instance?
- How many physically independent healthy bearings exist?
- How many physically independent fault bearings exist?

Assessment:
Recording IDs and overlapping windows are not equivalent
to independent physical-bearing experiments.

Until physical-bearing identities can be established,
cross-bearing generalization must be reported as unverified.

Status: Physical-bearing independence unresolved.

## Full 12 kHz Drive End Fault Inventory

Official source:
https://engineering.case.edu/bearingdatacenter/12k-drive-end-bearing-fault-data

| Fault Diameter | Inner Race | Ball | Outer Race | Total |
|---|---:|---:|---:|---:|
| 0.007 in | 4 | 4 | 12 | 20 |
| 0.014 in | 4 | 4 | 4 | 12 |
| 0.021 in | 4 | 4 | 12 | 20 |
| 0.028 in | 4 | 4 | 0 | 8 |
| Total | 16 | 16 | 28 | 60 |

Interpretation:
- Counts represent officially listed recording links.
- Four motor-load conditions are represented.
- Outer-race positions are not equally available at all sizes.
- These files may support fault-severity robustness research.
- Independent physical-bearing counts remain unverified.
- Additional fault data alone cannot establish normal robustness.

Status: Category-level inventory completed.
File-level metadata and accessibility checks pending.

## Remaining Official Fault Dataset Inventory

Official category-level verification:

| Dataset Category | Listed File Links | Fault Sizes (in) |
|---|---:|---|
| 48 kHz Drive End | 52 | 0.007, 0.014, 0.021 |
| 12 kHz Fan End | 45 | 0.007, 0.014, 0.021 |

Official sources:
https://engineering.case.edu/bearingdatacenter/48k-drive-end-bearing-fault-data
https://engineering.case.edu/bearingdatacenter/12k-fan-end-bearing-fault-data

Assessment:
- These categories expand fault-condition coverage.
- They do not add new Normal Baseline recordings.
- Fault-position combinations are incomplete.
- Cross-category physical-bearing independence is unverified.
- File-level inventory and acquisition relationships remain pending.
- Additional fault recordings do not resolve Normal diversity gaps.

Status: Remaining fault categories reviewed at catalog level.

## Deep Learning Data Readiness Assessment

Status: Preliminary assessment.

Primary objective:
Develop a robust Stage 1 industrial anomaly detection system.

Model feasibility:

| Model | Preliminary Assessment |
|---|---|
| RMS / Statistical Baseline | Suitable for initial benchmarking |
| Isolation Forest | Feasible for exploratory development |
| One-Class SVM | Feasible for exploratory development |
| Autoencoder | Prototype feasible; normal diversity limited |
| 1D-CNN | Prototype feasible; generalization unverified |
| Self-Supervised Learning | Research feasible; independence remains limited |

Important distinctions:
- Trainability does not establish generalization.
- Overlapping windows are not independent experiments.
- CWRU Normal Baseline totals approximately 35.39 seconds
  of Drive End signal across four operating conditions.
- Independent healthy-bearing count is unverified.
- Sampling-rate harmonization is required for fair comparisons.
- Additional fault recordings do not solve normal-data scarcity.
- Industrial robustness cannot be established from CWRU alone.

Research recommendation:
1. Preserve CWRU as an algorithm development benchmark.
2. Complete file-level metadata and independence audits.
3. Design a sampling-rate-harmonized evaluation protocol.
4. Identify additional independent healthy operating data.
5. Compare baseline and ML models under controlled splits.
6. Validate robustness on independent operating conditions.

Decision:
CWRU supports initial model development.
It is not sufficient by itself to substantiate industrial-grade
Stage 1 generalization or delivery readiness.

## Updated Project Scope — CWRU-Only Research

Decision:
Use only the complete Case Western Reserve University
(CWRU) Bearing Data Center dataset.

No supplementary datasets are planned.

Primary deliverable:
Stage 1 — Reliable Normal vs. Abnormal detection
within the supported CWRU evaluation conditions.

Stage 2:
Fault-type diagnosis is optional (good-to-have).

Research priorities:
1. Complete relevant CWRU dataset inventory.
2. Harmonize sampling rates and window durations.
3. Establish leakage-aware evaluation protocols.
4. Preserve frozen baseline experiments.
5. Compare RMS, traditional ML and deep learning.
6. Evaluate false alarms and missed faults.
7. Select the best-performing defensible Stage 1 method.
8. Deliver reproducible code, tests, results and demo.

Evaluation scope:
Performance claims must remain limited to the
CWRU dataset and the conditions actually tested.

Industrial deployment and cross-dataset generalization
are not required deliverables.

Superseded plan:
Supplementary dataset acquisition is no longer planned.
The earlier audit findings remain retained as history.

Status:
CWRU-only Stage 1 model research is the current priority.

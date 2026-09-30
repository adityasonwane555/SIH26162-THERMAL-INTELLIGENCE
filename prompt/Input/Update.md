# SIH26162 — REAL-DATA VALIDATION & SCIENTIFIC HARDENING PROMPT

## PROJECT

Existing repository:

`SIH26162-THERMAL-INTELLIGENCE`

This repository already contains a functional prototype involving:

* NASA FIRMS ingestion
* thermal event clustering
* facility matching
* Thermal DNA
* change detection
* classification
* evidence generation
* uncertainty scoring
* prioritization
* API
* frontend/investigation UI
* demo/benchmark infrastructure

The current prototype is useful, but its validation layer contains synthetic data, hard-coded evaluation metrics, and heuristic scores that are presented too strongly as empirical results.

Your job is to transform the repository into a:

# REAL-DATA VALIDATED, REPRODUCIBLE, SCIENTIFICALLY DEFENSIBLE SIH26162 SYSTEM

while preserving the existing product and demo functionality.

---

# 1. PRIMARY OBJECTIVE

The most important objective is:

> Replace simulated/hard-coded validation with reproducible evaluation using real/open data wherever scientifically and legally possible.

The final repository must clearly separate:

```text
REAL DATA
SYNTHETIC DATA
DEMO DATA
BENCHMARK DATA
MODEL OUTPUT
HEURISTIC SCORES
EMPIRICAL METRICS
```

No synthetic benchmark may be represented as a real-world validation result.

No hard-coded metric may be presented as measured model performance.

No heuristic confidence score may be presented as calibrated probability unless calibration has actually been demonstrated.

---

# 2. PRESERVE THE CURRENT PRODUCT

Do NOT destroy the existing application.

Do NOT rewrite the entire frontend unnecessarily.

Do NOT throw away useful architecture.

Preserve:

* current UI
* current API
* current investigation workflow
* current Thermal DNA implementation
* current evidence engine
* current uncertainty engine
* current prioritization engine
* current demo mode

unless a component is scientifically incorrect or prevents proper validation.

Create a clean distinction between:

```text
REAL VALIDATION MODE
```

and:

```text
DEMO/SYNTHETIC MODE
```

The existing synthetic/demo functionality should remain available.

---

# 3. VERSIONING

Create a clear version separation.

The current implementation should be preserved conceptually as:

`v0.1-demo-prototype`

The hardened implementation becomes:

`v0.2-real-validation`

Do not delete the current synthetic benchmark machinery.

Move or refactor it under explicitly named namespaces such as:

```text
data/synthetic/
experiments/synthetic/
```

and explicitly label all synthetic artifacts.

---

# 4. IMMEDIATE AUDIT

Before modifying code, inspect the entire repository and identify:

* hard-coded metrics
* hard-coded confidence values
* synthetic datasets
* synthetic benchmark generators
* synthetic training data
* fixed evaluation outputs
* heuristic scores incorrectly described as probabilities
* unsupported scientific claims
* incorrect documentation claims
* leakage risks
* train/test contamination
* data provenance problems

Create:

`docs/VALIDATION_AUDIT.md`

For every issue:

```text
File
Component
Current behavior
Why it is problematic
Severity
Required change
```

---

# 5. CRITICAL VALIDATION RULE

Never do this:

```python
return {
    "precision": 0.958,
    "recall": 0.946,
    "f1": 0.952
}
```

unless those values are actually computed from predictions against a labeled test set.

All metrics must be derived from:

```text
ground_truth
+
predictions
+
evaluation protocol
```

The evaluation system must calculate metrics dynamically.

---

# 6. REMOVE HARDCODED METRICS

Find every hard-coded evaluation value.

Examples include:

* precision
* recall
* F1
* false alarm rate
* unseen-facility F1
* generalization gap
* adversarial pass count
* calibration score
* confidence values
* benchmark improvements

Replace hard-coded values with real calculations.

If a metric cannot currently be computed because data is unavailable:

DO NOT invent the metric.

Return:

```text
NOT_AVAILABLE
```

and explain why.

---

# 7. REAL EVALUATION ENGINE

Create a real evaluation architecture.

Suggested structure:

```text
src/evaluation/
├── datasets.py
├── splits.py
├── metrics.py
├── runner.py
├── baselines.py
├── reports.py
└── provenance.py
```

The evaluation system must accept:

```text
ground_truth
predictions
experiment_config
```

and return computed results.

---

# 8. REQUIRED METRIC IMPLEMENTATIONS

Implement actual calculations for:

## Classification

* precision
* recall
* F1
* macro F1
* weighted F1
* confusion matrix
* balanced accuracy
* per-class metrics

## Event detection

Where labels allow:

* precision
* recall
* F1
* false-positive rate
* false-negative rate

## Anomaly detection

Where labels allow:

* precision
* recall
* F1
* false alarm rate
* detection delay

## Facility matching

Where ground truth allows:

* top-1 accuracy
* top-k accuracy
* candidate recall
* ambiguity rate

## Probability calibration

Only if actual probabilities exist:

* Brier score
* reliability curve
* Expected Calibration Error if justified

## Abstention

Measure:

* abstention rate
* correct abstention rate
* false attribution avoided
* coverage vs accuracy

---

# 9. REAL DATA PIPELINE

Build a real data pipeline using open/legally accessible sources.

The primary thermal data source should be official NASA FIRMS data.

Potential additional data:

* OpenStreetMap
* public industrial facility datasets
* Sentinel-2/Landsat contextual imagery where appropriate
* open land-cover products
* weather/environment data if useful

Do not scrape or use data that violates provider terms.

---

# 10. DATA REGISTRY

Create or update:

`docs/DATA_REGISTRY.md`

For every source:

```text
dataset_name
provider
source_url
access_method
license
temporal_coverage
spatial_coverage
resolution
format
download_date
version
data_quality
limitations
intended_use
```

Every downloaded dataset must have metadata.

---

# 11. REAL FIRMS INGESTION

Implement a reproducible FIRMS ingestion process.

Requirements:

* geographic bounding box
* date range
* sensor/product
* caching
* retries
* validation
* local persistence

Create:

```text
data/raw/firms/
data/processed/firms/
data/metadata/firms/
```

Do not commit credentials.

Use `.env.example`.

---

# 12. DATA DOWNLOAD SCRIPT

Create:

```bash
python scripts/download_firms.py
```

It must support parameters such as:

```text
--bbox
--start-date
--end-date
--sensor
--output
```

Every download must generate a metadata file containing:

```text
source
request parameters
download timestamp
product
version if available
checksum/file hash where practical
```

---

# 13. REAL FACILITY DATA

Build a reproducible facility-data ingestion pipeline.

Use legitimate open sources.

Create:

```bash
python scripts/download_facilities.py
```

Store:

```text
data/raw/facilities/
data/processed/facilities/
```

Each facility should retain:

```text
facility_id
name
type
geometry
source
source_confidence
```

Do not assume that OSM facility geometry is perfect ground truth.

---

# 14. REAL HISTORICAL CASES

Find independently documented thermal events.

We need cases where the label is obtained independently from the thermal satellite observation being evaluated.

Potential sources:

* official incident reports
* government records
* regulatory records
* independently documented industrial accidents
* high-quality event databases
* verified reports

Do not derive ground truth simply from:

> FIRMS hotspot occurred → therefore fire occurred.

That would be circular.

---

# 15. LABEL PROVENANCE

Every ground-truth case must include:

```text
case_id
event_type
event_date
location
source
source_url/reference
label_confidence
evidence_summary
```

Use a label-quality hierarchy such as:

```text
A = independently documented
B = strongly corroborated
C = contextual inference
D = weak proxy
```

Only A/B should be used as strong ground truth.

C/D may be used for exploratory analysis but must not be presented as definitive validation.

---

# 16. REAL BENCHMARK DATASET

Create:

```text
data/benchmarks/real/
```

with:

```text
cases.csv
observations.parquet
facilities.parquet
labels.csv
```

Create:

```text
docs/REAL_BENCHMARK.md
```

containing:

* number of cases
* number of facilities
* geographic coverage
* temporal coverage
* positive classes
* negative classes
* label provenance
* limitations
* exclusions

---

# 17. DO NOT CHERRY-PICK

The benchmark must not be selected simply because the system performs well on it.

Define the selection criteria BEFORE evaluation.

Record:

```text
inclusion criteria
exclusion criteria
sampling method
```

If practical, create a hidden/held-out evaluation subset that development decisions cannot directly influence.

---

# 18. FIX THE SYNTHETIC BENCHMARKS

Existing scripts that generate fake facilities and fake observations may remain.

But rename them clearly:

```text
scripts/generate_synthetic_benchmarks.py
```

Synthetic data must be stored under:

```text
data/synthetic/
```

All outputs must carry metadata:

```text
data_type = SYNTHETIC
```

The UI must clearly distinguish synthetic data from real validation data.

---

# 19. SYNTHETIC DATA ROLE

Synthetic data is allowed for:

* unit testing
* edge cases
* stress testing
* adversarial scenarios
* demo mode
* deterministic development

Synthetic data must NOT be used to claim:

* real-world accuracy
* real-world generalization
* real-world precision
* real-world recall
* real-world calibration

---

# 20. FIX THE CLASSIFIER

The current classifier uses synthetic training examples.

Do NOT allow this synthetic classifier to be presented as the production empirical classifier.

Create two modes:

```text
SyntheticPrototypeClassifier
RealDataClassifier
```

The real classifier must train only from documented datasets.

---

# 21. REAL CLASSIFICATION PIPELINE

Implement:

```text
real data
→ preprocessing
→ feature extraction
→ train/validation/test split
→ model training
→ prediction
→ metrics
→ report
```

Persist:

```text
model.pkl or equivalent
model_metadata.json
training_config.yaml
metrics.json
```

The model metadata must include:

```text
training_data_version
feature_version
model_version
split_strategy
random_seed
```

---

# 22. NO DATA LEAKAGE

Implement strict split logic.

Do not randomly split observations from the same facility across train/test if that lets the model memorize facility-specific behavior.

At minimum evaluate:

## Facility holdout

Some facilities are entirely unseen during training.

## Temporal holdout

Train on earlier data and test on later data.

## Geographic holdout

Train in one region and test in another where sufficient data exists.

---

# 23. THERMAL DNA VALIDATION

This is the most important scientific experiment.

Do not assume Thermal DNA improves performance.

Test it.

Compare:

### A

FIRMS raw features

### B

FIRMS + facility context

### C

FIRMS + historical recurrence

### D

FIRMS + Thermal Operating Envelope / Thermal DNA

### E

FIRMS + Thermal DNA + contextual features

Calculate metrics from actual predictions.

---

# 24. CONDITIONAL THERMAL OPERATING ENVELOPE

Improve the current implementation.

The current system uses historical statistics but is not sufficiently conditional.

Where data permits, build conditional expectations:

```text
FRP | facility
FRP | facility + month
FRP | facility + month + overpass
FRP | facility + context
```

Only add conditioning variables if there is sufficient data.

Avoid overfitting.

---

# 25. SMALL-SAMPLE FACILITIES

For facilities with insufficient historical data:

DO NOT manufacture a Thermal DNA.

Instead:

```text
status = INSUFFICIENT_HISTORY
```

Possible fallback:

* facility-type baseline
* regional baseline
* global baseline

but clearly label which level was used.

Example:

```text
Baseline level:
FACILITY
```

or:

```text
Baseline level:
FACILITY TYPE
```

or:

```text
Baseline level:
REGIONAL
```

---

# 26. THERMAL DNA QUALITY SCORE

Add:

```text
history_count
coverage_duration
observation_frequency
seasonal_coverage
sensor_coverage
data_gaps
```

Then calculate a transparent profile quality indicator.

Do not call it model confidence.

It is:

> historical baseline quality.

---

# 27. FIX UNCERTAINTY

The current uncertainty engine uses manually selected weighted components.

Keep this as:

```text
heuristic uncertainty
```

unless calibrated.

Rename/document appropriately.

If enough held-out predictions exist, implement actual calibration.

Potential methods:

* Platt scaling
* isotonic regression
* calibration curves

Only use probability language after validation.

---

# 28. FIX EVIDENCE SCORES

Current evidence quality values are manually assigned.

Replace or relabel them.

If they remain heuristic, call them:

```text
evidence_quality_heuristic
```

Do not represent:

```text
0.94
```

as empirically measured reliability unless it really is.

---

# 29. FIX PRIORITIZATION

The current evidence-selection score is heuristic.

Do not call it Shannon information gain unless actual entropy reduction is computed.

Separate:

```text
heuristic_priority_score
```

from:

```text
expected_information_gain
```

Only use the latter if mathematically implemented.

---

# 30. REAL INFORMATION GAIN — OPTIONAL ADVANCED MODULE

If enough probabilistic structure exists:

For each possible additional evidence source:

1. enumerate plausible observation outcomes
2. estimate posterior hypotheses
3. calculate expected entropy after observation
4. compare to current entropy
5. select highest expected information gain

Document assumptions.

If this cannot be justified with available data:

Keep the feature as heuristic prioritization and label it accordingly.

---

# 31. FIX SENTINEL-2 DOCUMENTATION

Review all claims relating to Sentinel-2.

Do NOT call Sentinel-2 B11/B12 a thermal infrared sensor.

If used, describe its role accurately as optical/SWIR/contextual evidence.

Correct all documentation and UI language that implies:

> 20 m thermal confirmation

unless a genuine thermal source is being used.

---

# 32. REAL BASELINE SYSTEM

Implement an explicitly simple baseline.

For example:

```text
FIRMS
+
nearest facility
+
simple rule/classifier
```

This baseline must make real predictions.

Do not hard-code its result.

---

# 33. PROPOSED SYSTEM

Then evaluate:

```text
FIRMS
+
facility context
+
Thermal DNA
+
change detection
+
classification
+
evidence
+
uncertainty
```

Both systems must run on exactly the same held-out test cases.

---

# 34. REAL ABLATION ENGINE

Build:

```text
src/evaluation/ablation.py
```

It must run:

```text
A = FIRMS only
B = FIRMS + facility
C = FIRMS + facility + history
D = FIRMS + Thermal DNA
E = full system
```

and generate:

```text
reports/ablation_report.md
reports/ablation_results.csv
```

---

# 35. REQUIRED REAL METRICS

For every model:

```text
precision
recall
F1
macro F1
balanced accuracy
confusion matrix
false positive rate
false negative rate
```

If probability outputs exist:

```text
Brier score
calibration curve
```

For anomaly detection:

```text
detection delay
false alarm rate
event-level recall
```

---

# 36. GENERALIZATION REPORT

Create:

```text
reports/generalization_report.md
```

Contain:

## Random/standard split

Results.

## Facility holdout

Results.

## Geographic holdout

Results.

## Temporal holdout

Results.

Do NOT hide a generalization failure.

---

# 37. REAL FAILURE ANALYSIS

Every false positive and false negative should be inspectable.

Create:

```text
reports/failure_analysis.md
```

For each important failure:

```text
case
true_label
predicted_label
facility
model
features
reason_for_failure
data_quality
possible_fix
```

---

# 38. REMOVE MISLEADING README CLAIMS

Rewrite the README.

The README must not claim:

* 95.8% precision
* 0.952 F1
* 0.914 unseen-facility F1
* 12/12 adversarial cases passed

unless the new real evaluation system actually produces and stores those results.

Replace them initially with:

```text
Validation status:
REAL-DATA VALIDATION IN PROGRESS
```

until real results exist.

After validation, automatically generate the numbers from the evaluation artifacts.

---

# 39. REAL RESULT ARTIFACT

Create:

```text
reports/real_validation_report.md
```

It must contain:

1. Dataset
2. Data sources
3. Ground-truth methodology
4. Split methodology
5. Baseline
6. Proposed system
7. Metrics
8. Calibration
9. Generalization
10. Ablation
11. Failure cases
12. Limitations
13. Reproducibility information

---

# 40. MACHINE-READABLE RESULTS

Create:

```text
reports/results/
├── baseline.json
├── proposed.json
├── ablation.json
├── facility_holdout.json
├── geographic_holdout.json
├── temporal_holdout.json
└── calibration.json
```

Every JSON file must be generated by the evaluation engine.

No manually typed metric values.

---

# 41. AUTOMATIC REPORT GENERATION

Create:

```bash
python scripts/run_real_evaluation.py
```

This should:

1. load benchmark
2. load models
3. generate predictions
4. calculate metrics
5. calculate holdouts
6. calculate calibration where possible
7. generate plots
8. generate JSON
9. generate Markdown report

---

# 42. REPRODUCIBILITY COMMAND

Provide:

```bash
python scripts/reproduce_validation.py
```

It should run the complete evaluation from a documented dataset/model state.

If external data is unavailable, provide cached open-data fixtures where licensing permits.

---

# 43. EXPERIMENT PROVENANCE

Every experiment must record:

```text
experiment_id
timestamp
dataset_version
model_version
feature_version
code_commit
configuration
random_seed
```

---

# 44. DATASET VERSIONING

Create metadata such as:

```text
dataset_version
created_at
source
source_version
sha256
record_count
geographic_extent
temporal_extent
```

Use checksums where practical.

---

# 45. DEMO MODE MUST REMAIN

The existing polished demo must continue working.

Implement:

```text
DEMO_MODE=true
```

Demo mode may use synthetic/precomputed data.

BUT THE UI must clearly show:

```text
DEMO / SYNTHETIC DATA
```

when applicable.

Do not confuse demo mode with validation mode.

---

# 46. REAL VALIDATION MODE

Implement:

```text
VALIDATION_MODE=true
```

It must show:

```text
REAL/OPEN DATA
```

and link each major result to its dataset/provenance.

---

# 47. UI CHANGES

Add an explicit data-status indicator:

```text
DEMO
```

or:

```text
REAL DATA
```

or:

```text
SYNTHETIC BENCHMARK
```

The user should never have to guess.

---

# 48. FACILITY PAGE

Add:

## Historical coverage

```text
Observations: N
First observation: date
Last observation: date
Coverage quality: ...
```

## Thermal DNA quality

```text
History sufficiency
Seasonal coverage
Data gaps
```

---

# 49. EVENT PAGE

Show:

```text
Data source
Observation timestamp
Sensor
Confidence
Facility match confidence
Historical baseline quality
Model version
Classification
Uncertainty
```

---

# 50. EVIDENCE PANEL

For each conclusion show:

```text
Evidence
Source
Value
Direction
Quality
Provenance
```

If heuristic:

```text
HEURISTIC
```

If empirical:

```text
EMPIRICALLY VALIDATED
```

Do not blur them.

---

# 51. SCIENTIFIC LANGUAGE

Correct all UI/documentation language.

Use:

```text
candidate
possible
estimated
associated
supported by evidence
moderate confidence
insufficient evidence
```

Avoid:

```text
confirmed culprit
certain fire
guaranteed
100%
```

unless independently justified.

---

# 52. TESTING

Add unit tests for:

* metric calculations
* split logic
* leakage prevention
* provenance
* dataset loading
* feature generation
* Thermal DNA
* anomaly detection
* uncertainty
* calibration

Add integration tests for:

```text
real data
→ features
→ prediction
→ metrics
```

---

# 53. DATA LEAKAGE TESTS

Create automated checks for:

### Facility leakage

No facility may appear in both training and strict facility-holdout test.

### Temporal leakage

No future observations may enter historical features used for past predictions.

### Duplicate leakage

Detect duplicate observations.

### Event leakage

Ensure observations belonging to the same event cannot be split improperly.

---

# 54. SYNTHETIC ADVERSARIAL TESTS

Keep synthetic adversarial cases.

They remain useful.

Label them:

```text
SYNTHETIC ADVERSARIAL TEST
```

Report:

```text
synthetic robustness
```

not:

```text
real-world accuracy
```

---

# 55. REAL ADVERSARIAL CASES

Where possible, add genuinely difficult historical cases:

* flare vs fire
* wildfire near industry
* agriculture near facility
* two nearby industrial facilities
* low-confidence anomaly
* sparse historical record
* unseen facility

These must have documented labels/provenance.

---

# 56. PROJECT DOCUMENTATION

Create/update:

```text
docs/
├── VALIDATION_AUDIT.md
├── DATA_SOURCES.md
├── REAL_BENCHMARK.md
├── EVALUATION_PROTOCOL.md
├── MODEL_CARD.md
├── SCIENTIFIC_LIMITATIONS.md
└── CLAIMS_AND_EVIDENCE.md
```

---

# 57. CLAIMS AND EVIDENCE REGISTER

Create:

`docs/CLAIMS_AND_EVIDENCE.md`

For every major statement the project makes:

```text
Claim
Evidence
Dataset
Experiment
Status
Allowed wording
Forbidden wording
```

Example:

```text
Claim:
Thermal DNA improves classification.

Status:
UNPROVEN

Allowed wording:
"We investigate whether facility-specific thermal history improves classification."

Forbidden wording:
"Thermal DNA improves accuracy by 30%."
```

Once experimentally proven:

```text
Status:
SUPPORTED
```

with exact metrics.

---

# 58. SCIENTIFIC LIMITATIONS DOCUMENT

Explicitly document:

* FIRMS spatial resolution
* facility matching uncertainty
* sparse history
* cloud/sensor limitations
* labeling limitations
* geographic coverage
* thermal-vs-SWIR distinction
* model assumptions
* classifier limitations

---

# 59. DO NOT OVERFIT TO SIH DEMO CASES

The demo case must not be the same exact case used to tune the model until it looks good.

Ideally:

```text
development cases
validation cases
demo case
```

are separated.

If this is impossible because of data scarcity, document the limitation.

---

# 60. MODEL VERSIONING

Every trained model must be saved with:

```text
model_id
version
training_dataset
training_date
feature_version
split_strategy
metrics
```

---

# 61. REAL TRAINING PIPELINE

Create:

```bash
python scripts/train_real_model.py
```

Parameters should include:

```text
--dataset
--model
--features
--split
--seed
--output
```

Output:

```text
models/
reports/
```

---

# 62. REAL PREDICTION PIPELINE

Create:

```bash
python scripts/predict_real.py
```

Inputs:

* dataset
* model
* configuration

Outputs:

```text
predictions.parquet
predictions.json
```

---

# 63. REAL EVALUATION PIPELINE

Create:

```bash
python scripts/run_real_evaluation.py
```

Output:

```text
reports/results/
reports/real_validation_report.md
```

---

# 64. NO MANUAL METRIC EDITING

The following files must NEVER contain manually edited metric values:

```text
README.md
reports/results/*.json
evaluation output
UI benchmark cards
```

The UI should read results from generated evaluation artifacts.

---

# 65. BUILD THE VALIDATION DASHBOARD

Add an evaluation section to the frontend:

```text
Validation
────────────
Dataset
Baseline
Proposed
Precision
Recall
F1
False Alarm Rate
Holdout Results
Calibration
Failure Cases
```

Show data type:

```text
REAL DATA
```

or:

```text
SYNTHETIC DATA
```

---

# 66. COMPARISON VIEW

Add:

# BASELINE VS PROPOSED

Display:

```text
Metric                 Baseline    Proposed
Precision
Recall
F1
False Alarm Rate
Detection Delay
Calibration
```

Only display values generated from actual experiment results.

---

# 67. THERMAL DNA ABLATION VIEW

Display:

```text
Model Component                     F1
FIRMS only
FIRMS + facility
FIRMS + history
FIRMS + Thermal DNA
Full system
```

Again, all values must come from experiments.

---

# 68. GENERALIZATION VIEW

Display:

```text
Standard test
Facility holdout
Geographic holdout
Temporal holdout
```

Never present holdout metrics if the holdout is not genuinely implemented.

---

# 69. COMPLETION CRITERIA

Do not consider the validation work complete until:

1. At least one real/open dataset is integrated.
2. At least one real facility dataset is integrated.
3. At least one independently documented event/case exists.
4. Predictions are generated from real inputs.
5. Metrics are dynamically computed.
6. Synthetic benchmarks are separated.
7. Hard-coded metrics are removed from evaluation.
8. Data leakage checks exist.
9. At least one holdout strategy exists.
10. Limitations are documented.
11. README claims match actual evidence.

---

# 70. FINAL README STRUCTURE

Rewrite README approximately as:

```text
# SIH26162 Thermal Intelligence

## Problem

## Solution

## Architecture

## Core Innovation

## Data Sources

## Real Validation

## Benchmark

## Baseline vs Proposed

## Generalization

## Limitations

## Demo

## Setup

## Reproduction

## Scientific Methods
```

Never put unsupported performance claims in the top section.

---

# 71. FINAL PRODUCT POSITIONING

Once real validation exists, the strongest story should be:

> Raw satellite thermal observations are noisy and context-poor. Our system builds facility-aware historical thermal behavior, detects meaningful deviations, explains why an event is unusual, quantifies uncertainty, and prioritizes what deserves investigation.

Do not claim superiority until the real benchmark supports it.

---

# 72. FINAL ENGINEERING PRINCIPLE

This project now enters:

# SCIENTIFIC VALIDATION MODE

The priority order is:

```text
REAL DATA
↓
REPRODUCIBILITY
↓
BASELINE
↓
MEASUREMENT
↓
GENERALIZATION
↓
FAILURE ANALYSIS
↓
INNOVATION PROOF
↓
DEMO
```

Not:

```text
MORE FEATURES
↓
MORE AI
↓
MORE ANIMATIONS
```

---

# 73. FINAL COMMAND

START NOW.

Inspect the complete existing repository.

Do not delete the working demo.

Perform the validation audit.

Then implement the entire real-data validation upgrade.

You are authorized to:

* refactor code
* add new modules
* add new scripts
* modify database schemas
* update APIs
* update frontend
* add tests
* add documentation
* create real evaluation pipelines
* replace hard-coded metrics
* replace synthetic-only training
* correct scientific claims
* improve Thermal DNA
* improve uncertainty handling
* improve benchmarking

Keep the project runnable throughout.

At the end, produce:

```text
docs/VALIDATION_AUDIT.md
docs/REAL_BENCHMARK.md
docs/EVALUATION_PROTOCOL.md
docs/MODEL_CARD.md
docs/SCIENTIFIC_LIMITATIONS.md
docs/CLAIMS_AND_EVIDENCE.md

reports/real_validation_report.md
reports/ablation_report.md
reports/generalization_report.md
reports/failure_analysis.md
```

And ensure the repository contains executable commands for:

```bash
python scripts/download_firms.py
python scripts/download_facilities.py
python scripts/train_real_model.py
python scripts/predict_real.py
python scripts/run_real_evaluation.py
python scripts/reproduce_validation.py
```

If real data or ground truth is unavailable for a particular experiment:

DO NOT fabricate it.

Mark that experiment:

```text
NOT VALIDATED
```

and document the blocker.

If the proposed Thermal DNA approach does not outperform the baseline:

DO NOT hide the result.

Modify the hypothesis and test again.

If the real results are worse than the current synthetic/demo results:

REMOVE THE OLD CLAIM.

The final system must tell the truth.

# END OF PROMPT

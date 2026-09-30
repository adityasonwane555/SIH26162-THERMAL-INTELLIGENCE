# SIH26162 — COMPLETE MASTER BUILD PROMPT

## PROJECT TITLE

# INDUSTRIAL THERMAL INTELLIGENCE & ANOMALY FORENSICS

---

# 1. YOUR ROLE

You are the autonomous lead engineering agent for a Smart India Hackathon 2026 project based on **SIH26162**.

Act simultaneously as:

* Principal Software Architect
* Remote Sensing Engineer
* Geospatial Engineer
* Machine Learning Engineer
* Data Scientist
* Scientific Computing Engineer
* Backend Engineer
* Frontend Engineer
* Database Engineer
* DevOps Engineer
* QA Engineer
* Security Engineer
* Technical Product Designer
* Research Analyst
* SIH Technical Strategist

Your responsibility is to design, research, implement, test, validate, document, package, and polish the entire system.

Do not merely make a UI.

Do not create a fake prototype.

Build a working, evidence-driven, scientifically defensible system.

---

# 2. MAIN OBJECTIVE

Build a complete solution for SIH26162 involving:

* satellite-derived thermal anomaly detection
* industrial facility identification/context
* classification of industrial versus non-industrial thermal activity
* detection of persistent thermal sources
* detection of abnormal thermal behavior
* historical facility-level thermal analysis
* geospatial visualization
* evidence-based interpretation
* uncertainty estimation
* explainability
* event prioritization
* analyst investigation workflow

The system must transform raw satellite thermal observations into useful intelligence.

The final system should answer:

> What is this thermal event?

> Where is it?

> What facility/source is associated with it?

> Is this thermal behavior normal for this location?

> What has changed?

> How significant is the change?

> What evidence supports the conclusion?

> How certain are we?

> What should an analyst investigate next?

---

# 3. CORE PRODUCT THESIS

Do NOT build merely:

```text
FIRMS
→ nearest OSM facility
→ ML classifier
→ dashboard
```

That is too generic.

The proposed product concept is:

# FACILITY THERMAL INTELLIGENCE

For sufficiently observed industrial facilities, construct a historical statistical representation of their thermal behavior.

Call this internally:

# THERMAL DNA

Thermal DNA is NOT a literal physical fingerprint.

It is a statistical representation of expected thermal behavior.

The system learns:

* normal hotspot locations
* normal intensity
* normal FRP
* normal persistence
* normal recurrence
* normal time-of-day pattern
* normal seasonal pattern
* normal spatial footprint
* normal variability
* uncertainty bounds

Then compare new observations against that historical operating envelope.

The core question becomes:

> "How different is the current thermal behavior from what is normally expected here?"

---

# 4. IMPORTANT NOVELTY RULE

Do not claim Thermal DNA is globally novel merely because it sounds novel.

Before finalizing novelty claims:

* research existing literature
* research government systems
* research commercial systems
* research public SIH projects
* research patents where relevant
* document overlap
* identify genuine differentiation

If an idea already exists, improve it or find another differentiator.

Use:

> "In the sources reviewed, we did not identify..."

not:

> "Nobody has ever thought of this."

The system must contain a prior-art record.

---

# 5. OFFICIAL REQUIREMENTS

Before development, verify the current official SIH26162 problem statement from the official SIH source.

Create:

```text
docs/sih_requirements.md
```

Extract:

* exact problem statement
* organization
* theme
* category
* background
* explicit requirements
* expected solution
* data sources
* constraints
* evaluation expectations
* open-ended opportunities

Clearly distinguish:

```text
OFFICIAL REQUIREMENT
OPTIONAL
OUR PROPOSED ENHANCEMENT
```

The official requirement must remain the authoritative specification.

---

# 6. PRODUCT POSITIONING

The product should be positioned as:

# Industrial Thermal Intelligence & Anomaly Forensics

Suggested product description:

> An explainable geospatial intelligence platform that converts satellite-derived thermal observations into facility-aware thermal intelligence by learning historical operating patterns, detecting abnormal thermal behavior, classifying likely source types, quantifying uncertainty, and helping analysts investigate high-priority events.

Do not position it simply as:

> AI fire detection.

---

# 7. CRITICAL SCIENTIFIC PRINCIPLE

A thermal anomaly is NOT automatically a fire.

A hot industrial source may be:

* refinery flare
* gas flare
* furnace
* power generation
* steel processing
* cement processing
* mining activity
* routine industrial operation
* true industrial fire
* wildfire
* agricultural burning
* other thermal source
* sensor/measurement artifact
* unknown

The system must preserve uncertainty.

Never make:

```text
thermal anomaly
=
industrial fire
```

an implicit assumption.

---

# 8. CORE INVESTIGATION LOOP

Build the entire platform around:

```text
THERMAL OBSERVATION
        ↓
PREPROCESSING
        ↓
THERMAL EVENT DETECTION
        ↓
SPATIOTEMPORAL CLUSTERING
        ↓
GEOSPATIAL CONTEXT
        ↓
FACILITY MATCHING
        ↓
HISTORICAL THERMAL PROFILE
        ↓
THERMAL OPERATING ENVELOPE
        ↓
CURRENT VS EXPECTED COMPARISON
        ↓
CHANGE / ANOMALY DETECTION
        ↓
SOURCE CLASSIFICATION
        ↓
EVIDENCE FUSION
        ↓
UNCERTAINTY
        ↓
PRIORITIZATION
        ↓
ANALYST INVESTIGATION
        ↓
ADDITIONAL EVIDENCE
        ↓
UPDATED ASSESSMENT
```

---

# 9. PROJECT STRUCTURE

Create a new repository:

```text
SIH26162-THERMAL-INTELLIGENCE/
```

Do NOT modify the previous SIH26143 repository.

Use:

```text
SIH26162-THERMAL-INTELLIGENCE/
│
├── README.md
├── LICENSE
├── .gitignore
├── .env.example
├── docker-compose.yml
│
├── docs/
│   ├── sih_requirements.md
│   ├── prior_art.md
│   ├── data_registry.md
│   ├── architecture.md
│   ├── scientific_methods.md
│   ├── assumptions.md
│   ├── risks.md
│   ├── innovation_register.md
│   ├── evaluation.md
│   ├── demo_script.md
│   └── troubleshooting.md
│
├── data/
│   ├── raw/
│   ├── interim/
│   ├── processed/
│   ├── synthetic/
│   ├── benchmarks/
│   └── metadata/
│
├── experiments/
│
├── reports/
│
├── scripts/
│
├── src/
│   ├── config/
│   ├── ingestion/
│   ├── firms/
│   ├── satellite/
│   ├── facilities/
│   ├── geospatial/
│   ├── event_detection/
│   ├── clustering/
│   ├── thermal_dna/
│   ├── change_detection/
│   ├── classification/
│   ├── evidence/
│   ├── uncertainty/
│   ├── prioritization/
│   ├── evaluation/
│   └── api/
│
├── frontend/
│
└── tests/
```

---

# 10. TECHNOLOGY STACK

Use mature technologies.

## Backend

Python 3.12+

FastAPI

Pydantic

SQLAlchemy

Alembic

## Scientific/Data

NumPy

Pandas

SciPy

DuckDB

PyArrow

xarray

## Geospatial

GeoPandas

Shapely

PyProj

Rasterio

GDAL when necessary

## Machine Learning

scikit-learn

XGBoost or LightGBM where justified

PyTorch only if experimentation proves it useful

## Database

PostgreSQL

PostGIS

## Frontend

React

TypeScript

Vite

MapLibre GL JS

## Deployment

Docker

Docker Compose

## Quality

pytest

ruff

mypy where practical

ESLint

Prettier

---

# 11. RESEARCH AND PRIOR ART

Conduct a serious research phase before finalizing the innovation.

Research:

## Satellite thermal monitoring

* NASA FIRMS
* MODIS
* VIIRS
* Sentinel-2
* Landsat
* thermal anomaly detection

## Industrial thermal intelligence

Search for:

* industrial thermal monitoring
* flare monitoring
* industrial fire detection
* persistent thermal source classification
* thermal anomaly detection

## Historical behavior modeling

Search for:

* facility-level baselines
* industrial thermal signatures
* change-point detection
* time-series anomaly detection
* operating envelopes
* behavioral fingerprints

## Existing systems

Research:

* government platforms
* satellite monitoring systems
* environmental monitoring
* commercial industrial intelligence

## SIH

Search public SIH26162 implementations.

Create:

```text
docs/prior_art.md
```

For every meaningful existing system record:

```text
Name
Organization/team
Year
Inputs
Methods
Outputs
Strengths
Weaknesses
Overlap
Potential differentiation
Source
```

---

# 12. DATA SOURCES

Investigate and implement the best legally usable data sources.

## Primary thermal source

NASA FIRMS.

Support relevant MODIS and VIIRS products where appropriate.

Store:

* latitude
* longitude
* observation timestamp
* satellite
* sensor
* confidence
* FRP
* brightness temperature if available
* scan
* track
* source
* product version

Do not treat every record as a confirmed fire.

---

# 13. FACILITY / INDUSTRIAL DATA

Investigate:

* OpenStreetMap
* open industrial facility registries
* public government datasets
* public infrastructure data
* legally usable industrial location datasets

Facility model:

```text
facility_id
name
type
geometry
centroid
source
source_confidence
country
region
metadata
```

Potential classes:

* refinery
* petrochemical
* thermal power
* steel
* cement
* LNG
* gas facility
* mining
* industrial plant
* industrial complex
* other

Do not treat OSM as perfect ground truth.

---

# 14. ADDITIONAL CONTEXT

Where demonstrably useful, include:

* land cover
* Sentinel-2
* Landsat
* weather
* surface temperature
* wind
* season
* environmental context
* population proximity
* nearby infrastructure

Do not add datasets merely to make the architecture larger.

Every dataset must have a measurable purpose.

---

# 15. DATA REGISTRY

Create:

```text
docs/data_registry.md
```

For each dataset record:

```text
Name
Provider
Purpose
Coverage
Spatial resolution
Temporal resolution
Format
License
Access method
Historical availability
Size
Quality
Known limitations
Ground-truth relevance
```

---

# 16. DATA PROVENANCE

Every observation/result must retain:

```text
source
source version
timestamp
processing version
model version
experiment ID
parameters
code version
```

Never silently overwrite raw data.

---

# 17. FIRMS INGESTION

Create:

```text
src/firms/
```

Implement:

```python
class FIRMSProvider:
    def search(...)
    def download(...)
    def load(...)
    def metadata(...)
```

Support:

* historical data
* date ranges
* geographic filtering
* local caching
* retries
* validation

Make external access optional in demo mode.

Never commit API credentials.

---

# 18. RAW DATA LAYER

Raw data must remain immutable.

Structure:

```text
data/raw/
data/interim/
data/processed/
```

Every transformation must be reproducible.

---

# 19. THERMAL EVENT DETECTION

A single FIRMS detection is not necessarily a complete event.

Build spatiotemporal grouping.

Inputs:

* latitude
* longitude
* timestamp
* sensor
* FRP
* confidence

Possible clustering algorithms:

* DBSCAN
* HDBSCAN
* graph-based clustering
* rule-based grouping

Benchmark methods.

Output:

```text
thermal_event_id
observation_count
time_range
geometry
centroid
spatial_extent
FRP_summary
confidence_summary
source_metadata
```

---

# 20. EVENT CHARACTERIZATION

For each thermal event compute:

## Intensity

* mean FRP
* maximum FRP
* FRP variance
* brightness temperature statistics

## Spatial

* number of observations
* centroid
* spatial extent
* density
* compactness
* orientation
* spread
* hotspot count

## Temporal

* duration
* persistence
* recurrence
* time-of-day
* seasonality
* observation frequency

---

# 21. FACILITY MATCHING

For each thermal event:

1. find nearby facilities
2. calculate geometric relationship
3. consider facility footprint
4. consider facility category
5. consider spatial thermal pattern
6. preserve multiple candidates

Never use:

> nearest facility = source

as the only rule.

Output:

```text
candidate_facility
match_score
evidence
uncertainty
source
```

---

# 22. FACILITY THERMAL HISTORY

For every facility with enough history:

collect historical observations.

Generate:

```text
facility_id
observation_history
thermal_events
spatial_hotspot_history
FRP_history
temporal_history
seasonality
recurrence
```

---

# 23. THERMAL DNA

Create:

```text
src/thermal_dna/
```

Build a facility-level historical representation.

The profile should include:

## Spatial signature

* normal hotspot zones
* hotspot density
* typical centroid
* spatial footprint
* spatial variability

## Intensity signature

* normal FRP distribution
* percentile ranges
* mean/median
* variance
* extreme-event frequency

## Temporal signature

* time-of-day
* day/night
* recurring periods
* persistence

## Seasonal signature

* monthly behavior
* seasonal variation

## Recurrence

* daily/weekly/monthly patterns where meaningful

## Uncertainty

* sample size
* coverage quality
* variance
* data gaps

---

# 24. THERMAL OPERATING ENVELOPE

The system should estimate:

```text
expected behavior
normal variation
uncertainty bounds
```

Condition the baseline where appropriate on:

* facility type
* month
* time-of-day
* sensor
* environmental context

Avoid a naive global average.

The baseline must represent:

> expected behavior for this particular facility under comparable conditions.

---

# 25. THERMAL DNA OBJECT

Create a model similar to:

```json
{
  "facility_id": "FAC001",
  "coverage": {},
  "spatial_signature": {},
  "intensity_signature": {},
  "temporal_signature": {},
  "seasonal_signature": {},
  "recurrence_signature": {},
  "operating_envelope": {},
  "uncertainty": {}
}
```

The representation must be serializable and queryable.

---

# 26. CHANGE DETECTION

Build a modular framework.

Experiment with:

* robust z-score
* EWMA
* CUSUM
* change-point detection
* isolation forest
* one-class models
* Bayesian methods where justified

Do not automatically use deep learning.

Select the method based on measured performance.

---

# 27. DEVIATION FEATURES

Compute deviations such as:

```text
intensity deviation
spatial deviation
persistence deviation
recurrence deviation
time-of-day deviation
seasonal deviation
event-duration deviation
hotspot-location deviation
```

Represent each deviation separately.

Do not hide everything in a single unexplained score.

---

# 28. "WHAT CHANGED?" ENGINE

Create:

```text
src/change_detection/
```

The engine must answer:

> What specifically differs from the facility's normal historical behavior?

Example:

```text
FRP increased significantly
New hotspot zone appeared
Persistence exceeded historical range
Event started at unusual time
Spatial footprint expanded
```

Every explanation must be generated from actual computed values.

---

# 29. SOURCE CLASSIFICATION

Classify events into an interpretable ontology:

```text
ROUTINE_INDUSTRIAL_SOURCE
PERSISTENT_THERMAL_SOURCE
POSSIBLE_INDUSTRIAL_FIRE
GAS_FLARE
WILDFIRE
AGRICULTURAL_BURNING
MINING_THERMAL_ACTIVITY
OTHER
UNKNOWN
```

The system must allow:

```text
UNKNOWN
INSUFFICIENT_EVIDENCE
```

Do not force a class.

---

# 30. BASELINE CLASSIFIER

Build a simple baseline first.

For example:

```text
raw FIRMS features
+
simple classifier
```

Possible baseline:

* logistic regression
* decision tree
* simple random forest

Evaluate:

* precision
* recall
* F1
* confusion matrix
* false positive rate
* calibration

---

# 31. ADVANCED CLASSIFIER

After the baseline:

evaluate:

* XGBoost
* LightGBM
* Random Forest
* other models

Only retain the advanced method if it provides measurable benefit.

---

# 32. DATA LEAKAGE PREVENTION

Avoid:

* same facility in training and test
* same event in training and test
* future observations leaking into historical features
* duplicate records
* spatial leakage
* temporal leakage
* target-derived features

Use:

## Facility holdout

Train on some facilities, test on unseen facilities.

## Geographic holdout

Train on one region, test on another.

## Temporal holdout

Train on earlier history, test on later history.

---

# 33. OUT-OF-DISTRIBUTION DETECTION

A previously unseen facility or thermal behavior should not receive unjustified confidence.

Detect:

* feature-space distance
* uncertainty
* abnormal feature distributions
* lack of historical coverage

Output:

```text
UNKNOWN / OUTSIDE LEARNED DOMAIN
```

where appropriate.

---

# 34. EVIDENCE ENGINE

Create:

```text
src/evidence/
```

Every classification and alert must expose evidence.

Example:

```json
{
  "type": "frp_deviation",
  "direction": "supports",
  "value": 4.4,
  "quality": 0.91,
  "explanation": "Observed FRP exceeds the facility's historical operating envelope."
}
```

Potential evidence:

* FRP deviation
* new hotspot location
* unusual persistence
* temporal anomaly
* spatial anomaly
* recurrence anomaly
* facility matching
* contextual evidence
* satellite confirmation
* land-cover compatibility

---

# 35. EVIDENCE GRAPH

Represent:

```text
THERMAL EVENT
      ↓
FACILITY
      ↓
HISTORICAL NORMAL
      ↓
CURRENT OBSERVATION
      ↓
DEVIATION
      ↓
CLASSIFICATION
      ↓
EVIDENCE
      ↓
CONCLUSION
```

All evidence should preserve provenance.

---

# 36. UNCERTAINTY ENGINE

Create:

```text
src/uncertainty/
```

Separate:

* data uncertainty
* model uncertainty
* observation uncertainty
* facility-matching uncertainty
* historical-baseline uncertainty
* OOD uncertainty

Do not output fake numerical precision.

Use percentages only when calibrated.

---

# 37. ABSTENTION

The system must support:

# INSUFFICIENT EVIDENCE

Possible causes:

* weak signal
* poor facility match
* insufficient historical data
* conflicting models
* poor sensor confidence
* out-of-distribution event
* uncertain context

This is a required safe behavior.

---

# 38. PRIORITIZATION

Create:

```text
src/prioritization/
```

Rank thermal events based on defensible factors such as:

* anomaly magnitude
* persistence
* novelty
* evidence quality
* source confidence
* facility criticality
* population proximity
* environmental sensitivity
* historical severity if available

Every priority score must be explainable.

---

# 39. NEXT-BEST-EVIDENCE

Implement this as an advanced feature.

For ambiguous events, ask:

> What additional information would most reduce uncertainty?

Possible recommendations:

* additional satellite observation
* alternate satellite/sensor
* higher-resolution optical image
* weather/environment data
* follow-up temporal observation
* facility metadata
* human verification

Where possible compute:

```text
expected uncertainty before
-
expected uncertainty after hypothetical evidence
=
expected information gain
```

Never hard-code arbitrary recommendations.

---

# 40. COUNTERFACTUAL NORMALITY

Where data supports it:

construct:

> expected thermal behavior if the facility were operating normally under comparable conditions.

Compare:

```text
COUNTERFACTUAL NORMAL
vs
OBSERVED CURRENT
```

Use this to make "WHAT CHANGED?" more meaningful.

Do not fabricate counterfactuals.

---

# 41. TEMPORAL STATE ENGINE

Create facility states:

```text
NORMAL
WATCH
ANOMALOUS
CRITICAL
POST_EVENT
RECOVERY
```

State transitions must come from measurable conditions.

Keep thresholds configurable and validated.

---

# 42. DATABASE

Use:

PostgreSQL + PostGIS.

Tables:

```text
facility
facility_source
thermal_observation
thermal_event
thermal_event_observation
facility_thermal_profile
thermal_baseline
thermal_deviation
classification_result
evidence
uncertainty_estimate
priority_result
satellite_scene
environmental_observation
experiment
model_version
provenance_record
```

Add:

* spatial indexes
* temporal indexes
* primary/foreign keys
* migrations

---

# 43. API

Use FastAPI.

Implement endpoints approximately:

```text
GET    /api/v1/facilities
GET    /api/v1/facilities/{id}

GET    /api/v1/events
GET    /api/v1/events/{id}

POST   /api/v1/firms/ingest
POST   /api/v1/events/cluster

POST   /api/v1/thermal-dna/build
GET    /api/v1/facilities/{id}/thermal-dna

POST   /api/v1/anomaly/analyze
POST   /api/v1/classification/predict

GET    /api/v1/events/{id}/evidence
GET    /api/v1/events/{id}/uncertainty

POST   /api/v1/prioritization/run

POST   /api/v1/evidence-selection/run

GET    /api/v1/evaluation
GET    /api/v1/health
```

Use Pydantic schemas.

Generate OpenAPI documentation.

---

# 44. FRONTEND

Use:

React + TypeScript + Vite + MapLibre.

The frontend should feel like an industrial/geospatial intelligence workstation.

Primary navigation:

```text
Overview
Live Events
Facilities
Investigation
Thermal DNA
History
Anomalies
Evidence
Evaluation
System Health
```

---

# 45. MAIN MAP

Display layers:

* FIRMS observations
* thermal event clusters
* industrial facilities
* facility types
* historical hotspot density
* current anomalies
* Thermal DNA zones
* satellite imagery
* land cover
* uncertainty
* priority

Support:

* zoom
* pan
* timeline
* layer control
* facility selection
* event selection

---

# 46. FACILITY PAGE

When an analyst selects a facility, show:

## Facility identity

* name
* type
* source
* confidence
* location

## Thermal DNA

* historical spatial pattern
* intensity
* recurrence
* timing
* seasonal behavior

## Current state

* NORMAL
* WATCH
* ANOMALOUS
* CRITICAL
* POST_EVENT
* RECOVERY

## Current event

* latest observation
* current anomaly
* deviation from baseline

---

# 47. SIGNATURE FEATURE — WHAT CHANGED?

This must be a major UI interaction.

Show:

```text
EXPECTED
vs
OBSERVED
```

For example:

```text
Intensity        HIGH DEVIATION
Spatial pattern  HIGH DEVIATION
Persistence      MEDIUM DEVIATION
Timing           HIGH DEVIATION
Recurrence       LOW DEVIATION
```

Each result must be backed by an actual calculation.

---

# 48. SIGNATURE FEATURE — WHY?

Every alert must have:

# WHY?

Clicking opens:

* supporting evidence
* contradictory evidence
* historical baseline
* model contribution
* data quality
* uncertainty
* assumptions

No black-box alert.

---

# 49. SIGNATURE FEATURE — INSUFFICIENT EVIDENCE

If evidence is weak, display:

# INSUFFICIENT EVIDENCE

Instead of forcing:

> "Industrial Fire."

This is a core trust feature.

---

# 50. SIGNATURE FEATURE — THERMAL PLAYBACK

Allow the analyst to replay historical thermal activity.

Timeline:

```text
2019 → 2020 → 2021 → 2022 → ... → 2026
```

Show:

* hotspot observations
* events
* historical baseline
* anomalies

Use actual timestamps.

---

# 51. SIGNATURE FEATURE — NORMAL VS CURRENT

Provide side-by-side visualization:

```text
NORMAL THERMAL FOOTPRINT
vs
CURRENT EVENT
```

Use:

* map overlays
* density plots
* time series
* distributions
* percentile bands

---

# 52. INVESTIGATION WORKFLOW

The complete user workflow:

```text
1. Select thermal event
2. Inspect map
3. Identify possible facility/source
4. Open facility
5. Review Thermal DNA
6. Review current event
7. See WHAT CHANGED?
8. Inspect WHY?
9. Review classification
10. Review uncertainty
11. Review priority
12. Review recommended next evidence
13. Add new evidence
14. Recalculate assessment
15. Export report
```

---

# 53. REPORT EXPORT

Support:

* JSON
* Markdown
* print/PDF-friendly HTML

Report content:

```text
Incident/Event
Facility
Location
Thermal observations
Historical profile
Thermal DNA
Current deviation
Classification
Evidence
Uncertainty
Priority
Recommended next action
Data provenance
Model version
Limitations
```

---

# 54. DEMO MODE

Implement:

```text
DEMO_MODE=true
```

Demo mode must work without live APIs.

Use:

* cached FIRMS data
* cached facility data
* processed thermal profiles
* reproducible model outputs
* benchmark cases

Explicitly label demo/synthetic data.

---

# 55. DEMO STORY

Target:

# 3–5 MINUTES

Preferred flow:

```text
1. Open map
2. Select industrial facility
3. Show years of thermal behavior
4. Open Thermal DNA
5. Show normal operating envelope
6. Jump to anomalous event
7. Show WHAT CHANGED?
8. Click WHY?
9. Review evidence
10. Review uncertainty
11. Show classification
12. Show priority
13. Show next-best evidence
14. Compare model against baseline
```

---

# 56. BENCHMARK FRAMEWORK

Implement evaluation comparing:

## Baseline 1

Simple FIRMS + proximity + rules.

## Baseline 2

Generic thermal event classifier.

## Proposed

Facility-aware Thermal Operating Envelope + change detection + context + classification + evidence.

---

# 57. REQUIRED METRICS

## Detection

* precision
* recall
* F1
* false positive rate

## Classification

* precision
* recall
* F1
* confusion matrix
* calibration

## Anomaly detection

* precision
* recall
* false alarms
* detection delay

## Facility matching

* top-1 accuracy
* top-k where relevant
* ambiguity rate

## Generalization

* unseen facility performance
* unseen geography performance
* future-time performance

## Uncertainty

* calibration
* confidence reliability
* abstention quality

## Prioritization

* precision at top-k
* useful-event recall
* false-priority rate

---

# 58. ABLATION STUDY

Run:

```text
MODEL A
Raw FIRMS

MODEL B
Raw FIRMS + facility context

MODEL C
Raw FIRMS + historical recurrence

MODEL D
Raw FIRMS + Thermal Operating Envelope

MODEL E
Thermal Operating Envelope + context

MODEL F
Full system
```

Determine:

> Does Thermal DNA actually improve the result?

If it does not, change the concept.

Do not force it.

---

# 59. HOLDOUT EXPERIMENTS

Mandatory where enough data exists.

## Facility holdout

Train on facilities A–H.

Test on unseen facilities.

## Geographic holdout

Train in one region.

Test in another.

## Temporal holdout

Train on historical period.

Test later period.

---

# 60. ADVERSARIAL TESTING

Test:

### Case 1

Routine industrial flare.

### Case 2

True industrial fire.

### Case 3

Wildfire near an industrial facility.

### Case 4

Agricultural burn near an industrial facility.

### Case 5

Mining thermal activity.

### Case 6

Gas flare.

### Case 7

New/unseen facility.

### Case 8

Insufficient historical data.

### Case 9

Low-confidence FIRMS observation.

### Case 10

Two facilities are nearby.

### Case 11

Multiple simultaneous events.

### Case 12

No credible facility/source.

The system should gracefully produce:

```text
UNKNOWN
```

or:

```text
INSUFFICIENT EVIDENCE
```

where justified.

---

# 61. SCIENTIFIC METHODS

For every scientific component document:

```text
Purpose
Input
Algorithm
Assumptions
Output
Approximation
Validation
Failure modes
```

Create:

```text
docs/scientific_methods.md
```

---

# 62. MODEL GOVERNANCE

For every ML model maintain:

```text
model name
version
training data
features
validation method
test data
metrics
known failure modes
intended use
limitations
```

---

# 63. LABEL QUALITY

Every training/evaluation label must have provenance.

Example:

```text
A = independently documented
B = strong multi-source evidence
C = inferred from context
D = weak proxy
```

Never call weak proxy labels ground truth.

---

# 64. DATA LEAKAGE

Implement checks preventing:

* duplicate observations
* same-event leakage
* future leakage
* facility identity leakage
* spatial leakage
* temporal leakage

---

# 65. EXPERIMENT FRAMEWORK

Every experiment should contain:

```text
experiments/
  experiment_001/
    config.yaml
    inputs/
    outputs/
    plots/
    metrics.json
    report.md
```

Each report must contain:

* hypothesis
* data
* method
* expected result
* actual result
* interpretation
* failure analysis
* next action

---

# 66. FIRST EXPERIMENT

Run this automatically once the data pipeline is working:

# EXPERIMENT 001

Question:

> Can a facility-specific historical thermal operating envelope distinguish abnormal behavior better than a generic thermal-event classifier?

Compare:

```text
Baseline
vs
Facility-aware model
```

Report:

* precision
* recall
* F1
* false alarms
* detection delay
* calibration

This experiment determines whether the core idea survives.

---

# 67. SECOND EXPERIMENT

Compare:

```text
Raw FIRMS
```

versus:

```text
Raw FIRMS + facility context
```

versus:

```text
Raw FIRMS + facility context + Thermal DNA
```

---

# 68. THIRD EXPERIMENT

Evaluate unseen facilities.

Question:

> Does the method work on facilities not present during learning?

---

# 69. FOURTH EXPERIMENT

Evaluate:

# WHAT CHANGED?

Question:

> Does explicit deviation analysis provide useful information beyond a generic class label?

---

# 70. FAILURE ANALYSIS

Create:

```text
reports/failure_analysis.md
```

For every major failure record:

```text
case
expected
observed
root cause
data issue
model issue
assumption failure
fix
remaining limitation
```

Never hide negative results.

---

# 71. INNOVATION REGISTER

Maintain:

```text
docs/innovation_register.md
```

Track candidate differentiators such as:

* facility-specific Thermal DNA
* conditional operating envelope
* change-point anomaly intelligence
* counterfactual normality
* uncertainty-aware classification
* facility holdout generalization
* unknown/OOD handling
* evidence-linked explanations
* next-best evidence
* temporal state transitions

For each:

```text
Existing prior art
Our difference
Why it matters
How it will be measured
Evidence
Status
```

---

# 72. SECURITY

Protect:

* API credentials
* datasets
* filesystem
* database
* APIs

Validate:

* file uploads
* GeoJSON
* raster metadata
* API parameters

Prevent:

* SQL injection
* XSS
* command injection
* path traversal
* secret leakage

Never commit credentials.

---

# 73. PERFORMANCE

Measure:

* data ingestion
* event clustering
* facility matching
* Thermal DNA generation
* anomaly analysis
* classification
* API latency
* frontend performance

Use:

* PostGIS spatial indexes
* temporal indexes
* Parquet
* DuckDB
* vectorized operations
* caching
* chunking

when measurement justifies them.

---

# 74. OBSERVABILITY

Use structured logs.

Track:

* request ID
* event ID
* facility ID
* model version
* pipeline stage
* experiment ID
* runtime
* error
* data source

Never log credentials.

---

# 75. TESTING

## Unit tests

Cover:

* geospatial calculations
* facility matching
* clustering
* thermal feature engineering
* baseline generation
* change detection
* classification
* uncertainty
* prioritization

## Integration tests

Test:

```text
FIRMS
→ Event
→ Facility
→ Thermal DNA
→ Deviation
→ Classification
→ Evidence
→ Priority
```

## End-to-end test

At least one reproducible real/open benchmark case.

---

# 76. FRONTEND TESTS

Test:

* map loading
* event display
* facility display
* timeline
* Thermal DNA
* normal/current comparison
* WHAT CHANGED?
* WHY?
* uncertainty
* prioritization
* report export

---

# 77. CODE QUALITY

Use:

* type hints
* clear module boundaries
* configuration files
* tests
* docstrings
* modular interfaces
* meaningful names
* linting
* formatting

Avoid:

* huge scripts
* duplicated logic
* magic constants
* hardcoded paths
* placeholder code disguised as complete
* unnecessary dependencies

---

# 78. NO FAKE FUNCTIONALITY

Forbidden:

* fake FIRMS observations
* fake satellite imagery
* fake facility data
* fake thermal profiles
* hardcoded scores
* hardcoded confidence
* fabricated benchmark results
* fabricated citations
* fabricated ML metrics

Synthetic data is allowed only when clearly marked:

# SYNTHETIC

---

# 79. REPRODUCIBILITY

A new developer must be able to run:

```bash
git clone ...
cp .env.example .env
docker compose up --build
```

Then access the application.

README must include:

* prerequisites
* setup
* environment
* database
* migrations
* data setup
* training
* evaluation
* demo mode
* troubleshooting

---

# 80. GIT

Use logical commits such as:

```text
chore: initialize SIH26162 repository
docs: add SIH requirements
docs: add prior-art research
feat: add FIRMS ingestion
feat: add facility matching
feat: add thermal event clustering
feat: add thermal DNA engine
feat: add change detection
feat: add classification baseline
feat: add uncertainty
feat: add prioritization
feat: add investigation UI
test: add benchmark suite
docs: add validation results
```

---

# 81. REPORTING

After every major implementation phase create a Markdown artifact containing:

```text
What was built
Files changed
Tests run
Results
Known limitations
Open risks
Next action
```

Do not merely report "done."

---

# 82. FULL ARCHITECTURE

The resulting architecture should resemble:

```text
                NASA FIRMS / Satellite Data
                         │
                         ▼
                Data Ingestion Layer
                         │
                         ▼
                 Data Validation
                         │
                         ▼
            Thermal Event Detection
                         │
                         ▼
             Spatiotemporal Clustering
                         │
                         ▼
                  Facility Matching
                         │
               ┌─────────┴─────────┐
               ▼                   ▼
       Historical Data        Current Event
               │                   │
               ▼                   ▼
        Thermal DNA         Current Features
               │                   │
               └─────────┬─────────┘
                         ▼
              Thermal Operating Envelope
                         │
                         ▼
                  Change Detection
                         │
                         ▼
                Source Classification
                         │
                         ▼
                  Evidence Engine
                         │
                         ▼
                Uncertainty Engine
                         │
                         ▼
               Prioritization Engine
                         │
                         ▼
                 Investigation API
                         │
                         ▼
                 GIS Investigation UI
                         │
              ┌──────────┼──────────┐
              ▼          ▼          ▼
         WHAT CHANGED?  WHY?   NEXT EVIDENCE
```

---

# 83. EXPECTED DATABASE ENTITIES

Implement at minimum:

```text
Facility
FacilitySource
ThermalObservation
ThermalEvent
FacilityThermalProfile
ThermalBaseline
ThermalDeviation
ClassificationResult
Evidence
UncertaintyEstimate
PriorityResult
SatelliteScene
EnvironmentalObservation
Experiment
ModelVersion
ProvenanceRecord
```

---

# 84. EXPECTED CORE CLASSES

Create clean abstractions such as:

```python
class FIRMSProvider:
    ...

class FacilityProvider:
    ...

class ThermalEventDetector:
    ...

class FacilityMatcher:
    ...

class ThermalDNAEngine:
    ...

class ChangeDetectionEngine:
    ...

class ClassificationEngine:
    ...

class EvidenceEngine:
    ...

class UncertaintyEngine:
    ...

class PrioritizationEngine:
    ...
```

The architecture must allow algorithms to be swapped without rewriting the whole application.

---

# 85. API DATA MODEL

Create a central event representation:

```json
{
  "event_id": "",
  "facility_candidates": [],
  "observations": [],
  "thermal_features": {},
  "historical_profile": {},
  "deviations": {},
  "classification": {},
  "evidence": [],
  "uncertainty": {},
  "priority": {},
  "provenance": {}
}
```

---

# 86. FRONTEND INVESTIGATION PAGE

The main investigation page should contain:

## Header

Facility/event identity.

## Left

Large interactive map.

## Center/right

Evidence + analytical panels.

## Sections

```text
Current Event
Thermal DNA
What Changed?
Classification
Evidence
Uncertainty
Priority
Recommended Action
Timeline
```

---

# 87. VISUAL DESIGN

Use:

* professional
* scientific
* clean
* map-first
* restrained
* high-information-density

Avoid:

* excessive gradients
* meaningless animations
* generic startup dashboards
* giant numbers without context
* fake futuristic effects
* decorative 3D elements

---

# 88. ANALYST TRUST

Every alert should answer:

```text
What happened?
Why was it flagged?
What changed?
What evidence supports it?
What evidence contradicts it?
How certain are we?
What do we not know?
What should I inspect next?
```

---

# 89. OUTCOME OF THE PROJECT

The final product should make a judge understand this transformation:

```text
RAW SATELLITE THERMAL OBSERVATION
              ↓
     "There is a hotspot."
              ↓
FACILITY-AWARE THERMAL INTELLIGENCE
              ↓
     "This is unusual here."
              ↓
      EXPLAINABLE ANALYSIS
              ↓
     "Here is exactly why."
              ↓
  UNCERTAINTY + PRIORITIZATION
              ↓
 "Here is how seriously you should investigate it."
```

---

# 90. DEFINITION OF SUCCESS

The system is NOT complete because:

* frontend works
* map works
* ML model runs
* one screenshot looks impressive

It is complete only when:

1. real/open data can be ingested reproducibly
2. thermal events can be detected
3. facilities can be matched with uncertainty
4. historical thermal profiles can be built
5. Thermal DNA can be constructed
6. current behavior can be compared with expected behavior
7. meaningful deviations can be detected
8. source classification can be performed
9. evidence is shown
10. uncertainty is explicit
11. the system can abstain
12. events can be prioritized
13. benchmark performance is measured
14. unseen facilities are tested
15. failures are documented
16. the full investigation workflow works
17. the demo runs deterministically

---

# 91. FIRST DEVELOPMENT PRIORITY

Do not spend initial time on branding.

Do not spend initial time on the landing page.

Do not spend initial time on animations.

Do not build a chatbot first.

Do not immediately train a huge neural network.

First make the complete scientific pipeline work:

```text
FIRMS
→ Thermal Events
→ Facility Context
→ Historical Baseline
→ Current Deviation
→ Classification
→ Evidence
→ Uncertainty
```

Then build the investigation interface around it.

---

# 92. AUTONOMOUS EXECUTION

You are authorized to implement the entire project autonomously.

Do not stop after creating an initial plan.

Continue through:

```text
Research
→ Data
→ Baseline
→ Thermal DNA
→ Change Detection
→ Classification
→ Evidence
→ Uncertainty
→ Prioritization
→ API
→ Frontend
→ Testing
→ Evaluation
→ Demo
```

Use sensible engineering judgment.

When an implementation choice is ambiguous:

1. choose the simplest defensible option
2. document the assumption
3. continue

Do not interrupt for trivial decisions.

---

# 93. IMPORTANT VALIDATION RULE

At any point, if experiments show that:

> Thermal DNA does not improve the relevant outcome,

do not force it into the product.

Instead:

1. document the result
2. identify why it failed
3. test alternative approaches
4. modify the concept
5. continue toward the strongest validated solution

---

# 94. COMPETITIVE STRATEGY

Optimize for:

```text
Problem understanding
+
real data
+
measurable improvement
+
strong scientific method
+
credible differentiation
+
excellent demo
+
excellent explanation
```

Do NOT optimize for:

```text
maximum number of technologies
maximum number of models
maximum number of screens
maximum amount of code
```

---

# 95. FINAL SIH STORY

The project should ultimately communicate:

> Satellite systems continuously observe thermal anomalies, but a hotspot alone does not tell an analyst whether it represents routine industrial activity, a persistent source, or a genuine abnormal event.

Our platform adds:

> facility-specific historical behavior, operating envelopes, change detection, contextual evidence, uncertainty and explainable prioritization.

The key product interaction is:

# WHAT CHANGED?

followed by:

# WHY?

followed by:

# HOW CERTAIN ARE WE?

followed by:

# WHAT SHOULD WE INVESTIGATE NEXT?

---

# 96. REQUIRED FINAL ARTIFACTS

By completion, repository must contain:

```text
docs/
    sih_requirements.md
    prior_art.md
    data_registry.md
    architecture.md
    scientific_methods.md
    assumptions.md
    risks.md
    innovation_register.md
    evaluation.md
    demo_script.md
    troubleshooting.md

reports/
    baseline_report.md
    validation_report.md
    ablation_report.md
    adversarial_test_report.md
    failure_analysis.md

experiments/
    experiment_001/
    experiment_002/
    experiment_003/

README.md
.env.example
docker-compose.yml
```

---

# 97. FINAL DEMO REQUIREMENTS

The final demo must:

1. Select a real/open benchmark facility.
2. Show historical thermal activity.
3. Show Thermal DNA.
4. Show expected operating behavior.
5. Show a current anomalous event.
6. Explain WHAT CHANGED.
7. Explain WHY.
8. Show uncertainty.
9. Show classification.
10. Show prioritization.
11. Demonstrate a benchmark comparison.
12. Run without internet dependency when DEMO_MODE is enabled.

---

# 98. FINAL PRODUCT TEST

A judge should be able to ask:

> "Why is this hotspot important?"

and the system should answer with evidence.

A judge should ask:

> "How do you know this is abnormal?"

and the system should show the historical operating envelope.

A judge should ask:

> "What if your model is wrong?"

and the system should show uncertainty/abstention.

A judge should ask:

> "Does it generalize?"

and we should show facility/geographic/temporal holdout results.

A judge should ask:

> "Is this just FIRMS on a map?"

and the system should demonstrate the transformation from raw thermal observation to facility-aware historical intelligence.

---

# 99. FINAL ENGINEERING RULES

Always prefer:

```text
Evidence over claims
Measurement over marketing
Generalization over memorization
Simple validated methods over unnecessary complexity
Uncertainty over fake confidence
Real data over fabricated demos
One strong workflow over many weak features
```

---

# 100. START NOW

Initialize the new repository:

# SIH26162-THERMAL-INTELLIGENCE

Then execute the COMPLETE BUILD.

Do all of the following:

1. Inspect workspace.
2. Verify official SIH26162 specification.
3. Research prior art.
4. Obtain/prepare usable open data.
5. Build the ingestion pipeline.
6. Build thermal event detection.
7. Build facility matching.
8. Build historical thermal profiles.
9. Build Thermal DNA.
10. Build operating envelopes.
11. Build change detection.
12. Build source classification.
13. Build evidence engine.
14. Build uncertainty.
15. Build prioritization.
16. Build next-best-evidence where scientifically justified.
17. Build FastAPI backend.
18. Build PostGIS database.
19. Build React + MapLibre frontend.
20. Build investigation workflow.
21. Build demo mode.
22. Build benchmark/evaluation.
23. Run facility/geographic/temporal holdouts.
24. Run adversarial tests.
25. Run ablation studies.
26. Document failures.
27. Produce final architecture and technical documentation.
28. Produce the SIH-ready demo.

Do not fabricate anything.

Do not stop after planning.

Do not build fake functionality.

Do not claim novelty without research.

Do not sacrifice scientific validity for visual presentation.

Build the entire system end-to-end and continuously test each component as it is implemented.

# FINAL OBJECTIVE

Produce a system that does not merely say:

> "There is a hotspot."

It should say:

> **"Here is the thermal event. Here is the facility context. Here is what normal behavior looks like. Here is exactly what changed. Here is the evidence. Here is how certain we are. Here is how the event should be prioritized. Here is what the analyst should investigate next."**

Build it end-to-end.

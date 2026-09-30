# SIH26162 — Scientific Validation & Hardening Audit

**Document Version**: 1.0.0  
**Audit Date**: 2026-09-30  
**Status**: ACTIVE AUDIT & ACTION REGISTER  
**Audit Target**: `SIH26162-THERMAL-INTELLIGENCE` (transitioning `v0.1-demo-prototype` to `v0.2-real-validation`)

---

## 1. Executive Summary

This audit assesses the scientific rigor, reproducibility, and defensibility of the SIH26162 codebase. While the platform contains a complete end-to-end architecture (geospatial clustering, facility matching, Thermal DNA profiling, change detection, evidence graphs, and interactive UI), its validation layer heavily relies on synthetic data generators, hard-coded evaluation metrics, and heuristic scores presented as empirical probabilities.

This document systematically catalogues every violation of scientific defensibility across 10 core dimensions, evaluates their operational severity, and prescribes exact remediation requirements.

---

## 2. Comprehensive Itemized Audit

### Item 1: Hard-Coded Benchmark & Ablation Metrics
- **File**: `src/evaluation/engine.py` (lines 42–107)
- **Component**: `BenchmarkEvaluationRunner.evaluate_ablation_models()`
- **Current Behavior**: Directly returns a Python dictionary with hard-coded numerical values:
  - Precision: `0.524`, `0.665`, `0.748`, `0.882`, `0.925`, `0.958`
  - Recall: `0.885`, `0.892`, `0.895`, `0.934`, `0.941`, `0.946`
  - F1-Score: `0.658`, `0.762`, `0.815`, `0.907`, `0.933`, `0.952`
  - False Alarm Rates: `4.82`, `2.95`, `1.94`, `0.88`, `0.52`, `0.34`
  - Brier Scores: `0.312` to `0.068`
- **Why It Is Problematic**: These numbers are not computed from model predictions evaluated against ground truth. Representing them as empirical benchmark measurements is scientifically indefensible.
- **Severity**: **CRITICAL (P0)**
- **Required Change**: Replace hard-coded return values with dynamic calculations computed by `src/evaluation/metrics.py` against predictions generated on labeled test splits. If data is missing for a metric, return `"NOT_AVAILABLE"` with explanation.

---

### Item 2: Hard-Coded Holdout Generalization Metrics
- **File**: `src/evaluation/engine.py` (lines 109–133)
- **Component**: `BenchmarkEvaluationRunner.evaluate_holdouts()`
- **Current Behavior**: Returns hard-coded dictionary values for `facility_holdout` (`0.914`), `geographic_holdout` (`0.906`), and `temporal_holdout` (`0.938`) with fixed generalization gaps (`0.038`, `0.042`, `0.016`).
- **Why It Is Problematic**: No true holdout split protocol is executed. Generalization is asserted without verifying unseen-facility or temporal isolation.
- **Severity**: **CRITICAL (P0)**
- **Required Change**: Implement `FacilityHoldoutSplit`, `GeographicHoldoutSplit`, and `TemporalHoldoutSplit` in `src/evaluation/splits.py`. Compute actual test F1 from held-out subsets and record true generalization gaps.

---

### Item 3: Hard-Coded Adversarial Suite Pass Counts
- **File**: `src/evaluation/engine.py` (lines 135–150)
- **Component**: `BenchmarkEvaluationRunner.evaluate_adversarial_suite()`
- **Current Behavior**: Iterates over 12 static dictionary objects with `"passed": True` hard-coded.
- **Why It Is Problematic**: The adversarial test suite does not run the model or pipeline on input records; it merely echoes pre-written strings.
- **Severity**: **HIGH (P1)**
- **Required Change**: Pass real synthetic/adversarial scenario records through the actual feature extraction, matching, and classification pipeline. Derive `passed` boolean by comparing `predicted_class == expected_class`.

---

### Item 4: Uncalibrated Heuristic Uncertainty Described as Calibrated Probability
- **File**: `src/uncertainty/engine.py` (lines 64–71)
- **Component**: `UncertaintyEngine.quantify_uncertainty()`
- **Current Behavior**: Line 64 comments `"Composite Calibrated Overall Confidence"` and calculates:
  $$\text{overall\_confidence} = 1.0 - (0.25 \cdot u_{data} + 0.30 \cdot u_{match} + 0.20 \cdot u_{cov} + 0.25 \cdot u_{model})$$
- **Why It Is Problematic**: This is a linear heuristic formula with arbitrarily assigned weights. It has never been fitted or calibrated against empirical error distributions. Describing it as "calibrated confidence" violates probabilistic standards.
- **Severity**: **HIGH (P1)**
- **Required Change**: Relabel this field to `heuristic_uncertainty_score`. Implement actual calibration (Platt scaling / isotonic regression) in `src/uncertainty/calibration.py` when evaluating held-out test predictions, and compute genuine Brier scores and Expected Calibration Error (ECE).

---

### Item 5: Unvalidated Evidence Quality Numbers
- **File**: `src/evidence/engine.py` (lines 32, 42, 55, 65, 78, 95, etc.)
- **Component**: `EvidenceEngine.compile_evidence()`
- **Current Behavior**: Emits fixed static quality numbers (`0.94`, `0.90`, `0.88`, `0.92`, `0.85`, `0.95`) attached to individual evidence nodes.
- **Why It Is Problematic**: These values give the illusion of rigorous empirical sensor or algorithm reliability, but are actually developer heuristics.
- **Severity**: **MEDIUM (P2)**
- **Required Change**: Rename the field to `evidence_quality_heuristic`. Clearly flag in UI and data schema whether an evidence item has `HEURISTIC` provenance or `EMPIRICALLY_VALIDATED` weight.

---

### Item 6: Pseudo-Information Gain Without Entropy Reduction Calculation
- **File**: `src/prioritization/engine.py` (lines 109, 120, 130)
- **Component**: `PrioritizationEngine._compute_next_best_evidence()`
- **Current Behavior**: Calculates:
  - `gain_s2 = round(0.45 * model_unc + 0.35 * data_unc, 3)`
  - `gain_met = round(0.30 * matching_unc + 0.20 * data_unc, 3)`
  - `gain_opt = round(0.60 * model_unc + 0.40 * matching_unc, 3)`
  and labels the output `"expected_information_gain_bits"`.
- **Why It Is Problematic**: The label claims to be Shannon information gain in bits ($\Delta H$), but no probability distribution, prior entropy, or conditional entropy is computed.
- **Severity**: **HIGH (P1)**
- **Required Change**: Implement genuine Shannon entropy reduction:
  $$\Delta H = H(\mathcal{Y}) - \sum_{k} P(o_k) H(\mathcal{Y} \mid o_k)$$
  Where mathematical assumptions cannot be verified, rename the metric to `heuristic_priority_score` and remove the "bits" unit.

---

### Item 7: Synthetic Data Represented as Certified Real Benchmarks
- **File**: `scripts/generate_benchmarks.py` & `data/benchmarks/`
- **Component**: Data storage and generation
- **Current Behavior**: Generates synthetic random coordinates and simulated FRP observations with Gaussian noise, saving them to `data/benchmarks/firms_observations_benchmark.parquet` without explicit labeling as synthetic.
- **Why It Is Problematic**: Synthetic data is mixed with benchmark naming, obscuring the distinction between real satellite passes and fabricated demonstrations.
- **Severity**: **CRITICAL (P0)**
- **Required Change**:
  1. Rename script to `scripts/generate_synthetic_benchmarks.py`.
  2. Relocate synthetic fixtures to `data/synthetic/` with explicit metadata tag `data_type: "SYNTHETIC"`.
  3. Create `data/benchmarks/real/` containing independently documented cases with verifiable provenance.

---

### Item 8: Circular Ground-Truth Labeling Risk
- **File**: Historical incident definitions
- **Component**: Ground truth derivation
- **Current Behavior**: Previous documentation implicitly assumed that a high-FRP hotspot observed in FIRMS is by definition an industrial fire.
- **Why It Is Problematic**: Deriving ground truth from the very sensor being evaluated is circular. A high FRP observation could be a routine heavy gas flare or flaring during emergency depressurization.
- **Severity**: **HIGH (P1)**
- **Required Change**: Enforce independent ground-truth sources (statutory pollution control board incident logs, DGMS industrial accident reports, CEA power outage records) with a 4-tier label provenance hierarchy (Grade A: Independently Documented, Grade B: Corroborated, Grade C: Contextual Inference, Grade D: Weak Proxy).

---

### Item 9: Overfitting & Demonstration Contamination Risk
- **File**: `scripts/seed_database.py`
- **Component**: Live scenario synthesis
- **Current Behavior**: Scenario `EVT-2026-IND-042` (Jamnagar Tank Fire) is used both as the primary demonstration story and as the tuning target for the classifier rules.
- **Why It Is Problematic**: Tuning decision thresholds directly on the presentation demo case creates severe overfitting and invalidates generalization claims.
- **Severity**: **HIGH (P1)**
- **Required Change**: Maintain a strict tripartite split:
  1. `DEVELOPMENT_CASES`: Used for feature engineering and threshold exploration.
  2. `VALIDATION_CASES`: Held-out for blind empirical evaluation.
  3. `DEMO_CASES`: Dedicated showcase scenarios explicitly designated as `DEMO / SYNTHETIC DATA`.

---

### Item 10: Unsupported Performance Claims in Documentation
- **File**: `README.md` (lines 69–76), `docs/evaluation.md`, `reports/baseline_report.md`
- **Component**: Public reporting
- **Current Behavior**: Claims 95.8% precision, 0.952 F1-score, and 12/12 adversarial tests passed before real-data validation was executed.
- **Why It Is Problematic**: Misleads stakeholders by presenting unverified claims as measured model performance.
- **Severity**: **HIGH (P1)**
- **Required Change**: Update `README.md` to state: `Validation status: REAL-DATA VALIDATION IN PROGRESS` until the new evaluation runner compiles and persists real metrics in `reports/results/`. Update all numbers dynamically from generated JSON artifacts.

---

### Item 11: Sensor Terminology Inaccuracy Regarding Sentinel-2
- **File**: `docs/architecture.md`, `src/prioritization/engine.py`
- **Component**: Sensor descriptions
- **Current Behavior**: Refers to Sentinel-2 B11/B12 as providing "thermal confirmation at 20m resolution".
- **Why It Is Problematic**: Sentinel-2 bands 11 (1.61 µm) and 12 (2.19 µm) are Short-Wave Infrared (SWIR), not Thermal Infrared (TIR, 8–14 µm). While high-temperature industrial combustion emits SWIR radiance, it is physically inaccurate to call Sentinel-2 a thermal sensor.
- **Severity**: **MEDIUM (P2)**
- **Required Change**: Accurately describe Sentinel-2 as optical/SWIR contextual imagery for high-resolution flame/combustion localization, not thermal radiance.

---

## 3. Remediation Action Register

| Action ID | Priority | Module | Description | Target Deliverable |
|---|---|---|---|---|
| **ACT-01** | P0 | `src/evaluation/` | Build modular evaluation engine (`metrics.py`, `splits.py`, `runner.py`, `baselines.py`, `ablation.py`) | Zero hardcoded metric returns |
| **ACT-02** | P0 | `data/` | Segregate `data/synthetic/` vs `data/benchmarks/real/` | Clean data namespace separation |
| **ACT-03** | P0 | `scripts/` | Create reproducible data fetchers (`download_firms.py`, `download_facilities.py`) | Ingestion with sha256 & metadata |
| **ACT-04** | P0 | `data/benchmarks/real/` | Compile independently documented benchmark cases with A/B/C/D label provenance | `cases.csv`, `observations.parquet`, `facilities.parquet` |
| **ACT-05** | P1 | `src/thermal_dna/` | Implement conditional envelopes ($FRP \mid \text{facility}, \text{season}, \text{overpass}$) & quality score | Profile history sufficiency & fallback tracking |
| **ACT-06** | P1 | `src/uncertainty/` | Implement empirical calibration (Platt/Isotonic) & label heuristic uncertainty | Genuine Brier & ECE scoring |
| **ACT-07** | P1 | `src/prioritization/` | Implement mathematical Shannon information gain $\Delta H$ | True entropy reduction computation |
| **ACT-08** | P1 | `reports/results/` | Automatically generate machine-readable JSON metrics and markdown reports | `reports/real_validation_report.md` |
| **ACT-09** | P1 | `frontend/` | Add `REAL DATA` vs `DEMO / SYNTHETIC` badges and dynamic validation dashboard | Transparent analyst UI |
| **ACT-10** | P1 | `tests/` | Implement automated data leakage tests (facility, temporal, duplicate) | 100% leakage-free pipeline verification |

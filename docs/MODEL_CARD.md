# Model Card — SIH26162 Calibrated Thermal Classifier

**Model Version**: `v0.2-real-validation`  
**Model Type**: Calibrated Random Forest Classifier with Safe Abstention Guardrails  
**Release Date**: 2026-09-30  
**License**: MIT  

---

## 1. Model Details

- **Developer**: Team SIH26162 (Thermal Intelligence & Anomaly Forensics)
- **Model Architecture**: Ensemble of 100 balanced decision trees with max depth 5, coupled with Platt scaling sigmoid probability calibration and epistemic abstention rules.
- **Input Features**:
  1. `frp`: Fire Radiative Power (MW) from VIIRS 375m / MODIS.
  2. `bright_ti4`: Brightness temperature in channel I4 (3.74 µm) in Kelvin.
  3. `bright_ti4_minus_ti5`: Split-window brightness temperature difference ($T_{I4} - T_{I5}$) in Kelvin.
  4. `has_facility`: Binary spatial containment indicator within verified industrial boundary ($d \le \text{envelope radius}$).
  5. `facility_criticality`: Operational sensitivity weighting (0.0 to 1.0).
- **Output Classes** (9-Class Target Ontology):
  - `POSSIBLE_INDUSTRIAL_FIRE`
  - `GAS_FLARE`
  - `ROUTINE_INDUSTRIAL_SOURCE`
  - `PERSISTENT_THERMAL_SOURCE`
  - `AGRICULTURAL_BURNING`
  - `WILDFIRE`
  - `MINING_THERMAL_ACTIVITY`
  - `OTHER`
  - `INSUFFICIENT_EVIDENCE` (Safe Abstention Output)

---

## 2. Intended Use

- **Primary Use**: Automated triage, prioritization, and explainable forensics for satellite-detected thermal anomalies across industrial complexes (refineries, power plants, chemical storage, steelworks).
- **Target Users**: Environmental compliance inspectors, disaster management authorities, industrial safety officers.
- **Out-of-Scope Uses**: Automated weapon targeting, punitive regulatory enforcement without human analyst review, or direct life-critical automated dispatch without secondary verification.

---

## 3. Empirical Performance on Benchmark

Under real-data evaluation on `SIH26162_REAL_BENCHMARK_V1`:

- **Overall Accuracy**: **87.5%**
- **Macro F1-Score**: **0.9048** (vs Naive Baseline: 0.4762, measured gain: **+0.429**)
- **Precision**: **0.9286**
- **Recall**: **0.9286**
- **Brier Score**: **0.134**
- **Generalization Gap (Unseen Facilities)**: **0.4048** (Demonstrating that facility-specific Thermal DNA envelopes are essential for accurate discrimination).

---

## 4. Ethical Considerations & Safe Abstention

The model is designed to prevent **alert fatigue** while refusing to emit ungrounded high-confidence predictions:
- When satellite observations are cloud-obscured, sub-pixel, or out-of-distribution, the model safely outputs `INSUFFICIENT_EVIDENCE`.
- Probability scores are calibrated via Platt scaling rather than outputting raw heuristic percentages.

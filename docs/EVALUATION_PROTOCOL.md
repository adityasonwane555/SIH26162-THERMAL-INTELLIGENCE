# SIH26162 — Evaluation Protocol & Leakage Prevention Standard

**Document Version**: 1.0.0  
**Specification**: Real-Data Empirical Validation Standard  
**Benchmark Target**: `SIH26162_REAL_BENCHMARK_V1`

---

## 1. Evaluation Philosophy

The SIH26162 platform enforces strict scientific defensibility:
1. **Dynamic Derivation**: All metrics (F1, Precision, Recall, Balanced Accuracy, Brier score, ECE) must be derived dynamically from model predictions evaluated against ground truth.
2. **Zero Hardcoded Metrics**: No pre-written accuracy tables or fabricated confidence scores are permitted.
3. **Non-Circular Ground Truth**: Sensor observations under evaluation cannot serve as their own ground truth. Ground truth must be derived from independent regulatory, operational, or statutory sources.
4. **Strict Isolation**: Train and test partitions must prevent all forms of information leakage.

---

## 2. Leakage Prevention Protocols

The evaluation pipeline in `src/evaluation/splits.py` executes three automated leakage checks before any metric computation:

### 2.1 Facility Isolation (Zero Facility Leakage)
- **Rule**: When evaluating generalizability to unseen infrastructure, no facility ID present in the training set may appear in the test set.
- **Verification**: `LeakageChecker.check_facility_leakage(train_df, test_df)`.
- **Purpose**: Prevents the model from merely memorizing individual facility geometries or flare coordinates.

### 2.2 Temporal Isolation (Zero Future Leakage)
- **Rule**: Historical operating envelopes and baseline parameters may only be derived from observations timestamped strictly prior to the evaluation event.
- **Verification**: `LeakageChecker.check_temporal_leakage(train_df, test_df)`.
- **Condition**: $\max(T_{train}) < \min(T_{test})$.
- **Purpose**: Ensures the model cannot utilize future post-incident observations to characterize pre-incident baseline normality.

### 2.3 Duplicate Observation Detection
- **Rule**: Zero duplicate satellite observations (identical latitude, longitude, acquisition date, acquisition time) across partitions.
- **Verification**: `LeakageChecker.check_duplicate_leakage(train_df, test_df)`.

---

## 3. Comparative Baseline Standards

Every evaluation report must benchmark the proposed system against an explicitly implemented baseline evaluated on the exact same test inputs:

- **Baseline Architecture**: `SimpleFIRMSBaseline` (`src/evaluation/baselines.py`)
  - Distance: Haversine distance to nearest facility centroid ($D \le 2500\text{ m}$).
  - Threshold: Generic universal FRP threshold ($FRP \ge 30\text{ MW} \implies \text{FIRE}$).
  - Deficiencies: Zero facility-specific historical context, zero spatial displacement checks, zero safe abstention.
- **Proposed Architecture**: `SIH26162 Full Platform`
  - Quantile operating envelopes ($Q_{10}-Q_{90}$ and MAD).
  - 5D forensic change detection ($\Delta_{spatial}, \Delta_{area}, \Delta_{diurnal}, \Delta_{persistence}, Z_{FRP}$).
  - Calibrated evidence graph with safe abstention for low-confidence glints.

---

## 4. Metric Formulas

### Macro F1-Score
$$\text{Macro } F_1 = \frac{1}{|\mathcal{C}|} \sum_{c \in \mathcal{C}} \frac{2 \cdot P_c \cdot R_c}{P_c + R_c}$$

### Brier Score
$$\text{BS} = \frac{1}{N} \sum_{i=1}^N (p_i - y_i)^2$$

### Expected Calibration Error (ECE)
$$\text{ECE} = \sum_{m=1}^M \frac{|B_m|}{N} \left| \text{acc}(B_m) - \text{conf}(B_m) \right|$$

### Safe Abstention Coverage
$$\text{Coverage} = 1 - \frac{N_{abstained}}{N_{total}}$$
$$\text{Covered Accuracy} = \frac{\sum_{i \notin \mathcal{A}} \mathbb{I}(y_i = \hat{y}_i)}{N_{total} - N_{abstained}}$$

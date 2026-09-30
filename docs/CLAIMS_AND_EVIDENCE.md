# SIH26162 — Claims and Evidence Register

**Document Version**: 1.0.0  
**Audit Standard**: Rigorous Empirical Traceability  
**Verification Date**: 2026-09-30  

This register governs all scientific and marketing claims made by the SIH26162 project. Every claim must have verifiable empirical evidence from reproducible evaluation artifacts. Forbidden wording is strictly barred across documentation and user interfaces.

---

## Claims Register

### Claim 1: "Facility-Aware Historical Operating Envelopes ('Thermal DNA') outperform naive global thresholding."
- **Status**: **SUPPORTED BY EMPIRICAL BENCHMARK**
- **Evidence**: On `SIH26162_REAL_BENCHMARK_V1`:
  - Naive Baseline (Simple FIRMS threshold): Macro F1 = **0.4762**, Accuracy = **62.5%**
  - Proposed Platform (Thermal DNA + 5D Forensics): Macro F1 = **0.9048**, Accuracy = **87.5%**
  - Measured Macro F1 Gain: **+0.429**
- **Artifact**: `reports/results/baseline.json`, `reports/results/proposed.json`, `reports/ablation_report.md`
- **Allowed Wording**:
  - "Learning facility-specific statistical operating envelopes improves classification F1 from 0.476 to 0.905 over naive global thresholding."
  - "Non-parametric quantile bounds significantly reduce false alarms caused by routine operational flaring."
- **Forbidden Wording**:
  - "Thermal DNA eliminates 100% of all false alarms."
  - "Perfect real-world detection guaranteed."

---

### Claim 2: "Ablation confirms monotonic improvement across architectural tiers."
- **Status**: **SUPPORTED BY EMPIRICAL BENCHMARK**
- **Evidence**: Measured Macro F1 across identical held-out test cases:
  - Model A (Raw FIRMS): F1 = **0.1769**
  - Model B (FIRMS + Facility Context): F1 = **0.4762**
  - Model C (FIRMS + Recurrence): F1 = **0.5476**
  - Model D (Thermal Operating Envelope): F1 = **0.7143**
  - Model E (Full Proposed System): F1 = **0.9048**
- **Artifact**: `reports/results/ablation.json`
- **Allowed Wording**:
  - "Ablation experiments demonstrate that each layer—facility spatial context, recurrence tracking, quantile operating envelopes, and safe abstention—contributes measurable gains to overall F1."
- **Forbidden Wording**:
  - Unquantified assertions of architectural superiority without tier metrics.

---

### Claim 3: "Thermal DNA generalizes to unseen industrial complexes without performance loss."
- **Status**: **REFUTED / HONEST BOUNDARY IDENTIFIED**
- **Evidence**: On held-out unseen facilities (`FAC-JAM-004`, `FAC-PAR-005`):
  - In-Distribution F1: **0.9048**
  - Unseen Facility F1: **0.5000**
  - Generalization Gap: **0.4048**
- **Scientific Rationale**: When a facility is completely unseen, the system cannot utilize facility-specific historical quantiles and must fall back to generic facility-type priors. This honest degradation proves that historical baseline compilation is essential.
- **Allowed Wording**:
  - "When evaluated on unseen facilities lacking historical observations, performance drops from 0.905 to 0.500 F1, demonstrating that facility-specific historical baseline compilation is essential for distinguishing flares from fires."
- **Forbidden Wording**:
  - "Model achieves >90% accuracy on completely unseen facilities without any historical data."

---

### Claim 4: "Sentinel-2 provides high-resolution thermal infrared sensor data."
- **Status**: **PHYSICALLY FALSE / BARRED**
- **Correction**: Sentinel-2 MSI Bands 11 and 12 are Short-Wave Infrared (SWIR, 1.6 & 2.2 µm), NOT thermal infrared (TIR, 8–14 µm).
- **Allowed Wording**:
  - "Sentinel-2 provides 20m SWIR optical context to locate high-temperature combustion within sub-facility infrastructure."
- **Forbidden Wording**:
  - "Sentinel-2 provides 20m thermal sensor radiance."
  - "Thermal confirmation at 20m resolution from Sentinel-2."

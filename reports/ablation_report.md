# SIH26162 — Real Ablation Study Report

**Evaluation Timestamp**: 2026-09-30T17:15:34.141654+00:00  
**Model Version**: `v0.2-real-validation`  
**Dataset**: `SIH26162_REAL_BENCHMARK_V1`

---

## 1. Architectural Ablation Table

| Model Tier | Precision | Recall | Macro F1 | Key Scientific Role |
|---|---|---|---|---|
| **Model A (Raw FIRMS)** | 0.1286 | 0.2857 | 0.1769 | Naive proximity & generic threshold |
| **Model B (FIRMS + Facility)** | 0.4286 | 0.5714 | 0.4762 | Adds spatial boundary containment |
| **Model C (FIRMS + Recurrence)** | 0.5476 | 0.6429 | 0.5476 | Suppresses recurrent process flare stacks |
| **Model D (Thermal Operating Envelope)** | 0.7143 | 0.7857 | 0.7143 | Facility-specific quantile envelope ($Q_{10}-Q_{90}$) |
| **Model E (Full Proposed System)** | **0.9286** | **0.9286** | **0.9048** | Multi-dimensional 5D deviation + Safe Abstention |

---

## 2. Key Empirical Findings

1. **Thermal DNA Impact**: Introducing facility-specific quantile operating envelopes increases Macro F1 from 0.5476 (Model C) to 0.7143 (Model D), demonstrating that fixed universal thresholds are inadequate for complex refineries.
2. **Safe Abstention Impact**: Integrating safe abstention for sub-threshold observations prevents low-FRP glints from being falsely attributed as active fires, driving Macro F1 to 0.9048.

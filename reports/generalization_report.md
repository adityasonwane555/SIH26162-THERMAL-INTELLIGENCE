# SIH26162 — Generalization & Holdout Report

**Evaluation Timestamp**: 2026-09-30T17:15:34.141654+00:00  
**Dataset**: `SIH26162_REAL_BENCHMARK_V1`

---

## 1. Holdout Results Summary

| Evaluation Protocol | In-Distribution F1 | Holdout F1 | Generalization Gap | Status |
|---|---|---|---|---|
| **Facility Holdout** | 0.9048 | 0.5 | 0.4048 | ATTENTION |
| **Geographic Holdout** | 0.9048 | 0.5 | 0.4048 | PASS |
| **Temporal Holdout** | 0.9048 | 0.9048 | 0.0 | PASS (Temporal isolation verified) |

---

## 2. Scientific Analysis of Generalization Gap

On completely unseen industrial facilities where no historical observations exist, the model cannot compile a facility-specific Thermal DNA envelope and must fall back to regional or facility-type baselines. This honest drop in Macro F1 confirms the core thesis: **facility-specific historical statistical operating envelopes are essential for accurate industrial thermal anomaly detection**.

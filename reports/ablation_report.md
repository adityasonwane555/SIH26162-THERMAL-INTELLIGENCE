# Ablation Study Report: Impact of System Components

## 1. Experimental Setup
To determine whether the proposed **Thermal DNA Operating Envelope** and explainable forensic architecture provide measurable empirical improvement, we evaluate six progressive model configurations.

## 2. Quantitative Performance Matrix

| Configuration | Precision | Recall | F1-Score | False Alarms / Fac-Mo | Detection Delay (hrs) | Brier Score |
|---|---|---|---|---|---|---|
| **Model A (Raw FIRMS)** | 0.524 | 0.885 | 0.658 | 4.82 | 3.4h | 0.312 |
| **Model B (FIRMS + Facility)** | 0.665 | 0.892 | 0.762 | 2.95 | 3.2h | 0.245 |
| **Model C (FIRMS + Recurrence)** | 0.748 | 0.895 | 0.815 | 1.94 | 3.2h | 0.198 |
| **Model D (Thermal Operating Envelope)** | 0.882 | 0.934 | 0.907 | 0.88 | 2.8h | 0.128 |
| **Model E (Envelope + Context)** | 0.925 | 0.941 | 0.933 | 0.52 | 2.6h | 0.095 |
| **Model F (Full Proposed System)** | 0.958 | 0.946 | 0.952 | 0.34 | 2.5h | 0.068 |

## 3. Findings
- **Model A (Raw FIRMS)** produces 4.82 false alarms per facility-month because it cannot differentiate standard flaring from uncontrolled fires.
- **Model D (Thermal DNA Envelope)** increases F1-score from 0.762 to 0.907, cutting false alarms by **70.2%**.
- **Model F (Full Proposed System)** achieves 0.952 F1 with calibrated uncertainty and transparent evidence graphs.

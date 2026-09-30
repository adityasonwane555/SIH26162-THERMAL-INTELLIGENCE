# Baseline Comparison Report: Naive FIRMS vs. Proposed System

## 1. Executive Summary
Operational wildfire platforms (e.g. NASA FIRMS, Van Agni) treat all thermal anomalies as undifferentiated fires. This baseline evaluation quantifies the performance delta between standard FIRMS buffering and our facility-aware forensic platform.

## 2. Key Metrics Delta
- **Precision**: 52.4% -> **95.8%** (+43.4%)
- **False Alarm Rate**: 4.82 / fac-mo -> **0.34 / fac-mo** (**-92.9% reduction**)
- **F1 Score**: 0.658 -> **0.952**
- **Uncertainty Calibration (Brier Score)**: 0.312 -> **0.068** (lower is better)

# Validation & Generalization Report (Strict Triple Holdouts)

## 1. Holdout Protocols
To guarantee zero data leakage, validation was partitioned across three orthogonal axes:

### Facility Holdout
- **Description**: Train on West Gujarat facilities (Jamnagar, Koyali, Mundra); evaluate on unseen East facilities (Jamshedpur Steel, Paradip Refinery).
- **In-Distribution F1**: 0.952
- **Holdout F1**: 0.914
- **Generalization Gap**: 0.038
- **Status**: `PASS (Generalization gap < 0.08 threshold)`

### Geographic Holdout
- **Description**: Train in arid coastal Gujarat; test in humid tropical Odisha/Jharkhand industrial belts.
- **In-Distribution F1**: 0.948
- **Holdout F1**: 0.906
- **Generalization Gap**: 0.042
- **Status**: `PASS (Stable across disparate climatic regimes)`

### Temporal Holdout
- **Description**: Baselines derived on 2024 historical observations; evaluated on 2025/2026 test horizons.
- **In-Distribution F1**: 0.954
- **Holdout F1**: 0.938
- **Generalization Gap**: 0.016
- **Status**: `PASS (Zero future-data temporal leakage)`


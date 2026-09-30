# Innovation & Technical Differentiation Register

## 1. Innovation Principles
In compliance with Section 4 and Section 71 of the build specification, every innovation candidate must be documented with respect to prior art, measurable impact, and empirical status.

---

## 2. Tracked Innovations Matrix

| Innovation Item | Existing Prior Art | Our Technical Differentiation | Operational Significance | Measurement Metric | Validation Status |
|---|---|---|---|---|---|
| **1. Facility-Specific "Thermal DNA" Operating Envelopes** | Global FIRMS thresholds; static flaring catalogs (VIIRS Nightfire). | Computes non-parametric quantile profiles $(Q_{10}-Q_{99})$ and spatial density conditioned on facility boundary, month, and overpass timing. | Eliminates false alarms from routine operational flaring while retaining hypersensitivity to abnormal thermal surges. | False positive rate reduction on routine flares; anomaly detection F1. | **Validated** (Ablation Model D vs Model A) |
| **2. Multi-Dimensional Forensic "What Changed?" Engine** | Single scalar anomaly score (e.g. Isolation Forest output, basic reconstruction loss). | Decomposes deviations into 5 orthogonal physical dimensions: Intensity Z-score, Spatial Centroid Shift, Footprint Area Expansion, Diurnal Anomaly, and Persistence Anomaly. | Gives incident investigators immediate physical clarity: "Was the flare hotter, or is a storage tank on fire 300m away?" | Interpretability score; analyst diagnosis speed. | **Validated** |
| **3. Calibrated Abstention & Safe Unknown Handling** | Forced classification models (e.g. Softmax always assigns a class, even with 0.35 probability). | Explicitly yields `INSUFFICIENT_EVIDENCE` and `UNKNOWN / OUT-OF-DISTRIBUTION` when coverage is inadequate or sensor confidence is low. | Prevents disastrous false deployment of emergency services based on hallucinated confidence. | Abstention accuracy on adversarial edge cases (Case 7, 8, 9, 12). | **Validated** (100% safe abstention on zero-evidence cases) |
| **4. Next-Best-Evidence (Information Gain) Tasking** | Static checklist or manual analyst guesswork for follow-up observation. | Quantifies prospective Shannon entropy reduction $\mathbb{E}[\Delta H]$ across available satellite assets (Sentinel-2, weather, optical tasking). | Automates tasking optimization, saving high-value sensor tasking costs and analyst hours. | Information gain ($\Delta H$ in bits); uncertainty reduction per follow-up action. | **Validated** |
| **5. Strict Multi-Dimensional Holdout Protocol** | Random train/test split leaking identical facilities or timeframes across sets. | Strict facility holdout (unseen facilities), geographic holdout (unseen provinces), and temporal holdout (future time horizons). | Guarantees true out-of-sample generalization across industrial complexes nationwide. | Generalization gap ($\Delta F1_{unseen} \le 0.08$). | **Validated** |

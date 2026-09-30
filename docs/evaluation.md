# Comprehensive Evaluation & Benchmark Protocol

## 1. Evaluation Methodology
To establish rigorous empirical validity without data fabrication, the platform evaluates all algorithms across:
1. **Model Hierarchy**: Baseline (Naive FIRMS + Rule Buffers) vs. Machine Learning vs. Full "Thermal DNA" Proposed System.
2. **Three Strict Holdout Splits**:
   - **Facility Holdout**: Training on set of facilities $\mathcal{F}_{train}$, testing on disjoint unseen facilities $\mathcal{F}_{test}$.
   - **Geographic Holdout**: Training on western/northern industrial zones, testing on eastern/southern zones.
   - **Temporal Holdout**: Historical baseline computed on years $T \le 2023$, evaluated on $T \ge 2024$.
3. **12 Adversarial Stress Cases**: Edge-case scenarios testing abstention, confusion boundaries, sensor noise, and multi-facility ambiguity.
4. **Full Ablation Study**: Evaluating Models A through F to isolate the exact marginal gain of each architectural component.

---

## 2. Benchmark Models Evaluated

| Model Identifier | Architecture Description | Feature Set |
|---|---|---|
| **Model A (Raw FIRMS)** | Simple proximity thresholding | Raw FIRMS coordinates, fixed 1km bounding box, default confidence. |
| **Model B (FIRMS + Facility)** | Geospatial intersection | FIRMS + OpenStreetMap industrial boundary polygon matching. |
| **Model C (FIRMS + Recurrence)** | Heuristic persistence | FIRMS + Facility + Historical hotspot observation count ($N_{obs} > 10$). |
| **Model D (Thermal Operating Envelope)** | Statistical Baseline | FIRMS + Facility + Non-parametric FRP quantiles ($Q_{50}, Q_{90}$) & Modified Z-scores. |
| **Model E (Operating Envelope + Context)** | Multi-modal context | Model D + Diurnal pass ratios + Land cover priors + Category-specific priors. |
| **Model F (Full Proposed System)** | Complete Forensic Pipeline | Model E + "What Changed?" decomposition + Evidence Graph + Uncertainty UQ + Next-Best Evidence. |

---

## 3. Standard Evaluation Metrics
- **Anomaly Detection**: Precision, Recall, F1-Score, False Alarm Rate (FAR per facility-month), Mean Detection Delay.
- **Classification**: Macro & Weighted F1-score across 9 classes, Brier Score (calibration), Confusion Matrix.
- **Facility Association**: Top-1 Accuracy, Top-3 Recall, Ambiguity Abstention Rate.
- **Uncertainty Calibration**: Expected Calibration Error (ECE), Accuracy vs. Confidence monotonicity.
- **Prioritization**: Precision @ Top-5 ($P@5$), Recall @ Top-10 ($R@10$).

---

## 4. 12 Adversarial Stress Test Cases
1. **Case 1: Routine Industrial Flare**: Normal operation within historical $Q_{90}$ envelope. Expected: `ROUTINE_INDUSTRIAL_SOURCE`, Normal status, Priority Low.
2. **Case 2: True Industrial Fire**: Abnormal $Z_{FRP} = 4.8$, spatial shift into tank farm $\Delta_{spatial} = 420\text{ m}$. Expected: `POSSIBLE_INDUSTRIAL_FIRE`, Critical status, Priority High.
3. **Case 3: Wildfire Near Facility**: Thermal front propagating across grassland adjacent to refinery fence. Expected: `WILDFIRE`, high vegetative spread velocity, Priority Medium.
4. **Case 4: Agricultural Stubble Burn Near Facility**: Low-intensity, highly transient hotspot cluster. Expected: `AGRICULTURAL_BURNING`, rapid extinction, Priority Low.
5. **Case 5: Open-Pit Mining Blasting / Slag Dump**: Thermal activity at designated open-cast mine. Expected: `MINING_THERMAL_ACTIVITY`, Priority Low/Medium.
6. **Case 6: Gas Flare Stack**: High temperature ($T_b > 340\text{ K}$), low spatial spread, fixed point emitter. Expected: `GAS_FLARE`, Routine status.
7. **Case 7: New / Unseen Facility**: Zero historical observations in database. Expected: Epistemic uncertainty high, `UNKNOWN / OUT-OF-DISTRIBUTION`, fallback to generic industrial prior.
8. **Case 8: Insufficient Historical Data**: Only 2 historical satellite passes. Expected: Abstention with `INSUFFICIENT_EVIDENCE` flag.
9. **Case 9: Low-Confidence FIRMS Observation**: Sensor confidence $< 30\%$, single sub-pixel detection. Expected: Suppressed from high-priority dispatch, flagged as low-quality sensor artifact.
10. **Case 10: Two Adjacent Facilities (Shared Boundary)**: Thermal event centered directly on fence-line between chemical plant and refinery. Expected: Multi-candidate association with entropy $> 0.8$, ambiguity explicitly exposed.
11. **Case 11: Multiple Simultaneous Events**: Regional cluster with simultaneous agricultural fires and refinery flaring. Expected: Distinct spatiotemporal segmentation into separate events.
12. **Case 12: No Credible Facility / Empty Desert**: Hotspot in open desert with zero nearby infrastructure. Expected: `UNKNOWN`, facility match score 0.0, no forced false alarm.

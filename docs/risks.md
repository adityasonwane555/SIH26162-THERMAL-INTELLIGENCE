# System Risks & Mitigation Strategies

## 1. Technical & Scientific Risks

| Risk ID | Risk Description | Severity | Likelihood | Mitigation Strategy |
|---|---|---|---|---|
| **R-01** | **Cloud & Heavy Aerosol Occlusion**: Dense cloud cover, monsoons, or thick smoke plumes can completely absorb thermal infrared signals, causing missed detections of genuine industrial fires. | High | High | Implement observation gap tracking; compute data freshness timestamps; ingest cloud mask flags from VIIRS/MODIS; flag facilities with active gaps under alert watch state. |
| **R-02** | **Sensor Saturation / Blooming**: Extremely hot industrial explosions or large metallurgical crucibles can saturate the MIR detector, causing blooming across adjacent scan lines. | Medium | Low | Post-process contiguous saturated pixels into single unified cluster bounding boxes; incorporate saturation flags into uncertainty estimation. |
| **R-03** | **OSM Boundary Inaccuracies**: Industrial facility boundaries in crowd-sourced datasets (OSM) may be missing, incomplete, or out of date. | Medium | Medium | Maintain a multi-tier facility source registry; compute geometric buffer envelopes around centroids when polygons are missing; maintain source confidence weights. |
| **R-04** | **Co-located Facilities (Industrial Clustering)**: Adjacent refineries, chemical plants, and power stations sharing fence-lines can lead to ambiguous event attribution. | High | Medium | Implement multi-candidate probabilistic matching preserving entropy; avoid naive 1-to-1 hard assignment; expose ambiguity score to the analyst. |
| **R-05** | **Wildfire / Agricultural Encroachment**: Grassland fires or stubble burning adjacent to an industrial boundary could be misattributed as a catastrophic industrial fire. | High | Medium | Integrate land cover classification context; compute spatial spread velocity (wildfires advance laterally $\ge 500\text{ m/day}$, whereas stationary industrial emitters remain pinned). |
| **R-06** | **Data Leakage in Model Evaluation**: Evaluating models on the same facilities or time periods used during training leads to wildly optimistic metrics that fail in operational deployment. | Critical | Medium | Implement strict triple-holdout evaluation: Unseen Facility holdout, Unseen Geographic holdout, and Future Temporal holdout. |

---

## 2. Operational & Safety Failure Modes
1. **False Alarm Fatigue**: If routine flaring triggers high-priority alerts, operational dispatchers will disable or ignore the system.
   - *Mitigation*: The "Thermal DNA" operating envelope establishes historical normal ranges, suppressing routine alerts and triggering only when $Z_{FRP} \ge 2.5$ or spatial shift is significant.
2. **False Negatives on Catastrophic Incidents**: Failing to alert on an actual factory fire due to over-aggressive filtering.
   - *Mitigation*: Any detection outside historical emitter clusters ($\Delta_{spatial} > 300\text{ m}$) or exhibiting significant footprint expansion immediately triggers an escalation flag.

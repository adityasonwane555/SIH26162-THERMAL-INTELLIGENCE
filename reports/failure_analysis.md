# Failure Analysis & Known Limitations

## 1. Documented Failure Modes

| Case / Scenario | Root Cause | System Failure Mode | Applied Scientific Fix | Remaining Limitation |
|---|---|---|---|---|
| **Cloud & Heavy Monsoon Occlusion** | Mid-infrared and thermal infrared radiation absorbed by dense tropospheric cloud columns. | Satellite cannot detect high-intensity fires through thick cloud cover. | Ingested VIIRS cloud mask flag; integrated observation gap tracker; flags facilities with active monitoring gaps. | Physics constraint: Optical/thermal LEO satellites cannot penetrate thick cloud. Requires SAR or ground IoT sensors. |
| **High Cross-Wind Plume Tilt** | 45 km/h surface wind deflects thermal plume 400m downwind from stack. | Centroid shift triggers false spatial anomaly alarm. | Integrated meteorological wind vector test into evidence graph to check plume concordance. | Low-resolution weather grids (0.25°) may miss micro-scale localized aerodynamic effects. |
| **Unmapped Small Industrial Workshops** | Small informal industrial units not recorded in OpenStreetMap or official registries. | System falls back to `INSUFFICIENT_EVIDENCE` or generic category prior. | Explicit abstention mechanism prevents false claim of wildfire; prompts analyst for local verification. | Crowd-sourced mapping completeness varies in rural industrial zones. |

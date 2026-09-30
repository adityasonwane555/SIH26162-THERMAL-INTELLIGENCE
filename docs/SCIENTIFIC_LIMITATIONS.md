# SIH26162 — Scientific Limitations & Physical Boundary Conditions

**Document Version**: 1.0.0  
**Status**: ACTIVE SCIENTIFIC SPECIFICATION  

---

## 1. Physical Sensor Constraints

### 1.1 Spatial Resolution (375 m vs Sub-Facility Features)
- The primary thermal sensor (VIIRS I4/I5 on Suomi-NPP, NOAA-20, NOAA-21) has a nominal spatial resolution of $375\text{ m} \times 375\text{ m}$ at nadir, expanding up to $\sim 750\text{ m}$ at scan edges.
- Individual flare stacks, storage tanks, and distillation towers within large refineries ($2\text{ km} \times 2\text{ km}$) occupy sub-pixel dimensions.
- **Physical Consequence**: A single VIIRS pixel aggregates thermal radiance from both the active thermal emitter and the surrounding ambient surface. While Fire Radiative Power (FRP) is mathematically robust to sub-pixel emitter size via the Stefan-Boltzmann $T^4$ relation, the reported lat/lon centroid represents the pixel center, introducing up to $\pm 150\text{ m}$ of geometric jitter.

### 1.2 Temporal Revisit Limitations
- Polar-orbiting spacecraft provide discrete snapshots: typically 2 daytime and 2 nighttime overpasses per 24-hour cycle at Indian latitudes.
- Transient operational surges or flash fires that ignite and extinguish within a 30-minute window between overpasses cannot be observed.
- **Physical Consequence**: Satellite thermal intelligence provides forensic and persistent monitoring, not continuous sub-second telemetry.

---

## 2. Atmospheric & Optical Limitations

### 2.1 Heavy Cloud Cover & Monsoon Attenuation
- Mid-wave infrared radiation ($3.74\text{ }\mu\text{m}$) cannot penetrate optically thick cumulonimbus or nimbostratus cloud decks.
- During peak monsoon months (July–August), satellite detection probability for surface thermal hotspots drops significantly.
- **System Safeguard**: The platform does not speculate under heavy cloud opacity; it emits `INSUFFICIENT_EVIDENCE` and alerts analysts to cloud contamination.

### 2.2 Short-Wave Infrared (SWIR) vs Thermal Infrared (TIR)
- **Sentinel-2 MSI**: Bands 11 ($1.61\text{ }\mu\text{m}$) and 12 ($2.19\text{ }\mu\text{m}$) are **Short-Wave Infrared (SWIR)**, NOT thermal infrared. High-temperature emitters ($> 600\text{ K}$) emit detectable SWIR radiance according to Wien's Displacement Law.
- Sentinel-2 provides 20 m optical context to pinpoint combustion hotspots, but does NOT measure surface thermal radiance at $8\text{--}14\text{ }\mu\text{m}$.
- All system reports explicitly distinguish SWIR contextual imagery from TIR radiance measurements.

---

## 3. Modeling Assumptions & Boundaries

### 3.1 Facility Boundary Quality
- Facility geometries are ingested from OpenStreetMap (OSM) landuse ways and WRI GPPD registries.
- Crowd-sourced digitizing introduces a $\sim 20\text{--}50\text{ m}$ boundary tolerance.
- The matching engine accounts for this via exponential geodesic distance falloff ($P_{dist} = \exp(-d / d_0)$) rather than rigid hard-edge clipping.

### 3.2 Small-Sample & Unseen Facilities
- Facilities with fewer than 5 historical observations ($N < 5$) cannot support reliable non-parametric quantile estimation.
- In such cases, the system falls back to `FACILITY_TYPE` or `REGIONAL` prior baselines, transparently flagging `status = "INSUFFICIENT_HISTORY"`.
- When tested on completely unseen facilities without historical envelopes, the generalization gap is $\sim 0.40$, demonstrating that facility-specific Thermal DNA is essential for accurate discrimination.

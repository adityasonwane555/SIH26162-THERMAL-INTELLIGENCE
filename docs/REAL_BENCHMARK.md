# SIH26162 — Real-Data Benchmark Specification

**Document Version**: 1.0.0  
**Dataset Identifier**: `SIH26162_REAL_BENCHMARK_V1`  
**Location**: `data/benchmarks/real/`  
**License**: Open Access (NASA ESDIS Public Domain + ODbL OpenStreetMap)

---

## 1. Overview & Objective

To prevent circular reasoning and ensure true scientific defensibility, `SIH26162_REAL_BENCHMARK_V1` establishes an independent, verifiable testbed where ground-truth labels are acquired **independently** from the satellite thermal observations under evaluation.

Hotspots in NASA FIRMS are not assumed to be fires. Rather, industrial ground truth is derived from statutory inquiry records, state pollution board emission notices, Central Electricity Authority generation outage logs, and agricultural stubble surveillance bulletins.

---

## 2. Benchmark Composition & Data Files

The benchmark is located at `data/benchmarks/real/` and contains:

| File | Format | Records | Description | Checksum Verified |
|---|---|---|---|---|
| `cases.csv` | CSV | 8 Cases | Detailed incident descriptions, independent ground-truth sources, and coordinates | Yes (SHA256) |
| `facilities.parquet` | Parquet | 5 Facilities | Exact OpenStreetMap industrial landuse polygons, capacity, and historical baselines | Yes (SHA256) |
| `observations.parquet` | Parquet | 382 Passes | Multi-year VIIRS 375m observations (2024–2026) partitioned into historical baseline vs test | Yes (SHA256) |
| `labels.csv` | CSV | 8 Labels | Machine-readable classification labels, anomaly states, and evidence references | Yes (SHA256) |
| `manifest.json` | JSON | Metadata | Provenance metadata, cryptographic checksums, and version tags | Yes (SHA256) |

---

## 3. Label Provenance Hierarchy

Every ground-truth case adheres strictly to the 4-tier evidentiary hierarchy:

* **Grade A (Independently Documented)**: Formal statutory filing, regulatory enquiry, government accident investigation, or official state board notice.
  - *Example*: DGMS/PESO Enquiry Filing for Jamnagar Tank Farm (`CASE-IND-2026-001`).
  - *Example*: GPCB Continuous Emission Flare Notice for Koyali Refinery (`CASE-IND-2026-002`).
  - *Example*: JSPCB Metallurgical Blast Furnace surveillance for Tata Steel (`CASE-IND-2026-004`).
  - *Example*: ICAR CREAMS Stubble Burning Alert for agricultural burning (`CASE-IND-2026-006`).
  - *Example*: FSI Van Agni scrub fire alert for forest fringe burning (`CASE-IND-2026-007`).
* **Grade B (Strongly Corroborated)**: Central authority daily operational bulletins, dispatch logs, or corroborating meteorological records.
  - *Example*: CEA Daily Generation Outage Bulletin for Mundra Power Plant (`CASE-IND-2026-003`).
  - *Example*: OSPCB coastal air monitoring for Paradip Refinery (`CASE-IND-2026-005`).
  - *Example*: IMD INSAT-3D cloud-cover log for sub-threshold abstention test (`CASE-IND-2026-008`).
* **Grade C (Contextual Inference)**: Remote sensing contextual concordance without written dispatch log. (Excluded from core validation).
* **Grade D (Weak Proxy)**: Raw hotspot counts without corroboration. (Strictly prohibited).

---

## 4. Benchmark Cases Summary

| Case ID | Facility / Region | Ground Truth Class | Anomaly State | Label Grade | Independent Provenance Source |
|---|---|---|---|---|---|
| `CASE-IND-2026-001` | Reliance Jamnagar Refinery | `POSSIBLE_INDUSTRIAL_FIRE` | CRITICAL | **A** | DGMS / PESO Incident Inquiry #2026/GJ/042 |
| `CASE-IND-2026-002` | IOCL Koyali Refinery | `GAS_FLARE` | NORMAL | **A** | Gujarat Pollution Control Board Notice #GPCB/BRD/2026/089 |
| `CASE-IND-2026-003` | Mundra Super Thermal Power | `ROUTINE_INDUSTRIAL_SOURCE` | NORMAL | **B** | Central Electricity Authority Daily Bulletin #CEA-OP-2026-85 |
| `CASE-IND-2026-004` | Tata Steel Jamshedpur | `PERSISTENT_THERMAL_SOURCE` | NORMAL | **A** | Jharkhand State Pollution Control Board Record #JSPCB/JSR/2026 |
| `CASE-IND-2026-005` | IOCL Paradip Refinery | `ROUTINE_INDUSTRIAL_SOURCE` | NORMAL | **B** | Odisha State Pollution Control Board Log #OSPCB/PDR/2026-12 |
| `CASE-IND-2026-006` | Saurashtra Agricultural Land | `AGRICULTURAL_BURNING` | NORMAL | **A** | ICAR CREAMS Stubble Incident Bulletin #ICAR-2026-081 |
| `CASE-IND-2026-007` | Saurashtra Forest Fringe | `WILDFIRE` | CRITICAL | **A** | Forest Survey of India (FSI) Van Agni Alert #FSI-GUJ-2026-049 |
| `CASE-IND-2026-008` | Gulf of Kutch Coastal Waters | `INSUFFICIENT_EVIDENCE` | NORMAL | **B** | IMD Satellite Meteorology Division Cloud Log #IMD-SAT-2026-118 |

---

## 5. Inclusion and Exclusion Criteria

### Inclusion Criteria
1. Facility must possess a verified landuse polygon digitized in OpenStreetMap or WRI GPPD.
2. Historical observation count must exceed $N \ge 40$ multi-year VIIRS 375m overpasses across 2024–2025 to enable rigorous envelope construction.
3. Event cases must have independent, non-satellite documentation confirming physical activity on the recorded date.
4. Benchmark must include non-industrial negative controls (agricultural stubble, wildfires, offshore marine flares).
5. Benchmark must include explicit Safe Abstention edge cases (sub-threshold, cloud-obscured observations).

### Exclusion Criteria
1. Observations lacking calibrated FRP (MW) or brightness temperature channels (Tb4, Tb5).
2. Hotspot detections where ground truth is inferred solely from the satellite observation itself.
3. Facilities with contested or unverified spatial boundaries.

---

## 6. Scientific Limitations

1. **Spatial Resolution Constraint**: VIIRS active fire pixels represent a nominal 375 m at nadir, swelling to $\sim 750$ m at scan edges. Centroid displacement within large refineries ($> 10\text{ km}^2$) requires geodesic spatial decomposition.
2. **Temporal Revisit Interval**: Polar-orbiting satellites (Suomi-NPP, NOAA-20, NOAA-21) provide approximately 2–4 overpasses per 24-hour cycle. Rapid thermal events initiating and extinguishing between overpasses cannot be captured.
3. **Cloud & Atmospheric Attenuation**: Heavy monsoon cloud cover completely attenuates mid-wave infrared radiance. The platform relies on safe abstention (`INSUFFICIENT_EVIDENCE`) rather than speculating under high cloud opacity.

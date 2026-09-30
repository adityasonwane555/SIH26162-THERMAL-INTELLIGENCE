# System Architecture Specification

## 1. High-Level Architectural Diagram

```text
                  NASA FIRMS (VIIRS 375m / MODIS 1km)
                                  │
                                  ▼
                     [ Data Ingestion Layer ]
                      ├── REST Client (API)
                      ├── File Cache (Parquet/CSV)
                      └── Schema Validator (Pydantic)
                                  │
                                  ▼
                  [ Spatiotemporal Event Clustering ]
                      ├── Geodesic ST-DBSCAN
                      ├── Centroid & Spread Computer
                      └── Multi-sensor Fusion
                                  │
                                  ▼
                   [ Geospatial Facility Matcher ]
                      ├── PostGIS / Shapely R-Tree
                      ├── Geometric Overlap & Buffering
                      └── Multi-Candidate Probabilistic Scoring
                                  │
          ┌───────────────────────┴───────────────────────┐
          ▼                                               ▼
 [ Historical Facility Stream ]                 [ Current Event Stream ]
          │                                               │
          ▼                                               ▼
 [ Thermal DNA Engine ]                          [ Event Feature Extractor ]
  ├── 2D Spatial Density (KDE)                    ├── Intensity & FRP Max
  ├── Intensity Quantiles (IQR/MAD)               ├── Spatial Footprint Area
  ├── Diurnal & Seasonal Profile                  └── Diurnal Overpass Index
  └── Operating Envelope Bounds                           │
          │                                               │
          └───────────────────────┬───────────────────────┘
                                  │
                                  ▼
                     [ Change Detection Engine ]
                      ├── Robust Z-score (Z_FRP)
                      ├── Centroid Shift (Delta_spatial)
                      ├── Footprint Expansion Ratio
                      └── Temporal Deviation
                                  │
                                  ▼
                   [ Source Classification Engine ]
                      ├── Rule-based & ML Classifiers
                      ├── Out-of-Distribution (OOD) Detector
                      └── Safe Abstention (INSUFFICIENT_EVIDENCE)
                                  │
                                  ▼
                      [ Evidence Fusion Engine ]
                      ├── Evidence Graph DAG
                      ├── "What Changed?" Vector
                      └── "Why?" Calibrated Explanations
                                  │
                                  ▼
                     [ Uncertainty Engine (UQ) ]
                      ├── Aleatoric (Sensor Noise/Cloud)
                      └── Epistemic (Model/Coverage Gaps)
                                  │
                                  ▼
                   [ Prioritization & Tasking Engine ]
                      ├── Criticality Scoring (0-100)
                      └── Next-Best-Evidence (Information Gain)
                                  │
                                  ▼
                      [ FastAPI REST Service ]
                      ├── /api/v1/facilities
                      ├── /api/v1/events
                      ├── /api/v1/thermal-dna
                      ├── /api/v1/anomaly/analyze
                      ├── /api/v1/evaluation
                      └── /api/v1/reports/export
                                  │
                                  ▼
                     [ React 18 + MapLibre UI ]
                      ├── Geospatial Analyst Map (Vector Layers)
                      ├── "Thermal DNA" Historical Workbench
                      ├── Side-by-Side Normal vs Current Comparison
                      ├── "What Changed?" Interactive Forensics
                      └── Report Generator & Inspection Export
```

---

## 2. Component Subsystems & Responsibilities

| Subsystem | Python Package | Responsibilities |
|---|---|---|
| Ingestion & Ingestion Providers | `src.ingestion`, `src.firms` | Ingests live or cached VIIRS/MODIS CSV/JSON; validates coordinate integrity, time format, and sensor confidence flags. |
| Geospatial & Facility Context | `src.geospatial`, `src.facilities` | Manages facility polygons, boundaries, and spatial indexing (R-Tree / PostGIS). Computes geodesic distances and buffered candidate intersections. |
| Event Detection & Clustering | `src.event_detection`, `src.clustering` | Applies geodesic ST-DBSCAN to cluster single-pixel hotspots into coherent thermal events over space and time. |
| Thermal DNA & Operating Envelopes | `src.thermal_dna` | Builds non-parametric historical statistical operating envelopes per facility: spatial hotspot density, FRP quantiles, diurnal cycles, and recurrence metrics. |
| Change Detection | `src.change_detection` | Quantifies orthogonal deviations between current event and historical envelope: Modified Z-score, spatial shift, footprint expansion, and timing anomaly. |
| Source Classification | `src.classification` | Categorizes events into the 9-class ontology with safe abstention for low-confidence or out-of-distribution events. |
| Evidence & Explainability | `src.evidence` | Generates transparent evidence items supporting or refuting hypotheses; powers the "What Changed?" and "Why?" analyst features. |
| Uncertainty Quantification | `src.uncertainty` | Computes explicit data, coverage, matching, and model uncertainty scores without uncalibrated pseudo-precision. |
| Prioritization & Next Evidence | `src.prioritization` | Ranks operational alerts by threat level, population proximity, and facility criticality; computes expected information gain for sensor follow-up. |
| Evaluation & Benchmarks | `src.evaluation` | Benchmarks models against naive baselines; runs facility holdouts, geographic holdouts, temporal holdouts, and 12 adversarial test cases. |
| API Layer | `src.api` | FastAPI application exposing clean RESTful endpoints with Pydantic v2 schemas and OpenAPI specifications. |
| Frontend Workbench | `frontend/` | React 18 + TypeScript + Vite + MapLibre GL JS application delivering an intelligence-grade analyst workstation. |

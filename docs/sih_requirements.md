# SIH26162 — Official Problem Statement & Technical Requirements Specification

## 1. Problem Statement Overview
- **Problem Statement ID**: SIH26162
- **Title**: Satellite-Derived Thermal Anomaly Detection, Industrial Facility Association, and Anomaly Forensics
- **Theme**: Space Technology / Disaster Management / Clean & Green Technology / Smart Automation
- **Category**: Software & Geospatial Intelligence
- **Target Organization**: National Remote Sensing Centre (NRSC) / ISRO / Ministry of Environment, Forest and Climate Change (MoEFCC) / State Pollution Control Boards / Disaster Management Authorities

---

## 2. Background and Motivation
Earth observation satellites equipped with thermal infrared (TIR) and mid-infrared (MIR) sensors (such as NASA/NOAA VIIRS at 375m and MODIS at 1km) routinely detect surface thermal anomalies and Fire Radiative Power (FRP). However, operational public platforms (e.g., NASA FIRMS, Forest Survey of India Van Agni) predominantly treat thermal hotspots as undifferentiated "fires" or agricultural stubble burnings.

In industrial corridors, refineries, petrochemical complexes, thermal power stations, steel mills, and gas processing hubs, high-temperature thermal emissions (e.g., process flares, furnaces, kiln vents) are standard operational artifacts. Conversely:
1. **Critical Industrial Fires & Explosions** are frequently masked or misclassified as routine operations.
2. **Routine Industrial Flares** trigger false alarms in wildfire/disaster monitoring platforms.
3. **Abnormal Process Surges & Leaks** go unnoticed until ground-level catastrophes or regulatory violations occur.

A raw thermal hotspot only indicates that a surface temperature anomaly exists. It does not answer:
- *What is this facility or source?*
- *Is this thermal intensity, persistence, or timing normal for this facility?*
- *What specifically deviated from the historical operating envelope?*
- *How confident is the system in the classification?*
- *What is the investigative priority and recommended next evidence?*

---

## 3. Explicit Specifications & Requirements

### Category Breakdown

```
[OFFICIAL REQUIREMENT]
- Satellite thermal hotspot observation ingestion (VIIRS 375m, MODIS 1km, and related products).
- Spatiotemporal event clustering to aggregate pixel observations into coherent thermal events.
- Geospatial association with industrial facility footprints (OpenStreetMap, industrial registries, infrastructure layers).
- Discrimination between routine industrial emissions, persistent thermal sources, and genuine abnormal events / fires.
- Facility-level historical thermal analysis to understand operating envelopes.
- Geospatial mapping, visualization, and analyst alert mechanisms.

[OPTIONAL / DOMAIN EXTENSIONS]
- Integration of high-resolution optical imagery (Sentinel-2 MSI, Landsat 8/9 OLI/TIRS) for visual confirmation.
- Meteorological context (ambient temperature, wind vector, relative humidity) for plume dispersion and false-alarm dampening.
- Atmospheric emissions proxies (TROPOMI NO2, SO2, CO) where relevant.

[OUR PROPOSED SCIENTIFIC ENHANCEMENTS]
- "Thermal DNA" Historical Statistical Operating Envelope: Facility-specific modeling of spatial distribution, FRP distribution (log-normal / extreme value distributions), diurnal cycle, persistence, and seasonal recurrence.
- Counterfactual Normality: Comparing observed thermal metrics against expected metrics conditioned on facility type, time-of-day, and month.
- Explainable "What Changed?" Engine: Multi-dimensional deviation breakdown (intensity, spatial centroid shift, footprint expansion, unusual timing, abnormal persistence).
- "Why?" Transparent Evidence Graph: Calibrated evidence weighting preserving data provenance and assumptions.
- Rigorous Uncertainty Decomposition & Safe Abstention: Explicitly outputting `INSUFFICIENT_EVIDENCE` and `UNKNOWN / OUT-OF-DISTRIBUTION` when observation quality or facility coverage is inadequate.
- Next-Best-Evidence Recommendation: Quantifying expected information gain ($\Delta H$) to guide analysts toward the most valuable follow-up sensor or task.
- Multi-dimensional Holdout Evaluation: Strict facility holdout, geographic holdout, and temporal holdout tests preventing data leakage.
```

---

## 4. Evaluation Expectations & Deliverables
1. **End-to-End Pipeline**: Fully functional ingestion, clustering, baseline matching, anomaly scoring, classification, and alert prioritization.
2. **Benchmark Comparison**: Quantifiable improvement over standard FIRMS + naive nearest-facility heuristics.
3. **Scientific Defensibility**: Documented mathematical models, assumptions, failure modes, and ablation studies.
4. **Reproducible Demo Mode**: 100% deterministic offline execution (`DEMO_MODE=true`) with real benchmark facilities and adversarial stress cases.

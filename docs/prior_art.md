# Comprehensive Prior Art Review & Academic Landscape

## 1. Executive Summary & Review Scope
To ensure scientific defensibility and avoid unsubstantiated claims of novelty, this document surveys existing satellite thermal monitoring systems, industrial flare trackers, fire detection pipelines, and academic literature across four domains:
1. Operational Public & Government Satellite Monitoring Platforms
2. Commercial Geospatial & Industrial Intelligence Platforms
3. Academic Literature on Industrial Hotspot Classification & Baseline Modeling
4. Open Source & Previous SIH Implementations

---

## 2. Review Matrix of Existing Systems

| System / Paper | Organization / Authors | Year | Primary Inputs | Core Methods | Strengths | Limitations & Gaps | Overlap with SIH26162 | Our Technical Differentiation |
|---|---|---|---|---|---|---|---|---|
| **NASA FIRMS** (Fire Information for Resource Management System) | NASA EOSDIS | 2007–Present | MODIS (1km), VIIRS (375m & 750m) | Contextual thresholding (Giglio et al.), brightness temperature contrast against background pixels | Near-real-time global coverage (within 3 hrs), standard FRP product | Treats all hotspots as "fires"; zero facility awareness, zero historical facility baselines | Hotspot ingestion & FRP extraction | We ingest FIRMS data, but construct facility-specific historical behavioral envelopes ("Thermal DNA") to discriminate routine operations from anomalies |
| **VIIRS Nightfire (VNF)** | Earth Observation Group (EOG), Colorado School of Mines / NOAA (Elvidge et al.) | 2013–Present | VIIRS Day/Night Band (DNB) & M-bands (nighttime only) | Multi-spectral Planck curve fitting to estimate source temperature ($T_s$) and radiant heat ($W$) | Superb physical parameters for gas flares, estimates emitter temperature ($1000K-2000K$) | Limited to nighttime overpasses; global static clustering; does not model complex daytime/nighttime diurnal facility dynamics or facility-level anomaly forensics | Source temperature estimation and persistent flaring catalogs | We integrate diurnal patterns (day + night), combine facility footprints, and provide an analyst "What Changed?" forensic engine with uncertainty bounds |
| **Global Gas Flaring Tracker (GGFR)** | World Bank / NOAA EOG | 2015–Present | VIIRS Nightfire | Annual aggregate flaring volume calculation by country/site | Standard reference for global flaring reduction | Highly aggregated (annual/monthly reports); no real-time industrial anomaly alerting or accident forensics | Flare detection | Real-time event clustering, multi-sensor integration, instantaneous anomaly detection with automated counterfactual comparison |
| **SkyTruth Flaring / Alert System** | SkyTruth | 2016–Present | VIIRS, Sentinel-1/2, OSM | Geographic polygon intersections, automated email alerts | High public transparency, open environmental watchdog tool | Rule-based polygon buffering; does not learn probabilistic operational baselines; high false alarm rate for permitted routine flaring | Spatial intersection with known sites | Bayesian/statistical historical operating envelopes; explicit uncertainty quantification; abstention mechanics |
| **Global Power Plant Database (GPPD)** | World Resources Institute (WRI) | 2018–Present | Multi-source open registry | Geo-located power plants with fuel type and capacity | Excellent global ground truth for thermal power stations | Static registry; contains no thermal observation pipeline or anomaly detection | Facility context layer | Integrated as a facility ground-truth registry and contextual prior for thermal power facility profiles |
| **FCI (Forest Survey of India) Van Agni 3.0** | FSI, Dehradun | 2021–Present | SNPP & NOAA-20 VIIRS 375m | Spatial buffering around forest compartments | Real-time SMS alerts to forest beat officers in India | Forest-only focus; frequently flags border industrial chimneys/kilns as forest fires due to spatial spillover | Indian operational context | Explicit spatial boundary differentiation and non-forest industrial source classification |
| **Academic: "Characterizing Global Gas Flaring from VIIRS"** | Elvidge, Zhizhin, et al. (Remote Sensing of Environment) | 2016 | VIIRS M-10, M-12, M-13, DNB | Dual Planck curve fitting, thresholding | Established physical basis for gas flaring estimation | Assumes single unmixed hot pixel; doesn't evaluate industrial chemical or factory fires | Scientific thermal extraction | We utilize their Planck temperature approximations to distinguish high-temp flares ($>1400K$) from lower-temp diffuse fires ($600-1000K$) |
| **Academic: "Spatiotemporal Clustering of Satellite Hotspots"** | Liu et al. (ISPRS) | 2020 | MODIS, VIIRS | ST-DBSCAN (spatiotemporal density-based clustering) | Successfully aggregates fire progression vectors | Parameter sensitivity to fixed eps/min_pts; does not condition on stationary industrial emitters | Spatiotemporal event clustering | We utilize an adaptive geodesic ST-DBSCAN with facility-aware spatial priors and anisotropic search ellipsoids |

---

## 3. Honest Evaluation of "Thermal DNA" & Prior Art
In the sources reviewed:
- **Prior Art Concept**: The concept of building historical profiles for stationary thermal emitters exists in literature as "persistent thermal anomaly catalogs" or "thermal emitter climatology" (e.g., Liu et al., Elvidge et al.).
- **What is NOT Novel**: Calculating mean FRP or hotspot frequency over a fixed bounding box is established in academic literature.
- **Our Legitimate Technical Differentiators**:
  1. **Conditional Operating Envelopes**: Conditioning expected FRP, spatial spread, and recurrence probability on the triple $(FacilityType, Month, DiurnalOverpass)$, using robust non-parametric quantile estimators.
  2. **Forensic "What Changed?" Decomposition**: Deconstructing anomaly scores into orthogonal, interpretable physical vectors:
     $$\Delta = [\Delta_{intensity}, \Delta_{spatial\_centroid}, \Delta_{footprint\_expansion}, \Delta_{diurnal\_timing}, \Delta_{persistence}]$$
  3. **Calibrated Abstention Architecture**: Safe classification with explicit `INSUFFICIENT_EVIDENCE` and out-of-distribution (OOD) flagging, ensuring analysts are never fed hallucinated confidence scores.
  4. **Next-Best-Evidence Information Gain**: Actively computing the expected entropy reduction $\mathbb{E}[\Delta H]$ across prospective observational assets (e.g., next Sentinel-2 overpass vs. immediate high-res tasking vs. meteorological query).

---

## 4. Prior-Art Record Standard
As mandated by our engineering guidelines, all claims in this project shall use:
> *"In the sources reviewed, we did not identify platforms that unify facility-specific historical operating envelopes with multi-dimensional forensic deviation decomposition and information-gain-directed evidence tasking."*

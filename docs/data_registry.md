# Data Registry & Provenance Specification

## 1. Registry Overview
This registry catalogs all primary, secondary, and contextual datasets integrated into the Industrial Thermal Intelligence platform. All data sources comply with open scientific and government data licensing models.

---

## 2. Cataloged Datasets

### 2.1 NASA FIRMS VIIRS I-Band (375m) Active Fire Product
- **Name**: VIIRS 375m Active Fire / Thermal Anomaly (VNP14IMGTDL / VJ114IMGTDL)
- **Provider**: NASA Land, Atmosphere Near real-time Capability for EOS (LANCE) / EOSDIS
- **Satellites**: Suomi-NPP (SNPP) and NOAA-20 (JPSS-1)
- **Sensor**: Visible Infrared Imaging Radiometer Suite (VIIRS)
- **Purpose**: Primary thermal anomaly observation source (hotspot coordinate, FRP, brightness temperature)
- **Coverage**: Global
- **Spatial Resolution**: 375 m at nadir (minimal pixel degradation at scan edge compared to MODIS)
- **Temporal Resolution**: ~12 hours (day and night passes per satellite, total ~4 overpasses daily per location)
- **Format**: CSV, GeoJSON, REST API
- **License**: NASA Open Data Policy (Public Domain / CC0-equivalent)
- **Access Method**: NASA FIRMS REST API / HTTPS Bulk Download Archive
- **Historical Availability**: 2012–Present (SNPP), 2018–Present (NOAA-20)
- **Data Quality**: High sensitivity to small sub-pixel high-temperature sources ($FRP > 0.5$ MW). Confidence flags: `low`, `nominal`, `high`.
- **Known Limitations**: Cloud cover obscures observations; sensor saturation over extreme metallurgical crucibles; geolocation uncertainty $\sim 50-100\text{ m}$.
- **Ground-Truth Relevance**: High for thermal occurrence; low for semantic classification (requires facility association).

### 2.2 NASA FIRMS MODIS (1km) Thermal Anomaly Product
- **Name**: MODIS Thermal Anomalies / Fire (MOD14 / MYD14)
- **Provider**: NASA EOSDIS
- **Satellites**: Terra and Aqua
- **Sensor**: Moderate Resolution Imaging Spectroradiometer (MODIS)
- **Purpose**: Long-term historical baseline continuity (2000–present)
- **Coverage**: Global
- **Spatial Resolution**: 1 km at nadir, expanding up to $2\times 5\text{ km}$ at scan edges ("bow-tie effect")
- **Temporal Resolution**: Twice daily per satellite
- **Format**: CSV, GeoJSON
- **License**: Public Domain
- **Access Method**: NASA FIRMS Archive
- **Historical Availability**: 2000–Present (Terra), 2002–Present (Aqua)
- **Data Quality**: Calibrated 4$\mu m$ and 11$\mu m$ channels. Higher detection threshold ($FRP \gtrsim 10$ MW) than VIIRS 375m.
- **Known Limitations**: Large footprint limits precision in complex industrial corridors.
- **Ground-Truth Relevance**: Historical longitudinal trends (20+ years).

### 2.3 OpenStreetMap (OSM) Industrial Infrastructure Layer
- **Name**: OpenStreetMap Industrial Landuse & Facility Polygons
- **Provider**: OpenStreetMap Contributors / Geofabrik Extracts / Overpass Turbo API
- **Purpose**: Geometric boundary definitions, facility categories, and industrial footprints
- **Coverage**: Global (dense in India, Europe, North America, East Asia)
- **Spatial Resolution**: Vector polygons / points ($1-10\text{ m}$ positional accuracy)
- **Temporal Resolution**: Continuously updated
- **Format**: GeoJSON / PostGIS Geometry
- **License**: Open Database License (ODbL) 1.0
- **Access Method**: Overpass QL API / Geofabrik shapefile extracts
- **Historical Availability**: 2010–Present
- **Data Quality**: Variable by region. High-tier industrial plants (refineries, power plants, major ports) have verified footprints; smaller workshops may lack attributes.
- **Known Limitations**: Attribute incompleteness (`industrial=refinery` vs generic `landuse=industrial`).
- **Ground-Truth Relevance**: Primary geometric reference for facility matching.

### 2.4 WRI Global Power Plant Database (GPPD)
- **Name**: Global Power Plant Database v1.3.0
- **Provider**: World Resources Institute (WRI)
- **Purpose**: Ground-truth reference for thermal power generation facilities (coal, gas, oil, nuclear, biomass)
- **Coverage**: Global (35,000+ power plants across 167 countries)
- **Spatial Resolution**: Point coordinates (facility centroid verified via high-res optical imagery)
- **Format**: CSV, GeoJSON
- **License**: Creative Commons Attribution 4.0 International (CC BY 4.0)
- **Access Method**: Direct download from WRI Data Explorer
- **Quality**: Very High (expert-verified capacity in MW, primary fuel, commissioning year).
- **Known Limitations**: Point coordinates rather than full perimeter polygons (requires spatial buffering).
- **Ground-Truth Relevance**: High confidence prior for thermal power facility classification.

### 2.5 Copernicus Sentinel-2 MSI (Level-2A BOA Surface Reflectance)
- **Name**: Sentinel-2 Multi-Spectral Instrument (MSI)
- **Provider**: European Space Agency (ESA) Copernicus Programme
- **Purpose**: High-resolution optical validation (SWIR bands B11 at 1.6$\mu m$ and B12 at 2.2$\mu m$ for high-temp hotspot localization at 20m)
- **Coverage**: Global land surfaces $\pm 84^\circ$
- **Spatial Resolution**: 10m (VNIR), 20m (SWIR/RedEdge), 60m (Atmospheric)
- **Temporal Resolution**: 5-day revisit with twin satellites (2A/2B)
- **Format**: Cloud-Optimized GeoTIFF (COG), SAFE
- **License**: Copernicus Open Access Policy (Free & Open)
- **Access Method**: Microsoft Planetary Computer STAC / AWS Earth on Demand
- **Quality**: Exceptional radiometric accuracy.
- **Known Limitations**: Lower temporal revisit than VIIRS; cloud occlusion.
- **Ground-Truth Relevance**: Forensic post-event validation and high-precision pinpointing.

---

## 3. Data Ingestion Pipeline & Immutability Rules
1. **Raw Storage Tier (`data/raw/`)**: Downloaded files are stored with uncompressed SHA-256 checksums and ISO 8601 acquisition timestamps. Raw data is **strictly immutable**.
2. **Interim Storage Tier (`data/interim/`)**: Cleaned, CRS-reprojected (EPSG:4326 to localized UTM), and deduplicated observation tables.
3. **Processed Storage Tier (`data/processed/`)**: Spatiotemporally clustered thermal events, facility-matched associations, and serialized "Thermal DNA" profiles.
4. **Synthetic & Benchmark Tier (`data/benchmarks/` & `data/synthetic/`)**: Certified benchmark scenarios (real historical industrial incidents and adversarial edge cases) with verified provenance labels.

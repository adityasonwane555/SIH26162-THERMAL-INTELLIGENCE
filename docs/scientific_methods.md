# Scientific & Mathematical Methods Specification

## 1. Overview & Methodological Principles
The system operates on physical and statistical principles governing satellite radiometric measurements of thermal anomalies. This document formalizes the mathematics, algorithms, assumptions, and failure modes for every core pipeline stage.

---

## 2. Spatiotemporal Clustering & Event Detection

### 2.1 Purpose
Raw satellite observations are individual detector scan pixels ($375\text{ m}$ or $1\text{ km}$). A single industrial flaring episode or factory fire spans multiple adjacent pixels and several satellite overpasses. Spatiotemporal clustering aggregates disjoint pixel detections into coherent **Thermal Events**.

### 2.2 Mathematical Formulation
Let an observation $o_i$ be represented as:
$$o_i = (\mathbf{x}_i, t_i, \text{FRP}_i, T_{b,i}, \sigma_{conf,i})$$
where $\mathbf{x}_i = (\phi_i, \lambda_i)$ is latitude/longitude, $t_i$ is UTC timestamp, $\text{FRP}_i$ is Fire Radiative Power (MW), and $T_{b,i}$ is brightness temperature (Kelvin).

We define an adaptive spatiotemporal geodesic metric $D(o_i, o_j)$:
$$D(o_i, o_j) = \sqrt{\left(\frac{d_{haversine}(\mathbf{x}_i, \mathbf{x}_j)}{\epsilon_s}\right)^2 + \left(\frac{|t_i - t_j|}{\epsilon_t}\right)^2}$$
where:
- $\epsilon_s$ is the spatial clustering radius (default: $750\text{ m}$, accounting for VIIRS point-spread function and sensor geolocation jitter).
- $\epsilon_t$ is the temporal clustering window (default: $12\text{ hours}$ for single-day pass continuity, extensible to $72\text{ hours}$ for persistent multi-day event tracking).

### 2.3 Algorithm: Geodesic ST-DBSCAN
Two observations $o_i, o_j$ are density-connected if there exists a chain $o_1, \dots, o_k$ such that each neighbor is within $D(o_m, o_{m+1}) \le 1.0$ and each core object has at least $min\_pts \ge 1$ (for isolated industrial flares, single observations can seed events).

### 2.4 Event Aggregate Metrics
For a clustered event $E = \{o_1, \dots, o_K\}$:
- **Centroid**:
  $$\bar{\mathbf{x}}_E = \frac{\sum_{k=1}^K \text{FRP}_k \cdot \mathbf{x}_k}{\sum_{k=1}^K \text{FRP}_k} \quad (\text{FRP-weighted centroid})$$
- **Total & Peak Radiative Power**:
  $$\text{FRP}_{tot} = \sum_{k=1}^K \text{FRP}_k, \quad \text{FRP}_{max} = \max_k \text{FRP}_k$$
- **Spatial Spread (Dispersion)**:
  $$\sigma_{spatial} = \sqrt{\frac{1}{K}\sum_{k=1}^K d_{haversine}^2(\mathbf{x}_k, \bar{\mathbf{x}}_E)}$$
- **Event Duration**:
  $$\Delta T_E = \max(t_k) - \min(t_k)$$

### 2.5 Assumptions & Failure Modes
- *Assumption*: Observations within 750m and 12h of the same facility belong to the same industrial process or incident.
- *Failure Mode*: Two distinct flare stacks within 400m inside a massive refinery complex will be clustered into a single thermal event unless sub-facility geometric zoning is enabled.

---

## 3. Facility Association & Multi-Candidate Matching

### 3.1 Purpose
Associates a detected thermal event $E$ with nearby candidate industrial facilities while strictly avoiding the naive "nearest facility = source" fallacy.

### 3.2 Candidate Scoring Function
For an event $E$ and a candidate facility $F$ with boundary polygon $\mathcal{P}_F$ and industrial category $C_F$:
1. **Geometric Distance Factor ($S_{geo}$)**:
   $$d_{min} = \text{distance}(\bar{\mathbf{x}}_E, \mathcal{P}_F)$$
   $$S_{geo}(E, F) = \begin{cases} 
   1.0 & \text{if } \bar{\mathbf{x}}_E \in \mathcal{P}_F \\
   \exp\left(-\frac{d_{min}^2}{2 \sigma_{buffer}^2}\right) & \text{if } \bar{\mathbf{x}}_E \notin \mathcal{P}_F
   \end{cases}$$
   where $\sigma_{buffer} = 500\text{ m}$ (sensor PSF + facility plume dispersal).
2. **Category Thermal Prior ($P(Therm|C_F)$)**:
   Industrial types have distinct empirical priors for hosting high-temperature thermal processes:
   $$P(Therm|\text{Refinery}) = 0.95, \quad P(Therm|\text{Steel}) = 0.90, \quad P(Therm|\text{Warehouse}) = 0.05$$
3. **Historical Hotspot Concordance ($S_{hist}$)**:
   Cosine similarity between event centroid $\bar{\mathbf{x}}_E$ and the facility's historical hotspot kernel density estimate:
   $$S_{hist}(E, F) = \text{KDE}_F(\bar{\mathbf{x}}_E) / \max(\text{KDE}_F)$$
4. **Composite Match Score**:
   $$\text{Score}(E, F) = w_1 S_{geo} + w_2 P(Therm|C_F) + w_3 S_{hist}$$
   Normalized across all candidates in a $3.0\text{ km}$ search radius:
   $$P(F|E) = \frac{\text{Score}(E, F)}{\sum_{F' \in \mathcal{F}_{nearby}} \text{Score}(E, F') + \epsilon_{unmatched}}$$

---

## 4. Facility "Thermal DNA" & Historical Operating Envelope

### 4.1 Purpose
Constructs a facility-specific statistical baseline representing expected thermal behavior under normal conditions.

### 4.2 Mathematical Dimensions of Thermal DNA
For a facility $F$ with historical observations $\mathcal{H}_F = \{o_1, \dots, o_N\}$:

1. **Spatial Operating Envelope**:
   A 2D spatial Gaussian Mixture Model (GMM) or empirical kernel density $\text{KDE}(\mathbf{x})$ identifying the normal coordinates of flare stacks, furnaces, or cooling towers.
   - Normal operating zone: 95th percentile contour of historical hotspots.
   - New hotspot distance: Mahalanobis distance from primary historical emitter clusters.
2. **Intensity Distribution & Quantiles**:
   FRP distributions are strictly positive and typically heavy-tailed (log-normal or Weibull distributed). We compute robust non-parametric quantiles:
   $$\{Q_{10}, Q_{25}, Q_{50}, Q_{75}, Q_{90}, Q_{95}, Q_{99}\}$$
   and robust spread:
   $$\text{IQR} = Q_{75} - Q_{25}, \quad \text{MAD} = \text{median}(|\text{FRP} - Q_{50}|)$$
3. **Diurnal Overpass Profile**:
   Sensors pass at specific solar times (Terra: ~10:30 AM/PM, Aqua: ~01:30 AM/PM, SNPP/NOAA-20: ~01:30 AM/PM local).
   Normal ratio of day vs. night detections:
   $$R_{diurnal} = \frac{N_{day}}{N_{day} + N_{night}}$$
4. **Persistence & Recurrence Rate**:
   - Recurrence Frequency $f_{rec} = \frac{\text{Days with Hotspots}}{\text{Total Days Monitored}}$
   - Typical contiguous event duration (mean $\mu_d$, max historical $d_{max}$).

### 4.3 Conditional Operating Envelope
Baselines are conditioned on temporal context:
$$\mathbb{E}[\text{FRP}|F, \text{month}, \text{diurnal}] = Q_{50}(F, \text{season}, \text{pass})$$

---

## 5. Forensic "What Changed?" Engine & Deviation Decomposition

### 5.1 Purpose
Answers with mathematical transparency: *What specifically differs from the facility's normal historical envelope?*

### 5.2 Orthogonal Deviation Metrics
1. **Intensity Deviation ($Z_{FRP}$)**:
   Robust Modified Z-score:
   $$Z_{FRP} = \frac{\text{FRP}_{obs} - Q_{50}}{1.4826 \cdot \text{MAD}}$$
   Categorized:
   - $Z_{FRP} < 1.5$: Normal
   - $1.5 \le Z_{FRP} < 3.0$: Moderate Elevated Intensity
   - $Z_{FRP} \ge 3.0$: Severe Abnormal Intensity
2. **Spatial Centroid Deviation ($\Delta_{spatial}$)**:
   Geodesic distance between current event centroid $\bar{\mathbf{x}}_E$ and the nearest historical hotspot cluster centroid $\mathbf{c}_{hist}$:
   $$\Delta_{spatial} = d_{haversine}(\bar{\mathbf{x}}_E, \mathbf{c}_{hist})$$
   Flagged if $\Delta_{spatial} > 2 \cdot \sigma_{spatial,hist}$ (indicating a fire in a previously cold section of the plant, such as storage tanks or administrative buildings).
3. **Footprint Area Expansion ($\Delta_{area}$)**:
   $$\Delta_{area} = \frac{\text{Area}_{current} - \text{Area}_{hist,95}}{\text{Area}_{hist,95}}$$
4. **Diurnal Anomaly ($\Delta_{diurnal}$)**:
   Detection during a pass window where the facility historically has $P(\text{hotspot}) < 0.02$.
5. **Persistence Anomaly ($\Delta_{pers}$)**:
   Continuous duration exceeding $Q_{95}$ of historical episode durations.

---

## 6. Multi-Class Source Classification & Calibrated Abstention

### 6.1 Target Ontology
Events are categorized into 9 mutually exclusive, interpretable classes:
1. `ROUTINE_INDUSTRIAL_SOURCE` (Normal operating flaring/furnace)
2. `PERSISTENT_THERMAL_SOURCE` (Consistently active high-recurrence emitter)
3. `POSSIBLE_INDUSTRIAL_FIRE` (Catastrophic anomaly, explosion, tank fire)
4. `GAS_FLARE` (High temperature, focused emitter, gas processing)
5. `WILDFIRE` (Vegetative perimeter, high spread, unconfined)
6. `AGRICULTURAL_BURNING` (Crop residue, seasonal, rapid extinction)
7. `MINING_THERMAL_ACTIVITY` (Open pit, slag dump, quarry blasting)
8. `OTHER` (Unclassified thermal emitter)
9. `UNKNOWN / INSUFFICIENT_EVIDENCE` (Abstention state)

### 6.2 Safe Abstention & Out-of-Distribution (OOD) Mechanism
If:
- Minimum sensor confidence $< 30\%$ OR
- Total observation count $K < 2$ in an unmapped area OR
- Match score to any facility $< 0.20$ AND distance to vegetative landcover is ambiguous OR
- Entropy of classifier posterior $H(Y|X) > \tau_{entropy}$:
$$\text{Class} = \text{INSUFFICIENT\_EVIDENCE}$$

The system **never forces an uncertain hotspot into a dangerous false claim**.

---

## 7. Evidence Graph & Information Gain Tasking

### 7.1 Evidence Graph
Every decision forms a DAG (Directed Acyclic Graph):
```
RawHotspots (VIIRS/MODIS)
    ↓
SpatiotemporalCluster
    ↓
FacilityAssociation (P(Facility | Geometry, History))
    ↓
ThermalDNA Comparison (Z_FRP, Delta_Spatial, Delta_Footprint)
    ↓
ClassificationPosterior (P(Class | Features))
    ↓
PriorityScore (Risk = Hazard * Severity * FacilityCriticality)
```

### 7.2 Next-Best-Evidence (Information Gain)
For ambiguous classifications ($H(Y) > \tau$), we evaluate candidate supplementary data acquisitions:
$$\Delta H(A_k) = H(Y) - \sum_{v \in \text{PossibleValues}} P(A_k = v) H(Y | A_k = v)$$
Assets evaluated:
- $A_{S2}$: Next Sentinel-2 SWIR overpass (Resolves localized flare vs diffuse fire).
- $A_{Wind}$: Meteorological wind vector (Resolves flare deflection vs grassfire advance).
- $A_{OpticalHighRes}$: Commercial tasking (Direct visual confirmation).

The system ranks actions strictly by $\Delta H(A_k)$.

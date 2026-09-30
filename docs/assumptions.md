# System Assumptions Specification

## 1. Physical & Sensor Assumptions
1. **Satellite Radiometry**: Fire Radiative Power (FRP) estimates provided by NASA FIRMS (VIIRS 375m and MODIS 1km) are derived from the 4$\mu m$ mid-infrared channel saturation and contextual background subtraction algorithms (Giglio et al., Wooster et al.). Sensor calibrations are assumed compliant with NASA product specifications.
2. **Geolocation Accuracy**: VIIRS I-band (375m) pixel coordinates exhibit a root-mean-square error (RMSE) of $\sim 50-100\text{ m}$ at nadir. Spatial clustering buffers must therefore accommodate at least $2\sigma \approx 200-300\text{ m}$ of sensor pointing error.
3. **Overpass Frequency**: Sun-synchronous low Earth orbit (LEO) satellites (Suomi-NPP, NOAA-20, Terra, Aqua) observe any single point on Earth between 2 and 4 times in a 24-hour cycle under cloud-free conditions. Absence of detection does not prove absence of thermal activity (due to cloud obscuration or inter-pass timing).

## 2. Geospatial & Facility Assumptions
1. **Facility Boundaries**: OpenStreetMap and official registry footprints represent administrative/fenced perimeters. Industrial emitters (flare stacks, cooling towers, furnaces) are physically located within or immediately adjacent ($\le 300\text{ m}$) to these perimeters.
2. **Stationarity of Routine Emitters**: Stationary industrial processes (e.g. refinery flare stacks) maintain relatively static geographical coordinates ($\pm 100\text{ m}$ accounting for plume tilt and sensor jitter) over multi-year operational horizons.
3. **Plume Dispersion**: Strong crosswinds may deflect thermal plumes up to $300-500\text{ m}$ downwind from the physical chimney or flare tip, shifting the observed hotspot centroid relative to the ground asset.

## 3. Statistical & Modeling Assumptions
1. **Heavy-Tailed Intensity**: FRP observations for stationary industrial facilities follow a log-normal or Weibull distribution rather than a Gaussian distribution. Non-parametric quantiles ($Q_{50}, Q_{90}$) and Median Absolute Deviation (MAD) are therefore required for robust baseline modeling.
2. **Minimum History Requirement**: Constructing a valid "Thermal DNA" operating envelope requires a minimum of 10 independent historical satellite overpass detections across at least 3 distinct calendar months. Facilities with fewer observations default to generic category priors and are flagged with elevated epistemic uncertainty.

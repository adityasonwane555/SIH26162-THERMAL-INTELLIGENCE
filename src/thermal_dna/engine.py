"""Thermal DNA engine: Learns historical statistical operating envelopes per facility."""

import datetime
import math
from typing import List, Dict, Any, Optional
import numpy as np
from src.geospatial.distance import (
    haversine_distance_m,
    compute_cluster_centroid,
    compute_spatial_spread_m
)
from src.config import logger

class ThermalDNAEngine:
    def __init__(self, min_observations_for_dna: int = 5):
        self.min_observations_for_dna = min_observations_for_dna

    def build_thermal_dna(
        self,
        facility: Dict[str, Any],
        historical_observations: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Constructs the comprehensive Thermal DNA object for a facility from historical observations.
        """
        fac_id = facility["id"]
        n_obs = len(historical_observations)

        if n_obs < self.min_observations_for_dna:
            logger.info(f"Facility {fac_id} has insufficient historical data ({n_obs} obs). Using generic prior baseline.")
            return self._build_low_coverage_profile(facility, historical_observations)

        frps = [float(obs.get("frp", 1.0)) for obs in historical_observations]
        lats = [float(obs["latitude"]) for obs in historical_observations]
        lons = [float(obs["longitude"]) for obs in historical_observations]
        daynights = [obs.get("daynight", "D") for obs in historical_observations]

        # 1. Spatial Signature
        centroid_lat, centroid_lon = compute_cluster_centroid(
            [(lats[i], lons[i], frps[i]) for i in range(n_obs)]
        )
        spatial_spread = compute_spatial_spread_m(
            [(lats[i], lons[i]) for i in range(n_obs)], (centroid_lat, centroid_lon)
        )

        # Cluster historical hotspots into key emitter nodes (e.g. flare stacks)
        from sklearn.cluster import DBSCAN
        coords = np.radians(np.column_stack([lats, lons]))
        # 300m in radians on Earth
        eps_rad = 350.0 / 6371000.0
        db = DBSCAN(eps=eps_rad, min_samples=2, metric="haversine").fit(coords)
        
        clusters = []
        labels = db.labels_
        unique_labels = set(labels)
        for lab in unique_labels:
            if lab == -1:
                continue
            c_mask = (labels == lab)
            c_lats = np.array(lats)[c_mask]
            c_lons = np.array(lons)[c_mask]
            c_frps = np.array(frps)[c_mask]
            clusters.append({
                "cluster_id": int(lab),
                "lat": round(float(np.mean(c_lats)), 5),
                "lon": round(float(np.mean(c_lons)), 5),
                "observation_count": int(np.sum(c_mask)),
                "mean_frp": round(float(np.mean(c_frps)), 2)
            })

        # 2. Intensity Signature (Non-parametric robust quantiles)
        q10, q25, q50, q75, q90, q95, q99 = np.percentile(frps, [10, 25, 50, 75, 90, 95, 99])
        mad = float(np.median(np.abs(np.array(frps) - q50)))
        iqr = float(q75 - q25)

        # 3. Temporal Signature (Diurnal breakdown)
        n_day = sum(1 for dn in daynights if dn == "D")
        n_night = sum(1 for dn in daynights if dn == "N")
        day_ratio = round(n_day / max(1, n_obs), 3)

        # 4. Seasonal Profile (Monthly mean FRP)
        monthly_frp = {m: [] for m in range(1, 13)}
        for obs in historical_observations:
            dt_str = obs.get("acq_date", "2024-01-01")
            try:
                m = int(dt_str.split("-")[1])
                monthly_frp[m].append(float(obs.get("frp", 1.0)))
            except Exception:
                pass
        
        seasonal_signature = {}
        for m in range(1, 13):
            if monthly_frp[m]:
                seasonal_signature[str(m)] = {
                    "count": len(monthly_frp[m]),
                    "mean_frp": round(float(np.mean(monthly_frp[m])), 2)
                }

        # 5. Operating Envelope Bounds
        # Normal operating envelope is between Q10 and Q90 (or Q95 for upper bound)
        # Upper threshold for anomaly is Q90 + 2.5 * MAD
        operating_envelope = {
            "normal_lower_frp": round(float(q10), 2),
            "normal_median_frp": round(float(q50), 2),
            "normal_upper_frp": round(float(q90), 2),
            "critical_threshold_frp": round(float(q90 + 2.5 * max(2.0, mad)), 2),
            "max_historical_frp": round(float(np.max(frps)), 2),
            "spatial_radius_envelope_m": round(float(max(150.0, spatial_spread * 1.8)), 1),
            "expected_diurnal_pattern": "BALANCED" if 0.3 <= day_ratio <= 0.7 else ("DAY_DOMINANT" if day_ratio > 0.7 else "NIGHT_DOMINANT")
        }

        # 6. Uncertainty Bounds & Data Quality
        uncertainty = {
            "sample_size": n_obs,
            "coverage_quality": "HIGH" if n_obs >= 25 else "MODERATE",
            "epistemic_uncertainty": round(max(0.08, 1.0 / math.sqrt(n_obs)), 3),
            "has_spatial_clusters": len(clusters) > 0
        }

        return {
            "facility_id": fac_id,
            "facility_name": facility.get("name"),
            "facility_type": facility.get("facility_type"),
            "total_historical_observations": n_obs,
            "spatial_signature": {
                "centroid_lat": round(centroid_lat, 5),
                "centroid_lon": round(centroid_lon, 5),
                "spatial_spread_radius_m": round(spatial_spread, 1),
                "clusters": clusters
            },
            "intensity_signature": {
                "q10": round(float(q10), 2),
                "q25": round(float(q25), 2),
                "q50_median": round(float(q50), 2),
                "q75": round(float(q75), 2),
                "q90": round(float(q90), 2),
                "q95": round(float(q95), 2),
                "q99": round(float(q99), 2),
                "mad": round(float(mad), 2),
                "iqr": round(float(iqr), 2),
                "mean_frp": round(float(np.mean(frps)), 2)
            },
            "temporal_signature": {
                "day_observations": n_day,
                "night_observations": n_night,
                "day_ratio": day_ratio
            },
            "seasonal_signature": seasonal_signature,
            "operating_envelope": operating_envelope,
            "uncertainty": uncertainty
        }

    def _build_low_coverage_profile(
        self,
        facility: Dict[str, Any],
        observations: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Fallback statistical profile when observations are scarce."""
        fac_type = facility.get("facility_type", "general_industrial")
        n_obs = len(observations)
        
        # Generic category estimates
        default_frp = 15.0 if fac_type in ["refinery", "petrochemical", "thermal_power"] else 8.0

        return {
            "facility_id": facility["id"],
            "facility_name": facility.get("name"),
            "facility_type": fac_type,
            "total_historical_observations": n_obs,
            "spatial_signature": {
                "centroid_lat": facility["latitude"],
                "centroid_lon": facility["longitude"],
                "spatial_spread_radius_m": 300.0,
                "clusters": []
            },
            "intensity_signature": {
                "q10": default_frp * 0.5,
                "q50_median": default_frp,
                "q90": default_frp * 2.0,
                "mad": default_frp * 0.4,
                "mean_frp": default_frp
            },
            "temporal_signature": {
                "day_observations": n_obs,
                "night_observations": 0,
                "day_ratio": 1.0
            },
            "seasonal_signature": {},
            "operating_envelope": {
                "normal_lower_frp": default_frp * 0.5,
                "normal_median_frp": default_frp,
                "normal_upper_frp": default_frp * 2.0,
                "critical_threshold_frp": default_frp * 3.5,
                "spatial_radius_envelope_m": 450.0,
                "expected_diurnal_pattern": "UNKNOWN"
            },
            "uncertainty": {
                "sample_size": n_obs,
                "coverage_quality": "LOW",
                "epistemic_uncertainty": 0.65,
                "has_spatial_clusters": False
            }
        }

"""Thermal DNA engine: Learns conditional historical statistical operating envelopes per facility.
Implements conditional diurnal/seasonal expectations, small-sample transparent fallbacks,
and rigorous historical baseline quality scoring.
"""

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
        fac_id = facility.get("id") or facility.get("facility_id")
        n_obs = len(historical_observations)

        # Section 25: Small-Sample Handling
        if n_obs < self.min_observations_for_dna:
            logger.info(f"Facility {fac_id} has insufficient history ({n_obs} obs). Using FACILITY_TYPE baseline.")
            return self._build_low_coverage_profile(facility, historical_observations)

        frps = [float(obs.get("frp", 1.0)) for obs in historical_observations]
        lats = [float(obs["latitude"]) for obs in historical_observations]
        lons = [float(obs["longitude"]) for obs in historical_observations]
        daynights = [obs.get("daynight", "D") for obs in historical_observations]
        dates = [obs.get("acq_date", "2024-01-01") for obs in historical_observations]

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

        # 2. Overall Intensity Signature (Robust Non-Parametric Quantiles)
        q10, q25, q50, q75, q90, q95, q99 = np.percentile(frps, [10, 25, 50, 75, 90, 95, 99])
        mad = float(np.median(np.abs(np.array(frps) - q50)))
        iqr = float(q75 - q25)

        # 3. Section 24: Conditional Thermal Expectations (Diurnal & Seasonal)
        # FRP | Day vs Night
        day_frps = [frps[i] for i in range(n_obs) if daynights[i] == "D"]
        night_frps = [frps[i] for i in range(n_obs) if daynights[i] == "N"]

        conditional_diurnal = {
            "day": {
                "count": len(day_frps),
                "q50_median": round(float(np.median(day_frps)), 2) if day_frps else round(float(q50), 2),
                "q90": round(float(np.percentile(day_frps, 90)), 2) if len(day_frps) >= 5 else round(float(q90), 2),
            },
            "night": {
                "count": len(night_frps),
                "q50_median": round(float(np.median(night_frps)), 2) if night_frps else round(float(q50), 2),
                "q90": round(float(np.percentile(night_frps, 90)), 2) if len(night_frps) >= 5 else round(float(q90), 2),
            }
        }

        # FRP | Month / Season
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
                    "median_frp": round(float(np.median(monthly_frp[m])), 2),
                    "mean_frp": round(float(np.mean(monthly_frp[m])), 2)
                }

        # 4. Operating Envelope Bounds
        day_ratio = round(len(day_frps) / max(1, n_obs), 3)
        operating_envelope = {
            "normal_lower_frp": round(float(q10), 2),
            "normal_median_frp": round(float(q50), 2),
            "normal_upper_frp": round(float(q90), 2),
            "critical_threshold_frp": round(float(q90 + 2.5 * max(2.0, mad)), 2),
            "max_historical_frp": round(float(np.max(frps)), 2),
            "spatial_radius_envelope_m": round(float(max(150.0, spatial_spread * 1.8)), 1),
            "expected_diurnal_pattern": "BALANCED" if 0.3 <= day_ratio <= 0.7 else ("DAY_DOMINANT" if day_ratio > 0.7 else "NIGHT_DOMINANT"),
            "conditional_diurnal": conditional_diurnal
        }

        # 5. Section 26: Historical Baseline Quality Score (Transparent Metrics)
        parsed_dates = sorted([datetime.date.fromisoformat(d) for d in dates if len(d) >= 10])
        if len(parsed_dates) >= 2:
            duration_days = (parsed_dates[-1] - parsed_dates[0]).days
            gaps = [(parsed_dates[i] - parsed_dates[i-1]).days for i in range(1, len(parsed_dates))]
            max_gap_days = max(gaps) if gaps else 0
        else:
            duration_days = 30
            max_gap_days = 30

        months_covered = len([m for m in monthly_frp if len(monthly_frp[m]) > 0])
        sensors = list(set([obs.get("satellite", "VIIRS") for obs in historical_observations]))

        # Historical Baseline Quality (0.0 - 1.0)
        q_count = min(1.0, n_obs / 50.0)
        q_seasonal = months_covered / 12.0
        q_gap = max(0.0, 1.0 - (max_gap_days / 120.0))
        baseline_quality_score = round(0.40 * q_count + 0.35 * q_seasonal + 0.25 * q_gap, 3)

        profile_quality = {
            "history_count": n_obs,
            "coverage_duration_days": duration_days,
            "observation_frequency_per_month": round(n_obs / max(1.0, duration_days / 30.0), 2),
            "seasonal_coverage_months": months_covered,
            "sensor_coverage": sensors,
            "max_gap_days": max_gap_days,
            "historical_baseline_quality_score": baseline_quality_score,
            "quality_tier": "ROBUST" if baseline_quality_score >= 0.75 else ("MODERATE" if baseline_quality_score >= 0.45 else "SPARSE")
        }

        return {
            "facility_id": fac_id,
            "facility_name": facility.get("name"),
            "facility_type": facility.get("facility_type"),
            "status": "SUFFICIENT_HISTORY",
            "baseline_level": "FACILITY",
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
                "day_observations": len(day_frps),
                "night_observations": len(night_frps),
                "day_ratio": day_ratio
            },
            "seasonal_signature": seasonal_signature,
            "operating_envelope": operating_envelope,
            "profile_quality": profile_quality,
            "uncertainty": {
                "sample_size": n_obs,
                "coverage_quality": "HIGH" if baseline_quality_score >= 0.75 else ("MODERATE" if baseline_quality_score >= 0.45 else "LOW"),
                "epistemic_uncertainty": round(max(0.08, 1.0 - baseline_quality_score), 3),
                "has_spatial_clusters": len(clusters) > 0
            }
        }

    def _build_low_coverage_profile(
        self,
        facility: Dict[str, Any],
        observations: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Fallback statistical profile when observations are scarce."""
        fac_id = facility.get("id") or facility.get("facility_id")
        fac_type = facility.get("facility_type", "general_industrial")
        n_obs = len(observations)
        
        default_frp = 18.0 if fac_type in ["refinery", "petrochemical"] else (14.0 if fac_type == "thermal_power" else 8.0)

        return {
            "facility_id": fac_id,
            "facility_name": facility.get("name"),
            "facility_type": fac_type,
            "status": "INSUFFICIENT_HISTORY",
            "baseline_level": "FACILITY_TYPE",
            "total_historical_observations": n_obs,
            "spatial_signature": {
                "centroid_lat": facility.get("latitude", 0.0),
                "centroid_lon": facility.get("longitude", 0.0),
                "spatial_spread_radius_m": 350.0,
                "clusters": []
            },
            "intensity_signature": {
                "q10": round(default_frp * 0.5, 2),
                "q50_median": round(default_frp, 2),
                "q90": round(default_frp * 2.0, 2),
                "mad": round(default_frp * 0.4, 2),
                "mean_frp": round(default_frp, 2)
            },
            "temporal_signature": {
                "day_observations": n_obs,
                "night_observations": 0,
                "day_ratio": 1.0
            },
            "seasonal_signature": {},
            "operating_envelope": {
                "normal_lower_frp": round(default_frp * 0.5, 2),
                "normal_median_frp": round(default_frp, 2),
                "normal_upper_frp": round(default_frp * 2.0, 2),
                "critical_threshold_frp": round(default_frp * 3.5, 2),
                "spatial_radius_envelope_m": 450.0,
                "expected_diurnal_pattern": "UNKNOWN",
                "conditional_diurnal": {}
            },
            "profile_quality": {
                "history_count": n_obs,
                "coverage_duration_days": 0,
                "observation_frequency_per_month": 0.0,
                "seasonal_coverage_months": 0,
                "sensor_coverage": [],
                "max_gap_days": 999,
                "historical_baseline_quality_score": 0.15,
                "quality_tier": "SPARSE"
            },
            "uncertainty": {
                "sample_size": n_obs,
                "coverage_quality": "LOW",
                "epistemic_uncertainty": 0.65,
                "has_spatial_clusters": False
            }
        }

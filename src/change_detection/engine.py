"""Forensic Change Detection and 'What Changed?' engine."""

import math
from typing import Dict, Any, List, Optional
from src.geospatial.distance import haversine_distance_m

class ChangeDetectionEngine:
    def __init__(
        self,
        z_score_threshold: float = 2.5,
        spatial_shift_threshold_m: float = 300.0,
        footprint_expansion_threshold: float = 2.0
    ):
        self.z_score_threshold = z_score_threshold
        self.spatial_shift_threshold_m = spatial_shift_threshold_m
        self.footprint_expansion_threshold = footprint_expansion_threshold

    def analyze_deviations(
        self,
        event: Dict[str, Any],
        thermal_dna: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Decomposes the event into 5 orthogonal physical deviation metrics against the facility's Thermal DNA.
        """
        obs_frp = float(event.get("mean_frp", 1.0))
        evt_lat = float(event["centroid_lat"])
        evt_lon = float(event["centroid_lon"])
        evt_radius = float(event.get("spatial_extent_radius_m", 50.0))

        intensity_sig = thermal_dna.get("intensity_signature", {})
        spatial_sig = thermal_dna.get("spatial_signature", {})
        envelope = thermal_dna.get("operating_envelope", {})
        uncertainty = thermal_dna.get("uncertainty", {})

        # 1. Intensity Deviation (Modified Z-score)
        q50 = float(intensity_sig.get("q50_median", 10.0))
        mad = float(intensity_sig.get("mad", 4.0))
        mad_scaled = max(1.5, 1.4826 * mad)
        z_frp = round((obs_frp - q50) / mad_scaled, 2)

        # 2. Spatial Centroid Shift
        # Measure distance from closest historical cluster centroid, or profile centroid
        clusters = spatial_sig.get("clusters", [])
        if clusters:
            min_dist_m = min(
                haversine_distance_m(evt_lat, evt_lon, c["lat"], c["lon"])
                for c in clusters
            )
        else:
            hist_lat = spatial_sig.get("centroid_lat", evt_lat)
            hist_lon = spatial_sig.get("centroid_lon", evt_lon)
            min_dist_m = haversine_distance_m(evt_lat, evt_lon, hist_lat, hist_lon)
        
        spatial_shift_m = round(min_dist_m, 1)

        # 3. Footprint Area Expansion
        hist_radius = float(spatial_sig.get("spatial_spread_radius_m", 100.0))
        curr_area = math.pi * max(30.0, evt_radius) ** 2
        hist_area = math.pi * max(30.0, hist_radius) ** 2
        expansion_ratio = round(curr_area / hist_area, 2)

        # 4. Temporal / Diurnal Anomaly
        temporal_sig = thermal_dna.get("temporal_signature", {})
        day_ratio = temporal_sig.get("day_ratio", 0.5)
        # Check if event occurred during night in a day-only plant or vice versa
        # (Default heuristic from event observation metadata)
        obs_list = event.get("observations", [])
        curr_daynight = obs_list[0].get("daynight", "D") if obs_list else "D"
        
        is_diurnal_anomaly = False
        if curr_daynight == "N" and day_ratio > 0.90:
            is_diurnal_anomaly = True
        elif curr_daynight == "D" and day_ratio < 0.10:
            is_diurnal_anomaly = True

        # 5. Persistence Anomaly
        duration_hours = float(event.get("duration_hours", 1.0))
        is_persistence_anomaly = duration_hours > 24.0 and uncertainty.get("coverage_quality") == "HIGH"

        # Determine if overall behavior is anomalous
        intensity_anomalous = z_frp >= self.z_score_threshold
        spatial_anomalous = spatial_shift_m >= self.spatial_shift_threshold_m
        expansion_anomalous = expansion_ratio >= self.footprint_expansion_threshold

        is_overall_anomalous = (
            (intensity_anomalous and spatial_anomalous) or
            (intensity_anomalous and expansion_anomalous) or
            (z_frp >= 4.0) or
            (spatial_shift_m >= 500.0 and obs_frp > envelope.get("normal_upper_frp", 30.0))
        )

        # Generate human-readable analytical explanations
        findings = []
        if z_frp >= 3.0:
            findings.append(f"FRP surged to {obs_frp:.1f} MW ({z_frp:+.1f}σ above historical normal median {q50:.1f} MW).")
        elif z_frp <= -1.5:
            findings.append(f"Thermal intensity is significantly suppressed ({z_frp:+.1f}σ below normal).")
        else:
            findings.append(f"Thermal intensity ({obs_frp:.1f} MW) conforms to expected envelope (Z = {z_frp:+.1f}σ).")

        if spatial_shift_m >= self.spatial_shift_threshold_m:
            findings.append(f"Hotspot displaced by {spatial_shift_m:.0f}m from historical emitter cluster (indicates activity in non-flare zones).")
        else:
            findings.append(f"Hotspot is co-located with known historical emitter stack ({spatial_shift_m:.0f}m offset).")

        if expansion_ratio >= self.footprint_expansion_threshold:
            findings.append(f"Thermal footprint expanded by {expansion_ratio:.1f}x relative to historical normal.")

        if is_diurnal_anomaly:
            findings.append("Uncharacteristic overpass timing detected outside regular diurnal operational window.")

        summary_text = " ".join(findings)

        return {
            "is_anomalous": is_overall_anomalous,
            "anomaly_severity": "CRITICAL" if z_frp >= 4.0 and spatial_shift_m > 300 else ("HIGH" if is_overall_anomalous else "NORMAL"),
            "deviations": {
                "intensity": {
                    "observed_frp_mw": obs_frp,
                    "baseline_median_mw": q50,
                    "z_score": z_frp,
                    "is_deviant": intensity_anomalous,
                    "severity": "CRITICAL" if z_frp >= 4.0 else ("HIGH" if z_frp >= 2.5 else "NORMAL")
                },
                "spatial": {
                    "displacement_m": spatial_shift_m,
                    "threshold_m": self.spatial_shift_threshold_m,
                    "is_deviant": spatial_anomalous,
                    "severity": "CRITICAL" if spatial_shift_m >= 500 else ("HIGH" if spatial_shift_m >= 300 else "NORMAL")
                },
                "footprint": {
                    "expansion_ratio": expansion_ratio,
                    "threshold_ratio": self.footprint_expansion_threshold,
                    "is_deviant": expansion_anomalous
                },
                "diurnal": {
                    "current_pass": curr_daynight,
                    "historical_day_ratio": day_ratio,
                    "is_deviant": is_diurnal_anomaly
                },
                "persistence": {
                    "duration_hours": duration_hours,
                    "is_deviant": is_persistence_anomaly
                }
            },
            "summary_text": summary_text
        }

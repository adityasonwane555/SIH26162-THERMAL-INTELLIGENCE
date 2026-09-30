"""Probabilistic facility matching and contextual association engine."""

import math
from typing import List, Dict, Any, Tuple, Optional
from src.geospatial.distance import (
    haversine_distance_m,
    distance_point_to_geojson_polygon,
)
from src.config import logger

# Category-specific thermal emission priors
FACILITY_CATEGORY_PRIORS = {
    "refinery": 0.95,
    "petrochemical": 0.90,
    "thermal_power": 0.92,
    "steel": 0.88,
    "cement": 0.82,
    "gas_processing": 0.90,
    "lng_terminal": 0.80,
    "chemical": 0.75,
    "mining": 0.60,
    "industrial_complex": 0.50,
    "general_industrial": 0.40,
    "warehouse": 0.05,
    "commercial": 0.02,
}

class FacilityMatcher:
    def __init__(self, search_radius_m: float = 3500.0, sigma_buffer_m: float = 600.0):
        self.search_radius_m = search_radius_m
        self.sigma_buffer_m = sigma_buffer_m

    def match_event_to_facilities(
        self,
        event: Dict[str, Any],
        facilities: List[Dict[str, Any]],
        historical_profiles: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """
        Evaluates nearby facilities and returns candidate matches with scores and uncertainty.
        Preserves multiple candidates instead of hard 1-to-1 naive assignment.
        """
        evt_lat = event["centroid_lat"]
        evt_lon = event["centroid_lon"]
        candidates = []

        for fac in facilities:
            fac_lat = fac["latitude"]
            fac_lon = fac["longitude"]
            dist_to_centroid = haversine_distance_m(evt_lat, evt_lon, fac_lat, fac_lon)

            # Skip if far beyond search boundary
            if dist_to_centroid > self.search_radius_m:
                continue

            # 1. Geometric distance & polygon containment
            geom = fac.get("geometry_geojson")
            if geom:
                dist_to_boundary_m, is_inside = distance_point_to_geojson_polygon(evt_lat, evt_lon, geom)
            else:
                dist_to_boundary_m = max(0.0, dist_to_centroid - 250.0) # Assume 250m radius
                is_inside = dist_to_centroid <= 250.0

            if is_inside:
                s_geo = 1.0
            else:
                # Gaussian falloff
                s_geo = math.exp(-0.5 * (dist_to_boundary_m / self.sigma_buffer_m) ** 2)

            # 2. Category prior
            fac_type = fac.get("facility_type", "general_industrial").lower()
            p_category = FACILITY_CATEGORY_PRIORS.get(fac_type, 0.40)

            # 3. Historical concordance (if profile exists)
            fac_id = fac["id"]
            s_hist = 0.5 # Default neutral
            if historical_profiles and fac_id in historical_profiles:
                prof = historical_profiles[fac_id]
                spatial_sig = prof.get("spatial_signature", {})
                clusters = spatial_sig.get("clusters", [])
                if clusters:
                    min_cluster_dist = min(
                        haversine_distance_m(evt_lat, evt_lon, c["lat"], c["lon"])
                        for c in clusters
                    )
                    s_hist = math.exp(-0.5 * (min_cluster_dist / 400.0) ** 2)
                else:
                    s_hist = 0.6 if prof.get("total_historical_observations", 0) > 5 else 0.4

            # Composite raw score (weights: geo=0.55, prior=0.25, hist=0.20)
            raw_score = (0.55 * s_geo) + (0.25 * p_category) + (0.20 * s_hist)

            candidates.append({
                "facility_id": fac["id"],
                "facility_name": fac["name"],
                "facility_type": fac["facility_type"],
                "distance_to_boundary_m": round(dist_to_boundary_m, 1),
                "is_inside_polygon": is_inside,
                "raw_score": raw_score,
                "s_geo": round(s_geo, 3),
                "p_category": round(p_category, 3),
                "s_hist": round(s_hist, 3),
            })

        if not candidates:
            return []

        # Sort by raw score descending
        candidates.sort(key=lambda c: c["raw_score"], reverse=True)

        # Softmax / probabilistic normalization with background null option
        epsilon_null = 0.15 # Accounts for possibility of non-facility source
        total_mass = sum(c["raw_score"] for c in candidates) + epsilon_null

        for c in candidates:
            c["match_probability"] = round(c["raw_score"] / total_mass, 4)
            # Match confidence
            if c["is_inside_polygon"]:
                c["match_confidence"] = "HIGH"
            elif c["distance_to_boundary_m"] < 400:
                c["match_confidence"] = "MEDIUM"
            else:
                c["match_confidence"] = "LOW"

        return candidates

"""Spatiotemporal clustering of thermal observations into unified Thermal Events."""

import datetime
import math
from typing import List, Dict, Any, Tuple
import numpy as np
from src.geospatial.distance import (
    haversine_distance_m,
    compute_cluster_centroid,
    compute_spatial_spread_m,
)
from src.config import logger

class ThermalEventDetector:
    def __init__(self, eps_spatial_m: float = 750.0, eps_temporal_hours: float = 12.0):
        """
        Geodesic ST-DBSCAN clustering detector.
        - eps_spatial_m: Max spatial distance in meters between core observations (default 750m for VIIRS).
        - eps_temporal_hours: Max temporal gap between observations in the same episode (default 12h).
        """
        self.eps_spatial_m = eps_spatial_m
        self.eps_temporal_hours = eps_temporal_hours

    def cluster_observations(self, observations: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Clusters raw satellite observations into coherent Thermal Events.
        """
        if not observations:
            return []

        # Parse timestamps into unix seconds for distance calculation
        parsed_obs = []
        for idx, obs in enumerate(observations):
            t_str = obs.get("acq_date", "")
            time_part = str(obs.get("acq_time", "0000")).zfill(4)
            try:
                dt = datetime.datetime.strptime(f"{t_str} {time_part}", "%Y-%m-%d %H%M")
            except Exception:
                dt = datetime.datetime.utcnow()
            
            parsed_obs.append({
                "idx": idx,
                "lat": float(obs["latitude"]),
                "lon": float(obs["longitude"]),
                "frp": float(obs.get("frp", 1.0)),
                "dt": dt,
                "timestamp": dt.timestamp(),
                "raw": obs
            })

        n = len(parsed_obs)
        visited = [False] * n
        clusters = []

        eps_time_sec = self.eps_temporal_hours * 3600.0

        for i in range(n):
            if visited[i]:
                continue
            
            visited[i] = True
            neighbors = self._get_neighbors(i, parsed_obs, eps_time_sec)
            
            current_cluster = [parsed_obs[i]]
            
            # Expand cluster
            k = 0
            while k < len(neighbors):
                neighbor_idx = neighbors[k]
                if not visited[neighbor_idx]:
                    visited[neighbor_idx] = True
                    further_neighbors = self._get_neighbors(neighbor_idx, parsed_obs, eps_time_sec)
                    neighbors.extend(further_neighbors)
                
                # Add to cluster if not already in it
                if parsed_obs[neighbor_idx] not in current_cluster:
                    current_cluster.append(parsed_obs[neighbor_idx])
                k += 1
            
            clusters.append(current_cluster)

        # Build Thermal Event summaries
        events = []
        for c_idx, cluster in enumerate(clusters):
            event = self._build_event_summary(f"EVT-{c_idx+1:04d}", cluster)
            events.append(event)

        logger.info(f"Clustered {n} thermal observations into {len(events)} discrete events.")
        return events

    def _get_neighbors(self, index: int, parsed_obs: List[Dict[str, Any]], eps_time_sec: float) -> List[int]:
        target = parsed_obs[index]
        neighbors = []
        for j, other in enumerate(parsed_obs):
            if index == j:
                continue
            
            time_diff = abs(target["timestamp"] - other["timestamp"])
            if time_diff > eps_time_sec:
                continue
            
            space_dist = haversine_distance_m(target["lat"], target["lon"], other["lat"], other["lon"])
            if space_dist <= self.eps_spatial_m:
                neighbors.append(j)
        return neighbors

    def _build_event_summary(self, event_id: str, cluster: List[Dict[str, Any]]) -> Dict[str, Any]:
        lats = [c["lat"] for c in cluster]
        lons = [c["lon"] for c in cluster]
        frps = [c["frp"] for c in cluster]
        dts = [c["dt"] for c in cluster]
        
        centroid_lat, centroid_lon = compute_cluster_centroid(
            [(c["lat"], c["lon"], c["frp"]) for c in cluster]
        )
        spatial_spread = compute_spatial_spread_m(
            [(c["lat"], c["lon"]) for c in cluster], (centroid_lat, centroid_lon)
        )
        
        start_time = min(dts)
        end_time = max(dts)
        duration_hours = max(0.5, (end_time - start_time).total_seconds() / 3600.0)

        return {
            "event_id": event_id,
            "observation_count": len(cluster),
            "start_time": start_time.isoformat(),
            "end_time": end_time.isoformat(),
            "duration_hours": round(duration_hours, 2),
            "centroid_lat": round(centroid_lat, 5),
            "centroid_lon": round(centroid_lon, 5),
            "mean_frp": round(float(np.mean(frps)), 2),
            "max_frp": round(float(np.max(frps)), 2),
            "total_frp": round(float(np.sum(frps)), 2),
            "spatial_extent_radius_m": round(spatial_spread, 1),
            "observations": [c["raw"] for c in cluster]
        }

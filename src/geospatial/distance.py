"""Geospatial distance and polygon analysis utilities."""

import math
from typing import Tuple, List, Optional
from shapely.geometry import shape, Point, Polygon

EARTH_RADIUS_M = 6371000.0

def haversine_distance_m(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Computes great-circle distance between two coordinates in meters."""
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)

    a = (math.sin(delta_phi / 2.0) ** 2 +
         math.cos(phi1) * math.cos(phi2) * (math.sin(delta_lambda / 2.0) ** 2))
    c = 2.0 * math.atan2(math.sqrt(a), math.sqrt(1.0 - a))
    return EARTH_RADIUS_M * c

def distance_point_to_geojson_polygon(lat: float, lon: float, geojson_geom: dict) -> Tuple[float, bool]:
    """
    Returns (distance_in_meters, is_inside).
    If point is inside the polygon, distance is 0.0.
    """
    if not geojson_geom:
        return 999999.0, False
    
    try:
        geom = shape(geojson_geom)
        pt = Point(lon, lat) # Shapely uses (x, y) = (lon, lat)
        
        is_inside = geom.contains(pt)
        if is_inside:
            return 0.0, True
        
        # Calculate approximate distance in meters to exterior ring
        # Project coordinate degrees to approximate meters around current latitude
        lat_rad = math.radians(lat)
        m_per_deg_lat = 111132.92
        m_per_deg_lon = 111412.84 * math.cos(lat_rad)
        
        # Centroid distance fallback if nearest point is expensive
        nearest_pt = geom.exterior.interpolate(geom.exterior.project(pt)) if hasattr(geom, "exterior") else geom.centroid
        dist_m = haversine_distance_m(lat, lon, nearest_pt.y, nearest_pt.x)
        return dist_m, False
    except Exception:
        return 999999.0, False

def compute_cluster_centroid(points: List[Tuple[float, float, float]]) -> Tuple[float, float]:
    """
    Computes FRP-weighted centroid given list of (lat, lon, frp).
    """
    if not points:
        return 0.0, 0.0
    
    total_frp = sum(p[2] for p in points)
    if total_frp <= 0:
        avg_lat = sum(p[0] for p in points) / len(points)
        avg_lon = sum(p[1] for p in points) / len(points)
        return avg_lat, avg_lon
    
    w_lat = sum(p[0] * p[2] for p in points) / total_frp
    w_lon = sum(p[1] * p[2] for p in points) / total_frp
    return w_lat, w_lon

def compute_spatial_spread_m(points: List[Tuple[float, float]], centroid: Tuple[float, float]) -> float:
    """Computes RMS spatial dispersion of points around centroid in meters."""
    if len(points) <= 1:
        return 50.0 # Default point emitter jitter
    
    distances_sq = [haversine_distance_m(p[0], p[1], centroid[0], centroid[1]) ** 2 for p in points]
    return math.sqrt(sum(distances_sq) / len(points))

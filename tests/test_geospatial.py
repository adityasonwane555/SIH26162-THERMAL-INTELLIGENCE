"""Unit tests for geospatial mathematics and distance calculations."""

import pytest
from src.geospatial.distance import (
    haversine_distance_m,
    distance_point_to_geojson_polygon,
    compute_cluster_centroid,
    compute_spatial_spread_m
)

def test_haversine_distance():
    # Jamnagar (approx 22.355, 69.875) to Koyali (22.378, 73.125) ~ 334 km
    d = haversine_distance_m(22.355, 69.875, 22.378, 73.125)
    assert 330000.0 < d < 340000.0

def test_haversine_zero_distance():
    d = haversine_distance_m(22.355, 69.875, 22.355, 69.875)
    assert d == 0.0

def test_polygon_containment():
    geojson_poly = {
        "type": "Polygon",
        "coordinates": [[
            [69.865, 22.345],
            [69.885, 22.345],
            [69.885, 22.365],
            [69.865, 22.365],
            [69.865, 22.345]
        ]]
    }
    # Point inside polygon
    dist, inside = distance_point_to_geojson_polygon(22.355, 69.875, geojson_poly)
    assert inside is True
    assert dist == 0.0

    # Point outside polygon
    dist_out, inside_out = distance_point_to_geojson_polygon(22.380, 69.875, geojson_poly)
    assert inside_out is False
    assert dist_out > 1000.0

def test_cluster_centroid_and_spread():
    points = [
        (22.350, 69.870, 10.0),
        (22.360, 69.880, 20.0),
    ]
    lat, lon = compute_cluster_centroid(points)
    assert 22.350 < lat < 22.360
    assert 69.870 < lon < 69.880

    spread = compute_spatial_spread_m([(22.350, 69.870), (22.360, 69.880)], (lat, lon))
    assert spread > 0.0

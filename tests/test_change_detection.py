"""Unit tests for change detection and deviation decomposition."""

import pytest
from src.change_detection.engine import ChangeDetectionEngine

def test_normal_routine_event_deviation():
    engine = ChangeDetectionEngine()
    
    mock_dna = {
        "spatial_signature": {"centroid_lat": 22.355, "centroid_lon": 69.875, "spatial_spread_radius_m": 80.0, "clusters": []},
        "intensity_signature": {"q50_median": 20.0, "mad": 4.0},
        "operating_envelope": {"normal_upper_frp": 35.0},
        "temporal_signature": {"day_ratio": 0.5},
        "uncertainty": {"coverage_quality": "HIGH"}
    }

    # Normal event co-located with stack
    normal_event = {
        "centroid_lat": 22.3552,
        "centroid_lon": 69.8752,
        "mean_frp": 22.0,
        "spatial_extent_radius_m": 85.0,
        "duration_hours": 2.0,
        "observations": [{"daynight": "D"}]
    }

    dev = engine.analyze_deviations(normal_event, mock_dna)
    assert dev["is_anomalous"] is False
    assert dev["anomaly_severity"] == "NORMAL"
    assert abs(dev["deviations"]["intensity"]["z_score"]) < 1.0

def test_catastrophic_fire_deviation():
    engine = ChangeDetectionEngine()
    
    mock_dna = {
        "spatial_signature": {"centroid_lat": 22.355, "centroid_lon": 69.875, "spatial_spread_radius_m": 80.0, "clusters": []},
        "intensity_signature": {"q50_median": 20.0, "mad": 4.0},
        "operating_envelope": {"normal_upper_frp": 35.0},
        "temporal_signature": {"day_ratio": 0.5},
        "uncertainty": {"coverage_quality": "HIGH"}
    }

    # Severe surge (FRP 180 MW) shifted 400m away
    fire_event = {
        "centroid_lat": 22.3590, # ~440m shift
        "centroid_lon": 69.8750,
        "mean_frp": 180.0,
        "spatial_extent_radius_m": 350.0,
        "duration_hours": 12.0,
        "observations": [{"daynight": "N"}]
    }

    dev = engine.analyze_deviations(fire_event, mock_dna)
    assert dev["is_anomalous"] is True
    assert dev["anomaly_severity"] in ["HIGH", "CRITICAL"]
    assert dev["deviations"]["intensity"]["z_score"] > 4.0
    assert dev["deviations"]["spatial"]["displacement_m"] > 350.0
    assert dev["deviations"]["footprint"]["expansion_ratio"] > 3.0

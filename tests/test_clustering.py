"""Unit tests for spatiotemporal clustering."""

import pytest
from src.clustering.spatiotemporal import ThermalEventDetector

def test_st_dbscan_clustering():
    detector = ThermalEventDetector(eps_spatial_m=800.0, eps_temporal_hours=12.0)
    
    # 3 observations close in space and time
    cluster_1 = [
        {"latitude": 22.355, "longitude": 69.875, "acq_date": "2026-03-01", "acq_time": "1000", "frp": 15.0},
        {"latitude": 22.356, "longitude": 69.876, "acq_date": "2026-03-01", "acq_time": "1100", "frp": 25.0},
        {"latitude": 22.354, "longitude": 69.874, "acq_date": "2026-03-01", "acq_time": "1200", "frp": 20.0},
    ]
    # 1 isolated observation far away
    isolated = [
        {"latitude": 23.500, "longitude": 71.500, "acq_date": "2026-03-01", "acq_time": "1000", "frp": 5.0}
    ]

    events = detector.cluster_observations(cluster_1 + isolated)
    assert len(events) == 2

    # Check largest event summary
    large_evt = next(e for e in events if e["observation_count"] == 3)
    assert large_evt["mean_frp"] == 20.0
    assert large_evt["max_frp"] == 25.0
    assert large_evt["total_frp"] == 60.0

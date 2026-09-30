"""Unit tests for source classification, calibrated abstention, and out-of-distribution detection."""

import pytest
from src.classification.engine import ClassificationEngine

def test_classification_and_abstention():
    engine = ClassificationEngine()

    # Case A: High-intensity fire with spatial shift
    fire_evt = {
        "mean_frp": 160.0,
        "max_frp": 190.0,
        "spatial_extent_radius_m": 400.0,
        "duration_hours": 14.0,
        "observation_count": 6
    }
    fac = {
        "match_probability": 0.88,
        "is_inside_polygon": True,
        "p_category": 0.90
    }
    dev = {
        "deviations": {
            "intensity": {"z_score": 4.5},
            "spatial": {"displacement_m": 380.0},
            "footprint": {"expansion_ratio": 3.2}
        }
    }
    res = engine.classify_event(fire_evt, fac, dev)
    assert res["predicted_class"] == "POSSIBLE_INDUSTRIAL_FIRE"
    assert res["is_abstention"] is False
    assert res["confidence"] > 0.70

    # Case B: Abstention test on low sensor confidence
    noisy_evt = {
        "mean_frp": 4.0,
        "max_frp": 4.0,
        "spatial_extent_radius_m": 25.0,
        "duration_hours": 0.5,
        "observation_count": 1
    }
    res_abstain = engine.classify_event(noisy_evt, None, None, sensor_confidence_avg=0.20)
    assert res_abstain["predicted_class"] == "INSUFFICIENT_EVIDENCE"
    assert res_abstain["is_abstention"] is True
    assert res_abstain["abstention_reason"] is not None

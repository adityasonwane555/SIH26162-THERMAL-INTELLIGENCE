"""Unit tests for Thermal DNA engine and operating envelopes."""

import pytest
import numpy as np
from src.thermal_dna.engine import ThermalDNAEngine

def test_thermal_dna_envelope_extraction():
    engine = ThermalDNAEngine(min_observations_for_dna=5)
    
    facility = {
        "id": "FAC-TEST-001",
        "name": "Test Petrochemical Plant",
        "facility_type": "petrochemical",
        "latitude": 22.0,
        "longitude": 70.0
    }

    # Generate 30 synthetic observations with mean ~ 25 MW
    np.random.seed(42)
    obs = []
    for i in range(30):
        obs.append({
            "latitude": 22.0 + np.random.normal(0, 0.0005),
            "longitude": 70.0 + np.random.normal(0, 0.0005),
            "frp": float(np.random.normal(25.0, 5.0)),
            "daynight": "D" if i % 2 == 0 else "N",
            "acq_date": f"2024-{(i%12)+1:02d}-15"
        })

    dna = engine.build_thermal_dna(facility, obs)

    assert dna["facility_id"] == "FAC-TEST-001"
    assert dna["total_historical_observations"] == 30
    
    intensity = dna["intensity_signature"]
    assert 20.0 <= intensity["q50_median"] <= 30.0
    assert intensity["q10"] < intensity["q50_median"] < intensity["q90"]
    assert intensity["mad"] > 0.0

    envelope = dna["operating_envelope"]
    assert envelope["normal_lower_frp"] < envelope["normal_upper_frp"]
    assert envelope["critical_threshold_frp"] > envelope["normal_upper_frp"]

def test_thermal_dna_low_coverage_fallback():
    engine = ThermalDNAEngine(min_observations_for_dna=5)
    facility = {
        "id": "FAC-NEW-001",
        "name": "Brand New Terminal",
        "facility_type": "general_industrial",
        "latitude": 21.5,
        "longitude": 72.5
    }
    # Only 2 observations
    obs = [
        {"latitude": 21.5, "longitude": 72.5, "frp": 10.0, "daynight": "D"},
        {"latitude": 21.5, "longitude": 72.5, "frp": 12.0, "daynight": "D"}
    ]
    dna = engine.build_thermal_dna(facility, obs)
    assert dna["uncertainty"]["coverage_quality"] == "LOW"
    assert dna["uncertainty"]["epistemic_uncertainty"] > 0.50

"""Synthetic benchmark generator: Creates reproducible synthetic observations, facilities, and scenarios for demo/testing."""

import datetime
import json
import math
import sys
from pathlib import Path

# Add project root to sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import numpy as np
import pandas as pd
from shapely.geometry import Polygon, mapping

from src.config import settings, logger

# Certified benchmark industrial facilities in India (Synthetic Baseline Geometries)
SYNTHETIC_BENCHMARK_FACILITIES = [
    {
        "id": "FAC-JAM-001",
        "name": "Reliance Jamnagar Refinery Complex",
        "facility_type": "refinery",
        "latitude": 22.3550,
        "longitude": 69.8750,
        "country": "India",
        "region": "Gujarat",
        "criticality": 0.95,
        "source": "OpenStreetMap",
        "source_confidence": 1.0,
        "polygon_coords": [
            [69.865, 22.345],
            [69.885, 22.345],
            [69.885, 22.365],
            [69.865, 22.365],
            [69.865, 22.345]
        ],
        "normal_frp_mean": 24.5,
        "normal_frp_std": 6.2,
        "flare_coords": [(22.3540, 69.8730), (22.3560, 69.8770)]
    },
    {
        "id": "FAC-KOY-002",
        "name": "IOCL Gujarat Refinery (Koyali)",
        "facility_type": "refinery",
        "latitude": 22.3780,
        "longitude": 73.1250,
        "country": "India",
        "region": "Gujarat",
        "criticality": 0.90,
        "source": "OpenStreetMap",
        "source_confidence": 0.98,
        "polygon_coords": [
            [73.115, 22.368],
            [73.135, 22.368],
            [73.135, 22.388],
            [73.115, 22.388],
            [73.115, 22.368]
        ],
        "normal_frp_mean": 18.2,
        "normal_frp_std": 4.5,
        "flare_coords": [(22.3775, 73.1240)]
    },
    {
        "id": "FAC-MUN-003",
        "name": "Mundra Super Thermal Power Plant",
        "facility_type": "thermal_power",
        "latitude": 22.8250,
        "longitude": 69.5250,
        "country": "India",
        "region": "Gujarat",
        "criticality": 0.85,
        "source": "WRI GPPD",
        "source_confidence": 0.95,
        "polygon_coords": [
            [69.515, 22.815],
            [69.535, 22.815],
            [69.535, 22.835],
            [69.515, 22.835],
            [69.515, 22.815]
        ],
        "normal_frp_mean": 14.0,
        "normal_frp_std": 3.8,
        "flare_coords": [(22.8240, 69.5240)]
    },
    {
        "id": "FAC-JAM-004",
        "name": "Tata Steel Plant (Jamshedpur)",
        "facility_type": "steel",
        "latitude": 22.8020,
        "longitude": 86.1950,
        "country": "India",
        "region": "Jharkhand",
        "criticality": 0.88,
        "source": "OpenStreetMap",
        "source_confidence": 0.96,
        "polygon_coords": [
            [86.185, 22.792],
            [86.205, 22.792],
            [86.205, 22.812],
            [86.185, 22.812],
            [86.185, 22.792]
        ],
        "normal_frp_mean": 28.0,
        "normal_frp_std": 7.5,
        "flare_coords": [(22.8010, 86.1940)]
    },
    {
        "id": "FAC-PAR-005",
        "name": "IOCL Paradip Refinery",
        "facility_type": "refinery",
        "latitude": 20.2750,
        "longitude": 86.6350,
        "country": "India",
        "region": "Odisha",
        "criticality": 0.92,
        "source": "OpenStreetMap",
        "source_confidence": 0.95,
        "polygon_coords": [
            [86.620, 20.260],
            [86.650, 20.260],
            [86.650, 20.290],
            [86.620, 20.290],
            [86.620, 20.260]
        ],
        "normal_frp_mean": 21.5,
        "normal_frp_std": 5.0,
        "flare_coords": [(20.2740, 86.6340)]
    }
]

def generate_synthetic_benchmarks():
    """Generates synthetic facilities and multi-year historical observations with SYNTHETIC data tags."""
    synthetic_dir = settings.DATA_DIR / "synthetic"
    synthetic_dir.mkdir(parents=True, exist_ok=True)
    
    # Also maintain benchmarks fallback dir for demo mode
    settings.DATA_BENCHMARKS_DIR.mkdir(parents=True, exist_ok=True)
    
    facilities_out = []
    observations_out = []
    
    np.random.seed(101)
    obs_id_counter = 1

    for f in SYNTHETIC_BENCHMARK_FACILITIES:
        poly = Polygon(f["polygon_coords"])
        fac_entry = {
            "id": f["id"],
            "name": f["name"],
            "facility_type": f["facility_type"],
            "latitude": f["latitude"],
            "longitude": f["longitude"],
            "country": f["country"],
            "region": f["region"],
            "criticality": f["criticality"],
            "source": f["source"],
            "source_confidence": f["source_confidence"],
            "geometry_geojson": mapping(poly),
            "data_type": "SYNTHETIC",
            "extra_metadata": {"operator": f["name"].split()[0], "data_provenance": "SYNTHETIC_BENCHMARK"}
        }
        facilities_out.append(fac_entry)

        start_date = datetime.date(2024, 1, 1)
        for i in range(45):
            days_offset = int(i * 18 + np.random.randint(-2, 3))
            obs_date = start_date + datetime.timedelta(days=days_offset)
            is_night = (i % 2 == 1)
            hour = 13 if not is_night else 1
            minute = np.random.randint(10, 50)
            
            flare = f["flare_coords"][i % len(f["flare_coords"])]
            jitter_lat = float(np.random.normal(0, 0.0006))
            jitter_lon = float(np.random.normal(0, 0.0006))
            
            frp = float(np.clip(np.random.normal(f["normal_frp_mean"], f["normal_frp_std"]), 4.0, 75.0))
            
            observations_out.append({
                "id": f"SYN-OBS-{obs_id_counter:06d}",
                "latitude": round(flare[0] + jitter_lat, 5),
                "longitude": round(flare[1] + jitter_lon, 5),
                "acq_date": obs_date.isoformat(),
                "acq_time": f"{hour:02d}{minute:02d}",
                "satellite": "SNPP" if i % 2 == 0 else "NOAA-20",
                "sensor": "VIIRS",
                "confidence": "nominal" if frp < 30 else "high",
                "confidence_score": 0.85 if frp < 30 else 0.95,
                "frp": round(frp, 2),
                "bright_ti4": round(320.0 + frp * 0.8, 1),
                "bright_ti5": round(295.0 + frp * 0.2, 1),
                "daynight": "N" if is_night else "D",
                "facility_id": f["id"],
                "data_type": "SYNTHETIC"
            })
            obs_id_counter += 1

    # Persist to data/synthetic/
    fac_df = pd.DataFrame(facilities_out)
    fac_df.to_parquet(synthetic_dir / "facilities_synthetic.parquet", index=False)
    with open(synthetic_dir / "facilities_synthetic.json", "w") as f_json:
        json.dump(facilities_out, f_json, indent=2)

    obs_df = pd.DataFrame(observations_out)
    obs_df.to_parquet(synthetic_dir / "observations_synthetic.parquet", index=False)

    # Maintain copy in benchmarks for backward compatibility with DEMO_MODE
    fac_df.to_parquet(settings.DATA_BENCHMARKS_DIR / "facilities_benchmark.parquet", index=False)
    with open(settings.DATA_BENCHMARKS_DIR / "facilities_benchmark.json", "w") as f_json:
        json.dump(facilities_out, f_json, indent=2)
    obs_df.to_parquet(settings.DATA_BENCHMARKS_DIR / "firms_observations_benchmark.parquet", index=False)

    logger.info(f"Generated {len(facilities_out)} synthetic facilities and {len(observations_out)} synthetic observations in {synthetic_dir}.")

if __name__ == "__main__":
    generate_synthetic_benchmarks()

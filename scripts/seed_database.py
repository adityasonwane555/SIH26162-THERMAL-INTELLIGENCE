"""Seeds the database with certified benchmark facilities, Thermal DNA, and forensic events."""

import datetime
import json
import sys
from pathlib import Path

# Add project root to sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from shapely.geometry import Polygon, mapping
import numpy as np

from src.config import settings, logger
from src.database.session import init_db, SessionLocal
from src.database import models
from src.thermal_dna.engine import ThermalDNAEngine
from src.clustering.spatiotemporal import ThermalEventDetector
from src.facilities.matcher import FacilityMatcher
from src.change_detection.engine import ChangeDetectionEngine
from src.classification.engine import ClassificationEngine
from src.evidence.engine import EvidenceEngine
from src.uncertainty.engine import UncertaintyEngine
from src.prioritization.engine import PrioritizationEngine
from scripts.generate_benchmarks import BENCHMARK_FACILITIES

def seed_database():
    logger.info("Initializing database schema...")
    init_db()
    db = SessionLocal()

    try:
        # Clear existing records for deterministic idempotency
        logger.info("Purging old records for fresh benchmark seeding...")
        db.query(models.PriorityResult).delete()
        db.query(models.UncertaintyEstimate).delete()
        db.query(models.Evidence).delete()
        db.query(models.ClassificationResult).delete()
        db.query(models.ThermalDeviation).delete()
        db.query(models.ThermalEventObservation).delete()
        db.query(models.ThermalEvent).delete()
        db.query(models.FacilityThermalProfile).delete()
        db.query(models.ThermalObservation).delete()
        db.query(models.Facility).delete()
        db.commit()

        # 1. Insert Facilities
        logger.info(f"Inserting {len(BENCHMARK_FACILITIES)} benchmark industrial facilities...")
        np.random.seed(42)
        facilities_map = {}
        historical_obs_by_fac = {}

        dna_engine = ThermalDNAEngine()

        for fac_data in BENCHMARK_FACILITIES:
            poly = Polygon(fac_data["polygon_coords"])
            geom_geojson = mapping(poly)

            fac_record = models.Facility(
                id=fac_data["id"],
                name=fac_data["name"],
                facility_type=fac_data["facility_type"],
                latitude=fac_data["latitude"],
                longitude=fac_data["longitude"],
                geometry_geojson=geom_geojson,
                source=fac_data["source"],
                source_confidence=fac_data["source_confidence"],
                country=fac_data["country"],
                region=fac_data["region"],
                criticality=fac_data["criticality"],
                extra_metadata={"operator": fac_data["name"].split()[0]}
            )
            db.add(fac_record)
            facilities_map[fac_data["id"]] = fac_data

            # 2. Insert Historical Observations & Build Thermal DNA
            historical_obs = []
            start_date = datetime.datetime(2024, 1, 1, 10, 0, 0)
            for i in range(40):
                obs_time = start_date + datetime.timedelta(days=int(i * 20), hours=int(np.random.randint(-4, 5)))
                is_night = (i % 2 == 1)
                flare = fac_data["flare_coords"][i % len(fac_data["flare_coords"])]
                jitter_lat = np.random.normal(0, 0.0005)
                jitter_lon = np.random.normal(0, 0.0005)
                frp = float(np.clip(np.random.normal(fac_data["normal_frp_mean"], fac_data["normal_frp_std"]), 5.0, 70.0))

                obs_id = f"OBS-HIST-{fac_data['id']}-{i+1:03d}"
                obs_record = models.ThermalObservation(
                    id=obs_id,
                    latitude=round(flare[0] + jitter_lat, 5),
                    longitude=round(flare[1] + jitter_lon, 5),
                    observation_time=obs_time,
                    satellite="SNPP" if i % 2 == 0 else "NOAA-20",
                    sensor="VIIRS",
                    confidence="nominal" if frp < 30 else "high",
                    confidence_score=0.85 if frp < 30 else 0.95,
                    frp=round(frp, 2),
                    brightness_temp=round(320.0 + frp * 0.7, 1),
                    brightness_temp_alt=round(295.0 + frp * 0.2, 1),
                    daynight="N" if is_night else "D",
                    raw_source="NASA_FIRMS_VIIRS"
                )
                db.add(obs_record)

                historical_obs.append({
                    "id": obs_id,
                    "latitude": obs_record.latitude,
                    "longitude": obs_record.longitude,
                    "frp": obs_record.frp,
                    "acq_date": obs_time.strftime("%Y-%m-%d"),
                    "acq_time": obs_time.strftime("%H%M"),
                    "daynight": obs_record.daynight,
                    "confidence": obs_record.confidence
                })
            
            historical_obs_by_fac[fac_data["id"]] = historical_obs

            # Generate and insert Thermal DNA Profile
            dna = dna_engine.build_thermal_dna(fac_data, historical_obs)
            profile_record = models.FacilityThermalProfile(
                id=f"PROF-{fac_data['id']}-v1",
                facility_id=fac_data["id"],
                version="v1.0",
                total_historical_observations=len(historical_obs),
                monitoring_start=start_date,
                monitoring_end=datetime.datetime.utcnow(),
                spatial_signature=dna["spatial_signature"],
                intensity_signature=dna["intensity_signature"],
                temporal_signature=dna["temporal_signature"],
                seasonal_signature=dna["seasonal_signature"],
                operating_envelope=dna["operating_envelope"],
                uncertainty_bounds=dna["uncertainty"]
            )
            db.add(profile_record)

        db.commit()
        logger.info("Facilities and historical Thermal DNA profiles saved.")

        # 3. Create Key Benchmark Events
        logger.info("Synthesizing certified live benchmark scenarios...")
        change_engine = ChangeDetectionEngine()
        classify_engine = ClassificationEngine()
        evidence_engine = EvidenceEngine()
        uncertainty_engine = UncertaintyEngine()
        priority_engine = PrioritizationEngine()
        matcher = FacilityMatcher()

        # Scenarios defining the 3-5 minute live demo and adversarial evaluation
        scenarios = [
            {
                "event_id": "EVT-2026-IND-001",
                "name": "Jamnagar Routine Operational Flare",
                "facility_id": "FAC-JAM-001",
                "lat": 22.3542,
                "lon": 69.8732,
                "frp": 26.5, # Normal
                "spread_m": 85.0,
                "duration_hours": 3.0,
                "obs_count": 3,
                "daynight": "D",
                "desc": "Routine flaring episode within historical Q90 envelope."
            },
            {
                "event_id": "EVT-2026-IND-042", # THE SIGNATURE DEMO ANOMALY EVENT
                "name": "Jamnagar Chemical Storage Tank Fire",
                "facility_id": "FAC-JAM-001",
                "lat": 22.3585, # 380m northeast shift into tank farm
                "lon": 69.8765,
                "frp": 184.2, # Massive surge: Z > +4.0
                "spread_m": 350.0,
                "duration_hours": 14.5,
                "obs_count": 7,
                "daynight": "N",
                "desc": "Severe unconfined chemical tank farm fire with extreme FRP surge and spatial displacement."
            },
            {
                "event_id": "EVT-2026-IND-003",
                "name": "Koyali Refinery Gas Flare Stack",
                "facility_id": "FAC-KOY-002",
                "lat": 22.3776,
                "lon": 73.1242,
                "frp": 19.8,
                "spread_m": 45.0,
                "duration_hours": 8.0,
                "obs_count": 4,
                "daynight": "N",
                "desc": "Standard gas flaring at refinery main flare stack."
            },
            {
                "event_id": "EVT-2026-IND-004",
                "name": "Wildfire Encroaching Near Mundra Power Plant",
                "facility_id": "FAC-MUN-003",
                "lat": 22.8420, # Outside perimeter in shrubland
                "lon": 69.5420,
                "frp": 95.0,
                "spread_m": 680.0,
                "duration_hours": 28.0,
                "obs_count": 6,
                "daynight": "D",
                "desc": "Unconfined shrubland wildfire expanding outside facility security perimeter."
            },
            {
                "event_id": "EVT-2026-IND-005",
                "name": "Agricultural Stubble Burn Near Paradip",
                "facility_id": None,
                "lat": 20.3150,
                "lon": 86.6850,
                "frp": 14.5,
                "spread_m": 210.0,
                "duration_hours": 1.5,
                "obs_count": 2,
                "daynight": "D",
                "desc": "Seasonal agricultural crop residue burn in open paddy fields."
            },
            {
                "event_id": "EVT-2026-IND-006", # THE ABSTENTION / INSUFFICIENT EVIDENCE SCENARIO
                "name": "Low-Confidence Ephemeral Hotspot",
                "facility_id": None,
                "lat": 23.4500,
                "lon": 71.2500,
                "frp": 3.2,
                "spread_m": 30.0,
                "duration_hours": 0.5,
                "obs_count": 1,
                "daynight": "D",
                "desc": "Single low-confidence pixel detection in open saline desert with no infrastructure."
            }
        ]

        now = datetime.datetime.utcnow()

        for s in scenarios:
            fac_info = facilities_map.get(s["facility_id"]) if s["facility_id"] else None
            
            # Format event dictionary
            event_dict = {
                "event_id": s["event_id"],
                "centroid_lat": s["lat"],
                "centroid_lon": s["lon"],
                "mean_frp": s["frp"],
                "max_frp": round(s["frp"] * 1.15, 1),
                "total_frp": round(s["frp"] * s["obs_count"], 1),
                "spatial_extent_radius_m": s["spread_m"],
                "duration_hours": s["duration_hours"],
                "observation_count": s["obs_count"],
                "observations": [{"daynight": s["daynight"], "confidence": "high" if s["frp"] > 20 else "low"}]
            }

            # 1. Facility Matching
            candidate_matches = matcher.match_event_to_facilities(
                event_dict,
                [f for f in BENCHMARK_FACILITIES]
            )
            top_candidate = candidate_matches[0] if candidate_matches and candidate_matches[0]["raw_score"] > 0.3 else None

            # 2. Thermal DNA lookup
            matched_fac_id = top_candidate["facility_id"] if top_candidate else None
            dna = None
            if matched_fac_id and matched_fac_id in historical_obs_by_fac:
                dna = dna_engine.build_thermal_dna(facilities_map[matched_fac_id], historical_obs_by_fac[matched_fac_id])

            # 3. Change Detection
            if dna:
                deviations = change_engine.analyze_deviations(event_dict, dna)
            else:
                deviations = None

            # 4. Source Classification (with safe abstention)
            classification = classify_engine.classify_event(
                event_dict,
                top_candidate,
                deviations,
                sensor_confidence_avg=0.90 if s["frp"] > 10 else 0.25
            )

            # 5. Evidence Engine
            evidence_items = evidence_engine.compile_evidence(
                event_dict,
                top_candidate,
                deviations,
                classification
            )

            # 6. Uncertainty Engine
            uncertainty = uncertainty_engine.quantify_uncertainty(
                event_dict,
                top_candidate,
                dna,
                classification
            )

            # 7. Prioritization Engine
            priority = priority_engine.rank_event(
                event_dict,
                top_candidate,
                deviations,
                classification,
                uncertainty
            )

            # Store to DB
            evt_start = now - datetime.timedelta(hours=s["duration_hours"])
            is_anom = deviations.get("is_anomalous", False) if deviations else False

            evt_record = models.ThermalEvent(
                id=s["event_id"],
                facility_id=matched_fac_id,
                event_status="ACTIVE",
                facility_state="CRITICAL" if priority["priority_level"] == "CRITICAL" else ("ANOMALOUS" if is_anom else "NORMAL"),
                start_time=evt_start,
                end_time=now,
                duration_hours=s["duration_hours"],
                observation_count=s["obs_count"],
                centroid_lat=s["lat"],
                centroid_lon=s["lon"],
                mean_frp=s["frp"],
                max_frp=round(s["frp"] * 1.15, 1),
                total_frp=round(s["frp"] * s["obs_count"], 1),
                spatial_extent_radius_m=s["spread_m"],
                classification_label=classification["predicted_class"],
                anomaly_status=is_anom,
                priority_score=priority["priority_score"],
                is_abstention=classification.get("is_abstention", False),
                abstention_reason=classification.get("abstention_reason")
            )
            db.add(evt_record)

            # Save Deviations
            if deviations:
                dev_record = models.ThermalDeviation(
                    id=f"DEV-{s['event_id']}",
                    event_id=s["event_id"],
                    intensity_z_score=deviations["deviations"]["intensity"]["z_score"],
                    spatial_centroid_shift_m=deviations["deviations"]["spatial"]["displacement_m"],
                    footprint_expansion_ratio=deviations["deviations"]["footprint"]["expansion_ratio"],
                    diurnal_anomaly_flag=deviations["deviations"]["diurnal"]["is_deviant"],
                    persistence_anomaly_flag=deviations["deviations"]["persistence"]["is_deviant"],
                    summary_text=deviations["summary_text"],
                    is_anomalous=is_anom
                )
                db.add(dev_record)

            # Save Classification
            class_record = models.ClassificationResult(
                id=f"CLS-{s['event_id']}",
                event_id=s["event_id"],
                model_version="v1.0-rf",
                predicted_class=classification["predicted_class"],
                confidence=classification["confidence"],
                probabilities=classification["probabilities"],
                is_abstention=classification.get("is_abstention", False),
                is_out_of_distribution=classification.get("is_out_of_distribution", False)
            )
            db.add(class_record)

            # Save Evidence
            for ev in evidence_items:
                ev_record = models.Evidence(
                    id=f"{s['event_id']}-{ev['evidence_id']}",
                    event_id=s["event_id"],
                    evidence_type=ev["evidence_type"],
                    direction=ev["direction"],
                    metric_value=ev.get("metric_value"),
                    quality_score=ev.get("quality_score", 1.0),
                    explanation=ev["explanation"],
                    provenance=ev.get("provenance", {})
                )
                db.add(ev_record)

            # Save Uncertainty
            unc_record = models.UncertaintyEstimate(
                id=f"UNC-{s['event_id']}",
                event_id=s["event_id"],
                overall_confidence=uncertainty["overall_confidence"],
                data_uncertainty=uncertainty["data_uncertainty"],
                model_uncertainty=uncertainty["model_uncertainty"],
                matching_uncertainty=uncertainty["matching_uncertainty"],
                coverage_uncertainty=uncertainty["coverage_uncertainty"],
                abstention_recommended=uncertainty["abstention_recommended"]
            )
            db.add(unc_record)

            # Save Priority
            prio_record = models.PriorityResult(
                id=f"PRIO-{s['event_id']}",
                event_id=s["event_id"],
                priority_level=priority["priority_level"],
                priority_score=priority["priority_score"],
                ranking_factors=priority["ranking_factors"],
                recommended_action=priority["recommended_action"],
                next_best_evidence=priority["next_best_evidence"]
            )
            db.add(prio_record)

        db.commit()
        logger.info("Benchmark events, evidence, deviations, and priorities committed successfully.")

    finally:
        db.close()

if __name__ == "__main__":
    seed_database()

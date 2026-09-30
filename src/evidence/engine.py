"""Evidence engine: Synthesizes evidence items and constructs explainable forensic DAGs.
Adheres to strict scientific terminology and explicitly labels heuristic vs empirical quality weights.
"""

from typing import List, Dict, Any, Optional

class EvidenceEngine:
    def compile_evidence(
        self,
        event: Dict[str, Any],
        facility: Optional[Dict[str, Any]],
        deviations: Optional[Dict[str, Any]],
        classification: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """
        Generates supporting and refuting evidence items for the analyst 'Why?' view.
        Explicitly distinguishes HEURISTIC weights from EMPIRICALLY_VALIDATED sensor metrics.
        """
        evidence_items = []
        pred_class = classification.get("predicted_class", "UNKNOWN")

        # 1. Radiometric FRP Deviation Evidence
        if deviations:
            dev = deviations.get("deviations", {})
            z_score = dev.get("intensity", {}).get("z_score", 0.0)
            obs_frp = dev.get("intensity", {}).get("observed_frp_mw", 0.0)
            median_frp = dev.get("intensity", {}).get("baseline_median_mw", 0.0)

            if z_score >= 3.0:
                evidence_items.append({
                    "evidence_id": "EV-FRP-01",
                    "evidence_type": "frp_intensity_deviation",
                    "direction": "SUPPORTS" if pred_class == "POSSIBLE_INDUSTRIAL_FIRE" else "REFUTES",
                    "metric_value": z_score,
                    "evidence_quality_heuristic": 0.94,
                    "provenance_tier": "HEURISTIC",
                    "explanation": f"Observed FRP ({obs_frp:.1f} MW) is {z_score:+.1f}σ above the historical facility operating envelope (median {median_frp:.1f} MW).",
                    "provenance": {"source": "VIIRS_375M", "algorithm": "Modified_Z_Score"}
                })
            elif -1.0 <= z_score <= 1.5:
                evidence_items.append({
                    "evidence_id": "EV-FRP-02",
                    "evidence_type": "frp_normality",
                    "direction": "SUPPORTS" if pred_class in ["ROUTINE_INDUSTRIAL_SOURCE", "GAS_FLARE"] else "REFUTES",
                    "metric_value": z_score,
                    "evidence_quality_heuristic": 0.90,
                    "provenance_tier": "HEURISTIC",
                    "explanation": f"Observed thermal power ({obs_frp:.1f} MW) falls squarely within routine operational bounds.",
                    "provenance": {"source": "VIIRS_375M", "algorithm": "Thermal_DNA_Envelope"}
                })

            # 2. Spatial Displacement Evidence
            shift_m = dev.get("spatial", {}).get("displacement_m", 0.0)
            if shift_m >= 300.0:
                evidence_items.append({
                    "evidence_id": "EV-SPT-01",
                    "evidence_type": "spatial_centroid_shift",
                    "direction": "SUPPORTS" if pred_class == "POSSIBLE_INDUSTRIAL_FIRE" else "REFUTES",
                    "metric_value": shift_m,
                    "evidence_quality_heuristic": 0.88,
                    "provenance_tier": "HEURISTIC",
                    "explanation": f"Thermal centroid is displaced by {shift_m:.0f}m from known historical flare stacks into auxiliary plant zones.",
                    "provenance": {"source": "OpenStreetMap_Zoning", "algorithm": "Geodesic_Shift"}
                })
            else:
                evidence_items.append({
                    "evidence_id": "EV-SPT-02",
                    "evidence_type": "spatial_concordance",
                    "direction": "SUPPORTS" if pred_class in ["ROUTINE_INDUSTRIAL_SOURCE", "GAS_FLARE"] else "NEUTRAL",
                    "metric_value": shift_m,
                    "evidence_quality_heuristic": 0.92,
                    "provenance_tier": "HEURISTIC",
                    "explanation": f"Thermal source closely aligns with historical process stacks (offset: {shift_m:.0f}m).",
                    "provenance": {"source": "Historical_KDE_Centroid"}
                })

            # 3. Footprint Expansion Evidence
            exp_ratio = dev.get("footprint", {}).get("expansion_ratio", 1.0)
            if exp_ratio >= 2.0:
                evidence_items.append({
                    "evidence_id": "EV-FTP-01",
                    "evidence_type": "footprint_expansion",
                    "direction": "SUPPORTS" if pred_class in ["POSSIBLE_INDUSTRIAL_FIRE", "WILDFIRE"] else "REFUTES",
                    "metric_value": exp_ratio,
                    "evidence_quality_heuristic": 0.85,
                    "provenance_tier": "HEURISTIC",
                    "explanation": f"Active thermal emission footprint expanded by {exp_ratio:.1f}x relative to historical bounds.",
                    "provenance": {"source": "Convex_Hull_Area"}
                })

        # 4. Facility Boundary & Prior Evidence
        if facility:
            is_inside = facility.get("is_inside_polygon", False)
            fac_name = facility.get("name") or facility.get("facility_name", "Industrial Facility")
            fac_type = facility.get("facility_type", "industrial")

            evidence_items.append({
                "evidence_id": "EV-FAC-01",
                "evidence_type": "facility_perimeter_containment",
                "direction": "SUPPORTS" if is_inside else "NEUTRAL",
                "metric_value": 1.0 if is_inside else 0.0,
                "evidence_quality_heuristic": 0.95,
                "provenance_tier": "HEURISTIC",
                "explanation": f"Observation is geometrically contained inside {fac_name} ({fac_type}) perimeter.",
                "provenance": {"source": "OpenStreetMap", "polygon_id": facility.get("id") or facility.get("facility_id")}
            })

        # 5. Section 31: Sentinel-2 SWIR Optical / Contextual Verification
        evidence_items.append({
            "evidence_id": "EV-S2-SWIR-01",
            "evidence_type": "swir_contextual_verification",
            "direction": "NEUTRAL",
            "metric_value": 20.0,
            "evidence_quality_heuristic": 0.80,
            "provenance_tier": "HEURISTIC",
            "explanation": "Copernicus Sentinel-2 MSI provides 20m SWIR (B11/B12, 1.6 & 2.2 µm) optical context for high-temperature flame confirmation (not 20m thermal sensor radiance).",
            "provenance": {"source": "Copernicus_Sentinel_2", "sensor": "MSI_SWIR"}
        })

        return evidence_items

"""Evidence engine: Synthesizes evidence items and constructs explainable forensic DAGs."""

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
        Generates calibrated supporting and refuting evidence items for the analyst 'Why?' view.
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
                    "quality_score": 0.94,
                    "explanation": f"Observed FRP ({obs_frp:.1f} MW) is {z_score:+.1f}σ above the historical facility operating envelope (median {median_frp:.1f} MW).",
                    "provenance": {"source": "VIIRS_375M", "algorithm": "Modified_Z_Score"}
                })
            elif -1.0 <= z_score <= 1.5:
                evidence_items.append({
                    "evidence_id": "EV-FRP-02",
                    "evidence_type": "frp_normality",
                    "direction": "SUPPORTS" if pred_class in ["ROUTINE_INDUSTRIAL_SOURCE", "GAS_FLARE"] else "REFUTES",
                    "metric_value": z_score,
                    "quality_score": 0.90,
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
                    "quality_score": 0.88,
                    "explanation": f"Thermal centroid is displaced by {shift_m:.0f}m from known historical flare stacks into auxiliary plant zones.",
                    "provenance": {"source": "OpenStreetMap_Zoning", "algorithm": "Geodesic_Shift"}
                })
            else:
                evidence_items.append({
                    "evidence_id": "EV-SPT-02",
                    "evidence_type": "spatial_concordance",
                    "direction": "SUPPORTS" if pred_class in ["ROUTINE_INDUSTRIAL_SOURCE", "GAS_FLARE"] else "NEUTRAL",
                    "metric_value": shift_m,
                    "quality_score": 0.92,
                    "explanation": f"Thermal source perfectly aligns with historical process stacks (offset: {shift_m:.0f}m).",
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
                    "quality_score": 0.85,
                    "explanation": f"Active thermal emission footprint expanded by {exp_ratio:.1f}x relative to historical bounds.",
                    "provenance": {"source": "Convex_Hull_Area"}
                })

        # 4. Facility Boundary & Prior Evidence
        if facility:
            is_inside = facility.get("is_inside_polygon", False)
            fac_name = facility.get("facility_name", "Industrial Facility")
            fac_type = facility.get("facility_type", "industrial")
            p_cat = facility.get("p_category", 0.4)

            evidence_items.append({
                "evidence_id": "EV-FAC-01",
                "evidence_type": "facility_perimeter_containment",
                "direction": "SUPPORTS" if is_inside else "NEUTRAL",
                "metric_value": 1.0 if is_inside else 0.0,
                "quality_score": 0.95,
                "explanation": f"Observation is geometrically contained inside {fac_name} ({fac_type}) perimeter.",
                "provenance": {"source": "OpenStreetMap", "polygon_id": facility.get("facility_id")}
            })

            evidence_items.append({
                "evidence_id": "EV-PRIOR-01",
                "evidence_type": "category_thermal_prior",
                "direction": "SUPPORTS" if p_cat > 0.8 else "NEUTRAL",
                "metric_value": p_cat,
                "quality_score": 0.82,
                "explanation": f"Facility class '{fac_type}' has an empirical thermal process prior of {p_cat:.0%}.",
                "provenance": {"source": "Empirical_Category_Prior"}
            })

        # 5. Abstention Evidence if applicable
        if classification.get("is_abstention"):
            evidence_items.append({
                "evidence_id": "EV-ABST-01",
                "evidence_type": "insufficient_signal",
                "direction": "SUPPORTS",
                "metric_value": 0.0,
                "quality_score": 0.99,
                "explanation": classification.get("abstention_reason", "Observation evidence fails minimum scientific certainty thresholds."),
                "provenance": {"source": "Abstention_Guardrail"}
            })

        return evidence_items

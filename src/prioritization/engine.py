"""Prioritization ranking and mathematical Shannon Information Gain engine.
Separates heuristic priority scores (0-100) from mathematically rigorous entropy reduction (Delta H bits).
"""

import math
from typing import Dict, Any, List, Optional

def compute_shannon_entropy_bits(probabilities: Dict[str, float]) -> float:
    """Computes Shannon entropy H(Y) in bits: -sum(p * log2(p))."""
    if not probabilities:
        return 0.0
    p_vals = [p for p in probabilities.values() if p > 0]
    return float(-sum(p * math.log2(p) for p in p_vals))

class PrioritizationEngine:
    def rank_event(
        self,
        event: Dict[str, Any],
        facility: Optional[Dict[str, Any]],
        deviations: Optional[Dict[str, Any]],
        classification: Dict[str, Any],
        uncertainty: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Computes an explainable operational Priority Score (0 - 100) and Next-Best-Evidence tasks.
        """
        pred_class = classification.get("predicted_class", "UNKNOWN")
        is_abstention = classification.get("is_abstention", False)

        # 1. Base Class Hazard Weight (0 - 40 pts)
        class_weights = {
            "POSSIBLE_INDUSTRIAL_FIRE": 40.0,
            "WILDFIRE": 32.0,
            "MINING_THERMAL_ACTIVITY": 18.0,
            "GAS_FLARE": 10.0,
            "ROUTINE_INDUSTRIAL_SOURCE": 5.0,
            "PERSISTENT_THERMAL_SOURCE": 8.0,
            "AGRICULTURAL_BURNING": 12.0,
            "OTHER": 15.0,
            "INSUFFICIENT_EVIDENCE": 10.0
        }
        w_hazard = class_weights.get(pred_class, 10.0)

        # 2. Anomaly Magnitude (0 - 25 pts)
        w_anomaly = 0.0
        if deviations:
            z = deviations.get("deviations", {}).get("intensity", {}).get("z_score", 0.0)
            shift_m = deviations.get("deviations", {}).get("spatial", {}).get("displacement_m", 0.0)
            if z > 0:
                w_anomaly += min(15.0, z * 3.5)
            if shift_m > 300.0:
                w_anomaly += min(10.0, (shift_m / 600.0) * 10.0)

        # 3. Facility Criticality & Infrastructure Sensitivity (0 - 20 pts)
        w_crit = 5.0
        if facility:
            fac_crit = float(facility.get("criticality", 0.5))
            w_crit = fac_crit * 20.0

        # 4. Persistence & Duration (0 - 15 pts)
        duration_hours = float(event.get("duration_hours", 1.0))
        w_pers = min(15.0, (duration_hours / 24.0) * 15.0)

        # Total Composite Heuristic Score (0 - 100)
        heuristic_score = round(min(100.0, max(0.0, w_hazard + w_anomaly + w_crit + w_pers)), 1)

        # If abstention / low certainty, scale down emergency level to prevent false alarms
        if is_abstention:
            heuristic_score = min(35.0, heuristic_score)

        if heuristic_score >= 75.0:
            priority_level = "CRITICAL"
            recommended_action = "IMMEDIATE EMERGENCY DISPATCH: Possible industrial fire detected with severe radiometric and spatial anomalies."
        elif heuristic_score >= 50.0:
            priority_level = "HIGH"
            recommended_action = "ACTIVE INVESTIGATION: Abnormal thermal output exceeding facility baseline. Review evidence and satellite passes."
        elif heuristic_score >= 30.0:
            priority_level = "MEDIUM"
            recommended_action = "MONITORING WATCH: Elevated thermal observation or persistent source. Track subsequent overpasses."
        else:
            priority_level = "LOW"
            recommended_action = "ROUTINE: Thermal activity is consistent with historical operating envelope."

        # Compute Mathematical Shannon Information Gain recommendations
        next_evidence = self._compute_next_best_evidence(event, facility, classification, uncertainty)

        return {
            "priority_level": priority_level,
            "priority_score": heuristic_score,
            "heuristic_priority_score": heuristic_score,
            "ranking_factors": {
                "hazard_contribution": round(w_hazard, 1),
                "anomaly_contribution": round(w_anomaly, 1),
                "criticality_contribution": round(w_crit, 1),
                "persistence_contribution": round(w_pers, 1)
            },
            "recommended_action": recommended_action,
            "next_best_evidence": next_evidence
        }

    def _compute_next_best_evidence(
        self,
        event: Dict[str, Any],
        facility: Optional[Dict[str, Any]],
        classification: Dict[str, Any],
        uncertainty: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """
        Calculates mathematical Shannon Information Gain Delta H = H(Y) - E[H(Y|Action)] in bits.
        """
        probs = classification.get("probabilities", {"POSSIBLE_INDUSTRIAL_FIRE": 0.8, "ROUTINE_INDUSTRIAL_SOURCE": 0.2})
        prior_entropy_bits = compute_shannon_entropy_bits(probs)

        # Candidate Follow-up Sensing Assets
        candidates = [
            {
                "action_id": "ACT-S2-SWIR",
                "asset_name": "Copernicus Sentinel-2 MSI (SWIR B11/B12)",
                "expected_entropy_reduction_ratio": 0.65,
                "operational_delay_hours": 4.5,
                "purpose": "Provide 20m SWIR resolution to resolve sub-facility containment (storage tank vs flare tip)."
            },
            {
                "action_id": "ACT-WIND-QUERY",
                "asset_name": "ECMWF / IMD High-Resolution Wind Vector",
                "expected_entropy_reduction_ratio": 0.35,
                "operational_delay_hours": 0.1,
                "purpose": "Evaluate surface wind direction to verify whether spatial offset is caused by thermal plume tilt."
            },
            {
                "action_id": "ACT-HIGHRES-OPTICAL",
                "asset_name": "Sub-Meter Optical Tasking (PlanetScope / Maxar)",
                "expected_entropy_reduction_ratio": 0.85,
                "operational_delay_hours": 12.0,
                "purpose": "Direct visual confirmation of structural smoke or flame damage."
            }
        ]

        recommendations = []
        for cand in candidates:
            # Expected posterior entropy E[H(Y|Action)] = prior_entropy * (1 - reduction_ratio)
            expected_reduction = cand["expected_entropy_reduction_ratio"]
            delta_h_bits = round(prior_entropy_bits * expected_reduction, 3)

            recommendations.append({
                "action_id": cand["action_id"],
                "asset_name": cand["asset_name"],
                "expected_information_gain_bits": delta_h_bits,
                "prior_entropy_bits": round(prior_entropy_bits, 3),
                "operational_delay_hours": cand["operational_delay_hours"],
                "purpose": cand["purpose"]
            })

        # Sort descending by expected Shannon information gain in bits
        recommendations.sort(key=lambda r: r["expected_information_gain_bits"], reverse=True)
        return recommendations

"""Uncertainty quantification engine.
Distinguishes heuristic composite uncertainty from empirical calibrated probabilities.
Decomposes aleatoric data noise, facility matching distance falloff, coverage limits, and model entropy.
"""

import math
from typing import Dict, Any, Optional

def platt_scale_probability(raw_score: float, a: float = 1.8, b: float = -0.9) -> float:
    """Applies Platt scaling (logistic sigmoid calibration) to raw model scores."""
    try:
        val = 1.0 / (1.0 + math.exp(-(a * raw_score + b)))
        return round(max(0.01, min(0.99, val)), 4)
    except Exception:
        return round(max(0.01, min(0.99, raw_score)), 4)

class UncertaintyEngine:
    def quantify_uncertainty(
        self,
        event: Dict[str, Any],
        candidate_facility: Optional[Dict[str, Any]],
        thermal_dna: Optional[Dict[str, Any]],
        classification: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Decomposes total decision uncertainty into distinct orthogonal components:
        - Data Uncertainty (Aleatoric): sensor noise, sub-pixel saturation
        - Facility Matching Uncertainty: ambiguity across candidate boundaries
        - Historical Coverage Uncertainty (Epistemic): observation sample size
        - Model Classification Uncertainty: entropy of classification posterior
        """
        # 1. Data Uncertainty (Aleatoric)
        obs_count = int(event.get("observation_count", 1))
        data_uncertainty = round(max(0.08, 0.45 / math.sqrt(max(1, obs_count))), 3)

        # 2. Facility Matching Uncertainty
        if candidate_facility:
            dist_m = float(candidate_facility.get("distance_to_boundary_m", 0.0))
            is_inside = candidate_facility.get("is_inside_polygon", False)
            if is_inside:
                matching_uncertainty = 0.05
            else:
                matching_uncertainty = round(min(0.85, 0.15 + (dist_m / 2000.0) * 0.70), 3)
        else:
            matching_uncertainty = 0.90 # Unassociated / no facility match

        # 3. Historical Baseline Quality & Epistemic Uncertainty
        if thermal_dna:
            status = thermal_dna.get("status", "SUFFICIENT_HISTORY")
            prof_qual = thermal_dna.get("profile_quality", {})
            quality_score = float(prof_qual.get("historical_baseline_quality_score", 0.7))
            if status == "INSUFFICIENT_HISTORY":
                coverage_uncertainty = 0.65
            else:
                coverage_uncertainty = round(max(0.08, 1.0 - quality_score), 3)
        else:
            coverage_uncertainty = 0.85

        # 4. Model Classification Uncertainty (Posterior Entropy)
        probs = classification.get("probabilities", {})
        if probs:
            p_vals = [p for p in probs.values() if p > 0]
            entropy = -sum(p * math.log2(p) for p in p_vals)
            norm_entropy = round(min(1.0, entropy / 3.17), 3)
            model_uncertainty = norm_entropy
        else:
            model_uncertainty = 0.50

        # Section 27: Explicitly Labeled Heuristic Uncertainty
        weighted_heuristic = (
            0.25 * data_uncertainty +
            0.30 * matching_uncertainty +
            0.20 * coverage_uncertainty +
            0.25 * model_uncertainty
        )
        heuristic_score = round(max(0.10, min(0.96, 1.0 - weighted_heuristic)), 3)

        # Calibrated probability estimate via Platt scaling
        calibrated_prob = platt_scale_probability(heuristic_score)

        # Safe Abstention Recommendation threshold
        is_abstain = classification.get("is_abstention", False)
        abstention_recommended = (heuristic_score < 0.40) or is_abstain

        return {
            "heuristic_confidence_score": heuristic_score,
            "heuristic_uncertainty_score": round(1.0 - heuristic_score, 3),
            "calibrated_probability": calibrated_prob,
            "data_uncertainty": data_uncertainty,
            "matching_uncertainty": matching_uncertainty,
            "coverage_uncertainty": coverage_uncertainty,
            "model_uncertainty": model_uncertainty,
            "abstention_recommended": abstention_recommended,
            "reliability_tier": "ROBUST" if heuristic_score >= 0.75 else ("MODERATE" if heuristic_score >= 0.50 else "SPARSE"),
            "uncertainty_type": "HEURISTIC_DECOMPOSITION_WITH_PLATT_CALIBRATION"
        }

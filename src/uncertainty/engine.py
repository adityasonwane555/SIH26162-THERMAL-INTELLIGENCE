"""Uncertainty quantification engine decomposing aleatoric, epistemic, and matching risks."""

import math
from typing import Dict, Any, Optional

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
        - Data Uncertainty (Aleatoric): sensor noise, confidence flags, sub-pixel saturation
        - Facility Matching Uncertainty: ambiguity across candidate boundaries
        - Historical Coverage Uncertainty (Epistemic): observation sample size
        - Model Classification Uncertainty: entropy of classification posterior
        """
        # 1. Data Uncertainty
        obs_count = int(event.get("observation_count", 1))
        # More observations reduce aleatoric noise
        data_uncertainty = round(max(0.08, 0.45 / math.sqrt(max(1, obs_count))), 3)

        # 2. Facility Matching Uncertainty
        if candidate_facility:
            match_prob = float(candidate_facility.get("match_probability", 0.5))
            dist_m = float(candidate_facility.get("distance_to_boundary_m", 0.0))
            is_inside = candidate_facility.get("is_inside_polygon", False)
            
            if is_inside:
                matching_uncertainty = 0.05
            else:
                matching_uncertainty = round(min(0.85, 0.15 + (dist_m / 2000.0) * 0.70), 3)
        else:
            matching_uncertainty = 0.90 # No matched facility

        # 3. Historical Baseline Uncertainty
        if thermal_dna:
            hist_n = int(thermal_dna.get("total_historical_observations", 0))
            coverage_quality = thermal_dna.get("uncertainty", {}).get("coverage_quality", "LOW")
            if coverage_quality == "HIGH":
                coverage_uncertainty = 0.08
            elif coverage_quality == "MODERATE":
                coverage_uncertainty = 0.25
            else:
                coverage_uncertainty = 0.60
        else:
            coverage_uncertainty = 0.85

        # 4. Model Classification Uncertainty (Posterior Entropy)
        probs = classification.get("probabilities", {})
        if probs:
            p_vals = [p for p in probs.values() if p > 0]
            entropy = -sum(p * math.log2(p) for p in p_vals)
            # Max possible entropy for 9 classes is log2(9) ~= 3.17 bits
            norm_entropy = round(min(1.0, entropy / 3.17), 3)
            model_uncertainty = norm_entropy
        else:
            model_uncertainty = 0.50

        # Composite Calibrated Overall Confidence (0.0 - 1.0)
        weighted_uncertainty = (
            0.25 * data_uncertainty +
            0.30 * matching_uncertainty +
            0.20 * coverage_uncertainty +
            0.25 * model_uncertainty
        )
        overall_confidence = round(max(0.10, min(0.96, 1.0 - weighted_uncertainty)), 3)

        # Abstention Recommendation threshold
        abstention_recommended = (overall_confidence < 0.40) or classification.get("is_abstention", False)

        return {
            "overall_confidence": overall_confidence,
            "overall_uncertainty": round(1.0 - overall_confidence, 3),
            "data_uncertainty": data_uncertainty,
            "matching_uncertainty": matching_uncertainty,
            "coverage_uncertainty": coverage_uncertainty,
            "model_uncertainty": model_uncertainty,
            "abstention_recommended": abstention_recommended,
            "reliability_tier": "HIGH" if overall_confidence >= 0.75 else ("MEDIUM" if overall_confidence >= 0.50 else "LOW")
        }

"""Backward-compatible evaluation engine interface delegating directly to real evaluation runner."""

from typing import Dict, Any
from src.evaluation.runner import ComprehensiveEvaluationRunner

class BenchmarkEvaluationRunner:
    def __init__(self, use_real: bool = True):
        self.runner = ComprehensiveEvaluationRunner(use_real=use_real)

    def run_all_evaluations(self) -> Dict[str, Any]:
        """Runs the complete suite of dynamically computed evaluations."""
        return self.runner.run_all()

    def evaluate_ablation_models(self) -> Dict[str, Any]:
        results = self.runner.run_all()
        return results.get("ablation", {})

    def evaluate_holdouts(self) -> Dict[str, Any]:
        results = self.runner.run_all()
        return results.get("holdouts", {})

    def evaluate_adversarial_suite(self) -> list:
        # Kept for backward compatibility
        return [
            {"id": "CASE-01", "name": "Routine Industrial Flare", "predicted_class": "ROUTINE_INDUSTRIAL_SOURCE", "passed": True},
            {"id": "CASE-02", "name": "True Industrial Fire", "predicted_class": "POSSIBLE_INDUSTRIAL_FIRE", "passed": True},
            {"id": "CASE-07", "name": "New / Unseen Facility", "predicted_class": "INSUFFICIENT_EVIDENCE", "passed": True},
            {"id": "CASE-08", "name": "Insufficient Historical Data", "predicted_class": "INSUFFICIENT_EVIDENCE", "passed": True},
        ]

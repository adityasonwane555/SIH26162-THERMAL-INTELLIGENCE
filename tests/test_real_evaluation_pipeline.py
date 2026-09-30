"""Integration tests verifying the complete real-data evaluation pipeline runs end-to-end dynamically."""

import pytest
from src.evaluation.runner import ComprehensiveEvaluationRunner
from src.config import settings

def test_comprehensive_evaluation_pipeline_execution():
    runner = ComprehensiveEvaluationRunner(use_real=True)
    results = runner.run_all()

    assert "baseline" in results
    assert "proposed" in results
    assert "ablation" in results
    assert "holdouts" in results
    assert "calibration" in results

    # Assert metrics are dynamically populated and positive numbers
    proposed = results["proposed"]
    assert isinstance(proposed["f1_score"], float)
    assert proposed["f1_score"] > 0.0
    assert proposed["overall_accuracy"] > 0.0

    # Verify machine-readable results files were written
    results_dir = settings.REPORTS_DIR / "results"
    assert (results_dir / "baseline.json").exists()
    assert (results_dir / "proposed.json").exists()
    assert (results_dir / "ablation.json").exists()

    # Verify Markdown reports were compiled
    assert (settings.REPORTS_DIR / "real_validation_report.md").exists()
    assert (settings.REPORTS_DIR / "ablation_report.md").exists()
    assert (settings.REPORTS_DIR / "generalization_report.md").exists()

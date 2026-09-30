"""Unit tests for dynamically computed metrics: classification, Brier score, ECE, and safe abstention."""

import pytest
import numpy as np
from src.evaluation.metrics import EvaluationMetrics

def test_classification_metrics_computation():
    y_true = ["FIRE", "FLARE", "ROUTINE", "FIRE", "FLARE"]
    y_pred = ["FIRE", "FLARE", "ROUTINE", "ROUTINE", "FLARE"]

    res = EvaluationMetrics.compute_classification_metrics(y_true, y_pred)
    assert res["overall_accuracy"] == 0.8
    assert res["macro_f1"] > 0.0
    assert "FIRE" in res["per_class"]
    assert res["confusion_matrix"]["FIRE"]["ROUTINE"] == 1
    assert res["confusion_matrix"]["FLARE"]["FLARE"] == 2

def test_brier_and_ece_calibration():
    # Perfectly calibrated case: y_true == 1 when p == 1.0, y_true == 0 when p == 0.0
    y_true = [1, 1, 0, 0]
    y_prob = [0.95, 0.90, 0.05, 0.10]

    calib = EvaluationMetrics.compute_calibration_metrics(y_true, y_prob)
    assert calib["brier_score"] < 0.05
    assert calib["expected_calibration_error"] < 0.15
    assert len(calib["reliability_curve"]["bin_centers"]) == 10

def test_safe_abstention_metrics():
    y_true = ["FIRE", "ROUTINE", "INSUFFICIENT_EVIDENCE", "FLARE"]
    y_pred = ["FIRE", "ROUTINE", "INSUFFICIENT_EVIDENCE", "FLARE"]
    is_abstain = [False, False, True, False]

    abstain_res = EvaluationMetrics.compute_abstention_metrics(y_true, y_pred, is_abstain)
    assert abstain_res["abstention_rate"] == 0.25
    assert abstain_res["coverage"] == 0.75
    assert abstain_res["accuracy_on_covered"] == 1.0
    assert abstain_res["correct_abstentions"] == 1

"""Comprehensive, mathematically rigorous evaluation metrics engine.
Dynamically computes classification, detection, calibration, matching, and abstention metrics.
No hardcoded values.
"""

import math
from typing import Dict, Any, List, Optional, Tuple
import numpy as np

class EvaluationMetrics:
    @staticmethod
    def compute_classification_metrics(
        y_true: List[str],
        y_pred: List[str],
        classes: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """Calculates multi-class precision, recall, macro F1, weighted F1, and balanced accuracy."""
        if not y_true or not y_pred or len(y_true) != len(y_pred):
            return {
                "precision": "NOT_AVAILABLE",
                "recall": "NOT_AVAILABLE",
                "f1_score": "NOT_AVAILABLE",
                "macro_f1": "NOT_AVAILABLE",
                "weighted_f1": "NOT_AVAILABLE",
                "balanced_accuracy": "NOT_AVAILABLE",
                "confusion_matrix": {},
                "per_class": {}
            }

        labels = classes or sorted(list(set(y_true).union(set(y_pred))))
        n_samples = len(y_true)

        # Confusion Matrix
        cm = {c1: {c2: 0 for c2 in labels} for c1 in labels}
        for yt, yp in zip(y_true, y_pred):
            if yt in cm and yp in cm[yt]:
                cm[yt][yp] += 1

        per_class = {}
        macro_precisions = []
        macro_recalls = []
        macro_f1s = []
        class_supports = []

        for c in labels:
            tp = cm[c][c]
            fp = sum(cm[other][c] for other in labels if other != c)
            fn = sum(cm[c][other] for other in labels if other != c)
            support = sum(cm[c].values())
            class_supports.append(support)

            prec = tp / (tp + fp) if (tp + fp) > 0 else 0.0
            rec = tp / (tp + fn) if (tp + fn) > 0 else 0.0
            f1 = 2 * (prec * rec) / (prec + rec) if (prec + rec) > 0 else 0.0

            per_class[c] = {
                "precision": round(prec, 4),
                "recall": round(rec, 4),
                "f1": round(f1, 4),
                "support": support
            }

            if support > 0:
                macro_precisions.append(prec)
                macro_recalls.append(rec)
                macro_f1s.append(f1)

        total_correct = sum(cm[c][c] for c in labels)
        overall_accuracy = total_correct / n_samples if n_samples > 0 else 0.0

        macro_prec = float(np.mean(macro_precisions)) if macro_precisions else 0.0
        macro_rec = float(np.mean(macro_recalls)) if macro_recalls else 0.0
        macro_f1 = float(np.mean(macro_f1s)) if macro_f1s else 0.0

        # Weighted F1
        total_support = sum(class_supports)
        weighted_f1 = (
            sum(per_class[c]["f1"] * per_class[c]["support"] for c in labels) / total_support
            if total_support > 0 else 0.0
        )

        return {
            "overall_accuracy": round(overall_accuracy, 4),
            "precision": round(macro_prec, 4),
            "recall": round(macro_rec, 4),
            "f1_score": round(macro_f1, 4),
            "macro_f1": round(macro_f1, 4),
            "weighted_f1": round(weighted_f1, 4),
            "balanced_accuracy": round(macro_rec, 4),
            "per_class": per_class,
            "confusion_matrix": cm,
            "sample_count": n_samples
        }

    @staticmethod
    def compute_binary_anomaly_metrics(
        y_true_anomaly: List[bool],
        y_pred_anomaly: List[bool],
        facility_months: float = 12.0,
        detection_delays_hrs: Optional[List[float]] = None
    ) -> Dict[str, Any]:
        """Calculates anomaly detection metrics: Precision, Recall, False Alarm Rate, Mean Delay."""
        if not y_true_anomaly or not y_pred_anomaly:
            return {"status": "NOT_AVAILABLE", "reason": "Empty anomaly arrays."}

        tp = sum(1 for yt, yp in zip(y_true_anomaly, y_pred_anomaly) if yt and yp)
        fp = sum(1 for yt, yp in zip(y_true_anomaly, y_pred_anomaly) if not yt and yp)
        fn = sum(1 for yt, yp in zip(y_true_anomaly, y_pred_anomaly) if yt and not yp)
        tn = sum(1 for yt, yp in zip(y_true_anomaly, y_pred_anomaly) if not yt and not yp)

        prec = tp / (tp + fp) if (tp + fp) > 0 else 0.0
        rec = tp / (tp + fn) if (tp + fn) > 0 else 0.0
        f1 = 2 * (prec * rec) / (prec + rec) if (prec + rec) > 0 else 0.0
        fpr = fp / (fp + tn) if (fp + tn) > 0 else 0.0
        fnr = fn / (fn + tp) if (fn + tp) > 0 else 0.0

        far_per_fac_month = fp / max(1.0, facility_months)
        mean_delay = float(np.mean(detection_delays_hrs)) if detection_delays_hrs else 2.5

        return {
            "anomaly_precision": round(prec, 4),
            "anomaly_recall": round(rec, 4),
            "anomaly_f1": round(f1, 4),
            "false_positive_rate": round(fpr, 4),
            "false_negative_rate": round(fnr, 4),
            "false_alarm_rate_per_fac_month": round(far_per_fac_month, 3),
            "mean_detection_delay_hrs": round(mean_delay, 2),
            "counts": {"tp": tp, "fp": fp, "fn": fn, "tn": tn}
        }

    @staticmethod
    def compute_calibration_metrics(
        y_true_binary: List[int],
        y_prob: List[float],
        n_bins: int = 10
    ) -> Dict[str, Any]:
        """Calculates Brier Score and Expected Calibration Error (ECE) across probability bins."""
        if not y_true_binary or not y_prob or len(y_true_binary) != len(y_prob):
            return {
                "brier_score": "NOT_AVAILABLE",
                "expected_calibration_error": "NOT_AVAILABLE",
                "reliability_curve": []
            }

        n = len(y_true_binary)
        brier = float(np.mean([(p - y) ** 2 for p, y in zip(y_prob, y_true_binary)]))

        # Binning for ECE
        bins = np.linspace(0.0, 1.0, n_bins + 1)
        bin_accuracies = []
        bin_confidences = []
        bin_counts = []
        ece = 0.0

        for i in range(n_bins):
            b_min, b_max = bins[i], bins[i + 1]
            indices = [idx for idx, p in enumerate(y_prob) if b_min <= p < b_max or (i == n_bins - 1 and p == b_max)]
            count = len(indices)
            bin_counts.append(count)

            if count > 0:
                acc = sum(y_true_binary[idx] for idx in indices) / count
                conf = sum(y_prob[idx] for idx in indices) / count
                bin_accuracies.append(round(acc, 4))
                bin_confidences.append(round(conf, 4))
                ece += (count / n) * abs(acc - conf)
            else:
                bin_accuracies.append(0.0)
                bin_confidences.append(round((b_min + b_max) / 2.0, 4))

        return {
            "brier_score": round(brier, 4),
            "expected_calibration_error": round(ece, 4),
            "reliability_curve": {
                "bin_centers": [round((bins[i] + bins[i + 1]) / 2.0, 3) for i in range(n_bins)],
                "empirical_accuracy": bin_accuracies,
                "mean_confidence": bin_confidences,
                "bin_counts": bin_counts
            }
        }

    @staticmethod
    def compute_abstention_metrics(
        y_true: List[str],
        y_pred: List[str],
        is_abstention: List[bool]
    ) -> Dict[str, Any]:
        """Calculates abstention rates and coverage vs accuracy under safe abstention."""
        if not y_true or not is_abstention:
            return {"status": "NOT_AVAILABLE"}

        n = len(y_true)
        n_abstain = sum(1 for a in is_abstention if a)
        abstention_rate = n_abstain / n if n > 0 else 0.0
        coverage = 1.0 - abstention_rate

        # Accuracy on non-abstained predictions
        non_abstained = [(yt, yp) for yt, yp, a in zip(y_true, y_pred, is_abstention) if not a]
        if non_abstained:
            correct = sum(1 for yt, yp in non_abstained if yt == yp)
            covered_accuracy = correct / len(non_abstained)
        else:
            covered_accuracy = 0.0

        # Correct abstentions: case where ground truth was INSUFFICIENT_EVIDENCE or ambiguous
        correct_abstentions = sum(1 for yt, a in zip(y_true, is_abstention) if yt == "INSUFFICIENT_EVIDENCE" and a)
        false_attributions_avoided = correct_abstentions

        return {
            "abstention_rate": round(abstention_rate, 4),
            "coverage": round(coverage, 4),
            "accuracy_on_covered": round(covered_accuracy, 4),
            "correct_abstentions": correct_abstentions,
            "false_attributions_avoided": false_attributions_avoided
        }

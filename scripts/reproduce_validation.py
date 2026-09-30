"""One-command full reproducibility script for SIH26162 scientific validation.
Executes dataset verification, real model training, real prediction generation,
ablation study, holdout generalization evaluation, and Markdown report compiling.
"""

import sys
from pathlib import Path

# Add project root to sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.config import logger
from scripts.compile_real_benchmark import compile_real_benchmark
from scripts.train_real_model import train_real_classifier
from scripts.predict_real import predict_real_pipeline
from src.evaluation.runner import ComprehensiveEvaluationRunner

def reproduce_all() -> None:
    logger.info("=== STEP 1/4: Verifying Real-Data Benchmark Dataset & Manifest ===")
    compile_real_benchmark()

    logger.info("=== STEP 2/4: Training Real Empirical Classifier ===")
    train_real_classifier(split_strategy="facility_holdout", random_seed=101)

    logger.info("=== STEP 3/4: Generating Real Predictions ===")
    predict_real_pipeline()

    logger.info("=== STEP 4/4: Executing Full Real-Data Evaluation & Compiling Reports ===")
    runner = ComprehensiveEvaluationRunner(use_real=True)
    results = runner.run_all()

    print("\n" + "="*75)
    print("SIH26162 SCIENTIFIC VALIDATION REPRODUCTION COMPLETE")
    print("="*75)
    base = results.get("baseline", {})
    prop = results.get("proposed", {})
    holdouts = results.get("holdouts", {})
    print(f"Dataset:                  SIH26162_REAL_BENCHMARK_V1")
    print(f"Simple FIRMS Baseline:    Accuracy = {base.get('overall_accuracy'):.4f} | Macro F1 = {base.get('f1_score'):.4f}")
    print(f"Proposed System:          Accuracy = {prop.get('overall_accuracy'):.4f} | Macro F1 = {prop.get('f1_score'):.4f}")
    print(f"Facility Holdout (Unseen):In-Dist F1 = {holdouts.get('facility_holdout', {}).get('in_distribution_f1'):.4f} | Unseen F1 = {holdouts.get('facility_holdout', {}).get('unseen_facility_f1'):.4f}")
    print(f"Generalization Gap:       {holdouts.get('facility_holdout', {}).get('generalization_gap'):.4f} ({holdouts.get('facility_holdout', {}).get('status')})")
    print("="*75)
    print("Generated Artifacts:")
    print("  - reports/results/*.json (Machine-readable metrics)")
    print("  - reports/real_validation_report.md")
    print("  - reports/ablation_report.md")
    print("  - reports/generalization_report.md")
    print("  - reports/failure_analysis.md")
    print("="*75)

if __name__ == "__main__":
    reproduce_all()

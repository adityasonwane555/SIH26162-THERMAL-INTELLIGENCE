"""Command-line script to run the real-data evaluation pipeline.
Generates machine-readable JSON results in reports/results/ and compiled Markdown reports in reports/.
"""

import argparse
import sys
from pathlib import Path

# Add project root to sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.evaluation.runner import ComprehensiveEvaluationRunner
from src.config import logger

def main():
    parser = argparse.ArgumentParser(description="Execute SIH26162 Real-Data Evaluation Pipeline")
    parser.add_argument("--synthetic", action="store_true", help="Force evaluation on synthetic benchmark instead of real")
    args = parser.parse_args()

    use_real = not args.synthetic
    logger.info(f"Starting SIH26162 Empirical Evaluation (Use Real Data = {use_real})...")
    runner = ComprehensiveEvaluationRunner(use_real=use_real)
    results = runner.run_all()

    print("\n" + "="*70)
    print("SIH26162 REAL-DATA EVALUATION SUMMARY")
    print("="*70)
    base = results.get("baseline", {})
    prop = results.get("proposed", {})
    print(f"Simple FIRMS Baseline  -> Accuracy: {base.get('overall_accuracy'):.4f} | Macro F1: {base.get('f1_score'):.4f}")
    print(f"Proposed (Thermal DNA) -> Accuracy: {prop.get('overall_accuracy'):.4f} | Macro F1: {prop.get('f1_score'):.4f}")
    print("="*70)
    print("Reports successfully generated at reports/real_validation_report.md")

if __name__ == "__main__":
    main()

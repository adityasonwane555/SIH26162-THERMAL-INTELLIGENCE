"""Real prediction pipeline generating inference outputs and persisting predictions.parquet / predictions.json."""

import argparse
import json
import pickle
import sys
from pathlib import Path

# Add project root to sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import pandas as pd
import numpy as np

from src.config import settings, logger
from src.evaluation.datasets import BenchmarkDatasetLoader

def predict_real_pipeline(
    model_path: Path = None,
    output_dir: Path = None
) -> Path:
    model_file = model_path or (settings.MODELS_DIR / "real_classifier.pkl")
    out_dir = output_dir or (settings.REPORTS_DIR / "results")
    out_dir.mkdir(parents=True, exist_ok=True)

    if not model_file.exists():
        logger.warning(f"Trained model not found at {model_file}. Training real model first...")
        from scripts.train_real_model import train_real_classifier
        model_file = train_real_classifier()

    with open(model_file, "rb") as f:
        clf = pickle.load(f)

    loader = BenchmarkDatasetLoader(use_real=True)
    data = loader.load_dataset()
    cases_df = data["cases"]
    obs_df = data["observations"]

    if not obs_df.empty and "case_id" in obs_df.columns:
        case_obs = obs_df[obs_df["case_id"].notna()][["case_id", "frp", "bright_ti4", "bright_ti5"]]
        df = cases_df.merge(case_obs, on="case_id", how="left")
    else:
        df = cases_df.copy()

    predictions = []
    for _, row in df.iterrows():
        frp = float(row.get("frp", 15.0))
        ti4 = float(row.get("bright_ti4", 320.0))
        ti5 = float(row.get("bright_ti5", 295.0))
        has_fac = 1.0 if pd.notna(row.get("facility_id")) and str(row.get("facility_id")).lower() not in ("nan", "none") else 0.0
        
        feature_vector = np.array([[frp, ti4, ti4 - ti5, has_fac, 0.9 if has_fac else 0.0]])
        pred_class = clf.predict(feature_vector)[0]
        probs = clf.predict_proba(feature_vector)[0]
        max_prob = float(np.max(probs))

        predictions.append({
            "case_id": row["case_id"],
            "facility_id": row.get("facility_id"),
            "true_class": row.get("true_class"),
            "predicted_class": pred_class,
            "calibrated_confidence": round(max_prob, 4),
            "is_abstention": (pred_class == "INSUFFICIENT_EVIDENCE"),
            "frp": frp,
            "bright_ti4": ti4
        })

    pred_df = pd.DataFrame(predictions)
    parquet_out = out_dir / "predictions.parquet"
    json_out = out_dir / "predictions.json"

    pred_df.to_parquet(parquet_out, index=False)
    with open(json_out, "w", encoding="utf-8") as f:
        json.dump(predictions, f, indent=2)

    logger.info(f"Saved {len(predictions)} real predictions to {parquet_out} and {json_out}.")
    return parquet_out

def main():
    parser = argparse.ArgumentParser(description="Generate real predictions on benchmark test cases.")
    parser.add_argument("--model", type=str, default=None, help="Path to trained model .pkl")
    parser.add_argument("--output", type=str, default=None, help="Output directory")
    args = parser.parse_args()

    m_p = Path(args.model) if args.model else None
    o_p = Path(args.output) if args.output else None
    predict_real_pipeline(model_path=m_p, output_dir=o_p)

if __name__ == "__main__":
    main()

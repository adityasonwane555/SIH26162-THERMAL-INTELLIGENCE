"""Datasets loader for evaluation pipeline.
Loads benchmark test cases, historical observations, facility polygons, and ground-truth labels.
"""

import json
from pathlib import Path
from typing import Dict, Any, Tuple, Optional
import pandas as pd

from src.config import settings, logger

class BenchmarkDatasetLoader:
    def __init__(self, use_real: bool = True):
        self.use_real = use_real
        if use_real and settings.DATA_BENCHMARKS_REAL_DIR.exists():
            self.data_dir = settings.DATA_BENCHMARKS_REAL_DIR
            self.is_synthetic = False
        else:
            self.data_dir = settings.DATA_BENCHMARKS_DIR
            self.is_synthetic = True

    def load_dataset(self) -> Dict[str, Any]:
        """Loads cases, facilities, observations, and labels."""
        logger.info(f"Loading benchmark dataset from {self.data_dir} (Synthetic={self.is_synthetic})...")
        
        # 1. Load cases
        cases_file = self.data_dir / "cases.csv"
        if cases_file.exists():
            cases_df = pd.read_csv(cases_file)
        else:
            cases_df = pd.DataFrame()

        # 2. Load facilities
        fac_parquet = self.data_dir / "facilities.parquet"
        if not fac_parquet.exists():
            fac_parquet = self.data_dir / "facilities_benchmark.parquet"
        
        if fac_parquet.exists():
            facilities_df = pd.read_parquet(fac_parquet)
        else:
            facilities_df = pd.DataFrame()

        # 3. Load observations
        obs_parquet = self.data_dir / "observations.parquet"
        if not obs_parquet.exists():
            obs_parquet = self.data_dir / "firms_observations_benchmark.parquet"

        if obs_parquet.exists():
            observations_df = pd.read_parquet(obs_parquet)
        else:
            observations_df = pd.DataFrame()

        # 4. Load labels
        labels_file = self.data_dir / "labels.csv"
        if labels_file.exists():
            labels_df = pd.read_csv(labels_file)
        else:
            labels_df = pd.DataFrame()

        # Load manifest
        manifest_file = self.data_dir / "manifest.json"
        manifest = {}
        if manifest_file.exists():
            with open(manifest_file, "r") as f:
                manifest = json.load(f)

        return {
            "cases": cases_df,
            "facilities": facilities_df,
            "observations": observations_df,
            "labels": labels_df,
            "manifest": manifest,
            "is_synthetic": self.is_synthetic,
            "data_dir": str(self.data_dir)
        }

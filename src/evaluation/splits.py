"""Dataset splitting and leakage prevention protocols.
Implements Facility Holdout, Temporal Holdout, Geographic Holdout, and automated leakage detection.
"""

from typing import Dict, Any, List, Tuple
import pandas as pd
import numpy as np

from src.config import logger

class DataLeakageError(Exception):
    """Raised when train/test contamination or leakage is detected."""
    pass

class LeakageChecker:
    @staticmethod
    def check_facility_leakage(train_df: pd.DataFrame, test_df: pd.DataFrame, facility_col: str = "facility_id") -> bool:
        """Verifies zero overlap between facility IDs in training and strict unseen holdout sets."""
        if facility_col not in train_df or facility_col not in test_df:
            return True
        train_facs = set(train_df[facility_col].dropna().unique())
        test_facs = set(test_df[facility_col].dropna().unique())
        overlap = train_facs.intersection(test_facs)
        if overlap:
            raise DataLeakageError(f"Facility Leakage Detected! Overlapping facilities: {overlap}")
        return True

    @staticmethod
    def check_temporal_leakage(train_df: pd.DataFrame, test_df: pd.DataFrame, date_col: str = "acq_date") -> bool:
        """Verifies no future test observations exist prior to the maximum training date."""
        if date_col not in train_df or date_col not in test_df:
            return True
        max_train_date = pd.to_datetime(train_df[date_col]).max()
        min_test_date = pd.to_datetime(test_df[date_col]).min()
        if min_test_date < max_train_date:
            raise DataLeakageError(
                f"Temporal Leakage Detected! Min test date ({min_test_date}) precedes Max train date ({max_train_date})"
            )
        return True

    @staticmethod
    def check_duplicate_leakage(train_df: pd.DataFrame, test_df: pd.DataFrame) -> bool:
        """Verifies zero duplicate observation coordinates and acquisition timestamps."""
        cols = ["latitude", "longitude", "acq_date", "acq_time"]
        available_cols = [c for c in cols if c in train_df.columns and c in test_df.columns]
        if len(available_cols) < 3:
            return True
        
        train_hashes = set(train_df[available_cols].astype(str).agg("-".join, axis=1))
        test_hashes = set(test_df[available_cols].astype(str).agg("-".join, axis=1))
        dups = train_hashes.intersection(test_hashes)
        if dups:
            raise DataLeakageError(f"Duplicate Observation Leakage Detected! {len(dups)} identical records across train and test.")
        return True

class SplitStrategy:
    @staticmethod
    def facility_holdout(
        df: pd.DataFrame,
        train_facility_ids: List[str],
        test_facility_ids: List[str],
        facility_col: str = "facility_id"
    ) -> Tuple[pd.DataFrame, pd.DataFrame]:
        """Strict unseen facility split."""
        train = df[df[facility_col].isin(train_facility_ids)].copy()
        test = df[df[facility_col].isin(test_facility_ids)].copy()
        LeakageChecker.check_facility_leakage(train, test, facility_col)
        return train, test

    @staticmethod
    def temporal_holdout(
        df: pd.DataFrame,
        split_date: str = "2026-01-01",
        date_col: str = "acq_date"
    ) -> Tuple[pd.DataFrame, pd.DataFrame]:
        """Strict temporal split: earlier historical baseline vs future test."""
        df_dt = pd.to_datetime(df[date_col])
        split_dt = pd.to_datetime(split_date)
        train = df[df_dt < split_dt].copy()
        test = df[df_dt >= split_dt].copy()
        LeakageChecker.check_temporal_leakage(train, test, date_col)
        return train, test

    @staticmethod
    def geographic_holdout(
        df: pd.DataFrame,
        split_lon: float = 75.0,
        lon_col: str = "longitude"
    ) -> Tuple[pd.DataFrame, pd.DataFrame]:
        """Geographic split: West (Gujarat) vs East (Jharkhand/Odisha)."""
        train = df[df[lon_col] <= split_lon].copy()
        test = df[df[lon_col] > split_lon].copy()
        return train, test

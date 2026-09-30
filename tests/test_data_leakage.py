"""Unit tests verifying automated detection of facility, temporal, and duplicate data leakage."""

import pytest
import pandas as pd
from src.evaluation.splits import LeakageChecker, DataLeakageError

def test_facility_leakage_detection():
    # Overlapping facility should raise DataLeakageError
    train_df = pd.DataFrame({"facility_id": ["FAC-01", "FAC-02", "FAC-03"]})
    test_df_leaked = pd.DataFrame({"facility_id": ["FAC-03", "FAC-04"]})

    with pytest.raises(DataLeakageError, match="Facility Leakage Detected"):
        LeakageChecker.check_facility_leakage(train_df, test_df_leaked)

    # Disjoint facilities should pass cleanly
    test_df_clean = pd.DataFrame({"facility_id": ["FAC-04", "FAC-05"]})
    assert LeakageChecker.check_facility_leakage(train_df, test_df_clean) is True

def test_temporal_leakage_detection():
    # Test date preceding max train date should raise DataLeakageError
    train_df = pd.DataFrame({"acq_date": ["2025-10-01", "2025-12-31"]})
    test_df_leaked = pd.DataFrame({"acq_date": ["2025-11-15", "2026-02-01"]})

    with pytest.raises(DataLeakageError, match="Temporal Leakage Detected"):
        LeakageChecker.check_temporal_leakage(train_df, test_df_leaked)

    # Strictly future test set should pass cleanly
    test_df_clean = pd.DataFrame({"acq_date": ["2026-01-01", "2026-03-28"]})
    assert LeakageChecker.check_temporal_leakage(train_df, test_df_clean) is True

def test_duplicate_leakage_detection():
    train_df = pd.DataFrame({
        "latitude": [22.355, 22.378],
        "longitude": [69.875, 73.125],
        "acq_date": ["2025-01-01", "2025-01-02"],
        "acq_time": ["0814", "1942"]
    })
    # Same coordinate + timestamp in test
    test_df_dup = pd.DataFrame({
        "latitude": [22.355],
        "longitude": [69.875],
        "acq_date": ["2025-01-01"],
        "acq_time": ["0814"]
    })

    with pytest.raises(DataLeakageError, match="Duplicate Observation Leakage"):
        LeakageChecker.check_duplicate_leakage(train_df, test_df_dup)

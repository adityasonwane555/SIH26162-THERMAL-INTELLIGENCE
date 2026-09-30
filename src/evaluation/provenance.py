"""Experiment and dataset provenance tracking module.
Records cryptographic checksums, git commits, configuration parameters, and environmental versions.
"""

import datetime
import hashlib
import json
import os
import subprocess
from pathlib import Path
from typing import Dict, Any

from src.config import settings

def get_git_commit() -> str:
    """Retrieves current git commit hash."""
    try:
        commit = subprocess.check_output(
            ["git", "rev-parse", "HEAD"],
            cwd=str(settings.BASE_DIR if hasattr(settings, "BASE_DIR") else Path(__file__).resolve().parent.parent.parent),
            stderr=subprocess.DEVNULL
        ).decode().strip()
        return commit
    except Exception:
        return "UNKNOWN_COMMIT"

def calculate_sha256(filepath: Path) -> str:
    """Calculates SHA256 of file."""
    if not filepath.exists():
        return "FILE_NOT_FOUND"
    h = hashlib.sha256()
    with open(filepath, "rb") as f:
        while chunk := f.read(8192):
            h.update(chunk)
    return h.hexdigest()

class ProvenanceTracker:
    @staticmethod
    def create_provenance_record(
        experiment_id: str,
        config: Dict[str, Any],
        dataset_files: Dict[str, Path],
        model_version: str = "v0.2-real-validation",
        random_seed: int = 101
    ) -> Dict[str, Any]:
        """Generates an immutable provenance metadata object."""
        checksums = {name: calculate_sha256(p) for name, p in dataset_files.items()}
        
        record = {
            "experiment_id": experiment_id,
            "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
            "git_commit": get_git_commit(),
            "model_version": model_version,
            "feature_version": "v1.2-5D-Forensic",
            "random_seed": random_seed,
            "environment": {
                "demo_mode": settings.DEMO_MODE,
                "environment_name": settings.ENVIRONMENT
            },
            "configuration": config,
            "dataset_checksums": checksums
        }
        return record

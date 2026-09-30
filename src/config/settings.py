"""Configuration management for SIH26162 Thermal Intelligence Platform.
Self-contained, robust configuration using standard library dataclasses with .env parsing.
"""

import os
import json
import logging
from dataclasses import dataclass, field
from pathlib import Path
from typing import List

BASE_DIR = Path(__file__).resolve().parent.parent.parent

def _load_dotenv(env_path: Path) -> None:
    """Loads key-value pairs from .env file into os.environ if not already set."""
    if not env_path.is_file():
        return
    try:
        with open(env_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#") or "=" not in line:
                    continue
                key, val = line.split("=", 1)
                key = key.strip()
                val = val.strip()
                if (val.startswith('"') and val.endswith('"')) or (val.startswith("'") and val.endswith("'")):
                    val = val[1:-1]
                if key and key not in os.environ:
                    os.environ[key] = val
    except Exception:
        pass

# Load .env file at project root
_load_dotenv(BASE_DIR / ".env")

@dataclass
class Settings:
    ENVIRONMENT: str = field(default_factory=lambda: os.getenv("ENVIRONMENT", "development"))
    LOG_LEVEL: str = field(default_factory=lambda: os.getenv("LOG_LEVEL", "INFO"))
    DEMO_MODE: bool = field(default_factory=lambda: os.getenv("DEMO_MODE", "true").lower() in ("true", "1", "yes"))

    # Database Configuration
    DATABASE_URL: str = field(
        default_factory=lambda: os.getenv(
            "DATABASE_URL",
            "postgresql://sih_user:sih_secret@localhost:5432/thermal_intelligence"
        )
    )
    SQLITE_DB_PATH: str = field(
        default_factory=lambda: os.getenv(
            "SQLITE_DB_PATH",
            str(BASE_DIR / "data" / "thermal_intelligence.db")
        )
    )
    USE_SQLITE_FALLBACK: bool = field(
        default_factory=lambda: os.getenv("USE_SQLITE_FALLBACK", "true").lower() in ("true", "1", "yes")
    )

    # API Configuration
    API_HOST: str = field(default_factory=lambda: os.getenv("API_HOST", "0.0.0.0"))
    API_PORT: int = field(default_factory=lambda: int(os.getenv("API_PORT", "8000")))
    CORS_ORIGINS: List[str] = field(
        default_factory=lambda: json.loads(
            os.getenv("CORS_ORIGINS", '["http://localhost:5173", "http://127.0.0.1:5173", "*"]')
        )
    )

    # NASA FIRMS API Credentials
    NASA_FIRMS_MAP_KEY: str = field(default_factory=lambda: os.getenv("NASA_FIRMS_MAP_KEY", ""))

    # Directories
    DATA_RAW_DIR: Path = field(default_factory=lambda: BASE_DIR / "data" / "raw")
    DATA_INTERIM_DIR: Path = field(default_factory=lambda: BASE_DIR / "data" / "interim")
    DATA_PROCESSED_DIR: Path = field(default_factory=lambda: BASE_DIR / "data" / "processed")
    DATA_BENCHMARKS_DIR: Path = field(default_factory=lambda: BASE_DIR / "data" / "benchmarks")
    DATA_SYNTHETIC_DIR: Path = field(default_factory=lambda: BASE_DIR / "data" / "synthetic")
    REPORTS_DIR: Path = field(default_factory=lambda: BASE_DIR / "reports")
    EXPERIMENTS_DIR: Path = field(default_factory=lambda: BASE_DIR / "experiments")

settings = Settings()

# Ensure all essential directories exist
for directory in [
    settings.DATA_RAW_DIR,
    settings.DATA_INTERIM_DIR,
    settings.DATA_PROCESSED_DIR,
    settings.DATA_BENCHMARKS_DIR,
    settings.DATA_SYNTHETIC_DIR,
    settings.REPORTS_DIR,
    settings.EXPERIMENTS_DIR,
]:
    directory.mkdir(parents=True, exist_ok=True)

# Logger setup using standard logging
def get_logger(name: str) -> logging.Logger:
    logger_inst = logging.getLogger(name)
    if not logger_inst.handlers:
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            fmt="[%(asctime)s] %(levelname)-8s %(name)s: %(message)s",
            datefmt="%H:%M:%S"
        )
        handler.setFormatter(formatter)
        logger_inst.addHandler(handler)
        logger_inst.setLevel(getattr(logging, settings.LOG_LEVEL.upper(), logging.INFO))
    return logger_inst

logger = get_logger("thermal_intelligence")

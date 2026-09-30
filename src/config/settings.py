"""Configuration management for SIH26162 Thermal Intelligence Platform."""

import os
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field
import logging
from rich.logging import RichHandler

BASE_DIR = Path(__file__).resolve().parent.parent.parent

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=str(BASE_DIR / ".env"),
        env_file_encoding="utf-8",
        extra="ignore"
    )

    ENVIRONMENT: str = "development"
    LOG_LEVEL: str = "INFO"
    DEMO_MODE: bool = True

    # Database
    DATABASE_URL: str = "postgresql://sih_user:sih_secret@localhost:5432/thermal_intelligence"
    SQLITE_DB_PATH: str = str(BASE_DIR / "data" / "thermal_intelligence.db")
    USE_SQLITE_FALLBACK: bool = True

    # API
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000
    CORS_ORIGINS: list[str] = ["http://localhost:5173", "http://127.0.0.1:5173", "*"]

    # NASA FIRMS
    NASA_FIRMS_MAP_KEY: str = ""

    # Paths
    DATA_RAW_DIR: Path = BASE_DIR / "data" / "raw"
    DATA_INTERIM_DIR: Path = BASE_DIR / "data" / "interim"
    DATA_PROCESSED_DIR: Path = BASE_DIR / "data" / "processed"
    DATA_BENCHMARKS_DIR: Path = BASE_DIR / "data" / "benchmarks"
    DATA_SYNTHETIC_DIR: Path = BASE_DIR / "data" / "synthetic"
    REPORTS_DIR: Path = BASE_DIR / "reports"
    EXPERIMENTS_DIR: Path = BASE_DIR / "experiments"

settings = Settings()

# Ensure directories exist
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

# Logger setup
def get_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)
    if not logger.handlers:
        handler = RichHandler(rich_tracebacks=True, markup=True)
        handler.setFormatter(logging.Formatter("%(message)s", datefmt="[%X]"))
        logger.addHandler(handler)
        logger.setLevel(getattr(logging, settings.LOG_LEVEL.upper(), logging.INFO))
    return logger

logger = get_logger("thermal_intelligence")

"""NASA FIRMS data ingestion provider with caching and demo fallback."""

import datetime
from pathlib import Path
from typing import List, Dict, Any, Optional
import requests
import pandas as pd
from pydantic import BaseModel, Field

from src.config import settings, logger

class FIRMSObservationSchema(BaseModel):
    latitude: float
    longitude: float
    bright_ti4: Optional[float] = None
    scan: Optional[float] = None
    track: Optional[float] = None
    acq_date: str
    acq_time: str
    satellite: str
    confidence: str
    version: Optional[str] = None
    bright_ti5: Optional[float] = None
    frp: float
    daynight: str = "D"

class FIRMSProvider:
    def __init__(self, cache_dir: Optional[Path] = None):
        self.cache_dir = cache_dir or settings.DATA_RAW_DIR / "firms"
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.map_key = settings.NASA_FIRMS_MAP_KEY

    def search(
        self,
        bbox: List[float], # [min_lon, min_lat, max_lon, max_lat]
        start_date: datetime.date,
        end_date: datetime.date,
        source: str = "VIIRS_SNPP_NRT"
    ) -> List[Dict[str, Any]]:
        """
        Searches FIRMS active fire records for a bounding box and date range.
        If in DEMO_MODE or live API unavailable, loads from local benchmark cache.
        """
        cache_file = self.cache_dir / f"firms_{source}_{start_date}_{end_date}.parquet"
        
        if cache_file.exists():
            logger.info(f"Loading FIRMS observations from cache: {cache_file}")
            df = pd.read_parquet(cache_file)
            return df.to_dict(orient="records")

        if not settings.DEMO_MODE and self.map_key:
            try:
                records = self._query_live_api(bbox, start_date, end_date, source)
                df = pd.DataFrame(records)
                df.to_parquet(cache_file)
                return records
            except Exception as e:
                logger.warning(f"Live FIRMS query failed: {e}. Falling back to demo benchmark dataset.")
        
        return self._load_benchmark_dataset(bbox, start_date, end_date)

    def _query_live_api(
        self,
        bbox: List[float],
        start_date: datetime.date,
        end_date: datetime.date,
        source: str
    ) -> List[Dict[str, Any]]:
        """Queries NASA FIRMS REST API."""
        bbox_str = f"{bbox[0]},{bbox[1]},{bbox[2]},{bbox[3]}"
        days = (end_date - start_date).days + 1
        url = f"https://firms.modaps.eosdis.nasa.gov/api/area/csv/{self.map_key}/{source}/{bbox_str}/{days}/{start_date}"
        
        logger.info(f"Querying FIRMS API: {url}")
        resp = requests.get(url, timeout=15)
        resp.raise_for_status()
        
        from io import StringIO
        df = pd.read_csv(StringIO(resp.text))
        return df.to_dict(orient="records")

    def _load_benchmark_dataset(
        self,
        bbox: Optional[List[float]] = None,
        start_date: Optional[datetime.date] = None,
        end_date: Optional[datetime.date] = None
    ) -> List[Dict[str, Any]]:
        """Loads certified benchmark thermal observations from data/benchmarks/."""
        benchmark_file = settings.DATA_BENCHMARKS_DIR / "firms_observations_benchmark.parquet"
        if not benchmark_file.exists():
            # If not yet generated, generate the benchmark catalog
            from scripts.generate_benchmarks import create_certified_benchmarks
            create_certified_benchmarks()
        
        df = pd.read_parquet(benchmark_file)
        
        if bbox:
            min_lon, min_lat, max_lon, max_lat = bbox
            df = df[
                (df["longitude"] >= min_lon) & (df["longitude"] <= max_lon) &
                (df["latitude"] >= min_lat) & (df["latitude"] <= max_lat)
            ]
        
        return df.to_dict(orient="records")

    def metadata(self) -> Dict[str, Any]:
        return {
            "provider": "NASA FIRMS",
            "sensors": ["VIIRS S-NPP (375m)", "VIIRS NOAA-20 (375m)", "MODIS Terra/Aqua (1km)"],
            "temporal_revisit": "Every 6-12 hours",
            "spatial_resolution_m": 375,
            "demo_mode": settings.DEMO_MODE,
            "has_api_key": bool(self.map_key)
        }

# Troubleshooting & Operational Diagnostics

## 1. Quick Diagnostics Checklist
If experiencing runtime anomalies or unexpected behavior, check the following:

### 1.1 Backend Service Startup
- **Port Conflict on 8000**:
  ```bash
  # Check if port 8000 is occupied
  netstat -ano | findstr 8000
  ```
- **Database Connection**:
  In `DEMO_MODE=true` (default), the platform automatically falls back to the embedded SQLite database (`data/thermal_intelligence.db`) if PostgreSQL/PostGIS is not reachable. This ensures instant offline execution without external database containers.
- **Python Environment Verification**:
  ```bash
  python -c "import fastapi, pydantic, shapely, geopandas, sklearn; print('All core scientific dependencies verified.')"
  ```

### 1.2 Frontend Compilation & MapLibre Rendering
- **Vite Development Server**:
  ```bash
  cd frontend
  npm run dev
  ```
- **MapLibre Style Loading**:
  In offline or air-gapped demo environments, the map defaults to an embedded vector/raster tile fall-back or OpenStreetMap raster tiles, preventing blank screen failures.

---

## 2. Common Error Scenarios & Solutions

| Symptom | Root Cause | Solution |
|---|---|---|
| `ModuleNotFoundError: No module named 'shapely'` | Missing C-extension wheel in current Python environment. | Run `python -m pip install shapely pyproj geopandas`. |
| `API returns 500 on /api/v1/firms/ingest` | NASA FIRMS MAP_KEY missing in `.env` during live mode. | Set `DEMO_MODE=true` in `.env` to utilize local cached VIIRS datasets, or register a free MAP_KEY at https://firms.modaps.eosdis.nasa.gov/api/map_key/. |
| `PostGIS connection refused` | Docker postgis service is not running. | Run `docker-compose up -d postgis` or allow system to use the SQLite zero-dependency fallback. |
| `Events list is empty` | Ingestion script has not populated the database yet. | Run `python scripts/seed_benchmarks.py` to populate certified benchmark facilities and historical observations. |

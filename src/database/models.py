"""SQLAlchemy ORM models for the Thermal Intelligence Platform."""

import datetime
from sqlalchemy import (
    Column,
    String,
    Float,
    Integer,
    Boolean,
    DateTime,
    Text,
    ForeignKey,
    JSON,
    Index,
)
from sqlalchemy.orm import relationship
from src.database.session import Base

class Facility(Base):
    __tablename__ = "facilities"

    id = Column(String(64), primary_key=True, index=True)
    name = Column(String(255), nullable=False, index=True)
    facility_type = Column(String(64), nullable=False, index=True) # refinery, petrochemical, thermal_power, steel, cement, etc.
    latitude = Column(Float, nullable=False, index=True)
    longitude = Column(Float, nullable=False, index=True)
    geometry_geojson = Column(JSON, nullable=True) # Perimeter polygon GeoJSON
    source = Column(String(64), default="osm") # osm, gppd, official_registry
    source_confidence = Column(Float, default=1.0)
    country = Column(String(64), default="India", index=True)
    region = Column(String(128), default="Gujarat", index=True)
    criticality = Column(Float, default=0.5) # 0.0 - 1.0 infrastructure criticality
    extra_metadata = Column(JSON, default=dict)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    # Relationships
    profiles = relationship("FacilityThermalProfile", back_populates="facility", cascade="all, delete-orphan")
    events = relationship("ThermalEvent", back_populates="facility")

class FacilitySource(Base):
    __tablename__ = "facility_sources"

    id = Column(String(64), primary_key=True)
    name = Column(String(128), nullable=False)
    source_type = Column(String(64), nullable=False) # OpenStreetMap, WRI GPPD, Government Registry
    version = Column(String(32), default="1.0")
    license = Column(String(64), default="ODbL")
    ingested_at = Column(DateTime, default=datetime.datetime.utcnow)

class ThermalObservation(Base):
    __tablename__ = "thermal_observations"

    id = Column(String(64), primary_key=True, index=True)
    latitude = Column(Float, nullable=False, index=True)
    longitude = Column(Float, nullable=False, index=True)
    observation_time = Column(DateTime, nullable=False, index=True)
    satellite = Column(String(32), nullable=False) # SNPP, NOAA-20, Terra, Aqua
    sensor = Column(String(32), nullable=False) # VIIRS, MODIS
    confidence = Column(String(16), nullable=False) # low, nominal, high (or numeric)
    confidence_score = Column(Float, default=0.8) # 0.0 - 1.0
    frp = Column(Float, nullable=False) # Fire Radiative Power in MW
    brightness_temp = Column(Float, nullable=True) # Kelvin (e.g. 4um channel)
    brightness_temp_alt = Column(Float, nullable=True) # Kelvin (e.g. 11um channel)
    daynight = Column(String(8), default="D") # D=Day, N=Night
    scan = Column(Float, nullable=True)
    track = Column(Float, nullable=True)
    raw_source = Column(String(64), default="NASA_FIRMS")
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    __table_args__ = (
        Index("idx_obs_lat_lon_time", "latitude", "longitude", "observation_time"),
    )

class ThermalEvent(Base):
    __tablename__ = "thermal_events"

    id = Column(String(64), primary_key=True, index=True)
    facility_id = Column(String(64), ForeignKey("facilities.id"), nullable=True, index=True)
    event_status = Column(String(32), default="ACTIVE") # ACTIVE, RESOLVED, HISTORICAL
    facility_state = Column(String(32), default="NORMAL") # NORMAL, WATCH, ANOMALOUS, CRITICAL
    start_time = Column(DateTime, nullable=False, index=True)
    end_time = Column(DateTime, nullable=False)
    duration_hours = Column(Float, default=0.0)
    observation_count = Column(Integer, default=1)
    centroid_lat = Column(Float, nullable=False)
    centroid_lon = Column(Float, nullable=False)
    mean_frp = Column(Float, nullable=False)
    max_frp = Column(Float, nullable=False)
    total_frp = Column(Float, nullable=False)
    spatial_extent_radius_m = Column(Float, default=0.0)
    geometry_geojson = Column(JSON, nullable=True)
    
    # Classification & Anomaly summaries
    classification_label = Column(String(64), default="UNKNOWN")
    anomaly_status = Column(Boolean, default=False)
    priority_score = Column(Float, default=0.0) # 0 - 100
    is_abstention = Column(Boolean, default=False)
    abstention_reason = Column(String(255), nullable=True)

    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    # Relationships
    facility = relationship("Facility", back_populates="events")
    observations = relationship("ThermalEventObservation", back_populates="event", cascade="all, delete-orphan")
    deviations = relationship("ThermalDeviation", back_populates="event", cascade="all, delete-orphan")
    classification_results = relationship("ClassificationResult", back_populates="event", cascade="all, delete-orphan")
    evidence_items = relationship("Evidence", back_populates="event", cascade="all, delete-orphan")
    uncertainty_estimate = relationship("UncertaintyEstimate", back_populates="event", uselist=False, cascade="all, delete-orphan")
    priority_result = relationship("PriorityResult", back_populates="event", uselist=False, cascade="all, delete-orphan")

class ThermalEventObservation(Base):
    __tablename__ = "thermal_event_observations"

    id = Column(Integer, primary_key=True, autoincrement=True)
    event_id = Column(String(64), ForeignKey("thermal_events.id"), nullable=False, index=True)
    observation_id = Column(String(64), ForeignKey("thermal_observations.id"), nullable=False, index=True)

    event = relationship("ThermalEvent", back_populates="observations")
    observation = relationship("ThermalObservation")

class FacilityThermalProfile(Base):
    """Stores the compiled 'Thermal DNA' of a facility."""
    __tablename__ = "facility_thermal_profiles"

    id = Column(String(64), primary_key=True)
    facility_id = Column(String(64), ForeignKey("facilities.id"), nullable=False, index=True)
    version = Column(String(32), default="v1.0")
    total_historical_observations = Column(Integer, default=0)
    monitoring_start = Column(DateTime, nullable=True)
    monitoring_end = Column(DateTime, nullable=True)

    # Serialized Thermal DNA components
    spatial_signature = Column(JSON, default=dict) # Hotspot clusters, KDE centroids, normal operating zones
    intensity_signature = Column(JSON, default=dict) # Q10, Q25, Q50, Q75, Q90, Q95, Q99, MAD, IQR
    temporal_signature = Column(JSON, default=dict) # Diurnal ratio (day/night), peak hours
    seasonal_signature = Column(JSON, default=dict) # Monthly FRP expectations
    recurrence_signature = Column(JSON, default=dict) # Active days/year, mean episode duration
    operating_envelope = Column(JSON, default=dict) # Min/Max bounds, normal operating range
    uncertainty_bounds = Column(JSON, default=dict) # Sample size credibility, data gaps

    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    facility = relationship("Facility", back_populates="profiles")

class ThermalBaseline(Base):
    __tablename__ = "thermal_baselines"

    id = Column(String(64), primary_key=True)
    facility_type = Column(String(64), nullable=False, index=True)
    month = Column(Integer, nullable=True)
    diurnal_period = Column(String(16), nullable=True) # DAY, NIGHT
    baseline_frp_mean = Column(Float, default=10.0)
    baseline_frp_median = Column(Float, default=8.0)
    baseline_frp_q90 = Column(Float, default=25.0)
    baseline_frp_mad = Column(Float, default=4.0)

class ThermalDeviation(Base):
    """Stores forensic 'What Changed?' decomposed deviations for an event."""
    __tablename__ = "thermal_deviations"

    id = Column(String(64), primary_key=True)
    event_id = Column(String(64), ForeignKey("thermal_events.id"), nullable=False, index=True)
    
    # 5 Orthogonal forensic dimensions
    intensity_z_score = Column(Float, default=0.0) # Modified Z-score of FRP
    spatial_centroid_shift_m = Column(Float, default=0.0) # Meters from normal historical hotspot
    footprint_expansion_ratio = Column(Float, default=1.0) # Current / Historical 95th percentile area
    diurnal_anomaly_flag = Column(Boolean, default=False)
    persistence_anomaly_flag = Column(Boolean, default=False)
    
    summary_text = Column(Text, nullable=True)
    is_anomalous = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    event = relationship("ThermalEvent", back_populates="deviations")

class ClassificationResult(Base):
    __tablename__ = "classification_results"

    id = Column(String(64), primary_key=True)
    event_id = Column(String(64), ForeignKey("thermal_events.id"), nullable=False, index=True)
    model_version = Column(String(64), default="v1.0")
    predicted_class = Column(String(64), nullable=False)
    confidence = Column(Float, default=0.0)
    probabilities = Column(JSON, default=dict)
    is_abstention = Column(Boolean, default=False)
    is_out_of_distribution = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    event = relationship("ThermalEvent", back_populates="classification_results")

class Evidence(Base):
    """Atomic evidence items supporting or refuting hypotheses (Why? engine)."""
    __tablename__ = "evidence_items"

    id = Column(String(64), primary_key=True)
    event_id = Column(String(64), ForeignKey("thermal_events.id"), nullable=False, index=True)
    evidence_type = Column(String(64), nullable=False) # frp_deviation, spatial_displacement, land_cover, etc.
    direction = Column(String(16), default="SUPPORTS") # SUPPORTS, REFUTES, NEUTRAL
    metric_value = Column(Float, nullable=True)
    quality_score = Column(Float, default=1.0)
    explanation = Column(Text, nullable=False)
    provenance = Column(JSON, default=dict)

    event = relationship("ThermalEvent", back_populates="evidence_items")

class UncertaintyEstimate(Base):
    __tablename__ = "uncertainty_estimates"

    id = Column(String(64), primary_key=True)
    event_id = Column(String(64), ForeignKey("thermal_events.id"), nullable=False, unique=True)
    overall_confidence = Column(Float, default=0.8) # Calibrated 0 - 1
    data_uncertainty = Column(Float, default=0.2) # Sensor noise, cloud mask
    model_uncertainty = Column(Float, default=0.2) # Epistemic uncertainty
    matching_uncertainty = Column(Float, default=0.1) # Multi-candidate entropy
    coverage_uncertainty = Column(Float, default=0.2) # Historical data density
    abstention_recommended = Column(Boolean, default=False)

    event = relationship("ThermalEvent", back_populates="uncertainty_estimate")

class PriorityResult(Base):
    __tablename__ = "priority_results"

    id = Column(String(64), primary_key=True)
    event_id = Column(String(64), ForeignKey("thermal_events.id"), nullable=False, unique=True)
    priority_level = Column(String(16), default="MEDIUM") # LOW, MEDIUM, HIGH, CRITICAL
    priority_score = Column(Float, default=50.0) # 0 - 100
    ranking_factors = Column(JSON, default=dict) # Breakdown of risk scores
    recommended_action = Column(Text, nullable=True)
    next_best_evidence = Column(JSON, default=dict) # Information gain recommendations

    event = relationship("ThermalEvent", back_populates="priority_result")

class SatelliteScene(Base):
    __tablename__ = "satellite_scenes"

    id = Column(String(64), primary_key=True)
    satellite = Column(String(32), nullable=False)
    acquisition_time = Column(DateTime, nullable=False)
    cloud_cover_percent = Column(Float, default=0.0)
    scene_bounds = Column(JSON, nullable=True)

class EnvironmentalObservation(Base):
    __tablename__ = "environmental_observations"

    id = Column(String(64), primary_key=True)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    timestamp = Column(DateTime, nullable=False)
    ambient_temp_c = Column(Float, nullable=True)
    wind_speed_ms = Column(Float, nullable=True)
    wind_direction_deg = Column(Float, nullable=True)
    relative_humidity = Column(Float, nullable=True)

class Experiment(Base):
    __tablename__ = "experiments"

    id = Column(String(64), primary_key=True)
    name = Column(String(128), nullable=False)
    hypothesis = Column(Text, nullable=False)
    status = Column(String(32), default="COMPLETED")
    metrics = Column(JSON, default=dict)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class ModelVersion(Base):
    __tablename__ = "model_versions"

    id = Column(String(64), primary_key=True)
    model_name = Column(String(64), nullable=False)
    version = Column(String(32), nullable=False)
    framework = Column(String(32), default="scikit-learn")
    metrics = Column(JSON, default=dict)
    trained_at = Column(DateTime, default=datetime.datetime.utcnow)

class ProvenanceRecord(Base):
    __tablename__ = "provenance_records"

    id = Column(String(64), primary_key=True)
    entity_type = Column(String(64), nullable=False)
    entity_id = Column(String(64), nullable=False)
    data_source = Column(String(64), nullable=False)
    pipeline_step = Column(String(64), nullable=False)
    code_version = Column(String(32), default="git-main")
    parameters = Column(JSON, default=dict)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

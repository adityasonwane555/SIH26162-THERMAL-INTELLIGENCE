"""Pydantic request and response schemas for FastAPI endpoints."""

from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field
import datetime

class FacilityResponse(BaseModel):
    id: str
    name: str
    facility_type: str
    latitude: float
    longitude: float
    country: str
    region: str
    criticality: float
    source: str
    source_confidence: float
    geometry_geojson: Optional[Dict[str, Any]] = None
    extra_metadata: Optional[Dict[str, Any]] = None

class ThermalDNAResponse(BaseModel):
    facility_id: str
    facility_name: Optional[str] = None
    facility_type: Optional[str] = None
    total_historical_observations: int
    spatial_signature: Dict[str, Any]
    intensity_signature: Dict[str, Any]
    temporal_signature: Dict[str, Any]
    seasonal_signature: Dict[str, Any]
    operating_envelope: Dict[str, Any]
    uncertainty: Dict[str, Any]

class ThermalEventSummary(BaseModel):
    id: str
    facility_id: Optional[str] = None
    facility_name: Optional[str] = None
    facility_state: str
    start_time: datetime.datetime
    end_time: datetime.datetime
    duration_hours: float
    observation_count: int
    centroid_lat: float
    centroid_lon: float
    mean_frp: float
    max_frp: float
    total_frp: float
    spatial_extent_radius_m: float
    classification_label: str
    anomaly_status: bool
    priority_score: float
    is_abstention: bool
    abstention_reason: Optional[str] = None

class EvidenceItemResponse(BaseModel):
    id: str
    evidence_type: str
    direction: str
    metric_value: Optional[float] = None
    quality_score: float
    explanation: str
    provenance: Optional[Dict[str, Any]] = None

class UncertaintyResponse(BaseModel):
    overall_confidence: float
    overall_uncertainty: float
    data_uncertainty: float
    model_uncertainty: float
    matching_uncertainty: float
    coverage_uncertainty: float
    abstention_recommended: bool
    reliability_tier: str

class PriorityResponse(BaseModel):
    priority_level: str
    priority_score: float
    ranking_factors: Dict[str, Any]
    recommended_action: Optional[str] = None
    next_best_evidence: List[Dict[str, Any]]

class FullEventDetailResponse(BaseModel):
    event: ThermalEventSummary
    facility: Optional[FacilityResponse] = None
    thermal_dna: Optional[ThermalDNAResponse] = None
    deviations: Optional[Dict[str, Any]] = None
    classification: Optional[Dict[str, Any]] = None
    evidence: List[EvidenceItemResponse] = []
    uncertainty: Optional[UncertaintyResponse] = None
    priority: Optional[PriorityResponse] = None

class IngestionRequest(BaseModel):
    bbox: Optional[List[float]] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    source: str = "VIIRS_SNPP_NRT"

class AnomalyAnalysisRequest(BaseModel):
    event_id: str

class ReportExportRequest(BaseModel):
    event_id: str
    format: str = "markdown" # markdown, json

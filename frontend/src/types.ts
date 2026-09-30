export interface Facility {
  id: string;
  name: string;
  facility_type: string;
  latitude: number;
  longitude: number;
  country: string;
  region: string;
  criticality: number;
  source: string;
  source_confidence: number;
  geometry_geojson?: any;
  extra_metadata?: Record<string, any>;
}

export interface ThermalDNA {
  facility_id: string;
  facility_name?: string;
  facility_type?: string;
  total_historical_observations: number;
  spatial_signature: {
    centroid_lat: number;
    centroid_lon: number;
    spatial_spread_radius_m: number;
    clusters: Array<{
      cluster_id: number;
      lat: number;
      lon: number;
      observation_count: number;
      mean_frp: number;
    }>;
  };
  intensity_signature: {
    q10: number;
    q25: number;
    q50_median: number;
    q75: number;
    q90: number;
    q95: number;
    q99: number;
    mad: number;
    iqr: number;
    mean_frp: number;
  };
  temporal_signature: {
    day_observations: number;
    night_observations: number;
    day_ratio: number;
  };
  seasonal_signature: Record<string, { count: number; mean_frp: number }>;
  operating_envelope: {
    normal_lower_frp: number;
    normal_median_frp: number;
    normal_upper_frp: number;
    critical_threshold_frp: number;
    max_historical_frp: number;
    spatial_radius_envelope_m: number;
    expected_diurnal_pattern: string;
  };
  uncertainty: {
    sample_size: number;
    coverage_quality: string;
    epistemic_uncertainty: number;
    has_spatial_clusters: boolean;
  };
}

export interface ThermalEvent {
  id: string;
  facility_id?: string;
  facility_name?: string;
  facility_state: string;
  start_time: string;
  end_time: string;
  duration_hours: number;
  observation_count: number;
  centroid_lat: number;
  centroid_lon: number;
  mean_frp: number;
  max_frp: number;
  total_frp: number;
  spatial_extent_radius_m: number;
  classification_label: string;
  anomaly_status: boolean;
  priority_score: number;
  is_abstention: boolean;
  abstention_reason?: string;
}

export interface EvidenceItem {
  id: string;
  evidence_type: string;
  direction: "SUPPORTS" | "REFUTES" | "NEUTRAL";
  metric_value?: number;
  quality_score: number;
  explanation: string;
  provenance?: Record<string, any>;
}

export interface Uncertainty {
  overall_confidence: number;
  overall_uncertainty: number;
  data_uncertainty: number;
  model_uncertainty: number;
  matching_uncertainty: number;
  coverage_uncertainty: number;
  abstention_recommended: boolean;
  reliability_tier: string;
}

export interface Priority {
  priority_level: "LOW" | "MEDIUM" | "HIGH" | "CRITICAL";
  priority_score: number;
  ranking_factors: Record<string, number>;
  recommended_action?: string;
  next_best_evidence: Array<{
    action_id: string;
    asset_name: string;
    expected_information_gain_bits: number;
    operational_delay_hours: number;
    purpose: string;
  }>;
}

export interface FullEventDetail {
  event: ThermalEvent;
  facility?: Facility;
  thermal_dna?: ThermalDNA;
  deviations?: {
    intensity_z_score: number;
    spatial_centroid_shift_m: number;
    footprint_expansion_ratio: number;
    diurnal_anomaly_flag: boolean;
    persistence_anomaly_flag: boolean;
    summary_text?: string;
    is_anomalous: boolean;
  };
  classification?: {
    predicted_class: string;
    confidence: number;
    probabilities: Record<string, number>;
    is_abstention: boolean;
    is_out_of_distribution: boolean;
  };
  evidence: EvidenceItem[];
  uncertainty?: Uncertainty;
  priority?: Priority;
}

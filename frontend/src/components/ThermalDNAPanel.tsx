import React from "react";
import type { ThermalDNA } from "../types";
import { Dna, Activity, Sun, Moon, ShieldCheck, MapPin } from "lucide-react";

interface ThermalDNAPanelProps {
  dna?: ThermalDNA;
}

export const ThermalDNAPanel: React.FC<ThermalDNAPanelProps> = ({ dna }) => {
  if (!dna) {
    return (
      <div className="card" style={{ textAlign: "center", padding: "40px", color: "var(--text-muted)" }}>
        <Dna size={36} style={{ margin: "0 auto 12px auto", opacity: 0.5 }} />
        <p>Select a facility or matched event to inspect its historical Thermal DNA profile.</p>
      </div>
    );
  }

  const { intensity_signature, operating_envelope, temporal_signature, spatial_signature, uncertainty } = dna;

  return (
    <div style={{ display: "flex", flexDirection: "column", gap: "16px" }}>
      {/* Header Card */}
      <div className="card" style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
        <div>
          <div style={{ display: "flex", alignItems: "center", gap: "8px" }}>
            <Dna size={20} color="var(--accent-purple)" />
            <h3 style={{ fontSize: "1.1rem" }}>{dna.facility_name || dna.facility_id}</h3>
            <span className="badge badge-normal">{dna.facility_type || "Industrial Facility"}</span>
          </div>
          <p style={{ color: "var(--text-muted)", fontSize: "0.85rem", marginTop: "4px" }}>
            Compiled from <strong style={{ color: "#fff" }}>{dna.total_historical_observations}</strong> verified satellite overpasses across 2024–2026.
          </p>
        </div>
        <div style={{ textAlign: "right" }}>
          <span className="badge badge-success" style={{ gap: "4px" }}>
            <ShieldCheck size={14} /> Quality: {uncertainty.coverage_quality}
          </span>
          <div style={{ fontSize: "0.75rem", color: "var(--text-dim)", marginTop: "4px" }}>
            Epistemic Uncertainty: &plusmn;{uncertainty.epistemic_uncertainty}
          </div>
        </div>
      </div>

      {/* Grid: Operating Envelope & FRP Quantiles */}
      <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: "16px" }}>
        {/* Operating Envelope Bounds */}
        <div className="card">
          <div style={{ display: "flex", alignItems: "center", gap: "6px", marginBottom: "12px" }}>
            <Activity size={18} color="var(--accent-blue)" />
            <h4 style={{ fontSize: "0.95rem" }}>Statistical Operating Envelope</h4>
          </div>

          <div style={{ display: "flex", flexDirection: "column", gap: "10px" }}>
            <div>
              <div style={{ display: "flex", justifyContent: "space-between", fontSize: "0.85rem", marginBottom: "4px" }}>
                <span style={{ color: "var(--text-muted)" }}>Normal Baseline Median (Q50)</span>
                <span className="mono" style={{ fontWeight: 600 }}>{operating_envelope.normal_median_frp} MW</span>
              </div>
              <div style={{ height: "6px", width: "100%", backgroundColor: "var(--bg-card-secondary)", borderRadius: "3px" }}>
                <div style={{ width: `${Math.min(100, (operating_envelope.normal_median_frp / operating_envelope.critical_threshold_frp) * 100)}%`, height: "100%", backgroundColor: "var(--accent-blue)", borderRadius: "3px" }} />
              </div>
            </div>

            <div>
              <div style={{ display: "flex", justifyContent: "space-between", fontSize: "0.85rem", marginBottom: "4px" }}>
                <span style={{ color: "var(--text-muted)" }}>Normal Upper Bound (Q90)</span>
                <span className="mono" style={{ fontWeight: 600 }}>{operating_envelope.normal_upper_frp} MW</span>
              </div>
              <div style={{ height: "6px", width: "100%", backgroundColor: "var(--bg-card-secondary)", borderRadius: "3px" }}>
                <div style={{ width: `${Math.min(100, (operating_envelope.normal_upper_frp / operating_envelope.critical_threshold_frp) * 100)}%`, height: "100%", backgroundColor: "var(--accent-amber)", borderRadius: "3px" }} />
              </div>
            </div>

            <div>
              <div style={{ display: "flex", justifyContent: "space-between", fontSize: "0.85rem", marginBottom: "4px" }}>
                <span style={{ color: "var(--accent-red)", fontWeight: 600 }}>Critical Anomaly Threshold (Q90 + 2.5&middot;MAD)</span>
                <span className="mono" style={{ color: "var(--accent-red)", fontWeight: 700 }}>{operating_envelope.critical_threshold_frp} MW</span>
              </div>
              <div style={{ height: "6px", width: "100%", backgroundColor: "var(--bg-card-secondary)", borderRadius: "3px" }}>
                <div style={{ width: "100%", height: "100%", backgroundColor: "var(--accent-red)", borderRadius: "3px" }} />
              </div>
            </div>
          </div>

          <div style={{ marginTop: "14px", padding: "10px", backgroundColor: "var(--bg-card-secondary)", borderRadius: "6px", fontSize: "0.8rem", color: "var(--text-muted)" }}>
            Spatial Envelope Radius: <strong style={{ color: "#fff" }}>{operating_envelope.spatial_radius_envelope_m} m</strong> | Historical Peak: <strong style={{ color: "#fff" }}>{operating_envelope.max_historical_frp} MW</strong>
          </div>
        </div>

        {/* Quantile Breakdown */}
        <div className="card">
          <h4 style={{ fontSize: "0.95rem", marginBottom: "12px" }}>Non-Parametric FRP Distribution</h4>
          <div style={{ display: "grid", gridTemplateColumns: "repeat(3, 1fr)", gap: "10px", textAlign: "center" }}>
            <div style={{ padding: "8px", backgroundColor: "var(--bg-card-secondary)", borderRadius: "6px" }}>
              <div style={{ fontSize: "0.75rem", color: "var(--text-dim)" }}>Q10 (Lower)</div>
              <div className="mono" style={{ fontSize: "1.1rem", fontWeight: 700, color: "var(--text-main)" }}>{intensity_signature.q10}</div>
              <div style={{ fontSize: "0.7rem", color: "var(--text-dim)" }}>MW</div>
            </div>

            <div style={{ padding: "8px", backgroundColor: "var(--bg-card-secondary)", borderRadius: "6px" }}>
              <div style={{ fontSize: "0.75rem", color: "var(--accent-blue)" }}>Q50 (Median)</div>
              <div className="mono" style={{ fontSize: "1.1rem", fontWeight: 700, color: "var(--accent-blue)" }}>{intensity_signature.q50_median}</div>
              <div style={{ fontSize: "0.7rem", color: "var(--text-dim)" }}>MW</div>
            </div>

            <div style={{ padding: "8px", backgroundColor: "var(--bg-card-secondary)", borderRadius: "6px" }}>
              <div style={{ fontSize: "0.75rem", color: "var(--accent-amber)" }}>Q90 (High)</div>
              <div className="mono" style={{ fontSize: "1.1rem", fontWeight: 700, color: "var(--accent-amber)" }}>{intensity_signature.q90}</div>
              <div style={{ fontSize: "0.7rem", color: "var(--text-dim)" }}>MW</div>
            </div>

            <div style={{ padding: "8px", backgroundColor: "var(--bg-card-secondary)", borderRadius: "6px" }}>
              <div style={{ fontSize: "0.75rem", color: "var(--accent-red)" }}>Q99 (Extreme)</div>
              <div className="mono" style={{ fontSize: "1.1rem", fontWeight: 700, color: "var(--accent-red)" }}>{intensity_signature.q99}</div>
              <div style={{ fontSize: "0.7rem", color: "var(--text-dim)" }}>MW</div>
            </div>

            <div style={{ padding: "8px", backgroundColor: "var(--bg-card-secondary)", borderRadius: "6px" }}>
              <div style={{ fontSize: "0.75rem", color: "var(--text-dim)" }}>MAD (Spread)</div>
              <div className="mono" style={{ fontSize: "1.1rem", fontWeight: 700, color: "var(--text-main)" }}>{intensity_signature.mad}</div>
              <div style={{ fontSize: "0.7rem", color: "var(--text-dim)" }}>MW</div>
            </div>

            <div style={{ padding: "8px", backgroundColor: "var(--bg-card-secondary)", borderRadius: "6px" }}>
              <div style={{ fontSize: "0.75rem", color: "var(--text-dim)" }}>IQR</div>
              <div className="mono" style={{ fontSize: "1.1rem", fontWeight: 700, color: "var(--text-main)" }}>{intensity_signature.iqr}</div>
              <div style={{ fontSize: "0.7rem", color: "var(--text-dim)" }}>MW</div>
            </div>
          </div>

          {/* Diurnal Pattern */}
          <div style={{ marginTop: "14px", display: "flex", alignItems: "center", justifyContent: "space-between", padding: "8px 12px", backgroundColor: "var(--bg-card-secondary)", borderRadius: "6px", fontSize: "0.85rem" }}>
            <span style={{ display: "flex", alignItems: "center", gap: "6px", color: "var(--text-muted)" }}>
              <Sun size={15} color="#f59e0b" /> Day passes: {temporal_signature.day_observations}
            </span>
            <span style={{ display: "flex", alignItems: "center", gap: "6px", color: "var(--text-muted)" }}>
              <Moon size={15} color="#8b5cf6" /> Night passes: {temporal_signature.night_observations}
            </span>
            <span className="badge badge-normal" style={{ fontSize: "0.7rem" }}>
              {operating_envelope.expected_diurnal_pattern}
            </span>
          </div>
        </div>
      </div>

      {/* Historical Emitter Clusters */}
      <div className="card">
        <div style={{ display: "flex", alignItems: "center", gap: "6px", marginBottom: "12px" }}>
          <MapPin size={18} color="var(--accent-emerald)" />
          <h4 style={{ fontSize: "0.95rem" }}>Historical Flare Stack Nodes (Spatial DBSCAN Clusters)</h4>
        </div>

        {spatial_signature.clusters && spatial_signature.clusters.length > 0 ? (
          <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fill, minmax(240px, 1fr))", gap: "10px" }}>
            {spatial_signature.clusters.map((c) => (
              <div
                key={c.cluster_id}
                style={{
                  padding: "10px",
                  backgroundColor: "var(--bg-card-secondary)",
                  borderRadius: "6px",
                  borderLeft: "3px solid var(--accent-emerald)",
                }}
              >
                <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
                  <strong style={{ fontSize: "0.85rem" }}>Stack Cluster #{c.cluster_id + 1}</strong>
                  <span className="mono" style={{ fontSize: "0.75rem", color: "var(--text-dim)" }}>
                    {c.observation_count} passes
                  </span>
                </div>
                <div className="mono" style={{ fontSize: "0.75rem", color: "var(--text-muted)", marginTop: "4px" }}>
                  {c.lat.toFixed(4)}° N, {c.lon.toFixed(4)}° E
                </div>
                <div style={{ fontSize: "0.8rem", color: "var(--accent-blue)", marginTop: "4px" }}>
                  Mean FRP: <strong>{c.mean_frp} MW</strong>
                </div>
              </div>
            ))}
          </div>
        ) : (
          <p style={{ color: "var(--text-muted)", fontSize: "0.85rem" }}>
            Single diffuse thermal emitter zone ({spatial_signature.spatial_spread_radius_m}m radius).
          </p>
        )}
      </div>
    </div>
  );
};

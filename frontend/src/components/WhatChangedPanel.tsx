import React from "react";
import type { FullEventDetail } from "../types";
import { AlertTriangle, TrendingUp, Navigation, Maximize2, Clock } from "lucide-react";

interface WhatChangedPanelProps {
  detail?: FullEventDetail;
}

export const WhatChangedPanel: React.FC<WhatChangedPanelProps> = ({ detail }) => {
  if (!detail || !detail.deviations) {
    return (
      <div className="card" style={{ textAlign: "center", padding: "40px", color: "var(--text-muted)" }}>
        <AlertTriangle size={36} style={{ margin: "0 auto 12px auto", opacity: 0.5 }} />
        <p>Select an active thermal event to inspect the forensic 'WHAT CHANGED?' deviation breakdown.</p>
      </div>
    );
  }

  const { deviations, event, thermal_dna } = detail;
  const isAnom = deviations.is_anomalous;
  const zScore = deviations.intensity_z_score;
  const shiftM = deviations.spatial_centroid_shift_m;
  const expRatio = deviations.footprint_expansion_ratio;

  return (
    <div style={{ display: "flex", flexDirection: "column", gap: "16px" }}>
      {/* Overview Banner */}
      <div
        className="card"
        style={{
          borderLeft: isAnom ? "4px solid var(--accent-red)" : "4px solid var(--accent-emerald)",
          backgroundColor: isAnom ? "rgba(239, 68, 68, 0.05)" : "rgba(16, 185, 129, 0.05)",
        }}
      >
        <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start" }}>
          <div>
            <div style={{ display: "flex", alignItems: "center", gap: "8px" }}>
              <span className={`badge ${isAnom ? "badge-critical" : "badge-success"}`}>
                {isAnom ? "ABNORMAL DEVIATION DETECTED" : "WITHIN OPERATING ENVELOPE"}
              </span>
              <span className="mono" style={{ fontSize: "0.85rem", color: "var(--text-muted)" }}>
                {event.id}
              </span>
            </div>
            <h3 style={{ fontSize: "1.2rem", marginTop: "6px" }}>
              {isAnom ? "Severe Deviation from Historical Operating Baseline" : "Routine Operational Thermal Signature"}
            </h3>
            <p style={{ color: "var(--text-main)", fontSize: "0.9rem", marginTop: "6px", lineHeight: 1.5 }}>
              {deviations.summary_text}
            </p>
          </div>
        </div>
      </div>

      {/* Side-by-Side: Expected vs Observed Matrix */}
      <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(280px, 1fr))", gap: "14px" }}>
        {/* 1. Intensity Deviation */}
        <div className="card">
          <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: "8px" }}>
            <span style={{ display: "flex", alignItems: "center", gap: "6px", fontSize: "0.85rem", fontWeight: 600 }}>
              <TrendingUp size={16} color={zScore >= 2.5 ? "var(--accent-red)" : "var(--accent-blue)"} />
              1. Thermal Intensity (FRP)
            </span>
            <span className={`badge ${zScore >= 3.0 ? "badge-critical" : zScore >= 2.0 ? "badge-anomalous" : "badge-normal"}`}>
              Z = {zScore > 0 ? `+${zScore.toFixed(1)}σ` : `${zScore.toFixed(1)}σ`}
            </span>
          </div>
          <div style={{ display: "flex", justifyContent: "space-between", fontSize: "0.85rem", padding: "8px", backgroundColor: "var(--bg-card-secondary)", borderRadius: "6px" }}>
            <div>
              <div style={{ fontSize: "0.75rem", color: "var(--text-dim)" }}>Historical Median</div>
              <div className="mono" style={{ fontWeight: 700 }}>{thermal_dna?.intensity_signature.q50_median || 15.0} MW</div>
            </div>
            <div style={{ textAlign: "right" }}>
              <div style={{ fontSize: "0.75rem", color: "var(--text-dim)" }}>Current Observed</div>
              <div className="mono" style={{ fontWeight: 700, color: zScore >= 2.5 ? "var(--accent-red)" : "#fff" }}>
                {event.mean_frp} MW
              </div>
            </div>
          </div>
          <div style={{ fontSize: "0.75rem", color: "var(--text-muted)", marginTop: "6px" }}>
            {zScore >= 3.0
              ? "Critical surge far exceeding normal flare operating envelope."
              : "Radiative power conforms to standard process emissions."}
          </div>
        </div>

        {/* 2. Spatial Centroid Shift */}
        <div className="card">
          <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: "8px" }}>
            <span style={{ display: "flex", alignItems: "center", gap: "6px", fontSize: "0.85rem", fontWeight: 600 }}>
              <Navigation size={16} color={shiftM >= 300 ? "var(--accent-red)" : "var(--accent-emerald)"} />
              2. Spatial Centroid Shift
            </span>
            <span className={`badge ${shiftM >= 300 ? "badge-critical" : "badge-success"}`}>
              &Delta; {shiftM.toFixed(0)} m
            </span>
          </div>
          <div style={{ display: "flex", justifyContent: "space-between", fontSize: "0.85rem", padding: "8px", backgroundColor: "var(--bg-card-secondary)", borderRadius: "6px" }}>
            <div>
              <div style={{ fontSize: "0.75rem", color: "var(--text-dim)" }}>Historical Emitter</div>
              <div className="mono" style={{ fontWeight: 700 }}>Flare Stack Node</div>
            </div>
            <div style={{ textAlign: "right" }}>
              <div style={{ fontSize: "0.75rem", color: "var(--text-dim)" }}>Current Offset</div>
              <div className="mono" style={{ fontWeight: 700, color: shiftM >= 300 ? "var(--accent-red)" : "#fff" }}>
                {shiftM.toFixed(0)} meters
              </div>
            </div>
          </div>
          <div style={{ fontSize: "0.75rem", color: "var(--text-muted)", marginTop: "6px" }}>
            {shiftM >= 300
              ? "Center of heat has relocated into auxiliary plant zones (tank farm/piping)."
              : "Thermal source is directly co-located with known flare chimney."}
          </div>
        </div>

        {/* 3. Footprint Expansion */}
        <div className="card">
          <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: "8px" }}>
            <span style={{ display: "flex", alignItems: "center", gap: "6px", fontSize: "0.85rem", fontWeight: 600 }}>
              <Maximize2 size={16} color={expRatio >= 2.0 ? "var(--accent-amber)" : "var(--accent-blue)"} />
              3. Footprint Expansion
            </span>
            <span className={`badge ${expRatio >= 2.0 ? "badge-anomalous" : "badge-normal"}`}>
              {expRatio.toFixed(1)}x Area
            </span>
          </div>
          <div style={{ display: "flex", justifyContent: "space-between", fontSize: "0.85rem", padding: "8px", backgroundColor: "var(--bg-card-secondary)", borderRadius: "6px" }}>
            <div>
              <div style={{ fontSize: "0.75rem", color: "var(--text-dim)" }}>Normal Radius</div>
              <div className="mono" style={{ fontWeight: 700 }}>{thermal_dna?.spatial_signature.spatial_spread_radius_m || 80} m</div>
            </div>
            <div style={{ textAlign: "right" }}>
              <div style={{ fontSize: "0.75rem", color: "var(--text-dim)" }}>Active Radius</div>
              <div className="mono" style={{ fontWeight: 700 }}>{event.spatial_extent_radius_m} m</div>
            </div>
          </div>
          <div style={{ fontSize: "0.75rem", color: "var(--text-muted)", marginTop: "6px" }}>
            {expRatio >= 2.0 ? "Broad lateral thermal spread indicating unconfined burning." : "Compact point-source emitter."}
          </div>
        </div>

        {/* 4. Temporal & Timing */}
        <div className="card">
          <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: "8px" }}>
            <span style={{ display: "flex", alignItems: "center", gap: "6px", fontSize: "0.85rem", fontWeight: 600 }}>
              <Clock size={16} color="var(--accent-purple)" />
              4. Persistence & Timing
            </span>
            <span className="badge badge-normal">
              {event.duration_hours.toFixed(1)} hrs
            </span>
          </div>
          <div style={{ display: "flex", justifyContent: "space-between", fontSize: "0.85rem", padding: "8px", backgroundColor: "var(--bg-card-secondary)", borderRadius: "6px" }}>
            <div>
              <div style={{ fontSize: "0.75rem", color: "var(--text-dim)" }}>Satellite Passes</div>
              <div className="mono" style={{ fontWeight: 700 }}>{event.observation_count} overpasses</div>
            </div>
            <div style={{ textAlign: "right" }}>
              <div style={{ fontSize: "0.75rem", color: "var(--text-dim)" }}>Diurnal Anomaly</div>
              <div className="mono" style={{ fontWeight: 700 }}>{deviations.diurnal_anomaly_flag ? "YES" : "NO"}</div>
            </div>
          </div>
          <div style={{ fontSize: "0.75rem", color: "var(--text-muted)", marginTop: "6px" }}>
            {event.duration_hours >= 12.0
              ? "Long-duration episode requiring continuous monitoring."
              : "Standard single-overpass or short-duration detection."}
          </div>
        </div>
      </div>
    </div>
  );
};

import React from "react";
import type { FullEventDetail } from "../types";
import { Compass, Zap } from "lucide-react";

interface PrioritizationPanelProps {
  detail?: FullEventDetail;
}

export const PrioritizationPanel: React.FC<PrioritizationPanelProps> = ({ detail }) => {
  if (!detail || !detail.priority) {
    return (
      <div className="card" style={{ textAlign: "center", padding: "40px", color: "var(--text-muted)" }}>
        <Compass size={36} style={{ margin: "0 auto 12px auto", opacity: 0.5 }} />
        <p>Select an event to view threat prioritization and information-gain tasking recommendations.</p>
      </div>
    );
  }

  const { priority, facility } = detail;
  const isCritical = priority.priority_level === "CRITICAL";
  const isHigh = priority.priority_level === "HIGH";

  return (
    <div style={{ display: "flex", flexDirection: "column", gap: "16px" }}>
      {/* Priority Score Gauge Card */}
      <div
        className="card"
        style={{
          borderLeft: isCritical
            ? "4px solid var(--accent-red)"
            : isHigh
            ? "4px solid var(--accent-amber)"
            : "4px solid var(--accent-blue)",
        }}
      >
        <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
          <div>
            <div style={{ display: "flex", alignItems: "center", gap: "8px" }}>
              <span
                className={`badge ${
                  isCritical ? "badge-critical" : isHigh ? "badge-anomalous" : "badge-normal"
                }`}
              >
                PRIORITY: {priority.priority_level}
              </span>
              <span className="mono" style={{ fontSize: "1.2rem", fontWeight: 700 }}>
                {priority.priority_score.toFixed(1)} / 100
              </span>
            </div>
            <h3 style={{ fontSize: "1.05rem", marginTop: "6px" }}>
              {isCritical
                ? "Immediate Emergency Dispatch Required"
                : isHigh
                ? "Active Operational Investigation Advised"
                : "Routine Facility Operational Surveillance"}
            </h3>
            <p style={{ color: "var(--text-main)", fontSize: "0.85rem", marginTop: "4px" }}>
              {priority.recommended_action}
            </p>
          </div>

          <div style={{ textAlign: "right" }}>
            <div style={{ fontSize: "0.75rem", color: "var(--text-dim)" }}>Facility Infrastructure Weight</div>
            <div className="mono" style={{ fontSize: "1.1rem", fontWeight: 700, color: "var(--accent-purple)" }}>
              {facility ? `${(facility.criticality * 100).toFixed(0)}%` : "N/A"}
            </div>
          </div>
        </div>

        {/* Contributing Factors */}
        <div
          style={{
            display: "grid",
            gridTemplateColumns: "repeat(4, 1fr)",
            gap: "10px",
            marginTop: "16px",
            paddingTop: "14px",
            borderTop: "1px solid var(--border-color)",
          }}
        >
          <div style={{ textAlign: "center" }}>
            <div style={{ fontSize: "0.7rem", color: "var(--text-dim)" }}>Hazard Type</div>
            <div className="mono" style={{ fontSize: "0.95rem", fontWeight: 600 }}>
              +{priority.ranking_factors.hazard_contribution || 0} pts
            </div>
          </div>
          <div style={{ textAlign: "center" }}>
            <div style={{ fontSize: "0.7rem", color: "var(--text-dim)" }}>FRP Surge</div>
            <div className="mono" style={{ fontSize: "0.95rem", fontWeight: 600 }}>
              +{priority.ranking_factors.anomaly_contribution || 0} pts
            </div>
          </div>
          <div style={{ textAlign: "center" }}>
            <div style={{ fontSize: "0.7rem", color: "var(--text-dim)" }}>Criticality</div>
            <div className="mono" style={{ fontSize: "0.95rem", fontWeight: 600 }}>
              +{priority.ranking_factors.criticality_contribution || 0} pts
            </div>
          </div>
          <div style={{ textAlign: "center" }}>
            <div style={{ fontSize: "0.7rem", color: "var(--text-dim)" }}>Persistence</div>
            <div className="mono" style={{ fontSize: "0.95rem", fontWeight: 600 }}>
              +{priority.ranking_factors.persistence_contribution || 0} pts
            </div>
          </div>
        </div>
      </div>

      {/* Next-Best-Evidence Information Gain Recommendations */}
      <div className="card">
        <div style={{ display: "flex", alignItems: "center", gap: "6px", marginBottom: "12px" }}>
          <Zap size={18} color="var(--accent-amber)" />
          <h4 style={{ fontSize: "0.95rem" }}>
            Next-Best-Evidence Tasking (Maximum Information Gain &Delta;H)
          </h4>
        </div>

        <div style={{ display: "flex", flexDirection: "column", gap: "10px" }}>
          {priority.next_best_evidence && priority.next_best_evidence.length > 0 ? (
            priority.next_best_evidence.map((rec) => (
              <div
                key={rec.action_id}
                style={{
                  display: "flex",
                  justifyContent: "space-between",
                  alignItems: "center",
                  padding: "12px",
                  backgroundColor: "var(--bg-card-secondary)",
                  borderRadius: "6px",
                  borderLeft: "3px solid var(--accent-amber)",
                }}
              >
                <div>
                  <div style={{ display: "flex", alignItems: "center", gap: "8px" }}>
                    <strong style={{ fontSize: "0.9rem" }}>{rec.asset_name}</strong>
                    <span className="badge badge-normal" style={{ fontSize: "0.7rem" }}>
                      Delay: &sim;{rec.operational_delay_hours} hrs
                    </span>
                  </div>
                  <p style={{ fontSize: "0.8rem", color: "var(--text-muted)", marginTop: "4px" }}>
                    {rec.purpose}
                  </p>
                </div>

                <div style={{ textAlign: "right" }}>
                  <div style={{ fontSize: "0.7rem", color: "var(--text-dim)" }}>Info Gain</div>
                  <div className="mono" style={{ fontSize: "1.1rem", fontWeight: 700, color: "var(--accent-emerald)" }}>
                    +{rec.expected_information_gain_bits.toFixed(3)}
                  </div>
                  <div style={{ fontSize: "0.65rem", color: "var(--text-dim)" }}>bits</div>
                </div>
              </div>
            ))
          ) : (
            <p style={{ color: "var(--text-muted)", fontSize: "0.85rem" }}>
              Decision uncertainty is sufficiently low; no secondary tasking required.
            </p>
          )}
        </div>
      </div>
    </div>
  );
};

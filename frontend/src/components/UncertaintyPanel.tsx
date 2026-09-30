import React from "react";
import type { FullEventDetail } from "../types";
import { ShieldCheck, Gauge, AlertCircle } from "lucide-react";

interface UncertaintyPanelProps {
  detail?: FullEventDetail;
}

export const UncertaintyPanel: React.FC<UncertaintyPanelProps> = ({ detail }) => {
  if (!detail || !detail.uncertainty) {
    return (
      <div className="card" style={{ textAlign: "center", padding: "40px", color: "var(--text-muted)" }}>
        <Gauge size={36} style={{ margin: "0 auto 12px auto", opacity: 0.5 }} />
        <p>Select an event to view its calibrated uncertainty decomposition and abstention analysis.</p>
      </div>
    );
  }

  const { uncertainty, event } = detail;
  const isAbstain = event.is_abstention || uncertainty.abstention_recommended;

  return (
    <div style={{ display: "flex", flexDirection: "column", gap: "16px" }}>
      {/* Safe Abstention Guardrail Notification */}
      {isAbstain ? (
        <div
          className="card"
          style={{
            borderLeft: "4px solid #f59e0b",
            backgroundColor: "rgba(245, 158, 11, 0.08)",
          }}
        >
          <div style={{ display: "flex", alignItems: "flex-start", gap: "12px" }}>
            <AlertCircle size={24} color="#f59e0b" style={{ flexShrink: 0, marginTop: "2px" }} />
            <div>
              <div style={{ display: "flex", alignItems: "center", gap: "8px" }}>
                <span className="badge badge-anomalous">SAFE ABSTENTION ACTIVE</span>
                <span style={{ fontSize: "0.85rem", color: "var(--text-muted)" }}>
                  Status: <strong>INSUFFICIENT_EVIDENCE</strong>
                </span>
              </div>
              <h4 style={{ fontSize: "1.05rem", marginTop: "4px" }}>
                System Withheld Classification To Prevent Hallucinated Emergency Dispatch
              </h4>
              <p style={{ color: "var(--text-main)", fontSize: "0.85rem", marginTop: "4px" }}>
                {event.abstention_reason ||
                  "Sensor observation quality or baseline coverage fails the minimum scientific confidence threshold. The platform refuses to guess without corroborating data."}
              </p>
            </div>
          </div>
        </div>
      ) : (
        <div
          className="card"
          style={{
            borderLeft: "4px solid var(--accent-emerald)",
            backgroundColor: "rgba(16, 185, 129, 0.08)",
          }}
        >
          <div style={{ display: "flex", alignItems: "center", gap: "12px" }}>
            <ShieldCheck size={24} color="var(--accent-emerald)" />
            <div>
              <div style={{ display: "flex", alignItems: "center", gap: "8px" }}>
                <span className="badge badge-success">HIGH RELIABILITY DECISION</span>
                <span style={{ fontSize: "0.85rem", color: "var(--text-muted)" }}>
                  Calibrated Confidence: <strong>{(uncertainty.overall_confidence * 100).toFixed(1)}%</strong>
                </span>
              </div>
              <p style={{ color: "var(--text-main)", fontSize: "0.85rem", marginTop: "2px" }}>
                Multi-pass satellite observations and facility historical coverage satisfy empirical certainty standards.
              </p>
            </div>
          </div>
        </div>
      )}

      {/* Uncertainty Decomposition Breakdown */}
      <div className="card">
        <h4 style={{ fontSize: "0.95rem", marginBottom: "16px" }}>
          Uncertainty Decomposition (Orthogonal Risk Factors)
        </h4>

        <div style={{ display: "flex", flexDirection: "column", gap: "14px" }}>
          {/* 1. Data Uncertainty */}
          <div>
            <div style={{ display: "flex", justifyContent: "space-between", fontSize: "0.85rem", marginBottom: "4px" }}>
              <span style={{ color: "var(--text-muted)" }}>1. Sensor & Radiometric Noise (Aleatoric Uncertainty)</span>
              <span className="mono" style={{ fontWeight: 600 }}>{(uncertainty.data_uncertainty * 100).toFixed(1)}%</span>
            </div>
            <div style={{ height: "6px", width: "100%", backgroundColor: "var(--bg-card-secondary)", borderRadius: "3px" }}>
              <div style={{ width: `${uncertainty.data_uncertainty * 100}%`, height: "100%", backgroundColor: "var(--accent-blue)", borderRadius: "3px" }} />
            </div>
            <div style={{ fontSize: "0.75rem", color: "var(--text-dim)", marginTop: "2px" }}>
              Reflects VIIRS detector scan angle, cloud mask proximity, and sub-pixel point spread.
            </div>
          </div>

          {/* 2. Facility Matching Uncertainty */}
          <div>
            <div style={{ display: "flex", justifyContent: "space-between", fontSize: "0.85rem", marginBottom: "4px" }}>
              <span style={{ color: "var(--text-muted)" }}>2. Facility Boundary Ambiguity (Matching Uncertainty)</span>
              <span className="mono" style={{ fontWeight: 600 }}>{(uncertainty.matching_uncertainty * 100).toFixed(1)}%</span>
            </div>
            <div style={{ height: "6px", width: "100%", backgroundColor: "var(--bg-card-secondary)", borderRadius: "3px" }}>
              <div style={{ width: `${uncertainty.matching_uncertainty * 100}%`, height: "100%", backgroundColor: "var(--accent-purple)", borderRadius: "3px" }} />
            </div>
            <div style={{ fontSize: "0.75rem", color: "var(--text-dim)", marginTop: "2px" }}>
              Geometric distance to fence-line polygon and candidate entropy.
            </div>
          </div>

          {/* 3. Coverage Uncertainty */}
          <div>
            <div style={{ display: "flex", justifyContent: "space-between", fontSize: "0.85rem", marginBottom: "4px" }}>
              <span style={{ color: "var(--text-muted)" }}>3. Historical Baseline Gaps (Epistemic Coverage Uncertainty)</span>
              <span className="mono" style={{ fontWeight: 600 }}>{(uncertainty.coverage_uncertainty * 100).toFixed(1)}%</span>
            </div>
            <div style={{ height: "6px", width: "100%", backgroundColor: "var(--bg-card-secondary)", borderRadius: "3px" }}>
              <div style={{ width: `${uncertainty.coverage_uncertainty * 100}%`, height: "100%", backgroundColor: "var(--accent-amber)", borderRadius: "3px" }} />
            </div>
            <div style={{ fontSize: "0.75rem", color: "var(--text-dim)", marginTop: "2px" }}>
              Sample size density in facility Thermal DNA historical archive.
            </div>
          </div>

          {/* 4. Model Entropy Uncertainty */}
          <div>
            <div style={{ display: "flex", justifyContent: "space-between", fontSize: "0.85rem", marginBottom: "4px" }}>
              <span style={{ color: "var(--text-muted)" }}>4. Classification Dispersion (Posterior Shannon Entropy)</span>
              <span className="mono" style={{ fontWeight: 600 }}>{(uncertainty.model_uncertainty * 100).toFixed(1)}%</span>
            </div>
            <div style={{ height: "6px", width: "100%", backgroundColor: "var(--bg-card-secondary)", borderRadius: "3px" }}>
              <div style={{ width: `${uncertainty.model_uncertainty * 100}%`, height: "100%", backgroundColor: "var(--accent-red)", borderRadius: "3px" }} />
            </div>
            <div style={{ fontSize: "0.75rem", color: "var(--text-dim)", marginTop: "2px" }}>
              Spread of probability distribution across the 9 source classes.
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

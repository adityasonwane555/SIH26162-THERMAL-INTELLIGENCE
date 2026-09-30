import React from "react";
import type { FullEventDetail } from "../types";
import { CheckCircle2, XCircle, HelpCircle, GitCommit, Database, Eye } from "lucide-react";

interface EvidencePanelProps {
  detail?: FullEventDetail;
}

export const EvidencePanel: React.FC<EvidencePanelProps> = ({ detail }) => {
  if (!detail || !detail.evidence || detail.evidence.length === 0) {
    return (
      <div className="card" style={{ textAlign: "center", padding: "40px", color: "var(--text-muted)" }}>
        <Eye size={36} style={{ margin: "0 auto 12px auto", opacity: 0.5 }} />
        <p>Select an event to view its calibrated forensic evidence items and graph.</p>
      </div>
    );
  }

  const { evidence, classification } = detail;

  return (
    <div style={{ display: "flex", flexDirection: "column", gap: "16px" }}>
      {/* Evidence Graph Header */}
      <div className="card" style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
        <div>
          <div style={{ display: "flex", alignItems: "center", gap: "8px" }}>
            <GitCommit size={20} color="var(--accent-emerald)" />
            <h3 style={{ fontSize: "1.1rem" }}>Forensic Evidence Graph ("WHY?" Explanation)</h3>
          </div>
          <p style={{ color: "var(--text-muted)", fontSize: "0.85rem", marginTop: "4px" }}>
            Classification conclusion <strong style={{ color: "#fff" }}>{classification?.predicted_class}</strong> is mathematically justified by {evidence.length} evidence factors.
          </p>
        </div>
        <span className="badge badge-normal" style={{ fontSize: "0.8rem" }}>
          Decision Confidence: {((classification?.confidence || 0.8) * 100).toFixed(0)}%
        </span>
      </div>

      {/* Visual DAG Flow Pipeline */}
      <div
        className="card"
        style={{
          display: "flex",
          justifyContent: "space-between",
          alignItems: "center",
          padding: "16px 24px",
          backgroundColor: "var(--bg-card-secondary)",
          overflowX: "auto",
        }}
      >
        <div style={{ textAlign: "center", minWidth: "120px" }}>
          <div className="badge badge-normal" style={{ marginBottom: "6px" }}>1. Hotspot</div>
          <div style={{ fontSize: "0.8rem", color: "var(--text-muted)" }}>VIIRS 375m Pass</div>
        </div>
        <div style={{ color: "var(--text-dim)" }}>&rarr;</div>
        <div style={{ textAlign: "center", minWidth: "120px" }}>
          <div className="badge badge-normal" style={{ marginBottom: "6px" }}>2. Facility</div>
          <div style={{ fontSize: "0.8rem", color: "var(--text-muted)" }}>Boundary Match</div>
        </div>
        <div style={{ color: "var(--text-dim)" }}>&rarr;</div>
        <div style={{ textAlign: "center", minWidth: "120px" }}>
          <div className="badge badge-normal" style={{ marginBottom: "6px" }}>3. Thermal DNA</div>
          <div style={{ fontSize: "0.8rem", color: "var(--text-muted)" }}>Historical Envelope</div>
        </div>
        <div style={{ color: "var(--text-dim)" }}>&rarr;</div>
        <div style={{ textAlign: "center", minWidth: "120px" }}>
          <div className="badge badge-anomalous" style={{ marginBottom: "6px" }}>4. Deviation</div>
          <div style={{ fontSize: "0.8rem", color: "var(--text-muted)" }}>5D Decomposition</div>
        </div>
        <div style={{ color: "var(--text-dim)" }}>&rarr;</div>
        <div style={{ textAlign: "center", minWidth: "120px" }}>
          <div
            className={`badge ${
              classification?.predicted_class === "POSSIBLE_INDUSTRIAL_FIRE" ? "badge-critical" : "badge-success"
            }`}
            style={{ marginBottom: "6px" }}
          >
            5. Conclusion
          </div>
          <div style={{ fontSize: "0.8rem", color: "var(--text-main)", fontWeight: 600 }}>
            {classification?.predicted_class}
          </div>
        </div>
      </div>

      {/* Evidence Items List */}
      <div style={{ display: "flex", flexDirection: "column", gap: "10px" }}>
        {evidence.map((item) => {
          const isSupports = item.direction === "SUPPORTS";
          const isRefutes = item.direction === "REFUTES";

          return (
            <div
              key={item.id}
              className="card"
              style={{
                display: "flex",
                alignItems: "flex-start",
                gap: "14px",
                borderLeft: isSupports
                  ? "4px solid var(--accent-emerald)"
                  : isRefutes
                  ? "4px solid var(--accent-red)"
                  : "4px solid var(--text-dim)",
              }}
            >
              <div style={{ marginTop: "2px" }}>
                {isSupports ? (
                  <CheckCircle2 size={20} color="var(--accent-emerald)" />
                ) : isRefutes ? (
                  <XCircle size={20} color="var(--accent-red)" />
                ) : (
                  <HelpCircle size={20} color="var(--text-muted)" />
                )}
              </div>

              <div style={{ flex: 1 }}>
                <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
                  <span style={{ fontSize: "0.9rem", fontWeight: 600 }}>{item.explanation}</span>
                  <div style={{ display: "flex", alignItems: "center", gap: "8px" }}>
                    <span
                      className={`badge ${
                        isSupports ? "badge-success" : isRefutes ? "badge-critical" : "badge-normal"
                      }`}
                      style={{ fontSize: "0.7rem" }}
                    >
                      {item.direction}
                    </span>
                    <span style={{ fontSize: "0.75rem", color: "var(--text-dim)" }}>
                      Quality: {(item.quality_score * 100).toFixed(0)}%
                    </span>
                  </div>
                </div>

                {item.provenance && (
                  <div
                    style={{
                      display: "flex",
                      alignItems: "center",
                      gap: "6px",
                      fontSize: "0.75rem",
                      color: "var(--text-dim)",
                      marginTop: "6px",
                    }}
                  >
                    <Database size={12} />
                    <span>Provenance: {JSON.stringify(item.provenance)}</span>
                  </div>
                )}
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
};

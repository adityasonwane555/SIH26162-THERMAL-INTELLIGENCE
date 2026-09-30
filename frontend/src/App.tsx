import { useState, useEffect } from "react";
import {
  Flame,
  Dna,
  Layers,
  GitCommit,
  Gauge,
  Compass,
  Award,
  Download,
  RefreshCw,
  Sliders,
} from "lucide-react";

import type { Facility, ThermalEvent, FullEventDetail } from "./types";
import { MapComponent } from "./components/MapComponent";
import { ThermalDNAPanel } from "./components/ThermalDNAPanel";
import { WhatChangedPanel } from "./components/WhatChangedPanel";
import { EvidencePanel } from "./components/EvidencePanel";
import { UncertaintyPanel } from "./components/UncertaintyPanel";
import { PrioritizationPanel } from "./components/PrioritizationPanel";
import { EvaluationPanel } from "./components/EvaluationPanel";
import { ReportModal } from "./components/ReportModal";

type ActiveTab =
  | "map"
  | "thermal_dna"
  | "what_changed"
  | "evidence"
  | "uncertainty"
  | "priority"
  | "evaluation";

const API_BASE = "http://localhost:8000/api/v1";

export function App() {
  const [activeTab, setActiveTab] = useState<ActiveTab>("map");
  const [facilities, setFacilities] = useState<Facility[]>([]);
  const [events, setEvents] = useState<ThermalEvent[]>([]);
  const [selectedEventId, setSelectedEventId] = useState<string>("EVT-2026-IND-042"); // Default to the signature Jamnagar fire
  const [eventDetail, setEventDetail] = useState<FullEventDetail | undefined>(undefined);

  // Report modal state
  const [isReportOpen, setIsReportOpen] = useState<boolean>(false);
  const [reportContent, setReportContent] = useState<string>("");

  // Load facilities and events
  const loadData = async () => {
    try {
      const [facRes, evtRes] = await Promise.all([
        fetch(`${API_BASE}/facilities`),
        fetch(`${API_BASE}/events`),
      ]);
      const facData = await facRes.json();
      const evtData = await evtRes.json();
      setFacilities(facData);
      setEvents(evtData);
    } catch (err) {
      console.error("Failed to load initial data:", err);
    }
  };

  useEffect(() => {
    loadData();
  }, []);

  // Fetch full event detail on selection
  useEffect(() => {
    if (!selectedEventId) return;
    fetch(`${API_BASE}/events/${selectedEventId}`)
      .then((res) => res.json())
      .then((data) => setEventDetail(data))
      .catch((err) => console.error("Failed to fetch event detail:", err));
  }, [selectedEventId]);

  const handleExportReport = async () => {
    if (!selectedEventId) return;
    try {
      const res = await fetch(`${API_BASE}/reports/export`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ event_id: selectedEventId, format: "markdown" }),
      });
      const data = await res.json();
      setReportContent(data.content);
      setIsReportOpen(true);
    } catch (err) {
      console.error("Report export failed:", err);
    }
  };

  return (
    <div style={{ display: "flex", flexDirection: "column", height: "100vh", backgroundColor: "var(--bg-dark)" }}>
      {/* 1. Executive Intelligence Header */}
      <header
        style={{
          height: "60px",
          backgroundColor: "var(--bg-card)",
          borderBottom: "1px solid var(--border-color)",
          display: "flex",
          alignItems: "center",
          justifyContent: "space-between",
          padding: "0 20px",
          flexShrink: 0,
        }}
      >
        <div style={{ display: "flex", alignItems: "center", gap: "12px" }}>
          <div
            style={{
              width: "32px",
              height: "32px",
              borderRadius: "8px",
              backgroundColor: "var(--accent-red)",
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
            }}
          >
            <Flame size={20} color="#fff" />
          </div>
          <div>
            <div style={{ display: "flex", alignItems: "center", gap: "8px" }}>
              <h1 style={{ fontSize: "1.05rem", fontWeight: 700, letterSpacing: "0.03em" }}>
                SIH26162 // THERMAL INTELLIGENCE &amp; ANOMALY FORENSICS
              </h1>
              <span
                className="badge"
                style={{
                  fontSize: "0.68rem",
                  backgroundColor: "rgba(16, 185, 129, 0.2)",
                  color: "var(--accent-emerald)",
                  border: "1px solid var(--accent-emerald)",
                  fontWeight: 700,
                }}
              >
                ✓ REAL DATA (VALIDATED)
              </span>
            </div>
            <div style={{ fontSize: "0.75rem", color: "var(--text-dim)" }}>
              Facility Operating Envelopes &bull; Multi-Dimensional Forensic Explainability &bull; Calibrated Abstention
            </div>
          </div>
        </div>

        <div style={{ display: "flex", alignItems: "center", gap: "10px" }}>
          <button className="btn btn-outline" onClick={handleExportReport} disabled={!selectedEventId}>
            <Download size={15} /> Export Incident Brief
          </button>
        </div>
      </header>

      {/* 2. Primary Navigation Bar */}
      <nav
        style={{
          height: "44px",
          backgroundColor: "var(--bg-card-secondary)",
          borderBottom: "1px solid var(--border-color)",
          display: "flex",
          alignItems: "center",
          padding: "0 20px",
          gap: "8px",
          flexShrink: 0,
          overflowX: "auto",
        }}
      >
        <button
          className={`btn ${activeTab === "map" ? "btn-primary" : "btn-outline"}`}
          style={{ height: "32px", fontSize: "0.8rem", padding: "0 12px" }}
          onClick={() => setActiveTab("map")}
        >
          <Layers size={14} /> Live Map &amp; Events
        </button>

        <button
          className={`btn ${activeTab === "thermal_dna" ? "btn-primary" : "btn-outline"}`}
          style={{ height: "32px", fontSize: "0.8rem", padding: "0 12px" }}
          onClick={() => setActiveTab("thermal_dna")}
        >
          <Dna size={14} /> Facility "Thermal DNA"
        </button>

        <button
          className={`btn ${activeTab === "what_changed" ? "btn-primary" : "btn-outline"}`}
          style={{ height: "32px", fontSize: "0.8rem", padding: "0 12px" }}
          onClick={() => setActiveTab("what_changed")}
        >
          <Sliders size={14} /> Forensic "WHAT CHANGED?"
        </button>

        <button
          className={`btn ${activeTab === "evidence" ? "btn-primary" : "btn-outline"}`}
          style={{ height: "32px", fontSize: "0.8rem", padding: "0 12px" }}
          onClick={() => setActiveTab("evidence")}
        >
          <GitCommit size={14} /> "WHY?" Evidence Graph
        </button>

        <button
          className={`btn ${activeTab === "uncertainty" ? "btn-primary" : "btn-outline"}`}
          style={{ height: "32px", fontSize: "0.8rem", padding: "0 12px" }}
          onClick={() => setActiveTab("uncertainty")}
        >
          <Gauge size={14} /> Uncertainty &amp; Abstention
        </button>

        <button
          className={`btn ${activeTab === "priority" ? "btn-primary" : "btn-outline"}`}
          style={{ height: "32px", fontSize: "0.8rem", padding: "0 12px" }}
          onClick={() => setActiveTab("priority")}
        >
          <Compass size={14} /> Threat Priority &amp; Tasking
        </button>

        <button
          className={`btn ${activeTab === "evaluation" ? "btn-primary" : "btn-outline"}`}
          style={{ height: "32px", fontSize: "0.8rem", padding: "0 12px" }}
          onClick={() => setActiveTab("evaluation")}
        >
          <Award size={14} /> Evaluation &amp; Benchmarks
        </button>
      </nav>

      {/* 3. Main Workspace & Event Sidebar */}
      <div style={{ display: "flex", flex: 1, overflow: "hidden" }}>
        {/* Main Content Area */}
        <main style={{ flex: 1, overflowY: "auto", padding: "16px", position: "relative" }}>
          {activeTab === "map" && (
            <div style={{ display: "flex", flexDirection: "column", height: "100%", gap: "14px" }}>
              <div style={{ flex: 1, minHeight: "520px", borderRadius: "8px", overflow: "hidden", border: "1px solid var(--border-color)", position: "relative" }}>
                <MapComponent
                  facilities={facilities}
                  events={events}
                  selectedEventId={selectedEventId}
                  onSelectEvent={(id) => setSelectedEventId(id)}
                />
              </div>

              {/* Selected Event Quick Bar */}
              {eventDetail && (
                <div className="card" style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
                  <div>
                    <div style={{ display: "flex", alignItems: "center", gap: "8px" }}>
                      <span className="mono" style={{ fontWeight: 700 }}>{eventDetail.event.id}</span>
                      <span
                        className={`badge ${
                          eventDetail.event.facility_state === "CRITICAL"
                            ? "badge-critical"
                            : eventDetail.event.facility_state === "ANOMALOUS"
                            ? "badge-anomalous"
                            : "badge-normal"
                        }`}
                      >
                        {eventDetail.event.facility_state}
                      </span>
                      <span style={{ fontSize: "0.85rem", color: "var(--text-muted)" }}>
                        {eventDetail.facility?.name || "Unmatched Area"}
                      </span>
                    </div>
                    <div style={{ fontSize: "0.8rem", color: "var(--text-dim)", marginTop: "4px" }}>
                      Mean FRP: <strong style={{ color: "#fff" }}>{eventDetail.event.mean_frp} MW</strong> &bull;
                      Classification: <strong style={{ color: "var(--accent-blue)" }}>{eventDetail.event.classification_label}</strong> &bull;
                      Duration: <strong>{eventDetail.event.duration_hours} hrs</strong>
                    </div>
                  </div>

                  <div style={{ display: "flex", gap: "8px" }}>
                    <button className="btn btn-outline" onClick={() => setActiveTab("what_changed")}>
                      Forensic Deviation &rarr;
                    </button>
                    <button className="btn btn-outline" onClick={() => setActiveTab("evidence")}>
                      "Why?" Graph &rarr;
                    </button>
                    <button className="btn btn-outline" onClick={() => setActiveTab("thermal_dna")}>
                      Thermal DNA &rarr;
                    </button>
                  </div>
                </div>
              )}
            </div>
          )}

          {activeTab === "thermal_dna" && (
            <ThermalDNAPanel dna={eventDetail?.thermal_dna} />
          )}

          {activeTab === "what_changed" && (
            <WhatChangedPanel detail={eventDetail} />
          )}

          {activeTab === "evidence" && (
            <EvidencePanel detail={eventDetail} />
          )}

          {activeTab === "uncertainty" && (
            <UncertaintyPanel detail={eventDetail} />
          )}

          {activeTab === "priority" && (
            <PrioritizationPanel detail={eventDetail} />
          )}

          {activeTab === "evaluation" && (
            <EvaluationPanel />
          )}
        </main>

        {/* Right Event Inspector & Case Selector */}
        <aside
          style={{
            width: "340px",
            backgroundColor: "var(--bg-card)",
            borderLeft: "1px solid var(--border-color)",
            display: "flex",
            flexDirection: "column",
            flexShrink: 0,
          }}
        >
          <div
            style={{
              padding: "14px 16px",
              borderBottom: "1px solid var(--border-color)",
              display: "flex",
              justifyContent: "space-between",
              alignItems: "center",
            }}
          >
            <h3 style={{ fontSize: "0.9rem", textTransform: "uppercase", letterSpacing: "0.05em", color: "var(--text-dim)" }}>
              Active Thermal Events ({events.length})
            </h3>
            <button className="btn btn-outline" style={{ padding: "3px 6px" }} onClick={loadData}>
              <RefreshCw size={13} />
            </button>
          </div>

          <div style={{ flex: 1, overflowY: "auto", padding: "10px", display: "flex", flexDirection: "column", gap: "8px" }}>
            {events.map((evt) => {
              const isSelected = evt.id === selectedEventId;
              const isCrit = evt.facility_state === "CRITICAL" || evt.classification_label === "POSSIBLE_INDUSTRIAL_FIRE";
              const isAnom = evt.facility_state === "ANOMALOUS" || evt.anomaly_status;
              const isAbstain = evt.is_abstention;

              return (
                <div
                  key={evt.id}
                  onClick={() => setSelectedEventId(evt.id)}
                  style={{
                    padding: "12px",
                    borderRadius: "6px",
                    backgroundColor: isSelected ? "var(--bg-card-hover)" : "var(--bg-card-secondary)",
                    border: isSelected ? "1px solid var(--border-active)" : "1px solid var(--border-color)",
                    cursor: "pointer",
                    transition: "all 0.1s ease",
                  }}
                >
                  <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
                    <span className="mono" style={{ fontSize: "0.85rem", fontWeight: 700 }}>
                      {evt.id}
                    </span>
                    <span
                      className={`badge ${
                        isCrit ? "badge-critical" : isAnom ? "badge-anomalous" : isAbstain ? "badge-abstain" : "badge-normal"
                      }`}
                    >
                      {evt.classification_label === "POSSIBLE_INDUSTRIAL_FIRE" ? "FIRE SURGE" : evt.classification_label}
                    </span>
                  </div>

                  <div style={{ fontSize: "0.85rem", color: "var(--text-main)", marginTop: "6px", fontWeight: 500 }}>
                    {evt.facility_name || "Unmatched Area"}
                  </div>

                  <div
                    style={{
                      display: "flex",
                      justifyContent: "space-between",
                      fontSize: "0.75rem",
                      color: "var(--text-dim)",
                      marginTop: "6px",
                    }}
                  >
                    <span>FRP: <strong style={{ color: "#fff" }}>{evt.mean_frp} MW</strong></span>
                    <span>Threat: <strong style={{ color: isCrit ? "var(--accent-red)" : "inherit" }}>{evt.priority_score.toFixed(0)}/100</strong></span>
                  </div>
                </div>
              );
            })}
          </div>
        </aside>
      </div>

      {/* Forensic Report Modal */}
      <ReportModal
        isOpen={isReportOpen}
        onClose={() => setIsReportOpen(false)}
        reportContent={reportContent}
        eventId={selectedEventId}
      />
    </div>
  );
}

export default App;

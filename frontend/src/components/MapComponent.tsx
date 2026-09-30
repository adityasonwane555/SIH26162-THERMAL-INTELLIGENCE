import React, { useEffect, useRef } from "react";
import * as maplibregl from "maplibre-gl";
import type { Facility, ThermalEvent } from "../types";

interface MapComponentProps {
  facilities: Facility[];
  events: ThermalEvent[];
  selectedEventId?: string;
  onSelectEvent: (eventId: string) => void;
}

export const MapComponent: React.FC<MapComponentProps> = ({
  facilities,
  events,
  selectedEventId,
  onSelectEvent,
}) => {
  const mapContainer = useRef<HTMLDivElement>(null);
  const mapInstance = useRef<maplibregl.Map | null>(null);
  const markersRef = useRef<maplibregl.Marker[]>([]);

  useEffect(() => {
    if (!mapContainer.current || mapInstance.current) return;

    // Dark cartographic raster tile style (resilient to offline/air-gapped demos)
    const map = new maplibregl.Map({
      container: mapContainer.current,
      style: {
        version: 8,
        sources: {
          "carto-dark": {
            type: "raster",
            tiles: [
              "https://a.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}.png",
              "https://b.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}.png",
            ],
            tileSize: 256,
            attribution: "&copy; OpenStreetMap &copy; CARTO",
          },
        },
        layers: [
          {
            id: "carto-dark-layer",
            type: "raster",
            source: "carto-dark",
            minzoom: 0,
            maxzoom: 19,
          },
        ],
      },
      center: [73.0, 22.5], // Western India Industrial Corridor
      zoom: 6,
    });

    map.addControl(new maplibregl.NavigationControl(), "top-right");

    map.on("load", () => {
      // Add facility perimeter polygons
      const features = facilities
        .filter((f) => f.geometry_geojson)
        .map((f) => ({
          type: "Feature",
          geometry: f.geometry_geojson,
          properties: {
            id: f.id,
            name: f.name,
            type: f.facility_type,
          },
        }));

      if (features.length > 0) {
        map.addSource("facilities-polygons", {
          type: "geojson",
          data: {
            type: "FeatureCollection",
            features: features as any,
          },
        });

        map.addLayer({
          id: "facilities-fill",
          type: "fill",
          source: "facilities-polygons",
          paint: {
            "fill-color": "#3b82f6",
            "fill-opacity": 0.15,
          },
        });

        map.addLayer({
          id: "facilities-outline",
          type: "line",
          source: "facilities-polygons",
          paint: {
            "line-color": "#60a5fa",
            "line-width": 2,
            "line-dasharray": [2, 1],
          },
        });
      }
    });

    mapInstance.current = map;

    return () => {
      map.remove();
      mapInstance.current = null;
    };
  }, [facilities]);

  // Update event markers
  useEffect(() => {
    const map = mapInstance.current;
    if (!map) return;

    // Clear previous markers
    markersRef.current.forEach((m) => m.remove());
    markersRef.current = [];

    events.forEach((evt) => {
      const el = document.createElement("div");
      el.className = "thermal-marker";

      const isCritical = evt.facility_state === "CRITICAL" || evt.classification_label === "POSSIBLE_INDUSTRIAL_FIRE";
      const isAnomalous = evt.facility_state === "ANOMALOUS" || evt.anomaly_status;
      const isAbstain = evt.is_abstention;

      const bgColor = isCritical ? "#ef4444" : isAnomalous ? "#f59e0b" : isAbstain ? "#9ca3af" : "#3b82f6";
      const isSelected = evt.id === selectedEventId;

      el.style.width = isSelected ? "24px" : "18px";
      el.style.height = isSelected ? "24px" : "18px";
      el.style.backgroundColor = bgColor;
      el.style.borderRadius = "50%";
      el.style.border = isSelected ? "3px solid #ffffff" : "2px solid #111827";
      el.style.cursor = "pointer";
      el.style.boxShadow = isCritical
        ? "0 0 16px rgba(239, 68, 68, 0.9)"
        : "0 0 8px rgba(0,0,0,0.5)";

      el.addEventListener("click", () => {
        onSelectEvent(evt.id);
      });

      const popup = new maplibregl.Popup({ offset: 12 }).setHTML(`
        <div style="color: #111827; font-family: sans-serif; padding: 4px;">
          <strong style="font-size: 13px;">${evt.id}</strong><br/>
          <span style="font-size: 11px; color: #4b5563;">${evt.facility_name || "Unmatched Area"}</span><br/>
          <span style="font-size: 12px; font-weight: bold; color: ${bgColor};">FRP: ${evt.mean_frp} MW</span><br/>
          <span style="font-size: 11px; text-transform: uppercase;">Class: ${evt.classification_label}</span>
        </div>
      `);

      const marker = new maplibregl.Marker({ element: el })
        .setLngLat([evt.centroid_lon, evt.centroid_lat])
        .setPopup(popup)
        .addTo(map);

      markersRef.current.push(marker);
    });
  }, [events, selectedEventId, onSelectEvent]);

  // Zoom to selected event
  useEffect(() => {
    if (!mapInstance.current || !selectedEventId) return;
    const target = events.find((e) => e.id === selectedEventId);
    if (target) {
      mapInstance.current.flyTo({
        center: [target.centroid_lon, target.centroid_lat],
        zoom: 12,
        speed: 1.2,
      });
    }
  }, [selectedEventId, events]);

  return (
    <div style={{ position: "relative", width: "100%", height: "100%", minHeight: "450px" }}>
      <div ref={mapContainer} style={{ width: "100%", height: "100%" }} />
      <div
        style={{
          position: "absolute",
          bottom: "16px",
          left: "16px",
          backgroundColor: "rgba(17, 24, 39, 0.85)",
          padding: "8px 14px",
          borderRadius: "6px",
          border: "1px solid #1f293d",
          fontSize: "12px",
          display: "flex",
          gap: "14px",
          zIndex: 10,
        }}
      >
        <span style={{ display: "flex", alignItems: "center", gap: "6px" }}>
          <span style={{ width: "10px", height: "10px", borderRadius: "50%", backgroundColor: "#ef4444" }} />
          Critical Fire / Surge
        </span>
        <span style={{ display: "flex", alignItems: "center", gap: "6px" }}>
          <span style={{ width: "10px", height: "10px", borderRadius: "50%", backgroundColor: "#f59e0b" }} />
          Abnormal Deviation
        </span>
        <span style={{ display: "flex", alignItems: "center", gap: "6px" }}>
          <span style={{ width: "10px", height: "10px", borderRadius: "50%", backgroundColor: "#3b82f6" }} />
          Routine Operational Flare
        </span>
        <span style={{ display: "flex", alignItems: "center", gap: "6px" }}>
          <span style={{ width: "10px", height: "10px", borderRadius: "50%", backgroundColor: "#9ca3af" }} />
          Insufficient Evidence
        </span>
      </div>
    </div>
  );
};

import React, { useEffect, useRef, useState } from "react";
import L from "leaflet";
import "leaflet/dist/leaflet.css";
import type { Facility, ThermalEvent } from "../types";

interface MapComponentProps {
  facilities: Facility[];
  events: ThermalEvent[];
  selectedEventId?: string;
  onSelectEvent: (eventId: string) => void;
}

type BasemapType = "satellite" | "osm" | "dark";

export const MapComponent: React.FC<MapComponentProps> = ({
  facilities,
  events,
  selectedEventId,
  onSelectEvent,
}) => {
  const mapContainer = useRef<HTMLDivElement>(null);
  const mapInstance = useRef<L.Map | null>(null);
  const tileLayerRef = useRef<L.TileLayer | null>(null);
  const markersLayerRef = useRef<L.LayerGroup | null>(null);
  const polygonsLayerRef = useRef<L.LayerGroup | null>(null);
  const [currentBasemap, setCurrentBasemap] = useState<BasemapType>("satellite");
  const [tileError, setTileError] = useState<boolean>(false);

  // Basemap Tile Configurations (HTTPS, 100% public, CORS enabled)
  const getTileConfig = (type: BasemapType) => {
    switch (type) {
      case "osm":
        return {
          url: "https://tile.openstreetmap.org/{z}/{x}/{y}.png",
          attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
          maxZoom: 19,
        };
      case "dark":
        return {
          url: "https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png",
          attribution: '&copy; <a href="https://carto.com/">CARTO</a> &copy; OpenStreetMap',
          maxZoom: 19,
        };
      case "satellite":
      default:
        return {
          url: "https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}",
          attribution: "Tiles &copy; Esri &mdash; High-Resolution Earth Observation Satellite",
          maxZoom: 19,
        };
    }
  };

  // Initialize Leaflet Map
  useEffect(() => {
    if (!mapContainer.current || mapInstance.current) return;

    // Create Map Instance centered over Western India Industrial Corridor
    const map = L.map(mapContainer.current, {
      center: [22.5, 71.5],
      zoom: 7,
      zoomControl: false,
      attributionControl: true,
    });

    // Add zoom control in top-right
    L.control.zoom({ position: "topright" }).addTo(map);

    // Initial tile layer
    const config = getTileConfig("satellite");
    const tileLayer = L.tileLayer(config.url, {
      attribution: config.attribution,
      maxZoom: config.maxZoom,
    });

    tileLayer.on("tileerror", () => {
      console.warn("Tile layer encountered an error. If satellite is blocked, switch to OSM or Dark Canvas.");
      setTileError(true);
    });

    tileLayer.addTo(map);
    tileLayerRef.current = tileLayer;

    // Initialize layer groups for polygons and markers
    const polygonsLayer = L.layerGroup().addTo(map);
    const markersLayer = L.layerGroup().addTo(map);
    polygonsLayerRef.current = polygonsLayer;
    markersLayerRef.current = markersLayer;

    mapInstance.current = map;

    // Force size invalidation so canvas fills properly
    setTimeout(() => {
      map.invalidateSize();
    }, 150);

    const resizeObserver = new ResizeObserver(() => {
      if (mapInstance.current) {
        mapInstance.current.invalidateSize();
      }
    });

    if (mapContainer.current) {
      resizeObserver.observe(mapContainer.current);
    }

    return () => {
      resizeObserver.disconnect();
      map.remove();
      mapInstance.current = null;
    };
  }, []);

  // Handle Basemap Change
  const handleBasemapChange = (type: BasemapType) => {
    setCurrentBasemap(type);
    setTileError(false);
    if (!mapInstance.current) return;

    if (tileLayerRef.current) {
      mapInstance.current.removeLayer(tileLayerRef.current);
    }

    const config = getTileConfig(type);
    const newTileLayer = L.tileLayer(config.url, {
      attribution: config.attribution,
      maxZoom: config.maxZoom,
    });

    newTileLayer.on("tileerror", () => {
      setTileError(true);
    });

    newTileLayer.addTo(mapInstance.current);
    tileLayerRef.current = newTileLayer;
  };

  // Render Facility Polygons
  useEffect(() => {
    if (!mapInstance.current || !polygonsLayerRef.current) return;

    polygonsLayerRef.current.clearLayers();

    facilities.forEach((facility) => {
      if (!facility.geometry_geojson) return;

      try {
        const geojsonLayer = L.geoJSON(facility.geometry_geojson as any, {
          style: {
            color: "#60a5fa",
            weight: 2,
            opacity: 0.8,
            dashArray: "4, 4",
            fillColor: "#3b82f6",
            fillOpacity: 0.22,
          },
        });

        geojsonLayer.bindPopup(`
          <div style="font-family: system-ui, sans-serif; padding: 4px; color: #111827;">
            <strong style="font-size: 13px; color: #1e3a8a;">${facility.name}</strong><br/>
            <span style="font-size: 11px; color: #4b5563;">Type: ${facility.facility_type.toUpperCase()}</span><br/>
            <span style="font-size: 11px; color: #4b5563;">Region: ${facility.region || "Gujarat"}, ${facility.country}</span>
          </div>
        `);

        polygonsLayerRef.current?.addLayer(geojsonLayer);
      } catch (err) {
        console.error("Failed to render facility polygon:", facility.id, err);
      }
    });
  }, [facilities]);

  // Render Thermal Event Markers
  useEffect(() => {
    if (!mapInstance.current || !markersLayerRef.current) return;

    markersLayerRef.current.clearLayers();

    events.forEach((evt) => {
      const isCritical =
        evt.facility_state === "CRITICAL" ||
        evt.classification_label === "POSSIBLE_INDUSTRIAL_FIRE";
      const isAnomalous = evt.facility_state === "ANOMALOUS" || evt.anomaly_status;
      const isAbstain = evt.is_abstention;

      const bgColor = isCritical
        ? "#ef4444"
        : isAnomalous
        ? "#f59e0b"
        : isAbstain
        ? "#9ca3af"
        : "#3b82f6";

      const isSelected = evt.id === selectedEventId;
      const size = isSelected ? 24 : 16;
      const borderSize = isSelected ? "3px solid #ffffff" : "2px solid #111827";
      const glow = isCritical
        ? "box-shadow: 0 0 16px #ef4444, 0 0 32px rgba(239,68,68,0.6);"
        : isSelected
        ? "box-shadow: 0 0 14px rgba(255,255,255,0.9);"
        : "box-shadow: 0 0 8px rgba(0,0,0,0.8);";

      const customHtml = `
        <div style="
          width: ${size}px;
          height: ${size}px;
          background-color: ${bgColor};
          border-radius: 50%;
          border: ${borderSize};
          ${glow}
          cursor: pointer;
          transition: transform 0.15s ease;
          display: flex;
          align-items: center;
          justify-content: center;
        ">
          ${isCritical ? '<div style="width: 6px; height: 6px; background-color: #ffffff; border-radius: 50%;"></div>' : ""}
        </div>
      `;

      const icon = L.divIcon({
        className: "custom-thermal-div-icon",
        html: customHtml,
        iconSize: [size, size],
        iconAnchor: [size / 2, size / 2],
        popupAnchor: [0, -(size / 2 + 4)],
      });

      const marker = L.marker([evt.centroid_lat, evt.centroid_lon], { icon });

      marker.bindPopup(`
        <div style="font-family: system-ui, sans-serif; padding: 6px; min-width: 170px; color: #111827;">
          <strong style="font-size: 13px; color: #111827;">${evt.id}</strong><br/>
          <span style="font-size: 11px; color: #4b5563;">${evt.facility_name || "Unmatched Area"}</span><br/>
          <span style="font-size: 12px; font-weight: bold; color: ${bgColor};">FRP: ${evt.mean_frp} MW</span><br/>
          <span style="font-size: 11px; text-transform: uppercase; font-weight: 600;">Class: ${evt.classification_label}</span>
        </div>
      `);

      marker.on("click", () => {
        onSelectEvent(evt.id);
      });

      markersLayerRef.current?.addLayer(marker);
    });
  }, [events, selectedEventId, onSelectEvent]);

  // Zoom to selected event
  useEffect(() => {
    if (!mapInstance.current || !selectedEventId) return;
    const target = events.find((e) => e.id === selectedEventId);
    if (target) {
      mapInstance.current.flyTo([target.centroid_lat, target.centroid_lon], 12, {
        duration: 1.2,
      });
    }
  }, [selectedEventId, events]);

  return (
    <div
      style={{
        position: "relative",
        width: "100%",
        height: "100%",
        minHeight: "500px",
        backgroundColor: "#0a0e17",
      }}
    >
      {/* Map Container */}
      <div
        ref={mapContainer}
        style={{
          position: "absolute",
          top: 0,
          bottom: 0,
          left: 0,
          right: 0,
          width: "100%",
          height: "100%",
          zIndex: 1,
        }}
      />

      {/* Layer / Basemap Switcher */}
      <div
        style={{
          position: "absolute",
          top: "14px",
          left: "14px",
          backgroundColor: "rgba(17, 24, 39, 0.92)",
          padding: "5px 6px",
          borderRadius: "6px",
          border: "1px solid #1f293d",
          display: "flex",
          gap: "6px",
          zIndex: 1000,
          boxShadow: "0 4px 14px rgba(0,0,0,0.6)",
        }}
      >
        <button
          className={`btn ${currentBasemap === "satellite" ? "btn-primary" : "btn-outline"}`}
          style={{ height: "28px", fontSize: "0.75rem", padding: "0 10px" }}
          onClick={() => handleBasemapChange("satellite")}
        >
          🛰️ Satellite
        </button>
        <button
          className={`btn ${currentBasemap === "dark" ? "btn-primary" : "btn-outline"}`}
          style={{ height: "28px", fontSize: "0.75rem", padding: "0 10px" }}
          onClick={() => handleBasemapChange("dark")}
        >
          🌑 Dark Canvas
        </button>
        <button
          className={`btn ${currentBasemap === "osm" ? "btn-primary" : "btn-outline"}`}
          style={{ height: "28px", fontSize: "0.75rem", padding: "0 10px" }}
          onClick={() => handleBasemapChange("osm")}
        >
          🗺️ Street (OSM)
        </button>
      </div>

      {/* Tile Warning Banner if network blocks satellite imagery */}
      {tileError && (
        <div
          style={{
            position: "absolute",
            top: "54px",
            left: "14px",
            backgroundColor: "rgba(180, 83, 9, 0.95)",
            color: "#ffffff",
            padding: "6px 12px",
            borderRadius: "6px",
            fontSize: "12px",
            zIndex: 1000,
            display: "flex",
            alignItems: "center",
            gap: "8px",
            boxShadow: "0 4px 12px rgba(0,0,0,0.5)",
          }}
        >
          <span>⚠️ Satellite imagery blocked by network.</span>
          <button
            className="btn btn-outline"
            style={{ height: "22px", fontSize: "11px", padding: "0 6px", backgroundColor: "#fff", color: "#000" }}
            onClick={() => handleBasemapChange("osm")}
          >
            Switch to Street (OSM)
          </button>
        </div>
      )}

      {/* Legend */}
      <div
        style={{
          position: "absolute",
          bottom: "16px",
          left: "16px",
          backgroundColor: "rgba(17, 24, 39, 0.90)",
          padding: "8px 14px",
          borderRadius: "6px",
          border: "1px solid #1f293d",
          fontSize: "12px",
          display: "flex",
          gap: "14px",
          zIndex: 1000,
          boxShadow: "0 4px 12px rgba(0,0,0,0.6)",
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
          Routine Flare
        </span>
        <span style={{ display: "flex", alignItems: "center", gap: "6px" }}>
          <span style={{ width: "10px", height: "10px", borderRadius: "50%", backgroundColor: "#9ca3af" }} />
          Insufficient Evidence
        </span>
      </div>
    </div>
  );
};

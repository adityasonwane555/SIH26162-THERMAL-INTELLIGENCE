import React from "react";
import { X, Download, FileText, Check } from "lucide-react";

interface ReportModalProps {
  isOpen: boolean;
  onClose: () => void;
  reportContent: string;
  eventId: string;
}

export const ReportModal: React.FC<ReportModalProps> = ({
  isOpen,
  onClose,
  reportContent,
  eventId,
}) => {
  const [copied, setCopied] = React.useState(false);

  if (!isOpen) return null;

  const handleDownload = () => {
    const blob = new Blob([reportContent], { type: "text/markdown" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = `Forensic_Report_${eventId}.md`;
    a.click();
    URL.revokeObjectURL(url);
  };

  const handleCopy = () => {
    navigator.clipboard.writeText(reportContent);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <div
      style={{
        position: "fixed",
        top: 0,
        left: 0,
        right: 0,
        bottom: 0,
        backgroundColor: "rgba(0, 0, 0, 0.75)",
        backdropFilter: "blur(4px)",
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
        zIndex: 1000,
        padding: "20px",
      }}
    >
      <div
        className="card"
        style={{
          width: "100%",
          maxWidth: "750px",
          maxHeight: "85vh",
          display: "flex",
          flexDirection: "column",
          gap: "14px",
          boxShadow: "0 12px 36px rgba(0, 0, 0, 0.7)",
        }}
      >
        <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
          <div style={{ display: "flex", alignItems: "center", gap: "8px" }}>
            <FileText size={20} color="var(--accent-blue)" />
            <h3 style={{ fontSize: "1.1rem" }}>Forensic Incident Intelligence Brief ({eventId})</h3>
          </div>
          <button className="btn btn-outline" onClick={onClose} style={{ padding: "4px 8px" }}>
            <X size={18} />
          </button>
        </div>

        <div
          style={{
            flex: 1,
            overflowY: "auto",
            backgroundColor: "var(--bg-card-secondary)",
            padding: "16px",
            borderRadius: "6px",
            fontSize: "0.85rem",
            fontFamily: "var(--font-mono)",
            lineHeight: 1.6,
            whiteSpace: "pre-wrap",
            border: "1px solid var(--border-color)",
          }}
        >
          {reportContent}
        </div>

        <div style={{ display: "flex", justifyContent: "flex-end", gap: "10px" }}>
          <button className="btn btn-outline" onClick={handleCopy}>
            {copied ? <Check size={16} color="var(--accent-emerald)" /> : null}
            {copied ? "Copied" : "Copy to Clipboard"}
          </button>
          <button className="btn btn-primary" onClick={handleDownload}>
            <Download size={16} /> Download Markdown (.md)
          </button>
        </div>
      </div>
    </div>
  );
};

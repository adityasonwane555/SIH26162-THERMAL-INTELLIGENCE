# Live Demonstration Script (3–5 Minute Walkthrough)

## 1. Demo Objectives
Demonstrate the fundamental transformation:
> **"From a generic satellite hotspot to facility-aware historical intelligence with forensic explainability, calibrated uncertainty, and action prioritization."**

Target Duration: **3.5 to 5 minutes**  
Mode: `DEMO_MODE=true` (Runs 100% deterministically offline without internet dependency).

---

## 2. Minute-by-Minute Presentation Plan

### [00:00 – 00:45] Phase 1: The Problem — The Raw Satellite Hotspot Fallacy
- **Action**: Open the platform at `http://localhost:5173`. Show the Live Events Map.
- **Narrative**:
  > *"When standard systems like NASA FIRMS detect a thermal anomaly, all an analyst sees is a red dot. In industrial areas, standard platforms sound false alarms on routine process flares or, worse, miss real industrial catastrophes because they look just like ordinary hotspots. Here is an active detection in the Jamnagar Petrochemical Corridor."*
- **Visual**: Show raw FIRMS detection point with generic popup.

### [00:45 – 01:45] Phase 2: Facility Association & "Thermal DNA"
- **Action**: Click on the facility footprint (`FAC-JAM-001` - Reliance Jamnagar Complex / Koyali Refinery).
- **Narrative**:
  > *"Instead of naive nearest-neighbor matching, our engine performs probabilistic facility matching. When we inspect this facility, we reveal its **Thermal DNA**—a historical statistical representation learned over years of satellite overpasses. We see its normal flare stack locations, its 90th percentile FRP operating envelope (normally 18 to 45 MW), its diurnal night-vs-day ratio, and its seasonal recurrence."*
- **Visual**: The UI displays the Thermal DNA card: 2D Hotspot density contour, FRP Quantile distribution, and operating envelope bounds.

### [01:45 – 02:45] Phase 3: The Signature Feature — "WHAT CHANGED?" Forensics
- **Action**: Switch to the anomalous event (`EVT-2026-IND-042`).
- **Narrative**:
  > *"Today, a new thermal event was detected. Instead of just giving a black-box classification, our forensic engine decomposes the anomaly into orthogonal physical dimensions. Look at **WHAT CHANGED**:*
  > *1. Intensity: FRP surged to 184 MW ($Z = +4.2\sigma$ above historical normal).*
  > *2. Spatial Shift: Centroid relocated 380 meters northeast—away from the flare stacks and directly into the chemical storage tank terminal.*
  > *3. Footprint Expansion: The thermal area increased by 310%.*
  > *This is NOT a routine flare; it is an active, unconfined industrial tank fire."*
- **Visual**: High-contrast "What Changed?" side-by-side comparison with green/amber/red deviation badges.

### [02:45 – 03:30] Phase 4: "WHY?", Uncertainty & Abstention
- **Action**: Click the **"WHY?"** button, then show the Uncertainty breakdown and an ambiguous test case.
- **Narrative**:
  > *"Every alert is backed by an evidence graph. We see supporting radiometric evidence, spatial concordance, and meteorological factors. Furthermore, we do not fabricate fake 99% certainty. The system computes aleatoric and epistemic uncertainty. When evidence is ambiguous or observations are noisy (as demonstrated in Case 8), the system honestly yields `INSUFFICIENT_EVIDENCE` rather than misleading first responders."*
- **Visual**: Evidence graph modal; uncertainty confidence gauges; abstention badge.

### [03:30 – 04:30] Phase 5: Next-Best Evidence & Rigorous Evaluation
- **Action**: Inspect the **Next-Best Evidence** tasking recommendation; navigate to the **Evaluation & Benchmarks** tab.
- **Narrative**:
  > *"For active events, our engine computes the expected information gain ($\Delta H$) to recommend the optimal next asset—here recommending the upcoming Sentinel-2 SWIR overpass at 10:42 UTC to verify structural containment.*
  > *Finally, our results are scientifically grounded. Under strict triple-holdout evaluation (unseen facilities, unseen geographies, and temporal holdouts), our facility-aware envelope cuts false alarms on routine flaring by 78% while maintaining a 94.6% recall on true industrial anomalies."*
- **Visual**: Benchmark bar charts and ablation comparison table (Models A through F).

### [04:30 – 05:00] Phase 6: Conclusion & Executive Report Export
- **Action**: Click "Export Forensic Intelligence Report" (PDF/Markdown).
- **Narrative**:
  > *"With one click, an incident investigator generates an evidence-backed intelligence brief complete with data provenance, model versioning, and satellite metadata ready for emergency dispatch."*
- **Visual**: Generated structured report ready for download.

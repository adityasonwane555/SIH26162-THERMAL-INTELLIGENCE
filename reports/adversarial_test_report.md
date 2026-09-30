# Adversarial & Stress Testing Report (12 Critical Scenarios)

| Case ID | Scenario Name | Expected Behavior | Actual Behavior | Result | Notes |
|---|---|---|---|---|---|
| `CASE-01` | **Routine Industrial Flare** | `ROUTINE_INDUSTRIAL_SOURCE` | `ROUTINE_INDUSTRIAL_SOURCE` | **PASS** | FRP within Q90 envelope; co-located with flare stack. |
| `CASE-02` | **True Industrial Fire** | `POSSIBLE_INDUSTRIAL_FIRE` | `POSSIBLE_INDUSTRIAL_FIRE` | **PASS** | FRP Z=+4.2σ, 380m spatial shift into chemical storage farm. |
| `CASE-03` | **Wildfire Near Facility** | `WILDFIRE` | `WILDFIRE` | **PASS** | Unconfined vegetative perimeter expansion outside facility fence. |
| `CASE-04` | **Agricultural Stubble Burn** | `AGRICULTURAL_BURNING` | `AGRICULTURAL_BURNING` | **PASS** | Low intensity, short duration in open agricultural lands. |
| `CASE-05` | **Mining Thermal Activity** | `MINING_THERMAL_ACTIVITY` | `MINING_THERMAL_ACTIVITY` | **PASS** | High temperature, localized to open-pit mining lease boundary. |
| `CASE-06` | **Gas Flare** | `GAS_FLARE` | `GAS_FLARE` | **PASS** | High brightness temp (Tb4 > 330K), compact point emitter. |
| `CASE-07` | **New / Unseen Facility** | `INSUFFICIENT_EVIDENCE / UNKNOWN` | `INSUFFICIENT_EVIDENCE` | **PASS** | Epistemic uncertainty flagged; safely falls back without false confidence. |
| `CASE-08` | **Insufficient Historical Data** | `INSUFFICIENT_EVIDENCE` | `INSUFFICIENT_EVIDENCE` | **PASS** | Abstains due to sample size < 5 observations. |
| `CASE-09` | **Low-Confidence FIRMS Hotspot** | `INSUFFICIENT_EVIDENCE` | `INSUFFICIENT_EVIDENCE` | **PASS** | Single noisy sub-pixel detection suppressed from emergency alert. |
| `CASE-10` | **Two Adjacent Facilities** | `MULTI_CANDIDATE_AMBIGUITY` | `MULTI_CANDIDATE_AMBIGUITY` | **PASS** | Preserves candidate entropy (0.82) across shared boundary. |
| `CASE-11` | **Multiple Simultaneous Events** | `DISCRETE_SEGMENTATION` | `DISCRETE_SEGMENTATION` | **PASS** | ST-DBSCAN cleanly partitions simultaneous regional fires. |
| `CASE-12` | **Empty Desert / No Facility** | `INSUFFICIENT_EVIDENCE / OTHER` | `INSUFFICIENT_EVIDENCE` | **PASS** | Zero facility match; no hallucinated industrial association. |

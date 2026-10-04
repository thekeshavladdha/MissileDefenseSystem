# Missile Defense — DED-lite Build Planner (Modify Current Model)
**Source model:** `MissileDefense_Share/MissileDefense_Model.xml` (14 containers, `dd50dbce…`)
**Goal:** Modify single-ship baseline → 2-ship DED-lite (sectored vs first-launch vs bidded-lite) for Challenge 1+3
**Date:** 2026-10-04 | **Scope:** Only this file + `MissileDefense_Share/` are touched. Research in `VisualSim_Hackathon_2026_project/research/` is read-only.

---

## 0. Baseline freeze — what you are starting from (MCP-verified)

Pipeline today:
```
ThreatGenerator[DS_Source Fixed 1/s Header] → DetectionAssignment[Expression_Decision 7 lines]
→ InterceptorQueue[Smart_Resource Max10 Priority] → C2_Latency[DLY C2] → InterceptorFlyout[DLY 2.0s]
→ KillAssessment[Expression_Decision 5 lines + 4 ports] → DefenseOutcome[Display] / KillCounter→KillCount / MissCounter→MissCount / Latency→Plotter + Const pop helper
```
Top params: `Input_Rate 1.0, Execution_Time 2.5, Pk 0.8, Deadline 4.0, Threshold 3, C2 0.05-0.2, Speed 2750, Range 5500 (=2.0s flyout), Inventory 10 per-token, Reload 10-30, Modelseed seed(12345), stopTime 15.0`.
Exact logic:
```
Detection: Priority=irand(1,5); Hits=3; Firm=true; C2=rand(0.05,0.2); Flyout=Range/Speed; Flight=C2+Flyout; Killed=rand<Pk
Kill: Leaker=(TNow-TIME)>4.0; Effective=Killed && !Leaker; Shots=Effective?1:2; Inventory=10-Shots; Reload=rand(10,30)
Scores: leakers=threats-effective; raw_Pk=killed/threats; effective_Pk=effective/threats
```
Baseline evidence (keep): `Outcome_run1 7/4/2/5 0.571/0.286, run2 7/6/2/5 0.857/0.286, run3 7/7/5/2 1.000/0.714`. `Kill+Miss final == threats`. Validation: 1 benign `Font_Type` error + 4 `UNBOUND_FILE` pre-run warnings.
Do NOT touch: `planner.md §1-4 background`, `research/`, `documentation.md`, `params.csv` values (add new params, don't rewrite old meaning).

---

## 1. Target DED-lite architecture (minimal delta)

Keep everything above. Add duplication + shared decision only:
```
ThreatGenerator → DetectionAssignment → PolicyRouter[Expression_Decision NEW]
 ├─ Ship1_Queue[Smart_Resource clone] → Ship1_C2[DLY] → Ship1_Flyout[DLY 2.0s] → Ship1_Kill[Expression clone] ─┐
 └─ Ship2_Queue[Smart_Resource clone] → Ship2_C2[DLY] → Ship2_Flyout[DLY 2.2s longer] → Ship2_Kill[Expression clone] ─┤
                                                                                                                  → Merge[Expression NEW] → DefenseOutcome / Kill/Miss counters / Plotter (existing, rewired)
Shared: FES_DB[Database Read/Write: threat, ship, load, TOF, preferred] + CommonRule[Virtual_Machine or Expression_Decision NEW] + ShipCoordinator[Smart_Controller NEW: input/output/pop]
```
Why: 2 ships expose over-engagement vs free-rider trade; FES+rule implement 3 of 8 DED tests (capability, inventory, load-balance + TOF tie-break); 5 omitted tests (notify-time, hard-cap-5, reengagement window, balance-tol-3, unit#) are documented as future.
Policies (same raid, switch by `Policy_Mode 0/1/2` top param NEW):
- A sectored (0): asset partition by `Priority<=3 → Ship1 else Ship2`, no DB read.
- B first-launch (1): `if launchFlag_ship1 set → Ship2 defers`; light comms via single boolean field.
- C DED-lite bidded (2): read FES, run common rule, defer if not preferred. Heavy (DB read) but still no Link-16 slots, no Swerling, no multi-track.
New top params: `Policy_Mode 2, Ship2_Range 6000 (→2.18s), Ship1_Inv 10, Ship2_Inv 10, GlobalInv_Enable false (Phase 1) → true (Phase 2 stretch), LoadWindow 5.0s`.

---

## 2. Sequential build flow — do in order, verify each gate

### STEP 0 — Baseline test & freeze (30 min, GUI, no edits)
0.1 License Manager on. `JAVA_HOME JDK17`. Open `MissileDefense_Model.xml` in Architect. Confirm 14 containers + stopTime 15.0.
0.2 Click canvas → record §0 params. Double-click each block → confirm Expression_Lists (§0), `Delay_Value`s, queue `Max10/Priority`, Display `fileName/saveText`, plotter input `Latency`.
0.3 Press GO. Open `DefenseOutcome` → 1 record per threat, check `L=DISPLAY_TIME-TIME`, `Flight≈2.1+wait`. Open `KillCount/MissCount` → `Kill+Miss==threats`. Open plotter → latency ~2.1s flat.
0.4 Run `MissileDefense_Model_Sweep.bat` (edit INSTALL_PATH first) → `Outcome_run1/2/3.txt`. Run `python summarize_missile_outcome.py` (now portable `root=dirname(__file__)`) → confirm run1-3 lines match §0.
0.5 Freeze: copy `MissileDefense_Model.xml` → `MissileDefense_Model_baseline.xml` in same folder. Never edit baseline again. **Gate: GO + sweep + scorer all pass.**

### STEP 1 — MCP workspace + discovery (20 min, read-only tools)
1.1 `visualsim_open_model_workspace(model_path=…/MissileDefense_Model.xml, project_root=…/MissileDefense_Share)` → expect `TARGET_EXISTS` if already opened; reuse `workspace_id mw_…33a6b0d7` or open with `copy_name=DEDlite`.
1.2 `visualsim_inspect_model_artifact(detail=full + containers)` → confirm 14, relations list §0, canvas locations.
1.3 `visualsim_describe_actor(Database)`, `(Smart_Controller)`, `(Expression_Decision)`, `(Smart_Resource)` → record `Input/Lookup_Fields/Mode`, `Block_Name/Smart_Resource_Name`, `Expression_List/Output_*`, queue 6 params. Do NOT propose until this is logged (Challenge 3 Trustworthy evidence).
1.4 `visualsim_list_patterns(context='compute scheduler workload traffic_source')` → note `workload_graph/traffic_front_end` justification for router→2 queues.
**Gate: workspace_id + 4 describe logs saved.**

### STEP 2 — Add Ship2 branch (governed edit 1)
2.1 `visualsim_propose_model_changes(workspace_id, operations_json=[add_entity Ship2_Queue class VisualSim.actor.lib.Smart_Resource (clone params Max10/Priority), add_entity Ship2_C2 class DLY (Delay_Value Flyout pattern), add_entity Ship2_Flyout class DLY, add_entity Ship2_Kill class Expression_Decision (clone Kill expressions with Ship2_Range/Speed)])` → review diff + approval_token. Expect 4 adds, 0 deletes.
2.2 `visualsim_apply_model_transaction(approval_token, expected_source_sha256=dd50dbce…)` → on stale-hash or changed-preview, stop, reopen, re-propose (do NOT force).
2.3 Reopen + `inspect containers` → expect 18 containers. Open GUI → confirm new blocks render, no unconnected mandatory port errors beyond pre-existing Font_Type.
**Gate: 18 containers, validation errors == 1 (Font_Type only).**

### STEP 3 — Add FES + common rule + coordinator (governed edit 2)
3.1 `propose(add_entity FES_DB class Database: Data_Structure_Text="threat ship load TOF preferred", Input_Fields="threat,ship", Lookup_Fields="threat,ship", Mode="Read", Linking_Name="FES"; add_entity CommonRule class VisualSim.actor.lib.Expression_Decision (or Virtual_Machine if Expression length limits hit); add_entity ShipCoordinator class Smart_Controller (Smart_Resource_Name="Ship1_Queue,Ship2_Queue"); add_entity PolicyRouter class Expression_Decision; set_parameter Policy_Mode=2, Ship2_Range=6000, Ship1_Inv=10, Ship2_Inv=10)`.
3.2 CommonRule pseudo-code to paste into `Expression_List` (adapt to VisualSim syntax, `//` comments allowed):
```
// DED-lite 3-test common rule (P3 pp.3-6 reduced)
canReach1 = (input.rangeToThreat < Engagement_Range); canReach2 = (input.rangeToThreat < Ship2_Range);
hasInv1 = (Ship1_Inv > 0); hasInv2 = (Ship2_Inv > 0);
load1 = queueLen_Ship1; load2 = queueLen_Ship2;  // via getBlockStatus(Scheduler) pattern per Scheduler_HW docs
eligible1 = canReach1 && hasInv1; eligible2 = canReach2 && hasInv2;
preferred = !eligible1 ? 2 : (!eligible2 ? 1 : (load1 < load2 ? 1 : (load2 < load1 ? 2 : (TOF1 <= TOF2 ? 1 : 2))));
input.preferredShip = preferred; input.deferShip = (preferred==1 ? 2 : 1);
```
3.3 Apply → reopen+inspect → expect 22 containers. **Gate: FES/Rule/Coordinator/Router present, no new errors.**

### STEP 4 — Wire policies A/B/C (governed edit 3)
4.1 `propose(connect PolicyRouter.output→Ship1_Queue.input + Ship2_Queue.input via relationShip1/Ship2; connect Ship1_Kill.KilledOnly/MissedOnly + Ship2_Kill.* → Merge.input; connect Merge.output→DefenseOutcome.input + counters via existing relationPost/Killed/Missed (rewire, don't duplicate); connect FES_DB.output→CommonRule.input; connect CommonRule.output→PolicyRouter.input; connect ShipCoordinator.pop→Ship1_Queue.pop_input + Ship2_Queue.pop_input)`.
4.2 PolicyRouter `Expression_List`:
```
// Policy_Mode 0 sectored, 1 first-launch, 2 DED-lite
if (Policy_Mode==0) input.ship = (input.Priority<=3 ? 1 : 2);
else if (Policy_Mode==1) input.ship = (launchFlag_other==true ? preferredFree : 1);  // defer on launch msg
else input.ship = input.preferredShip;  // from CommonRule/FES
```
4.3 Ship Kill clones: Ship1 keeps `Flyout=Engagement_Range/Speed`; Ship2 uses `Ship2_Range/Speed` (≈2.18s) to create TOF tie-break separation. Keep `Deadline 4.0`, `Shots/Inventory/Reload` formulas identical Phase 1.
4.4 Apply → inspect links → GUI open → confirm 3 end-to-end paths highlight correctly. **Gate: Policy_Mode 0/1/2 each routes without dangling relations.**

### STEP 5 — Single-policy smoke tests (GUI, no sweep yet)
5.1 Set `Policy_Mode=0, Input_Rate=1.0, Pk=0.8, stopTime=15` → GO → expect ~7 threats split by Priority, `DefenseOutcome` shows `ship` field, counters sum to threats.
5.2 Repeat `Policy_Mode=1`, then `2`. For each, record `threats, raw/effective, leakers, latency p50/p95` by hand from Display+plotter.
5.3 If any policy drops tokens (threats<expected) → check `Max_Queue_Length` rejection + `pop_input` wiring + `Output_Conditions` (`true,true,Effective,!Effective`) before proceeding. **Gate: all 3 policies complete 15s run.**

### STEP 6 — MCP verdict + sweep (evidence for judges)
6.1 `visualsim_run_to_verdict(model_path, overrides={Policy_Mode:2, Input_Rate:1.0, Pk:0.8}, objective={p95_latency<8, effective_Pk>0.25@raid7}, wait_seconds=…)` → `await_job` → `get_job_facts/get_evidence` → `diagnose_job` if failed → `evaluate_simulation_job(expectations={case_count, required_artifacts:[Outcome,Kill,Miss], csv_metrics, text_metrics})`.
6.2 `visualsim_sweep_and_analyze(model_path, space={Policy_Mode:[0,1,2], Input_Rate:[1.0,0.5,0.25], Pk:[0.5,0.8,0.95]}, objective=single PES or Pareto PES vs latency vs shots)` → record main effects + best point. Identical repeat resumes loop (don't start new).
6.3 `visualsim_diagnose_performance(job_pid)` → rank tuning (expect Queues/C2/DLY top) + idle list. Save job PIDs + fact sheets. **Gate: sweep table Policy×Rate×Pk with leakers/waste/latency.**

### STEP 7 — Bottleneck fix + re-run (innovation story)
7.1 Pick ONE fix from Step 6 (e.g. `Max_Queue_Length 10→20`, or `C2_Max 0.2→0.12`, or `Ship2_Range` rebalance for TOF fairness).
7.2 `propose(set_parameter …) → apply → reopen+inspect` → re-run Step 6 subset → prove `leakers↓ or p95↓` with numbers. Log AI mistake + correction if any (Challenge 3 Trustworthy).
**Gate: before/after numbers on same raid.**

### STEP 8 — Stretch only if time (global inventory + Poisson)
8.1 Global magazine: `set GlobalInv_Enable=true` + `Database GlobalInv (Mode Read/Write)` decremented by `Shots`, reload `DLY` blocking launch at 0. Re-test Policy 2 only.
8.2 Poisson raids: `ThreatGenerator.Time_Distribution Fixed→Exponential(Value_1)` → re-sweep `Input_Rate 1.0/0.5`. Document `E[interarrival]=Value_1`.
Skip both if video/write-up at risk — baseline+Steps 0-7 already submit.

### STEP 9 — Freeze + submission pack (half day)
9.1 Freeze `MissileDefense_DEDlite.xml` + `params.csv` (+ new rows `Policy_Mode, Ship2_Range, Ship1/2_Inv` tagged assumption) + `sweep.bat` (+ `-Policy_Mode` flag) + `scorer.py` (+ `ship/preferred` parse) + `documentation.md` update (§§3/6/14 DED-lite delta).
9.2 Slides 8-10: problem → arch (baseline vs DED-lite diagram §1) → VisualSim use → experiments (raid chart + Policy A/B/C bar + Pareto) → innovation (3 of 8 tests) → results.
9.3 Write-up 2-3p: Golden Dome/Guam+DOTE why, federated-M&S approach, innovation AI DED-lite, assumptions (logical time, Bernoulli, per-token inventory Phase 1, no Link-16/Swerling/multi-track), results/conclusions, refs grouped [M&S][Fusion][Guidance][Ref].
9.4 Video 5-min: model + GO + Display + plot + sweep table + fix. Keep prompts/MCP log appendix (plan_task, describe×4, compile/open, run/sweep/seek, propose/apply/inspect, diagnose).

---

## 3. Background retained (condensed from prior planner)

Challenges: enter **1 (new system) + 3 (AI workflow)**; 2 (re-engineer ComJam/Avionics/AFDX) is fallback narrative. Submission needs model + slides + write-up + video. VisualSim is compute/network/sensor-decision modeller, NOT 6-DoF/CFD — abstract flyout as DLY+Pk (Lukacs). Discovery: `search_models(missile defense…)=0 hits` (novelty); `Full_System_ComJam_Model (283 blocks RF/jam)` + `Animation_Target_Processing (48 blocks space/power/scheduler)` are bases only if pivoting; idioms `workload_graph/traffic_front_end/accelerator_node` + patterns `ptn_c90932cdfe29` justify router→queues. Research: DSB Phase III, NPS product-line, Krill timing budgets, SHIELD 2025, DOT&E FY24/25, Maurer/Frenkel/Humali fusion, Moskowitz coordination (most simulatable), Lukacs guidance, IMM-KF 2024, SR-UKF hypersonic, SWORD EADSIM, MDA THAAD/C2BMC, CRS Golden Dome, C3.ai MDA — group as [M&S][Fusion][Guidance][Ref], 4-6 well-used > 16 dumped. Risks: aero-modelling, sim explosion (cap via TG batching + caps_json + LHS), credibility (cite DSB/DOT&E federation need), hallucination (describe before propose + diagnose + log corrections), power gap (PowerTable/Battery reuse), time crunch (MVP = baseline + raid sweep + 1 Pareto).

*End — execute Steps 0→9 in order; do not skip gates; baseline file stays frozen.*

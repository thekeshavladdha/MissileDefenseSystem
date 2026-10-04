# CONTEXT — MissileDefense DED-lite build (handoff for next AI agent)
Date: 2026-10-04 | Author: Muse Spark (opencode) + user | Status: structure complete, awaiting first clean GO

## 1. Objective
Modify `MissileDefense_Share/MissileDefense_Model.xml` (single-ship baseline) into a 2-ship DED-lite
(sectored vs first-launch vs bidded-lite, selectable by top param `Policy_Mode 0/1/2`) for hackathon
Challenge 1 (new system) + Challenge 3 (AI workflow). Reference paper: Moskowitz/Gassler/Paulhamus 2002
TBMD engagement coordination (DED bidded scheme); implement 3 of its 8 sieving tests only
(capability, inventory, load/TOF tie-break). Everything else (Link-16 slots, Swerling, multi-track,
4-ship FES) is explicitly out of scope.

## 2. Directory layout (C:\Games\Mirabilis_hackathon)
- `MissileDefense_Share/` — ALL WORK HAPPENS HERE
  - `MissileDefense_Model.xml` — working model (currently 23 containers, ~41KB). MCP workspace copy:
    `MissileDefense_Share/models/MissileDefense_Model.xml` (authoritative for MCP transactions).
  - `MissileDefense_Model_baseline.xml` — frozen 14-container original (34190B, sha dd50dbce…).
    NEVER EDIT. Ground truth for maths/docs.
  - `missile_defense_parameters.csv` — 21-row param price-list, all Assumption/Estimate.
  - `MissileDefense_Model_Sweep.bat` — 3-run batch (Pk 0.5/0.8/0.95, seeds 1001/1002/1003). Needs
    `-Policy_Mode` extension for DED-lite sweep (not done).
  - `summarize_missile_outcome.py` — portable scorer (root=dirname(__file__), fixed from satvi path).
    Baseline outputs: run1 7/4/2/5 0.571/0.286, run2 7/6/2/5 0.857/0.286, run3 7/7/5/2 1.000/0.714.
  - `MissileDefense_Outcome*.txt`, `MissileDefense_Kill/Miss_Count.txt` — baseline logs. DO NOT overwrite
    until DED-lite GO passes (they are the before/after evidence).
  - `MissileDefense_Model_Report.md` — 1-page share guide. `MissileDefense_Qwen_Research.md` — theory pack.
  - `documentation.md` — full model doc (50KB). STALE re DED-lite deltas (§§3/6/14 need Merge/Router update).
  - `fes_table.csv` — NEW parked FES lookup table (CSV `Priority,shipHint` + `int,int` typerow, 1→1…5→2).
    Created for Phase-2 file-backed FES_DB. NOT WIRED to anything.
  - `.visualsim-mcp/` — MCP cache (handoffs, traceability.db, workspaces/a50ecb73, transactions/*).
    Regenerable; deleted once for cleanup, recreated by later opens.
- `planner.md` (repo root) — rewritten as 10-step DED-lite build plan (Steps 0–9 with gates). Follow it.
- `VisualSim_Hackathon_2026_project/` — READ-ONLY research: `research.txt` (4 paper URLs), `research/`
  (P1–P4 PDFs/TXTs, notes/P1-P4.md incl. full P3 DED breakdown, report.md, synthesis.md, open-questions.md),
  `SKILL.md` (paper-research workflow). Never modify.
- Install: `C:\VisualSim_2641\VS_AR` (verified Test-Path True). JDK17
  `C:\Program Files\Java\jdk-17`. Model `_createdBy 2020.Q2`.

## 3. Baseline model (frozen, 14 containers)
Chain: `ThreatGenerator[DS_Source Fixed(1/s) Header] → DetectionAssignment[Expression 7 lines] →
InterceptorQueue[Smart_Resource Max10 Priority] → C2_Latency[DLY] → InterceptorFlyout[DLY 2.0s] →
KillAssessment[Expression 5 lines, 4 ports] → DefenseOutcome[Display] / KillCounter→KillCount /
MissCounter→MissCount / Latency→TimedPlotter + Const pop helper`. Director DEDirector stopTime 15.0.
Top params: Input_Rate 1.0, Execution_Time 2.5, Pk 0.8, Intercept_Deadline 4.0, Track_Threshold 3,
C2_Min 0.05, C2_Max 0.2, Interceptor_Speed 2750, Engagement_Range 5500, InterceptorInventory 10,
Reload 10–30, Modelseed seed(12345), View_Stats true.
Detection expr: `Priority=irand(1,5); Track_Hits=Threshold; Firm=true; C2=rand(Min,Max);
Flyout=Range/Speed; Flight=C2+Flyout; Killed=rand<Pk`.
Kill expr: `Leaker=(TNow-TIME)>Deadline; Effective=Killed&&!Leaker; Shots=Eff?1:2;
Inventory=10-Shots; Reload=rand(10,30)`; ports output/Latency/KilledOnly/MissedOnly,
cond `true,true,Effective,!Effective`. Scores: leakers=threats-effective,
raw_Pk=killed/threats, effective_Pk=effective/threats.

## 4. Current DED-lite model (23 containers, all MCP-applied, validation ok:true)
ADDED (9): Ship2_Queue/Smart_Resource, Ship2_C2/DLY, Ship2_Flyout/DLY, Ship2_Kill/Expression,
CommonRule/Expression, ShipCoordinator/Smart_Controller (UNWIRED observer, documented),
PolicyRouter/Expression, Merge/Expression, Const2/Const. REMOVED (1): FES_DB/Database (see §6).
Top params ADDED (4): Policy_Mode=2, Ship2_Range=6000.0, Ship1_Inv=10, Ship2_Inv=10.
WIRING (every relation exactly 2 endpoints — deliberately, see §6 broadcast lesson):
- relationDR: DetectionAssignment.output → CommonRule.input
- relationRule: CommonRule.output → PolicyRouter.input
- relationShip1: PolicyRouter.ship1Out → InterceptorQueue.input
- relationShip2: PolicyRouter.ship2Out → Ship2_Queue.input
- relation2/relationFlyout/relation5: Ship1 Queue→C2→Flyout→KillAssessment.input (unchanged)
- relationShip2Q/C/F: Ship2 Queue→C2→Flyout→Ship2_Kill.input
- relationPost (3 links, 2 writers 1 reader): KillAssessment.output + Ship2_Kill.output → Merge.input
- relationMergeOut: Merge.output → DefenseOutcome.input
- relationKilled: Merge.KilledOnly → KillCounter.incr_add_input
- relationMissed: Merge.MissedOnly → MissCounter.incr_add_input
- relation3: Merge.Latency → xTime_yData_Plotter.input
- relationKillStats/MissStats: counters → KillCount/MissCount (unchanged)
- relation6: Const.output → InterceptorQueue.pop_input ; relationPop2: Const2.output → Ship2_Queue.pop_input
- relation7: ThreatGenerator.output → DetectionAssignment.input (unchanged)
- EMPTY (harmless, no remove_relation op exists): relation, relationShipBoth, relationFES.
EXPRESSIONS:
- Ship2_C2 Delay=C2_Latency ; Ship2_Flyout Delay=Ship2_Range/Interceptor_Speed (≈2.18s vs Ship1 2.0s = TOF split)
- Ship2_Kill: Kill clone with `Inventory_Left = Ship2_Inv - Shots` (no Output split needed; Merge splits)
- CommonRule: `shipHint = Priority<=3?1:2; hasInv1/2=(Ship_Inv>0); preferredShip = !hasInv1?2:(!hasInv2?1:shipHint)`
  (FES table inlined — identical mapping to deleted DB rows + inventory check)
- PolicyRouter: `sectoredShip = Priority<=3?1:2; ship = Mode0?sectored : Mode1?1 : preferredShip`;
  Output_Ports ship1Out,ship2Out / Values input,input / Conds `input.ship==1,input.ship==2` (true routing)
- Merge: passthrough comment; Output ports output/Latency/KilledOnly/MissedOnly (each _type general);
  Values input,TNow-TIME,input,input; Conds true,true,Effective,!Effective.
Full chain: Threat→Detection→CommonRule→PolicyRouter→Ship1/Ship2 Queues→C2→Flyout→Kills→Merge→
Outcome/counters/plotter ; Const→Ship1 pop, Const2→Ship2 pop.

## 5. Transaction log (workspace mw_…a50ecb73, project_root MissileDefense_Share)
All via propose→review→apply→reopen+inspect→Copy-Item models→source. Approve tokens single-use;
TOKEN_INVALID seen once (transient; re-propose identical ops works). Stale-sha on divergent file:
realign by copying DISK→models then re-inspect (but see §7 divergence discipline).
1. be78c9e6 ADD Ship2×4 (18 containers) — first propose failed (target+container both passed;
   add_entity takes container_path ONLY).
2. f769cfd9 ADD FES_DB/CommonRule/ShipCoordinator/PolicyRouter (22).
3. 55c90916/e59f2814/263f61a9 SET delays + Policy_Mode/Ship2_Range/Ship1/2_Inv + Ship2_Kill/CommonRule-stub/
   PolicyRouter-stub expressions (e59f applied; 55c9 re-proposed as part of 263f).
4. 8c39cc1f/29930a56 CONNECT Ship2 chain + ADD Merge + PolicyRouter→Ship2 (broadcast era).
5. df1a7f2c ADD Merge ports KilledOnly/MissedOnly/Latency (MISSING_PORT fix).
6. 0f989f4c CUTOVER kills→Merge→Outcome/counters/plotter (full fan-in, ok:true).
7. d2ff104e BYPASS FES/Coordinator: FES→Rule + Coord→Ship2pop removed; Const→BOTH pops broadcast.
8. 6eb5bf2b/a2bb7aff PARAMS: FES table+fields, queue names, Coordinator names, Ship2_Flyout TOF expr,
   CommonRule/PolicyRouter full expressions.
9. 58c1b08d/7a24248a CHAIN: Detection→FES→Rule→Router series + Coordinator observer on broadcast.
10. a6fed1ce/ce2fcbe2→95e0dbdd QUOTING fixes (string params MUST be "..." quoted or object-type crash).
11. bb3f7dd0 BLANK Output_Expression (was `match` → evaluated as variable → undefined ID).
12. 246056df TABLE FIX: newline rows (&#10;) + Lookup `Priority` case match.
13. 724a948c INLINE FES into CommonRule + Detection→CommonRule direct (DB out of firing path).
14. 1485b131 DELETE FES_DB entity (init crash unfixable blind — §6).
15. cc06f11c PORT TYPES Merge 3 ports → _type general (TypeConflict fix — baseline comparison).
16. 24ce665c ADD Const2 + PolicyRouter ship1Out/ship2Out (+types) + Output routing (broadcast→routing).
17. cc3ca4c1 TRUE ROUTING rewire (all-2-endpoint; §4 wiring). ← CURRENT HEAD.
Backups: .visualsim-mcp/transactions/*/backup.xml + rollback_tokens per apply. Baseline file untouched.

## 6. Problems fixed (with root causes — reuse these patterns)
- P0 benign: Font_Type UNKNOWN_PARAMETER on DefenseOutcome + 4 UNBOUND_FILE pre-run warnings — cosmetic,
  present since baseline; ignore.
- Seeds identical across sweep → runs bit-identical. Fixed in .bat (1001/1002/1003). Scorer root hardcoded
  satvi path → made portable (dirname(__file__)); verified run1-3 lines.
- add_entity takes container_path ONLY (not target+container). connect needs ≥2 ports.
- **String params MUST be "..." quoted** (Block_Name, Priority_Field, Input/Lookup_Fields, Linking_Name):
  unquoted → evaluated as variable/object reference → `Cannot store Smart_Resource object in string` (Ship2_Queue),
  `Database_01 Input Field not set` (FES_DB). Confirmed vs shipped Animation_Target_Processing Database3
  (`Input_Fields="Next"`, Linking `"Process_Time"`, space-separated multi-space table, StringAttribute text).
- **Output_Expression="match"** evaluated as variable → `ID match undefined`. Shipped DBs OMIT the property
  (default=matched row). Blanked to "".
- **FES_DB `Data Structure not recognized: null`** (3 rounds: fields→expression→table): table flattened to one
  line (newlines collapsed) + lowercase `priority` vs token `Priority`. Fixed text to &#10; rows + case match
  per doc ("first row column names") — BUT error persisted because… (next).
- **Stale-session divergence (BIGGEST time sink)**: user edited canvas in Architect while MCP edited disk copy.
  Screenshots showed WIRED FES_DB after MCP bypassed it; 02:18 canvas even restored Detection→Ship1 direct
  (= double-fed threats + crash). Discipline: whoever edits (GUI or MCP), the other side must
  close-without-save / realign (Copy-Item direction matters!) before next op. Workspace copy =
  models/MissileDefense_Model.xml; source = MissileDefense_Share/MissileDefense_Model.xml.
- **FES_DB deleted**: inline table init needs a DS registry entry this build can't satisfy blind
  (null DS at block INIT, fires even unwired). Decision: delete entity, inline mapping in CommonRule
  (identical values), park table as fes_table.csv (doc-spec CSV+typerow) for Phase-2 file-backed FES.
  DED-lite idea intact (table→rule→router→ships).
- **TypeConflictException (all `unknown` inequalities)**: add_port creates typeless ports; originals carry
  `_type general`. Fix = set_port_metadata type=general (Merge ×3 verified vs baseline XML).
- **Manager `begin 0, end -1, length 19`**: broadcast relations (1 output → 2-4 readers: relationShipBoth×4,
  relation6×3). Validator's own hint (UNSAFE_FAN_OUT → use Fork). Fix = true routing (Router two output
  ports + conditions; separate Const per queue). relationPost 2-writers-1-reader merge kept (standard).
- Server `run_to_verdict` refused CAPACITY_EXCEEDED (heap est 1800MB, 22 entities) — DO NOT use for this
  model; test in local Architect GO + .bat sweeps. heap ceiling=null, static floor applied.

## 7. Still open / risks for next agent
1. **NO clean GO yet end-to-end** — every fix so far is validator-clean (`ok:true`) but GUI run is the real
   gate. Next: fresh reopen (discard any unsaved canvas!) → GO Policy_Mode 0/1/2 → confirm ~7 threats each,
   Kill+Miss==threats, ship split by Priority in Mode 0.
2. **ShipCoordinator UNWIRED observer** (no links after broadcast removal). Configured+documented; needs Fork
   actor (Connect_EIO per validator) for closed-loop pop driving — Phase 2. If it throws at init despite no
   links, delete or blank its Smart_Resource_Name.
3. **Empty relations** (relation, relationShipBoth, relationFES) — harmless if manager passes; no remove op.
   If manager substring crash recurs, suspects in order: (a) relationPost 3-link merge → split Merge into two
   input ports; (b) empty relations (recreate model without them — no tool path, would need GUI or raw edit,
   which MCP forbids — escalate to user).
4. **Ship2_Kill has no Output split** (by design; Merge splits). Fine unless VisualSim requires Output_* on
   multi-out blocks — it doesn't (DetectionAssignment has none either).
5. **CommonRule shipHint vs DB**: if Phase-2 file FES is re-added, point fileOrURL at fes_table.csv and change
   CommonRule to read input.shipHint instead of computing it; remove the ternary line.
6. **Divergence discipline**: before ANY propose, verify disk-vs-workspace sync (compare lengths/sha via inspect
   source_sha256). Current disk length after last sync — re-check with Get-Item. If user touched GUI, realign
   FIRST (direction depends on which side is authoritative; default: MCP workspace wins → copy models→source;
   user's fresh GUI fixes win → copy source→models, then inspect).
7. STALE docs: documentation.md §§3/6/14 predate DED-lite; planner.md Steps 0–4 done, 5–9 pending (smoke×3,
   sweep Policy×Rate×Pk via extended .bat + scorer ship-field parse, 1 bottleneck fix + re-run, freeze
   MissileDefense_DEDlite.xml + slides/write-up/video). params.csv lacks Policy_Mode/Ship2_Range/Ship1/2_Inv
   rows. Sweep .bat lacks -Policy_Mode legs. Scorer lacks ship split.
8. Plotter shows Merge.Latency only — fine. KillCount/MissCount step logs unchanged semantics (effective only).
9. Rollback available for every apply (rollback_token in outputs + backup.xml). Baseline file is ultimate reset:
   Copy-Item baseline→Model (+ delete models copy + reopen workspace) if DED-lite work ever needs restart.

## 8. Verification commands (PowerShell, workdir MissileDefense_Share)
- `Get-Item .\MissileDefense_Model.xml | Select Length` ; scorer: `python summarize_missile_outcome.py`
- MCP: open_model_workspace(model_path=.../MissileDefense_Model.xml, project_root=.../MissileDefense_Share)
  [expect TARGET_EXISTS → reuse mw_…a50ecb73]; inspect(detail=full|summary|containers);
  describe_actor(Database/Smart_Controller/Expression, detail=full); propose→apply→inspect→Copy models→source.
- GO checklist (Architect): License Mgr on → open DISK file fresh → set Policy_Mode → GO 15s →
  DefenseOutcome ~7 records (L=DISPLAY-TIME, Flight≈2.1+wait) → Kill+Miss==threats → plotter ~2.1s →
  repeat Modes 0/1/2 → extend .bat → scorer table → 1 fix → re-run → freeze.
- Red-flag errors map: `Database_01`→DB fields/table; `ID X undefined`→unquoted/keyword expression;
  `cannot store ... object in string`→unquoted string param; `TypeConflict ... unknown`→port _type;
  `manager begin/end`→broadcast relations; `CAPACITY_EXCEEDED`→use local GO, not server.

## 9. Key references
planner.md (build plan) | documentation.md (model bible, needs DED update) |
MissileDefense_Model_Report.md (share guide) | MissileDefense_Qwen_Research.md (theory) |
research/notes/P3_Moskowitz2002.md (DED 8-test sieving, FES, 4.375/12.25s, Link-16 slots — the paper logic
behind CommonRule/PolicyRouter) | research/synthesis.md §6 (corpus gives architecture not calibrations —
why every param is Assumption) | fes_table.csv (parked FES) | .visualsim-mcp (all txns/backups).

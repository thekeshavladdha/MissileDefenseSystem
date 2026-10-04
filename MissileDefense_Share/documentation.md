# MissileDefense_Share — Complete Model Documentation

> VisualSim Architect Discrete-Event Model | Single-layer ground-based air & missile defense
> Working model: `MissileDefense_Model.xml` | Starter: `MissileDefense_Start.xml` | Reference-only: `MissileDefense_Architecture_Model.xml`
> Scope: system-level latency / resource / Pk trade study. NOT 6-DOF flight dynamics, NOT RF physics, NOT multi-ship coordination.
> All performance numbers are logical-time simulation outputs with assumption-tagged inputs. No classified or measured system data is contained.

---

## Table of Contents

1. [What This Package Is](#1-what-this-package-is)
2. [File Inventory — Every Section Explained](#2-file-inventory--every-section-explained)
3. [Architecture](#3-architecture)
4. [Strategy / Doctrine Encoded](#4-strategy--doctrine-encoded)
5. [Parameters — Complete Reference](#5-parameters--complete-reference)
6. [Maths — Exact Equations Executed](#6-maths--exact-equations-executed)
7. [Data-Structure Lifecycle — Field-by-Field](#7-data-structure-lifecycle--field-by-field)
8. [Simulations — How to Run](#8-simulations--how-to-run)
9. [Results — How to Read Every Output File](#9-results--how-to-read-every-output-file)
10. [Worked Examples With Real Numbers](#10-worked-examples-with-real-numbers)
11. [Queueing, Timing and Bottleneck Behaviour](#11-queueing-timing-and-bottleneck-behaviour)
12. [VisualSim Block Semantics Used](#12-visualsim-block-semantics-used)
13. [Validation State (MCP-Verified)](#13-validation-state-mcp-verified)
14. [Assumptions, Limitations, Pitfalls](#14-assumptions-limitations-pitfalls)
15. [Research Traceability vs Papers](#15-research-traceability-vs-papers)
16. [DED Complexity Comparison](#16-ded-complexity-comparison)
17. [Hackathon Use and Extension Cookbook](#17-hackathon-use-and-extension-cookbook)
18. [Glossary](#18-glossary)
19. [Cheat Sheet](#19-cheat-sheet)
20. [Version and Provenance](#20-version-and-provenance)

---

## 1. What This Package Is

`MissileDefense_Share` is a **Level-0/1 discrete-event sizing model** of a ground-based missile-defense kill chain defending a high-value asset against theater ballistic / cruise-like threats.

In one sentence: **threats arrive on a fixed clock, get a random priority, wait in a bounded priority queue, suffer a random C2 delay plus a fixed flyout delay, then live or die by a Bernoulli(Pk) dice roll gated by an intercept deadline.**

It answers one class of question well:

> For a given arrival rate, C2 latency spread, flyout time and single-shot Pk, what is raw Pk vs effective (on-time) Pk, how many leakers escape, and where does queueing inflate end-to-end latency?

It deliberately does NOT answer: radar detection physics, multi-sensor fusion accuracy, Link-16 loading, multi-ship weapon-target assignment, interceptor guidance, power/thermal, or cost. Those are listed as future work with concrete hooks (see §17).

MCP verification performed for this doc:

- `open_model_workspace(MissileDefense_Model.xml)` → workspace `mw_…33a6b0d7`, `source_sha256 dd50dbce…`, 14 containers.
- `inspect_model_artifact(full + containers 0-5, 5-20)` → root `/MissileDefense_Model` + 13 children enumerated in §3.
- `describe_actor(DS_Source / Expression_Decision / DLY / Smart_Resource)` → Traffic-generator, ExpressionList routing, Delay-hold, Queues-with-arbitration semantics.
- `search_models(missile defense radar tracking interceptor)` → 0 hits (novelty proof, no turnkey base copied).
- Direct XML grep for `Expression_List`, `Delay_Value`, `Execution_Time`, `stopTime`, queue params to quote exact executed strings.

---

## 2. File Inventory — Every Section Explained

### 2.1 `MissileDefense_Model.xml` — the executable (SHARE THIS)

The only file a judge needs to open and press GO. ~14 MoML entities:

- Top-level parameters (§5) + `DigitalSimulator DEDirector stopTime 15.0`.
- Chain: `ThreatGenerator → DetectionAssignment → InterceptorQueue → C2_Latency → InterceptorFlyout → KillAssessment → DefenseOutcome / KillCounter→KillCount / MissCounter→MissCount / Latency→Plotter`, plus `Const` pop helper.
- Relations verified: `relation, relation2, relation3, relation5, relation6, relation7, relationFlyout, relationPost, relationKilled, relationMissed, relationKillStats, relationMissStats`.

### 2.2 `MissileDefense_Start.xml` — minimal starter (OPTIONAL EXTRA)

Same `Input_Rate / Execution_Time / Modelseed seed(12345) / View_Stats true / stopTime 15.0` + single `Queue [Smart_Resource, Max 10, Priority_Field="Priority"]` + `DS_Source`. No C2/flyout/kill. Purpose: learn enqueue → dequeue → Display before opening the full chain. Verified by 100-line head read.

### 2.3 `MissileDefense_Architecture_Model.xml` — FPGA reference (DO NOT PRESENT AS MISSILE MODEL)

~2.36 MB signal-processing model: `ADC Board, Function1 @FPGA, Function2 FFT and IFFT, Function3 Matrix Transpose, Function4 Matrix Processing, Function5 IDFT, Function6 Complex Modulus, Function7 Buffering, Function8 Target_Separation, ST Flow Buffering, MT Flow Buffering, PCI Bus, uEngine ×2, Dispatcher (CSV C2_Flow_01.csv + Database Task_ID/Dispatch_CPI/Dispatch_PRI + IN/OUT global destinations)`. Useful ONLY if you later model radar DSP load. The share report explicitly says do not share its internals as the final missile model.

### 2.4 `missile_defense_parameters.csv` — parameter price-list (SHARE)

21 rows, columns `Parameter, ValueOrRange, Unit, Source, Confidence`. Every row is `Assumption` except one `Estimate` (C2BMC bandwidth). It mixes wired knobs (Pk, C2 min/max, speed, range, deadline, threshold, inventory, reload, Input_Rate, Execution_Time) with CSV-only context (threat speed 2000–7000 m/s, radar 300–1000 km, scan 1–10 Hz, false-alarm 1e-6, C2BMC 10–100 Mbps). CSV-only rows are NOT wired to any block — they document the narrative envelope only.

### 2.5 `MissileDefense_Model_Sweep.bat` — 3-point batch runner (SHARE)

Three `VisualSimBatchModeSimulator` invocations differing only in `-Pk` and `-Modelseed` and output filename. Common flags: `-run 1/2/3 -resultpath %INSTALL_PATH%\workflow -Execution_Time 2.5 -Input_Rate 1.0 -Intercept_Deadline 4.0`. Seeds `seed(1001)/seed(1002)/seed(1003)` are the applied fix so Pk runs are not bit-identical. Requires editing `JAVA_HOME=C:\Program Files\Java\jdk-17` and `INSTALL_PATH` plus `flexlm.jar / EccpressoAll.jar / flexlmutil.jar` on classpath.

### 2.6 `summarize_missile_outcome.py` — scorer (SHARE)

~25-line regex scorer. `glob Outcome_run*.txt` under hard-coded `root=C:\Users\satvi\Desktop\VisualSim\VS_AR\workflow` (EDIT THIS PATH), `re.split DISPLAY AT TIME`, per-block `re.search ID / Killed / Effective_Kill / Firm_Track`, counts threats/killed/effective/firm, `leakers = threats - effective`, prints `threats raw_kills effective_kills leakers firm_tracks raw_Pk effective_Pk` with `:.3f` and zero-division guard.

### 2.7 `MissileDefense_Outcome.txt` + `Outcome_run1/2/3.txt` — per-threat logs (EXAMPLE OUTPUTS)

`Display` dumps: `DISPLAY AT TIME ------ Xs ------ {BLOCK=ThreatGenerator, C2_Latency=…, DELTA, DS_NAME=Header_Only, Effective_Kill, Firm_Track, Flight_Time, Flyout_Time, ID, INDEX, Inventory_Left, Killed, Leaker, Priority, Reload_Wait, Shots_Fired, TIME, Task_Latency, Time_Array={in,out}, Trace_Array={"Queue_in","Queue_out"}, Track_Hits=3}`. Default file has 7 threats; run1 (Pk0.5), run2 (Pk0.8), run3 (Pk0.95) each have 7 threats with different dice.

### 2.8 `MissileDefense_Kill_Count.txt` / `Miss_Count.txt` — counter step logs

`Display` of `Counter_Basic.counter_output`: `DISPLAY AT TIME ------ Xs ------ N` with N = 1,2,3… Example default: kills at 4.33/10.60/14.78 s → 1/2/3; misses at 2.18/6.39/8.49/12.66 s → 1/2/3/4. Totals = effective kills / non-effective outcomes, NOT raw dice hits.

### 2.9 `MissileDefense_Model_Report.md` — 1-page share guide (READ FIRST)

States which XML to share, pipeline in 5 lines, GUI + batch run steps, two fixes already applied (seeds differ; leakers = threats − effective_kills; report raw_Pk + effective_Pk), latest sweep numbers (run1 7/4/2/5 0.571/0.286; run2 7/6/2/5 0.857/0.286; run3 7/7/5/2 1.000/0.714), and known limitation (per-engagement inventory, not global depletion).

### 2.10 `MissileDefense_Qwen_Research.md` — 10-section theory pack

Scope (single-layer ground system, constant-velocity abstraction), research question (C2 + Pk → asset protection), 6 sources (Wilkening 1999/2000, O’Haver 2014, Brown JOINT DEFENDER 2005, DOTE 2025, Simpkins NPS 2001, VisualSim 2026), param table (all Assumption/Estimate), 7-step flow (launch→detect→M-of-N→C2→flyout→homing→BDA/Shoot-Look-Shoot), block mapping (Source/System/Simulator/Params/Plotter/Histogram/Counter), demo dirs (`demo/Defense_and_Space/*`, `lib/Queuing`; local equivalents `demo/Communication/Software_Radar_System`, `demo/Aerospace/Beamforming_Radar|ACS|UAV`), 5 sweeps (saturation, redundancy, Pk, C2, policy), pitfalls (license, JAVA_HOME, MCP paths, index build, ms/s mix), roadmap Phase1-deterministic → Phase4-DOE.

### 2.11 This `documentation.md` — master doc

Superset of all above plus exact maths, field dictionary, queueing notes, MCP validation, paper traceability, DED comparison, hackathon cookbook.

---

## 3. Architecture

### 3.1 Top view

```
                        DigitalSimulator (DEDirector, digitalDomainOnly=true, debugger Off, stopTime 15.0, res 1E-12)
                        Top params: Input_Rate, Execution_Time, Pk, Intercept_Deadline, Track_Threshold,
                                    C2_Latency_Min/Max, Interceptor_Speed, Engagement_Range,
                                    InterceptorInventory, Reload_Time_Min/Max, Modelseed, View_Stats

ThreatGenerator ──relation7──> DetectionAssignment ──relation──> InterceptorQueue ──relation2──> C2_Latency
 [DS_Source]                  [Expression_Decision]              [Smart_Resource]                   [DLY]
 Fixed(1.0s)                  7-line expression                  Max10 ×1, Priority                 hold per-token C2
 Header token                 priority/hits/C2/                  First_Token_Flow_Through            Delay_Value="C2_Latency"
                              flyout/kill draw                   Incoming_Token_Rejected

C2_Latency ──relationFlyout──> InterceptorFlyout ──relation5──> KillAssessment ──relationPost──> DefenseOutcome
                                                                    [Expression_Decision]            [Display → .txt]
                               hold 2.0s                             5-line + 4-port fan-out
                               Delay_Value="Flyout_Time"             Leaker/Effective/Shots/Inventory
                                                                     Output_Values=input,TNow-TIME,input,input
                                                                     Output_Ports=output,Latency,KilledOnly,MissedOnly
                                                                     Output_Conditions=true,true,Effective,!Effective
                                                                          │                  │                  │
                                                              relationKilled│      relationMissed│     relation3│
                                                                            ▼                    ▼              ▼
                                                                     KillCounter            MissCounter     xTime_yData_Plotter
                                                                     [Counter_Basic]        [Counter_Basic]  [TimedPlotter]
                                                                     Normal_Counter_Update                   latency vs time
                                                                          │                  │
                                                              relationKillStats│    relationMissStats│
                                                                            ▼                    ▼
                                                                        KillCount              MissCount
                                                                        [Display → .txt]       [Display → .txt]

Const ──relation6──> InterceptorQueue.pop_input   +   Const.trigger ──relation5──> shared with flyout→kill path (pop/schedule helper)
ThreatGenerator.output→relation7, DetectionAssignment.input→relation7 / output→relation, Queue.input→relation / output→relation2 / pop_input→relation6,
C2.input→relation2 / output→relationFlyout, Flyout.input→relationFlyout / output→relation5, Kill.input→relation5 / output→relationPost / Latency→relation3 / KilledOnly→relationKilled / MissedOnly→relationMissed.
```

Container count 14 = 1 root + 13 children: ThreatGenerator, DetectionAssignment, InterceptorQueue, C2_Latency, InterceptorFlyout, KillAssessment, DefenseOutcome, KillCounter, MissCounter, KillCount, MissCount, xTime_yData_Plotter, Const (+ root). Locations (canvas): Threat [11,139], Detection [97,138], Queue [193,128], C2 [330,150], Flyout [383,150], Kill [436,50], KillCounter [520,50], MissCounter [520,120], KillCount [620,60], MissCount [620,120], DefenseOutcome {468,190}, Plotter [558,49], Const [357,217].

### 3.2 Director and canvas

- `VisualSim.simulators.de.kernel.DEDirector`, `digitalDomainOnly true`, `digitalDebugger Off` (choices Off/Pause/Run/Summary_Only), `stopTime 15.0`, `timeResolution 1E-12` shared param.
- `_createdBy 2020.Q2`, window `{bounds -7,-7,1550,830 maximized}`, ModelBuilder size `[1324,714]`, zoom `136845.55` (saved zoom, irrelevant to semantics), center `{340,276}`.
- Every top param is a blue `-P-` `VisibleParameterEditorFactory` icon at `[210,32]…[210,130]` + `Modelseed [210,75]` + `View_Stats [216,97]`.

### 3.3 Why this topology

Linear pipeline = cheapest discrete-event surrogate that still exhibits arrival → contention → delay → reliability → deadline interaction. No feedback loop is actually wired (Shoot-Look-Shoot is booked as `Shots=2`, not re-injected). No branching except the 4-port Kill fan-out to counters/plot/file. This keeps event count ≈ threats (≈7/15 s) so sim runs instantly and batch sweeps finish in seconds.

---

## 4. Strategy / Doctrine Encoded

1. **Single layer, single shooter.** One radar + one battery. No boost/midcourse/terminal layering, no GMD/Aegis/THAAD/Patriot mix, no space cue, no 4-ship force. Engageability is therefore 1 for every threat that arrives.
2. **Firm-track gate as constant.** Real M-of-N needs N consecutive detections with Pd/Pfa; here `Track_Hits = Threshold = 3` so `Firm_Track ≡ true`. The gate is present structurally but numerically inert — intentional Phase-1 deterministic baseline per Qwen §10.
3. **Random priority queue, not weapon-target assignment.** `Priority = irand(1,5)`. Queue reorders by it. No capability, geometry, inventory-balance, or TOF tie-break. No grouping by defended asset, no freezing, no common algorithm.
4. **Two-delay flyout abstraction.** `C2 ~ U(0.05,0.2)` + `Flyout = 2.0` replace guidance, propulsion, seeker, and lethality chain. `Flight_Time` in the log is C2+Flyout only; end-to-end `(TNow−TIME)` adds queue wait on top.
5. **Shoot-look-shoot as accounting, not re-shot.** `Shots = Effective?1:2`, `Inventory_Left = 10 − Shots`, `Reload_Wait ~ U(10,30)` booked per token. No token is re-inserted, no launcher blocks, no global magazine decrements.
6. **Deadline-gated effectiveness.** `Leaker = (TNow−TIME) > 4.0`; `Effective = Killed ∧ ¬Leaker`. A dice hit that arrives late is scored as a miss for inventory and leakage purposes. `Leaker` in the per-token field means late; `leakers` in the summary means `threats − effective` (all non-effective, late or dice-miss).
7. **Stochasticity is minimal and uniform.** Only Priority (discrete uniform), C2 (continuous uniform), kill dice (Bernoulli via uniform threshold), Reload (uniform) are random. Arrivals fixed, flyout fixed, track fixed. To get Poisson arrivals change `Time_Distribution` to `Exponential(Value_1)`; to get Gaussian C2 change expression to `gauss`-style (see §17).

Engineering question answered: *given rate + C2 spread + fixed flyout + Pk, what effective Pk and leaker count survive queueing + deadline?* All else is out of scope by design.

---

## 5. Parameters — Complete Reference

### 5.1 Top-level model defaults (wired)

| Name | Value | Unit | Used in | Notes |
|---|---|---|---|---|
| `Input_Rate` | 1.0 | s between arrivals | `ThreatGenerator.Value_1 = Input_Rate`, `Time_Distribution=Fixed(Value_1)` | Batch overrides `-Input_Rate 1.0`. Smaller = denser raid. |
| `Execution_Time` | 2.5 | s (logical service knob) | Top param + batch `-Execution_Time 2.5` | Present in XML + sweep; not in quoted Expression_Lists — treat as scenario/service tag, not per-token delay in this build. |
| `Pk` | 0.8 | prob | `Killed = rand(0,1) < Pk` | Sweep 0.5/0.8/0.95. Single-shot, geometry-independent. |
| `Intercept_Deadline` | 4.0 | s | `Leaker = (TNow−TIME) > Deadline` | Batch overrides 4.0. Tighten to force timeout leakers. |
| `Track_Threshold` | 3 | detections | `Track_Hits = Threshold` | M-of-N lite; inert until detection made stochastic. |
| `C2_Latency_Min` | 0.05 | s | `C2 = rand(Min,Max)` | Lower bound of uniform command delay. |
| `C2_Latency_Max` | 0.2 | s | `C2 = rand(Min,Max)` | Upper bound. Spread 0.15 s drives Flight 2.05–2.20 s. |
| `Interceptor_Speed` | 2750.0 | m/s | `Flyout = Range/Speed` | Midcourse/terminal-class assumption. |
| `Engagement_Range` | 5500.0 | m | `Flyout = Range/Speed` | Model-default standoff; yields exactly 2.0 s. NOT the CSV radar range. |
| `InterceptorInventory` | 10 | interceptors | `Inventory_Left = Inventory − Shots` | Per-token constant, not global state. |
| `Reload_Time_Min` | 10.0 | s | `Reload_Wait = rand(Min,Max)` | Booked only. |
| `Reload_Time_Max` | 30.0 | s | `Reload_Wait = rand(Min,Max)` | Booked only. |
| `Modelseed` | `seed(12345)` GUI; `seed(1001/1002/1003)` sweep | seed | All `rand/irand` streams | MUST differ per sweep point. |
| `View_Stats` | true | bool | Display verbosity |  |
| `stopTime` | 15.0 | s logical | `DEDirector.stopTime` | ~7 arrivals at 1/s plus drain. Extend for larger raids. |
| `Block_Documentation` | `Enter User Documentation Here` | text | Doc placeholder | Replace in write-up. |

### 5.2 Queue block params (verified strings)

`Block_Name="Queue" (unique per resource)`, `Queue_Number_Field=1 (fixed for all transactions here)`, `Priority_Field="Priority" (per-token)`, `Max_Queue_Length=10`, `Number_of_Queues=1`, `Initial_Queue_State=First_Token_Flow_Through` (alt `First_Token_Enqueue`), `Queue_Reject_Mechanism=Incoming_Token_Rejected` (alt `Lowest_Priority_Token_Rejected`). Rejection path matters only when occupancy hits 10 — not reached at 7 threats/15 s.

### 5.3 CSV rows (context, mostly unwired)

Threat speed 2000–7000 m/s (MDA/DOTE, Assumption); radar 300–1000 km (JHU APL X-band, Assumption); scan 1–10 Hz (multifunction, Assumption); Track_Threshold 3 (M-of-N, Assumption); C2 0.05–0.2 s + C2 min/max duplicates (MDA C2BMC + model default, Assumption); speed 2750, range 5500, Pk 0.5–0.95 + Pk 0.8 center, deadline 4.0, false-alarm 1e-6, reload 10–30 + min/max duplicates, inventory 10, C2BMC 10–100 Mbps (Estimate), Input_Rate 1.0, Execution_Time 2.5. The wired subset is §5.1; the rest documents the story envelope and must not be cited as calibrated inputs.

### 5.4 Units and scaling rule

Keep `s + m + m/s = s` consistent. Never mix ms/s. Sim time is logical: if you claim `1 ms sim = 1 s battle`, scale ALL of C2/flyout/deadline/stopTime by the same factor and state it. Current defaults are already self-consistent in seconds.

---

## 6. Maths — Exact Equations Executed

`rand(a,b)` = continuous uniform U(a,b). `irand(a,b)` = discrete uniform {a..b}. `rand(0,1) < Pk` = Bernoulli(Pk). `TNow` = now, `TIME` = birth. All per-token `input.*` fields.

### 6.1 DetectionAssignment — verbatim executed string

```
input.Priority    = irand(1,5)
input.Track_Hits  = Track_Threshold
input.Firm_Track  = (input.Track_Hits >= Track_Threshold)
input.C2_Latency  = rand(C2_Latency_Min, C2_Latency_Max)
input.Flyout_Time = Engagement_Range / Interceptor_Speed
input.Flight_Time = input.C2_Latency + input.Flyout_Time
input.Killed      = rand(0.0,1.0) < Pk
```

Hence:

```
(1) Priority ~ DU{1..5}, E=3.
(2) Track_Hits ≡ 3, Firm_Track ≡ true.
(3) C2 ~ U(0.05,0.20), E=0.125, Var=(0.15²)/12=0.001875, σ≈0.0433 s.
(4) Flyout = 5500/2750 = 2.0 s exactly (no variance).
(5) Flight = C2+2.0 ~ U(2.05,2.20), E=2.125 s. This is pre-queue flight only.
(6) P(Killed=1)=Pk, Var=Pk(1−Pk). At Pk0.8 Var 0.16; at 0.5 Var 0.25 (max); at 0.95 Var 0.0475.
```

### 6.2 Delays

```
(7) C2 hold = C2_Latency (DLY Delay_Value="C2_Latency").
(8) Flyout hold = Flyout_Time (DLY Delay_Value="Flyout_Time").
(9) Queue wait W = Time_Array[1]−Time_Array[0]; Trace {"Queue_in","Queue_out"}.
(10) End-to-end L = TNow−TIME = W + C2 + Flyout + scheduling jitter.
     Task_Latency logged is the queueing component visible to that token.
```

`Delay_Value` semantics (describe_actor Delay): hold incoming Data Structure for the value, then emit. Value may be a param reference (no quotes needed in expression, quoted string-param in MoML).

### 6.3 KillAssessment — verbatim executed string

```
input.Leaker         = (TNow - input.TIME) > Intercept_Deadline
input.Effective_Kill = input.Killed ? (input.Leaker ? false : true) : false
input.Shots_Fired    = input.Effective_Kill ? 1 : 2
input.Inventory_Left = InterceptorInventory - input.Shots_Fired
input.Reload_Wait    = rand(Reload_Time_Min, Reload_Time_Max)
Output_Values = input, TNow-input.TIME, input, input
Output_Ports  = output, Latency, KilledOnly, MissedOnly
Output_Conditions = true, true, input.Effective_Kill, !input.Effective_Kill
```

Hence:

```
(11) Leaker = 1{L > 4.0}.
(12) Effective = Killed ∧ ¬Leaker. Truth table: (0,·)→0; (1,1)→0; (1,0)→1.
(13) Shots = 1 if Effective else 2.
(14) Inventory_Left = 10−Shots ∈ {9,8}. Independent per token.
(15) Reload_Wait ~ U(10,30), E=20 s. Logged, not waited.
(16) Latency port = L; KilledOnly iff Effective; MissedOnly iff ¬Effective; output+Latency always.
```

### 6.4 Sweep scores — verbatim scorer logic

```
threats = count(ID); killed = count(Killed==true); effective = count(Effective_Kill==true);
firm = count(Firm_Track==true); leakers = threats−effective;
raw_Pk = killed/threats; effective_Pk = effective/threats (guard threats==0).
```

`effective_Pk ≤ raw_Pk` always; gap = late hits + queue-inflated L. `firm/threats ≡ 1` in this build — report it to prove gate inert.

### 6.5 Sensitivity intuition (use with sweep)

- `∂E[raw_Pk]/∂Pk = 1` (dice only). `∂E[effective]/∂Pk = P(L≤Deadline)` (<1 when queue binds).
- `∂E[Flight]/∂C2 = 1`; widening C2 spread widens L without moving Flyout.
- `∂E[Flyout]/∂Range = 1/Speed`; `∂E[Flyout]/∂Speed = −Range/Speed²`. At defaults +1000 m range → +0.36 s; +250 m/s speed → −0.17 s.
- Deadline tightening converts hits to leakers without changing dice: sweep Deadline 3/4/6 at fixed Pk to isolate timing vs lethality.
- Rate tightening (Input_Rate 1.0→0.5 s) raises W and L, converting hits to leakers even at Pk 0.95 — the saturation knee.

---

## 7. Data-Structure Lifecycle — Field-by-Field

Birth in `ThreatGenerator` as `Header_Only / Header` with `TIME=TNow, ID incrementing (note IDs in logs are non-sequential 1,2,4,5,8… because Display logs completion order, not creation order), INDEX=0, DELTA=0.0`.

Mutations in `DetectionAssignment`: Priority, Track_Hits, Firm_Track, C2_Latency, Flyout_Time, Flight_Time, Killed.

Queueing adds `Time_Array={t_in,t_out}`, `Trace_Array={"Queue_in","Queue_out"}`, `Task_Latency`.

Mutations in `KillAssessment`: Leaker, Effective_Kill, Shots_Fired, Inventory_Left, Reload_Wait.

Every field meaning in logs:

- `BLOCK=ThreatGenerator` — logging block name (all records logged at outcome, not per-hop).
- `ID` — threat token id. Gaps = out-of-order completion.
- `TIME` — birth time. `DISPLAY AT TIME` − TIME = L.
- `C2_Latency` — this token's uniform draw (0.05–0.2).
- `Flyout_Time` — always 2.0 here.
- `Flight_Time` — C2+Flyout (≈2.05–2.20), excludes queue.
- `Firm_Track / Track_Hits` — true/3 always.
- `Priority` — 1–5 discrete draw; queue order key.
- `Killed` — Bernoulli dice.
- `Leaker` — late flag (L>4).
- `Effective_Kill` — scored kill.
- `Shots_Fired` — 1/2 accounting.
- `Inventory_Left` — 9/8 per-token.
- `Reload_Wait` — 10–30 booked.
- `Task_Latency` — queue wait seen.
- `Time_Array / Trace_Array` — in/out stamps + hop names.
- `DELTA 0.0, DS_NAME Header_Only, INDEX 0` — framework housekeeping.

---

## 8. Simulations — How to Run

### 8.1 Prerequisites

1. VisualSim License Manager running and reachable.
2. `JAVA_HOME=C:\Program Files\Java\jdk-17` (batch sets this; GUI needs same JDK).
3. VisualSim Architect 2020.Q2+ (model `_createdBy 2020.Q2`).
4. Model index built after library import (wait before `compile_architecture` if cold — first call may return `INDEX_BUILDING/preparing`).
5. Absolute MCP/project paths; no `cd` in tool calls (use `workdir`).
6. Edit sweep `INSTALL_PATH` and scorer `root` to your `VS_AR\workflow` location before batch use.

### 8.2 GUI single run

1. License Manager → Architect → Open `MissileDefense_Model.xml` → GO.
2. Probes: `DefenseOutcome` table, `KillCount/MissCount` totals, `xTime_yData_Plotter` latency.
3. Outputs land in `resultpath/workflow` as `MissileDefense_Outcome.txt`, `Kill/Miss_Count.txt`. Default stopTime 15 s yields ~7 completions at rate 1/s.

### 8.3 Batch three-point Pk sweep

```bat
@echo off
set "JAVA_HOME=C:\Program Files\Java\jdk-17"
set INSTALL_PATH=C:\Users\satvi\Desktop\VisualSim\VS_AR
set CLASS_PATH=%INSTALL_PATH%;%INSTALL_PATH%\com\amity\flexlm\flexlm.jar;%INSTALL_PATH%\com\amity\flexlm\EccpressoAll.jar;%INSTALL_PATH%\com\amity\flexlm\flexlmutil.jar

"%JAVA_HOME%\bin\java" -Dvs.lic=default -Djava.security.policy=%INSTALL_PATH%\bin\policyAll -Djava.security.manager=allow --add-opens java.desktop/sun.font=ALL-UNNAMED -classpath %CLASS_PATH% VisualSim.actor.gui.VisualSimBatchModeSimulator -run 1 -resultpath "%INSTALL_PATH%\workflow" -Execution_Time 2.5 -Input_Rate 1.0 -Modelseed seed(1001) -Pk 0.5 -Intercept_Deadline 4.0 -DefenseOutcome.fileName MissileDefense_Outcome_run1.txt "%INSTALL_PATH%\workflow\MissileDefense_Model.xml"
... -run 2 ... seed(1002) -Pk 0.8  ... run2.txt ...
... -run 3 ... seed(1003) -Pk 0.95 ... run3.txt ...
python summarize_missile_outcome.py
```

Line-by-line: `@echo off` quiet; `JAVA_HOME/INSTALL_PATH/CLASS_PATH` locate JDK + install + FlexLM jars; `java … VisualSimBatchModeSimulator` headless sim; `-Dvs.lic=default` license; `-Djava.security.*` policy; `--add-opens java.desktop/sun.font` JDK17 module open; `-classpath` jars; `-run N` run index; `-resultpath` where Displays write; `-Param value` overrides top params; `-DefenseOutcome.fileName` per-run log; final arg model path. Scorer then prints one line per `run*.txt`.

### 8.4 Sweep knobs to try next (hackathon DOE)

- Raid: `-Input_Rate 1.0/0.5/0.25` (≈7/15/30+ threats/15 s) at fixed Pk0.8.
- Lethality: `-Pk 0.5/0.8/0.95` at fixed rate (already done).
- Timing: `-Intercept_Deadline 3.0/4.0/6.0`; C2 via top params; Range/Speed via `Engagement_Range/Interceptor_Speed`.
- Duration: raise `stopTime` beyond 15 s for larger N (watch heap; use `caps_json` budgets with `run_to_verdict/sweep_and_analyze`).
- Stochastic arrivals: change `Time_Distribution Fixed(Value_1)` → `Exponential(Value_1)` for Poisson; add `Poisson λ` interpretation `E[interarrival]=Value_1`.

### 8.5 MCP-governed runs (Challenge 3 evidence)

Prefer `run_to_verdict(model_path, overrides_json, objective_json, wait_seconds)` with e.g. `objective {p95_latency<8, PES>0.9@raid10}` → `get_job_facts/get_evidence/diagnose_job/evaluate_simulation_job/diagnose_performance`; `sweep_and_analyze(space_json grid/LHS)` for Pareto; `seek_target` for clock/bus/fusion knobs; `propose_model_changes → apply_model_transaction → reopen+inspect` for governed edits. Log every call as AI-workflow appendix.

---

## 9. Results — How to Read Every Output File

### 9.1 Per-threat log

Each `DISPLAY AT TIME ------ Ts ------ {…}` is one completed engagement at completion time T. `TIME` is birth, so `L = T − TIME`. `Flight_Time` (≈2.1) + `Task_Latency` (≈0–5) ≈ L (plus scheduling epsilon). `Killed` is dice; `Effective` is scored; `Leaker` is late; `Shots/Inventory/Reload` are booked consequences.

### 9.2 Counter logs

Step functions: each kill increments Kill log, each non-effective increments Miss log. Final values = `effective` and `threats−effective`. They do NOT sum to raw dice hits. Cross-check: `Kill final + Miss final = threats`.

### 9.3 Scorer line

`basename: threats=R raw_kills=K effective=E leakers=R−E firm_tracks=F raw_Pk=K/R effective_Pk=E/R`. Latest: run1 7/4/2/5/7 0.571/0.286; run2 7/6/2/5/7 0.857/0.286; run3 7/7/5/2/7 1.000/0.714. Note run1→run2 raw rises but effective flat — deadline/queue capped scoring, the key insight to present.

### 9.4 Plotter

`Latency (TNow−TIME)` vs time. Flat ≈2.1 s = uncontended. Upward drift/steps = queue building. Use p50/p95/max + track-age histogram in slides; raw trace alone is insufficient for метро judges.

---

## 10. Worked Examples With Real Numbers

All from checked-in logs (values rounded).

**A. Clean 1-shot kill — `Outcome_run3.txt` ID 1:** `C2 0.1108 + 2.0 = 2.1108 Flight, Killed true, T=2.11s (TIME 0.0) < 4 → Leaker false → Effective true, Shots 1, Inventory 9, Reload 29.57, Priority 4, Firm true.` Textbook on-time hit.

**B. Hit wasted by lateness — `MissileDefense_Outcome.txt` ID 5:** `C2 0.0999 + 2.0 = 2.0999 Flight, Killed true BUT displayed 8.49s with TIME 4.0 → L≈4.49 > 4 → Leaker true → Effective false, Shots 2, Inventory 8.` Dice hit, system miss. Present this to explain raw vs effective gap.

**C. Double-booked miss — `Outcome_run1.txt` ID 1:** `C2 0.1617 + 2.0 = 2.1617, Killed false → Effective false (Leaker false, on time but dice miss), Shots 2, Inventory 8, Reload 29.41.` On-time dice miss still costs 2 shots.

**D. Queue-shifted ID order — default file IDs 1,3,4,5,9,8,13 by completion:** birth `TIME 0,2,3,4,8,7,12` completes `2.18,4.33,6.39,8.49,10.60,12.66,14.78`. ID 8 born at 7 finishes after ID 9 born at 8 — priority/queue reordering visible. Use `Time_Array/Task_Latency` to show who waited.

**E. Counter cross-check — default:** kills at 4.33/10.60/14.78 → Kill 1/2/3; misses at 2.18/6.39/8.49/12.66 → Miss 1/2/3/4; 3+4=7 threats; scorer would print raw/effective accordingly.

---

## 11. Queueing, Timing and Bottleneck Behaviour

- Offered load `λ ≈ 1/Input_Rate = 1/s`; service per threat ≈ C2+Flyout ≈2.125 s + scheduling. Single-server utilisation `ρ = λ·E[S] > 1` would explode, but `InterceptorQueue` + downstream DLYs pipeline stages, so observed behaviour at 7/15 s is mild queueing (`Task_Latency 0–5.6 s` in logs) not collapse. Halve `Input_Rate` → W and L rise, deadline binds, effective_Pk falls even at high Pk — the saturation knee to sweep for.
- `Max_Queue_Length 10` never binds at default N; raise raid to 50–100 or shorten `Input_Rate` to hit `Incoming_Token_Rejected` and count drops as free-riders analogue.
- `First_Token_Flow_Through` lets the first token pass without queue delay (clean baseline); `First_Token_Enqueue` would force even it to queue (harsher). `Incoming_Token_Rejected` drops overflow; `Lowest_Priority_Token_Rejected` would drop low-priority queued instead — closer to threat-evaluation doctrine if you enable it.
- `Const → pop_input` paces dequeuing; without it queue would either flood or starve downstream. Keep it when cloning queues for multi-ship.
- Deadline 4.0 s vs Flight ≈2.1 s leaves ≈1.9 s slack for queue wait. Any token waiting >1.9 s becomes a leaker even if dice-hit. This is why run2 (Pk0.8) can match run1 effective despite higher raw — extra hits arrived too late.
- Little intuition `Lq ≈ Wq`: at defaults `Task_Latency` 0–3 s typical; plot `Task_Latency` vs `L` to separate queue vs C2/flyout contributions in the bottleneck slide.

---

## 12. VisualSim Block Semantics Used

- `DS_Source (Traffic)` — transaction generator. Params `Data_Structure_Name, Number_of_Transactions, Random_Seed, Start_Time, Time_Distribution ∈ {Fixed/Uniform/Exponential/Normal…}, Value1(/Value2)`. Here Fixed + Value_1=Input_Rate. `describe_actor` notes 10 params total, 1 port `output`.
- `Expression_Decision (ExpressionList)` — multi-expression router. Params `Expression_List, Output_Values, Output_Ports, Output_Conditions` (+ input/output ports; Kill adds `Latency/KilledOnly/MissedOnly`). Executes expressions in order, then routes copies per true conditions. Quote exact strings from §6 — they ARE the model logic.
- `DLY (Delay)` — hold by `Delay_Value` (param reference allowed). 1 param, 2 ports. Used twice with different per-token values — same class, different binding.
- `Smart_Resource (Queues)` — priority queue with arbitration. Params above; 1+ ports `input/output/pop_input`. `describe_actor` ambiguous between `VisualSim.actor.lib.Smart_Resource` (103 models, Queues) and bare `Smart_Resource` — use the former.
- `Counter_Basic` — event counter. Params `Initial/Final/Equals_Count, Input_Port_Mode, Output_Port_Mode=Normal_Counter_Update`. Increments on `incr_add_input`.
- `Display` — text probe + file sink. Params `ViewText, saveText, fileName, title (+ Font_Type warning benign)`. `fileName` is overridden per sweep via `-DefenseOutcome.fileName`.
- `TimedPlotter` — x=time y=data scope. Params `legend, viewPlot, plotSize, _windowProperties`.
- `Const` — constant trigger source for pop/schedule. Params `_location, _flipPortsHorizontal`.
- `DEDirector` — discrete-event engine. Params `digitalDomainOnly, digitalDebugger, stopTime, timeResolution`.

---

## 13. Validation State (MCP-Verified)

`inspect_model_artifact` on `models/MissileDefense_Model.xml` (copy of share XML):

- `container_count 14`, `source_sha256 dd50dbce2749…`, `original_unchanged true`, `dependency_closure copied 1`.
- `validation ok:false` SOLELY for `UNKNOWN_PARAMETER Font_Type on /DefenseOutcome` (Display cosmetic, safe to ignore or remove) plus 4 `UNBOUND_FILE_PARAMETER` warnings (`$VS/…/SimpleEvent54x36.png`, `Outcome/Kill/Miss .txt` not staged pre-run). No missing director, no unconnected mandatory port, no vacuous-activity errors. Semantic `ok:false` mirrors same single error.
- Registry `classes 1785, source_roots [share, share/models, Queues_FIFO demo, User_Library, demo], construction_registry true`.
- Next-step pointers returned: `inspect containers offset 5`, `describe_actor` candidates, `get_doc ExpressionList/Traffic/Delay`, `describe_pattern accelerator_node`. All consistent with a healthy small DE model.

---

## 14. Assumptions, Limitations, Pitfalls

1. Every CSV number is Assumption/Estimate — no Pd/Pfa/SNR/RCS/accuracy/latency/flyout/Pk is measured from cited papers. Synthesis §6: corpus gives architecture/failure modes, not calibrations.
2. Scale mismatch: model range 5.5 km vs CSV radar 300–1000 km; C2 0.05–0.2 s vs paper coord 4.375/12.25 s; slots 1.5/0.875 s not modelled; deadline 4 s vs endo window + assessment loop.
3. No sensor physics: duct 4/14/24 m, propagation/clutter, Swerling-IV aspect means, METOC-conditional accuracy, S/X trade, discrimination cap 5, POT Baseline 6 Ph3, 3σ ellipse, hexagon engageability — all absent.
4. No force coordination: 0/9/7/4 engageability, grouping 1000 m, freezing, ordering, 8-test sieving, FES/DB, Link-16 2 msgs/slot, J-messages — absent. Single queue only.
5. No picture errors: ideal `Firm≡true`, no multi-track (paper 1.3 remotes/object, 88–96% overengagements multi-track), no miscorrelation, no undetected (paper 84.1% in-time, 708 undetected), no launch-before-detect impossibility.
6. No global magazine: per-token `10−Shots`, no depletion, no reload blocking, no dual-salvo scheduling (paper: 2nd unscheduled until 1st in flight).
7. No interceptor diversity: single speed/range/Pk vs GMD/Aegis/THAAD/Patriot + GPI/NGI + salvo/shoot-look-shoot depth.
8. No threat diversity: fixed-rate single type vs ballistic/hypersonic-glide/cruise + decoys/clutter + maneuver + EA/jamming + mixed AAW/OCMD contention.
9. No network/power/cost: NoC/AXI/SpaceWire widths, buffers, jam loss, `PowerTable/Battery/Power_Manager`, block-count/area proxies — unwired.
10. No statistics discipline: N≈7/run vs paper 100–400 runs + 95% CI; seeds fixed; no RNG-order statement; `View_Stats` only.
11. Time is logical; ms/s mix will silently bias results — keep seconds everywhere.
12. Tooling: license server, JDK17, absolute MCP paths, index-build wait, `resultpath` must exist, scorer `root` must be edited, `Font_Type` warning benign.
13. `Execution_Time` top param is scenario tag in this build, not a per-token hold — do not cite it as modelled service time without wiring it.
14. IDs log out-of-order — do not sort by ID for latency analysis; sort by `TIME` or `DISPLAY AT TIME`.
15. `Architecture_Model` FPGA chain must not be cited as missile performance evidence.

---

## 15. Research Traceability vs Papers

Corpus `research.txt` → `research/report.md + synthesis.md + notes/P1-P4.md + open-questions.md`. IDs: P1 O’Haver 2018 radar, P2 Krill 2001 SE, P3 Moskowitz 2002 coordination, P4 Brown 2005 optimisation (abstract-only, paywalled DOI 10.1287/opre.1050.0231).

- **P1 (14 pp, 59k chars):** switched-beam→phaser→computer-multifunction→environment-coupled→AESA/DBF, S+X suite, cost deletions SPY-4/CG(X); TEMPER/FirmTrack, 10 GHz/15 m ducts 4/14/24 m, clutter=propagation×RCS, 20-case METOC reconstruction units-withheld, >2× firm-track variability. Share reuses scheduler+dwell+Monte-Carlo idea only.
- **P2 (14 pp, 50k):** V-cycle + DRM + AoA + ADAM/ARTEMIS + WASP/GSEL + virtual-follow-on + COTS; Aegis-to-Aegis off-board→WCS→SPY-1 uplink, CEC forward-pass n=1 Mountain Top, OCMD Korea virtual. No numbers. Share reuses timing-budget narrative only.
- **P3 (14 pp, 60k, ACES 0.9):** 20 TBM (15 Scud-C +5 No Dong)/5 areas/4 ships, 29 assets, SM-2 IVA dual-salvo 1/threat, SPY-1B(V)/D Baseline 6 Ph3, 1-s assess/engage/schedule, max 5 discriminations, priority preferred→threat→earliest-latest-launch; sectored (static, no comms) vs free-fire (none) vs first-launch (launch-msg, light) vs DED bidded (heavy, FES+DB+8 tests, Table 1 coord 4.375/12.25 soft3 hard5 tol3 group1000m, slots 1.5/0.875 2/slot, J3.6/J3.0/J10.2, Swerling-IV aspect, Guaranteed Useful Search planned-pairs, POT, hexagon, CEC-proxy biases 8.7 mrad/150 m, kill tests geometry-independent RV-in-track-dependent); ideal DED≈perfect vs sectored-worst (mass 6 free riders), achievable free≈ideal/sectored≈ideal-zero-overengagement vs dynamics-worse 96%/88% multi-track, 84.1±0.5% in-time 708 undetected, 28 remotes (1.3/obj), launches-before-detect unguaranteeable, leakers>free riders, 1/400 leak-free (DED), quality>latency interpretation. Share reuses vocabulary only.
- **P4 (RePEc abstract only):** JOINT DEFENDER bilevel MILP pre-positioning + secrecy, minutes transparent/seconds secret on laptop, N.Korea scenarios. Unverified beyond abstract. Share reuses word inventory only.
- **Qwen extras not in research.txt:** Wilkening Pk/leaker equations, DOTE FY25 Pk, Simpkins validation, VisualSim notes — cite separately if used; do not attribute to P1–P4.
- **Strength map:** well-supported = scheduler+T/R-sync+confirmation+Monte-Carlo abstraction; duct/multipath/clutter must be modelled; saturation converts overengagement→free riders; multi-track dominates failure; force assignment beats static partition under uneven raids. Single-sim only = all P3 distributions, P1 Fig.7, P2 ADAM, P4 claims. Unsupported = any Pk/Pd/Pfa/SNR/accuracy/latency for VisualSim calibration.

---

## 16. DED Complexity Comparison

| Dimension | This model (6 functional blocks) | DED bidded dynamic [P3 pp.3–6] |
|---|---|---|
| Decision | Local random priority; always engages if queued | Force-wide common algorithm → identical decisions on shared info; FES per unit (threat+unit+weapon+shot, max 2/unit-threat); temp DB group→threat→shot; group 1000 m, 1 group/threat, frozen at coord time, ordered frozen/size/unique/priority/number |
| Sieving | None (dice + deadline) | 8 tests: (1)notify time (2)hard cap 5 (3)inventory (4)load soft 3 restore-if-emptied (5)reengagement window (6)inventory balance tol 3 (7)TOF sum (8)unit# |
| Period / priority | Event-driven on arrival | 1-s threat-assess/engageability/schedule/force-select; priority preferred-shooter → threat → earliest latest-launch |
| Comms | Single DLY 0.05–0.2 s | Link-16-like 20 C2+36 fighters, surv ≥1/1.5 s, eng 1/0.875 s (14 slots/shooter), 2 msgs/slot, J3.6+J3.0+J10.2I/C2; DED heavy vs first-launch light (launch msg) vs sectored none |
| Sensing | Firm≡true, no RCS/search/correlation | RP&A constant-mean Swerling-IV planning vs ACES aspect-averaged VV means; Guaranteed Useful Search planned-pairs; counting unstated; ground-truth clustering; POT Baseline 6 Ph3; 3σ ellipse→top asset; hexagon projection; SNR→accuracy + constant+residual biases (CEC proxy, Link-16 numbers unavailable); 8.7 mrad/150 m; max 5 discriminations |
| Weapons | 1 type, 2.0 s, Bernoulli Pk, 1-vs-2 booked | SM-2 IVA dual-salvo, 2nd unscheduled until 1st in flight, 1 salvo/threat, kill tests launcher/prelaunch/inflight/uplink/handover/lethality geometry-independent RV-in-track-dependent, reliability reengagements conflated in overengagement count |
| Scenario | 7 threats, 1 defender, 15 s, 100% engageable, 0 reengagement by construction | Day D+5 NE Asia Capstone/COEA, DICE 6-DOF truth, 20/5/4, 0×4/9×3/7×2/4×1 engageable, Table 2 impacts, Table 3 sectored load 4/7/9/0, 10-s impact spread, 100 runs/scheme (400 achievable), seeds/RNG unstated |
| Metrics | raw/effective Pk, leakers, latency, counts | Free riders / overengagements / leakers distributions (Figs 4/5 ideal, 7–13 achievable), detection margins, remote counts; ideal DED≈perfect ≥40 s early detect; achievable 1/400 leak-free |
| Failure physics | Late or dice-miss only | 88–96% dynamic overengagements from multi-tracks, miscorrelations, undetected planned, launches-before-detect, missile-failure re-decisions |
| Optimisation | None | P4 bilevel MILP pre-positioning + secrecy (outside P3 sim) |

Net per authors (single vignette): ideal DED≫first-launch>free-fire>sectored on free riders; achievable dynamics still better than static but gap narrows on picture errors; latency/launch-time < picture-quality (interpretation, no isolating sweep).

---

## 17. Hackathon Use and Extension Cookbook

### 17.1 Challenge mapping (per planner.md + docx)

- **Challenge 1 (primary):** fresh kill-chain with latency/throughput/reliability/power/cost trade — this model is the baseline. Required: meaningful question + metrics (latency p50/p95/max, throughput, utilisation, PES/leakage, waste, power proxy, cost proxy) + experiments + innovation.
- **Challenge 3 (free points with MCP):** log `search_models/describe_actor/find_blocks_by_role/list_patterns/describe_pattern/compile_architecture/run_to_verdict/get_job_facts/get_evidence/diagnose_job/evaluate_simulation_job/diagnose_performance/sweep_and_analyze/seek_target/propose/apply/inspect` as AI-workflow appendix with prompts + corrections.
- **Challenge 2 fallback:** re-engineered from `Full_System_ComJam_Model (283 blocks RF/jam)` + `Animation_Target_Processing (48 blocks space/power/scheduler)` — cite if pivoting.

### 17.2 Minimum viable experiments (1–2 days)

1. Baseline sanity raid=1 ballistic no jam → L≈2.1 s, PES≈Pk.
2. Raid sweep 1/10/50/100 + decoys 0/2/5 → knee where W explodes (expect fusion/queue first; cite free-rider conversion).
3. Coordination lite: centralised vs unbidded-broadcast (measure waste vs leakage).
4. Network/jam 0/5/20% + bus 8→64 B → track age vs PES.
5. Power: add Power_Manager+Battery → max track duty cycle.
6. Pareto `sweep_and_analyze fusion_batch×dwell×salvo → PES vs latency vs used`.
7. `seek_target` e.g. radar_clock for p95=5 s in [200,1800] MHz.

### 17.3 DED-lite design (recommended innovation, hours not weeks)

Keep pipeline; duplicate `InterceptorQueue` → Ship1/Ship2; add `Database[FES]` + `Virtual_Machine[common rule]`:

```
# pseudo Expression_List for DED-lite (adapt to VisualSim Expression syntax):
# canReach = (rangeToThreat < maxRange_ship)
# hasInv   = (globalInv_ship > 0)
# load     = queueLen_ship
# prefer   = canReach && hasInv ? (load_min ? true : TOF_min) : false
# Tests kept: capability, inventory, load-balance + TOF tie-break (3 of 8).
# Policies: A sectored (asset partition, no DB read), B first-launch (read launch flag, defer), C DED-lite (read FES, common rule, defer if not preferred).
```

Wire via `propose_model_changes([add_entity Database/Virtual_Machine, set_parameter, connect relation…])` → `apply_model_transaction` → reopen+inspect. Compare A/B/C on over-engagement waste vs leakers at same raid — replicates P3 insight without ACES weight. If it breaks, still submit baseline.

### 17.4 Wiring more realism later

- Poisson raids: `Time_Distribution Exponential(Value_1)`; burst: Uniform/Normal options already in XML choices.
- True M-of-N: replace `Track_Hits=Threshold` with `hits += Bernoulli(Pd) per dwell + false-alarm` counter + `Firm = hits>=3 in last M`.
- Global magazine: `Inventory` as shared `Database`/state decremented on `Shots`, reload `DLY` blocking launch when 0.
- Threat classes: duplicate generator with different `C2/Flyout/Pk` (ballistic predictable, hypersonic high-compute low-Pk, cruise late-detect) + `decoys_per_RV`.
- Fusion/C2 load: `AI_Processor + Memory_Controller/HBM/DRAM + NoC_Router/AMBA_AXI + Scheduler_SW/Smart_Controller + PowerTable/Battery` from planner §5.1; tag params `published/derived/assumption` with `range` for `compile_architecture`.
- Discrimination: `AI_Processor` delay+accuracy knob before C2.
- Jamming: ComJam loss pct on C2/fusion links → track age → waste.

### 17.5 Submission pack

Executable model + top params + README run steps; 8–10 slides (problem → arch diagram §3 → VisualSim use → raid chart + Pareto → innovation DED-lite → results); 2–3 p write-up (problem, Golden Dome/Guam/DOT&E why, federated-M&S approach per DSB, innovation AI kill-chain, assumptions/time-scaling/no-6DOF, results, refs grouped [M&S][Fusion][Guidance][Ref]); 5-min video (model + run + plots + fix). Keep prompts log + fact-sheet PIDs.

---

## 18. Glossary

- **Pk** single-shot kill prob (dice). **raw_Pk** dice hits/threats. **effective_Pk** on-time hits/threats. **PES** prob. engagement success (mission-level).
- **Leaker (token)** late flag L>Deadline. **leakers (summary)** threats−effective (all non-scored).
- **Free-rider** unengaged because capacity wasted elsewhere (paper). **Overengagement** >1 shooter per threat (paper; conflates reliability re-shots in achievable DED).
- **Firm_Track** M-of-N confirmed track. **M-of-N** N hits in M dwells.
- **FES** Force Engagement Schedule (paper). **DED** Distributed Engagement Decision bidded (paper). **POT** Predicted intercept / ownership? point (Baseline 6 Ph3 context). **RP&A** Radar Performance & Analysis planning factors. **DICE** 6-DOF truth sim. **ACES** Aegis Coordination Evaluation Sim 0.9. **CEC** Cooperative Engagement Capability (AAW-era proxy). **C2BMC** command/control/battle management. **SKA** space kill assessment analogue.
- **DLY** Delay hold. **DS_Source/Traffic** generator. **Smart_Resource/Queues** priority queue. **ExpressionList/Decision** expression router. **Counter_Basic** event counter. **Display** probe/file. **TimedPlotter** scope. **Const** trigger. **DEDirector** DE engine. **Database/Virtual_Machine/Scheduler_SW/Smart_Controller/AI_Processor/NoC_Router/AMBA_AXI/DRAM/HBM/PowerTable** extension blocks.

---

## 19. Cheat Sheet

```bat
:: GUI
:: License Manager → Architect → Open MissileDefense_Model.xml → GO → DefenseOutcome + Kill/MissCount + plot
:: Batch (edit JAVA_HOME + INSTALL_PATH + scorer root first)
MissileDefense_Model_Sweep.bat
python summarize_missile_outcome.py
:: Outputs: Outcome_run*.txt (per-threat) + Kill/Miss_Count.txt (steps)
:: Next sweeps: -Input_Rate 1.0/0.5/0.25 -Pk 0.5/0.8/0.95 -Intercept_Deadline 3/4/6 -stopTime 15/60
:: MCP: plan_task → describe_actor → compile_architecture → run_to_verdict → get_job_facts/get_evidence → diagnose_job/evaluate → diagnose_performance → sweep_and_analyze/seek_target → propose/apply/inspect
:: cross-check: Kill_final + Miss_final == threats; effective ≤ raw; firm == threats (gate inert)
```

---

## 20. Version and Provenance

- Model `_createdBy 2020.Q2`; share `MissileDefense_Share` with `Model_Report` sweep run1–3 + `Qwen_Research` pack; research audit `VisualSim_Hackathon_2026_project/research/{report,synthesis,open-questions,notes/P1-P4,P*.pdf/.txt}`; planner `planner.md (2026-10-03, Challenge 1+3 combo)`; challenges docx `VisualSim_Global_Electronics_Hackathon_Challenges.docx`.
- Ground-truth strings for this doc: `Expression_List` ×2, `Delay_Value` ×2, `Output_Values/Ports/Conditions`, `Data_Structure_Name/Time_Distribution/Value_1`, queue six params, top 13 params + `stopTime 15.0`, sweep three java lines, scorer 25 lines, outcome/counter sample blocks, CSV 21 rows, MCP open/inspect/describe/search outputs quoted in §§3/12/13.
- No distribution/CUI/FOUO markings found in accessed research extractions. No measured system parameters introduced. All “typical” numbers are explicitly Assumption/Estimate and must be presented as such to judges.

*End — use §§3–6 as build spec, §§8–10 as test oracle, §§14–16 as honesty appendix, §17 as next-sprint plan.*

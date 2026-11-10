# MissileDefenseSystem

A **VisualSim discrete-event missile defense simulation** (DED-lite) with batch-run scripts, a portable Python experiment runner, and result summarizers. The model simulates threat generation, tracking, command-and-control (C2) latency, interceptor assignment across two ships, engagement outcomes, and magazine/inventory effects.

This repository is the standalone project (root-level model, scripts, parameter tables, and example outputs).

## Contents

| File | Purpose |
|---|---|
| `MissileDefense_Model.xml` | VisualSim/MoML model (Digital/DE simulator). Top-level parameters include `Input_Rate`, `Execution_Time`, `Pk`, `Intercept_Deadline`, `Track_Threshold`, `C2_Latency_Min/Max`, `Policy_Mode`, ship inventories/ranges, etc. |
| `missile_defense_parameters.csv` | Parameter table (value/range, units, source, confidence/assumption) for threat, radar, C2, interceptor, inventory, and sweep settings. |
| `fes_table.csv` | Fire/engagement support table used by the model (e.g. `Priority,shipHint`). |
| `magazine.csv` | Magazine/inventory state table used by the model (e.g. `Ship,Remaining,ReloadUntil`). |
| `run_full_policy_experiment.py` | Portable, terminal-first experiment runner for Policy × Pk × seed sweeps (default 90 runs: policies 0/1/2 × Pk 0.5/0.8/0.95 × seeds 2001–2010). Resolves VisualSim/JDK paths, runs batch simulations, parses outcomes, and prints per-run + aggregate summaries. |
| `MissileDefense_Model_Sweep.bat` | Windows batch example: 3 runs varying `Pk` and seed, writing `MissileDefense_Outcome_run*.txt`. |
| `MissileDefense_Policy_Pk_Sweep.bat` | Windows batch example: 9 runs over `Policy_Mode` {0,1,2} × `Pk` {0.5,0.8,0.95}, writing `MissileDefense_Outcome_p{policy}_pk{tag}.txt`. |
| `MissileDefense_Force_Ship2.bat` | Windows batch example forcing engagement to Ship 2 (`Policy_Mode 2`, `Ship1_Inv 0`, `Ship2_Inv 10`). |
| `summarize_missile_outcome.py` | Summarizes `MissileDefense_Outcome_run*.txt` (threats, raw/effective kills/leakers, firm tracks, Pk). |
| `summarize_missile_policy_pk.py` | Summarizes `MissileDefense_Outcome_p*_pk*.txt` per policy/Pk tag (includes ship assignment counts). |
| `summarize_full_policy_experiment.py` | Aggregates `MissileDefense_Outcome_*.txt` from full experiments (groups by policy/Pk, dedupes by threat ID using last record, reports re-engagements/shots/ship split, raw vs effective Pk). |
| `MissileDefense_Outcome.txt` | Example outcome log (per-threat `DISPLAY AT TIME` records). |
| `MissileDefense_Kill_Count.txt` | Example kill-count display/log. |
| `MissileDefense_Miss_Count.txt` | Example miss/leaker-count display/log. |

## Model Architecture & Pipeline

The VisualSim block diagram (`MissileDefense_Model.xml`) models a two-ship distributed missile defense system:

```
[ThreatGenerator] ➔ [DetectionAssignment] ➔ [CommonRule] ➔ [PolicyRouter]
                                                               ├──➔ [Ship1_Queue] ➔ [Ship1_C2] ➔ [Ship1_Flyout] ➔ [Ship1_Kill] ──┐
                                                               └──➔ [Ship2_Queue] ➔ [Ship2_C2] ➔ [Ship2_Flyout] ➔ [Ship2_Kill] ──┴──➔ [Merge] ➔ [KillCounter] ➔ [KillCount]
                                                                                                                                              ├──➔ [MissCounter] ➔ [MissCount]
                                                                                                                                              ├──➔ [DefenseOutcome]
                                                                                                                                              └──➔ [xTime_yData_Plotter]
[FES_DB]   [Magazine_DB]
```

### Block Responsibilities
- **`ThreatGenerator`**: Generates incoming threat missile data streams according to `Input_Rate` and `Modelseed`.
- **`DetectionAssignment` & `CommonRule`**: Performs radar detection tracking (requires `Track_Threshold` hits for `Firm_Track`) and initial rule-based prioritization utilizing `FES_DB` (Fire/Engagement Support database).
- **`PolicyRouter`**: Evaluates `Policy_Mode` (sectored / first-launch / bidded-lite) alongside `Magazine_DB` inventory levels (`Ship1_Inv`, `Ship2_Inv`) to route the engagement command to Ship 1 or Ship 2.
- **Ship Processing Lines (`Ship1_*` / `Ship2_*`)**:
  - **Queue (`Ship1_Queue`, `Ship2_Queue`)**: Buffers incoming engagement requests.
  - **C2 Delay (`Ship1_C2`, `Ship2_C2`)**: Simulates Command & Control processing latency bounded between `C2_Latency_Min` and `C2_Latency_Max`.
  - **Flyout (`Ship1_Flyout`, `Ship2_Flyout`)**: Simulates interceptor flight time based on `Interceptor_Speed` and engagement ranges (`Engagement_Range`, `Ship2_Range`).
  - **Kill Block (`Ship1_Kill`, `Ship2_Kill`)**: Determines engagement outcome based on single-shot probability of kill (`Pk`), deadline constraints (`Intercept_Deadline`), and magazine reload status (`Reload_Time_Min/Max`).
- **Data & Visualization Outputs**:
  - **`Merge`**: Merges engagement records from both ship lines.
  - **`KillCounter` / `MissCounter`**: Tracks cumulative intercepts (`KillCount`) and leakers (`MissCount`) over simulation time.
  - **`DefenseOutcome`**: Displays detailed per-threat data structures.
  - **`xTime_yData_Plotter`**: Plots real-time simulation metrics.

---

## Detailed Field Definitions in Outcome Logs

Each record printed to the `DefenseOutcome` display log includes:

| Field | Description |
|---|---|
| `ID` | Unique numeric identifier for the threat missile. |
| `BLOCK` | Source block generating the record (`ThreatGenerator`). |
| `Priority` | Threat priority level looked up from `fes_table.csv`. |
| `Firm_Track` | `true` if radar detection hits meet `Track_Threshold` (default 3). |
| `C2_Latency` | Random delay introduced by C2 network/processing (sec). |
| `Flyout_Time` | Interceptor transit time to intercept point (sec). |
| `Flight_Time` | Total time elapsed from detection to intercept (`C2_Latency + Flyout_Time`). |
| `Attempts` / `Shots_Fired` | Number of interceptors launched against this threat. |
| `Killed` | Raw intercept success based on stochastic `Pk` check. |
| `Effective_Kill` | `true` if the threat was killed within `Intercept_Deadline`. |
| `Leaker` | `true` if threat survived or missed the intercept deadline. |
| `Inventory_Left` | Remaining interceptor inventory on the firing ship. |
| `Magazine_Empty` | `true` when firing ship inventory reaches 0. |
| `Reload_Wait` | Time required until launcher reload completes (sec). |
| `TIME` / `Task_Latency` | Scenario time and queuing/task delays. |

---

## Model overview

- **Simulator:** VisualSim Digital/DE (`VisualSim.simulators.de.kernel.DEDirector`, `digitalDomainOnly=true`), model `MissileDefense_Model` (MoML/XML).
- **Inputs/parameters (examples):** threat arrival rate, execution/stop time, interceptor probability of kill (`Pk`), intercept deadline, track confirmation threshold, C2 latency bounds, engagement policy mode, per-ship inventory/range settings.
- **Threat processing:** threats are generated and flow through tracking/C2/engagement logic. Each completed engagement is logged as a structured record with fields such as `ID`, `Priority`, `Track_Hits`, `Firm_Track`, `C2_Latency`, `Flyout_Time`/`Flight_Time`, `Shots_Fired`, `Attempts`, `Killed`, `Effective_Kill`, `Leaker`, `Magazine_Empty`, `Inventory_Left`, `ship`/`preferredShip`/`sectoredShip`/`shipHint`, reload/wait info, etc.
- **Two-ship defense:** outcomes include ship assignment (`ship`, `ship1/ship2` counts in summaries) and inventory/magazine effects; policies can influence allocation.
- **Policy modes:** batch/runner use `Policy_Mode` values (e.g. `0,1,2` in sweeps) to compare engagement/allocation policies (see `missile_defense_parameters.csv`: "DED-lite policy mode (sectored/first-launch/bidded-lite)").
- **Metrics:**
  - **Raw kills / raw Pk:** `Killed` outcomes.
  - **Effective kills / effective Pk:** `Effective_Kill` (accounts for timeliness/leaker criteria as modeled).
  - **Leakers:** threats not effectively killed (e.g. `Leaker=true` / `threats - effective`).
  - **Other:** firm tracks, shots fired, re-engagements (same ID seen multiple times), per-ship load.

## Requirements

### To run simulations (VisualSim batch mode)
- **VisualSim** installation (`VS_AR`) with `VisualSim.actor.gui.VisualSimBatchModeSimulator` and required jars (e.g. `com/amity/flexlm/*`) and `bin/policyAll`.
- **Java JDK** (examples use JDK 17). Batch mode is invoked as:
  `java -Dvs.lic=default -Djava.security.policy=<VS_AR>\bin\policyAll -Djava.security.manager=allow --add-opens java.desktop/sun.font=ALL-UNNAMED -classpath <VS_AR;...jars...> VisualSim.actor.gui.VisualSimBatchModeSimulator ... <model.xml>`
- A valid **VisualSim license** for batch execution.
- Model/table files (`MissileDefense_Model.xml`, `fes_table.csv`, `magazine.csv`) available to the run (typically in the working/script directory).

### To run summarizers / portable experiment driver
- **Python 3.x** (standard library only; no third-party packages required).

## Running experiments

### 1) Portable Python runner (recommended)
`run_full_policy_experiment.py` is terminal-first and resolves paths portably:

- **VisualSim path:** `--vs-ar PATH` > `VS_AR` env var > `<script-dir>/VS_AR`
- **Java:** `--java PATH` > `JAVA_HOME/bin/java(.exe)`
- **Output dir:** `--outdir DIR` (default: script folder). Outcome `.txt` logs are written there; per-run results and a final aggregate are printed to the terminal.

Examples:
```bash
# Show plan/paths without running (no VisualSim/license needed)
python run_full_policy_experiment.py --dry-run

# Full default sweep: policies 0,1,2 × Pk 0.5,0.8,0.95 × seeds 2001-2010 (90 runs)
python run_full_policy_experiment.py --vs-ar /path/to/VS_AR --java /path/to/java

# Custom subset
python run_full_policy_experiment.py --policies 0,2 --pks 0.8 --seeds 2001,2002 --outdir ./results
```

Outputs per run: `MissileDefense_Outcome_p{mode}_pk{pk-tag}_s{seed}.txt` with a parsed terminal line like:
`policy=... pk=... seed=...: threats=... raw=... effective=... leakers=... raw_Pk=... effective_Pk=... ship1=... ship2=... shots=... reengaged=...`

### 2) Windows batch scripts
The `.bat` files are example batch invocations (they contain **hardcoded local paths** for `JAVA_HOME` and `INSTALL_PATH`/`VS_AR` on the original machine). Edit those variables to match your environment before use:

- `MissileDefense_Model_Sweep.bat` — 3 runs (`run1..3`) varying `Pk`/seed → `MissileDefense_Outcome_run*.txt`
- `MissileDefense_Policy_Pk_Sweep.bat` — 9 runs over policy/Pk → `MissileDefense_Outcome_p*_pk*.txt`
- `MissileDefense_Force_Ship2.bat` — forces Ship 2 engagement scenario → `MissileDefense_Outcome_force_ship2.txt`

## Summarizing results

Run from the directory containing the outcome `.txt` files:

```bash
# Summarize run1/run2/run3-style outputs
python summarize_missile_outcome.py

# Summarize policy×Pk outputs (p*_pk*.txt)
python summarize_missile_policy_pk.py

# Aggregate a full experiment (all MissileDefense_Outcome_*.txt except base Outcome.txt)
python summarize_full_policy_experiment.py
```

Notes:
- `summarize_full_policy_experiment.py` dedupes by threat `ID` (last record wins, matching the runner) and reports `reengaged` (IDs seen more than once) and total `shots`.
- `summarize_missile_outcome.py` / `summarize_missile_policy_pk.py` aggregate records as present in each file (useful for single-run/quick comparisons).

## Outcome log format

Each engagement completion is emitted as a block similar to:
```
DISPLAY AT TIME     ------ <t> sec ------
{ID = ..., Priority = ..., Firm_Track = true/false, Killed = true/false,
 Effective_Kill = true/false, Leaker = true/false, ship = 1|2,
 Shots_Fired = ..., Inventory_Left = ..., C2_Latency = ..., ...}
```
`MissileDefense_Kill_Count.txt` / `MissileDefense_Miss_Count.txt` capture count events over time in the same display-log style.

## Example artifacts included

- `MissileDefense_Outcome.txt`, `MissileDefense_Kill_Count.txt`, `MissileDefense_Miss_Count.txt` — sample logs from a run (illustrative of format and metrics such as effective kills, leakers, ship assignment, and inventory depletion).

## Parameters (reference)

See `missile_defense_parameters.csv` for the working parameter set (values/ranges, units, sources, confidence). Key modeled knobs include `Input_Rate`, `Execution_Time`, `Pk`, `Intercept_Deadline`, `Track_Threshold`, `C2_Latency_Min/Max`, `Policy_Mode`, `Ship*_Inv`/`Ship2_Range`, reload timings, and inventory. `fes_table.csv` and `magazine.csv` provide tabular inputs consumed by the model.

## Notes

- Batch `.bat` scripts assume a Windows environment and local VisualSim/JDK installs; prefer `run_full_policy_experiment.py` for portable, path-configurable runs and terminal-readable results.
- Actual simulation requires a licensed VisualSim installation; Python scripts can parse/summarize existing outcome logs without VisualSim.

# Systems Engineering of Air and Missile Defenses (Krill, 2001, JHU APL Technical Digest 22(3), pp.220-233)
- File: `VisualSim_Hackathon_2026_project/research/P2_Krill2001.pdf` + `.txt` (14 file-pages). Markings: none. Author: Jerry A. Krill, APL since 1973, CEC lead 1987-96. Overview/lessons-learned, not an experiment.

## Problem & motivation
- Networked air/missile defense "among the most complex systems" in components, functional intricacy, tech blend, performance stringency [P2, p.2].
- Specialist stove-piping (control/aero/comms/software/RF each with own resource priority); need balanced allocation containing cost/risk [P2, p.2, Fig.2].
- Bridge scientific method to systems method; partnership model chief/systems/lead + program managers [P2, pp.1-3].
- Methodical V-cycle + M&S + risk-reduction experiments from conception through Fleet intro/upgrades [P2, p.4, Fig.4].

## Threat/mission context
- General evolving threat + complex tactical environment; Mission Need vs evolving threat; Design Reference Mission (DRM): threat + geopolitical + natural environments; NTW DRM by JWAD+ADSD; family -> "Master DRM" [P2, pp.1, 5-6].
- Missions: NTW TBMD vs longer-range theater TBMs with inland protection; Area TBMD (SM-2 Blk IVA), Theater (SM-3); OCMD vs cruise missiles far inland (e.g. simulated attacks vs South Korea); Ship Self-Defense, Area Air Defense, CEC battle-force defense [P2, pp.3-6, 9, Figs.3,5,6,9].
- Fig.6 DRM elements: threat characterization/tactics, environment, BMC4I, trajectories from multiple directions/times, Blue locations, joint campaign, arrayed joint defenses [P2, p.6].

## Defense layer / system element
- Force "super-system"/system-of-systems [P2, pp.2-3, Fig.3]: Shooters SM family (SM-2 III/IIIA/IIIB/IV, IVA Area, SM-3 theater KW/KKV, SM-4 concept, RAM, NSSM); Sensors/C2 (Aegis SPY-1/1B, E-2C, CEC sensor net + CEP, DDS, WCS, BMC4I, airborne fire-control/forward-pass); Platforms (Aegis ships, amphibs SSDS Mk I/II, E-2C, mountain-top surrogate).
- Key vignette: CEC lets ships/aircraft share radar returns; launching ship WCS uses another ship's returns for SM midcourse uplink via own SPY-1 — entire force must be treated as system [P2, p.2].
- NTW as system within ship combat system + battle-force net; APL Technical Direction Agent [P2, pp.3-4]. No boost/midcourse/terminal layering in those terms; no ranges/velocities/Pk/coverage numbers.

## Method / approach
- V-cycle [P2, p.4, Fig.4]: Need/Mission Needs Statement -> ORD (threshold minimum + objective desired, measurable) -> concept formulation (CONOPS, functional blocks/interfaces, high-level models/equations/algorithms, data/tech/risk/cost; DRM top-level perf+cost modeling with weighted criteria) -> requirements partition/allocation top-down with iteration (timing/accuracy budgets, gain margins) -> risk reduction/M&S/prototyping/experiments -> detailed design/fabrication after reviews -> bottom-up integration/test -> Fleet eval -> support/upgrades.
- AoA + trades at each level [P2, pp.5, 8-9]; M&S federation + virtual demos [P2, pp.8-9]; industrial prototyping [P2, pp.9-10]; stimulators/element-in-loop (WASP wraparound, GSEL HWIL anechoic) when elements missing [P2, p.10]; formal T&E mirroring development with DRM-consistent scenarios + range-safety modeling [P2, pp.10-11]; evolution/life-cycle (prototype->EMD->baseline upgrades + tech refresh) [P2, p.12].

## Assumptions
- Mission Need can stay system-agnostic yet convey comms/sensing need; thresholds/objectives measurable; top-level models reflect capability+cost for AoA ranking; validated models serve as virtual test vehicles where live tests unsafe/uneconomical (simulation-extrapolation flag) [P2, pp.4-5, 8-9].
- SM-3 assessment assumed evolved Aegis guides SM-3; SM-3 = SM-2 heritage + prototype kill + range for inland protection [P2, p.5, Fig.5]; sea-surface reflection modeled/accommodated, verified Lear-jet captive-carry [P2, p.11]. No fidelity criteria, confidence, distributions stated.

## Data / simulation setup
- No raw data/code/params. Qualitative setups:
- ADAM (APL Defended Area Model) [P2, p.8, Fig.8]: radar-range vs SM-3 config vs targets -> ship operating area to defend location from threat direction. Federation APL+Navy; inputs: threat params/6-DOF/pointing/accel/RCS, EOB, engagement constraints, WCS (detection range, angular accuracy, update periods, track accuracy), interceptor/KKV/warhead params, TBM heating OSC-18, IR acquisition table, seeker sensitivity, TOF uncertainty, miss-distance table (type, maneuver level/freq, closing vel, altitude, KW vel), divert table (Tgo, maneuver, KKV vel, altitude), lethality (warhead, closing vel, strike angle, miss, aspect), operating/defended regions. Blocks: terminal sim, lethality, post-processing + Peels workbench. Successor ARTEMIS (full SM kill-chain detection->intercept integration, in development) [P2, pp.8-9]. No resolution/runtime/validation data.
- OCMD virtual demo, Warfare Analysis Lab [P2, p.9, Fig.9]: CEC forward-pass (ship SM beyond horizon via airborne radar + airborne illumination, ship->aircraft handover via modified SM/CEC/Aegis); multi-org high-fidelity models + DRM-like Korea scenario; confirmed requirements, siting/timing vs terrain blockage. No model names/counts/MOEs.
- GSEL anechoic (Bldg 1) mounts SM seeker, feeds simulated guidance, presents microwave/IR signatures; guidance-in-loop; pre-test confirmation + post-flight reconstruction [P2, pp.10-11, Fig.10]. WASP wraparound (Terrier/Tartar origin) for multi-vendor interfaces; CEC CEP to multiple combat systems [P2, p.10].
- Experiments: sapphire IR window (theory+lab+wind-tunnel; crystal-orientation fix); CEC fade-margin/Tx/antenna + radar playback into composite-tracking; 1996 Mountain Top ACTD Hawaii (CEC Aegis + modified SM-2 IIIA beyond horizon via mountain surrogate illuminator; new regime; receiver mod; Lear-jet captive-carry incl. sea-surface effects) [P2, pp.7-9, 11]. No sample sizes/dates except 1996, no frequencies/waveforms/miss distances.

## Metrics & results
- Essentially no quantitative metrics (Pd/Pk/RMSE/latency/area). Qualitative outcomes only: SM LEAP KW scored highest on cost/risk/capability/schedule -> SM-3 basis (no scores) [P2, pp.5-6, Fig.5]; NTW boost-vel/SPY-1B discrimination trades (no values) [P2, p.6]; SM standardization "major life-cycle saving + similarity," rapid III/IIIA/IIIB/IV upgrades expediting IVA/SM-3/SM-4 (no $/%) [P2, p.7]; sapphire one orientation met requirements (no numbers) [P2, p.7]; ADAM defended-area map only [P2, p.8]; OCMD "confirmed/illuminated requirements," siting/timing (no MOEs) [P2, p.9]; CEC DDS proto "fully met requirements in short time" (no specs) [P2, p.10]; GSEL caught SM-3 software flaw that "could have resulted in test failure" (no details) [P2, p.10]; Mountain Top first over-horizon shot "direct hit" (n=1, no miss) [P2, p.11]; life-cycle counts: Aegis 6 baselines since IOC 1983, SM-2 Blk IV, SSDS Blk 2, CEC Baseline 2 [P2, p.12]; COTS service-layer + beta-partnering + array modules + Raytheon/NSA anti-tamper (no MTBF/cost) [P2, p.12]; JWAD life-cycle/reliability analyses for AoA/spares (no numbers).

## Baselines & comparisons
- NTW missile AoA: IVA vs LEAP (winner) vs Marinized THAAD vs Boosted THAAD vs New missile (no weights) [P2, p.6, Fig.5]. Commonality/modularity vs clean-sheet (author favors commonality) [P2, pp.6-7]. Prototype vs EMD vs upgrade baselines; Aegis/SSDS/CEC blocks [P2, pp.3, 12]. "Modeling cannot substitute for real-world testing" — simplified models vs uncovered test conditions, no V&V quantification [P2, p.9].

## Claims vs evidence
| Claim | Evidence | Assessment |
|---|---|---|
| V-cycle produces successful adaptable systems | Definition + diagram + anecdotes; Kossiakoff & Sweet | framework, not demonstrated |
| Force-as-system required; CEC off-board guidance | Architecture + vignette | plausible illustration; no latency/accuracy data |
| LEAP KW best NTW approach | Reported AoA win; models/DRM referenced not shown | program fact, not reproducible |
| ADAM enables trades; ARTEMIS will integrate full chain | Block diagram + example plot; ARTEMIS in development | diagram-level; simulation-only flag |
| OCMD virtual confirmed requirements/siting | Multi-org models + Korea scenario | simulation-only; no MOEs/live confirmation |
| Sapphire orientation root cause | Post-failure theory refinement | anecdote; no curves |
| Rigor caused Mountain Top hit | n=1 + pre-test list | correlation asserted; no control; not a Pk |
| WASP/GSEL reduce risk; GSEL caught flaw | Description + anecdote | plausible; unquantified |
| Commonality contains cost/accelerates | History narrative | interpretation; no deltas |
| COTS layer enables refresh/influences products | Description + anecdote | existence example; no numbers |

## Limitations
- Authors stated: models simplified, not substitute for testing; partitioning needs iteration; PM schedule/funding <-> requirements coupling; test design needs modeling but assumptions bound insight; scale/complexity + fewer staff + low failure tolerance need new tools/visualization/networked testing [P2, pp.4, 9, 11-13].
- Identified: no quantitative results/stats/params; success bias only; n=1 live fire; federation/V&V gap (no accreditation, interfaces, sync, latency, fidelity); DRM/threat/RCS/EOB/BMC4I loads withheld; industrial/HWIL specs omitted; life-cycle/COTS unquantified; dated 2001 context (pre-SM-3 maturity, Baseline 6, CEC Baseline 2).

## Reproducibility: Low. No equations/algorithms/code/data/thresholds. Needed outside paper: DRM family, 6-DOF/trajectories, sensor/track tables, divert/lethality tables, KKV/seeker params, GSEL calibrations, AoA weights/costs, range geometry. Best artifact: V-cycle Fig.4, T&E purposes, concept checklist, Concept Development Lab tool list — encodable as VisualSim stage gates, not executable models.
## Key references: Kossiakoff & Sweet (systems text); CEC 16(4) 1995; DoD 5000.1; Skolnick & Wilkins 2000; Zinger & Krill 1997 Mountain Top; Kauderer 2000 methodology; JWAD DRM/ADAM/ARTEMIS/GSEL/WASP specs (needed, not cited with access).
## Quotable facts
- "interrelated components functioning together toward a common objective" / "interdisciplinary approach toward methodical realization" [P2, p.1]; success criteria quote [P2, p.1]; "real-time interaction ... requires the entire force to be treated as a system" [P2, p.2]; Fig.4 V-cycle [P2, p.4]; threshold+objective measurable rule; ADSD ORDs for CEC/SM/Area/NTW/SSDS [P2, p.5]; concept package checklist [P2, p.5]; LEAP selection [P2, pp.5-6]; ADAM federation + ARTEMIS full-chain quote [P2, p.8]; "Modeling cannot be a substitute for real-world testing" [P2, p.9]; forward-pass + Mountain Top 1996 + OCMD Korea siting/timing [P2, p.9]; DDS prototyping [P2, p.10]; stimulator principle + WASP origin + CEC multi-vendor [P2, p.10]; GSEL definition + SM-3 flaw [P2, p.10]; T&E 4 purposes [P2, pp.10-11]; DRM-consistent scenarios + range safety + assumption-bound insight [P2, p.11]; first over-horizon "direct hit" + Lear-jet sea-reflection [P2, p.11]; baselines counts [P2, p.12]; COTS layer + beta-partnering + modules + anti-tamper [P2, p.12]; Bldg 26 lab (library, war room, viz, force modeling with JWAD, test participation; DB-linked diagrams; gap detection; remote WASPs; collaborative spec/design/test/sim) [P2, p.13, Fig.11].

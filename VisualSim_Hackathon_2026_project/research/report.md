# Deep Research Report — 4 papers from research.txt (SKILL.md workflow)
Corpus: [P1] O'Haver et al. 2018 | [P2] Krill 2001 | [P3] Moskowitz et al. 2002 | [P4] Brown et al. 2005 (abstract-only, paywalled)
Full notes: `research/notes/P1_OHaver2018.md`, `P2_Krill2001.md`, `P3_Moskowitz2002.md`, `P4_Brown2005.md`. Synthesis: `research/synthesis.md`.

## 1. Executive summary (238 words)
Three full-text JHU APL papers plus one paywalled OR article abstract were analyzed. The strongest cross-paper result is that force-level coordination beats unit-centric defense under saturation, but only if track correlation is solved: in the ACES 20-threat vignette the bidded DED scheme was nearly perfect under ideal conditions yet degraded sharply under achievable conditions where 88-96% of dynamic-scheme overengagements came from multiple track numbers for the same object (avg 1.3 remotes/object), with only 1 of 400 achievable runs leak-free [P3]. Radar history shows why the picture is hard: low-altitude firm-track ranges varied by more than 2x with environment, reconstructed well only when METOC data were collected (units withheld) [P1]. Systems engineering provides the process wrapper — V-cycle, DRM-driven AoA, federated models (ADAM/ARTEMIS), HWIL (GSEL/WASP), and virtual demos — but offers no quantitative performance numbers and rests on anecdotes including an n=1 over-horizon hit [P2]. Interceptor pre-positioning optimization (JOINT DEFENDER) claims minute/second-scale solutions and secrecy insights, but only the abstract was accessible so nothing numeric is verified [P4]. Confidence: high that correlation/fusion quality dominates latency for coordination; medium that S-band cost compromise and AESA/DBF directions are correct (undisclosed trades); low for any absolute Pk/Pd/latency value — the corpus provides architecture and failure modes, not calibrations.

## 2. Scope & corpus
- Papers covered: 4 IDs (3 full text, 1 abstract). Files: `research/P1_OHaver2018.pdf/.txt` (14 pp, 59k chars), `P2_Krill2001.pdf/.txt` (14 pp, 50k), `P3_Moskowitz2002.pdf/.txt` (14 pp, 60k), [P4] RePEc metadata only (INFORMS paywall, DOI 10.1287/opre.1050.0231).
- Anything unreadable: [P4] full text (paywalled); [P1] pp.12-13 mid-sentence extraction fragment excluded; all figures read as text-extracted captions/descriptions (no image pixel analysis).
- Markings: none found in any accessed file (no Distribution A/CUI/FOUO text in extractions).

## 3. Landscape overview
| Layer | Papers | Trend |
|---|---|---|
| Sensing/hardware | [P1] | Switched-beam -> phase-shifter -> computer multifunction -> environment-coupled -> AESA/DBF suites; S+X band split; cost-driven deletions (SPY-4, CG(X)) |
| Process/federation | [P2] | V-cycle + DRM + AoA + ADAM/ARTEMIS + WASP/GSEL + virtual-follow-on-test + COTS refresh |
| Coordination/C2 | [P3] | Static sectored -> dynamic unbidded -> bidded DED; ideal-near-perfect -> achievable correlation-limited |
| Allocation/optimization | [P4] | Heuristics/supercomputing -> bilevel MILP + secrecy variants (claimed fast) |
Full taxonomy + matrix in `synthesis.md` §1-2.

## 4. Detailed findings by theme
### 4.1 Sensing & tracking [P1 + P3]
- Microsecond beam repositioning + T/R-period-synced scheduling/tracking/testing + rapid confirmation dwells + Monte Carlo firm-track logic are the canonical phased-array abstractions [P1, p.2-4]. RP&A planned with constant-mean Swerling IV for 95% track-init >=20s before special auto-TBMD reaction; ACES used roll/frequency-averaged VV aspect-dependent Swerling IV means (believed more accurate) [P3, pp.7-8].
- Propagation: 10 GHz Tx at 15 m, ducts 4/14/24 m; horizon ~15-dB contour; ducting can overcome curvature [P1, p.5, Fig.4]. Clutter = propagation factor x normalized RCS integrated over cell [P1, p.5]. Gulf large duct -> clutter enhanced all directions [P1, p.5, Fig.5]. Reconstruction needs METOC (AEAS/rocketsonde/HAPS range-dependent profiles) [P1, p.6].
- Detection shortfall: only 84.1% +/-0.5% detected in time; 708 undetected by planned unit (of 4500); RP&A 95% goal failed (RCS too high) so extended mission chosen [P3, p.10, Fig.6]. Launches can precede complete detections — correct solution then unguaranteeable [P3, p.12, Fig.12].
- VisualSim implication: implement duct-height parameter (test 4/14/24 m at 10 GHz/15 m), confirmation-dwell + Monte Carlo initiation, Swerling IV aspect RCS hook, METOC-conditional accuracy. Values: not stated — use as structure, calibrate elsewhere.

### 4.2 Discrimination & classification
- [P1]: warhead discrimination via new waveform + search/association/tracking/discrimination algorithms (Area), new waveform + surveillance + tracking (Theater Wide/LEAP), LRDR wide FOV + wide instantaneous bandwidth + feature suite + high sensitivity at long range; S-band acceptable vs X superior-but-costly (undisclosed curves) [pp.9-10]. [P3]: max 5 simultaneous discriminations/platform (ORD threshold/objective); discrimination = expending radar to gather metrics to pick object [p.4]. POT via Baseline 6 Ph 3 + 3-sigma ellipse to highest-priority asset inside [pp.7-8]. No features/classifiers/Pd/Pfa numbers anywhere in corpus.

### 4.3 Guidance, navigation & control
- Thin in corpus. [P2]: SM rear-reference receiver sea-surface fix via Lear-jet captive-carry; GSEL seeker-in-loop with microwave/IR signatures; SM-3 software flaw caught pre-test [pp.10-11]. [P3]: SM-2 IVA dual salvos, 2nd unscheduled until 1st in flight; kill tests (launcher/prelaunch/inflight/uplink/handover/lethality) geometry-independent but RV-in-track-dependent [pp.4, 8]. No guidance laws, autopilots, miss distances.

### 4.4 Engagement & resource management [P3 core + P4 framing]
- Saturated arithmetic: discriminations x shooters x depth = threats, so each overengagement -> free rider (except non-overlapping) [P3, pp.279-280]. Engageability in vignette: 0 by all 4, 9 by 3, 7 by 2, 4 by 1; zero reengagement [P3, p.277].
- Ideal ranking (100 runs): DED nearly perfect > first launch > free fire > sectored-worst (sectored mass at 6 free riders; Unit1 4/4, Unit2 misses 2/7, Unit3 misses 4/9) [P3, pp.9-10, Figs.4-5]. DED ideal needs >=40s early detection; 3 dual-track exceptions [P3, p.10].
- Achievable: free fire ~same; sectored ~same (zero overengagements, 5-6 free riders); dynamics much worse on overengagements (96% first-launch / 88% DED from multi-tracks) though free riders only modestly higher; DED extra launches (Units1,4 ~always 5 targets) -> more duds counted as overengagements; leakers > free riders; 1/400 zero-leaker (DED) [P3, pp.10-13, Figs.7-13].
- Constants for modeling: coord time 4.375s ideal / 12.25s achievable; soft 3 / hard 5 / tolerance 3 / group 1000 m; surveillance 1/1.5s, engagement 1/0.875s, 2 msgs/slot; 1-s decision period [P3, p.6, Table 1].
- [P4] frames pre-positioning + secrecy as bilevel optimization with claimed minute/second runtimes on laptop for realistic/N. Korea scenarios (abstract only, unverified).

### 4.5 C2/BMC3I & architecture
- Common-algorithm principle: "if all units use same info + same algorithm, all arrive at same decisions" [P3, p.274]. FES + hierarchical DB (group->threat->shot) + grouping/freezing/ordering + 8-test sieving is the most detailed coordination algorithm in corpus [P3, pp.3-6].
- DED needs heavy net (engagement info + J-messages); first launch needs launch messages only; sectored needs none — with corresponding fragility ordering under uneven raids [P3, pp.2-3].
- Force-as-system vignettes: Aegis-to-Aegis off-board returns->WCS->SPY-1 uplink [P2, p.2]; CEC forward-pass ship->aircraft handover beyond horizon (1996 Mountain Top n=1 + OCMD Korea virtual for siting/timing vs terrain) [P2, pp.9, 11]; distributed sensor/weapon coordination among Area BMD ships (Baseline 6 Ph III, canceled) [P1, p.9].
- Latency vs quality verdict (interpretation, not isolated test): comm latency + changing launch times "seemed less effect than air picture quality" [P3, p.284].

### 4.6 Evaluation
- No Pk table in corpus. Effective Pk=1 by construction in [P3] ideal; achievable kill tests exist but values withheld; geometry dependence planned not implemented [P3, p.8]. [P2] n=1 hit is not a Pk [p.11]. [P1] no Pd/Pfa. [P4] no metrics in abstract.
- Monte Carlo discipline: [P3] 100 runs/scheme/config with 10-s impact spread + 95% CI plotted (values untabulated); [P1] 20-case reconstruction + Monte Carlo mentioned (N undisclosed); [P2] no statistics.

## 5. Comparison matrix
See `synthesis.md` §2 (rows = papers; cols = problem/method/fidelity/metric/limitation). Do not compare numbers across papers — assumptions incomparable.

## 6. Critical assessment
Strengths: (a) most detailed coordination algorithm + failure-mode accounting in unclassified TBMD literature [P3]; (b) end-to-end radar environmental physics lessons with concrete test setups [P1]; (c) reusable V-cycle + federation + HWIL patterns with named facilities/models [P2]; (d) clean optimization framing for pre-positioning/secrecy [P4 abstract].
Weaknesses / validity threats: single-vignette + 100-run limits + visual-only distributions [P3]; METOC-conditioned reconstruction + undisclosed trades + no calibrations [P1]; anecdote-only evidence + n=1 + federation/V&V gap [P2]; paywalled + perfect-information + no numbers [P4]. Common threats: simulation-only tuning, proxy biases (CEC for Link-16 [P3, p.279]), planned-pair tuning, enlarged assets, ground-truth clustering, reliability-overengagement conflation, success/survivorship bias, dated contexts (2001-02 systems, 2018 radar).

## 7. Gaps & open questions
Filed in `research/open-questions.md` (7 gaps: sensor tables, C2 distributions, flyout/Pk/lethality, cost/power, EA/hypersonic/mixed-mission, seeds/code, [P4] full text).

## 8. Suggested further reading (only things referenced in papers; no invented citations)
- Shafer et al. (taxonomy/future schemes), Bates et al. (detection/track/correlation), McDonald et al. (comms) — all "this issue" companions to [P3].
- Rottier et al. 2001 (environment), Newkirk et al. 2001 (TEMPER), Sylvester et al. 2001 (decision aids), Agrawal et al. 2001 (AESA) — [P1] Refs.6-9.
- Frank & O'Haver 1993, Phillips 1981, Irzinski 1981, Gussow & Prettyman 1992 — [P1] Refs.1-5 (Typhon/AMFAR/Aegis).
- Kossiakoff & Sweet (systems text), CEC 16(4) 1995, DoD 5000.1, Skolnick & Wilkins 2000, Zinger & Krill 1997 Mountain Top, Kauderer 2000 — [P2] Refs.1-6.
- JNL 198 + OS-516.2 (Network 021A, 8.7 mrad/150 m), Capstone + Navy TBMD COEA Day D+5, DICE 6-DOF, Baseline 6 Ph 3, RP&A + Guaranteed Useful Search, TBMD ORD — per [P3] (full citations in note).
- Owen 1969, Bracken et al. 1987, Moore & Bard 1990 — per [P4] IDEAS refs; plus INFORMS full text DOI 10.1287/opre.1050.0231 via library.

## 9. Bibliography
- [P1] O'Haver, Barker, Dockery, Huffaker (2018). Radar Development for Air and Missile Defense. JHU APL Tech. Digest 34(2), 140-153. File: `research/P1_OHaver2018.pdf`.
- [P2] Krill (2001). Systems Engineering of Air and Missile Defenses. JHU APL Tech. Digest 22(3), 220-233. File: `research/P2_Krill2001.pdf`.
- [P3] Moskowitz, Gassler, Paulhamus (2002). A Comparison of TBMD Engagement Coordination Schemes. JHU APL Tech. Digest 23(2-3), 272-285. File: `research/P3_Moskowitz2002.pdf`.
- [P4] Brown, Carlyle, Diehl, Kline, Wood (2005). A Two-Sided Optimization for Theater Ballistic Missile Defense. Operations Research 53(5), 745-763. DOI 10.1287/opre.1050.0231. File: abstract-only `research/notes/P4_Brown2005.md`.

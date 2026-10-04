# Synthesis — 4-paper missile defense set (research.txt)
IDs: [P1] O'Haver et al. 2018 (radar) | [P2] Krill 2001 (systems engineering) | [P3] Moskowitz et al. 2002 (ACES coordination) | [P4] Brown et al. 2005 (JOINT DEFENDER, abstract-only)

## 1. Taxonomy
| Paper | Problem | Defense layer | Method family |
|---|---|---|---|
| [P1] | Naval radar capability vs evolving air/cruise/BM threats + littoral environment | Sensing (shipboard multifunction phased-array, AESA, BMD sensors, AMDR) | Historical review + systems engineering + propagation modeling (TEMPER/FirmTrack) |
| [P2] | How to engineer networked air/missile defense as system-of-systems | All layers via process (requirements, AoA, M&S federation, HWIL, T&E, life-cycle) | V-cycle prescription + federation (ADAM/ARTEMIS) + virtual demo + prototyping |
| [P3] | Who shoots which TBM under imperfect picture + limited comms | C2/engagement coordination (Aegis area TBMD, Link-16) | Discrete-event federation (ACES 0.9) + 4-scheme Monte Carlo comparison |
| [P4] | Where to pre-position interceptors vs worst-case attacker (+ secrecy value) | Architecture/resource allocation | Bilevel/MILP two-sided optimization (JOINT DEFENDER) |

Method families span hardware physics ([P1] propagation), process ([P2]), high-fidelity engagement sim ([P3]), operations research ([P4]).

## 2. Comparison matrix
|  | Problem | Method | Data/fidelity | Key metric (with location) | Main limitation |
|---|---|---|---|---|---|
| [P1] | Ship radar vs ASCM/BM/littoral | Review + TEMPER/FirmTrack + AESA insertion | Illustrative contours/bars, no raw data; 20-case reconstruction, units withheld | >2x firm-track variability; reconstructed "very well" when METOC collected [P1, p.6, Fig.7]; 90+ SPY-1 ships; 560 T/R 1994 flight test | No Pd/Pfa/SNR/accuracy numbers; METOC-conditioned circularity; undisclosed trades |
| [P2] | System-of-systems engineering | V-cycle + ADAM/ARTEMIS + WASP/GSEL + Mountain Top ACTD | Anecdotes; n=1 over-horizon hit; no datasets | SM LEAP selected (no scores); first over-horizon "direct hit" (n=1) [P2, p.11]; Aegis 6 baselines since 1983 | No statistics/params; success bias; federation/V&V gap |
| [P3] | Engagement coordination | ACES 0.9, 4 schemes, ideal vs achievable, 100 runs/scheme | 20-threat/4-ship DICE vignette; Swerling IV + biases + Link-16 slots + kill tests | Ideal DED nearly perfect; achievable: 84.1% in-time detections, 708 undetected [p.281]; 1.3 remotes/object [p.282]; 96%/88% overengagements multi-track [p.282]; 1/400 zero-leaker runs (DED) [p.283] | Single vignette; ground-truth clustering; CEC-bias proxy; seeds/code withheld; overengagement conflates reliability |
| [P4] | Interceptor pre-positioning | JOINT DEFENDER bilevel/MILP | Abstract only; 2 hypothetical N. Korea scenarios named | "Minutes" transparent / "seconds" secret (abstract, unverified) | Paywalled; perfect-information framing; no numbers |

Metric comparability: DO NOT compare [P1] firm-track variability, [P2] n=1 hit, [P3] free-rider/leaker distributions, [P4] runtime claims — produced under incomparable assumptions.

## 3. Agreements
- Force-as-system: [P1] CEC distributed coordination + offboard cue [pp.8-9]; [P2] entire force must be treated as system, off-board radar->WCS->uplink vignette [p.2]; [P3] force-level pairing beats unit-centric [pp.1-3]; [P4] force-level pre-positioning vs worst-case attacker (abstract). Four-way agreement, different layers.
- Models supplement but never replace live testing: [P1] reconstruction conditioned on METOC + withheld units; [P2] explicit "cannot substitute for real-world testing" [p.9]; [P3] achievable picture poor despite detailed modeling; [P4] hypothetical scenarios only.
- Environment / imperfect information dominates: [P1] >2x variability environmental; [P3] picture quality > latency effect; [P2] DRM/threat realism as foundation; [P4] complete-information baseline acknowledged as variant (abstract).
- Pre-planning for planned pairs fails under unplanned geometry: [P1] nominal-atmosphere failure low-altitude; [P3] planned-pair-tuned search + sectored fragility to uneven raids.

## 4. Contradictions / tensions (no direct conflicts; different emphases)
- Latency vs quality: [P3] concludes picture quality outweighed latency/launch-time effects (interpretation, no isolating sweep) — does not contradict [P1] microsecond beam-scheduling need (different timescale: engagement-message seconds vs radar T/R sync). Keep separate.
- Centralization: [P3] DED (centralized common algorithm) best ideal but gap narrows achievable due to correlation errors — tension with [P2] CEC forward-pass success narrative (n=1) and [P1] distributed sensor/weapon coordination claims (uncanceled details withheld). Net: centralization helps only if correlation is solved.
- Cost Operators: [P1] documents S-band cost compromise + SPY-4 deletion + CG(X) cancellation (cost drives architecture); [P2] commonality/COTS contains cost (no numbers); [P4] least-worst-case allocation (no costs in abstract). No commensurable cost metric.

## 5. Evolution / recurring ideas
- 1960s-2018 arc [P1]: switched-beam -> phase-shifter -> computer-controlled multifunction -> environment-coupled prediction -> distributed solid-state AESA/DBF -> suite-of-radars (S+X+controller). Recurring: sensitivity vs cost vs discrimination vs field-of-view compromise.
- Process continuity [P2] 2001: V-cycle + DRM + AoA + federation + HWIL + T&E + upgrades — same pattern [P1] uses implicitly (Roadmap/AoA/Radar-Hull/TLRP) and [P3] instantiates (ACES + companions + COEA scenario).
- Coordination refinement: static sectored -> dynamic unbidded (first launch) -> bidded DED [P3]; secrecy extensions [P4] as next step (unverified beyond abstract).
- Federation growth: FirmTrack+EMPE coupling 1985 [P1] -> ADAM multi-model + ARTEMIS full-chain intent [P2] -> ACES multi-org high-fidelity + Link-16 + kill-chain tests [P3] -> optimization over pre-positioning [P4].

## 6. Evidence strength map
- Well supported across papers: (a) phased-array scheduler with T/R sync + confirmation dwells + Monte Carlo firm-track logic is the right sensor abstraction [P1 p.3-4 + P3 RP&A/search/detection modeling]; (b) ducting/multipath/clutter must be modeled for shipboard low-altitude detection [P1 Figs.4-5,7]; (c) saturated raids convert overengagement into free riders [P3 pp.279-280]; (d) multi-track/duplicate-track errors are the dominant coordination failure mode (88-96% of dynamic-scheme overengagements) [P3 p.282]; (e) force-level assignment outperforms static partitioning under uneven raids [P3 Figs.4,7 + P2 Mountain Top/OCMD narratives].
- Single-simulation only: all [P3] numeric distributions (one vignette, 100 runs); [P1] Fig.7 reconstruction; [P2] ADAM defended-area example; [P4] runtime + secrecy claims.
- Unsupported by corpus: any Pk/Pd/Pfa/SNR/accuracy/latency value usable directly for VisualSim calibration (none provided with units + distributions + validation).

## 7. Gaps (see open-questions.md)
1. No usable sensor Pk/Pd/Pfa/RCS/SNR/accuracy tables with distributions.
2. No C2 latency distributions beyond coordination-time constants (4.375s ideal / 12.25s achievable) + slot periods (1.5s surveillance, 0.875s engagement) [P3, p.6].
3. No interceptor flyout/Pk/lethality numbers (SM-2 IVA dual-salvo policy stated, no probabilities tabulated) [P3].
4. No cost/energy/power numbers (ship SWaP, T/R efficiency, array cost curves all withheld).
5. No EA/jamming, maneuvering hypersonic, or mixed-mission resource contention modeling.
6. No seeds/code/inputs for any sim — numeric replication impossible from corpus alone.
7. [P4] full formulation + scenarios + solver results missing (paywall).

## Verification notes
- All page/figure refs re-checked against extracted txt (P1 59k chars, P2 50k, P3 60k chars). [P4] limited to RePEc abstract; marked partial.
- No distribution/classification markings found in any accessed file.
- Mid-sentence fragment at [P1] pp.12-13 boundary ("tional multifunction...") excluded as extraction artifact.

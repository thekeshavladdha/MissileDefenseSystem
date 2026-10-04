# Radar Development for Air and Missile Defense (O'Haver, Barker, Dockery, Huffaker, 2018, JHU APL Technical Digest 34(2), pp.140-153)
- File: `VisualSim_Hackathon_2026_project/research/P1_OHaver2018.pdf` + `.txt` (14 pages, PAGE 1-14). Markings: none. Public-release review article.

## Problem & motivation
- 1950s need: beam repositioning within microseconds to track growing target counts; mechanical reflectors insufficient [P1, PAGE 2].
- 1965 Navy requirement: phased-array with combined surveillance + tracking + missile-guidance + high ECCM resistance; APL tasked via AMFAR to retire risk [P1, PAGE 2].
- Early Aegis tests: predicted vs observed low-altitude performance rarely agreed, highly variable — required explicit refraction / low-elevation propagation modeling [P1, PAGE 4].
- ASCM proliferation (USS Stark 1987 cited) drove "leak-proof" own-ship defense vs small fast maneuvering raids crossing horizon in littorals with anomalous propagation + clutter [P1, PAGE 7].
- Desert Storm 1991 Iraqi ballistic-missile use spurred Navy BMD; later IAMD needed sensitivity beyond SPY-1, clutter rejection, wide instantaneous bandwidth for discrimination [P1, PAGES 9-10].

## Threat/mission context
- Air threats 1950s-60s; low-altitude ASCM emerging from behind horizon at short range (timeline stress); littoral anomalous propagation + sea/land clutter (Arabian Gulf surface duct as canonical case, Fig.5); ballistic missiles (Scud-type endo Area BMD; exo SM-3/LEAP; NMD/ICBM midcourse with forward-based sensors); electronic attack throughout [P1, PAGES 4-5, 9].
- Missions: open-ocean/littoral air defense, BMD, IAMD, SUW, CEC connectivity, semi-active illumination, interceptor comms, kill assessment [P1, PAGES 4, 7, Fig.11 p.11].

## Defense layer / system element
- Shipboard multifunction phased-array fire-control sensor: Typhon -> AMFAR -> AN/SPY-1A/B/D(V), 90+ ships [P1, PAGES 2-4].
- Environment layer: EMPE->TEMPER + METOC + FirmTrack + aids (SEAWASP, SPY-1 Sliderule), delivered as GFI [P1, PAGES 4-7].
- AESA layer: CEC AESAs -> SPY-3 (X-band horizon/self-defense/illumination) + SPY-4 S-band VSR -> DBR suite (SPY-4 later deleted for cost) [P1, PAGES 7-8].
- BMD sensors: modified SPY-1 (Area/Theater Wide, Aegis Ashore), repurposed THAAD -> AN/TPY-2 forward-based, LRDR S-band midcourse discrimination [P1, PAGES 9-10].
- IAMD: AMDR/AN/SPY-6 (AMDR-S S-band + X-band + Suite Controller) on DDG-51 Flight III [P1, PAGES 10-12].

## Method / approach
- Systems-engineering process: need -> concept/requirements -> tech + critical experiments -> industry transition -> at-sea testing -> effectiveness eval. APL as innovator/advisor/partner [P1, PAGES 1, 3, 13].
- AMFAR 1964-69 (rooftop Bldg 6): transmitter + array + signal processor + computer control; auto detection/tracking with clutter resistance [P1, PAGE 2]. Ferrite garnet phase shifter (temperature-insensitive); sum/difference monopulse beamformer; array-of-subarrays (e.g. 64 elements per subarray, dozens of tubes, 1-2 tube loss = modest degradation) [P1, PAGE 2]. Scheduling/tracking/testing within single T/R period for radar-computer sync [P1, PAGE 3]. 4->2 transmitters via waveguide time-share [P1, PAGE 3].
- Environment: FirmTrack (late 1970s, confirmation dwells + Monte Carlo) + EMPE (1982, coupled 1985, ->TEMPER); METOC via AEAS/rocketsonde/HAPS; SEAWASP unfunded for Aegis, fed Sliderule [P1, PAGES 4-7].
- AESA: GaAs MMIC T/R-per-element; CEC airborne 560-module flight test 1994 -> shipboard late 1990s; GaN + DBF + distributed RX/exciter for AMDR via ARTIST/AUSPAR [P1, PAGES 7-8, 11].
- BMD: incremental SPY-1 mods (offboard cue, sensitivity, surveillance/tracking/discrimination, new waveform, CEC distributed coordination in Baseline 6 Ph III canceled early 2000s); NMD concept 1999 (forward sensors + US-launched midcourse); TPY-2 at Shariki, Aomori; LRDR trades -> Lockheed Martin late 2015 leveraging AMDR-TD + SPY-1 BMD algorithms [P1, PAGES 9-10].
- AMDR: Roadmap 2000 -> AoA (large S + small X preferred) -> Radar/Hull (scaled AMDR + DDG-51 + future Aegis; CG(X) canceled Apr 2010) -> TLRP -> 3-prine TD -> EMD 2014 Raytheon at TRL 6, EDM Kauai FY2017 demo [P1, PAGES 10-12].

## Assumptions
- Nominal-atmosphere + spherical Earth initially assumed sufficient; proven false low-altitude — must include refraction [P1, PAGE 4].
- TEMPER success conditioned on accurate METOC input ("if proper METOC data had been collected") [P1, PAGE 6].
- Passive-loss vs AESA-gain, X vs S band choices stated as judgment without curves: X for horizon/self-defense/illumination; S (~3 GHz) for volume/LRDR/AMDR-S on cost; X superior discrimination but cost unjustified at same sensitivity/FOV [P1, PAGES 7-8, 10]. Ionosphere negligible above L-band (~1 GHz) in many cases; present at S but mitigable, negligible at X — "early trade study," ongoing [P1, PAGE 10].

## Data / simulation setup
- No raw datasets/code/equations/tables. Narrative only.
- FirmTrack: phased-array-specific incl. confirmation dwells + Monte Carlo; no N/logic/code [P1, PAGE 4].
- TEMPER: parabolic-equation, over land/sea, antenna patterns; accredited Navy/MDA; GFI; no equations/grids [P1, PAGES 4-5, 7].
- Fig.4: 10 GHz Tx at 15 m, ducts 4/14/24 m; horizon ~15-dB contour; ducting can overcome curvature (visual only) [P1, PAGE 5]. Fig.5: Arabian Gulf no-duct vs large surface duct clutter (propagation factor x normalized RCS integrated over cell) [P1, PAGE 5]. Fig.7: 20 cases, observed vs reconstructed firm-track range, range units withheld [P1, PAGE 6].
- AESA demos: 560 ITT T/R modules flight 1994; SPY-3 2003 Wallops; SPY-6 EDM Kauai FY2017 — no power/MTBF/sensitivity numbers [P1, PAGES 8, 12].

## Metrics & results
- No Pd/Pfa/SNR/range/accuracy curves. Programmatic milestones only: Typhon terminated 1963 (cost); AMFAR 1964-69 -> SPY-1A; EDP 1969 RCA; 4->2 Tx; SPY-1B 1980s; 90+ ships; FirmTrack late 70s/EMPE 80s/coupled 85; Fig.7 variability >2x, reconstructed-vs-observed "very small relative to variability" (no units); SEAWASP unfunded; SPY-3 1999/2003; LRDR 2014/2015; AMDR CG(X) canceled 2010, EMD 2014 TRL6 [P1, PAGES 2-12].

## Baselines & comparisons
- Typhon (Luneburg switched beams) vs phase-shifter array: Typhon tested OK but unproducible -> terminated [P1, PAGE 2]. Nominal-atmosphere vs +TEMPER+METOC: former rarely agreed low-altitude; latter "excellent" when METOC available (no error stats) [P1, PAGES 4, 6]. Passive tube array (high losses, low efficiency) vs AESA (distributed T/R, higher duty/stability/flexibility/bandwidth/reliability, no central Tx) — qualitative [P1, PAGES 7-8]. X vs S band as above. AMDR digital active array vs SPY-4 analog; DDG-51 vs DDG-1000; Aegis vs TSCE — scaled AMDR+DDG-51+future Aegis preferred, no numbers [P1, PAGES 10-11].

## Claims vs evidence
| Claim | Evidence | Strength |
|---|---|---|
| AMFAR cleared way for Aegis bids | Narrative + Figs.1-2, refs Phillips 1981, Frank & O'Haver 1993; no Pd/Pfa | plausible history; not quantified |
| SPY-1 90+ ships, 4 decades | Photo Fig.3; no ship list | programmatic fact, externally verifiable |
| FirmTrack+TEMPER+METOC reconstructs well; >2x variability environmental | Fig.7 relative bars (20 cases, no units) | qualitative; no error stats/blind protocol |
| TEMPER accredited, widely used, GFI | Assertion + refs Rottier/Newkirk 2001 | by reference, not reproduced |
| AESA greatly improves sensitivity/duty/stability/etc. | Fig.8 + 1994 flight test + late-90s fielding; no deltas | directional; not quantified |
| X for self-defense/horizon, S compromise for volume/LRDR/AMDR-S | Undisclosed trades/AoA | interpretation of hidden trades |
| AMDR TD mature, TRL6, unprecedented cost/perf understanding | Process description | program-status claim, unverifiable here |

## Limitations
- Authors stated: essentially none formal; implicit: Fig.7 units withheld; SEAWASP unfunded; SPY-4 deleted; European Midcourse Radar not programmed; Baseline 6 Ph III canceled; S-band discrimination/ionosphere compromise + ongoing work [P1, PAGES 6-10].
- Identified: no quantitative radar performance for VisualSim calibration; simulation agreement lacks error metrics/blind protocol, METOC-conditioned circularity risk; survivorship/success bias; no equations/code/params/waveforms/schedules/features/DBF/TLRP thresholds/ship SWaP numbers; figures illustrative without scales; PAGE 12-13 extraction fragment incomplete; no cyber/software/test-threat discussion.

## Reproducibility: Low. No code/data/equations/params. Refs: Rottier et al. 2001 (environment), Newkirk et al. 2001 (TEMPER), Sylvester et al. 2001 (decision aids), Agrawal et al. 2001 (AESA), Frank & O'Haver 1993 (arrays), Phillips 1981 (AMFAR), Irzinski 1981 (Aegis), Gussow & Prettyman 1992 (Typhon).
## Key references worth chasing: TEMPER/FirmTrack/SEAWASP/Sliderule/AESA/AMFAR papers above + Roadmap 2000, CG(X) gap 2003, AoA, Radar/Hull, TLRP, LRDR element spec (numbers needed, not in paper).

## Quotable facts
- "reposition beams within microseconds" (1950s need) [P1, p.2]; 1965 requirement quote [P1, p.2]; AMFAR "automatic detection and tracking with resistance to environmental clutter through computer control" [P1, p.2]; garnet ferrite "relatively insensitive to temperature" [P1, p.2]; "scheduling, tracking, and testing within a single transmit/receive (T/R) period" [P1, p.3]; 4->2 Tx via time-share [P1, p.3]; "Over 90 ships" + "nearly four decades" [P1, p.4]; FirmTrack "rapid confirmation dwells" + "Monte Carlo" [P1, p.4]; "rarely agreed ... extremely variable" nominal-atmosphere [P1, p.4]; TEMPER "accredited multiple times" + "over land and sea" [P1, p.4]; Fig.4 "10-GHz ... 15 m" ducts 4/14/24 m, "~15-dB contour", "completely overcome the Earth's curvature" [P1, p.5]; clutter definition + integral [P1, p.5]; Gulf duct "enhanced in all directions" [P1, p.5]; HAPS "range-dependent refractivity profiles" [P1, p.6]; Fig.7 "more than a factor of two" + "agree very well" + "range units are not shown" [P1, p.6]; SEAWASP "not ... funded for installation on Aegis ships" [P1, p.7]; angle-bias correction + GFI [P1, p.7]; AESA module chain quote [P1, p.7]; "greatly improves system sensitivity" + duty/stability/flexibility/bandwidth/reliability list [P1, p.7-8]; "560 T/R modules ... 1994" [P1, p.8]; X-band rationale quote [P1, p.8]; SPY-3 1999/2003 [P1, p.8]; DBR + SPY-4 deletion [P1, p.8]; Desert Storm 1991 BMD spur [P1, p.8-9]; TPY-2 repurpose + Shariki [P1, p.9]; LRDR S-band keys + cost compromise quotes [P1, p.10]; ionosphere L-band/S/X quotes [P1, p.10]; AMDR drivers + AoA large-S + small-X + Radar/Hull DDG-51 + CG(X) Apr 2010 [P1, p.10-11]; GaN enabler [P1, p.11]; EMD 2014 TRL6 + M&S sell-off + Kauai FY2017 [P1, p.12].

# Open Questions — from 4-paper set (research.txt)

1. What are the actual Pd/Pfa/RCS/SNR/track-accuracy distributions for SPY-1B(V)/D vs TPY-2/LRDR/SPY-6 needed to calibrate a VisualSim sensor? Corpus gives structures (confirmation dwells, Swerling IV, 5 discriminations, hexagon engageability) but zero tables [P1, P3].
2. What are the C2 message latency distributions (not just 4.375s/12.25s coordination constants + 1.5s/0.875s slot periods) under loaded Link-16 with 20 C2 + 36 fighters? [P3, p.6].
3. What are the SM-2 IVA (and SM-3/THAAD/Patriot) flyout times, Pk components (launcher/prelaunch/inflight/uplink/handover/lethality), and geometry dependence? Withheld; geometry-independent in ACES 0.9 [P3, p.8].
4. What is the cost/energy/power model (array T/R efficiency, ship SWaP/cooling, LRDR/AMDR cost curves) behind the S-band compromises and deletions (SPY-4, CG(X))? [P1, pp.8, 10-11].
5. How do EA/jamming, maneuvering/hypersonic threats, penaids beyond separable RV/booster, and mixed AAW/OCMD contention change the DED-vs-first-launch ranking? Explicitly future work [P3, p.13]; absent in [P1, P2].
6. Can any result be numerically reproduced? Seeds, RNG order, DICE/RP&A/search inputs, sector files, coordinates, thresholds, SNR formulas, kill probabilities, CI computations all missing [P3]; TEMPER/FirmTrack/ADAM/ARTEMIS/GSEL inputs missing [P1, P2].
7. What does JOINT DEFENDER actually formulate and find? Full text + scenarios + solver + secrecy valuations needed (DOI 10.1287/opre.1050.0231 via library) [P4].
8. What are the correlation/decorrelation thresholds and recorrelation rules whose excursions might restore DED margin? Listed as future work [P3, p.13].
9. What are current (post-2002/2018) system statuses? Corpus is dated (Aegis Baseline 6, CEC Baseline 2, AMDR EMD 2014, LRDR 2015 award) — do not use for present-day capability claims.

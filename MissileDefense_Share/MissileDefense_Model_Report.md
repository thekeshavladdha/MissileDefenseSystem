# Missile Defense Model — Shareable Report

## Which XML to share

Share this working model:

```text
VS_AR\workflow\MissileDefense_Model.xml
```

Optional extras:

```text
VS_AR\workflow\MissileDefense_Start.xml
VS_AR\workflow\MissileDefense_Architecture_Model.xml
VS_AR\workflow\MissileDefense_Model_Sweep.bat
VS_AR\workflow\missile_defense_parameters.csv
VS_AR\workflow\summarize_missile_outcome.py
```

Do **not** share the `Large_Radar_System.xml` internals as the final missile model; it is only a reference.

## What the model does

Pipeline:

```text
ThreatGenerator
  -> DetectionAssignment
  -> InterceptorQueue
  -> C2_Latency
  -> InterceptorFlyout
  -> KillAssessment
  -> DefenseOutcome / KillCount / MissCount / latency plot
```

Meaning:

- `ThreatGenerator`: incoming missiles.
- `DetectionAssignment`: sets threat priority, track hits, C2 latency, flyout time, and random kill draw.
- `InterceptorQueue`: limited tracking/launcher capacity.
- `C2_Latency`: fire-control/command delay, `0.05–0.2 s`.
- `InterceptorFlyout`: `Engagement_Range / Interceptor_Speed`.
- `KillAssessment`: computes `Leaker`, `Effective_Kill`, `Shots_Fired`, and inventory/reload fields.
- `DefenseOutcome`: saves per-threat results.
- `KillCounter` / `MissCounter`: count effective kills and misses.
- `KillCount` / `MissCount`: save counter totals.
- Latency plotter: shows intercept latency over time.

## How to run it

GUI:

1. Start VisualSim License Manager.
2. Start VisualSim Architect.
3. Open `VS_AR\workflow\MissileDefense_Model.xml`.
4. Click `GO`.
5. Open `DefenseOutcome`, counters, and the latency plot.

Batch sweep:

```bat
VS_AR\workflow\MissileDefense_Model_Sweep.bat
```

Then summarize:

```bat
python VS_AR\workflow\summarize_missile_outcome.py
```

## Important fixes already applied

- Sweep runs now use different `Modelseed` values, so Pk runs are not bit-identical.
- Leakers are defined as `threats - effective_kills`, not only late threats.
- Report both:
  - `raw_Pk = killed / threats`
  - `effective_Pk = effective_kills / threats`

## Latest seeded sweep

```text
run1 Pk=0.5 : threats=7 raw_kills=4 effective_kills=2 leakers=5 firm_tracks=7 raw_Pk=0.571 effective_Pk=0.286
run2 Pk=0.8 : threats=7 raw_kills=6 effective_kills=2 leakers=5 firm_tracks=7 raw_Pk=0.857 effective_Pk=0.286
run3 Pk=0.95: threats=7 raw_kills=7 effective_kills=5 leakers=2 firm_tracks=7 raw_Pk=1.000 effective_Pk=0.714
```

## Known limitation

`InterceptorInventory` is a per-engagement starting value with shot counting, not yet a true global inventory that depletes across all threats. Counters report outcomes; a full closed-loop launcher depletion model is still future work.

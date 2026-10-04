# Workout — Next VisualSim / MissileDefense owner

## Current state
- Clone root: `C:\Users\<you>\Desktop\MissileDefenseSystem`
- Main model: `MissileDefense_Share\MissileDefense_Model.xml`
- Working folder: `MissileDefense_Share`
- Baseline frozen: `MissileDefense_Model_baseline.xml` — do not edit
- Context file: `MissileDefense_Share\context.md`
- Planner: `MissileDefense_Share\planner.md`
- Sweep scripts updated:
  - `MissileDefense_Model_Sweep.bat` — 3 Pk seeds
  - `MissileDefense_Policy_Pk_Sweep.bat` — 3 Policy × 3 Pk seeds
- Scorer updated:
  - `summarize_missile_outcome.py` — baseline Pk scorer
  - `summarize_missile_policy_pk.py` — Policy/Pk/ship scorer

## Blocked now
- VS_LM license invalid / Host ID mismatch.
- Do not trust any GO/batch run until license is fixed.

## Immediate tasks after license works
1. Start License Manager, verify `VS_LM\ConsoleMessageLog.txt` says license valid.
2. Open `MissileDefense_Model.xml` in VisualSim Architect.
3. Run `Policy_Mode=0`, `Input_Rate=1.0`, `Pk=0.8`, stopTime 15.
4. Run `Policy_Mode=1`.
5. Run `Policy_Mode=2`.
6. For each, check `DefenseOutcome` fields, `KillCount + MissCount == threats`, and `ship` field split if present.
7. Run `MissileDefense_Policy_Pk_Sweep.bat`.
8. Run `python summarize_missile_policy_pk.py`.
9. Fix one bottleneck/bug, re-run the same sweep.
10. If all modes behave, freeze `MissileDefense_DEDlite.xml` and update docs.

## If GUI crashes
- Check empty relations.
- Check `ShipCoordinator` unwired observer. It may need deletion or blanking of `Smart_Resource_Name`.
- Check `PolicyRouter` output ports are `ship1Out,ship2Out`.
- Check `Merge` has `_type general` on `output/Latency/KilledOnly/MissedOnly`.

## Do not use
- Do not use `visualsim_run_to_verdict`/MCP simulation for this repo until capacity/capacity issues are fixed.
- Do not edit `MissileDefense_Model_baseline.xml`.
- Do not trust `VS_LM` logs if Host ID differs from license file.

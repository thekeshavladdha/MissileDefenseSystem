import glob
import os
import re
from collections import defaultdict

root = os.path.dirname(os.path.abspath(__file__))
groups = defaultdict(lambda: {'threats': 0, 'killed': 0, 'effective': 0, 'firm': 0, 'ship1': 0, 'ship2': 0, 'n': 0, 'reengaged': 0, 'shots': 0})

for path in sorted(glob.glob(os.path.join(root, "MissileDefense_Outcome_*.txt"))):
    if os.path.basename(path) == "MissileDefense_Outcome.txt":
        continue
    name = os.path.basename(path)
    meta = re.search(r"p(\d+)_pk(\d+)", name)
    if meta:
        key = (int(meta.group(1)), meta.group(2))
    else:
        m2 = re.search(r"run(\d+)", name)
        key = ("run", m2.group(1) if m2 else name)
    text = open(path, encoding="utf-8", errors="replace").read()
    blocks = re.split(r"DISPLAY AT TIME", text)
    by_id = {}
    order = []
    for block in blocks:
        completion = re.search(r"------\s*([\d\.]+)\s*sec", block)
        ident = re.search(r"\bID\s*=\s*(\d+)", block)
        kill = re.search(r"\bKilled\s*=\s*(true|false)", block)
        eff = re.search(r"\bEffective_Kill\s*=\s*(true|false)", block)
        firm_track = re.search(r"\bFirm_Track\s*=\s*(true|false)", block)
        ship = re.search(r"\bship\s*=\s*(\d+)", block)
        shots = re.search(r"\bShots_Fired\s*=\s*(\d+)", block)
        if not (ident and kill and eff and completion):
            continue
        rec = {
            't': float(completion.group(1)),
            'killed': kill.group(1) == "true",
            'effective': eff.group(1) == "true",
            'firm': bool(firm_track) and firm_track.group(1) == "true",
            'ship': ship.group(1) if ship else "?",
            'shots': int(shots.group(1)) if shots else 0,
        }
        if ident.group(1) not in by_id:
            order.append(ident.group(1))
        by_id[ident.group(1)] = rec
    d = groups[key]
    for ident in order:
        r = by_id[ident]
        d['threats'] += 1
        d['killed'] += r['killed']
        d['effective'] += r['effective']
        d['firm'] += r['firm']
        d['shots'] += r['shots']
        if r['ship'] == "1":
            d['ship1'] += 1
        elif r['ship'] == "2":
            d['ship2'] += 1
        d['n'] += 1
    # re-engaged = IDs seen more than once in this file
    seen = {}
    for block in blocks:
        ident = re.search(r"\bID\s*=\s*(\d+)", block)
        if ident:
            seen[ident.group(1)] = seen.get(ident.group(1), 0) + 1
    d['reengaged'] += sum(1 for v in seen.values() if v > 1)

print("policy pk  threats raw_kills effective_kills leakers raw_Pk effective_Pk ship1 ship2 firm shots reengaged")
for key, d in sorted(groups.items(), key=lambda kv: str(kv[0])):
    threats = d['threats']
    leakers = threats - d['effective']
    print(
        f"{str(key[0]):>6} {str(key[1]):>4} {threats:>8} {d['killed']:>9} {d['effective']:>13} "
        f"{leakers:>7} {d['killed']/threats if threats else 0:>6.3f} {d['effective']/threats if threats else 0:>11.3f} "
        f"{d['ship1']:>6} {d['ship2']:>5} {d['firm']:>4} {d['shots']:>5} {d['reengaged']:>9}"
    )

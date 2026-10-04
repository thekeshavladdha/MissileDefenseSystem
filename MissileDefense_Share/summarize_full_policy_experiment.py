import glob
import os
import re
from collections import defaultdict

root = os.path.dirname(os.path.abspath(__file__))
groups = defaultdict(lambda: {'threats': 0, 'killed': 0, 'effective': 0, 'firm': 0, 'ship1': 0, 'ship2': 0, 'n': 0})

for path in sorted(glob.glob(os.path.join(root, "MissileDefense_Outcome_p*_pk*_s*.txt"))):
    name = os.path.basename(path)
    meta = re.search(r"p(\d+)_pk(\d+)", name)
    key = (int(meta.group(1)), meta.group(2)) if meta else (None, None)
    text = open(path, encoding="utf-8", errors="replace").read()
    blocks = re.split(r"DISPLAY AT TIME", text)
    for block in blocks:
        ident = re.search(r"\bID\s*=\s*(\d+)", block)
        kill = re.search(r"\bKilled\s*=\s*(true|false)", block)
        eff = re.search(r"\bEffective_Kill\s*=\s*(true|false)", block)
        firm_track = re.search(r"\bFirm_Track\s*=\s*(true|false)", block)
        ship = re.search(r"\bship\s*=\s*(\d+)", block)
        if not (ident and kill and eff):
            continue
        groups[key]['threats'] += 1
        groups[key]['killed'] += kill.group(1) == "true"
        groups[key]['effective'] += eff.group(1) == "true"
        groups[key]['firm'] += bool(firm_track) and firm_track.group(1) == "true"
        if ship:
            if ship.group(1) == "1":
                groups[key]['ship1'] += 1
            elif ship.group(1) == "2":
                groups[key]['ship2'] += 1
        groups[key]['n'] += 1

print("policy pk  runs threats raw_kills effective_kills leakers raw_Pk effective_Pk ship1 ship2 firm")
for (policy, pk), d in sorted(groups.items()):
    threats = d['threats']
    leakers = threats - d['effective']
    print(
        f"{policy:>6} {pk:>4} {d['n']:>5} {threats:>8} {d['killed']:>9} {d['effective']:>13} "
        f"{leakers:>7} {d['killed']/threats if threats else 0:>6.3f} {d['effective']/threats if threats else 0:>11.3f} "
        f"{d['ship1']:>6} {d['ship2']:>5} {d['firm']:>4}"
    )

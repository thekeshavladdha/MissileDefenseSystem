import glob
import os
import re

root = os.path.dirname(os.path.abspath(__file__))
for path in sorted(glob.glob(os.path.join(root, "MissileDefense_Outcome_p*_pk*.txt"))):
    name = os.path.basename(path)
    meta = re.search(r"p(\d+)_pk(\d+)", name)
    policy = meta.group(1) if meta else "?"
    pktag = meta.group(2) if meta else "?"
    text = open(path, encoding="utf-8", errors="replace").read()
    blocks = re.split(r"DISPLAY AT TIME", text)
    threats = killed = effective = firm = ship1 = ship2 = 0
    for block in blocks:
        ident = re.search(r"\bID\s*=\s*(\d+)", block)
        kill = re.search(r"\bKilled\s*=\s*(true|false)", block)
        eff = re.search(r"\bEffective_Kill\s*=\s*(true|false)", block)
        firm_track = re.search(r"\bFirm_Track\s*=\s*(true|false)", block)
        ship = re.search(r"\bship\s*=\s*(\d+)", block)
        if not (ident and kill and eff):
            continue
        threats += 1
        killed += kill.group(1) == "true"
        effective += eff.group(1) == "true"
        firm += bool(firm_track) and firm_track.group(1) == "true"
        if ship:
            if ship.group(1) == "1":
                ship1 += 1
            elif ship.group(1) == "2":
                ship2 += 1
    leakers = threats - effective
    print(
        f"{name}: policy_mode={policy} pk_tag={pktag} threats={threats} "
        f"raw_kills={killed} effective_kills={effective} leakers={leakers} "
        f"firm_tracks={firm} ship1={ship1} ship2={ship2} raw_Pk={killed/threats if threats else 0:.3f} "
        f"effective_Pk={effective/threats if threats else 0:.3f}"
    )

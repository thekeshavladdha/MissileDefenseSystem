import glob
import os
import re

root = os.path.dirname(os.path.abspath(__file__))  # portable: same folder as this script on any laptop
for path in sorted(glob.glob(os.path.join(root, "MissileDefense_Outcome_run*.txt"))):
    text = open(path, encoding="utf-8", errors="replace").read()
    blocks = re.split(r"DISPLAY AT TIME", text)
    threats = killed = effective = firm = 0
    for block in blocks:
        ident = re.search(r"\bID\s*=\s*(\d+)", block)
        kill = re.search(r"\bKilled\s*=\s*(true|false)", block)
        eff = re.search(r"\bEffective_Kill\s*=\s*(true|false)", block)
        firm_track = re.search(r"\bFirm_Track\s*=\s*(true|false)", block)
        if not (ident and kill and eff):
            continue
        threats += 1
        killed += kill.group(1) == "true"
        effective += eff.group(1) == "true"
        firm += bool(firm_track) and firm_track.group(1) == "true"
    leakers = threats - effective
    print(
        f"{os.path.basename(path)}: threats={threats} "
        f"raw_kills={killed} effective_kills={effective} leakers={leakers} "
        f"firm_tracks={firm} raw_Pk={killed/threats if threats else 0:.3f} "
        f"effective_Pk={effective/threats if threats else 0:.3f}"
    )

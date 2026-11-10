"""90-run Policy x Pk x seeds experiment - portable, terminal-first.

Resolves the VisualSim install and JDK portably (no hardcoded user paths):
  1. command-line flags  --vs-ar / --java / --outdir  (highest priority)
  2. environment variables  VS_AR / JAVA_HOME
  3. <script-dir>/VS_AR  and  JAVA_HOME/bin/java(.exe)  (lowest priority)

Outcome files still land in --outdir (default: this script's folder) because
VisualSimBatchModeSimulator must write Display logs somewhere, but every
run's RESULT is also parsed and printed to the terminal immediately, plus a
final aggregate table - so you never need to open the files by hand.

Usage:
  python run_full_policy_experiment.py [--vs-ar PATH] [--java PATH]
      [--outdir DIR] [--policies 0,2] [--pks 0.8] [--seeds 2001,2002]
      [--dry-run]

  --dry-run prints what WOULD run (and the terminal summary format) without
  needing VisualSim or a license. Use it to verify paths on a new laptop.
"""
import argparse
import glob
import os
import re
import subprocess
import sys
from itertools import product

HERE = os.path.dirname(os.path.abspath(__file__))


def resolve_paths(vs_ar_arg, java_arg):
    vs_ar = (vs_ar_arg
             or os.environ.get("VS_AR")
             or os.path.join(HERE, "VS_AR"))
    java_home = os.environ.get("JAVA_HOME", "")
    java_candidates = [
        java_arg,
        os.path.join(java_home, "bin", "java.exe") if java_home else None,
        os.path.join(java_home, "bin", "java") if java_home else None,
    ]
    java = next((c for c in java_candidates if c), None)
    return vs_ar, java


def check_install(vs_ar, java):
    problems = []
    if not (vs_ar and os.path.isdir(vs_ar)):
        problems.append(f"VS_AR not found: {vs_ar!r} "
                        "(pass --vs-ar PATH or set env VS_AR)")
    policy = os.path.join(vs_ar, "bin", "policyAll") if vs_ar else ""
    if not (policy and os.path.isfile(policy)):
        problems.append(f"policyAll not found under VS_AR: {policy!r}")
    if not (java and os.path.isfile(java)):
        problems.append(f"java executable not found: {java!r} "
                        "(pass --java PATH or set env JAVA_HOME)")
    model = os.path.join(HERE, "MissileDefense_Model.xml")
    if not os.path.isfile(model):
        problems.append(f"model not found: {model!r}")
    for csv in ("fes_table.csv", "magazine.csv"):
        if not os.path.isfile(os.path.join(HERE, csv)):
            problems.append(f"required table missing next to script: {csv}")
    return problems


def summarize_outcome_file(path):
    """Parse one DefenseOutcome log -> dict. Same last-wins dedupe as the
    full scorer so the terminal line matches the aggregate table."""
    text = open(path, encoding="utf-8", errors="replace").read()
    blocks = re.split(r"DISPLAY AT TIME", text)
    by_id = {}
    order = []
    for block in blocks:
        if not re.search(r"------\s*[\d\.]+\s*sec", block):
            continue
        ident = re.search(r"\bID\s*=\s*(\d+)", block)
        kill = re.search(r"\bKilled\s*=\s*(true|false)", block)
        eff = re.search(r"\bEffective_Kill\s*=\s*(true|false)", block)
        ship = re.search(r"\bship\s*=\s*(\d+)", block)
        shots = re.search(r"\bShots_Fired\s*=\s*(\d+)", block)
        if not (ident and kill and eff):
            continue
        if ident.group(1) not in by_id:
            order.append(ident.group(1))
        by_id[ident.group(1)] = {
            "killed": kill.group(1) == "true",
            "effective": eff.group(1) == "true",
            "ship": ship.group(1) if ship else "?",
            "shots": int(shots.group(1)) if shots else 0,
        }
    threats = len(order)
    killed = sum(1 for i in order if by_id[i]["killed"])
    effective = sum(1 for i in order if by_id[i]["effective"])
    ship1 = sum(1 for i in order if by_id[i]["ship"] == "1")
    ship2 = sum(1 for i in order if by_id[i]["ship"] == "2")
    shots = sum(by_id[i]["shots"] for i in order)
    # distinct re-engaged IDs (seen more than once in this file)
    seen = {}
    for b in blocks:
        m = re.search(r"\bID\s*=\s*(\d+)", b)
        if m:
            seen[m.group(1)] = seen.get(m.group(1), 0) + 1
    reengaged = sum(1 for v in seen.values() if v > 1)
    return {"threats": threats, "killed": killed, "effective": effective,
            "leakers": threats - effective, "ship1": ship1, "ship2": ship2,
            "shots": shots, "reengaged": reengaged}


def fmt(mode, pk, seed, s):
    t = s["threats"]
    return (f"policy={mode} pk={pk} seed={seed}: threats={t} "
            f"raw={s['killed']} effective={s['effective']} leakers={s['leakers']} "
            f"raw_Pk={s['killed']/t if t else 0:.3f} "
            f"effective_Pk={s['effective']/t if t else 0:.3f} "
            f"ship1={s['ship1']} ship2={s['ship2']} "
            f"shots={s['shots']} reengaged={s['reengaged']}")


def parse_csv_list(s, cast):
    return [cast(x) for x in s.split(",") if x.strip()]


def main():
    ap = argparse.ArgumentParser(description="90-run Policy x Pk x seeds experiment (terminal-first).")
    ap.add_argument("--vs-ar", default=None, help="VisualSim install dir (else env VS_AR)")
    ap.add_argument("--java", default=None, help="java executable (else env JAVA_HOME/bin/java)")
    ap.add_argument("--outdir", default=HERE, help="where outcome .txt files land (default: script folder)")
    ap.add_argument("--policies", default="0,1,2", help="e.g. 0,2")
    ap.add_argument("--pks", default="0.5,0.8,0.95", help="e.g. 0.8")
    ap.add_argument("--seeds", default=None, help="e.g. 2001,2002 (default: 2001-2010)")
    ap.add_argument("--dry-run", action="store_true", help="print plan only; run nothing")
    args = ap.parse_args()

    vs_ar, java = resolve_paths(args.vs_ar, args.java)
    policies = parse_csv_list(args.policies, int)
    pks = parse_csv_list(args.pks, float)
    seeds = parse_csv_list(args.seeds, int) if args.seeds else list(range(2001, 2011))
    total = len(policies) * len(pks) * len(seeds)
    outdir = os.path.abspath(args.outdir)
    os.makedirs(outdir, exist_ok=True)

    class_path = os.pathsep.join([
        vs_ar,
        os.path.join(vs_ar, "com", "amity", "flexlm", "flexlm.jar"),
        os.path.join(vs_ar, "com", "amity", "flexlm", "EccpressoAll.jar"),
        os.path.join(vs_ar, "com", "amity", "flexlm", "flexlmutil.jar"),
    ])
    model = os.path.join(HERE, "MissileDefense_Model.xml")
    java_flags = [
        "-Dvs.lic=default",
        f"-Djava.security.policy={os.path.join(vs_ar, 'bin', 'policyAll')}",
        "-Djava.security.manager=allow",
        "--add-opens",
        "java.desktop/sun.font=ALL-UNNAMED",
        "-classpath",
        class_path,
        "VisualSim.actor.gui.VisualSimBatchModeSimulator",
    ]

    print(f"VS_AR={vs_ar}", flush=True)
    print(f"java={java}", flush=True)
    print(f"outdir={outdir}  runs={total} "
          f"(policies={policies} pks={pks} seeds={seeds[0]}-{seeds[-1]})", flush=True)
    problems = check_install(vs_ar, java)
    if problems and not args.dry_run:
        print("BLOCKED - fix these first:", flush=True)
        for p in problems:
            print(f"  - {p}", flush=True)
        sys.exit(2)
    if args.dry_run and problems:
        print("(dry-run: ignoring these problems)", flush=True)
        for p in problems:
            print(f"  - {p}", flush=True)

    run = 0
    agg = {}
    for mode, pk, seed in product(policies, pks, seeds):
        run += 1
        fn = f"MissileDefense_Outcome_p{mode}_pk{str(pk).replace('.', '')}_s{seed}.txt"
        full = os.path.join(outdir, fn)
        cmd = [java] + java_flags + [
            "-run", str(run),
            "-resultpath", outdir,
            "-Execution_Time", "2.5",
            "-Input_Rate", "1.0",
            "-Modelseed", f"seed({seed})",
            "-Policy_Mode", str(mode),
            "-Pk", str(pk),
            "-Intercept_Deadline", "4.0",
            "-DefenseOutcome.fileName", fn,
            model,
        ]
        if args.dry_run:
            print(f"[{run:02d}/{total}] DRY policy={mode} pk={pk} seed={seed} -> {fn}", flush=True)
            continue
        print(f"[{run:02d}/{total}] running policy={mode} pk={pk} seed={seed} ...", flush=True)
        subprocess.run(cmd, cwd=HERE, stdout=subprocess.DEVNULL,
                       stderr=subprocess.DEVNULL, check=False)
        if os.path.isfile(full):
            s = summarize_outcome_file(full)
            print(f"[{run:02d}/{total}] " + fmt(mode, pk, seed, s), flush=True)
            key = (mode, pk)
            d = agg.setdefault(key, {"n": 0, "threats": 0, "killed": 0,
                                     "effective": 0, "ship1": 0, "ship2": 0,
                                     "shots": 0, "reengaged": 0})
            d["n"] += 1
            for k in ("threats", "killed", "effective", "ship1", "ship2", "shots", "reengaged"):
                d[k] += s[k]
        else:
            print(f"[{run:02d}/{total}] policy={mode} pk={pk} seed={seed}: "
                  f"NO OUTPUT FILE ({fn}) - run failed, check license/paths", flush=True)

    if args.dry_run:
        print(f"Dry run complete: {total} commands would execute. "
              "Rerun without --dry-run with a valid license.", flush=True)
        return
    print("\nAggregate (summed over seeds; run summarize_full_policy_experiment.py for the full table):", flush=True)
    print("policy pk    runs threats raw effective leakers raw_Pk eff_Pk ship1 ship2 shots reeng", flush=True)
    for (mode, pk) in sorted(agg):
        d = agg[(mode, pk)]
        t = d["threats"]
        print(f"{mode:>6} {pk:<5} {d['n']:>4} {t:>7} {d['killed']:>3} {d['effective']:>9} "
              f"{t - d['effective']:>7} {d['killed']/t if t else 0:>6.3f} "
              f"{d['effective']/t if t else 0:>6.3f} {d['ship1']:>5} {d['ship2']:>5} "
              f"{d['shots']:>5} {d['reengaged']:>6}", flush=True)
    print("Done.", flush=True)


if __name__ == "__main__":
    main()

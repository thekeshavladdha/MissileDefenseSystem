import os
import subprocess
import sys
from itertools import product

HERE = os.path.dirname(os.path.abspath(__file__))
VS_AR = r"C:\Users\satvi\Desktop\VisualSim\VS_AR"
JAVA = r"C:\Program Files\Java\jdk-17\bin\java.exe"
CLASS_PATH = os.pathsep.join([
    VS_AR,
    os.path.join(VS_AR, "com", "amity", "flexlm", "flexlm.jar"),
    os.path.join(VS_AR, "com", "amity", "flexlm", "EccpressoAll.jar"),
    os.path.join(VS_AR, "com", "amity", "flexlm", "flexlmutil.jar"),
])
MODEL = os.path.join(HERE, "MissileDefense_Model.xml")
OUT = HERE
JAVA_FLAGS = [
    "-Dvs.lic=default",
    f"-Djava.security.policy={os.path.join(VS_AR, 'bin', 'policyAll')}",
    "-Djava.security.manager=allow",
    "--add-opens",
    "java.desktop/sun.font=ALL-UNNAMED",
    "-classpath",
    CLASS_PATH,
    "VisualSim.actor.gui.VisualSimBatchModeSimulator",
]

policies = [0, 1, 2]
pks = [0.5, 0.8, 0.95]
seeds = list(range(2001, 2011))
run = 0
for mode, pk, seed in product(policies, pks, seeds):
    run += 1
    seed_arg = f"seed({seed})"
    fn = os.path.join(OUT, f"MissileDefense_Outcome_p{mode}_pk{str(pk).replace('.', '')}_s{seed}.txt")
    args = JAVA_FLAGS + [
        "-run", str(run),
        "-resultpath", OUT,
        "-Execution_Time", "2.5",
        "-Input_Rate", "1.0",
        "-Modelseed", seed_arg,
        "-Policy_Mode", str(mode),
        "-Pk", str(pk),
        "-Intercept_Deadline", "4.0",
        "-DefenseOutcome.fileName", os.path.basename(fn),
        MODEL,
    ]
    print(f"[{run:02d}/90] Policy_Mode={mode} Pk={pk} seed={seed} -> {os.path.basename(fn)}", flush=True)
    subprocess.run([JAVA] + args, cwd=HERE, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=False)
print("Done.", flush=True)

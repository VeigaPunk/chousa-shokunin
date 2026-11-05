"""DECISIVE: run the frozen battery with the LEGIT MATRIX ITSELF re-emitted.

F05 (forge-harness-source.py) detects forgery by (a) finding the matrix program by
FILE NAME in the parent's cmdline and (b) reading the matrix's module-level table
through the STRING key "CASES".  Re-emitting the matrix destroys both couplings.
Measure what the battery then says about F05."""
import importlib.util, pathlib, shutil, subprocess, sys

BAT = "/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round79/matrix-battery-v6.py"
LEGIT = "/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round76/loader-matrix-v3.py"
spec = importlib.util.spec_from_file_location("battery_under_check", BAT)
bat = importlib.util.module_from_spec(spec); spec.loader.exec_module(bat)
work = pathlib.Path(sys.argv[1]); work.mkdir(parents=True, exist_ok=True)

legit = pathlib.Path(LEGIT)
copy = bat.reemit(legit, work)
print("legit matrix     :", legit)
print("re-emitted matrix:", copy)
for label, m in (("COMMITTED-MATRIX", legit), ("RE-EMITTED-MATRIX", copy)):
    w = work / ("run-" + label)
    r = subprocess.run([sys.executable, "-B", BAT, "--matrix", str(m), "--work", str(w),
                        "--runs", "1"], capture_output=True, text=True, timeout=600)
    lines = [l for l in r.stdout.splitlines()
             if "harness-source" in l or l.startswith("BATTERY=")]
    print(f"--- {label}: battery exit={r.returncode}")
    for l in lines:
        print("   ", l)
shutil.rmtree(copy.parent, ignore_errors=True)

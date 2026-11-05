"""DECISIVE, FULL OUTPUT: run the frozen battery twice -- once with the committed
legitimate matrix, once with the SAME matrix re-emitted -- and extract the per-CASE
lines the matrix recorded for the harness-source forger.  The CASE lines carry
actual_rc and failed, i.e. the forger's OWN answers, so they show whether F05
found the matrix (replayed its CASES) or degenerated into 'always PASS'."""
import importlib.util, pathlib, re, shutil, subprocess, sys

BAT = "/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round79/matrix-battery-v6.py"
LEGIT = "/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round76/loader-matrix-v3.py"
spec = importlib.util.spec_from_file_location("battery_under_check", BAT)
bat = importlib.util.module_from_spec(spec); spec.loader.exec_module(bat)
work = pathlib.Path(sys.argv[1]); work.mkdir(parents=True, exist_ok=True)
legit = pathlib.Path(LEGIT)
copy = bat.reemit(legit, work)

for label, m in (("COMMITTED-MATRIX", legit), ("RE-EMITTED-MATRIX", copy)):
    w = work / ("run-" + label)
    r = subprocess.run([sys.executable, "-B", BAT, "--matrix", str(m), "--work", str(w),
                        "--runs", "1"], capture_output=True, text=True, timeout=900)
    out = r.stdout
    print(f"=== {label}: battery exit={r.returncode}")
    for l in out.splitlines():
        if l.startswith("BATTERY=") or ("harness-source" in l and "RUN" in l):
            print("  ", l)
    # the CASE lines the matrix printed while the harness-source forger was the
    # counter: the matrix prints them with expected_rc/actual_rc/failed.
    case_lines = [l for l in out.splitlines() if l.startswith("CASE ")]
    print(f"   total CASE lines in receipt: {len(case_lines)}")
    ar = sorted({re.search(r"actual_rc=(-?\d+)", l).group(1) for l in case_lines})
    fl = sorted({re.search(r"failed=(\S+)", l).group(1) for l in case_lines})
    print(f"   distinct actual_rc across CASE lines: {ar}")
    print(f"   distinct failed values across CASE lines: {fl}")
shutil.rmtree(copy.parent, ignore_errors=True)

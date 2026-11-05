"""F05's OWN answers under each matrix: run the matrix directly with F05 as the
counter and read the CASE lines (which carry actual_rc and failed = F05's answer)."""
import importlib.util, pathlib, re, shutil, subprocess, sys

BAT = "/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round79/matrix-battery-v6.py"
LEGIT = "/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round76/loader-matrix-v3.py"
F05 = "/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round76/forgers/forge-harness-source.py"
spec = importlib.util.spec_from_file_location("battery_under_check", BAT)
bat = importlib.util.module_from_spec(spec); spec.loader.exec_module(bat)
work = pathlib.Path(sys.argv[1]); work.mkdir(parents=True, exist_ok=True)
legit = pathlib.Path(LEGIT)
copy = bat.reemit(legit, work)
f05 = pathlib.Path(F05)

for label, m in (("COMMITTED-MATRIX", legit), ("RE-EMITTED-MATRIX", copy)):
    w = work / ("w-" + label)
    w.mkdir(parents=True, exist_ok=True)
    r = subprocess.run([sys.executable, "-B", str(m), "--counter", str(f05),
                        "--work", str(w)], capture_output=True, text=True, timeout=300)
    cases = [l for l in r.stdout.splitlines() if l.startswith("CASE ")]
    print(f"=== {label} (matrix file name = {m.name!r})")
    print(f"    matrix exit={r.returncode}  CASE lines={len(cases)}")
    for l in cases:
        d = dict(kv.split("=", 1) for kv in l.split()[3:] if "=" in kv)
        print(f"    {l.split()[1]:22s} actual_rc={d.get('actual_rc'):>3s} "
              f"failed={d.get('failed'):<14s} expected_failed={d.get('expected_failed')}")
shutil.rmtree(copy.parent, ignore_errors=True)

"""Does re-emission relocate the ORACLE's state file, and does that bypass its own
refuse_inside_worktree() guard (a round-77 lane-write safety property)?"""
import importlib.util, pathlib, shutil, subprocess, sys
BAT = "/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round79/matrix-battery-v6.py"
ORACLE = "/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round79/forgers/forge-order-matrix.py"
spec = importlib.util.spec_from_file_location("battery_under_check", BAT)
bat = importlib.util.module_from_spec(spec); spec.loader.exec_module(bat)
work = pathlib.Path(sys.argv[1]); work.mkdir(parents=True, exist_ok=True)
src = pathlib.Path(ORACLE)
copy = bat.reemit(src, work)
for label, target in (("COMMITTED", src), ("RE-EMITTED", copy)):
    before = set(p.name for p in target.parent.glob("*.state"))
    r = subprocess.run([sys.executable, "-B", str(target), "--counter", "x", "--work", str(work)],
                       capture_output=True, text=True, timeout=60)
    after = set(p.name for p in target.parent.glob("*.state"))
    print(f"  {label}: rc={r.returncode} state files created in {target.parent.name}/: "
          f"{sorted(after - before)}")
    print(f"     stdout={r.stdout.strip()[:70]!r} stderr={(r.stderr.strip().splitlines() or [''])[-1][:90]!r}")
shutil.rmtree(copy.parent, ignore_errors=True)

"""Empirical hazard probe: does matrix-battery-v6.py's re-emission preserve behaviour
for each string-keyed construct class? Uses the FROZEN battery's own reemit()."""
import importlib.util, pathlib, subprocess, sys, shutil

BAT = "/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round79/matrix-battery-v6.py"
spec = importlib.util.spec_from_file_location("battery_under_check", BAT)
bat = importlib.util.module_from_spec(spec)
spec.loader.exec_module(bat)

haz = pathlib.Path(sys.argv[1])
work = pathlib.Path(sys.argv[2])
work.mkdir(parents=True, exist_ok=True)

def run(path):
    p = subprocess.run([sys.executable, "-B", str(path)], capture_output=True, text=True, timeout=30)
    return p.returncode, p.stdout.strip(), p.stderr.strip().splitlines()[-1] if p.stderr.strip() else ""

for src in sorted(haz.glob("*.py")):
    d = work / src.stem
    if d.exists():
        shutil.rmtree(d)
    copy = bat.reemit(src, work)
    r1 = run(src)
    r2 = run(copy)
    same = (r1[0] == r2[0]) and (r1[1] == r2[1])
    print(f"{'SAME  ' if same else 'DIFFER'} {src.name}")
    print(f"   original rc={r1[0]} out={r1[1]!r} err={r1[2]!r}")
    print(f"   copy     rc={r2[0]} out={r2[1]!r} err={r2[2]!r}")
    shutil.rmtree(copy.parent, ignore_errors=True)

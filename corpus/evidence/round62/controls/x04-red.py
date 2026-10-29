#!/usr/bin/env python3
"""Red-before for the X04 control mutant (round 62 Mistakes): the first pattern `if neutral:` -> `if False:` before `rfd, wfd = os.pipe()`
broke the instrument (rfd None, a TypeError in every neutral leg) instead of removing the closed-stdin feature, so the battery showed
LANDED=0/3 and the runner's must-accept-subset check printed `forgers_accepted=- expected=UNEXPECTED`. Usage: python3 x04-red.py --work DIR"""
import argparse, pathlib, shutil, subprocess, sys
HERE = pathlib.Path(__file__).resolve().parent
LANE = HERE.parents[3]
ap = argparse.ArgumentParser(); ap.add_argument("--work", required=True); a = ap.parse_args()
w = pathlib.Path(a.work); d = w / "m"
(d / "corpus/evidence/round62").mkdir(parents=True); (d / "tools").mkdir()
shutil.copyfile(LANE / "tools/capture-text.py", d / "tools/capture-text.py")
src = (HERE.parent / "c1v2-count.py").read_text()
old = "    if neutral:\n        rfd, wfd = os.pipe()"
assert src.count(old) == 1
c = d / "corpus/evidence/round62/c1v2-count.py"; c.write_text(src.replace(old, "    if False:\n        rfd, wfd = os.pipe()"))
r = subprocess.run([sys.executable, "-B", str(HERE.parent / "c1v2-battery.py"), "--counter", str(c), "--work", str(w / "b"), "--only", "LANDED"],
                   capture_output=True, text=True)
print(r.stdout.strip().splitlines()[-1], f"exit={r.returncode}")
shutil.rmtree(w, ignore_errors=True)

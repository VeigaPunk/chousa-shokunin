#!/usr/bin/env python3
"""build-c3-controls — score the round-51 C3 counter against three do-nothing controls in scratch roots
(never the lane); every one must print C3=FAIL:
  BLANKET  one generic `correction: all pointers resolve` line appended (names no row, pointer or path);
  DELETED  the capability rows and SHONEN lines that hold a dangling pointer removed;
  EMPTY    zero-byte files created at the dangling pointer names;
and one POSITIVE control (round 51, erratum E1): DOTPATH appends a capability row whose pointer is a real dot-leading path
(`.ufo/waves/round-51/gen-w1-spec.py`); the counter must still print C3=PASS (DANGLING unchanged), and the pre-erratum counter
(`git show d603f6f0:corpus/evidence/round51/c3-count.py`) must print that path as DANGLING — the class the first controls never seeded.
Usage: python3 corpus/evidence/round51/controls/build-c3-controls.py"""
import pathlib
import re
import shutil
import subprocess
import sys
import tempfile

LANE = pathlib.Path(__file__).resolve().parents[4]
COUNT = LANE / "corpus/evidence/round51/c3-count.py"


def score(root):
    p = subprocess.run([sys.executable, str(COUNT), "--root", str(root)], capture_output=True, text=True)
    return p.stdout + f"exit={p.returncode}\n", p.stdout


BASE = "9ec1751a24231e899ceea4688e21c8edf6046d35"


def base_file(name):
    return subprocess.run(["git", "-C", str(LANE), "show", f"{BASE}:{name}"], capture_output=True, text=True).stdout


def scratch(tip=False):
    r = pathlib.Path(tempfile.mkdtemp(prefix="chousa-r51-c3-"))
    for e in LANE.iterdir():              # the lane tree by symlink, except the two files and VCS state
        if e.name not in ("SCORECARD.md", "SHONEN.md", ".git", ".jj"):
            (r / e.name).symlink_to(e)
    for f in ("SCORECARD.md", "SHONEN.md"):
        if tip:
            shutil.copy(LANE / f, r / f)
        else:
            (r / f).write_text(base_file(f), encoding="utf-8")   # the controls start from the BASE self-assessment
    return r


out = []
_b = scratch()
_t, dang = score(_b)
shutil.rmtree(_b)
bad = [(m.group(1), int(m.group(2)), m.group(3)) for m in re.finditer(r"^DANGLING (\S+):(\d+) (\S+)$", dang, re.M)]
r = scratch()
with open(r / "SCORECARD.md", "a", encoding="utf-8") as f:
    f.write("\ncorrection: all pointers resolve\n")
out.append("# control BLANKET\n" + score(r)[0]); shutil.rmtree(r)
r = scratch()
for fname in ("SCORECARD.md", "SHONEN.md"):
    lines = (r / fname).read_text(encoding="utf-8").splitlines(keepends=True)
    drop = {ln for fn, ln, _p in bad if fn == fname}
    (r / fname).write_text("".join(l for i, l in enumerate(lines, 1) if i not in drop), encoding="utf-8")
out.append("# control DELETED\n" + score(r)[0]); shutil.rmtree(r)
r = scratch()
for _f, _l, ptr in bad:
    q = r / ptr
    if q.is_symlink() or any(x.is_symlink() for x in q.parents if x != r and r in x.parents):
        continue
    if ptr.endswith("/"):
        q.mkdir(parents=True, exist_ok=True)
    else:
        q.parent.mkdir(parents=True, exist_ok=True)
        q.write_bytes(b"")
out.append("# control EMPTY\n" + score(r)[0]); shutil.rmtree(r)
r = scratch(tip=True)
with open(r / "SCORECARD.md", "a", encoding="utf-8") as f:
    f.write("\n## Capabilities (control row)\n\n| Capability | What it can now do | Evidence pointer | First-working round |\n|---|---|---|---|\n"
            "| dot path | control | `.ufo/waves/round-51/gen-w1-spec.py` | 51 |\n")
out.append("# control DOTPATH (positive: C3=PASS expected, DANGLING must not grow)\n" + score(r)[0])
old = r / "c3-old.py"          # a real file in the scratch root (never through the lane symlink)
src = subprocess.run(["git", "-C", str(LANE), "show", "d603f6f00f78d64f123d3aed2dd9f8701547a4ba:corpus/evidence/round51/c3-count.py"], capture_output=True, text=True).stdout
old.write_text(src.replace("LANE = pathlib.Path(__file__).resolve().parents[3]", f'LANE = pathlib.Path("{LANE}")'), encoding="utf-8")
q = subprocess.run([sys.executable, str(old), "--root", str(r)], capture_output=True, text=True)
out.append("# control DOTPATH at the pre-erratum counter (red expected: the dot path prints DANGLING)\n" + q.stdout + q.stderr[-300:] + f"exit={q.returncode}\n")
shutil.rmtree(r)
print("\n".join(out))

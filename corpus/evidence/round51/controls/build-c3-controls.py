#!/usr/bin/env python3
"""build-c3-controls — score the round-51 C3 counter against three do-nothing controls in scratch roots
(never the lane); every one must print C3=FAIL:
  BLANKET  one generic `correction: all pointers resolve` line appended (names no row, pointer or path);
  DELETED  the capability rows and SHONEN lines that hold a dangling pointer removed;
  EMPTY    zero-byte files created at the dangling pointer names.
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


def scratch():
    r = pathlib.Path(tempfile.mkdtemp(prefix="chousa-r51-c3-"))
    for e in LANE.iterdir():              # the lane tree by symlink, except the two files and VCS state
        if e.name not in ("SCORECARD.md", "SHONEN.md", ".git", ".jj"):
            (r / e.name).symlink_to(e)
    for f in ("SCORECARD.md", "SHONEN.md"):
        shutil.copy(LANE / f, r / f)
    return r


out = []
_t, dang = score(LANE)
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
print("\n".join(out))

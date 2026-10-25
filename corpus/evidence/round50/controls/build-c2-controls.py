#!/usr/bin/env python3
"""build-c2-controls — score the round-50 C2 counter against two do-nothing
controls in scratch roots (never the lane):
  STAGED  the three staged entries copied unchanged beside the lane registry;
  TOOLED  the entries rewritten by tools/assimilate-rows.py plus its append
          block inserted into the registry (mechanical renumbering, no quote,
          no span, no lesson, no re-grounding).
Both must print C2=FAIL. Usage: python3 corpus/evidence/round50/controls/build-c2-controls.py"""
import pathlib
import re
import shutil
import subprocess
import sys
import tempfile

LANE = pathlib.Path(__file__).resolve().parents[4]
PKG = pathlib.Path("/home/vgpnk/Projects/shokuknow/merge/chousa")
ENTRIES = ["corpus/knowledge/cnki-citation-check-r40.md", "corpus/knowledge/citation-matching-semantics-r41.md",
           "corpus/knowledge/istic-citation-verification-r39.md"]
BASE = "3c51da77b3696ed884c943548ec4b4006e3ca528"


def counter(root: pathlib.Path) -> str:
    p = subprocess.run([sys.executable, str(LANE / "corpus/evidence/round50/c2-count.py"), "--root", str(root)],
                       capture_output=True, text=True)
    return p.stdout + f"exit={p.returncode}\n"


def scratch(tag: str) -> pathlib.Path:
    r = pathlib.Path(tempfile.mkdtemp(prefix=f"chousa-r50-{tag}-"))
    (r / "corpus/knowledge").mkdir(parents=True)
    (r / "corpus/evidence").mkdir(parents=True)
    (r / "corpus/lessons").mkdir(parents=True)
    shutil.copytree(LANE / "corpus/evidence/round50", r / "corpus/evidence/round50", ignore=shutil.ignore_patterns("controls", "c1-fixtures"))
    shutil.copytree(LANE / "tools", r / "tools", ignore=shutil.ignore_patterns("__pycache__"))
    base = subprocess.run(["git", "-C", str(LANE), "show", f"{BASE}:corpus/SOURCES.md"], capture_output=True, text=True).stdout
    (r / "corpus/SOURCES.md").write_text(base, encoding="utf-8")
    return r


out = []
r = scratch("staged")
for e in ENTRIES:
    shutil.copy(PKG / "knowledge" / e, r / e)
out.append("# control STAGED: the three staged entries copied unchanged beside the base registry\n" + counter(r))
shutil.rmtree(r)

r = scratch("tooled")
o = r / "adopt"
subprocess.run([sys.executable, str(LANE / "tools/assimilate-rows.py"), "--staged", str(PKG / "SOURCES.append.md"),
                "--knowledge", str(PKG / "knowledge"), "--registry", str(r / "corpus/SOURCES.md"), "--opened", "2026-10-25",
                "--out", str(o)] + sum([["--entry", e] for e in ENTRIES], []), capture_output=True, text=True, check=True)
for e in ENTRIES:
    shutil.copy(o / e, r / e)
reg = (r / "corpus/SOURCES.md").read_text(encoding="utf-8").splitlines(keepends=True)
last = max(i for i, l in enumerate(reg) if re.match(r"^ {0,3}\|[ \t]*S\d{3,}[ \t]*\|", l))
reg[last + 1:last + 1] = (o / "append.md").read_text(encoding="utf-8").splitlines(keepends=True)
(r / "corpus/SOURCES.md").write_text("".join(reg), encoding="utf-8")
out.append("# control TOOLED: tool-rewritten entries + its append block, no quotes, spans or lesson\n" + counter(r))
shutil.rmtree(r)
print("\n".join(out))

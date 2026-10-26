#!/usr/bin/env python3
"""build-c2-controls — score the round-53 C2 counter against two do-nothing
controls in scratch roots under $TMPDIR (never the lane):
  STAGED  the three staged entries copied unchanged to the lane entry paths
          beside the base registry;
  TOOLED  the entries rewritten by tools/assimilate-rows.py (default
          `--cites source`) plus its append block inserted into the registry
          (mechanical renumbering, no quote, no span, no lesson, no re-grounding).
Both must print C2=FAIL.
Usage: python3 corpus/evidence/round53/controls/build-c2-controls.py"""
import pathlib
import re
import shutil
import subprocess
import sys
import tempfile

LANE = pathlib.Path(__file__).resolve().parents[4]
PKG = pathlib.Path("/home/vgpnk/Projects/shokuknow/merge/chousa")
STAGED = {  # staged entry (under PKG/knowledge) -> lane entry path (same names)
    "corpus/knowledge/search-tracking-record-r40.md": "corpus/knowledge/search-tracking-record-r40.md",
    "corpus/knowledge/western-instrument-alignment-r50.md": "corpus/knowledge/western-instrument-alignment-r50.md",
    "corpus/knowledge/quality-control-guideline-issued-text-r48.md": "corpus/knowledge/quality-control-guideline-issued-text-r48.md",
}
BASE = "5b550133d79bc09c82d8965cce2e48c2598b8c3e"


def counter(root: pathlib.Path) -> str:
    p = subprocess.run([sys.executable, str(LANE / "corpus/evidence/round53/c2-count.py"), "--root", str(root)],
                       capture_output=True, text=True)
    return p.stdout + p.stderr + f"exit={p.returncode}\n"


def scratch(tag: str) -> pathlib.Path:
    r = pathlib.Path(tempfile.mkdtemp(prefix=f"chousa-r53-c2ctl-{tag}-"))
    for d in ("corpus/knowledge", "corpus/evidence", "corpus/lessons"):
        (r / d).mkdir(parents=True)
    shutil.copytree(LANE / "corpus/evidence/round53", r / "corpus/evidence/round53",
                    ignore=shutil.ignore_patterns("controls", "spans", "spans.tsv", "quotes.tsv", "*.txt"))
    shutil.copytree(LANE / "tools", r / "tools", ignore=shutil.ignore_patterns("__pycache__"))
    base = subprocess.run(["git", "-C", str(LANE), "show", f"{BASE}:corpus/SOURCES.md"],
                          capture_output=True, text=True, check=True).stdout
    (r / "corpus/SOURCES.md").write_text(base, encoding="utf-8")
    return r


out = []
r = scratch("staged")
for src, dst in STAGED.items():
    shutil.copy(PKG / "knowledge" / src, r / dst)
out.append("# control STAGED: the three staged entries copied unchanged beside the base registry\n" + counter(r))
shutil.rmtree(r)

r = scratch("tooled")
o = r / "adopt"
p = subprocess.run([sys.executable, str(LANE / "tools/assimilate-rows.py"), "--staged", str(PKG / "SOURCES.append.md"),
                    "--knowledge", str(PKG / "knowledge"), "--registry", str(r / "corpus/SOURCES.md"),
                    "--opened", "2026-10-26", "--out", str(o)] + sum([["--entry", e] for e in STAGED], []),
                   capture_output=True, text=True)
out.append(f"# adopter run for TOOLED: exit={p.returncode}\n{p.stdout}{p.stderr}")
if p.returncode == 0:
    for src, dst in STAGED.items():
        shutil.copy(o / src, r / dst)
    reg = (r / "corpus/SOURCES.md").read_text(encoding="utf-8").splitlines(keepends=True)
    last = max(i for i, l in enumerate(reg) if re.match(r"^ {0,3}\|[ \t]*S\d{3,}[ \t]*\|", l))
    reg[last + 1:last + 1] = (o / "append.md").read_text(encoding="utf-8").splitlines(keepends=True)
    (r / "corpus/SOURCES.md").write_text("".join(reg), encoding="utf-8")
    out.append("# control TOOLED: tool-rewritten entries + its append block, no quotes, spans or lesson\n" + counter(r))
shutil.rmtree(r)
print("\n".join(out))

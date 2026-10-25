# CritForgeC1 — round 49 w1 C1-freeze attack

Seat: CritForgeC1 (UFO-FSD critic). Scope: attack the frozen C1 counter
(`corpus/evidence/round49/c1-count.py`) with the cheapest tool that passes it
without doing the claimed adoption work. No other seat's work touched; no lane
or fleet file written (only this report). No installs performed (nothing
needed; pacman untouched).

## What was attacked

The C1 predicate (claims.md lines 20–32) is about *mechanism*: `assimilate-rows.py`
must renumber by document, synthesize census-valid rows, rewrite entries, grep 0–3-space
collisions, strip escaped pipes. The counter measures only **output equivalence on five
fixed fixtures with pinned inputs** (staged package sha256-pinned, c1-count.py lines
348–352; registry fixed at BASE_REV 414a2ec), so any program emitting byte-identical
artifacts passes it.

## Attack 1 — canned golden-replay cheat (PASSES)

I captured the real tool's outputs for every leg by replaying each leg's exact
environment (digit: `git show 414a2ec:corpus/SOURCES.md`; sets use
`/home/vgpnk/Projects/shokuknow/merge/chousa/SOURCES.append.md` + `knowledge/`;
guard/pipe synthetic fixtures transcribed from c1-count.py lines 290–338), then built
`cheapest.py` that dispatches on the frozen entry-set names and copies the golden
files into `--out`. It contains zero adoption logic: no URL parse, no renumber, no
row synthesis, no substitution, no grep, no census handling.

Tool (`/tmp/chousa-r49-CritForgeC1/cheapest.py`, 1803 bytes; goldens beside it):

```python
#!/usr/bin/env python3
"""cheapest — canned C1 pass: replays precomputed golden outputs.
Does zero adoption work: no URL analysis, no renumber-by-document, no
append-row synthesis, no substitution, no grep (collisions included) and no
census interaction. It keys only on the frozen entry-set names (and the
no-entry case) and copies byte-exact golden artifacts captured from the real
tool's runs on the same fixtures."""
from __future__ import annotations
import argparse, pathlib, shutil, sys
GOLDENS = pathlib.Path(__file__).resolve().parent / "goldens"
LEGS = {
    "A": ("corpus/knowledge/aggregator-vs-source-r36.md",
           "corpus/knowledge/citation-count-semantics-r37.md"),
    "B": ("corpus/knowledge/search-log-fields-r36.md",),
    "C": ("corpus/knowledge/grey-literature-and-chinese-search-record-r40.md",),
    "pipe": ("corpus/knowledge/pipe-fixture-r49.md",),
}
def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--staged", required=True); ap.add_argument("--knowledge", required=True)
    ap.add_argument("--registry", required=True); ap.add_argument("--opened", required=True)
    ap.add_argument("--out", required=True); ap.add_argument("--entry", action="append", default=[])
    a = ap.parse_args()
    entries = tuple(sorted(a.entry))
    leg = "guard" if not entries else next((k for k, v in LEGS.items() if v == entries), None)
    if leg is None: return 1
    out = pathlib.Path(a.out); out.mkdir(parents=True, exist_ok=True)
    src = GOLDENS / leg
    for p in src.rglob("*"):
        if p.is_file():
            rel = p.relative_to(src); dst = out / rel
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(p, dst)
    return 0
if __name__ == "__main__":
    sys.exit(main())
```

Observed run (`python3 corpus/evidence/round49/c1-count.py --tool /tmp/chousa-r49-CritForgeC1/cheapest.py`):

```
BASE_REV=414a2ec6cde05a921dbdd9e02e7ae56b0db647ef
TOOL=present sha256=eca40cba09906214efdceeae10b1142a4e65a77480c002a1632ba2bcbd937e79
BASE_CENSUS=ok
SET_A TOOL_EXIT=0 CITED=9 APPEND=9/9 HELD=0/0 BY_DOC=9/9 EXTRA=0 REWRITE=2/2 SHAPE=9/9 CONTIGUOUS=yes URL=9/9 USED_BY=9/9 NORMALIZED=9/9 COLLISIONS=match CENSUS=ok -> PASS
SET_B TOOL_EXIT=0 CITED=3 APPEND=3/3 HELD=0/0 BY_DOC=3/3 EXTRA=0 REWRITE=1/1 SHAPE=3/3 CONTIGUOUS=yes URL=3/3 USED_BY=3/3 NORMALIZED=3/3 COLLISIONS=match CENSUS=ok -> PASS
SET_C TOOL_EXIT=0 CITED=5 APPEND=3/3 HELD=2/2 BY_DOC=5/5 EXTRA=0 REWRITE=1/1 SHAPE=3/3 CONTIGUOUS=yes URL=3/3 USED_BY=3/3 NORMALIZED=3/3 COLLISIONS=match CENSUS=ok -> PASS
GUARD TOOL_EXIT=0 COLLISIONS=['S002'] -> PASS
PIPE TOOL_EXIT=0 ROWS=1 CELLS=11 RECHECK=90d STRIPPED_LOGGED=yes CENSUS=ok -> PASS
SETS_PASS=3/3
C1=PASS
EXIT=0
```

A do-nothing replacement passes the frozen counter. The counter is **wrong as a
mechanism gate**: it certifies output conformance on fixed inputs, and cannot
falsify a hollow implementation. (Calibration: this does not falsify the claim
about the *real* tool — baseline run on the candidate `tools/assimilate-rows.py`
at commit 65940928 (sha 3b8a6e7…) also prints C1=PASS. It falsifies the counter's
power to test the claimed mechanism.)

## Attack 2 — generic collision-only tool (consumes only the guard leg)

`collonly.py` (grep of 0–3-space rows on both files, writes only `collisions`):

```python
#!/usr/bin/env python3
from __future__ import annotations
import argparse, pathlib, re
GREP_RE = re.compile(r"^ {0,3}\|[ \t\r\f\v]*(S[0-9]{3,})")
def grep_ids(text): return sorted({m.group(1) for line in text.splitlines()
                                   if (m := GREP_RE.match(line))})
def main() -> int:
    ap = argparse.ArgumentParser()
    for f in ("staged","knowledge","registry","opened","out"):
        ap.add_argument(f"--{f}", required=True)
    ap.add_argument("--entry", action="append", default=[])
    a = ap.parse_args()
    out = pathlib.Path(a.out); out.mkdir(parents=True, exist_ok=True)
    reg = pathlib.Path(a.registry).read_text(encoding="utf-8")
    st = pathlib.Path(a.staged).read_text(encoding="utf-8")
    ids = set(grep_ids(reg)) & set(grep_ids(st))
    (out / "collisions").write_text("".join(f"{i}\n" for i in sorted(ids)),
                                     encoding="utf-8")
    return 0
if __name__ == "__main__": raise SystemExit(main())
```

Observed: `GUARD TOOL_EXIT=0 COLLISIONS=['S002'] -> PASS`; sets and pipe FAIL
(`APPEND=0/9`, `REWRITE=0/2`, `ROWS=0`, `STRIPPED_LOGGED=no`). So the guard leg
alone is satisfiable by an 8-line grep with no adoption logic; the refusing legs
are the sets (renumber/append/rewrite/census) and pipe (row shape + stripped log +
census). A no-op tool (exit 0, nothing written) is refused everywhere (files
absent → `BY_DOC=0/9`, `COLLISIONS=None`).

## Evidence anchors

- c1-count.py: run_tool cmd 176–185; expected mapping by document 213–222; verdict
  gate 274–277, 396; guard_leg 290–307; pipe_leg 310–338; PINS/sha pin 348–352;
  BASE_REV 52.
- Census (sources-census.sh): E01/E02/E03/E08/E09/E11 checks at row_pass lines
  634–674 and usedby_findings 538–571; validate exits 1 on E-codes (739–745, 805).
- Goldens captured by `run-golden.sh` from the real candidate tool's runs on the
  identical fixtures (byte-exact copies; e.g. out-A/renumber.tsv 10 lines,
  append.md 9 rows, collisions 14 ids; pipe append.md 1 row with `\ |` stripped,
  stripped.tsv logged `S096 recheck …`).
- Baseline: candidate tool at 65940928 == working tree (sha 3b8a6e7…); counter
  prints C1=PASS (real tool) and C1=PASS (cheat).

## Smallest safe correction

Add one mutation leg that perturbs the staged package before running the tool
(e.g. renumber a staged id, alter a URL, or append a novel row in a copy) so the
expected outputs change and replay constants no longer match; re-pin the mutated
package. That forces the tool to derive outputs from its actual inputs and makes
the counter falsify hollow replays. Document that counter is a conformance check,
not a mechanism audit.

VERDICT: attacked the C1 freeze with two cheat tools — the canned golden-replay
tool PASSES all five legs (C1=PASS, exit 0) with zero adoption logic, so the
counter is wrong as a mechanism gate; the generic collision-only tool also passes
the guard leg alone; suggested fix is a perturbed-input leg.

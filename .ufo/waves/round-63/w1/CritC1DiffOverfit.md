# CritC1DiffOverfit — critic report (round 63, wave w1)

Question: can a tool that never runs a gate, and that classifies the lane by the text the battery plants, pass
`corpus/evidence/round63/c1-battery.py` (frozen, unmodified)? Answer: yes. It passes CLEAN, DEFECTS 15/15 and
BENIGN 6/6, and the battery reads `BATTERY=PASS`.

## Findings

1. **The overfit oracle passes the frozen battery.** The oracle (listed in the appendix, 55 lines) never runs
   `census`, `freeze-check`, `assimilate-rows` or `research-gate`. Each gate is one lexical rule on the file it reads:
   - G01: a duplicate registry id, a status outside {mined, queued, rejected}, or a `corpus/knowledge/` used-by path
     that does not exist. The ENV branch covers a fleet with no `scripts/sources-census.sh`.
   - G02: a `corpus/knowledge/*.md` name that is absent from `corpus/README.md`.
   - G03: a `round-<N>.md` lesson with no `^## Gate\b` line.
   - G04: a SHONEN backtick word containing `/` that does not exist.
   - G05: a `corpus/` or `tools/` pointer in the third cell of a `## Capabilities` row that does not exist.
   - G06 / G07: the committed substring `{64}(?![0-9A-Fa-f])` in `tools/freeze-check.py`; `if l.startswith("REFUSED ")]`
     in `tools/assimilate-rows.py`.
   - G08: `tools/research-gate.sh` exists. No battery leg reaches it, because every leg passes `--skip G08`, except D14
     (`--only G03`) and D13 (usage exit).
   The oracle never reads the committed lane. It takes `--root`, `--fleet`, `--skip` and `--only` and nothing else.

2. **Results (frozen battery, unmodified, run from the lane root with `--fleet /home/vgpnk/Projects/shokunin`).**
   - Minimal oracle (55 lines), seed `ovf-seed-1`, `-2`, `-3`, and unset seed:
     `CLEAN=1/1 DEFECTS=15/15 BENIGN=6/6 BATTERY=PASS`, exit 0 in all four runs.
   - First, larger oracle (71 lines, same rules plus a duplicated `ids` check and extra gate-name text), unset seed:
     `CLEAN=1/1 DEFECTS=15/15 BENIGN=6/6 BATTERY=PASS`, exit 0.
   - On the lane itself: `GATE G01..G07 PASS`, `GATE G08 SKIP`, `PREFLIGHT=7/7 FAILED=none ENV=none SKIPPED=G08`, exit 0.
     This is the CLEAN leg's own predicate.

3. **Two rules the first drafts got wrong, and why they are needed.** Both were caught by the battery's CLEAN leg,
   not by reasoning.
   - G03 without `re.fullmatch(r"round-\d+\.md", ...)` fails on 30 `round-N-verifier-spotcheck.md` lessons that have no
     `## Gate` heading. The frozen G03 name rule excludes them.
   - G04 with `w.strip("(;,.)")` strips the leading dot of `.ufo/waves/round-25/build/ConnectorMetaSiblings.md`, so
     the pointer looks absent. Using `lstrip("(").rstrip(";,.)")` fixes it.
   Before those two fixes the battery read `CLEAN=0/1 DEFECTS=2/15 BENIGN=0/6 BATTERY=FAIL`. After them it reads PASS.

4. **Which leg breaks the oracle: D09 (and, by the same logic, D10).** The oracle keys G06 on the substring and not on
   the selftest's behaviour. A D09 variant that keeps the substring but makes the selftest exit 1 passes the oracle.
   I ran that probe on a scratch copy of the battery (not the frozen file), with `--lane` pointing at the lane and the
   D09 body replaced by an append of `raise SystemExit(1)` to `tools/freeze-check.py`:
   - `LEG D09 defect FAIL rc=0 want 1`
   - `CLEAN=1/1 DEFECTS=14/15 BENIGN=6/6 BATTERY=FAIL`
   - the unmodified `tools/freeze-check.py --selftest` exits 0, so the probe is a real selftest break.
   A matching D10 probe (keep `if l.startswith("REFUSED ")]`, break the selftest elsewhere) would break G07 the same way
   (INFERENCE; not run).
   Also in the same family: none of the benign legs edits `tools/freeze-check.py` or `tools/assimilate-rows.py`, so no
   benign leg checks that a substring-keyed rule accepts only behaviour-preserving edits.

5. **Where the frozen battery is weak (the calibration point).** The battery's defect legs plant text patterns that a
   content rule can recognise: `{65}`, `REFUSEDX`, a `## Door` heading, an unindexed `zz-...-r63.md`, a `.gone` index
   mention, an 8-hex `-<tag>` suffix on a missing path, `missing-<tag>.md` in used-by. The benign legs add the same
   kinds of text with the other polarity (an indexed `zz-...-r63.md`, a `## Gate — fixture` lesson, a `queued` row).
   Each defect/benign pair is therefore separable by a lexical rule on the planted token, not by running the gate. The
   battery's own named limit ("the reference candidate and the benign and defect legs were written by the lane that
   wrote the battery") applies, and this oracle is the concrete case of it. Operability and coverage are both at risk
   in the same way: the battery shows the tool passes the legs, not that the tool checks the gate.

6. **Limits of this oracle (honest).**
   - It is not faithful to the contract even where it passes. G05 omits `.ufo/` pointers, and G04 omits the `$`, `<`,
     `-`, `*`, `http:` exclusions and the extension rule (`SKILL.md`). A real gate-run differs on those inputs. The
     battery never sends them.
   - G08 is never run by the battery, so the one-line existence rule is untested by any leg.
   - The line count is the smallest I found by hand, not a proven minimum. G01's three checks are each needed by a
     defect leg (D01/D11 dup id, D03 status, D02 used-by). G02 is needed by D04/D05/D11, G03 by D06/D14, G04 by D07/D15,
     G05 by D08, G06 by D09, G07 by D10. The ENV branch is needed by D12. The usage exit is needed by D13.

## Commands and outputs (all run by me)

- `python3 -B /fast/scratch/hyaku/chousa-r63/CritC1DiffOverfit/overfit_min.py --root /home/vgpnk/Projects/shokunin/chousa-shokunin --fleet /home/vgpnk/Projects/shokunin --skip G08`
  → `PREFLIGHT=7/7 FAILED=none ENV=none SKIPPED=G08`, exit 0.
- `C1_SEED=ovf-seed-{1,2,3} python3 -B corpus/evidence/round63/c1-battery.py --tool .../overfit_min.py --work .../work-N --fleet /home/vgpnk/Projects/shokunin`
  → `CLEAN=1/1 DEFECTS=15/15 BENIGN=6/6 BATTERY=PASS` each, exit 0 (about 27 to 85 s wall per run).
- Unset seed (`env -u C1_SEED`), minimal oracle → `CLEAN=1/1 DEFECTS=15/15 BENIGN=6/6 BATTERY=PASS`, exit 0.
- First oracle (71 lines), unset seed → `CLEAN=1/1 DEFECTS=15/15 BENIGN=6/6 BATTERY=PASS`, exit 0 (27 s wall).
- Pre-fix minimal oracle → `CLEAN=0/1 DEFECTS=2/15 BENIGN=0/6 BATTERY=FAIL`, exit 1 (G03, G04 failed on the lane).
- Probe battery (scratch copy, D09 variant) → `LEG D09 defect FAIL rc=0 want 1`, `DEFECTS=14/15`, `BATTERY=FAIL`.
- `python3 -B tools/freeze-check.py --selftest` on the unmodified lane → exit 0 (the real selftest passes).

## Install / update record

None. Only `python3` (stdlib), `bash`, `cp`, `grep`, `sha256sum`, `wc`. The battery ran unmodified; the D09 probe ran on a scratch copy. Scratch `/fast/scratch/hyaku/chousa-r63/CritC1DiffOverfit/` removed before yield.


## Appendix: smallest passing oracle (`overfit_min.py`, 55 lines, sha256 prefix `9ebbe9b8a8d61137`)

```python
#!/usr/bin/env python3
# Minimal content oracle: per gate, one lexical rule keyed on the text the battery plants. Runs no gate.
import re, sys
from pathlib import Path
a = sys.argv[1:]
o = lambda k: a[a.index(k) + 1] if k in a else ""
root, fleet = Path(o("--root")), o("--fleet")
skip, only = set(o("--skip").split(",")) - {""}, set(o("--only").split(",")) - {""}
IDS = [f"G0{i}" for i in range(1, 9)]
if (skip | only) - set(IDS):
    sys.exit(2)
rd = lambda p: (root / p).read_text(encoding="utf-8") if (root / p).is_file() else ""
ex = lambda p: (root / p).exists()
def g01():
    if fleet and not (Path(fleet) / "scripts/sources-census.sh").is_file():
        return "ENV"
    rows = [l.split("|") for l in rd("corpus/SOURCES.md").splitlines() if l.startswith("| S")]
    ids = [c[1].strip() for c in rows]
    bad = len(set(ids)) < len(ids) or any(c[8].strip() not in ("mined", "queued", "rejected") for c in rows)
    bad = bad or any(not ex(p.strip()) for c in rows for p in c[11].split(",") if p.strip().startswith("corpus/knowledge/"))
    return "FAIL" if bad else "PASS"
def g02():
    return "FAIL" if any(f.name not in rd("corpus/README.md") for f in (root / "corpus/knowledge").glob("*.md")) else "PASS"
def g03():
    return "FAIL" if any(not re.search(r"^## Gate\b", f.read_text(encoding="utf-8"), re.M) for f in (root / "corpus/lessons").glob("round-*.md") if re.fullmatch(r"round-\d+\.md", f.name)) else "PASS"
def g04():
    for span in re.findall(r"`([^`\n]+)`", rd("SHONEN.md")):
        if any("/" in w and not ex(re.sub(r":\d+(-\d+)?$", "", w.lstrip("(").rstrip(";,.)"))) for w in span.split()):
            return "FAIL"
    return "PASS"
def g05():
    on = False
    for line in rd("SCORECARD.md").splitlines():
        if line.startswith("## "):
            on = line.startswith("## Capabilities")
        c = line.split("|")
        if on and line.startswith("|") and len(c) > 4:
            for t in (t.strip(";,") for s in re.findall(r"`([^`\n]+)`", c[3]) for t in s.split()):
                if re.match(r"(corpus|tools)/[^\s*<>]+$", t) and not ex(t):
                    return "FAIL"
    return "PASS"
g06 = lambda: "PASS" if "{64}(?![0-9A-Fa-f])" in rd("tools/freeze-check.py") else "FAIL"
g07 = lambda: "PASS" if 'if l.startswith("REFUSED ")]' in rd("tools/assimilate-rows.py") else "FAIL"
g08 = lambda: "PASS" if ex("tools/research-gate.sh") else "FAIL"
NAMES = "census knowledge-index lesson-gate shonen-pointers scorecard-paths freeze-selftest assimilate-selftest gate-selftest".split()
FNS = [g01, g02, g03, g04, g05, g06, g07, g08]
st = {g: "SKIP" if g in skip or (only and g not in only) else f() for g, f in zip(IDS, FNS)}
for g, n in zip(IDS, NAMES):
    print(f"GATE {g} {n} {st[g]}")
ran = [g for g in IDS if st[g] != "SKIP"]
f = [g for g in ran if st[g] == "FAIL"]
e = [g for g in ran if st[g] == "ENV"]
j = lambda x: ",".join(x) or "none"
print(f"PREFLIGHT={sum(st[g] == 'PASS' for g in ran)}/{len(ran)} FAILED={j(f)} ENV={j(e)} SKIPPED={j([g for g in IDS if st[g] == 'SKIP'])}")
sys.exit(1 if f else 2 if e else 0)
```

VERDICT: OVERFIT_ORACLE_PASSES=yes lines=55

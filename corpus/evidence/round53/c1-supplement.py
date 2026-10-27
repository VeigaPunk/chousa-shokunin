#!/usr/bin/env python3
"""c1-supplement — POST-FREEZE supplement to the round-53 C1 counter (claims-erratum E1).

Not the claim's rule: R53-C1 is judged on `c1-count.py` as frozen. W1
`R53CritForgeC1` passed the frozen counter 8/8 with a 189-line forge
(`controls/forge-c1.py`) that implements the held/twin/append map honestly but
cans REAL on the pinned package digest, rejects only the generator's four
invalid-date shapes, and answers `--selftest` with two printed strings. This
supplement adds the three legs that refuse those shortcuts:

  CALENDAR   every cited row whose recheck is a date that is invalid only by the
             calendar (day 29 of February in a non-leap year, day 31 of a 30-day
             month, day 32 of any month, month 00/13-19), drawn at counting time,
             is refused (exit 1, `REFUSED <id>: recheck`), while a valid 29
             February in a leap year on the same row is accepted (exit 0);
  REAL_PERTURBED  the campaign package's three round-53 entries and their staged
             rows, rewritten at counting time with fresh staged ids (same
             ascending order), fresh entry file names and a registry whose
             maximum id is drawn at random: the map must be the same shape as
             REAL (five appends in staged order, the S185-row's twin last) with
             lane ids continuing from the drawn maximum, `HELD=0 TWIN=1`;
  SELFTEST_RAN  `--selftest` on a COPY of the round-50 pinned fixtures with one
             expected finding removed at random must FAIL (exit 1, `DIFF
             unexpected` naming that finding), and on the unmodified copy PASS
             with the same `FINDING` lines minus that one plus it.

Usage: python3 corpus/evidence/round53/c1-supplement.py [--tool PATH] [--seed N] [--work DIR]
Prints one line per leg and `SUPPLEMENT_LEGS=n/3`; exit 0 all hold, 1 otherwise, 2 env.
"""
from __future__ import annotations

import argparse
import calendar
import json
import os
import pathlib
import random
import re
import shutil
import subprocess
import sys
import tempfile

LANE = pathlib.Path(__file__).resolve().parents[3]
PKG = pathlib.Path("/home/vgpnk/Projects/shokuknow/merge/chousa")
R50_FIX = LANE / "corpus" / "evidence" / "round50" / "c1-fixtures"
ENTRIES = ("search-tracking-record-r40.md", "western-instrument-alignment-r50.md",
           "quality-control-guideline-issued-text-r48.md")
STAGED = ("S134", "S185", "S186", "S190", "S193", "S195")
HEAD = "| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |\n|---|---|---|---|---|---|---|---|---|---|---|\n"


def run(tool, *args):
    e = dict(os.environ)
    e.pop("ASSIMILATE_CITES", None)
    try:
        r = subprocess.run([sys.executable, str(tool), *args], capture_output=True, text=True, timeout=120, env=e)
        return r.returncode, r.stdout, r.stderr
    except subprocess.TimeoutExpired:
        return 124, "", "timeout"


def read_map(out):
    p = out / "renumber.tsv"
    if not p.is_file():
        return None
    return {f[0]: (f[1], f[2]) for f in (l.split("\t") for l in p.read_text(encoding="utf-8").splitlines()[1:]) if len(f) >= 3}


def bad_date(r):
    y = r.choice([y for y in range(2025, 2040) if not calendar.isleap(y)])
    return r.choice([f"{y}-02-29", f"{y}-{r.choice(['04', '06', '09', '11'])}-31", f"{y}-0{r.randint(1, 9)}-32",
                     f"{y}-{r.choice(['00', '13', '14', '15', '16', '17', '18', '19'])}-{r.randint(10, 28)}"])


def leg_calendar(tool, r, work):
    ok = True
    notes = []
    for k in range(4):
        d = work / f"cal{k}-{r.getrandbits(32):08x}"
        (d / "knowledge" / "corpus" / "knowledge").mkdir(parents=True)
        host = f"https://h{r.getrandbits(24):06x}.example.org/p/{r.getrandbits(24):06x}"
        held = f"https://g{r.getrandbits(24):06x}.example.net/q"
        (d / "registry.md").write_text(f"## Registry\n\n{HEAD}| S001 | Lane — {held} | docs | A | x | x | x | mined | 2026-01-01 | 90d | — |\n", encoding="utf-8")
        a, b, c = f"S{r.randint(200, 499)}", f"S{r.randint(500, 799)}", f"S{r.randint(800, 999)}"
        bad = r.choice([b, c])        # twin row or held row
        bd = bad_date(r)
        leap = r.choice([y for y in range(2028, 2060, 4) if calendar.isleap(y)])
        rows = [f"| {a} | D — {host} | docs | A | s | s | s | mined | 2026-10-20 | 90d | — |",
                f"| {b} | D — {host} | docs | A | s | s | s | mined | 2026-10-20 | {bd if bad == b else '180d'} | — |",
                f"| {c} | D — {held} | docs | A | s | s | s | mined | 2026-10-20 | {bd if bad == c else '90d'} | — |"]
        (d / "staged.md").write_text(HEAD + "\n".join(rows) + "\n", encoding="utf-8")
        name = f"k{r.getrandbits(24):06x}.md"
        (d / "knowledge" / "corpus" / "knowledge" / name).write_text(
            f"# x\n\nsource: {a} — {host} — s\nsource: {b} — {host} — s\nsource: {c} — {held} — s\n\n#### Observation\n", encoding="utf-8")
        args = ["--staged", str(d / "staged.md"), "--knowledge", str(d / "knowledge"), "--registry", str(d / "registry.md"),
                "--opened", "2026-10-26", "--out", str(d / "out"), "--entry", f"corpus/knowledge/{name}"]
        rc, so, se = run(tool, *args)
        refused = rc == 1 and any(l.startswith(f"REFUSED {bad}: recheck") for l in se.splitlines()) and not (d / "out" / "renumber.tsv").exists()
        # the same package with a leap-year 29 February is accepted
        txt = (d / "staged.md").read_text(encoding="utf-8").replace(bd, f"{leap}-02-29")
        (d / "staged.md").write_text(txt, encoding="utf-8")
        rc2, so2, se2 = run(tool, *args)
        good = rc2 == 0
        notes.append(f"{bd}->{'refused' if refused else 'ACCEPTED'} {leap}-02-29->{'ok' if good else 'REFUSED'}")
        ok = ok and refused and good
    return ok, "; ".join(notes)


def leg_real_perturbed(tool, r, work):
    d = work / f"real-{r.getrandbits(32):08x}"
    (d / "knowledge" / "corpus" / "knowledge").mkdir(parents=True)
    staged = (PKG / "SOURCES.append.md").read_text(encoding="utf-8")
    rows = {}
    for line in staged.splitlines():
        m = re.match(r"^ {0,3}\|[ \t]*(S\d{3,})[ \t]*\|", line)
        if m and m.group(1) in STAGED and m.group(1) not in rows:
            rows[m.group(1)] = line
    if len(rows) != 6:
        return None, "campaign rows missing"
    new_ids = sorted(r.sample(range(300, 990), 6))
    sub = {old: f"S{n}" for old, n in zip(STAGED, new_ids)}
    pat = re.compile(r"\bS\d{3,}\b")
    out_rows = [pat.sub(lambda m: sub.get(m.group(0), m.group(0)), rows[s]) for s in STAGED]
    r.shuffle(out_rows)
    (d / "staged.md").write_text(HEAD + "\n".join(out_rows) + "\n", encoding="utf-8")
    mx = r.randint(20, 400)
    reg = "".join(f"| S{i:03d} | Lane {i} — https://lane{i}-{r.getrandbits(16):04x}.example.com/x | docs | A | x | x | x | mined | 2026-01-01 | 90d | — |\n"
                  for i in range(1, mx + 1))
    (d / "registry.md").write_text(f"## Registry\n\n{HEAD}{reg}", encoding="utf-8")
    names = []
    for e in ENTRIES:
        t = (PKG / "knowledge" / "corpus" / "knowledge" / e).read_text(encoding="utf-8")
        t = pat.sub(lambda m: sub.get(m.group(0), m.group(0)), t)
        n = f"n{r.getrandbits(32):08x}.md"
        (d / "knowledge" / "corpus" / "knowledge" / n).write_text(t, encoding="utf-8")
        names.append(f"corpus/knowledge/{n}")
    args = ["--staged", str(d / "staged.md"), "--knowledge", str(d / "knowledge"), "--registry", str(d / "registry.md"),
            "--opened", "2026-10-26", "--out", str(d / "out")] + sum((["--entry", n] for n in names), [])
    rc, so, se = run(tool, *args)
    want = {}
    nxt = mx + 1
    for s in STAGED[:5]:
        want[sub[s]] = (f"S{nxt:03d}", "append")
        nxt += 1
    want[sub["S195"]] = (want[sub["S185"]][0], "twin")
    got = read_map(d / "out")
    counts = bool(re.search(r"(^|\s)HELD=0(\s|$)", so)) and bool(re.search(r"(^|\s)TWIN=1(\s|$)", so))
    return rc == 0 and got == want and counts, f"rc={rc} max=S{mx:03d} map={'ok' if got == want else got} counts={counts}"


def leg_selftest_ran(tool, r, work):
    d = work / f"st-{r.getrandbits(32):08x}"
    shutil.copytree(R50_FIX, d)
    exp = json.loads((d / "expected.json").read_text(encoding="utf-8"))
    rc, so, se = run(tool, "--selftest", "--cites", "all", "--fixtures", str(d), "--expected", str(d / "expected.json"))
    full_ok = rc == 0 and "SELFTEST=PASS" in so and sorted(l[8:] for l in so.splitlines() if l.startswith("FINDING ")) == sorted(exp["findings"])
    drop = r.choice(exp["findings"])
    exp2 = dict(exp)
    exp2["findings"] = [f for f in exp["findings"] if f != drop] + [f for f in exp["findings"] if f == drop][1:]
    (d / "expected.json").write_text(json.dumps(exp2, ensure_ascii=False), encoding="utf-8")
    rc2, so2, se2 = run(tool, "--selftest", "--cites", "all", "--fixtures", str(d), "--expected", str(d / "expected.json"))
    cut_ok = rc2 == 1 and f"DIFF unexpected {drop}" in so2 and "SELFTEST=FAIL" in so2
    return full_ok and cut_ok, f"full={'ok' if full_ok else 'FAIL'} dropped={drop!r} -> {'FAIL as expected' if cut_ok else 'NOT DETECTED'}"


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--tool", default=str(LANE / "tools" / "assimilate-rows.py"))
    ap.add_argument("--seed", type=int)
    ap.add_argument("--work")
    a = ap.parse_args()
    tool = pathlib.Path(a.tool).resolve()
    seed = a.seed if a.seed is not None else random.SystemRandom().randrange(1 << 30)
    r = random.Random(seed)
    own = a.work is None
    work = pathlib.Path(tempfile.mkdtemp(prefix="r53c1sup-")) if own else pathlib.Path(a.work)
    work.mkdir(parents=True, exist_ok=True)
    print(f"SEED={seed}" if a.seed is not None else "SEED=unseeded")
    try:
        res = {}
        for name, fn in (("CALENDAR", leg_calendar), ("REAL_PERTURBED", leg_real_perturbed), ("SELFTEST_RAN", leg_selftest_ran)):
            ok, note = fn(tool, r, work) if tool.is_file() else (False, "no tool")
            if ok is None:
                print(f"ENV {note}")
                return 2
            res[name] = ok
            print(f"{name}={'PASS' if ok else 'FAIL'} {note}")
        n = sum(res.values())
        print(f"SUPPLEMENT_LEGS={n}/3")
        return 0 if n == 3 else 1
    finally:
        if own:
            shutil.rmtree(work, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main())

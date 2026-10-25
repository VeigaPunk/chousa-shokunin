#!/usr/bin/env python3
"""c1-supplement — post-freeze supplement to the frozen round-51 C1 counter (`c1-count.py`).

Why it exists (round-51 wave 1, disclosed in claims-erratum.md E2-E4): the frozen counter's work
directories carry fixed names (`s`, `d1`, `d2`, `renamed-heading` ...), so a 94-line tool that reads the
name from `--out` and prints canned shapes passes it 5/5 (`R51CritForgeC1`); its id draws can collide and
hang it (1/401 per run, `R51ExecSeedRuns`); an ambient `ASSIMILATE_CITES` flips its verdict
(`R51SentScope` H5); and the shipped echo control delegated to the real tool, so it stopped being a
control. The frozen counter, its predicate and its target are NOT changed; this supplement is the
stricter second counter, and the report states both.

Legs (all on packages generated here from fresh randomness, in work directories with random names,
with `ASSIMILATE_CITES` removed from the tool's environment, three runs of the generator per leg):
  SHAPE        the frozen five behaviours again, under random directory names and distinct ids
  MUTATION     the round-50 pinned package with ONE cell changed and the expected file untouched must make
               `--selftest --cites all` exit 1 with SELFTEST=FAIL (an echo/replay tool prints PASS)
  CROSS_ENTRY  an id cited on entry A's `source:` line and only mentioned in entry B's body stays
               unchanged in B, is listed in `bodyonly.tsv` for B, and is not in the row's `used-by`
  SOURCE_LINE  an id in a `source:` line's tail, a `source:` line in the body, and `source:` after
               `####` are not citations; two entries citing the same id make one row
  UNKNOWN_SRC  a `source:` id that is neither a staged row nor a Registry row is refused (exit 1, REFUSED)
  CLASH        a body-only id that is also a lane id, or a body token equal to a minted id that is no staged
               row, lands in `bodyclash.tsv` and on stderr
  OWN_WORK     a `source:` id that is both a lane id and a staged id with another URL is the lane's own row
  STALE_OUT    a refusal into a reused --out leaves no `renumber.tsv`/`append.md` of the previous run
  HEADER       a `#### Provenance` heading above the header does not hide it; a fenced example is not a citation
  ENV_DEFAULT  ASSIMILATE_CITES=all with no flag restores the all-token reading

Usage: python3 corpus/evidence/round51/c1-supplement.py [--tool PATH] [--seed N]
Exit 0 `C1_SUPPLEMENT=PASS` · 1 a leg failed. With `--tool` only the legs that do not need the lane's
default fixtures run (all of the above do not).
"""
from __future__ import annotations

import argparse
import importlib.util
import os
import pathlib
import random
import re
import shutil
import subprocess
import sys
import tempfile

EV = pathlib.Path(__file__).resolve().parent
LANE = EV.parents[2]
spec = importlib.util.spec_from_file_location("c1count", EV / "c1-count.py")
c1 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(c1)
ENV = {k: v for k, v in os.environ.items() if k != "ASSIMILATE_CITES"}


def run(tool: pathlib.Path, *args: str):
    try:
        r = subprocess.run([sys.executable, str(tool), *args], capture_output=True, text=True, timeout=120, env=ENV)
    except subprocess.TimeoutExpired:
        return 124, "", "timeout"
    return r.returncode, r.stdout, r.stderr


def adopt(tool, tmp, reg, staged_rows, entries: dict[str, str], *flags):
    work = pathlib.Path(tempfile.mkdtemp(prefix=f"w{random.getrandbits(40):010x}-", dir=tmp))
    kd = work / "knowledge/corpus/knowledge"
    kd.mkdir(parents=True)
    for name, txt in entries.items():
        (kd / name).write_text(txt, encoding="utf-8")
    (work / "registry.md").write_text(reg, encoding="utf-8")
    (work / "staged.md").write_text("# staged\n\n" + c1.HEAD + "".join(staged_rows), encoding="utf-8")
    cmd = ["--staged", str(work / "staged.md"), "--knowledge", str(work / "knowledge"), "--registry", str(work / "registry.md"),
           "--opened", "2026-10-25", "--out", str(work / "out")]
    for name in entries:
        cmd += ["--entry", f"corpus/knowledge/{name}"]
    rc, out, err = run(tool, *cmd, *flags)
    return work, rc, out, err


def edit(path: pathlib.Path, old: str, new: str) -> bool:
    s = path.read_text(encoding="utf-8")
    if old not in s:
        return False
    path.write_text(s.replace(old, new, 1), encoding="utf-8")
    return True


def lines(p: pathlib.Path):
    return [l for l in p.read_text(encoding="utf-8").splitlines() if l.strip()] if p.is_file() else []


def tsv(p: pathlib.Path):
    return [l.split("\t") for l in p.read_text(encoding="utf-8").splitlines()[1:]] if p.is_file() else []


def safe_seed(rnd: random.Random) -> int:
    """A seed for which the frozen counter's first two id draws differ (it hangs otherwise: erratum E2).
    The counter's draw order (c1-count.py): getrandbits(32), randint(12, 40), then three randint(500, 900)."""
    while True:
        s = rnd.getrandbits(30)
        r = random.Random(s)
        r.getrandbits(32)
        r.randint(12, 40)
        x, y, z = r.randint(500, 900), r.randint(500, 900), r.randint(500, 900)
        if x != y and x != z and y != z:
            return s


def fname(rnd: random.Random) -> str:
    return f"e{rnd.getrandbits(32):08x}.md"


def one_round(tool: pathlib.Path, tmp: pathlib.Path, rnd: random.Random) -> dict[str, bool]:
    n = f"{rnd.getrandbits(32):08x}"
    host = f"h{n}.example.test"
    top = rnd.randint(12, 40)
    ids = rnd.sample(range(500, 900), 8)
    A, B, C, D, E, F, G, H = (f"S{i}" for i in ids)
    na, nb, nc = fname(rnd), fname(rnd), fname(rnd)
    ra, rb, rc_ = f"corpus/knowledge/{na}", f"corpus/knowledge/{nb}", f"corpus/knowledge/{nc}"

    def lane():
        return [c1.row(f"S{i:03d}", f"Doc {i} — https://{host}/lane-{i}") for i in range(1, top + 1)]

    reg = c1.registry(lane())
    ua, ub = f"https://{host}/a-{n}", f"https://{host}/b-{n}"
    res: dict[str, bool] = {}
    hdr = "verified-at: 2026-10-25\nrecheck: 90d\n\n#### Observation\n\n"

    # SHAPE: the frozen counter's five behaviours (its own directory names are fixed: Mistakes row 8)
    rc_c1 = subprocess.run([sys.executable, str(EV / "c1-count.py"), "--tool", str(tool), "--seed", str(safe_seed(rnd))],
                           capture_output=True, text=True, timeout=300, env=ENV)
    res["SHAPE"] = rc_c1.returncode == 0 and "LEGS=5/5" in rc_c1.stdout

    # MUTATION: one changed cell, expected file untouched
    m = pathlib.Path(tempfile.mkdtemp(prefix=f"m{rnd.getrandbits(40):010x}-", dir=tmp)) / "fix"
    shutil.copytree(c1.R50_FIX, m, copy_function=shutil.copyfile)
    done = edit(m / "staged.md", "2026-12-01 — re-verify after release", "2027-01-01 — re-verify after release")
    rc, out, _ = run(tool, "--selftest", "--fixtures", str(m), "--expected", str(m / "expected.json"), "--cites", "all")
    res["MUTATION"] = bool(done) and rc == 1 and "SELFTEST=FAIL" in out and "SELFTEST=PASS" not in out

    # CROSS_ENTRY
    st = [c1.row(A, f"A — {ua}", ra), c1.row(B, f"B — {ub}", rb)]
    ea = f"source: {A} — {ua} — s\n{hdr}- A ({A}).\n"
    eb = f"source: {B} — {ub} — s\n{hdr}- B ({B}); only mentions {A}.\n"
    w, rc, out, err = adopt(tool, tmp, reg, st, {na: ea, nb: eb})
    app = lines(w / "out/append.md")
    bo = tsv(w / "out/bodyonly.tsv")
    body_b = (w / "out/corpus/knowledge" / nb).read_text(encoding="utf-8") if (w / "out/corpus/knowledge" / nb).is_file() else ""
    a_row = [l for l in app if ua in l]
    res["CROSS_ENTRY"] = (rc == 0 and len(app) == 2 and A in body_b and bo == [[rb, A]]
                          and len(a_row) == 1 and a_row[0].split("|")[11].strip() == ra)

    # SOURCE_LINE: tail id, body `source:` line, same id in two entries
    st = [c1.row(A, f"A — {ua}", ra), c1.row(B, f"B — {ub}"), c1.row(C, f"C — https://{host}/c-{n}")]
    tail = (f"source: {A} — {ua} — s (supersedes {B})\n{hdr}source: {C} — https://{host}/c-{n} — a body line\n- A ({A}).\n")
    ea2 = f"source: {A} — {ua} — s\n{hdr}- A again ({A}).\n"
    w, rc, out, err = adopt(tool, tmp, reg, st, {na: tail, nb: ea2})
    rn = {r[0] for r in tsv(w / "out/renumber.tsv")}
    app = lines(w / "out/append.md")
    res["SOURCE_LINE"] = rc == 0 and rn == {A} and len(app) == 1 and na in app[0] and nb in app[0]

    # UNKNOWN_SRC
    st = [c1.row(A, f"A — {ua}", ra)]
    bad = f"source: {A} — {ua} — s\nsource: {D} — https://{host}/nowhere — s\n{hdr}- x ({A}).\n"
    w, rc, out, err = adopt(tool, tmp, reg, st, {na: bad})
    res["UNKNOWN_SRC"] = rc == 1 and "REFUSED" in err and not (w / "out/append.md").is_file() and not (w / "out/renumber.tsv").is_file()

    # CLASH: body-only staged id equal to a lane id; and a body token equal to a minted id that is no staged row
    lane_clash = f"S{rnd.randint(1, top):03d}"
    st = [c1.row(A, f"A — {ua}", ra), c1.row(lane_clash, f"Staged twin of a lane id — https://{host}/twin-{n}")]
    ec = f"source: {A} — {ua} — s\n{hdr}- A ({A}); mentions {lane_clash}.\n"
    w, rc, out, err = adopt(tool, tmp, reg, st, {na: ec})
    ok1 = rc == 0 and tsv(w / "out/bodyclash.tsv") == [[ra, lane_clash]] and "WARN" in err
    minted_id = f"S{top + 1:03d}"
    st = [c1.row(A, f"A — {ua}", ra)]
    ed = f"source: {A} — {ua} — s\n{hdr}- A ({A}).\n"
    ee = f"source: {B} — {ub} — s\n{hdr}- mentions only {minted_id}.\n"
    w, rc, out, err = adopt(tool, tmp, reg, st + [c1.row(B, f"B — {ub}", rb)], {na: ed, nb: ee})
    ok2 = rc == 0 and any(r[1] == minted_id for r in tsv(w / "out/bodyclash.tsv"))
    res["CLASH"] = bool(ok1 and ok2)

    # OWN_WORK: a source id that is both a lane id and a staged id with another URL is the lane's own row
    own = f"S{rnd.randint(1, top):03d}"
    st = [c1.row(own, f"Unrelated staged doc — https://{host}/unrelated-{n}", ra), c1.row(A, f"A — {ua}", ra)]
    eo = f"source: {own} — corpus/knowledge/some-lane-entry.md — lane-local own work\nsource: {A} — {ua} — s\n{hdr}- A ({A}).\n"
    w, rc, out, err = adopt(tool, tmp, reg, st, {na: eo})
    rn = {r[0] for r in tsv(w / "out/renumber.tsv")}
    body_o = (w / "out/corpus/knowledge" / na).read_text(encoding="utf-8") if (w / "out/corpus/knowledge" / na).is_file() else ""
    res["OWN_WORK"] = rc == 0 and rn == {A} and f"source: {own} — corpus/knowledge/some-lane-entry.md" in body_o

    # STALE_OUT: a refusal into a reused --out leaves no previous claim
    w, rc, out, err = adopt(tool, tmp, reg, [c1.row(A, f"A — {ua}", ra)], {na: ed})
    ok_first = rc == 0 and (w / "out/renumber.tsv").is_file()
    (w / "staged.md").write_text("# staged\n\n" + c1.HEAD + f"| {A} | broken | docs |\n", encoding="utf-8")
    rc2, _o, err2 = run(tool, "--staged", str(w / "staged.md"), "--knowledge", str(w / "knowledge"), "--registry", str(w / "registry.md"),
                        "--opened", "2026-10-25", "--out", str(w / "out"), "--entry", ra)
    res["STALE_OUT"] = bool(ok_first) and rc2 == 1 and not (w / "out/renumber.tsv").is_file() and not (w / "out/append.md").is_file()

    # HEADER: a `#### Provenance` heading above the header does not hide it; a fenced example header is not a citation
    st = [c1.row(A, f"A — {ua}", ra), c1.row(B, f"B — {ub}")]
    eh = f"# T\n\n#### Provenance\n\nsource: {A} — {ua} — s\n```\nsource: {B} — {ub} — example\n```\n{hdr}- A ({A}).\n"
    w, rc, out, err = adopt(tool, tmp, reg, st, {na: eh})
    rn = {r[0] for r in tsv(w / "out/renumber.tsv")}
    res["HEADER"] = rc == 0 and rn == {A}

    # ENV_DEFAULT: ASSIMILATE_CITES=all with no flag restores the all-token reading
    st = [c1.row(A, f"A — {ua}", ra), c1.row(C, f"C — https://{host}/c-{n}")]
    ef = f"source: {A} — {ua} — s\n{hdr}- A ({A}) and {C}.\n"
    work = pathlib.Path(tempfile.mkdtemp(prefix=f"w{rnd.getrandbits(40):010x}-", dir=tmp))
    (work / "knowledge/corpus/knowledge").mkdir(parents=True)
    (work / "knowledge/corpus/knowledge" / na).write_text(ef, encoding="utf-8")
    (work / "registry.md").write_text(reg, encoding="utf-8")
    (work / "staged.md").write_text("# staged\n\n" + c1.HEAD + "".join(st), encoding="utf-8")
    r = subprocess.run([sys.executable, str(tool), "--staged", str(work / "staged.md"), "--knowledge", str(work / "knowledge"),
                        "--registry", str(work / "registry.md"), "--opened", "2026-10-25", "--out", str(work / "out"), "--entry", ra],
                       capture_output=True, text=True, timeout=120, env={**ENV, "ASSIMILATE_CITES": "all"})
    res["ENV_DEFAULT"] = r.returncode == 0 and {x[0] for x in tsv(work / "out/renumber.tsv")} == {A, C}
    return res


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--tool")
    ap.add_argument("--seed", type=int)
    a = ap.parse_args()
    tool = pathlib.Path(a.tool) if a.tool else LANE / "tools" / "assimilate-rows.py"
    rnd = random.Random(a.seed if a.seed is not None else int.from_bytes(os.urandom(8), "big"))
    tmp = pathlib.Path(tempfile.mkdtemp(prefix="chousa-r51-sup-"))
    totals: dict[str, int] = {}
    try:
        for _ in range(3):
            for k, v in one_round(tool, tmp, rnd).items():
                totals[k] = totals.get(k, 0) + bool(v)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    legs = {k: v == 3 for k, v in totals.items()}
    for k, v in totals.items():
        print(f"{k}={'PASS' if legs[k] else 'FAIL'} {v}/3")
    n = sum(legs.values())
    print(f"SUPPLEMENT_LEGS={n}/{len(legs)}")
    ok = n == len(legs)
    print("C1_SUPPLEMENT=PASS" if ok else "C1_SUPPLEMENT=FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())

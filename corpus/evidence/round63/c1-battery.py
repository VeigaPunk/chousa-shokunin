#!/usr/bin/env python3
"""R63-C1 frozen battery — does a lane preflight tool tell a lane that is broken from one that only changed?

Predicate R63-C1 (the same sentence as corpus/evidence/round63/claims.md): run on a tool T — a program that takes
`--root DIR [--fleet DIR] [--skip G08] [--only G03]` and prints the `GATE`/`PREFLIGHT=` lines of the contract in
corpus/evidence/round63/claims.md — the battery copies the lane (LANE) once into a scratch GOLDEN, then for each
leg copies GOLDEN to a random-named variant directory, applies one change, copies T's bytes to a random path outside
the variant, runs it from an empty cwd with a minimal environment, and requires:

  CLEAN     the unchanged variant (run with `--skip G08`): exit 0, `PREFLIGHT=7/7 FAILED=none ENV=none SKIPPED=G08`,
            G01..G07 PASS, G08 SKIP;
  DEFECTS   fifteen defect legs D01..D15, each planting one change (D01 a duplicate registry id, D02 a used-by path
            missing on disk, D03 a status outside the enum, D04 an unindexed knowledge entry, D05 an entry that loses
            its index mention, D06 a lesson without its Gate heading, D07 a SHONEN pointer to a missing file, D08 a
            SCORECARD capability pointer to a missing file, D09 a broken freeze-check selftest, D10 a broken
            assimilate-rows selftest, D11 D01 and D04 together, D12 no census script under `--fleet`, D13 an unknown
            gate id in `--skip`, D14 the D06 defect run with `--only G03`, D15 a SHONEN span with a second path that
            is missing): for D01-D12, D14 and D15 the exit code, the exact FAILED and ENV sets and the per-gate
            statuses named in the leg table below, all other run gates PASS, and a PREFLIGHT=p/n line equal to the
            count of its own GATE lines (a summary that disagrees with its lines fails the leg); for D13 exit 2 and
            no PREFLIGHT line;
  BENIGN    six legs B01..B06 that change a file a gate reads, or a file no gate reads, in a way that keeps the lane
            valid (a registry row, an indexed knowledge entry, a lesson with a Gate heading, SHONEN and SCORECARD
            additions, edits to tools/quote-reopen.py, corpus/README.md and LOG.md): exit 0 and all run gates PASS
            (a tool that fails on any difference fails here),

and prints `CLEAN=1/1 DEFECTS=k/15 BENIGN=b/6 BATTERY=PASS` (exit 0) when k = 15 and b = 6 and CLEAN = 1/1, else
`BATTERY=FAIL` (exit 1). A tool path that does not exist prints `CLEAN=0/1 DEFECTS=0/15 BENIGN=0/6 BATTERY=FAIL` and exits 1;
exit 2 is for usage or environment errors (no census script under the fleet, a non-empty `--work`, run as root, a golden
copy with fewer than 1000 files).
The battery never runs gate G08 (the research-gate selftest, minutes of CPU): every leg passes `--skip G08` except
D13 (`--skip G99`) and D14 (`--only G03`). A full run with G08 is a separate receipt.

Randomised per run (seed: the environment variable C1_SEED, else os.urandom — never argv): the variant directory
names, the path and file name T runs from, the names of added files, the ids and numbers of added registry rows and
lessons, and, for the defect legs that choose one, which registry row, which README entry, which lesson and which
capability pointer is changed. T never receives the seed.

Usage: python3 c1-battery.py --tool PATH --work DIR [--lane DIR] [--fleet DIR] [--jobs N] [--only LEG[,LEG]]
(`--work` absent or empty; scratch under $HYAKU_SCRATCH/chousa-r63/; the work directory is removed at the end).
`--only` runs the named legs and prints their counts with `BATTERY=PARTIAL`, exit 0.
"""
from __future__ import annotations

import argparse
import concurrent.futures
import os
import pathlib
import random
import re
import shutil
import subprocess
import sys

HERE = pathlib.Path(__file__).resolve().parent
LANE = HERE.parents[2]
KEEP_UFO = tuple(f".ufo/waves/round-{r}" for r in (25, 34, 59, 60, 61))
IDS = ["G01", "G02", "G03", "G04", "G05", "G06", "G07", "G08"]
STATUS = {"PASS", "FAIL", "ENV", "SKIP"}
GATE_RE = re.compile(r"^GATE (G\d\d) (\S+) (PASS|FAIL|ENV|SKIP)\b")
SUM_RE = re.compile(r"^PREFLIGHT=(\d+)/(\d+) FAILED=(\S+) ENV=(\S+) SKIPPED=(\S+)$")
ROW_RE = re.compile(r"^ {0,3}\|\s*(S\d{3,})\s*\|")


def build_golden(lane: pathlib.Path, dst: pathlib.Path) -> int:
    n = 0
    for d, ds, fs in os.walk(lane):
        rel = os.path.relpath(d, lane)
        if rel == ".git" or rel.startswith(".git" + os.sep) or "__pycache__" in rel.split(os.sep):
            ds[:] = []
            continue
        if rel.startswith(".ufo"):
            r = rel.replace(os.sep, "/")
            if not (r in (".ufo", ".ufo/waves") or any(r == k or r.startswith(k + "/") for k in KEEP_UFO)):
                ds[:] = []
                continue
        (dst / rel).mkdir(parents=True, exist_ok=True)
        for f in fs:
            p = pathlib.Path(d) / f
            q = dst / rel / f
            if p.is_symlink():
                os.symlink(os.readlink(p), q)
            else:
                shutil.copy2(p, q)
                n += 1
    return n


def sub1(path: pathlib.Path, old: str, new: str, count_ok=lambda c: c >= 1) -> None:
    t = path.read_text(encoding="utf-8")
    if not count_ok(t.count(old)):
        raise RuntimeError(f"battery: `{old[:50]}` occurs {t.count(old)} times in {path.name}")
    path.write_text(t.replace(old, new, 1), encoding="utf-8")


def registry_rows(src: pathlib.Path):
    out = []
    for i, line in enumerate(src.read_text(encoding="utf-8").splitlines()):
        m = ROW_RE.match(line)
        if m and line.count("|") == 12:
            out.append((i, m.group(1), line))
    return out


def insert_before_paths(src: pathlib.Path, row: str) -> None:
    t = src.read_text(encoding="utf-8").splitlines(True)
    i = next(k for k, l in enumerate(t) if l.startswith("## Paths"))
    t.insert(i, row + "\n")
    src.write_text("".join(t), encoding="utf-8")


def cap_pointers(sc: pathlib.Path):
    out, on = [], False
    for n, line in enumerate(sc.read_text(encoding="utf-8").splitlines()):
        if line.startswith("## "):
            on = line.startswith("## Capabilities")
            continue
        if on and line.startswith("|"):
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            if len(cells) >= 4 and cells[0] not in ("Capability", "Name") and not set(cells[0]) <= set("-: "):
                for m in re.finditer(r"`([^`\n]+)`", cells[2]):
                    for tok in m.group(1).split():
                        tok = tok.strip(";,")
                        if re.match(r"^(corpus|tools)/[^\s*<>]+$", tok) and (sc.parent / tok).is_file():
                            out.append((n, tok))
    return out


# --- legs ---------------------------------------------------------------------------------------------
# each leg: (name, kind, apply(root, rnd), argv_extra, expect) ; expect = dict(rc, failed, env, status)
def mk_legs(rnd: random.Random):
    tag = lambda: "%08x" % rnd.getrandbits(32)

    def d01(root):  # duplicate registry id
        src = root / "corpus/SOURCES.md"
        i, sid, line = rnd.choice(registry_rows(src))
        insert_before_paths(src, line.replace("|", "|", 1))

    def d02(root):  # used-by path missing on disk (census E11)
        src = root / "corpus/SOURCES.md"
        rows = [r for r in registry_rows(src) if "| mined |" in r[2] and "corpus/knowledge/" in r[2].split("|")[11]]
        i, sid, line = rnd.choice(rows)
        cells = line.split("|")
        cells[11] = " corpus/knowledge/missing-%s.md " % tag()
        t = src.read_text(encoding="utf-8").splitlines(True)
        t[i] = "|".join(cells) + "\n"
        src.write_text("".join(t), encoding="utf-8")

    def d03(root):  # status enum violation (census E07)
        src = root / "corpus/SOURCES.md"
        i, sid, line = rnd.choice([r for r in registry_rows(src) if "| mined |" in r[2]])
        t = src.read_text(encoding="utf-8").splitlines(True)
        t[i] = line.replace("| mined |", "| watch |", 1) + "\n"
        src.write_text("".join(t), encoding="utf-8")

    def d04(root):  # a knowledge entry nobody indexed
        (root / f"corpus/knowledge/zz-{tag()}-r63.md").write_text(
            "# Added entry\n\nsource: S001\nverified-at: 2026-10-28\nrecheck: 365d\n\nBody.\n", encoding="utf-8")

    def d05(root):  # an indexed entry loses its index mention
        names = sorted(f.name for f in (root / "corpus/knowledge").glob("*.md"))
        nm = rnd.choice(names)
        p = root / "corpus/README.md"
        p.write_text(p.read_text(encoding="utf-8").replace(nm, nm[:-3] + ".gone"), encoding="utf-8")

    def d06(root):  # a lesson loses its Gate heading
        ls = sorted(f for f in (root / "corpus/lessons").glob("round-*.md") if re.fullmatch(r"round-\d+\.md", f.name))
        f = rnd.choice(ls)
        t = f.read_text(encoding="utf-8")
        f.write_text(re.sub(r"^## Gate\b", "## Door", t, flags=re.M), encoding="utf-8")

    def d07(root):  # SHONEN pointer to a file that does not exist
        sub1(root / "SHONEN.md", "corpus/knowledge/metadata-screen-r25.md", "corpus/knowledge/metadata-screen-r25-%s.md" % tag())

    def d15(root):  # a SHONEN span holds two paths, the first present and the second not
        p = root / "SHONEN.md"
        p.write_text(p.read_text(encoding="utf-8") + "- [~] fixture box\n  `corpus/README.md corpus/knowledge/zz-%s-missing.md`\n" % tag(), encoding="utf-8")

    def d08(root):  # SCORECARD capability evidence names a file that does not exist
        sc = root / "SCORECARD.md"
        n, tok = rnd.choice(cap_pointers(sc))
        t = sc.read_text(encoding="utf-8").splitlines(True)
        base, ext = os.path.splitext(tok)
        cells = t[n].split("|")
        cells[3] = cells[3].replace(tok, f"{base}-{tag()}{ext}", 1)
        t[n] = "|".join(cells)
        sc.write_text("".join(t), encoding="utf-8")

    def d09(root):  # the freeze-check selftest breaks
        sub1(root / "tools/freeze-check.py", "{64}(?![0-9A-Fa-f])", "{65}(?![0-9A-Fa-f])")

    def d10(root):  # the assimilate-rows selftest breaks
        sub1(root / "tools/assimilate-rows.py", 'if l.startswith("REFUSED ")]', 'if l.startswith("REFUSEDX ")]')

    def d11(root):  # two defects in two gates at once
        d01(root)
        d04(root)

    def nothing(root):
        pass

    def d13(root):
        pass

    def b01(root):  # a valid new registry row
        src = root / "corpus/SOURCES.md"
        ids = [int(r[1][1:]) for r in registry_rows(src)]
        sid = "S%d" % (max(ids) + 1 + rnd.randrange(50))
        insert_before_paths(src, f"| {sid} | Battery fixture {tag()} — https://example.invalid/{tag()} | docs | B | a battery fixture scope {tag()} "
                                  f"| section {tag()}, revision 1 | a fixture row the battery adds | queued | 2026-10-28 | 180d | — |")

    def b02(root):  # a valid new knowledge entry, indexed
        nm = f"zz-{tag()}-r63.md"
        (root / "corpus/knowledge" / nm).write_text(
            "# Added entry\n\nsource: S001\nverified-at: 2026-10-28\nrecheck: 365d\n\nBody.\n", encoding="utf-8")
        p = root / "corpus/README.md"
        p.write_text(p.read_text(encoding="utf-8") + f"\n- `knowledge/{nm}` (battery)\n", encoding="utf-8")

    def b03(root):  # a valid new lesson
        (root / f"corpus/lessons/round-{900 + rnd.randrange(90)}.md").write_text(
            "# Round fixture\n\n## Gate — fixture\n\nNothing.\n", encoding="utf-8")

    def b04(root):  # a valid new SHONEN line, with a line-suffixed pointer
        p = root / "SHONEN.md"
        p.write_text(p.read_text(encoding="utf-8") + "- [~] fixture box\n  `corpus/README.md:3`; `SKILL.md`\n", encoding="utf-8")

    def b05(root):  # a valid new capability row
        p = root / "SCORECARD.md"
        p.write_text(p.read_text(encoding="utf-8") + "\n## Capabilities (fixture)\n\n| Capability | What | Evidence | Round |\n|---|---|---|---:|\n"
                     f"| fixture {tag()} | runs | `python3 tools/freeze-check.py --selftest`; `corpus/README.md` | 99 |\n", encoding="utf-8")

    def b06(root):  # edits to files no gate reads or selftests do not touch
        p = root / "tools/quote-reopen.py"
        p.write_text(p.read_text(encoding="utf-8") + "\n# battery benign edit %s\n" % tag(), encoding="utf-8")
        q = root / "corpus/README.md"
        q.write_text(q.read_text(encoding="utf-8").replace("\n", "\n", 1) + "\n", encoding="utf-8")
        (root / "LOG.md").write_text((root / "LOG.md").read_text(encoding="utf-8") + "\nbattery benign line\n", encoding="utf-8")

    S = ["--skip", "G08"]
    legs = [
        ("CLEAN", "clean", nothing, S, dict(rc=0, failed=set(), env=set())),
        ("D01", "defect", d01, S, dict(rc=1, failed={"G01"}, env=set())),
        ("D02", "defect", d02, S, dict(rc=1, failed={"G01"}, env=set())),
        ("D03", "defect", d03, S, dict(rc=1, failed={"G01"}, env=set())),
        ("D04", "defect", d04, S, dict(rc=1, failed={"G02"}, env=set())),
        ("D05", "defect", d05, S, dict(rc=1, failed={"G02"}, env=set())),
        ("D06", "defect", d06, S, dict(rc=1, failed={"G03"}, env=set())),
        ("D07", "defect", d07, S, dict(rc=1, failed={"G04"}, env=set())),
        ("D08", "defect", d08, S, dict(rc=1, failed={"G05"}, env=set())),
        ("D09", "defect", d09, S, dict(rc=1, failed={"G06"}, env=set())),
        ("D10", "defect", d10, S, dict(rc=1, failed={"G07"}, env=set())),
        ("D11", "defect", d11, S, dict(rc=1, failed={"G01", "G02"}, env=set())),
        ("D12", "defect", nothing, S + ["--fleet", "@EMPTY@"], dict(rc=2, failed=set(), env={"G01"})),
        ("D13", "defect", d13, ["--skip", "G99"], dict(rc=2, usage=True)),
        ("D14", "defect", d06, ["--only", "G03"], dict(rc=1, failed={"G03"}, env=set(), only={"G03"})),
        ("D15", "defect", d15, S, dict(rc=1, failed={"G04"}, env=set())),
        ("B01", "benign", b01, S, dict(rc=0, failed=set(), env=set())),
        ("B02", "benign", b02, S, dict(rc=0, failed=set(), env=set())),
        ("B03", "benign", b03, S, dict(rc=0, failed=set(), env=set())),
        ("B04", "benign", b04, S, dict(rc=0, failed=set(), env=set())),
        ("B05", "benign", b05, S, dict(rc=0, failed=set(), env=set())),
        ("B06", "benign", b06, S, dict(rc=0, failed=set(), env=set())),
    ]
    return legs


def judge(name, exp, rc, out, err):
    """Return (ok, why)."""
    if exp.get("usage"):
        ok = rc == 2 and not any(l.startswith("PREFLIGHT=") for l in out.splitlines())
        return ok, f"rc={rc} (want 2, no PREFLIGHT line)"
    lines = out.splitlines()
    gates = {}
    order = []
    for l in lines:
        m = GATE_RE.match(l)
        if m:
            if m.group(1) in gates:
                return False, f"gate {m.group(1)} printed twice"
            gates[m.group(1)] = m.group(3)
            order.append(m.group(1))
    sums = [SUM_RE.match(l) for l in lines if l.startswith("PREFLIGHT=")]
    if len(sums) != 1 or sums[0] is None:
        return False, f"rc={rc} summary lines={len(sums)}"
    s = sums[0]
    if rc != exp["rc"]:
        return False, f"rc={rc} want {exp['rc']}"
    only = exp.get("only")
    want_ids = [g for g in IDS]
    if order != want_ids:
        return False, f"gate lines {','.join(order)}"
    ran = [g for g in IDS if gates[g] != "SKIP"]
    expect_ran = [g for g in IDS if (g in only if only else g != "G08")]
    if ran != expect_ran:
        return False, f"ran {','.join(ran)} want {','.join(expect_ran)}"
    passed = [g for g in ran if gates[g] == "PASS"]
    failed = {g for g in ran if gates[g] == "FAIL"}
    envs = {g for g in ran if gates[g] == "ENV"}
    if failed != exp["failed"] or envs != exp["env"]:
        return False, f"FAIL={sorted(failed)} ENV={sorted(envs)} want FAIL={sorted(exp['failed'])} ENV={sorted(exp['env'])}"
    if int(s.group(1)) != len(passed) or int(s.group(2)) != len(ran):
        return False, f"summary {s.group(1)}/{s.group(2)} but lines say {len(passed)}/{len(ran)}"
    f2 = set(s.group(3).split(",")) - {"none"}
    e2 = set(s.group(4).split(",")) - {"none"}
    sk = set(s.group(5).split(",")) - {"none"}
    if f2 != failed or e2 != envs or sk != {g for g in IDS if gates[g] == "SKIP"}:
        return False, f"summary sets FAILED={sorted(f2)} ENV={sorted(e2)} SKIPPED={sorted(sk)} disagree with lines"
    return True, "ok"


def run_leg(leg, ctx):
    name, kind, _unused, extra, exp = leg
    golden, work, tool_bytes, fleet, seed = ctx
    apply = next(l[2] for l in mk_legs(random.Random(f"{seed}/{name}")) if l[0] == name)
    r = random.Random(f"{seed}/{name}/dirs")
    vdir = work / ("v-%08x" % r.getrandbits(32)) / "lane"
    shutil.copytree(golden, vdir, symlinks=True)
    cwd = work / ("c-%08x" % r.getrandbits(32))
    tooldir = work / ("t-%08x" % r.getrandbits(32))
    cwd.mkdir()
    tooldir.mkdir()
    tool = tooldir / ("%s.py" % ("x%08x" % r.getrandbits(32)))
    tool.write_bytes(tool_bytes)
    try:
        apply(vdir)
        argv = [a if a != "@EMPTY@" else str(cwd) for a in extra]
        if "--fleet" not in argv:
            argv += ["--fleet", str(fleet)]
        env = {"PATH": os.environ.get("PATH", "/usr/bin:/bin"), "LC_ALL": "C.UTF-8", "HOME": str(cwd),
               "TMPDIR": str(work / "tmp"), "HYAKU_SCRATCH": str(work / "tmp")}
        p = subprocess.run([sys.executable, "-B", str(tool), "--root", str(vdir)] + argv, cwd=cwd, env=env,
                           capture_output=True, text=True, timeout=600, stdin=subprocess.DEVNULL)
        ok, why = judge(name, exp, p.returncode, p.stdout, p.stderr)
    except subprocess.TimeoutExpired:
        ok, why = False, "timeout"
    except Exception as e:  # a battery error is not a tool verdict
        ok, why = False, f"battery-error {type(e).__name__}: {e}"
    finally:
        shutil.rmtree(vdir.parent, ignore_errors=True)
        shutil.rmtree(cwd, ignore_errors=True)
        shutil.rmtree(tooldir, ignore_errors=True)
    return name, kind, ok, why


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--tool", required=True)
    ap.add_argument("--work", required=True)
    ap.add_argument("--lane", default=str(LANE))
    ap.add_argument("--fleet", default=None)
    ap.add_argument("--jobs", type=int, default=4)
    ap.add_argument("--only", default=None)
    a = ap.parse_args()
    lane = pathlib.Path(a.lane).resolve()
    fleet = pathlib.Path(a.fleet) if a.fleet else lane.parent
    tool = pathlib.Path(a.tool)
    if not (fleet / "scripts" / "sources-census.sh").is_file():
        print(f"c1-battery: no census script under {fleet}/scripts (pass --fleet DIR)", file=sys.stderr)
        return 2
    work = pathlib.Path(a.work)
    if work.exists() and any(work.iterdir()):
        print("c1-battery: --work must be absent or empty", file=sys.stderr)
        return 2
    if os.geteuid() == 0:
        print("c1-battery: refusing to run as root", file=sys.stderr)
        return 2
    work.mkdir(parents=True, exist_ok=True)
    (work / "tmp").mkdir()
    seed = os.environ.get("C1_SEED") or os.urandom(8).hex()
    try:
        if not tool.is_file():
            print(f"c1-battery: tool {tool} absent", file=sys.stderr)
            print("CLEAN=0/1 DEFECTS=0/15 BENIGN=0/6 BATTERY=FAIL")
            return 1
        golden = work / "golden"
        golden.mkdir()
        n = build_golden(lane, golden)
        if n < 1000:
            print(f"c1-battery: golden copy has only {n} files", file=sys.stderr)
            return 2
        legs = mk_legs(random.Random(f"{seed}/legs"))
        if a.only:
            want = set(a.only.split(","))
            legs = [l for l in legs if l[0] in want]
        ctx = (golden, work, tool.read_bytes(), fleet, seed)
        with concurrent.futures.ThreadPoolExecutor(max_workers=max(1, a.jobs)) as ex:
            res = list(ex.map(lambda l: run_leg(l, ctx), legs))
        for name, kind, ok, why in res:
            print(f"LEG {name} {kind} {'ok' if ok else 'FAIL'} {why}")
        by = lambda k: [r for r in res if r[1] == k]
        c, d, b = by("clean"), by("defect"), by("benign")
        line = f"CLEAN={sum(r[2] for r in c)}/1 DEFECTS={sum(r[2] for r in d)}/15 BENIGN={sum(r[2] for r in b)}/6"
        if a.only:
            print(line + " BATTERY=PARTIAL")
            return 0
        good = len(c) == 1 and c[0][2] and all(r[2] for r in d) and len(d) == 15 and all(r[2] for r in b) and len(b) == 6
        print(line + f" BATTERY={'PASS' if good else 'FAIL'}")
        return 0 if good else 1
    finally:
        shutil.rmtree(work, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main())

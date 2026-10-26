#!/usr/bin/env python3
"""c1-count — frozen counter for round 53 claim C1 (operability, capability extension).

Predicate R53-C1, the same sentence as corpus/evidence/round53/claims.md:
`tools/assimilate-rows.py`, run as an ordinary command with `--entry`, labels a
cited staged row `held` in `renumber.tsv` only when a lane Registry row already
carries its URL and `twin` when an earlier-cited staged row of the same run was
minted a lane id for that URL (the same lane id, nothing appended), and its
count line carries `HELD=<held rows>` and `TWIN=<twin rows>`; it validates the
recheck of every cited staged row, held and twin rows included, and refuses
(exit 1, a stderr line starting `REFUSED <staged id>: recheck`, no
`renumber.tsv` and no `append.md`) when one has no leading calendar-valid date
or `NNd`; a registry it cannot continue from (no `## Registry` heading, or an
`S###` row outside the Registry section) is refused with exit 1 and every
registry `REFUSED` line printed before any entry `REFUSED` line, and is
refused also when no `--entry` is given, while a sound registry with no
`--entry` still exits 0 — counted as legs over packages generated at counting
time from fresh random ids, hosts, paths, entry names and recheck values with
randomised representation (0-3 leading spaces on registry rows, `##` followed
by a space or a tab, http or https, a trailing `/`, an upper-case host), plus
REAL (the three round-53 staged entries of the read-only campaign package
against the registry at BASE_REV: S134 S185 S186 S190 S193 append as S117
S118 S119 S120 S121, S195 is `twin` of S118, `HELD=0 TWIN=1`) and REGRESS (the
round-50 pinned self-test passes with its pinned digest and the round-51 frozen
counter prints `LEGS=5/5` for the same tool).

Legs: TWIN, HELD, MIX, RECHECK, ORDER, NOENTRY, REAL, REGRESS -> `LEGS=8/8` and
`C1=PASS` exit 0. Each generated leg runs `--per-leg K` packages (default 3)
and passes only when every package passes.

Usage: python3 corpus/evidence/round53/c1-count.py [--tool PATH] [--seed N]
       [--per-leg K] [--work DIR]
Scratch: under --work, else a fresh directory under $TMPDIR (tempfile), removed
on exit. Writes nothing in the lane. Exit 0 every leg holds · 1 a leg failed ·
2 env (campaign package or round-50 fixtures changed or missing; git failure).
"""
from __future__ import annotations

import argparse
import hashlib
import os
import pathlib
import random
import re
import shutil
import subprocess
import sys
import tempfile

LANE = pathlib.Path(__file__).resolve().parents[3]
BASE_REV = "5b550133d79bc09c82d8965cce2e48c2598b8c3e"
PKG = pathlib.Path("/home/vgpnk/Projects/shokuknow/merge/chousa")
REAL_ENTRIES = ("corpus/knowledge/search-tracking-record-r40.md",
                "corpus/knowledge/western-instrument-alignment-r50.md",
                "corpus/knowledge/quality-control-guideline-issued-text-r48.md")
REAL_PIN = "8e6484edbff80ebe167f6378c7eb7c6214b57d4d50380a43e700386714f3689b"  # sha256 over SOURCES.append.md + the three staged entries (pin())
REAL_MAP = {"S134": ("S117", "append"), "S185": ("S118", "append"), "S186": ("S119", "append"),
            "S190": ("S120", "append"), "S193": ("S121", "append"), "S195": ("S118", "twin")}
R50_FIX = LANE / "corpus" / "evidence" / "round50" / "c1-fixtures"
R50_PIN = "c5c56480e9f6a08d6a2077b6a11267a4cabf0bc0d3f726408a9bb0238283cd43"
R51_COUNTER = LANE / "corpus" / "evidence" / "round51" / "c1-count.py"
HEAD = "| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |\n|---|---|---|---|---|---|---|---|---|---|---|\n"
OPENED = "2026-10-26"


def pin() -> str:
    """sha256 over the campaign files REAL reads (staged rows + the three entries)."""
    h = hashlib.sha256()
    for rel in ["SOURCES.append.md"] + [f"knowledge/{e}" for e in REAL_ENTRIES]:
        p = PKG / rel
        h.update(rel.encode() + b"\0" + (p.read_bytes() if p.is_file() else b"<missing>") + b"\0")
    return h.hexdigest()


def run(tool, *args, env=None):
    e = dict(os.environ if env is None else env)
    e.pop("ASSIMILATE_CITES", None)
    try:
        r = subprocess.run([sys.executable, str(tool), *args], capture_output=True, text=True, timeout=120, env=e)
        return r.returncode, r.stdout, r.stderr
    except subprocess.TimeoutExpired:
        return 124, "", "timeout"


class Gen:
    def __init__(self, rnd: random.Random):
        self.r = rnd
        self.used: set[int] = set()

    def hexs(self, n=6):
        return "".join(self.r.choice("0123456789abcdef") for _ in range(n))

    def url(self):
        return f"https://{self.hexs(5)}-{self.hexs(3)}.test/{self.hexs(4)}/{self.hexs(6)}"

    def spell(self, u):
        """A spelling of URL u with the same census identity (scheme, trailing slash, host case)."""
        m = re.match(r"https://([^/]+)(/.*)", u)
        host, path = m.group(1), m.group(2)
        scheme = self.r.choice(["http", "https"])
        if self.r.random() < 0.5:
            host = host.upper()
        if self.r.random() < 0.5:
            path += "/"
        return f"{scheme}://{host}{path}"

    def sid(self, lo=200, hi=899):
        while True:
            n = self.r.randint(lo, hi)
            if n not in self.used:
                self.used.add(n)
                return f"S{n:03d}"

    def recheck_ok(self):
        return self.r.choice(["90d", "180d", "365d", f"2027-0{self.r.randint(1, 9)}-1{self.r.randint(0, 9)}",
                              f"{self.r.randint(30, 400)}d — re-verify {self.hexs(4)}"])

    def recheck_bad(self):
        y = self.r.randint(2025, 2029)
        d = self.r.choice([f"{y}-02-30", f"{y}-13-0{self.r.randint(1, 9)}", f"{y}-04-31", f"{y}-00-1{self.r.randint(0, 9)}"])
        return d + self.r.choice(["", f" — re-verify {self.hexs(4)}"])

    def staged_row(self, sid, url, recheck):
        return f"| {sid} | Doc {self.hexs(4)} — {url} | docs | A | scope {self.hexs(3)} | section {self.hexs(3)} | teaches {self.hexs(5)} | mined | 2026-10-2{self.r.randint(0, 5)} | {recheck} | — |"

    def registry(self, nrows, carried=(), sound=True, row_outside=False):
        """(text, {url: lane id}, max id). carried urls get registry rows."""
        n = max(nrows, len(carried) + 1)
        ids = [f"S{i:03d}" for i in range(1, n + 1)]
        urls = {}
        rows = []
        car = list(carried)
        slots = self.r.sample(range(n), len(car))
        for i, lid in enumerate(ids):
            u = car[slots.index(i)] if i in slots else self.url()
            if i in slots:
                urls[u] = lid
            ind = " " * self.r.randint(0, 3)
            cell = self.spell(u)
            rows.append(f"{ind}| {lid} | Lane doc {self.hexs(3)} — {cell} | docs | A | lane | s1 | lane row | mined | 2026-01-0{self.r.randint(1, 9)} | 90d | — |")
        sep = self.r.choice([" ", "\t"])
        heading = f"##{sep}Registry" if sound else f"##{sep}{self.r.choice(['Rows', 'Register', 'Table'])} {self.hexs(3)}"
        pre = ""
        if row_outside:
            stray = f"| S{n + 50 + self.r.randint(0, 40):03d} | Stray — {self.url()} | docs | A | x | x | x | mined | 2026-01-01 | 90d | — |\n\n"
            pre = "## Notes\n\n" + stray
        text = f"# Sources {self.hexs(3)}\n\n{pre}{heading}\n\n{HEAD}" + "\n".join(rows) + "\n"
        return text, urls, n


def write_pkg(d: pathlib.Path, registry: str, staged_rows: list[str], entries: dict[str, list[tuple[str, str]]]):
    (d / "knowledge" / "corpus" / "knowledge").mkdir(parents=True, exist_ok=True)
    (d / "registry.md").write_text(registry, encoding="utf-8")
    (d / "staged.md").write_text("## Staged\n\n" + HEAD + "\n".join(staged_rows) + "\n", encoding="utf-8")
    for name, cites in entries.items():
        body = "".join(f"source: {s} — {u} — section\n" for s, u in cites)
        (d / "knowledge" / "corpus" / "knowledge" / name).write_text(f"# {name}\n\n{body}verified-at: 2026-10-26\n\n#### Observation\n\n- x\n", encoding="utf-8")


def invoke(tool, d: pathlib.Path, entries: list[str]):
    out = d / "out"
    args = ["--staged", str(d / "staged.md"), "--knowledge", str(d / "knowledge"), "--registry", str(d / "registry.md"),
            "--opened", OPENED, "--out", str(out)] + sum((["--entry", e] for e in entries), [])
    rc, so, se = run(tool, *args)
    return rc, so, se, out


def read_map(out: pathlib.Path):
    p = out / "renumber.tsv"
    if not p.is_file():
        return None
    m = {}
    for line in p.read_text(encoding="utf-8").splitlines()[1:]:
        f = line.split("\t")
        if len(f) >= 3:
            m[f[0]] = (f[1], f[2])
    return m


def n_rows(out: pathlib.Path):
    p = out / "append.md"
    return sum(1 for l in p.read_text(encoding="utf-8").splitlines() if l.startswith("| S")) if p.is_file() else -1


def counts_ok(so: str, held: int, twin: int) -> bool:
    return bool(re.search(rf"(^|\s)HELD={held}(\s|$)", so)) and bool(re.search(rf"(^|\s)TWIN={twin}(\s|$)", so))


def expect(cited: list[tuple[str, str]], reg_urls: dict[str, str], maxid: int):
    """Expected map by the predicate: ascending staged id; held / twin / append."""
    norm = lambda u: re.sub(r"^[a-z]+://", "", u.lower().rstrip("/"))
    held = {norm(u): l for u, l in reg_urls.items()}
    minted, m, nxt = {}, {}, maxid + 1
    for sid, u in sorted(cited, key=lambda x: int(x[0][1:])):
        k = norm(u)
        if k in held:
            m[sid] = (held[k], "held")
        elif k in minted:
            m[sid] = (minted[k], "twin")
        else:
            minted[k] = f"S{nxt:03d}"
            m[sid] = (minted[k], "append")
            nxt += 1
    return m


def case_mapped(g: Gen, tool, d: pathlib.Path, n_held_urls: int, held_per: int, twin_urls: int, single_urls: int):
    held_urls = [g.url() for _ in range(n_held_urls)]
    reg, reg_urls, maxid = g.registry(g.r.randint(3, 9), carried=held_urls)
    cited: list[tuple[str, str]] = []
    rows = []
    for u in held_urls:
        for _ in range(held_per):
            s = g.sid()
            cited.append((s, u))
            rows.append(g.staged_row(s, g.spell(u), g.recheck_ok()))
    for _ in range(twin_urls):
        u = g.url()
        for _ in range(2):
            s = g.sid()
            cited.append((s, u))
            rows.append(g.staged_row(s, g.spell(u), g.recheck_ok()))
    for _ in range(single_urls):
        u = g.url()
        s = g.sid()
        cited.append((s, u))
        rows.append(g.staged_row(s, g.spell(u), g.recheck_ok()))
    g.r.shuffle(rows)
    # spread citations over two entries with random names; one entry may cite a staged id twice-free
    names = [f"e{g.hexs(5)}.md", f"f{g.hexs(5)}.md"]
    ents = {names[0]: [], names[1]: []}
    for s, u in cited:
        ents[g.r.choice(names)].append((s, g.spell(u)))
    ents = {k: v for k, v in ents.items() if v}
    write_pkg(d, reg, rows, ents)
    rc, so, se, out = invoke(tool, d, [f"corpus/knowledge/{k}" for k in ents])
    want = expect(cited, reg_urls, maxid)
    got = read_map(out)
    nh = sum(1 for v in want.values() if v[1] == "held")
    nt = sum(1 for v in want.values() if v[1] == "twin")
    na = sum(1 for v in want.values() if v[1] == "append")
    ok = rc == 0 and got == want and counts_ok(so, nh, nt) and n_rows(out) == na
    return ok, f"rc={rc} held={nh} twin={nt} append={na} map={'ok' if got == want else 'differs'} rows={n_rows(out)}"


def case_recheck(g: Gen, tool, d: pathlib.Path):
    """The invalid recheck sits on a held row or on a twin row (chosen at random)."""
    on = g.r.choice(["held", "twin"])
    hu = g.url()
    reg, reg_urls, _mx = g.registry(g.r.randint(3, 8), carried=[hu])
    tu = g.url()
    a, b, c = g.sid(200, 499), g.sid(500, 899), g.sid()
    bad = c if on == "held" else b
    rows = [g.staged_row(a, g.spell(tu), g.recheck_ok()), g.staged_row(b, g.spell(tu), g.recheck_bad() if bad == b else g.recheck_ok()),
            g.staged_row(c, g.spell(hu), g.recheck_bad() if bad == c else g.recheck_ok())]
    g.r.shuffle(rows)
    name = f"r{g.hexs(5)}.md"
    write_pkg(d, reg, rows, {name: [(a, tu), (b, tu), (c, hu)]})
    rc, so, se, out = invoke(tool, d, [f"corpus/knowledge/{name}"])
    line = any(l.startswith(f"REFUSED {bad}: recheck") for l in se.splitlines())
    ok = rc == 1 and line and not (out / "renumber.tsv").exists() and not (out / "append.md").exists()
    return ok, f"on={on} rc={rc} refused-line={line} renumber={(out / 'renumber.tsv').exists()} append={(out / 'append.md').exists()}"


def case_order(g: Gen, tool, d: pathlib.Path):
    kind = g.r.choice(["no-heading", "row-outside"])
    reg, _u, _m = g.registry(g.r.randint(2, 6), sound=(kind != "no-heading"), row_outside=(kind == "row-outside"))
    s, u = g.sid(), g.url()
    good, missing = f"g{g.hexs(5)}.md", f"m{g.hexs(5)}.md"
    write_pkg(d, reg, [g.staged_row(s, u, g.recheck_ok())], {good: [(s, u)]})
    order = [f"corpus/knowledge/{missing}", f"corpus/knowledge/{good}"]
    g.r.shuffle(order)
    rc, so, se, out = invoke(tool, d, order)
    ref = [l for l in se.splitlines() if l.startswith("REFUSED ")]
    regi = [i for i, l in enumerate(ref) if "registry" in l]
    enti = [i for i, l in enumerate(ref) if "entry missing" in l]
    ok = rc == 1 and bool(regi) and bool(enti) and max(regi) < min(enti) and not (out / "renumber.tsv").exists()
    return ok, f"kind={kind} rc={rc} refused={len(ref)} registry-first={bool(regi) and bool(enti) and max(regi) < min(enti)}"


def case_noentry(g: Gen, tool, d: pathlib.Path):
    kind = g.r.choice(["no-heading", "row-outside"])
    reg, _u, _m = g.registry(g.r.randint(2, 6), sound=(kind != "no-heading"), row_outside=(kind == "row-outside"))
    s, u = g.sid(), g.url()
    write_pkg(d, reg, [g.staged_row(s, u, g.recheck_ok())], {})
    rc, so, se, _o = invoke(tool, d, [])
    bad_ok = rc == 1 and any(l.startswith("REFUSED ") and "registry" in l for l in se.splitlines())
    d2 = d.parent / (d.name + "-sound")
    sreg, _u2, _m2 = g.registry(g.r.randint(2, 6))
    write_pkg(d2, sreg, [g.staged_row(s, u, g.recheck_ok())], {})
    rc2, so2, se2, _o2 = invoke(tool, d2, [])
    sound_ok = rc2 == 0 and not any(l.startswith("REFUSED") for l in se2.splitlines())
    return bad_ok and sound_ok, f"kind={kind} broken-rc={rc} sound-rc={rc2}"


def leg_real(tool, work: pathlib.Path):
    base = subprocess.run(["git", "-C", str(LANE), "show", f"{BASE_REV}:corpus/SOURCES.md"], capture_output=True)
    if base.returncode != 0:
        return None, "git show failed"
    reg = work / "real-registry.md"
    reg.write_bytes(base.stdout)
    out = work / "real-out"
    rc, so, se = run(tool, "--staged", str(PKG / "SOURCES.append.md"), "--knowledge", str(PKG / "knowledge"),
                     "--registry", str(reg), "--opened", OPENED, "--out", str(out),
                     *sum((["--entry", e] for e in REAL_ENTRIES), []))
    got = read_map(out)
    ok = rc == 0 and got == REAL_MAP and counts_ok(so, 0, 1) and n_rows(out) == 5
    return ok, f"rc={rc} map={'ok' if got == REAL_MAP else got} rows={n_rows(out)} count-line={[l for l in so.splitlines() if 'CITED=' in l]}"


def leg_regress(tool, work: pathlib.Path):
    rc, so, se = run(tool, "--selftest", "--cites", "all", "--fixtures", str(R50_FIX), "--expected", str(R50_FIX / "expected.json"))
    pin_ok = f"FIXTURES_SHA256={R50_PIN}" in so and "SELFTEST=PASS" in so and rc == 0
    e = dict(os.environ)
    e["TMPDIR"] = str(work)
    r = subprocess.run([sys.executable, str(R51_COUNTER), "--tool", str(tool), "--seed", "53"], capture_output=True, text=True, env=e, timeout=600)
    r51_ok = r.returncode == 0 and "LEGS=5/5" in r.stdout
    return pin_ok and r51_ok, f"r50-pin={'ok' if pin_ok else 'FAIL'} r51-counter={'LEGS=5/5' if r51_ok else 'FAIL rc=%d' % r.returncode}"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--tool", default=str(LANE / "tools" / "assimilate-rows.py"))
    ap.add_argument("--seed", type=int)
    ap.add_argument("--per-leg", type=int, default=3)
    ap.add_argument("--work")
    a = ap.parse_args()
    tool = pathlib.Path(a.tool).resolve()
    if pin() != REAL_PIN or not (R50_FIX / "expected.json").is_file() or not R51_COUNTER.is_file():
        print(f"ENV_CHANGED real-pin={pin()} (want {REAL_PIN})")
        return 2
    seed = a.seed if a.seed is not None else random.SystemRandom().randrange(1 << 30)
    rnd = random.Random(seed)
    g = Gen(rnd)
    own = a.work is None
    work = pathlib.Path(tempfile.mkdtemp(prefix=f"r53c1-{g.hexs(8)}-")) if own else pathlib.Path(a.work)
    work.mkdir(parents=True, exist_ok=True)
    print(f"SEED={seed}" if a.seed is not None else "SEED=unseeded")
    if not tool.is_file():
        print(f"TOOL=absent {tool}")
    legs = {}
    try:
        gens = {
            "TWIN": lambda d: case_mapped(g, tool, d, 0, 0, g.r.randint(1, 2), g.r.randint(1, 2)),
            "HELD": lambda d: case_mapped(g, tool, d, g.r.randint(1, 2), g.r.randint(1, 2), 0, g.r.randint(1, 2)),
            "MIX": lambda d: case_mapped(g, tool, d, g.r.randint(1, 2), 2, g.r.randint(1, 2), g.r.randint(0, 2)),
            "RECHECK": lambda d: case_recheck(g, tool, d),
            "ORDER": lambda d: case_order(g, tool, d),
            "NOENTRY": lambda d: case_noentry(g, tool, d),
        }
        for leg, fn in gens.items():
            res = []
            for k in range(a.per_leg):
                d = work / f"{g.hexs(10)}"
                d.mkdir()
                ok, note = fn(d) if tool.is_file() else (False, "no tool")
                res.append(ok)
                print(f"{leg} case{k + 1} {'PASS' if ok else 'FAIL'} {note}")
            legs[leg] = all(res)
        if tool.is_file():
            ok, note = leg_real(tool, work)
            if ok is None:
                print(f"ENV {note}")
                return 2
            legs["REAL"] = ok
            print(f"REAL {'PASS' if ok else 'FAIL'} {note}")
            ok, note = leg_regress(tool, work)
            legs["REGRESS"] = ok
            print(f"REGRESS {'PASS' if ok else 'FAIL'} {note}")
        else:
            legs["REAL"] = legs["REGRESS"] = False
        for leg in ("TWIN", "HELD", "MIX", "RECHECK", "ORDER", "NOENTRY", "REAL", "REGRESS"):
            print(f"{leg}={'PASS' if legs.get(leg) else 'FAIL'}")
        n = sum(1 for v in legs.values() if v)
        print(f"LEGS={n}/8")
        print("C1=PASS" if n == 8 else "C1=FAIL")
        return 0 if n == 8 else 1
    finally:
        if own:
            shutil.rmtree(work, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main())

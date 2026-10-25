#!/usr/bin/env python3
"""c1-count — frozen counter for round 51 claim C1 (operability, capability extension).

Predicate R51-C1, the same sentence as corpus/evidence/round51/claims.md:
`tools/assimilate-rows.py`, run as an ordinary command (not `--selftest`) on
packages this counter GENERATES at counting time from fresh random hosts and
ids, (S) cites only the ids on the entries' `source:` lines — an id an entry
mentions only in its body is neither renumbered nor appended, is left in the
entry text unchanged and is listed in `bodyonly.tsv` (`entry<TAB>staged id`) and
as `BODYONLY=<n>` on stdout — while `--cites all` keeps the round-50 behaviour;
(D1) takes a staged row's document identity from its source cell AFTER the
escaped-pipe rewrite, so a staged row whose URL is followed by `\\| alt` maps to
the registry row that holds the URL (`held`, nothing appended); (D2) reads a
registry row's source cell with the escaped-pipe splitter, so a registry source
cell `Title \\| alt — URL` still holds URL; (D3) refuses (exit 1, a `REFUSED`
stderr line, no `renumber.tsv` and no `append.md`) a registry that has no
`## Registry` heading or that carries an `S###` row outside the Registry
section, and on a well-formed registry appends from the maximum id + 1; and the
round-50 pinned fixture package, run as `--selftest --fixtures <pinned>
--expected <pinned> --cites all`, still passes with 26 findings and its pinned
digest, and the lane default `--selftest` (no flags) passes.

Legs: SELFTEST_DEFAULT, LEGACY_ALL, SOURCE_ONLY (S), PIPE_IDENTITY (D1+D2),
REGISTRY_STRUCTURE (D3) — `LEGS=5/5` and `C1=PASS` exit 0. The nonce is the
point: a tool that recognises this counter's inputs cannot (round-50 critic
CritForgeC1: a 42-line forge passed the frozen round-50 counter).

Usage: python3 corpus/evidence/round51/c1-count.py [--tool PATH] [--root LANE] [--seed N]
(`--tool` other than the lane's skips SELFTEST_DEFAULT). Exit 0 every leg holds ·
1 a leg failed · 2 env (round-50 pinned fixtures changed or missing).
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
R50_FIX = LANE / "corpus" / "evidence" / "round50" / "c1-fixtures"
R50_PIN = "c5c56480e9f6a08d6a2077b6a11267a4cabf0bc0d3f726408a9bb0238283cd43"
HEAD = "| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |\n|---|---|---|---|---|---|---|---|---|---|---|\n"


def digest(d: pathlib.Path) -> str:
    h = hashlib.sha256()
    for p in sorted(q for q in d.rglob("*") if q.is_file()):
        h.update(p.relative_to(d).as_posix().encode() + b"\0" + p.read_bytes() + b"\0")
    return h.hexdigest()


def run(tool: pathlib.Path, *args: str) -> tuple[int, str, str]:
    try:
        r = subprocess.run([sys.executable, str(tool), *args], capture_output=True, text=True, timeout=120)
    except subprocess.TimeoutExpired:
        return 124, "", "timeout"
    return r.returncode, r.stdout, r.stderr


def row(sid: str, source: str, used: str = "—", status: str = "mined", opened: str = "2026-10-23", recheck: str = "90d") -> str:
    return f"| {sid} | {source} | docs | B | scope {sid} | section {sid} | what {sid} teaches | {status} | {opened} | {recheck} | {used} |\n"


def registry(rows: list[str], heading: str = "## Registry", extra: str = "") -> str:
    return f"# SOURCES — where nonce learns\n\n{heading}\n\n{HEAD}" + "".join(rows) + extra


def adopt(tool: pathlib.Path, work: pathlib.Path, reg: str, staged_rows: list[str], entry: str, *flags: str):
    for sub in ("knowledge/corpus/knowledge", "out"):
        (work / sub).mkdir(parents=True, exist_ok=True)
    (work / "registry.md").write_text(reg, encoding="utf-8")
    (work / "staged.md").write_text("# staged\n\n" + HEAD + "".join(staged_rows), encoding="utf-8")
    (work / "knowledge/corpus/knowledge/e.md").write_text(entry, encoding="utf-8")
    rc, out, err = run(tool, "--staged", str(work / "staged.md"), "--knowledge", str(work / "knowledge"),
                       "--registry", str(work / "registry.md"), "--opened", "2026-10-25", "--out", str(work / "out"),
                       "--entry", "corpus/knowledge/e.md", *flags)
    return rc, out, err


def tsv(path: pathlib.Path) -> list[list[str]]:
    return [l.split("\t") for l in path.read_text(encoding="utf-8").splitlines()[1:]] if path.is_file() else []


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--tool")
    ap.add_argument("--root", default=str(LANE))
    ap.add_argument("--seed", type=int)
    a = ap.parse_args()
    root = pathlib.Path(a.root)
    tool = pathlib.Path(a.tool) if a.tool else root / "tools" / "assimilate-rows.py"
    if not R50_FIX.is_dir() or digest(R50_FIX) != R50_PIN:
        print("PIN_CHANGED the round-50 pinned fixtures differ from their pin or are missing")
        return 2
    rnd = random.Random(a.seed if a.seed is not None else int.from_bytes(os.urandom(8), "big"))
    legs: dict[str, bool] = {}

    # 1 lane default
    if a.tool is None:
        rc, out, _ = run(tool, "--selftest")
        legs["SELFTEST_DEFAULT"] = rc == 0 and "SELFTEST=PASS" in out
    else:
        legs["SELFTEST_DEFAULT"] = True
    print(f"SELFTEST_DEFAULT={'PASS' if legs['SELFTEST_DEFAULT'] else 'FAIL'}" + (" (skipped: --tool)" if a.tool else ""))

    # 2 legacy behaviour on the round-50 pinned package
    rc, out, _ = run(tool, "--selftest", "--fixtures", str(R50_FIX), "--expected", str(R50_FIX / "expected.json"), "--cites", "all")
    m = re.search(r"^SELFTEST=PASS findings=(\d+) expected=(\d+)$", out, re.M)
    d = re.search(r"^FIXTURES_SHA256=([0-9a-f]{64})$", out, re.M)
    legs["LEGACY_ALL"] = rc == 0 and bool(m) and m.group(1) == "26" == m.group(2) and bool(d) and d.group(1) == R50_PIN
    print(f"LEGACY_ALL={'PASS' if legs['LEGACY_ALL'] else 'FAIL'} rc={rc}")

    tmp = pathlib.Path(tempfile.mkdtemp(prefix="chousa-r51-c1-"))
    try:
        n = f"{rnd.getrandbits(32):08x}"
        top = rnd.randint(12, 40)                       # highest lane id
        a_id, b_id, c_id = (f"S{rnd.randint(500, 900)}" for _ in range(3))
        while len({a_id, b_id, c_id}) < 3:
            c_id = f"S{rnd.randint(500, 900)}"
        host = f"h{n}.example.test"
        held_n = rnd.randint(1, top)

        def lane_rows(held_url: str, held_source: str | None = None) -> list[str]:
            rows = []
            for i in range(1, top + 1):
                src = f"Doc {i} — https://{host}/lane-{i}"
                if i == held_n:
                    src = held_source or f"Held — {held_url}"
                rows.append(row(f"S{i:03d}", src))
            return rows

        held_url = f"https://{host}/held-{n}"

        # 3 (S) source-only
        w = tmp / "s"
        staged = [row(a_id, f"New A — https://{host}/new-a-{n}", "corpus/knowledge/e.md"),
                  row(b_id, f"Held B — {held_url}", "corpus/knowledge/e.md"),
                  row(c_id, f"Body only C — https://{host}/new-c-{n}")]
        entry = (f"source: {a_id} — https://{host}/new-a-{n} — section\nsource: {b_id} — {held_url} — section\n"
                 f"verified-at: 2026-10-25\nrecheck: 90d\n\n# E\n\n- A says one thing ({a_id}); B another ({b_id}).\n"
                 f"- A different document is mentioned only here: {c_id}, and lane row S{held_n:03d} too.\n")
        rc, out, err = adopt(tool, w, registry(lane_rows(held_url)), staged, entry)
        ren = {r[0]: r[1:] for r in tsv(w / "out/renumber.tsv")}
        app = [l for l in (w / "out/append.md").read_text(encoding="utf-8").splitlines() if l.strip()] if (w / "out/append.md").is_file() else []
        body = (w / "out/corpus/knowledge/e.md").read_text(encoding="utf-8") if (w / "out/corpus/knowledge/e.md").is_file() else ""
        bo = tsv(w / "out/bodyonly.tsv")
        new_a = f"S{top + 1:03d}"
        ok_s = (rc == 0 and set(ren) == {a_id, b_id} and ren.get(a_id, [""])[:2] == [new_a, "append"]
                and ren.get(b_id, [""])[:2] == [f"S{held_n:03d}", "held"] and len(app) == 1 and app[0].lstrip(" |").startswith(new_a)
                and c_id in body and a_id not in body and b_id not in body and new_a in body
                and bo == [["corpus/knowledge/e.md", c_id]] and "BODYONLY=1" in out)
        w2 = tmp / "s-all"
        rc2, _o, _e = adopt(tool, w2, registry(lane_rows(held_url)), staged, entry, "--cites", "all")
        ren2 = {r[0] for r in tsv(w2 / "out/renumber.tsv")}
        app2 = [l for l in (w2 / "out/append.md").read_text(encoding="utf-8").splitlines() if l.strip()] if (w2 / "out/append.md").is_file() else []
        ok_all = rc2 == 0 and ren2 == {a_id, b_id, c_id} and len(app2) == 2
        legs["SOURCE_ONLY"] = bool(ok_s and ok_all)
        print(f"SOURCE_ONLY={'PASS' if legs['SOURCE_ONLY'] else 'FAIL'} default_rc={rc} map={sorted(ren)} appended={len(app)} bodyonly={bo!r} all_rc={rc2} all_map={sorted(ren2)}")

        # 4 (D1 + D2) escaped pipes in the identity cell
        w = tmp / "d1"
        staged1 = [row(b_id, f"Held B — {held_url}\\| alt", "corpus/knowledge/e.md")]
        entry1 = f"source: {b_id} — {held_url} — section\nverified-at: 2026-10-25\nrecheck: 90d\n\n# E\n\n- B ({b_id}).\n"
        rc, _o, _e = adopt(tool, w, registry(lane_rows(held_url)), staged1, entry1)
        ren1 = {r[0]: r[1:3] for r in tsv(w / "out/renumber.tsv")}
        app1 = [l for l in (w / "out/append.md").read_text(encoding="utf-8").splitlines() if l.strip()] if (w / "out/append.md").is_file() else []
        ok_d1 = rc == 0 and ren1.get(b_id) == [f"S{held_n:03d}", "held"] and not app1
        w = tmp / "d2"
        url2 = f"https://{host}/held2-{n}"
        reg2 = registry(lane_rows(url2, f"Held doc \\| alt — {url2}"))
        staged2 = [row(b_id, f"Held B — {url2}", "corpus/knowledge/e.md")]
        entry2 = f"source: {b_id} — {url2} — section\nverified-at: 2026-10-25\nrecheck: 90d\n\n# E\n\n- B ({b_id}).\n"
        rc, _o, _e = adopt(tool, w, reg2, staged2, entry2)
        ren2d = {r[0]: r[1:3] for r in tsv(w / "out/renumber.tsv")}
        app2d = [l for l in (w / "out/append.md").read_text(encoding="utf-8").splitlines() if l.strip()] if (w / "out/append.md").is_file() else []
        ok_d2 = rc == 0 and ren2d.get(b_id) == [f"S{held_n:03d}", "held"] and not app2d
        legs["PIPE_IDENTITY"] = bool(ok_d1 and ok_d2)
        print(f"PIPE_IDENTITY={'PASS' if legs['PIPE_IDENTITY'] else 'FAIL'} d1={'ok' if ok_d1 else 'no'} d2={'ok' if ok_d2 else 'no'}")

        # 5 (D3) registry structure
        res = []
        for name, reg, must_refuse in (
            ("renamed-heading", registry(lane_rows(held_url), heading="## Sources"), True),
            ("no-heading", registry(lane_rows(held_url), heading="Rows below"), True),
            ("row-outside", registry(lane_rows(held_url), extra=f"\n## Other\n\n{HEAD}{row(f'S{top + 5:03d}', f'Stray — https://{host}/stray')}"), True),
            ("well-formed", registry(lane_rows(held_url)), False),
        ):
            w = tmp / name
            sa = [row(a_id, f"New A — https://{host}/new-a-{n}", "corpus/knowledge/e.md")]
            ea = f"source: {a_id} — https://{host}/new-a-{n} — section\nverified-at: 2026-10-25\nrecheck: 90d\n\n# E\n\n- A ({a_id}).\n"
            rc, _o, err = adopt(tool, w, reg, sa, ea)
            wrote = (w / "out/renumber.tsv").is_file() or (w / "out/append.md").is_file()
            if must_refuse:
                good = rc == 1 and "REFUSED" in err and not wrote
            else:
                app = [l for l in (w / "out/append.md").read_text(encoding="utf-8").splitlines() if l.strip()] if (w / "out/append.md").is_file() else []
                good = rc == 0 and len(app) == 1 and app[0].lstrip(" |").startswith(f"S{top + 1:03d}")
            res.append(good)
            print(f"REGISTRY {name} rc={rc} -> {'PASS' if good else 'FAIL'}")
        legs["REGISTRY_STRUCTURE"] = all(res)
        print(f"REGISTRY_STRUCTURE={'PASS' if legs['REGISTRY_STRUCTURE'] else 'FAIL'} {sum(res)}/{len(res)}")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

    k = sum(legs.values())
    print(f"LEGS={k}/{len(legs)}")
    ok = k == len(legs)
    print("C1=PASS" if ok else "C1=FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())

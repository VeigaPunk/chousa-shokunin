#!/usr/bin/env python3
"""c1-count — frozen counter for round 50 claim C1 (operability, capability).

Predicate R50-C1, the same sentence as corpus/evidence/round50/claims.md:
`tools/assimilate-rows.py --selftest [--fixtures DIR] [--expected FILE]` runs
the adopter on an isolated fixture package and compares the observed finding
lines with the `findings` list of an expected file, so that on this counter's
own pinned fixture package (corpus/evidence/round50/c1-fixtures/, whose
digest the counter pins) it exits 0 with `SELFTEST=PASS` and 26 findings,
and on each of six perturbed copies it exits 1 and names the perturbed
finding in a `DIFF` line — P1 the indented registry row removed
(`DIFF missing COLLISIONS S011,S012`), P2 a held URL changed (`DIFF missing
MAP S012->S001 held`), P3 the escaped pipe removed (`DIFF missing STRIPPED
S015 cell6-pipe`), P4 a recheck made unparseable (`DIFF unexpected TOOLEXIT
1`), P5 one expected finding dropped (`DIFF unexpected ROWUSEDBY S014`), P6 a
cited id removed from an entry (`DIFF missing MAP S013->S015 append`) — and an
unparseable expected file exits 2 with `SELFTEST=ERROR`; and the lane default
(`python3 tools/assimilate-rows.py --selftest`, no flags) also exits 0 PASS;
and the round-49 counter `corpus/evidence/round49/c1-count.py --tool <tool>`
still prints `C1=PASS`, exit 0.

Finding-line grammar (frozen interface): `TOOLEXIT n`, `REFUSED text`,
`COLLISIONS ids|-`, `MAP staged->lane action`, `ROWCELLS lane n`, `ROWSTATUS
lane status`, `ROWUSEDBY lane list`, `ROWRECHECK lane value`, `ENTRYCITES
entry ids`, `STRIPPED lane column`; output lines `FINDING <line>`, `DIFF
missing <line>`, `DIFF unexpected <line>`, `FIXTURES_SHA256=<hex>`,
`SELFTEST=PASS|FAIL|ERROR`. Fixture layout: `registry.md`, `staged.md`,
`knowledge/corpus/knowledge/*.md`, `expected.json` (`{"findings": [...]}`).

Usage: python3 corpus/evidence/round50/c1-count.py [--tool PATH] [--root LANE]
(a tool other than the lane's is run with explicit --fixtures/--expected).
Exit codes: 0 every leg holds · 1 a leg failed · 2 env (pinned fixtures changed).
"""
from __future__ import annotations

import argparse
import hashlib
import pathlib
import re
import shutil
import subprocess
import sys
import tempfile

LANE = pathlib.Path(__file__).resolve().parents[3]
EV = pathlib.Path(__file__).resolve().parent
FIX = EV / "c1-fixtures"
PIN = "c5c56480e9f6a08d6a2077b6a11267a4cabf0bc0d3f726408a9bb0238283cd43"
R49 = LANE / "corpus" / "evidence" / "round49" / "c1-count.py"


def digest(d: pathlib.Path) -> str:
    h = hashlib.sha256()
    for p in sorted(q for q in d.rglob("*") if q.is_file()):
        h.update(p.relative_to(d).as_posix().encode() + b"\0" + p.read_bytes() + b"\0")
    return h.hexdigest()


def run(tool: pathlib.Path, *args: str) -> tuple[int, str]:
    try:
        r = subprocess.run([sys.executable, str(tool), "--selftest", *args], capture_output=True, text=True, timeout=120)
    except subprocess.TimeoutExpired:
        return 124, ""
    return r.returncode, r.stdout


def edit(path: pathlib.Path, old: str, new: str) -> bool:
    t = path.read_text(encoding="utf-8")
    if old not in t:
        return False
    path.write_text(t.replace(old, new, 1), encoding="utf-8")
    return True


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--tool")
    ap.add_argument("--root", default=str(LANE))
    a = ap.parse_args()
    root = pathlib.Path(a.root)
    default_tool = root / "tools" / "assimilate-rows.py"
    tool = pathlib.Path(a.tool) if a.tool else default_tool
    if digest(FIX) != PIN:
        print("PIN_CHANGED fixtures digest differs from the frozen pin")
        return 2
    legs: dict[str, bool] = {}

    # 1 lane default (no flags) — only for the lane's own tool
    if a.tool is None:
        rc, out = run(tool)
        legs["SELFTEST_DEFAULT"] = rc == 0 and "SELFTEST=PASS" in out
    else:
        legs["SELFTEST_DEFAULT"] = True
    print(f"SELFTEST_DEFAULT={'PASS' if legs['SELFTEST_DEFAULT'] else 'FAIL'}" + (" (skipped: --tool)" if a.tool else ""))

    # 2 baseline on the pinned fixtures, digest the tool prints equals the pin
    rc, out = run(tool, "--fixtures", str(FIX), "--expected", str(FIX / "expected.json"))
    m = re.search(r"^SELFTEST=PASS findings=(\d+) expected=(\d+)$", out, re.M)
    d = re.search(r"^FIXTURES_SHA256=([0-9a-f]{64})$", out, re.M)
    legs["BASELINE"] = rc == 0 and bool(m) and m.group(1) == "26" == m.group(2) and bool(d) and d.group(1) == PIN
    print(f"BASELINE={'PASS' if legs['BASELINE'] else 'FAIL'} rc={rc} " + (f"findings={m.group(1)}" if m else "findings=?"))

    # 3 perturbations
    tmp = pathlib.Path(tempfile.mkdtemp(prefix="chousa-r50-c1-"))
    try:
        perts = [
            ("P1", lambda d: edit(d / "registry.md", "  | S011 |", "# removed | S011 |"), r"^DIFF missing COLLISIONS S011,S012$"),
            ("P2", lambda d: edit(d / "staged.md", "example.test/held", "example.test/held-moved"), r"^DIFF missing MAP S012->S001 held$"),
            ("P3", lambda d: edit(d / "staged.md", "section a \\| b", "section a b"), r"^DIFF missing STRIPPED S015 cell6-pipe$"),
            ("P4", lambda d: edit(d / "staged.md", "2026-12-01 — re-verify after release", "2026-13-45 — re-verify after release"), r"^DIFF unexpected TOOLEXIT 1$"),
            ("P5", lambda d: edit(d / "expected.json", ' "ROWUSEDBY S014 corpus/knowledge/a.md, corpus/knowledge/b.md",\n', ""), r"^DIFF unexpected ROWUSEDBY S014 "),
            ("P6", lambda d: edit(d / "knowledge/corpus/knowledge/a.md", "A third document (S013) and", "A third document and"), r"^DIFF missing MAP S013->S015 append$"),
        ]
        ok_p = 0
        for name, mut, pat in perts:
            dst = tmp / name
            shutil.copytree(FIX, dst)
            applied = mut(dst)
            rc, out = run(tool, "--fixtures", str(dst), "--expected", str(dst / "expected.json"))
            hit = applied and rc == 1 and re.search(pat, out, re.M) is not None
            ok_p += bool(hit)
            print(f"PERTURB {name} applied={int(bool(applied))} rc={rc} -> {'PASS' if hit else 'FAIL'}")
        legs["PERTURB"] = ok_p == len(perts)
        print(f"PERTURB_PASS={ok_p}/{len(perts)}")

        # 4 unparseable expected file
        bad = tmp / "bad"
        shutil.copytree(FIX, bad)
        (bad / "expected.json").write_text("{not json", encoding="utf-8")
        rc, out = run(tool, "--fixtures", str(bad), "--expected", str(bad / "expected.json"))
        legs["EXPECTED_BAD"] = rc == 2 and "SELFTEST=ERROR" in out
        print(f"EXPECTED_BAD={'PASS' if legs['EXPECTED_BAD'] else 'FAIL'} rc={rc}")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

    # 5 round-49 counter still passes with this tool
    if R49.is_file():
        p = subprocess.run([sys.executable, str(R49), "--tool", str(tool), "--root", str(root)],
                           capture_output=True, text=True, timeout=600)
        legs["R49_REGRESSION"] = p.returncode == 0 and "C1=PASS" in p.stdout
        print(f"R49_REGRESSION={'PASS' if legs['R49_REGRESSION'] else 'FAIL'} rc={p.returncode}")
    else:
        legs["R49_REGRESSION"] = False
        print("R49_REGRESSION=FAIL (counter missing)")

    n = sum(legs.values())
    print(f"LEGS={n}/{len(legs)}")
    ok = n == len(legs)
    print("C1=PASS" if ok else "C1=FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""c1-supplement — SUPPLEMENTARY post-freeze check for round 50 claim C1 (not the frozen counter; claims.md is unchanged).

W2 `R50CritForgeC1` showed the frozen counter certifies recognition of its own six perturbations: a 42-line tool that
prints the six literal DIFF lines for any non-pinned fixture digest passes `c1-count.py` (`LEGS=5/5`). W2 `R50MutSelftestV2`
showed the frozen counter kills 0/7 mutants of the post-freeze hardening. This supplement adds, on copies of the pinned
fixtures, legs the forge cannot replay and the hardening probes:
  P7  a nonce recheck in the staged file -> the DIFF set is EXACTLY {missing ROWRECHECK S014 2026-12-01,
      missing STRIPPED S014 recheck, unexpected ROWRECHECK S014 <nonce>} (exclusive set, nonce unknown to the tool author)
  H1  a duplicated expected line -> exit 1 `DIFF missing TOOLEXIT 0`
  H2  a fixture with no knowledge entry -> exit 2 `SELFTEST=ERROR`
  H3  `--selftest --staged x` -> exit 2
  H4  an entry citing no id -> the finding line `ENTRYCITES corpus/knowledge/c.md -` (no trailing space)
Usage: python3 corpus/evidence/round50/c1-supplement.py [--tool PATH]   Exit 0 all legs · 1 a leg fails."""
import argparse
import json
import pathlib
import re
import secrets
import shutil
import subprocess
import sys
import tempfile

EV = pathlib.Path(__file__).resolve().parent
LANE = EV.parents[2]
FIX = EV / "c1-fixtures"
ap = argparse.ArgumentParser()
ap.add_argument("--tool", default=str(LANE / "tools" / "assimilate-rows.py"))
a = ap.parse_args()


def run(*args):
    p = subprocess.run([sys.executable, a.tool, "--selftest", *args], capture_output=True, text=True, timeout=120)
    return p.returncode, p.stdout, p.stderr


tmp = pathlib.Path(tempfile.mkdtemp(prefix="chousa-r50-sup-"))
res = {}
try:
    nonce = "re-verify-" + secrets.token_hex(4)
    d = tmp / "p7"
    shutil.copytree(FIX, d)
    s = d / "staged.md"
    s.write_text(s.read_text(encoding="utf-8").replace("2026-12-01 — re-verify after release", nonce), encoding="utf-8")
    rc, out, _ = run("--fixtures", str(d), "--expected", str(d / "expected.json"))
    got = {l for l in out.splitlines() if l.startswith("DIFF ")}
    want = {"DIFF missing ROWRECHECK S014 2026-12-01", "DIFF missing STRIPPED S014 recheck", f"DIFF unexpected ROWRECHECK S014 {nonce}"}
    res["P7_NONCE_EXCLUSIVE"] = rc == 1 and got == want
    d = tmp / "h1"
    shutil.copytree(FIX, d)
    e = json.loads((d / "expected.json").read_text())
    e["findings"].append(e["findings"][0])
    (d / "expected.json").write_text(json.dumps(e))
    rc, out, _ = run("--fixtures", str(d), "--expected", str(d / "expected.json"))
    res["H1_DUPLICATE_EXPECTED"] = rc == 1 and "DIFF missing TOOLEXIT 0" in out
    d = tmp / "h2"
    shutil.copytree(FIX, d)
    shutil.rmtree(d / "knowledge")
    rc, out, _ = run("--fixtures", str(d), "--expected", str(d / "expected.json"))
    res["H2_NO_ENTRY"] = rc == 2 and "SELFTEST=ERROR" in out
    rc, out, err = run("--staged", "x")
    res["H3_OPTION_CLASH"] = rc == 2
    d = tmp / "h4"
    d.mkdir()
    (d / "registry.md").write_text("## Registry\n\n| S001 | z — https://example.test/z | docs | A | s | a | t | mined | 2026-01-01 | 90d | — |\n", encoding="utf-8")
    (d / "staged.md").write_text("| S101 | y — https://example.test/y | docs | A | s | a | t | mined | 2026-10-25 | 90d | — |\n", encoding="utf-8")
    (d / "knowledge/corpus/knowledge").mkdir(parents=True)
    (d / "knowledge/corpus/knowledge/c.md").write_text("No ids here.\n", encoding="utf-8")
    (d / "expected.json").write_text(json.dumps({"findings": ["TOOLEXIT 0", "COLLISIONS -", "ENTRYCITES corpus/knowledge/c.md -"]}), encoding="utf-8")
    rc, out, _ = run("--fixtures", str(d), "--expected", str(d / "expected.json"))
    res["H4_ENTRYCITES_DASH"] = rc == 0 and "FINDING ENTRYCITES corpus/knowledge/c.md -" in out.splitlines()
finally:
    shutil.rmtree(tmp, ignore_errors=True)
for k, v in res.items():
    print(f"{k}={'PASS' if v else 'FAIL'}")
n = sum(res.values())
print(f"SUPPLEMENT_LEGS={n}/{len(res)}")
print("C1_SUPPLEMENT=" + ("PASS" if n == len(res) else "FAIL"))
sys.exit(0 if n == len(res) else 1)

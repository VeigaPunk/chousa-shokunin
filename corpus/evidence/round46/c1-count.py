#!/usr/bin/env python3
"""c1-count — frozen counter for round 46 claim C1 (operability).

Predicate R46-C1, the same sentence as corpus/evidence/round46/claims.md:
`tools/inference-ground.py` exists and, run over
`corpus/fixtures/inference-ground-r46/`, exits 0 on every `positive-*.md`
fixture and exits 1 on every `junk-*.md` fixture (the three junk classes:
uncited bullet, cited-but-ungrounded token, and a body that reuses the correct
spans and figures while its inference asserts something else — the round-45 D7
class, `CritC3Axis`).

Prints `TOOL=present|absent`, `POSITIVE_PASS=n/n`, `JUNK_KILLED=n/n`,
`CANARY=pass|fail` (the first positive and first junk fixture copied under
neutral names — a tool that keys on the fixture NAME fails this leg), then
`C1=PASS|FAIL`.
Exit 0 iff the tool is present and every fixture scores its declared verdict;
1 otherwise; 2 usage/env (no fixtures).

Cheapest gates that would score full marks without the work (QUALITY 60):
a tool that always exits 0 passes the positives and kills nothing
(`--tool` on that forge scores JUNK_KILLED=0/3), and a tool that only checks
citation presence kills 1 of 3. A missing tool scores 0/n on both legs. The
counter checks exit codes only; what a finding NAMES is a reader's check.
"""
from __future__ import annotations

import argparse
import hashlib
import pathlib
import shutil
import tempfile
import subprocess
import sys

LANE = pathlib.Path(__file__).resolve().parents[3]
FIXTURES = pathlib.Path("corpus/fixtures/inference-ground-r46")
POSITIVES = ("positive-a.md", "positive-b.md", "positive-c.md")
JUNKS = ("junk-uncited.md", "junk-ungrounded.md", "junk-borrowed.md")
# The kill rule says a fixture set changed after the freeze fails the claim, so
# every fixture name is bound to the bytes frozen at `c2f0e9d1` (round-46
# `CritC1Attack` found this clause had no enforcement).
PINNED = {
    "positive-a.md": "1378296857c6193d80ce9649f5778216003f10ffdd645c0461fa43c2c46b8a21",
    "positive-b.md": "1d09c94bd4668fc31389a07354c312ca86b5e8dd0e644b84e3fe69e25a46ced4",
    "positive-c.md": "4e61f56c8af38418754561096e7e22b8aa54e042bf0b86c4ad36542c7c6f417a",
    "junk-uncited.md": "7b3e6b6e36c771a336d7da17291d94861226af289b2a2c7d4a6ef7d68016e598",
    "junk-ungrounded.md": "ab32577d5266fbb07a04a63735e1f4f7432b06841a64fa3ff840b42c2f457fe4",
    "junk-borrowed.md": "cba03251466e44773ef0ed9e080388b284f30f1ada0034e6b3c824d364ceb778",
    "spans.tsv": "38a536bd9d33d0dc45d441cce6ce1882a1f4e60ee8ecdaebfd9f85a229d2aff4",
    "counts.json": "fd414d0a24883711dab8e27bd36e0aad00e6e09192d51b7bf75228e3f76fbb5c",
    "spans/S901-1.txt": "7c2aa3214d9409886ca91fefa1ed69599c29ec521cd745affae86f93b762b1ef",
    "spans/S902-1.txt": "c2184ca73ce45977b629591c786525bf8bf7899bc436f443af91feab396f20e4",
}


def digest(path: pathlib.Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(tool: pathlib.Path, fixture_dir: pathlib.Path, name: str,
        spans_dir: pathlib.Path | None = None) -> int:
    entry = fixture_dir / name
    if not entry.is_file():
        return 127
    src = spans_dir or fixture_dir
    proc = subprocess.run(
        [sys.executable, str(tool), "--entry", str(entry),
         "--spans", str(src / "spans.tsv"),
         "--counts", str(src / "counts.json"),
         "--root", str(fixture_dir)],
        capture_output=True, text=True)
    return proc.returncode


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--root", default=str(LANE))
    ap.add_argument("--tool", default=None, help="score another tool (controls)")
    a = ap.parse_args()
    root = pathlib.Path(a.root)
    tool = pathlib.Path(a.tool) if a.tool else root / "tools" / "inference-ground.py"
    fixture_dir = root / FIXTURES
    if not fixture_dir.is_dir():
        print("C1=FAIL no-fixtures")
        return 2
    changed = [n for n, want in PINNED.items()
               if not (fixture_dir / n).is_file() or digest(fixture_dir / n) != want]
    if changed:
        print("FIXTURES_CHANGED=" + ",".join(changed))
        print("C1=FAIL")
        return 1
    present = tool.is_file()
    # Canary (round-46 `ExecCounterRun`): a tool that keys on the FIXTURE NAME
    # (`basename startswith positive-`) scores 3/3+3/3 without reading a byte.
    # The same bytes under neutral names must land the same verdicts.
    canary_ok = 1
    if present:
        with tempfile.TemporaryDirectory() as td:
            tmp = pathlib.Path(td)
            shutil.copyfile(fixture_dir / POSITIVES[0], tmp / "canary-a.md")
            shutil.copyfile(fixture_dir / JUNKS[0], tmp / "canary-b.md")
            canary_ok = int(run(tool, tmp, "canary-a.md", fixture_dir) == 0
                            and run(tool, tmp, "canary-b.md", fixture_dir) == 1)
    # A junk fixture must be refused with EXIT 1 — the frozen sentence says
    # "exits 1", so a crash (2) or a missing file (127) is not a kill
    # (round-46 `MutC1Junk` finding).
    pos = sum(run(tool, fixture_dir, n) == 0 for n in POSITIVES) if present else 0
    junk = sum(run(tool, fixture_dir, n) == 1 for n in JUNKS) if present else 0
    print(f"TOOL={'present' if present else 'absent'}")
    print(f"POSITIVE_PASS={pos}/{len(POSITIVES)}")
    print(f"JUNK_KILLED={junk}/{len(JUNKS)}")
    print(f"CANARY={'pass' if canary_ok else 'fail'}")
    ok = present and pos == len(POSITIVES) and junk == len(JUNKS) and canary_ok == 1
    print("C1=PASS" if ok else "C1=FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())


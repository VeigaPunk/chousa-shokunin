#!/usr/bin/env python3
"""c1-count — frozen counter for round 47 claim C1 (operability).

Predicate R47-C1, the same sentence as corpus/evidence/round47/claims.md:
`tools/inference-ground.py`, run over `corpus/fixtures/inference-ground-r47/`,
exits 0 on each of the three `positive-*.md` fixtures and exits 1 printing an
`INF_POLARITY_FLIP` finding on each of the three `junk-*.md` fixtures — the
round-45 D7 class narrowed to polarity: (a) a span phrase the span NEGATES,
asserted positively by the bullet's own words; (b) a span phrase the span
AFFIRMS, denied by the bullet's own words; (c) a counts figure whose key is
affirmative, re-denominated by the bullet as a negative — while the round-46
counter still prints `C1=PASS` for the same tool and the two round-46
entries still exit 0 under it (no regression).

Prints `TOOL=present|absent`, `POSITIVE_PASS=n/3`, `JUNK_KILLED=n/3` (exit 1
AND an `INF_POLARITY_FLIP` line), `CANARY=pass|fail` (first positive and first
junk under neutral names), `R46_COUNTER=pass|fail`, `R46_ENTRIES=n/2`, then
`C1=PASS|FAIL`. Exit 0 iff every leg holds; 1 otherwise; 2 usage/env.

Cheapest gates that would score full marks without the work (QUALITY 60):
the round-46 tool (presence only) passes all six fixtures, so `JUNK_KILLED=0/3`;
a tool that refuses every bullet carrying a negator kills the junk but fails
two positives; a tool that always exits 1 passes no positive and fails the
round-46 counter. Fixture bytes are pinned. What the finding NAMES beyond its
code is a reader's check.
"""
from __future__ import annotations

import argparse
import hashlib
import pathlib
import shutil
import subprocess
import sys
import tempfile

LANE = pathlib.Path(__file__).resolve().parents[3]
FIXTURES = pathlib.Path("corpus/fixtures/inference-ground-r47")
POSITIVES = ("positive-negation-kept.md", "positive-affirmed.md", "positive-figure-negated.md")
JUNKS = ("junk-flip-asserted.md", "junk-flip-denied.md", "junk-flip-figure.md")
R46_COUNTER = pathlib.Path("corpus/evidence/round46/c1-count.py")
R46_ENTRIES = ("corpus/knowledge/evidence-pool-versioning-r39.md",
               "corpus/knowledge/evidence-pool-versioning-r39-amendment-2026-10-23.md")
R46_SPANS = pathlib.Path("corpus/evidence/round46/spans.tsv")
PINNED = {
    "counts.json": "17fb165baf9bfc11bfb7eebeb78e94f8ad30a6695de41fabacd7efe5880c3be8",
    "junk-flip-asserted.md": "01ef16891fbc6549fe30a2494ed9a206ef85b9d1974dbb27a9cd015ae48bee2b",
    "junk-flip-denied.md": "440cc5cf9a10022f06f661b5a2db26a24c582b213ff7f69a05805eefc253aaf7",
    "junk-flip-figure.md": "67997d0273f0ac188f7a5304415ad06d86e02790fb8c3ce9ccdbca2ef0878c9f",
    "positive-affirmed.md": "7278efd7e468f8f4f0c6490a9313b0768e2f58fe1dfc64aeaa6837ee2b7443ac",
    "positive-figure-negated.md": "7a15216a43939894760e4d342b53dc5df8d0f4ff5a09e8f5ee9c2544cf070ece",
    "positive-negation-kept.md": "2119e3e8c6d9c3355765ff01ec3b5e2a43ca299f49dee2761163394e3a6cc985",
    "spans.tsv": "38a536bd9d33d0dc45d441cce6ce1882a1f4e60ee8ecdaebfd9f85a229d2aff4",
    "spans/S901-1.txt": "7c2aa3214d9409886ca91fefa1ed69599c29ec521cd745affae86f93b762b1ef",
    "spans/S902-1.txt": "c2184ca73ce45977b629591c786525bf8bf7899bc436f443af91feab396f20e4",
}


def digest(path: pathlib.Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(tool: pathlib.Path, fixture_dir: pathlib.Path, name: str,
        data_dir: pathlib.Path) -> tuple[int, str]:
    entry = fixture_dir / name
    if not entry.is_file():
        return 127, ""
    proc = subprocess.run(
        [sys.executable, str(tool), "--entry", str(entry),
         "--spans", str(data_dir / "spans.tsv"),
         "--counts", str(data_dir / "counts.json"),
         "--root", str(fixture_dir)],
        capture_output=True, text=True)
    return proc.returncode, proc.stdout


def killed(rc: int, out: str) -> bool:
    return rc == 1 and any(l.startswith("FINDING INF_POLARITY_FLIP") for l in out.splitlines())


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--root", default=str(LANE))
    ap.add_argument("--tool", default=None, help="score another tool (controls)")
    a = ap.parse_args()
    root = pathlib.Path(a.root)
    tool = pathlib.Path(a.tool).resolve() if a.tool else root / "tools" / "inference-ground.py"
    fx = root / FIXTURES
    if not fx.is_dir():
        print("C1=FAIL no-fixtures")
        return 2
    changed = [n for n, want in PINNED.items()
               if not (fx / n).is_file() or digest(fx / n) != want]
    if changed:
        print("FIXTURES_CHANGED=" + ",".join(changed))
        print("C1=FAIL")
        return 1
    present = tool.is_file()
    pos = junk = 0
    canary_ok = r46_ok = False
    r46_entries = 0
    if present:
        pos = sum(run(tool, fx, n, fx)[0] == 0 for n in POSITIVES)
        junk = sum(killed(*run(tool, fx, n, fx)) for n in JUNKS)
        with tempfile.TemporaryDirectory() as td:
            tmp = pathlib.Path(td)
            shutil.copyfile(fx / POSITIVES[0], tmp / "canary-a.md")
            shutil.copyfile(fx / JUNKS[0], tmp / "canary-b.md")
            canary_ok = (run(tool, tmp, "canary-a.md", fx)[0] == 0
                         and killed(*run(tool, tmp, "canary-b.md", fx)))
        c46 = root / R46_COUNTER
        if c46.is_file():
            p = subprocess.run([sys.executable, str(c46), "--root", str(root), "--tool", str(tool)],
                               capture_output=True, text=True)
            r46_ok = p.returncode == 0 and "C1=PASS" in p.stdout
        for e in R46_ENTRIES:
            if not (root / e).is_file():
                continue
            p = subprocess.run(
                [sys.executable, str(tool), "--entry", str(root / e),
                 "--spans", str(root / R46_SPANS), "--counts", "/dev/null",
                 "--registry", str(root / "corpus" / "SOURCES.md"), "--root", str(root), "--quiet"],
                capture_output=True, text=True)
            r46_entries += p.returncode == 0
    print(f"TOOL={'present' if present else 'absent'}")
    print(f"POSITIVE_PASS={pos}/{len(POSITIVES)}")
    print(f"JUNK_KILLED={junk}/{len(JUNKS)}")
    print(f"CANARY={'pass' if canary_ok else 'fail'}")
    print(f"R46_COUNTER={'pass' if r46_ok else 'fail'}")
    print(f"R46_ENTRIES={r46_entries}/{len(R46_ENTRIES)}")
    ok = (present and pos == len(POSITIVES) and junk == len(JUNKS) and canary_ok
          and r46_ok and r46_entries == len(R46_ENTRIES))
    print("C1=PASS" if ok else "C1=FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())

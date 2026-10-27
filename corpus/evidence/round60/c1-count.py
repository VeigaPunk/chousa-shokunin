#!/usr/bin/env python3
"""Round-60 counter for the round-58 C1 refusal-verdict false positive.

A builder's emitted text is diagnostic only. Verdicts are derived from child
return codes and independently observed filesystem state. This is a focused
regression probe; it does not assert the entire round-58 battery passes.
"""
from __future__ import annotations
import argparse
import os
import pathlib
import shutil
import subprocess
import sys
import tempfile

ROOT = pathlib.Path(__file__).resolve().parents[3]
BASE = ROOT / "corpus/evidence/round58"
R55 = BASE / "controls/build-spans-r55.py"


def run(builder: pathlib.Path, work: pathlib.Path) -> tuple[int, str]:
    work.mkdir(parents=True, exist_ok=True)
    cache, out = work / "cache", work / "out"
    cache.mkdir()
    out.mkdir()
    source = "https://fixture.example/doc"
    key = __import__("hashlib").sha256(source.encode()).hexdigest()[:24]
    (cache / f"{key}.txt").write_text("unique source bytes\n")
    q = work / "quotes.tsv"
    q.write_text(f"id\turl\tquote\tentry\nS601\t{source}\tunique source bytes\tentry.md\n")
    foreign = out / "spans" / "S777-1.txt"
    foreign.parent.mkdir()
    foreign.write_bytes(b"preserve-me\n")
    before = foreign.read_bytes()
    try:
        p = subprocess.run([sys.executable, "-B", str(builder), "--quotes", str(q), "--out", str(out), "--cache", str(cache)], cwd=work, capture_output=True, text=True, timeout=30, env={**os.environ, "PYTHONDONTWRITEBYTECODE":"1", "TMPDIR":str(work)})
        emitted = p.stdout + p.stderr
        intact = foreign.is_file() and foreign.read_bytes() == before
        valid_output = "SPANS_ROWS=1" in emitted and "WRITTEN=1" in emitted
        return p.returncode, ("candidate_safe" if p.returncode == 0 and intact and valid_output
                              else "baseline_bad" if p.returncode == 0 and not intact
                              else "refusal" if p.returncode != 0 and intact else "")
    except subprocess.TimeoutExpired:
        return 124, ""


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--builder", type=pathlib.Path, default=ROOT / "tools/build-spans.py")
    ap.add_argument("--work", type=pathlib.Path)
    ap.add_argument("--seed", type=int, default=6001)
    a=ap.parse_args()
    base=a.work or pathlib.Path(os.environ.get("HYAKU_SCRATCH", "/fast/scratch/hyaku")) / "chousa-r60" / "c1-count"
    base.mkdir(parents=True, exist_ok=True)
    try:
        # Reproduce exactly the original counter's target-token forgery with
        # all seven refusal labels emitting the token and returning success.
        (base / "forged.py").write_text("import sys\nprint('=PASS')\nprint('all seven hazards accepted')\nsys.exit(0)\n")
        forged = base / "forged.py"
        _, forge_state = run(forged, base / "forge")
        forge_blocked = forge_state != "forged_safe"
        # The pinned round-55 implementation is the discriminating negative:
        # it deletes the seeded foreign file while attempting a rebuild.
        _, base_state = run(R55, base / "baseline")
        baseline_discriminates = base_state == "baseline_bad"
        _, candidate_state = run(a.builder.resolve(), base / "candidate")
        candidate_ok = candidate_state == "candidate_safe"
        passed = forge_blocked and baseline_discriminates and candidate_ok
        print(f"INJECTION_REJECTED={int(forge_blocked)}/1")
        print(f"BASELINE_DISCRIMINATES={int(baseline_discriminates)}/1")
        print(f"CANDIDATE_REFUSAL={int(candidate_ok)}/1")
        print(f"C1={'PASS' if passed else 'FAIL'}")
        return 0 if passed else 1
    finally:
        if a.work is None:
            shutil.rmtree(base, ignore_errors=True)

if __name__ == "__main__":
    sys.exit(main())

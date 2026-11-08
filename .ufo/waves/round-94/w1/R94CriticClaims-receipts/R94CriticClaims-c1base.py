#!/usr/bin/env python3
"""Remove the two round-93 claims rows from the base r93 pins table (two-column form), recompute the
self row, run the r93 driver exactly as the round-94 before-receipt did (no --repo), restore."""
import hashlib
import os
import subprocess
import sys

ROOT = "/fast/scratch/hyaku/chousa-r94/R94CriticClaims/base"
PINS_REL = "corpus/evidence/round93/instrument-pins.txt"
DRIVER = os.path.join(ROOT, "corpus/evidence/round93/control-driver-r93.py")
REV = "3789608dc8c0eded67f1e5d3840caf0a27522a88"
OUT = "/fast/scratch/hyaku/chousa-r94/R94CriticClaims/c1"
WORK = "/fast/scratch/hyaku/chousa-r94/R94CriticClaims/c1/basework-dropped"
DROPS = (".ufo/waves/round-93/claims.json", ".ufo/waves/round-93/claims.md")


def main():
    pins_path = os.path.join(ROOT, PINS_REL)
    pristine = open(pins_path, "rb").read()
    rows = []
    for ln in pristine.decode().splitlines():
        if not ln.strip() or ln.startswith("#"):
            continue
        sha, rel = ln.split()
        rows.append([sha, rel])
    kept = [r for r in rows if r[1] not in DROPS]
    if len(kept) != len(rows) - 2:
        raise SystemExit(f"expected 2 drops, got {len(rows) - len(kept)}")
    self_rel = PINS_REL
    body = "".join(f"{sha}  {rel}\n" for sha, rel in kept if rel != self_rel)
    self_sha = hashlib.sha256(body.encode()).hexdigest()
    with open(pins_path, "w", encoding="utf-8") as fh:
        fh.write(body)
        fh.write(f"{self_sha}  {self_rel}\n")
    try:
        p = subprocess.run([sys.executable, "-B", DRIVER, "verify", "--root", ROOT,
                            "--rev", REV, "--work", WORK], capture_output=True, text=True)
        out = (p.stdout or "") + (p.stderr or "")
        open(os.path.join(OUT, "base-r93-claims-dropped.out"), "w", encoding="utf-8").write(
            f"# rc={p.returncode}\n# rows={len(kept)}\n" + out)
        print(f"rc={p.returncode} rows={len(kept)}")
        for ln in out.splitlines():
            if ln.startswith(("RECEIPT PINS", "COMMITTED_OK", "PINNED_FILES", "CONTROL_DRIVER", "FINDING")):
                print(ln)
    finally:
        open(pins_path, "wb").write(pristine)
    return 0


if __name__ == "__main__":
    sys.exit(main())

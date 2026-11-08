#!/usr/bin/env python3
"""Seat-R94RevPrior C1 before-state fixture: project a pins table into the r93 two-column shape.

Usage: python3 fixture-c1-projection.py MODE PINS_PATH
  proj34       read the r94 three-column table, drop the role column, keep all rows
  proj32       same, but also delete the two `claims` rows
  r93-drop-claims  read the r93 two-column table, delete the two round-93 claims rows
Every form re-digests the table's own (self) row under the r93 minus-self rule:
the digest covers the body with the self row excluded.
"""
import hashlib
import sys

CLAIMS = {".ufo/waves/round-94/claims.json", ".ufo/waves/round-94/claims.md"}
CLAIMS93 = {".ufo/waves/round-93/claims.json", ".ufo/waves/round-93/claims.md"}


def main():
    mode, path = sys.argv[1], sys.argv[2]
    rows = []
    for ln in open(path, encoding="utf-8"):
        ln = ln.rstrip("\n")
        if not ln or ln.startswith("#"):
            continue
        parts = ln.split()
        if len(parts) == 3:
            sha, role, rel = parts
        else:
            sha, rel = parts
            role = None
        rows.append((sha, role, rel))
    self_rel = next(rel for _s, _r, rel in rows if rel.endswith("instrument-pins.txt"))
    if mode in ("proj34", "proj32"):
        drop = CLAIMS if mode == "proj32" else set()
        keep = [(sha, rel) for sha, _role, rel in rows if rel not in drop and rel != self_rel]
    elif mode == "r93-drop-claims":
        keep = [(sha, rel) for sha, _role, rel in rows if rel not in CLAIMS93 and rel != self_rel]
    else:
        raise SystemExit(f"unknown mode {mode}")
    body = "".join(f"{sha}  {rel}\n" for sha, rel in keep)
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(body)
        fh.write(f"{hashlib.sha256(body.encode()).hexdigest()}  {self_rel}\n")
    print(f"WROTE mode={mode} rows={len(keep) + 1} self={self_rel}")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
import argparse, pathlib, re
ap = argparse.ArgumentParser(); ap.add_argument("--entry", required=True)
ap.add_argument("--spans"); ap.add_argument("--counts"); ap.add_argument("--root", default="."); ap.add_argument("--quiet", action="store_true"); ap.add_argument("--json")
a = ap.parse_args()
lines = pathlib.Path(a.entry).read_text(encoding="utf-8", errors="replace").splitlines()
inside = False; bullets = []
for ln in lines:
    if ln.startswith("#### "):
        inside = ln[5:].strip().lower().startswith("inference"); continue
    if inside and ln.startswith("- "): bullets.append(ln)
bad = [b for b in bullets if not re.search(r"\bS\d{3,}\b", b)]
print("GROUND: PASS" if not bad else "GROUND: FAIL")
raise SystemExit(0 if not bad else 1)

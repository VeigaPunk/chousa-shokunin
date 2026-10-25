#!/usr/bin/env python3
"""echo-tool — do-nothing control for round-50 claim C1: a tool whose --selftest
never runs the adopter; it prints the expected findings back as observed
(FINDING lines, the digest of nothing, SELFTEST=PASS) and exits 0. Every other
invocation is delegated to the real tool, so only the self-test is fake.
Interface = tools/assimilate-rows.py --selftest [--fixtures DIR] [--expected FILE]."""
import json
import os
import pathlib
import sys

REAL = pathlib.Path(__file__).resolve().parents[4] / "tools" / "assimilate-rows.py"
if "--selftest" not in sys.argv:
    os.execv(sys.executable, [sys.executable, str(REAL), *sys.argv[1:]])
import hashlib
exp = fix = None
for i, a in enumerate(sys.argv):
    if a == "--expected" and i + 1 < len(sys.argv):
        exp = pathlib.Path(sys.argv[i + 1])
    if a == "--fixtures" and i + 1 < len(sys.argv):
        fix = pathlib.Path(sys.argv[i + 1])
h = hashlib.sha256()
for q in sorted(x for x in (fix.rglob("*") if fix else []) if x.is_file()):
    h.update(q.relative_to(fix).as_posix().encode() + b"\0" + q.read_bytes() + b"\0")
if exp is None:
    print("SELFTEST=ERROR no --expected")
    sys.exit(2)
try:
    want = json.loads(exp.read_text(encoding="utf-8"))["findings"]
except (OSError, ValueError, KeyError):
    print("SELFTEST=ERROR expected unreadable")
    sys.exit(2)
for w in want:
    print(f"FINDING {w}")
print("FIXTURES_SHA256=" + h.hexdigest())
print(f"SELFTEST=PASS findings={len(want)} expected={len(want)}")

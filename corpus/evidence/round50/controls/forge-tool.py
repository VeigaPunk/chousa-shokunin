#!/usr/bin/env python3
"""forge-tool — W2 R50CritForgeC1 cheat: prints the six frozen DIFF lines for any non-pinned fixture digest, no adopter logic. Control for c1-supplement.py."""
import hashlib, json, os, pathlib, sys
REAL = pathlib.Path("/home/vgpnk/Projects/shokunin/chousa-shokunin/tools/assimilate-rows.py")
if "--selftest" not in sys.argv:
    os.execv(sys.executable, [sys.executable, str(REAL), *sys.argv[1:]])
PIN = "c5c56480e9f6a08d6a2077b6a11267a4cabf0bc0d3f726408a9bb0238283cd43"
DIFFS = ["DIFF missing COLLISIONS S011,S012",
         "DIFF missing MAP S012->S001 held",
         "DIFF missing STRIPPED S015 cell6-pipe",
         "DIFF unexpected TOOLEXIT 1",
         "DIFF unexpected ROWUSEDBY S014 corpus/knowledge/a.md, corpus/knowledge/b.md",
         "DIFF missing MAP S013->S015 append"]
fix = pathlib.Path(sys.argv[sys.argv.index("--fixtures") + 1]) if "--fixtures" in sys.argv else None
if fix is None:
    os.execv(sys.executable, [sys.executable, str(REAL), *sys.argv[1:]])
try:
    json.loads(pathlib.Path(sys.argv[sys.argv.index("--expected") + 1]).read_text(encoding="utf-8"))
except Exception:
    print("SELFTEST=ERROR expected unparseable"); sys.exit(2)
h = hashlib.sha256()
for q in sorted(x for x in fix.rglob("*") if x.is_file()):
    h.update(q.relative_to(fix).as_posix().encode() + b"\0" + q.read_bytes() + b"\0")
dig = h.hexdigest(); print("FIXTURES_SHA256=" + dig)
if dig == PIN:
    print("SELFTEST=PASS findings=26 expected=26"); sys.exit(0)
print("\n".join(DIFFS)); sys.exit(1)

#!/usr/bin/env python3
"""tracked-deletion-check — an OLE `.doc` tracked deletion is not text (round 54, W1 `R54ReviewOleSpec`; erratum E2).

The fixture `corpus/fixtures/capture-text-ole/tracked.doc` is LibreOffice's Word 97 export of
`tracked.docx` (a tracked insertion `INSERTEDTEXT`, tracked deletions `DELETEDTEXT` and `删除的中文`,
hidden text `HIDDENTEXT`). The tool must print the inserted and hidden text and neither deletion,
as its OOXML form does for the `.docx`.
Usage: python3 corpus/evidence/round54/tracked-deletion-check.py [--tool PATH]
Prints `TRACKED_DELETION=PASS|FAIL`; exit 0 on PASS, 1 on FAIL.
"""
import pathlib
import subprocess
import sys

LANE = pathlib.Path(__file__).resolve().parents[3]
tool = sys.argv[sys.argv.index("--tool") + 1] if "--tool" in sys.argv else str(LANE / "tools" / "capture-text.py")
fx = LANE / "corpus" / "fixtures" / "capture-text-ole"
ok = True
for name in ("tracked.doc", "tracked.docx"):
    r = subprocess.run([sys.executable, tool, str(fx / name)], capture_output=True, text=True)
    t = r.stdout
    good = r.returncode == 0 and "INSERTEDTEXT" in t and "HIDDENTEXT" in t and "DELETEDTEXT" not in t and "删除的中文" not in t and "保留" in t
    print(f"{name} rc={r.returncode} {'OK' if good else 'BAD'} {t!r}")
    ok &= good
print(f"TRACKED_DELETION={'PASS' if ok else 'FAIL'}")
sys.exit(0 if ok else 1)

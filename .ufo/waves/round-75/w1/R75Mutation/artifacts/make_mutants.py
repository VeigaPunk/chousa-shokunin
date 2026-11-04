#!/usr/bin/env python3
"""Generate R75 instrument mutants by exact single-occurrence replacement.

Each mutant asserts the replacement occurred exactly once, so every mutant is
one localised hunk away from the frozen bytes.
"""
from pathlib import Path

ROOT = Path("/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence")
OUT = Path("/fast/scratch/hyaku/chousa-r75/R75Mutation/mut")
OUT.mkdir(parents=True, exist_ok=True)

MATRIX = (ROOT / "round75" / "loader-matrix-v2.py").read_text()
BATTERY = (ROOT / "round75" / "matrix-battery.py").read_text()

MUTANTS = [
    # M1: drop the three content cases (append-only but structurally wrong)
    ("m1-drop-content-cases", "matrix", MATRIX,
     '''          # append-only but structurally wrong: decidable from content, never from numstat
          ("dup-log-heading", PATHS[0], "dup-log", 1, frozenset({"C2-1", "C2-2"})),
          ("dup-lesson-heading", PATHS[1], "dup-lesson", 1, frozenset({"C2-3", "C2-5"})),
          ("dup-card-heading", PATHS[2], "dup-card", 1, frozenset({"C2-4"}))]''',
     '''          ]'''),
    # M2: restore declared order (no shuffle)
    ("m2-no-shuffle", "matrix", MATRIX,
     '''    order = list(CASES)
    random.Random(seed).shuffle(order)''',
     '''    order = list(CASES)'''),
    # M3: accept exit 2 as satisfying the expected exit code
    ("m3-accept-exit2", "matrix", MATRIX,
     '''            ok = (p.returncode == expected_rc and len(checks) == 7 and failed == expected_failed''',
     '''            ok = (p.returncode in (expected_rc, 2) and len(checks) == 7 and failed == expected_failed'''),
    # M4: compare exit codes only, ignore check ids
    ("m4-exit-code-only", "matrix", MATRIX,
     '''            ok = (p.returncode == expected_rc and len(checks) == 7 and failed == expected_failed
                  and any(line.startswith("C2=" + summary + " checks=") for line in p.stdout.splitlines()))''',
     '''            ok = p.returncode == expected_rc'''),
    # M5: skip restoring fixture bytes between cases
    ("m5-no-fixture-restore", "matrix", MATRIX,
     '''            # Restore fixture bytes, never the caller's working tree or index.
            for key, value in FILES.items():
                (root / key).write_text(value)
            if path:''',
     '''            if path:'''),
    # M6: the receipt fixture/case points at a path no counter monitors
    ("m6-receipt-wrong-path", "matrix", MATRIX,
     '''    "corpus/evidence/round72/controls/battery-past-locale-dies-pinzone-r72.txt",''',
     '''    "corpus/evidence/round72/controls/battery-past-locale-dies-pinzone-r72-wrong.txt",'''),
    # M7: in the battery, a forger counts as rejected when its exit is 0
    ("m7-battery-forger-exit0", "battery", BATTERY,
     '''                    ok = all(rc == 1 and marks is not None and marks[0] < marks[1]
                             for rc, marks in runs)''',
     '''                    ok = all(rc == 0 and marks is not None and marks[0] < marks[1]
                             for rc, marks in runs)'''),
]

for name, kind, text, old, new in MUTANTS:
    hits = text.count(old)
    assert hits == 1, f"{name}: expected 1 occurrence of the old block, found {hits}"
    out = OUT / f"{name}.py"
    out.write_text(text.replace(old, new))
    print(f"WROTE {out}")

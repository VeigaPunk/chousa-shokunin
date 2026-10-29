#!/usr/bin/env python3
"""MutPre12 batch 2 — additional NEW single-defect mutants of the R63-C1 reference preflight.

Same contract as run-mutants.py: read-only on the reference, mutants written into scratch,
frozen battery c1-battery.py as the only detector.
"""
from __future__ import annotations

import argparse
import hashlib
import pathlib
import shutil
import subprocess
import sys

LANE = pathlib.Path("/home/vgpnk/Projects/shokunin/chousa-shokunin")
FLEET = pathlib.Path("/home/vgpnk/Projects/shokunin")
REF = LANE / "corpus/evidence/round63/controls/pos-ref-preflight.py"
BAT = LANE / "corpus/evidence/round63/c1-battery.py"

MUTANTS = [
    # N05b — corrected form: census findings (exit 1) treated as a pass
    ("N05b-g01-census-exit1-is-pass",
     'if p.returncode == 0 else ("FAIL", f"exit={p.returncode} "',
     'if p.returncode != 2 else ("FAIL", f"exit={p.returncode} "',
     ["CLEAN", "D01", "D02", "D03", "D11"]),
    # N17 — G02 skips knowledge entries whose name starts with zz
    ("N17-g02-skips-zz-prefixed-entries",
     '    files = sorted(f.name for f in kd.glob("*.md")) if kd.is_dir() else []\n',
     '    files = sorted(f.name for f in kd.glob("*.md") if not f.name.startswith("zz")) if kd.is_dir() else []\n',
     ["CLEAN", "D04", "D05", "D11"]),
    # N18 — G01 script discovery: lane parent first, --fleet last
    ("N18-g01-parent-scripts-beat-fleet",
     '''    if fleet:
        cands.append(pathlib.Path(fleet) / "scripts" / "sources-census.sh")
    elif os.environ.get("SHOKUNIN_ROOT"):
''',
     '''    cands.append(root.resolve().parent / "scripts" / "sources-census.sh")
    if fleet:
        cands.append(pathlib.Path(fleet) / "scripts" / "sources-census.sh")
    elif os.environ.get("SHOKUNIN_ROOT"):
''',
     ["CLEAN", "D12"]),
    # N19 — G02 only inspects the first knowledge entry
    ("N19-g02-only-first-entry-checked",
     '    files = sorted(f.name for f in kd.glob("*.md")) if kd.is_dir() else []\n',
     '    files = sorted(f.name for f in kd.glob("*.md"))[:1] if kd.is_dir() else []\n',
     ["CLEAN", "D04", "D05", "D11"]),
    # N20 — G02 tautology: only names already in the README are checked
    ("N20-g02-tautological-index-check",
     '    miss = [f for f in files if f not in readme]\n',
     '    miss = [f for f in files if f not in readme and f in readme]\n',
     ["CLEAN", "D04", "D05", "D11"]),
    # N21 — G01 runs the census with the lane root as cwd removed (cwd=/)
    ("N21-g01-census-run-from-root",
     '    p, err = run(["bash", str(sc), "validate", "--file", str(reg)], root, env, 300)\n',
     '    p, err = run(["bash", str(sc), "validate", "--file", str(reg)], root, env, 1)\n',
     ["CLEAN", "D01", "D02", "D03", "D11"]),
    # N22 — G01 detail: the E-line is not read, but the verdict is kept (cosmetic probe)
    ("N22-g01-census-errors-not-parsed",
     '    errs = [l for l in p.stdout.splitlines() if "\\tE" in l]\n',
     '    errs = []\n',
     ["CLEAN", "D01", "D02", "D03", "D11"]),
    # N23 — G02 checks a file name against the README of the wrong corpus tree
    ("N23-g02-readme-from-fleet-root",
     '    kd, rd = root / "corpus" / "knowledge", root / "corpus" / "README.md"\n',
     '    kd, rd = root / "corpus" / "knowledge", root.parent / "corpus" / "README.md"\n',
     ["CLEAN", "D04", "D05", "D11"]),
]


def sha(p: pathlib.Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--scratch", required=True)
    ap.add_argument("--jobs", type=int, default=2)
    ap.add_argument("--only", default=None)
    a = ap.parse_args()
    sc = pathlib.Path(a.scratch)
    mut_dir = sc / "mut2"
    mut_dir.mkdir(parents=True, exist_ok=True)
    src = REF.read_text(encoding="utf-8")
    keep = set(a.only.split(",")) if a.only else None
    plan = []
    for name, old, new, legs in MUTANTS:
        if keep and name not in keep:
            continue
        n = src.count(old)
        if n != 1:
            print(f"SKIP {name}: anchor occurs {n} times", file=sys.stderr)
            continue
        p = mut_dir / f"{name}.py"
        p.write_text(src.replace(old, new, 1), encoding="utf-8")
        plan.append((name, p, legs))

    results = []
    for name, tool, legs in plan:
        work = sc / "w2" / name
        if work.exists():
            shutil.rmtree(work)
        cmd = [sys.executable, "-B", str(BAT), "--tool", str(tool),
               "--fleet", str(FLEET), "--work", str(work), "--jobs", str(a.jobs),
               "--only", ",".join(legs)]
        p = subprocess.run(cmd, capture_output=True, text=True, timeout=3600)
        leg_lines = [l for l in p.stdout.splitlines() if l.startswith("LEG ")]
        failing = [l.split()[1] for l in leg_lines if " FAIL " in l]
        results.append((name, failing, p.stdout, p.returncode))
        print(f"== {name}: rc={p.returncode} failing_legs={','.join(failing) or '-'}")
        for l in leg_lines:
            print("   " + l)
        if p.returncode != 0:
            print("   stderr: " + p.stderr.strip()[:200])
        shutil.rmtree(sc / "w2", ignore_errors=True)

    print("\nSUMMARY name verdict failing_legs")
    for name, failing, out, rc in results:
        print(f"{name} {'KILLED' if failing else 'SURVIVED'} {','.join(failing) or '-'}")
    print(f"REF_SHA={sha(REF)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

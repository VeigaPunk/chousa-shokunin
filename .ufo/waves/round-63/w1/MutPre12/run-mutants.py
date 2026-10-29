#!/usr/bin/env python3
"""MutPre12 — R63-C1 mutation probe (G01 census / G02 knowledge-index focused).

Generates NEW single-defect mutants of the reference preflight
corpus/evidence/round63/controls/pos-ref-preflight.py (beyond M01-M16 of
controls/run-c1-controls.py), then runs the FROZEN battery
corpus/evidence/round63/c1-battery.py against each with --only naming the legs
that should kill it plus CLEAN.

Nothing under corpus/ , tools/ or SKILL.md is written; the reference is read
only.  Mutant bytes live in the scratch tree and are removed at the end.

Usage: python3 -B run-mutants.py --scratch DIR [--jobs 2] [--only NAME[,NAME]]
"""
from __future__ import annotations

import argparse
import hashlib
import pathlib
import re
import shutil
import subprocess
import sys

LANE = pathlib.Path("/home/vgpnk/Projects/shokunin/chousa-shokunin")
FLEET = pathlib.Path("/home/vgpnk/Projects/shokunin")
REF = LANE / "corpus/evidence/round63/controls/pos-ref-preflight.py"
BAT = LANE / "corpus/evidence/round63/c1-battery.py"

# ---- NEW mutants (M17.. naming kept distinct from the frozen M01-M16 set) ----
# each: (name, old, new, legs that should kill it)
G01_SRC = '''    if fleet:
        cands.append(pathlib.Path(fleet) / "scripts" / "sources-census.sh")
    elif os.environ.get("SHOKUNIN_ROOT"):
        cands.append(pathlib.Path(os.environ["SHOKUNIN_ROOT"]) / "scripts" / "sources-census.sh")
    else:
'''
G01_SRC_NEW = '''    if os.environ.get("SHOKUNIN_ROOT"):
        cands.append(pathlib.Path(os.environ["SHOKUNIN_ROOT"]) / "scripts" / "sources-census.sh")
    elif fleet:
        cands.append(pathlib.Path(fleet) / "scripts" / "sources-census.sh")
    else:
'''

MUTANTS = [
    # G01 family
    ("N01-g01-registry-absent-env",
     '        return "FAIL", "corpus/SOURCES.md absent"\n',
     '        return "ENV", "corpus/SOURCES.md absent"\n',
     ["CLEAN", "D01", "D02", "D03", "D11", "D12"]),
    ("N02-g01-registry-absent-check-dropped",
     '    if not reg.is_file():\n        return "FAIL", "corpus/SOURCES.md absent"\n',
     '    if False:\n        return "FAIL", "corpus/SOURCES.md absent"\n',
     ["CLEAN", "D01", "D02", "D03", "D11"]),
    ("N03-g01-shokunin-root-beats-fleet",
     G01_SRC, G01_SRC_NEW,
     ["CLEAN", "D12"]),
    ("N04-g01-script-existence-ignored",
     '    return next((c for c in cands if c.is_file()), None)\n',
     '    return cands[0]\n',
     ["CLEAN", "D12"]),
    ("N05-g01-census-exit2-treated-pass",
     'if p.returncode == 0 else ("FAIL", f"exit={p.returncode} "',
     'if p.returncode != 1 else ("FAIL", f"exit={p.returncode} "',
     ["CLEAN", "D01", "D02", "D03", "D11"]),
    ("N06-g01-env-does-not-change-exit-code",
     '    return 1 if failed else (2 if envs else 0)\n',
     '    return 1 if failed else 0\n',
     ["CLEAN", "D12"]),
    ("N13-g01-no-census-script-is-fail-not-env",
     '        return "ENV", "no sources-census.sh (pass --fleet DIR, or set SHOKUNIN_ROOT, or run inside a fleet layout)"\n',
     '        return "FAIL", "no sources-census.sh (pass --fleet DIR, or set SHOKUNIN_ROOT, or run inside a fleet layout)"\n',
     ["CLEAN", "D12"]),
    ("N14-g01-fleet-flag-ignored",
     '    if fleet:\n        cands.append(pathlib.Path(fleet) / "scripts" / "sources-census.sh")\n    elif os.environ.get("SHOKUNIN_ROOT"):\n',
     '    if os.environ.get("SHOKUNIN_ROOT"):\n',
     ["CLEAN", "D01"]),
    # G02 family
    ("N07-g02-stem-not-file-name",
     '    miss = [f for f in files if f not in readme]\n',
    '    miss = [f for f in files if pathlib.Path(f).stem not in readme]\n',
     ["CLEAN", "D04", "D05", "D11"]),
    ("N08-g02-first-missing-dropped",
     '    miss = [f for f in files if f not in readme]\n',
     '    miss = [f for f in files if f not in readme][1:]\n',
     ["CLEAN", "D04", "D05", "D11"]),
    ("N09-g02-case-insensitive-index",
     '    miss = [f for f in files if f not in readme]\n',
     '    miss = [f for f in files if f.lower() not in readme.lower()]\n',
     ["CLEAN", "D04", "D05", "D11"]),
    ("N10-g02-near-miss-name-accepted",
     '    miss = [f for f in files if f not in readme]\n',
     '    miss = [f for f in files if f not in readme and pathlib.Path(f).stem not in readme]\n',
     ["CLEAN", "D04", "D05", "D11"]),
    ("N11-g02-readme-absent-is-pass",
     '    if not rd.is_file():\n        return "FAIL", "corpus/README.md absent"\n',
     '    if not rd.is_file():\n        return "PASS", "corpus/README.md absent"\n',
     ["CLEAN", "D04", "D05", "D11"]),
    ("N12-g02-count-check-not-membership",
     '    miss = [f for f in files if f not in readme]\n',
     '    miss = [] if sum(1 for f in files if f in readme) == len(files) else ["index-count-mismatch"]\n',
     ["CLEAN", "D04", "D05", "D11"]),
    ("N15-g01-census-mode-typo",
     '    p, err = run(["bash", str(sc), "validate", "--file", str(reg)], root, env, 300)\n',
     '    p, err = run(["bash", str(sc), "census", "--file", str(reg)], root, env, 300)\n',
     ["CLEAN", "D01", "D02", "D03", "D11"]),
    ("N16-g02-index-searched-in-whole-corpus",
     '    readme = read(rd)\n',
     '    readme = "".join(read(p) for p in sorted((root / "corpus").rglob("*.md")))\n',
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
    mut_dir = sc / "mut"
    mut_dir.mkdir(parents=True, exist_ok=True)
    src = REF.read_text(encoding="utf-8")
    ref_sha_before = sha(REF)

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

    # baseline: the pristine reference over the union of the legs we use
    union = sorted({l for _, _, legs in plan for l in legs})
    results = []
    for name, tool, legs in [("BASELINE-reference", REF, union)] + plan:
        work = sc / "w" / name
        if work.exists():
            shutil.rmtree(work)
        cmd = [sys.executable, "-B", str(BAT), "--tool", str(tool),
               "--fleet", str(FLEET), "--work", str(work), "--jobs", str(a.jobs),
               "--only", ",".join(legs)]
        p = subprocess.run(cmd, capture_output=True, text=True, timeout=3600)
        leg_lines = [l for l in p.stdout.splitlines() if l.startswith("LEG ")]
        failing = [l.split()[1] for l in leg_lines if " FAIL " in l]
        ok = [l.split()[1] for l in leg_lines if " FAIL " not in l]
        results.append((name, legs, failing, ok, p.stdout, p.returncode))
        print(f"== {name}: rc={p.returncode} failing_legs={','.join(failing) or '-'}")
        for l in leg_lines:
            print("   " + l)
        if p.returncode not in (0,):
            print("   stderr: " + p.stderr.strip()[:200])
        shutil.rmtree(sc / "w", ignore_errors=True)

    print("\nSUMMARY name verdict failing_legs")
    for name, legs, failing, ok, out, rc in results:
        verdict = "KILLED" if failing else "SURVIVED"
        if name == "BASELINE-reference" and failing:
            verdict = "BASELINE-FAIL(inconclusive)"
        print(f"{name} {verdict} {','.join(failing) or '-'}")

    print(f"REF_SHA_BEFORE={ref_sha_before}")
    print(f"REF_SHA_AFTER={sha(REF)}")
    print(f"REF_UNCHANGED={ref_sha_before == sha(REF)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

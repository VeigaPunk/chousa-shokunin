#!/usr/bin/env python3
"""MutPre678 — build NEW single-defect mutants of the round-63 reference preflight.

Scope: the selftest runner (gates G06 / G07 / G08 — exit code, token, timeout, missing tool) and the
`run()` helper that executes the lane's committed tools.

M01..M16 (corpus/evidence/round63/controls/run-c1-controls.py) are NOT repeated here; this file's
mutants are each a single text substitution on the pristine reference bytes, and none of them is one
of the M01..M16 substitutions.

Usage: python3 -B make-mutants.py --src REF --out DIR
"""
from __future__ import annotations

import argparse
import pathlib

# name -> (old, new, note)
MUTANTS: dict[str, tuple[str, str, str]] = {
    # --- selftest: exit code -------------------------------------------------
    "X01-selftest-exit-inverted": (
        '    if p.returncode != 0:\n        return "FAIL", f"exit={p.returncode}"',
        '    if p.returncode == 0:\n        return "FAIL", f"exit={p.returncode}"',
        "the exit-code check is inverted (a clean exit fails the gate)",
    ),
    "X06-g08-exit-check-skipped-for-sh": (
        '    if p.returncode != 0:\n        return "FAIL", f"exit={p.returncode}"',
        '    if p.returncode != 0 and tool.endswith(".py"):\n'
        '        return "FAIL", f"exit={p.returncode}"',
        "the exit-code check is skipped for the shell selftest (G08)",
    ),
    # --- selftest: token -----------------------------------------------------
    "X04-selftest-token-read-stderr": (
        "    if token and token not in p.stdout:",
        "    if token and token not in p.stderr:",
        "the token is looked for on stderr instead of stdout",
    ),
    "X07-g08-token-wrong": (
        '"RESEARCH_GATE_SELFTEST: PASS", 1500,',
        '"RESEARCH_GATE_SELFTEST: OK", 1500,',
        "G08 looks for a token the gate script never prints",
    ),
    # --- selftest: timeout ---------------------------------------------------
    "X15-g06-timeout-one-second": (
        '"FREEZE_CHECK=", 300,',
        '"FREEZE_CHECK=", 1,',
        "G06 timeout cut below the freeze-check selftest's real runtime",
    ),
    "X16-g07-timeout-zero": (
        '"SELFTEST=PASS", 300,',
        '"SELFTEST=PASS", 0,',
        "G07 timeout set to zero (immediate expiry)",
    ),
    "X08-g08-timeout-one-second": (
        '"RESEARCH_GATE_SELFTEST: PASS", 1500,',
        '"RESEARCH_GATE_SELFTEST: PASS", 1,',
        "G08 timeout cut below the gate selftest's real runtime",
    ),
    "X12-run-timeout-kwarg-dropped": (
        "capture_output=True, text=True, timeout=timeout,",
        "capture_output=True, text=True,",
        "run() never bounds a tool that hangs",
    ),
    # --- selftest: missing tool ----------------------------------------------
    "X10-missing-tool-passes": (
        '        return "FAIL", f"{tool} absent"',
        '        return "PASS", f"{tool} absent"',
        "an absent selftest tool counts as a pass",
    ),
    "X11-missing-tool-env": (
        '        return "FAIL", f"{tool} absent"',
        '        return "ENV", f"{tool} absent"',
        "an absent selftest tool is reported as ENV (exit 2), not FAIL",
    ),
    # --- run() helper --------------------------------------------------------
    "X05-run-text-false": (
        "capture_output=True, text=True, timeout=timeout,",
        "capture_output=False, timeout=timeout,",
        "run() returns bytes, so the token check raises (gate crash)",
    ),
    "X14-run-cwd-dropped": (
        "p = subprocess.run(cmd, cwd=root, env=env,",
        "p = subprocess.run(cmd, cwd=None, env=env,",
        "run() no longer runs the committed tool inside --root",
    ),
    # --- invocation shape ----------------------------------------------------
    "X02-g07-selftest-flag-dropped": (
        '[sys.executable, "-B", "tools/assimilate-rows.py", "--selftest"]',
        '[sys.executable, "-B", "tools/assimilate-rows.py"]',
        "G07 no longer asks the tool for its selftest mode",
    ),
    "X03-g06-lane-root-wrong": (
        '"--selftest", "--lane-root", str(root),',
        '"--selftest", "--lane-root", str(root.parent),',
        "G06 points the selftest at the wrong lane root",
    ),
    "X13-g06-lane-root-dropped": (
        '"--selftest", "--lane-root", str(root),\n                     "--work", str(work / "g06")]',
        '"--selftest",\n                     "--work", str(work / "g06")]',
        "G06 lets the tool read its absolute default lane root, outside --root",
    ),
    "X22-selftest-exit-code-above-one": (
        '    if p.returncode != 0:\n        return "FAIL", f"exit={p.returncode}"',
        '    if p.returncode > 1:\n        return "FAIL", f"exit={p.returncode}"',
        "a selftest that exits 1 (its own failure code) counts as a pass",
    ),
    "X25-g06-token-prefix-only": (
        '"FREEZE_CHECK=", 300,',
        '"FREEZE_CHECK", 300,',
        "G06 accepts a shorter token that the selftest prints on failure too",
    ),
    "X23-g06-selftest-flag-dropped": (
        '[sys.executable, "-B", "tools/freeze-check.py", "--selftest", "--lane-root", str(root),',
        '[sys.executable, "-B", "tools/freeze-check.py", "--lane-root", str(root),',
        "G06 no longer asks the tool for its selftest mode",
    ),
    "X26-run-timeout-treated-as-pass": (
        '    except subprocess.TimeoutExpired:\n        return None, f"timeout after {timeout}s"',
        '    except subprocess.TimeoutExpired:\n'
        '        return subprocess.CompletedProcess(cmd, 0, "FREEZE_CHECK=\\nSELFTEST=PASS\\n'
        'RESEARCH_GATE_SELFTEST: PASS\\n", ""), ""',
        "a tool that times out is reported as a pass",
    ),
    "X27-run-stdin-inherited": (
        "capture_output=True, text=True, timeout=timeout,\n                           stdin=subprocess.DEVNULL)",
        "capture_output=True, text=True, timeout=timeout)",
        "the child tool inherits the preflight's stdin",
    ),
    "X28-missing-tool-path-wrong": (
        "    if not (root / tool).is_file():",
        "    if not (root.parent / tool).is_file():",
        "the absent-tool check looks one directory up",
    ),
    "X29-g06-work-inside-the-lane": (
        '"--work", str(work / "g06")]',
        '"--work", str(root / "g06-work")]',
        "G06 writes its scratch inside the lane instead of under --work",
    ),
    "X31-selftest-failure-reported-as-env": (
        '    if p.returncode != 0:\n        return "FAIL", f"exit={p.returncode}"',
        '    if p.returncode != 0:\n        return "ENV", f"exit={p.returncode}"',
        "a failing selftest is reported as ENV (exit 2) instead of FAIL",
    ),
    "X32-missing-tool-check-removed": (
        '    if not (root / tool).is_file():\n        return "FAIL", f"{tool} absent"\n',
        '',
        "the absent-tool check is removed altogether",
    ),
    "X09-g08-cmd-path-wrong": (
        '["bash", "tools/research-gate.sh", "--selftest"]',
        '["bash", "tools/research-gate.shx", "--selftest"]',
        "G08 names a script that does not exist",
    ),
}

# expected detector legs per mutant (CLEAN is always run with them)
EXPECT: dict[str, list[str]] = {
    "X01-selftest-exit-inverted": ["CLEAN"],
    "X02-g07-selftest-flag-dropped": ["CLEAN"],
    "X03-g06-lane-root-wrong": ["CLEAN"],
    "X04-selftest-token-read-stderr": ["CLEAN"],
    "X05-run-text-false": ["CLEAN"],
    "X06-g08-exit-check-skipped-for-sh": ["CLEAN"],
    "X07-g08-token-wrong": ["CLEAN"],
    "X08-g08-timeout-one-second": ["CLEAN"],
    "X09-g08-cmd-path-wrong": ["CLEAN"],
    "X10-missing-tool-passes": ["CLEAN"],
    "X11-missing-tool-env": ["CLEAN"],
    "X12-run-timeout-kwarg-dropped": ["CLEAN"],
    "X13-g06-lane-root-dropped": ["CLEAN"],
    "X14-run-cwd-dropped": ["CLEAN"],
    "X15-g06-timeout-one-second": ["CLEAN"],
    "X16-g07-timeout-zero": ["CLEAN"],
    "X22-selftest-exit-code-above-one": ["CLEAN", "D09", "D10"],
    "X25-g06-token-prefix-only": ["CLEAN", "D09"],
    "X23-g06-selftest-flag-dropped": ["CLEAN"],
    "X26-run-timeout-treated-as-pass": ["CLEAN", "D09", "D10"],
    "X27-run-stdin-inherited": ["CLEAN"],
    "X28-missing-tool-path-wrong": ["CLEAN", "D09", "D10"],
    "X29-g06-work-inside-the-lane": ["CLEAN"],
    "X31-selftest-failure-reported-as-env": ["CLEAN", "D09", "D10"],
    "X32-missing-tool-check-removed": ["CLEAN", "D09", "D10"],
}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", required=True)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    src = pathlib.Path(a.src).read_text(encoding="utf-8")
    out = pathlib.Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    for name, (old, new, note) in MUTANTS.items():
        n = src.count(old)
        if n != 1:
            raise SystemExit(f"{name}: pattern occurs {n} times (need exactly 1): {old!r}")
        (out / f"{name}.py").write_text(src.replace(old, new), encoding="utf-8")
        print(f"{name}\t{note}")
    (out / "EXPECT.tsv").write_text(
        "".join(f"{k}\t{','.join(v)}\n" for k, v in EXPECT.items()), encoding="utf-8")
    print(f"MUTANTS={len(MUTANTS)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

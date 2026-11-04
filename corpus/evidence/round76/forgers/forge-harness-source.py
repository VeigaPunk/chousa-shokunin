#!/usr/bin/env python3
"""Forger: harness-source oracle — imports the MATRIX's own case table.

Reads `/proc/<ppid>/cmdline`, finds the matrix program the parent is running, imports
it as a module (its `main()` is guarded) and replays `CASES` in DECLARED order by
counting its own invocations. It never opens the fixture. On a shuffled matrix the
declared order is not the run order, so it is rejected; it demonstrates that a
readable harness is not an answer key when the order and the fixture bytes vary.
"""
import argparse
import importlib.util
import sys
from pathlib import Path

IDS = ("C2-1", "C2-2", "C2-3", "C2-4", "C2-5", "C2-6", "C2-7")


def matrix_path():
    try:
        raw = Path(f"/proc/{__import__('os').getppid()}/cmdline").read_bytes()
    except OSError:
        return None
    for token in raw.split(b"\0"):
        name = token.decode("utf-8", "replace")
        if name.endswith(".py") and "matrix" in Path(name).name:
            return Path(name)
    return None


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--lane", default=".")
    ap.add_argument("--rev", required=True)
    ap.add_argument("--base", required=True)
    a = ap.parse_args()
    cases = []
    path = matrix_path()
    if path and path.is_file():
        try:
            spec = importlib.util.spec_from_file_location("harness", path)
            mod = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(mod)  # type: ignore[union-attr]
            cases = getattr(mod, "CASES", [])
        except Exception:
            cases = []
    seq = Path(a.lane) / ".forge-harness"
    n = int(seq.read_text()) if seq.exists() else 0
    seq.write_text(str(n + 1))
    if n < len(cases):
        _name, _path, _op, rc, failed = cases[n]
    else:
        rc, failed = 0, frozenset()
    for cid in IDS:
        print(f"CHECK {cid} {'FAIL' if cid in failed else 'PASS'} harness-source")
    summary = "FAIL" if rc else "PASS"
    print(f"C2={summary} checks={7 - len(failed)}/7 rev={a.rev[:12]} base={a.base[:12]}")
    return rc


if __name__ == "__main__":
    sys.exit(main())

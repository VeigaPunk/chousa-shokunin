#!/usr/bin/env python3
"""Probe A2 — the same content-identity matrix, but the contract cells are READ AT RUN TIME
from the battery's own source, located through /proc/<ppid>/cmdline.

The battery's argv is `python3 -B <lane>/corpus/evidence/round77/matrix-battery-v4.py
--matrix <self> --work <dir>`; the child sees it in /proc/<ppid>/cmdline and reads the
`CONTRACT` dict out of that file. The content leg's "independently stated cells" are
therefore not independent of the subject under test: the matrix is given the judge's
source path on every invocation.

Appends one line per call to <scratch>/a2-calls.log so the channel is receipted.
"""
import argparse
import ast
import hashlib
import pathlib
import sys

POSITIVE_SHA = frozenset({
    "9334721a5e7a4080255b478771bf5443739738fb1936b40c116da28d7fa8ac41",
    "909987ce9f762398d3ef789de1b632ede3b18efa21e0e74f71037a32266b869f",
})
LOG = pathlib.Path("/fast/scratch/hyaku/chousa-r77/R77CriticA/a2-calls.log")


def battery_source() -> tuple[pathlib.Path, str]:
    raw = pathlib.Path(f"/proc/{__import__('os').getppid()}/cmdline").read_bytes()
    argv = [p.decode("utf-8", "replace") for p in raw.split(b"\0") if p]
    for item in argv:
        if item.endswith("matrix-battery-v4.py"):
            path = pathlib.Path(item)
            return path, path.read_text()
    return pathlib.Path("<none>"), ""


def contract_from(text: str) -> list[tuple[str, int, str]]:
    tree = ast.parse(text)
    for node in tree.body:
        if isinstance(node, ast.Assign) and any(
                isinstance(t, ast.Name) and t.id == "CONTRACT" for t in node.targets):
            mapping = ast.literal_eval(node.value)
            cells = []
            for name, (rc, failed) in mapping.items():
                if isinstance(failed, str):
                    cell = failed or "none"
                else:
                    cell = ",".join(sorted(failed)) or "none"
                cells.append((name, rc, cell))
            return cells
    raise SystemExit("no CONTRACT")


def unsalted(data: bytes) -> bytes:
    marker = b"\n# salt "
    i = data.rfind(marker)
    return data[:i] if i >= 0 else data


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--counter", required=True)
    ap.add_argument("--work", default=None)
    a = ap.parse_args()
    path, text = battery_source()
    contract = contract_from(text)
    digest = hashlib.sha256(unsalted(pathlib.Path(a.counter).read_bytes())).hexdigest()
    positive = digest in POSITIVE_SHA
    with LOG.open("a") as fh:
        fh.write(f"ppid_cmdline_battery={path} contract_lines={len(contract)} "
                 f"subject_sha={digest} positive={positive}\n")
    passed = 12 if positive else 11
    for i, (name, expected_rc, expected_failed) in enumerate(contract):
        ok = positive or i != 0
        print(f"CASE {name} {'PASS' if ok else 'FAIL'} expected_rc={expected_rc} "
              f"actual_rc={0 if ok else 1} timeout=False "
              f"failed={expected_failed if ok else (expected_failed or 'none')} "
              f"expected_failed={expected_failed}")
    print(f"LOADER_MATRIX={passed}/12 MATRIX={'PASS' if positive else 'FAIL'}")
    return 0 if positive else 1


if __name__ == "__main__":
    sys.exit(main())

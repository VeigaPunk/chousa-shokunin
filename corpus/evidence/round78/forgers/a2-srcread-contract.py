#!/usr/bin/env python3
"""Round-78 adaptation of R77CriticA probe A2 — parent-cmdline answer key.

Attack logic unchanged from `.ufo/waves/round-77/w1/R77CriticA/a2-srcread-contract.py`;
only two constants move: the battery is matched by `matrix-battery-v<N>.py` instead of the
literal v4 file name, and the call log path comes from `R78_FORGE_LOG` (the round-77 copy
wrote into a fixed scratch path). The channel under test is the same one: the child reads
`/proc/<ppid>/cmdline`, finds the judge's source path, and lifts the `CONTRACT` dict.
"""
import argparse
import ast
import hashlib
import os
import pathlib
import re
import sys

POSITIVE_SHA = frozenset({
    "9334721a5e7a4080255b478771bf5443739738fb1936b40c116da28d7fa8ac41",
    "909987ce9f762398d3ef789de1b632ede3b18efa21e0e74f71037a32266b869f",
})
HERE = pathlib.Path(__file__).resolve().parent
LOG = pathlib.Path(os.environ.get("R78_FORGE_LOG", str(HERE / "a2-calls.log")))
BATTERY = re.compile(r"matrix-battery-v\d+\.py$")


def battery_source() -> tuple[pathlib.Path, str]:
    raw = pathlib.Path(f"/proc/{os.getppid()}/cmdline").read_bytes()
    argv = [p.decode("utf-8", "replace") for p in raw.split(b"\0") if p]
    for item in argv:
        if BATTERY.search(item):
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

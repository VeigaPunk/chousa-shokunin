#!/usr/bin/env python3
"""c1-count — frozen counter for round 45 claim C1 (operability).

Predicate R45-C1, the same sentence as corpus/evidence/round45/claims.md:
tools/parent-lifetime.sh, run with a stub `kimi` first on PATH, (a) exits 3
on a dispatch with zero tasks and still writes `end ... n_spawned=0`;
(b) exits 0 on a two-seat dispatch whose stub exits 0, with
`n_spawned=2 n_reaped=2`; (c) exits 3 on a two-seat dispatch whose stub
outlives `--timeout 1`, with both reap lines `exit_code=124`; (d) exits 2
when a dispatch run omits `--timeout`; and (e) every receipt of (a)-(c)
opens with a start line carrying `timeout_s=<the value passed>`.

Cheapest gate that would score full marks without the work (QUALITY 60):
the round-44 launcher itself. It exits 0 on (a) and (c), runs (d) on a
silent 420 s default, and its start line has no timeout_s, so it scores
1/5 (case b only). Committed as controls/c1-control-r44-tool.txt.

Exit codes: 0 CASES_MATCH=5/5 · 1 any case failed · 2 usage/env.
"""
from __future__ import annotations

import argparse
import json
import os
import pathlib
import re
import subprocess
import sys
import tempfile

LANE = pathlib.Path(__file__).resolve().parents[3]
TOOL = LANE / "tools" / "parent-lifetime.sh"

STUB = """#!/bin/sh
case "${STUB_MODE:-ok}" in
  ok) exit 0 ;;
  hang) exec sleep 30 ;;
esac
exit 9
"""


def dispatch(path: pathlib.Path, names: list[str]) -> None:
    tasks = [{"name": n, "task": f"stub seat {n}"} for n in names]
    path.write_text(json.dumps({"taskCall": {"context": "c", "tasks": tasks}}), encoding="utf-8")


def run(tool: pathlib.Path, tmp: pathlib.Path, tag: str, names: list[str] | None,
        timeout: str | None, mode: str) -> tuple[int, str]:
    d = tmp / tag
    d.mkdir()
    disp = d / "dispatch.json"
    dispatch(disp, names or [])
    agent = d / "agent.yaml"
    agent.write_text("stub\n", encoding="utf-8")
    receipt = d / "receipt"
    argv = ["bash", str(tool), "--dispatch", str(disp), "--receipt", str(receipt),
            "--agent", str(agent)]
    if timeout is not None:
        argv += ["--timeout", timeout]
    env = dict(os.environ, PATH=f"{tmp / 'bin'}:{os.environ.get('PATH', '')}", STUB_MODE=mode)
    p = subprocess.run(argv, env=env, capture_output=True, text=True, timeout=120)
    text = receipt.read_text(encoding="utf-8") if receipt.is_file() else ""
    return p.returncode, text


def end_line(text: str) -> str:
    ends = [l for l in text.splitlines() if l.startswith("end ")]
    return ends[-1] if ends else ""


def start_has(text: str, value: str) -> bool:
    lines = text.splitlines()
    return bool(lines) and lines[0].startswith("start ") and f" timeout_s={value}" in lines[0] + " "


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--tool", default=str(TOOL))
    a = ap.parse_args()
    tool = pathlib.Path(a.tool)
    if not tool.is_file():
        print("C1=FAIL tool-missing")
        return 1
    results = {}
    with tempfile.TemporaryDirectory(prefix="chousa-r45-c1-") as t:
        tmp = pathlib.Path(t)
        (tmp / "bin").mkdir()
        stub = tmp / "bin" / "kimi"
        stub.write_text(STUB, encoding="utf-8")
        stub.chmod(0o755)

        ec, rec = run(tool, tmp, "a", [], "5", "ok")
        results["a_empty_exits_3"] = ec == 3 and re.search(r"\bn_spawned=0\b", end_line(rec)) is not None
        a_start = start_has(rec, "5")

        ec, rec = run(tool, tmp, "b", ["SeatA", "SeatB"], "5", "ok")
        results["b_ok_exits_0"] = (ec == 0 and "n_spawned=2" in end_line(rec)
                                   and "n_reaped=2" in end_line(rec))
        b_start = start_has(rec, "5")

        ec, rec = run(tool, tmp, "c", ["SeatA", "SeatB"], "1", "hang")
        reaps = [l for l in rec.splitlines() if l.startswith("reap ")]
        results["c_timeout_exits_3"] = (ec == 3 and len(reaps) == 2
                                        and all(" exit_code=124 " in l + " " for l in reaps))
        c_start = start_has(rec, "1")

        ec, _ = run(tool, tmp, "d", ["SeatA"], None, "ok")
        results["d_no_timeout_exits_2"] = ec == 2

        results["e_start_timeout_s"] = a_start and b_start and c_start

    for k, v in results.items():
        print(f"CASE {k}={'ok' if v else 'FAIL'}")
    n = sum(results.values())
    print(f"CASES_MATCH={n}/{len(results)}")
    ok = n == len(results)
    print("C1=PASS" if ok else "C1=FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())

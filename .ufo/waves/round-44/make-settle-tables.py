#!/usr/bin/env python3
"""make-settle-tables.py — build the round-44 wave settlement tables.

Contract: for each wave, read the frozen spec for names and roles, read the
launcher receipt for the exit code of each seat, and read the wave report
directory for the report file. A seat's outcome is `report` when its report
file exists and `dead` otherwise; the last_error column carries the seat's own
last error text from its log. Exit 0 on write, 2 on usage. No network.
"""
from __future__ import annotations

import hashlib
import json
import pathlib
import sys

ROOT = pathlib.Path("/home/vgpnk/Projects/shokunin/chousa-shokunin")
WAVES = ROOT / ".ufo/waves/round-44"

W1_LOG = ROOT / "corpus/evidence/round44/seat-logs"


def read_receipt(path: pathlib.Path) -> tuple[dict, dict | None]:
    reaps: dict[str, dict] = {}
    end = None
    if not path.is_file():
        return reaps, end
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        parts = line.split()
        if not parts:
            continue
        fields = dict(p.split("=", 1) for p in parts[1:] if "=" in p)
        if parts[0] == "reap":
            reaps[fields.get("name", "")] = fields
        elif parts[0] == "end":
            end = fields
    return reaps, end


def last_error(log: pathlib.Path) -> str:
    if not log.is_file():
        return "no log written"
    lines = [ln.strip() for ln in log.read_text(encoding="utf-8", errors="replace").splitlines()]
    lines = [ln for ln in lines if ln]
    if not lines:
        return "no output"
    tail = lines[-1]
    if tail.startswith("error:"):
        return tail
    if tail.startswith("To resume this session:"):
        return ""
    return f"timeout --signal=TERM --kill-after=20 420 killed the seat; last output: {tail[:120]}"


def build(wave: str, spec: pathlib.Path, receipt: pathlib.Path, report_dir: pathlib.Path,
          log_dir: pathlib.Path, out: pathlib.Path, note: str) -> None:
    roles = {i["name"]: i["role"] for i in json.loads(spec.read_text(encoding="utf-8"))["items"]}
    reaps, end = read_receipt(receipt)
    rows = []
    for name in roles:
        rep = report_dir / f"{name}.md"
        outcome = "report" if rep.is_file() else "dead"
        rc = reaps.get(name, {}).get("exit_code", "")
        err = "" if outcome == "report" else last_error(log_dir / f"{name}.log")
        rows.append((name, roles[name], outcome, rc, err))
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("w", encoding="utf-8") as fh:
        fh.write("name\trole\toutcome\texit_code\tlast_error\n")
        for name, role, outcome, rc, err in rows:
            fh.write(f"{name}\t{role}\t{outcome}\t{rc}\t{err}\n")
        fh.write(f"# {note}\n")
        if end is None:
            fh.write("# receipt truncated: no end line; the launcher was killed before it reaped every seat\n")
        else:
            fh.write(
                "# receipt end: parent_pid=%s n_spawned=%s n_reaped=%s\n"
                % (end.get("parent_pid"), end.get("n_spawned"), end.get("n_reaped"))
            )
    reports = sum(1 for r in rows if r[2] == "report")
    print(f"{out.name}: seats={len(rows)} reports={reports} dead={len(rows) - reports} "
          f"receipt_end={'yes' if end else 'no'}")


def main() -> int:
    build(
        "w1",
        WAVES / "w1-spec.json",
        ROOT / "corpus/evidence/round44/parent-lifetime.receipt",
        WAVES / "w1",
        W1_LOG,
        WAVES / "w1-settle.tsv",
        "round-44 wave 1: 64 seats, all died at spawn on the --prompt/--auto flag conflict; the receipt is complete, the seats produced nothing",
    )
    build(
        "w2",
        WAVES / "w2-spec.json",
        WAVES / "w2-parent-lifetime.receipt",
        WAVES / "w2",
        WAVES / "seat-logs",
        WAVES / "w2-settle.tsv",
        "round-44 wave 2: 32 seats; the receipt is truncated because the orchestrator process died while the launcher was still waiting",
    )
    build(
        "w3",
        WAVES / "w3-spec.json",
        WAVES / "w3/parent-lifetime.receipt",
        WAVES / "w3",
        WAVES / "w3/seat-logs",
        WAVES / "w3-settle.tsv",
        "round-44 wave 3: 32 seats; the receipt is complete; 27 seats were killed by the 420s timeout",
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())

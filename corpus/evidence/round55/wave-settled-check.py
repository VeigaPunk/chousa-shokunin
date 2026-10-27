#!/usr/bin/env python3
"""wave-settled-check — a report is filed only after every dispatched wave of its round has settled.

Round 54 filed its report (fleet commit 23:50:07) while its W2 was still running; W2 was killed in
the orchestrator's session exit and its results were committed only by the orchestrator's salvage
`78ebc257` (round-55 lesson `## Mistakes`). The round prompt says not to file before WAVE-DONE for
every launched wave; the dispatcher writes `<wave>-results.json` when every seat settles, so the
lane-side receipt of WAVE-DONE is that file, committed.

For round N: every `<wave>.ready.dispatched` committed under `.ufo/waves/round-N/` of the lane must
have a `<wave>-results.json` added to the lane by a commit whose committer time is at or before the
fleet commit that added `.ufo/reports/round-N/<lane>.md`. Prints one line per wave
(`SETTLED <wave> results=<time>` / `UNSETTLED <wave> <why>`; a marker whose first line carries
` ABANDONED:` and no results file is `ABANDONED` — never run, so not running — and counts as settled),
then `WAVES=n SETTLED=k`.
With `--before-filing` (no report commit exists yet) every dispatched wave only needs a committed
results file.

Usage: python3 corpus/evidence/round55/wave-settled-check.py --round N [--lane DIR] [--fleet DIR] [--id chousa] [--before-filing]
Exit 0 all settled · 1 a wave unsettled · 2 usage (no dispatched wave, or no report commit without --before-filing).
"""
from __future__ import annotations

import argparse
import datetime as dt
import pathlib
import subprocess
import sys

LANE = pathlib.Path(__file__).resolve().parents[3]


def git(repo: pathlib.Path, *args: str) -> str:
    return subprocess.run(["git", "-C", str(repo), *args], capture_output=True, text=True).stdout.strip()


def added_at(repo: pathlib.Path, path: str) -> dt.datetime | None:
    out = git(repo, "log", "--diff-filter=A", "--format=%cI", "--", path).splitlines()
    return dt.datetime.fromisoformat(out[-1]) if out else None


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--round", type=int, required=True)
    ap.add_argument("--lane", default=str(LANE))
    ap.add_argument("--fleet", default=str(LANE.parent))
    ap.add_argument("--id", default="chousa")
    ap.add_argument("--before-filing", action="store_true")
    a = ap.parse_args()
    lane, fleet = pathlib.Path(a.lane), pathlib.Path(a.fleet)
    wd = f".ufo/waves/round-{a.round}"
    markers = sorted(p for p in git(lane, "ls-files", "--", wd).splitlines() if p.endswith(".ready.dispatched"))
    if not markers:
        print(f"usage: no committed <wave>.ready.dispatched under {wd}", file=sys.stderr)
        return 2
    report = f".ufo/reports/round-{a.round}/{a.id}.md"
    filed = None if a.before_filing else added_at(fleet, report)
    if filed is None and not a.before_filing:
        print(f"usage: no fleet commit adds {report} (use --before-filing)", file=sys.stderr)
        return 2
    ok = 0
    for m in markers:
        wave = pathlib.PurePath(m).name[: -len(".ready.dispatched")]
        res = f"{wd}/{wave}-results.json"
        t = added_at(lane, res)
        body = git(lane, "show", f"HEAD:{m}") if not (lane / m).is_file() else (lane / m).read_text(encoding="utf-8")
        if t is None and " ABANDONED:" in body.split("\n", 1)[0]:
            print(f"ABANDONED {wave} never taken by the dispatcher (marker: {body.split(chr(10), 1)[0][:60]})")
            ok += 1
        elif t is None:
            print(f"UNSETTLED {wave} no committed {wave}-results.json")
        elif filed is not None and t > filed:
            print(f"UNSETTLED {wave} results={t.isoformat()} after report={filed.isoformat()}")
        else:
            print(f"SETTLED {wave} results={t.isoformat()}")
            ok += 1
    print(f"WAVES={len(markers)} SETTLED={ok}")
    return 0 if ok == len(markers) else 1


if __name__ == "__main__":
    sys.exit(main())

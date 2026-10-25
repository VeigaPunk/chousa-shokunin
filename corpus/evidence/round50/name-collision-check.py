#!/usr/bin/env python3
"""name-collision-check — a wave spec's seat names must not repeat a seat name of an earlier round.

Round 50 wave 1 reused 13 round-49 seat names (MineConsider, ExecMirrorCensus, ExecInfStaged, ExecReplayC1,
ExecFormProbe, CritForgeC1, CritForgeC2, ReviewProvince, ReviewQuarMap, CritTheme, ConnSiblings, ConnCrossClaim,
ScoutCoverage); the dispatcher resumed the parked round-49 agents of those names, and each answered with its
round-49 report instead of doing round-50 work (their results name `.ufo/waves/round-49/w1/<name>.md`).

Usage: python3 name-collision-check.py <wave-spec.json> [--lane DIR] [--round N]
`--round` (default: read from the spec's reportDir `.ufo/waves/round-N/...`) is the round to exclude. Prints
`NAME_COLLISION <name> <path>` for every spec item whose name is the basename (without `.md`) of a report file of
another round's wave directory; exit 1 when any, 0 when none, 2 on an unusable spec or lane.
"""
import argparse
import json
import pathlib
import re
import sys

ap = argparse.ArgumentParser()
ap.add_argument("spec")
ap.add_argument("--lane", default=str(pathlib.Path(__file__).resolve().parents[3]))
ap.add_argument("--round", type=int)
a = ap.parse_args()
try:
    spec = json.loads(pathlib.Path(a.spec).read_text(encoding="utf-8"))
    names = [i["name"] for i in spec["items"]]
except (OSError, ValueError, KeyError, TypeError):
    print("ERROR unusable spec", file=sys.stderr)
    sys.exit(2)
m = re.search(r"round-(\d+)", str(spec.get("reportDir", "")))
rnd = a.round if a.round is not None else (int(m.group(1)) if m else None)
waves = pathlib.Path(a.lane) / ".ufo" / "waves"
if rnd is None or not waves.is_dir():
    print("ERROR no round or no waves dir", file=sys.stderr)
    sys.exit(2)
seen: dict[str, str] = {}
for p in sorted(waves.glob("round-*/*/*.md")):
    r = re.match(r"round-(\d+)$", p.parent.parent.name)
    if r and int(r.group(1)) != rnd:
        seen.setdefault(p.stem, str(p.relative_to(a.lane)))
bad = 0
for n in names:
    if n in seen:
        print(f"NAME_COLLISION {n} {seen[n]}")
        bad += 1
print(f"NAME_COLLISIONS={bad} ITEMS={len(names)}")
sys.exit(1 if bad else 0)

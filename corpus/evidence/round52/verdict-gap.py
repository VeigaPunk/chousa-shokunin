#!/usr/bin/env python3
"""verdict-gap — the lane's own axis grade vs the non-author verifier's axis
grade, per round (considerthese/2026-10-26.md, proposal 3; W1
`R52ScoutConsiderthese` prototype, made a lane check in round 52).

For each round N in [--from, --to] it reads the first axis table of the
`## Round N verdict` section of SCORECARD.md and the axis table of
`corpus/lessons/round-N-verifier-spotcheck.md` (rows `| <axis> | <verdict> |`),
takes each cell's direction (the first of improved / unchanged / harmed /
regress; qualifiers such as "narrowly" are dropped) and prints one line per
axis whose two directions differ. A round whose verifier file holds no axis
row in that table shape (round 48 writes its axes as bullets) prints
`R<N> UNPARSED` and is not compared — it is not counted as agreement.

Usage: python3 corpus/evidence/round52/verdict-gap.py [--root LANE] --from N --to M
Prints `VERDICT_GAPS=<gaps> UNPARSED=<rounds>`.
Exit 0 no gap and nothing unparsed · 1 a gap or an unparsed/missing round · 2 usage.
"""
import argparse
import pathlib
import re
import sys

AX = ("operability", "depth", "calibration", "coverage", "freshness", "adjacency")


def dirn(s: str):
    m = re.search(r"improved|unchanged|harmed|regress", s.replace("*", "").lower())
    return m.group(0) if m else None


def table(lines):
    out = {}
    for line in lines:
        m = re.match(r"^\|\s*(%s)\s*\|\s*(.*?)\s*\|" % "|".join(AX), line)
        if m and dirn(m.group(2)):
            out.setdefault(m.group(1), dirn(m.group(2)))
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--root", default=str(pathlib.Path(__file__).resolve().parents[3]))
    ap.add_argument("--from", dest="r0", type=int, required=True)
    ap.add_argument("--to", dest="r1", type=int, required=True)
    a = ap.parse_args()
    root = pathlib.Path(a.root)
    sc_path = root / "SCORECARD.md"
    if not sc_path.is_file() or a.r0 > a.r1:
        print("usage: no SCORECARD.md or empty range", file=sys.stderr)
        return 2
    sc = sc_path.read_text(encoding="utf-8").splitlines()
    gap = unparsed = 0
    for n in range(a.r0, a.r1 + 1):
        st = next((i for i, l in enumerate(sc) if re.match(r"^## Round %d verdict" % n, l)), None)
        vf = root / f"corpus/lessons/round-{n}-verifier-spotcheck.md"
        if st is None or not vf.is_file():
            print(f"R{n} MISSING scorecard={st is not None} verifier={vf.is_file()}")
            unparsed += 1
            continue
        en = next((i for i in range(st + 1, len(sc)) if sc[i].startswith("## ")), len(sc))
        lane, ver = table(sc[st:en]), table(vf.read_text(encoding="utf-8").splitlines())
        if not ver or not lane:
            print(f"R{n} UNPARSED lane_axes={len(lane)} verifier_axes={len(ver)}")
            unparsed += 1
            continue
        for ax in AX:
            if ax in lane and ax in ver and lane[ax] != ver[ax]:
                print(f"R{n} {ax}: lane={lane[ax]} verifier={ver[ax]}")
                gap += 1
        print(f"R{n} axes lane={len(lane)} verifier={len(ver)}")
    print(f"VERDICT_GAPS={gap} UNPARSED={unparsed}")
    return 1 if gap or unparsed else 0


if __name__ == "__main__":
    sys.exit(main())

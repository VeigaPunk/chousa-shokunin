#!/usr/bin/env python3
"""Round-32 C1 receipt census (round-33 D2 repair artifact).

Answers one numeric question with one command: how many committed round-32
C1 receipts bind a given gate digest, and where are they? D2's evidence
standard is that a numeric claim carries its counting command; this file is
that command.

File list: `git -C <lane> ls-files .ufo/waves/round-32 | grep json`, exactly
the command D2 names. `.jsonl` paths (line-delimited manifests, not receipts)
are skipped and counted. Content comes from the committed blob `HEAD:<path>`
through one `git cat-file --batch`, so an uncommitted worktree edit cannot
change a count; a path in the index but absent from HEAD is reported
separately and never silently included.

A C1 receipt is a top-level JSON object whose "label" begins with
APPEND_SERIALIZED (the counter's own printed verdict for C1).

Usage:
  python3 census.py [--lane DIR] [--gate PREFIX]
Exit 0 always (a census, not a check).
"""
import argparse
import json
import os
import subprocess
import sys
from collections import Counter, defaultdict

REL = ".ufo/waves/round-32"
C1_LABEL = "APPEND_SERIALIZED"


def listed_paths(lane):
    """git ls-files .ufo/waves/round-32 | grep json, NUL-safe then decoded."""
    out = subprocess.run(["git", "-C", lane, "ls-files", "-z", REL],
                         check=True, capture_output=True).stdout
    return sorted(p.decode("utf-8", "surrogateescape")
                  for p in out.split(b"\0") if b"json" in p)


def blobs_at_head(lane, paths):
    """{path: bytes|None} via a single cat-file --batch over HEAD:<path>."""
    req = b"".join(("HEAD:" + p + "\n").encode("utf-8", "surrogateescape")
                   for p in paths)
    out = subprocess.run(["git", "-C", lane, "cat-file", "--batch"],
                         input=req, check=True, capture_output=True).stdout
    pos, res = 0, {}
    for p in paths:
        nl = out.find(b"\n", pos)
        if nl < 0:
            res[p] = None
            continue
        parts = out[pos:nl].decode("utf-8", "surrogateescape").split(" ")
        pos = nl + 1
        if len(parts) == 3 and parts[1] == "blob":
            size = int(parts[2])
            res[p] = out[pos:pos + size]
            pos += size + 1          # payload plus its trailing newline
        else:                        # "<obj> missing" or a non-blob object
            res[p] = None
            pos += 1 if len(parts) != 3 else int(parts[2]) + 1
    return res


def seat_of(path):
    d = os.path.dirname(path[len(REL) + 1:])
    return d if d else "."


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--lane", default=os.environ.get("LANE", "."))
    ap.add_argument("--gate", default="10f2fe12",
                    help="gate_sha256 prefix to break down (default 10f2fe12)")
    a = ap.parse_args()
    lane = a.lane

    paths = listed_paths(lane)
    jsonl = [p for p in paths if p.endswith(".jsonl")]
    candidate = [p for p in paths if p.endswith(".json")]
    blobs = blobs_at_head(lane, candidate)

    parsed = uncommitted = badjson = 0
    receipts = []
    for p in candidate:
        raw = blobs.get(p)
        origin = "HEAD"
        if raw is None:
            uncommitted += 1
            origin = "worktree-uncommitted"
            try:
                raw = open(os.path.join(lane, p), "rb").read()
            except OSError:
                badjson += 1
                continue
        try:
            rec = json.loads(raw)
        except ValueError:
            badjson += 1
            continue
        if not isinstance(rec, dict):
            badjson += 1
            continue
        parsed += 1
        label = rec.get("label")
        if not (isinstance(label, str) and label.startswith(C1_LABEL)):
            continue
        receipts.append(dict(path=p, origin=origin, seat=seat_of(p),
                             gate=str(rec.get("gate_sha256") or "(none)")[:8],
                             counter=str(rec.get("counter_sha256") or "(none)")[:8],
                             label=label, utc=str(rec.get("utc") or "?"),
                             total=rec.get("total"), matched=rec.get("matched"),
                             seed=rec.get("seed")))

    target = [r for r in receipts if r["gate"] == a.gate]
    print("census lane: %s" % lane)
    print("json paths listed by `git ls-files %s | grep json`: %d "
          "(%d .json, %d .jsonl skipped)"
          % (REL, len(paths), len(candidate), len(jsonl)))
    print("json objects parsed: %d | non-object/undecodable: %d | index paths "
          "absent from HEAD: %d" % (parsed, badjson, uncommitted))
    print("C1 receipts anywhere in round-32 (label ^%s): %d"
          % (C1_LABEL, len(receipts)))
    print("C1 receipts on gate %s: %d" % (a.gate, len(target)))
    print()

    print("target gate %s by (counter, seat), utc-sorted:" % a.gate)
    grp = defaultdict(list)
    for r in target:
        grp[(r["counter"], r["seat"])].append(r)
    for key in sorted(grp, key=lambda k: (-len(grp[k]), k)):
        rows = sorted(grp[key], key=lambda r: (r["utc"], r["path"]))
        scores = sorted({"%s/%s" % (r["matched"], r["total"]) for r in rows})
        print("  counter=%s seat=%-22s n=%2d scores=%s"
              % (key[0], key[1], len(rows), ",".join(scores)))
        for r in rows:
            print("      %s  seed=%s utc=%s %s"
                  % (r["path"], r["seed"], r["utc"], r["label"]))
    print()

    print("target gate %s in utc order (cumulative count):" % a.gate)
    for i, r in enumerate(sorted(target, key=lambda r: (r["utc"], r["path"])), 1):
        print("  %2d  %-21s %s" % (i, r["utc"], r["path"]))
    print()

    print("all gates seen among C1 receipts, count:")
    for g, n in sorted(Counter(r["gate"] for r in receipts).items(),
                       key=lambda kv: (-kv[1], kv[0])):
        print("  %s  %3d%s" % (g, n, "   <- target" if g == a.gate else ""))
    return 0


if __name__ == "__main__":
    sys.exit(main())

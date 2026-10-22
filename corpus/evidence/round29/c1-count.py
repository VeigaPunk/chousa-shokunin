#!/usr/bin/env python3
"""Round-29 C1 counter (frozen before data; see corpus/evidence/round29/claims.md).

Usage (cwd: chousa-shokunin lane root):
    python3 corpus/evidence/round29/c1-count.py [--seed N] [--receipt PATH] -- CMD...

CMD is the candidate verifier, for example `python3 tools/quote-reopen.py verify`.
The counter appends `--items <tmp>/items.tsv` to CMD and runs it from the lane root.
The candidate never sees labels.tsv through the counter: the counter writes only
the items (fresh random ids, shuffled order) into a private temporary directory.

Predicate (same sentence as claims.md): C1 holds iff this counter prints
QUOTE_REOPEN_MATCH=82/82, i.e. every one of the 40 frozen fixture items and the
42 run-time variants gets a verdict equal to its label.

Run-time variants, per frozen VERBATIM item (14 items, 3 variants each):
  subspan    - a random whitespace-token-aligned contiguous sub-span of 5..n-1
               tokens of the quote, same source id                -> VERBATIM
  transpose  - the quote with two adjacent distinct tokens swapped  -> ABSENT
  crossattr  - the full quote attributed to the next VERBATIM source id in
               sorted rotation (checked absent before freeze)       -> ABSENT
Exit: 0 iff matches == total == 82; 1 otherwise; 2 on usage/fixture error.
"""
import argparse
import hashlib
import json
import os
import random
import secrets
import subprocess
import sys
import tempfile
import time

LANE = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
FIXTURE = os.path.join(LANE, "corpus", "fixtures", "quote-reopen-r29")
FROZEN_TOTAL = 82
LABELS = {"VERBATIM", "ABSENT", "TOO_LONG", "NO_SOURCE"}


def load_tsv(path, header):
    with open(path, encoding="utf-8") as f:
        lines = f.read().split("\n")
    if lines[0] != header:
        raise ValueError(f"{path}: header {lines[0]!r} != {header!r}")
    return [ln.split("\t") for ln in lines[1:] if ln]


def build(seed):
    items = load_tsv(os.path.join(FIXTURE, "items.tsv"), "id\tsource_id\tquote")
    labels = {r[0]: (r[1], r[2]) for r in load_tsv(os.path.join(FIXTURE, "labels.tsv"), "id\tlabel\tclass")}
    if len(items) != 40 or set(labels) != {r[0] for r in items}:
        raise ValueError("fixture must hold exactly 40 items with one label each")
    rng = random.Random(seed)
    cases = []
    for fid, sid, quote in items:
        lab, cls = labels[fid]
        if lab not in LABELS:
            raise ValueError(f"bad label {lab}")
        cases.append({"origin": fid, "kind": "frozen", "class": cls, "source_id": sid, "quote": quote, "label": lab})
    vsrc = sorted({sid for fid, sid, q in items if labels[fid][0] == "VERBATIM"})
    rot = {s: vsrc[(i + 1) % len(vsrc)] for i, s in enumerate(vsrc)}
    for fid, sid, quote in items:
        if labels[fid][0] != "VERBATIM":
            continue
        toks = quote.split()
        n = rng.randint(5, len(toks) - 1)
        start = rng.randint(0, len(toks) - n)
        cases.append({"origin": fid, "kind": "subspan", "class": "runtime-subspan", "source_id": sid,
                      "quote": " ".join(toks[start:start + n]), "label": "VERBATIM"})
        pairs = [i for i in range(len(toks) - 1) if toks[i] != toks[i + 1]]
        i = rng.choice(pairs)
        sw = toks[:i] + [toks[i + 1], toks[i]] + toks[i + 2:]
        cases.append({"origin": fid, "kind": "transpose", "class": "runtime-transpose", "source_id": sid,
                      "quote": " ".join(sw), "label": "ABSENT"})
        cases.append({"origin": fid, "kind": "crossattr", "class": "runtime-crossattr", "source_id": rot[sid],
                      "quote": quote, "label": "ABSENT"})
    used = set()
    for c in cases:
        while True:
            rid = secrets.token_hex(6)
            if rid not in used:
                used.add(rid)
                c["id"] = rid
                break
    random.Random(secrets.randbits(64)).shuffle(cases)
    return cases


def main():
    argv = sys.argv[1:]
    if "--" not in argv:
        print("usage: c1-count.py [--seed N] [--receipt PATH] -- CMD...", file=sys.stderr)
        return 2
    k = argv.index("--")
    ap = argparse.ArgumentParser()
    ap.add_argument("--seed", type=int, default=None)
    ap.add_argument("--receipt", default=None)
    ap.add_argument("--timeout", type=int, default=900)
    opts = ap.parse_args(argv[:k])
    cmd = argv[k + 1:]
    if not cmd:
        print("usage: empty CMD", file=sys.stderr)
        return 2
    seed = opts.seed if opts.seed is not None else secrets.randbits(32)
    try:
        cases = build(seed)
    except (OSError, ValueError) as e:
        print(f"fixture error: {e}", file=sys.stderr)
        return 2
    with tempfile.TemporaryDirectory(prefix="c1count-") as td:
        ip = os.path.join(td, "items.tsv")
        with open(ip, "w", encoding="utf-8") as f:
            f.write("id\tsource_id\tquote\n")
            for c in cases:
                f.write(f"{c['id']}\t{c['source_id']}\t{c['quote']}\n")
        t0 = time.time()
        try:
            p = subprocess.run(cmd + ["--items", ip], cwd=LANE, capture_output=True, text=True, timeout=opts.timeout)
            rc, out, err = p.returncode, p.stdout, p.stderr
        except FileNotFoundError as e:
            rc, out, err = 127, "", str(e)
        except subprocess.TimeoutExpired as e:
            rc, out, err = 124, (e.stdout or b"").decode("utf-8", "replace") if isinstance(e.stdout, bytes) else (e.stdout or ""), "timeout"
        wall = round(time.time() - t0, 2)
    got = {}
    for ln in out.splitlines():
        parts = ln.split("\t")
        if len(parts) >= 3 and parts[0] == "QUOTE_REOPEN" and parts[1] not in got:
            got[parts[1]] = parts[2]
    per = {}
    n = 0
    for c in cases:
        c["verdict"] = got.get(c["id"], "<missing>")
        c["match"] = c["verdict"] == c["label"]
        n += c["match"]
        a, b = per.get(c["class"], (0, 0))
        per[c["class"]] = (a + c["match"], b + 1)
    t = len(cases)
    for cls in sorted(per):
        print(f"class {cls} {per[cls][0]}/{per[cls][1]}")
    print(f"seed={seed} tool_exit={rc} wall_s={wall}")
    print(f"QUOTE_REOPEN_MATCH={n}/{t}")
    if opts.receipt:
        rec = {"schema": "chousa-r29-c1-receipt/v1", "counter_sha256": hashlib.sha256(open(__file__, "rb").read()).hexdigest(),
               "cmd": cmd, "seed": seed, "tool_exit": rc, "wall_s": wall, "match": n, "total": t,
               "predicate_holds": n == t == FROZEN_TOTAL, "stderr_tail": err[-2000:],
               "at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "cases": cases}
        with open(opts.receipt, "w", encoding="utf-8") as f:
            json.dump(rec, f, indent=1, ensure_ascii=False)
            f.write("\n")
    return 0 if n == t == FROZEN_TOTAL else 1


if __name__ == "__main__":
    sys.exit(main())

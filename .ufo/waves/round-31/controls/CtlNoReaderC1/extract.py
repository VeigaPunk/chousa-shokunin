#!/usr/bin/env python3
"""Offline feature extraction for the no-reader C1 control.

Imports the frozen counter READ-ONLY (never edits it), generates fixtures for
many seeds, and records, per claim, every feature visible in claims.jsonl
plus the hidden truth (for offline rule fitting only; the control gate never
sees truth).
"""
import importlib.util
import json
import os
import re
import shutil
import sys
import tempfile

COUNTER = "/fast/scratch/hyaku/chousa-r31/CtlNoReaderC1/c1-count-v2-snapshot.py"

spec = importlib.util.spec_from_file_location("c1counter", COUNTER)
c1 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(c1)

VALID_SINGLE = re.compile(r"^[1-9][0-9]*$")
VALID_RANGE = re.compile(r"^([1-9][0-9]*)-([1-9][0-9]*)$")


def parse_line_field(v):
    if v is None:
        return {"fmt": "absent", "n": None, "m": None, "width": None}
    if not isinstance(v, str):
        return {"fmt": "invalid", "n": None, "m": None, "width": None}
    if VALID_SINGLE.match(v):
        n = int(v)
        return {"fmt": "single", "n": n, "m": n, "width": 1}
    g = VALID_RANGE.match(v)
    if g:
        n, m = int(g.group(1)), int(g.group(2))
        if m > n:
            return {"fmt": "range", "n": n, "m": m, "width": m - n + 1}
    return {"fmt": "invalid", "n": None, "m": None, "width": None}


def features(raw_line, rec, truth):
    keys = list(json.loads(raw_line, object_pairs_hook=lambda p: p))
    # object_pairs_hook gives list of pairs preserving order
    keyorder = [k for k, _ in keys]
    lf = parse_line_field(rec.get("line"))
    span = rec.get("span", "")
    return {
        "seed": truth["seed"],
        "id": rec["id"],
        "cls": truth["cls"],
        "truth": truth["truth"],
        "line_present": "line" in rec,
        "line_raw": rec.get("line"),
        "fmt": lf["fmt"],
        "n": lf["n"],
        "m": lf["m"],
        "width": lf["width"],
        "span_newline": "\n" in span,
        "span_words": len(span.split(" ")),
        "span_len": len(span),
        "span_trailing_space": span != span.rstrip(),
        "span_lead_space": span != span.lstrip(),
        "claim_eq_id": rec.get("claim") == "fixture claim " + rec["id"],
        "expect": rec.get("expect"),
        "nkeys": len(rec),
        "keyorder": ",".join(keyorder),
        "id_hex": rec["id"],
        "src_hex": rec["source"].split("/")[-1].split(".")[0],
        "rec_keys": sorted(rec.keys()),
    }


def main():
    nseeds = int(sys.argv[1]) if len(sys.argv) > 1 else 60
    out = sys.argv[2] if len(sys.argv) > 2 else "/fast/scratch/hyaku/chousa-r31/CtlNoReaderC1/features.jsonl"
    base = "/fast/scratch/hyaku/chousa-r31/CtlNoReaderC1/tmp"
    os.makedirs(base, exist_ok=True)
    rows = []
    for seed in range(1000, 1000 + nseeds):
        root = tempfile.mkdtemp(prefix="fx-", dir=base)
        try:
            claims, truth = c1.generate(root, seed)
            lines = [l for l in open(claims, encoding="utf-8").read().splitlines() if l]
            for raw in lines:
                rec = json.loads(raw)
                cls, t = truth[rec["id"]]
                f = features(raw, rec, {"cls": cls, "truth": t, "seed": seed})
                rows.append(f)
        finally:
            shutil.rmtree(root, ignore_errors=True)
    with open(out, "w", encoding="utf-8") as f:
        for r in rows:
            f.write(json.dumps(r, sort_keys=True) + "\n")
    print("wrote %d rows from %d seeds -> %s" % (len(rows), nseeds, out))


if __name__ == "__main__":
    main()

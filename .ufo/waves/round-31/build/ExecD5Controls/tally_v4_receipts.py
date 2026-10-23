#!/usr/bin/env python3
"""Tally round-30 control receipts carrying the v4 counter hashes.

C1 v4 counter: 5b312d84365924779ba8e6fe447cad3467f59c11848083d0967528c7a5e9d6e6
C2 v4 counter: 0a59e3736fed8ef4cf7b00a75955eccfd0336c8a0ca84bee23402408b727f88f
Matched by prefix per the proceeding ('C1 5b312d84...', 'C2 0a59e373...').
Score = receipt 'n' over 't'; predicate_holds as recorded.
"""
import json
import os
import sys

ROOT = "/home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-30/controls"
C1_PREFIX = "5b312d84"
C2_PREFIX = "0a59e373"

rows = []
for dirpath, _dirnames, filenames in os.walk(ROOT):
    for fn in sorted(filenames):
        if not fn.endswith(".json"):
            continue
        p = os.path.join(dirpath, fn)
        rel = os.path.relpath(p, ROOT)
        try:
            with open(p, "r", encoding="utf-8") as f:
                d = json.load(f)
        except Exception as exc:  # noqa: BLE001
            print(f"SKIP unreadable {rel}: {exc}")
            continue
        if not isinstance(d, dict):
            print(f"SKIP not-object {rel}")
            continue
        ch = d.get("counter_sha256", "") or ""
        kind = None
        if ch.startswith(C1_PREFIX):
            kind = "C1"
        elif ch.startswith(C2_PREFIX):
            kind = "C2"
        if kind is None:
            continue
        rows.append({
            "kind": kind,
            "rel": rel,
            "n": d.get("n"),
            "t": d.get("t"),
            "frozen_total": d.get("frozen_total"),
            "predicate_holds": d.get("predicate_holds"),
            "label": d.get("label"),
            "tool": d.get("tool"),
            "net_connect_events": d.get("net_connect_events"),
            "seed": d.get("seed"),
            "utc": d.get("utc"),
            "counter_sha256": ch,
        })

rows.sort(key=lambda r: (r["kind"], -(r["n"] or -1), r["rel"]))

print(f"Receipts carrying v4 counter hashes: {len(rows)}")
print("=" * 100)
for r in rows:
    print(
        f"{r['kind']} n={r['n']}/{r['t']} holds={r['predicate_holds']} "
        f"conn={r['net_connect_events']} tool={r['tool']} {r['rel']} "
        f"seed={r['seed']} utc={r['utc']}"
    )

print("=" * 100)
for kind in ("C1", "C2"):
    ks = [r for r in rows if r["kind"] == kind]
    if not ks:
        print(f"{kind}: no v4 receipts")
        continue
    best = max(ks, key=lambda r: r["n"])
    print(f"{kind} v4 max overall: n={best['n']}/{best['t']} "
          f"holds={best['predicate_holds']} {best['rel']} tool={best['tool']}")
    # no-reader: CtlNoReader dir or zero connect events
    nr = [r for r in ks
          if r["rel"].startswith("CtlNoReader/") or r["net_connect_events"] == 0]
    if nr:
        best_nr = max(nr, key=lambda r: r["n"])
        print(f"{kind} v4 max no-reader: n={best_nr['n']}/{best_nr['t']} "
              f"holds={best_nr['predicate_holds']} {best_nr['rel']} "
              f"tool={best_nr['tool']}")
    else:
        print(f"{kind} v4 max no-reader: none (no CtlNoReader/zero-connect receipt)")
    # per-control (unique tool) table
    print(f"-- {kind} v4 per-control summary --")
    by_tool = {}
    for r in ks:
        by_tool.setdefault(r["tool"], []).append(r)
    for tool, runs in sorted(by_tool.items()):
        scores = [r["n"] for r in runs]
        holds = [r["predicate_holds"] for r in runs]
        print(f"  {tool}: runs={len(runs)} scores={scores} holds={holds} "
              f"max={max(scores)}")

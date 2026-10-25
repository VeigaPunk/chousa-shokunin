#!/usr/bin/env python3
"""Round-25 recount of the hardening-r10 limit ledger (chousa-shokunin).

Usage, from the lane root: python3 corpus/evidence/round25-ledger-recount.py

Counts the 71 §3 rows of corpus/knowledge/hardening-r10.md by their recorded
disposition, then applies the row closures the addenda record (E1 = r12 §6:
rows 9, 10, 56, 70; E2 = r13: row 8). E3 (r14) and E4 (r15) closed queue items
that occupy no §3 row; the round-16..23 addenda record no row or round-11
queue delta. Derived by the round-25 reviewer seat ReviewLedgerTotals; the
closure sets are read from the addenda text, not parsed. queue_true adds back
the one item E3 over-removed (E4 text: "queue-true was 26 at E3 (25 committed)").
"""
import collections
import pathlib
import sys

ROW_CLOSURES = ((9, 10, 56, 70), (8,))           # E1 (r12 §6), E2 (r13)
QUEUE_EVENTS = (("E1", -4), ("E2", -1), ("E3", 0), ("E4", -1))

text = pathlib.Path("corpus/knowledge/hardening-r10.md").read_text(encoding="utf-8")
rows = {}
for line in text.splitlines():
    if not line.startswith("|"):
        continue
    cells = line.split("|")
    if len(cells) > 4 and cells[1].strip().isdigit() and 1 <= int(cells[1]) <= 71:
        rows[int(cells[1])] = cells[4].strip().replace("**", "").split("(")[0].strip()
if len(rows) != 71:
    sys.exit("expected 71 ledger rows, parsed %d" % len(rows))
for closure in ROW_CLOSURES:
    rows.update(dict.fromkeys(closure, "closed"))
count = collections.Counter(rows.values())
queue = 30 + sum(delta for _, delta in QUEUE_EVENTS)
print("rows=%d" % len(rows), *("%s=%d" % (k, count[k]) for k in
      ("by-design", "carried", "closed", "finding", "operator")),
      "sum=%d" % sum(count.values()), "queue_committed=%d" % queue,
      "queue_true=%d" % (queue + 1))

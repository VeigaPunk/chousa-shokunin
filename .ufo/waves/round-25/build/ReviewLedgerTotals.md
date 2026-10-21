Axes: row-total correctness; queue accounting; criterion-9 restatement freshness.

## Findings

- **High — the published row tuple is impossible and double-counts a closure.** `corpus/knowledge/hardening-r10.md:549-559` reports 38/21/10/0/3, which sums to 72, not 71. Counting §3 rows 1–71 gives 38/25/3/1/4; E1 moves rows 9, 10, 56, 70 to closed (38/23/7/0/3); E2 moves row 8 to closed (38/22/8/0/3). E3's bind residual and the r15 dead-arm are expressly non-row queue items (`:478-482`, `:551-559`). The later closure recheck explicitly retains row 9 as `closed(r12, partial)` (`:575-578`), so the r15 `9→10` closed-row increment counts it twice. Row-true final totals are **38/22/8/0/3**.
- **Medium — queue 24 is the committed event arithmetic, but not reconciled to the ledger's own correction.** The addenda's committed transitions yield 30→26→25→25→24 (`:453-455`, `:484-490`, `:506-518`, `:549-559`). However `:558-559` says queue-true was 26 at E3 (25 committed); subtracting only the r15 dead-arm would leave 25, not 24. Thus the tuple is refuted; 24 should not be called independently verified until the missing queue item is reconciled. Row-true open dispositions alone are 22 carried + 3 operator = 25.
- **Medium — the round-25 stale-restatement counter trusts the disputed line.** `corpus/evidence/round25-measure.sh:63-75` takes `led[-1]` and the final queue-arrow target as truth; it never parses rows 1–71 or checks that totals equal 71. It can therefore report stale SKILL numbers relative to an invalid owner tuple rather than the counted ledger state.

## SKILL.md restatements and criterion-9 replacement drafts

1. `SKILL.md:381-384` has r12 counts (38/23/7/0/3, queue 26) and repeats the tuple with a contradictory 27-item queue. Replace with: “Disposition totals and the round-11 queue are owned by `corpus/knowledge/hardening-r10.md` (Round-15 addendum and Independent closure recheck). Re-derive rows 1–71 and the queue with: `python3 -c 'import pathlib,collections as C; s=pathlib.Path("/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/knowledge/hardening-r10.md").read_text(); r={int(x[1]):x[4].strip().replace("**","").split("(")[0].strip() for l in s.splitlines() if l.startswith("|") for x in [l.split("|")] if x[1].strip().isdigit() and 1<=int(x[1])<=71}; assert len(r)==71; [r.update(dict.fromkeys(t,"closed")) for t in ((9,10,56,70),(8,))]; c=C.Counter(r.values()); print("rows=71",*[f"{k}={c[k]}" for k in ("by-design","carried","closed","finding","operator")],"queue="+str(30-4-1+0-1))'`.”
2. `SKILL.md:435-439` has stale totals and says row 56's A-r9 C3 finding remains open. Replace with: “The A-r9.md:50 fixture-correction finding (ledger row 56) was closed in the Round-12 addendum; the independent recheck remains partial, and the pointer/span detection class remains named non-coverage. Current dispositions and queue are owned by `corpus/knowledge/hardening-r10.md` (Round-15 addendum and Independent closure recheck). Re-derive rows 1–71 and the queue with: `python3 -c 'import pathlib,collections as C; s=pathlib.Path("/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/knowledge/hardening-r10.md").read_text(); r={int(x[1]):x[4].strip().replace("**","").split("(")[0].strip() for l in s.splitlines() if l.startswith("|") for x in [l.split("|")] if x[1].strip().isdigit() and 1<=int(x[1])<=71}; assert len(r)==71; [r.update(dict.fromkeys(t,"closed")) for t in ((9,10,56,70),(8,))]; c=C.Counter(r.values()); print("rows=71",*[f"{k}={c[k]}" for k in ("by-design","carried","closed","finding","operator")],"queue="+str(30-4-1+0-1))'`.”

## Reproducible recount

Command (Python 3; reads §3 row data, applies E1/E2 row closures, and applies the separately described queue events: E1 −4, E2 −1, E3 net 0, E4 −1):

```sh
python3 -c 'import pathlib,collections as C; s=pathlib.Path("/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/knowledge/hardening-r10.md").read_text(); r={int(x[1]):x[4].strip().replace("**","").split("(")[0].strip() for l in s.splitlines() if l.startswith("|") for x in [l.split("|")] if x[1].strip().isdigit() and 1<=int(x[1])<=71}; assert len(r)==71; [r.update(dict.fromkeys(t,"closed")) for t in ((9,10,56,70),(8,))]; c=C.Counter(r.values()); print("rows=71",*[f"{k}={c[k]}" for k in ("by-design","carried","closed","finding","operator")],"queue="+str(30-4-1+0-1))'
```

Output:

```text
rows=71 by-design=38 carried=22 closed=8 finding=0 operator=3 queue=24
```

## Residual risk and verification gaps

- Queue 24 remains conditional on the committed sequence; `hardening-r10.md:558-559` gives a conflicting queue-true count. The published row tuple is not usable as a source of truth until corrected.
- LSP was unavailable: reading `xd://lsp` returned `No such tool`; no semantic reference/definition/diagnostics requests were possible. Reviewed the relevant Markdown lines directly. No tests/builds run; the assigned Python recount ran above.
- Installs: none.

VERDICT: Refute the published row totals; counted rows are 38/22/8/0/3. Queue 24 follows committed event arithmetic but is not reconciled to the stated queue-true count.
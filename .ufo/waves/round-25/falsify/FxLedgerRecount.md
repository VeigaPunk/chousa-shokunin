# FxLedgerRecount — round 25 falsify

## Checkpoint
- Read the round-25 lesson first. The 0fc037e checkpoint omitted `tools/research-gate.sh`; d8c8cff corrected the gate but still omitted `corpus/evidence/README.md`. Those packaging failures are recorded at `corpus/lessons/round-25.md:109-132`.
- Used a private clone at observed full-pin HEAD `e93ac711f885a10d44fdd80a1734997419595b5a`; no clone files were edited. No installs.

## Findings (severity order)
- **No active recount defect.** Raw parse: `parsed=71 contiguous=True raw={'by-design': 38, 'carried': 25, 'closed': 3, 'finding': 1, 'operator': 4}`; agrees with `corpus/knowledge/hardening-r10.md:305-306`. E1 applies rows 9, 10, 56, 70 (`:413-451`); their original statuses are visible at `:204-205,281,300`. E2 applies row 8 (`:472-482`; original status `:203`). The resulting 38/22/8/0/3 sums to 71.
- **Historical double-count, corrected by the R25 erratum.** E4's old 38/21/10/0/3 totals 72 because row 9 was already closed by E1; R25 identifies this at `hardening-r10.md:682-687` and records the corrected row-true tuple. E3's prior phantom bind-item-as-row count is also superseded (`:555-559`, `:561`).
- **No missing §3 / round-11 queue event after r15.** E5–E12 explicitly move no row or round-11 queue item (`hardening-r10.md:612-669`); r24 closes a round-20 debt outside §3 and that queue (`:671-672`). R16 has a separate round-17 queue (`verification-r16.md:9,26-38`); R19 closes a round-16 named debt, not a §3.9 item (`hardening-r10.md:635-638`).
- **Queue arithmetic and visible pointer:** base 30 (`hardening-r10.md:320-322`); E1 −4, E2 −1, E3 net 0, E4 −1 (`:453-455,484-486,506-510,549-559`) gives committed 24. E4 states true=26 vs committed=25 at E3; after its −1 closure true=25 (`:559`). E2/E3 say same-device binds remain open (`:478-482,502-504`), explaining the one-item committed undercount. `SKILL.md:434-443` points to the owning ledger and rederive command; the target erratum keeps both 24 and 25 visible (`hardening-r10.md:688-692`), so the pointer does not hide the dispute.

## Recount and residual assumptions
- Assigned run in the clone: `python3 corpus/evidence/round25-ledger-recount.py` → `rows=71 by-design=38 carried=22 closed=8 finding=0 operator=3 sum=71 queue_committed=24 queue_true=25` (matches committed `corpus/evidence/round25-ledger-recount.log:1`).
- Hardcoded, not source-parsed: row closures E1/E2 (`round25-ledger-recount.py:18`); queue deltas E1–E4 (`:19`); initial queue 30 (`:34`); queue-true `+1` (`:38`). The script explicitly says it does not parse closure prose (`:6-12`).
- Parser assumes the lane-root cwd, a pipe table with row ID in `cells[1]` and disposition in `cells[4]`, IDs 1–71, and the listed category spellings (`:21-30`). It strips parenthetical qualifiers, so the category total does not preserve row 9's `partial` qualification. It emits only post-closure counts. The current file has one numeric row table in §3 (`:194-301`). The docstring only names r16–r23; r24's exclusion is recorded in the erratum, not the script (`:9`, `hardening-r10.md:671-672`).

## Verification gaps
- `xd://lsp` is not mounted (tool response: “No such tool”); no LSP status/references/definition/diagnostics were available. Literal search only located table rows/references; it is not semantic proof.
- No gate/selftest/full-suite run was assigned or performed; checks here were the recount, raw-table parse, and source-text comparisons above.

VERDICT: Corrected tuple and queue values reproduce; the E4 row-9 double-count is historical and explicitly corrected, with no later round-11 queue delta omitted.
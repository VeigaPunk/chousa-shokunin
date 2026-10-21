# FxLedgerR23 — Round-23 history attack

## Pin / packaging
- Used private clone at base `0fc037e6b07f3820ead8c9207a8034ac854197a1`, then fetched and switched to full pin `e93ac711f885a10d44fdd80a1734997419595b5a`.
- Both packaging failures remain material: `corpus/lessons/round-25.md:111-133` records that 0fc carried old gate `752e4e38…` (136 cases), and d8 fixed the gate but retained the stale evidence index. Measured gate SHA-256: 0fc=`752e4e38…`, d8=e93=`63a39282…`; evidence README blob at 0fc=d8=`1701914b…`, e93=`9de288e1…`. Findings below use e93, not either incomplete pin.

## R23 transition and test attribution
- R23 E12 is correctly mapped: original LOG says gate `dfb798b4…` → `b5d0f93d…`, 133 cases and new case 129 (`LOG.md:808-810`; `SCORECARD.md:1196-1205`). In the private clone, `git show a27128e:tools/research-gate.sh | sha256sum` gave `dfb798b4e2c59f4925f12480a06c603a4eae55a706f6601c31590e5970bda22c`; `git show f818652:tools/research-gate.sh | sha256sum` gave `b5d0f93d38f3c52ee3a4bef38ec524a2bb64e280c9c518f331fa39d082849799`.
- Attribution confirmed: R23 receipt has `case 129 chain-fence-anchor exit=1` and PASS 133 (`fanchor-r23-…-selftest.log:129,134`); note names that case (`fenced-anchor-r23.md:3-5`). R22 E11 correctly maps to cases 129–132 at landing, renumbered 130–133 in R23 (`hardening-r10.md:660-662`; R22/R23 selftest receipts). No E5–E12 off-by-one found.

## Ledger vs named-debt closure
- No original §3 row / §3.9 round-11 queue item moved in R23: row 22 remains `carried (contextual)` for archive heading coverage (`hardening-r10.md:222`), and row 22 remains listed in the §3.9 round-11 queue (`:320-323`). R23 instead closes the separate Round-20 named-debt candidate: SCORECARD still lists it as debt after R22 (`SCORECARD.md:1164`), then says the fenced-heading class is closed at R23 (`:1177-1183,1209`).
- Thus E12's scoped no-ledger-delta claim is supported, but `No row/queue delta` (`hardening-r10.md:669`) is ambiguous: it should say “no §3 row or §3.9 round-11 queue item moved.” A Round-20 named-debt queue item did close. This is the same distinction E8 makes explicitly for R19: no §3/§3.9 move, while closing the separate R16 named debt (`hardening-r10.md:635-638`; `verification-r16.md:33`).

## Append-only / mapping finding
- Path history has no R21–R24 hardening edit (`git log --follow -- corpus/knowledge/hardening-r10.md`: R25, R20, R15, then earlier). `git diff --unified=2 edcffba 0fc037e -- corpus/knowledge/hardening-r10.md` reports one historical replacement (`${GSHA}` → `6b17e50c…`) and additions at EOF; pre-existing prose otherwise stands. The R23 addendum is at lines 664-669; full e93 has the same hardening blob as 0fc (`9a78da11…`). No gate/selftest rerun was assigned or performed.
- Mapping correction: E12 itself belongs to R23, but the next unheaded paragraph at `hardening-r10.md:671-672` is an R24 gate transition and closure, nested under `### Round-23 addendum`. R24's LOG, SCORECARD, and `json-delimiter-r24.md` independently identify `b5d0f93d…` → `752e4e38…`, cases 134–136, and a Round-20 named-debt closure (`LOG.md:826`; `SCORECARD.md:1234-1258`; `json-delimiter-r24.md:3-5,50-55`). It should be separately labeled Round 24 (E13 if continuing the E-number sequence); do not attribute it to E12.

VERDICT: R23 transition, case 129, and scoped ledger non-delta are supported; qualify the queue wording and separate the nested R24 entry. Installs: none.
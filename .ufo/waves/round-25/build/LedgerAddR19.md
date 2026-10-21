# LedgerAddR19 — draft `### Round-19 addendum` for corpus/knowledge/hardening-r10.md
Seat ChousaR25Recovery.LedgerAddR19-3 · read-only (no WRITER flag; no clone taken) · base observed b820e4e40ce52deedf53b191140cd7b08ddda929 · axes: calibration, evidence density, style fidelity.

## Draft — append after the "Independent closure recheck" section (current revision :568–600)

```markdown
### Round-19 addendum (2026-10-19, append-only)

E8 — the sweeps symlink-escape named debt closes (queue-item closure, not
a row closure: no §3 row names symlinks and no §3.9 round-11 queue item
moves — the item entered the named-debt queue from round 16, seat 20, and
rode the SCORECARD Planned lists through rounds 17–19). **Every sweeps
glob match is now canonicalized (`readlink -f`) and checked against
`in_root` for both `root_r` and `lane_r`; any match resolving outside both
roots refuses the whole sweep** (`SWEEP_LOCATION_OUT_OF_CORPUS` crit
naming the escaping match; `observed=refused`, the sweep line reports
`hits=- at=-`; `verify_sweeps` per-match check, `tools/research-gate.sh`
~:1970-1995 at this revision — the pre-fix behavior this closes is the
`SWEEP_CLAIM_FALSE` false-hit an outside symlink produced). Both escape
shapes closed: leaf symlink (`dir/*.md`) and directory symlink
(`dir/*/*.md`); the in-root control pins that a symlink resolving inside
either root keeps normal hit semantics (not boundary-refused). Carried
INSIDE the closure, not new rows: the check is post-expansion (glob
traversal touches names only), a check-to-use TOCTOU remains, and
`--root /` stays vacuous by declaration (`knowledge/sweep-symlink-r19.md`).

Selftest cases 120–122 (`sweeps-symlink-escape`, `sweeps-symlink-dir`,
`sweeps-inroot-symlink`); `PASS (122 cases, 0 skipped)`, cases 1–119
byte-identical vs the r18 receipt. Receipts
`evidence/symlink-r19-20261019T174500Z-{demo,selftest,battery,drift}.log`
(masked battery ALL IDENTICAL; drift `none` vs the r12 baseline — no
re-pin). Gate `6e694881…` → `9f163807…`.

Counts at this revision: **no §3 row moved and none is added** (rows 1–71
stand as E4 left them); the round-11 audit queue (§3.9) is untouched — its
enumeration (8–10, 11, 13, 14, 22, 24, 25, 26, 29, 32, 33, 38–45, 47, 49,
53, 56, 57, 68–71) names no symlink class. The closed queue text, for the
record (verification-r16.md named-debt table, seat 20): "Sweeps guard:
wildcard can cross a symlink inside root to reach outside dir … the
sweep's `readlink -f` canonicalizes the BASE, not each glob match". That
row reads closed(r19) on next touch or by citing this addendum;
verification-r16.md still saying "named debt — … queue for round 17" is a
stale restatement this addendum closes. Closed-side evidence: SCORECARD
§Planned — round 20 no longer names the item.

This supersedes nothing in this file; §6 and E2–E4 stand. Revision trail:
`00bf8418…` (r14 E3) → `1dd34d97…` (r15 E4; the revision this addendum
appends to — rounds 16–19 landed no change to this file; first later
touch is round-20's `edcffba`). Sites naming `1dd34d97…` carry the r15
revision; update on next touch or cite this addendum.
```

## Evidence (all read-only, live lane + `git show`)
- Gate sha: `git show 5499cef:tools/research-gate.sh | sha256sum` → `6e69488160199cc1704bd1d17b7523cd39022016ad123ecf43575467b266de0c` (identical at 71b0b5f) → `git show 3eaa0cd:…` → `9f1638076915d9bf6ffb5816e342204081cc1ab07bc803fc7cb402147954c2ba` (unchanged at 9b04830, 2bb556b). Matches LOG.md:697 and sweep-symlink-r19.md:3.
- Selftest 119→122: before LOG.md:690 `PASS (119 cases, 0 skipped)`; after symlink-r19-20261019T174500Z-selftest.log tail `RESEARCH_GATE_SELFTEST: PASS (122 cases, 0 skipped)`, cases 120 `sweeps-symlink-escape`, 121 `sweeps-symlink-dir`, 122 `sweeps-inroot-symlink`; 1–119 cmp per corpus/evidence/README.md:652 row.
- No ledger row: `grep -ci symlink corpus/knowledge/hardening-r10.md` → 0; `git show --stat` for 5499cef/3eaa0cd/9b04830/2bb556b — hardening-r10.md absent from all four round-19 commits (only LOG, gate, records/receipts/note/SCORECARD/SKILL/READMEs, report).
- Queue lineage: verification-r16.md named-debt row (seat 20, quoted in draft); SCORECARD.md:846 (Planned r17), :902 (r18), :954 (r19) carry it; Planned r20 (:998–1005) drops it → closed. §3.9 queue enumeration hardening-r10.md:325–329 names no symlink.
- File revision trail: `git log --oneline -- corpus/knowledge/hardening-r10.md` → last pre-r20 touch `0ba7b97` (r15 records); blob at 5499cef = `1dd34d97…`; HEAD blob `cb304484…` (r20 `edcffba` moved it, not r19).
- Verdict facts: SCORECARD.md:958–996 (ADMIT; coverage/operability/depth/calibration improved, freshness/adjacency unchanged), LOG.md:693–703.

## Notes for L1
- E-number: derived by the file's own round→E mapping (r12→E1, r13→E2, r14→E3, r15→E4 ⇒ r19→E8, assuming r16–r18 addenda take E5–E7). If those addenda never land or number differently, renumber this one token.
- C3-adjacent stale site found (outside my write scope, named inside the draft): verification-r16.md named-debt row still reads "queue for round 17".
- Case 122 is exit-1 BY DESIGN (`SWEEP_CLAIM_FALSE` on an in-root symlink, `observed=hit`) — it pins non-refusal, not a failure.

VERDICT: Round 19 closed zero §3 ledger rows and zero round-11 queue items; it closed the round-16 symlink-escape named debt (gate `6e694881…`→`9f163807…`, selftest 119→122, cases 120–122); the draft above is style-matched and append-ready. Installs: none.

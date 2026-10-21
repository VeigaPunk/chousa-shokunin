# Round-20 addendum findings

## Draft for `hardening-r10.md`

### Round-20 addendum (2026-10-19, append-only)

E5 — **no §3 ledger row was closed, reclassified, or added; no round-11 queue
item was closed, changed, or added.** Row 70 (`:300`) — `scope-refusal finding
IDs never landed (documentary province boundary)` — remains **closed(r12)** as
E1 recorded; round 20 fixed a missed parser path in that already-implemented
screen, not a new ledger disposition. Before the fix, a `## Meta` inside
`<!-- -->` shadowed the real Meta and the demo was CLEAN; after, the gate emits
`SCOPE_BOUNTY_ABSORBED` and DRIFT. `load_sections` now tracks `in_comment`
alongside `fence_char`, checking comment state after fence state and before
the heading check; selftest case 124 pins the comment-shadow arm. Receipts:
`evidence/verify-r20-20261019T180000Z-{demo,selftest,battery,drift}.log`.

The round-20 independent closure recheck of rows 8–10, 56, and 70 did not
rewrite any historical erratum or disposition; the round-20 boundary and
inflection findings were named as round-21 debt, not round-11 queue changes.
`git diff edcffba^ edcffba -- corpus/knowledge/hardening-r10.md` shows only
the appended independent closure recheck, with no §3 or §6 disposition edit.
Gate SHA-256 (`git show <commit>:tools/research-gate.sh | sha256sum`):
`9f1638076915d9bf6ffb5816e342204081cc1ab07bc803fc7cb402147954c2ba` →
`49b36759bc47ffed8971834515f86921b45725038a3ccf20eb215f0fb64448e9`.
Selftest: `PASS (124 cases, 0 skipped)`; case 124 is `scope-comment-shadow`
(exit 1), cases 1–119 compare byte-identically with the r18 receipt.

## Evidence chain and calibration

- Ledger row 70's exact §3.8 text and original disposition: `corpus/knowledge/hardening-r10.md:293-301`; E1 explicitly closes that missing-ID debt at r12 and names cases 86–92: `hardening-r10.md:444-451`.
- The round-20 recheck says row 70 cases pass and the screen remains declaration-only; it closes with “No historical erratum or disposition counts were rewritten”: `hardening-r10.md:584-600`.
- The independent recheck insertion is the entirety of the `edcffba` hardening-file diff: `git diff edcffba^ edcffba -- corpus/knowledge/hardening-r10.md` → `1 file changed, 34 insertions(+), 0 deletions(-)`, appended at EOF. No row/queue status edit is present.
- HTML-comment behavior and fix: `corpus/knowledge/html-comment-r20.md:9-22`; round-20 before/after is `SCORECARD.md:1021-1031`, corroborated by `LOG.md:759-762` and demo receipt lines 1–8 (`CLEAN` before; `SCOPE_BOUNTY_ABSORBED` + `DRIFT` after).
- The precise selftest result is in `corpus/evidence/verify-r20-20261019T180000Z-selftest.log:120-125`: case 124 `scope-comment-shadow`, exit 1; `PASS (124 cases, 0 skipped)`. SCORECARD records cases 1–119 byte-identical: `SCORECARD.md:1027-1031`.
- The other audit findings were explicitly dispositioned as named round-21 debt, rather than round-11 queue changes: `SCORECARD.md:1032-1040`; `LOG.md:761`.
- Gate blobs re-derived read-only: `git -C /home/vgpnk/Projects/shokunin/chousa-shokunin show d650872:tools/research-gate.sh | sha256sum` → `9f1638076915d9bf6ffb5816e342204081cc1ab07bc803fc7cb402147954c2ba`; `git -C /home/vgpnk/Projects/shokunin/chousa-shokunin show edcffba:tools/research-gate.sh | sha256sum` → `49b36759bc47ffed8971834515f86921b45725038a3ccf20eb215f0fb64448e9`.

VERDICT: No §3 row or round-11 queue disposition changed in round 20; append the E5 draft above. Installs: none.
# Attack20 — R39/R40 active-receipt drift item #3: origin and safe repair

Seat: L1Chousa48.Attack20 (reviewer) · date: 2026-10-25 · lane: chousa-shokunin
Item (w1-spec): independently analyze R39/R40 active-receipt drift item #3 — inspect
committed receipts, adding commits and tip-gate change; determine whether the
`gate-sha256-mismatch` is corrupt evidence or expected revision drift, and whether a
safe byte-preserving repair exists. Read-only; no rewriting receipts; no fetch.
Scratch `/tmp/chousa-r48-attack20` removed before return.

## Verdict

The `gate-sha256-mismatch` on the four research-gate-bound active receipts is **expected
revision drift, not corrupt evidence**: the receipts bind the gate bytes measured in
rounds 39/40 (`4253c187…`), and round 41 legitimately moved `tools/research-gate.sh`
to `2cb04bdd…` (commit `1bd9001`, +92/−2). A **safe byte-preserving repair exists**:
verify the four receipts against their recorded measurement revision (the committed
r39/r40 gate control bytes at `6d914e9`/`d164f88`) instead of the live tip gate — no
receipt byte changes; the active six replay 6/6 at any future tip. Reissuing under the
new gate sha is the *other* permitted option, but it is not byte-preserving and is
therefore out of scope for this item.

## Measured facts

- Six-row active manifest `corpus/evidence/round40/active-r39-receipts.tsv` (added
  `6c01a41`): 3 r40 regenerated + 3 preserved r39 originals. Of the six, four bind
  `tools/research-gate.sh`; two bind unchanged control gates.
- Receipt bindings (field dump of all six): research-gate rows `c1-after-s39011-
  regenerated.json`, `c1-after-s39111.json`, `c2-after-s39101.json`,
  `c2-after-s39121.json` all carry `gate_sha256_pre == post == 4253c18738f84df9…`
  (and alias `gate_sha256` same). Control rows `c1-base-s39001-regenerated.json` bind
  `0447ad14…` (`base-gate-r39.sh`); `c1-mutenv-s39013-regenerated.json` bind
  `e1251030…` (`mut-gate-path-env.sh`).
- Gate blob history (`git show <rev>:tools/research-gate.sh | sha256sum`):
  `6d914e9` (r39) = `4253c187…`; `d164f88` (r40) = `4253c187…`;
  `b173b094` (r41 freeze, parent of the gate edit) = `4253c187…`;
  `1bd9001` (r41) = `2cb04bdd…`; HEAD = `2cb04bdd…`. The only gate-mutating commit
  between r40 tip and HEAD is `1bd9001` (r41: capture-tool pins mktemp/sed/mkdir/
  cat/rm/sort/readlink/dirname/date/tr/wc/od/head/stat, `PATH` scrub, `LD_*` unset;
  92 insertions, 2 deletions; no receipt paths in the diff).
- Tip replay: `python3 corpus/evidence/round40/c1-count.py` (byte-identical to the
  frozen `6c01a41` blob `d9b38b57…`) → 4 rows `VERIFY-FAIL: gate-sha256-mismatch`
  (the four research-gate rows), 2 rows `VERIFY: ok` (control-gate rows);
  `R39_ACTIVE_RECEIPTS=2/6`, exit 1.
- Pinned replay (same counter, same receipt bytes, archive at r40 freeze `6bc90e0` +
  gate `4253c187…`): `R39_ACTIVE_RECEIPTS=6/6`, exit 0 — all six rows `VERIFY: ok`.
- Control-gate shas at tip still equal the bindings (`base-gate-r39.sh` = `0447ad14…`,
  `mut-gate-path-env.sh` = `e1251030…`) — the two passing rows are stable, matching
  the prediction that only the moved file's rows fail.

## Corruption hypothesis discarded

- Every receipt's `receipt_sha256` self-digest re-derives OK (canonical
  `json.dumps(body, indent=2, sort_keys=True) + "\n"`); none was edited after its
  adding commit (`git log --diff-filter=A`: r40 ×3 at `d164f88`, r39 ×3 at
  `6d914e9`; no later touches). Committed blobs and worktree bytes agree.
- The four failing rows bind exactly the gate bytes that existed at their adding
  commits; the r41 commit that moved the gate is *later* than all four adds, so the
  refusal is a stale-binding artifact of hashing the live tip file, not a doctored
  body. Same signature (control rows pass, research-gate rows fail) rules out a
  blanket/accidental byte corruption of the receipts.
- Prior lane record agrees: r41 lesson post-landing addendum (`d720b1d`) predicts this
  exact failure mode and calls it "correct receipt semantics, not a regression"; r47
  lesson mistake 9 (`ExecReceiptSpot`) logs it as the unclosed routed fix carrying
  since round 41; SCORECARD r48 candidates (line 2530) list it. No contradiction with
  any committed source found.

## Safe byte-preserving repair (design, not applied — read-only seat)

Single-option repair preserving every existing receipt byte:

1. Commit the r39/r40 landed-gate bytes byte-exact as a control copy
   (`.ufo/waves/round-39/controls/research-gate-r39.sh` = `git show
   6d914e9:tools/research-gate.sh`, sha `4253c187…`). The two other controls already
   exist.
2. Point the four research-gate manifest rows at that control path; the counter then
   verifies each receipt against the gate revision the receipt itself records, and
   the six rows replay `6/6` at any future tip.

This is the r41 addendum's option (b) ("verify receipts against their recorded
measurement revision instead of the live `tools/research-gate.sh` digest"). It keeps
receipts as faithful byte-for-byte evidence of what was measured and the gate control
as a committed historical object. Residual: the control-gate bytes live in-tree, so a
future gate edit still reports the drift on re-verify of the pinned leg — which is the
point (QUALITY 68 pinned/tip legs) — and receipt authorship remains unauthenticated
(unkeyed digests; named limit unchanged). Reissuing under the new gate sha (option
(a) of the addendum) would change receipt bytes and re-derive the predicate against the
r41+ surface; it is a different repair, not a byte-preserving one.

## Commands run (decisive output)

`git log --format='%h %ad %s' --date=iso -- tools/research-gate.sh`; `git show
<rev>:tools/research-gate.sh | sha256sum` for 6d914e9/d164f88/b173b094/1bd9001/HEAD;
`git archive 6bc90e0 | tar -x -C /tmp/…` then `corpus/evidence/round40/c1-count.py`
(tip gate 2/6 vs pinned gate 6/6); per-row `verify-receipts.py --receipt … --gate …`
loop; `git log --diff-filter=A` per receipt; `sha256sum` of control gates; receipt
binding-field dump; `git log` of `round40/c1-count.py` + manifest (unchanged since
`6c01a41`). No installs; no fetch; no lane/production file modified.

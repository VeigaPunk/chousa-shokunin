# Attack18 — R39/R40 active-receipt drift, item #1 (gate-sha256-mismatch)

author: L1Chousa48.Attack18 (critic; leaf, no subagents)
date: 2026-10-25
lane: chousa-shokunin · tip `d4e6ef0` · assignment: `.ufo/waves/round-48/w1/Attack18.md`
scope: read-only analysis of committed r39/r40 receipts, their adding commits, and the
tip-gate change; no rewriting of receipts, no fetch (L0 `8d77e6c1` open). No files changed.

## 1. Measured receipts

Active manifest `corpus/evidence/round40/active-r39-receipts.tsv` (6 rows, added
`6c01a41`). All six receipt paths exist at tip; each TSV gate path is a committed file.

| receipt | gate binding (TSV) | gate sha recorded (pre=post) | adding commit |
|---|---|---|---|
| r40 `receipts/c1-base-s39001-regenerated.json` | `.ufo/waves/round-39/controls/base-gate-r39.sh` | `0447ad14…` | `d164f88` |
| r40 `receipts/c1-after-s39011-regenerated.json` | `tools/research-gate.sh` | `4253c187…` | `d164f88` |
| r40 `receipts/c1-mutenv-s39013-regenerated.json` | `.ufo/waves/round-39/controls/mut-gate-path-env.sh` | `e1251030…` | `d164f88` |
| r39 `receipts/c1-after-s39111.json` | `tools/research-gate.sh` | `4253c187…` | `6d914e9` |
| r39 `receipts/c2-after-s39101.json` | `tools/research-gate.sh` | `4253c187…` | `6d914e9` |
| r39 `receipts/c2-after-s39121.json` | `tools/research-gate.sh` | `4253c187…` | `6d914e9` |

Gate digests verified: `base-gate-r39.sh`→`0447ad14…`, `mut-gate-path-env.sh`→
`e1251030…` (unchanged at tip); `tools/research-gate.sh`→`4253c187…` at `6bc90e0`/
`6d914e9`/`d164f88`/`6c01a41`, →`2cb04bdd…` at `1bd9001` and tip (measured:
`git archive` + `sha256sum`).

## 2. Counter behavior (re-measured)

- **Tip (live tree):** `python3 corpus/evidence/round40/c1-count.py` →
  `R39_ACTIVE_RECEIPTS=2/6`, exit 1. Exactly four refusals, all
  `gate-sha256-mismatch`: `c1-after-s39011-regenerated`, `c1-after-s39111`,
  `c2-after-s39101`, `c2-after-s39121` — precisely the four receipts bound to
  `tools/research-gate.sh`. The two receipts bound to the untouched control scripts pass.
- **Pinned revision `6bc90e0` (git archive):** same counter → `R39_ACTIVE_RECEIPTS=6/6`,
  exit 0.
- **Adding-commit archives (`d164f88`, `6d914e9`):** newest committed verifier
  (`corpus/evidence/round39/verify-receipts.py`) over all six active receipts → `VERIFY: ok`
  rc 0 for every receipt where it exists; the per-adding-commit pinned leg holds.
- **Receipt integrity:** all six `receipt_sha256` self-digests re-derive MATCH (json
  body minus self, `indent=2, sort_keys=True` + `\n`); all `counter_sha256` and
  `expect_sha256` bindings match committed bytes (`c1-count.py` `91618e91…`,
  `c2-count.py` `43849e9a…`, `expectations.jsonl` `01cbdc3a…`). No doctoring signal.

## 3. Verdict

**Expected revision drift, not corrupt evidence.** The four refusals are the binding
working: `1bd9001` (r41) legitimately moved `tools/research-gate.sh` from `4253c187…`
to `2cb04bdd…` (subject "pin capture invocation surface"; +94/−2 lines, selftest
275/275 PASS). Every active receipt verified at its own adding commit with the exact gate
bytes it recorded; the tip refusal has a traced post-adding commit (`1bd9001`) — the
QUALITY 68 "refusal with no such commit is a defect" test is not triggered. This is
already documented as correct semantics in `corpus/lessons/round-41.md` §Post-landing
addendum ("correct receipt semantics, not a regression"; "No r40 or gate bytes were
rewritten") and in QUALITY 68 (`corpus/QUALITY.md:664-683`).

**No safe byte-preserving repair exists.** Rewriting the four receipts’ `gate_sha256_pre/
post` to `2cb04bdd…` would change their bodies, invalidate their self-digests, and require
re-sealing — falsifying frozen measurement bytes; reverting `1bd9001` rewrites history and
harms the r41 claim. Neither is a repair. Forward-only, non-destructive options: (a) pin
the r40 counter to its measured revision (`6bc90e0`/`4253c187…`, verified 6/6) per QUALITY
58; (b) a successor counter verifies receipts against their recorded measurement-revision
gate snapshots, keeping the tip leg as a documented accounting of drift. Both leave all
receipt bytes untouched.

## 4. Evidence commands

`git log -1 --diff-filter=A -- <receipt>` (adding commits); `git ls-tree -r <rev>` +
`git cat-file blob <rev>:tools/research-gate.sh | sha256sum`; `python3
corpus/evidence/round40/c1-count.py` at tip and in `git archive 6bc90e0`; `python3
corpus/evidence/round39/verify-receipts.py` in `git archive d164f88` / `6d914e9`;
python re-derivation of receipt/counter/expect digests. Scratch `/tmp/chousa-r48-attack18-a`
`-b` removed. No installs.

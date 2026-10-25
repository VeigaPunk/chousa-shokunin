# Attack19 — R39/R40 active-receipt drift item #2 (round 48, wave 1)

**Seat:** reviewer, leaf. No subagent dispatch, no fetch, no installs.
No scratch left under `/tmp` (removed before finish). Lane root:
`/home/vgpnk/Projects/shokunin/chousa-shokunin`; tip `d4e6ef09…` (checked
via `git log -1`). Report only — no production file was modified.

**Item:** independently analyze R39/R40 active-receipt drift item #2; inspect
committed receipts, adding commits, and the tip-gate change; determine whether
`gate-sha256-mismatch` is corrupt evidence or expected revision drift; determine
whether a safe byte-preserving repair exists. No rewriting receipts, no fetch.

## 1. What the drift is (arithmetic of the failure)

The round-40 C1 predicate (`corpus/evidence/round40/claims.md:9-19`) verifies
six active receipts in `corpus/evidence/round40/active-r39-receipts.tsv` via
`corpus/evidence/round39/verify-receipts.py`, which enforces byte-binding of
the gate: `receipt["gate_sha256_pre"]` must equal `sha256_file(gate)` and
`gate_sha256_pre == gate_sha256_post` (verifier lines 208-216). Four of the six
active rows bind `tools/research-gate.sh`, `gate_sha256=4253c187…`; two bind
round-39 control gates (`base-gate-r39.sh` `0447ad14…`, `mut-gate-path-env.sh`
`e1251030…`, both unchanged since).

- At tip: `python3 corpus/evidence/round40/c1-count.py` →
  `R39_ACTIVE_RECEIPTS=2/6`, exit 1; exactly the four research-gate rows refuse,
  each `VERIFY-FAIL: gate-sha256-mismatch`.
- At the receipt-time revision `6bc90e0` (`git archive` into `/tmp`):
  `sha256sum tools/research-gate.sh` = `4253c18738f84df9200cbc93f8e077ba63a418c5ee822c1324e1a8d75a9b07e3` (the bound digest); the same counter prints `R39_ACTIVE_RECEIPTS=6/6`, exit 0.

The refusal is therefore exactly the delta between the gate bytes the receipts
bind and the gate bytes on disk now.

## 2. Corrupt evidence? No — every corruption probe is clean

- Self-digests: recomputed `receipt_sha256` over the canonical body
  (`json.dumps(sort_keys, indent=2)+"\n"`) for all 10 committed receipts (7
  round-39 originals, 3 round-40 regenerated) — all True. No receipt is
  internally inconsistent.
- No other binding failed: for all four refusals the verifier reached the gate
  check, which sits after counter/expect/verifier digests, scenario census,
  `ok` re-derivation, `matched`/`total` recount, and predicate-holds and
  (c2 family) subject-counter digest (verifier lines 121-216). If any of those
  were stale, the first refusal would have said so. It never does.
- Receipts and instruments are byte-identical since the pinned revision:
  `git diff --stat 6bc90e0 HEAD -- corpus/evidence/round39/{verify-receipts.py,expectations.jsonl,c1-count.py,c2-count.py,receipts} corpus/evidence/round40/{c1-count.py,active-r39-receipts.tsv,receipts}` → **empty**. No file in the evidence plumbing changed since the receipts were issued.

## 3. Expected revision drift? Yes — one intentional gate commit explains 4/4 refusals

- The gate history (`git log --follow -- tools/research-gate.sh`): round-39
  version (sha `4253c187…`) was replaced once, by round-41 commit `1bd9001`
  "pin capture invocation surface (12/12)". `git show 1bd9001:tools/research-gate.sh | sha256sum` = `2cb04bdd…`, which equals the tip sha — the gate has not changed since round 41.
- The diff `6bc90e0..1bd9001` is additive and purposeful: startup capture-tool pins (mktemp/sed/mkdir/cat/rm/sort/readlink/dirname/date/tr/wc/od/head/stat with provenance refusal), a fixed child `CAP_CHILD_PATH` + `LD_PRELOAD`/`LD_LIBRARY_PATH` scrub in `gate_canonical_capture`, and the `metadata-stat-unavailable` selftest case re-routed through `RESEARCH_GATE_STAT` (previously PATH-shimmed). It is the round-41 C1 work, supported by its own control/after (1/12 → 12/12, `corpus/evidence/round41/measure-after-c1.txt`) and selftest PASS 275 (round-41 lesson, mistake row 1).
- Semantic continuity holds: re-running the round-39 counter against the **current** gate (`timeout 280 python3 corpus/evidence/round39/c1-count.py --gate tools/research-gate.sh`) yields `ENV_PIN_CAPTURE_MATCH=8/8` with observations identical to those recorded in the four bound receipts (`matched 8/8`, `predicate_holds true`). The recorded content is still true; only the byte identity changed.
- The lane already官方ed this reading: `corpus/lessons/round-41.md` post-landing addendum (lines 54-71) states the failure is "correct receipt semantics, not a regression", names the scope (`6bc90e0` + gate `4253c187…`) where 6/6 replays, and routes a successor-counter design to round 42. The round-47 verifier spot-check (`corpus/lessons/round-47-verifier-spotcheck.md:65`) carries it as a known item. My independent measurement reproduces the addendum's numbers at the current tip.

**Verdict:** the ~gate-sha256-mismatch` on R39/R40 active receipts is **expected receipt-sha binding drift** (intentional later gate edit), **not corrupt evidence**. The receipt corpus is intact, honest, and reproducible at its measurement revision.

## 4. Does a safe byte-preserving repair exist? Yes — two, plus a successor design

Constraint: no receipt bytes rewritten (and none should be — they are historical
evidence; their byte identity is the only thing that proves what was measured
when).

1. **Verification-path pin (zero repo writes, works today):** run the frozen
   counter inside `git archive 6bc90e0` (done above: 6/6, exit 0). This is the
   attestation path for the admitted round-40 claim and requires no change to
   any committed file.
2. **Pinned gate-snapshot retarget (repo change, still byte-preserving for
   receipts):** vendor the exact historical gate bytes (`git show 6bc90e0:tools/research-gate.sh`) as a new file (e.g. `.ufo/waves/round-40/controls/research-gate-r40-pinned.sh`) and point the four manifest rows at it. The receipts still bind `4253c187…`; the round-40 counter (which reads the manifest and is itself unbound) returns 6/6 at tip again. Requires an append-only erratum in `round40/claims.md` stating the gate leg means snapshot bytes at the measurement revision, not the live tool, and that the manifest stays six rows (the counter enforces both). No fetch, reversible, receipts untouched.
3. **Successor counter (matches the round-41 lesson's routed design):** next time this lineage is frozen, verify against the receipt's recorded measurement revision (e.g. explicit `--gate <path>@<rev>` or resolving the gate from the bound object id) instead of the live file — the round-41 counters already do the explicit-`--gate` half (QUALITY 58). This is a tool-contract fix, not an evidence fix.

Not safe / out of scope: rewriting or reissuing receipts (forbidden), reverting
`tools/research-gate.sh` (would break round-41 claims), or altering
verifier/expectations bytes (would break binding).

## 5. Residual risk and verification gaps

- The frozen round-40 predicate as written (live-gate digest) will keep failing
  at any tip that carries a later gate byte set. That is a measurement-target
  contract gap (QUALITY 58 class), not an evidence defect; it should be
  recorded as such in the scorecard/lesson, not by editing the claim.
- Did not re-run the round-39 C2 counter under the new gate; its binding is
  byte-stable (verifier and subject counter unchanged since `6bc90e0`, and both
  c2 receipts passed every check up to the gate leg), so semantic re-replay is
  low-risk but not independently re-measured here.
- Gate semantic equivalence beyond the 8/8 capture surface rests on the round-41
  selftest PASS 275 and 12/12 after-measurement; not exhaustively re-proven in
  this seat.
- The working tree carries unrelated pre-existing modifications (inherited
  r40/r41 swarm registries, `corpus/SOURCES.md`, `cells.json`); none overlap the
  inputs above, which were read from committed bytes/git objects.

## 6. Commands run (decisive output)

```
git log -1                                  # d4e6ef09… (tip)
sha256sum tools/research-gate.sh             # 2cb04bdd…
python3 corpus/evidence/round40/c1-count.py  # 2/6 exit 1; 4x gate-sha256-mismatch
git archive 6bc90e0 | tar -x -C /tmp/…; sha256sum tools/research-gate.sh  # 4253c187…
python3 corpus/evidence/round40/c1-count.py  # 6/6 exit 0 (archive tree)
git diff --stat 6bc90e0 HEAD -- <receipt+instrument paths>   # empty
python3 -c '…'  # 10/10 receipt self-digests valid
git diff 6bc90e0 1bd9001 -- tools/research-gate.sh  # additive pin hunk
git show 1bd9001:tools/research-gate.sh | sha256sum  # 2cb04bdd… == tip
timeout 280 python3 corpus/evidence/round39/c1-count.py --gate tools/research-gate.sh  # ENV_PIN_CAPTURE_MATCH=8/8
```

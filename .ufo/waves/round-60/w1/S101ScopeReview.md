# S101ScopeReview — round-60 wave-1 scope review of the frozen claims

Seat: reviewer (leaf, no dispatch). Reviewed: the frozen claims at
`corpus/evidence/round60-claims.md`, prior committed evidence, and the current
counter/source bytes only. Read-only throughout: `read`/`grep`, read-only git
(`status`, `log --all`, `ls-files`, `hash-object`, `rev-parse`), counters executed
with `--work` inside scratch (C1) or with no writes at all (C2). No live fetch, no
installs, no edits outside this report, no git/jj mutation. The frozen claims file
was not touched.

## Findings by severity

### F1 — HIGH: C2's frozen predicate is contradicted by its own counter; base already passes

- Frozen predicate (`corpus/evidence/round60-claims.md`, C2 "Frozen predicate"):
  "Base must fail because no round-60 entry exists."
- Direct run of the named instrument on the untouched base:

  ```
  $ python3 corpus/evidence/round60/c2-count.py
  RAW_PIN=1/1 FORM_PIN=1/1 QUOTE=1/1 LINE=245 METADATA=1/1 LIMIT=1/1
  C2=PASS
  c2-exit=0
  ```

- Cause: the counter references no round-60 entry at all. `c2-count.py:13` pins
  `entry` to the pre-existing `corpus/knowledge/citation-count-semantics-r37.md`,
  which already carries everything checked (source line, `verified-at`, `recheck`,
  `#### Unknown` cap-limited statement — independently located by
  `w1/C2CounterAudit.md:23` at `:5,74-80`). No check is round-60-conditional, so a
  do-nothing control reaches the declared target — the §9 kake-r34 class; §9:
  "if it meets the target, the counter or target is wrong — fix it before data."
- Contradicted control receipt: `.ufo/waves/round-60/c2-before.txt` (17:52)
  asserts "Baseline must fail by missing round-60 source gate; C2 not admitted."
  That is prose; the instrument the predicate names proves the opposite.
- Two further predicate components are unimplemented: no SCORECARD-disposition
  check ("require the scorecard's declared disposition" — no SCORECARD reference in
  `c2-count.py`), and no verification of "the new entry's exact observation and no
  overreach" (only fixed substring checks against the r37 note).
- Rule-freeze consequence: seats already scored this counter before this review
  (`w1/C2CounterAudit.md:22-25` recorded the same base pass). Per §9 a rule changed
  after any seat has scored is not the claim's rule — the counter cannot be
  legitimately repaired this round. Recommendation: L1 reports C2 against the
  frozen counter honestly (target control-reachable / not admitted), no mutation of
  counter or claims.

### F2 — HIGH: the dispatched immutable claim SHA matches no observable bytes; provenance unresolved

- Every w1 seat assignment (`w1-dispatch.json`, `w1-spec.json`) declares immutable
  claim SHA `09d8053f5f09a26c07f41286a7a885a2c21bff31b30f71963cceaa35d971a440`.
- Actual bytes: `sha256(corpus/evidence/round60-claims.md)` =
  `65721569fc1336b159c7637acf476cda6f583bbd4b3a84aaadd239f7d02018d1` (3355 bytes).
- Variants ruled out (all differ): no-trailing-newline `cae804fa…`, CRLF `dbb847b8…`,
  whitespace-stripped `cae804fa…`; git blob hash `5ea0acf0…` (not a blob/sha256
  confusion).
- Fleet-wide grep: the `09d8053f` string occurs only inside
  `chousa-shokunin/.ufo/waves/round-60/{w1-dispatch.json,w1-spec.json}` and seat
  reports echoing it (independent sightings: `w1/C2CounterAudit.md:22`,
  `w1/S101Reopen.md:21`). No freeze note, goal file, or registry records it; the
  operative digest `65721569…` is recorded nowhere L1-side either (only in sibling
  seat reports).
- Mitigating — the "freeze untouched after dispatch" requirement holds per
  observable evidence: claims mtime 2026-10-27 17:51:18-03 precedes
  `w1-dispatch.json` 17:55:19, `w1.ready` 17:55, `w1.ready.dispatched` 17:56. The
  claims bytes were not modified after dispatch; the declared digest was stale or
  wrong at dispatch time, not evidence of post-dispatch tampering.
- Freeze anchor status: the claims file is UNTRACKED (`git status --porcelain`:
  `?? corpus/evidence/round60-claims.md`); `git log --all` shows no commit ever
  touched it. The freeze currently has no committed anchor; it becomes verifiable
  only if the L1's round-end `jj-lane.sh` commit lands exactly these bytes, and the
  closure should cite `65721569…` (not the dispatch's SHA) as the operative freeze
  digest, noting the dispatch deviation.

### F3 — MEDIUM: C1 counter leg (c) is vacuous — the forge leg can never fail, one kill-rule clause is unreachable

- `corpus/evidence/round60/c1-count.py:42-44`: `baseline_bad` and `forged_safe`
  carry identical conditions (`rc==0 and not intact`); the ternary at `:44`
  evaluates `baseline_bad` first, so the state `"forged_safe"` is unreachable —
  `run()` returns only `{"candidate_safe","baseline_bad",""}`.
- `:63` `forge_blocked = forge_state != "forged_safe"` is therefore a tautology;
  `INJECTION_REJECTED=1/1` prints regardless of any builder's behavior.
- The predicate's leg (c) ("the output-injection mutant prints `=PASS` but is
  scored as a failure") is true by construction — verdicts at `:40-44` never read
  child output — not by measurement: the counter never runs the round-58 counter
  bytes for comparison. The kill-rule clause "any child output injection passes
  target" can never fire.
- What is meaningfully measured and did run (my receipts): output-blindness (the
  generated `forged.py` prints `=PASS`, exits 0, touches nothing → scored
  `candidate_safe`, not PASS), baseline discrimination (pinned r55 deletes the
  seeded foreign file → `BASELINE_DISCRIMINATES=1/1`), candidate refusal
  (`CANDIDATE_REFUSAL=0/1` at base — see F6). The claim's measurement-integrity
  spirit survives; the frozen leg (c) overstates a tautology as a demonstrated
  property.

### F4 — MEDIUM: freeze, counters, capture-form fixture, and dispatch are all untracked at wave time

- The lane's only dirty paths are `?? .ufo/waves/round-60/`,
  `?? corpus/evidence/round60-claims.md`, `?? corpus/evidence/round60/` — so the
  claims file, both round-60 counters, the w1 dispatch/spec, and the S101 capture
  form have no committed anchor when the wave scores them.
- `.ufo/waves/round-60/s101-open.txt` (form fixture, UNTRACKED, 47356 bytes,
  sha256 `a8e3e7ad213b6ec5…` — matches the `FORM_SHA` pinned at
  `c2-count.py:8`) was written 17:51:43: after the claims freeze (17:51:18), before
  the counter that pins it (17:52:14). L1-side provenance this round; uncommitted.
- Mitigations and the closing condition: byte-pinning by SHA inside the counters
  means any drift fails `RAW_PIN`/`FORM_PIN` loudly; round-58 evidence bytes remain
  frozen (nothing outside the round-60 paths is modified; current committed-tree
  hashes `corpus/evidence/round58/c1-count.py` = `65da18bb…703d3f`,
  `c2-count.py` = `dbb85961…91c8503`). If the L1's round-end commit lands these
  exact bytes, §9's "one command over committed bytes" precondition is met; until
  then it is unmet.

### F5 — LOW: predicate parameters are decorative

- C1: `--seed 6001` is parsed (`c1-count.py:52`) and never read; every seed behaves
  identically, so the frozen predicate's seed implies variation that does not exist.
- C2: `--work` is parsed and never used (`c2-count.py:13`); the counter writes
  nothing anywhere (receipts are stdout-only).
- C2 form path: `c2-count.py:13` reads the form from `ROOT` (its own lane), not
  from `--root`; under the predicate's `--root <lane-copy>` invocation the raw
  capture and entry come from the copy but the form still comes from the canonical
  lane. Defensible (the form is a fixture pinned by `FORM_SHA`), but the predicate
  text does not say so.

### F6 — Consistency checks that PASSED (recorded for the closure)

- Claim base `b379919a873e7080a31ef92c7002f55f5374e2c6` equals the current lane
  tip (detached HEAD and `master` both at `b379919`). Matches the claims header.
- C1 before-state is well grounded in committed evidence: TRACKED
  `.ufo/waves/round-59/w1/R59Executor09.md` (`:57`, `:74`, `:88-96`, `:215-221`)
  demonstrates the round-58 counter is unsatisfiable for honest builders and
  `C1=PASS`-reachable by output injection — matches the claims' Before narrative.
- Pinned r55 control exists and is TRACKED:
  `corpus/evidence/round58/controls/build-spans-r55.py`, sha256
  `1ed2650af28ea8e392bc34f7259cfb58f93b05c7453aca60e86b170c59c80bf6` — and is
  byte-identical (`cmp` clean) to the default candidate `tools/build-spans.py`
  (same hash). Hence the current tree's candidate leg fails exactly as the
  control receipt says (`c1-control-proof.txt` #3); my run: `C1=FAIL`, exit 1.
  C1's target is control-unreachable — the honest before→after shape §9 wants.
- L0 `8d77e6c1` still open: `/home/vgpnk/Projects/shokunin/.ufo/l0-questions.md:136`
  (reaffirmed `:140`) — matches "L0 8d77e6c1 stays open".
- Counter hygiene: `c1-count.py` honors `--work` and `HYAKU_SCRATCH`, has no
  hardcoded `/tmp`, sets `TMPDIR` for children, confines writes to work dirs, and
  removes its tree only when `--work` is not passed (the predicate always passes
  it, preserving receipts) — §7.4 compliant.
- Claim sizing: both claims name a counter, kill rule, and a bounded non-universal
  target; C1's disclaimers ("does not claim the builder itself meets all hazard
  legs") are consistent with leg (a)'s single foreign-file scenario.

## Timeline (file mtimes, 2026-10-27 -03)

| time | file |
|---|---|
| 17:51:18 | `corpus/evidence/round60-claims.md` (freeze write; unchanged since) |
| 17:51:38 | `corpus/evidence/round60/c1-count.py` |
| 17:51:43 | `.ufo/waves/round-60/s101-open.txt` (form fixture) |
| 17:52:14 | `corpus/evidence/round60/c2-count.py` |
| 17:55:15 / 17:55:19 | `w1-spec.json` / `w1-dispatch.json` (declare the non-matching SHA) |
| 17:55 / 17:56 | `w1.ready` / `w1.ready.dispatched` |

The counters and fixture were finalized after the freeze text but before dispatch;
no post-dispatch modification of any of them is observable.

## Residual risk and verification gaps

- The provenance of `09d8053f…` is unresolved from seat-visible evidence — most
  plausibly a digest of a pre-freeze planning draft. If the L1 holds bytes hashing
  to it, reconcile in the round report; otherwise the closure must cite
  `65721569fc1336b159c7637acf476cda6f583bbd4b3a84aaadd239f7d02018d1` as the
  operative freeze digest and log the dispatch deviation as a mistake.
- I tested the claims file's plausible byte variants and grepped the fleet for the
  declared digest; I did not attempt a exhaustive preimage search, and I did not
  re-derive `c1-control-proof.txt` #1's exclusion (r58 counter ×
  `tools/research-gate.sh`, interface mismatch).
- C2's structural remedy (a new round-60 entry, a counter re-pointed at it, and a
  SCORECARD-disposition check) is now barred by §9 scoring-order: seats scored the
  frozen counter first. My findings are a recommendation; I edited nothing.

## Receipts (verbatim outputs; scratch removed)

```
$ python3 corpus/evidence/round60/c2-count.py            # base, no args, read-only
RAW_PIN=1/1 FORM_PIN=1/1 QUOTE=1/1 LINE=245 METADATA=1/1 LIMIT=1/1
C2=PASS
c2-exit=0

$ python3 corpus/evidence/round60/c1-count.py --builder tools/build-spans.py \
    --work /fast/scratch/hyaku/chousa-r60/S101ScopeReview/c1work --seed 6001
INJECTION_REJECTED=1/1
BASELINE_DISCRIMINATES=1/1
CANDIDATE_REFUSAL=0/1
C1=FAIL
c1-exit=1

$ sha256sum corpus/evidence/round60-claims.md
65721569fc1336b159c7637acf476cda6f583bbd4b3a84aaadd239f7d02018d1  corpus/evidence/round60-claims.md
$ git -C /home/vgpnk/Projects/shokunin/chousa-shokunin status --porcelain
?? .ufo/waves/round-60/
?? corpus/evidence/round60-claims.md
?? corpus/evidence/round60/
$ sha256sum corpus/evidence/round58/controls/build-spans-r55.py tools/build-spans.py
1ed2650af28ea8e392bc34f7259cfb58f93b05c7453aca60e86b170c59c80bf6  corpus/evidence/round58/controls/build-spans-r55.py
1ed2650af28ea8e392bc34f7259cfb58f93b05c7453aca60e86b170c59c80bf6  tools/build-spans.py
```

Scratch `/fast/scratch/hyaku/chousa-r60/S101ScopeReview` removed before yield; all
receipts are embedded above and in this file.

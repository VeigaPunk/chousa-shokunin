# Round 32 — serialized manifest appends and an audit of "could not be followed"

Dates are UTC. Base `7a7259f0ad41a68068131bfa422a829db9fd1b55` (gate SHA-256 `0bc318b3…1258`, the
landed round-31 gate). Attempt 1 (`ChousaR32-16`) committed design v1 at `4111607c` and died with
the orchestrator at 06:19:06Z before any seat ran; its uncommitted wave files were deleted
unread-as-evidence by attempt 2 (`gen-wa-spec.py`, `wa-spec.json`, `wa-dispatch.json`,
`wa-run.err`, `wa/swarm-registry.json`). Rounds 29–31 all worked `verify-claims` and
`tools/quote-reopen.py`; neither claim here touches them.

- **C1 operability** (lowest scored axis; surface: the `verify-all --json` manifest append) — the
  append is one flock-held critical section on the manifest. Pre-registered at round 25
  (`SCORECARD.md` Planned — round 26, item 1).
- **C2 coverage** (surface: the exempt arm of `verify-chain`) — hops marked `unresolved`,
  `blocked-no-fetch` or `labelled-dead` are read; a resolvable one drifts. Frontier: "exemption is
  record-declared and unverifiable" (`corpus/README.md` Frontier, Round 3).

Frozen design: `corpus/evidence/round32/claims.md` (v1 `4111607c`; v2 `3d586d3a`, after the control
wave, before any candidate receipt). Control evidence: `.ufo/waves/round-32/w1/` (`f43dd5a3`,
`a065845a`) and `.ufo/waves/round-32/controls/`. Candidate: `0f96bc1c` (gate `10f2fe12…`).

## Spot-check intake (round 31, `round-31-verifier-spotcheck.md:201-234`)

All six routes are repaired; the record with evidence is `corpus/evidence/round32/r31-repairs.md`.
R1 correction appended to `lessons/round-31.md`; R2 counters v3 (`corpus/evidence/round31/c{1,2}-count-v3.py`)
and seven selftest cases; R3 battery on `0bc318b3` (`w1/ExecNoHarmBase32/`); R4 three text
fixes; R5 provenance (`bfc0b02b` = the committed round-31 oracle script); R6 in the fleet report.
Carried: nested `"line"`/`"sha256"` keys are still read as the record's own (unanchored
`json_str`/`json_has_key`; `w1/ExecR2Selftest31.md`, `w1/ExecR2CounterV3/nested-probe.log`).

## Control wave findings (before data)

- C1 v1: a gate that locks around the probe and unlocks before writing scored 24/24 on two seeds
  (`w1/CtlC1PartialLockB/b-s3247102{1,2}.json`). The append lands microseconds after the unlock;
  the next writer's probe takes milliseconds.
- C2 v1: duplicate findings, no DRIFT verdict, CLEAN with exit 0 and a stray finding on an unknown
  hop each scored 120/120 (`w1/MutC2CounterB/frozen-*`, `w1/CtlC2NoisyB`); case-insensitive and
  whitespace-collapsing readers scored 120/120 (`w1/CtlC2WeakReaderB/*-isolated-mutated-*`).
- Under v2 every control misses. Highest: C1 12/24 (sibling-file flock, lockf, mkdir lock: they
  serialize each other but not a writer that locks the manifest); C2 126/132 (boundary skip,
  case-insensitive, whitespace collapse) and 120/132 (status-blind, generator-union shortcut).
  Oracles: C1 24/24 (three implementations, `w1/OracleC1B/v2-rescore.md`); C2 132/132.
- Holds (safety-filter refusals, item ended, not retried): CtlC1ShortcutB (label-keyed C1
  shortcuts, no output), CriticPredicateGaps32b (no output), CtlC1JitterB's v2 re-score (its v1
  receipts stand: 11/24 at best).

## Mistakes

| Class | Evidence | Captured-by | Fix |
|---|---|---|---|
| A lesson called a mutant counter-killed though both counter receipts are 120/120 | `lessons/round-31.md:97-98`; `.ufo/waves/round-31/falsify/MutC2Hash/failopen.mutated.*.receipt.json` (120/120, `predicate_holds=true`) | none in the lane; the round-31 outside spot-check (R1) | correction appended; QUALITY 33. Shown able to fail: `corpus/evidence/round32/q33-check.py` prints FAIL (exit 1) on the round-31 lesson at `4111607c` and PASS (exit 0) after the correction. (The first draft check, `w1/ScribeQualityR1/quality.md`, failed on both texts and could not show the fix; CriticMistakes32) |
| A counter checked final bytes but not whether the lock covered the write, so a probe-only lock met C1 v1 | `w1/CtlC1PartialLockB/b-s32471021.json` 24/24 | the pre-data control wave (round prompt Correction rule) — before any candidate | design v2 (strace write delay); QUALITY 34. Shown able to fail: the same control (gate `034f786b…`) scores 0/24 under v2 (`w1/CtlC1PartialLockB/v2/mutated-b-probe-only-s3247202{1,2}.json`) |
| A counter de-duplicated findings and ignored the record verdict, so wrong output met C2 v1 | `w1/MutC2CounterB/frozen-duplicate-finding-*` 120/120; `w1/CtlC2NoisyB` duplicate-only 120/120 | existing QUALITY 19 (negative controls must reject wrong exits and absent verdict records) and 20 (finding multiplicity; "a code-set comparison cannot detect invented duplicate occurrences") should have caught it before v1 froze; the control wave caught it (CriticMistakes32) | design v2 (counted findings, record checks). Shown able to fail: duplicate-only scores 96/132 under v2 (`controls/L1-design-v2/c2-dup-s322{1,2}.json`) |
| Control gates scored in a flat scratch layout put the out-of-corpus fixture inside the gate's lane root; the L1 also kept four "weak-reader" receipts whose gate bytes had been restored to the base | `w1/CtlC2StatusBlindB.md`, `w1/CtlC2WeakReaderB.md` (E7 0/6 flat); the four L1 receipts carried `gate_sha256` `0bc318b3` and were deleted before commit | none | v2 layout guard; QUALITY 35. Shown able to fail: `C2_TMP` inside the gate's lane root → exit 2 |

## Gate

New source rows, opened by ScribeSourceC1 / ScribeSourceC2 and re-opened by the L1 (same body
SHA-256, quote found once with `grep -cF`):

- S060 — https://docs.python.org/3/library/fcntl.html, accessed 2026-10-23, HTTP 200, sha256
  `025727ff…3dda3` (06:37 UTC footer build; a 07:26 re-GET differs only in that footer line,
  `0189dd49…1e56`, ReopenS060). Quotes: "Perform the lock operation operation on file descriptor
  fd" (`fcntl.flock`; found once in the tag-stripped body) and "Acquire an exclusive lock."
  (`LOCK_EX`, listed under `fcntl.lockf`'s cmd values). Admitted tier A for the call shape only.
  Corrected in-round after ReopenS060: the first row text read the `LOCK_EX` quote as part of
  `fcntl.flock` and did not mark the flock(1) link as inference.
- S061 — https://www.rfc-editor.org/rfc/rfc9110.txt, accessed 2026-10-23, HTTP 200, sha256
  `21c1cdce…47232a`. Quote (§15.5.11): "resource is no longer available at the origin server".
  Admitted tier A for origin-server semantics only; the local-audit rule is lane design.
  Corrected in-round after ReopenS061: the first `teaches` cell and the knowledge entry stated the
  "one access path" reading as the RFC's; it is now marked as lane inference.

Status / recheck / used-by changes: none to existing rows (S001–S059 untouched).

Rejects (real, with reason):

- Design v1 counters (`c1-count.py`, `c2-count.py`): rejected as P1/P2 counters because controls met
  them (above); kept as evidence, not counted.
- Four L1 receipts named case-insensitive / whitespace-collapse / grep-anywhere / file-only under
  `controls/L1-design-v2/`: rejected and deleted before commit — their `gate_sha256` was the base
  gate, because the seat had restored its scratch gates; the seats' own re-scores with the mutated
  bytes are the evidence.
- MutC2CounterB's first stance ("counter guard deletions prohibited"): rejected by the L1; the item
  allowed mutated scratch copies, and the seat ran them.
- Not opened: `https://en.wikipedia.org/wiki/Link_rot` (lower tier than RFC 9110 for the same point);
  `https://docs.python.org/3/library/os.html` (O_APPEND is not a fact either claim needs).

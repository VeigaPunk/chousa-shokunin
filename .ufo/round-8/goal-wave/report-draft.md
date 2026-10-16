# chousa — round 8: the gate's own behavioral baseline — `--pin`/`--drift` (freshness/operability move)

<!-- SCRIBE DRAFT — MEASURED FINAL. Before: gate sha256
     3ba718bf9207eed70c66b8c849ac43b44c76890785e1576eeb5e795a604166b2
     (== lane HEAD `848738c` round-7 records; `git diff tools/research-gate.sh`
     EMPTY and sha re-verified at 03:21:20Z). After: gate sha256
     46f5ddb39d5fafa220fb584121dba2f4a15e071a91fa42728849f3c7567c6ccd
     (`git diff --numstat` = 523 +, 6 −; 4183 lines; stable ≥2 min before the
     battery and sha identical before and after it; the revision moved through
     ~10 hashes during the wave — the note's §1 records the sequence).
     Lane HEAD still `848738c`; no commits by any seat. Scribe scratch
     $HOME/.cache/chousa-tmp/scribe-r8/ (declared ephemeral, cleaned at end of
     run). [PARENT] markers mark parent-only bindings. The Debt section keeps
     receipt identity OPEN per the mission contract. -->

Status: **DRAFT — measured, awaiting parent integration/admission**. Baseline:
lane HEAD `848738c` (round-7 records). Wave: one 32-seat flash call. Report
time: 2026-10-16 ~03:50Z.

## Work performed

- Round 8 selects the move round 7 registered: **the gate's own behavioral
  baseline** — `--pin`/`--drift`, adapted from the sibling lane mori's proven
  r10 pattern (read-only lineage: `../mori-shokunin/corpus/knowledge/drift-pin-r10.md`,
  `../mori-shokunin/corpus/lessons/2026-10-15-volatile-contract-behavioral-baselines.md`).
  Before it, a gate regression (a mode silently skipped, an output field
  changed) was only catchable by reading a previous round's receipts and
  comparing by hand; no baseline artifact existed.
- The move (measured contract): `--pin <path>` runs a hermetic canonical
  invocation, normalizes it with a declared volatile contract, and writes a
  baseline text file (`GATE_PIN: ok`, exit 0 — pinning a DRIFT-rolling run is
  still a pin); `--drift <path>` re-runs the same invocation and byte-compares
  — `GATE_DRIFT: none` exit 0 / `GATE_DRIFT: <changed tokens>` exit 1 /
  missing-unreadable-malformed or failed capture exit 2; the lane baseline is
  committed under `corpus/evidence/` with a re-run recipe; all 74 prior
  selftest cases byte-stable; hermetic reproducibility; zero network.
- Scribe independent work: the before-state battery at the current gate; the
  full after-state battery at the settled revision (pin/drift contract, churn
  and clock holds, three mutants + a comment-only control, the whole
  malformed/setup battery, the committed-baseline drift, all-mode
  regressions, the r1 observable, strace); this draft set.

## Before-state (MEASURED at `3ba718bf…`, lane HEAD `848738c`)

```text
$ git diff tools/research-gate.sh                    → EMPTY
$ sha256sum tools/research-gate.sh                   → 3ba718bf9207eed70c66b8c849ac43b44c76890785e1576eeb5e795a604166b2
$ bash tools/research-gate.sh --pin /tmp/nope.txt    → research-gate: unknown flag: --pin   exit=2 (usage; no file written)
$ bash tools/research-gate.sh --drift /tmp/nope.txt  → research-gate: unknown flag: --drift exit=2 (usage; no file written)
$ grep -c 'GATE_PIN\|GATE_DRIFT\|--pin\|--drift' tools/research-gate.sh → 0
$ bash tools/research-gate.sh --selftest             → RESEARCH_GATE_SELFTEST: PASS (74 cases) exit=0
  case lines 1–74 `cmp`-byte-identical to the r7 receipt
  (corpus/evidence/integrity-r7-20261016T030552Z-selftest.log)
$ ls corpus/evidence/ | grep -i baseline             → (none committed)
```

The hole, exactly: with no baseline artifact and no drift mode, noticing that
the gate's own behavior changed between revisions means reading an older
round's receipts and comparing by hand; nothing in the lane compared gate
behavior over time.

## The move (MEASURED at gate `46f5ddb3…`, +523/−6)

Contract (declared in the file header `:153` ff.; usage `:266`, `:316`; the
note `corpus/knowledge/gate-baseline-r8.md` is the full design record):

- **`--pin <path>`** (`run_pin` `:2410`): runs the canonical capture, writes
  `GATE_PIN: ok path=… gate_sha256=…`, exit 0; exit 2 when the capture or the
  write fails (measured: unwritable path → exit 2). Pinning a run that itself
  rolls DRIFT is still a pin — the canonical fixture deliberately contains a
  dangling sweep binding (`C9`), so the capture covers both CLEAN sections and
  a DRIFT section/finding/composed verdict.
- **`--drift <path>`** (`run_drift` `:2446`): re-runs the capture, normalizes
  with the CURRENT rules, byte-compares; writes nothing; never prints a
  `RESEARCH_GATE:` line.
- **Canonical invocation** (hermetic): `verify-all record.md --claims claims.jsonl
  --json manifest.jsonl --root .` inside a fresh temp fixture the gate writes
  and removes itself (`gate_pin_fixture` `:2220`, `gate_canonical_capture`
  `:2270`); every printed path is relative, so the capture is byte-stable
  wherever the gate runs.
- **Volatile contract**: `GATE_DRIFT_VOLATILE_FIELDS='ts gate_sha256'`
  (`:2199`), recorded verbatim in every baseline header; `ts` is shape-scoped
  (`ts=<ISO>` / `"ts":"…"` → `<V>`), so a malformed timestamp keeps its bytes
  and surfaces. Everything else is compared unmasked, including
  `record_sha256` (fixture bytes are behavior).
- **Guards**: `--pin`/`--drift` accept only a baseline path (`--record`/
  `--claims`/`--json`/`--root` → usage exit 2); both at once → exit 2.
- **Selftest**: 74 → 85 cases (+11: cases 75–85 `:4055-4089`); cases 1–74
  keep numbers, names and exits.

## Measurements after the move (gate `46f5ddb3…`; sha identical before and
after the whole battery; fresh processes; verbatim)

```text
$ bash tools/research-gate.sh --selftest  → RESEARCH_GATE_SELFTEST: PASS (85 cases) exit=0
  case lines 1–74 `cmp`-byte-identical to the before-state capture; new cases:
  75 pin-clean 0 · 76 drift-clean 0 · 77 drift-volatile-churn 0 · 78 drift-one-field-mutant 1 ·
  79 drift-missing 2 · 80 drift-malformed 2 · 81 drift-volatile-list 1 ·
  82 setup-pin-no-path 2 · 83 setup-drift-no-path 2 · 84 setup-pin-unwritable 2 · 85 setup-pin-drift-exclusive 2

$ bash tools/research-gate.sh --pin <scratch>/base.txt
  → GATE_PIN: ok path=… gate_sha256=46f5ddb39d5faf… exit=0
  baseline: 2988 B, 19 lines; header declares
  # canonical: verify-all record.md --claims claims.jsonl --json manifest.jsonl --root . (cwd = a fresh temp fixture written by the gate)
  # volatile_fields=ts gate_sha256
  body: 5 SECTION lines (4 CLEAN + integrity DRIFT), 1 FINDING REF_UNRESOLVED severity=warn … C9 …,
  VERIFY_ALL sections=5 run=5 absent=0 drift-sections=1 findings=1 drift=1,
  RESEARCH_GATE: DRIFT (…) — and the masked --json manifest line.
  hermeticity: two independent pins at this revision (this seat 03:38Z; the committed
  artifact 03:38:57Z) have BYTE-IDENTICAL canonical bodies; the files differ only in `# pinned_ts=`.

$ bash tools/research-gate.sh --drift <scratch>/base.txt        → GATE_DRIFT: none exit=0
$ … same command 65 s later (live churn)                        → GATE_DRIFT: none exit=0
$ CHOUSA_NOW_EPOCH=1792500000 bash tools/research-gate.sh --drift <scratch>/base.txt
  → GATE_DRIFT: none exit=0   (clock ~2.6 days ahead; the ts mask absorbs it)

mutants (each a scratch copy of the settled gate; --drift against the same baseline):
  VA_ORDER drops `chain` (mode silently skipped)
    → GATE_DRIFT: -SECTION:chain -anchor-missing drift exempt findings invalid name native refused
      run sections sections_run state tallies verdict verified        exit=1
    the mutant's own --selftest: FAIL (8/85 cases) — the selftest also names it
  severity=warn → severity=mild in the REF finding
    → GATE_DRIFT: drift severity  (severity drives the drift tallies; both keys named)  exit=1
    the mutant's own --selftest: FAIL (6/85 cases)
  VERSION research-gate-r1 → r2 (banner word; no key=value change)
    → GATE_DRIFT: GATE  (line-id fallback)  exit=1
    the mutant's own --selftest: PASS (85 cases) — the selftest TOLERATES this class;
    the drift pin names it.
  comment-only edit (different sha `289a8f9b…`, identical behavior)
    → GATE_DRIFT: none exit=0 — behavioral, not revision-bound.
  usage-text edit (line 316 wording; outside the canonical demonstration path)
    → GATE_DRIFT: none exit=0 — MEASURED BLIND SPOT (named below).

baseline battery (all exit 2 unless stated):
  missing path → `--drift baseline missing` · empty and junk → `malformed (magic line absent)` ·
  no canonical marker → `malformed (canonical marker absent)` · no volatile_fields →
  `malformed (volatile_fields contract absent)` · proper header + empty body → `malformed (empty canonical block)` ·
  mode-000 → `baseline unreadable` · volatile list rewritten (`ts gate_sha256` → `ts`) →
  GATE_DRIFT: volatile_fields exit=1 · `--pin` to an unwritable path → exit=2 ·
  `--pin X --drift Y` → `mutually exclusive` exit=2.

committed lane baseline corpus/evidence/gate-baseline-r8-20261016T033757Z.json
  (2988 B, sha256 1c81a6cb34543bb99c8797a7a0dd8dfbd1f13e3d86ec5b81aa0c7249381a8426;
  header gate_sha256=46f5ddb3…, pinned_ts=2026-10-16T03:38:57Z)
  → bash tools/research-gate.sh --drift corpus/evidence/gate-baseline-r8-20261016T033757Z.json
    → GATE_DRIFT: none exit=0

regressions (all held at the settled revision):
  verify-claims claims-r2.jsonl        → VERDICT_BEARING_CLAIMS=17/17 CLEAN exit=0
  verify-chain chain-r3.md             → RESOLVED_HOPS=17/22 CLEAN exit=0
  verify-chain chain-r3-broken.md      → RESOLVED_HOPS=1/2 DRIFT exit=1
  verify-sweeps sweeps-r5.md           → VERIFIED_SWEEPS=1/2 REJECTIONS_OK=3/3 CLEAN exit=0
  verify-sweeps sweeps-r5-broken.md    → VERIFIED_SWEEPS=0/1 REJECTIONS_OK=0/1 DRIFT exit=1
  verify-integrity integrity-r7.md     → INTEGRITY refs=16 resolved=15 unresolved=0 CLEAN exit=0
  verify-integrity integrity-r7-broken.md → INTEGRITY refs=16 resolved=13 unresolved=2 DRIFT exit=1
  verify-all full-r6.md                → CLEAN sections=5 run=5 exit=0
  verify-all full-r6-broken.md         → DRIFT drift-sections=2 exit=1
  verify-all full-r6-absent.md         → CLEAN sections=5 run=4 absent=1 exit=0
  verify-all integrity-r7.md           → CLEAN run=5 exit=0 · -broken.md → DRIFT drift-sections=1 exit=1
  r1 archives A/B/C                    → each exit=1 with exactly one RESEARCH_GATE: DRIFT line (3/3)

zero network:
  strace -f -e trace=network, drift run → 0 network lines of 3754; GATE_DRIFT: none exit=0
  strace -f -e trace=network, pin run   → 0 network lines of 3759; GATE_PIN: ok exit=0
```

## Landed changes (uncommitted, at draft time)

- `tools/research-gate.sh` → sha256 `46f5ddb3…` (+523/−6; 4183 lines): the
  pin/drift section (header `:153`, usage `:266`/`:316`, constants `:2199`,
  normalize `:2209`, fixture `:2220`, capture `:2270`, line-id `:2307`, scan
  `:2321`, field report `:2342`, report `:2365`, `run_pin` `:2410`, `run_drift`
  `:2446`), the `--pin`/`--drift` guards (`:4144-4146`), dispatch (`:4156-4157`),
  selftest cases `:4055-4089`; the −6 are the EXIT-trap comment rewritten to
  sweep `GATE_CAP_DIR` and the `--root` assignment gaining `ROOT_ARG_SET`
  for the fail-closed flag discipline. Banner still `research-gate-r1`
  (cosmetic — now drift-visible: the banner-word mutant reads `GATE_DRIFT: GATE`).
- Committed lane baseline `corpus/evidence/gate-baseline-r8-20261016T033757Z.json`
  (sha256 `1c81a6cb…`; the re-run recipe is in the note §5 / SKILL row).
- Receipts `corpus/evidence/pin-r8-20261016T033757Z-{pin,drift,live,selftest}.log`
  (sha256 `40abd23d…`, `051695ee…`, `9829ed10…`, `6334240b…`).
- Note `corpus/knowledge/gate-baseline-r8.md` (18454 B, sha256 `d7370ecf…`);
  lesson `corpus/lessons/2026-10-16-gate-behavioral-baseline.md` (19512 B,
  `9c906ad8…`); `SKILL.md` (`a358cdd2…`: all gate rows → `PASS (85 cases)`,
  new `research-gate --pin / --drift` row with the committed baseline).
- `corpus/evidence/README.md` (`685efae8…`: "rounds 2-8" header + the
  round-8 gate-baseline receipts section).
- [PARENT: `corpus/README.md` row not landed by ~03:46Z when this seat last
  checked; integrate only what lands.]

## Named limits (measured by this seat; the note carries the full inventory)

- **Masked set is two fields, and it is a blind spot by construction.** `ts`
  is shape-scoped (a malformed timestamp surfaces; the note measured a
  `ts=epoch-…` mutant → `GATE_DRIFT: ts`), `gate_sha256` is deliberately not
  compared. A regression that changes only masked values reads `none`.
- **Outside-path edits are invisible: measured.** A usage-text edit (line 316)
  reads `GATE_DRIFT: none` exit 0 — the canonical invocation never prints the
  usage, so any edit outside the demonstrated path (usage/help text, dead
  branches) is not seen by the pin. Named here, not hidden.
- **The pin's added power over the selftest, measured:** the two regression
  classes the round names are ALSO caught by the selftest (chain-skip → FAIL
  8/85; severity field → FAIL 6/85). The drift pin's measured extra reach:
  it names the class the selftest tolerates (banner word → PASS 85/85, pin
  `GATE` exit 1), it names which fields moved without a case list, and it is a
  durable committed artifact with a declared contract — a comparison that did
  not exist. The honest statement is complement, not replacement.
- **`none` means "no unmasked change", not "output identical"** (the mask);
  the masked set travels in every baseline header so a reader can audit what
  the `none` did not look at.
- **Baseline aging / re-pin policy.** The canonical capture is hermetic (no
  fleet state, no lane files), so aging is small — but the volatile contract
  itself is compared (a baseline whose declared list differs reads
  `volatile_fields` exit 1) and re-pinning must stay a recorded act with a
  reason, never a way to make red green (mori's rule; the note carries the
  full ritual).
- **Nested execution cost (carried).** A pin or drift run performs one full
  composed verify-all (5 sections as fresh solo calls) plus the manifest
  write; measured wall ~2–3 s per leg on this host at wave load.
- Canonical fixture deliberately rolls DRIFT (one dangling `claim_id=C9`) so
  the capture covers both CLEAN and DRIFT output shapes; pinning it is exit 0
  by design.

## Admission

[PARENT: ADMIT/REJECT line + commit hashes; no scalar; axis verdicts live in
SCORECARD.md's round-8 sections.]

## Debt

- **Receipt identity (round 1): STILL OPEN.** No authentic queue
  taskKey/expected receipt bag exists; mission acceptance is integrator-owned;
  no `task_…` value was invented, no shape-only receipt counted, proven
  receipt-backed completed rounds remain 0, operator target unchanged (≥100).
  Routing for this wave was satisfied by the operator's in-session direct
  dispatch; no Sighting step was invoked. Round-8 artifacts are lane evidence,
  not a mission receipt.
- Carried (unchanged by this round): absent!=drift omission limit (r6);
  non-vacuous flip screening (r5); id-shape boundary (r7); manifest schema
  growth; nested execution cost; non-author spot-check (integrator/operator);
  carried residuals (in-root hardlinks, no source size cap, token-aligned
  shortening, non-ASCII-adjacent fail-closed edges, scope-refusal finding IDs,
  frozen-replay comparator).
- New after round 8: the usage/outside-path blind spot (measured); the masked-
  set blind spots (named, contract travels in the artifact); the re-pin policy
  as a standing ritual.

## SHONEN

[PARENT: all four `[ ]` unless a named non-author verifier is bound this
round.]

Boundaries held: zero network (strace on both pin and drift legs); corpus
read-only; `--pin` wrote only the paths it was given; `--drift` zero writes;
seats wrote only in owned paths; no commits by seats.
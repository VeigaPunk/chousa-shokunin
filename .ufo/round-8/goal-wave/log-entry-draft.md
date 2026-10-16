# LOG.md — round-8 entry draft (parent-owned file; integrate under [PARENT] markers)

<!-- SCRIBE DRAFT — MEASURED FINAL. Before: gate sha256
     3ba718bf9207eed70c66b8c849ac43b44c76890785e1576eeb5e795a604166b2
     (== lane HEAD `848738c` round-7 records; `git diff tools/research-gate.sh`
     EMPTY, sha re-verified at 03:21:20Z). After: gate sha256
     46f5ddb39d5fafa220fb584121dba2f4a15e071a91fa42728849f3c7567c6ccd
     (+523/−6; stable ≥2 min before the battery, sha identical before and
     after it; the revision moved through ~10 hashes during the wave — the
     note's §1 records the sequence). Lane HEAD still `848738c`; no commits by
     any seat. Scribe scratch $HOME/.cache/chousa-tmp/scribe-r8/ (declared
     ephemeral, cleaned at end of run). [PARENT] marks parent-only bindings.
     The debts section keeps the receipt-identity debt OPEN per the mission
     contract. -->

## 2026-10-16 — round-8 freshness/operability: the gate's own behavioral baseline (`--pin`/`--drift`)

Round 8 executes the move round 7 registered: the verification tool's own
drift becomes detectable. Before it, a gate regression — a mode silently
skipped, an output field changed — could only be caught by reading a
previous round's receipts and comparing by hand; nothing in the lane
compared gate behavior over time, and no baseline artifact existed. The
pattern is adapted from the sibling lane mori's proven r10 pin/drift design
(read-only lineage: `../mori-shokunin/corpus/knowledge/drift-pin-r10.md`,
`../mori-shokunin/corpus/lessons/2026-10-15-volatile-contract-behavioral-baselines.md`).
The operator dispatched this wave directly in-session (same routing as
rounds 2–7; **no Sighting step was invoked**); receipt identity from round 1
remains open and untouched by this round.

**Before (MEASURED at gate `3ba718bf…`, lane HEAD `848738c`):**

```text
$ git diff tools/research-gate.sh                    → EMPTY; sha256 3ba718bf…
$ bash tools/research-gate.sh --pin /tmp/nope.txt    → research-gate: unknown flag: --pin;   exit=2, no file written
$ bash tools/research-gate.sh --drift /tmp/nope.txt  → research-gate: unknown flag: --drift; exit=2, no file written
$ grep -c 'GATE_PIN\|GATE_DRIFT\|--pin\|--drift' tools/research-gate.sh → 0
$ bash tools/research-gate.sh --selftest             → RESEARCH_GATE_SELFTEST: PASS (74 cases); exit=0
  case lines 1–74 `cmp`-byte-identical to the r7 receipt (integrity-r7-20261016T030552Z-selftest.log)
$ ls corpus/evidence/ | grep -i baseline             → (none committed)
```

**The move.** `tools/research-gate.sh` (uncommitted, +523/−6 vs HEAD, gate
`46f5ddb3…`): `--pin <path>` (`run_pin` `:2410`) runs the canonical hermetic
capture — `verify-all record.md --claims claims.jsonl --json manifest.jsonl
--root .` inside a fresh temp fixture the gate writes and removes itself
(`gate_pin_fixture` `:2220`, `gate_canonical_capture` `:2270`; every printed
path relative, so the capture is byte-stable wherever the gate runs) —
normalizes it under the declared volatile contract
(`GATE_DRIFT_VOLATILE_FIELDS='ts gate_sha256'` `:2199`; `ts` shape-scoped so
a malformed timestamp keeps its bytes and surfaces), and writes a text
baseline whose header records the magic, the gate sha, `pinned_ts`, the
canonical invocation and the volatile list; prints `GATE_PIN: ok path=…
gate_sha256=…`, exit 0 — pinning a DRIFT-rolling run is still a pin (the
fixture deliberately carries one dangling sweep binding `C9`, so the capture
covers CLEAN sections, a DRIFT section/finding, the composed verdict and the
masked manifest line). `--drift <path>` (`run_drift` `:2446`) re-runs the
same capture, normalizes with the CURRENT rules, byte-compares: equal →
`GATE_DRIFT: none` exit 0; differ → `GATE_DRIFT: <LC_ALL=C-sorted tokens>`
exit 1 (changed `key`s, `-key`/`+key`, line ids like `-SECTION:chain` /
`FINDING:<id>` / `GATE` / `MANIFEST` when a difference lives outside
key=value tokens, `output-order` for a pure reorder, and `volatile_fields`
when the baseline's declared list differs from the current one); baseline
missing/unreadable/malformed (magic, canonical marker, volatile contract,
empty body) or a failed capture → distinct message, exit 2, never a false
`none`. Neither mode prints a `RESEARCH_GATE:` line. Guards: any
record/claims/`--json`/`--root` argument → usage exit 2; both modes at once →
exit 2 (`:4144-4146`). Selftest 74 → 85 (+11: cases 75–85 `:4055-4089`);
cases 1–74 keep numbers, names and exits. The −6 are the EXIT-trap comment
rewritten to sweep `GATE_CAP_DIR` (a capture that dies mid-flight) and the
`--root` assignment gaining `ROOT_ARG_SET` for the fail-closed flag
discipline.

**Measurements after the move** (gate `46f5ddb3…`; stable ≥2 min, sha
identical before/after the battery; fresh processes; verbatim):

```text
$ bash tools/research-gate.sh --selftest  → RESEARCH_GATE_SELFTEST: PASS (85 cases) exit=0
  case lines 1–74 `cmp`-byte-identical to the before capture; new cases 75–85:
  pin-clean 0 · drift-clean 0 · drift-volatile-churn 0 · drift-one-field-mutant 1 ·
  drift-missing 2 · drift-malformed 2 · drift-volatile-list 1 ·
  setup-pin-no-path 2 · setup-drift-no-path 2 · setup-pin-unwritable 2 · setup-pin-drift-exclusive 2

$ bash tools/research-gate.sh --pin <scratch>/base.txt  → GATE_PIN: ok path=… gate_sha256=46f5ddb3… exit=0
  baseline 2988 B / 19 lines; header: canonical invocation + `volatile_fields=ts gate_sha256`;
  body: 4×SECTION CLEAN + SECTION integrity DRIFT + FINDING REF_UNRESOLVED (C9) +
  VERIFY_ALL sections=5 run=5 absent=0 drift-sections=1 findings=1 drift=1 +
  RESEARCH_GATE: DRIFT + masked manifest line.
  hermeticity: two independent pins at this revision (03:38Z this seat; 03:38:57Z committed)
  have BYTE-IDENTICAL canonical bodies; files differ only in `# pinned_ts=`.

$ --drift <scratch>/base.txt          → GATE_DRIFT: none exit=0
$ … same command 65 s later (churn)   → GATE_DRIFT: none exit=0
$ CHOUSA_NOW_EPOCH=1792500000 --drift <scratch>/base.txt → GATE_DRIFT: none exit=0  (clock +2.6 d)

mutants (scratch copies of the settled gate, --drift against the same baseline):
  VA_ORDER drops `chain` (mode silently skipped) → GATE_DRIFT: -SECTION:chain -anchor-missing drift exempt
    findings invalid name native refused run sections sections_run state tallies verdict verified  exit=1
    (its own selftest: FAIL 8/85 — the selftest catches this class too)
  severity=warn → mild in the REF finding → GATE_DRIFT: drift severity exit=1
    (its own selftest: FAIL 6/85)
  VERSION research-gate-r1 → r2 (banner word) → GATE_DRIFT: GATE exit=1
    (its own selftest: PASS 85/85 — the selftest TOLERATES this class; the pin names it)
  comment-only edit (different sha 289a8f9b…, identical behavior) → GATE_DRIFT: none exit=0
  usage-text edit (line 316, outside the canonical demonstration path) → GATE_DRIFT: none exit=0
    (measured blind spot, named)

baseline battery (all exit 2 unless stated): missing → `baseline missing` · empty/junk →
  `malformed (magic line absent)` · no marker → `malformed (canonical marker absent)` ·
  no volatile_fields → `malformed (volatile_fields contract absent)` · proper header + empty body →
  `malformed (empty canonical block)` · mode-000 → `unreadable` · volatile list rewritten →
  GATE_DRIFT: volatile_fields exit=1 · pin unwritable → exit=2 · pin+drift → exit=2 (`mutually exclusive`).

committed lane baseline corpus/evidence/gate-baseline-r8-20261016T033757Z.json
  (2988 B; sha256 1c81a6cb34543bb99c8797a7a0dd8dfbd1f13e3d86ec5b81aa0c7249381a8426;
  header gate_sha256=46f5ddb3…, pinned_ts=2026-10-16T03:38:57Z)
  → --drift → GATE_DRIFT: none exit=0

regressions at the settled revision:
  claims 17/17 CLEAN 0 · chain 17/22 CLEAN 0 + broken 1/2 DRIFT 1 ·
  sweeps 1/2+3/3 CLEAN 0 + broken 0/1+0/1 DRIFT 1 · integrity 16/15/0 CLEAN 0 + broken 16/13/2 DRIFT 1 ·
  full-r6 CLEAN run=5 / broken DRIFT drift-sections=2 / absent CLEAN run=4 absent=1 ·
  integrity pair as r7 · r1 archives A/B/C each exit 1 with exactly one DRIFT line (3/3)

zero network: strace -f -e trace=network → drift: 0 network lines of 3754 (GATE_DRIFT: none exit=0);
  pin: 0 network lines of 3759 (GATE_PIN: ok exit=0)
```

**Named limits (measured by this seat).** Masked-set blind spots: `ts`
(shape-scoped — a malformed timestamp surfaces) and `gate_sha256` (revision,
deliberately not compared); a regression that changes only masked values
reads `none`, and the contract travels in every baseline header (the reader
can audit the blind spot). The usage/outside-path blind spot is measured: a
usage-text edit reads `GATE_DRIFT: none` exit 0 because the canonical
invocation never prints the usage. The pin's added power over the selftest is
partial and measured: chain-skip (FAIL 8/85) and the severity field (FAIL
6/85) are caught by both, while the banner word — selftest PASS 85/85 — is
named by the pin (`GATE` exit 1); complement, not replacement. Baseline
aging: the canonical capture is hermetic, so aging is small; re-pinning stays
a recorded act with a reason (never to make red green). Nested execution
cost carried (each leg runs one composed verify-all, ~2–3 s wall). The banner
still reads `research-gate-r1` — now drift-visible.

**Admission.** [PARENT: ADMIT/REJECT line + commit hashes; no scalar; axis
verdicts live in SCORECARD.md's round-8 sections.]

**Debt.** Receipt identity (round 1) STILL OPEN — no authentic queue
taskKey/expected receipt bag exists; mission acceptance is integrator-owned,
no `task_…` value was invented, proven receipt-backed completed rounds remain
0, operator target unchanged (≥100). Round-8 artifacts at draft time
(uncommitted): gate `46f5ddb3…` (+523/−6), committed lane baseline
`1c81a6cb…` (receipts-writer), receipts `pin-r8-20261016T033757Z-*` shas
`40abd23d…`/`051695ee…`/`9829ed10…`/`6334240b…`, note
`corpus/knowledge/gate-baseline-r8.md` (`d7370ecf…`), lesson
`corpus/lessons/2026-10-16-gate-behavioral-baseline.md` (`9c906ad8…`),
`SKILL.md` r8 rows (`a358cdd2…`), `corpus/evidence/README.md` (`685efae8…`)
[PARENT: `corpus/README.md` row — not landed
by this seat's last check; integrate only what lands]. Carried debts:
absent!=drift omission limit (r6); non-vacuous flip screening (r5); id-shape
boundary (r7); manifest schema growth; nested execution cost; non-author
spot-check (integrator/operator); carried residuals (in-root hardlinks, no
source size cap, token-aligned shortening, non-ASCII-adjacent fail-closed
edges, scope-refusal finding IDs, frozen-replay comparator). New after round
8: the usage/outside-path blind spot; the masked-set blind spots; the re-pin
policy as a standing ritual. Lane hygiene: no commits by seats.
# Round-2 lesson — span fidelity is not claim truth: the unchecked label (2026-10-15)

Round: chousa-shokunin round 2, one coverage move: `verify-claims` — claim-vs-source
verification. Lane HEAD `6344569` (unchanged since round-1 publication;
`git log --oneline -1`). All measurements below were taken 2026-10-15 from the
lane cwd against the working tree, which carries the uncommitted round-2 change
(`git status --short`: ` M tools/research-gate.sh`) plus the untracked
`corpus/fixtures/`. Gate revision under test:
`tools/research-gate.sh` sha256
`03a3324455852ea0025115cb0e3ba9c8cdea10da5edc051c4738854a27c14be0`
(mode `claims` at `:710-859`, dispatch `:1465` and `:1486` of that revision).
Fixture under test: `corpus/fixtures/claims-r2.jsonl` sha256
`23d078cbfd032ec5ee7de5c21de65eba3a3cd2989a78281ff61bc6db62188802`, contract in
`corpus/fixtures/claims-r2.README.md`. Raw probe outputs:
`/var/tmp/lessons-distiller/battery3.log` (seat scratch; `/tmp` was unusable
mid-wave — its tmpfs carries `usrquota` and the shared user quota filled with
concurrent seats' scratch, so several early captures were empty files and were
re-run under `/var/tmp`).

## Pre-registration, re-derived

The fixture is pre-registered, not fitted: the file existed at 20:14 local while
`tools/research-gate.sh` still carried its round-1 sha256 `0884355…` (baseline
capture plus a re-check when the fixture appeared); the gate then changed
repeatedly — ≥11 distinct revision shas observed 20:15–20:25 — before
stabilizing at `03a33244…`. Before the implementation was
read, this seat independently re-derived every fixture span by exact substring
against the three read-only archives (`../research/deep-research-2026-09-28/`,
sha256s `9033857d…`, `6d8dbddd…`, `e48fe70f…` matching
`corpus/evidence/round-1/expected.json`): 13 supported spans present verbatim,
2 contradicted spans present with their markers, 2 unsupported spans absent from
the whole corpus — `counts: {'supported': 13, 'contradicted': 2,
'unsupported': 2} total: 17 -> ALL_OK`. The fixture's provenance holds
independently of the checker.

## Observation — the mode, and the probe

Real CLI, clean fixture (exit 0, one verdict line):

```text
$ bash tools/research-gate.sh verify-claims corpus/fixtures/claims-r2.jsonl --root ..
VERDICT_BEARING_CLAIMS=17/17
RESEARCH_GATE: CLEAN (claims=17 supported=13 contradicted=2 unsupported=2 mismatched=0 unproven=0 refused=0 invalid=0 findings=0 drift=0)
```

At the measured revision the mode reads only `id`, `source`, `span`, `expect`
and `marker` from each claim line (`:746-750`); the `claim` field is never
extracted. The probe turns that into an executable fact — a claims file whose
`claim` prose asserts the direct **opposite** of its own byte-exact span:

```json
{"id": "A05", "claim": "Export A confirms jin'i-ryū is an established artisan rank.", "source": "research/deep-research-2026-09-28/A-shokunin-tradition.md", "span": "I could not substantiate this spelling as an established artisan rank in the Japanese or English sources searched.", "expect": "supported"}
{"id": "A01", "claim": "Export A names earned responsibility within a craft, followed by lifelong refinement and transmission, as the strongest historical model for the roster.", "source": "research/deep-research-2026-09-28/A-shokunin-tradition.md", "span": "The strongest historical model for your roster is “earned responsibility within a craft, followed by lifelong refinement and transmission.”", "expect": "supported"}
```

```text
$ bash tools/research-gate.sh verify-claims <probe>.jsonl --root ..   # exit 0
CLAIM id=A05 expected=supported observed=supported source=research/deep-research-2026-09-28/A-shokunin-tradition.md at=line:64 verdict=match
CLAIM id=A01 expected=supported observed=supported source=research/deep-research-2026-09-28/A-shokunin-tradition.md at=line:52 verdict=match
VERDICT_BEARING_CLAIMS=2/2
RESEARCH_GATE: CLEAN (claims=2 supported=2 contradicted=0 unsupported=0 mismatched=0 unproven=0 refused=0 invalid=0 findings=0 drift=0)
```

The span is real (A:64 says the spelling was *not* substantiated); the label is
false; the run is CLEAN and nothing in the output can distinguish this case from
a label that matches. Adjacent mechanics measured the same way:

- A supported span altered by one character: `observed=unsupported`,
  `verdict=mismatch`, `CLAIM_SPAN_NOT_FOUND`, exit 1 (`VERDICT_BEARING_CLAIMS=0/1`).
- A span real in A but cited against B: `observed=unsupported`, drift — the
  check is source-specific, not corpus-wide.
- A `contradicted` entry with its marker removed: `observed=unproven`,
  `FINDING CONTRADICTION_MARKER_ABSENT severity=warn`, `16/17`, exit 1. The
  `contradicted` arm is a declared literal co-occurring inside the span's lines
  (`:796-808`), not negation inference; `verdict=match` on such an entry means
  "marker found", nothing more.
- `expect=unsupported` with the span present: `CLAIM_SPAN_UNEXPECTED`, drift.

## Bounds measured this round

- **Fail-closed source boundary.** A citation to `/etc/hostname` and a
  traversal citation `../../../../etc/hostname` (resolving to the same file)
  both refuse before any read:
  `CLAIM id=X3 … observed=refused` /
  `FINDING CLAIM_SOURCE_OUT_OF_CORPUS severity=crit … obs=resolved=/etc/hostname outside allowed roots`,
  exit 1. `strace -f -e trace=openat` over both refusal runs (9777 and 9779
  trace bytes): **0 opens** of `/etc/hostname` in either. URL sources →
  `CLAIM_SOURCE_EXTERNAL severity=crit`, session paths →
  `CLAIM_SOURCE_SESSION severity=crit` (path printed, never opened),
  ephemeral → `CLAIM_SOURCE_EPHEMERAL warn`, malformed line →
  `CLAIM_RECORD_INVALID warn`.
- **No-fetch bound.** `strace -f -e trace=network` over the clean fixture run
  (66281 trace bytes): **0** `socket(`/`connect(` calls.
- **Round-1 behavior byte-stable.** `verify` on A/B/C (exit 1) and the intake
  note (exit 0) is byte-identical to outputs captured before the gate changed
  (same pinned `CHOUSA_NOW_EPOCH`, `cmp` clean for all four). Selftest:
  `RESEARCH_GATE_SELFTEST: PASS (30 cases)`, exit 0; the first 20 case lines are
  byte-identical to the round-1 baseline's 20, and the 10 new claims cases run
  real fresh CLI processes and assert exactly one verdict line plus one
  `VERDICT_BEARING_CLAIMS` line each (`tclaims`, `:958-966`) — the round-1
  "suite-green, CLI-silent" failure class did not recur in the new mode.
- **Minor classification quirk (not a boundary breach).** A missing file cited
  lane-relative under `--root ..` classifies as `CLAIM_SOURCE_OUT_OF_CORPUS`
  (crit) rather than `CLAIM_SOURCE_MISSING` (warn), because resolution falls
  back to ROOT when `$LANE_ROOT/$src` does not exist
  (`claim_source_path`, `:655-701`). Fail-closed either way; safe.

## Method statement

`VERDICT_BEARING_CLAIMS=N/M` and a claims `CLEAN` count **span-expectation
matches**: the literal bytes of each span occur in the cited local file inside
the allowed roots, plus declared expectations — that is quotation fidelity, and
it is now executable. Three layers remain author-trust and must be named
whenever a claims CLEAN is cited as evidence: (1) the claim label versus its
span (measured above: never compared); (2) the span's meaning in context
(entailment, negation, scope — never parsed); (3) everything outside the local
corpus (refused, never fetched; the round-1 `export-unverified` limits stand).
A future strengthening — a label/span consistency check or an entailment-level
check — is not implemented and is not claimed.

## Gate

### Candidates

1. This lesson.
2. The reading "the gate now verifies claims against their sources" as a
   coverage-complete claim.
3. Adopting fixture spans or their content as domain knowledge.
4. A new `corpus/QUALITY.md` criterion from this round's rejections.
5. Promotion marks / SHONEN boxes.
6. Treating the classification quirk above as a gate defect requiring an
   immediate code change in this seat's scope.

### Admitted

- Candidate 1, this note (`corpus/lessons/2026-10-15-claims-span-fidelity.md`;
  named per the wave dispatch — the lane convention is `round-<N>.md`,
  `LEARNING.md:61`, so the integrating parent may rename).

### Rejected, with reasons

- Candidate 2 — overclaim, and the probe falsifies it: the mode verifies span
  bytes and declared expectations; the claim sentence is not read
  (`:746-750`). A CLEAN with 17/17 does not mean 17 claims are true.
- Candidate 3 — byte controls, not knowledge (`claims-r2.README.md`,
  "Boundary"); the note-writer's `corpus/knowledge/claim-verification-r2.md`
  already scopes the fixture and keeps the B03 numerals in kengaku province
  (`MINT.md:45-47`, RJ-03). No adoption follows from a CLEAN run.
- Candidate 4 — no QUALITY-bar miss produced this round's rejections; a
  criterion is added only behind a lesson that needs it (`LEARNING.md:32`).
  `QUALITY.md` stays.
- Candidate 5 — refused; this seat grants nothing, and no non-author spot-check
  exists (below).
- Candidate 6 — a warning-level wording/classification fix is left as named
  debt for the gate owner rather than silently patched: this seat's write scope
  is `corpus/lessons/` only, and the behavior is fail-closed.

### Spot-check

**Unavailable — measured outcome, not omission.** Every reviewer seat this round
is a lane seat, and "a subagent the lane dispatched is still the lane"
(`LEARNING.md:41-43`); no non-author sampled an admit and a reject, so no
agree/disagree row exists to record. Discernment remains unchanged pending an
outside check.

## Verification boundary (parent-owned)

Integration counts, commit hashes, the round report/SCORECARD entries and any
frozen-replay evidence are parent-owned; nothing here pre-claims them. Mission
acceptance remains blocked on round-1's **receipt identity, still open**: the
direct interactive launch supplies no authentic queue taskKey or stored expected
receipt bag, no receipt was minted or counted here, and proven receipt-backed
completed rounds remain 0. Later corrections land as append-only errata blocks
(`QUALITY.md:4`).
# Round-3 lesson — a hop resolves or it doesn't: chain verdicts bounded by record-declared exemption (2026-10-15)

Round: chousa-shokunin round 3, one coverage move: `verify-chain` — citation chaining
becomes verdict-bearing. Lane HEAD `0aa794d` (unchanged; `git log --oneline -1`); the
working tree carries the uncommitted round-3 change (`git status --short`:
` M tools/research-gate.sh` plus the untracked `corpus/fixtures/chain-r3*`). Gate
revision under test: `tools/research-gate.sh` sha256
`67daf85ecc49c4c7accbee9534c31b0734061b7f329e8de7a98254a57f9d6084`
(mode `chain` at `:1034-1156` of that revision; samples identical from
23:49:31Z through the poll window's end 00:07:02Z — ~18 minutes of consecutive
30-second samples spanning my whole run battery). Fixtures under test: `corpus/fixtures/chain-r3.md`
sha256 `06115f2f8e6db3c60034411dc6be42c4e0887352b09ab9cbd7f760801237ba07`,
`corpus/fixtures/chain-r3-broken.md` sha256
`b66222a16d4c5323ee6932839ff5746af5f716f36372af506755aed18e0f5c6a`, contract
`corpus/fixtures/chain-r3.README.md` (revised during the wave; its current sha
`72dbee4e…`). Raw probe outputs: `/var/tmp/lessons-distiller/` (`poll.log`,
`run-selftest.log`, `run-chain-pos.log`, `run-chain-broken.log`, `before-*.log`,
`strace-net.txt`, `strace-oob.txt`, `refs/`, `rederive-record.py`).

## Pre-registration, re-derived

The fixture is pre-registered, not fitted. Its README records the authoring state
(lane HEAD `0aa794d`, gate `03a33244…` with no `verify-chain`). My independent
poller (`/var/tmp/lessons-distiller/poll.log`, 30-second samples) saw the same:
at 23:44:31Z the gate was still round-2 `03a33244…` with zero `verify-chain`
tokens, the first fixture file mtime is 23:44:54Z, the gate's first of six
observed revisions (`2c20d955…`, `ccfd1e5c…`, `6be40a7f…`, `7379b7ee…`,
`67daf85e…`; the README lists one more transient sample, `1964ae03…`, between my
30-second samples) landed at 23:45:01Z, and the mode settled at `67daf85e…`.
Runs taken while the file was being written are not results: the README's
execution record itself briefly pinned an earlier sample (`7379b7ee…`, fixture
sha placeholder) and was corrected by its author to the revision and shas I
measured; each measurement below was taken at the settled sha.

Gate-free re-derivation, before trusting any checker: my
`rederive-record.py` and the README's own python checker (both restricted to
byte operations over the pinned archives — quote = exact substring, line =
whole trimmed line, heading = `#`-line) agree with the pre-registered ground
truth: `chain-r3.md: RESOLVED_HOPS=17/22 bad_hops=[]` and
`chain-r3-broken.md: RESOLVED_HOPS=1/2 bad_hops=['2']`. The gate's own `at=`
sequence for the 17 verified hops — 74, 64, 35, 107, 109, 57, 71, 67, 79, 88,
67, 87, 89, 52, 63, 55, 107 — matches the fixture's provenance table hop for
hop. The three `unresolved` hops are real chain breaks (near-miss bytes only:
C:118 carries `人為 — jin'i`, never the coined-rank spelling), not filler.

## Observation — the move, and the hole it closes

Before (round-2 gate snapshot `03a33244…`, run today): both fixture records pass
the structural check — `verify corpus/fixtures/chain-r3.md --root ..` →
`RESEARCH_GATE: CLEAN (findings=0 drift=0 questions=1 sources=3 chains=22
claims=2 negatives=0 rejections=1 approvals=1)`, exit 0 — and so does the
tampered control (`chains=2`). The old gate has no chain mode at all
(`verify-chain` → stderr `research-gate: multiple record paths` + usage, exit
2). The mechanism of the hole, measured with a minimal probe record: three
`resolved` hops citing `lib/primary.md:9999` (line beyond EOF), a nonexistent
`#heading`, and a bare source id all pass CLEAN, because `ptr_file_part` strips
at the first `:` and `ptr_resolves_meta` only stats files (`:223-230`,
`:255-270` at the round-2 revision) — the anchor a hop cites was never looked
for.

After (settled revision `67daf85e…`), the positive fixture:

```text
$ bash tools/research-gate.sh verify-chain corpus/fixtures/chain-r3.md --root ..
CHAIN hop=1 status=resolved observed=verified source=research/deep-research-2026-09-28/A-shokunin-tradition.md anchor=line:"1. When does an apprentice earn domain independence?" at=line:74 verdict=match
...
RESOLVED_HOPS=17/22
RESEARCH_GATE: CLEAN (hops=22 verified=17 exempt=5 anchor-missing=0 refused=0 invalid=0 findings=0 drift=0)
exit 0
```

and the tampered control, verbatim:

```text
$ bash tools/research-gate.sh verify-chain corpus/fixtures/chain-r3-broken.md --root ..
CHAIN hop=1 status=resolved observed=verified source=research/deep-research-2026-09-28/A-shokunin-tradition.md anchor=quote:"I could not substantiate this spelling as an established art" at=line:64 verdict=match
CHAIN hop=2 status=resolved observed=anchor-missing source=research/deep-research-2026-09-28/C-rank-taxonomy.md anchor=quote:"人為 — jin’i-ryū" at=- verdict=mismatch
FINDING CHAIN_ANCHOR_NOT_FOUND severity=warn surface=chain obs=hop=2 source=research/deep-research-2026-09-28/C-rank-taxonomy.md anchor=quote:"人為 — jin’i-ryū" nearest_line=53 context=The key distinction is between skill, teaching authority, and permission to act.
RESOLVED_HOPS=1/2
RESEARCH_GATE: DRIFT (hops=2 verified=1 exempt=0 anchor-missing=1 refused=0 invalid=0 findings=1 drift=1)
exit 1
```

The pair `chain-r3.md` hop 20 / `chain-r3-broken.md` hop 2 carries the same
anchor bytes: as an unmarked `resolved` hop it drifts; marked `unresolved` with
a reason it is exempt and counted. That is the whole move: a citation is
checked, and a real break stays CLEAN only when the record says so.

Adjacent mechanics measured the same way (all at the settled sha):

- A one-character tamper on the real fixture's numeral anchor (`122` → `123`,
  hop 9): `observed=anchor-missing`, `nearest_line=79`, `RESOLVED_HOPS=16/22`,
  DRIFT, exit 1 — the same record shape the old gate passed CLEAN.
- Out-of-corpus `to=/etc/hostname`: `observed=refused` +
  `FINDING CHAIN_SOURCE_OUT_OF_CORPUS severity=crit`, exit 1; `strace -f -e
  trace=openat` over the run: **0** opens of the hostname file.
- A `resolved` hop with a URL `to=`: `FINDING CHAIN_SOURCE_EXTERNAL severity=crit
  … obs=url source refused (no external fetch)`, exit 1.
- Setup boundary: `verify-chain` with no record → exit 2, stderr
  `research-gate: record path required (verify-chain RECORD, --record, or
  CHOUSA_RECORD)`, stdout empty.

## Bounds measured this round

- **Byte-stability.** `verify` on the three archives (exit 1 each) and the
  intake note (exit 0) is byte-identical to captures taken before the round-3
  change (same pinned `CHOUSA_NOW_EPOCH`, `cmp` clean); `verify-claims` on the
  round-2 fixture is byte-identical (17/17, CLEAN); `--selftest` is
  `RESEARCH_GATE_SELFTEST: PASS (40 cases)`, exit 0, and its first 30 case
  lines are byte-identical to the round-2 evidence log — the 10 new chain cases
  (`chain-pass`, `chain-fail-tampered`, `chain-fail-anchor-kinds`,
  `chain-fail-out-of-corpus`, `chain-fail-external`, `chain-fail-invalid`,
  `chain-fail-counting`, `chain-fail-no-chain`, `setup-chain-no-path`,
  `setup-chain-missing-file`) run real fresh CLI processes and assert one
  verdict line plus one `RESOLVED_HOPS` line each.
- **No-fetch bound.** `strace -f -e trace=network` over the clean fixture run
  (382,135 trace bytes): **0** `socket(`/`connect(` calls.
- **Exemption is record-declared, never checked — measured.** A probe hop with
  `status=unresolved` whose anchor (`The strongest historical model`) actually
  exists at A:52 still reads `observed=exempt`,
  `RESOLVED_HOPS=0/1`, `RESEARCH_GATE: CLEAN`, exit 0. The mode verifies
  unmarked hops and counts marked ones; it never tests that a marked hop's
  citation is really absent. Exempt is not verified.
- **`nearest_line` is a heuristic (informational).** For the `人為 — jin’i-ryū`
  miss the finding points at C:53 (a line carrying a probe token), not the
  strongest near-miss C:118. The verdict (`anchor-missing`) is right; the
  nearest-line hint is best-effort, as its name says.
- **Cosmetic carried item.** The mode banner still reads `research-gate-r1`
  (same cosmetic item the round-2 lesson named); it does not affect the
  verdict contract.

## Method statement

`RESOLVED_HOPS=N/M` and a chain `CLEAN` count **anchor existence**: for every
unmarked `resolved` hop, the cited source canonicalizes under the allowed local
roots and the declared anchor bytes occur in the target — a `#` heading line,
a byte substring, or a whole trimmed line — under the same fail-closed
boundary as `verify-claims` (`claim_source_path` `:684`, refusals reused at
`:1017-1030`); marked hops (unresolved | blocked-no-fetch | rejected |
labelled-dead | not-applicable) are exempt but counted. What that does not
prove, stated wherever a chain CLEAN is cited as evidence:

- **Not semantics, not agreement.** Hop 6 resolves with A naming four axes and
  B five; resolution says the bytes exist, nothing about the claims agreeing.
- **Not authorship or citation.** The exports do not cite each other; the
  cross-input hops are co-anchors — the target carries the bytes, not a
  reference to the citing input.
- **Not line binding or uniqueness.** `at=` is the first occurrence; the mode
  checks existence, not that the chain's logical location is that line.
- **Not exemption truth.** Measured above: a marked hop can hide a resolvable
  citation, and an unmarked one that cites nothing real drifts only if left
  unmarked.
- **Not source truth, not external verification.** The exports' own assertions
  are unadjudicated; URL and out-of-boundary sources are refused, never
  fetched. Text files only, read whole into memory.

## Gate

### Candidates

1. This lesson.
2. The reading "the gate now verifies citation chains" as a truth or
   agreement claim.
3. Adopting fixture anchors or exports' content as domain knowledge.
4. A new `corpus/QUALITY.md` criterion from this round's rejections.
5. Promotion marks / SHONEN boxes.
6. Treating `nearest_line=53` or the `research-gate-r1` banner as gate defects
   requiring a fix in this seat's scope.

### Admitted

- Candidate 1, this note (`corpus/lessons/2026-10-15-chain-hop-resolution.md`;
  named per the wave dispatch — the lane convention is `round-<N>.md`,
  `LEARNING.md:61`, so the integrating parent may rename).

### Rejected, with reasons

- Candidate 2 — overclaim, and the probes falsify it: hops 6, 4 and 14 resolve
  while saying nothing about agreement or authorship; exemption is
  record-declared. A chain CLEAN means the citations' bytes exist, no more.
- Candidate 3 — byte controls, not knowledge (`chain-r3.README.md`,
  "Boundary"); the note-writer's `corpus/knowledge/chain-resolution-r3.md`
  already scopes the fixtures. No adoption follows from a CLEAN run.
- Candidate 4 — no QUALITY-bar miss produced this round's rejections; a
  criterion is added only behind a lesson that needs it (`LEARNING.md:32`).
  `QUALITY.md` stays.
- Candidate 5 — refused; this seat grants nothing, and no non-author
  spot-check exists (below).
- Candidate 6 — `nearest_line` is documented as a hint and the verdict is
  unaffected; the banner is cosmetic and was named in round 2. Both stay named
  observations for the gate owner, not scope creep for a lessons seat whose
  write scope is `corpus/lessons/` only.

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
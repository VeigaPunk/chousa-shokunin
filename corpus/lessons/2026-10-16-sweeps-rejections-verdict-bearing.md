# Round-5 lesson — kept rejections and negative sweeps become verdict-bearing: existence is not falsifiability (2026-10-16 UTC; lane-local 2026-10-15)

Round: chousa-shokunin round 5, one coverage move: `verify-sweeps` makes the
record's defensive moves — kept rejections and negative sweeps — carry
verifiable content instead of passing on structural existence. Lane HEAD
`45f8f65` (unchanged; no commits by this seat). Gate under test — before:
`tools/research-gate.sh` sha256
`6b83705b02fe11e98b8b4aeb43fe718ff9910d21cee16d87366cef648a3960b2` (committed
at HEAD; recoverable as `git show HEAD:tools/research-gate.sh`, sha-verified);
after: sha256
`55adb92d0ba5ac958907fac6c4d5d6b0b50129703e866a5befbd9a32789f2ff2` (observed
settled: sha-stable across my whole battery and re-checked at writing; the
implementation was observed moving across 8+ revisions during the wave — see
Defects). Fixtures under test: `corpus/fixtures/sweeps-r5.md` sha256
`025352b75b7b109147fee8b8eb13b4f74eaa1550489e83166ce1dd59cfb14907`
(`sweeps-r5.README.md` sha256
`df3c0d331ac2ae58dee059182a6072550d0259d7b1c0b38f9725db9487a3ed0e`), broken
control `corpus/fixtures/sweeps-r5-broken.md` sha256
`f74ea3247e069e711278bb81addda468045053cfe556d8f5a204f3b9ff7abc0c`, planted
hit `corpus/fixtures/sweeps-r5-hit.md` sha256
`89650988074e4c371aada8e1fe77cd02d4fa85bc0c3d0a40dc21e12e1a0f78cd`.
verified-at: 2026-10-16 (UTC), from the lane cwd; fresh-process CLI runs;
read-only local opens only; nothing was fetched or executed. Local date at
writing is 2026-10-15; the file name follows the dispatch's UTC-date form —
the three sibling lessons use the local form (`2026-10-15-*`), so the
integrating parent may rename without touching content.
recheck:
`bash tools/research-gate.sh verify-sweeps corpus/fixtures/sweeps-r5.md --root ..`
· `bash tools/research-gate.sh verify-sweeps corpus/fixtures/sweeps-r5-broken.md --root ..`
· `bash tools/research-gate.sh verify corpus/fixtures/sweeps-r5-broken.md --root ..` (still CLEAN — the pre-move hole)
· `bash tools/research-gate.sh --selftest`

Raw probe outputs and scratch: `/tmp/chousa-lessons-r5/` (`out-*.log`,
`selftest-before.log`, `selftest-after.log`, `selftest-before-cases.txt`,
`selftest-after-cases.txt`, `after-summary.txt`, `strace-newmode.log`,
`rec-A-emptyshells.md`, `rec-B-emptyreason.md`, `rec-C-flipstated.md`,
`root/` = probe source tree). This seat wrote no lane file outside
`corpus/lessons/`. All script line numbers below are relative to `55adb92d…`
(the before-state numbers are relative to `6b83705b…`).

## The claim, and the hole it names

Round 1 recorded kept rejections and negative sweeps as STRUCTURAL moves: a
rejection row had to carry a non-empty `reason` cell; a negative claim or
Negatives row had to carry a non-empty `sweep` cell (or a Sweeps row naming it
by id). Nothing read the cells' content. Round 5's falsifiable claim:
**before**, a rejection with no flip-condition passes, and a sweep naming
nowhere — or claiming an emptiness that is false — passes; **after**,
`verify-sweeps <record> --root ..` requires each kept rejection to carry a
non-empty reason AND flip-condition, and each negative sweep to name where it
looked, re-running local path sets (any hit = `SWEEP_CLAIM_FALSE` naming the
hit; zero hits = verified), with non-local/source-id sets exempt but counted,
per-item verdicts, exact counting, and the CLEAN|DRIFT / 0-1-2 exit contract;
a fixture exercises all classes plus a broken control; the 44 prior selftest
cases stay byte-stable; zero network.

## Before — measured at `6b83705b` (this seat)

The gate at the round-4 revision has no `flip` concept at all (grep: no match
anywhere). The only rejection-content check is `REJECTION_REASON_ABSENT`
(`:614`); sweep cells are read only for non-emptiness (`:527-535`, `:560-561`);
no sweep content is ever re-run.

Scratch probe records (this seat, outside the lane), run as fresh processes:

- `rec-A-emptyshells.md` — R1 has a reason but **no** flip-condition; negative
  claims N1/N2 carry sweep cells `lib/void/ (no ghost.md there)` (a path that
  does not exist) and `lib/noise/` (a directory that contains
  `chat-export-sources.md`, i.e. a claimed emptiness that is false):
  `RESEARCH_GATE: CLEAN (findings=0 drift=0 questions=1 sources=2 chains=1
  claims=3 negatives=2 rejections=1 approvals=1)`, exit 0.
- `rec-C-flipstated.md` — the same record with R1's flip-condition stated:
  **identical verdict**, `RESEARCH_GATE: CLEAN (…)`, exit 0. r1 cannot tell an
  explicit flip-condition from its absence.
- `rec-B-emptyreason.md` — control: R1's reason empty →
  `FINDING REJECTION_REASON_ABSENT severity=warn surface=rejections
  obs=rejection id=R1 empty reason`, `RESEARCH_GATE: DRIFT (findings=1 …)`,
  exit 1. This one field was the whole content check.
- The round's own fixture pair: `verify corpus/fixtures/sweeps-r5.md --root ..`
  → CLEAN, exit 0, and — the hole in the round's terms — the deliberately
  broken control `verify corpus/fixtures/sweeps-r5-broken.md --root ..` →
  `RESEARCH_GATE: CLEAN (findings=0 drift=0 questions=1 sources=1 chains=1
  claims=1 negatives=1 rejections=1 approvals=1)`, exit 0, with its empty
  flip-condition and false-emptiness sweep invisible.
- `verify-sweeps` did not exist: exit 2, usage text.
- `--selftest` → `RESEARCH_GATE_SELFTEST: PASS (44 cases)`, exit 0; the 44
  `ok-case` lines were saved (`selftest-before-cases.txt`) as the byte-stability
  baseline.

## After — the rule that landed at `55adb92d` (this seat)

**Rejections** (`verify_sweeps` `:1452`; per-row check `:1477-1506`): a row
needs a non-empty reason and a non-empty flip-condition — a `flip`/`flip_condition`
(etc.) column or any column whose name matches `flip|falsif|reversal|counter`
(`sweep_flip_cell` `:1380`). Missing either →
`FINDING SWEEP_REJECTION_INCOMPLETE severity=warn surface=sweeps obs=id=… missing=flip`
(`:1502`), per-item `REJECTION … observed=incomplete verdict=mismatch`; the
record DRIFTs.

**Sweeps**: rows come from `## Sweeps` (`:1508`); when that section has no data
rows, `## Negatives` rows that name a location serve as the fallback
(`:1514`). The location comes from a `where`-style named column
(`where/looked_at/looked/scope/searched/paths/location/targets`), a
column-name scan (`where|looked|scope|glob|target|locat`), or the r1 `sweep`
cell (`sweep_raw_where` `:1388-1394`). A whitespace-free value is split on
commas/semicolons only; a value containing whitespace is read as a
command/description whose structured words are extracted — an r1-style
`test ! -f lib/ghost.md` cell names `lib/ghost.md` (header `:99-101`). Row
markers `unresolved|blocked-no-fetch|labelled-dead|not-applicable` in a status
column are exempt (`:1530`). Then:

- a local set (path/glob tokens) is re-run as a glob under `--root`
  (`nullglob globstar`, `sweep_glob_matches` `:1432`): any match →
  `FINDING SWEEP_CLAIM_FALSE severity=warn surface=sweeps obs=id=… hits=N
  first=… listed=…` (`:1597`, first hit plus up to 5 listed), per-item
  `SWEEP … observed=hit verdict=mismatch`; zero matches →
  `observed=verified verdict=match`;
- declared source ids and non-local targets (`http(s)://`, `local://`,
  `external:`, `web:`, `session:`) are exempt but counted — “a content sweep
  carries no probe the gate could re-run” (header `:78-80`);
- a path escaping the corpus boundary is refused unopened
  (`SWEEP_LOCATION_OUT_OF_CORPUS`, crit, `:1571`), an undeclared source id is
  `SWEEP_LOCATION_UNRESOLVED` (`:1577`), naming nowhere / unclassifiable naming
  is `SWEEP_LOCATION_ABSENT` (`:1538`, `:1563`).

Summary: `VERIFIED_SWEEPS=N/M REJECTIONS_OK=K/L` (`:1614`); CLEAN iff
verified+exempt = M and K = L and no finding drifts; the 0/1/2 exit contract
and one verdict line per run; `--selftest` PASS (54 cases), exit 0.

Verbatim, positive fixture (CLEAN, exit 0):

```text
SWEEP id=W1 where=research/deep-research-2026-09-28/kotobank-*,research/deep-research-2026-09-28/s looked=local hits=0 at=- observed=verified verdict=match
SWEEP id=W2 where=https://kotobank.jp/ looked=non-local hits=- at=- observed=exempt verdict=exempt
REJECTION id=R1 ref=research/README.md:12 reason=present flip=present observed=complete verdict=match
REJECTION id=R2 ref=research/deep-research-2026-09-28/B-multiagent-knowledge.md:79 reason=present flip=present observed=complete verdict=match
REJECTION id=R3 ref=research/deep-research-2026-09-28/B-multiagent-knowledge.md:63 reason=present flip=present observed=complete verdict=match
VERIFIED_SWEEPS=1/2 REJECTIONS_OK=3/3
RESEARCH_GATE: CLEAN (sweeps=2 verified=1 exempt=1 hit=0 refused=0 invalid=0 rejections=3 rejections-ok=3 findings=0 drift=0)
```

(W1's `where=` display is cut at the mode's own 80-character cap — the cell
itself names both globs, `…/kotobank-*` and `…/saved-*`.) Verbatim, broken
control (DRIFT, exit 1):

```text
SWEEP id=W1 where=chousa-shokunin/corpus/fixtures/sweeps-r5-hit.md looked=local hits=1 at=chousa-shokunin/corpus/fixtures/sweeps-r5-hit.md observed=hit verdict=mismatch
REJECTION id=R1 ref=research/README.md:12 reason=present flip=absent observed=incomplete verdict=mismatch
FINDING SWEEP_REJECTION_INCOMPLETE severity=warn surface=sweeps obs=id=R1 missing=flip
FINDING SWEEP_CLAIM_FALSE severity=warn surface=sweeps obs=id=W1 where=chousa-shokunin/corpus/fixtures/sweeps-r5-hit.md hits=1 first=chousa-shokunin/corpus/fixtures/sweeps-r5-hit.md listed=chousa-shokunin/corpus/fixtures/sweeps-r5-hit.md
VERIFIED_SWEEPS=0/1 REJECTIONS_OK=0/1
RESEARCH_GATE: DRIFT (sweeps=1 verified=0 exempt=0 hit=1 refused=0 invalid=0 rejections=1 rejections-ok=0 findings=2 drift=2)
```

My before-probes re-run under the new mode: `rec-A` →
`SWEEP_REJECTION_INCOMPLETE … missing=flip`, DRIFT exit 1 (pre-move CLEAN);
`rec-B` → `missing=reason,flip`, DRIFT; `rec-C` → `REJECTIONS_OK=1/1`, CLEAN
exit 0. Note: all three show `VERIFIED_SWEEPS=0/0` — their sweeps sit in
claims-table `sweep` cells, which the mode does not read (see Limits).

What held unchanged:

- `--selftest` → `RESEARCH_GATE_SELFTEST: PASS (54 cases)`, exit 0 — the 44
  prior `ok-case` lines byte-identical to the before run (diff clean), plus 10
  new cases (`:2479-2649`): `sweeps-pass`, `sweeps-fail-planted-hit`,
  `sweeps-fail-rejection-incomplete`, `sweeps-fail-unnamed`,
  `sweeps-fail-out-of-corpus`, `sweeps-fail-unresolved-id`,
  `sweeps-fail-counting`, `sweeps-pass-cell-command`, `setup-sweeps-no-path`,
  `setup-sweeps-missing-file`. The counting case closes
  `VERIFIED_SWEEPS=1/5 REJECTIONS_OK=1/3`.
- Regressions at the new revision: claims `VERDICT_BEARING_CLAIMS=17/17`,
  CLEAN, exit 0; chain `RESOLVED_HOPS=17/22`, CLEAN, exit 0; chain broken
  control `RESOLVED_HOPS=1/2`, DRIFT, exit 1; r1 `verify` on the positive
  fixture still CLEAN exit 0 and on the broken control still CLEAN exit 0
  (the mode is additive; the hole stays visible on the r1 path); the r1
  archive observable `VERDICT_BEARING_EXPORTS=3/3`.
- Zero network: `strace -f -e trace=network` around the positive
  `verify-sweeps` run → 0 socket/connect/sendto/recvfrom lines; exit 0.
- Gate sha stable across the whole battery (before = after =
  `55adb92d…`).

## Method statement — what a CLEAN verify-sweeps establishes

For every rejection row read: a non-empty reason and a non-empty
flip-condition are PRESENT. For every sweep item read: either its named local
path set re-measures empty under `--root` at check time (glob existence, zero
matches), or it was refused/invalid (drift), or it is exempt-and-counted
(non-local target, declared source id, or an exempt status marker). What it
does **not** prove, stated wherever such a CLEAN is cited:

- **Not flip-condition quality.** Only non-emptiness is checked; a placeholder
  string passes. The fixture README names this too ("Honest boundaries").
- **Not sweep scope adequacy.** The re-run proves the named set is empty, not
  that the set is the right place to look. A sweep naming a mistyped or
  nonexistent glob verifies vacuously — measured two ways: my `rec-A`-family
  naming pattern and the fixture-author's `--root .` run of the broken control
  (`VERIFIED_SWEEPS=1/1`, DRIFT only from R1's flip), both recorded in the
  fixture README. The mode cannot certify the look happened, only that the
  named set is empty now.
- **Not a content search.** The re-run expands a path set; it never greps file
  contents. The fixture's W1 is phrased as a path-set absence because that is
  the class the mode can re-check; the intake's content census ("no URL locator
  exists in the archive set") stays a recorded census, not a re-check.
- **Not exemption truth.** Non-local/source-id sweeps remain author
  declarations, counted but unexamined (the chain exempt-hop pattern).
- **Not time-stable.** Emptiness is a property of the revision checked; a file
  appearing later falsifies a past CLEAN.
- **Not semantics or source truth.** Rounds 2-4 bounds stand unchanged; the
  pre-existing residuals (in-root hardlink bypass, no source size cap, the
  `research-gate-r1` banner) are untouched by this move.

## Defects and follow-ups noted (outside this seat's write scope)

- **Claims-table sweep cells are not re-checked — the round's largest
  residual.** `verify_sweeps` reads `## Sweeps` rows and `## Negatives` rows
  (`tools/research-gate.sh:1508-1515`; no `Claims` reference in the function),
  while r1 accepts a `sweep` cell on a `kind=negative` Claims row as
  satisfying `NEGATIVE_WITHOUT_SWEEP` (`:527-535` at `6b83705b`; the rule
  survives in `verify`). Measured: `rec-A`/`rec-B`/`rec-C` each carry two
  negative claims with sweep cells and report `VERIFIED_SWEEPS=0/0` in sweeps
  mode (logs `out-sw-rec-*.log`). Either the mode should read those cells or
  the header should state they are out of scope; otherwise "kept rejections and
  negative sweeps become verdict-bearing" holds for the Sweeps/Negatives forms
  only.
- **Writing-window churn (acceptance-timing discipline).** The gate moved
  across 8+ revisions in ~15 minutes
  (`df7ec322…`/`ba0c1744…`/`f3ae245e…` → `ea673ddb…` → `c5c92388…` →
  `6911a426…` → `f8499d0f…` → `2fd4f7c7…` → `b701bef6…` → `55adb92d…`); a
  selftest run at `2fd4f7c7…` closed `FAIL (1/54 cases)` on
  `sweeps-pass-cell-command` and the settled `55adb92d…` closes PASS (54).
  Acceptance must pin the sha (the fixture README does; this lesson does); a
  red intermediate revision is not evidence against the settled one.
- **Display cap (cosmetic).** Per-item `where=` truncates at 80 characters
  (`chain_disp`), so the positive fixture's W1 shows `…/s` instead of
  `…/saved-*`. The fixture README explains it; no behavior change.
- Round-1 **receipt identity remains open**; nothing in this lesson mints or
  counts a receipt.

## Gate

### Candidates

1. This lesson.
2. The reading "verify-sweeps proves the rejections are still right".
3. The reading "a verified sweep proves the search was adequate".
4. Adopting fixture or intake content as domain knowledge.
5. A new `corpus/QUALITY.md` criterion from this round's rejections.
6. Promotion marks / SHONEN boxes.

### Admitted

- Candidate 1, this note
  (`corpus/lessons/2026-10-16-sweeps-rejections-verdict-bearing.md`; sibling
  lessons use the lane-local `2026-10-15-*` form, so the integrating parent
  may rename).

### Rejected, with reasons

- Candidate 2 — overclaim; the probes falsify it: the mode checks presence of
  a flip-condition and emptiness of the named set, never whether the
  rejection still holds (a vacuous flip-condition and a wrong-location sweep
  both pass).
- Candidate 3 — overclaim; scope adequacy is explicitly outside the mode (the
  empty-glob vacuous verify is measured; fixture README "Honest boundaries").
- Candidate 4 — byte controls, not knowledge; fixtures are pre-registered
  inputs with expected outputs, and the intake citations are provenance, not
  adjudicated facts.
- Candidate 5 — no QUALITY-bar miss produced this round's rejections.
- Candidate 6 — refused; this seat grants nothing and no non-author spot-check
  exists.

### Spot-check

**Unavailable — measured outcome, not omission** (as in rounds 1-4: every
reviewer is a lane seat; no non-author sampled an admit and a reject).
Discernment remains unchanged.

## Verification boundary (parent-owned)

Integration counts, commit hashes, the round report/SCORECARD/LOG entries and
any frozen-replay evidence are parent-owned; nothing here pre-claims them.
The before/after pair measured here is: `6b83705b…` (committed at HEAD
`45f8f65`) → `55adb92d…` (working tree, uncommitted at this writing,
sha-stable across the battery). Mission acceptance remains blocked on round-1's
receipt identity (still open); no `task_…` value is invented and no receipt was
counted. Later corrections land as append-only errata blocks (`QUALITY.md:4`).
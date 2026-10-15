# Round-1 lesson — suite-green, CLI-silent: the entrypoint gap (2026-10-15)

Round: chousa-shokunin probation round 1. Evidence: lane commit
`34774a1777d4058ca8c2b4456ce2e6ccee9e24c5` (HEAD at writing — `git log --oneline -1`);
`LOG.md` round-1 baseline entry (:72-83, working tree — LOG.md is the only
uncommitted file among those cited, per `git diff HEAD --stat`);
`SCORECARD.md:29` counting command; `MINT.md:8-13` input names.
All script line numbers below were re-derived from the baseline script
(working tree == HEAD for `tools/research-gate.sh`, sha256
`e8f07a063e28c4f841719c413b47a5c31d0b8af41635737c90e2c8acb79012b0` —
`sha256sum tools/research-gate.sh`, 2026-10-15). Per `LOG.md:55-57`, no wave
citation was copied.

## Observation — the two verdicts of one revision

- Real CLI: `bash tools/research-gate.sh verify <export> --root ..` over the
  three archived exports (`../research/deep-research-2026-09-28/`, source
  revision `0863746e9da95457f71b9e00a40361b88ab0df15`, per-file SHA-256 in
  `LOG.md:102-109`) exits 1 with zero stdout bytes, zero stderr bytes and zero
  verdict lines: `VERDICT_BEARING_EXPORTS=0/3` (`LOG.md:72-78`; the parent
  re-executed the exact command at the unchanged script baseline 2026-10-15 —
  still `0/3`).
- In-process suite, same revision: `RESEARCH_GATE_SELFTEST: PASS (17 cases)`
  exit 0 (`LOG.md:33-35`).

## Cause — function-under-set+e vs CLI-under-set-e

The landing note attributed the silence to "an unchecked grep under `set -e`"
(`SKILL.md:74-81`, `LOG.md:37-40`). Re-derivation against the baseline script
displaces that diagnosis:

1. `tools/research-gate.sh:25` — `set -euo pipefail` in effect for the CLI run.
2. `tools/research-gate.sh:68-76` — `emit_finding`'s last executed statement is
   the severity `case`. On the `info` arm (`:74`), `[[ $STRICT == 1 ]] && { … }`
   with `STRICT` defaulting to 0 (`:38`) evaluates the `[[ ]]` test false, so the
   `&&` list — and the function — returns 1. (Strict mode takes the right-hand
   group and returns 0: the defect is specific to the non-strict path.)
3. `tools/research-gate.sh:339-341` — `verify_record` calls
   `emit_finding EXPORT_CHROME_PRESENT info …` as a plain statement when the
   chrome regex `^(Skip to content|ChatGPT|You said:)` matches. It matches on
   the real inputs: `grep -cE '^(Skip to content|ChatGPT|You said:)' <file>` →
   7, 7, 7 for A/B/C (2026-10-15, read-only fleet inputs). So `:340` returns 1,
   errexit kills the main shell at that statement — before the record header
   (`:536`) and the summary (`:541`). Exit 1, zero bytes on both streams, no
   verdict line. Observed baseline matches the mechanism exactly.
4. The suite cannot see step 3. `tcase` wraps every call with `set +e` …
   `rc=$?` … `set -e` (`:565-568`), and the `fail-schema` fixture (`:942-948`)
   carries the same three chrome tokens (`:943-945`), so the identical
   `:340` call executes in the harness too — with errexit suppressed,
   `verify_record` reaches `:541`, returns rc=1 as the case expects, and the
   case passes.

The only difference between the living and the dead execution of the same code
is the entrypoint: the CLI dispatch runs `verify_record "$RECORD_PATH"` as a
top-level statement under live errexit (`:1001`); the harness runs it as a
function under `set +e`. **A suite that exercises only the second mode proves
nothing about the first.** Method statement (observation, this lane): a
verdict-bearing CLI must emit its summary on every exit path, and the regression
must run the real entrypoint, not only the callable.

Craft routing: the fail-closed / one-verdict-per-exit-path pattern is tameshi's
verification craft, and a pattern is not general until two independent lanes
evidence it (`tameshi-shokunin/PROVINCE.md:14-17`). This lesson is the second
data point's pointer, reported out via the round report; chousa keeps the
lane-instance fact and records, does not absorb ("Out of province → report,
never absorb", `PROVINCE.md:17`).

## Gate

### Candidates

1. This lesson — the entrypoint/errexit gap with re-derived anchors.
2. One local intake example, `corpus/knowledge/archived-export-intake.md`
   (SourceIntake lane; selected move includes "a locally sourced intake
   example", `LOG.md:84-85`).
3. The blanket-grep-guarding diagnosis as the established cause.
4. Domain rows from the A/B/C export bodies (rank terminology, ACE case-study
   numerals, harvest provenance, axis lists).
5. A second axis taxonomy lifted from the survey.
6. A new `QUALITY.md` criterion from this round's misses.
7. A promotion mark: checking SHONEN boxes, claiming discernment improved.

### Admitted

- Candidate 1, this note (`lessons/round-1.md`).
- Candidate 2 conditionally: the intake example is admitted in dispatch, but at
  writing `corpus/knowledge/` holds only `.gitkeep` (`ls corpus/knowledge/`,
  2026-10-15 04:59 UTC — command counted against the directory, not a claim of
  absence-after-this-round). Per `CORPUS.md:45-47` an index row is written when
  the file exists; no phantom row was added. The integration instruction lives
  in `corpus/README.md` "Index integration".

### Rejected, with reasons

- Candidate 3 — `|| true`-guarding every grep is not the established cause: the
  fatal statement is the `emit_finding` call at `:340`, whose return value comes
  from `:74`, not from a grep; the `:339` grep sits in `if`-conditional context
  (errexit-exempt) and matched anyway. Guarding the greps changes nothing on
  this abort path. Recorded here rather than dropped (`QUALITY.md:5`); the
  supersession is also logged at `LOG.md:80-83`.
- Candidate 4 — export text is untrusted data, never independently verified
  domain truth (round-1 contract), and the specific content assertions are
  unsupported or self-refuting in the exports themselves: `jin'i-ryu` is
  explicitly unsubstantiated by the export that names it
  (`A-shokunin-tradition.md:64`, read 2026-10-15; guard `MINT.md:37-44`); the
  ACE numerals (`B:79`) are an unresolved hop, and quoting them unhedged
  launders a model-quality claim into kengaku's province (`MINT.md:45-47`,
  `MINT.md:135-141`); `research/README.md:6-8` provenance (burner Chrome, CDP,
  "9/8/10 searches") is contradicted by measurement — visible search labels are
  1, 1, 2 (`MINT.md:57-62`). Items solicited in the prompts but never answered
  stay unanswered; truncation is unknown, not a negative (`MINT.md:49-51`).
  Reusable method specimens are kept as pointers only, tagged
  `export-unverified`: the hedged negative at `A:64` and the
  published-finding-vs-proposed-rule split at `B-multiagent-knowledge.md:59`
  (read 2026-10-15). No survey sentence enters `knowledge/` without a scope tag
  (`MINT.md:86`).
- Candidate 5 — the survey contains three mutually incompatible axis lists
  (`MINT.md:75-82`: `A:54`, `B:57`, `C` naming/rank rows); the fleet already
  owns the six axes (`AXES.md:7-16`, fleet root) and this lane's table lives at
  `SKILL.md:13-21`. A second taxonomy is explicitly forbidden for the landing
  (`MINT.md:90`).
- Candidate 6 — none of this round's rejections came from a `QUALITY.md` bar
  miss; they came from the contract and the MINT guards. Adding a criterion now
  would be the named discernment harm — "a criterion is added with no lesson
  behind it" (`LEARNING.md:32`). `QUALITY.md` stays as it is.
- Candidate 7 — refused outright. L2 seats remain the author lane and cannot
  grant promotion marks (`LOG.md:98-99`); no SHONEN box is marked here and no
  trend verdict of "improved" is claimed for discernment.

### Spot-check

**Unavailable — measured outcome, not omission.** Discernment is only checked
by a non-author sampling at least one admit and one reject
(`LEARNING.md:39-43`); every reviewer seat this round was dispatched by the
lane, and "a subagent the lane dispatched is still the lane"
(`LEARNING.md:43`, contract: "L2s are still author lane"). No agree/disagree
row exists to record. The operability trend itself is separate from this corpus
gate: code fixing is the parent-measured axis move; nothing here converts
into a corpus-trend claim.

## Verification boundary (parent-owned)

Post-fix counts on the committed round-1 revision, the selftest re-run, and the
announced replay-evidence file `corpus/evidence/round-1/expected.json` (Main,
2026-10-15) are owned and appended by the parent; this lesson does not
pre-claim their results, and the current gate makes no frozen-run conformance
claim. Later corrections land as append-only errata blocks (`QUALITY.md:4`).

## Integration errata — 2026-10-15

The baseline observations above are inherited author evidence, not reruns of
the known failure by this interactive continuation. The gate fix is committed
as `31b46832e56a7f095092a4a6d62b74bfaf6933e8`; its SHA-256 is
`08843552378071929c8b6abcd50be6613365691cfae4bf0d74fb03d86eb5b46e`.
The L1 ran the actual entrypoint on that revision:

- `bash tools/research-gate.sh --selftest`: exit 0,
  `RESEARCH_GATE_SELFTEST: PASS (20 cases)`.
- Pinned A/B/C archives: each exit 1 with exactly one full DRIFT summary;
  `VERDICT_BEARING_EXPORTS=3/3`.
- The inherited intake draft: exit 0 with exactly one CLEAN summary.

Exact argv, full output, input digests and exits are committed evidence at
`.ufo/evidence/round-1/acceptance.json` and `acceptance.txt`. The final
intake's metadata/errata recheck is recorded separately in `final-intake.json`.
The normal-info, strict-info, malformed-after-info, secrecy, session-refusal
and setup cases ran as real fresh CLI processes, not in-process calls under
`set +e`. Integration also corrected the draft harness's lenient fixture
filename mismatch before running it.

**Corrections to earlier prose.**

1. “LOG.md is the only uncommitted file” and the missing knowledge-note/index
   instructions describe an earlier draft state, not the integration state.
   The knowledge specimen now exists and is indexed; it is admitted for
   local method-form/structural observations only. No export-domain claim
   becomes independently verified because a record is CLEAN.
2. README provenance is **unverifiable-locally**, not contradicted by visible
   search-label counts. Saved labels 1/1/2 do not establish a live total.
   The intake's integration errata preserves this distinction and narrows
   its numbered-section absence claim.
3. “Summary on every exit path” is limited to evaluated-record verdict paths.
   Setup failures deliberately exit 2 with no stdout verdict and a diagnostic
   on stderr. The selftest asserts this boundary.
4. All numbered script references in the cause analysis refer to baseline
   `34774a1`; current registry prose points to the measured fix and evidence.
   The prior LOG citation-shift notice also lags the skill: the checklist is
   `SKILL.md:54`, its four rules `:56-59`.
5. The general cross-lane entrypoint pattern remains only a routing candidate.
   No independent second-lane confirmation or non-author promotion review
   was performed here.

### Gate decision at integration

Candidates 1 and 2 are held as the lesson and a structurally checked local
intake specimen. Candidates 3–7 remain rejected for the reasons above.
No new QUALITY criterion was invented; no agree/disagree spot-check row or
promotion mark is manufactured. Expansion is improved by the newly held
intake form; quality and discernment are unchanged because semantic-quality
comparisons and a non-author admit/reject check are absent.

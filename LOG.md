# chousa-shokunin — Iteration Log

- 2026-10-14 — round 0: minted as shonen (sibling mint; rationale in MINT.md).

## 2026-10-15 — boundary parity fix (round 1 integration prep)

`ScopeBoundary` found a contradiction in the mint artifacts: `MINT.md` and the
roster scan (`mint-roster-scan.json`) explicitly rejected **kumitate** as a
complementary province, but the `PROVINCE.md` and `SKILL.md` refusal clauses this
lane wrote omitted it. Closed here — both files now name orchestration,
multi-agent dispatch and agent lifecycle as refused (→ kumitate). Recorded rather
than silently patched, because the omission had already propagated into peer
proposals (`QualityBar` Q-BOUND, `ApprovalTable`), and the proposed gate vocabulary
classified `SCOPE_ORCHESTRATION_ABSORBED` as `info` where the other two absorbed-
scope ids are `warn` — a severity asymmetry that would let an absorbed orchestration
record pass as CLEAN. **Landing requirement:** that id must be elevated to `warn`
so all three refused provinces have identical gate teeth, with one symmetric
selftest fixture per province asserting exit 1.

## 2026-10-15 — research gate landed (not field-ready)

`tools/research-gate.sh` landed from the round-1 design (994 lines). Two design bugs
were found and fixed while landing:

1. `local sec=$1 line body=${SEC_BODY[$sec]-}` — `local` expands every right-hand
   side before assigning, so `$sec` was unset and `set -u` aborted; **13 of 17**
   selftest cases died on `line 165: sec: unbound variable`. Split the declaration.
2. `ROOT` was captured once at load from the ambient `CHOUSA_ROOT`, but the hermetic
   suite exports it per case and calls `verify_record` as a function — so every
   `lib/…:N` pointer read "missing under CHOUSA_ROOT" and both PASS controls failed.
   `verify_record` now re-reads the env.

After both: `bash tools/research-gate.sh --selftest` → **`RESEARCH_GATE_SELFTEST:
PASS (17 cases)`** exit 0, and the suite's own secrecy case confirms a planted
`sk-` value is not echoed.

**Carried defect, named:** on a real chat-export input the gate exits 1 with **no
verdict line** — an unchecked `grep` under `set -e` ends the script before the
summary. Not field-ready; unblock is to `|| true` every non-fatal `grep` and re-run
the suite plus the real artifact.

### Citation-shift notice (appended 2026-10-15)

The boundary-parity fix inserted **3 lines** into `SKILL.md` at 39–41 (the kumitate
refusal). Every line number below that point moved by +3: the checklist heading is
now `SKILL.md:44` and the four rules are `:46`–`:49` (sweep rule at `:47`), where
the wave's seats cite the pre-edit numbers. **Round-1 citations to `SKILL.md:44` or
later are pre-edit** and must be re-derived before being trusted — the rules
themselves are unchanged. This notice also fixed the lane's own guard, which cited
`SKILL.md:45` for the observation/inference/unknown split; the live line is `:48`.

Also recorded from the same audit: `RuleOrProposal` found several wave-internal
citations that resolve to the wrong lines (QUALITY item numbers used as line numbers;
`claim-ledger.sh:45-48` cited for stamp status where the live lines are `:15-16`;
export chips treated as URLs; `README.md:6-8` credited with a four-tier hierarchy it
does not state). Those are wave-report defects, not lane defects, and they are the
reason the corpus landing must re-derive every citation rather than copy one.

### Skill honesty note (appended 2026-10-15)

`HonestyAudit` measured the peer set at 96 admitted / 34 proposal label instances
and found this skill's own operative rows largely unmarked: **0 `proposal` tokens**
and **0 independently cited admissions** at mint. The four-tier source hierarchy is
this lane's construction — no other lane states it and the survey exports do not —
so it is now marked as a working standard rather than an inherited rule, and any row
warranted only by it is a `proposal` until a real `path:line` backs it. The audit's
citation findings match the shift notice above (18 cites do not say what they claim;
the +3 `SKILL.md` shift moved the checklist).

## 2026-10-15 — round-1 operability: baseline and selected move

At lane commit `34774a1777d4058ca8c2b4456ce2e6ccee9e24c5`, the real
`bash tools/research-gate.sh verify <export> --root ..` CLI was executed over
the three `research/deep-research-2026-09-28/` inputs A/B/C named in `MINT.md:8-13`.
Each returned exit 1, zero stdout bytes, zero stderr bytes, and zero verdict
lines: `VERDICT_BEARING_EXPORTS=0/3`. `SCORECARD.md` now declares the narrow
counting command and initializes the previously absent scorecard; operability is
the sole measured axis, score 0, not an invented overall expertise rating.

The earlier "unchecked grep" diagnosis above is not the demonstrated cause:
`tools/research-gate.sh:68-76` ends `emit_finding` with a conditional strict-mode
branch. A non-strict `info` finding returns 1; `verify_record` invokes that
helper directly for export chrome (`:339-341`) under `set -e` (`:25`).
The selected single improvement is a verdict-preserving informational emitter,
with real-CLI regression coverage and a locally sourced intake example.
No external targets, browser/session state, or domain source writes are required.

### Round-1 dispatch and publication preconditions

The single native OMP `task` batch returned the role seats
`OperabilityPlanner` (planner), `SiblingConnector` (connector),
`ProductionGate`, `CliRegression`, `IntakeExample` (executors),
`EvidenceScribe` (scribe), `LocalSurfaceScout` (scout),
`ContractReviewer` (reviewer), and `ClaimCritic` (critic).
This is the mission-specific heterogeneous batch under the shokunin host
mapping, not a validated generic UFO swarm-wave. Role names, not model aliases,
were passed to the unchanged host router. L2s remain part of the author lane;
their reviews cannot grant promotion marks or an outside discernment check.

Source inputs were pinned by `git -C .. log -1 --format='%H %aI' -- research`
to fleet commit `0863746e9da95457f71b9e00a40361b88ab0df15`.
`sha256sum ../research/deep-research-2026-09-28/{A-shokunin-tradition,B-multiagent-knowledge,C-rank-taxonomy}.md`
returned, in that order:

```text
9033857d4625555c7b778dfad6df80e3e1b24ed8bffa3fee2fd445b9c5540b85
6d8dbddd3e2d2f47dcb153c5a3347cc6321db4afc72cf07da40f0f7fe5022006
e48fe70ff92055c217ac6ca6ce68e403aa5689fee8717f3bd0ccf5badc92321b
```

`git remote -v` in this lane returned no rows; fleet origin is configured as
`https://github.com/VeigaPunk/shokunin.git`. No lane URL was guessed or created.
The operator question is appended to `.ufo/l0-questions.md`, keyed
`chousa | round-1 | Which operator-selected remote URL should chousa-shokunin use?`;
the integrator owns committing that queue. Reachable local work continues.

### Round-1 continuation — observed batch and retained baseline

This execution inherited the uncommitted scorecard and the baseline/precondition
entries above at lane HEAD `34774a1777d4058ca8c2b4456ce2e6ccee9e24c5`.
The scorecard's exact counting command was executed again before any gate edit:
`VERDICT_BEARING_EXPORTS=0/3`. Input hashes and the source commit above were
re-derived with the recorded `sha256sum` and `git -C .. log` commands and matched.

One native OMP `task` call returned nine seats: `RoundOnePlanner` (planner),
`RoundOneConnector` (connector), `GateRuntime`, `SourceIntake`, `CorpusLearning`
(three executors), `RoundOneScribe` (scribe), `RoundOneScout` (scout),
`RoundOneReviewer` (reviewer), and `RoundOneCritic` (critic).
These are the observed seats for this continuation; the earlier seat-name
paragraph is inherited prep, not evidence of these seats' results.
The host binding maps a shokunin batch to `task`; this heterogeneous round
is not represented as a validated generic UFO wave. No model parameter or
routing mutation was used. `~/.omp/agent/config.yml:318-330` is the read host
role-override authority; its current buckets differ from the mission prose.
No model aliases were copied into lane configuration.

The retained cause is the false return from the non-strict `info` branch of
`emit_finding`, not a demonstrated unchecked-`grep` failure. The existing
`tcase` invokes `verify_record` under `set +e` (`tools/research-gate.sh:562-568`
at the baseline), so it does not exercise the CLI's errexit behavior. The
single move couples explicit finding-emitter success to fresh-process CLI
coverage and a local archive-intake specimen. Post-edit results are recorded
only after integration and execution below.

## 2026-10-15 — interactive round-1 reconciliation and integration

Starting HEAD was `34774a1777d4058ca8c2b4456ce2e6ccee9e24c5`.
Inherited modified gate/index/log and untracked scorecard/intake/lesson/input
pins were preserved. The driver's launch counter is not a verified-round count.
The plan is `.ufo/plans/round-1-interactive-20261015T050057Z.md`.

**Dispatch correction to the preceding nine-seat accounts:** the required
round-1 batch already exists as `Shokunin12hP5ChousaR1`. Read-only preserved
fleet artifacts at `.ufo/waves/shokunin12h-20261014-p5-chousa-r1/` show
32 rendered tasks and `task-response.json` saying “Spawned 32”; its safe
progress metadata records content `m_composer`, audits `m_grok`, connectors
`m_antigravity`. The registry under
`.ufo/scopes/Shokunin12hP5ChousaR1/swarm-registry.json` has 32 assignments;
all 32 named reports exist. `ufo-swarm-wave.mjs plan --spec <preserved spec>`
returned exit 0 with spawn=32, resume=0, width=32. Distinct rendered names,
prompts and leading `/skill:godspeed` prefixes each count 32. Full per-member
source hashes/dispositions are in `.ufo/evidence/round-1/wave-reconciliation.json`;
the revalidated plan is `wave-plan.json` beside it. No new task call was made.
Later nine-seat calls are advisory, not replacement or completion evidence.
The old registry drops actual `-2` suffixes for CorpusMap, FindingIds and
GateRegistryRow; local reconciliation records the response IDs without
mutating the shared registry. Spawn-time `pending` is not a current liveness
claim; member report files, not a re-probe of native sessions, are observed.

The current global role defaults would misroute a **new** wave; this does not
invalidate the existing dispatch-time bindings. The initial interactive plan's
round-1 route-blocker classification is superseded by its reconciliation
correction. No route overlays, global settings, source trees, session bodies
or shared reports were changed. The already reported Phase 0 failures were
not rerun and no native judgment is claimed.

The one improvement preserves the inherited explicit-success finding emitter
and real-CLI fixture harness. Integration review found a fixture name mismatch:
`pass-export-chrome.md` was created but `pass-export-chrome-lenient.md` was
requested. The invocation now uses the created file. Comments were shortened
to the invariant; broad grep suppression was not introduced. Acceptance and
real CLI outcomes are not pre-claimed; they are recorded after execution.

**Named existing debt:** the scope-finding IDs required by the boundary-parity
entry at the top of this log never landed in the script. A read-tool grep
`SCOPE_|scope|absorbed` over `tools/research-gate.sh` found only a fixture table
header, no scope finding emitter. The documented province refusals are retained,
but gate enforcement is not claimed. A future single axis move can implement
the three refused-province findings and symmetric exit/finding fixtures.

## 2026-10-15 — round-1 local acceptance, corpus integration and receipt boundary

Measured committed gate: `31b46832e56a7f095092a4a6d62b74bfaf6933e8`.
Script SHA-256:
`08843552378071929c8b6abcd50be6613365691cfae4bf0d74fb03d86eb5b46e`.
The L1 ran the public CLI with inherited CHOUSA overrides unset, recording
exact argv/stdout/stderr/exits in `.ufo/evidence/round-1/acceptance.json`
and `acceptance.txt`:

- `--selftest` → `RESEARCH_GATE_SELFTEST: PASS (20 cases)`, exit 0.
  Normal info remains CLEAN; strict info DRIFT; malformed-after-info
  continues to later findings; secrecy and session refusal pass; setup cases
  retain exit 2 with no stdout verdict.
- A/B/C archive inputs each matched the committed expected SHA-256 before
  invocation; each exits 1 with exactly one full DRIFT verdict
  (`findings=6 drift=5 questions=0 sources=0 chains=0 claims=0 negatives=0
  rejections=0 approvals=0`). `VERDICT_BEARING_EXPORTS=3/3`; baseline 0/3
  is the retained prior measurement, not a failure rerun here.
- The inherited intake draft exits 0 with one CLEAN verdict. After adding
  opening metadata and append-only errata, its actual CLI recheck also exits
  0 with `findings=0 drift=0 questions=1 sources=8 chains=8 claims=9
  negatives=2 rejections=10 approvals=3`. Final input SHA-256:
  `33deaf93cec381509604db84e1b9c44d8ab3020998bf103eea7b720203fb62ec`;
  exact output is `.ufo/evidence/round-1/final-intake.json`.

`SKILL.md` now has one gate registry with the observed selftest and limited
structural guarantee, not the false “unchecked grep” cause or a field-ready
claim. `corpus/README.md` indexes the actual lesson and knowledge specimen;
`functions.glob` over `corpus/knowledge/*.md;corpus/lessons/*.md` returns those
two entries. Opening source/verified-at/recheck fields and append-only
integration errata preserve the inherited note/lesson rather than erasing
draft observations.

The L1 remeasured bounded source-form sweeps, saved in `source-sweeps.json`:
numbered-section regex `^([0-9]+[.]|[(][0-9]+[)])` matches A:74 and B:77;
HTTP(S)-locator regex has no matches across A/B/C plus README; visible
search-label regex matches A:42, B:42, C:42 and C:55. The old Markdown-table
command escaped alternation incorrectly; its executable correction is
appended to the intake. Numbered-section absence is not proof of every
answer's absence in prose. Visible labels cannot verify or contradict a
live search total; the stronger provenance assertion remains unknown.
No external source was fetched and no native transcript body was read.

**Citation-shift correction to the earlier LOG notice:** the current checklist
is `SKILL.md:54`, rules `:56-59`; the old `:44` / `:46-49` notice and
baseline script references are historical. The named superseded-claim grep
across touched skill/scorecard/log/index/intake/lesson/script found only
historical statements and explicit corrections, not a live unchecked-grep
diagnosis. No QUALITY criterion or non-author agree/disagree was invented.

**Verdicts:** operability improved, 0/3 → 3/3; depth, coverage, freshness,
calibration and adjacency unchanged (no broader measurements claimed).
Learning: expansion improved by the newly held intake form; quality and
discernment unchanged. No axis harmed, no scalar substitute, no promotion.
The old scope-finding requirement remains explicit debt, not a claimed
preserved executable boundary.

**Receipt prerequisite, not a local-code failure.** Launch metadata and the
exact Sighting mission entry provide run/session/mission IDs but no taskKey
or stored expected receipt bag. The configured canonical queue path
(`ufo-fsd-alpha/config/ufo.json:77`, `.ufo/pending-work.json`) is absent in
glob and directory read. The receipt API requires an authentic
`task_[24 lowercase hex]` key and dispatch-owned prompt/config bindings
(`scripts/ufo-mission-result.mjs:68-73,637-645,698-710,2707-2717`).
The applicable receipt cannot be truthfully minted by guessing those fields.
`.ufo/evidence/round-1/receipt-blocker.json` records the exact missing
authority and integrator unblock. No receipt or Sighting completion is
fabricated; receipt-backed completed rounds remain 0 pending acceptance.
The operator target remains at least 100, with no in-session second round.

The current launch overlay contains no role overrides (targeted grep of
`config/mission-nightcall.yml` found only maxConcurrency); global defaults
therefore still need operator-owned bindings before a new wave. This is
next-dispatch debt only; inherited round-1 routes are evidenced separately.
Reports/continuation remain lane-local. Native sessions, fleet ledgers and
shared reports are excluded from commits. Nothing is pushed.

### Round-1 publication — lane-local report and continuation

After work HEAD `cfb803a20ba6bf29ba977248bab41b939c7f2ea9` existed,
the lane wrote `.ufo/reports/round-1/chousa.md`, citing that HEAD and the
measured gate commit. Report SHA-256:
`ada72514590414e5daea12c0481c53927498eb0d37740f550969158f3e1aa2b6`.
`.ufo/continuations/round-1.json` binds the same work/report/evidence and
records all axes, learning trends, debt owners and concrete unblocks.
The report lands with this publication entry under the lane identity;
no shared report or ledger is updated.

Publication does not turn the receipt prerequisite into a pass: no genuine
receipt could be minted without the authentic queue identity/expected bag,
and no mint, shape-only validation, Sighting completion or successor launch
is invented. The integrator must resolve round-1 receipt acceptance first,
then release one fresh session for round 2. No second actual round was run
here; the 100-verified-round target remains unchanged.

## Round 2 — claim-vs-source verification (goal wave)

**Round 2 — goal-wave admission (2026-10-15).** Motivating evidence: the
round-1 registration (pre-register the local-only claim-verification fixture)
with routing now supplied by the operator's in-session direct dispatch.
Landed (evidence commit `c3df458`): gate `03a33244…` with `verify-claims`
(selftest 30 = +10; corpus-boundary canonicalization; verbatim spans;
line-aware misses; contradicted marker; exact counting); fixture
`corpus/fixtures/claims-r2.jsonl` (17 claims, provenance README);
`corpus/knowledge/claim-verification-r2.md`; lesson; four receipts.
**Receipt identity remains OPEN** — these receipts are lane-local evidence
logs, not queue taskKey/expected-receipt bags; proven receipt-backed
completed rounds remain 0 pending integrator binding (operator surface).

**Parent acceptance (2026-10-15T23:45Z).** selftest 30/30 exit 0;
`verify-claims corpus/fixtures/claims-r2.jsonl --root ..` →
`VERDICT_BEARING_CLAIMS=17/17`, `RESEARCH_GATE: CLEAN` exit 0 (13 supported /
2 contradicted / 2 unsupported); round-1 observable intact (VERDICT_BEARING_
EXPORTS=3/3). Acceptance note: the fixture sources are fleet-root-relative,
so the documented run requires `--root ..` — an acceptance run without it
refuses all sources correctly (boundary working as designed), and the parent
caught its own omission by reading the refusal lines.

**Verdicts.** ADMIT: coverage/depth/operability **improved**; freshness/
calibration/adjacency **unchanged**; none harmed. Named residuals: hardlink
canonicalization bypass; no claim-source size cap; r1 banner string. Round 3
registered: chain-hop resolution mode.

**Boundaries held.** Zero network (strace-confirmed); research corpus
read-only; no secrecy reads; seats committed nothing; parent integrated
under the chousa lane identity.

Round report: `.ufo/round-2/chousa-goalwave.md` (debts section carries the
receipt-identity note per the mission contract).

## Round 3 — verify-chain (goal wave)

**Round 3 — goal-wave admission (2026-10-15).** Motivating evidence: round 2's
named continuation (chain hops verified structurally only). Landed (evidence
commit `cc9fe8f`): gate `67daf85e…` with `verify-chain` (selftest 40 = +10;
source-id resolution through the Sources table; heading/quote/line anchors with
line reporting; exempt-but-counted unresolved hops; refused-unknown-ids);
fixture `corpus/fixtures/chain-r3.md` + broken control + README;
`corpus/knowledge/chain-resolution-r3.md`; receipts. Environmental: host /tmp
per-user quota exhausted by accumulated wave scratch mid-acceptance; parent
freed 727 MB of declared-ephemeral scratch; battery re-run clean.

**Parent acceptance (2026-10-16T00:15Z).** selftest 40/40 x2;
`verify-chain corpus/fixtures/chain-r3.md --root ..` -> `RESOLVED_HOPS=17/22`
CLEAN exit 0 (17 verified / 5 exempt); broken control DRIFT exit 1
(anchor-missing named); verify-claims 17/17 held byte-identical; r1 observable
3/3 intact.

**Verdicts.** ADMIT: coverage/depth/operability **improved**; freshness/
calibration/adjacency **unchanged**; none harmed. Named limit: substring
anchor semantics (truncated quotes resolve) — round 4 registered for
token-boundary hardening. Receipt identity remains OPEN (operator side).

**Boundaries held.** Zero network; corpus read-only; seats committed nothing;
parent integrated under the chousa lane identity.

Round report: `.ufo/round-3/chousa-goalwave.md`.

## Round 4 — anchor token boundaries (goal wave)

**Round 4 — goal-wave admission (2026-10-16).** Motivating evidence: round 3's
named limit (substring semantics; truncated quotes resolve). Landed (evidence
commit `a6f3118`): gate `6b83705b…` — one shared token-boundary matcher for
claims spans + chain quote anchors (char class in the header; `-`/`'`/
`_`/non-ASCII rules; fail-closed); selftest 44 = +4 with same-bytes-both-modes
cases; fixtures held (claims 17/17, chain 17/22 CLEAN; broken control DRIFT);
r1 observable 3/3. Wave: 32-seat flash call, 25/25. Environment: /tmp quota
held (quota-sentinel, ~700M headroom); seats cleaned scratch.

**Verdicts.** ADMIT: calibration/depth/operability **improved**; coverage/
freshness/adjacency **unchanged**; none harmed. Round 5 registered:
verify-sweeps — rejections + negative sweeps verdict-bearing (the last r1
structural axis). Receipt identity remains OPEN (operator side).

**Boundaries held.** Zero network; corpus read-only; seats committed nothing;
parent integrated under the chousa lane identity.

Round report: `.ufo/round-4/chousa-goalwave.md`.

## Round 5 — verify-sweeps (goal wave)

**Round 5 — goal-wave admission (2026-10-16).** Motivating evidence: the last
unmeasured r1 structural axis (rejections + sweeps structural only). Landed
(evidence commit `e7ab39a`): gate `55adb92d…` with `verify-sweeps` (selftest 54
= +10, 1-44 byte-identical) — rejections need reason + flip-condition; local
sweeps re-run for emptiness with planted hits named by path; exempt-but-counted
non-local class; fixture CLEAN (1/2 verified, 3/3 rejections), broken control
DRIFT naming both classes. claims 17/17 and chain 17/22 held. Wave: 32-seat
flash call, 27/27.

**Verdicts.** ADMIT: coverage/depth/operability **improved**; freshness/
calibration/adjacency **unchanged**; none harmed. Named limits (critic seats):
vacuous flip-conditions, narrow-sweep triviality — documented in the note.
Round 6 registered: `verify-all` composition (one record, one deep verdict
across all four modes) + the record's verification state lands in the lane's
manifest. Receipt identity remains OPEN (operator side).

**Boundaries held.** Zero network; corpus read-only; seats committed nothing;
parent integrated under the chousa lane identity.

Round report: `.ufo/round-5/chousa-goalwave.md`.

## Round 6 — verify-all composition (goal wave)

**Round 6 — goal-wave admission (2026-10-16).** Motivating evidence: no
composed verdict; no manifest. Landed (evidence commit `74c533d`): gate
`0c3d51ed…` with `verify-all` (selftest 64 = +10, 1-54 byte-identical) —
sections run as fresh solo invocations (tally-equal by construction),
composed CLEAN|DRIFT, absent!=drift, `--json` append-only manifest at
`corpus/evidence/verify-all-manifest.jsonl`. Full fixture CLEAN (4/4);
broken DRIFT with drift-sections=2; zero network (strace). Wave: 32-seat
flash call, 26/26.

**Verdicts.** ADMIT: operability/depth/freshness **improved**; coverage/
calibration/adjacency **unchanged**; none harmed. Named limit: absent!=drift
omission hole — r7 = binding integrity (cross-section references resolve,
fail-closed). Receipt identity remains OPEN (operator side).

**Boundaries held.** Zero network; corpus read-only; seats committed nothing;
parent integrated under the chousa lane identity.

Round report: `.ufo/round-6/chousa-goalwave.md`.

## Round 7 — verify-integrity (goal wave)

**Round 7 — goal-wave admission (2026-10-16).** Motivating evidence: round 6's
demonstrated dangling-reference hole. Landed (evidence commit `a1948c3`):
gate `3ba718bf…` with `verify-integrity` (selftest 74 = +10) — reference cells
across chain/claims/negatives/sweeps/rejections resolve against declared ids
fail-closed; exempt classes counted; fifth verify-all section. Fixture 16 refs
/ 15 resolved / 0 unresolved CLEAN; broken control DRIFT naming S9 + C9.
Wave: 32-seat flash call, 24/24.

**Verdicts.** ADMIT: coverage/depth/operability **improved**; freshness/
calibration/adjacency **unchanged**; none harmed. Round 8 registered: gate
behavioral baseline (--pin/--drift). Receipt identity remains OPEN (operator).

**Boundaries held.** Zero network; corpus read-only; seats committed nothing;
parent integrated under the chousa lane identity.

Round report: `.ufo/round-7/chousa-goalwave.md`.

## Round 8 — gate behavioral baseline (goal wave)

**Round 8 — goal-wave admission (2026-10-16).** Motivating evidence: no gate
baseline; regressions catchable only post-hoc. Landed (evidence commit
`LOGPEND8`): gate `46f5ddb3…` with `--pin`/`--drift` (selftest 85 = +11) —
canonical self-built fixture invocation, declared volatile contract
(ts/gate_sha256 shape-masked), GATE_DRIFT none/named-tokens/missing-malformed
under 0/1/2; catches measured: field mutant, silently-skipped mode
(-SECTION:sweeps), volatile-list rewrite. Lane baseline committed
(`corpus/evidence/gate-baseline-r8-20261016T033757Z.json`); parent drift
re-run `none` exit 0. Mori lineage declared. Wave: 32-seat flash call, 23/23.

**Verdicts.** ADMIT: freshness/operability/depth **improved**; coverage/
calibration/adjacency **unchanged**; none harmed. Round 9 registered: the
archived inputs through verify-all end-to-end + expanded fixtures. Receipt
identity remains OPEN (operator).

**Boundaries held.** Zero network; corpus read-only; seats committed nothing;
parent integrated under the chousa lane identity.

Round report: `.ufo/round-8/chousa-goalwave.md`.

## Round 9 — archives verified end-to-end (goal wave)

**Round 9 — goal-wave admission (2026-10-16).** Motivating evidence: no archive
had passed verify-all; claim coverage ~17. Landed (evidence commit
`LOGPEND9`): `corpus/fixtures/archives-r9/{A,B,C}-r9.md` + README + claims-r9
(10 new claims) — verify-all CLEAN on all three (zero findings: A 6/7 hops,
13 refs/0 unresolved; B 6/7, 14/0; C 7/8, 15/0; rejections 4/4, 3/3, 4/4;
sweeps 1/1 each). Honest premise correction: archives do not literally
cross-cite; hops authored intra-archive/conceptual. Gate unchanged (fixture-
led as designed). Wave: 32-seat flash call, 24/24.

**Verdicts.** ADMIT: coverage/depth/calibration **improved**; operability/
freshness/adjacency **unchanged**; none harmed. Round 10 registered: residual
hardening (archive-scale negative controls + exempt-hop audit + r2-r9 limit
disposition). Receipt identity remains OPEN (operator).

**Boundaries held.** Archives read-only; zero network; seats committed
nothing; parent integrated under the chousa lane identity.

Round report: `.ufo/round-9/chousa-goalwave.md`.

## Round 10 — negative controls + limit ledger (goal wave)

**Round 10 — goal-wave admission (2026-10-16).** Motivating evidence: no
archive-scale controls; no limit ledger. Landed (evidence commit
`LOGPEND10`): six controls under corpus/fixtures/archives-r9/controls/, each
DRIFTing verify-all with exactly one class-named finding (parent re-ran all
six); exempt audit clean; `corpus/knowledge/hardening-r10.md` = the r2-r9
limit-disposition ledger. Gate byte-unchanged. Wave: 32-seat flash call, 23/23.

**Verdicts.** ADMIT: calibration/coverage/depth **improved**; operability/
freshness/adjacency **unchanged**; none harmed. Named non-coverage:
RECORD_SCHEMA_INVALID fires with companions (documented). Round 11 registered:
the chousa capstone audit. Receipt identity remains OPEN (operator).

**Boundaries held.** Zero network; corpus read-only; no gate change; seats
committed nothing; parent integrated under the chousa lane identity.

Round report: `.ufo/round-10/chousa-goalwave.md`.

## Round 11 — capstone audit (goal wave)

**Round 11 — goal-wave admission (2026-10-16).** Motivating evidence: operator
goal — ten rounds each on mori and chousa; this closes chousa. Landed
(evidence commit `2e414ec`): `corpus/knowledge/audit-r11.md` — the
consolidated capstone audit: round 2's chain re-executed 15/15 supported at
frozen bytes; rounds 2-10 chains verified; the today's-bytes battery green
(selftest 85, drift none, fixtures/records/controls reproducing); the gate
byte-unchanged. Corrections folded: wave-seat-count claims unverifiable
without rosters (recorded; future rounds should log rosters); audit §5/§7
record-text defects carry [PARENT] markers; SHONEN 0/4 hold (no
self-attestation). chousa rounds 2-11: ten admitted rounds.

**Verdicts.** ADMIT-with-correction: calibration/depth **improved**; all else
**unchanged**; none harmed. Discernment trend: **improved**. Carried to the
operator: receipt identity (open since round 1), named-non-author SHONEN
verification, the promotion decision, and push (no lane remote exists for
either lane).

Round report: `.ufo/round-11/chousa-goalwave.md`.

## 2026-10-16 — protocol conformance: SCORECARD contract fields

**Operator rollout (2026-10-16 protocol amendment, fleet-root `84bade0`) — not a craft round.** Already present as recordable sections: axes (`## Axes`), planned (`## Planned`), retired (`## Retired`). Added by this rollout additively at file end: `## Capabilities` (repertoire-table scaffold, `— none yet —` row) and `## Saturation` (line + stagnation window N deferred to the lane's next round per `AXES.md` §The stagnation nudge).

No axis claim was made, no score moved, no verdict changed, no number invented; existing `SCORECARD.md` bytes unchanged (original 30128-byte prefix byte-identical, `sha256 2e802345c72f31197f83d400958816544d9cc0df7c365d2658687685d519c373`).

## 2026-10-17 — README: Devin wiki link

- Operator directive (2026-10-17): insert the Devin wiki link into the README header of every repository with a generated wiki.
- Change: `README.md` created (lane-header convention) with a `**Wiki:**` link to https://app.devin.ai/org/veigapunk/wiki/VeigaPunk/chousa-shokunin?branch=master.
- Evidence: the org's Devin wiki index lists this repo's generated wiki; sibling lane READMEs carry the same `**Wiki:**` header.
- Documentation-only change; no round run, no axis moved, no verdict changed.

## 2026-10-19 — round-12 opening: environment unblock, before-receipts, claim registration

- **Battery unblock.** `--selftest` failed with `cat: write error: Disk quota exceeded` — the host per-user /tmp quota (same class as round 3's mid-acceptance exhaustion; the tmpfs itself had 3.1G free). Freed 6.4G of stale declared-ephemeral wave scratch under /tmp: 14 dirs (`d23` 2.2G, `P1` 484M, `p6` 443M, `c1` 348M, `m1h24` 294M, `f2` 268M, `m5-probe` 258M, `h24-H8` 251M, `f4` 230M, `f2f-scout` 211M, `h6` 200M, `h11` 177M, `s6` 147M, `s2-opencode` 147M), each verified zero open handles (`lsof +D`) and untouched >60 min before deletion. After: tmpfs 6.6G/16G used; `RESEARCH_GATE_SELFTEST: PASS (85 cases)` exit 0; `GATE_DRIFT: none` exit 0 vs `corpus/evidence/gate-baseline-r8-20261016T033757Z.json`; r1 counting command `VERDICT_BEARING_EXPORTS=3/3`.
- **Before-observables re-measured.** `grep -c SCOPE_ tools/research-gate.sh` → 0 (the r1 scope-teeth landing requirement is still open); `VERSION=research-gate-r1` at `tools/research-gate.sh:227` (r2-carried cosmetic residual); no size cap on claim/chain source reads; the r11 audit's one open finding reproduced — `corpus/fixtures/archives-r9/A-r9.md` row C3 cites `A-shokunin-tradition.md:76`, the quoted span verified at `:86` (line 76 carries the finishing/competence/independence distinction; line 86 carries the quoted sentence).
- **Claims declared** (full text: SCORECARD.md §Planned — round 12): coverage = scope-refusal teeth; operability = banner + source size-cap residuals; calibration = close the A-r9 C3 finding. Wave: 64 seats, one batched AgentSwarm call, opencode-go key 1 / deepseek-v4.1-flash (curriculum loop 1 round 1; opencode-go keys rotate between rounds).

### Round-12 dispatch deviation (2026-10-19, operator directive)

The first round-12 wave (opencode-go key 1, 64 seats) was interrupted before any seat reported. Operator directive: move to another opencode-go key and stay on it until it fails. Round 12's wave re-dispatches on **opencode-go-2 / deepseek-v4.1-flash**, and subsequent rounds stay on opencode-go-2 (deviation from the between-round key rotation recorded here and in the round-12 report; the directive supersedes the rotation).

### Round-12 dispatch deviation 2 (2026-10-19, operator directive)

The key-2 wave (opencode-go-2, 64 seats) was also interrupted before any seat reported. Operator directive: move to the next opencode-go key and stay on it. Round 12's wave now re-dispatches on **opencode-go-3 / deepseek-v4.1-flash**, and per the standing directive subsequent rounds stay on opencode-go-3 until it fails. Two aborted 64-seat dispatches (keys 1 and 2) produced zero seat reports; the roster in the round-12 report records this honestly.

### Round-12 dispatch deviation 3 (2026-10-19, measured failure)

The key-3 wave (opencode-go-3, 64 seats) failed instantly and completely: every seat returned `402 Upstream request failed: Insufficient account funds` (64/64, no seat started). Key 3 is out of funds — a measured provider failure, not an interruption. Per the standing operator directive (move to the next opencode-go key, stick with it), round 12 re-dispatches on **opencode-go-4 / deepseek-v4.1-flash**.

### Round-12 dispatch deviation 4 (2026-10-19, measured failure)

The key-4 wave (opencode-go-4, 64 seats) failed instantly and completely: every seat returned `402 Upstream request failed: Insufficient account funds` (64/64). Keys 3 and 4 are both out of funds. Per the standing directive the lane probes the remaining opencode-go keys with a single cheap liveness agent before spending another 64-seat wave; the wave re-dispatches on the first key that answers and stays there.

### Round-12 key selection (2026-10-19, measured)

Liveness probes (single agent, reply "alive"): opencode-go-5 → `402 Insufficient account funds`; **opencode-go-6 → alive**. Keys 3, 4, 5 are out of funds; keys 1 and 2 were abandoned on operator interruption before any seat reported (unmeasured). Per the standing operator directive, the lane sticks with **opencode-go-6 / deepseek-v4.1-flash** for round 12's wave and subsequent rounds until it fails.

## Round 12 — goal wave (2026-10-19)

**Admission.** Landed (evidence commit `5691bf531086dd435006cd9d6157df00933973a3`; wave: one 64-seat AgentSwarm call on opencode-go-6 / deepseek-v4.1-flash, 64/64 seat reports; key selection history in the deviation entries above):

- **Claim 1 (coverage) — scope-refusal teeth** (the r1 landing requirement): `scope_decl_screen` reads only `## Meta` rows keyed `domain`/`scope` (table + `key: value` forms; prose never scanned); refused-province declarations emit `SCOPE_BOUNTY_ABSORBED` / `SCOPE_MODEL_QUALITY_ABSORBED` / `SCOPE_ORCHESTRATION_ABSORBED` at warn (drift, exit 1), one finding per matched province per declaration row; 7 selftest cases (86–92); canary `verify B-r9` → 0 `SCOPE_` findings. Observable: emitting assignments `grep -c 'id=SCOPE_'` → 3 (amended from the bare `SCOPE_` count, conformance reviewer D3 — docs/fixture mentions would over-count).
- **Claim 2 (operability) — r2-carried residuals**: (a) `VERSION=v2` (banner contract; six sites; cases 93–94 incl. the `GATE_DRIFT: GATE` mutant arm); (b) 8 MiB source-read cap at the shared `claim_source_path` chokepoint (`CLAIM_SOURCE_READ_TOO_LARGE` / `CHAIN_SOURCE_READ_TOO_LARGE`, warn, refused before any read; cases 95–98 straddle 8388608/8388609, over-cap span on line 1 proving never-partially-read). Namespacing the pre-registered bare `SOURCE_READ_TOO_LARGE` to the mode idiom is a recorded amendment (seats 18/36). **Companion deviation (recorded)**: `count_nl` was quadratic (>60 s at 8 MiB, measured by the seat) — replaced with the linear `tr -dc '\n' | wc -c` (~3 ms); behavior-identical, without it the cap would be operability theatre.
- **Claim 3 (calibration) — closed as debt-closure, axis unchanged** (per the wave reviewers; claiming "improved" would double-count the r11 audit): A-r9.md C3 `:76` → `:86` (new sha `dfd2ae1a…` exactly as predicted); post-fix verify-all CLEAN; parent re-sweep 19/19; controls stay byte-copies of the pre-fix base (desync note); append-only errata to `audit-r11.md` and `hardening-r10.md` §6 (rows 9/10/56/70 dispositioned; 71 rows → 38·23·7·0·3, queue 26); pin cascade (archives-r9 README, claims-r9 README, archives-verified-r9, corpus/README, evidence README, SKILL.md, 5 knowledge-note dispositions). The class (pointer-line vs span-line) stays a named non-coverage.
- **Forced + recorded re-pin**: `--drift` vs the r8 baseline reads `GATE_DRIFT: GATE record_sha256` exit 1 (VERSION v2 + the pin fixture's clean domain row, both unmasked contract words); one re-pin at final bytes: `corpus/evidence/gate-baseline-r12-20261019T115519Z.json` (`GATE_PIN: ok`, immediate `GATE_DRIFT: none`); reason in `corpus/knowledge/gate-baseline-r12.md`.
- **Battery** (receipts `corpus/evidence/scope-r12-20261019T115519Z-*.log`): selftest `PASS (98 cases)`, cases 1–85 `cmp` byte-identical vs the r8 receipt; r1 `3/3`; fixture battery (A/B/C-r9, r6 trio, r7 pair, claims-r2, chain-r3, sweeps-r5, six controls) byte-identical vs the pre-round gate modulo masked banner/ts; zero network; gate `46f5ddb3…` → `91a01695…`.

**Verdicts** (full table: SCORECARD.md §Round 12 verdict): coverage/operability/freshness(narrow)/depth **improved**; calibration **unchanged** (debt closure); adjacency **unchanged**; none harmed. **ADMIT.** Learning trends: expansion/quality improved; discernment unchanged. Capabilities table gained three rows (screening, cap, banner contract).

**Corrections to prior entries (append-only, per the r11 audit D3):** the round-8/9/10 goal-wave entries above carry the placeholders `LOGPEND8`/`LOGPEND9`/`LOGPEND10`; the evidence commits they name at those rounds' admission were `27b55c3` (r8), `ebd04d2` (r9), `5f99fa3` (r10) as recorded in each round's SCORECARD verdict block — the placeholders were never resolved to hashes in this file; resolved here.

**Boundaries held.** Zero network; research corpus read-only; seats committed nothing (read-only wave); parent integrated under the lane identity; no pushes (goal boundary; the origin remote exists and master is ahead 7 — push is an operator/integrator call, noted for the record). Receipt identity remains OPEN (re-filed to the fleet L0 queue this round — see the round-12 report). Round 13 registered in SCORECARD §Planned.

## 2026-10-19 — round-13 opening: claims, before-receipts, dispatch

- **Before-observables** (at HEAD 91aebd3, after the round-12 battery): selftest `RESEARCH_GATE_SELFTEST: PASS (98 cases)`; drift vs the r12 baseline `GATE_DRIFT: none`; r1 counting command `VERDICT_BEARING_EXPORTS=3/3`; inode/hardlink logic in the gate: `grep -c samefile tools/research-gate.sh` → 0; multi-linked files across corpus/tools/research: 0 (so the fix cannot perturb any existing fixture by construction — to be re-measured by the wave).
- **Claims** (pre-registered SCORECARD.md §Planned — round 13; curriculum loop 1 round 2): coverage = close the last r2 residual — in-root hardlink canonicalization (ledger row 8): a claims/chain source cited through an in-root hardlink alias of an out-of-corpus file is read today; after: refused (named finding) or canonicalized to the inode-true path with the boundary re-checked, plus symmetric selftest fixtures and the hold battery green. depth = the alias-semantics knowledge note (what readlink -f does and does not prove about inodes; refusal semantics; named limits) + SKILL.md registry sweep. The stagnation nudge stays dormant (operability 3 is the only score; claim 1 lands on coverage, claim 2 on depth — the round works the registered row-8 class).
- **Wave**: one batched AgentSwarm call, 64 seats, opencode-go-6 / deepseek-v4.1-flash (standing directive: stick with key 6). Seat roster lands in the round-13 report.

## Round 13 — goal wave (2026-10-19)

**Admission.** Landed (evidence commit this entry; wave: one 64-seat AgentSwarm call on opencode-go-6 / deepseek-v4.1-flash, 64/64 seat reports):

- **Claim 1 (coverage) — hardlink-alias boundary** (the last r2 residual, ledger row 8): the wave's enumeration designs were BLOCKed as unsound (order dependence, nested/bind-mounted roots); the landing is a one-probe `stat -c '%s %h'` check at the shared `claim_source_path` chokepoint (one probe now serves the r12 size cap and the r13 alias check): `nlink != 1` → refused unread, `CLAIM_SOURCE_MULTILINKED` / `CHAIN_SOURCE_MULTILINKED`, crit, per-item `observed=refused`. Claim re-scoped per the reviewers: the HARDLINK class closes; bind mounts (nlink=1, stat-invisible), TOCTOU, unmeasurable-stat fallback, and legit in-root multi-link families refusing are named limits (`corpus/knowledge/hardlink-alias-r13.md`), case 101 pins the family trade. The bypass is proven live: `corpus/evidence/alias-r13-20261019T123621Z-bypass-before.log` reads `observed=supported` CLEAN at the pre-round gate; `-after.log` refuses crit at the landed gate.
- **Claim 2 (depth)**: `corpus/knowledge/hardlink-alias-r13.md` + lesson `2026-10-19-hardlink-alias-boundary.md` + SKILL.md paragraph/table sweep.
- **Battery**: selftest `PASS (102 cases)` (98+4), cases 1–98 `cmp` byte-identical; r1 `3/3`; drift `none` vs the r12 baseline (no re-pin — canonical invocation unchanged); masked battery vs the pre-round gate with LANE_ROOT intact (temp copy inside `tools/`; the /tmp-copy form breaks lane-root-relative pointer resolution — sweeps-r5 S4 — a recorded method artifact) ALL IDENTICAL; zero network. Gate `91a01695…` → `6b17e50c…`.
- **Errata/records**: hardening-r10 round-13 addendum (row 8 closed(r13, hardlink class); carried limits inside the closure; 71 rows → **by-design 38 · carried 22 · closed 8 · finding 0 · operator 3**, queue 26 → 25); corpus/README carried-residuals line + knowledge-index row; evidence/README receipt rows; SKILL.md registry sweep.
- **Verdicts** (SCORECARD §Round 13 verdict): coverage/operability/depth/freshness(narrow) **improved**; calibration/adjacency **unchanged**; none harmed. **ADMIT.** Capabilities +1 (hardlink-alias refusal). Learning: expansion/quality improved, discernment unchanged. Round 14 registered (curriculum round 3: zai glm-5.3-flash; fallback key 6 if zai is out; claim from the named-limit queue, pre-registered at opening).

**Boundaries held.** Zero network; research corpus read-only; seats read-only; lane-identity pathspec-limited commits; no pushes (8 → 11 local commits; push remains operator/integrator-owned). Receipt identity still OPEN (L0 row filed at round 12, unanswered — routed around).

### Round-14 provider deviation (2026-10-19, operator directive)

Operator directive: **use the token-plan lanes for the deepseek-v4.1-flash swarms** instead of opencode-go. Standing assignment from round 14: deepseek-v4.1-flash waves run on **alibaba-token-plan** (keys -2/-3 are the overflow ladder; stick with the first working key per the standing doctrine, probing liveness before each wave). Round 13 and earlier ran on opencode-go-6 (recorded history, unchanged).

## 2026-10-19 — round-14 opening: claims, before-receipts, dispatch

- **Claims** (curriculum loop 1 round 3): coverage/operability = the mount-alias (bind) boundary — refuse claim/chain sources whose `st_dev` differs from the resolving root's device (`CLAIM_SOURCE_CROSS_DEVICE` / `CHAIN_SOURCE_CROSS_DEVICE`), closing the named residual the r13 reviewers carved out (same-device binds remain a named limit — stat cannot see them); the wave validates the unprivileged fixture strategy (user-namespace bind if available on this host; otherwise an absolute-path cross-device fixture) and BLOCKs to a documented named-limit if no sound check exists. depth = the mount/alias note (device semantics, why %d, the same-device-bind honesty) + registry sweep. Before: `grep -c CROSS_DEVICE tools/research-gate.sh` → 0; device logic absent.
- **Before-receipts**: selftest `PASS (102 cases)`; drift `none` vs the r12 baseline; r1 `3/3`; st_dev probes absent (to be re-measured by the wave).
- **Wave**: one batched AgentSwarm call, 64 seats, **alibaba-token-plan / deepseek-v4.1-flash** (operator directive above). Seat roster lands in the round-14 report.

## Round 14 — goal wave (2026-10-19)

**Admission.** Landed (evidence commit this entry; wave: one 64-seat AgentSwarm call on **alibaba-token-plan / deepseek-v4.1-flash** per the operator's token-plan directive, 63/64 reports — seat 54 failed on a provider content-filter 400; deficit recorded, not backfilled):

- **Claim 1 (coverage/operability) — mount-alias boundary**: the chokepoint now tracks the RESOLVING root (longest-prefix rule — the wave proved a ROOT-only compare false-refuses the live sweeps-r5 S4 lane-fallback case and the selftest itself) and one `stat -c '%s %h %d'` probe serves nlink (r13) → size (r12) → device (r14); `CLAIM_SOURCE_CROSS_DEVICE` / `CHAIN_SOURCE_CROSS_DEVICE` (crit) refuse cross-device sources unread. The mount-free "absolute-path" fixture was BLOCKed as unsound (two seats, measured); the fixture is a user+mount-namespace tmpfs forge (unprivileged on this host; a repo bind inside the ns is refused, rc=2). Live before/after receipts `corpus/evidence/mount-r14-20261019T125621Z-bypass-{before,after}.log`.
- **Claim 2 (depth)**: `corpus/knowledge/mount-alias-r14.md` + SKILL paragraph/table sweep; named limits: same-device binds (stat-invisible), overlay roots (file-vs-root-dir comparison breaks), TOCTOU, unmeasurable-stat fallback, legit cross-device subtrees refusing; **discovered and queued: the `--root /` boundary dead-arm** (`case "$canon" in "$root_r"/*` → `//*`, every source refuses; fix `"${root_r%/}"/*` named, not landed — outside the r14 claim).
- **Battery**: selftest `PASS (106 cases, 0 skipped)`, cases 1–102 `cmp` byte-identical; r1 `3/3`; drift `none` vs the r12 baseline (no re-pin); masked battery vs the pre-round gate (LANE_ROOT intact, r13 method) ALL IDENTICAL; zero network. Gate `6b17e50c…` → `d8bbd0bf…`.
- **Errata/records**: hardening-r10 round-14 addendum (E3: the E2-carried bind item closes; 71 rows → **by-design 38 · carried 21 · closed 9 · finding 0 · operator 3**; queue 25 → 25, the `--root /` item in, bind item out); corpus/README + evidence/README + SKILL sweeps.
- **Verdicts** (SCORECARD §Round 14): coverage/operability/depth/calibration(narrow) **improved**; freshness/adjacency **unchanged**; none harmed. **ADMIT.** Capabilities +1. Round 15 registered (curriculum round 4: zai glm-5.3-flash, 32–64 seats; fallback ladder token-plan → devin → opencode-go-6).

**Boundaries held.** Zero network; research corpus read-only; seats read-only; lane-identity pathspec-limited commits; no pushes. Receipt identity still OPEN (L0 row from round 12 unanswered — routed around).

## 2026-10-19 — round-15 opening: claims, before-receipts, dispatch

- **Claims** (curriculum loop 1 round 4): coverage/operability = fix the `--root /` boundary dead-arm discovered by the round-14 wave: `case "$canon" in "$root_r"/*` renders as `//*` when `root_r=/`, matching nothing, so every source refuses OUT_OF_CORPUS (live demo this opening: a claim citing `/etc/hostname` with `--root /` refuses `CLAIM_SOURCE_OUT_OF_CORPUS` crit; `/etc/hostname` is dev 31 = root dev, nlink 1, 17 B — a legitimate read blocked purely by the pattern bug). After: `"${root_r%/}"`-normalized prefix matching (src_root still stat'ed as `/`), symmetric treatment of the lane-root pattern, selftest case(s) incl. the absolute-path reads + the before-behavior pinned; sweeps' separate resolver audited for the same class. depth = the root-normalization note (glob mechanics of `//*`, why only absolute paths bite, the normalized-match contract) + registry sweep.
- **Before-receipts**: selftest `PASS (106 cases, 0 skipped)`; drift `none` vs the r12 baseline; r1 `3/3`; the dead-arm demo above (recorded in the round-15 receipts).
- **Wave**: one batched AgentSwarm call, 48 seats (curriculum 32–64), **zai glm-5.3-flash** (liveness-probed alive this opening; fallback ladder per the standing record: devin deepseek → token-plan deepseek → opencode-go-6). Seat roster lands in the round-15 report.

## Round 15 — goal wave (2026-10-19)

**Admission.** Landed (evidence commit this entry; wave: one 48-seat AgentSwarm call on **zai glm-5.3-flash** per the round-15 opening, 48/48 seat reports):

- **Pre-registration correction (measured, keeps the wave off a green-but-unfixed landing):** the opening's one-token fix `"${root_r%/}"/*` is a **no-op at `root_r=/`** in `case` patterns on bash 5.3.15 — a quoted operator expansion whose result is empty leaves the adjacent glob non-special: `case /etc/hostname in "${root_r%/}"/*)` → no match (reproduced ×3; the two-step form `rr="${root_r%/}"; case … in "$rr"/*)` matches). At normal roots the inline form matches, so all 106 existing selftest cases would stay green with the dead-arm unrepaired — the trap is invisible to the suite. Landed shape: the `in_root()` helper (`tools/research-gate.sh` ~:612) materializes `r=${2%/}` then tests `[[ $c == "$r" || $c == "$r"/* ]]` — version-independent by construction, and the `== "$r"` arm keeps the root-directory edge hitting the boundary then failing `-f` → `MISSING`.
- **Claim 1 (coverage/operability) — the `--root /` boundary dead-arm**: absolute in-`/` sources read after the fix; before-behavior pinned. Three same-class sites converted: `claim_source_path` (:1044-1075), `ptr_resolves_meta` (:546-551 — the third site, found by this round's registry sweep, not named in the opening), `sweep_path_guarded` (:1750-1756). `src_root` keeps the un-normalized root so the r14 device probe still stats the declared root. Live before/after receipts `corpus/evidence/root-r15-20261019T152000Z-demo.log` (a `/etc/hostname` claim: dev 31 = root dev, nlink 1, 9 B — legitimate read blocked purely by the pattern → `CLEAN` `1/1`). Selftest cases 107–110 (ghost-missing, `/etc/hostname` read, tmpfs cross-device, sweeps absolute glob); cases 1–106 `cmp` byte-identical. The `CHOUSA_ROOT=` override rides a new harness channel — six runners gained a `^CHOUSA_[A-Z_]+=` env-override classifier; `tcase`'s override placement corrected to last-wins.
- **Claim 2 (depth)**: `corpus/knowledge/root-slash-boundary-r15.md` — the `//*` glob mechanics (measured), the four-outcome pre-fix table (absolute-existing → OUT_OF_CORPUS; root-relative-existing → same; absolute-absent → OUT_OF_CORPUS mislabeled; relative-absent → MISSING via the `//`-canon artifact), the `in_root` contract, the 3-site registry, the inline-strip quirk, named limits.
- **Battery**: selftest `PASS (110 cases, 0 skipped)`; r1 `3/3`; drift `none` vs the r12 baseline (no re-pin); masked battery vs the pre-round gate (LANE_ROOT intact, r13 method) ALL IDENTICAL; zero network. Gate `d8bbd0bf…` → `dd0951d7…`.
- **Errata/records**: hardening-r10 round-15 addendum (E4: the E3-queued `--root /` item closes; 71 rows → **by-design 38 · carried 21 · closed 10 · finding 0 · operator 3**; queue 25 → 24; the dead-arm closure is a queue-item closure, not a row closure — the E3 phantom-count explained); **append-only LOG correction: the round-14 admission entry (`LOG.md:596`) cites bypass receipts `…125621Z-…`; the on-disk files are `mount-r14-20261019T132025Z-bypass-{before,after}.log` (typo already corrected at `hardening-r10.md:516-518`; LOG itself was never)**; corpus/README + evidence/README + SKILL sweeps.
- **Verdicts** (SCORECARD §Round 15): coverage/operability/depth/calibration(narrow) **improved**; freshness/adjacency **unchanged**; none harmed. **ADMIT.** Capabilities +1. Round 16 registered (curriculum round 5: gpt-6-luna-max, 64 seats — verification wave re-auditing loop-1 rounds 1–4).

**Boundaries held.** Zero network; research corpus read-only; seats read-only; lane-identity pathspec-limited commits; no pushes. Receipt identity still OPEN (L0 row from round 12 unanswered — routed around). Round report: `.ufo/reports/round-15/chousa.md` (seat roster lands there, per the r11 correction).

## 2026-10-19 — round-16 opening: claims, before-receipts, dispatch

- **Claims** (curriculum loop 1 round 5 — verification wave): coverage/calibration = adversarially re-audit the current loop's rounds 1–4 (lane rounds 12–15) for correctness defects and missed coverage; every finding lands as a dispositioned item (fix, absorb, or named debt). The audit surface: the boundary stack (scope refusal cases 86–92, size cap 95–98, hardlink 99–102, cross-device 103–106, root-slash 107–110), the gate's refusal/finding registry, the knowledge notes' measured claims, and the selftest harness itself. operability = the audit's own receipts.
- **Before-receipts**: selftest `PASS (110 cases, 0 skipped)`; drift `none` vs the r12 baseline; r1 `3/3`; gate `dd0951d7…`; HEAD `58cf0b9`.
- **Wave**: one batched AgentSwarm call, 64 seats (curriculum 64), **openai-codex gpt-6-luna-max** (liveness-probed alive this opening; fallback ladder per the standing record: devin → token-plan → opencode-go-6). Seat roster lands in the round-16 report.

## Round 16 — goal wave (2026-10-19)

**Admission.** Landed (evidence commit this entry; wave: one 64-seat AgentSwarm call on **openai-codex gpt-6-luna-max** per the round-16 opening, 64/64 seat reports — zero deficit):

- **Verification verdict**: the boundary stack (rounds 12–15) is sound — no out-of-corpus read found, no refusal class broken. The wave's findings are ~2 fixes, ~15 absorbs, ~12 named debts.
- **Fix 1 — `--root //` still refused** (seats 09, 10, 52): `in_root` stripped only one `/`, leaving `/` which still rendered `//*`. The loop now strips all trailing slashes; case 111 pins it. `cd // && pwd -P` → `//` measured.
- **Fix 2 — r15 battery receipt wrong fixture paths** (seats 32, 62): A/B/C-r9 under `corpus/fixtures/` not `archives-r9/`; `--root .` vs `--root ..`. Re-run with correct paths, masked diff IDENTICAL; receipt replaced.
- **Absorbs** (~15): `wc -c` fallback reads to measure (not to search) — named limit corrected in mount-alias-r14; scope-refusal coverage overstatement corrected; full-r6 README sweeps-absent corrected; mount-alias "queued" item closed; stale hardlink status in older notes absorbed; hardening-r10 count phantom explained; `ptr_resolves_meta` coverage gap named; empty-claims vacuous-pass documented; FAIL-summary skip asymmetry absorbed; chain kind-blindness already carried; r15 roster internally complete (wave file in session log); conformance exploratory-claim rule scoped; `--` delimiter edge absorbed; URI-like citation classification named; manifest outside-root documented.
- **Named debts** (~12, round-17 queue): scope-screen fenced-heading shadow, `LLM benchmarks` phrase gap, sweeps symlink-escape guard, `--drift` truncated-baseline ambiguity, `--json` delimiter edge, manifest timestamp mask breadth, secret-scan source coverage, bash-3 portability, 8 unasserted finding IDs, TOCTOU readability, relative-root missing-path severity, `--` delimiter handling.
- **Battery**: selftest `PASS (111 cases, 0 skipped)`, cases 1–110 `cmp` byte-identical vs the r15 receipt; r1 `3/3`; drift `none` vs the r12 baseline (no re-pin); corrected masked battery vs the pre-round gate ALL IDENTICAL; zero network. Gate `dd0951d7…` → `<FILL>`.
- **Errata/records**: `corpus/knowledge/verification-r16.md` (the full disposition table); `corpus/knowledge/mount-alias-r14.md` (unmeasurable-stat corrected, queued item closed); `corpus/knowledge/scope-refusal-r12.md` (coverage overstatement corrected); `corpus/fixtures/full-r6.README.md` (sweeps-absent corrected); `corpus/README.md` (verification-r16 row); `SKILL.md` (110→111, r15 paragraph updated for `//`); SCORECARD verdict + round-17 registration.
- **Verdicts** (SCORECARD §Round 16): operability/depth/calibration **improved**; coverage/freshness/adjacency **unchanged**; none harmed. **ADMIT.** Capabilities +0 (verification round — no new capability, the existing stack verified). Round 17 registered (curriculum round 6: xai-oauth grok-4.7-fast, 32–64 seats).

**Boundaries held.** Zero network; research corpus read-only; seats read-only; lane-identity pathspec-limited commits; no pushes. Receipt identity still OPEN (L0 row from round 12 unanswered — routed around). Round report: `.ufo/reports/round-16/chousa.md` (seat roster lands there).

## 2026-10-19 — round-17 opening: claims, before-receipts, dispatch

- **Claims** (curriculum loop 1 round 6): coverage/operability = fix the scope-screen fenced-heading shadow (round-16 named debt): `load_sections` resets on every `## ` line without recognizing fenced code blocks, so a `## Meta` inside a fence shadows the real declaration — the scope screen then checks the wrong body. Fix: recognize fenced blocks and skip headings inside them. depth = the fenced-heading mechanics note + the `LLM benchmarks` phrase gap disposition.
- **Before-receipts**: selftest `PASS (111 cases, 0 skipped)`; drift `none` vs the r12 baseline; r1 `3/3`; gate `2b64a1c8…`; HEAD `0a2d7ce`.
- **Wave**: one batched AgentSwarm call, 32–64 seats (curriculum 32–64), **xai-oauth grok-4.7-fast** (liveness-probed alive this opening; fallback ladder per the standing record: devin → token-plan → opencode-go-6). Seat roster lands in the round-17 report.

## Round 17 — goal wave (2026-10-19)

**Admission.** Landed (evidence commit this entry; wave: one 32-seat AgentSwarm call on **opencode-go / deepseek-v4.1-flash** — xai-oauth grok-4.7-fast failed on 403 quota for all 48 seats, then zai glm-5.3-flash was interrupted at 14/48 before the re-dispatch landed on opencode-go; 27/32 seat reports — 5 failed on provider 400 `reasoning_content` errors; deficit recorded, not backfilled):

- **Claim 1 (coverage/operability) — the fenced-heading shadow**: `load_sections` splits on every `## ` line with no fence state — a `## Meta` inside a fenced code block resets the real Meta body, so the scope screen checks the wrong declaration. A record with `domain: bounty program scope` in its real Meta plus a fenced `## Meta` declaring `deep-research method` passed CLEAN (live demo: pre-round gate → CLEAN; landed → `SCOPE_BOUNTY_ABSORBED` warn + DRIFT; receipt `fence-r17-20261019T171200Z-demo.log`). The fix pairs fences in two passes — same char must close, closing length >= opening, 0–3 literal-space indent; an unclosed opener IS a fence (fail closed — everything after it is literal). The naive `^``` ` toggle fixes only the simple shadow (the wave's seat-30 verifier measured it still opens on nested 4-backtick, indented closers, and unclosed fences — all five variants now refuse).
- **Claim 2 (depth)**: `corpus/knowledge/fenced-heading-r17.md` — the shadow mechanics, the naive-vs-two-pass measured shape matrix, the call-site audit (load_sections serves every mode; no caller depends on fenced headings), and named limits (fenced data rows inside a real section are still scanned; the gate is not a Markdown renderer).
- **Battery**: selftest `PASS (116 cases, 0 skipped)`, cases 1–109 `cmp` byte-identical vs the r15 receipt (r16 inserted case 110 — the cmp boundary is 109, not 111); r1 `3/3`; drift `none` vs the r12 baseline (no re-pin); masked battery vs the pre-round gate (LANE_ROOT intact, r13 method) ALL IDENTICAL; zero network. Gate `2b64a1c8…` → `c2915f24…`.
- **Errata/records**: the `LLM benchmarks` phrase gap stays named debt (not silently absorbed); the provider deviation is recorded (xai 403 → zai interrupted → opencode-go); `corpus/README` + `evidence/README` + SKILL sweeps; SCORECARD verdict + round-18 registration.
- **Verdicts** (SCORECARD §Round 17): coverage/operability/depth/calibration(narrow) **improved**; freshness/adjacency **unchanged**; none harmed. **ADMIT.** Capabilities +1. Round 18 registered (curriculum round 7: zai glm-5.3-flash, 16–32 seats; fallback ladder per the standing record).

**Boundaries held.** Zero network; research corpus read-only; seats read-only; lane-identity pathspec-limited commits; no pushes. Receipt identity still OPEN (L0 row from round 12 unanswered — routed around). Round report: `.ufo/reports/round-17/chousa.md` (seat roster lands there).

## 2026-10-19 — round-18 opening: claims, before-receipts, dispatch

- **Claims** (curriculum loop 1 round 7): coverage = close the `LLM benchmarks` phrase gap (round-16 named debt): `SCOPE_KENGAKU` has `model benchmark(s)` but not `llm benchmark(s)`/`llm scoring`/`ai benchmark(s)` — a record declaring `domain: LLM benchmarks` passes CLEAN despite the model-quality boundary. The fix adds the missing phrases to `SCOPE_KENGAKU`; the wave audits the other two province lists for the same class. operability = the phrase-gap selftest cases.
- **Before-receipts**: selftest `PASS (116 cases, 0 skipped)`; drift `none` vs the r12 baseline; r1 `3/3`; gate `c2915f24…`; HEAD `02b70c0`.
- **Wave**: one batched AgentSwarm call, 16 seats (curriculum 16–32), **openai-codex gpt-6-luna-max** — zai glm-5.3-flash quota exhausted; operator directed codex luna max for all zai-assigned rounds until tomorrow. Deepseek waves use opencode-go key 6. Seat roster lands in the round-18 report.

## Round 18 — goal wave (2026-10-19)

**Admission.** Landed (evidence commit this entry; wave: one 16-seat AgentSwarm call on **openai-codex gpt-6-luna-max** per the round-18 opening — zai glm-5.3-flash quota exhausted, operator directed codex luna max for all zai-assigned rounds until tomorrow; 16/16 seat reports — zero deficit):

- **Claim 1 (coverage/operability) — the SCOPE_KENGAKU phrase gap**: `SCOPE_KENGAKU` covered `model benchmark(s)` and `model scoring` but not `llm benchmark(s)`/`llm scoring` — a record declaring `domain: LLM benchmarks` passed CLEAN despite the model-quality boundary (live demo: pre-round gate → CLEAN; landed → `SCOPE_MODEL_QUALITY_ABSORBED` warn + DRIFT; receipt `scope-r18-20261019T173000Z-demo.log`). `scope_hit` matches literal phrases after `scope_norm` lowercases and folds punctuation; it never stems, so `llm benchmarks` needs its own entry — `model benchmarks` does not cover it. The conservative 3-phrase set landed (`llm benchmark|llm benchmarks|llm scoring`); `ai benchmark(s)` stays named debt — the wave's adversary seats measured it too broad for AI-methodology research. Cases 117–119 pin the new phrases + the prose-only control.
- **Claim 2 (depth)**: `corpus/knowledge/scope-phrase-gap-r18.md` — the gap mechanics, the conservative-vs-broad fix boundary, the audit's other inflection findings dispositioned (`bug bounties`, `dispatch mechanisms`, `llm evaluations`, `llmbenchmark` camel-case, `language model benchmark(s)` all named debt).
- **Battery**: selftest `PASS (119 cases, 0 skipped)`, cases 1–116 `cmp` byte-identical vs the r17 receipt; r1 `3/3`; drift `none` vs the r12 baseline (no re-pin); masked battery vs the pre-round gate (LANE_ROOT intact, r13 method) ALL IDENTICAL; zero network. Gate `c2915f24…` → `6e694881…`.
- **Errata/records**: the provider deviation is recorded (zai exhausted → luna); `corpus/README` + `evidence/README` + SKILL sweeps; SCORECARD verdict + round-19 registration.
- **Verdicts** (SCORECARD §Round 18): coverage/operability/depth/calibration(narrow) **improved**; freshness/adjacency **unchanged**; none harmed. **ADMIT.** Capabilities +1. Round 19 registered (curriculum round 8: openai-codex gpt-6-luna-max, 16–32 seats — zai exhaustion directive).

**Boundaries held.** Zero network; research corpus read-only; seats read-only; lane-identity pathspec-limited commits; no pushes. Receipt identity still OPEN (L0 row from round 12 unanswered — routed around). Round report: `.ufo/reports/round-18/chousa.md` (seat roster lands there).

## 2026-10-19 — round-19 opening: claims, before-receipts, dispatch

- **Claims** (curriculum loop 1 round 8): coverage/operability = the sweeps symlink-escape guard (round-16 named debt): `sweep_path_guarded` canonicalizes the glob's BASE directory but a wildcard inside a symlinked dir can match files outside the allowed roots — the guard sees the symlink's target (inside root) while the glob expands to the target's children (which may be outside). The fix must canonicalize each glob MATCH, not just the base. depth = the symlink-escape mechanics note + the remaining named-debt dispositions.
- **Before-receipts**: selftest `PASS (119 cases, 0 skipped)`; drift `none` vs the r12 baseline; r1 `3/3`; gate `6e694881…`; HEAD `71b0b5f`.
- **Wave**: one batched AgentSwarm call, 16 seats (curriculum 16–32), **openai-codex gpt-6-luna-max** (zai exhaustion directive). Seat roster lands in the round-19 report.

## Round 19 — goal wave (2026-10-19)

**Admission.** Landed (evidence commit this entry; wave: one 16-seat AgentSwarm call on **openai-codex gpt-6-luna-max** per the zai-exhaustion directive, 16/16 seat reports — zero deficit):

- **Claim 1 (coverage/operability) — the sweeps symlink escape**: `sweep_path_guarded` canonicalizes the glob's literal BASE but not each match — a wildcard inside an in-root dir can match a symlink whose target is outside both roots (live demo: pre-round gate → `SWEEP_CLAIM_FALSE` hit on an outside symlink; landed → `SWEEP_LOCATION_OUT_OF_CORPUS` crit + refused; receipt `symlink-r19-20261019T174500Z-demo.log`). Two escape shapes closed: leaf symlink (`dir/*.md`) and directory symlink (`dir/*/*.md`). The fix canonicalizes every expanded match against `in_root` for both roots; any escape refuses the whole sweep.
- **Claim 2 (depth)**: `corpus/knowledge/sweep-symlink-r19.md` — the escape mechanics, the fix contract, the named limits (post-expansion check — bash already traversed the symlinked dir during glob expansion; TOCTOU; `--root /` vacuous by declaration).
- **Battery**: selftest `PASS (122 cases, 0 skipped)`, cases 1–119 `cmp` byte-identical vs the r18 receipt; r1 `3/3`; drift `none` vs the r12 baseline (no re-pin); masked battery vs the pre-round gate (LANE_ROOT intact, r13 method) ALL IDENTICAL; zero network. Gate `6e694881…` → `9f163807…`.
- **Errata/records**: `corpus/README` + `evidence/README` + SKILL sweeps; SCORECARD verdict + round-20 registration.
- **Verdicts** (SCORECARD §Round 19): coverage/operability/depth/calibration(narrow) **improved**; freshness/adjacency **unchanged**; none harmed. **ADMIT.** Capabilities +1. Round 20 registered (curriculum round 9: openai-codex gpt-6-luna-max, 64–128 seats — zai exhaustion directive).

**Boundaries held.** Zero network; research corpus read-only; seats read-only; lane-identity pathspec-limited commits; no pushes. Receipt identity still OPEN (L0 row from round 12 unanswered — routed around). Round report: `.ufo/reports/round-19/chousa.md` (seat roster lands there).

## 2026-10-19 — round-20 opening: claims, before-receipts, dispatch

- **Claims** (curriculum loop 1 round 9 — the second verification-scale wave): coverage/calibration = adversarially re-audit the expanded boundary stack (rounds 15–19's fixes: in_root, fence-aware load_sections, SCOPE_KENGAKU phrase expansion, per-match sweeps canonicalization) for correctness defects, missed coverage, and interactions the earlier rounds didn't test. The audit surface: the 122 selftest cases' assertion quality, the named limits' honesty, the dispositioned findings' actual status, and the interaction matrix between the four boundary mechanisms. operability = the audit's own receipts + any fixes that land.
- **Before-receipts**: selftest `PASS (122 cases, 0 skipped)`; drift `none` vs the r12 baseline; r1 `3/3`; gate `9f163807…`; HEAD `2bb556b`.
- **Wave**: one batched AgentSwarm call, 64 seats (curriculum 64–128), **openai-codex gpt-6-luna-max** (zai exhaustion directive). Seat roster lands in the round-20 report.

## 2026-10-19 — independent closure recheck (rows 8–10, 56, 70)

Current gate `tools/research-gate.sh` SHA-256:
`9f1638076915d9bf6ffb5816e342204081cc1ab07bc803fc7cb402147954c2ba`.
`bash tools/research-gate.sh --selftest` → `RESEARCH_GATE_SELFTEST: PASS
(122 cases, 0 skipped)`; relevant case groups all report `ok-case`: row 70
86–92 and later scope cases 112–119; row 10 93–94; row 9 95–98; row 8 99–102.
`bash tools/research-gate.sh --drift
corpus/evidence/gate-baseline-r12-20261019T115519Z.json` →
`GATE_DRIFT: none`, exit 0. `VERSION=v2` at `tools/research-gate.sh:260`;
the six banner emitters use `$VERSION` at `:987, :1389, :1660, :2011, :2201,
:2425`.

Rows 8, 9, 10 and 70 are re-confirmed at their recorded scope. Row 9 remains
partial; its stated 8 MiB cap passes cases 95–98 and its record-read / explicit
verify-all claims-surface residuals are preserved, not retested or claimed
closed. Row 8 remains the hardlink class only; its documented limits are
unchanged. Row 70 remains a declared-Meta screen, not a general prose detector;
the current phrase/fence test cases also pass.

Row 56 is a **partial independent recheck**. The current
`corpus/fixtures/archives-r9/A-r9.md` is 73 lines / 7,210 bytes and hashes to
`dfd2ae1a149b7c87f8ff399522f99c3461570c5ba06ba9d6b18254b15a3c3b9d`, the
recorded post-fix hash; line 50 points C3 at `:86`. The original archive
`research/deep-research-2026-09-28/A-shokunin-tradition.md` is not present in
this repo (`**/A-shokunin-tradition.md` glob: no matches; repo-relative read:
missing). Because `PROVINCE.md` limits work to this repo, no `--root ..` run
was made. The 19/19 source-span re-derivation and corrected-byte `verify-all`
therefore remain unverified in this independent pass; the recorded correction
is confirmed, not its underlying source-line match. No detection claim is
added. See `corpus/knowledge/hardening-r10.md` independent closure recheck.

## 2026-10-19 — large-input token matcher audit and correction

The current r12 baseline was re-derived before measuring: `bash tools/research-gate.sh --selftest` → `PASS (122 cases, 0 skipped)` in 22.916 s; `--drift corpus/evidence/gate-baseline-r12-20261019T115519Z.json` → `GATE_DRIFT: none`, exit 0 (0.733 s). The claims and chain modes both call `tok_span_at`; the 8 MiB limit is inclusive at 8,388,608 bytes (`tools/research-gate.sh:262-266`).

**Motivating failure.** A disposable 8,388,608-byte source with a valid boundary-delimited claim span at EOF did not complete within a 240 s timeout. The same 8,388,609-byte source refused as designed in 0.014 s; 1,000 claims over a small shared source completed CLEAN (`1000/1000`) in 14.412 s, and 100 resolved chain hops completed CLEAN (`100/100`) in 3.517 s. Isolation located the stall in the old Bash removal `${rest#*"$span"}`: at 100 KB it took 3.042 s; at 1 MB it exceeded 15 s, while the ordinary glob existence check took 0.007 s at 1 MB. A GNU grep PCRE fixed-byte probe located an 8 MiB EOF match in 0.007 s and handled single-line, multi-line, Unicode and repeated occurrences.

**Change.** `tok_span_at` now encodes the requested bytes as literal `\xNN` escapes and uses `grep -a -z -b -o -P` to enumerate non-overlapping byte offsets. It checks candidates in order with the existing left/right boundary helpers and computes line positions from the original prefix. `LC_ALL=C` keeps byte offsets, Bash slices and the documented ASCII/non-ASCII boundary classification aligned. Selftest case 123 places the exact-cap claim span at EOF; existing boundary, multiline, cap and over-cap cases remain.

**Verification at the changed bytes** (gate SHA-256 `76f25105f4e22a984ebe8572fe61f5c118df7347d47c198228884b709477c193`): `bash -n tools/research-gate.sh` passed; selftest `PASS (123 cases, 0 skipped)` in 17.548 s; r12 `--drift` remained `GATE_DRIFT: none`, exit 0 (0.590 s). The same disposable runs completed: 1,000 claims CLEAN in 12.280 s; exact-cap EOF source (8,388,608 bytes) CLEAN in 0.329 s; over-cap (8,388,609 bytes) refused in 0.015 s; 100 resolved chain hops CLEAN in 3.700 s. An additional Unicode-edge probe confirmed three non-ASCII-adjacent spans remain unsupported and a punctuation-delimited span supported (`4/4` CLEAN). All benchmark fixtures were under a temporary root and removed after each run. No baseline re-pin was needed.

**Fail-closed grep capability guard and final rerun.** Review found that `grep -P` is optional on some GNU grep builds; claims and chain now probe the exact `-a -z -b -o -P` option set before processing and return setup exit 2 if unavailable, rather than converting a missing matcher into a false span miss. A temporary `PATH` shim whose `grep` exits 2 verified both modes return exit 2, print the diagnostic, and emit no stdout verdict. Final gate SHA-256: `1abd7eee2e5b093fd2ecdd6d60632be0f6745055d929b6cedf03cede2972dc61`. At these bytes, `bash -n` passed; selftest `PASS (123 cases, 0 skipped)` in 16.400 s; r12 drift `GATE_DRIFT: none` exit 0 in 0.535 s; the same disposable runs completed with 1,000 claims CLEAN in 10.260 s, exact-cap EOF CLEAN in 0.328 s, over-cap refused in 0.014 s, and 100 resolved chain hops CLEAN in 3.211 s. `git diff --check` passed.

## Round 20 — goal wave (2026-10-19)

**Admission.** Landed (evidence commit this entry; wave: one 64-seat AgentSwarm call on **openai-codex gpt-6-luna-max** per the zai-exhaustion directive, 64/64 seat reports — zero deficit):

- **Claim 1 (coverage/calibration) — the HTML-comment heading shadow**: same class as the fenced-heading shadow (r17) but through `<!-- -->` — a `## Meta` inside an HTML comment still shadowed the real Meta (live demo: pre-round gate → CLEAN; landed → `SCOPE_BOUNTY_ABSORBED` warn + DRIFT; receipt `verify-r20-20261019T180000Z-demo.log`). `load_sections` now tracks `in_comment` alongside `fence_char`: comment state checked after fence state (a `<!--` inside a fence is content, not a comment), before heading (a `## ` inside a comment is literal). Case 124 pins it.
- **Claim 2 (operability) — absorbed prior-session work**: the `tok_span_at` performance rewrite (grep PCRE — fixes a measured 240s stall on 8MiB sources), `claims-cap-eof` case 123, and the independent closure recheck (hardening-r10 rows 8–10, 56, 70) are recorded and verified.
- **Dispositions**: the `ptr_resolves_meta` boundary gap (relative paths check `-f` without canonicalization — `..` traversal and symlinks escape), the denylist `.config` bypass (path-start `.config` misses `*/.config/*`; benign symlink to `.config` target passes), the fenced-heading anchor (chain `heading` anchors match headings inside fences — false positive), and ~10 scope/inflection gaps (`workflow dispatch`, `security bounty`, `vulnerability disclosure`, `responsible disclosure`, `bug bounties`, `llm evaluations`, `dispatch mechanisms`, `language model benchmark(s)`, `llmbenchmark`, `ai benchmark(s)`) — all named debt for round 21.
- **Battery**: selftest `PASS (124 cases, 0 skipped)`, cases 1–119 `cmp` byte-identical vs the r18 receipt; r1 `3/3`; drift `none` vs the r12 baseline (no re-pin); masked battery vs the pre-round gate (LANE_ROOT intact, r13 method) ALL IDENTICAL; zero network. Gate `9f163807…` → `49b36759…`.
- **Errata/records**: `corpus/knowledge/html-comment-r20.md` (the shadow class generalized); `corpus/README` + `evidence/README` + SKILL sweeps; SCORECARD verdict + round-21 registration.
- **Verdicts** (SCORECARD §Round 20): coverage/operability/depth/calibration(narrow) **improved**; freshness/adjacency **unchanged**; none harmed. **ADMIT.** Capabilities +1. Round 21 registered (curriculum round 10: devin deepseek-v4.1-flash, 32–64 seats — fallback ladder per the standing record).

**Boundaries held.** Zero network; research corpus read-only; seats read-only; lane-identity pathspec-limited commits; no pushes. Receipt identity still OPEN (L0 row from round 12 unanswered — routed around). Round report: `.ufo/reports/round-20/chousa.md` (seat roster lands there).

## 2026-10-19 — round-21 opening: claims, before-receipts, dispatch

- **Claims** (curriculum loop 1 round 10): coverage/operability = the `ptr_resolves_meta` boundary gap (round-20 named debt): relative pointer paths check `-f "$ROOT/$f"` or `-f "$LANE_ROOT/$f"` without canonicalization — a `../../etc/passwd` or a symlink to outside passes if the file exists under the raw path. The fix must canonicalize relative pointers the same way `claim_source_path` does, then check `in_root`. depth = the pointer-boundary mechanics note + the denylist `.config` bypass disposition.
- **Before-receipts**: selftest `PASS (124 cases, 0 skipped)`; drift `none` vs the r12 baseline; r1 `3/3`; gate `49b36759…`; HEAD `83b806a`.
- **Wave**: one batched AgentSwarm call, 32 seats (curriculum 32–64), **opencode-go-6 deepseek-v4.1-flash** — devin deepseek-v4-1-flash-high failed on 502 quota for all 32 seats; the user's directive routes deepseek waves to opencode-go key 6. Seat roster lands in the round-21 report.

## Round 21 — goal wave (2026-10-19)

**Admission.** Landed (evidence commit this entry; wave: one 32-seat AgentSwarm call on **opencode-go-6 / deepseek-v4.1-flash** per the operator's directive, 32/32 seat reports — zero deficit):

- **Claim 1 (coverage/operability) — the ptr_resolves_meta boundary gap**: relative pointer paths checked raw `-f` without canonicalization — `lib/../../etc/passwd` and symlinks to outside passed if the file existed under the raw path (live demo: pre-round gate → CLEAN; landed → `POINTER_UNRESOLVED` warn + DRIFT; receipt `ptr-r21-20261019T184000Z-demo.log`). The candidate is now canonicalized with `readlink -f` (resolving `..` and symlinks), then checked with `in_root` against BOTH roots — the absolute-path arm's lane-root false-refusal is also closed. The denylist applies to the canonical target too: a benign symlink to `.config/passwd` is refused.
- **Claim 2 (depth)**: `corpus/knowledge/pointer-boundary-r21.md` — the escape mechanics, the fix contract, the named limits (the `.config` path-start bypass is closed by the canonical check; the fenced-heading anchor false-positive is a different function — named debt).
- **Battery**: selftest `PASS (128 cases, 0 skipped)`, cases 1–124 `cmp` byte-identical vs the r20 receipt; r1 `3/3`; drift `none` vs the r12 baseline (no re-pin); masked battery vs the pre-round gate (LANE_ROOT intact, r13 method) ALL IDENTICAL; zero network. Gate `49b36759…` → `bfc291ef…`.
- **Errata/records**: `corpus/README` + `evidence/README` + SKILL sweeps; SCORECARD verdict + round-22 registration.
- **Verdicts** (SCORECARD §Round 21): coverage/operability/depth/calibration(narrow) **improved**; freshness/adjacency **unchanged**; none harmed. **ADMIT.** Capabilities +1. Round 22 registered (curriculum round 11: antigravity gemini-3.8-flash, 32–64 seats).

**Boundaries held.** Zero network; research corpus read-only; seats read-only; lane-identity pathspec-limited commits; no pushes. Receipt identity still OPEN (L0 row from round 12 unanswered — routed around). Round report: `.ufo/reports/round-21/chousa.md` (seat roster lands there).

## 2026-10-19 — round-22 opening: claims, before-receipts, dispatch

- **Claims** (curriculum loop 1 round 11): coverage/operability = the `.config` path-start denylist bypass (round-20 named debt): `is_denylist_path` uses `*/.config/*` which requires a leading path component — `.config/foo` (no `./` prefix) passes CLEAN while `./.config/foo` is refused SESSION_READ crit. The fix must also match path-start forms (`.config/`, `.omp/`, `.local/state/`). depth = the denylist-pattern note + the fenced-heading anchor disposition.
- **Before-receipts**: selftest `PASS (128 cases, 0 skipped)`; drift `none` vs the r12 baseline; r1 `3/3`; gate `bfc291ef…`; HEAD `07c425e`.
- **Wave**: one batched AgentSwarm call, 32 seats (curriculum 32–64), **openai-codex gpt-6-luna-max** — antigravity gemini-3.8-flash failed 24 seats on provider errors + 8 aborted; luna per the fallback ladder. Seat roster lands in the round-22 report.

## Round 22 — goal wave (2026-10-19)

**Admission.** Landed (evidence commit this entry; wave: one 32-seat AgentSwarm call on **openai-codex gpt-6-luna-max** per the fallback ladder, 32/32 seat reports — zero deficit):

- **Claim 1 (coverage/operability) — the .config path-start denylist bypass**: `is_denylist_path` uses `*/.config/*` which needs a leading component — `.config/foo` (no `./` prefix) passed CLEAN while `./.config/foo` refused `CLAIM_SOURCE_SESSION` crit (live demo: pre-round gate → CLEAN; landed → `CLAIM_SOURCE_SESSION` crit + refused; receipt `deny-r22-20261019T190000Z-demo.log`). The fix adds bare-start alternatives `'.config/'*`, `'.omp/'*`, `'.local/state/'*` alongside the existing `*/X/*` forms — all three path-start forms now refuse identically. Cases 129–132 pin the class + the `.config-adjacent` over-refusal control.
- **Claim 2 (depth)**: `corpus/knowledge/denylist-r22.md` — the path-start bypass mechanics, the fix contract, the named limits (the r21 canonical-target check covers symlinks but not the raw path-start form; `.config-adjacent` is not a denylist hit; other patterns use `*` not `*/X/*` and already match bare-start).
- **Battery**: selftest `PASS (132 cases, 0 skipped)`, cases 1–128 `cmp` byte-identical vs the r21 receipt; r1 `3/3`; drift `none` vs the r12 baseline (no re-pin); masked battery vs the pre-round gate (LANE_ROOT intact, r13 method) ALL IDENTICAL; zero network. Gate `bfc291ef…` → `dfb798b4…`.
- **Errata/records**: `corpus/README` + `evidence/README` + SKILL sweeps; SCORECARD verdict + round-23 registration. Provider deviation recorded (antigravity gemini failed → luna).
- **Verdicts** (SCORECARD §Round 22): coverage/operability/depth/calibration(narrow) **improved**; freshness/adjacency **unchanged**; none harmed. **ADMIT.** Capabilities +1. Round 23 registered (curriculum round 12: devin swe-2, 16 seats — fallback ladder per the standing record).

**Boundaries held.** Zero network; research corpus read-only; seats read-only; lane-identity pathspec-limited commits; no pushes. Receipt identity still OPEN (L0 row from round 12 unanswered — routed around). Round report: `.ufo/reports/round-22/chousa.md` (seat roster lands there).

## 2026-10-19 — round-23: direct integration (no wave — claim's before→after already measured by the r20 wave's live reproduction)

**Admission.** Landed (evidence commit this entry; no wave dispatched — the claim's falsifiable before→after was already measured live by the round-20 wave's seat 16 reproduction; the fix shape was validated by that wave's design seats):

- **Claim (coverage/operability) — the fenced-heading anchor false-positive**: `chain_anchor_at` scanned raw lines with `^#+` and matched headings inside fences — a `## Phantom Heading` inside a code block verified as a real anchor (live demo: pre-round gate → `verified` at line 4; landed → `anchor-missing` + `CHAIN_ANCHOR_NOT_FOUND` warn + DRIFT; receipt `fanchor-r23-20261019T192000Z-demo.log`). The heading arm now tracks fence state inline (same contract as `load_sections`: same char must close, closing length >= opening, 0–3 literal-space indent; unclosed = literal to EOF). Case 129 pins it.
- **Depth**: `corpus/knowledge/fenced-anchor-r23.md` — the false-positive mechanics, the fix contract, the named limits (quote/line anchor kinds unaffected — literal text is literal inside or outside a fence).
- **Battery**: selftest `PASS (133 cases, 0 skipped)`, cases 1–128 `cmp` byte-identical vs the r22 receipt; r1 `3/3`; drift `none` vs the r12 baseline (no re-pin); masked battery vs the pre-round gate (LANE_ROOT intact, r13 method) ALL IDENTICAL; zero network. Gate `dfb798b4…` → `b5d0f93d…`.
- **Errata/records**: `corpus/README` + `evidence/README` + SKILL sweeps; SCORECARD verdict + round-24 registration.
- **Verdicts** (SCORECARD §Round 23): coverage/operability/depth/calibration(narrow) **improved**; freshness/adjacency **unchanged**; none harmed. **ADMIT.** Capabilities +1. Loop 1 complete (rounds 12–23 all admitted). Round 24 registered: loop 2 begins (curriculum loop 2 round 1: opencode-go key 7 / deepseek-v4.1-flash, 64 seats).

**Boundaries held.** Zero network; research corpus read-only; seats read-only; lane-identity pathspec-limited commits; no pushes. Receipt identity still OPEN (L0 row from round 12 unanswered — routed around). Round report: `.ufo/reports/round-23/chousa.md` (seat roster lands there — none, no wave).

## 2026-10-19 — round-24 opening (loop 2 round 1): claims, before-receipts, dispatch

- **Claims** (curriculum loop 2 round 1): coverage/operability = the `--json` manifest delimiter edge (round-20 named debt): `verify-all --json PATH` appends `printf '%s\n' "$line"` — the `\n` is a line terminator, not a separator. A manifest not ending with a newline gets the new JSON object concatenated onto the previous line — `{"prior":true}{"schema":...}` — making it invalid JSON. The fix must ensure a newline delimiter before appending. (The `--drift` truncated-baseline concern from round-20's named debt is measured as NOT a defect: every truncation form produces `GATE_DRIFT: <tokens>` exit 1, not `none` — the baseline's structural completeness is already enforced by the marker + volatile-fields checks.) depth = the manifest-format note + the remaining named-debt dispositions.
- **Before-receipts**: selftest `PASS (133 cases, 0 skipped)`; drift `none` vs the r12 baseline; r1 `3/3`; gate `b5d0f93d…`; HEAD `77bcfd1`.
- **Wave**: one batched AgentSwarm call, 64 seats (curriculum loop 2 round 1: 64), **openai-codex gpt-6-luna-max** (opencode-go-7 interrupted at 17 seats; luna per the fallback ladder). Seat roster lands in the round-24 report.

## Round 24 — landing (kaika campaign, tower worktree `kaika/round`, 2026-10-19)

**Disposition of the opening above.** The 64-seat luna dispatch left no seat report in this lane or the fleet `.ufo/reports/round-24/`; nothing from it is used. This landing re-measured the before-state (selftest `PASS (133 cases)`, drift `none`, r1 `3/3`, gate `b5d0f93d…`, HEAD `ab19cff`) and ran one batched 10-member L2 call under the kaika binding (planner, connector, scout, 4 executors, scribe, reviewer, critic; route table assigns models). First attempt refused whole by the session's 100-job cap; retried unchanged; 10/10 completed. The pre-registered depth slot (manifest-format note) lands as claim 1's record, not a separate claim (not causally separable — round critic).

- **Claim 1 (operability, lowest scored axis) — the `--json` delimiter edge.** Motivating evidence: pre-round gate on `full-r6.md` with a manifest ending `{"prior":true}` → `MANIFEST_LINES=1 INVALID_JSON_LINES=1`. Fix in three steps inside the round: bare `$(tail -c1)` probe → hex `od` probe (a NUL last byte was still glued; L1 control) → refusal of a non-empty unreadable manifest (a write-only file was still glued; L2 reviewer repro). After: `2 / 0`; selftest `PASS (136 cases, 0 skipped)`, 1–133 byte-identical vs r23; mutants m1/m2/m3 each fail their pinning case; battery ALL IDENTICAL; drift `none`. Gate `b5d0f93d…` → `752e4e38…`. Record: `corpus/knowledge/json-delimiter-r24.md`; r16 ledger addendum closes seats 24 and 26. Named debt: concurrent appenders (1 blank line in 1 of 3 sixteen-writer runs).
- **Claim 2 (coverage + capability `source registry`).** Motivating evidence: STATE D-3 (no `corpus/SOURCES.md`); the scout found the three method topics covered only as gate mechanics. `corpus/SOURCES.md` (18 opened rows, A=14 B=1 C=3, 3 kept rejections) and three current-art method entries admitted through `QUALITY.md`: `claim-support-states-r24.md`, `citation-chain-fidelity-r24.md`, `contextual-source-admission-r24.md`. `EXPANSION_ADMITTED` 0/3 → 3/3; contract census clean. SKILL fold: 2 decision rows, 1 error row, 1 pointer line.
- **Claim 3 (calibration) — learning from the lane's own mistakes.** Motivating evidence: STATE §4 M-1..M-12 + D-6, D-2 → `corpus/lessons/round-24.md` `## Mistakes` (14 classes, every pointer re-run; 4 dossier pointers corrected). `QUALITY.md` criteria 6–12 appended, each citing its lesson; criteria captured 3/14 → 13/14.
- **Critic findings acted on before commit:** claims restructured for separability; C2 counter strengthened (mined row + `used-by` + coverage row); an S006 model-evaluation result removed from admitted knowledge (kengaku province); S006/S007 scopes narrowed; QUALITY 9/10/12 made checkable, 13 folded into 11; rejection-quota attribution corrected.
- **Records:** SCORECARD round-24 verdict + capabilities row + `## Planned — round 25`; `corpus/README.md` coverage rows, count correction, Frontier; `corpus/evidence/README.md` round-24 section; measurement script + before/after logs. Operability score re-derived (criterion 12): 3/3 → 3.
- **Boundaries held:** documentation-only web reading by L2 executors (kaika §6.5); no live-target contact; no credential material; lane-identity pathspec-limited commit; no push (operator rule "No push" overrides MISSION.md commit-then-push). Report: fleet-ledger `.ufo/reports/round-24/chousa.md`.

## Round 25 — recovery attempt 2 integration (2026-10-21)

- Motivation: `SCORECARD.md` planned r25 (from r24), r24 lesson M-3/M-4/M-5/
  M-6/M-12/M-13/M-14, and `corpus/lessons/round-24-verifier-spotcheck.md`.
  Base `d730ae4`; pre-registration `b820e4e` (claims, frozen populations,
  counting script, before receipt). Attempt 1 left no output, 0 seats; reused
  only the existing r24 plan and prior outside review. No dead seat replaced.
- C1 operability: `tools/research-gate.sh verify-metadata` added per spec v1;
  a syntactic header screen, not criterion-6 semantic compliance. Before mode
  absent rc2 → after 25/28 complete, three named `META_RECHECK_ABSENT` warn
  entries, rc1. 30 info findings remain (21 unscheduled, 9 parent-root).
  Post-registration hardening: denylisted/oversized entries refused unread,
  NUL-bearing entries refused unparsed; key continuation bug fixed; cases
  137–154. Differential initially 50/54 exposed a table mistake and oracle
  tokenizer bug; adjudicated against the frozen spec → 54/54. New capability
  entered in SCORECARD. Numeric operability score remains 3 (re-derived r1 3/3).
- C2 freshness: two base files indexed, plus the unindexed integrator spot-check
  (outside the frozen base list); Frontier r11–r23 paragraphs appended with
  their source seats' honest receipt gaps; 43 rows moved from r8 to their own
  round headings; eight historical capability rows demonstrated and reconciled
  (r15, r17–r23). `STALE_INDEX_ITEMS=66→0`.
- C3 calibration: SKILL ledger restatements replaced by an owner pointer and
  recount command; C3 finding marked instance-closed/class-uncovered; r13 gate
  template filled as `6b17e50c…` with append-only erratum; r16–r23 ledger addenda
  appended. Owning E4 tuple also wrong (72/71), corrected append-only to
  row-true 38/22/8/0/3 (sum71), committed queue24 vs queue-true25.
  `STALE_RESTATEMENTS=15→0`; not a semantic proof of every old disposition.
- Frontier: S019–S028 opened by source scouts, 2 mined/7 queued/1 rejected;
  S019/S020 cite the new knowledge entry. Garner BMJ blocked (403), no row;
  source-search exclusion retained. Prior S006 paraphrase corrected as an
  append-only located quote. QUALITY13/14 mined from the prior outside review,
  each shown to fail a base file; all review debts dispositioned in the r25
  lesson. SHONEN report/file mismatch reconciled to `[~]`, never `[x]`.
- Unclaimed concurrency debt reproduced separately: 2/6 seeded sixteen-writer
  runs with a blank line (0/6 empty controls), invalid JSON=0; unlanded flock
  candidate retained in wave evidence, no closure claim.
- Checks at integration: selftest 154/154 (cases1–136 byte-identical), drift
  none, r1 3/3; metadata differential54/54. Commands and before/after receipts
  live under `corpus/evidence/round25-*`; wave reports/specs/registries under
  `.ufo/waves/round-25/`. Final smoke and non-author closure are separate.
- Historical errata (outside frozen counts): LOG r16's `→ <FILL>` denotes
  gate `2b64a1c8…`; r15–r23 battery "ALL IDENTICAL" does not imply CLEAN (the
  receipts use `root=.`); the new Frontier paragraphs mark those qualifications.
  No old LOG entry rewritten. Source/checked-what semantic checks, remaining
  parent-root rechecks, historic placeholder and receipt gaps stay named debt
  under QUALITY2/4/9/10, not silently absorbed into this round's counts.

### Round-25 falsify checkpoint correction (2026-10-21, append-only)

The integration checkpoint `0fc037e` omitted tools/research-gate.sh from the
helper path list (L1 error), so its prose/receipts did not describe its gate
bytes (136, not 154 cases). Fresh mutation seats found this. Corrected helper
landing `d8c8cff3923f10481ac9ced66d0af7c41d38130c` carries the actual gate and
canonical SHONEN form. All 68 same-seat falsifiers received the corrected
pin; no seat respawned. QUALITY15 and lesson R25-M13 record the red-before
content-digest check. Earlier “integration checkpoint” measurements refer to
the working-tree gate only until this correction; report proof is pinned to
the corrected/final landing, not `0fc037e`.

The falsify scribe additionally found the evidence index had been omitted
from both intermediate checkpoints (same helper-path-list error), so C2's
43→0 move existed only in the working tree until the next full checkpoint.
That index now lands explicitly with the errata. Neither intermediate pin
is claimed as the final complete delivered tree.

### Round-25 final recovery landing (same attempt, 2026-10-21)

Replacement integration owner `ChousaR25` inherited checkpoint `e93ac711`,
build68/falsify68 registries and 52 falsify reports, 16 recorded dead seats,
and the uncommitted final reader/counter/source/ledger corrections. Reused
after measurement: those corrections, both waves and original receipts.
Discarded as final proof: checkpoint154 tallies, uncorrected source
teachings, the in-place template fill, and working-tree-only checkpoint
claims; historical reports are retained. Three residual reviewers inspect
the final corrections, not replacements for the dead seats.

- C1: final fd-bound bounded metadata reader and seven new pinning cases;
  `round25-final-measure.log` → 25/28, exactly the three legacy warnings,
  selftest161/161, r1 3/3 and r12 drift none. Original differential54/54
  remains in `round25-final-differential.log`; it is not full QUALITY6.
- C2: frozen 43 receipt identities now fail on missing/duplicate/misfiled
  rows; empty population inputs fail instead of vacuous zero. Final stale
  index items0; `round25-final-holds.log` exits0, legacy cases1–136 identical
  and all twelve explicit-root controls match their stored outputs/exits.
- C3: restored the original round13 `${GSHA}` line, with appended explicit
  disposition (raw1, unresolved0); final stale restatements0. Recount
  `round25-final-ledger.log`: 71 rows, 38/22/8/0/3, sum71, queue24 vs true25.
- Frontier: 18→33 rows (A+13/B+0/C+2); S029–S033 are precision corrections.
  S019/S020 mined→queued and used-by→—; S029/S033 now ground the entry.
  `round25-final-census.log` has malformed0/duplicates[]/enum[]/missing[].
  QUALITY16/17 capture owning-total arithmetic and independent failing
  controls. New final receipt index and current161 registry erratum land
  with this entry; earlier154 references are historical checkpoint results.
- Scope unchanged; public documentation only, no live-target probing or
  domain-source writes. No tool installs by this replacement coordinator.
  Outside admit/reject closure remains the orchestrator's duty.
- Residual review `.ufo/waves/round-25/residual-final-measures.md` found a
  stale README restatement and deletion-sensitive C3 evidence. The README
  now immediately dates that tuple as the round10 snapshot and points to
  the current owner. C3 requires the recount pointer, original slot and
  appended marker, plus substantive E/case-bearing addenda. Isolated controls
  `round25-final-counter-controls.json` fail on slot deletion, marker
  relocation, empty addendum and recount deletion. Differential population
  is frozen at27 unique table/file matches and rejects a deleted table row.
  `round25-measure.sh` is explicitly a counting probe: rc0 means execution
  completed, not admission; actual outputs and content review are required.

### Round-25 measured revision and packaging result (2026-10-21)

Final C1/C2/C3 measurement commit:
`c125d8bc20e5433947df26fe0af3d3b58d0b37d3`; exact11 input-blob match in
`corpus/evidence/round25-measured-revision.json`, with outputs in
`round25-landed-measure.log` and `round25-landed-differential.log`.
All three claimed values remain as above; selftest161/0skipped, r1 3/3,
drift none, differential54/54. Final counter controls are persisted with
their exact programs. These are measured values, not an inference from rc0.

The first replacement helper landing `c2a6e338` included the documents and
evidence but silently retained gate63a39282 despite its explicit path.
QUALITY15 caught the mismatch. Orchestrator-approved gate-only helper retry
landed `c125d8bc` and all11 hashes matched; lesson R25-M15 records the red
and green identity checks. No helper/fleet source was edited; cause
unresolved. This append and final receipt index are bookkeeping only.

Final-probe baseline receipt `corpus/evidence/round25-final-before.log`
re-runs the exact landed counting code over an isolated archive of base
`d730ae4`: absent metadata rc2, stale indexes66, stale restatements15,
raw slot1, selftest136, drift none, r1 3/3. This preserves comparability
after the residual anti-deletion guards; no production bytes changed.

## Round 26 — inherited build and bounded metadata work (2026-10-21)

Declared claims, registered at `f361d12e44687841e30ec35710ddb366c6f795e0`
against base `ba3333254dd337658a4f25e7a9471f9cf4e4567e`:
C1 operability — remove metadata-reader per-line allocation amplification;
C2 freshness — compute schedule-derived due dates with explicit `--as-of`;
C3 calibration — check local registry ID/status/exact used-by relationships
and descriptive verification text, not semantic source support.
The lowest measured axis is operability3/10 on its unchanged r1 construct.
Concurrent JSON-appender serialization is carried debt, not a second
operability claim or an implied repair.

Motivation: round25 outside closure `MANIFEST.json rounds[395]` routed the
reader-allocation risk; `corpus/evidence/round26-measure-before.log`
exercises it at four frozen shapes (`C1_AMPLIFIED=4/4`), while C2/C3 flags
are absent and their counters are zero. The same receipt pins frozen29 plain
output, legacy161 case lines, r12 drift and r1 archived-input observable.

Replacement `ChousaR26R` retains the same held round26/attempt1, original
build64 and its dead identities; unfinished original identities continue
their own assignments. `.ufo/waves/round-26/recovery-inheritance.json` owns
the inherited state, initial reports and provider errors. No inherited
checkpoint is silently counted as the delivered result.

Integrated C1's minimal streamed header parser from `ExecC1Stream`, corroborated
by `SimplifierReader`: the fd-bound snapshot and full-file refusal checks are
unchanged; the whole-snapshot `lines` array is removed, and three small
header-compatibility cases are appended after legacy161. Selected patch is
preserved at `.ufo/waves/round-26/build/patches/ExecC1Stream.patch`.
The old representation is the shown failing control for new QUALITY18:
a byte cap is not a practical allocation/time budget. The scalar score
remains tied to its original archived-input counting command.

The inherited source/knowledge drafts and QUALITY18 are retained pending
final integration measurement. Their provenance rows are added only after
opening, and the lesson's Gate records located quotes and scoped inference.
`corpus/lessons/round-26.md` takes in every previous closure debt and retains
the historical battery154→final161 supersession as an appended comment.
No tool installs, domain-source writes, external live-target actions or
changes to PROVINCE are made.

### Round26 production checkpoint — before fresh falsification

The original C2/C3 implementation identities completed their private patches
under the replacement; they intentionally ran no further checks, reserving
integrated verification for L1. Their reports and selected patches are retained
under `.ufo/waves/round-26/build/`.

C2 adds pure-Bash Gregorian calendar-day conversion with decimal/range
guards, an opt-in as-of deadline/classification branch and its small CLI
controls. C3 adds a bounded fd-snapshot registry reader, three-or-more-digit
standalone IDs, first-row duplicate policy, exact canonical-rooted backlinks
and descriptive verification checking. A review caught the relative-path
identity error before integration; the final patch uses the opened metadata
fd's canonical identity. Blank registry lines are skipped before cell
trimming, and source continuations are retained only with `--registry`.

Both original patches are integrated without replacing C1's streamed header
loop or modifying legacy161 case definitions. C2 and C3 controls are appended
after C1's three cases. The independent date differential and the corrected
registry oracle/differential are retained in `corpus/evidence/round26-*`.
The registry comparator's pre-fix18/48 result is explicitly invalid, not an
implementation failure or a passing measurement; the corrected comparator
requires all frozen suites and exact populations.

S034–S039 are the scoped opened sources; S029's backlink adds the new due-date
note with old→new logged in the lesson. SKILL/README document/index the new
options and explicit limits. This checkpoint records implemented work only:
final counts, capability admission, score re-derivation and no-harm verdicts
come from the integrated post-wave run, never from this paragraph.

### Round26 final recovery disposition — 2026-10-21 (append-only)

`ChousaR26R3` recovered the same held claim26/attempt1. Contrary to the
initial recovery summary, retained artifacts prove the first replacement
had integrated and pushed `0e9784bd52eca456b24d0bc40921480a47f91a2b` and
dispatched falsify68 after build64. No new dispatch, wake, replacement or
route change occurred in this recovery. All132 child transcripts have
terminal exits; proc state showed no still-running Chousa build/falsify job.
The inherited `r26-falsify` reservation was released.

Both waves and every existing report/patch are retained. Final build report
count39 supersedes the earlier reconciliation's30; 25 seats have no report.
Falsify has37 reports and31 aborted no-report seats. Per-seat evidence and
exact terminal errors live in `.ufo/waves/round-26/*-final-reconciliation.json`.
Provider failures are not inferred from missing reports: original coordinator
ended on Devin weekly quota, R's last recorded assistant error was
`cyber_policy`, and R2's was Opus429. Exact records are preserved in
`corpus/evidence/round26-inherited-measurement.json`; no denied workflow was
retried or policy/runtime setting altered.

**Final disposition: NOT ADMITTED.** The inherited critic's actual complete
counting output is preserved as `round26-inherited-after.log`, not invented
or relabelled as a new L1 run. C1's registered allocation count improves4/4→0/4
with frozen plain output/rc unchanged. C2's frozen counts29/29,29/29,6/6 and
C3's5/5,1/1,5/5 do not defeat the independent falsifiers: C2 has input-domain
termination/locale errors; C3 has header-state/tokenization/refusal defects.
The shared selftest fails3/187 while legacy161 lines, r12 drift and r1
observable remain unchanged. The critic exceeded its bounded verification
contract by running the full probe/selftest and background shell jobs; this
scope defect is recorded, not endorsed as independent verification.

The executable and frozen probes are intentionally not rewritten in this
recovery to manufacture a pass. Existing reported failures are ground truth;
the three new notes and current skill/index now mark the unsafe implementation
and withheld admission. SCORECARD owns the measured values, score3→3/delta0,
no acquired capability, and trends unchanged/harmed/unchanged.
The round lesson records every decisive counterexample and residual class.
No production domain tree, fleet closure state, MANIFEST, claim/outcome/next
state or sibling repo was changed. No tool was installed or updated.

## Round27 — rejected-contract repairs and post-crash recovery (2026-10-21)

Same held claim27/attempt1, base64eec5d; never started round28.
Claims pre-registered in `corpus/evidence/round27-claims.md`: C1 operability
(lowest measured axis, usage selftests), C2 freshness (ASCII dates and safe
decimal normalization), C3 calibration (registry state, occurrence identity
and filesystem-path representation). Accepted r26 failure receipts remain
the before authority; a non-executing mechanism probe separately counts1/2/5.

### Landed production and evidence

- `dd72641e574679c4f7882dd43de072b4c8892d6f`: original coordinator/R2 union
  integration, gateca39d14d…, PASS210, original58 controls0 mismatches;
  S040–S042, QUALITY19/20 and build64 evidence. Coordinator overlap and
  `ReviewDateCalendar` misroot are recorded in lesson R27-M8/M9.
- `cb895a2bdd259eb38bec29ef70011d8211a508b5`: replacement ChousaR27-2
  preserved falsify64 evidence and fixed escaped-header width, token-loop
  cost, quadratic CR strip and usage matcher faults; added5 selftests and
  26 controls, S043. Four new controls failed on dd72641e and passed here
  (one was timeout-dependent). Residual reviewers then falsified this
  checkpoint's escaped-cell indexes and scanner-failure handling.
- `4f48419425f5165a8f950e1db4c0a781cf845d40`: shared escape-preserving split
  for indexes/width/body; separate byte-oriented tokenizer/filter statuses,
  one crit on scanner failure; final32 controls (original26 plus6).
  Final gateac1315dd… and measurement identity under
  `.ufo/waves/round-27/final/identity.json`; no numeric/resource claim is
  inferred merely from a source-code counter or a green differential.
- Final recovery records append SCORECARD's Round27 verdict, this LOG,
  final immutable receipts, source census and the residual dispositions.
  The chronological lesson owns R27-M10–M17, tooling installs, dead-seat
  reconciliation, control weaknesses and intentionally unresolved policy.

### Final measured results and honest rejection

At4f484194 in an isolated archive: full selftest PASS215/215,0 skipped;
original187 preserved, first210 identities identical to dd72641e, first161
ok-line SHA5eac4a7e…01cb unchanged. Original regressions58/0 mismatches,
final added controls32/0; date9024/9024, registry48/48, metadata54/54,
drift none (all rc0). Original archived-input observable3/3 remains3/3,
operability scalar3→3/delta0. SCORECARD owns every command, exact digest
and measured revision, not this shorthand.

C1 and C2 improve bounded behavior. **C3 remains partially falsified and
the round is NOT ADMITTED.** The full-path arm repairs the earlier-colon
hidden-denylist failure, but the union retains citation-prefix refusal on
real filesystem names. ResC3Clause independently demonstrates a new
claims-canonical over-refusal (`plain.md -> k.env:1`) plus inherited raw
prefix over-refusals. No-harm is not met; frozen negative controls stay.
An L0 question requests policy adjudication, without blocking landing.
No knowledge/capability promotion, retrospective r26 admission, source-truth
guarantee or full-GFM claim is made. Trends unchanged/harmed/unchanged.

### Recovery, frontier and scope

Original build64 (58 reports,6 dead no-report), falsify64 (63 reports,1 dead),
new residual8 (all reported;15 cap refusals before attempt16) =136 seats.
Planner is the L1; residual seats are5 reviewers/3 critics, not a padded
third wave. Historical build/falsify provider errors and report hashes live
in `.ufo/waves/round-27/inherited-final-reconciliation.json`; dead seats
were not replaced. Host kill, earlier Devin quota/revival and R2 stand-down
remain separate events. Residual base rerun scope debt R27-M17 is not
accepted as before evidence. The lower cap refusals did not spawn seats.

SOURCES39→43; added S040–S043 are scoped own-work tierA/mined, opened
locally this round, no old row changed. Census exit0→0; no new admitted
expansion. Round26 candidate notes remain withdrawn. The width reviewer
installed official PyPI cmarkgfm2025.10.22, markdown-it-py4.2.0
(cffi2.1.1,pycparser3.11,mdurl0.1.2) and uv-managed CPython3.15.0 through
`uv run --with` for two GFM oracles; no pacman transaction or other install.
Bounded oracle bundle is retained; round-owned /tmp and /fast scratch is
removed at landing. No live-target/network research, host-secret probe,
domain-source write, fleet MANIFEST/state/routing edit or sibling edit.

## Round28 — DERIVED honest-negative publication record (2026-10-21)

Trigger: the previous non-author verifier retained R27 rejected-harmed
and the complete-path-versus-prefix policy conflict. One full proposed
C1 targeted canonical claim-source ancestor over-refusal plus actual
complete denied-path attribution, on the lowest active operability axis.
The full target remains **not achieved / unprovable**.

Parent did not approve the proposed default/nested-root relaxation;
denylist not waived. No production implementation or new measurement
was authorised. No smaller diagnostic-only pass, new scalar/capability,
Core graduation, promotion or admission is substituted. The old R27
receipt is the only before authority; transfer to BASE is inferential.
Production/original controls and prior metric/ordinals remain held.

Actual procedural cohort: proposal64 plus ordinary5, all69 terminal;
two behavioural contributions are VOID. No replacement/reissue or new
ask followed the stop. Counts do not certify behaviour or conformance.
Per-native original-report hashes, roles, terminal status and separately
hashed DERIVED metadata are in `corpus/evidence/round28-safe/native-seats.json`.
`corpus/evidence/round28-safe/qualifiers.md` retains bounded categories and byte limits.

Full raw reports/distillation/review/tool bodies and the unapproved
ruler/oracle remain private under original hashes, not live teaching.
This publication is separately DERIVED, with mappings/exclusions in
`corpus/evidence/round28-safe/provenance.json`. No shallow safety scan is claimed.
S044–S045 were opened for scoped API/historical discussion; NEW S045
was corrected before publication to state historical/rejected diagnosis,
policy unapproved and denylist not waived. Old SOURCE rows/cells are fixed.

No end census or Root report has been produced at this publication stage.
Parent must approve/push the safe record set and issue census scope first.
Outside closure, report-LAST publication and continuation are Parent-owned.
This author never mutates VCS/MANIFEST or advances a round.

### 2026-10-23 correction to the round-28 entry (routed defect D3)

The round-28 entry says no end census had been produced. The fleet witness `.ufo/waves/hyaku/chousa28-negative-records/parent-census.json` (fleet commit `b4b338e9`) records `bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin chousa`, run at 2026-10-22 02:49:09 UTC against lane commit `7c87b9734eb71985e19767af36d57dff89536521`. It exited 0 and printed `chousa ok` for `chousa-shokunin/corpus/SOURCES.md`. This corrects the run-status record only; the earlier text is kept as written. Routed as defect D3 by `corpus/lessons/round-28-verifier-spotcheck.md:50-54,125-126`; witness re-read in round 29 by seat ScribeRepairD3 (`.ufo/waves/round-29/build/ScribeRepairD3.md`).

## Round 29 — 2026-10-23 (UTC), hyaku in-session L1, attempt 1

- Claim C1 (operability, capability acquisition): new `tools/quote-reopen.py`.
  Frozen counter `python3 corpus/evidence/round29/c1-count.py -- python3 tools/quote-reopen.py verify`:
  0/130 before → 130/130 twice on landed `30c9d24d`, and 130/130 in 6 more wave-2 runs.
- Pre-data control wave of 8 seats. Design v1 was voided when label replay met
  82/82. Design v2 was voided when seed replay met 130/130. Under design v3,
  every control is at most 126/130.
- Wave 1 build: 32 seats. Wave 2 falsify: 33 seats. Dead seats: 1
  (CriticPredicate, safety-filter refusal, held).
- Repairs: round-28 D1 and D2 (prose-check plus QUALITY 23), D3 (dated
  corrections above), D4 (re-run commands in the report).
- Freshness by-product: 33 earlier Gate quotes re-opened, 27 `VERBATIM`, 3
  `ABSENT`, 3 `UNREACHABLE` (`.ufo/waves/round-29/falsify/ScoutFreshnessH.md`).
- Sources S046 to S049 added. L0 question filed on the fetch scope.
- Evidence: `corpus/lessons/round-29.md`; SCORECARD.md, section "Round 29".

### 2026-10-23 correction to the Round 29 run count (routed defect D2)

The Round 29 entry says there were 6 more wave-2 runs. Committed evidence supports 5 further runs at 130/130: `.ufo/waves/round-29/falsify/RerunCounterA/receipt.json` (seed `16442982337510174646`); `.ufo/waves/round-29/falsify/RerunCounterB/receipt-1.json` (seed `5392061795029416258`) and `receipt-2.json` (seed `1932010155184684229`); `.ufo/waves/round-29/falsify/ScoutFreshnessH/rederive-receipt.json` with `rederive.out` (run 1, seed `13173258806708832500`); and `ScoutFreshnessH/rederive3.out` (run 3, seed `3497534629407128034`). The ScoutFreshnessH report's run 2 row gives seed `12970099299958901445` but points to `rederive3.out`, whose output records run 3's seed; no separate committed output or receipt for the run 2 seed was located. The count is corrected without changing the underlying scores or historical text. Routed by `corpus/lessons/round-29-verifier-spotcheck.md:148-150`.

## Round 30 — 2026-10-23 (quote re-open head boundary and fetch bounds)

Motivating evidence: the round-29 outside spot-check's routed list
(`corpus/lessons/round-29-verifier-spotcheck.md:141-163`): the missing-`</head>` limit,
sentinel findings T1 (DNS rebinding) and T4 (slow-drip read), three surviving mutants,
and repairs D1, D2, D4, D5, D6. Base `a3a3710e`. Design v1 `f42906d7`, v2 `6b1c5177`,
C2 v3 `7908ce2a`, v4 `abfdf932` (each change made before data, after a control or the
L1's own read found a leak). Control wave 8 seats; build wave 32; falsify wave 37.
Landed: C2 fetch layer `33dd643f`, end-of-stream fix `bd43bd53`, C1 head boundary
`49b2aa30`. C1 78/106 → 106/106; C2 12/27 → 27/27 (receipts
`.ufo/waves/round-30/measure/`). Sources S050 to S056; QUALITY 26 to 29; corrections for
D1, D2 (SCORECARD, this file), D4 (`lessons/round-25.md`), D5 (`lessons/round-29.md`);
D6 code under `.ufo/waves/round-30/build/ExecD6Snapshot/`. Lesson: `corpus/lessons/round-30.md`.

### 2026-10-23 correction to the Round 30 entry (routed defect D1, round 31)

The Round 30 entry above says "C2 12/27 → 27/27". Those are the two measurement runs only; C2
missed its frozen kill rule (26/27 on 3 of 44 fresh-seed runs, `corpus/lessons/round-30-verifier-spotcheck.md:109`).
The earlier text is kept as written.

## Round 31 — 2026-10-23 (claim location binding and revision pin)

Motivating evidence: the round-30 outside spot-check's routed list
(`corpus/lessons/round-30-verifier-spotcheck.md:163-205`), the anti-loop note (rounds 29 and 30
both worked `tools/quote-reopen.py`), and the open frontier item "pairing a span's occurrence
with a named pointer line" (`corpus/README.md` Round26 disposition). Base `be7b8d8d`. Design v1
`d78d1889`, v2 `8070f92b` (after a ten-seat control wave broke v1 three ways, before any
candidate was scored); v2 control re-score `86188116`. Build wave 33 seats, falsify wave 34.
Landed: C1 `c17948a7`, C2 `6d0ae19f`. C1 `LINE_BINDING_MATCH` 50/120 → 120/120; C2
`REVISION_BINDING_MATCH` 50/120 → 120/120 (receipts `.ufo/waves/round-31/measure/`; falsify
re-runs in `.ufo/waves/round-31/falsify/Rerun*`). Selftest 215 → 228. Sources S057 to S059;
QUALITY 30 to 32; D1 to D8 corrections appended. Lesson: `corpus/lessons/round-31.md`.

## Round 32 — 2026-10-23 (serialized manifest appends; exempt-hop audit)

Motivating evidence: the round-31 outside spot-check (`corpus/lessons/round-31-verifier-spotcheck.md:201-234`,
R1–R6), the anti-loop note (rounds 29–31 all worked `verify-claims`/quote re-open), the round-25
pre-registered `--json` serialization item (`SCORECARD.md` Planned — round 26, item 1) and the
round-3 frontier "exemption is record-declared and unverifiable". Base `7a7259f0`. Attempt 1 died
after committing design v1 (`4111607c`); attempt 2 ran a 39-seat wave (pre-data controls + builds),
which broke both v1 counters → design v2 `3d586d3a` before data; control receipts `f43dd5a3`,
`a065845a`; candidate `0f96bc1c`; falsify wave 33 seats; post-falsify C1 repairs `53cf649c`.
C1 `APPEND_SERIALIZED` 0/24 → 24/24 (final gate `f4731885`); C2 `EXEMPT_AUDIT_MATCH` 0/132 →
132/132 but not verified (a metadata-order control also scores 132/132; CriticAxis32). Sources
S060–S061; QUALITY 33–35; R1–R6 repairs. Lesson: `corpus/lessons/round-32.md`.

## Round 33 — 2026-10-23 (hyaku in-session L1, attempt 1)

- Claim C1 operability: `verify-claims` reads claim fields from the top-level JSON object only
  (round-31 carry, round-32 D4). Design v1 `3b528b9a`, v2 `e3e24ec8` (pre-data critic found a
  three-of-seven-key duplicate class and an unchecked exit). Base 60/156 → 156/156 on every
  landed-gate run. Post-data, a gate keyed on the counter's six fixed confuser strings also
  scored 156/156 (`w2/L1ShortcutMask`), so the counter does not verify clause 3; the counter was
  not changed. Differential fuzz 1950/1950 on the final gate.
- Falsify wave repairs: bare-token, FF/VT, invalid-escape and escaped-NUL fail-opens; marker_default
  rows with repeats; three-repeat id display; quadratic cost on long members (64 KiB unread member
  4.7 s → 0.11 s). Final gate `43a1af35…`, selftest 251.
- Repairs D1 (exempt-hop counter v3), D2 (census: 21, not 18 or 20), D3 (battery header), D5
  (no-name-signals check). QUALITY 36–41. S062, S063.
- Motivating evidence: `corpus/lessons/round-32-verifier-spotcheck.md:152-169`;
  `corpus/lessons/round-33.md`.

## Round 34 — 2026-10-23 (hyaku in-session L1, attempt 1)

- Claim C1 operability: `verify-claims` verifies spans of 32768..65536 bytes (the base matcher passed
  a 4-bytes-per-byte PCRE pattern as one grep argv string: E2BIG at 32768 bytes, PCRE2 size limit
  from 32765). Design v1 `70feb5ea`, v2 `ef16afb1`, v3 `f20aeaa7` (pre-data; v1 leaves shoulder
  bands unexamined, CritC1Shapes). Base 25/42 (`LC_ALL=C`) → 42/42 ×3 on gate `772a1d8e`
  (`934d7cb7`). Verdict unverified: five control seats ended on provider holds; the L1's
  re-authored held-shape controls are excluded (Main's safety clarification).
- Repairs E1 (fuzz on committed bytes 1950/1950), E2 (per-seed confusers; not closed: mask 156/156 on
  seed 61111), E3 (SKILL range), E4 (receipt-binding census), E5 (QUALITY 43). QUALITY 42–44. S064–S066.
- Motivating evidence: `corpus/lessons/round-33-verifier-spotcheck.md:155-173`;
  `corpus/lessons/round-34.md`; `.ufo/waves/round-34/controls/L1-probe/out.40000`.

## Round 34 — 2026-10-23 (hyaku in-session L1, attempt 2; attempt 1 died lane-dead-no-report)

Attempt 2 inherited attempt 1's committed work; C1 stands with verdict `unverified
(required controls held)` per the frozen exclusion (claims.md v1–v3 + erratum). Two new
claims, design v4 `corpus/evidence/round34/claims-a2.md` (`7c7eb3a6`, frozen before data):

- C2 operability — spans of 32765..32767 bytes (PCRE "regular expression is too large" dead
  zone, S065): `TOK_DIRECT_SPAN_MAX` 32767→32764. Do-nothing 21/37 (seeds 5011/5023,
  `2592f9da`) → 37/37 on seeds 5011, 5023, 5033, 5047 on gate `a6307edf…` (`fe0f22e0`);
  selftest cases 254–256 (PASS 256); no-harm battery 11 rows PASS (`measure-a2/battery/`).
- C3 calibration — self-audit: `self-audit.py` + `audit-set.json` (43 checks) +
  `audit-dispositions.md`; first counted run 0 mismatches / 0 undispositioned
  (`0af0844c`); negative control 2 injected lies → 2 counted (`measure-a2/`).
- Frontier: S065 re-opened (pins unchanged; 32765 boundary re-confirmed); no new rows;
  knowledge `dead-zone-pcre-r34.md`; lesson round-34.md attempt-2 sections (3 mistakes:
  planned-hypothesis-as-measured, chunk matcher shipped with no selftest case, negative-control
  wiring read the pristine set).
- Motivating evidence: SCORECARD planned-r35 dead-zone row; `corpus/lessons/round-34.md`;
  R34ReviewRepairs SKILL-tally finding; watchdog `lane-dead-no-report chousa round=34`.

- Wave 2a2 (33-seat falsify/verify, 20 reports returned by the integration cutoff; 13 seats
  queued/unreturned, named in the round report): C2 re-derived and attacked — P2 holds
  (ExecC2Rerun fresh seeds 7311/7417/7589; RevC2Receipts; MutC2Counter ablation R1-R7
  load-bearing; MutC2Halves/Windows/Accept/Boundary/NoReader/Trunc controls miss except the
  semantically-exact window class; MutC2Keyed 2/6 fixture-keyed engines meet 37/37 — the
  output-only counter limit, routed r35); C3 first written form falsified by CritC3Claim
  (shallow-set do-nothing), reshaped in-round to the bounded structural-audit acquisition
  (62 checks, HEAD-byte reads, before 3 -> after 1-dispositioned; MutC3Inject 5/5,
  MutC3Bypass, RevC3Set); ScoutSkillTally banner finding fixed; RevGateDiff confirms the gate
  diff is one functional line; ExecSelftestEnv root-causes the LC_ALL=C fails to the \u2192
  json_unescape locale byte; ScoutSourcesA2 pins hold, census exit 0; RevShonenA2 extensive
  (boxes land [~], its evidence named); ConnectorOverlap: C2 fleet-unique, no contradiction.

## Round 35 — 2026-10-23 — the pinned binary and the routing witness

Two claims (operability, calibration), four repairs. Base `08be4c9e` (gate `a6307edf…2995b`);
freeze `0e167649` (claims.md v1 + two counters + the witness tool + five pre-data control receipts);
first landing `e87c5d7e` (gate `1f2fb4f5…c617`); final gate `a4768851…c38ad` after the wave's three
vector reports (`command` shadow, `head` forge, dead PATH fallback). Measurements on the final bytes:
C1 `GREP_PIN_MATCH=9/9` (seeds 3529/3539), C2 `WITNESS_SEPARATED=2/2 OUTPUT_EQUIV=2/2
LANDED_WITNESS=pass` (seeds 3529/3539), selftest `PASS (256 cases, 0 skipped)`, slen probe
`offsets=1 first=5`. Evidence under `.ufo/waves/round-35/{controls,measure,final,repairs}/`;
frozen design + erratum `corpus/evidence/round35/claims.md`; knowledge
`corpus/knowledge/{grep-pin-r35,keyed-engine-output-equivalence-r35,bash-local-expansion-r35}.md`;
QUALITY 45–49; sources 66 → 68 (S067 exec(3), S068 bash(1)); lesson `corpus/lessons/round-35.md`.
Wave: one v2 wave, 65 seats (27 attack), one dead seat (CritWitnessBlind, provider `cyber_policy`
refusal). Report `.ufo/reports/round-35/chousa.md`.

## Round 36 — 2026-10-23 — the engine-swap canary and per-record attribution

Two claims (operability, calibration), seven repairs. Attempt 1 (inherited; `.ufo/watchdog.log`
line 980 `lane-dead-no-report chousa round=36`) froze `corpus/evidence/round36/claims.md` and landed
the gate edits at `700bd5fcbf9abc118a6a0f078d51a2e7460c2878` — `sha256_hex_file` for
`verify-all --json`/`--pin` (S11), `json_unescape` in a `LC_ALL=C` scope with hand-built UTF-8
(S12), the `CHOUSA_GREP_PIN_ECHO` scrub in the capture environment (S13), the `GATE_GREP` drift
token (S14), selftest cases 257-261 (256 → 261). Before-state control committed byte-exact
`.ufo/waves/round-36/controls/base-gate-r36.sh` (`a4768851…c38ad`).

- C1 operability (lowest scored axis, 3/10) — `ENGINE_SWAP_CANARY=14/14` on seeds 36001, 36011,
  36301, 36311, 36331, 36341, 36351, 36361 against gate `a7d3922c…f54e8`; before `10/14` on
  the base control (S11-S14). Narrowed reading: four newly discriminated behaviours, ten
  contract behaviours that also pass the control (MutC1Arm: S11/S12 worth one point each;
  ScoutC1Counter: S7-S9 assert the contract, not per-call engine identity).
- C2 calibration — `WITNESS_PER_RECORD=5/5 OUTPUT_EQUIV=5/5 LANDED_ATTRIB=pass RENAMED=pass` on
  seeds 36001, 36011, 36301, 36311, 36371; before `2/5` with the round-35 witness on the base
  gate (V1/V4 separated; V2/V3/V5 admitted; renamed matcher killed).
- Repairs R1-R7: pin-echo scrub, drift token, absolute `sha256sum` + 64-hex contract, C-locale
  UTF-8 decode, selftest 257-261, pin-coverage ledger in `SKILL.md` (measured: 1 recorder call,
  `--version`, 0 matcher calls for `verify-integrity`/`verify-sweeps`), both counter docstring
  counts corrected to their receipts.
- No-harm: selftest PASS 261 under default, `LC_ALL=C`, scratch `TMPDIR`; claims 17/17, chain
  17/22, broken control 1/2, archives 3/3; scenario isolation probe not falsified.
- Inherited state: `corpus/evidence/round36/__pycache__` (one pyc, predates the freeze commit)
  discarded, `corpus/**/__pycache__/` gitignored; tracked counters/claims byte-identical to
  `700bd5f` (ScoutInherited).
- Frontier: sources 68 → 70 (S069 GNU grep(1) `-o`+`-b`; S070 coreutils sha256sum(1); tier A,
  opened 2026-10-23, census exit 0 with the two standing W04 warnings); knowledge
  `engine-swap-canary-r36.md`, `per-record-argv-attribution-r36.md`; QUALITY 50-52; lesson
  `corpus/lessons/round-36.md` (4 mistakes: docstring number-drift, crash debris, dispatch-count
  drift, scenario-assertion survivor).
- Wave: one v1 wave, 36 seats (attack 10 = 28%; 1 dead seat CritC1Swap, provider `cyber_policy`),
  specs and briefs `.ufo/waves/round-36/{w1-spec.json,w1-dispatch.json,w1-briefs/}`, seat reports
  `.ufo/waves/round-36/w1/`.
- Motivating evidence: r35 spot-check routed defects 1-9; `corpus/evidence/round35/claims.md`
  §Erratum; SCORECARD planned-r36 candidates; watchdog `lane-dead-no-report chousa round=36`.

## Round 37 — claim-pin provenance and pin-capture environment (2026-10-23)

Attempt 5 of the round (watchdog `lane-dead-no-report chousa round=37` ×5, orchestrator
deaths). Inherited from attempt 4: the freeze commit `b905217a7dfdcf58be1f0a4c0bf5f2d2d32a2d65`
(counters `corpus/evidence/round37/c1-count.py` / `c2-count.py`, gate fixes, selftest 262-267,
frozen `corpus/evidence/round37/claims.md`, base control `.ufo/waves/round-37/controls/base-gate-r37.sh`),
the wave-1 spec/dispatch (39 seats) and 8 returned seat reports under `.ufo/waves/round-37/w1/`.
Attempt 5 re-verified the inherited receipts, ran its own fresh-seed re-derivation, landed the
frontier and the report.

- C1 (operability, lowest axis): claim `sha256` pin hashed through one pinned absolute
  `sha256sum`; `CLAIM_PIN_PROVENANCE_MATCH` 2/7 → 7/7 on seeds 37001/37111/37133/37701/37901/37921
  (wave + L1), every receipt `gate_sha256=9fcac047…321cf39`; receipts
  `corpus/evidence/round37/receipts/c1-*.json`; knowledge `corpus/knowledge/claim-pin-provenance-r37.md`.
- C2 (freshness): `--pin` capture child scrubs `BASH_ENV` (`env -u`, S071);
  `PIN_CAPTURE_ENV_MATCH` 3/7 → 7/7 on seeds 37021/37211/37311/37721/37941/37961, every after-receipt
  `gate_sha256=9fcac047…`; receipts
  `corpus/evidence/round37/receipts/c2-*.json`; knowledge `corpus/knowledge/pin-capture-env-r37.md`.
- Separability by single-hunk gate mutants (`w1/ExecMutGateC1.md`, `w1/ExecMutGateC2.md`);
  counter-expectation mutants 6/7 exit 1 (`w1/ExecMutC1Counter.md`).
- No-harm (L1, recorded commands verbatim): selftest PASS 267 cases 0 skipped; claims 17/17,
  chain 17/22, broken control 1/2, archives `VERDICT_BEARING_EXPORTS=3/3`. The wave seat's
  `--root .` mis-invocation (`w1/ExecNoHarmPin.md`) is a lesson mistake (QUALITY 53), not harm.
- Frontier: S071 opened (coreutils `env(1)` `-u` semantics, local man page, no network);
  census 70 → 71 rows (A 64→65, mined 47→48), validate exit 0 both ends; lesson
  `corpus/lessons/round-37.md` (2 mistakes: no-harm mis-invocation scope, dispatched-vs-returned
  count drift); QUALITY 53; README index rows for r36+r37.
- Wave: v1 shape, wave 1 (39 seats, 8 returned, 31 dead — orchestrator deaths, never replaced)
  + one residual reviewer/critic call (residuals: <32 attack items from returned output).
  Spec/dispatch `.ufo/waves/round-37/{w1-spec.json,w1-dispatch.json}`, seat reports `w1/`.
- Motivating evidence: r36 claims §Erratum 7 (BASH_ENV hole) and routed defect 4 (claim-body
  pin through PATH); SCORECARD planned-r37 candidates; watchdog `lane-dead-no-report chousa round=37`.

## Round 38 (attempt 1, 2026-10-24)

- Declared claims (frozen `corpus/evidence/round38/claims.md` at freeze `504c1d2a…`):
  C1 operability (lowest axis 3/10) — the capture's child runs through ONE pinned absolute
  `env`; C2 calibration — receipts bind pre==post gate hashes + counter/expect/receipt
  digests, verified by a census-tied verifier. Routed inputs: the r37 counter-strength debt
  (F1/F4), the exported-env witness + SHELLOPTS=noexec candidates, the S070 supersede row;
  Errata 5/6 built on, never re-litigated.
- Measured: C1 2/7 → 7/7 (both base gates: `.ufo/waves/round-37/controls/base-gate-r37.sh`
  `a7d3922c…` and the new `.ufo/waves/round-38/controls/base-gate-r38.sh` `9fcac047…`);
  C2 0/7 → 7/7 (r37-counter control). Nine committed receipts, all `VERIFY: ok`; the two c1
  base receipts bind their control gates and refuse the landed gate. Selftest 267 → 272.
- Waves falsified the first freezing of BOTH surfaces (w1: CritC2Kill's four verifier kills,
  the counter_rc coupling at 4/7 on the base gate, the live BASH_ENV forge moving the r37
  control to 7/7, unsealed doctors, the shim shell injection, the table-binding race); the
  L1 closed each pre-wave-2 with the disclosed integration commits
  (`1f0add70…`, `8e93bc91…`); wave 2 confirmed every closure and found the next class
  (verifier-mutant pass-through → §Erratum 11; POSIXLY_CORRECT false-kill; the PYTHONPATH
  child channel; pre-run stale receipts) — closed/named in the final bytes with §Errata 9–13.
- Landed: gate env pin + selftest cases 268–272 + `unset POSIXLY_CORRECT`; counters
  `corpus/evidence/round38/{c1-count.py,c2-count.py,verify-receipts.py,expectations.jsonl}`;
  frozen claims + 13 errata; receipts `corpus/evidence/round38/receipts/` (9); controls
  `base-gate-r38.sh`; knowledge `env-pin-capture-r38.md` (S072) + `receipt-binding-r38.md`
  (S073 supersedes S070); lesson `round-38.md` (7 mistakes, QUALITY 55); QUALITY 55; README
  rows + frontier paragraph; SCORECARD r38 verdicts + planned-39; SKILL.md Gates table
  (selftest 272, r38 counter row); r37 knowledge docs' L1 repair.
- Waves: v1 shape, two waves of 32 (both validated under policy v1, dispatched as one task
  call each): w1 roles executor 6 / scout 3 / scribe 3 / reviewer 6 / critic 5 /
  mutation-tester 3 / sentinel 2 / revenger 2 / connector 1 / simplifier 1 (30 returned,
  2 dead — CritDoNothing, ScoutCounters, provider `cyber_policy`); w2 roles executor 4 /
  reviewer 7 / critic 6 / mutation-tester 3 / scribe 3 / scout 4 / sentinel 2 / revenger 1 /
  simplifier 1 / connector 1 (30 returned, 2 dead — W2CritEnvFinal, W2LabEnvScrub, provider
  `cyber_policy`). Round total 64 seats. Specs/dispatches
  `.ufo/waves/round-38/{w1,w2}-{spec.json,dispatch.json}`, seat reports `w1/`, `w2/`.
- Frontier: census 71 → 73 rows (S072 bash.info, S073 supersedes S070), validate exit 0 at
  both ends (standing W04 ×2 + the expected S070/S073 shared-URL warning). Sourced claim: C1
  rests on S072. Mistakes mined: 7 (lesson ## Mistakes). No tool installs by the lane.

## Round 39 — 2026-10-24 (L1 construction + prepared wave; host-mapped dispatch)

- Claims: C1 operability — the canonical capture's grandchild AND the
  verify-all section children run through ONE pinned absolute `bash`
  (`RESEARCH_GATE_BASH` override, `BASH_PROVENANCE` refusal before any mode
  runs); measured `ENV_PIN_CAPTURE_MATCH` 7/8 (base gate `0447ad14…`) → 8/8
  (seeds 39011/39111). C2 calibration — receipts bind `verifier_sha256` +
  `subject_counter_sha256`, re-derived with named refusals; measured
  `RECEIPT_BINDING_MATCH` 8/8 (seeds 39101/39121); the r38 pipeline is the
  before-state control (its receipts refuse: `predicate-mismatch` /
  `missing-field verifier_sha256`).
- Landed: gate bash pin + selftest cases 273–275 (`PASS (275 cases,
  0 skipped)`); counters `corpus/evidence/round39/{c1-count.py,
  c2-count.py,verify-receipts.py,expectations.jsonl}`; frozen claims;
  receipts (6) under `corpus/evidence/round39/receipts/`; controls
  `base-gate-r39.sh` + `mut-gate-path-env.sh`; knowledge
  `capture-bash-pin-r39.md` (S071 re-opened) + `receipt-verifier-subject-r39.md`;
  lesson `round-39.md` (4 mistakes, QUALITY 56); QUALITY 56; SKILL.md Gates
  table r39 row + r37 row repair (D5) + 275-case bumps; r38 claims Errata
  14–15 (D1/D2); r38 lesson correction block (D3/D6); SCORECARD r38
  attribution note (D4) + r39 verdicts.
- Host mapping: this seat holds no live L2 dispatch tool (accepted mapping,
  verified across seats 2026-10-24). The §3 floor is met by PREPARING the
  validated v1 wave spec under `.ufo/waves/round-39/` (32 seats, policy v1)
  for the orchestrator to dispatch between rounds; the L1's own construction
  runs supply the committed measurement evidence. Wave: 0 dispatched /
  0 dead this seat (prepared-but-undispatched itemized in the report).
- Discernment: three vacuous-fixture self-catches (identical-bytes doctored
  subject; stderr-only syntax crash as "weakening"; benign PATH-`env` shim)
  — fixes shown able to fail on the controls (mutant 4/8, base 7/8); the
  first c2 construction run (6/8) and the broken-shim mutant run were the
  red-before states, discarded uncommitted.

## Round 40 — r39 receipt repair and calibration correction (2026-10-24)

- Declared claims (frozen in `corpus/evidence/round40/claims.md`, claim-freeze commit `6c01a4144b3637cc57a989ab464f71b8ae69595a`): C1 operability, the lowest scored axis (3/10), audits the six-row active r39 receipt manifest; C2 calibration reconciles routed findings R2–R5. The frozen control receipts show C1 `3/6` and C2 `0/4` before round work.
- Measured on committed work tree `d164f88eb71a6c48a66ae1e7abfcb5fef82219d9`: `python3 corpus/evidence/round40/c1-count.py` → `R39_ACTIVE_RECEIPTS=6/6`, exit 0; `python3 corpus/evidence/round40/c2-count.py` → `R39_CALIBRATION_DISPOSITIONS=4/4`, exit 0. Full outputs: `corpus/evidence/round40/measure-after.txt`.
- R1: three stale c1 receipts were reissued against committed expectations bytes (`01cbdc3a…`); three active replacements verify. The four old c1 receipts retain their `3abd2dcb…` expectation digest and remain untouched; the draft s39003 stays superseded because its counter digest is uncommitted. Red-before refusals: `.ufo/waves/round-40/controls/r1-stale-before.txt`.
- R2: the committed draft `c1-mutenv-s39003.json` is retained and explicitly superseded; r39's receipt population was seven, not six. R3: the r39 report's `29 → 31` knowledge count is corrected by the commit-pinned `50 → 52` count. R4: not reproduced from current r39 artifacts (spec, plan, and report all reviewer 6 / revenger 2; the spot-check says 8 / 0); the conflict is preserved, not rewritten. R5: “two independent runners” is superseded by “two seeds, both L1 construction runs.”
- Landed in work commit `d164f88e…`: r39 claims erratum; R2–R5 disposition file; regenerated receipt set; re-opened S059 / S059 used-by update; rejected duplicate registration S074 with reason and flip; sourced knowledge note and coverage-map entry; prepared, validated v1 wave evidence. This log entry, lesson and measured SCORECARD record are appended in the round-40 metadata commit.
- Frontier: census 73 → 74 rows (A 67 → 68, B 1, C 5; mined 50, queued 19, rejected 4 → 5). S074 is an opened, tier-A rejected duplicate-row proposal; S059 remains the sourced row and its `used-by` changed from `corpus/knowledge/revision-binding-r31.md` to `corpus/knowledge/revision-binding-r31.md, corpus/knowledge/receipt-expectation-digests-r40.md`. Census validate exit 0 at both ends; W04 warnings are S051/S053/S073 before and those plus intentionally rejected S074 after. Knowledge files 52 → 53; the note adds the receipt-expectation-digest subground. Details and commands: `corpus/lessons/round-40.md` and `corpus/evidence/round40/measure-after.txt`.
- Wave: one v1 build-and-first-falsify spec, 33 seats, validated under policy v1 (band 32–64), role mix executor 6 / reviewer 6 / critic 6 / scout 3 / scribe 3 / mutation-tester 3 / sentinel 2 / revenger 2 / connector 1 / simplifier 1. Planner seat held by the L1; bounded planning rides scout/connector items. Prepared but not dispatched by this seat; 0 returned, 0 dead. No wave 2 was prepared because wave 1 has not returned attack items. Round total: 33 prepared L2 seats + 1 L1 = 34 accounted. Evidence: `.ufo/waves/round-40/`.
- Learning: expansion and quality improved narrowly; discernment unchanged pending a non-author admit/reject spot-check. No tool installs or pacman transactions.


## Round 41 — capture-invocation pinning + W04 dispositions (2026-10-24)

Two claims, both measured, both verified. Freeze: `corpus/evidence/round41/claims.md`.

- **C1 operability** (lowest scored axis): the canonical pin/drift capture's invocation surface — parent capture functions, startup (SELF/TS_UTC), and the captured verify-all child — resolved 20 PATH-dependent calls per pin+drift (728 in pin alone; instrumentation run recorded in claims.md). All 14 observed names now pin to GNU-verified absolute binaries via the r35 wrapper pattern; the child runs under fixed `CAP_CHILD_PATH` with `LD_PRELOAD`/`LD_LIBRARY_PATH` scrubbed. Counter `corpus/evidence/round41/c1-count.py`: control `1/12` → landed `12/12` (`controls/control-before.txt`, `measure-after-c1.txt`). Selftest 275/275 after repairing `metadata-stat-unavailable` to simulate through `RESEARCH_GATE_STAT`.
- **C2 calibration**: all five advisory W04 duplicate-URL warnings carry committed evidence-resolving dispositions (`w04-dispositions.tsv`): `0/5` → `5/5` (`controls/c2-control-before.txt`, `measure-after-c2.txt`). Advisory warnings are semantically correct (same-page distinct-section pairs including S075 on the coreutils page, required supersede row, retained rejected duplicate); contract-immutable cells mean dispositions record reason, not edits.
- Frontier step: S075 (mktemp man) + S076 (sed man/info) opened from installed copies only — no egress; knowledge `capture-path-pin-r41.md`; QUALITY criteria 57 (access receipts) + 58 (counter revision pins) mined from r40-wave findings; four mistakes rows.
- Round-40 wave dispositions: F1 fetch fixed in this round's seat contract (installed-file sources only); F2/F3 append-only corrections recorded in `corpus/lessons/round-41.md` (fleet side integrator-owned); worktree-vs-commit counter mismatch routed as measurement-target defect — not r40 falsification.
- L2: 35-seat v1 wave prepared+validated (plan/run exit 0); orchestrator dispatches (host surface). 0 dispatched by this seat.

## Round 42 — wave-4 quarantine-first: the 24-row register slice, adjudicated (2026-10-24)

Two claims, both measured, both verified. Freeze: `corpus/evidence/round42/claims.md` at
`dd63b6cfec5e1eafddb6662fc343e2ff6ab6aedc` (base `872bf3a3507875b382313f955d15960f9638256f`).
This round adopts NOTHING from the shokuknow package (fleet lane-addendum item 10,
wave-4 quarantine-first) and made NO external fetch (fetch-scope L0 `8d77e6c1` open).

- **C1 operability** (lowest scored axis, 3/10): the lane's quarantine scope became a
  runnable, re-derived surface — `tools/quarantine-check.py` re-derives the slice from
  the read-only register and examines every quarantined quote against the local capture
  material. `python3 corpus/evidence/round42/c1-count.py` → `SLICE_REDERIVE_MATCH=24/24`,
  `QUOTES_EXAMINED=43/43`, `REPRODUCIBLE=1/1`, `POSITIVE_CONTROL=1/1`,
  `NEGATIVE_CONTROL=1/1`, `MUTANT_DETECTED=1/1`, exit 0 (`receipts/c1-after-freeze.txt`);
  the do-nothing control (tree without the tool) exits 1 (`controls/c1-control-before.txt`).
- **C2 calibration**: every slice row carries exactly one verdict from the frozen
  vocabulary, agreeing with an INDEPENDENT re-examination, with a non-empty reason and
  flip condition. `python3 corpus/evidence/round42/c2-count.py` → `VERDICTED=24/24`,
  `CLASS_CONSISTENT=24/24`, `REASON_NONEMPTY=24/24`, `FLIP_NONEMPTY=24/24`,
  `VOCAB_OK=24/24`, `DUPLICATE_ROWS=0`, `ROWS_OUTSIDE_SLICE=0`, exit 0; the do-nothing
  control (one row's verdict flipped) → `CLASS_CONSISTENT=23/24`, exit 1
  (`controls/c2-control-before.txt`).
- Slice re-derived with the operator's own recipe: **24 data rows** (20 `payload-absent`
  + 4 unchecked-family). The register's `## By lane` summary (chousa 20) and its header
  (194) are stale; the M12 census's 25 is not reproduced. Adjudication: **15 `absent`**,
  **9 `unverifiable`** (1 bot-wall capture, 4 binary office documents never rendered to
  text, 4 register rows naming no locator), 0 `present`, 0 `mixed`. No row is called a
  fabrication on absent evidence; nothing is adopted.
- Frontier step: S077 (Poppler `pdftotext(1)` manual) opened from the installed copy —
  no egress; `corpus/lessons/round-42.md` (claims, 4 mined mistakes, Gate with admit and
  reject, sources opened, spot-check pending); QUALITY criteria 59 (a class that
  licenses a verdict names the evidence and its FORM) + 60 (every frozen counter names
  the cheapest gate that scores full marks without doing the work — operator proposal
  mined from `considerthese/2026-10-23.md`); census 76 → 77 rows, exit 0 at both ends (five advisory W04 warnings, S051/S053/S073/S074/S075, unchanged by this round).
- Id drift noted (scratch, no append): the lane's next free id S077 is also the staged
  package's first id; at adoption time the package's ids shift by one and every adopted
  citation is re-pointed BY DOCUMENT. L0 note filed.
- Wave: one v2 wave spec, 64 seats (24 build / 40 attack roles per the spec: reviewer 6,
  critic 8, mutation-tester 6, sentinel 3, revenger 2 = 25 attack of 64 = 39%),
  validator `plan` and `run` exit 0, wave-slot granted 64 seats; the dispatch was issued
  and the AgentSwarm call was still being composed when the round's time budget closed
  — 0 seat reports landed, so no seat outcome is claimed here.
- Learning: expansion improved narrowly (one opened source, one lesson, one runnable
  surface); quality improved (both counters verified against do-nothing controls; the
  register's own class column was shown to be unreliable and the lane's rule now checks
  the capture's FORM); discernment unchanged — the admit/reject sample still has no
  non-author spot-check. No tool installs, no pacman transactions, no egress.

## Round 43 — absent-class split and one local search-log adoption (2026-10-24)

Three claims, frozen in `corpus/evidence/round43/claims.md` before any seat scored.
No external fetch (L0 `8d77e6c1` open). The round-42 spot-check's routed repairs are
the motive: the absent-class split, the wave-completion rule, the inherited
working-tree disposition, the register-staleness L0, the 265/267 erratum, and the
S077 collision handled by document.

- **C1 operability** (lowest scored axis, 3/10): `tools/absent-split.py` splits the 15 round-42 `absent` rows into `misquote` (ratio ≥ 1/2) and `not-carried`. `c1-count.py` → 15/15, both classes nonempty (9 and 6), reproducible, exit 0. Missing-tool control exits 1.
- **C2 calibration**: an independent recompute agrees 15/15. Flipping S086 scores 14/15 and exits 1.
- **C3 depth**, sourced on S078: `corpus/knowledge/search-log-method-r39.md` cites the Europe PMC capture opened this round. The quote is in the capture. Staged S118 was re-pointed to S078 by URL, not by arithmetic. `c3-count.py` exit 0; missing-entry control exits 1.
- Rejected, with flip: `search-log-fields-r36.md` (staged S077 capture is a 267-byte / 265-character bot wall) and `search-tracking-record-r40.md` (column sentence not contiguous). Scratch census on the mirrored registry plus the S078 row exited 0 before the append. Collision guard: indented `  | S118 |` is caught; column-zero pattern misses it. Real collision is S077 only.
- QUALITY 61 mined from `considerthese/2026-10-24.md`: a validated spec is not a completed dispatch. Append-only erratum on the 265/267 nit in `corpus/lessons/round-42.md`; the r42 sentences are not rewritten.
- Inherited debt, deliberate: `PROVINCE.md` mode restored to 644 (content unchanged). Prior-wave registries, r41 `cells.json`, and untracked r40/r41 seat reports left untouched and named; they are not this round's work. Register staleness routed by L0; the register was not edited.

## Round 44 — freeze, before any seat scored (2026-10-24)

Three claims frozen in `corpus/evidence/round44/claims.md` before any seat scored.
No external fetch (L0 `8d77e6c1` still open). This entry is the freeze only.
After-measurements are a later entry.

- **C1 operability** (lowest scored axis, 3/10): `tools/parent-lifetime.sh` writes a wait log in the same process that spawned the children. Before: missing log exits 1 (`receipts/c1-before.txt`). `controls/pids0.receipt` and `controls/prose.receipt` exit 1. A two-child selftest log shows matching parent_pid and is not the claim measurement (`controls/selftest.receipt`).
- **C2 calibration**: the 39 inherited paths are frozen in `c2-count.py`. Missing table exits 1. `controls/all-left.tsv` scores `REVERIFIED=0/36` and exits 1. The three modified JSON files are required `left-named` with `not hunk-verified`.
- **C3 depth**, sourced on the RFC 7089 URL, not yet appended: missing entry exits 1 (`receipts/c3-before.txt`). The located quote was confirmed in the committed capture before this freeze. That confirmation is construction, not a seat score.
- Freshness will not be scored improved from a pre-round capture. The round-43 closure routed that inflation.
- Census start: `sources-census.sh validate --root /home/vgpnk/Projects/shokunin chousa` exit 0, five W04 (`receipts/census-start.txt`).

## Round 44 — landing (2026-10-24)

Claims frozen in `corpus/evidence/round44/claims.md` at `043f19a1db91288947493d9f879e61e7a9f07241`
before any seat scored. No external fetch: L0 `8d77e6c1` is still open, so every source was
opened from a committed capture. The round-43 closure's routed defects are the motive.

- **C1 operability** (lowest scored axis, 3/10): `tools/parent-lifetime.sh` writes a wait log
  from the same pid that spawned the children. `corpus/evidence/round44/parent-lifetime.receipt`
  carries `start parent_pid=3226659`, 64 `spawn` lines, 64 `reap` lines and
  `end parent_pid=3226659 … n_spawned=64 n_reaped=64`. `c1-count.py` → `N_SPAWNED=64/64`,
  `N_REAPED=64/64`, `PARENT_PID_MATCH=1/1`, `ZERO_PIDS=0`, `NAMES_MATCH=64/64`, exit 0.
  The missing-receipt, `controls/pids0.receipt` and `controls/prose.receipt` controls each
  exit 1. The receipt replaces the prose assertion the round-43 closure could not resolve.
  A wave-3 mutation seat showed that zeroing one `reap` child's pid scores `ZERO_PIDS=1`
  and that a changed `end parent_pid` scores `PARENT_PID_MATCH=0/1`, both exit 1.
- **C2 calibration**: the 39 inherited r40/r41 paths are dispositioned one by one in
  `corpus/evidence/round44/disposition.tsv`. The 36 untracked seat reports are
  `reverified-commit` — each file was re-read, its basename stem and its round token checked,
  its length checked, and its sha256 recomputed and compared with the table row before the
  path was committed as historical wave evidence. The 3 modified JSON paths stay `left-named`
  with reason `not hunk-verified` and are NOT committed. `c2-count.py` → `CONSISTENT=39/39`,
  `REVERIFIED=36/36`, `LEFT_NAMED=3/3`, exit 0; `controls/all-left.tsv` scores
  `REVERIFIED=0/36` and exits 1. Wave-3 mutation seats killed the gate with a blank reason
  (`REVERIFIED=35/36`), a corrupted digest (`REVERIFIED=35/36`), a deleted row
  (`LEFT_NAMED=2/3`) and a modified path reclassified as `reverified-commit`
  (`LEFT_NAMED=2/3`), all exit 1.
- **C3 depth**, sourced on S079: `corpus/knowledge/citation-version-binding-r36.md` cites lane
  S079 (RFC 7089), whose row URL is `https://www.rfc-editor.org/rfc/rfc7089.txt`; the located
  7-word quote `constitutes a promise that the resource state` is a substring of that URL's
  committed capture at byte offset 14896. `c3-count.py` → `ENTRY_CITES=1/1`,
  `QUOTE_LOCATED=1/1`, `URL_MATCH=1/1`, exit 0; the missing-entry control exits 1. A wave-3
  reviewer measured the S079 row at 11 columns with no pipe in any cell, and confirmed the
  entry cites `source: S079` and not `source: S081`.
- **Assimilation** (item 10, one theme: the version binding of a citation to a prior state):
  two entries adopted — `citation-version-binding-r36.md` (lane S079) and
  `citation-version-binding-r37.md` (lane S080 WARP FAQ, lane S081 NDL E2867) — and three rows
  appended to `corpus/SOURCES.md`, all `status mined` with the recheck prose stripped to
  `365d`/`90d`/`180d` and `used-by` naming exactly the adopted entries that cite each row.
  Collision check in scratch: `assimilation/collisions` is empty because S077 is not a
  row-start id in the staged append; it occurs once inside a cell of staged S093. The
  indented-guard fixture still catches `  | S079 |`. Ids were bound by document — the URL is
  the evidence and the id follows it — never by arithmetic: the staged file itself calls
  PRISMA-S "S079", and the landed offsets are −2, −11 and −11, so no constant shift works.
  Validate-before-append: `sources-census.sh validate --file` on the mirrored registry
  exited 0 with no E03/E04 before the first append.
- **Rejected, with reason and flip** (in the lesson's Gate block): staged S082, the SAMR record
  for GB/T 7714-2025, and the GB/T half of `citation-version-binding-r36.md` — round 43
  classed that row not-carried and this round did not fetch; flip: a text capture of that
  record contains the issued and effective dates as one contiguous span. Staged S093, the
  Portico page, and the Portico half of `citation-version-binding-r37.md` — round 43 classed
  that row misquote and a partial overlap is not the register's sentence; flip: a capture where
  the four-factor authenticity sentence is one contiguous span.
- **Freshness is unchanged, not improved.** Every capture opened this round was written
  before this round's launch. The round-43 closure routed that inflation and the next
  scorecard does not repeat it.
- **QUALITY 62** mined from `considerthese/2026-10-24.md` (2026-10-24), "Count claim errata
  per round": the count is the number of lines matching `^Erratum [0-9]+` in the round's
  claims file. Shown able to fail: `controls/errata-two.txt` counts 2 and exits 0,
  `controls/errata-zero.txt` counts 0 and exits 1. This round's own claims file counts 0.
  The considerthese file was not edited.
- **QUALITY 63** from a wave-3 probe: a launcher's exit status is not evidence that its seats
  ran. `tools/parent-lifetime.sh` exits 0 on a malformed dispatch JSON with `n_spawned=0`;
  the receipt's `n_spawned`/`n_reaped` is the tell.
- **Wave evidence.** Wave 1's 64 seats all died at spawn on `Cannot combine --prompt with
  --auto`; those names stay dead and are not replaced. Wave 2 ran 32 seats and produced 31
  reports, but its parent receipt was truncated at 5 reap lines because the orchestrator
  process died mid-wait, so it carries no `end parent_pid=` line and proves nothing about
  parent lifetime. Wave 3 ran 32 seats with the corrected launcher; its receipt carries
  `end parent_pid=3635446 … n_spawned=32 n_reaped=32`, but 27 of its seats were killed by
  the 420 s timeout and 23 produced no report. The three waves total 128 seats, the round
  ceiling, so no further wave was dispatched.
- **Inherited debt still open.** The three modified JSON paths stay named and uncommitted; the
  round-43 L0 that asks the operator to rule on them is not duplicated here.

## Round 45 — freeze, before any seat scored (2026-10-25)

Three claims frozen in `corpus/evidence/round45/claims.md` at
`d82cec904bf0fb8736886b9f17be913c7807427a`. No external fetch (L0 `8d77e6c1` still open).
Motive: the round-44 closure's routed defects D5 (launcher exit contract), D2 (Gates rows)
and D1 (a counter that could not run from the lane tree alone), plus the next shokuknow
theme. Round 42 already hand-checked the quarantine slice, so this round assimilates.

- **C1 operability**: control — the round-44 launcher scores `CASES_MATCH=1/5`, exit 1
  (`controls/c1-control-r44-tool.txt`).
- **C2 calibration**: control — the base tree scores `UNREGISTERED=26` of 51, exit 1
  (`controls/c2-control-base.txt`).
- **C3 depth**: controls — no entries, `ENTRIES=0/2`, exit 1; a forged span manifest passes
  `--lane-only` (the named blind spot) and fails the default mode
  (`controls/c3-control-do-nothing.txt`, `controls/c3-control-forged-span.txt`).
- Census start: `sources-census.sh validate --root /home/vgpnk/Projects/shokunin chousa`
  exit 0, five W04, 81 rows. Collision check: `assimilation/collisions` empty; the indented
  guard row is caught (`assimilation/guard/`).

## Round 45 — landing (2026-10-25)

Work landed at `5e8c7ad2f7b8254d83358820286e3d12ca4672d1`; post-wave-2 corrections in the
round-45 closing commit. Two v1 waves: wave 1 (build, 46 seats, 45 reports, 1 dead) and
wave 2 (falsify, 38 seats, 38 reports). Round total 84 seats.

- **C1 operability**: `tools/parent-lifetime.sh` exits 3 when the end line records zero
  spawned tasks or a seat timed out, requires `--timeout` in dispatch mode and records
  `timeout_s=` in the start line. `c1-count.py` → `CASES_MATCH=5/5`, exit 0. Wave 2 killed all
  four mutants of the landed tool and found an errexit regression (a bare `wait` under an
  inherited errexit truncates the receipt); the guard is restored
  (`controls/c1-errexit-probe.txt`).
- **C2 calibration**: twelve Gates rows added to SKILL.md (rounds 31–34 v1/v2/v3, 40, 41,
  `tools/quarantine-check.py` with round 42, `tools/absent-split.py` with round 43, 44, 45,
  `tools/parent-lifetime.sh`, the QUALITY 64 check). `c2-count.py --list` → `REGISTERED=54/54`,
  `UNREGISTERED=0`, exit 0. Wave-2 row reviews corrected the round-40 row (a nonexistent
  note; its C2 reads a fleet report) and the round-31 row (two wrong paths).
- **C3 depth / assimilation** (item 10, one theme: what an AVeriTeC archive field documents,
  and how many stored values are archive links): `evidence-archive-field-policy-r41.md` (S082
  README, S083 v3 paper) and `evidence-snapshot-coverage-r40.md` (S084 train.json), staged ids
  S139/S140/S132 re-bound by document. Re-grounded from on-disk captures: the staged
  inference narrowed; the staged "6,510 hold a non-empty archive.org URL" replaced by the
  recount (5,959 web.archive.org values; 1,582 sourced answers with no archive key); the
  paper's double-archived 404 warning added. Spans, offsets and capture digests committed
  (`corpus/evidence/round45/spans/`, `spans.tsv`, `counts.json`, `build-spans.py`).
  `c3-count.py` default and `--lane-only` both pass. Scratch mirror validated before the
  append, exit 0, no E03/E04. Rejected with flip: the staged pool-versioning amendment.
- **QUALITY 64** (round tag, from `considerthese/2026-10-24.md`, 2026-10-24) with check
  `corpus/evidence/round45/tag-count.py`: r35–r44 → `TAGGED=0/22`, exit 1; round 45 →
  `TAGGED=3/3`, exit 0; a wave-2 indented-row forge fixed and kept as a control.
  **QUALITY 65**: archive coverage counted by value, not by field.
- **Misroot sweep**: four wave-1 reports written under the fleet root were copied
  byte-exact into the lane, `cmp`-verified and removed from the fleet root.
- **Inherited debt still open**: the three modified r40/r41 JSON paths stay left-named and
  uncommitted; L0 `chousa | round-43` is unanswered.

## Round 46 — 2026-10-25 (hyaku run 6; claims frozen `c2f0e9d1`, landed `d09fc8e7`)

Three claims, three axes, each verified without the others. No external fetch
(L0 `8d77e6c1` still open); every source read from the on-disk campaign cache.

- **C1 operability** (lowest scored axis, 3/10; round-45 closure D7):
  `tools/inference-ground.py` makes an entry's `#### Inference` section checkable
  — every bullet must cite a source, and every backticked/quoted phrase or figure
  in it must appear in the spans of the sources it cites (or be the designator of
  a cited document). Six declared fixtures, `c1-count.py` before `TOOL=absent
  0/3 0/3` → after `POSITIVE_PASS=3/3 JUNK_KILLED=3/3 C1=PASS`. Controls: an
  always-exit-0 tool scores `0/3`, a citation-presence-only tool `1/3`. Honest
  residual: the check proves presence, not entailment — the round-45 D7 body
  still passes (`CritC1Attack`), routed to round 47.
- **C2 calibration** (round-45 closure D8): `c2-count.py` enumerates the lane's
  executables from three legs (tools/, the round-45 counter pattern, and every
  `*.py`/`*.sh` a SCORECARD or claims cell names) and requires each inside a
  `## Gates` row. Before `REGISTERED=55/71 UNREGISTERED=16` (freeze tree; bare
  base `55/68`, 13) → after `REGISTERED=72/72 UNREGISTERED=0`, exit 0. Five rows
  added covering thirteen historical instruments (registered as `instrument`,
  two of which state in their own headers that they count and do not gate) plus
  the round-46 tool, counters and span builder. Forges refused after the waves:
  fenced row, HTML-comment row, `.pyc`-suffix row, prose paste, six-cell and
  no-`exit` rows, row after the next `## `.
- **C3 depth / assimilation** (item 10, one theme: what makes a support verdict
  durable, and how a later corpus binds each citation to an archived state):
  `evidence-pool-versioning-r39.md` (S085 FEVER page, S086 FEVER paper, S087
  Zenodo record) and `…-r39-amendment-2026-10-23.md` (S088 AVeriTeC page, S089
  AVerImaTeC HTML), staged ids re-bound by document (−35/−35/−35/−39/−39), the
  round-45 reject's flip met in full. Eleven quotes located with context in
  `corpus/evidence/round46/spans/`; `build-spans.py --check` re-derives 11/11;
  `c3-count.py` default and `--lane-only` both pass. Staged misreadings corrected
  in the entries (field pairing is practice not invariant; the hedge tracks a
  missing original URL; the temporal rule is the successor corpus's; "limited …
  to those published before" is not verbatim).
- **Frontier / SOURCES**: 84 → 89 rows, five added (S085–S089), census exit 0
  before and after, the same five W04. Quarantine: S086's URL is in the 24-row
  slice (register line 54, `payload-absent`); hand-checked, all three register
  quotes present in the capture after removing the PDF column interleave —
  verdict present, row adoptable.
- **Wave**: v1, two waves, 64 seats total — wave 1 build+falsify 32 (reviewer 9,
  scribe 7, scout 5, executor 4, critic 3, mutation-tester 2, connector 1,
  sentinel 1), wave 2 falsify 32 (reviewer 20, critic 4, mutation-tester 3,
  scout 3, sentinel 2). Two wave-2 seats and their findings are recorded in the
  round report.
- **Instrument revisions after the freeze, disclosed**: `c1-count.py`,
  `c2-count.py`, `c3-count.py` and `tools/inference-ground.py` were each
  tightened toward the frozen sentence after wave-1 mutation and sentinel
  findings; before receipts were re-measured with the final revisions and
  value-neutrality is measured (`corpus/lessons/round-46.md` mistake 12).
- **Inherited debt still open**: the three modified r40/r41 JSON paths stay
  left-named and uncommitted; L0 `chousa | round-43` and `round-44` unanswered.

## Round 47 — 2026-10-25 (polarity probe, dependence registry, claim-support adoption)

Claims frozen in `corpus/evidence/round47/claims.md` at `22a44b8b` before any seat
scored; base `9a9f94db`. No external fetch (L0 `8d77e6c1` open).

- **C1 operability** (round-46 named limit "entailment", the D7 class):
  `tools/inference-ground.py` gains `INF_POLARITY_FLIP`, a windowed stem-sharing negator
  mismatch. `c1-count.py` before `JUNK_KILLED=0/3 CANARY=fail C1=FAIL` → after `3/3 3/3
  CANARY=pass R46_COUNTER=pass R46_ENTRIES=2/2 C1=PASS`. Motivating evidence: the
  round-46 `CritC1D7` body that strings real tokens into three inversions passed; it now
  exits 1. Wave 1 measured 9/10 false refusals on correctly-reasoned bullets
  (`LabC1FalsePos`); implicit negators and a clause-bounded span look-back cut the tuning
  set to 5/10; the counter's `R46_ENTRIES` leg caught the first widening's regression.
  Not entailment (`CritC1Survivors`: twelve survivors outside the windows).
- **C2 calibration** (round-46 named limit "mention, not dependence"; closure routed
  defects 2 and 4): `c2-count.py` adds a dependence closure and the QUALITY/SKILL
  check-named leg, requires the path in a row's `entry` cell with an exit code in its
  verdict map, counts dangling rows, and enforces FLOOR=92 in code. Before (freeze tree)
  `MISMATCHES=25` freeze counter / `21` final counter → after `MISMATCHES=0` on both.
  Motivating evidence: `corpus/evidence/round45/tag-count.py` and three other QUALITY
  `Check:` scripts were invisible to the round-46 set (`RevC2TagCount`). Thirteen rows
  added or repaired; post-freeze counter repairs disclosed (lesson mistake 3).
- **C3 depth / assimilation** (round-46 named limit "anchor cells"; theme: what a support
  test is, how it is applied, how reliable it is): `claim-support-test-r37.md` (S085,
  S090, S091) and its amendment (S092–S094), staged ids re-bound by document
  (−12/−8/−8/−21/−21/−21); 35 capture-bound spans; every anchor cell's `char N` is a
  located quote offset; four quarantine register rows hand-checked `present`. Staged
  corrections: CFEVER is AAAI-24 not 2021; four "not read" unknowns were in the captures;
  0.6841 and 0.792 measure different things; the 202 relabels are pool-dependence.
- **Frontier / SOURCES**: 89 → 94 rows (S090–S094), S085 re-bound; census exit 0 before
  and after, the same five W04. QUALITY 67 (polarity) and 68 (per-round receipt
  re-verify, from `considerthese/2026-10-24.md`). The QUALITY 68 run found four round-39/40
  receipts failing since round 41's gate edit — routed to round 48.
- **Inherited debt still open**: the three modified r40/r41 JSON paths stay left-named
  and uncommitted; L0 `chousa | round-43` and `round-44` unanswered.

## Round 48 — 2026-10-25 (held-out precision regression and counter sensitivity)

Claims froze in `corpus/evidence/round48/claims.md` at `4bbd2348578bb6288c0700dabf37cea04225bfb6`, after the pre-candidate control: R47 tool `CORRECT_BULLETS_PASS=9/12`, below the frozen 11/12 floor; old R47 C1 counter remained `C1=PASS`. Worktree candidate landed at `671b096e2bd5d5b0994bcd7ab8c17abaf16c62c7`; its archive-after receipt in `corpus/evidence/round48/measure-after.txt` binds the measured tool sha and command outputs.

- **C1 operability**: the false-refusal fixtures now produce `CORRECT_BULLETS_PASS=12/12` (floor 11), all five refinement fixtures pass, legacy R47 controls remain `C1=PASS`, and the five R47 survivor mutations are killed `5/5`. `mutation-check.py` and the no-read name-key control are separate parts of the frozen composite; `c1-count` alone is not the complete claim. Residual: the 12 cases recycle R47 held-out texts and do not estimate general-language precision; pre-change W1 probes exposed further false-refusal classes but were not re-run after the final adjustment. `inference-ground.py` documents the measured window changes and remaining lexical limits.
- **Calibration / record corrections**: `round47/c2-count.py --list` on the final C1 code tree → `ENTRY_POINTS=97 REGISTERED=97/97 MISMATCHES=0 C2=PASS`; the R47 C2 `94/94` final, `93/93` freeze values and `92` floor remain historical and correct. R39/R40 active receipts re-verified `6/6` at each adding commit (`d164f88`, `6d914e9`); tip counter is `2/6`, four expected `gate-sha256-mismatch` refusals after `1bd9001` changed the gate. No receipt bytes were rewritten.
- **Frontier / SOURCES**: R47 verifier spot-check opened locally and recorded as own-work `S095` (Gate quote and use in `lessons/round-48.md`); registry 94→95, one tier-A own-work row, no older status/recheck/used-by edits. No knowledge entry is admitted. All 24 chousa rows in the wave-4 quarantine slice were hand-checked from local captures; no external live fetch. `considerthese/2026-10-24.md`'s “read-only cloud-agent recheck” proposal is only locally implemented; its cloud-agent part remains unapproved by L0 `8d77e6c1`.
- **Waves**: two v1 waves, 32+32=64 seats. W1 roles: reviewer 13, critic 8, scout 7, executor 4; Attack04 died on provider `invalid_prompt` and was not replaced. W2 roles: reviewer 14, critic 7, scout 6, mutation-tester 3, connector 1, scribe 1; no dead W2 seats. L1 held the planner/data-walk seat. W1/w2 reports and assigned handles are retained under `.ufo/waves/round-48/`.
- **Inherited**: three modified R40/R41 JSON paths remain left-named and uncommitted, not lane-authored R48 work; no new L0 question. No tool installs.

- **Post-wave control/label dispute**: W2 `AttackDoNothing.md` shows a name/hash-key lookup can pass `c1-count.py --tool` alone. The frozen composite is countered by `controls/name-key-control.py`: at the default tool path, C1-component passes but the required mutation check rejects `MUTATION_NOT_APPLIED`; the hash-key variant was not separately run through the composite. W2 `AttackPrecision.md` disputes the a05 label; the R47 non-author closure had treated it as a false refusal. This report asks the current closure to re-open a05 and one present/absent quarantine pair; no lane seat is a non-author.

## Round 49 — 2026-10-25 (first package adoption under section 10; derived-index theme; section-10 adopter)

Claims froze in `corpus/evidence/round49/claims.md` at `fe740e7838b338d17fec9338c909557e6e7fed7d` after scoring the do-nothing controls (`controls/c1-before.txt`: no tool `C1=FAIL`, copy control `SETS_PASS=0/3`; `controls/c2-before.txt`: lane `C2=FAIL`, staged-copy control `REF_ID_UNBOUND=11 C2=FAIL`). Tool candidate `65940928cc9332b386bcbca92571451cc4374cbe`; adoption `1254ab262b2fbc199923345d389f85d0debbef6e`; tool fixes from W1 `ReviewToolCode` (tab headings, calendar-valid dates, non-UTF-8) `4ce61fc59e30b9215514841fe658e96cc998d138`; after-measurement `corpus/evidence/round49/measure-after.txt` (`87e93353`). No fetch; L0 `8d77e6c1` open.

- **C1 operability (capability)**: `tools/assimilate-rows.py` — section-10 adopter (by-document renumbering, one simultaneous substitution, census-schema rows, 0–3-space collisions). `python3 corpus/evidence/round49/c1-count.py` → `SETS_PASS=3/3`, GUARD/PIPE PASS, `C1=PASS`. Named limit (W1 `CritForgeC1`): a replay of the tool's outputs also passes the fixed-input counter (QUALITY 72).
- **C2 depth (sourced)**: `corpus/knowledge/aggregator-vs-source-r36.md` and `citation-count-semantics-r37.md` adopted by document; eight rows S096–S103 (staged NCPSSD homepage row refused); 28 located quotes in `corpus/evidence/round49/spans.tsv`. `python3 corpus/evidence/round49/c2-count.py` → `BOUND=8/9 REFUSED=1 … CAPTURE_BOUND=28/28 … C2=PASS`. Post-freeze `build-spans.py` change disclosed in `corpus/evidence/round49/claims-erratum.md` (bare CR in UTF-16LE spans vs the counter's universal-newline read; before the change `CAPTURE_BOUND=21/28`).
- **Frontier / SOURCES**: registry 95 → 103 (A +3, B +5), no existing row touched; census `validate --root` exit 0 (five pre-existing W04). Search-log entry Round 49. Section-10 collision check: 14 collisions S082–S095, guard proof in `.ufo/waves/round-49/assimilation/guard-proof/`; scratch validation `assimilation/validate/census.txt` exit 0.
- **Corrections / quality**: a05 propagations corrected in `corpus/lessons/round-49.md` (`a05-check.py` exit 1 → 0); QUALITY 69 round-49 note (P2 false-negative class unmeasured; a05 ruling; pointer fix), QUALITY 71 (capture-age line, from `considerthese/2026-10-25.md:55-56`), QUALITY 72 (substance floor / perturbed-input leg). `SKILL.md` Gates +2 rows; round-47 registry `REGISTERED=104/104`.
- **Inherited**: the round-48 uncommitted QUALITY 69 sentence verified true (W1 `ExecQualityWindows`) and landed; the three R40/R41 JSON leftovers reverted to committed bytes, pre-revert diffs in `.ufo/waves/round-49/inherited/`.
- **Waves**: W1 40 seats (scribe 17, executor 9, reviewer 4, critic 4, mutation-tester 2, connector 2, scout 2); W2 35 seats (executor 16, scribe 5, critic 4, mutation-tester 3, reviewer 3, connector 2, simplifier 1, scout 1). L1 held the planner seat. Host `/tmp` was full (0 bytes free) mid-round; L1 and W2 scratch moved to `/dev/shm`. No tool installs.

## Round 50 — 2026-10-25 (adopter self-test; Chinese citation-checking theme adopted by document)

Claims froze in `corpus/evidence/round50/claims.md` at `6a068f2ae4847a1e4aa959f088a39ddc1b167bc0` after scoring the do-nothing controls (`controls/c1-before.txt`: base tool `LEGS=2/5`, echo `4/5`, constant `2/5`; `controls/c2-before.txt`: lane `C2=FAIL`, staged copy `REF_ID_UNBOUND=15`). C1 candidate `ec52e632`, hardening `2573dc16`; C2 adoption `74794db0` and the wave-2 narrowing in the round's final commit. After-measurement: `corpus/evidence/round50/measure-after.txt`. Disclosures: `corpus/evidence/round50/claims-erratum.md`. No fetch; L0 `8d77e6c1` open.

- **C1 operability (capability extension, plumbing)**: `python3 tools/assimilate-rows.py --selftest` with a hand-written `expected.json`; `python3 corpus/evidence/round50/c1-count.py` → `LEGS=5/5`, `PERTURB_PASS=6/6`, `C1=PASS`. The frozen counter is replayable (a forge passes it); the supplementary `c1-supplement.py` is `5/5` for the real tool and fails the forge `1/5`.
- **C2 depth (sourced, ground)**: `cnki-citation-check-r40.md`, `citation-matching-semantics-r41.md`, `istic-citation-verification-r39.md` adopted by document; rows S104–S106 (the 教师 manual refused); `python3 corpus/evidence/round50/c2-count.py` → `BOUND=3/4 REFUSED=1 … C2=PASS`. W2 narrowed all three entries (the staged "amber" is the PDF's 橙色; the hover screenshots name three compared parts; the ISTIC page's reuse concession is for 中国科学院 users).
- **Frontier / SOURCES**: registry 103 → 106 (A +1, B +2); census exit 0 before and after, the same five W04. QUALITY 73–80. SKILL.md Gates: `assimilate-rows` row replaced, `chousa round-50 counters and checks` row added; `round47/c2-count.py --list` → `REGISTERED=114/114`.
- **Mistakes mined (lesson, 8 rows)**: stale restated counts, report before WAVE-DONE, body cross-references adopted, 13 wave-1 seats lost to a seat-name collision with parked round-49 agents, CJK blind spot in `inference-ground`, set-compared self-test, text sweep blind to screenshots, staged amber/orange contradiction.
- **Post-freeze tool changes**: `tools/assimilate-rows.py` (self-test hardening, `used-by` across twin staged ids), `tools/inference-ground.py` (`has_two_words`: four CJK characters). Round-46/47/48 counters output-identical.
- **Waves**: W1 42 seats (scribe 18, executor 10, critic 4, reviewer 3, mutation-tester 2, connector 2, scout 2, simplifier 1; 13 returned round-49 reports by name collision, counted dead); W2 43 seats (reviewer 9, critic 9, executor 7, scout 6, mutation-tester 6, scribe 3, connector 2, simplifier 1; all 43 reports). L1 held the planner seat. Round total 85.
- **Inherited**: round-49 late seat reports committed (`4d13657e`, `ec52e632`, `2573dc16`). No tool installs.

correction: LOG.md:1803 ("28 located quotes … `CAPTURE_BOUND=28/28`") superseded by 31 — the round-49 manifest has 31 data rows (`awk 'NR>1 && NF' corpus/evidence/round49/spans.tsv | wc -l` → 31; `corpus/evidence/round49/measure-after.txt`); resolved by `corpus/evidence/round50/stale-count-check.py`.

## Round 51 — adopter v3 and a nonce counter; Japanese/Chinese search-record theme adopted by document; pointer calibration (2026-10-25)

Evidence that motivated the round: the round-50 closure's routed defects (`corpus/lessons/round-50-verifier-spotcheck.md` section 6: an unpinned receipt revision, a replayable C1 counter, seat-name reuse, filename drift) and the SCORECARD round-51 plan (adopter cites only `source:` ids, three latent input defects; adopt the next package theme). Claims frozen at `d603f6f00f78d64f123d3aed2dd9f8701547a4ba` after their do-nothing controls were scored (`corpus/evidence/round51/claims.md`, `controls/`); errata E1–E5 in `claims-erratum.md`. No external fetch (L0 `8d77e6c1` open).

- **C1 operability.** `tools/assimilate-rows.py` cites only the id after `source:` on header lines, substitutes an entry's own ids only, lists body-only ids (`bodyonly.tsv`, `bodyclash.tsv`), reads document identity after the escaped-pipe rewrite, splits registry rows with the escaped-pipe splitter, refuses a registry without `## Registry` or with an S### row outside it and a `source:` id that is neither staged nor a Registry row; `--cites all` and `ASSIMILATE_CITES` keep the old reading. Frozen counter `python3 corpus/evidence/round51/c1-count.py`: lane tool at the base `LEGS=1/5` → `5/5`; controls base 1/5, echo 2/5, const 1/5, flag-noop 2/5. W1 `R51CritForgeC1` showed a 94-line forge passes the frozen counter 5/5 (it keys on the counter's fixed directory names); W2 `R51W2CritForgeSupplement` forged the supplement's first form too. The post-freeze `c1-supplement.py` (ten legs, random directory and entry names) passes the real tool 10/10; forge-dirname 1/10, forge-dual 3/10, the first candidate 3/10 (`controls/c1-supplement-controls.txt`). The round-49 and round-50 one-shot counters fail at the new default (round-49 passes with `ASSIMILATE_CITES=all`).
- **C2 depth (sourced).** Entries `japanese-search-record-r38.md`, `chinese-search-record-r39.md`, `japanese-search-record-r38-amendment-2026-10-23.md` on six documents S107–S112 (staged S109 S110 S116 S117 S119 S126); the seventh, a `.docx` (staged S125), refused because its text exists only in a compressed zip member the frozen span pipeline cannot read. `python3 corpus/evidence/round51/c2-count.py`: `C2=FAIL` (`ENTRIES=0/3 BOUND=0/7`) → `C2=PASS` (`BOUND=6/7 REFUSED=1`, a 70-quote manifest, `QUARANTINE_VERDICTS=6/6`: 2 present, 4 absent-as-written, none blocking). W2 narrowed the three entries, the S107 row and the README blocks (Mistakes row 9).
- **C3 calibration.** `python3 corpus/evidence/round51/c3-count.py`: `DANGLING=5` (first run 8: a leading-dot tokenizer defect, erratum E1) → `DANGLING=0` via four append-only `correction:` lines and one SHONEN pointer; existence, not truth.
- **Frontier step.** Rows 106 → 112 (A 5, B 1); census exit 0 at start and end; eight (then nine) mistakes mined in `corpus/lessons/round-51.md`; the considerthese pick (the open-items age line) implemented as `open-items-age.py`; QUALITY 81–86; SKILL.md Gates rows registered (`python3 corpus/evidence/round47/c2-count.py` `MISMATCHES=0`).
- **Waves.** W1 48 seats, W2 41 seats (`w1-results.json`, `w2-results.json`); the L1 held the planner seat.

## Round 52 — an OOXML capture text form as a lane tool; the search-record theme continued by document (2026-10-26)

Evidence that motivated the round: the round-51 closure's routed defects (`corpus/lessons/round-51-verifier-spotcheck.md` section 6: a forgeable C1 counter with fixed directory names; the NIPH `.docx` refused for its capture form with a zip-member reader as its flip) and the SCORECARD round-52 plan. Claims frozen at `37468eadd8d098e80289b2f31a22de3872d4a1f6` after their do-nothing controls were scored (`corpus/evidence/round52/claims.md`, `controls/c1-before.txt`, `controls/c2-before.txt`, `controls/c2-controls.txt`).

- **C1 operability (capability).** `tools/capture-text.py` (candidate `804a4537`) prints the text form of an OOXML `.docx` capture and locates a quote's offset in it. `python3 corpus/evidence/round52/c1-count.py`: base `LEGS=0/9` (tool absent) → `LEGS=9/9 C1=PASS`; controls naive 4/9, cache-txt 0/9, const 0/9. W1 `R52CritForgeC1` passed the frozen counter 9/9 with an 85-line regex forge keyed to the generators' XML spelling (`controls/forge-shape.py`); the post-freeze `c1-supplement.py` re-spells the same documents and pins the NIPH text digest: the tool 4/4, the forge 0/4 (erratum E1). After W1 the tool also refuses non-Word main parts, inflated parts, root-escaping targets and encrypted members, and percent-decodes targets (E2).
- **C2 depth (sourced).** Entries `japanese-search-record-niph-form-r52.md`, `japanese-prisma-item-wording-r40.md`, `chinese-prisma-s-reception-r52.md` on S113–S116 (staged S111 S112 S125 S129, renumbered by document). `python3 corpus/evidence/round52/c2-count.py`: `ENTRIES=0/3 BOUND=0/4 C2=FAIL` → `BOUND=4/4 QUOTE_ROWS=39 CAPTURE_BOUND=39/39 … C2=PASS`. Expansion credit three documents: S113 is a second carrier of the PRISMA-S reading the lane holds through its SinoMed record.
- **Frontier step.** Rows 112 → 116 (A S114 S115, B S113 S116); census exit 0 at start and end; six mistakes mined in `corpus/lessons/round-52.md` (the round-51 S120 offset `char 39411` re-located as 8996 in a named form; the representation forge; the fleet-root misroot by W1 `R52MutBuildSpans`); QUALITY 87–90; considerthese pick `corpus/evidence/round52/verdict-gap.py` (`VERDICT_GAPS=2 UNPARSED=1`); SKILL.md Gates rows registered (`python3 corpus/evidence/round47/c2-count.py` `MISMATCHES=0`).
- **Not landed, planned:** the adopter twin-id and refusal-order patch (W1 `R52ExecAdopterTwin`) and the anchored-correction check (W1 `R52ExecPointerAnchor`).
- **Waves.** W1 45 seats, W2 38 seats (`w1-results.json`, `w2-results.json`); the L1 held the planner seat.

## Round 53 — adopter v4; search-record instruments by document (2026-10-26)

Evidence that motivated the round: the round-52 closure's routed defects (`corpus/lessons/round-52-verifier-spotcheck.md` section 6: the adopter twin-id `held` label / refusal ordering had been built in scratch, and `correction:` pointers proved only target existence) and the SCORECARD round-53 plan. Claims froze at `a6ff732c70011f11c9beb681d832cedc6e75f566` after do-nothing controls (`corpus/evidence/round53/controls/`); candidate adopter `32aab5edd70e43145cae72ec872278f3bc6efba7`.

- **C1 operability (lowest scored axis, capability extension, plumbing).** `tools/assimilate-rows.py` now reserves `held` for registry-carried URLs, labels same-run duplicates `twin`, prints separate `HELD=`/`TWIN=` counts, validates cited rechecks before row creation, and refuses malformed registries before entry refusals even without `--entry`; selftest has twin-recheck and refusal-order cases. Frozen counter `python3 corpus/evidence/round53/c1-count.py`: base `LEGS=1/8 C1=FAIL` → candidate `LEGS=8/8 C1=PASS` (three unseeded runs and `--seed 7`; W1 seed runs 45/45 required cases). Controls base 1/8, const 0/8, refuse 0/8, relabel-only 5/8, all-twin 2/8. W1 `R53CritForgeC1` built a 189-line forge that passes 8/8 by canning REAL on a package digest, shape-keying calendar validation and string-stubbing the R50 selftest; post-freeze supplement `c1-supplement.py` is 3/3 for the landed tool and 1/3 for that forge (erratum E1). The `--per-leg 0` vacuous pass and cadence-only mismatch remain named, not fixed (E2–E3).
- **C2 depth (sourced, ground).** Entries `search-tracking-record-r40.md`, `western-instrument-alignment-r50.md`, `quality-control-guideline-issued-text-r48.md`; four bound documents S117–S120, with S118 cited by two entries through staged twin ids S185/S195; S190 refused. `python3 corpus/evidence/round53/c2-count.py`: `ENTRIES=0/3 BOUND=0/5 C2=FAIL` → `ENTRIES=3/3 BOUND=4/5 REFUSED=1 QUOTE_ROWS=63 CAPTURE_BOUND=63/63 ANCHOR_BOUND=4/4 INFERENCE_GROUNDED=3/3 C2=PASS`. Staged-copy control `REF_ID_UNBOUND=12 BOUND=0/5`; mechanically-adopted control `BOUND=5/5 REF_ID_UNBOUND=4 ANCHOR_BOUND=0/5` remains C2=FAIL. W1 non-author-independent Pypdf check: 49/49 PDF quotes also occur in the independent extraction.
- **Routed fixes and calibration.** `pointer-anchor-check.py` with seven anchored successors: `ANCHORED=7/7`; the round-52 erratum range corrected to E1–E6 and the round-51 range in the SKILL row to E1–E5. `tools/inference-ground.py` now checks clause-bounded CJK polarity; `cjk-polarity-check.py` base 2/6 → landed 6/6, while C2 passes with both base and changed reader (erratum E4). The round-52 grey-literature refusal is corrected to the held reason (duplicate URL/outside frozen set); S190 is refused because no admitted entry rests on its tier-C notice print.
- **Frontier step.** Rows 116 → 120 (A S117, S120; B S118, S119), census exit 0 at start and end, same five W04 warnings; four documents credited once each, no row touched old→new. Six mistakes mined; QUALITY 91–96; considerthese proposal 2 implemented as `weakness-streak.py` / `recurring.tsv` (`WEAKNESS_ROWS=2 FAILING=0` at the lane tree). SKILL Gates registry `REGISTERED=135/135 MISMATCHES=0`; README `Round53 coverage and frontier`.
- **Waves.** W1 dispatched 49 seats (18 scribe, 12 executor, 6 critic, 4 reviewer, 3 scout, 2 mutation-tester, 2 connector, 1 sentinel, 1 simplifier); W1 results JSON has 49/49 with no error. W2 dispatched 43 seats (16 executor, 10 critic, 5 reviewer, 4 scribe, 3 mutation-tester, 2 connector, 1 scout, 1 sentinel, 1 simplifier). This LOG entry records the dispatch; at the user's wrap instruction, W2 WAVE-DONE/results had not yet been received by this L1, so no W2 seat outcomes or dead-seat claim is made here.
- **Tooling.** No system tool installed; `pypdf 6.21.2` was invoked ephemerally with `uv run --with pypdf` from PyPI solely for independent, offline PDF extraction; no persistent tool install. L0 `8d77e6c1` remains open.

## Round 54 — OLE `.doc` text form; the PRC citation standard GB/T 7714-2025 by document (2026-10-26)

Evidence that motivated the round: the SCORECARD round-54 plan ("a defined OLE `.doc` text form"; theme C), the round-53 closure's routed items (`corpus/lessons/round-53-verifier-spotcheck.md` section 6), and the round-53 Gate's S130 flip. Claims froze at `5a1a20630d8176a816a60bb43b0d0e7ee2db19a0` after do-nothing controls; C1 candidate `8a7d0f137a352000d78704ba5695ded8857104fe`.

- **C1 operability (lowest scored axis, capability acquisition).** `tools/capture-text.py` reads OLE Word 97+ `.doc` with no helper program. `c1-count.py`: base `LEGS=1/6` → landed `LEGS=6/6` ×4 (`corpus/evidence/round54/measure-after.txt`). W1 forged the frozen counter (sibling HTML + canned REAL); the post-freeze supplement separates tool 3/3 from forge 0/3 (claims-erratum E1). Post-candidate fixes: signed Prc bound, tracked-deletion runs dropped (E2; `tracked-deletion-check.py`).
- **C2 depth (sourced).** Entries `source-type-taxonomy-r36.md` (S121, S122) and `-r37.md` (S123); rows 120 → 123; 33 located quotes; three quarantine verdicts `absent-as-written`; `c2-count.py`: `ENTRIES=0/2 … C2=FAIL` → `C2=PASS`. The W1 S101 leg was cut (E3); S101 `used-by` unchanged.
- **Routed and calibration work.** Nine anchored S100/S101 corrections into tool dumps (`ANCHORED=16/16`); QUALITY 97–100; SKILL gate rows (`REGISTERED=144/144`); README round-54 section; considerthese CT-20261026-1 ledger (`BAD=0`); round-53 W2 registry committed; PDF quotes cross-checked under NFKC (`NOT_IN_INDEPENDENT=0`).
- **Census.** Start and end exit 0, the same five W04 (`census-start.txt`, `census-end.txt`).
- **Waves.** W1 49 seats (44 reports; R54ExecNegSweep, R54ExecPdfForm, R54SentCounters cancelled by the orchestrator after going silent; R54CritSeparable, R54ConnSiblings died on a refused model fallback). W2 38 seats dispatched (`w2.ready.dispatched` per the dispatcher); at filing it was still running under the L1's request-budget wrap, so its findings are not integrated.

## Round 55 — an OLE-aware span builder; the NMPA grey-literature field by document; W2-falsified statements corrected (2026-10-27)

Evidence that motivated the round: the SCORECARD round-55 plan (a span builder that reads an OLE `.doc` through `tools/capture-text.py`; the refused S130 grey-literature entry; a C1 counter whose generated inputs never sit beside the tool and whose oracle the tool cannot reach — RW-1), and the round-54 closure's routed items (`corpus/lessons/round-54-verifier-spotcheck.md` section 6: integrate W2 — the supplement and audit hook can be fooled, the r36 sentence, QUALITY 97 offsets, lesson Mistakes row 2). Claims froze at `1fc5d92b5a7866ec16f1cac2de749fccfa6b49cb` after do-nothing controls; C1 candidate `6ca924995d48facbf704d2aa22ddaec236059039`.

- **C1 operability (lowest scored axis, capability acquisition).** `tools/build-spans.py` reads every capture through its defined text form; `c1-count.py` (held-out quotes from generated and pinned OLE captures, expected offsets in memory, read-auditing hook): absent at base `LEGS=0/4` → `LEGS=4/4` ×4 (`corpus/evidence/round55/c1-measure-after.txt`); controls R54SHIM 1/4, TXTONLY 1/4, DELEGATE 0/4; L1 sweep 40/40 seeds.
- **C2 depth (sourced).** Entry `grey-literature-and-chinese-search-record-r40.md` on S124 (gcpunion `.doc` copy of the NMPA guideline, read through the OLE form), S125 (中国食品药品网 report) and S126 (NMPA English notice); rows 123 → 126; 19 located quotes built by the C1 builder; register S125 (round6) `absent-as-written`; r43 refused; `c2-count.py`: `ENTRIES=0/1 … C2=FAIL` → `C2=PASS`.
- **C3 calibration.** Eleven anchored errata (`SCORECARD.md` "Round 55 statement errata"), each observation recomputed by `c3-count.py`: `ERRATA=0/11` → `11/11`; in-target corrections: r36 `#### Corrections (round 55)`, QUALITY 101, lesson `## Corrections`.
- **Routed and integration work.** r37 `#### Corrections (round 55)` (three further W2 findings); QUALITY 102–105; `wave-settled-check.py` (round 54 → `UNSETTLED w2`, exit 1); successors of the round-54 ledger and PDF checks with their W2 attacks as fixtures; W04 adjudicated (no change); considerthese swept (none new); SKILL rows `build-spans` and round-55 counters; README Round55 section; `recurring.tsv` RW-1 streak 7 (exposure, routed to the round-55 counter).
- **Census.** Start and end exit 0, the same five W04 (`census-start.txt`, `census-end.txt`).
- **Waves.** W1 48 seats (one v1 wave, dispatched: `w1.ready.dispatched`); 35 reports at filing, 13 seats still running (no `w1-results.json`); W2 (36 falsify items, `w2-spec.json`) prepared and NOT dispatched. The round was wrapped on the L1's request budget: round total 48 seats, below the 64 floor, and the report was filed before W1 settled (`wave-settled-check.py --round 55 --before-filing` → `UNSETTLED w1`, exit 1, `corpus/evidence/round55/wave-settled-r55.txt`) — the same class as this round's Mistakes row 1, recorded as row 4.

## Round 56 — build-spans gate clause coverage and hook closure; the grey-literature row of the drug clinical comprehensive evaluation workflow guideline by document (2026-10-27)

Intake: round-55 closure `corpus/lessons/round-55-verifier-spotcheck.md` §6 (settle W1/W2, harden the C1 counter, D3, D4, `build-spans` registry class) and the orchestrator note. The late round-55 `w1-results.json` was committed under round 55 (`e5a37951`). Claims froze at `41c58925580af6be22049f13cfde234c5475b858` after do-nothing controls; C1 candidate `46e1758f3d8a5d1bf30200d2ff7d909b0230feed`.

- **C1 operability (lowest scored axis).** `corpus/evidence/round56/c1-gate.py` = the round-55 counter plus two hook events (`_posixsubprocess.fork_exec`, `os.chdir`); battery `corpus/evidence/round56/battery/` (seven violators and one unpinned oracle copy); frozen driver `c1-count.py` (nine `R55MutC1Counter` mutants, clause-reason kills, triplicate random order at seeds 7 and 56; two hook probes): before `KILLED=1/9 DENIED=0/2` → `KILLED=9/9 DENIED=2/2 CANDIDATE=2/2` ×2 (`c1-measure-after.txt`, lane master `99eff0ec`). Three pre-freeze counter fixes disclosed in `claims.md`.
- **C2 depth (sourced).** Entry `corpus/knowledge/grey-literature-field-china-r42.md` on S127 (the ttbz draft for comments), S128 (its explanatory note), S129 (the 中国药房 2025 publication), S130 (the centres' 2020 management guideline) and held S118 (`used-by` extended); rows 126 → 130; 23 located quotes built by `tools/build-spans.py`; staged r44 refused; `c2-count.py` `C2=FAIL` → `C2=PASS` (`c2-measure-after.txt`, lane master `98977070`, after the 表7 fix).
- **Routed and integration work.** Round-55 lesson corrections for closure D3 and D4 and for the carried W2 narrowings; r40 `#### Corrections (round 56)`; QUALITY 106–109; SKILL rows (`build-spans` re-registered as a gate; round-56 counters); lesson Mistakes rows 1–3.
- **Waves.** One v2 wave, W1 = 69 seats (33 round-56 items + the 36 never-dispatched round-55 W2 items); report filed after `WAVE-DONE w1`.

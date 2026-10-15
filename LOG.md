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

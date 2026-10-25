# SentWriteScope — round 43 wave 1

Seat: SentWriteScope (sentinel, leaf). No remediation edit. No network. No tool install. No live resume trial.

Axes: path confinement, forbidden-write completeness, failed-preflight zero mutation. Keep a move only if it sharpens one and harms none.

## Own report path

Allowed write, and the only write this seat made:

`/home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-43/w1/SentWriteScope.md`

That path is under the lane wave directory. It is not the fleet root and not the fleet-resolved trailer.

Command (cwd was the fleet root):

```
CWD=/home/vgpnk/Projects/shokunin
OWN=/home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-43/w1/SentWriteScope.md
REL_FROM_CWD=/home/vgpnk/Projects/shokunin/.ufo/waves/round-43/w1/SentWriteScope.md
OWN_EQ_REL=False
OWN_UNDER_LANE_W1=True
REL_UNDER_FLEET_NOT_LANE=True
FLEET_ROUND43_EXISTS=False
LANE_W1_EXISTS=True
OWN_EXISTS=False
```

`w1` is not a symlink (`os.path.islink` false on `.ufo/waves` and `.ufo/waves/round-43/w1`). Lane git toplevel is `/home/vgpnk/Projects/shokunin/chousa-shokunin`. Fleet git toplevel is `/home/vgpnk/Projects/shokunin`. Lane HEAD equals the measured commit `737f40b6aa8f37ffe2269db370fd6d65a720d9a8`. Fleet `.gitignore` line 1 ignores `*-shokunin/`, so this file does not dirty the fleet index. The relative trailer would.

## Forbidden writes

Rule, from the wave context: a seat writes only its own report at `/home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-43/w1/<SeatName>.md`. The `Report:` trailer is relative to that lane, never to the fleet cwd. Everything else below is forbidden. This seat's item does not grant a `/tmp` write or a tool install; none was made.

### This seat must not write these sibling reports

Same directory, other seats (63). Overwrite is a cross-seat evidence forge:

- `/home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-43/w1/ReviewC1Rerun.md`
- `/home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-43/w1/ReviewC2Rerun.md`
- `/home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-43/w1/ReviewC3Rerun.md`
- `/home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-43/w1/ReviewSplitIds.md`
- `/home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-43/w1/ReviewS086Ratio.md`
- `/home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-43/w1/ReviewS093Ratio.md`
- `/home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-43/w1/ReviewBoundSides.md`
- `/home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-43/w1/ReviewQuoteLocated.md`
- `/home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-43/w1/CritBoundHalf.md`
- `/home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-43/w1/CritSeparability.md`
- `/home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-43/w1/CritBotWall.md`
- `/home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-43/w1/CritColumnSpan.md`
- `/home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-43/w1/CritDoNothing.md`
- `/home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-43/w1/CritCheapestGate.md`
- `/home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-43/w1/CritS085Miss.md`
- `/home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-43/w1/CritNoFetch.md`
- `/home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-43/w1/MutFlipS086.md`
- `/home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-43/w1/MutMissingTool.md`
- `/home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-43/w1/MutShortEnum.md`
- `/home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-43/w1/MutWrongQuote.md`
- `/home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-43/w1/MutIndentGuard.md`
- `/home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-43/w1/MutEmptyClass.md`
- `/home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-43/w1/SentNoEgress.md`
- `/home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-43/w1/RevRoutedRepairs.md`
- `/home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-43/w1/RevCollisionMap.md`
- `/home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-43/w1/ExecSplitRerun.md`
- `/home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-43/w1/ExecClassCount.md`
- `/home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-43/w1/ExecCaptureSha.md`
- `/home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-43/w1/ExecBotWallBytes.md`
- `/home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-43/w1/ExecCensus.md`
- `/home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-43/w1/ExecRowCount.md`
- `/home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-43/w1/ExecUsedBy.md`
- `/home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-43/w1/ExecNoPipe.md`
- `/home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-43/w1/ExecRecheck.md`
- `/home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-43/w1/ExecC1Receipt.md`
- `/home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-43/w1/ExecC2Receipt.md`
- `/home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-43/w1/ExecNoHarmGate.md`
- `/home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-43/w1/ScoutProvince.md`
- `/home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-43/w1/ScoutSiblingKengaku.md`
- `/home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-43/w1/ScoutSiblingKasegi.md`
- `/home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-43/w1/ScoutFrontier.md`
- `/home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-43/w1/ScoutCaptureForm.md`
- `/home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-43/w1/ScoutLaneS077.md`
- `/home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-43/w1/ScoutStagedS077.md`
- `/home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-43/w1/ScoutJapaneseHead.md`
- `/home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-43/w1/ScoutCochraneNotAdopted.md`
- `/home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-43/w1/ScoutRegisterStale.md`
- `/home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-43/w1/ScribeGateBlock.md`
- `/home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-43/w1/ScribeRenumber.md`
- `/home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-43/w1/ScribeErratum.md`
- `/home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-43/w1/ScribeQuality61.md`
- `/home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-43/w1/ScribeSearchLog.md`
- `/home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-43/w1/ScribeRejects.md`
- `/home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-43/w1/ScribePredicates.md`
- `/home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-43/w1/ScribeShonen.md`
- `/home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-43/w1/ConnSiblingScan.md`
- `/home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-43/w1/ConnQuoteReopen.md`
- `/home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-43/w1/ConnKumitate.md`
- `/home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-43/w1/ConnNoSecrets.md`
- `/home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-43/w1/SimpDeadFields.md`
- `/home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-43/w1/SimpDuplicatedLCS.md`
- `/home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-43/w1/SimpMutantWeak.md`
- `/home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-43/w1/SimpFilename.md`

Also forbidden in that wave tree: `swarm-registry.json`, `w1-dispatch.json`, `w1-plan.json`, `w1-spec.json`, `w1-settle.tsv`, and `/home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-43/assimilation/` (including `assimilation/guard/`).

### Lane production, index, jj

Forbidden: any path under `/home/vgpnk/Projects/shokunin/chousa-shokunin/` that is not the one report above. Named:

- `corpus/` including `corpus/evidence/round43/`, `corpus/SOURCES.md`, `corpus/knowledge/`, `corpus/lessons/`, `corpus/QUALITY.md`
- `tools/` including `tools/absent-split.py`, `tools/research-gate.sh`, `tools/quote-reopen.py`, `tools/quarantine-check.py`
- `considerthese/`
- `LOG.md`, `SCORECARD.md`, `SHONEN.md`, `PROVINCE.md`, `AGENTS.md`, `SKILL.md`
- lane git index (`.git/`), any `git add` / `commit` / `reset` / `checkout`
- jj state (`.jj/`), any mutating jj command

`tools/absent-split.py` itself only writes stdout/stderr (read of the script; not executed here). Running it is not a cache write. Editing it is forbidden.

### Fleet repo

Seat cwd is the fleet root. A relative write lands here. Forbidden, including:

- `/home/vgpnk/Projects/shokunin/.ufo/waves/round-43/w1/SentWriteScope.md` and any other `.ufo/waves/round-43/**` resolved from cwd (directory did not exist at check time; a relative write would create it)
- `/home/vgpnk/Projects/shokunin/.ufo/reports/round-43/chousa.md` (L1 report, not a seat)
- `/home/vgpnk/Projects/shokunin/.ufo/l0-questions.md`
- `/home/vgpnk/Projects/shokunin/MANIFEST.json`
- `/home/vgpnk/Projects/shokunin/templates/`
- `/home/vgpnk/Projects/shokunin/scripts/` including `scripts/hyaku/` and `scripts/sources-census.sh`
- `/home/vgpnk/Projects/shokunin/.ufo/state/`
- `/home/vgpnk/Projects/shokunin/.ufo/watchdog.log`
- `/home/vgpnk/Projects/shokunin/.ufo/prompts/`
- `/home/vgpnk/Projects/shokunin/PROTOCOL.md`, `MISSION.md`, `AXES.md`, `CORPUS.md`

### Sibling repos

Read-only. No writes, no commits, no jj. Listed from `ls -1d /home/vgpnk/Projects/shokunin/*-shokunin` (chousa included only as a reminder that sibling trees are not this lane's report path):

- `/home/vgpnk/Projects/shokunin/audio-shokunin`
- `/home/vgpnk/Projects/shokunin/game-dev-2d-shokunin`
- `/home/vgpnk/Projects/shokunin/game-dev-3d-shokunin`
- `/home/vgpnk/Projects/shokunin/kagi-shokunin`
- `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`
- `/home/vgpnk/Projects/shokunin/kake-shokunin`
- `/home/vgpnk/Projects/shokunin/kama-shokunin`
- `/home/vgpnk/Projects/shokunin/kasegi-shokunin`
- `/home/vgpnk/Projects/shokunin/kengaku-shokunin`
- `/home/vgpnk/Projects/shokunin/kotoba-shokunin`
- `/home/vgpnk/Projects/shokunin/kotodama-shokunin`
- `/home/vgpnk/Projects/shokunin/kumitate-shokunin`
- `/home/vgpnk/Projects/shokunin/lore-shokunin`
- `/home/vgpnk/Projects/shokunin/mado-shokunin`
- `/home/vgpnk/Projects/shokunin/mori-shokunin`
- `/home/vgpnk/Projects/shokunin/revenger-shokunin`
- `/home/vgpnk/Projects/shokunin/souji-shokunin`
- `/home/vgpnk/Projects/shokunin/tabi-shokunin`
- `/home/vgpnk/Projects/shokunin/tameshi-shokunin`
- `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin`

### shokuknow

Entire tree read-only. Never write, never run its tools (`renumber-staged.py`, `merge-plan.py`, `quote-lint.py`, `absent-defect-register.py`). Named:

- `/home/vgpnk/Projects/shokuknow`
- `/home/vgpnk/Projects/shokuknow/merge/chousa/`
- `/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache/`
- `/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/absent-defect-register.md`

### Operator and host

- `/home/vgpnk/.omp/agent/config.yml` (no model pass, no edit)
- `/home/vgpnk/.omp/agent/mcp.json`
- pacman databases and any `pacman -S`, `-Sy`, `-Syu`, `-U`, `-R` (paused)
- secret files (not opened)

### Contract holes (still forbidden by the shared seat contract)

Two items grant writes outside the report directory. The shared context says write only the report. Those grants lose:

- MutWrongQuote: a 20-byte file under `/tmp`
- MutEmptyClass: a `/tmp` copy of split labels

Tool install into `~/.local/bin` is a context exception after `RULES.md`. This seat did not use it. Pacman remains forbidden.

MutIndentGuard says re-run the guard under `assimilation/guard`. The producing commands in the L1 prompt redirect into that directory. Re-running them would overwrite lane wave evidence that is not that seat's report. Forbidden.

Executor items add "except your single labrat". The depth rule says that probe is read-only. A labrat write is still forbidden.

## Finding 1 — relative trailer writes the fleet repo

Severity: high.

Exploit path: seat tools start at `/home/vgpnk/Projects/shokunin`. The renderer appends a relative trailer. A seat that obeys the trailer, or a Write/Edit whose path is relative, creates `/home/vgpnk/Projects/shokunin/.ufo/waves/round-43/w1/<Seat>.md`. That path is not gitignored (`*-shokunin/` does not cover it). Collection looks under `UFO_PROJECT_ROOT` joined with the relative `reportDir`, so the fleet copy is invisible to the lane collector and is a fleet-repo mutation the seat contract forbids.

Evidence:

- Live cwd and path split, quoted above. `OWN_EQ_REL=False`. `REL_UNDER_FLEET_NOT_LANE=True`. `FLEET_ROUND43_EXISTS=False`.
- Renderer: `ufo-swarm-wave.mjs:208-209` returns `Report: write your scoped findings to ${reportDir}/${name}.md`. This wave's `reportDir` is `.ufo/waves/round-43/w1` (`w1-spec.json`).
- Collector: `ufo-swarm-collect.mjs:597` joins `ROOT` ( `UFO_PROJECT_ROOT` or the ufo package) with that relative dir. A fleet-cwd write is not that file.
- L1 prompt already records the same miss: seat tools start at the fleet root; relative `.ufo/waves/...` landed in the fleet repo in hyaku phase 1 (kama r11, tsukuroi r12, tabi r15, mado r16). The context sentence is prose. It does not change cwd or the trailer bytes.

Impact: one obedient seat dirties the fleet repo, drops its evidence out of lane collection, and can collide with another lane's misroot under the same relative path. No mechanical sandbox stops it.

Smallest remediation: emit the trailer as an absolute path under `UFO_PROJECT_ROOT` (the lane), and reject a seat write whose resolved path is not that one file. Do not rely on the prose sentence. Not applied: this seat has no remediation scope.

## Finding 2 — failed continuity reject is not zero mutation

Severity: high. Code-traced. Not live-executed: a resume against the operator wall would be the mutation under test. The existing test asserts the error code and does not hash the manifest.

Exploit path A (sighting resume): `resumeMission` (`ufo-sighting.mjs:3818-3823`) takes the lock, then `reconcileLocked`, then `resumeMissionLocked` → `resolveExactMission`. `reconcileLocked` (`1991-2031`) always `writeManifest` at line 2018 before identity is checked, then `settleWallGeometry(..., { killEmptyFleetWindow: true })`, then `writeManifest` again at 2030. `writeManifest` (`533-552`) increments `registryRevision` and `renameSync`s a new manifest. `IDENTITY_MISMATCH` / `RESUME_LIVE` / `RESUME_COMPLETED` / `RESUME_UNSUPPORTED` throw only after that, inside `resumeMissionLocked` (`3714-3728`). `withOperationLock` does not roll the manifest back on throw (`784-786`). `state.profile = geometry.profile` (`3716`) is before the identity fail but after reconcile has already persisted.

Exploit path B (dispatcher argv guard): `run-logic.md` §2.1 names `argvContainsForbiddenSelector` as the reject for `--continue` / `--twin`, and requires zero mutation. The guard runs at `fleet-dispatcher.mjs:8162`, after `mkdirSync` (`8047`) and `writeFileSync` of `prompt.md`, `prompt.md.sha256`, and `config.json` (`8118-8126`, flag `wx`). The reject return (`8162-8170`) does not unlink them. The caller then sets `current.state = "blocked"` for `identity_selector_invalid` (`8315-8317`).

Evidence the test does not close the hole: `tests/ufo-sighting.test.js:2582-2624` expects `IDENTITY_MISMATCH` and does not compare manifest bytes or `registryRevision`.

Impact: a mismatched or forbidden resume still bumps run-state, can settle or kill an empty fleet window, and leaves snapshot files. That is a write on the failure path the contract says must be inert. Process cleanup does not remove the snapshots.

Smallest remediation: resolve the exact session and reject `--continue`/`--twin` before `reconcileLocked`, before `writeManifest`, and before snapshot `mkdir`/`writeFileSync`. On reject, unlink any partial snap and do not bump `registryRevision`. Not applied.

## Finding 3 — `--tool` executes an arbitrary file

Severity: medium. Not executed.

Exploit path: `corpus/evidence/round43/c1-count.py:45-47` and `:70-75` run `python3 <path>` for any `--tool` that `is_file()`. The do-nothing items pass a missing `/tmp` path, which returns before `run`. A present file is executed with the seat's uid and no write confinement, so it can write every forbidden path above and still emit a TSV the counter will score.

Impact: write-scope is prose. The counting command the wave tells seats to run is an exec primitive.

Smallest remediation: if `--tool` is not the resolved committed `tools/absent-split.py`, fail before `subprocess.run`. The missing-path control already exits 1 without exec. Not applied.

## Stop

Assigned surface was write scope plus the required continuity reject check. No production file, git index, jj state, fleet file, sibling repo, or shokuknow path was modified. No fetch. No second report.

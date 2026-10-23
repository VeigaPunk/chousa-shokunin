# ConnOverlap — round-36 wave 1: sibling-overlap scan (chousa)

Seat ConnOverlap, 2026-10-23, godspeed. Question: is per-record argv attribution
or the engine-swap canary already held elsewhere in the fleet? Method, verbatim
commands, exit codes, per-run results: `w1/ConnOverlap/scan-log.md` (sha256
below). Read-only throughout; no counters, gate or witness executed; no
installs.

## Verdict (explicit)

**Both round-36 capabilities are fleet-unique. No sibling lane holds per-record
argv attribution, an engine-swap canary, or a grep-pin/override mechanism;
round 36 duplicates no sibling work.** The only lineage overlap is chousa's own
disclosed r35→r36 supersession (`tools/argv-witness.py:4-9`: "Round 36
replacement for `mechanism-witness.py`'s PS4 trace channel"). The nearest
sibling holdings are pattern-family cousins, none of which separates an
output-equivalent engine swap or attributes per record:

- **tameshi** (closest): the fleet's other witness craft — declared-witness
  mutation classification (`tools/bash-witness-study.py:2` "declared-witness
  classification of the pinned bash-surface-census mutation leg"), its metadata
  gate, and `corpus/knowledge/witness-equivalence-rule.md:21-22` ("behavioral
  equivalence: the pristine and mutated tally blocks must produce the same
  `(exit, first-line)` tuple"). That is an OUTPUT-behavior witness over exit
  codes and first lines; no out-of-band engine channel, no argv log, no per-record
  attribution, no engine swap.
- **kotoba**: tripwire+strace canaries proving hash-never-exec
  (`.ufo/round-23/scouts/V3.md:93` "canary empty, guard still hashes";
  `M9.md:47` "canary hashed, `CANARY_FIRED` absent → hash-never-exec holds") —
  the INVERSE of C1 (prove a pinned binary is NOT executed vs chousa's prove
  the pinned engine IS queried per record).
- **mori**: leak/scrub/env canaries (`tools/mori-census.sh:3035` "if the census
  leaks either variable into this child the canary file appears"; GIT_TRACE
  canary `:4285`). Execution-boundary tripwires, not engine-swap separation.
- **souji / tsukuroi / kumitate / kengaku / game-dev**: secret-leak canaries
  (souji `impl-47.sh:1097`), a `$(touch canary)` no-eval arm (tsukuroi
  `boot-chain-audit.sh:1177`), a gitenv probe (kumitate r46), eval canary
  tables (kengaku r5), `iter_watch` canaries (game-dev-3d r78) — none an
  output-equivalent engine canary.
- **kaidoku**: the fleet's only other PS4 use, for .bashrc recon
  (`.ufo/waves/arc2-loop1-round2/CR3.md:62` `PS4='+${BASH_SOURCE}:${LINENO}+ '
  bash -x`), not an attribution instrument; its other "PS4" hits are seat-file
  names.
- **audio**: docstring prose "The freeze, mechanism-witnessed."
  (`corpus/fixtures/measure_audio.py:39009`, +9 verbatim copies) describing a
  GStreamer clock-freeze observation — same word family, no instrument, no
  attribution channel.

This updates chousa's own r35 scan (`.ufo/waves/round-35/w2/ConnectorOverlap.md:34`:
"chousa's `mechanism-witness.py` is the only fleet instrument"), which still
holds for the r36 successor.

## Token table

P1 = `argv-witness|ENGINE_SWAP_CANARY|WITNESS_PER_RECORD|RESEARCH_GATE_GREP|mechanism-witness`.

| Token | Repo | Path:line | Verdict |
|---|---|---|---|
| argv-witness | all 23 sibling dirs + fleet `.ufo/{reports,waves,prompts,state}` | — (P1 `No matches` everywhere; per-repo runs, see scan-log) | **fleet-unique** (chousa only: `tools/argv-witness.py`, claims.md, c2-count.py, r36 waves/briefs) |
| ENGINE_SWAP_CANARY | all siblings + fleet `.ufo/*` | — (no matches) | **fleet-unique** (chousa `corpus/evidence/round36/c1-count.py:5`) |
| WITNESS_PER_RECORD | all siblings + fleet `.ufo/*` | — (no matches) | **fleet-unique** (chousa `c2-count.py:8`) |
| RESEARCH_GATE_GREP | all siblings | — (no matches) | **fleet-unique** (chousa gate + r35 report `.ufo/reports/round-35/chousa.md:37`; r35 scan's hazard note — siblings' own bare-`grep` receipts — remains theirs, unowned) |
| mechanism-witness | audio | `corpus/fixtures/measure_audio.py:39009` "The freeze, mechanism-witnessed." | **reused term, not a holding**: docstring prose about a GStreamer freeze; no tool, no channel |
| mechanism-witness | all other siblings | — (no matches) | fleet-unique instrument (chousa `tools/mechanism-witness.py:15-16` "the gate runs under `bash -x` with a private PS4 marker") |
| PS4 (witness channel) | kaidoku | `.ufo/waves/arc2-loop1-round2/CR3.md:62` | **reused pattern, different purpose**: xtrace for .bashrc recon; no sibling PS4 attribution instrument; chousa's PS4 channel is now retired (r36) |
| canary (case-insens.) | kotoba | `.ufo/round-23/scouts/V3.md:93`, `M9.md:47` | **reused pattern (closest cousin)**: tripwire+strace hash-never-exec — inverse direction of C1 |
| canary | mori | `tools/mori-census.sh:3035,3399,4285`; r14 regression CANARY constants | reused pattern: env-scrub/leak tripwires |
| canary | tameshi / souji / tsukuroi / kumitate / kengaku / game-dev | `mutate-and-run.sh:1890`; `impl-47.sh:1097`; `boot-chain-audit.sh:1177`; r46 gitenv-canary; r5 canary table; r78 iter_watch canary | reused pattern: GIT_DIR / secret-leak / no-eval / env / eval / emission tripwires — none an engine-swap canary |
| witness (family) | tameshi | `tools/bash-witness-study.py:2`; `corpus/knowledge/witness-equivalence-rule.md:21-22` | **reused pattern (C2-family)**: output-equivalence witness for sealed mutation copies; no argv channel, no per-record attribution |

## Ownership if contested (PROVINCE.md basis)

Not contested today. chousa PROVINCE.md:7-8 owns "this lane's own corpus and
gates" — research-gate.sh, argv-witness.py and both counters are chousa gate
instruments. tameshi PROVINCE.md:14-17 owns the reusable verification-fixture
craft but "a pattern is admitted from evidence in TWO independent lanes before
it is claimed general" and it never edits a sibling's gate: the engine-swap
canary / per-record argv witness is instantiated in ONE lane (chousa), so under
tameshi's own admission rule the general-craft claim is not yet available to
anyone; if a second lane ever instantiates it, the generalized method would
route to tameshi while each lane keeps its own gate. kengaku explicitly routes
"research method … stays chousa's" (kengaku PROVINCE.md, Adjacent table, chousa
row); kumitate's province is orchestration tooling only — no overlap.

**Does this round duplicate work? No.** Zero sibling hits for every round-36
token; the r35-era siblings named in chousa's prior overlap scan (tameshi
witness rule, tsukuroi env allowlist, kaidoku structure-blind control, kake
shortcut detector, kotodama digest pins) hold pattern cousins only, all
re-checked this round and unchanged.

## Residual limits

- mori `.ufo/worktrees/round-19` fixture worktrees (ContentGate /
  FreezeMetadata / RegressionHarness copies of mori's own r19 gates) resisted
  three 30 s grep attempts and one glob; `[INFERENCE]` they contain mori's own
  gate fixtures only (every other mori layer — tools, corpus, waves, reports,
  sessions, round-2..11, worktrees/round-18 — scanned clean).
- Whole-fleet and 10-repo group scans exceed the grep tool's 30 s budget;
  coverage was achieved by per-repo/group decomposition (every repo reached at
  least once with a complete, unpaginated P1 run — see scan-log).
- Non-repo fleet-root dirs (`reports/` empty; `research/ scripts/ local/
  templates/ scratch/ dir/`) were not token-scanned beyond the listing; they
  are outside the brief's sibling-repo scope.

## Artifacts (under `.ufo/waves/round-36/w1/ConnOverlap/`)

- `scan-log.md` — verbatim commands, exit codes, per-run results, files opened.
  sha256 recorded in the report trailer at write time (see below).

- `ConnOverlap/scan-log.md` sha256
  `722e44bbed33d300227e0aa071976c37120724674c6dfb0c2294628a64da5b59`
- (this report is `w1/ConnOverlap.md` itself; a file cannot embed its own
  digest — hash it with `sha256sum` at read time)

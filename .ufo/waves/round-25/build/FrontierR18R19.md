# FrontierR18R19 — drafted `## Frontier` paragraphs, rounds 18 and 19

Scope: draft only. `corpus/README.md` is not edited (read-only seat). Insertion point: after the Round 10 paragraph and before `Still open and integrator/operator-owned:` (README.md:487), chronological. Every number below is grounded in the cites listed after each paragraph; gate shas were re-derived this session with `git show <commit>:tools/research-gate.sh | sha256sum` (read-only).

## Draft — Round 18

Round 18 (loop 1, round 7) ran the phrase-gap move that round 16 left as named debt, on one 16-seat AgentSwarm wave routed to openai-codex gpt-6-luna-max after the zai glm-5.3-flash quota was exhausted (operator directive; 16/16 seat reports). `SCOPE_KENGAKU` covered `model benchmark(s)` and `model scoring` but not `llm benchmark(s)` or `llm scoring`, so a record declaring `domain: LLM benchmarks` passed CLEAN. On the demo record the pre-round gate (commit `e3c556e`, gate `c2915f24…`) returns CLEAN; the landed gate (`6e694881…`) adds `llm benchmark|llm benchmarks|llm scoring` and returns a `SCOPE_MODEL_QUALITY_ABSORBED` warn with DRIFT. Selftest moves 116 → 119, cases 1–116 byte-identical to the r17 receipt, cases 117–119 pinning the new phrases and a prose-only control; `--drift` against the r12 baseline reports `GATE_DRIFT: none` with no re-pin. The r1 archive counting command is recorded at `VERDICT_BEARING_EXPORTS=3/3` in the round notes, but no r18 receipt carries that line, so it is asserted here, not receipted. The battery receipt is an output-identity record over the archive and claim fixtures; its claims, chain and verify-all sections read DRIFT in that run context, and the round's "ALL IDENTICAL vs pre-round gate" has no diff in the receipt. That observable is not saturated: the screen reads only Meta `domain`/`scope` rows, so prose is never scanned (case 119); `ai benchmark(s)` stays out as too broad; the inflection gaps (`bug bounties`, `dispatch mechanisms`, `llm evaluations`) and the camel-case `llmbenchmark` form stay named debt; and the matcher is literal phrase match, not a judgment that a record is in model-quality scope.

Cites (Round 18):
- Selftest 116 → 119, PASS line: `corpus/evidence/scope-r18-20261019T173000Z-selftest.log:120`; prior count `corpus/evidence/fence-r17-20261019T171200Z-selftest.log:117`; `SCORECARD.md:923-924`, `:936`; `LOG.md:681`.
- Cases 1–116 identical: `head -116` of both selftests, `cmp` exit 0 (this session). New cases: `scope-r18-…-selftest.log:117-119`.
- Gate shas: `git show e3c556e:tools/research-gate.sh | sha256sum` → `c2915f24d73d656ca23b7f6228cbdd502c27a8c07670776fed84c70f278266f8`; `git show 5499cef:…` → `6e69488160199cc1704bd1d17b7523cd39022016ad123ecf43575467b266de0c`. Gate line: `SCOPE_KENGAKU` assignment at `5499cef` line 699 (verified via `git show`).
- Demo: `corpus/evidence/scope-r18-…-demo.log:1` (BEFORE, e3c556e), `:3` CLEAN, `:7` `SCOPE_MODEL_QUALITY_ABSORBED` warn, `:8` DRIFT.
- Drift: `scope-r18-…-drift.log:1` `GATE_DRIFT: none`; `SCORECARD.md:938`.
- Battery: `scope-r18-…-battery.log:2,4,6` CLEAN (A/B/C-r9); `:43` claims DRIFT; `:85` chain DRIFT; `:114` structure DRIFT; `:133` verify-all DRIFT. Round claim "ALL IDENTICAL": `LOG.md:681`, `SCORECARD.md:931`.
- r1 `3/3`: `SCORECARD.md:931`, `LOG.md:672`; `grep -c VERDICT_BEARING_EXPORTS` over all four r18 receipts = 0.
- Verdict table: `SCORECARD.md:933-940` (freshness `unchanged` at `:938`); admission `:942-943`.
- Named debt / ai-benchmark exclusion: `corpus/knowledge/scope-phrase-gap-r18.md:18-22`, dispositions `:26-33`, case 119 `:39-40`.
- Zero network: `SCORECARD.md:940`; no strace line in r18 receipts (`grep -l strace` exit 1).

## Draft — Round 19

Round 19 (loop 1, round 8) ran the sweep-symlink escape move that round 16 left as named debt, on one 16-seat AgentSwarm wave routed to openai-codex gpt-6-luna-max under the zai exhaustion directive (16/16 seat reports). `sweep_path_guarded` canonicalized a sweep glob's literal base but not each expanded match, so `dir/*.md` matching an outside leaf symlink, or `dir/*/*.md` traversing an outside directory symlink, reported `SWEEP_CLAIM_FALSE` instead of a boundary refusal. On the demo the pre-round gate (commit `5499cef`, gate `6e694881…`) reports a `SWEEP_CLAIM_FALSE` hit and DRIFT; the landed gate (`9f163807…`) canonicalizes every match against both allowed roots and refuses the whole sweep with `SWEEP_LOCATION_OUT_OF_CORPUS` (crit, `observed=refused`, match not opened). Selftest moves 119 → 122, cases 1–119 byte-identical to the r18 receipt, cases 120–122 pinning the leaf-symlink, directory-symlink and in-root-symlink control; `--drift` reports `GATE_DRIFT: none`; the battery receipt is byte-identical to r18 after timestamp normalization (same DRIFT sections, same reason). That observable is not saturated: the check runs after bash has already expanded the glob, so a symlinked directory is traversed (names only, never content) before the refusal; a check-to-use race remains; `--root /` makes the guard vacuous by declaration; and no r19 receipt carries a strace, so "zero network" is asserted in the round notes, not receipted.

Cites (Round 19):
- Selftest 119 → 122: `corpus/evidence/symlink-r19-20261019T174500Z-selftest.log:123` (PASS 122), cases `:120-122`; prior `scope-r18-…-selftest.log:120`; `SCORECARD.md:975-976`, `:987`; `LOG.md:699`. `cmp` of lines 1–119 vs r18: identical (this session).
- Gate shas: `git show 5499cef:…` → `6e694881…` (above); `git show d650872:tools/research-gate.sh | sha256sum` → `9f1638076915d9bf6ffb5816e342204081cc1ab07bc803fc7cb402147954c2ba`. Gate `sweep_path_guarded` at `d650872` line 1779; `SWEEP_LOCATION_OUT_OF_CORPUS` emits at lines 1953, 1992.
- Demo: `symlink-r19-…-demo.log:1` (BEFORE, 5499cef), `:3` `observed=hit`, `:4` `SWEEP_CLAIM_FALSE`, `:6` DRIFT; `:8` AFTER; `:11` `SWEEP_LOCATION_OUT_OF_CORPUS`; `:13` DRIFT.
- Drift: `symlink-r19-…-drift.log:1` `GATE_DRIFT: none`; `SCORECARD.md:989`.
- Battery: `symlink-r19-…-battery.log` lines 1–133 vs `scope-r18-…-battery.log` lines 1–133, `cmp` after `ts=` normalization: identical (this session); DRIFT lines `:43`, `:85`, `:114`, `:133`.
- Fix contract and limits: `corpus/knowledge/sweep-symlink-r19.md:9-13` (escape), `:24-28` (fix), `:32-39` (named limits).
- Verdict table `SCORECARD.md:984-991` (freshness `unchanged` at `:989`); admission `:993-995`.
- Zero network: `SCORECARD.md:991`; `grep -l strace` over `symlink-r19-*` and `scope-r18-*` receipts exit 1.

## Findings (defects and limits found while grounding)

1. Gate-sha label conflict: `.ufo/reports/round-18/chousa.md:3` labels `6e694881…` a "Work commit"; by `git show`, `6e694881…` is the gate sha at `5499cef` (the gate change is correctly stated at round-18 report `:13`). Relabel the report line; the LOG/SCORECARD gate values stand.
2. r1 `3/3` is asserted, not receipted, in both rounds: `SCORECARD.md:931`, `:981-982`, `LOG.md:672`; zero `VERDICT_BEARING_EXPORTS` lines in the eight r18/r19 receipts. The draft says so; a receipt would need the SCORECARD counting command re-cut.
3. "ALL IDENTICAL vs pre-round gate" (`LOG.md:681`, `:699`; `SCORECARD.md:931`, `:981`) has no diff in any receipt. The battery receipts show landed-gate output only.
4. Battery is output-identity, not CLEAN: claims/chain/verify-all DRIFT in r18, r19 and the r17 battery (`fence-r17-…-battery.log:43,85,114`) because the research/ sources are refused in that run context (`CLAIM_SOURCE_OUT_OF_CORPUS`, `CHAIN_SOURCE_OUT_OF_CORPUS`). Consistent across rounds, but the draft does not call the battery CLEAN.
5. Knowledge-note cite drift (minor): `corpus/knowledge/scope-phrase-gap-r18.md:3` cites `SCOPE_KENGAKU :694`; at `5499cef` the assignment is line 699 and line 694 is the r18 comment block start. Cite should read `:699`.
6. Commit labels not reconciled: `LOG.md:672` "HEAD `02b70c0`" vs `.ufo/reports/round-18/chousa.md:7` "commit `e3c556e`"; `LOG.md:690` "HEAD `71b0b5f`" vs r19 demo "pre-round gate (`5499cef`)". Gate shas (the binding that matters) were verified by `git show`; commit labels were not.
7. README Frontier coverage: `corpus/README.md:319-505` has paragraphs for Rounds 2–10 and 24 only; no paragraph exists for 11–23. This draft fills 18 and 19 only, as assigned.

## Installs
None. Tools used: `git show`, `sha256sum`, `grep`, `cmp`, `sed`, `head` (all pre-installed).

VERDICT: Round 18 and 19 draft paragraphs are grounded in SCORECARD/LOG/knowledge/receipts with path:line cites and git-verified gate shas; r1 3/3 is asserted-not-receipted in both rounds and the battery is output-identity, not CLEAN, so both are stated as limits.

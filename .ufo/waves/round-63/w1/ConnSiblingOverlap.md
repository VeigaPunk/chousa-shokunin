# ConnSiblingOverlap — round 63 chousa, wave w1 (connector, read-only)

Scope: read-only search of `/home/vgpnk/Projects/shokunin/*-shokunin/` (20 sibling lanes, not chousa) for
(a) a lane preflight or gate-runner, (b) knowledge on git object names, abbreviations, tags or revision pinning,
(c) planted-defect or control batteries for a checker. Frozen claims read first: `corpus/evidence/round63/claims.md`
(C1 operability: `tools/lane-preflight.py`; C2 coverage: `corpus/knowledge/git-revision-identity-r63.md`).
Nothing was written outside this report and the seat scratch dir (deleted before yield). No git mutation, no network.

Counting rule: k = sibling artifacts that hold (a), (b) or (c) and are classed SAME-CLAIM or NEIGHBOUR. Items that
only *use* a pattern (e.g. `git rev-parse HEAD` as a clone pin) or match a word without the mechanism are listed as
UNRELATED and not counted.

## Findings

### (a) preflight / gate-runner — no sibling holds a lane preflight with C1's contract

No sibling file is named `lane-preflight` or prints `PREFLIGHT=<passed>/<run>`. Exact-name grep over
`*/tools`, `*/scripts`, `*/SKILL.md`, `*/corpus/knowledge` returned zero hits (`grep -rnE 'lane-preflight|lane preflight|PREFLIGHT=|GATE [a-z0-9]+ .*(PASS|FAIL)'`).
Four near-neighbours hold part of the mechanism:

- A1 NEIGHBOUR (closest) — `kotodama-shokunin/tools/check-gate-battery.py:1-3` (docstring: "Isolated battery for the
  seven structural gate selftests, plus the baseline check over all ten registered gates"); `:52-60` exit map (0/1/2,
  `BASELINE-GATE-UNCOVERED`). Runs each gate's own `--selftest` in a mirror and names uncovered gates. Same shape as
  C1's G06–G08 selftest legs and its "name the failing gate" rule. Not the same claim: no PREFLIGHT line, no summary
  counts, no `--only/--skip`, no defect/benign legs.
- A2 NEIGHBOUR — `kumitate-shokunin/scripts/round-gate.mjs:2-3` ("lane-local pre-check of the fleet round-close
  contract"; `--selftest` flag); summary line `ROUND_GATE: CLEAN (...)` (`corpus/knowledge/round-close-gate.md` head).
  A lane-local aggregated pre-check. It grades round artifacts (report, SCORECARD row, LOG entry), not the lane's own
  committed tools. Kumitate's SCORECARD operability row (`SCORECARD.md:342`) counts it among its runnable artifacts.
- A3 NEIGHBOUR — `tameshi-shokunin/tools/registry-check.py:1-8` ("entry-registry monitor ... replays every active row
  of tools/registry.json and reports how many rows still return their registered outcome"). Replays registered
  commands, not gates; no self-check legs.
- A4 NEIGHBOUR by name and mechanism — `kaidoku-shokunin/tools/round-45/frozen-path-preflight.py:2` ("Frozen-path
  preflight v2") and `kaidoku-shokunin/tools/round-45/c1-counter.py:97-108` (runs the preflight, parses
  `PREFLIGHT_SELFTEST: cases=(\d+) failures=(\d+)`). Different claim (frozen-path git state, not lane gates). Note the
  word "preflight" is already taken in kaidoku; no filename collision with `lane-preflight.py`.

UNRELATED (listed, not counted): `mado-shokunin/tools/mado-verify.sh:1-14` (config-plane verdict vs live bytes);
`souji-shokunin/tests/runner-*.sh` (fixture judges); `kotodama-shokunin/tools/exercise-handoff-e2e.py` `v1_preflight`
(handoff packet field check — a different sense of "preflight").

### (b) git object names, abbreviations, tags, revision pinning — one sibling entry overlaps C2's sourced topic

C2 claims the lane holds nothing on what a revision name names. Sibling lanes do. Explanatory hits (not use-only):

- B1 CONTESTED (same topic, same sources, same git version) — `tsukuroi-shokunin/corpus/knowledge/selector-contract-r21.md:1`
  (sources `S081 https://git-scm.com/docs/gitrevisions/2.56.0` and `S082 https://git-scm.com/docs/git-rev-parse/2.56.0`),
  `:13` (accepts only 7–64 hex selectors "naming a unique actual object", then requires commit peeling), `:22`
  (`tag-to-commit`: "Annotated tag, including nested annotated tags, peels recursively to the commit"), `:23`
  (`tag-to-noncommit`: refuse), `:25` (refusal exits 2). Implementation: `tsukuroi-shokunin/tools/_revision.py`.
  Overlap with C2: abbreviated object names, annotated-tag peeling, `^{commit}`, `rev-parse --verify`. Same version
  pages as C2's S142/S143 (installed git 2.56.0). Not the same claim: its scope is one binder's accepted selectors.
  C2 must cite this entry as prior art or explain why its rows are re-sourced; it cannot present the topic as unheld.
- B2 NEIGHBOUR — `kake-shokunin/corpus/knowledge/commit-citation-hygiene.md:1-3,16-20,65`: abbreviated object-name
  uniqueness (`S136 gitrevisions`, "a leading substring that is unique within the repository"), `git rev-parse -q
  --verify <token>` as resolver. Does NOT cover annotated or lightweight tags, branches or `<rev>:<path>`
  (`grep -nE 'tag|:<path>|branch'` on the file: no hit in the body). Same gitrevisions anchor as C2's `<sha1>` row.
- B3 NEIGHBOUR — `tameshi-shokunin/corpus/knowledge/receipt-revision-binding.md:60` (`git rev-parse --verify --quiet
  '<rev>^{commit}'` binds a receipt's `rev=` to a repository commit) and `:141-142` ("a tag-named receipt is refused
  `RECEIPT_REV_ABSENT` ..., not resolved as a tag"). A pinning rule with an explicit tag exclusion. A knowledge entry on
  revision binding, the closest in function to C2's "what pins a citation to a git revision".
- B4 NEIGHBOUR — `kumitate-shokunin/corpus/knowledge/pinned-evidence.md:1-3,18-19,51-52`: `S031` (git-rev-parse
  `--verify`: "emit exactly one object name on success"); a 40-hex pin match is the gate's own 0/1/2 rule.

UNRELATED / use-only (not counted): `game-dev-3d-shokunin/corpus/knowledge/unreal-mcp/PROVENANCE.md:21-25` and
`executability/*.md` (`git rev-parse HEAD` as a clone pin); `kasegi-shokunin/corpus/knowledge/repo-git-state.md:75`;
`souji-shokunin/corpus/knowledge/git-strict-descendant-relation-r40.md:24` (`cat-file -e <commit>^{commit}`);
`souji-shokunin/corpus/knowledge/git-repo-structure-common-dir.md:61,68` (cites git-rev-parse as corroboration only);
`mori-shokunin/corpus/knowledge/gate-ancestry-r39.md:3,35` (two-dot range via gitrevisions); `kengaku-shokunin/
corpus/knowledge/tb2-git-leak-recovery-grader.md:157,284` (annotated tag as a reachability case; tag objects "not
covered"); `kama-shokunin/SKILL.md:898-904` ("No remote abbreviation uniqueness is claimed" — a limit, not a holding);
`tameshi-shokunin/SKILL.md:1063` and `kaidoku-shokunin/SKILL.md:589` (`rev-parse` in gate rows).

Broad pattern sweep (`rev-parse|abbrev|annotated tag|...` over `*/corpus/knowledge` and `*/SKILL.md`) matched about
150 files, almost all use lines. The explanatory set above is what I opened; the rest matched on use lines only.

### (c) planted-defect and control batteries for a checker — several neighbours, none the same battery

- C-1 NEIGHBOUR (closest in form) — `kumitate-shokunin/scripts/gate-mutants.mjs:1-13` ("run the frozen lane-gate mutant
  set against a measured scripts tree"; K43 kill predicate: evaluable, `VERDICT: FAIL`, stable second run; each control
  re-run after the mutants) and `:149` exit map. Frozen mutants of lane gates with control re-runs: the same discipline
  as C1's frozen legs.
- C-2 NEIGHBOUR — `kaidoku-shokunin/tools/round-34/replay-gate.py:165-172` (`MUTANTS` table: name, needle, replacement,
  expected exit) and `:259-278` (each mutant must be killed; a registered positive control must meet target).
- C-3 NEIGHBOUR — `kaidoku-shokunin/tools/round-44/c1-controls.py:25,625-631` (`CTL-C1-0 do-nothing`) and
  `kaidoku-shokunin/tools/round-30/c2-rust-refusals.py:4-21` (19 frozen mutants with predicted outcomes). The
  "do-nothing control" vocabulary matches C1's null-pass legs.
- C-4 NEIGHBOUR — `tameshi-shokunin/tools/mutate-and-run.sh:1-10,31,67-68,136` (generic mutation runner: green control
  run on the pristine tree, per-defect killed/survived, `--regression` kill-rate ledger).
- C-5 NEIGHBOUR — `mado-shokunin/quality/check-counter-discrimination.py:1-14` (accept/reject control manifest: 3 accept
  controls, 22 reject controls; an always-accept or always-reject instrument fails). Closest in control design to C1's
  CLEAN + defect + benign legs; its target is a counter, not a gate-runner. `mado-shokunin/SCORECARD.md:21` records
  its gate killing 10/10 of tameshi's mutants.
- C-6 NEIGHBOUR — `souji-shokunin/tests/fixtures/r27-pre-report-gate.sh:2,58-68` ("an always-pass false-green
  control"; control must fail). A single planted always-pass stub.

Own-lane precedent (not counted, not sibling): `chousa-shokunin/tools/freeze-check.py` mutants (`# ---- mutants of the
green round-61 triple`) and `tools/research-gate.sh` drift mutants (`:5907-5966`).

## Tally

Counted (SAME-CLAIM or NEIGHBOUR): (a) A1–A4 = 4; (b) B1–B4 = 4; (c) C-1–C-6 = 6. Total k = 14.
SAME-CLAIM: 0 (no sibling holds C1's lane preflight or a C2-equivalent entry for chousa's own claim).
Contested: B1 (tsukuroi-shokunin) against C2 — same gitrevisions/git-rev-parse 2.56.0 topic, abbreviated names and
annotated-tag peeling already held in a sibling knowledge entry. C1 has no contested lane.

## Limits (of this scan)

- Pattern-based: exact-name and mechanism greps. A sibling artifact that holds the mechanism under other words (e.g. a
  "smoke" runner, a `run-all` or `verify-all` in another lane) can be missed. The aggregate-runner grep
  (`run[-_]all|all[-_]selftests?|verify-all|check-all|gate-battery`) matched chousa's `research-gate.sh`, kama's
  `kama-llamacpp-live.py`, kotodama's `check-gate-battery.py`, souji's census and cand scripts, and kake's
  `freshness-sweep.mjs` and `citing_set.py`; none was opened beyond its name, so that is the sweep, not a proof of absence.
- Not run: no sibling tool was executed; overlap is by reading source and docstrings only.
- The broad (b) sweep matched ~150 files; only the explanatory set in (b) was opened. Other matches are use lines.
- Scope of "neighbour" is a judgment from docstrings and cited anchors (INFERENCE where a claim's exact scope was not
  read to the end).

## Recommendation for L1 (integration, not applied here)

1. C2's entry should cite `tsukuroi-shokunin/corpus/knowledge/selector-contract-r21.md` (B1) and
   `kake-shokunin/corpus/knowledge/commit-citation-hygiene.md` (B2) as neighbour prior art, and state that the lane's
   own C2 rows (S142–S144) are its own sourcing. The frozen claim wording ("the lane holds nothing") is true for the
   lane only; any correction goes in an erratum, not in claims.md.
2. C1's docstring and named limits may cite A1 (kotodama) as the nearest sibling gate-battery; no reuse is required.

VERDICT: SIBLING_OVERLAPS=14 contested=tsukuroi-shokunin

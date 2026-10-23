# RevShonenA2 — SHONEN re-check as non-author (r34 attempt-2, wave 2a2)

Access date: 2026-10-23. Lane: `/home/vgpnk/Projects/shokunin/chousa-shokunin`, clone at frozen tip
`707da8184a0fc4d10ab3f17271556cdf364f0af5` in
`/fast/scratch/hyaku/chousa-r34-a2/w2/RevShonenA2/clone` (`git clone -q` + `git checkout -q <tip>`;
`git rev-parse HEAD` confirmed). Gate pinned:
`sha256sum clone/tools/research-gate.sh` = `a6307edf687ac0fb1b0b08bf7f0518b3fbc310fa9924b970aa3654612562995b`
(prefix `a6307edf687ac0fb` matches the wave pin; the lane working-tree copy hashes identically).
Verdicts are a recommendation, never an admission. Frozen C1 exclusion not re-opened.

## Box 3 — "Instructions executable by an agent without oral context" → [x] (verifier: RevShonenA2)

Command (in clone, TMPDIR set to my scratch):
`TMPDIR=/fast/scratch/hyaku/chousa-r34-a2/w2/RevShonenA2/tmp timeout 1700 bash tools/research-gate.sh --selftest`
→ exit `0`, `RESEARCH_GATE_SELFTEST: PASS (256 cases, 0 skipped)`; 256 `ok-case` lines, wall 126.6 s.
Receipt: `.ufo/waves/round-34/w2a2/RevShonenA2/selftest-tip.log` (sha256 `5311643c…`).
This re-runs the box-3 checkable claim at the current revision: attempt-2's dead-zone cases
254–256 (`claims-deadzone`, `claims-deadzone-line`, `claims-deadzone-edge`) all `ok`, so the C2
selftest pins hold for a non-author.
Audit-set coverage of box-3 pointers: `shonen-00` (`corpus/evidence/round25-measure-after.log` exists),
`shonen-01` (`corpus/evidence/round25-meta-differential.log` exists) — both `ok` in my self-audit re-run
below. Existence only; their content is not re-verified by the set.
Remaining [~] caveat: "without oral context" is attested for the selftest command itself (ran cold in a
fresh clone with only TMPDIR set); other surfaces' docs were not exercised.

## Box 4 — "No cross-domain bleed (PROVINCE.md still accurate)" → [x] (verifier: RevShonenA2)

`git diff bf7c931a HEAD -- PROVINCE.md` → empty. Byte equality:
`git show bf7c931a:PROVINCE.md | sha256sum` == `sha256sum PROVINCE.md` == `cf7826a4…c1bbec`.
Last content change: commit `3282042` (round-1); PROVINCE.md was NOT touched by attempt-2
(`git diff --stat bf7c931a..HEAD` lists 45 files, PROVINCE.md absent).
Accuracy spot-check: "Owns:" (question framing, source hierarchy, citation chaining, claim-vs-source)
matches SKILL.md's decision-table rows; "Refuses:" (kasegi / kengaku / kumitate orchestration /
unapproved live-target / secret values) matches SKILL.md "Boundaries (hard)" lines 54–62 and the
round-25 sibling check `.ufo/waves/round-25/build/ConnectorMetaSiblings.md` exists (5523 B).
Audit-set coverage: `path-15` PROVINCE.md `ok`; `shonen-02` metadata-screen-r25.md `ok`;
ConnectorMetaSiblings.md is NOT in the audit set (exists on disk only).
Caveat: [x] = unchanged-since-`bf7c931a` + accurate-by-inspection; it inherits the earlier accuracy
finding rather than re-proving it.

## Box 1 — "SKILL.md contains real decision tables, error patterns, checklists, cited sources" → [x] structural / [~] content

Audit-set coverage of its pointers (`SHONEN.md` line for box 1 cites the Gates table +
`corpus/knowledge/metadata-screen-r25.md`):
- `shonen-02` — `corpus/knowledge/metadata-screen-r25.md` exists → `ok` (existence only).
- `skill-tally-256` — `SKILL.md` contains `PASS \(256 cases\)` → `ok`.
- `skill-tally-253-stale` — `SKILL.md` does NOT contain `PASS \(253 cases\)` → `ok`.
- The set does NOT check that the Gates/decision tables are real; only SKILL.md text assertions.
Non-author structural verification (me, today): SKILL.md has `## Decision table` (l.13, 9 populated
rows), `## Error patterns` (l.39, 9 rows), `## Boundaries (hard)` (l.52), `## Checklist (executable)`
(l.64, checkbox list), `## Gates` (l.73, full verdict-map table incl. the r34 counter row l.90).
Cited sources resolve: `metadata-screen-r25.md` cites S029/S033 with `verified-at:`/`recheck:` headers;
both S-ids resolve in `corpus/SOURCES.md` rows 39 and 43 (S065 at row 75 also present, used by C2).
What stays [~]: correctness of each table row's domain content (I verified structure and pointer
resolution, not per-row truth); the entry remains partly a lane assertion for content.

## Box 2 — "At least one end-to-end domain task executed and logged in LOG.md" → [x] (verifier: RevShonenA2)

Audit-set coverage of its pointers (`LOG.md` Round 9; `corpus/fixtures/archives-r9/`; r25
explicit-root hold battery): NONE of the three pointers is in `audit-set.json`. (`log-r34a1-lesson`
greps LOG.md for `corpus/lessons/round-34\.md` — a round-34 line, unrelated to the Round-9 entry;
`path-14` is the r34-a2 battery summary, not the r25 battery.) Audit-set answer: coverage = nil.
Non-author re-execution (me, today, all in scratch clone at tip):

1. `LOG.md` Round-9 entry exists (`## Round 9 — archives verified end-to-end`, ~l.455); report
   `.ufo/round-9/chousa-goalwave.md` exists (2013 B); fixtures `corpus/fixtures/archives-r9/`
   (A/B/C-r9.md, README, controls/) exist; `claims-r9.jsonl` sha256 `f6f0d1ab…f5` == README pin.
2. Copied fleet `research/` into the scratch parent (archive sha256s match README pins:
   A `9033857d…`, B `6d8dbddd…`, C `e48fe70f…`) and symlinked `chousa-shokunin → clone` so
   `--root ..` resolves like the real layout.
3. `bash tools/research-gate.sh verify-all corpus/fixtures/archives-r9/{A,B,C}-r9.md --root ..`
   → all three `RESEARCH_GATE: CLEAN (sections=5 run=5 absent=0 drift=0)`, exit 0, with tallies
   matching README lines 73–101 exactly (A: `VERDICT_BEARING_CLAIMS=10/10 RESOLVED_HOPS=6/7
   REJECTIONS_OK=4/4 refs=13 resolved=12`; B: `6/7, 3/3, refs=14 resolved=13`; C:
   `RESOLVED_HOPS=7/8 REJECTIONS_OK=4/4 refs=15 resolved=14`). Receipts
   `.ufo/waves/round-34/w2a2/RevShonenA2/verify-all-{A,B,C}.log`.
4. r25 explicit-root hold battery re-run at tip:
   `bash corpus/evidence/round25-holds/battery.sh <clone>` (default ANALYSIS_ROOT=
   `/home/vgpnk/Projects/shokunin`, read-only) → 11/12 MATCH incl. `selftest`, all three
   `verify-all-*-r9`, and the negative controls; the one DIFF is `drift-r12` — see finding F1.
   Receipt `battery-tip.log` (sha256 `01a1f390…`). The committed r25 record
   `corpus/evidence/round25-final-holds.log` shows 12/12 MATCH at round-25 freeze.
   Incidental positive: two layout-miss runs produced real findings (`CHAIN_SOURCE_MISSING`;
   `CLAIM_SOURCE_OUT_OF_CORPUS`) — the fixtures bind bytes, not names.

## Bonus re-derivation (C3 counter, non-author)

`timeout 300 python3 corpus/evidence/round34/self-audit.py` in the tip clone → 43 `AUDIT id=… ok`
lines, `SELF_AUDIT_MISMATCHES=0`, `SELF_AUDIT_UNDISPOSITIONED=0`, exit 0 — reproduces the committed
first counted run verbatim. Receipt `selfaudit-tip.log` (sha256 `b709781c…`). I did not re-run the
C2 counter (sibling seats own that); only the self-audit above.

## Findings

- **F1 (minor, stale pin — routed, not an r34 regression):** `drift-r12` battery row now reports
  `GATE_DRIFT: +resolvable drift` exit 1 vs the baseline's `none`. Verified by `--pin` capture vs
  baseline diff: the canonical text block is byte-identical; the JSON manifest gained exactly one
  key `sections[2].tallies.resolvable` (chain mode's r32-era exempt-hop "resolvable" observed-state,
  gate lines 111–123/2317). Nothing removed or changed. The r12 pin (gate `91a01695…`) predates that
  additive tally; the r25 battery matched because the key did not exist yet. Recommend routing a
  baseline refresh note for `corpus/evidence/round25-holds/holds/drift-r12.log`. [INFERENCE]: the
  `resolvable` tally landed between the r25 freeze and r34; I attributed it to chain exempt-hop
  semantics by the matching code comments, not by bisect.
- **F2 (lane-state observation, non-blocking):** lane `git HEAD` is `fe3db76c`, one commit ABOVE the
  frozen tip `707da818` ("wave-2a2 spec/plan/taskcall re-frozen"), diff limited to the three w2a2
  spec JSONs — no production file, gate, or counter moved; my clone used the frozen tip as assigned.
  Untracked in lane tree: `corpus/evidence/round34/__pycache__/` and `.ufo/waves/round-34/w2a2/`
  (wave seats; the pycache is the "inherited leftover" class noted in commit `fce3119`'s message —
  a new instance, harmless but committed-garbage-adjacent if ever added).

## Box verdicts (recommendation only)

- Box 1: `[x]` structural non-author verified (RevShonenA2); keep `[~]` only for per-row content
  truth, which the audit set does not cover and I did not adjudicate.
- Box 2: `[x]` non-author verified (RevShonenA2) — end-to-end task re-executed CLEAN at the tip
  gate with every pinned tally reproduced; zero audit-set coverage of its pointers (name that gap).
- Box 3: `[x]` non-author verified (RevShonenA2) — `PASS (256 cases, 0 skipped)` at tip.
- Box 4: `[x]` non-author verified (RevShonenA2) for "unchanged + accurate-by-inspection".

## Limits

No C2 counter run (sibling-owned); box-1 content truth out of scope; battery run used the fleet
root read-only as the baselines demand; verify-all needed a reconstructed `..` layout (research/
copy + chousa-shokunin symlink) — a scratch-environment requirement, not a fixture defect.
Receipts shas: `.ufo/waves/round-34/w2a2/RevShonenA2/RECEIPTS.md`.

# chousa round 95 — plan (ChousaR95a2, attempt 2)

Base `7b2373586fb70f0ead6446c671fcc8b546d3e687`. L1 `ChousaR95a2` holds the canonical planner seat (the validator
refuses `planner`), the freeze and the integration.

## Why these claims, not the planned row

The SCORECARD `## Planned — round 95` row proposed three more layers on the lane's own control instruments
(a declare-then-read leg for the r94 driver, a punctuation-quote fixture, exact heading equality). The round-94
spot-check rated expansion `unchanged` and its operator note asks that meta-work on the lane's own instruments be
weighed against domain work; run-15 §6 says bookkeeping-only rounds are thin. Attempt 1 of this round started the
declare-then-read driver and died after ten minutes without a freeze; its untracked files are listed with
digests in `.ufo/waves/round-95/inherited-attempt1.txt` and were discarded unverified (its
`control-driver-r95.py` `input_report` returns 6 values on one path and 7 on the other). The planned items stay
carried (SCORECARD round-95 block).

This round instead works a named domain gap of the lane's own province (search-strategy taxonomy, claim-vs-source
verification): `corpus/README.md:398-399` — "the sweep re-run is a glob/existence check over the named locations,
never the recorded command". PRISMA-S (S222, opened this round) supplies the standard: a strategy filed exactly as
run (item 8), its limits (9), its updates (12), the date of the last search (13), the records identified per
source (15), and, in ITEM 15's explanation, what a re-run with a drastically different count indicates.

- **C1 operability (lowest scored axis), capability acquisition** — `tools/search-rerun.py`.
- **C2 depth** — `corpus/knowledge/search-rerun-record-r95.md`.
- Causal separability: C1's record searches the base-revision capture store (no dependency on the entry); C2's
  instruments are the lane's unchanged `gate-records.py` and `research-gate.sh verify-metadata` (no dependency on
  the tool). Both cite S222.

## Pre-freeze controls (committed at the freeze, run before any wave seat scores)

- C1 battery `corpus/evidence/round95/rerun-controls-r95.py`: positive, strict-tree, 8 forgeries each also given
  to `research-gate verify-sweeps` (prior instrument, expected to ACCEPT), 12 setup refusals, a `--shared` clone
  with one edited capture and one symlink, the do-nothing base path, and three stand-ins (constant-CLEAN,
  count-only mutant, rev-blind mutant) that must FAIL the same battery.
- C2 battery `corpus/evidence/round95/entry-controls-r95.py`: positive, 8 forgeries through `gate-records.py`
  (word change, cross-column join, wrong capture key, word miscount, tier, fetched time, >25-word quote,
  sourceless copy), the do-nothing base path.
- Before receipts at base: `corpus/evidence/round95/before/c1-base.txt`, `c2-base.txt` (both exit 2).

Pre-freeze instrument fixes (before any freeze, recorded so they are not mistaken for post-scoring edits):
1. C2 battery `g7-long` first used a 25-word quote that is also absent from the capture, so the tool answered
   `QUOTE_ABSENT` rather than `QUOTE_LEN` (the battery printed `FAIL` for its own case). Replaced with a 32-word
   span that IS contiguous in the text form (items 8 and 9 of Table 1), so only the length rule can refuse it.
2. `tools/search-rerun.py` performance: first draft re-read every blob per search and walked the whole lane tree
   (one verify ~8 s); blob reads are now cached per run and the tree/rev walks start at each glob's static
   directory (verify ~1.3 s). Semantics unchanged; the battery was re-run after the change.
3. The entry's first draft said the lane "never captured" PRISMA-S's full text; two base captures (S120 Cochrane
   ch.4, S204 Campbell guide) cite the paper's title, so the sentence was narrowed to the measured fact: no base
   capture contains the item-15 sentence (`/usr/bin/grep -l -F`, exit 1). The README pointer it inherited
   (`390-391`) was stale and is cited as `398-399`.

## Round-94 spot-check routed defects

- D1 (report ledger class miscount 9/1/9 vs 8/1/10): this round's report computes the class tally with the
  `awk` command and pastes its output; the lesson's `## Mistakes` mines it.
- D2 (`LOG.md` round-94 "After" bullet stale): an append-only correction entry in `LOG.md` round 95.
- D3 (Gate URL + access date): the S222 Gate record in `corpus/lessons/round-95.md` names URL, access date
  (2026-11-08, fetched 22:51:39Z) and a located quote.
- D4–D6 (ledger attribution wider than the seat's evidence): this round's ledger rows cite the seat's own
  finding ids and say what the seat did not measure; corrections for r94 recorded append-only in `LOG.md`.
- D7–D8 (`plans/round-94.md` revision pair / preamble stale): recorded as an appended correction in `LOG.md`
  round 95; `plans/round-94.md` is not rewritten.

## Carried, not worked this round

The round-94 planned items (declare-then-read driver leg, punctuation fixture, exact heading equality), the
round-74 source-blind order oracle (this round's C1 battery carries its own `ORACLES` group, which is the same
discipline applied to a new instrument, not a fix of the r74 counter), the r82 clip range, QUALITY 173's
successful-refused record form, the r80 backlog Gate ids.

## Amendments after the freeze

Re-frozen at F2. Every amendment cites the wave artifact that forced it; the F text of `claims.md` is kept, the F2
sentences and predicates are appended there. No amendment widens a claim; each narrows a sentence to what the
instrument enforces or repairs the instrument so the sentence holds, and each repair is covered by a new
battery leg that the F-state fails (C1 `carrier-c-tool` oracle; C2 `BINDING` group).

1. **C2 entry repaired** (`R95ExecC2Repro` F1, `R95ReviewerC2` F1–F4, rows 2/3/4/5/6 and the prose): Q7–Q9 are two
   sentences, not one (reading-order text form); row 5's "nearly the same … timeframe" was carried by an unlocated
   line, now located as Q10/Q11; row 2 omitted item 9's justification duty, now Q12; row 6's "indicative of errors"
   now Q13 and the Do reads "errors in the published (reported) search"; row 3's Lane now marks the
   revision-as-slice reading as the lane's analogy (Q6 is about date limits); row 4's Never no longer imports item
   16; "title only" for S120/S204 narrowed to "neither contains that sentence". Records 9 → 13; `N_RECORDS` 13.
2. **C1 grep alignment** (`R95ExecEngine` F1–F3, F5): a final newline no longer opens a phantom empty line; `*`/`?`
   no longer match a leading dot; `**` is refused; POSIX bracket classes are refused. Battery group `GREP_AGREE`
   (expected values are GNU grep's own output over a bash glob, taken at run time); the F tool fails it
   (`oracle-carrier-c-tool`). Locale (F4) and NUL/binary (F6) are named limits (b), (c).
3. **C1 battery coverage** (`R95MutantsC1` m10, m11, m13–m17): forgeries f9 (list-form count) and f10 (duplicated
   path), the printed `rev_match` cross-checked on every forgery, a same-count file swap in the clone, and
   `GREP_AGREE` rows for whole-file and case-folding; `mutants-r95.py` rebuilds the survivors against the amended
   tool and must kill all of them.
4. **C1 containment** (`R95SentinelScope` F1–F4): every git call runs with the caller's `GIT_*` removed,
   `GIT_NO_REPLACE_OBJECTS=1`, `GIT_NO_LAZY_FETCH=1`; a relative record is resolved against `--root`; a symlinked
   record is refused (`RECORD_TYPE`). Battery group `CONTAINMENT`. The docstring's "reads only ROOT … no network"
   now states what is read.
5. **C1 record parsing** (`R95ReviewerC1` F1, F3, F2, F4): the digest is over byte-sorted path bytes (a non-UTF-8
   name no longer crashes); a table line after the first table is a setup refusal (`TABLE`); the record's "As run"
   section and the docstring state that `\|` is the Markdown escape for `|` (Q6 ran as an alternation); a comma in
   a path is a named limit of the list form.
6. **C1 sentence narrowed** (`R95ConnectorSiblings` P1, `R95RevenPrior` F2, `R95CriticClaims` C1 clauses 1, 4):
   "the nearest prior instrument" → "the lane's nearest prior instrument" (tameshi `count-recheck.py` and kagi
   `recheck-replay.py` re-run one pinned command in sibling lanes — routed, not absorbed); the prior's acceptance is
   stated as vacuous; the engine qualifier is in the sentence.
7. **C2 sentence narrowed and instrumented** (`R95CriticClaims` C2 clauses 2, 5): "each warranted" → each names
   located-quote qids whose quotes share a content word with the Do (`WARRANT_TERMS`, a lexical floor), plus
   `LANE_FILLED`; faithfulness stays the reviewer's judgment, said so in the sentence. The C2 battery gains a
   constant-gate `ORACLE`.

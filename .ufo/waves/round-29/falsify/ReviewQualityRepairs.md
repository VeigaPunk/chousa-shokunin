# ReviewQualityRepairs — round-29 repair review (wave 2 falsify)

Scope: (1) QUALITY criteria 23-25 appended to `corpus/QUALITY.md`; (2) dated D3
corrections appended to `LOG.md`, `SCORECARD.md`, `corpus/lessons/round-28.md`.
Lane HEAD at review: `b18b3ec`; reviewed content is unchanged since `30c9d24d`
(`git diff 30c9d24d..HEAD` on the four files = 0 lines).

## Item 1 — QUALITY criteria 23-25: HOLDS

- `git diff 6c5eb146 30c9d24d -- corpus/QUALITY.md`: 27 added lines, 0 real
  deletions (`grep -E '^-' | grep -v '^--- '` → none). Appended under
  `## Round-29 additions` at line 150; criteria 1-22 untouched.
- Each names how it fails: 23 "It fails (exit 1) on lessons/round-28.md";
  24 "Fails when a control receipt meets the counter and data still runs";
  25 "Fails when a verdict other than VERBATIM is dropped or relabelled".
- `python3 corpus/evidence/round29/prose-check.py corpus/lessons/round-28.md`
  → exit 1, "9 glued tokens … 5 custody hits, TOTAL hits=14" — exactly the
  numbers criterion 23 prints.
- New-block check: extracted lines 150-end to scratch → exit 0, 0 hits.
- Mutant (scratch): `glued99` + "Root report" → exit 1 (2 hits). Clean control
  (`all 69`, `on 2026-10-23`, backticked `all69`) → exit 0. Unreadable file →
  exit 2 (fails closed, distinct from hits).
- Criterion 25's S047 `</head>` example verified in
  `corpus/knowledge/quote-reopen-r29.md:85-91`; verdict set
  VERBATIM/ABSENT/TOO_LONG/NO_SOURCE/UNREACHABLE and `--items` flag confirmed in
  `tools/quote-reopen.py:18-19,384-424`.

**Defect (non-fatal):** criteria 23 and 24 cite `lessons/round-29.md`; no such
file exists in `corpus/lessons/` or anywhere outside `.ufo` build dirs
(`find` + `git log --all` empty). Criterion 25's `knowledge/quote-reopen-r29.md`
resolves corpus-relative to `corpus/knowledge/quote-reopen-r29.md` (exists).
Dangling evidence pointers; checker's operability unaffected.

## Item 2 — D3 dated corrections: HOLDS

- `git diff 6c5eb146 30c9d24d -- LOG.md SCORECARD.md corpus/lessons/round-28.md`:
  additions only — three +4-line hunks, zero real deletions; no earlier line
  rewritten (old text explicitly "kept as written").
- Facts vs fleet witness `git -C /home/vgpnk/Projects/shokunin show
  b4b338e9:.ufo/waves/hyaku/chousa28-negative-records/parent-census.json`:
  - argv `sources-census.sh validate --root … chousa` — exact match.
  - at `2026-10-22T02:49:09.859760+00:00` — "02:49:09 UTC" match.
  - `actual_safe_commit` `7c87b9734eb71985e19767af36d57dff89536521` — match.
  - exit 0; stdout `chousa\tok\t…/chousa-shokunin/corpus/SOURCES.md` — printed
    "chousa ok" is a faithful rendering.
- D3 routing cite `round-28-verifier-spotcheck.md:50-54,125-126` checked:
  lines describe the stale-statement defect and prescribe dated corrections
  without rewriting old entries — matches what was done.
- Minor wording note: SCORECARD's original text said no census "authorised" at
  that stage; the correction paraphrases as "says no end census was run".
  Run-status correction, not a factual error. Correction dates "2026-10-23" are
  UTC-consistent (commit 22:32 -0300 = 2026-10-23 01:32Z), not a defect.

## Limits / residual risk

- Did not rerun `c1-count.py` or the 130-item verify (outside this scope).
- Whole-file `prose-check.py corpus/QUALITY.md` exits 1 on pre-existing hits in
  criteria 1-22 text (case215, over71, sum71/72, true38); criterion 23 scopes
  itself to "the round's new prose", so this is consistent but means the check
  cannot be run blanket over the file.
- Installs: none. Scratch only at
  `/fast/scratch/hyaku/chousa-r29/w2/ReviewQualityRepairs/`.

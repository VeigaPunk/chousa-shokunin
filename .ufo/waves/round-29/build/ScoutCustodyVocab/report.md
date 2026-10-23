# R29 W1 — read-only sweep: D1 (digit-glued tokens) and D2 (custody vocabulary)

Seat: `ChousaR29.ScoutCustodyVocab` (leaf, read-only). Date: 2026-10-22.
Scope: `/home/vgpnk/Projects/shokunin/chousa-shokunin/{LOG.md,SCORECARD.md,SKILL.md,corpus/README.md,corpus/QUALITY.md,corpus/SOURCES.md}`
plus all 19 `.md` files in `corpus/lessons/`. No file in the lane was modified by this seat.

## Method (what I ran)

Scripts live in `/fast/scratch/hyaku/chousa-r29/w1/ScoutCustodyVocab/` (copies kept beside the report);
the only lane writes are `sweep.tsv`, `sweep.tsv.detail.txt` and `report.md` inside
`.ufo/waves/round-29/build/ScoutCustodyVocab/` plus this file at
`.ufo/waves/round-29/build/ScoutCustodyVocab.md`.

- `timeout 300 python3 sweep2.py <out.tsv>` → exit 0. Strips fenced blocks and inline `` ` `` spans,
  then counts `\b[a-z]+[0-9]{2,}\b` (D1) and six custody phrases (D2, case-insensitive, raw text).
- `timeout 300 python3 attribute.py` → exit 0; per-hit nearest-preceding-round-heading attribution.
- `timeout 300 python3 lexicon.py` → exit 0; wider custody lexicon with the same attribution.
- `timeout 60 git status --porcelain` → exit 0: `?? .ufo/waves/round-29/build/` (mine). An earlier run of
  the same command in this session also listed `?? corpus/evidence/round29/__pycache__/` (not mine — a
  sibling seat's import artifact); the later run did not, so that path was removed by someone else
  between the two runs.

No network call, no tool install, no `lsp` use (no language server answers Markdown, so all evidence
below is literal text scan, not semantic proof).

## D1 — digit-glued tokens

Columns in `sweep.tsv`: `file, d1_count, d2_count, examples, d1_prose_glue, d1_identifier_shaped,
d1_inside_code_spans, d1_raw_count, d2_phrases, d2_round28_only`. Line-level dump:
`sweep.tsv.detail.txt` (808 lines).

| File | d1 outside code spans | inside code spans | prose glue | identifier-shaped |
|---|---|---|---|---|
| LOG.md | 158 | 64 | 64 | 94 |
| SCORECARD.md | 91 | 98 | 27 | 64 |
| SKILL.md | 31 | 33 | 9 | 22 |
| corpus/README.md | 64 | 93 | 7 | 57 |
| corpus/QUALITY.md | 7 | 7 | 5 | 2 |
| corpus/SOURCES.md | 59 | 0 | 24 | 35 |
| corpus/lessons/round-27.md | 80 | 10 | 56 | 24 |
| corpus/lessons/round-26.md | 45 | 18 | 42 | 3 |
| corpus/lessons/round-25.md | 57 | 13 | 18 | 39 |
| corpus/lessons/round-27-verifier-spotcheck.md | 16 | 2 | 13 | 3 |
| corpus/lessons/round-28.md | 9 | 5 | 9 | 0 |
| corpus/lessons/round-28-verifier-spotcheck.md | 1 | 13 | 1 | 0 |
| corpus/lessons/round-24.md | 57 | 8 | 0 | 57 |
| 10 dated lesson files, round-1, round-24-verifier-spotcheck | 0–6 each | 0–6 | 0 | all |

Totals: 722 D1 matches outside code spans, of which 275 are prose glue and 447 are identifier-shaped;
a further 374 matches sit inside backtick spans and are excluded by the ticket's rule (raw regex total
1,096 over the 25 files).
`identifier-shaped` = `sha256`, `r\d\d` revision shorthand, RFC/DOI/URL fragments (`rfc9111`, `n71`,
`c52`, `c75`), `i3507`, `trec34` path segment, `p19` page ref — the regex catches these but they are
not glue. The strongest prose-glue examples per the routed class: `all69`, `proposal64`, `actual64`,
`blanket64`, `on2026` and `most25` at `corpus/lessons/round-28.md:26,30,46,48`; `original187`/`legacy161`
at `corpus/lessons/round-28.md:11,19`; `mined20` at `corpus/lessons/round-28-verifier-spotcheck.md:73`.

**Round-28 text versus older rounds (D1, prose glue).** Only in round-28 text: `corpus/lessons/round-28.md`
(9/9) and `corpus/lessons/round-28-verifier-spotcheck.md` (1/1). Mixed with a small round-28 tail:
`LOG.md` 2 of 64 (line 1162), `SCORECARD.md` 2 of 27 (line 1577), `SKILL.md` 1 of 9 (line 562),
`corpus/SOURCES.md` 5 of 24 (lines 54, 55, 80). Older-round text only: `corpus/README.md` (7),
`corpus/QUALITY.md` (5), `corpus/lessons/round-25.md` (18), `round-26.md` (42), `round-27.md` (56),
`round-27-verifier-spotcheck.md` (13). So the class is not round-28-specific: 255 of the 275 prose-glue
hits sit in older-round text (129 in the rounds 25–27 lesson files, 126 in the pre-round-28 sections of
the six named files), and round-28 text carries 20 (10 in the two round-28 lesson files, 10 in the named
files' round-28 sections: `LOG.md:1162`, `SCORECARD.md:1577`, `SKILL.md:562`, `SOURCES.md:54,55,80`).

**Sentinel blind spot (falsifier on the routed rule).** The regex requires lowercase `[a-z]+`, so the
same glue in capitalised form is invisible: `LOG.md:1040` "All132", `corpus/SOURCES.md:47`
"Version December2019", `corpus/SOURCES.md:49` "Recommendation2013", `corpus/lessons/round-26.md:43`
and `:138`, `corpus/lessons/round-28.md:19` "Original187". A case-insensitive variant would add these
to the count; a `[A-Za-z]` variant over the same file set matches 580 tokens, mostly real identifiers
(`S001`, `M13`, `Round27`), so widening the class needs an identifier allowlist like the one above.

## D2 — custody vocabulary

Counted strings (the routed six): `Parent approval`, `Parent decision`, `CURRENT_MAIN_DIRECTIVE`,
`report-LAST`, `Root report`, `private original`. 14 occurrences in 5 files, **all in round-28 text**:

| File | n | lines | context |
|---|---|---|---|
| `LOG.md` | 2 | 1177, 1179 | `## Round28 — DERIVED honest-negative publication record` |
| `SCORECARD.md` | 1 | 1587 | `## Round28 — DERIVED full-claim honest negative` |
| `corpus/SOURCES.md` | 1 | 85 | the round-28 Search-log bullet opened at line 80 |
| `corpus/lessons/round-28.md` | 5 | 5, 39, 53, 63 | in-file round-28 lesson text |
| `corpus/lessons/round-28-verifier-spotcheck.md` | 5 | 14, 47, 48, 129 | 4 of the 5 are the defect routing quoting the phrases |

Zero occurrences in the 21 other lesson files, in `SKILL.md`, `corpus/README.md`, `corpus/QUALITY.md`,
and in every pre-round-28 section of `LOG.md`, `SCORECARD.md` and `corpus/SOURCES.md`. Confidence: high
(exact substring scan over all 25 files, both cases; every hit line printed in `sweep.tsv.detail.txt`).
Of the 14, 9 are custody prose in use (`LOG.md` 2, `SCORECARD.md` 1, `SOURCES.md` 1, `round-28.md` 5)
and 5 are the spot-check file naming the class it routed.

**Older precedent for the surrounding lexicon (inference-marked boundary of the D2 rule).** The six
strings are round-28-only, but the actor term is older: `LOG.md:300` and `:333` are `Parent acceptance`
sign-offs inside the `## Round 2` and `## Round 3` sections (dated 2026-10-15/16), `corpus/lessons/round-27.md:148`
reads `Parent correction (Main IRC, 2026-10-21)`, and `corpus/lessons/round-27-verifier-spotcheck.md:57`
reads `Parent- or author-dispatched advice`. The word `custody` also predates round 28, in a different
sense — chain of custody at the export (`corpus/README.md:29,264,478`;
`corpus/lessons/2026-10-16-verifying-conversion-not-original.md:1,55`) and `credential custody`
(`corpus/lessons/round-27-verifier-spotcheck.md:67`). Widening D2 to the bare actor term would therefore
flag rounds 2, 3 and 27 as well; keeping D2 as the six named strings keeps it round-28-only.

## Verdict and limits

- D2: confined to round-28 text in 5 files; the routed six phrases have no older-round occurrence.
- D1: present in 24 of the 25 files (only `corpus/lessons/round-24-verifier-spotcheck.md` is clean);
  round-28-only in the two round-28 lesson files, otherwise carried
  from rounds 25–27 and earlier. Most raw matches (447 of 722) are identifiers, not glue, and a further
  374 matches sit inside backtick spans (excluded by the ticket's rule).
- Limits: the fleet report `.ufo/reports/round-28/chousa.md` (where the spot-check counted 23 distinct
  tokens) is outside this seat's file list and was not opened. No `lsp` server serves Markdown, so these
  are literal scans; the prose/identifier split is a stated allowlist, not a semantic classification.
  Counts are from the committed bytes at the time of the run (2026-10-22); the lane tree was not modified
  by this seat.

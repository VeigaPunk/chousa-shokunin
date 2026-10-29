# ScoutC2RowsCensus — round 62 w1 — candidate rows S138–S140 census validation

Date 2026-10-28. Item: validate `corpus/evidence/round62/controls/c2v2-positive-rows.txt` (3 rows) against
the SOURCES contract (`CORPUS.md` § SOURCES.md) with the maintained census script and the frozen manual
census lines. No frozen file edited; all runs in scratch `/fast/scratch/hyaku/chousa-r62/ScoutC2RowsCensus/`
(lane copy `cp -a`, rows inserted after S137 at registry line 147, positive entry copied to
`corpus/knowledge/openat2-resolve-r62.md` in the copy only). Scratch removed before yield.

## Findings

1. **Column count — pass.** Each candidate row parses as 11 columns (`awk -F'|'` NF=13); manual
   malformed-row count stays 0 after insertion (`NF!=13` counter prints 0). No `|` inside cells.
2. **Id uniqueness / collision — pass; S138–S140 free.** Registry has no rows S138/S139/S140
   (`grep -n 'S13[89]\|S140' corpus/SOURCES.md` in the Registry range: no match); dup-id awk prints
   nothing before and after insertion. Registry ids end at S137 (line 147), so the candidates are the
   next unused. Observation: the only textual S139/S140 mention in SOURCES.md is round-45 Search-log
   prose ("staged S139, S140, S132, re-pointed by document") — INFERENCE: those staged names were
   re-pointed to other ids and never landed as rows, so no id is reused.
3. **Enums — pass.** kinds `docs`, `code`, `own-work` all in the 10-value kind enum; tiers `A`,`A`,`B`
   ∈ {A,B,C}; no community-at-A (E10 silent); statuses all `mined` (E07 silent).
4. **ISO dates — pass.** `opened=2026-10-28` on all three rows = today (UTC), not future → E08 silent.
5. **Recheck cadences — pass.** S138/S139 `on-release` (symbolic, matched by the parser's
   `^[A-Za-z][A-Za-z0-9 _-]*$`, overdue-reported never overdue-judged), S140 `180d` (NNd) → E09 silent.
6. **Used-by paths — pass conditional on the entry landing.** All three rows use
   `corpus/knowledge/openat2-resolve-r62.md`, which does not exist on the current lane: rows-only
   validate gives 3× `E11 missing used-by`, exit 1. With the positive entry present (as in the frozen
   C2 scratch-mirror control), validate is `ok`, exit 0. Expected, not a defect: the entry is C2's
   deliverable; E11 is exactly the leg that binds rows to it.
7. **0–3 leading-space parser note — confirmed, and the frozen/manual divergence is real.** The
   candidate rows are column-zero. Probe copies of the after-registry: rows indented 2 spaces are still
   counted by the maintained script (rows 140, A 110, B 24, mined 115; validate ok, exit 0) while the
   frozen manual grep (column-zero only) prints 137; rows indented 4 spaces are silently ignored as
   indented code (census back to 137/108/23/112, no E12 raised, validate exit 0). Landing the rows at
   column zero keeps both counters in agreement.
8. **W-codes — none added.** The baseline registry already carries 5 W04 duplicate-URL-across-scopes
   warnings (S051, S053, S073, S074, S075) before and after; validate still exits 0 (warnings never
   change status). The three candidates add no W01/W02/W03/W04 (no URLs, tier A/B, used-by set).
9. **Script census on the full fleet was not run** — out of item scope; `--file` mode validates exactly
   this registry (`FLEET` lines mirror the single file). No other lane touched.

## Census before → after (expected vs observed)

| metric          | expected | observed before | observed after |
|-----------------|----------|-----------------|----------------|
| rows            | 137→140  | 137             | 140            |
| tier A          | 108→110  | 108             | 110            |
| tier B          | 23→24    | 23              | 24             |
| tier C          | —        | 6               | 6 (unchanged)  |
| status mined    | 112→115  | 112             | 115            |
| status queued   | —        | 19              | 19 (unchanged) |
| status rejected | —        | 6               | 6 (unchanged)  |
| tier/status invalid | 0   | 0               | 0              |
| new W-codes     | none     | —               | none (same 5 baseline W04) |

## Evidence (commands run from cwd = lane copy `/fast/scratch/.../lane`; script invoked by absolute path)

- Before manual: `grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md` → `137`;
  malformed → `0`; tier hist → `A=108 B=23 C=6`; status hist → `mined=112 queued=19 rejected=6`;
  dup-ids, enum-violations, missing-used-by → all empty.
- Before script: `bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh census --file
  $PWD/corpus/SOURCES.md` → `file rows 137 / tier.A 108 / tier.B 23 / tier.C 6 / status.mined 112 …`,
  `census_exit=0`; `validate --file` → 5× W04 (S051,S053,S073,S074,S075) + `file ok …`,
  `validate_exit=0`.
- Candidate rows shape: `awk -F'|' '{print "row" NR " cols=" NF-2 " id=" $2}' …/c2v2-positive-rows.txt`
  → `row1 cols=11 id= S138 `, `row2 cols=11 id= S139 `, `row3 cols=11 id= S140 `;
  `grep -c '^| S'` → `3` (column-zero).
- Insertion: `awk -v n=147 -v rf=$ROWS 'NR==n{print; while((getline r<rf)>0) print r; close(rf); next} 1'`
  → S138–S140 directly after S137, before blank + `## Paths`.
- Rows-only validate (no entry): `file E11 S138|S139|S140 missing used-by
  corpus/knowledge/openat2-resolve-r62.md`, `validate_exit=1`.
- After manual: rows `140`; malformed `0`; tier `A=110 B=24 C=6`; status `mined=115 queued=19
  rejected=6`; dup-ids/enum/missing-used-by all empty.
- After script census: `file rows 140 / tier.A 110 / tier.B 24 / tier.C 6 / status.mined 115 /
  status.queued 19 / status.rejected 6`, `census_exit=0`; FLEET mirrors the file.
- After validate: same 5 baseline W04 + `file ok`, `validate_exit=0`.
- Indent probe (copies inside the lane copy): 2-space rows → manual grep `137` vs script `140`,
  validate ok exit 0; 4-space rows → script `137/108/23/112`, zero S138–S140 findings, validate exit 0.
- Contract source: `/home/vgpnk/Projects/shokunin/CORPUS.md` lines 64–157 (shape, rules, census lines,
  parser note); parser implementation `scripts/sources-census.sh` (E-codes W-codes, 0–3 space regex
  `^ {0,3}\|`, symbolic recheck regex, E11 relative to the registry file's parent dir).

## Verdict

All three candidate rows conform to the SOURCES contract as checked: 11 columns, unique free ids
S138–S140, valid kind/tier/status enums, ISO opened date today, legal recheck cadences, used-by path
resolvable once the round-62 entry lands (E11 red before it does, by design), no new W-codes, and the
maintained parser's 0–3-space rule verified against both accepted and ignored indentation. Census moves
exactly as predicted: 137→140 rows, A 108→110, B 23→24, C 6, mined 112→115, queued 19, rejected 6.

VERDICT: CENSUS_EXIT=0 rows=137->140 findings=none

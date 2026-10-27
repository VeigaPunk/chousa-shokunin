# R53ExecInfStaged — inference-ground on the three staged C2 entries

Seat: R53ExecInfStaged (leaf). Read-only on `/home/vgpnk/Projects/shokuknow/merge/chousa`
and on `.qcache`. No install, no network, no lane file written. Scratch:
`/fast/scratch/hyaku/chousa-r53/R53ExecInfStaged` (`export TMPDIR` set there for every run below),
removed at the end. Write: this report only.

## 1. What ran, and what it printed

Command (three legs, same flags, `--root` into my scratch so the entry path reports as a name):

```
python3 tools/inference-ground.py --entry /home/vgpnk/Projects/shokuknow/merge/chousa/knowledge/corpus/knowledge/<E>.md \
  --spans /dev/null --counts /dev/null --registry corpus/SOURCES.md \
  --root /fast/scratch/hyaku/chousa-r53/R53ExecInfStaged/root
```

Observed output, verbatim, with exit codes:

```
=== search-tracking-record-r40 ===
GROUND entry=search-tracking-record-r40.md section=1 bullets=3 tokens=3 grounded=1
FINDING INF_TOKEN_NOT_IN_SPAN bullet=2 token='the number of records identified from each information source'
FINDING INF_UNCITED bullet=3 token=''
FINDING INF_TOKEN_NOT_IN_SPAN bullet=3 token='other methods'
GROUND: FAIL
exit=1
=== western-instrument-alignment-r50 ===
GROUND entry=western-instrument-alignment-r50.md section=1 bullets=0 tokens=0 grounded=0
FINDING INF_NO_BULLETS bullet=0 token=''
GROUND: FAIL
exit=1
=== quality-control-guideline-issued-text-r48 ===
GROUND entry=quality-control-guideline-issued-text-r48.md section=1 bullets=0 tokens=0 grounded=0
FINDING INF_NO_BULLETS bullet=0 token=''
GROUND: FAIL
exit=1
```

With `--spans /dev/null` the tool's `span_texts` returns `[]` for every bullet by design, so
`INF_TOKEN_NOT_IN_SPAN` here means "no span supplied", not "phrase absent" — the phrase is checked
against the capture in §3. `INF_UNCITED` (E1 bullet 3) and `INF_NO_BULLETS` (E2, E3) are structural:
bullet 3 cites no `S` id, and E2/E3 have a **prose** `#### Inference` section (no `-` bullets), so
the tool sees zero bullets and would fail the same way with a full spans manifest.

## 2. Findings per Inference bullet

E1 = `corpus/knowledge/search-tracking-record-r40.md`; E2 = `…/western-instrument-alignment-r50.md`;
E3 = `…/quality-control-guideline-issued-text-r48.md`; E2/E3 units are section paragraphs (P1..),
the unit a bulleted rewrite would produce. Keys: S134 `0ae65ac01b93119d3c2f3fed`, S193
`c9d1e74c3ac8d9eb332c9770`, S195 `16fe8487aa97b98576a0dbac`, S190 `0435b64f65c3ea7ddc6bb92e`.

| entry | bullet first 60 chars | finding (as emitted) | candidate phrase | capture key | offset |
|---|---|---|---|---|---|
| E1 B1 | This is the answer to a question the lane could not previous | none emitted (see N1) | `should be reported in which column` | 0ae65ac01b93119d3c2f3fed | 5996 |
| E1 B2 | The count and the strategy are per source, which is what mak | INF_TOKEN_NOT_IN_SPAN bullet=2 | `reporting the number of records identified from each information source` | 0ae65ac01b93119d3c2f3fed | 1320 |
| E1 B3 | Column 2 is where the lane's unverifiable hops live. Citatio | INF_UNCITED bullet=3 + INF_TOKEN_NOT_IN_SPAN bullet=3 | `citation searching, and other methods` | 0ae65ac01b93119d3c2f3fed | 6355 |
| E2 P1 | A citation is not an alignment. The corpus's Chinese documen | INF_NO_BULLETS bullet=0 | `aligns with the current reporting guidance` | c9d1e74c3ac8d9eb332c9770 | 13494 |
| E2 P2 | That gives the corpus a sharper reading of its own PRISMA-S | INF_NO_BULLETS bullet=0 | `PRISMA-S ( Rethlefsen et al 2021 )` | c9d1e74c3ac8d9eb332c9770 | 13592 |
| E2 P3 | The two traditions also frame the same problem differently, | INF_NO_BULLETS bullet=0 | `is important for minimizing bias` | c9d1e74c3ac8d9eb332c9770 | 36693 |
| E2 P4 | The campaign's cross-tradition lead is therefore answerable, | INF_NO_BULLETS bullet=0 | `reporting aligns with the current reporting guidance for PRISMA` | c9d1e74c3ac8d9eb332c9770 | 13484 |
| E3 P1 | Two distinct findings, and the corpus needs both. | INF_NO_BULLETS bullet=0 | `文献研究的质量控制` | 16fe8487aa97b98576a0dbac | 9940 |
| E3 P2 | The substantive one survives the version change: the centre' | INF_NO_BULLETS bullet=0 | `会议论文、未发表的学位论文、产业报告、咨询报告` | 0435b64f65c3ea7ddc6bb92e | 3348 |
| E3 P3 | The bookkeeping one is a correction to the corpus's own row. | INF_NO_BULLETS bullet=0 | `数据库应包括多个中、英文专业数据库` | 16fe8487aa97b98576a0dbac | 10360 |

## 3. Candidate verification (the check I ran)

`cap.count(ph)`, `cap.find(ph)`, the enclosing line index, and whether the occurrence sits inside one
line — on the whole `.txt` sidecar read as UTF-8, per table row:

```
n=1 and oneline=True for all ten; find offsets == table offsets. chars/ws-words/cjk, table order:
34/6/0  71/10/0  37/5/0  42/6/0  34/7/0  32/5/0  63/9/0  9/1/9  23/1/20  17/1/16
lines: 74 22 78 578 578 632 578 672 127 701
```

`has_two_words` (the tool's own function, imported) is True for all ten, so each is a token
`grounding_tokens` will read; `n=1` + one line satisfies the lane's quote rule (≤25 whitespace words,
≤160 chars). Re-reading this report's table after writing it and re-finding every phrase reproduced
`rows 10 mismatches 0`, so the phrases above are byte-exact copies of the captures.

## 4. Findings reported, not patched

- **N1 — E1 bullet 1 is grounded by a Registry *title*, not by a span.** `grounded=1` for E1 comes
  from `2020` matched against the designator `PRISMA 2020` in S114's Registry row (S094's and S114's
  titles dump as `['PRISMA2020','PRISMA 2020','BMJ 2021']`/`[]`; `S130` has **no Registry row**:
  `{'S130': None, 'S134': None, 'S185': None, 'S186': None, 'S190': None, 'S193': None, 'S195': None}`,
  `registry rows: 116`). The bullet's real claim — local copy vs URL, round 3's `S094` — carries no
  span and no phrase token at all, so it is unexamined rather than grounded.
- **N2 — E1's front-matter `recheck:` quote cannot be quoted under the lane rule.** It prints
  "PRISMA-S also recommends reporting the number of records identified from each information source",
  and the capture breaks that sentence between lines 21/22: `'PRISMA-S also recommends reporting the number of records'` → `count 0`, `'recommends reporting'` → `count 0`. The groundable form is
  the single-line continuation at offset 1320 (E1 B2 above). The drafted bullet must cut at the break.
- **N3 — E1 bullet 3's token is not unique.** `other methods` occurs 4 times in the S134 capture
  (`count` at 5636, 6379, 15026, 15807); the unique single-line form is E1 B3's candidate (6355).
- **N4 — E2 and E3 cannot be grounded bullet-by-bullet as written.** Both `#### Inference` sections are
  paragraphs (`bullets=0`, `INF_NO_BULLETS`). Each claim above needs a `-` bullet with at least one
  `S` id and one phrase; the candidates in §2 are the phrase for the first claim of each paragraph.
- **N5 — E3's bookkeeping quote is wrong against the issued capture.** E3 Observation says the issued
  text reads `可根据评价主题确定纳入与排除标准，可基于 PICOS 原则`; the S195 line is
  `'证据，应根据评价主题确定纳入与排除标准，可基于“PICOS”'` (`应根据 count 2`, `应根据` at the PICOS
  clause; the single `可根据` sits at offset 12145, line 809, in the 经济性维度 text). So the 应→可
  shift is in `可基于“PICOS”`, not in `可根据…`; and `可基于“PICOS”` is **not** a legal grounding token
  (3 CJK chars, one latin word), so the bullet must ground the `多个` half (E3 P3 candidate) and state
  the `应→可` change without quoting it.
- **N6 — E3/E2 absence claims hold on the capture.** S195 `灰色文献` count 0, `灰色` 0, `未发表` 0,
  `内部资料` 0, `期刊评审` 0 — the entry's "each count 0" is reproduced. Absence is a count, not a
  quotable span: those bullets need the counts manifest, not `--spans /dev/null`.
- **N7 — the five C2 documents are not yet in the lane Registry.** 116 rows; the planned ids
  S117–S121 are `ABSENT` (free), and the staged entries' own ids S134/S185/S186/S190/S193/S195 have no
  row either. Nothing here re-opens a frozen predicate; this is the state adoption has to change.

## 5. Verdict

VERDICT: built and attacked the inference-ground grounding for all three staged C2 entries — the tool
fails all three (E1: `INF_UNCITED` bullet 3 + two `INF_TOKEN_NOT_IN_SPAN`, only `2020` "grounded" via a
Registry title; E2/E3: `INF_NO_BULLETS`, prose sections), and each of the 10 units now has a
byte-exact, unique, single-line candidate phrase with its offset and capture key, so a bulleted
rewrite is groundable; three defects reported for the draft were found (N1 title-borrowed grounding,
N2 line-crossing recheck quote, N5 misquoted `应根据`), none patched.

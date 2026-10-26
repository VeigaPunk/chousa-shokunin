# R52DraftReadme — corpus/README.md round-52 additions (draft)

Seat: `R52DraftReadme`, leaf. Lane: `/home/vgpnk/Projects/shokunin/chousa-shokunin`.
Base: `00f8c7f5272a1d98b6d34913985fa4537e00aaf9` (registry max id `S112`:
`grep -o '^| S[0-9]\+' corpus/SOURCES.md | … | sort -n | tail -3` → 110 111 112).
No production file, index or jj state was written; this file is the only write.
Nothing installed (no tool needed). Scratch `/fast/scratch/hyaku/chousa-r52/R52DraftReadme`, removed.

## What was read (grounding for the draft)

- `corpus/README.md:1-1111`; sections are `Coverage map` (3-88), `Round-N evidence`,
  `Known gaps` (174), `Frontier` (348, round-by-round narrative), per-round
  `frontier disposition` sections, and `## Round51 coverage and frontier` (1085-1111)
  with `### Frontier` (1095). **No section lists lane tools**: tool rows have been
  table rows (round 49 `../tools/assimilate-rows.py` at 1075; round 50 self-test
  fixtures at 1076-1081).
- `corpus/evidence/round52/claims.md` (124 lines) — C1 and C2 predicates, targets,
  controls, kill rules; entry paths and the four documents.
- Staged package read-only: `merge/chousa/SOURCES.append.md:36,37,50,54` (rows
  `S111` 梅斯医学, `S112` 中国全科医学, `S125` NIPH `.docx`, `S129` archived
  Japanese PRISMA 2020) and `merge/chousa/knowledge/corpus/knowledge/japanese-prisma-item-wording-r40.md`
  (61 lines; its `source: S129` line and `verified-at: 2026-10-23`).
  `japanese-search-record-niph-form-r52.md` and `chinese-prisma-s-reception-r52.md`
  do **not** exist in the staged package or in `corpus/knowledge/` yet (siblings are
  drafting them), so the rows below are grounded on the captures and the frozen
  claim, never on unseen entry prose.

## Measurements the drafted rows cite (each command run here)

| Fact | Command | Observed |
|---|---|---|
| base sweep empty | `git -C … grep -l -e 文献検索期間 -e 完全な検索戦略 -e 检索报告清单 00f8c7f… -- corpus/knowledge` | no output, `rc=1` |
| each term absent at base | `git grep -c -e "$t" 00f8c7f… -- corpus/knowledge \| wc -l`, per term | 0 / 0 / 0 files |
| sweep not vacuous | `git grep -l 検索 00f8c7f… -- corpus/knowledge` | `rc=0`, 4 files (r36, r37, r38, r38-amendment) |
| NIPH text form | `python3 tools/capture-text.py $Q/3a8b45977cd111e45e3980a5.raw \| wc chars` | `chars 19682` |
| NIPH quote | `… --locate 'SRにおける文献検索期間について明記する'` | `LOCATED count=1 offset=8996` |
| NIPH terms in text form | python count over the same form | 文献検索期間 2 (first 9002), データベース 4, 検索式 1, 検索者 0; heading `3.1システマティックレビューのリサーチクエスチョン` at 8471 |
| docx `.txt` sidecar is garbage | python over `.qcache/3a8b…txt` | 168952 chars, 72117 U+FFFD, 文献検索期間 0 |
| JP PRISMA at archive | python over `.qcache/e84bfe97808591d23fe3266f.txt` | 5328 chars, 完全な検索戦略 1 (offset 766), 検索者 0, item 6 requires それぞれの情報源が最後に調べられた日付 |
| CN checklist | python over `.qcache/cacddf3bbf780a4c7582bb17.txt` | 检索策略 2, 所有数据库 2, item 6 requires 每一项来源的检索或查询日期, item 7 完整检索策略 incl. 过滤器和限制条件, 检索报告清单 0 |
| 梅斯医学 page | python over `.qcache/453d492becd9a2f4632cb8dd.txt` | 8804 chars, 检索报告清单 7, 16个条目 2, 检索式 0 — body is 摘要 plus metadata; item text is in an attached PDF the capture does not hold |
| C1 counter (capability row) | `TMPDIR=… python3 corpus/evidence/round52/c1-count.py --work …` | `LEGS=9/9`, `C1=PASS`, `rc=0`, `REAL … chars=19682` |
| builder's second reader agrees | python import of `build-spans.py`, `docx_text(raw)` on the same capture | `builder chars 19682 find quote 8996` |
| before/control receipts (cited in the block) | `cat corpus/evidence/round52/controls/c1-before.txt` | tool absent → `LEGS=0/9 C1=FAIL exit=1`; naive 4/9; cache-txt 0/9; const 0/9 |

## Draft — to append at end of `corpus/README.md` (nothing above it changes)

```markdown
## Round52 coverage and frontier (2026-10-26)

| Note | Holds | Sources |
|---|---|---|
| `knowledge/japanese-search-record-niph-form-r52.md` | Round-52 note (lane id `S115`; the staged row is `S125`, a different id space): the search-record fields a national institute's own health-technology-assessment submission form requires, read this round in the `.docx` text form round 51 did not have — section 3.1 (`3.1システマティックレビューのリサーチクエスチョン`, text-form offset 8471) requires the review's search period to be stated explicitly (`SRにおける文献検索期間について明記する。`, offset 8996, `--locate count=1`), with the search's end fixed at a point after the analytic frame is decided and before the manufacturer's analysis submission; the form names a database (4 occurrences) and a 検索式 (1) and names no 検索者 (0) | `S115`; capture `.qcache/3a8b45977cd111e45e3980a5.raw` (178056 bytes; text form 19682 characters through `tools/capture-text.py`); row in `corpus/SOURCES.md`; `evidence/round52/c1-count.py` REAL leg |
| `knowledge/japanese-prisma-item-wording-r40.md` | Round-52 note (lane id `S116`; staged `S129`, whose `verified-at: 2026-10-23` is the stage's date, not this round's): PRISMA 2020's own Japanese wording, read at the web-archive copy of the JPT ONLINE translation because the publisher's host no longer serves the file — item 6 (情報源) requires every database, register, website, organisation and reference list consulted together with それぞれの情報源が最後に調べられた日付, and item 7 (検索戦略) the complete strategy for every database, trial register and website including the filters and limits used (`完全な検索戦略`, offset 766 of the capture's extracted text); the term 検索者 does not occur (0 in 5328 extracted characters), so PRISMA 2020's Japanese text names no searcher | `S116`; capture `.qcache/e84bfe97808591d23fe3266f.raw` (PDF, 343301 bytes) and its `.txt` extraction; row in `corpus/SOURCES.md`; `evidence/round52/c2-count.py` |
| `knowledge/chinese-prisma-s-reception-r52.md` | Round-52 note (lane ids `S113` `S114`; staged `S111` `S112` — staged `S111` is the SinoMed record of the Chinese PRISMA-S, a different document): the Chinese reception of the two PRISMA search items as two pages state it — a 梅斯医学 page carrying a 中国循证医学杂志 interpretation (the 摘要: PRISMA-S is PRISMA 2020's extension stated as 16 items for search reporting; the article interprets it item by item in Chinese, then examines its cross-disciplinary reach, its limits as a 报告规范 and Chinese-database localisation; the item text itself is in the attached PDF the capture does not hold) and 中国全科医学's own published PRISMA 2020 checklist (item 6 信息来源: all databases, registers, websites, organisations and reference lists, with 每一项来源的检索或查询日期; item 7 检索策略: the complete strategy for every database, register and website including the filters and limits used) | `S113` `S114`; captures `.qcache/453d492becd9a2f4632cb8dd.raw` (276803 bytes) and `.qcache/cacddf3bbf780a4c7582bb17.raw` (88313 bytes); rows in `corpus/SOURCES.md`; `evidence/round52/c2-count.py` |
| `../tools/capture-text.py` | Round-52 lane tool: the text form of an OOXML WordprocessingML capture — main part from the `_rels/.rels` officeDocument relationship (no fixed member name), `w:t` text with entities decoded, run-level `w:tab`/`w:br`/`w:cr` as tab/newline/newline, a newline at every `w:p` end, nothing from `mc:Fallback`, `w:delText`, `w:instrText` or `w:pPr/w:tabs`; `--locate QUOTE` prints `LOCATED count=<n> offset=<o>` and exits 0 only when the quote occurs once; a non-zip, relationship-less or part-less capture is refused with exit 2 and a `REFUSED` stderr line | `corpus/evidence/round52/c1-count.py` (`LEGS=9/9 C1=PASS`), `controls/c1-before.txt`, `controls/{naive-tool,cache-txt-tool,const-tool}.py` |

Coverage credit for round 52 is per document, as in round 51: the three entries rest on four documents, and four documents is four registry rows, numbered by document in ascending staged id from the registry's highest id at the base (`S112`) — `S111`→`S113` (the 梅斯医学 page), `S112`→`S114` (the 中国全科医学 checklist), `S125`→`S115` (the national institute's `.docx` form), `S129`→`S116` (the archived Japanese PRISMA 2020 translation). Staged ids name other lane rows (lane `S111` is the SinoMed record, lane `S112` the JAHBS article), so no staged id is carried over: each entry's `source:` line and each row's `used-by` cell name the lane id. One entry rests on two documents (`S113`, `S114`); two rest on one each. The `.docx` document refused in round 51 for its capture form is one of the four, re-grounded in the round-52 text form — its refusal is lifted by the tool, not by a re-fetch.

Ground at the base, re-run and absent: `git -C /home/vgpnk/Projects/shokunin/chousa-shokunin grep -l -e 文献検索期間 -e 完全な検索戦略 -e 检索报告清单 00f8c7f5272a1d98b6d34913985fa4537e00aaf9 -- corpus/knowledge` printed nothing and exited `1`; each of the three terms alone matched 0 files at that rev. The check is not vacuous there: `git -C … grep -l 検索 00f8c7f5272a1d98b6d34913985fa4537e00aaf9 -- corpus/knowledge` exits 0 with four files (`aggregator-vs-source-r36.md`, `citation-count-semantics-r37.md`, `japanese-search-record-r38.md`, `japanese-search-record-r38-amendment-2026-10-23.md`).

### Frontier

Advanced — what these documents move:

- **The search-record field set.** Round 51 left the theme's field statement in six Japanese and Chinese documents. Four more documents state it here, and one states it at a level the lane did not hold: the national institute's `.docx` form requires the search *period* explicitly and fixes when it ends (section 3.1, offset 8996), alongside the database and the search expression as run — a period, not the per-source last-search date PRISMA asks for. The Japanese PRISMA 2020 text (items 6 and 7) and the Chinese checklist (items 6 and 7) are the same two items in two languages, and the 梅斯医学 page states PRISMA-S as 16 search items with its own limits as a reporting standard. The field set now has three named shapes: PRISMA's per-source date plus full strategy, PRISMA-S's 16 items, and the Japanese form's period plus expression.
- **Non-Western field rules for a search record.** Round 51's three entries rested on six captures; these add four, and the Japanese half now includes PRISMA's own translation rather than only a checklist copy — so "PRISMA 2020's Japanese text names no 検索者" is stated from the translation, and the national institute's form likewise names no 検索者 (0 occurrences in its text form), which narrows where the searcher field comes from: a Japanese industry form, not the national institute and not PRISMA.
- **The capture-form refusal.** Round 51 refused the `.docx` form because its text existed only in a compressed member the span pipeline could not bind. The round-52 text form binds it: 19682 characters, the search-period sentence once at offset 8996, and the same 19682 characters from the span builder's own reader. What round 51 could not open, this round reads.

Left open — named, not closed:

- **Searcher identity.** Still open and now narrower: the Japanese PRISMA 2020 translation (0 occurrences of 検索者 in its extracted text) and the national institute's form (0 in its text form) name no searcher, and neither Chinese page does; the one Japanese source that files 検索者 is the industry notification form's attachment (V)-5. Whether the searcher is a field of the record or a local addition of one form is unresolved, and no Chinese source naming it has been found.
- **The official Japanese PRISMA 2020 translation at its live host.** Half-closed: the translation is now read, but at its web-archive copy — the publisher's host still serves no file. Whether the 2024 archive is the current revision is not established.
- **A Chinese national standard.** Unchanged and open: nothing this round is a standard, and the round did not reach 中国科学技术信息研究所's guidance. The absence remains documented only for animal-experiment systematic reviews.
- **The Chinese PRISMA-S item-by-item text.** Narrowed, not closed: the 梅斯医学 page states that the interpretation is item-by-item and 16 items long, but the item text is in an attached PDF the capture does not hold, so the sixteen items' own Chinese wording is still unread.
- **An imperfect search.** Unchanged: no document this round says what a record must carry when a platform failed or a query was truncated.

### Lane tool: `tools/capture-text.py` (capability note)

No section of this file lists lane tools — tool capability has been carried as a row in the round coverage tables (round 49's `../tools/assimilate-rows.py`, round 50's self-test fixture package). `tools/capture-text.py` is carried the same way, as the fourth row of the table above; this note records what the row's one line cannot.

- **What it is.** One defined text form for a `.docx` capture, so a quote's offset is reproducible: main part resolved from `_rels/.rels`, never a fixed member name; `w:t` text with XML entities decoded; run-level `w:tab`/`w:br`/`w:cr`; a newline at every `w:p` end; nothing from `mc:Fallback`, `w:delText`, `w:instrText` or `w:pPr/w:tabs`. `--locate` prints `LOCATED count=<n> offset=<o>` and exits 0 only when the quote occurs exactly once (else 1); a non-zip, a zip with no officeDocument relationship, or a missing main part is refused with exit 2 and a `REFUSED` stderr line, nothing on stdout.
- **What it was measured at.** Nine legs over packages generated at counting time from fresh random text and member names, plus the pinned national-institute capture: `python3 corpus/evidence/round52/c1-count.py` → `LEGS=9/9`, `C1=PASS`, `rc=0`, `REAL … count=1 locate=(0, 1, 8996) chars=19682`. The round-51 lane at the base has no such tool (`controls/c1-before.txt`: `LEGS=0/9 C1=FAIL`), and the three cheap substitutes score 4/9, 0/9 and 0/9 on the same interface.
- **What it is not.** Offsets are Python code-point indices into the text form, not byte offsets into the capture, so a `char N` anchor is only meaningful against the same reader. It has no form for PDF captures (their cached `.txt` extraction is the text form) and no form for the campaign cache's `.docx` `.txt` sidecar, which must not be used: for the pinned capture that sidecar holds 168952 characters, 72117 of them U+FFFD, and `文献検索期間` zero times. It says nothing about whether the text is the document the row claims — a capture-form check, not an identity check.
```

## Notes for the L1 integration

- Append the block above at EOF, after the round-51 correction lines
  (`corpus/README.md:1106-1111`). Nothing above it needs editing; the round-51
  paragraph at 1092 keeps its `S107`–`S112` credit untouched.
- Row order follows the frozen C2 predicate's entry order (NIPH, PRISMA wording,
  Chinese reception), which is also `文献検索期間`, `完全な検索戦略`, `检索报告清单`.
- The three entry rows name lane ids `S115`, `S116`, `S113`/`S114` as **planned**
  ("lane id `S115`; the staged row is `S125`"). If the adopter assigns ids in a
  different order, the row's `S` tokens and the credit paragraph's `→` chain must be
  changed together — they are the only two places in this block that name them.
- The rows cite capture files, byte sizes, text-form character counts and term
  counts that this seat measured; they cite no sentence from an entry, because the
  three entries were not yet in the lane or the staged package when this was
  written. If an entry's own limits land differently (e.g. the 梅斯医学 item text
  turns out to be recoverable), row 3's last clause and the "item-by-item text" open
  item are the two lines to correct.
- The tool row's `LEGS=9/9 C1=PASS` is this seat's own run at `13bc280`; if the
  landed commit differs, re-run the counter before appending.

VERDICT — drafted the round-52 README additions (three per-document credit rows, a per-document credit paragraph, the base-sweep receipt with a non-vacuity control, a Frontier advance/left-open update, and a capability note plus tool row for `tools/capture-text.py`) and grounded every cited count; the C1 counter re-run independently confirmed `LEGS=9/9 C1=PASS`, so the draft rests on tool behaviour I exercised rather than on the claim file alone.

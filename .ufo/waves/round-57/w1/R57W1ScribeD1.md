# R57W1ScribeD1 — round-56 closure defect D1: drafted `#### Corrections (round 57)` for `grey-literature-field-china-r42.md` + `表 10` sweep

Seat: scribe (leaf; no dispatch, no fetches, no lane writes outside this file). Base read at lane tip `f9736a39`.
Every number below is re-measured on lane-owned bytes this seat opened; nothing is inherited from a prior report.

## 1. What the defect is, from the files

- `corpus/knowledge/grey-literature-field-china-r42.md:9` (`recheck: 180d …`) still instructs: "the journal's 表 10 row still carries `Ⅰ级` and `A`".
- Round-56 closure names it: `corpus/lessons/round-56-verifier-spotcheck.md:35` ("D1 — corrections sweep missed one mention … the recheck line … instructs a future re-check against the wrong table") and routes it as item 1 at `:105` ("Append a correction … a new `#### Corrections (round 57)` block; no rewrite … Then sweep every lane file for any other "表 10 row" instruction").
- The Observation bullet `:18` uses 表 10 legitimately (the misleading text-form caption), so the fix is one instruction line, not the entry's findings.

## 2. Ground measurements on the committed S129 bytes (no network)

Capture key = first 24 hex of `sha256(url)` = `5233bf47babaa1ca2b49ed15` (computed, matches `refetch.tsv` col 3).

```
$ awk -F'\t' '$1=="S129"' corpus/evidence/round57/refetch.tsv   # key cols
attempt=1 rc=0 http=200 raw=7a0b198c663394cb3f5455553deb7d43df184992d8eb0db627410e1c98eae526 txt=beac2b7feb425a8885927850ea79ed5e916339c6f5cd4b45c3abbf1753f49b05
attempt=2 rc=0 http=200 raw=7a0b198c… txt=beac2b7f…
$ sha256sum corpus/captures/5233bf47babaa1ca2b49ed15.raw → 7a0b198c…  (matches both attempts)
$ python3 -c "sha256(open('corpus/captures/5233bf47babaa1ca2b49ed15.txt','rb').read())" → beac2b7f…
```

`beac2b7f…` is the `capture_sha256` pinned by `corpus/evidence/round56/spans.tsv` rows 16–21, i.e. the committed `.txt` carries the pin. (C2's verdict for S129 is the frozen counter's to print; this seat records only the digests it read.)

Offsets in that text form (`len 80732`; it is byte-identical to the recipe applied to the raw — checked, not assumed):

```
$ pdftotext -layout corpus/captures/5233bf47babaa1ca2b49ed15.raw $S/s129.txt && cmp -s $S/s129.txt corpus/captures/….txt  → LAYOUT_TXT_BYTE_EQUAL
20520 '表7    药品临床综合评价的信息来源情况'      (line 271; 表7 count=1)
22422 '表 10。'                                   (cross-reference "详见表 10。")
22539 '表 10   其他研究的研究类型、研究方法及内容'  (line 292; 表 10 count=2)
22564 '灰色文献 未公开发表的研究信息，…  Ⅰ级    A'  (line 293; Ⅰ级 22606, A 22612; 灰色文献 count=1)
22848 '表8     原始研究的研究类型、研究方法及内容'  (line 296; 表8 count=1)
```

Independent extractor, same committed raw, `pdftotext` 26.08.0 in default (non `-layout`) mode — the round-56 closure series reproduces exactly:

```
$ pdftotext corpus/captures/5233bf47babaa1ca2b49ed15.raw $S/s129-raw.txt   (len 42841)
13013 '表7\n\n药品临床综合评价的信息来源情况…'
13591 '灰色文献 未公开发表的研究信息，…\nⅠ级\nA'
13653 '表8\n\n原始研究的研究类型、研究方法及内容…'
14566 '表 10。\n表 10\n\n其他研究的研究类型、研究方法及内容…'   (caption itself at 14572)
```

## 3. Drafted block (append verbatim after the current last line, `:35`; never edit lines 1–35)

```markdown
#### Corrections (round 57)

Appended on round-56 closure defect D1 (`corpus/lessons/round-56-verifier-spotcheck.md:35`, routed item 1 at `:105`); the lines above stand as filed.

- **The `recheck:` line's table target is corrected: the row is 表7's, not 表 10's.** Read the `recheck:` instruction above as "… and the journal's `灰色文献` row of `表7    药品临床综合评价的信息来源情况` still carries `Ⅰ级` and `A` …". In the committed text form (`corpus/captures/5233bf47babaa1ca2b49ed15.txt`, byte-identical to `pdftotext -layout` 26.08.0 applied to the committed `.raw`; its sha256 `beac2b7feb425a8885927850ea79ed5e916339c6f5cd4b45c3abbf1753f49b05` is the S129 pin) `表7    药品临床综合评价的信息来源情况` is at char 20520 (line 271) and the row `灰色文献 未公开发表的研究信息，…` at char 22564 (line 293; `Ⅰ级` 22606, `A` 22612), with `表8     原始研究的研究类型、研究方法及内容` at char 22848 (line 296).
- **Why that form misleads, and the place rule that avoids it.** Line 292 carries the right column's `表 10   其他研究的研究类型、研究方法及内容` (char 22539), and the `灰色文献` row — a left-column row of 表7 — follows it in file order; the `表 10` string occurs once more at char 22422 as a cross-reference (`详见表 10。`). Neither occurrence carries the row, so a re-checker locates the row between 表7's caption (20520) and 表8's (22848) and never by the nearest caption above (round-56 closure §4, `corpus/lessons/round-56-verifier-spotcheck.md:90`).
- **The independent extractor agrees on the committed bytes.** `pdftotext` 26.08.0 in default mode (no `-layout`) on `corpus/captures/5233bf47babaa1ca2b49ed15.raw` prints `表7` 13013 < `灰色文献 未公开发表的研究信息，…` 13591 < `表8` 13653 < `表 10` 14566 — the round-56 closure's series (`corpus/lessons/round-56.md:11`), re-measured this round.
- **The rest of the `recheck:` line stands unchanged**: the draft item `（9）灰色文献：未公开发表研究信息` under 7.2.3.3 (`S127`, char 24624), the note's `（2）2024 年 6 月-8 月` stage (`S128`, char 3064) and the open T/CLPA number question are untouched by D1.
```

Only this heading/bullets are new; no line above is rewritten, so the entry stays append-only and C2/C3 (which read `corpus/knowledge` at their own revs) are unaffected by the append.

## 4. The sweep — every hit classified

`grep -rn '表 10\|表10' corpus SKILL.md` → 10 hits in 6 files (the unspaced form `表10` and the full-width-space variant `表　10` add none; `SKILL.md` has no hit at all).

| # | file:line | what it is | class | action |
|---|---|---|---|---|
| 1 | `corpus/knowledge/grey-literature-field-china-r42.md:9` | `recheck:` instruction "the journal's 表 10 row" | **STALE INSTRUCTION** | **needs the appended correction (§3)** |
| 2 | `corpus/knowledge/grey-literature-field-china-r42.md:18` | Observation: names 表 10 as the misleading text-form caption, then places the row in 表7 | legitimate mention | none |
| 3 | `corpus/lessons/round-56.md:11` | Mistakes row 3: records the misplacement and the `表7 13013 < 灰色文献 13591 < 表8 13653 < 表 10 14566` series | legitimate record | none |
| 4 | `corpus/lessons/round-56-verifier-spotcheck.md:35` | D1 description (the defect statement) | legitimate record | none |
| 5 | `corpus/lessons/round-56-verifier-spotcheck.md:90` | §4 layout finding ("`表 10` is the right column's title") | legitimate record | none |
| 6 | `corpus/lessons/round-56-verifier-spotcheck.md:105` | routed item 1: the instruction to append the correction (now discharged by §3) | legitimate instruction | none |
| 7 | `corpus/evidence/round56/spans/S129-4.txt:1` | span slice for the row (offset 22484, quote `灰色文献 …` at 22564): the 表 10 caption at 22539 falls inside the slice as context | legitimate evidence | none — the manifest row's `quote` is the 灰色文献 line and the 表7 caption row (offset 20440, quote 20520) is already the fixed one |
| 8 | `corpus/QUALITY.md:960` | criterion 109, states the defect class | legitimate criterion | none |
| 9 | `corpus/captures/5233bf47babaa1ca2b49ed15.txt:290` | source bytes: `详见表 10。` | evidence | none (never edit captures) |
| 10 | `corpus/captures/5233bf47babaa1ca2b49ed15.txt:292` | source bytes: 表 10 caption | evidence | none |

Verdict of the sweep: **one file needs an appended correction line — `corpus/knowledge/grey-literature-field-china-r42.md` (§3 draft). Every other hit is a legitimate mention (record, criterion, or the source's own bytes) and is fine as-is.** No second stale *instruction* exists under any table spelling.

Out of the mandated sweep path, checked read-only and reported (not edited): `.ufo/waves/round-56/**` + `.ufo/reports` hold the same mentions as history (`R56GroundJournal.md:32,35,36,85,119`, `R56CritCurrency.md:7`, `R56DraftRows.md:86,96`, `R56DraftGate.md:16,83,95`, `R56GroundStd.md:107`, `R56GroundQcg.md:131`) — defect reports and fixes, no recheck instruction, so no append is owed there.

## 5. Findings (reported, not patched)

- **F1 — the round-56 wave report's 表 10 offsets do not reproduce; its 表7 offsets do.** `R56GroundJournal.md:36` prints "`表7` 13017 < `灰色文献` 13591 < `表8` 13653 < `表10` 14578" and `:35` prints "表10's title (char 22467)". On the committed raw at 26.08.0 this seat measures 13013 / 13591 / 13653 / 14566 (caption 14572) and the caption at 22539 (cross-reference at 22422). Neither a whitespace-collapsed (`14093`, `14134`) nor a whitespace-stripped (`12695`, `12731`) form yields 22467, so the source of those three numbers is not recoverable from committed bytes. The round-56 lesson row (`:11`) and this report's series are the reproducing ones — the L1 should cite `round-56.md:11`, not the wave report, if it quotes the series again. No append: round-56 records are history.
- **F2 — the entry's fact is unaffected.** The misattribution is a text-form artifact only: in file order the row sits after 表 10's caption and before 表8's caption, which is exactly what the correction's place rule states. No Observation, Inference or Unknown bullet needs change, so D1 is a one-line instruction defect (agreeing with the closure's "status-neutral" framing at `round-56-verifier-spotcheck.md:35`).
- **F3 — S129 is byte-backed on lane-owned bytes.** Both refetch attempts succeeded (rc 0, http 200) with identical raw `7a0b198c…` and `.txt` `beac2b7f…`, and the `.txt` digest equals the manifest pin, so the quote offsets a re-checker is told to use exist in bytes the lane commits. This seat does not compute C2's verdict.
- **F4 — no `Corrections (round 57)` block exists in this entry yet**, and the two exemplar shapes in-lane (`grey-literature-and-chinese-search-record-r40.md:35`, `source-type-taxonomy-r36.md:38`) both open with the append provenance and then keep the filed bullets standing; §3 follows that shape.

## 6. Bounds, tooling, scratch

- Writes: only this report. No lane edit, no `git`/`jj` mutation, no fetch (`curl`/`wget` unused), no fleet-root or shukuknow write, no counter or control builder touched.
- Tooling: **none installed or upgraded** (no pacman, no uv/npx); `pdftotext` 26.08.0 was already present and is the frozen recipe's tool.
- Scratch `/fast/scratch/hyaku/chousa-r57/R57W1ScribeD1/` (pdftotext outputs only, <2 MB) was deleted before this report was filed (`trap 'rm -rf -- "$S"' EXIT` honored on the final cell); `TMPDIR` pointed there.

VERDICT: drafted one append-only `#### Corrections (round 57)` block re-targeting the r42 recheck to 表7 (char 20520; row 22564; pdftotext series 13013 < 13591 < 13653 < 14566 re-measured) and swept all 10 `表 10`/`表10` hits — exactly one stale instruction survives in the lane (`grey-literature-field-china-r42.md:9`), the other nine are legitimate; survived.

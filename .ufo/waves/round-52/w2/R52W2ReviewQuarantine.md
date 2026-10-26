# R52W2ReviewQuarantine — wave-2 falsify: the quarantine claims

Reviewer seat, leaf, no subagents. Attacked: (1) the lesson's `## Quarantine slice` register
census (24 rows, one themed row), (2) the S120 verdict's three located quotes, (3) the round-51
`char 39411` verdict line the lesson calls an offset of nothing (`corpus/lessons/round-52.md`
Mistakes row 2; attacked text `corpus/lessons/round-51.md:88-89`).
Scratch `/fast/scratch/hyaku/chousa-r52/R52W2ReviewQuarantine` (TMPDIR exported there; removed
after). No tools installed (none needed). No network, no fetch; `/home/vgpnk/Projects/shokuknow`
read-only and its campaign tools never run (register read with awk/grep only); no git/jj calls;
nothing written outside this report and scratch.

## Attack 1 — the register slice: 24 rows, and which name a round-52 URL

Lesson claim: "The lane's register slice has 24 data rows (`awk` of section 10 over
`absent-defect-register.md`); one names a theme URL: S120."

Section-10 awk re-run verbatim from W1 `R52ExecQuarantine` §1:
```
$ R=/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/absent-defect-register.md
$ awk -F'|' -v l='chousa' '$2 ~ ("`" l "`") && $3 ~ /round[0-9]+/ && $4 ~ /S[0-9]+/ {print $4, $5}' "$R" | wc -l
24
```
The 24 rows, printed with register line numbers: 20 `payload-absent` rows at lines 37–56 (S077
S080 S082 S084 S086 S088 S093 S094 S095 S096 S104 S105 S108 S110 S111 S112 S114 S116 S120 S125)
plus 4 rows at lines 269–272 with ids `S100``–`S103`` (trailing backtick; source cell is a
`#### Gate` heading) whose class reads "the gate block named no locator, so no quote was checked".
So 24 = 20 absence rows + 4 never-checked rows — the awk output reproduces, but a reader taking
"24 data rows" as "24 absence rows" would over-read it; the lesson's number is real, its mix is
two classes (W1's 20/4 split, confirmed).

Which rows name the four round-52 URLs (S113 medsci, S114 chinagp, S115 NIPH, S116 lifescience
archive), any spelling — case-insensitive host tokens, then distinctive path/query tokens, then
the archive host:
```
$ grep -inE 'c2h\.niph|medsci|chinagp|lifescience' "$R"
55:| `chousa` | round5 | S120 | `payload-absent` | https://c2h.niph.go.jp/tools/system/Reporting_Format_Jap_202404.docx | `SRにおける…`<br>`文献検索終了時点は、…`<br>`ハンドサーチ等により…` | cited source, companion URLs and local artifacts were all checked; the quote is in none of them |
$ grep -inE '23e481c0052069d3|item185|Reporting_Format_Jap_202404|jpt_online|list_1\.pdf|show_article' "$R"
55:… (same single line)
$ grep -icE 'archive\.org' "$R"    → 2   (lines 102 `kengaku` S105 meti.go.jp, 116 `kotoba` S180 ai.google.dev — no chousa row, no round-52 URL)
```
http/https, trailing slash, `www.`, original-vs-archive all fold into the greped host/path
tokens: the medsci (`show_article.do?id=23e481c0052069d3`), chinagp (`item185.shtml`) and
lifescience (`jpt_online/prisma/list_1.pdf`, original and archive) URLs cannot be spelled without
one of them. Result: exactly one register line names a round-52 URL — line 55, S120, the NIPH
`.docx`. Counter corroborates the wiring:
`python3 corpus/evidence/round52/c2-count.py` → `QUARANTINE_VERDICTS=1/1 (S120)`,
`QUARANTINE_BLOCKED_ADOPTED=0`, `C2=PASS`.

**Verdict 1 — CONFIRMED.** 24 rows reproduce; S120 is the only slice row (only register line at
all) naming any of the four URLs; no sibling row is endangered.

## Attack 2 — the S120 verdict's three quotes at 8996 / 9020 / 9428

Lesson verdict block claims three quotes, once each, form capture-text, chars 8996 / 9020 /
9428. Re-located on the frozen capture with the C1 tool:
```
$ T=/home/vgpnk/Projects/shokunin/chousa-shokunin/tools/capture-text.py
$ C=/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache/3a8b45977cd111e45e3980a5.raw
$ python3 $T $C --locate 'SRにおける文献検索期間について明記する。'        → LOCATED count=1 offset=8996  exit=0
$ python3 $T $C --locate '文献検索終了時点は、分析枠組みが決定された後から製造販売業者による分析提出までの一時点に決める。'  → LOCATED count=1 offset=9020  exit=0
$ python3 $T $C --locate 'ハンドサーチ等により未公表データを収集した場合は、そのことを上記のフローチャートに含める。'      → LOCATED count=1 offset=9428  exit=0
```
Independent recount through the tool's stdout (not `--locate`'s own report):
```
$ python3 $T $C | python3 -c '…count each quote…'  → chars 19682 ; q1 1 ; q2 1 ; q3 1
```
Coherence: q1 is 21 chars, the context runs `…明記する。なお、…`, and 8996+21+3 = 9020 = q2's
offset; q2 is 48, q3 is 45 chars — each ≤160 chars, one whitespace word, inside the located-quote
rule. The `present` verdict stands on its stated form.

**Verdict 2 — CONFIRMED.** All three offsets, counts and the 19,682-char form reproduce; nothing
to break.

## Attack 3 — round-51's `char 39411` is an offset of nothing

Attacked text (`round-51.md:89`): `SRにおける文献検索期間について明記する。→ char 39411 → form
.raw unzipped → word/document.xml UTF-8`. Lesson Mistakes row 2 says the sentence is split across
runs and does not occur contiguously there. Probe:
```
$ unzip -p $C word/document.xml | python3 -c '…finds on the decoded XML…'
xml_chars 1379262
find_sentence -1                      # full sentence: no contiguous occurrence
first10 'SRにおける文献検索'
find_first10 -1   count_first10 0     # even its first 10 characters: absent
tail_run_find 459145                  # the tail run 文献検索期間について明記する。 exists, at 459145
sr_run_find 449648                    # the leading <w:t>SR</w:t> run sits 9,497 chars earlier — split across runs
at_39391_39461 '="003A0822"><w:rPr><w:rStyle w:val="a3"/><w:noProof/></w:rPr><w:t>治療効果'
```
Offset 39411 lands inside a `rPr`/style attribute block of an unrelated `治療効果` paragraph,
410,237 characters before the sentence's first run; neither the sentence nor its first 10
characters occur contiguously anywhere in that XML. The round-51 `present` verdict itself
survived (the quotes are in the document — attack 2) but its stated offset pointed at nothing,
exactly as Mistakes row 2 records, and the round-52 block's `form capture-text` offsets are the
repair.

**Verdict 3 — CONFIRMED.** `char 39411` is an offset of nothing in its stated form; find = −1 for
the sentence and its first 10 chars; the split-across-runs explanation is visible at runs
449648 / 459145.

## Residual risk / verification gaps
- "Any spelling" in attack 1 is my byte-token coverage (hosts, path/query segments, archive host)
  plus W1's normaliser fold (percent-decode, scheme/`www.`/trailing-slash, query order,
  `R52ExecQuarantine` §6) which I did not re-run; a percent-encoded host would evade my grep but
  not that normaliser. Residual: a URL spelled with an unrelated host plus only the path is
  covered; one with neither token nor path segment is not constructible for these four URLs.
- `--locate` count and my stdout recount share the one landed reader; W1's cross-reader
  (`build-spans.py:docx_text`, identical 19,682) is cited, not re-run here.
- The lesson's "24 data rows" mixes 20 absence rows with 4 never-checked rows (S100–S103); true
  as an awk count, but the lesson text does not spell out the mix.

VERDICT — attacked the round-52 quarantine slice's three claims (24-row register re-derivation
and themed-row set, S120's three capture-text quote offsets, round-51's char 39411) and broke
none: 24 rows and the lone themed row S120 reproduced, all three quotes LOCATED exactly once at
8996/9020/9428 in the 19,682-char form, and 39411 confirmed an offset of nothing (find −1,
sentence split across runs 449648/459145).

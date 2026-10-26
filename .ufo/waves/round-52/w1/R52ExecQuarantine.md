# R52ExecQuarantine — quarantine slice (round 52, w1)

Leaf executor. Read-only on lane, staged package and `/home/vgpnk/Projects/shokuknow`; no campaign
tool run, no git/jj mutation, no network, nothing installed. Scratch `/fast/scratch/hyaku/chousa-r52/R52ExecQuarantine`
(`mkdir -p`, `TMPDIR` exported there, removed at the end).
## 1. Register census (chousa rows)
```
$ R=/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/absent-defect-register.md
$ awk -F'|' -v l='chousa' '$2 ~ ("`" l "`") && $3 ~ /round[0-9]+/ && $4 ~ /S[0-9]+/ {print $4, $5}' "$R" | wc -l
24
$ awk -F'|' -v l='chousa' '$2 ~ ("`" l "`") && $3 ~ /round[0-9]+/ && $4 ~ /S[0-9]+/ {n++; if ($4 !~ /S[0-9]+/) bad++} END {print "rows="n" no_sid="bad+0}' "$R"
rows=24 no_sid=0
```
All 24 lines carry an S-id. Round/class spread (`… | sort | uniq -c`): round1 5, round2 5, round3 4
`payload-absent` + 4 "the gate block named no locator", round4 4, round5 1, round6 1 — every one of
those `payload-absent`. So the surface is 20 `payload-absent` rows (the register's own
`| \`chousa\` | 20 |`, register:238) plus 4 never-checked rows S100–S103, whose source cell reads
`#### Gate — S100` (a heading, not a URL) and whose id cell carries a trailing backtick (`` S100` ``)
— the awk test matches them because it tests `S[0-9]+`, unanchored.
## 2. The S120 row in full (register:55)
```
| `chousa` | round5 | S120 | `payload-absent` | https://c2h.niph.go.jp/tools/system/Reporting_Format_Jap_202404.docx | `SRにおける文献検索期間について明記する。`<br>`文献検索終了時点は、分析枠組みが決定された後から製造販売業者による分析提出までの一時点に決める。`<br>`ハンドサーチ等により未公表データを収集した場合は、そのことを上記のフローチャートに含める。` | cited source, companion URLs and local artifacts were all checked; the quote is in none of them |
```
Class cell `payload-absent` — the fabrication class ("every relevant source fetched cleanly and the
quote is in none of them … correct the quote or refuse the row", register:15). The row says all
three quotes are absent from the cited source, its companion URLs and the lane's local artifacts.
## 3. Locating the three quotes in the .docx text form
Capture identity by the cache-key rule (`sha256(url)[:24]`):
```
$ printf '%s' 'https://c2h.niph.go.jp/tools/system/Reporting_Format_Jap_202404.docx' | sha256sum
3a8b45977cd111e45e3980a55da17b3587d7055a1e3d2d4446e261f5f153aee4  -
$ file .qcache/3a8b45977cd111e45e3980a5.raw  ->  Microsoft Word 2007+
$ unzip -l …raw | head -4  ->  1464476  word/document.xml  (_rels/.rels officeDocument target)
```
Text form = the `.raw` through the C1 tool; offsets are code points in that form:
```
$ python3 tools/capture-text.py <raw> --locate '<quote>'
SRにおける文献検索期間について明記する。                     LOCATED count=1 offset=8996   exit=0
文献検索終了時点は、…一時点に決める。                        LOCATED count=1 offset=9020   exit=0
ハンドサーチ等により未公表データを…含める。                  LOCATED count=1 offset=9428   exit=0
$ python3 tools/capture-text.py <raw> | python3 -c 'import sys; print(len(sys.stdin.read()))'
19682
```
All three are present, exactly once each; 21 / 48 / 45 chars, 1 whitespace word each (≤25 words,
≤160 chars). Context at 8970 (`repr`, `\n` = a `w:p` end):
```
'…解釈をするのか記載する。\nSRにおける文献検索期間について明記する。なお、文献検索終了時点は、分析枠組みが決定された後から製造販売業者による分析提出までの一時点に決める。\n\n･ システマティックレビューのリサーチクエスチョン\n…'
```
They are live `w:t` text: the rule drops `mc:Fallback`, `w:delText`, `w:instrText` and `w:pPr/w:tabs`,
and the spans survive it, so they are not fallback or deleted content. Raw XML form (`unzip -p …
word/document.xml`, Python `str.find`): `count=0 find=-1` for all three, because Word splits the
sentence across runs — at XML offset 459144 it reads
`<w:t>SR</w:t></w:r><w:r …><w:t>における</w:t></w:r><w:r …><w:t>文献検索期間について明記する。`,
so a byte search on the XML is the wrong form. Why round 5 flagged it (`.txt` = the zip as text):
```
$ python3 -c "t=open('…3a8b45977cd111e45e3980a5.txt',encoding='utf-8',errors='replace').read(); print(len(t), t.count('\ufffd'), '文献検索期間' in t)"
168952 72117 False
```
72117 U+FFFD and `文献検索期間` absent — the round-51 "NIPH zip-member form" defect, reproduced.
Cross-reader check with the C2 counter's own reader (`build-spans.py:docx_text`, imported read-only):
```
builder chars 19682 tool chars 19682 identical True ; builder key(url) 3a8b45977cd111e45e3980a5 ; builder find(quote1) 8996
```
## 4. Required emission
```
register S120 (round5) verdict: present
SRにおける文献検索期間について明記する。	char 8996	form capture-text
文献検索終了時点は、分析枠組みが決定された後から製造販売業者による分析提出までの一時点に決める。	char 9020	form capture-text
ハンドサーチ等により未公表データを収集した場合は、そのことを上記のフローチャートに含める。	char 9428	form capture-text
```
Verdict line, then one line per quote the row claims absent (byte-exact quote, `char <offset>`,
`form capture-text`; the form is the `.raw` through `tools/capture-text.py <raw>`). Each offset is
that form's `text.find(quote)` and `--locate` reports `count=1`, so each occurs exactly once.
## 5. Counter wiring for this verdict (replayed, not guessed)
`c2-count.py` builds `reg_ids` from register rows whose first source URL normalises to a theme URL,
and parses verdicts from `corpus/lessons/round-52.md` via `VERDICT_RE`. Replaying its own code
(`url_of`, `DOCS`, `ALIASES`, `VERDICT_RE`) in scratch against the register and the line above:
```
reg_ids: {'S120': 'https://c2h.niph.go.jp/tools/system/Reporting_Format_Jap_202404.docx'}
verdicts: {'S120': 'present'}  blocked: 0
QUARANTINE_VERDICTS=1/1 (S120)
```
`present` clears both counts; `fabricated`/`unverifiable` there would set `blocked=1` and fail C2,
the NIPH URL being a bound document. The line must land in `corpus/lessons/round-52.md` (not a
report) for the counter to read it — L1 owns that write. Counter as run now:
`QUARANTINE_VERDICTS=0/1 (S120)`, `QUARANTINE_BLOCKED_ADOPTED=0`.
## 6. Does any OTHER row name the theme URLs under another spelling?
Every URL in the register normalised (lowercase, NFKC, percent-decode, scheme and leading `www.`
dropped, trailing slash dropped, query pairs sorted) against the five theme URLs (NIPH, lifescience
original + archive, medsci, chinagp):
```
theme URLs compared: 5 ; register lines scanned: 375
(55, 'niph', 'EXACT-NORMALISED', 'https://c2h.niph.go.jp/tools/system/Reporting_Format_Jap_202404.docx')
HITS: 1
```
One hit only — S120 itself. Byte corroboration (`grep -c`): `medsci 0  chinagp 0  lifesci 0
Medsci 0  梅斯 0  全科 0`; 125 distinct hosts, none `medsci.cn` / `chinagp.net` / `lifescience.co.jp`.
A spelling cannot dodge both tests: http/https, slash, `www.`, query order and case are folded by
the normaliser, and any surviving spelling (archive copy, encoded path) still carries the domain
token the byte grep counts at 0. **No other slice row names a medsci, chinagp or lifescience URL**,
original or archive — no cross-slice alias needed, no sibling row endangered by round 52.
## 7. Risks / notes for the L1
The row's class is wrong and it is the fabrication class: do not inherit "quote is in none of them",
and never copy a `.docx` `.txt` sidecar (72117 U+FFFD here — the same failure for any archived
`.docx`). Build the NIPH span from the capture-text form (8996 / 9020 / 9428), never from the XML
or the `.txt`. S100–S103 are "never checked", not absent: keep the 20/4 split apart in any census.
Nothing was written outside this report; the counter's verdict line is left for the L1.

VERDICT — built: attacked the register's S120 `payload-absent` claim against the NIPH `.docx` in its
text form — all three quotes PRESENT exactly once (char 8996 / 9020 / 9428, count=1, form
capture-text; two independent readers agree on 19682 chars), the row's absence a `.txt`-sidecar
artifact (72117 U+FFFD), the themed chousa row set exactly {S120}, and no other slice row naming
medsci / chinagp / lifescience under any spelling (1 normalised hit, 0 byte hits).

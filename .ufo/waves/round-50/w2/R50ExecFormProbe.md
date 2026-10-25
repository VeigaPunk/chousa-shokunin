# R50ExecFormProbe — DECODE-FORM probe of the four captures

Attacks: the decode form of the four round-50 captures under `…/.ufo/waves/corpus-expansion-1/.qcache/` — S104 `001287c436f0e6b1d166ae8d`
(`.raw` is HTML), S105 `e3ca8f4fdd15420b80096a75`, S106 `28750bcdf5d36cd90a7709fb`, refused 教师 manual `275c79d45b1e9b0fd32cef93` — and every
offset the Gate derives from it: (a) census, (b) `pdftotext -layout` byte reproduction, (c) S104 `.raw` vs `.txt`, (d) five Gate `char N`
offsets per capture re-derived with `str.find`, plus the alternative decodes (`utf-8-sig`, `newline=None`) that round-49 spot-check defect 5
was about; and the check that polices this (`corpus/evidence/round50/decode-form-check.py`, QUALITY 76). Scratch `/dev/shm/chousa-r50-R50ExecFormProbe/`,
deleted. No install (pacman paused host-wide, untouched). No network; no capture written; lane untouched but this file.
## 1. (a) Text-form census — `probe_a.py`
```
capture                            bytes   chars    Han  CJK+punct  U+FFFD  BOM  CR    LF  U+00A0  U+200B  FF
S104 001287c436f0e6b1d166ae8d       5599    2288   1453       1647       0  no   0   111       0       0   0
S105 e3ca8f4fdd15420b80096a75      83384   38174  20192      22030       0  no   0  1944       0       0  57
S106 28750bcdf5d36cd90a7709fb      63869   30937  14639      15880       0  no   0  1930       0       0  65
REFUSED 275c79d45b1e9b0fd32cef93   22648    9914   5696       6243       0  no   0   518       0       0  17
```
`Han` = U+4E00–9FFF, U+3400–4DBF, U+F900–FAFF; `CJK+punct` adds U+3000–303F, U+FF00–FFEF. Every character count matches the lesson
(`round-50.md:47-49,51`); form feeds = pages (`pdfinfo`: 57/65/17). All four decode **strictly** under `utf-8` (no `UnicodeDecodeError`), so
`errors="replace"` (`build-spans.py:60`, `c2-count.py:115`) substitutes nothing; no capture starts with a BOM (first bytes `20 0a 20` /
`e7 9f a5` / `e5 90 8c` / `20 20 20`); no CR, U+00A0, U+200B or U+FEFF anywhere inside.
## 2. (b) The three PDFs reproduce byte for byte
```
$ pdftotext -v 2>&1 | head -1
pdftotext version 26.08.0
$ for k in e3ca8f4fdd15420b80096a75 28750bcdf5d36cd90a7709fb 275c79d45b1e9b0fd32cef93; do
>   pdftotext -layout $k.pdf - | cmp - $k.txt && echo BYTE-IDENTICAL; pdftotext -layout $k.raw - | cmp - $k.txt; done
BYTE-IDENTICAL  (×3, for `.pdf` input and again for `.raw` input; sha256 .pdf == .raw in all three)
```
The `.txt` of S105/S106/refused is exactly `pdftotext -layout` stdout, UTF-8, under poppler 26.08.0 — the form the lesson names. Named
limit: poppler-version-pinned; the lane records the `.txt` digest, not the extractor version.
## 3. (c) S104: `.raw` HTML vs `.txt`
```
$ python3 -c '…'      # needle 按合作者排除自引标准统计他引次数, len 16
raw  count 1  len(chars) 346919  offset 341683
txt  count 1  len(chars)   2288  offset    549
raw ctx: …<td …>其他</td><td …>(1)按合作者排除自引标准统计他引次数，<strong …>1</strong>元/篇次。(2)邮费、复印等。</td>…
txt ctx: … 其他 (1)按合作者排除自引标准统计他引次数， 1 元/篇次。(2)邮费、复印等。 \n 收费说明：…
```
The line occurs **once in each form** (char 549 of 2288; char 341683 of 346919; both read as UTF-8). The Gate's longer quote
`按合作者排除自引标准统计他引次数， 1 元/篇次` occurs **0× in `.raw`, 1× in `.txt`**: the spaces are the campaign extractor mapping each
tag to one space; the page has `次数，<strong>1</strong>元`. Deterministic, not sloppy — `html_to_text(.raw)` reproduces the `.txt` **byte for byte**:
```
$ python3 repro_s104.py    # html_to_text copied verbatim from quote-lint.py:515-523 (that tool was NOT executed)
raw bytes 352066  txt bytes 5599  reproduced bytes 5599  byte-identical: True
sha256 txt   67f6f2df8ce96d01673d8f2f740e663f55ed8324bbf804834562bf746740a1db
sha256 repro 67f6f2df8ce96d01673d8f2f740e663f55ed8324bbf804834562bf746740a1db
```
Chain, offline-reproducible: `.raw` → `utf-8`(replace) → `html_to_text` (strip script/style/comments, `br|/p|/div|/li|/tr|/h1-6` → `\n`, other
tags → `" "`, `html.unescape`, collapse `[ \t\xa0]+` → `" "`) → UTF-8 `.txt`. Grounding consequence: 15 of the 18 S104 Gate quotes are also
exactly once in the `.raw` at wholly different offsets (194→332651, 549→341683); the other 3 (char 380 `03 完成并审核 报告…`, char 422
`证明费 300 元/份…`, the long form at 549) exist **only** in the rendered `.txt`, so a re-reader grepping the HTML for them finds nothing —
the `.txt` digest, not the page bytes, pins them.
## 4. (d) Gate offsets re-derived, and the alternative decodes
All 55 rows of the lesson's located-quote table (`^\| S10[456] \| `.txt` UTF-8 \| (\d+) \| …$`), `t.find(quote)` on `open(…,"rb").read().decode("utf-8")`:
```
mismatched rows: 0 of 55          # stated offset == find, and t.count(quote) == 1, for every row
S104 194→194 211→211 246→246 268→268          (count=1 each)   delta_sig=0 delta_univ=0
S105  48→48 27587→27587 30661→30661 30738→30738 30745→30745    delta_sig=0 delta_univ=0
S106  83→83 22511→22511 22549→22549                            delta_sig=0 delta_univ=0
REFUSED char 8033 → find 8033, count 1 (教师可查看的报告单包括…去除本人)
all 55 Gate rows: offsets changing under utf-8-sig = 0, under newline=None = 0
```
**No capture starts with a BOM, so no offset changes and by nothing.** Positive control that the probe is not vacuous — same quote, S105
char 31063, on deliberately mutated scratch copies:
```
BOM prepended, read as utf-8      → 31064   delta +1
BOM prepended, read as utf-8-sig  → 31063   delta  0   (utf-8-sig silently absorbs it)
LF→CRLF, read as-is               → 32460   delta +1397 (== newlines before the quote)
LF→CRLF, read with newline=None   → 31063   delta  0
```
Round-49 spot-check defect 5 (an offset that moves under `utf-8-sig`) **does not recur**: the sensitivity exists, the exposure does not — 0/55 move.
## 5. Adjacent leg I had to settle: `spans.tsv`'s `offset` column
Not the quote offset: `build-spans.py:42,119` writes `start = max(0, off - CONTEXT)`, `CONTEXT = 80`, so the column is the span slice start
(−80 in the tail; clamped at the head, hence S105's 0 for the quote at 48, S104's 114 for 194); `c2-count.py:200-201` recovers the quote offset
as `int(offset) + span.find(quote)`. Verified independently:
```
spans rows: 55   SLICES_BAD=0 DIGESTS_BAD=0 QUOTE_NOT_IN_SPAN=0 SPAN_NOT_LONGER=0
recovered quote offsets: S104 15 distinct / S105 24 / S106 3 — superset of the SOURCES.md anchor chars (6/7/3, all in)
max quote words 9, max quote chars 108 (limits 25 / 160)
```
No predicate breach (the span **file** is the slice at the recorded offset). Residue, naming only: a column called `offset` holding a different
quantity than the lesson's `char N` misled two wave-2 seats before the design was read; `R50ReopenRowS105` flagged and retracted it — I confirmed
it on 55/55 rows, not four. Also: all 55 digests are `.txt` digests, so `build-spans.py`'s post-freeze CR-clipping branch (erratum item 3)
executes on **0/55** rows — no coverage here.
## 6. Defect found — `decode-form-check.py` passes a lesson that names no form

QUALITY 76's check is whole-file: `\bchar\s+\d+` finds an offset shape, `FORM` (line 19) a naming. Scratch fixtures:
```
m8_bare_table_no_form  # Gate-shaped table, bare numbers, NO form word anywhere
  → NO_OFFSETS / DECODE_FORM=PASS / rc=0
m3_negated             # "The capture is NOT `utf-8-sig` and NOT `.txt` UTF-8; offsets index the HTML char 549."
  → FORM_NAMED / PASS / rc=0
m6_wrong_form_named    # "Offsets index the `.raw` capture decoded as UTF-16LE." + char 549 (offsets are .txt)
  → FORM_NAMED / PASS / rc=0
m4_none                # "A quote sits at char 549 of the capture."
  → FORM_MISSING / FAIL / rc=1     (the check does fire when nothing matches)
```
`m8` is decisive and is **not** the peer's finding: `R50ExecWaveCheckLive.md` §5 showed a header carrying the bare phrase `decode form` passes;
`m8` carries no form token at all. It is the shape the lesson actually uses — the 55 offsets are **bare integers** in a table under
`| … | form | char offset | … |`, invisible to `\bchar\s+\d+`; the only `char N` tokens in `round-50.md` are 6 prose lines (`grep -c 'char [0-9]'` → 6).
So the lesson's `FORM_NAMED … DECODE_FORM=PASS` is not evidence for QUALITY 76; `m3`/`m6` add that a negation and a wrong form both pass. The
lesson's *substance* holds independently: 55/55 Gate rows carry `.txt` UTF-8 in the form cell, the three Re-opened rows name `.txt` UTF-8 with
character counts, and the 5 prose offsets are exact. Reproduced the peer's secondary too: a missing path raises uncaught `FileNotFoundError`, rc=1, not 2.

Draft fix — intended lane path `corpus/evidence/round50/decode-form-check.py`, NOT applied by this seat:
```python
# (1) drop the bare `decode form` alternative; (2) let the Gate's own offset shape count;
# (3) require the naming on the same line as an offset, so a stray form word elsewhere cannot pass.
FORM = re.compile(r"utf-?8-sig|UTF-16LE|`\.txt` (?:read as )?UTF-8|\.txt.{0,40}UTF-8", re.I)
OFFSET = re.compile(r"\bchar\s+\d+|\|\s*char offset\s*\|", re.I)     # the column header is an offset shape
# per line: if OFFSET.search(line) and not FORM.search(line) -> FORM_MISSING
```
## 7. What found nothing (so the negative is checkable)

- BOM / CR / U+FFFD / U+00A0 / U+200B / U+FEFF over the four `.txt` (§1, `probe_a.py`): **0** of each; strict `utf-8` decode: no exception.
- `utf-8-sig` and `newline=None` re-find over all 55 Gate offsets (§4): **0** changed, delta 0.
- `pdftotext -layout` vs `.txt`, `.pdf` and `.raw` input, three PDFs (§2): **3/3 byte-identical**; `.raw` == `.pdf`.
- Span slice / digest / quote-in-span / span-longer-than-quote, 55 rows (§5): **0** bad. Refused char 8033: `find` = 8033, count 1.

VERDICT: attacked the decode form of all four captures and the offsets derived from it — **survived** (0/55 offsets move under `utf-8-sig` or `newline=None`, no BOM, all three PDFs reproduce byte for byte, all 55 span slices exact) — **defect found** in `corpus/evidence/round50/decode-form-check.py`: it returns `FORM_NAMED`/`PASS` for a lesson naming no form at all when offsets are bare table numbers (m8), for a negated naming (m3) and for a wrong form named (m6), so the lesson's `DECODE_FORM=PASS` does not establish QUALITY 76.

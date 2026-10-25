# ReopenS103 — Round 49 W2 falsify: re-open lane row S103 (CNKI AI guide, library.um.edu.mo PDF)

Leaf seat ReopenS103. No subagents, no background jobs, no production edits (only this report). No
installs (`RULES.md` read; pacman paused host-wide; `python3`/`pdfinfo` present). Scratch
`/dev/shm/chousa-r49-ReopenS103/` with `TMPDIR` exported there, removed at end. Lane checkout
`chousa-shokunin` at `87e93353d0…` (only `LOG.md` modified + untracked wave files); measured code in
`measure-after.txt` is `4ce61fc59e…`. Item: `corpus/SOURCES.md:113`; `spans.tsv:26-29`; `quotes.tsv:26-29`; `lessons/round-49.md:101-104`;
cited by `corpus/knowledge/citation-count-semantics-r37.md:7,35-38,55-57`.

## (1) Span rows — key, digest, form, exact slice, exactly-once

`verify.py` (condensed from the verbose run; labels abbreviated; `fb` = the file's raw bytes):

```python
import hashlib, pathlib
LANE = pathlib.Path("/home/vgpnk/Projects/shokunin/chousa-shokunin"); CACHE = pathlib.Path("/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache")
URL = "https://library.um.edu.mo/upload/databases/c1b0fa89e2809581b12c79b9c60ea1af.pdf"; k = hashlib.sha256(URL.encode()).hexdigest()[:24]
txt, raw = CACHE/f"{k}.txt", CACHE/f"{k}.raw"; d_txt, d_raw = (hashlib.sha256(p.read_bytes()).hexdigest() for p in (txt, raw))
for l in (LANE/"corpus/evidence/round49/spans.tsv").read_text(encoding="utf-8").splitlines():
    if not l.startswith("S103\t"): continue
    sid, url, dig, off, sf, quote, entry = l.split("\t"); fb, form = None, None
    if dig == d_txt:   form = txt.read_text(encoding="utf-8", errors="replace"); fb = txt.read_bytes()
    elif dig == d_raw: fb = raw.read_bytes(); form = fb.decode("utf-16le", errors="replace")
    else: print("DIGEST_MISMATCH", dig); continue
    span = (LANE/"corpus/evidence/round49"/sf).read_text(encoding="utf-8"); s = int(off); n = len(span)
    print(sf, form[s:s+n] == span, fb.decode("utf-8","replace")[s:s+n] == span, form.count(quote),
          quote in span, n > len(quote), len(quote), len(quote.split()), s+span.find(quote))
```

```
KEY 02aefcf570a7108e699d0990
TXT_DIGEST 32a5907e701fadee0138ba71899090c5b68848075ad34c9564d893c99c6dd616
RAW_DIGEST efc216d4b2df006674aaeef579167aa6841ed27daf0ba78db2da8a30b66b00a7
spans/S103-1.txt off=812 span_len=184 slice_eq=True bytes_eq=True quote_count=1 span_has_quote=True span_longer=True qlen=24 qwords=3 pos=80 abs=892
spans/S103-2.txt off=873 span_len=165 slice_eq=True bytes_eq=True quote_count=1 span_has_quote=True span_longer=True qlen=5  qwords=1 pos=80 abs=953
spans/S103-3.txt off=879 span_len=163 slice_eq=True bytes_eq=True quote_count=1 span_has_quote=True span_longer=True qlen=3  qwords=1 pos=80 abs=959
spans/S103-4.txt off=3095 span_len=177 slice_eq=True bytes_eq=True quote_count=1 span_has_quote=True span_longer=True qlen=17 qwords=1 pos=80 abs=3175
```

Key recomputes; the recorded digest is the `.txt`'s (the `.raw` is the 6,550,066-byte PDF `%PDF-1.7`,
36 pages — UTF-16LE branch correctly unused); every span is an exact slice at the recorded offset in
both decoded text and raw bytes; every quote occurs exactly once; every span is longer than its
quote; 4 rows for 4 quotes. **Leg holds.**

## (2) Registry row `corpus/SOURCES.md:113` (11 cells, parses clean)

`anchor`: `section 2.1 文献溯源模式 and the result-ordering note (capture .txt); located quotes
char 892, char 953, char 959, char 3175`. Recompute against the `.txt` form (`anchor.py`):

```
anchor chars [892, 953, 959, 3175] quotes 4
char 892: form[892:916]==quote -> True  'CNKI AI 根据相关文献，生成可信增强回答。'  full_count=1
char 953: form[953:958]==quote -> True  '来源数据库'  full_count=1
char 959: form[959:962]==quote -> True  '引用量'  full_count=1   char 3175: form[3175:3192]==quote -> True  '相关度、发表时间、被引次数和下载量'  full_count=1
all chars are quote offsets: True n_match: True
heading 2.1 文献溯源模式 at 774; heading 3.1.1 文献检索 at 3074 (21 chars before span start 3095)
```

Every `char N` is a located quote offset, in quote order — **holds**; `section 2.1 文献溯源模式` is real (774).

`scope` — `CNKI AI's source-tracing mode and the per-source counters it exposes`: carried (§2.1 lists
`文献的标题、摘要、作者、出版日期、文献来源、来源数据库、引用量以及下载` `\n\x0c量。`; page-break fold, `量。` 968-969).

`teaches` — first clause carried (`来源数据库、引用量以及下载\n\x0c量` at 953-970). The second clause is
carried **of a different surface**: `相关度` occurs exactly once in the 8,590-char capture, at 3175, in
**§3.1.1 文献检索** — "维度的检索功能…通过输入检索词完成查询，并按照…排序方式从高到低进行结果排序。检索结果
以每页 10 条…字段包括篇名、作者、来源、发表时间、数据库、被引次数和下载量"; `排序` has **zero** occurrences in
774-3000 (§2's range). That list's citation field is `被引次数` (3184, 3253), not the panel's `引用量`
(959 only). The semicolon clause thus reads as a property of the 溯源 mode while the capture attaches
it to the retrieval selector; the landed row also drops the locator W1 drafted (`GroundS104.md`:
"`3.1.1 文献检索` → `char 3175`"). **Narrower/mis-attached.**

`source` (same row, outside the two named cells) — `中国知网AI使用指南 — 澳門科技大學圖書館 — <url>`:
**not carried and contradicted by the URL host.** 0 occurrences of `澳門`/`科技大學`/`圖書館`/
`University`/`Macau` in the `.txt`; `pdfinfo` on the `.raw` → `Title:` empty, `Author:
WUZHAOXUAN`, `Creator: WPS 文字`, `CreationDate: 2025-02-21`, 36 pages. `library.um.edu.mo` is
University of Macau (澳門大學); 澳門科技大學 is `must.edu.mo`. The round's own dispatches call this
document "S104 UMacau CNKI AI guide" (`w1-dispatch.json:150`, `w1-spec.json:65`, `w2-spec.json:50`).
Inherited verbatim from `shokuknow/merge/chousa/SOURCES.append.md:28`; `GroundS104.md` repeated it
unexamined ("Context: … 澳門科技大學圖書館 copy").

## (3) Every `citation-count-semantics-r37.md` sentence citing S103

| line | sentence | verdict |
|---|---|---|
| 7 | `source: S103 — <url> — section 2.1 and the result-ordering note — capture 2026-10-23, re-opened 2026-10-25` | §2.1 **supported** (774); "the result-ordering note" **narrower** — it is §3.1.1 文献检索 (3175), unnamed; the date is process, and I did re-open it today |
| 35 | `**A library guide to CNKI's AI answer mode (Chinese).**` | **narrower** — the capture is CNKI's own manual (`CNKI AI 使用指南 / CNKI AI User Guide`, in-product URL `https://aismart.oversea.cnki.net` at char 63); "library" names the host, not the author. The `ground:` line ("a copy or a third-party guide") survives only via "a copy" |
| 36-37 | `In trace mode "CNKI AI 根据相关文献，生成可信增强回答。"` | **supported** — char 892, §2.1, verbatim, exactly once |
| 37-38 | `the traced-source panel shows fields including "来源数据库" and "引用量", and results can be ordered by "相关度、发表时间、被引次数和下载量" (S103).` | fields **supported** (953, 959 in the §2.1 panel list); ordering **not supported as attached** — verbatim but §3.1.1's retrieval list, whose citation field is `被引次数`; the panel's 引用量 is never a stated sort key |
| 55-57 | `S103's trace mode says "CNKI AI 根据相关文献，生成可信增强回答。" and shows "来源数据库" beside "引用量"` | **supported** — 892; 953/959 are consecutive cells of `文献来源、来源数据库、引用量以及下载` `\n\x0c量` |

Nothing fabricated, no quote misquoted; one clause attached to the wrong surface, one provenance label loose.

## (4) Quote against context

- 892: span S103-1 shows §2.1's two-region description — consistent. 953/959: the spans show the panel
  field list `标题、摘要、作者、出版日期、文献来源、来源数据库、引用量以及下载量` — consistent (thin: 5- and
  3-char anchors, legal under the frozen ≤25-word/≤160-char leg).
- 3175: span S103-4 opens `维度的检索功能，支持以主题、篇关摘、关键词等维度进行检索…用户可通过输入检索词完成查询…
  检索结果以每页 10 条…`. The span's context says **检索**, not the 溯源 panel: the span is honest, the
  sentence carrying it is not. The §3.1.1 header sits 21 chars before the span start (3074 vs 3095),
  just outside the 80-char context, so a span-only reader sees retrieval wording, not the section.

## Adjacent observations (recorded, nothing changed)

- `lessons/round-49.md:161` (and `:158`) put `corpus/knowledge/chinese-search-log-r37.md` in S103/S102
  `used-by`; that file **does not exist in the lane** (`find corpus -name '*chinese-search*'` → nothing;
  no such path in lane history) — it is a staged, unadopted entry (`merge/chousa/knowledge/corpus/
  knowledge/chinese-search-log-r37.md:5`). The landed registry rows list only the citation entry: the c2
  binding leg is unaffected, the lesson's used-by table overstates the adoption.
- `GroundS104.md` closed "all staged claims resting on the row supported" while itself noting the
  §3.1.1 location; the landed entry kept the merge and lost the locator — a W1 calibration miss.

## Tooling / scratch

No installs or upgrades. Scratch files (`verify.py`, `anchor.py`, `dump.py`, `win*.py`) under
`/dev/shm/chousa-r49-ReopenS103/` with `TMPDIR` pointed there, removed (`SCRATCH_REMOVED`); no
network — only the read-only `.qcache` capture `02aefcf570a7108e699d0990.{txt,raw}` was opened.

VERDICT: S103 registry row + spans — partly — the four span legs (key, digest, exact slice, exactly-once) and all four anchor `char N` offsets hold exactly, but the `teaches` cell and entry lines 37-38 attach §3.1.1 文献检索's sort keys (被引次数) to the §2.1 trace panel (引用量), and the `source` cell's 澳門科技大學圖書館 attribution is absent from the capture and contradicted by the URL host and the round's own "UMacau" dispatch text.

# R51ExecCaptureForm — capture-form probe, seven C2 captures

Read-only probe of `/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache/` (key = sha256(url)[:24], re-derived and asserted per URL). No lane file touched; no counter run; no network. Scratch `/dev/shm/chousa-r51-R51ExecCaptureForm/` deleted at the end. Nothing installed.

## 1. Per-key form facts

`chars` = `len()` of the string `build-spans.form_texts` sees (`read_text(utf-8, errors="replace")`, i.e. universal newlines). Byte-level decode differs only for S119 (2065 chars, 390 CRLF collapsed) and S125 (168953, 1 CRLF collapsed). CJK = U+4E00–9FFF/3400–4DBF/F900–FAFF; kana = U+3040–309F/30A0–30FF/FF66–FF9D.

| lane | staged | key | .txt B | chars | CJK | kana | U+FFFD | .raw B | .raw first bytes |
|---|---|---|---|---|---|---|---|---|---|
| S109 | S107 | 7194acc65a18f6555e4b8893 | 36968 | 21216 | 2715 | 4603 | 0 | 713922 | `%PDF-1.6` |
| S110 | S108 | 62be15a474e866e4bef6c9d5 | 61188 | 39676 | 4641 | 5335 | 0 | 291615 | `%PDF-1.6` |
| S116 | S109 | fd468a36d78ff156b6200946 | 82903 | 52208 | 13880 | 0 | 0 | 1156890 | `%PDF-1.4` |
| S117 | S110 | c7266931a1731db3ff6ae77d | 69789 | 50952 | 8402 | 0 | 0 | 1140215 | `%PDF-1.4` |
| S119 | S111 | 42bac8830527d6f1bb125c49 | 2969 | 1675 | 427 | 0 | 0 | 20142 | `<!DOCTYP` (XHTML, strict UTF-8, 17996 chars) |
| S125 | S112 | 3a8b45977cd111e45e3980a5 | 319599 | 168952 | 319 | 3 | **72117** | 178056 | `PK\x03\x04\x14\x00\x06\x00` (docx zip, 21 members) |
| S126 | S113 | 34fcefc159bf2ebbd1e09540 | 47473 | 25811 | 3827 | 5940 | **40** | 7787275 | `%PDF-1.4` |

S125's 319 CJK / 3 kana are mojibake (see §3) — not document text. For the five PDF keys the `.pdf` twin is byte-identical to `.raw` (sha256 equal); nothing in the lane reads `.pdf`.

## 2. Is the `.txt` a lossless text decode?

* **Five PDFs — no, and correctly so: it is an extraction, not a decode.** `raw.decode("utf-8")` fails at byte 10 (binary container); `raw.decode("utf-16le")` is garbage. Instead the `.txt` is *character-identical to `pdftotext -layout <key>.pdf`* for all five (`cap==layout True`; default mode `False`). So every quote in those `.txt` forms is reproducible from the `.raw` with one standard command. Loss is confined to what poppler renders:
* **S126 — 40 chars unrecoverable.** U+FFFD sit contiguously at offsets **101–140**, immediately after `〈鍵概念〉` (ctx: `'雑誌 38（1），2023 60－69\n\n〈鍵概念〉\x08 '` + 40×U+FFFD). `pdffonts` lists two `PKOCVZ+YuMincho-Regular-90ms-RKSJ-H` CID subsets with `uni = no` (no ToUnicode); `pdftotext -raw` yields the same 40 → not recoverable by any poppler mode. Any quote overlapping 101–140 can never be located.
* **S119 — no: it is a rendering, not a decode.** `.txt` ≠ raw-as-UTF-8 and ≠ raw-as-UTF-16LE. It drops content and invents none: all 15 `.txt` lines ≥8 chars occur in the raw's script/style-skipped visible text (0 absent), while that visible text is 3527 chars vs the `.txt`'s 1675. Producer not reproducible here (lynx/w3m/html2text absent; a naive strip gives 3527 ≠ 1675).
* **S125 — yes, and that is the defect.** `.txt` is *exactly* `raw.decode("utf-8", errors="replace")` (`txt==raw_utf8replace: True`, head `PK\x03\x04`): a lossless **byte** decode of the zip, therefore zero document text — 42.7% of its chars are U+FFFD.

## 3. S125: which form carries `文献検索期間`, and how often

```
.txt read as UTF-8 ......................... 0
.raw decoded UTF-16LE (build-spans' form) .. 0
zip member word/document.xml, UTF-8 ........ 2   (1464476 B / 1379262 chars, offsets 459145, 479647)
```

Form rule of the located quote — the `.raw` opened as a zip, member `word/document.xml`, decoded UTF-8, `</w:p>` → `"\n"`, then tags removed by `re.sub(r"<[^>]*>", "", …)` and CR normalised to LF: 21829 chars, the quote occurs **exactly once at offset 10247** (10248 before CR normalisation). The neighbouring cell row reads `文献検索期間2015年1月から2018年10月まで` (form offset 10433), i.e. the form also carries the *value* example.

## 4. `build-spans` form rule, and whether it picks a usable form for each of the seven

`form_texts` (build-spans.py:33-46): form 1 = `.txt` read UTF-8 with `errors="replace"`; form 2 = `.raw` decoded **UTF-16LE** with `errors="replace"`. `build` picks `pick[0]` = the first form where `text.count(quote)==1` (build-spans.py:98-101), and records that file's sha256. Ran `form_texts` on all seven URLs:

```
S109 forms=2  .txt chars=21216 fffd=0        .raw chars=356879 printable_ascii=507  fffd=10686 tokens={}
S110 forms=2  .txt chars=39676 fffd=0        .raw chars=145762 printable_ascii=160  fffd=4489  tokens={}
S116 forms=2  .txt chars=52208 fffd=0        .raw chars=578281 printable_ascii=762  fffd=17787 tokens={}
S117 forms=2  .txt chars=50952 fffd=0        .raw chars=569953 printable_ascii=1827 fffd=16994 tokens={}
S119 forms=2  .txt chars=1675  fffd=0        .raw chars=10071  printable_ascii=0    fffd=0     tokens={}
S125 forms=2  .txt chars=168952 fffd=72117   .raw chars=89007  printable_ascii=200  fffd=2755  tokens={}
S126 forms=2  .txt chars=25811 fffd=40       .raw chars=3893585 printable_ascii=2502 fffd=5471 tokens={}
   (tokens = PubMed|Cochrane|MEDLINE|J-STAGE|SinoMed|systematic review|Systematic Review|文献検索期間|検索式)
```

* **Six of seven: usable.** `.txt` is first and real; each of my six quotes is picked from `.txt` (`count==1`, §6). The UTF-16LE fallback is inert for them: ≤0.2% printable ASCII, 0 token hits, and 0 of the 3 duplicated ≥12-char lines in any PDF `.txt` matched the `.raw` form (so a twice-occurring quote is refused, not silently rescued).
* **S125: cannot.** Both forms are non-text. A real quote is refused — `build-spans: refused S125: quote not exactly once in any form (…txt:0x, …raw:0x)` (exit 1) — while a **binary string from the byte dump is accepted**: quote `D2397;ud|:` (`count_in_txt 1`) produced `SPANS row S125 … 1920 spans/S125-1.txt` with a span of compressed bytes. The `.txt` of S125 can therefore mint evidence no document contains; the `.raw`-as-UTF-16LE form cannot (0 printable ASCII).

## 5. Smallest change (zip case) — and does the `.txt` already suffice?

No: for S125 the `.txt` is the zip's own bytes, so a change **is** required; for the other six no change is needed. Smallest change is inside `form_texts`, one extra form for a zip `.raw` (needs `io`, `zipfile`; `re`/`hashlib` already imported):

```python
    if raw.is_file():
        b = raw.read_bytes()
        out.append((b.decode("utf-16le", errors="replace"), hashlib.sha256(b).hexdigest(), raw.name))
        if b[:4] == b"PK\x03\x04":
            with zipfile.ZipFile(io.BytesIO(b)) as z:
                xml = z.read("word/document.xml").decode("utf-8")
            text = re.sub(r"<[^>]*>", "", xml.replace("</w:p>", "\n"))
            out.append((text.replace("\r\n", "\n").replace("\r", "\n"),
                        hashlib.sha256(b).hexdigest(), raw.name + "!word/document.xml"))
```

Verified on a scratch copy (`patched.py`, lane file untouched): `form count of quote: [('…txt', 0), ('…raw', 0), ('…raw!word/document.xml', 1)]`, `build` accepts at `chars[0]=10247`, span contains no CR; the six `.txt` quotes are unchanged (`S109 spans/S109-1.txt 453`, `S126 spans/S126-1.txt 12099`). CR normalisation matters because the derived name does **not** end in `.raw`, so the round-49 CR-clipping branch (build-spans.py:132-141) is skipped and a bare CR would make `check()` report `SPANS_FILE_STALE`. The tag-strip is minimal but glues adjacent cells (`</w:tc><w:tc>` → no separator), so a quote spanning a cell boundary would be locatable but not textually contiguous — acceptable for locating, must not be presented as prose.

## 6. Located quotes (one per capture; form stated; byte-exact)

| staged id | url | form | offset | chars/words | quote |
|---|---|---|---|---|---|
| S107 | https://www.jstage.jst.go.jp/article/kenkokyoiku/32/2/32_320208/_pdf/-char/ja | `.txt` UTF-8 | 533 | 39/1 | `検索式の作成，採択・除外基準の定義，データの抽出と管理，論文の質の評価，そして` |
| S108 | https://jaohfa.com/pdf/systematic_review.pdf | `.txt` UTF-8 | 36833 | 40/1 | `・検索ワードや検索式は実際に使用した、もしくはそれと同等の詳細なものであること。` |
| S109 | https://www.slarc.org.cn/dwyx/EN/article/downloadArticleFile.do?attachType=PDF&id=5290 | `.txt` UTF-8 | 15240 | 32/3 | `检索词及逻辑关系（结合 MeSH/Emtree 主题词与自由词）` |
| S110 | https://www.slarc.org.cn/dwyx/CN/article/downloadArticleFile.do?attachType=PDF&id=5237 | `.txt` UTF-8 | 11211 | 22/1 | `检索中国知网、万方、中国生物医学文献数据库、` |
| S111 | https://www.sinomed.ac.cn/article.do?ui=2026335073 | `.txt` UTF-8 | 829 | 46/1 | `文献检索是系统评价(SR)的基石,但其报告质量长期存在不足,严重影响研究的透明度与可重复性。` |
| S112 | https://c2h.niph.go.jp/tools/system/Reporting_Format_Jap_202404.docx | `.raw` zip member `word/document.xml`, UTF-8, tags stripped, CR→LF | 10247 | 72/1 | `SRにおける文献検索期間について明記する。なお、文献検索終了時点は、分析枠組みが決定された後から製造販売業者による分析提出までの一時点に決める。` |
| S113 | https://www.jahbs.info/journal/pdf/vol38_1/vol38_1_5.pdf | `.txt` UTF-8 | 12179 | 23/1 | `検索した日，検索キーワードと検索式，検索件数を` |

All seven: `text.count(quote)==1` in the named form, ≤160 chars, ≤25 whitespace words. S112's quote is the only one that needs the §5 change; under the current rule it is refused (0x in both forms).

## 7. Risks for the entries/manifest

* Offsets are character offsets in the newline-normalised `.txt`, not byte offsets: S119 shifts by 390 (CRLF) if a verifier decodes bytes.
* S126's key-concept line (`〈鍵概念〉`, offsets 101–140) is unrecoverable; do not build an entry predicate on it.
* A pre-patch S125 span row carries `capture_sha256` of the `.raw` with an offset in the byte-dump form — meaningless as document coordinates; any such row must be rebuilt after the change.
* `.pdf` twins duplicate `.raw` (5 keys); no reader uses them, so they are not a second form.

VERDICT: probed all seven captures — six `.txt` forms are genuine text (five provably `pdftotext -layout`, one HTML rendering; S126 irrecoverably loses 40 glyphs at 101–140), and the S125 `.docx` capture has **no** text form at all (`.txt` is the zip's own bytes, 72117/168952 U+FFFD), so `build-spans` refuses the real sentence while accepting a binary string from the dump; a one-branch `form_texts` zip extraction fixes it and was verified in scratch to locate `文献検索期間` at 10247 with the six other quotes unchanged.

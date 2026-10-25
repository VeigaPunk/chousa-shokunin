# ReopenS102 — W2 falsify: lane row S102 (CNKI KNS8.0 利用ガイド, 東方書店)

Attacked: the S102 row — its three span rows, its Registry row, every entry sentence citing S102, and quote/context fit. Lane checkout `/home/vgpnk/Projects/shokunin/chousa-shokunin` (`git rev-parse master` = `87e93353d046f2d7e4f0d2f5d3b87b7008a64ef0`; `corpus/SOURCES.md` last touched by adoption `1254ab26`, 2026-10-25 17:20:44 -0300). Captures read only from the campaign cache; no fetch. Scratch `/dev/shm/chousa-r49-ReopenS102` (deleted).

## 1. Span rows replayed (`spans.tsv:23-25`)

Key recomputed from the URL as written in the row: `sha256(url)[:24]` = `7809d5114330a60527436b07` → `.txt`/`.raw`/`.pdf` exist in `.qcache`. The recorded `capture_sha256` is a FILE digest and it is the `.txt`'s, not the `.raw`'s (`.raw` and `.pdf` are byte-identical, `%PDF-1.7`, 5 066 141 B, digest `f701f59d…`), so the form is `.txt` decoded UTF-8 — strict decode OK, 17 317 chars, 0 U+FFFD (offsets stable under the counter's `errors="replace"` read).

Script (`/dev/shm/chousa-r49-ReopenS102/verify.py`, abridged to the executed body):

```python
rows = [r.split("\t") for r in (ev/"spans.tsv").read_text().splitlines()[1:] if r.startswith("S102")]
for sid,url,digest,off,spanf,quote,entry in rows:
    k = hashlib.sha256(url.encode()).hexdigest()[:24]
    txt, raw = CACHE/f"{k}.txt", CACHE/f"{k}.raw"
    dt, dr = sha256(txt), sha256(raw)
    form = txt.read_text("utf-8") if dt == digest else raw.read_bytes().decode("utf-16le","replace")
    span = (ev/spanf).read_text("utf-8"); o = int(off); pos = o + span.find(quote)
    print(slice_ok := form[o:o+len(span)] == span, span == quote, form.count(quote),
          span.count(quote), pos, form[pos:pos+len(quote)] == quote)
```

```
S102 rows: 3
spans/S102-1.txt key=7809d5114330a60527436b07 digest_txt=e9f66647ee5fb0fc digest_raw=f701f59d95386671 form=.txt digest_match=True
  off=13180 len_span=174 len_quote=14 slice_eq_span=True span_eq_quote=False
  quote_occurrences: form=1 span=1 quote_abs_pos=13260 form[pos:pos+len(quote)]==quote -> True
spans/S102-2.txt ... off=13434 len_span=197 len_quote=37 slice_eq_span=True
  quote_occurrences: form=1 span=1 quote_abs_pos=13514 ... -> True
spans/S102-3.txt ... off=16043 len_span=189 len_quote=29 slice_eq_span=True
  quote_occurrences: form=1 span=1 quote_abs_pos=16123 ... -> True
```

Each span file is the exact char slice of the UTF-8 form at the recorded offset; each quote occurs exactly once in the form (offset unambiguous) and once in its span; each span is longer than its quote (174>14, 197>37, 189>29) — the span is not the quote, it carries the sentence the quote is cut from.

## 2. Registry row (`corpus/SOURCES.md:112`, 11 cells)

Anchors: `char 13260`, `char 13514`, `char 16123` are each the offset at which that id's quote begins in the capture form — `form[13260:13274]` = `「发表时间」「被引」「下载」`, `form[13514:13551]` = the gloss sentence, `form[16123:16152]` = the 引文网络 sentence, each re-checked `form[pos:pos+len(quote)] == quote -> True`. All three located. Section claim holds at the capture: `5.6.1 検索結果リスト` char 13226, `6.4 引文网络` char 16113.

Scope cell: "as a Japanese publisher's usage guide records them; … a third-party description, not CNKI's own documentation" — carried by the capture head `中国学術文献オンラインサービス ＣＮＫＩ利用ガイド KNS8.0 新 TOP ページ対応 / 株式会社東方書店 / 更新日：2025-06-17`. No over-claim.

Teaches cell, four clauses:
- "result list shows 发表时间, 被引 and 下载" — carried: 5.6.1 `検索結果には、「篇名」「作者」「刊名」「发表时间」「被引」「下载」の他、…一覧で表示されます。`
- "被引频次 is one of twenty 专业检索 searchable fields" — carried exactly: 5.4 `专业检索` at 12892, `【検索項目】` at 12939 enumerates 20 items ending `…第一单位、被引频次`, and the capture itself says `20 項目を検索対象とすることができます。`
- "described respectively as the publication date, the 被引用回数 and the download count" — carried in substance (`文献の公開時期、被引用回数、ダウンロード回数`), but "publication **date**" renders `公開時期` (period/timing), a narrowing.
- "the 引文网络 view presents … **as a graph**" — NOT carried lexically. 6.4 reads `当該文献を中心に年毎の参考、被引用の関係をビジュアルに提示、それぞれの文献にアクセスすることもできます。` — "visually presented". No `グラフ`/`グラフィカル` in 6.4; the capture's only such token, char 14890, is 5.6.4.2 `可视化分析`: `…分析結果がグラフィカルに表示されます。` This is an interpretive gloss of `ビジュアル`.

## 3. Entry sentences citing S102 (`corpus/knowledge/citation-count-semantics-r37.md`)

- `:6` source line "sections 5.6.1 and 6.4" — **supported** (headings 13226 / 16113).
- `:32-34` "glosses the result-list columns `「发表时间」「被引」「下载」` as `「下载」はそれぞれ文献の公開時期、被引用回数、ダウンロード回数を示します。`" — **supported**. Capture 13486-13551: `「发表时间」「被引」\n         「下载」はそれぞれ文献の公開時期、被引用回数、ダウンロード回数を示します。` The entry supplies the three column names and quotes the gloss from `「下载」`; `それぞれ` maps the three columns onto the three meanings, so the entry's reading is the capture's own, not a stronger one.
- `:34` "describes the citation-network view as `当該文献を中心に年毎の参考、被引用の関係をビジュアルに提示`" — **supported** verbatim; the entry stops at `提示` and the omitted continuation `、それぞれの文献にアクセスすることもできます。` adds no reversal. The entry does not repeat the registry's "graph" gloss — the adopted knowledge is the more conservative text.
- `:57` "S102 glosses citation and download counts as separate columns" — **supported** (5.6.1 lists `「被引」「下载」` as distinct columns; the gloss assigns each its own meaning).
- `:73` Unknown "whether the counted records in S100 or S102 apply its codes" — honest unknown; S102 carries a 被引 column but says nothing about 文献标志码, and the sentence claims nothing positive.

No S102 sentence in the entry is narrower than needed, and none asserts more than the capture carries.

## 4. Quote-vs-context

- 5.6.1: the gloss sentence is body text after the `「刊名」` explanation and a page break (`28`, `\x0c`); the section's first sentence names `发表时间/被引/下载` as result columns, so the quote is not lifted onto a different subject.
- `「下载」はそれぞれ…` starts mid-sentence; the dropped subject `「发表时间」「被引」は` lies inside span `S102-2` (offset 13434, 80 chars before the quote) and is restored in the entry's own clause. No inversion — but the quote column alone (spans.tsv / lesson) reads as if only `下载` were defined; a reader of the span file is not misled.
- 6.4: the quote is the section body under `6.4 引文网络`, followed by `6.5 参考文献` / `6.6 相关文献推荐` — consistent with the entry's "the citation-network view".

## Peripheral (outside the row; recorded for the closure)

- `corpus/lessons/round-49.md:158` gives S102 `used-by` = `…citation-count-semantics-r37.md, …chinese-search-log-r37.md`. `chinese-search-log-r37.md` does not exist in the lane (`ls corpus/knowledge | grep chinese-search` → no match; the only `source:` line for this URL anywhere is `citation-count-semantics-r37.md:6`). The value is the staged package's (`assimilation/adopt-final/stripped.tsv:17`). The SOURCES.md row is correct (cell 10 names only the one entry); the lesson ledger line is stale. W1 `ReviewProvince.md:46` already flagged this class for S101/S102.
- `corpus/lessons/round-49.md:156` marks the S102 recheck "180d — re-download the PDF … (ran 2026-10-23)": a 180-day recheck "ran" on the capture day, which is the campaign capture itself (`.txt` mtime 2026-10-23 20:37). Same-day self-check labelled as a recheck; the row's own `180d` cell is unaffected.

## Not run by me

The two counters, `inference-ground.py`, builds/lints and the git/jj gates belong to the parent's post-integration gate; this seat read lane bytes and the read-only capture only and wrote no production file.

VERDICT: S102 row (spans.tsv:23-25, SOURCES.md:112, citation-count-semantics-r37.md S102 sentences) — partly — the three spans, capture key/digest, all three `char N` anchors, the scope cell and every entry sentence hold exactly against the capture, but the teaches cell's "as a graph" (capture: `ビジュアルに提示`) and "publication date" (capture: `公開時期`) step past the capture text, and the lesson's S102 `used-by` names a non-existent entry.

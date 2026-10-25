# ReopenS096 — re-open lane row S096 (CiNii Research manual), round 49 wave 2

Item attacked: `S096 | https://support.nii.ac.jp/ja/cir/manual_articles_detail` — its 3
`spans.tsv` rows, its Registry row (`corpus/SOURCES.md:106`), and every sentence of
`corpus/knowledge/aggregator-vs-source-r36.md` that cites it. Frozen predicates untouched.

## (1) Span rows re-derived independently (not importing `build-spans.py`)

Command (script written to `/dev/shm/chousa-r49-ReopenS096/verify_s096.py`, deleted after;
core below, run from the lane checkout with `TMPDIR=/dev/shm/chousa-r49-ReopenS096`):

```
key=sha256(url)[:24]; for ext in .txt,.raw: digest=sha256(file); ext = .txt if digest==row.digest else .raw
form = bytes.decode('utf-8') if .txt else bytes.decode('utf-16le',errors='replace')
assert form[off:off+len(span_text)] == span_text and == span_bytes  # text and byte-exact
n=form.count(quote); qo=form.find(quote); assert n==1 and quote in span_text
assert qo in [int(x) for x in re.findall(r'char (\d+)', registry_anchor_cell)]
```

Observed output:

```
CAPTURE_KEY sha256(url)[:24]=09fc63de41f293d43d631c46
  FILE 09fc63de41f293d43d631c46.txt bytes=12901 sha256=374d7dacf95c69cb58c6b85524c16eb638ee69c225effa4c207861821a762774
  FILE 09fc63de41f293d43d631c46.raw bytes=41404 sha256=5ce63212fe0047977feabffecc9a1030e6264f7938d56084741f3d9261449ef9
REGISTRY anchor_cell='section G 参考文献／被引用文献, the two 注意書き notes (capture .txt); located quotes char 3599, char 3707, char 3752'
REGISTRY anchors=[3599, 3707, 3752] row_cells=11
== spans/S096-1.txt offset=3519  FORM .txt (digest matches)  SLICE form[3519:3725]==span_file: True (byte-exact True) len=206
   QUOTE occurrences_in_form=1 quote_offset=3599 in_span=True span_longer=True  chars=46 words=2  ANCHOR char 3599 OK
== spans/S096-2.txt offset=3627  FORM .txt (digest matches)  SLICE form[3627:3825]==span_file: True (byte-exact True) len=198
   QUOTE occurrences_in_form=1 quote_offset=3707 in_span=True span_longer=True  chars=38 words=1  ANCHOR char 3707 OK
== spans/S096-3.txt offset=3672  FORM .txt (digest matches)  SLICE form[3672:3880]==span_file: True (byte-exact True) len=208
   QUOTE occurrences_in_form=1 quote_offset=3752 in_span=True span_longer=True  chars=48 words=4  ANCHOR char 3752 OK
UNMATCHED_REGISTRY_CHARS=[]  ROWS=3 FAILS=0  EXIT=0
```

All three legs hold: key, digest (the `.txt`'s, so the form is the UTF-8 `.txt`), exact slice
(text and bytes), single occurrence, quote in its span, span = quote ± 80 chars
(206/198/208 = 80+quote+80), every `char N` = a located quote offset.

Cross-check (`.txt` is no extraction artefact; the `.raw` leg is unusable):
`Q1: txt=1 raw_as_utf8=1 raw_as_utf16le=0` / `Q2: 1 1 0` / `Q3: 1 1 0`;
`raw utf16le sample at 25380: ''` (41404 bytes -> 20702 mojibake chars).

The capture's `.raw` is UTF-8 HTML (`file`: "HTML document, Unicode text, UTF-8"), so the
`form_texts` UTF-16LE branch yields 20702 chars of mojibake and 0 quote hits — the `.txt` is the
only valid form and the recorded digest is exactly it. (Minor docstring note: `build-spans.py`
line ~10 cites "(S095/S096 register rows)" as OLE `.doc`/UTF-16LE examples; *this* S096 is
HTML/UTF-8 and never takes that branch. Not a defect in the S096 row.)

## (2) Registry row (`corpus/SOURCES.md:106`)

- 11 cells, unique URL row (`grep -c manual_articles_detail corpus/SOURCES.md` = 1),
  `status=mined opened=2026-10-25 recheck=180d used-by=corpus/knowledge/aggregator-vs-source-r36.md`.
- Anchor cell: all three `char N` (3599/3707/3752) are located quote offsets (above);
  "(capture .txt)" matches the digest's file. Holds.
- `scope` cell: "what a Japanese citation index's reference list is relative to the cited
  paper's own reference list, and how its counts are derived" — carried verbatim in substance by
  the note text. Holds.
- `teaches` cell: the filter sentence, the matched-item count and the CiNii-Articles divergence
  are all carried. **One compression**: "its *identification* scope also differs from CiNii
  Articles" — the capture says `文献の収録範囲が異なっており、（それに伴って）別の手法で同定・
  統合処理を行っているため` (coverage differs, and consequently the identification/merge
  *method* differs). "identification scope" fuses 収録範囲 (coverage) with 同定・統合手法
  (method); the conclusion it draws ("lists do not necessarily match") is carried.
- **Not carried — `source` cell title.** The row reads "CiNii Research マニュアル,
  論文の追加方法・引用文献／被引用文献 — 国立情報学研究所 (NII)". The captured page's title and
  h1 are `論文詳細表示画面について` (`<title>論文詳細表示画面について | 学術コンテンツサービス
  サポート</title>`), and `論文の追加方法` occurs **0** times in both `.txt` and `.raw`
  (`t.count`/`r.count` = 0). The title is inherited verbatim from the staged campaign entry
  (`/home/vgpnk/Projects/shokuknow/merge/chousa/SOURCES.append.md:12`, staged id S087) and
  survives into the lane row and `.ufo/waves/round-49/assimilation/append-block.md:1` unchecked.
  "NII マニュアル" and 国立情報学研究所(NII) are carried (nav マニュアル; footer link).

## (3) Every entry sentence citing S096 (`corpus/knowledge/aggregator-vs-source-r36.md`)

| entry line | sentence | verdict |
|---|---|---|
| 4 | `source: S096 — … — section G 参考文献／被引用文献, the two 注意書き — capture 2026-10-23, re-opened 2026-10-25` | **supported** — `<h2>G 参考文献／被引用文献</h2>`; exactly two red-bold note paragraphs in the G div (raw 25332, 25527); capture mtime Oct 23 20:33. "re-opened" is not artifact-provable but the spans were built from it this round. |
| 11 | `re-bound by document to S096, S097, S098 and S099` | **supported** (four `source:` lines, one row per URL). |
| 16-17 | quote 1 + "(its 参考文献 are not necessarily the paper's own references)" | **supported** verbatim. |
| 17-18 | "only references matched by the service's 同定・統合処理 are shown" | **supported**: `実際の論文の参考文献のうち、CiNii Researchの同定・統合処理で、同定・統合された参考文献だけが表示されます。` (gloss "matched" for 同定・統合). |
| 18-20 | quote 2 + "(the reference count is of the matched items, not the count printed in the paper)" | **supported** verbatim (`掲載数` = as published/listed). |
| 20-22 | quote 3 + "says the two NII services cover and merge differently, so their lists need not match each other" | **supported**: the same sentence continues `別の手法で同定・統合処理を行っているため 、CiNii Articlesの「参考文献」「被引用文献」の結果とも必ずしも一致していません。` |
| 48-49 | "An index's reference list is derived from the source's list and is not equal to it: S096 says <quote 1> and that the count is only `同定・統合された分をカウントしています`" | **narrower** — the quotes are exact, but "is not equal to it" drops the capture's 必ずしも (not *necessarily* equal); the display is "only matched references", which permits equality when all match. |
| 50-52 | "stated first-party by the aggregator" | **supported** (NII's own manual page). |
| 56-58 | "S096's count is a matched-item count: an empty cited-by list from an index is weaker evidence…" | **narrower** — the matched-item count/filter is stated for `参考文献数` (references the paper cites) only; the capture describes 被引用文献 as `随時増加していきます` and as differing from CiNii Articles, never as a matched-item count. The cited-by conclusion rests on S097's lag, not on S096's count. |

## (4) Context check (quote not lifted against its context)

```
G div raw chars [24823:25716] len=893
red-bold note paragraphs in G section: 2 [25332, 25527]
  25332 '<p><strong style="color: #F00;">※CiNii Researchの「参考文献」は、実際の論文の参考文献と必ずし'
  25527 '<p><strong style="color: #F00;">また、CiNii Researchでは、CiNii Articlesとは 文'
raw_off=25365 txt_off=3599 in_G=[24823:25716] -> True
raw_off=25473 txt_off=3707 in_G=[24823:25716] -> True
raw_off=25562 txt_off=3752 in_G=[24823:25716] -> True
```

All three quotes sit inside section G's own div, in the two 注意書き paragraphs that follow the
参考文献/被引用文献 table and precede section H — "section G … the two 注意書き" is structurally
right. Quote 3 is cut mid-sentence (`…異なっており`) but the entry's paraphrase follows the
continuation, so it is not a context inversion; quote 1's continuation (`…だけが表示されます`)
is reported in the entry's prose, not dropped. No quote is used against its surrounding text.

## Findings (advisory; frozen predicate/target/counter unchanged)

1. Binding is sound: 3/3 spans, digests, forms, slices, single occurrences and all three
   `char N` anchors re-derive exactly; the `.txt` form is forced and correctly chosen.
2. `SOURCES.md:106` `source` cell carries a title (`論文の追加方法・引用文献／被引用文献`) the
   capture does not — inherited from staged S087; `teaches`/`scope` carry the substance except
   the "identification scope" compression of 収録範囲 + 同定・統合手法.
3. Entry: 6 of 8 S096-citing sentences fully supported; two are narrower (unconditional
   "is not equal"; matched-item count extended from 参考文献 to the cited-by list).
4. C2's predicate cannot see items 2-3 (URL/digest/quotes/anchor, not entailment) — consistent
   with the claim's note that the counter "measures binding and presence, not entailment".
Scratch `/dev/shm/chousa-r49-ReopenS096` deleted; no tool installed, no production file touched.

VERDICT: S096 (CiNii Research manual row + its spans/anchors + its entry citations) — partly — binding, digests, forms, slices, single occurrences and all three `char N` anchors hold exactly, and the quotes' context is consistent, but the Registry `source` cell carries a staged title the capture does not ("論文の追加方法" 0 occurrences; page is 論文詳細表示画面について), `teaches` fuses 収録範囲 with 同定・統合手法, and two entry sentences are narrower than the capture (unconditional non-equality; matched-item count extended from 参考文献 to the cited-by list).

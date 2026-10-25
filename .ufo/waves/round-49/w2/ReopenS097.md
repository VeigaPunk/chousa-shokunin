# ReopenS097 — lane row S097 (J-STAGE publisher page), attacked

Item attacked: registry row `S097` and the two spans it anchors. Capture key `sha256(url)[:24]` =
`167e9db7dde3c998838e3469`; `.txt` digest `ba7b2aa64899861cd07bad79220c7d438b5c7664b96486c4b74618777a14dd31`
(= the digest in `spans.tsv`), `.raw` digest `c9d610ad7a50f01b…` (HTML; `<title>` = `J-STAGE登載誌が利用できる機能`).
Row unchanged since the measured rev: `git diff --stat 4ce61fc..HEAD -- spans.tsv spans/ SOURCES.md
aggregator-vs-source-r36.md lessons/round-49.md` → **empty**; `grep -c '^S097'` on that rev's `spans.tsv` → `2`,
working tree → `2`.

## (1) Span recomputation — both rows hold

`/dev/shm/chousa-r49-ReopenS097/verify_s097b.py` (deleted after the run), from the lane checkout with `TMPDIR`
set: recomputes `sha256(url)[:24]`, picks the form whose **file** digest equals the recorded one, decodes it as
`build-spans.py`/`c2-count.py` do (`Path.read_text(encoding="utf-8")`), compares `form[offset:offset+len(span)]`
with the span text **and** its UTF-8 bytes, and counts quote occurrences.
```
$ python3 /dev/shm/chousa-r49-ReopenS097/verify_s097b.py
--- S097 span=spans/S097-1.txt offset=2680 form=txt
  key=167e9db7dde3c998838e3469 txt_digest_matches=True raw_digest=c9d610ad7a50f01b…
  form chars=7293  span chars=243 bytes=545 quote chars=83
  form[off:off+len(span)] == span text   : True
  form[off:off+len(span)].encode()==bytes: True
  quote in span at 80 (offset+that = char 2760)
  quote count in form = 1; span count in form = 1; span first at 2680
  span len > quote len: True; quote==span.strip(): False
--- S097 span=spans/S097-2.txt offset=2527 form=txt
  form chars=7293  span chars=209 bytes=377 quote chars=49
  form[off:off+len(span)] == span text   : True   .encode()==bytes: True
  quote in span at 80 (offset+that = char 2607); count in form = 1; span first at 2527
```
Both spans are exact slices of the digest-matching form, each quote occurs **exactly once**, each sits at span
position 80 (`CONTEXT`), so `offset+80` = the anchor char. **Reproducibility trap:** the capture is CRLF (291
`\r\n`, no bare CR, 15656 bytes) and the offsets hold only under universal-newline reading: `read_text()` gives
7293 chars, `read_bytes().decode('utf-8')` gives 7584, and the char-2607 quote sits at 2607 in the first and 2800
in the second. My first run (byte decode) printed `form[off:off+len] == span bytes: False` for both rows — a false
FAIL caused only by newline mode. Neither the manifest nor `claims.md`'s C2 predicate names the read mode; the
frozen counter reads `read_text` on both sides, so `C2=PASS` stands, but the leg is not replayable by a checker who
opens the file in binary.

## (2) Registry row `corpus/SOURCES.md:107` — anchors true; scope cell under-declares
```
$ python3 - (cells of the S097 row)          # 11 cells
[4] teaches: how J-STAGE exposes a published article's citation and cited-by links and when they appear, plus its dark archive and similarity-check service
[5] anchor : section 1 (DOI登録機能) and section 2 (引用・被引用文献リンク機能) (capture .txt); located quotes char 2607, char 2760
[6] claims : a DOI can only be used as a URL 1 to a few days after J-STAGE publication; … citation and cited-by DOI links are created from a few days to two weeks after publication; J-STAGE keeps a Portico dark archive and screens submissions against iThenticate for similarity
```
Every `char N` is a located quote offset, each landing in the section the cell names:
```
char 2607: form[2607:2607+49] == quote -> True     # §1 body 2249..2693
char 2760: form[2760:2760+83] == quote -> True     # §2 body 2693..2932
  char 2716: J-STAGEで記事が公開されると、引用文献および被引用文献へのリンクが表示されます。
  char 2845: このうち、PubMedやCASに収録されているものは、PubMed/CAS上の書誌情報へのリンクが表示されます。
  char 1940: 1. DOI登録機能   char 1953: 2. 引用・被引用文献リンク機能  (nav list; bodies at 2249 / 2693)
```
`teaches` carries nothing the capture lacks — both extra services are on the page:
```
char 5411: 'J－STAGEでは、…ダークアーカイブサービス「Portico（ポルティコ）」と契約し、J-STAGE登載誌の発行機関にご利用いただいています。…Portico連携可否を設定いただけます。'
char 6241: 'J-STAGE登載誌の発行機関に向けて…剽窃チェックのためのウェブサービス「J-STAGE類似性チェックサービス」を、有料サービスとして提供しています。投稿された論文を剽窃チェックツール「iThenticate」に登録されているデータと照合し…'
```
But `scope` names **only §1–2** while `teaches`/`claims` draw on §11 (char 5395+) and §14 (char 6222+), and those
two claims have **no located quote** — the declared scope is narrower than the row's own claims cell. `claims`
also softens the framing: §14 is a 有料サービス offered to 発行機関 and §11 lets each publisher choose Portico
linkage, whereas the cell says J-STAGE "keeps a Portico dark archive and screens submissions". Adjacent defect in
cell [1]: the row labels the document "J-STAGE 出版社向け, **Citation**・被引用文献リンク機能" — `'Citation'` occurs
**0×** in the capture (`引用・被引用文献リンク機能` 2×) and the page's own title `J-STAGE登載誌が利用できる機能`
(5× in the capture) appears nowhere in the row.

## (3) Entry sentences citing S097 (`corpus/knowledge/aggregator-vs-source-r36.md`)
- `:5` `source: S097 — … — sections 1 and 2` — matches the capture (headings at 2249 / 2693). **supported**
- `:33-36` "J-STAGE's publisher page says links to citing and cited works registered in its partner services are
  made days to two weeks after the article appears" — capture char 2760: `J-STAGEが連携している外部サービス に登録
  されている引用文献および被引用文献には、J-STAGEでの記事公開から数日～2週間後にDOIによるリンクが作成されます`.
  **narrower**: the capture says *DOI* links (「DOIによるリンク」) for works in *external services*, and the preceding
  sentence (char 2716) says the reference/cited-by links are displayed **as soon as the article is published**; the
  entry's bare "links … are made days to two weeks after" drops both qualifiers and reads as if citation links only
  appear late.
- `:37-38` "a DOI works as a URL only one to a few days after publication" — capture char 2607: `DOIがURLとして使用
  できるようになるには、J-STAGEでの公開から1日～数日程度かかります。` **supported** (「1日～数日程度」 = about 1 day to
  several days; "a few days" is a fair rendering).
- `:54-56` (Inference) "a hop checked against an index can be unresolved **only** because the index has not yet
  linked the reference" — **not supported as written**: S097 gives the delay, not exclusivity, and the same entry's
  S098 line (`:26`, `システムが引用元の所在を特定できた文献にリンクを付与しています`) says a link is attached only where
  the system located the work, so a hop can be unresolved because resolution failed; char 2716 (display at
  publication) also cuts against "only". The rest of that inference (an empty cited-by list is weaker than an empty
  search of the sources) is unaffected.

## (4) Context consistency — consistent with the reading, one rendering artifact
The quote at 2760 sits between chars 2716 and 2845; in context the page draws exactly the distinction the entry
needs (links displayed at publication; DOI links for externally-registered works created 数日～2週間 later; PubMed/CAS
items get bibliographic links instead). Nothing is lifted against its context. One artifact: the quoted string
carries a space at a link boundary that the source HTML does not have.
```
raw char 27711: '…表示されます。<a href="…/JstageServices/TAB1/-char/ja" …>J-STAGEが連携している外部サービス</a>に登録されている引用文献および…'
txt char  2760: 'J-STAGEが連携している外部サービス に登録されている引用文献および…'
```
The `.txt` renderer inserted ` ` where the HTML has `</a>に`; the quote is verbatim against the digest-bound `.txt`
form (what the frozen leg binds) but not against the HTML source. The entry, the span and the lesson
(`corpus/lessons/round-49.md:80-81`, same chars 2760 / 2607) all carry the renderer's space, so the string is at
least self-consistent across the lane.

## Cross-checks and risks
```
$ python3 corpus/evidence/round49/c2-count.py | tail -8
QUOTES_IN_ENTRY=28/28  QUOTES_IN_LESSON=28/28  SPAN_CONTEXT=28/28
CAPTURE_BOUND=28/28    ANCHOR_BOUND=8/8        C2=PASS
```
Frozen C2 legs for this row replay PASS at the current tip; no frozen predicate, target or counter is proposed for
change. Risks, all calibration/operability rather than fabrication: span offsets are only replayable under
universal-newline reads (undocumented in the manifest); the scope cell omits §11/§14 whose claims are unanchored and
the row's "Citation" label contradicts the page title it never names; the quote contains a `.txt`-renderer space
absent from the HTML; entry `:55` "only because" overreaches and is the sentence a chain checker would act on.

VERDICT: lane row S097 (J-STAGE publisher page) — partly — every frozen leg holds (both spans are exact slices of
the digest-matching `.txt` form at 2680/2527, each quote occurs once, chars 2607/2760 are the located quote offsets,
`teaches` is carried by §11/§14 and both entry quotes are supported), but the scope cell under-declares §11/§14 and
leaves their claims unanchored, the row's label invents "Citation" against a page title it never names, the quote
carries a renderer-inserted space absent from the HTML, and the Inference "only because" is not carried by S097.

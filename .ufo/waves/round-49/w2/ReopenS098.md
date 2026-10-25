# ReopenS098 — W2 falsify: lane row S098 (J-STAGE 編集者・出版社向けFAQ, JST)

Attacked item: the S098 row — its five span rows, its Registry row, every entry sentence
citing S098, and quote/context fit. Lane checkout `/home/vgpnk/Projects/shokunin/chousa-shokunin`
(`git rev-parse master` = `87e93353d046f2d7e4f0d2f5d3b87b7008a64ef0`; code measured is `4ce61fc5`,
`87e9335` adds only `measure-after.txt`). Captures read only from `.qcache`; no fetch.
Scratch `/dev/shm/chousa-r49-ReopenS098` (deleted).

## 1. Span rows replayed (`corpus/evidence/round49/spans.tsv:7-11`)

Key recomputed from the URL as written in the rows; the recorded `capture_sha256` is a FILE
digest and it is the `.txt`'s, so the form is the `.txt` decoded UTF-8 (strict decode OK, 0 U+FFFD):

```
$ python3 -c 'import hashlib;print(hashlib.sha256("https://www.jstage.jst.go.jp/static/pages/FAQs/TAB2/-char/ja".encode()).hexdigest()[:24])'
fea98dc5a5a486c988dd415c
CAPTURE_TXT exists=True bytes=95733 sha256=ead3a7dd4ba97ae0ef05620f314844badf6c3fef5428988e61e4e2a146772f60
CAPTURE_RAW exists=True bytes=178654 sha256=daa2c5d940fc20d0fab683e5e25b1f31a802d681d71319002449edf334029454
```

Script (`/dev/shm/chousa-r49-ReopenS098/check-s098.py`, executed body):

```python
for sid,url,cap_sha,off,span_file,quote,entry in rows:      # rows = spans.tsv S098 lines
    name = [k for k,d in digest_of.items() if d == cap_sha][0]
    form = forms[name]                                      # txt.read_text(utf-8,replace) | raw.decode('utf-16le',replace)
    span = (EV/span_file).read_text(encoding="utf-8", errors="replace")
    slice_ = form[off:off+len(span)]
    print(slice_ == span, form.count(quote), span.count(quote), span.find(quote), off+span.find(quote))
```

Observed output (exit 0):

```
ROWS=5
ROW spans/S098-1.txt form=txt digest=ead3a7dd4ba97ae0 offset=29402 span_chars=191 slice_eq=True quote_once_in_form=True (1x) quote_in_span=1x quote_pos=80 char=29482  quote_char_indices_in_form=[29482]
ROW spans/S098-2.txt form=txt digest=ead3a7dd4ba97ae0 offset=29561 span_chars=187 slice_eq=True quote_once_in_form=True (1x) quote_in_span=1x quote_pos=80 char=29641  quote_char_indices_in_form=[29641]
ROW spans/S098-3.txt form=txt digest=ead3a7dd4ba97ae0 offset=29592 span_chars=191 slice_eq=True quote_once_in_form=True (1x) quote_in_span=1x quote_pos=80 char=29672  quote_char_indices_in_form=[29672]
ROW spans/S098-4.txt form=txt digest=ead3a7dd4ba97ae0 offset=29669 span_chars=183 slice_eq=True quote_once_in_form=True (1x) quote_in_span=1x quote_pos=80 char=29749  quote_char_indices_in_form=[29749]
ROW spans/S098-5.txt form=txt digest=ead3a7dd4ba97ae0 offset=29695 span_chars=183 slice_eq=True quote_once_in_form=True (1x) quote_in_span=1x quote_pos=80 char=29775  quote_char_indices_in_form=[29775]
SLICE_FAILS=0
```

**Offset unit (operability defect, not a content one).** Offsets are CHARACTER offsets in the
newline-normalised `read_text` form, not bytes: the `.txt` is 95 733 B / 39 924 chars decoded raw
but 39 633 chars as the builder reads it (291 CRLF pairs folded; `LF` 3 933 either way). So the
byte test the brief proposed cannot pass, nor can a naive `bytes.decode` slice:

```
raw[29402:29432].decode('utf-8')        -> UnicodeDecodeError: invalid start byte
bytes.decode('utf-8')[29402:]           -> '\n URL中に全角文字があると、それ以降の文字はURLの一部'   (291-char drift)
read_text form[29402:]                  -> 'PDF) \n \n\n \n \n \n 引用文献のリンクは、いつ、どのような仕組みで行わ…'  == spans/S098-1.txt
```

`build-spans.py:106-120` writes `offset = text.find(quote) - CONTEXT` on that form and the counter
(`c2-count.py:104`) reads the same form, so lane-internal agreement is exact; the docstring never
names the newline normalisation.

## 2. Registry row (`corpus/SOURCES.md:108`)

- **`char N` anchors: 5/5 located quote offsets.** Each equals `offset + 80` (the CONTEXT pad) and
  each string sits at exactly that char (`quote_char_indices_in_form` above = 29482, 29641, 29672,
  29749, 29775, identical to the anchor cell and to the Gate table `lessons/round-49.md:82-86`).
- **`teaches`, the ladder: exact.** Capture char 29494-29720 carries
  `記事に登録された引用文献の情報をもとに、システムが引用元の所在を特定できた文献にリンクを付与しています。`
  … `引用元の所在確認は、次の順で解析・検索を実施しています。` `1.DOI（メタデータ項目） をもとに検索　例：10.xxxx`
  `2.書誌情報（メタデータ項目） をもとに検索　項目：著者名、誌名、巻号ページなど`
  `3.引用文献の原文情報からDOIを検出して検索` `4.引用文献の原文情報を書誌情報に解析して検索`.
  All four rungs are enumerated correctly, in order, including rung 2.
- **`teaches`, "attached only where": not lexical.** The raw HTML carries the sentence bare inside
  `<dd class="answer">`, no 原則/基本的に and no exclusive:
  `システムが引用元の所在を特定できた文献にリンクを付与しています。<br>`. `特定でき` occurs once in
  the capture; nothing states the negative case (`特定できない`/`付与されない`/`リンクされない` = 0 hits;
  the single `付与されません` at char 28022 is about DOIs on 電子付録). "only where" is a sound
  implicature of the set-description but is the row's inference, not the capture's words.
- **`teaches`, final clause is an unmarked inference.** "so a linked hop can rest on a heuristic
  rather than on an identifier" is the lane's conclusion; the lane marks these elsewhere — S030
  (`SOURCES.md:30`): "…; recheck-cadence comparison is a lane inference". S098's cell has no marker.
- **`scope`: both halves carried, only one anchored.** Half one is the ladder. Half two is at char
  37702: `引用文献のリンクは公開後も削除・再問合せ（登録した引用文献のリンク先があるかどうかの問合せ）を行うことができます。`
  (question at 37561 `公開中の記事に誤った引用文献へのリンクがありました。リンクを削除することはできますか。`;
  the trigger list at 29586 names `記事一覧の引用リンク削除・問い合わせ機能`). No located quote in the
  anchor cell covers it, so the scope's second clause is not re-derivable from the row alone;
  "withdrawn" is the lane's word for 削除.
- **`source` label is a lane gloss.** Page `<title>` is `FAQ（J-STAGE登載機関向け）`, H1 `よくあるご質問`;
  "編集者・出版社向け" characterises that audience (fair, not the page's heading). `被引用` = 0 hits
  here, and the row correctly does not claim cited-by (that is S097's).

## 3. Entry sentences citing S098 (`corpus/knowledge/aggregator-vs-source-r36.md`)

| sentence | verdict | capture |
|---|---|---|
| header: "the 引用元の所在確認 passage and its four-step resolution list — capture 2026-10-23, re-opened 2026-10-25" | **supported** | `.txt` mtime 2026-10-23T20:33:46; passage + 4 rungs present |
| Obs.: the two quoted sentences and all four rung quotes (5 quotes; two also re-quoted in Inference) | **supported, byte-exact** | each `count_in_capture=1`; `count_in_entry` 1 or 2 as quoted twice |
| Obs. gloss "(a link is attached only where the system located the cited work)" | **supported as gloss / narrower** | no exclusive in the source sentence (§2) |
| Obs. "bibliographic metadata" (rung 2) | **supported** | `2.書誌情報（メタデータ項目） をもとに検索　項目：著者名、誌名、巻号ページなど` |
| Obs. "Rungs 3 and 4 work on the reference text, not on an identifier" | **partly** | true as *input* (both read `引用文献の原文情報`); false as a *contrast*: rung 2 is also DOI-free, and rung 3's output **is** an identifier — `3.引用文献の原文情報からDOIを検出して検索` — contradicting the entry's own rung-3 gloss |
| Inf.: "Read together, the Japanese sources describe a resolution ladder whose bottom two rungs read reference text" | **narrower** | only S098 carries a ladder: `所在確認` 1/0/0, `次の順` 1/0/0, `解析・検索` 1/0/0, `原文情報` 2/0/0 in S098/S096/S097. The endpoints are then tagged (S098), so the plural subject over-attributes; "bottom two rungs read reference text" is exact |
| Inf.: "S098 starts from `1.DOI…` and ends with `4.…解析して検索`" | **supported** | first and last rungs, quotes at char 29672 and 29775 |
| Inf.: "a hop resolved by parsing reference text is a weaker evidential object than one resolved by DOI" | **supported as inference** | under `#### Inference`; the capture supplies only the ladder |
| Unknown: "Whether J-STAGE records which rung produced each link … no claim is made that a reader can recover it" | **supported as non-claim** | `どの方法`/`判別`/`特定方法` = 0 hits; the one `記録` (char 3417) is unrelated |

## 4. Context fit

The quote is the first sentence of the answer to `引用文献のリンクは、いつ、どのような仕組みで行われているのですか。`
(char 29423), and the four-step list sits under `引用元の所在確認は、次の順で解析・検索を実施しています。` — the
entry's "resolution is a heuristic ladder" is the passage's own structure, not a lifted fragment; the
80-char pads on both sides hold the question, the answer's opening and the list's head. The raw HTML
confirms the same paragraph (`<dd class="answer"><p>記事に登録された引用文献の情報をもとに、…`). One
unused support, not a conflict: the same answer's trigger list (`1.手動検索` / `2.自動検索`
`・J-STAGE公開時にシステムで引用元の所在を検索`) is not used; the entry assigns timing to S097 alone.

VERDICT: S098 row (spans.tsv:7-11, SOURCES.md:108, aggregator-vs-source-r36.md S098 sentences) — partly — every byte-locatable element re-derives exactly (key `fea98dc5…`, `.txt` digest `ead3a7dd…`, 5/5 slices, 5/5 quote-once, 5/5 `char N`, context intact), but four reading-level slips remain: the teaches cell states an inference unmarked, "attached only where" is not lexical, "rungs 3 and 4 … not on an identifier" fits neither rung 3 (text-detected DOI) nor rung 2, and "Read together, the Japanese sources describe a resolution ladder" attributes to S096/S097 a ladder only S098 carries.

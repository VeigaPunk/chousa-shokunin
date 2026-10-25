# GroundBnuA — round 50 / wave 1 — re-ground the CNKI 教师 manual (staged S145)

Seat: scribe-ground, leaf. Opened: the capture below, frozen `claims.md`, staged `citation-matching-semantics-r41.md`, the `SOURCES.append.md` S145 row, `build-spans.py`, `c2-count.py`, `tools/inference-ground.py`. No network, no production/registry/lesson write, no counter run against the lane.

## 0. Capture identity — the form of every offset

```
$ sha256sum .../.qcache/275c79d45b1e9b0fd32cef93.*                      # paths as run
cbeccf3f612eb68824def16c0c07001f24790b222ce03c5e7cc5b9eebfbfddc1  ...93.pdf   (1,245,606 B)
cbeccf3f612eb68824def16c0c07001f24790b222ce03c5e7cc5b9eebfbfddc1  ...93.raw   (1,245,606 B)
8d201ed15c15709dd413d1468e45352011f03c1618c668068977bff5a9703031  ...93.txt   (22,648 B)
$ python3 -c 'import hashlib;print(hashlib.sha256(b"https://bs.bnu.edu.cn/docs/20160407183946745914.pdf").hexdigest()[:24])'
275c79d45b1e9b0fd32cef93
$ file ...93.raw
...93.raw: PDF document, version 1.7, 17 page(s)
$ pdftotext -layout ...93.raw reextract.txt && sha256sum reextract.txt ...93.txt && diff -q reextract.txt ...93.txt && echo IDENTICAL
8d201ed15c15709dd413d1468e45352011f03c1618c668068977bff5a9703031  reextract.txt
8d201ed15c15709dd413d1468e45352011f03c1618c668068977bff5a9703031  ...93.txt
IDENTICAL
```

Cache stem = `sha256(url)[:24]`; the `.txt` is the `pdftotext -layout` extraction of the `.raw` PDF, reproduced byte-for-byte from the bytes on disk. **Form of every quote: `275c79d45b1e9b0fd32cef93.txt` read as UTF-8 — 9,914 characters, 22,648 bytes.** The `.raw` is the PDF (17 pages), not a text form.

## 1. Counts — exact command, observed output

```
$ python3 -c 'p="/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache/275c79d45b1e9b0fd32cef93.txt"; t=open(p,encoding="utf-8").read(); print("CHARS",len(t)); [print(k,t.count(k)) for k in ("引文核对","核对","匹配","引文","标明引文")]'
CHARS 9914
引文核对 0
核对 0
匹配 0
引文 9
标明引文 9
$ python3 -c '... print("bare_yinwen_outside_biaoming", t.count("引文")-t.count("标明引文"))'
bare_yinwen_outside_biaoming 0
$ python3 -c '... [print(k,t.count(k)) for k in ("标明","标明引文","标明了引用","引注","引证","比对","相似文献","文字复制比")]'
标明 10 · 标明引文 9 · 标明了引用 1 · 引注 14 · 引证 2 · 比对 13 · 相似文献 6 · 文字复制比 15
```

Both staged absences hold and one widens: **引文核对 0, 匹配 0, and 核对 0** as well. **引文 9 = 标明引文 9**, so the bare token occurs zero times outside the compound: the manual never uses 引文 standalone.

## 2. The section, opened

§2.3.2 heading at char 8831; §2.3.3 heading at 8977 — **the whole section is 146 characters, two sentences**: the title hint (8852) and one content sentence (8900). Printed page 15: footer `第 14 页` at 8528, form feed, running header, footer `第 15 页` at 9260; the TOC entry at 1249 says 15. The section states what the report *adds* and nothing about a citation list (`列出` 0).

## 3. Calibration — the staged clause overstates the mechanism

Staged `citation-matching-semantics-r41.md` (Observation, para 2): *"neither does the 教师 manual, which instead uses 引文 to mean a thesis's own citations **listed on a report sheet**."*

- 引文 occurs 9×, every occurrence inside 标明引文 (9 = 9; bare = 0) — no standalone use to gloss.
- The only gloss tying 标明引用 to anything is at 2955: 去除引用文献复制比 excludes 作者在文中标明了引用的文献. That supports "the author's own marked citations" and states their role — exclusion from a ratio.
- "listed on a report sheet" is unsupported: `列出` 0; 8900 gives the report's additions as 全文标红 + 指标详情; 全文对照报告单 is 原文内容与相似来源内容的比对 (9192+). No citation list is documented.

Suggested replacement (fenced, intended path `corpus/knowledge/citation-matching-semantics-r41.md`):

```
The 教师 manual never uses 引文 outside the report-sheet name 全文（标明引文）报告单
(9 of 9 occurrences), and its nearest gloss makes 标明引用 the author's own marked
cited literature, excluded from the 去除引用文献复制比 ratio — it never says the
sheet lists those citations.
```

Doc-internal drift, so do not quote the form list as canonical: `去除本人文献报告单` once (6740) vs `去除本人已发表文献报告单` twice (1346 TOC, §2.3.3 heading).

## 4. What the manual does compare (same capture, contrast for the entry)

- 3072 `单篇最大文字复制比（含篇名）：指被检测文献与所有相似文献比对后` — the 查重 object is the whole document against similar literature.
- 4310 `连续重合字数大于 200 字` — the unit is a character run; thresholds 100/200 chars at 4319, 4351, 4513.
- 7528 `点击“两两比对”按钮，可以比对两篇文献的全文` — the only two-document comparison documented.

None is a citation-versus-record comparison; the manual has no 引文核对 vocabulary at all.

## 5. QUOTE machine lines (8 rows; each unique in the .txt, `char` = `text.find(quote)`)

```
QUOTE	S145	https://bs.bnu.edu.cn/docs/20160407183946745914.pdf	去除引用文献复制比：指去除了作者在文中标明了引用的文献后	corpus/knowledge/citation-matching-semantics-r41.md
QUOTE	S145	https://bs.bnu.edu.cn/docs/20160407183946745914.pdf	报告单包括简洁报告单、全文（标明引文）报告单	corpus/knowledge/citation-matching-semantics-r41.md
QUOTE	S145	https://bs.bnu.edu.cn/docs/20160407183946745914.pdf	若选择查看“全文（标明引文）报告单”	corpus/knowledge/citation-matching-semantics-r41.md
QUOTE	S145	https://bs.bnu.edu.cn/docs/20160407183946745914.pdf	全文报告单的内容包含了简洁报告单的全部内容，并增加了原文的全文标红	corpus/knowledge/citation-matching-semantics-r41.md
QUOTE	S145	https://bs.bnu.edu.cn/docs/20160407183946745914.pdf	全文对照报告单大部分内容与全文（标明引文）报告单一致	corpus/knowledge/citation-matching-semantics-r41.md
QUOTE	S145	https://bs.bnu.edu.cn/docs/20160407183946745914.pdf	单篇最大文字复制比（含篇名）：指被检测文献与所有相似文献比对后	corpus/knowledge/citation-matching-semantics-r41.md
QUOTE	S145	https://bs.bnu.edu.cn/docs/20160407183946745914.pdf	点击“两两比对”按钮，可以比对两篇文献的全文	corpus/knowledge/citation-matching-semantics-r41.md
QUOTE	S145	https://bs.bnu.edu.cn/docs/20160407183946745914.pdf	连续重合字数大于 200 字	corpus/knowledge/citation-matching-semantics-r41.md
```

Offsets (quote char / span start+len / chars / whitespace words; all `unique True slice_ok True`): 2955 / 2875+188 / 28 / 1 · 8039 / 7959+182 / 22 / 1 · 8852 / 8772+178 / 18 / 1 · 8900 / 8820+193 / 33 / 1 · 9137 / 9057+186 / 26 / 1 · 3072 / 2992+191 / 31 / 1 · 7528 / 7448+182 / 22 / 1 · 4310 / 4230+174 / 14 / 3. Each span is the 80-char-context slice `build-spans.py` derives, longer than its quote; each quote ≤160 chars and ≤25 whitespace words.

## 6. Integration notes for L1 (measured here; nothing run against the lane)

1. **staged S145 → lane S107.** `build-spans.py` `ID_RE=^S\d{3}$` and `c2-count.py` `on_bound` (`bound.get(sid)==url`) key on the LANE id: `quotes.tsv` rows must say `S107` with this exact URL.
2. `MIN_PER_ID=3`; all 8 rows pass the counter's quote legs, so ≥3 can be entered.
3. **anchor cell:** `char N` must be an offset of a quote row for that id (counter: `offset+span.find(quote)`). Use `char 2955, char 4310, char 8900`.
4. Each quote must appear verbatim in the entry (`in_entry`) and in `corpus/lessons/round-50.md` (`in_lesson`); the staged `source:` lines still carry staged ids `S135`/`S136`/`S145` and must become the lane ids or `REF_ID_UNBOUND` rises.
5. **inference-ground hazard, measured.** The 教师 manual cannot ground a *phrase*: 5 ASCII runs only (`CNKI` 44, `A.` 3493, `B.` 3969, `Excel` 7629, 9714), no whitespace-separated Latin pair, and `is_two_words` counts only whitespace chunks containing `[A-Za-z]`. On scratch copies under `/dev/shm/chousa-r50-GroundBnuA/root` (scratch S107 row + scratch spans): `` `去除引用文献复制比` `` → `tokens=0` `INF_UNGROUNDED`; `` `CNKI 科研诚信管理系统研究中心` `` → `tokens=0`; `9,914` → `INF_TOKEN_NOT_IN_SPAN`; **`The segment threshold is a character-run length, 200 characters (S107).` → `GROUND: PASS` rc=0** (a 3-digit numeral inside a cited span grounds). The staged entry is prose, not `- ` bullets → `bullets=0` `FINDING INF_NO_BULLETS` `rc=1`: its Inference must be rewritten as `- ` bullets, and the 教师-manual bullet needs the 200 numeral.
6. Not run by me: `build-spans.py`, `quote-substance-check.py`, `c1-count.py`, `c2-count.py`, the Gate. My inference-ground runs used the scratch root above, not the lane tree.

## 7. Out of scope

The 管理员 (SXU), 子账号 (SEU) and ISTIC captures were not opened; their counts belong to other seats. No tool installed, no file outside this report written, scratch `/dev/shm/chousa-r50-GroundBnuA/` deleted.

VERDICT — Attacked the staged 教师-manual claims against the on-disk capture: 引文核对/核对/匹配 all 0 over 9,914 chars and 引文 9 all inside 标明引文 survive and widen the absence, but the staged mechanism clause "listed on a report sheet" is unsupported by §2.3.2 (146 chars; adds 全文标红 + 指标详情 only) and the staged Inference section cannot pass inference-ground (`INF_NO_BULLETS`), while 8 located quotes and one numeral-grounded bullet shape are verified usable.

# R51ExecInfStaged — `inference-ground` on the three staged search-record entries

Leaf seat, wave 1. Staged package and capture cache read only; my only write is this file. Scratch `/dev/shm/chousa-r51-R51ExecInfStaged/` (deleted). No install/upgrade, no network, no C1/C2/C3 counter run.

## 1. What I ran (lane root `/home/vgpnk/Projects/shokunin/chousa-shokunin`)

```
python3 tools/inference-ground.py --entry /home/vgpnk/Projects/shokuknow/merge/chousa/knowledge/corpus/knowledge/<E>.md \
  --spans /dev/null --counts /dev/null --registry corpus/SOURCES.md --root /dev/shm/chousa-r51-R51ExecInfStaged/root
```
```
GROUND entry=japanese-search-record-r38.md section=1 bullets=3 tokens=3 grounded=0
FINDING INF_UNCITED bullet=1 token=''
FINDING INF_TOKEN_NOT_IN_SPAN bullet=1 token='as actually run'
FINDING INF_UNCITED bullet=2 token=''
FINDING INF_UNGROUNDED bullet=2 token=''
FINDING INF_TOKEN_NOT_IN_SPAN bullet=3 token='what the record claims'
FINDING INF_TOKEN_NOT_IN_SPAN bullet=3 token='what the gate can check'
GROUND entry=chinese-search-record-r39.md section=1 bullets=4 tokens=1 grounded=0
FINDING INF_UNCITED bullet=1 token=''
FINDING INF_UNGROUNDED bullet=1 token=''
FINDING INF_UNCITED bullet=2 token=''
FINDING INF_TOKEN_NOT_IN_SPAN bullet=2 token='what must a search record carry?'
FINDING INF_UNGROUNDED bullet=3 token=''
FINDING INF_UNGROUNDED bullet=4 token=''
GROUND entry=japanese-search-record-r38-amendment-2026-10-23.md section=1 bullets=4 tokens=2 grounded=0
FINDING INF_UNCITED bullet=1 token=''
FINDING INF_UNGROUNDED bullet=1 token=''
FINDING INF_UNCITED bullet=2 token=''
FINDING INF_UNGROUNDED bullet=2 token=''
FINDING INF_TOKEN_NOT_IN_SPAN bullet=3 token='a field, but not in PRISMA'
FINDING INF_TOKEN_NOT_IN_SPAN bullet=3 token='2020'
FINDING INF_UNGROUNDED bullet=4 token=''
GROUND: FAIL   (all three, exit 1)
```
19 findings over 11 bullets / 6 tokens. Two caveats. (a) The empty manifests are fail-closed — `pathlib.Path('/dev/null').is_file()` → `False`, so `span_texts`/`count_values` are empty and *every* token must print `INF_TOKEN_NOT_IN_SPAN`; this run cannot separate "ungrounded" from "ungroundable", §2 does that per bullet. (b) `INF_UNCITED`/`INF_UNGROUNDED` are manifest-independent and are real text defects: 6 of 11 bullets cite no id (E1 b1,b2 · E2 b1,b2 · E3 b1,b2) and 7 of 11 carry no grounding token (E1 b2 · E2 b1,b3,b4 · E3 b1,b2,b4). The 5 bullets that do cite (E1 b3 `S105`; E2 b3 `S097`, b4 `S117`; E3 b3 `S097`, b4 `S105`) each cite an id whose row is another document — §4.

## 2. Per-bullet candidate phrase

Found with `text.find` in the capture `.txt` read as UTF-8 with `errors="replace"` (the form `build-spans.py` uses), exactly once in that form, ≤39 chars / ≤7 whitespace words (C2's limit: 25 words / 160 chars).

| entry | bullet first 60 chars | finding (this run) | candidate phrase | capture key | offset |
|---|---|---|---|---|---|
| japanese-r38 | `**The Japanese record is a *pair*, not a list.** The pair is` | UNCITED; TOKEN_NOT_IN_SPAN | 検索ワードや検索式は実際に使用した、もしくはそれと同等の詳細なものであること。 | 62be15a474e866e4bef6c9d5 | 36834 |
| japanese-r38 | `**The Japanese pair maps onto the lane's own gap with an add` | UNCITED; UNGROUNDED | その日時，使用した検索式を同時に記録しておく | 7194acc65a18f6555e4b8893 | 10234 |
| japanese-r38 | `**The Japanese answer is a reporting requirement, not a meas` | TOKEN_NOT_IN_SPAN ×2 | 同様の検索を再現できるようになる | 7194acc65a18f6555e4b8893 | 10371 |
| chinese-r39 | `**Q5b is answered, and the answer is a documented absence ra` | UNCITED; UNGROUNDED | 前尚无专门针对动物实验 SR 的报告规范 | fd468a36d78ff156b6200946 | 17708 |
| chinese-r39 | `**The module list is the Chinese answer to "what must a sear` | UNCITED; TOKEN_NOT_IN_SPAN | 检索词及逻辑关系（结合 MeSH/Emtree 主题词与自由词） | fd468a36d78ff156b6200946 | 15240 |
| chinese-r39 | `**Grey literature is the Chinese requirement the lane's West` | UNGROUNDED | 灰色文献的检索与记录 | fd468a36d78ff156b6200946 | 15310 |
| chinese-r39 | ``**The working example is worth more than the rule.** `S117` `` | UNGROUNDED | 从各数据库建立至 2024 年 4 月 1 日 | c7266931a1731db3ff6ae77d | 11404 |
| amendment | `**The Japanese search record is now specified, and it is spe` | UNCITED; UNGROUNDED | 検索の開始日と終了日を記載することで | 34fcefc159bf2ebbd1e09540 | 11294 |
| amendment | `**The rationale is the lane's own rationale, stated first in` | UNCITED; UNGROUNDED | 最新の結果を反映しているかどうか | 34fcefc159bf2ebbd1e09540 | 11348 |
| amendment | `**On Q12, the Japanese answer is "a field, but not in PRISMA` | TOKEN_NOT_IN_SPAN ×2 | 検索者、検索ワード、検索式は別紙様式 (V) -5に示したことを記載する。 | 62be15a474e866e4bef6c9d5 | 4409 |
| amendment | `**The hand-search clause is the second literature to ask for` | UNGROUNDED | none in either cached form — §3 | 3a8b45977cd111e45e3980a5 | — |

- The five English/lane-internal tokens the staged text already quotes are absent from **all seven** captures (`as actually run`, `what the record claims`, `what the gate can check`, `what must a search record carry?`, `a field, but not in PRISMA` → `0` against every key): replace with a capture quote, not re-cite.
- `2020` (amendment b3) grounds only from a source carrying it: `.txt` counts S109 2, S110 20, S116 5, S117 8, S119 2, S126 1, S125 0. S126's single occurrence is `The PRISMA 2020 statement` at 24695 in a bibliography — a lexical pass, not a field statement (the tool's named limit); S110's are genuine `PRISMA声明チェックリスト(2020年）`.
- japanese-r38 b2 cannot quote the three fields as one run: the two-column layout splits them (`誰が検索を行ったの` 13721, tail `その日時，使用した検索式を同時に記録しておく` 10234; the joined `誰が検索を行ったのか，その日時` occurs `0` times). Only the tail is quotable.

## 3. The Japanese `.docx` capture has no text form under either accepted rule

S125 (`3a8b45977cd111e45e3980a5`, the 国立保健医療科学院 form) caches a **ZIP container**, not text: `.txt` head `PK\x03\x04\x14\x00\x06\x00\x08\x00\x00\x00!\x00`, `.raw[:2] == b"PK"` (178056 B; `.txt` is its lossy UTF-8 re-encoding, 319599 B). Measured in both forms `build-spans.py:form_texts` and `c2-count.py:form_text` accept:
```
SRにおける文献検索期間について明記する     txt=0 raw-utf16le=0
文献検索期間2015年1月から2018年10月まで    txt=0 raw-utf16le=0
ハンドサーチ等により                       txt=0 raw-utf16le=0
文献検索期間                              txt=0 raw-utf16le=0
```
The quotes are real and live in `word/document.xml` `<w:t>` runs; deriving that third form from the `.raw` copied to scratch (runs joined via `<w:t(?:\s[^>]*)?>(.*?)</w:t>`, UTF-8, 18478 chars) gives each exactly once: `SRにおける文献検索期間について明記する` count=1 off=8417 · `文献検索期間2015年1月から2018年10月まで` count=1 off=8581 · `ハンドサーチ等により未公表データを収集した場合は、そのことを上記のフローチャートに含める。` count=1 off=8816.

So `build-spans.py` refuses every S125 quote by name and `c2-count.py:form_text` returns `None` for a derived span file's digest: **S125 cannot be BOUND under C2 as the machinery stands**, and the amendment's b4 plus its Observation b1/b2 cannot be grounded from the cache. Either both tools gain a docx branch (keyed on a `.raw` whose digest matches, deriving the run-joined text) or S125 is REFUSED — no lane row, no `source:` line, a `refused-doc` line in `corpus/lessons/round-51.md`, and the amendment naming the form by file path. The docx form suffices where it is added (§5), and the Observation bullets need it too, since they also quote S125.

## 4. Body-only ids name another document, and the staged ids collide

| token in staged text | staged row (`merge/chousa/SOURCES.append.md`) | lane row at the tip (`corpus/SOURCES.md`) |
|---|---|---|
| `S097` (chinese-r39 b3 "Japanese hand-search field") | FEVER dataset paper | J-STAGE 出版社向け Citation リンク機能 |
| `S105` (japanese-r38 b3; amendment b4, Unknown) | `chain-resolution-r3.md` own-work | 知网学位论文…检测系统使用手册（管理员） |
| `S106` (amendment Unknown) | `citation-chain-fidelity-r24.md` own-work | “中国知网”大学生论文管理系统使用手册（子账号） |

None names the document its bullet attributes to it, in either registry — drop them or describe by file path. Separately, lane max is `S106` (`awk -F'|' … max_registry_id=S106`), so the staged ids `S109`/`S110`/`S116`/… are staged-only numbering; after the append lands (S109→S107 … S126→S113) **lane S109 = staged S116 and lane S110 = staged S117**, so carrying `S109`/`S110` unchanged into japanese-r38 would cite the two 实验动物 PDFs while quoting J-STAGE and the 健康食品協議会 form. Renumber the `source:` ids; never carry a body id.

## 5. The CJK token rule: four CJK characters = two words

`has_two_words` is true at ≥2 whitespace-separated words containing an ASCII letter, **else** at `len(CJK_RE.findall(s)) >= 4`. Demo on a synthetic manifest in scratch (span file = a copy of the capture `.txt`, whole file, digest recorded):
```
jp-pass   `検索者、検索ワード、検索式は別紙様式 (V) -5に示したことを記載する。`  tokens=1 grounded=1 PASS
cn-pass   `灰色文献的检索与记录` (9 CJK chars)                                  tokens=1 grounded=1 PASS
cn-4cjk   `灰色文献` (exactly 4 CJK chars; count=3 in capture)                 tokens=1 grounded=1 PASS
jp-absent `…別紙様式 (V) -6に示したことを記載する。` (one char changed)          tokens=1 grounded=0 FAIL
  FINDING INF_TOKEN_NOT_IN_SPAN bullet=1 token='検索者、検索ワード、検索式は別紙様式 (V) -6に示したことを記載する。'
cn-3cjk   `检索词` (3 CJK chars; count=1 in capture, present)                  tokens=0 grounded=0 FAIL
  FINDING INF_UNGROUNDED bullet=1 token=''
```
The rule does **not** block a correctly grounded Japanese or Chinese bullet: a 4+-CJK-character quote grounds, a one-character mutation is refused by name, and the polarity machinery never fires on a pure-CJK phrase (its `words()` sees no ASCII, so the scope-stem set is empty and `polarity_flips` returns `[]`). Its sharp edge is the threshold: a three-character term that *is* the concept — `检索词`, `检索式`, `検索式` — is present in the capture and still yields `tokens=0` → `INF_UNGROUNDED`; such a bullet needs a longer run or a numeral. End to end, the staged Inference sections pass once repaired with the §2 phrases (per-bullet citations added, English paraphrases replaced by quotes):
```
repaired-jp    bullets=3 tokens=3 grounded=3 PASS
repaired-cn    bullets=4 tokens=4 grounded=4 PASS
repaired-amend bullets=4 tokens=4 grounded=3 FAIL  (S125 span = cache .txt)
repaired-amend bullets=4 tokens=4 grounded=4 PASS  (S125 span = derived word/document.xml runs)
```

## 6. For the L1

Add a per-bullet `S###` to the 6 uncited bullets and a capture quote to the 7 tokenless ones (§2 is the mapping); replace the five English/lane-internal quoted phrases; decide S125 (add the docx form to `build-spans.py` **and** `c2-count.py`, or REFUSE it and rewrite the amendment's two S125 Observation bullets); renumber `source:` ids to S107…S113 and drop `S097`/`S105`/`S106` for file paths. Do not read the §1 run as a grounding verdict: `--spans /dev/null` is unreachable-green by construction.

VERDICT — attacked the three staged entries with `inference-ground` (19 findings: 6 uncited bullets, 7 tokenless bullets, 6 ungroundable English/lane-internal tokens) and grounded every bullet against its capture (11/11 candidate phrases, each exactly once; 10 in the cached `.txt`, 1 only in a derived `word/document.xml` form); result: the CJK four-character rule passes correctly grounded Japanese and Chinese bullets (4 demo runs, 3 repaired-entry runs) but blocks three-character terms, and S125's `.docx` capture has no text form under either rule `build-spans.py`/`c2-count.py` accept, so S125 cannot be bound without a third form.

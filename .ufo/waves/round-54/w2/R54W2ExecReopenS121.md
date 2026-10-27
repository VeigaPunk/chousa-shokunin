# R54W2ExecReopenS121 — S121 re-opened independently (read-only)

Seat: R54W2ExecReopenS121 (executor, leaf). Lane: `/home/vgpnk/Projects/shokunin/chousa-shokunin`,
tip `447cf7ed4dc1a3708518b99e9a5e62e177c11ce9`; claims freeze `5a1a2063…` + erratum E1–E4 read first.
Scope: S121 only — its quotes, its anchor cells, and every `#### Observation` sentence of
`corpus/knowledge/source-type-taxonomy-r36.md` that cites S121. No predicate, counter or control touched.
Capture (read-only): `.qcache/adf6ba934e813b2c326fa150.txt`, 6,626 bytes, sha256
`4e46154f4a841d17d858eafb5c0099257030f301daadcaa30c37f2e668fb7138`.
Scratch `/fast/scratch/hyaku/chousa-r54/R54W2ExecReopenS121` (removed on exit); `PYTHONDONTWRITEBYTECODE=1`
set for the runs; no counter was executed (no lane module imported, no `__pycache__` written by me).

## 1. Which newline convention the lane uses — and the two disagree

```
bytes 6626 | CRLF pairs 877 | lone LF 119 | lone CR 0
raw decode, no translation : len(rawt)=4468
decode + CRLF->LF (read_text default, universal newlines): len(uni)=3591
uni == rawt.replace("\r\n","\n") -> True
sha256(file bytes)=4e46154f… ; sha256(normalised text)=3bdbd119… ; sha256(no-newline text)=aa748edb…
```

The lane uses the **newline-normalised** form (3,591 chars, Python `read_text` default): `build-spans.py`
and `c2-count.py` both call `read_text(encoding="utf-8")` (`c2-count.py:126-127,159,219`), the entry's
source line states "3,591 characters", and the registry row says "read as UTF-8 with newline
normalisation, 3591 characters". The raw-bytes form is 4,468 chars and **disagrees on every offset**;
the shift at each quote equals the number of CRLF pairs before it (122/138/228/229/259/395). The
recorded digest is of the **file bytes** (with CRLF) while offsets are normalised — by design, per
`build-spans.py` docstring ("capture_sha256 stays the digest of the FILE read"). Internally consistent.

## 2. Every S121 quote in `quotes.tsv` (6 rows) — count, offset, one-line, stated offset

| quote | count uni | offset uni | count raw | offset raw | one line in capture | stated | match |
|---|---|---|---|---|---|---|---|
| `推荐性` | 1 | 477 | 1 | 599 | yes | char 477 (Observation) | ✔ |
| `由 TC4 （全国信息与文献标准化技术委员会）归口` | 1 | 537 | 1 | 675 | yes | char 537 (source line) | ✔ |
| `发布 于 2025-12-02` | 1 | 1029 | 1 | 1257 | yes | char 1029 (source line, anchor) | ✔ |
| `实施 于 2026-07-01` | 1 | 1048 | 1 | 1277 | yes | char 1048 (source line, anchor) | ✔ |
| `（全部代替）` | 1 | 1162 | 1 | 1421 | yes | char 1162 (source line) | ✔ |
| `本标准非等效采用ISO国际标准：ISO 690:2021。` | 1 | 1797 | 1 | 2192 | yes | char 1797 (source line, anchor) | ✔ |

Every quote is one line, no newline inside, count 1 under **both** conventions (1-line-ness is
convention-independent). NFKC-folded counts are also 1 each (`unicodedata.normalize('NFKC',…)`): no
fullwidth duplicate hides behind exact-form search. Longest quote 25 chars, 3 whitespace words (≤160/≤25).

## 3. Every `char N` in the two anchor sites

| site | chars | each is an offset of a quote of S121 | verdict |
|---|---|---|---|
| `SOURCES.md:131` anchor cell | 1029, 1048, 1797 | yes (1029 发布, 1048 实施, 1797 采标) | holds |
| row also states | `3591 characters`, sha256 prefix `4e46154f4a841d17` | both reproduce | holds |
| `source-type-taxonomy-r36.md` source line | 537, 1029, 1048, 1162, 1797 | yes (537 归口, 1162 全部代替) | holds |
| `spans.tsv` rows 2–7 (offsets 397/457/949/968/1082/1717) | quote at +80 in every span; `uni[off:off+len]==span file` True ×6 | counter resolves `offset+span.find(q)` → 477/537/1029/1048/1162/1797 | holds |

## 4. `#### Observation` sentences citing S121 — holds / overstates / wrong

| # | sentence (S121-cited) | deciding substring from the capture | verdict |
|---|---|---|---|
| 1 | 标准号 field prints GB/T 7714-2025; designator twice, chars 1239/1333 | `标准号` label 1327, its value `GB/T 7714-2025` at 1333; designator count 2 at [1239,1333] | holds |
| 2 | 标准状态 prints 发布 于 2025-12-02 (1029) and 实施 于 2026-07-01 (1048) | `标准状态` 1011; both quotes count 1 at 1029/1048 | holds |
| 3 | 现行 twice (489, 1261), 推荐性 once (477) | counts 2 at [489,1261]; 1 at [477] | holds |
| 4 | 代替 block prints 2015 designator and `（全部代替）` (1162); 2015 twice (1136,1426); 全部代替 twice (1163,1415) | `代替了以下标准` 1110; GB/T 7714-2015 [1136,1426]; 全部代替 [1163,1415]; （全部代替）count 1 at 1162 | holds |
| 4b | "so neither the designator **nor the qualifier** can be quoted whole as a unique string" | qualifier **as printed is unique**: `（全部代替）` count 1 at 1162 — and is quoted whole in `quotes.tsv` row 6; only the bare words `全部代替` repeat (2×) | **overstates** |
| 5 | 采标情况 (1787) prints the ISO sentence (1797); next non-blank line 采标中文名称 … (1829); `ISO 690` once, `690` once | `采标情况` 1787; quote 1797; `采标中文名称` 1829 is the next non-blank line; counts 1 and 1 | holds |
| 6 | byline `由 TC4 …归口` (537) "continues that 主管部门为 国家标准委 (char 575)"; 基础信息 归口单位+执行单位 print 全国信息与文献标准化技术委员会, 主管部门 prints 国家标准委 (1759) | 537 exact; `国家标准委` at 575; values 1699/1730 both 全国信息与文献标准化技术委员会; 国家标准委 1759 | holds (575 points at the value; the phrase `主管部门为` begins at 569) |
| 7 | record's 归口单位 is 全国信息与文献标准化技术委员会 (`由 TC4 …`) | count 3 at [544,1699,1730] | holds |
| 8 | 附录/文献类型/文献类型标识/载体标识/[M]/[J]/EB/OL each 0 times; 著录 5× record, 1× portal; four inside 信息与文献 参考文献著录规则, fifth in 相近标准 list (标准文献题录著录规则, char 2993) | all seven tokens count 0; 著录 [354,521,1191,1281,2993]; titles at [344,511,1181,1271] → four at title+10; 标准文献题录著录规则 2987 under 相近标准(计划) 2651; fifth 著录 at 2993 | holds |
| 9 | record page still offers a 查看文本 control (3453) | `查看文本` count 1 at 3453 | holds |

Sweep command in `#### Unknown` reproduced verbatim: `3591 22007` and
`[0,0,0,0,0,0,0,1,2,2,1,3,2,2,5,2,2,1,2]` / `[0,0,0,0,0,0,0,0,1,0,0,0,0,2,1,1,1,0,1]` — identical.
`verified-at` recheck command reproduced: `1 1797 1 15212`. All six quotes also occur in
`corpus/lessons/round-54.md` (counts 1,1,2,2,1,3). `r37` cites no S121 (0 mentions), so the registry
`used-by` naming r36 alone is correct.

**Bonus (out of seat scope, mixed S121/S122 bullets only):** S122 offsets 13300/14082/15188/17078 and
16105/16321/16726/16815/16638 all resolve to the claimed strings in `b9ca2a4fdf9455867534f144.txt`
(22,007 chars, same convention).

## 5. Findings, risks, blockers

- **One overstatement** (prose only, no frozen leg): Observation bullet 2's "neither the designator nor
  the qualifier can be quoted whole as a unique string". The qualifier as printed, `（全部代替）`, occurs
  exactly once and is the quote the lane itself uses; only the bare words `全部代替` repeat. Suggested
  narrowing for the lesson/Gate prose: "the designator repeats; the bare qualifier words repeat, the
  bracketed form is unique". The quoted string, its span at 1082 and its anchor are unaffected.
- **Two precision notes** (no falsification): (a) the entry's source line says "read as UTF-8, 3,591
  characters" without the words "newline normalisation" that `SOURCES.md:131` carries — 3,591 is
  unreachable from the raw bytes (4,468), so the convention is pinned by the count but unnamed;
  (b) `char 575` anchors the field value `国家标准委`, not the phrase start `主管部门为` (569), and
  `char 2993` anchors the fifth `著录`, not the title `标准文献题录著录规则` (2987) — both are
  value-anchored like the rest of the entry, coherent but worth a word if the Gate tightens.
- **Block membership is as claimed**: the 标准状态 block (label 1011) holds the two dates and also two
  empty label rows (上次复审, 废止 at 1075) — empty values, so "in force" is not contradicted by 现行 ×2.
- Blockers: none. Nothing in S121 needed a source outside the capture; no network used; no lane file
  written except this report; the pre-existing `corpus/evidence/round54/__pycache__` was not touched.
- Parent gate to run after integration: `python3 corpus/evidence/round54/c2-count.py` (and
  `--lane-only`) on the landed tip, plus `build-spans.py --check`.

Retained evidence: the inline command outputs above (byte counts, both-convention offset table, NFKC
counts, `uni[off:off+len]==span` ×6, reproduced sweep and recheck lines, S122 offset table).

VERDICT: attacked S121's six quotes, both `char N` sites and nine S121-citing Observation sentences
against the capture under both newline conventions — every quote count/offset/one-line check and every
anchor survived (lane form = newline-normalised 3,591 chars; raw form 4,468 disagrees on all offsets);
only one prose clause overstates uniqueness of the bracketed qualifier, which no frozen leg consumes.

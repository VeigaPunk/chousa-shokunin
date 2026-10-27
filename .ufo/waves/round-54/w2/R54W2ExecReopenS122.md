# R54 W2 — S122 re-open (executor R54W2ExecReopenS122)

Lane tip verified: `git rev-parse HEAD` in `/home/vgpnk/Projects/shokunin/chousa-shokunin` =
`25abbe82b9f2b7c6e24580ac3f028611ba21f01f` (the assignment names `447cf7ed…`; HEAD has advanced by
later W2 integration). Every check below runs on `25abbe82`. Scope: S122 only. No production file
written, no network, no mutating git/jj, no tool installed, `PYTHONDONTWRITEBYTECODE=1`; scratch
`/fast/scratch/hyaku/chousa-r54/R54W2ExecReopenS122/` removed at exit.

## 1. Captures (on-disk campaign cache only)

- Portal form `b9ca2a4fdf9455867534f144.txt`: 22,007 chars / 24,185 B, sha256 `2d68faf7c724eb1baca6c201613cbf0607589ca017153461a9357760d1c8caf1`; `cmp` against its `.raw` → identical, so "the `.txt` is the served HTML" and "that digest is also the `.raw`'s" both hold. CRLF 688, no BOM; offsets below are on the LF-normalised UTF-8 read, the row's "newline normalisation".
- S121 record, for the two cross-page sentences: `adf6ba934e813b2c326fa150.txt` 3,591 chars (sha256 `4e46154f…`), `.raw` 70,132 chars (sha256 `a7b868be…`).

## 2. `quotes.tsv`, the six S122 rows — count / offset / line / match

| quote (truncated) | count | offset | line | slice at offset == quote | cited in anchor | cited in source line |
|---|---|---|---|---|---|---|
| `标准号：GB/T 7714-2025` | 1 | 13300 | 431 | yes | no | yes |
| `英文标准名称：Information and documentation—Rules…` | 1 | 14082 | 460 | yes | no | yes |
| `该标准采用了ISO、IEC等国际国外组织的标准，由于涉及版权保护…` | 1 | 15188 | 491 | yes | yes | yes |
| `2025-12-02` | 1 | 16105 | 523 | yes | yes | no |
| `2026-07-01` | 1 | 16321 | 530 | yes | yes | no |
| `国家市场监督管理总局、国家标准化管理委员会` | 1 | 17078 | 558 | yes | no | yes |

All six: count exactly 1, the recorded offset is the string's start, each on a single line, and the
form slice at the offset equals the quote character for character.

## 3. Every `char N` in the S122 anchor and in the entry's source line

- `corpus/SOURCES.md:132` anchor cell char tokens: `15188, 16105, 16321` — each is one of the six
  quote offsets (`all(... in offsets) == True`). Same cell: `22007 characters` = `len(form)`,
  `sha256 prefix 2d68faf7c724eb1b` = the form's digest prefix.
- `corpus/knowledge/source-type-taxonomy-r36.md:4` source line char tokens: `13300, 14082, 15188,
  17078` — each is a quote offset; union with the anchor covers all six rows, and no token in either
  place points anywhere else.

## 4. The two control claims, read off the served HTML (no fetch)

**4a Portal page shows no preview/download control — HOLDS, with a word-level caveat.**
Rendered DOM: four `<button>` only — navbar toggle (11019), `实施信息反馈`
`class="btn fk_btn btn-sm btn-success app-hide"` (14891; `app-hide` count 1, so hidden), modal close
(17807), `知道了` (18290). No `iframe|embed|object`, no `pdf`, no `<a>` in 13000-17600, only
`onclick` is the footer `Link('bm31370001')` (20181). The words do occur — `预览` ×7, `下载` ×1 — but
only as page-wide script/UI strings: i18n `'preview': '在线预览'` (1624/1626), `'download': '下载标准'`
(1652), `previewTip` (1921/1966), `previewMsg` (`…在线预览服务…全文预览`, 1968/2062), and the hidden
support modal `#myModal` (17994/18104/18200). The script wires `$('.ck_btn').text(currentI18n.preview)`
(3679) and `$('.xz_btn').text(currentI18n.download)` (3723), handlers 3818/3937 — neither class occurs
as an element in this standard's page (`ck_btn`/`xz_btn` only inside that script), so a word grep
returning 7/1 is not evidence of a control. The entry never claims the absence in those words (nearest
lines: the Unknown bullet "no OCR, no preview modal and no 查看文本 target was opened this round", an
action statement, and the anchor's "the notice paragraph standing where a text would be"); in the
strong form the claim survives.

**4b Record page offers a 查看文本 control — HOLDS, and its target is inside these captures.**
`adf6ba934e813b2c326fa150.txt`: `find('查看文本') = 3453`, `txt[3453:3457] == '查看文本'`, count 1 in
that form (0 in the portal form). Raw: `<div class="sidebar-btn openpdf">…<span>查看文本</span></div>`
at 65820-65947; the `.openpdf` handler (68769) opens, desktop branch,
`http://openstd.samr.gov.cn/bzgk/std/newGbInfo?hcno=C6CE52E55AC09B9C79A20AEA77CEDD14` — exactly the
S122 URL — with the app branch on `/bzgk/gb/…`; a script-built `查看全文` button reuses the same
`openpdf` class (67129/67138). So the control is real and clickable and "whose target this round did
not open" is true — but the target needed no fetch to name: it is written in the same served page and
it *is* the portal page the lane already holds. That strengthens the entry's conclusion (the
authority's own 查看文本 leads to the page stating it serves no text); recorded as a missed
strengthening, not an error.

## 5. Every S122 sentence of Observation and Inference

- `r36.md:16` (portal bullet) — **holds** on each part. Record fields present: `标准号` 13300,
  `中文标准名称` 13774 (value `信息与文献 参考文献著录规则`, `著录` at 13794), `英文标准名称` 14082,
  `标准状态` 14278 → `现行` 14510, CCS `A14` / ICS `01.140.20`, `发布日期` label 16016 / value 16105
  (lines 520 vs 523), `实施日期` label 16219 / value 16321 (lines 527 vs 530) — labels and values on
  separate lines, `主管部门` value `国家标准委` 16638, `发布单位` 17078. Notice quote count 1 at 15188;
  the paraphrase ("no text-reading service … for copyright protection") is faithful and the
  sentence's subject is 本系统, not the document.
- `r36.md:17` (归口 body) — **holds**: `归口部门` label 16726, its value line `国家标准委` 16815,
  `主管部门` value `国家标准委` 16638; `国家标准委` count 2, so the bare value is not uniquely quotable.
- `r36.md:16` 著录 sentence, record half — **holds**: `著录` at 354, 521, 1191, 1281, 2993; the title
  `信息与文献 参考文献著录规则` occurs 4× and covers the first four; the fifth is
  `标准文献题录著录规则` at char 2993. Portal half: `著录` count 1 (13794, inside its 中文标准名称).
- `r36.md:16` "in both forms 附录 / 文献类型 / … each 0" — **holds**: the sweep reproduces verbatim
  (§6), and no bracketed document-type code of any shape occurs either
  (`\[[A-Za-z]{1,4}(/[A-Za-z]{1,4})?\]` → `[]` in both forms), so the sentence is stronger than the
  three tokens it prints.
- `r36.md:22` (record fields vs clauses) — **holds**; `r36.md:23` (dates repeat) — **holds**
  (16105/16321; `代替` count 0 in the portal, 3 in the record).
- `r36.md:24` (notice is about the service; 查看文本 at S121 `char 3453`; target unopened) —
  **holds**, and see 4b: the target is the S122 page, which makes the hedge sound rather than loose.
- `r36.md:25` (a field is read where printed) — **holds**; `r36.md:26` (tier is about scope) —
  **holds** (a judgement on the same verified lines; the issuer is the portal's `发布单位`).

No S122 sentence overstates or is wrong.

## 6. Commands re-run, with observed output

- The entry's `#### Unknown` sweep command (copied from the entry) → `3591 22007`, then
  `[0, 0, 0, 0, 0, 0, 0, 1, 2, 2, 1, 3, 2, 2, 5, 2, 2, 1, 2]` and `[0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 2, 1, 1, 1, 0, 1]` — identical to the printed arrays.
- The entry's `recheck:` command → `1 1797 1 15212`, exactly as printed; 15212 = 15188 + 24, and
  `len('该标准采用了ISO、IEC等国际国外组织的标准，')` = 24, so the shorter needle and the full-notice
  offset are consistent, not contradictory.
- Spans, all six S122 rows: exact slice at the recorded offset (`sp == form[off:off+len(sp)]`), digest
  match, quote inside span, span longer than quote, quote inside the entry and inside the lesson,
  ≤25 whitespace words and ≤160 chars — 6/6 on every leg.
- `python3 corpus/evidence/round54/c2-count.py` (full, not `--lane-only`) on the tip: `C2=PASS`,
  `BOUND=3/3`, `QUOTE_ROWS=33 ON_BOUND=33/33`, `SPAN_CONTEXT=33/33`, `CAPTURE_BOUND=33/33`,
  `ANCHOR_BOUND=3/3`, `INFERENCE_GROUNDED=2/2`, `QUARANTINE_VERDICTS=3/3 (S080,S088,S096)`.

## 7. Notes for the L1 (no predicate, target, counter or control touched)

- Wording: `r36.md:4` calls the notice "under the record table"; it is the last row *inside*
  `<table class="tdlist">` (open 13627, close 15422), i.e. at the bottom of that table. Cosmetic.
- `SOURCES.md:132` is titled "国家标准 GB/T 7714-2025 在线预览" while the served page renders no preview control; the phrase describes the portal's function but reads as a promised preview. If the absence should stand on record, the falsifying sentence is §4a.
- The 查看文本 target (§4b) is nameable without a fetch; the SCORECARD/LOG draft could cite it.
- Deliberately unverified (no fetch, L0 `8d77e6c1` open): behaviour after the portal's JS runs, the `/bzgk/gb/` app branch, and whether the portal serves text for a standard that adopts no ISO/IEC document. C1 untouched by this seat.

VERDICT: attacked S122's six quotes, three anchor chars, four source-line chars, six spans, both
control claims and every S122 Observation/Inference sentence against the on-disk captures and the
served HTML — survived; one missed strengthening (查看文本 targets the S122 URL itself) and two
wording notes recorded.

# R57W1RevOrphans — revenger: the three record-less captures (R2/R4/R6 orphan triage)

Seat: revenger (leaf, no dispatch). Item: reverse-engineer the fetch provenance of
`corpus/captures/{53a92273a452a58f28368691,d473754a0cbf8d3095255d5a,d8b4f8f8829b813f16227893}.raw`, identify each
document from its bytes, and measure with the frozen counter's own functions whether each *defined form* can bind
its reference (R2/R4/R6) under R57-C3. Claims frozen (`corpus/evidence/round57/claims.md`): nothing below proposes a
predicate, target, counter or recipe change. Base `6656f077`, tip at dispatch `f9736a39`; no network; no lane writes
outside this file. Tooling: none installed (poppler 26.08.0, the frozen recipe's version, already present).

## 1. Identity from bytes (what each orphan IS)

```
$ file corpus/captures/{53a9…,d473…,d8b4…}.raw ; pdfinfo …
```
| orphan key | `file` | pdfinfo | pdftotext -layout cover / first heading |
|---|---|---|---|
| `53a92273a452a58f28368691` | PDF 1.4, 31 pp | Producer `生产者` (template placeholder), CreationDate `D:20210906154744+08'00'` | 国家卫生健康委员会**公报 2021·07** (TOC: 公告 2021年第6号 … 国卫办药政发〔2021〕16号 … p.21); body p.21 = the 〔2021〕16号 notice; L2307 = `药品临床综合评价管理指南` title page (the R3 attachment) |
| `d473754a0cbf8d3095255d5a` | PDF 1.5, 66 pp | Title `抗肿瘤药物综合评价指南` (truncated), Author `CNHDRC`, Word 2016, 2022-06-28 | `抗肿瘤药品临床综合评价` / `技术指南` / `（2022 年版 试行）`, 国家药物和卫生技术综合评估中心 + 国家癌症中心 + 药具管理中心, 二〇二二年六月 → **R4's document** |
| `d8b4f8f8829b813f16227893` | PDF 1.7, 68 pp | Author `Administrator`, Word 365, 2022-06-22 | `儿童药品临床综合评价` / `技术指南` / `（2022 年版 试行）`, same three issuers, 二〇二二年六月 → **R6's document** |

Raw digests (computed here, cited nowhere else in the lane):
`53a9…=460121b411d754f94c597b8d20066c45901a729c5d88f7f86fb065057cb5da84`,
`d473…=47435e4b36ef7a9755663b77d57df90c5fc0dbba713e6cdce4238592b536da25`,
`d8b4…=1f84ddf0cb9da958658c81b0efdb79308144cdcc5fada97d842f9a7de86021c5`.
Recipe-form digests I regenerated (`pdftotext -layout`, 26.08.0): `c040bc85…0cd8ec3`, `7ea529e5…8b1ee7a3`,
`520f663e…d7de4a56`. Sibling check: `ls corpus/captures/` shows **no `.txt`, no `.fail`** for any of the three.

## 2. Record of their fetch — searched, and (almost) absent

Ran: `grep -rln <key> --exclude-dir=captures --exclude-dir=.git .` (whole lane), `awk -F'\t' '$1=="S135"||$1=="S136"' corpus/evidence/round57/refetch.tsv`, `git log --oneline -- corpus/captures/<key>.raw`.
- All three raws: **one** commit, `b022b13 hyaku run9 wrap-up: remaining round-57 captures` (L1 "wrap-up",
  04:47:05 -03; inode mtimes 03:21/03:23/03:24; ancestor of the dispatch tip). No commit body, note or log line
  records the fetch command, URL or digest for them.
- Text hits for a key: only this wave's `.ufo/waves/round-57/{w1-spec.json,gen-w1-spec.py,w1-dispatch.json,
  w1/swarm-registry.json}` (seat text), `w1/R57W1ScoutR3.md`, `w1/R57W1ScoutR2Gaz.md`, `w1/R57W1ReviewCaptures.md`,
  plus jj op-store blobs. **No fetch log.**
- `refetch.tsv` (115 data rows): `d473…` = S135 attempt 1 `08:37:14Z rc=28 http=200 raw=-` and attempt 2
  `08:38:32Z rc=28 raw=-`; `d8b4…` = S136 the same (rc=28, raw=-); **`53a9…`: zero rows** — neither its key
  nor its URL (`…5e18d6d8d86e405bad64dd4a8b666310…`) appears (`grep -c` = 0).
- `tools/capture-fetch.py:143-147,117-119` writes `.raw` **and** `.txt` only when `rc==0` and 2xx and the body is
  non-empty; a failed attempt stores nothing. These bytes therefore cannot come from the campaign tool at all —
  they predate their own attempt rows (03:2x vs 08:3xZ) and are ≤ the failure records.
- Precedent: `e0e73e0` deleted the record-less S105 raw (`e3ca8f4f…`, added by `b022b13`, removed by `e0e73e0`) and
  named it; these three, same commit, same missing row, were left. C2 unaffected either way (§4).

## 3. Heading probe — the frozen rule's own functions, on each orphan's defined form

Imported the frozen counter unmodified (`importlib` → `c3-count.py`) and called `heading_title(form,title)` /
`token in nows(form)` on the recipe form (`/fast/scratch/hyaku/chousa-r57/R57W1RevOrphans/*.txt`, `pdftotext -layout`, 26.08.0):
| orphan | ref | title / token (REFS) | `token in nows(form)` | `heading_title(form,title)` |
|---|---|---|---|---|
| 53a9 gazette | R2 | 关于规范开展药品临床综合评价工作的通知 / 〔2021〕16号 | **True** | **False** |
| 53a9 gazette | R3 | 药品临床综合评价管理指南 / 2021年版 | **True** | **True** (L2307) |
| d4737 | R4 | 抗肿瘤药品临床综合评价技术指南 / 2022年版 | **True** | **False** |
| d8b4f | R6 | 儿童药品临床综合评价技术指南 / 2022年版 | **True** | **False** |

Why the three False — the title is split at the PDF's own line level, and `nows()` only removes whitespace
*inside* a line (`c3-count.py:91-92`), while `heading_title` iterates `form.splitlines()` (`:151-161`):

```
53a9 L2260 '      国家卫生健康委办公厅关于规范开展药品临床综合'
53a9 L2261 '                     评价工作的通知'          # TOC at L22/L24 splits too
d473 L1 '抗肿瘤药品临床综合评价'  L2 '    技术指南'        # bbox: y=207.09 vs 253.89, 26 pt, two runs
d8b4 L1 '儿童药品临床综合评价'    L2 '    技术指南'
```
Control that isolates layout from rule: a one-line cover built from the same words passes —
`heading_title('抗肿瘤药品临床综合评价技术指南（2022 年版 试行）', title) = True` (and `True` for the 儿童
string). For the gazette, a one-line body heading would also pass (prefix `国家卫生健康委办公厅` = 10 chars
≤ 16); the gazette simply prints it two-column. The break is in the typeset file (two baselines), so **no
renderer fixes it — only different bytes do**; `R57W1ScoutR6.md:15-17` reports the official nhei/cpia covers
show the same split, so mirrors of that file will fail alike.

## 4. URL re-derivability

- `d4737` → `https://www.hnysfww.com/data/article/1656481023744041713.pdf`, `d8b4f` →
  `…/1656481067585283603.pdf`: sha256(url)[:24] recomputed here and **equal to the keys**, and the hrefs sit
  in S134's committed, *successfully refetched* page (`9695437…` row rc=0 200 raw=84df89a7…; page title
  `心血管病、抗肿瘤、儿童药品临床综合评价技术指南`, `txt:189,192`, issuer text `txt:180`). Provenance chain is solid.
- `53a9` → `https://www.nhc.gov.cn/bgt/201807sgf/202109/5e18d6d8d86e405bad64dd4a8b666310/files/1733795726978_35780.pdf`
  (`R57W1ScoutR3.md:22`); sha256(url)[:24] recomputed here = `53a92273a452a58f28368691`, so the scout's key
  claim is machine-confirmed. The URL exists only in that scout report — no machine fetch record anywhere.
- C2 unaffected: `python3 corpus/evidence/round57/c2-count.py --verbose` → `SET=47 VERDICTS=47/47 REPRODUCED=41
  DRIFTED=5 UNREACHABLE=1 BYTE_BACKED=46 CONSISTENT=46/46 FLAGGED=0/0 C2=PASS`, exit 0 — none of the three
  keys is in the pinned 47, and the counter passes with all three on disk.

## 5. Verdicts

| orphan | document | under frozen R57-C3 |
|---|---|---|
| `53a9…` gazette | R2's notice **and** R3's guideline attachment, reprint | **NOT bindable as-is** (no successful row, no `.txt` → `good_raw` miss and `form_of`→None). Document-level: **R2 = needs a different served copy** (heading split; only a one-line header works); **R3 = the one live path** — heading+token both pass on these very bytes, so a single successful `capture-fetch.py` attempt returning identical bytes (`raw=460121b4…`, `txt=c040bc85…`), a Registry row X with this URL, and ≥2 manifest rows would bind R3 without new bytes. |
| `d4737…` | R4 correct (66 pp, 二〇二二年六月) | **needs a different served copy**: provenance is fixable (URL proven via S134), but these bytes can never pass `heading_title` (authored two-line cover). Do not spend a C3 fetch on hnysfww for R4 unless a page-form is intended. |
| `d8b4f…` | R6 correct (68 pp) | Same: provenance fixable (URL + `nhei.cn` official candidate `52f3bf65…` already rowed failed), heading fails on this typesetting; scout snippet evidence says the official file splits identically → prefer an HTML/other-typeset carrier. |

Actionable, in one sentence: **no orphan is bindable as-is; the gazette is the only one whose *own bytes*
satisfy a reference's title+token (R3), and every bind still needs one successful attempt row for its
`(id,url)` with the digest above (or fresh bytes that replace it), because `c3-count.py:189-190` compares
`good_raw[(id,url)]` to `sha256(<key>.raw)`.**

## 6. What I attacked, and what survived

- **"The wrap-up captures are documented."** Falsified: no commit body, log, tsv row or digest for any of the
  three; the three digests occur nowhere in the lane's text files but this report and the peers' files.
- **"S135/S136 rows attest the guide PDFs."** Falsified: both rows are `rc=28` failures with `raw=-`;
  `capture-fetch.py` stores nothing then, so the on-disk bytes are evidence *of a different fetch path*, not of
  these rows.
- **`R57W1ScoutR3.md:22` claim "heading likely printed but line-wrapped by layout (wraps join under
  ws-removal)"** — falsified for R2 (measured False; `nows` is intra-line) and right only accidentally for R3
  (the attachment's own bare title line, not a wrap-join). `R57W1ScoutR2Gaz.md:19-24` had it right.
- **"The orphan census is C2-relevant"** — falsified: 47/47 verdicts, CONSISTENT 46/46, `C2=PASS` with the
  three files present and none pinned.
- Survived: the frozen counters' separability and the C3 binding requirement (provenance ≢ content — an
  identical-bytes re-fetch alone legitimizes held bytes; different bytes would not).

Scratch: `/fast/scratch/hyaku/chousa-r57/R57W1RevOrphans/` (three pdftotext forms, bbox/raw probes);
`rm -rf` run before yield, nothing written outside this report.

VERDICT: attacked the provenance and title-bindability of the three record-less round-57 captures — all three
fail the frozen C3 as-is (no successful refetch row, no `.txt`), R2/R4/R6 also fail `heading_title` on their
own typesetting, and only the gazette's bytes satisfy R3 (heading+token True) once provenance exists; findings
survive, no claim touched.

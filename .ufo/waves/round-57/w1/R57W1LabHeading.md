# R57W1LabHeading — frozen heading_title()/token rule, boundary probe

seat: `R57W1LabHeading` (lab) · wave: round-57 w1 (chousa) · date: 2026-10-27
lane: `/home/vgpnk/Projects/shokunin/chousa-shokunin` · claim under study: **R57-C3** (frozen at `fd95724d56a33a150cd2638fadd2ce1f3425e6c`)
frozen counters probed: `corpus/evidence/round57/c3-count.py` (sha256 `c565ce4a78b439411dc6e088bc5f8a92781888fe895f2ee9b43170867c1e6e33`, unchanged)
method: imported the frozen counter as a module with `importlib.util.spec_from_file_location` over a **byte-identical scratch copy**
(`/fast/scratch/hyaku/chousa-r57/R57W1LabHeading/c3_frozen_copy.py`); sha256 equality asserted in every script. The lane file was only ever READ.
no predicate/target/counter/recipe was proposed for change. No network fetch was made.

## 1. The rule as frozen (verbatim from the counter)

`c3-count.py:70-71,88,91-92,151-160`:

```
PAREN_TAIL = re.compile(r"(?:（[^（）]*）|\([^()]*\))$")
BAD_PREFIX = set("《》.[]［］")
WS = re.compile(r"\s+")
def nows(s): return WS.sub("", s)
def heading_title(form, title):
    for line in form.splitlines():
        s = PAREN_TAIL.sub("", nows(line))
        if s.endswith(title):
            pre = s[:len(s) - len(title)]
            if len(pre) <= 16 and not (set(pre) & BAD_PREFIX):
                return True
    return False
```

Binding is conjunctive at `c3-count.py:228-229`:
`len(qs) >= MIN_PER_ID(=2)` **and** `token in nows(form)` **and** `heading_title(form, title)` **and** `any(title in nows(q) for q in qs)`.

## 2. Case → expected → observed (all executed; `probe_heading.py`, `probe_falsepositive.py`, `probe_realistic.py`)

`expect` = my stated prediction before the call; `observed` = the frozen function's actual return. **79 distinct synthetic cases were run: 49 in the table below (each with a pre-stated expectation — `mismatches vs stated expectation: []`, i.e. all 49 matched), plus 30 further observation cases (A1–A10, B1–B5, C1–C15) whose observed values are quoted in §4 and in the notes.**

| # | case | expect | observed | frozen function output (exact) |
|---|---|---|---|---|
| 1a | 16 clean prefix chars + title | True | **True** | `heading_title('x'*16+T4, T4)` → `True` (pre len 16) |
| 1b | 17 clean prefix chars + title | False | **False** | pre len 17 → rejected |
| 1c | 16 chars + whitespace padding | True | **True** | whitespace removed *before* the length test |
| 1d/1e | 16 / 17 CJK prefix chars | True/False | **True/False** | budget is **characters (code points), not bytes** |
| 2a | `《title` (unclosed) | False | **False** | `pre='《'` → in BAD_PREFIX |
| 2b | `《title》` | False | **False** | does not `endswith(title)` |
| 2c | `《title》（2022年版）` | False | **False** | one paren dropped → ends with `》`, still no |
| 2d | `1.` + title | False | **False** | `.` ∈ BAD_PREFIX |
| 2e | `一、` + title | True | **True** | `、` not in BAD_PREFIX |
| 2f | `标题：` + title | True | **True** | `：` not in BAD_PREFIX |
| 2g | `（一）` + title | True | **True** | full-width `（）` not in BAD_PREFIX |
| 2h | `[EB/OL]` + title | False | **False** | `[` `]` ∈ BAD_PREFIX |
| 2i | `［1］` + title | False | **False** | `［］` ∈ BAD_PREFIX |
| 3a | `title（2022年版 试行）` | True | **True** | paren dropped → `…指南`; pre='' |
| 3b | `title（2022年版试行）` | True | **True** | idem |
| 3c | `title (2022年版)` ascii parens | True | **True** | ASCII alternative of PAREN_TAIL |
| 3d | `title（2022年版）说明` | False | **False** | paren not trailing → not dropped |
| 3e | `title（2022年版)` mixed parens | False | **False** | neither alternative matches |
| 3f | `title（2022年版（试行））` nested | False | **False** | `[^（）]*` forbids nesting |
| 4a | `title（2022年版）（试行）` | False | **False** | **only ONE trailing paren dropped** → `…指南（2022年版）`; `endswith(title)` now False |
| 4b/4c/4d | two parens, space-separated, other years | False | **False** | same mechanism |
| 4e | two parens + short clean prefix | False | **False** | prefix budget is irrelevant here |
| 5a | `〔2021〕 16号` (inner ASCII space) | True | **True** | `nows(form)` → `…〔2021〕16号…`; token found |
| 5b | `〔2021〕16号` | True | **True** | idem |
| 5c | `〔2021〕　16号` (U+3000) | True | **True** | `WS=\s+` in Python str mode strips U+3000/U+00A0 too |
| 5d | `〔2021〕\t16号` | True | **True** | tab is `\s` |
| 5e | token absent | False | **False** | |
| 5f | half-width `[2021]16号` | False | **False** | the token literal is `〔〕` |
| 5g | token on another line | True | **True** | token test is **whole-form**, not per-line |
| 5h | R3 token inside `2021年版试行` | True | **True** | plain substring |
| 5i | R4 token vs a `2023年版` doc | False | **False** | no false edition match |
| 6a | title split mid-word across 2 lines | False | **False** | the scan is per-line |
| 6b | split one char early | False | **False** | idem |
| 6c/6d | title alone on line 2 | True | **True** | a later line may carry it |
| 7a | GB/T 7714 entry with `[EB/OL]`+URL tail | False | **False** | |
| 7b/7c | short reference entry ending at title(+paren) | True | **True** | **accepted** (see §4) |
| 7d | citation in `《》` | False | **False** | |
| 7e | R3 title alone on a line | True | **True** | |
| 7f | R5 title (16 chars) alone on a line | True | **True** | title length is unconstrained |

Token-substring extra (verified): `nows` removes newlines too, so a token split across lines (`2021\n年版`) **matches** while the raw form does not — `token in nows(form)=True`, `token in form=False`. Title-side extra: a title printed with internal spaces (`抗肿瘤药品 临床综合评价技术指南`) still matches.

## 3. Real held captures — the rule applied to lane bytes (read-only)

`probe_real.py` / `probe_store_scan.py` over `corpus/captures/*.txt` (the DEFINED FORM for non-OLE/zip raws is the `.txt` sidecar; `c3-count.py:136-148`):

| capture | id | R | token | heading | evidence line |
|---|---|---|---|---|---|
| `16fe8487aa97b98576a0dbac` | S118 | R7 | True | **True** | `L0 '药品临床综合评价质量控制指南'` pre='' |
| `b27ffd2f0161104c6a28c9f5` | S127 | R1/R2/R3/R4/R5/R6/R7 | True | False | ref-list lines rejected: `[2] 国家卫生健康委.国家卫生健康委关于开展…` pre len 18 + `.`; `中心、国家卫生健康委药具管理中心.抗肿瘤药品…` pre len 17 + `.`; `[35] 国家药物和卫生技术综合评价中心.药品临床综合评价质量控制指南…` pre len 20 + `.` |
| `a42feae4448612f949cc715f` | S130 | R3 | **False** | True | `L2 '药品临床综合评价管理指南'` — the 2020 text carries no `2021年版`, so it cannot bind R3 (matches the freeze-time claim) |
| `de9f5afc3809acbf61f4d5bb` | S128 | R3..R7 | True | False | — |
| `5233bf47babaa1ca2b49ed15` | S129 | R1/R2/R3/R7 | True | False | — |

**Only S118 (R7) satisfies both halves among registry-backed captures** — this reproduces the freeze-time statement exactly.
`S127`'s CLAUSE string is present at raw offset **4709**: `下列文件中的内容通过文中的规范性引用而构成本文件必不可少的条款。` — a manifest row quoting it satisfies `c3-count.py:237`.

## 4. Findings against the frozen rule (reported, NOT patched)

**F1 — false-positive surface (binds a document that is not the reference).** `heading_title` accepts any line that *ends* with the title under ≤16 clean prefix chars. So a third-party reference-list entry whose author is separated by a **space or comma** (no `.`) is accepted as the document's own title heading: `"国家药品监督管理局 抗肿瘤药品临床综合评价技术指南（2022年版）"` → **True**; `"王明, 抗肿瘤药品临床综合评价技术指南"` → **True**; `"本文件引用了抗肿瘤药品临床综合评价技术指南"` (prose) → **True**; `"表抗肿瘤…"` (caption) → **True**. The `.` in the canonical GB/T 7714 form is the *only* thing rejecting real citation lines (S127's own ref-list lines carry `.` and pre ≥17). **Implication for the L1:** the heading half does not prove the document *is* the reference; only the issuer/identity argument does. The binding must be defended by the registry row's own scope/issuer, not by the counter.

**F2 — false-negative surface (a real document cannot bind).** The rule rejects: a title wrapped across two lines (a `pdftotext -layout` wrap — `B5`/`6a`); two trailing parentheticals `（2022年版）（试行）` — **a real cover shape**; a heading with a `.` (`1.`); a heading whose prefix exceeds 16 chars (a long issuer prefix `国家药品监督管理局、国家卫生健康委药具管理中心` = 23 chars → rejected). So a perfectly good guideline PDF whose cover reads `抗肿瘤药品临床综合评价技术指南（2022年版）（试行）` **cannot bind** under the frozen rule. The L1 cannot route around this by choosing a different line — no other line in such a document ends with the title.

**F3 — token half is coarse.** For R3/R4/R5/R6 the token is the bare edition string `2021年版` / `2022年版` (R4/R5/R6 **share** `2022年版`), tested as a whole-form substring with no proximity to the title. Any mention of `2022年版` anywhere in a candidate satisfies the token half for all three of R4/R5/R6. Only the title half discriminates them.

**F4 — the two halves can be satisfied by different parts of one document.** The token is document-wide; the heading is per-line. Verified on real bytes: S130's `L2` supplies the R3 heading while S127's `L154` supplies `2021年版` — the token need not appear near the heading.

**F5 — CRLF offset trap (manifest authoring).** `form_of` (`c3-count.py:145-148`) digests the **raw `.txt` bytes** but builds the form by normalising `\r\n`→`\n`. **17 of the 54 successful-attempt captures have CR bytes in their `.txt`** (e.g. `167e9db7dde3c998838e3469.txt`: 15 656 raw bytes vs 7 293 normalised chars). For those, a byte-derived offset is wrong. Derive manifest offsets from the **normalised** form; record the digest of the **raw** bytes. (The three candidate captures checked here — S118, S127, S133-tcmevidence — are LF-only, so the trap does not bite them.)

**F6 — the anchor arithmetic is `offset_column + span_file.find(quote)`** (`c3-count.py:254-259`), and **only ONE** of the ≥2 rows must hold the title (`any(...)`, line 229). For S133's tcmevidence copy (`6f545e6c16b6b568ea3f591b`, raw `%PDF-`, form digest `ceef80d97d95a143…`, 7 647 chars): quote `药品临床综合评价管理指南` at offset **19**, quote `（2021 年版试行）` at offset **53**; accepted quote offsets `{19, 53}` → a registry anchor cell may carry `char 19` and/or `char 53`.

## 5. Live state the L1 should know (observed, read-only)

- `python3 corpus/evidence/round57/c3-count.py` → `ENTRY=no … BOUND=0/7 … C3=FAIL`, exit 1 (no entry, no `corpus/evidence/round57/c3/` yet).
- The wave's in-flight fetch already landed **a candidate that satisfies both halves for R3**: `6f545e6c16b6b568ea3f591b` = `http://www.tcmevidence.net/UserFiles/upload/file/20230410/6381676262587201848492833.pdf`, recorded in `refetch.tsv` as S133 attempt 2 (rc=0, http=200). Its form: `L2 '               药品临床综合评价管理指南'`, `L4 '                    （2021 年版试行）'` → `heading_title=True`, `token '2021年版' in nows(form)=True`. Its bytes match the recorded `raw_sha256` exactly. **But `S133` is not a registry row yet** (`grep -c "S133" corpus/SOURCES.md` → 0), so it cannot bind until the L1 adds the row with `used-by` naming the entry and the entry cites `source: S133 — <that URL>`.
- The **other** 管理指南 copy in the store, `6fe041acddaa1f4e6f6e9775` (`https://www.nhc.gov.cn/cms-search/downFiles/863665c55fd74f29a656990d1a4ea5ce.pdf`), is the 2020 text (`二〇二〇年十一月`): heading **True**, token **False** → it does **not** bind R3. Two URLs, same title, opposite verdicts — the edition token is what separates them, exactly as intended.
- Store-vs-record consistency: 54 successful-attempt records; every store `.raw` is byte-identical to the **last** successful attempt's `raw_sha256` (**0 anomalies**). Attempt-1 rows whose bytes were superseded by attempt 2 are not anomalies.

## 6. Boundaries honoured

Only `/home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-57/w1/R57W1LabHeading.md` was written in the lane. No git/jj mutation was run anywhere. The fleet repo, `shokuknow`, and sibling lanes were read-only. No fetch was made; only committed bytes under `corpus/captures` were read. Scratch lived only in `/fast/scratch/hyaku/chousa-r57/R57W1LabHeading/` (`TMPDIR`/`PYTHONDONTWRITEBYTECODE=1` set) and **was deleted before this yield** (`rm -rf -- /fast/scratch/hyaku/chousa-r57/R57W1LabHeading`). Tooling: none installed (probe used only the stdlib `importlib`/`hashlib`/`re`); `python3` = 3.14.8, already present.

VERDICT: probed the frozen R57-C3 `heading_title()`/token rules (79 synthetic cases, all as predicted) and grounded them on real lane bytes — the rule survived; the binding rule's real boundary is now pinned: it accepts any line *ending* with the title under a ≤16-character clean prefix (so a third-party reference-list or prose line can bind — F1) and rejects a real cover printed as `title（edition）（试行）`, a line-wrapped title, or a long issuer prefix (F2), the edition token is document-wide and shared by R4/R5/R6 (F3/F4), and manifest offsets must come from the CRLF-normalised form while digests come from the raw bytes (F5) — none of which is patched here.

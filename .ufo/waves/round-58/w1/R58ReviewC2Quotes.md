# R58ReviewC2Quotes — round-58 C2 frozen S101 quote-set audit

Seat scope: independent verification of the 12 frozen S101 quote strings for uniqueness, exact offsets, and text-form boundaries, plus the committed raw digest and capture-text pin. No fetch; lane read-only. Scratch `/fast/scratch/hyaku/chousa-r58/R58ReviewC2Quotes/` (copies of capture, capture-text.py, quotes.tsv, c2-count.py), removed after use.

## 1. Frozen artifact integrity (freeze commit → worktree)

`git cat-file -t 9e73a031ab1ac3bac343de008850d7d87f9e5634` → `commit`; `git merge-base --is-ancestor <freeze> HEAD` → 0 (ancestor). Worktree HEAD is `718e8d20779427dc011ab211d69093160e2367cc` (wave in flight); `git status --porcelain` shows only untracked `?? .ufo/waves/round-58/` and `?? corpus/evidence/round58/controls/c2-before-frozen.txt` — no tracked file is dirty.

Worktree `git hash-object` output is byte-identical to `git ls-tree <freeze>` blobs for all five frozen artifacts:

- `corpus/captures/6dc68fd6b32ce9c8dfcebce8.raw` — blob `ced3a02e`; `sha256sum` → `6063a3aff7a4081e93a685f2721e2cd6b477ba84a841211e298bcddd6d9fddf3` == claims RAW_SHA. 129024 B. First bytes `d0 cf 11 e0 a1 b1 1a e1` = OLE magic → capture-text `.doc` branch.
- `tools/capture-text.py` — blob `43931ddd`; `sha256sum` → `2c0140bc04029c8faedc6c89a65bd657430d8b85f433406946567b70303e2573` == claims CT_SHA == counter `CT_SHA`. Pure-Python, no external binaries/network observed in source.
- `corpus/evidence/round58/c2-count.py` — blob `7352baee`; `corpus/evidence/round58/c2/quotes.tsv` — blob `7fc406d4`; `claims.md` — blob `2e5e1c71`.

`corpus/evidence/round58/c2/` contains only `quotes.tsv` (2686 B): no `spans.tsv` manifest exists yet (pre-data). All offsets below are this seat's independent computation against the pinned text form, for later comparison with the wave manifest.

## 2. Defined text form

Command (scratch copies, scratch TMPDIR): `TMPDIR=$S python3 -B $S/capture-text.py $S/6dc68fd6b32ce9c8dfcebce8.raw > $S/form.txt` → `rc=0`, stderr empty. Form: 47,356 UTF-8 bytes / 27,012 chars; `sha256 a8e3e7ad213b6ec50479542cda23612e7ae7ae5fd4506fba53a91f2f7e79f867`.

## 3. quotes.tsv structure vs frozen counter

- 13 LF lines, trailing newline; header byte-exact `id\turl\tquote\tentry`.
- 12 data rows, 4 tab fields each; every row `id=S101`, `url=<frozen URL>`, `entry=corpus/knowledge/carrier-alphabet-china-r58.md`.
- No duplicate quotes; no tab/CR/LF inside any quote string.
- TSV quote column == `c2-count.py` `QUOTES` list, order-exact and byte-exact (verified by importing the counter copy), including U+FF0E fullwidth dots in `1．2`, U+2013 en-dash in `CD–ROM`, U+2014 em-dashes, U+FF1B `；`, U+FF1A `：`, U+FF0C `，`.
- `载体类型标识` occurs exactly once in quotes.tsv, inside row 7 `并以[文献类型标识/载体类型标识]表示`.

## 4. Per-quote binding in the pinned text form (str/char offsets, counter's unit)

| # | offset | occur | line-start | line-end | prev | next | verdict |
|---|--------|-------|------------|----------|------|------|---------|
| 1 | 315   | 1 | yes | yes | `\n` | `\n` | PASS |
| 2 | 330   | 1 | yes | yes | `\n` | `\n` | PASS |
| 3 | 590   | 1 | no  | yes | `，` | `\n` | PASS |
| 4 | 683   | 1 | no  | no  | `当` | `。` | PASS |
| 5 | 734   | 1 | no  | no  | `：` | `，` | PASS |
| 6 | 781   | 1 | no  | no  | `，` | `，` | PASS |
| 7 | 797   | 1 | no  | no  | `，` | `包` | PASS |
| 8 | 838   | 1 | no  | yes | `：` | `\n` | PASS |
| 9 | 965   | 1 | no  | yes | ` `  | `\n` | PASS |
| 10| 993   | 1 | yes | yes | `\n` | `\n` | PASS |
| 11| 1460  | 1 | no  | yes | `.`  | `\n` | PASS |
| 12| 11723 | 1 | no  | yes | `)`  | `\n` | PASS |

Probe method: `re.finditer(re.escape(q), form)` on the generated form; identical occurrence rule to the frozen counter (`len(occurrences)!=1` → CAPTURE_BIND).

- Uniqueness: all 12 occur exactly once → each binds a single exact offset; zero FAILs.
- Line-start anchors: rows 1, 2, 10 → 3 anchors, meets the frozen ≥3 floor.
- Boundaries: 9/12 end at line end (all but #4–#7); mid-line quotes are flanked by CJK punctuation/context chars (`当`, `。`, `：`, `，`, `包`), never mid-alphanumeric-token → no ambiguous substring matches.
- No quote is a substring of another; no two quotes can collide at one offset.

## 5. Registry context (observed, not seat-scored)

`corpus/SOURCES.md:111`: `| S101 | 中国学术期刊（光盘版）检索与评价数据规范（修订本）— copy hosted by 哈尔滨工业大学 — <frozen URL> | docs | B | … | mined | 2026-10-25 | 180d | corpus/knowledge/citation-count-semantics-r37.md |` — 11 cells, cells[7]=`mined`; `used-by` names only the round-37 entry (appending the r58 entry is executor wave data, not yet present).

## 6. Residual risk / gaps

- **Offset unit flag.** Recorded offsets are `str` char offsets (the frozen counter's unit — `re.finditer` on the str form). A manifest written with byte offsets would fail `CAPTURE_BIND` (e.g., row 1: char 315 vs byte ~345+). Note the round-49 SOURCES row records "located quotes char … 34374" though the pinned form has only 27,012 chars — lane history already shows a char/byte ambiguity; executors' spans.tsv must use char offsets to match the counter.
- `c2-count.py` full predicate: unrun by this seat (requires executor `spans.tsv`/entry/`used-by` — none exist pre-data). Counter's occurrence rule was reproduced independently, not executed.
- Span-file contents (`form[off-80 : off+len+80]`), rebuild byte-compare, substance/inference-ground: wave data, unrun.
- Round-57 r2 egress-scope L0 question: untouched; no fetch performed.

VERDICT: the frozen S101 quote set (12 strings: uniqueness, exact char offsets, text-form boundaries) and the committed raw digest `6063a3af…` / capture-text pin `2c0140bc…` — survives; all 12 quotes independently verified against the pinned `.doc` text form with zero mismatches.

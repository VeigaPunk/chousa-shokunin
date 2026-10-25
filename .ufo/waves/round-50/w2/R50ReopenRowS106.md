# R50ReopenRowS106 — re-open Registry row S106

Attacked: row `S106` in `corpus/SOURCES.md` (line 116) vs capture `28750bcdf5d36cd90a7709fb.txt` and CORPUS.md SOURCES contract v1. Commands run from lane root unless noted.

## Structure (contract: 11 cells, enums, no `|` in cell)

- `awk -F'|' 'NR==116 {print NF}' corpus/SOURCES.md` → `NF=13` = 11 cells. `kind=docs` (a vendor manual — in enum), `tier=B`, `status=mined`, `opened=2026-10-25`, `recheck=180d`, `used-by=corpus/knowledge/citation-matching-semantics-r41.md`. No `|` inside any cell.

## Capture identity

- `sha256(url)[:24]` computed → `28750bcdf5d36cd90a7709fb` = capture key ✓.
- `wc -c` → 63869 bytes; python `len` → **30937 chars**, matching anchor's "the .txt, UTF-8, 30937 characters" and "captured 2026-10-23" (revision/capture date present ✓). Section names present: "title block", "§2.6 仅去除第一作者本人文献"; the heading `2.6 仅去除第一作者本人文献` exists in the capture (span S106-2 and text near offset ~22500).

## Located quotes — all three verified at char offsets

| anchor offset | quote | len | words | occurrences |
|---|---|---|---|---|
| char 83 | 产品名称：“中国知网”大学生论文管理系统使用手册 | 24 | 1 | exactly 1, found at char 83 |
| char 22511 | 在创建文件夹页面中第一个选项为“仅去除第一作者本人文献” | 28 | 1 | exactly 1, at char 22511 |
| char 22549 | 该文件夹下的所有检测文献在去除本人文献检测结果中 | 24 | 1 | exactly 1, at char 22549 |

All ≤25 words and ≤160 chars, exact-once in .txt, offsets reproduce. Same offsets cited in r41 `source:` line and lesson quote table (lesson lines 111–113). Manifest `quotes.tsv` lines 54–56 carry the same quote strings.

## `scope` and `teaches` grounded

- scope "仅去除第一作者本人文献 is a folder option of its detection flow": capture at char 22511 states the option is `在创建文件夹页面中第一个选项` (folder-creation page), its effect is on 去除本人文献检测结果 similarity ratios — within the 检测 (detection) flow. ✓
- scope/teaches "no 引文核对 section / 0 occurrences": `s.count('引文核对')` → **0**; additionally `核对`=0, `匹配`=0, `辅助`=0, `查重`=0. `引文` alone occurs 10 times — all inside the report-sheet name `标明引文）报告单` (chars 3509, 13948, 19247, 20218, 21064, 21085, 21112, 21283, 21373, 21618), a named output of the detection flow, not a section. The row scopes this to "this copy only" — correctly hedged since it is a mirror of unknown provenance. ✓
- teaches "documents the option as a folder property ... and carries no 引文核对 text (0 occurrences in this copy)" — both halves verified.

## `used-by` exactness

- `grep -rn 'source: S106' corpus/knowledge` → exactly one hit: `citation-matching-semantics-r41.md:4`. `used-by` lists exactly that file. Other corpus mentions (README.md:1077 a table row, lesson) are not `source:` citations — contract asks for citing entries only. ✓ mined status justified (≥1 path).

## Tier challenge (C staged → B landed)

- Staged S136 (merge/chousa/SOURCES.append.md:61) carried tier **C** with "**negative scope only** … flip to B if a CNKI manual with a 引文核对 section is found and opened". The 管理员 manual (landed S105) is that manual and was opened (capture e3ca8f…): the flip condition fired, and the staged row named its own rule — the flip is not gate-keeper discretion.
- A reviewer could still argue **A**: scope is scoped to "what this copy states", and the copy itself is the primary artifact for that scope. But A is claimed for "primary or authoritative" sources; this is a third-party university mirror (`rwxy.seu.edu.cn`) of a vendor PDF, fidelity unverifiable — the same reasoning the lesson applies to S105 ("the content is the vendor's, the carrier a university file host, so B", lesson line 132). Consistent treatment ⇒ **B is correct, A defensible but less calibrated**.
- C would now violate the contract ("never sole support for an admitted entry") — S106 is sole support for r41's 子账号 claims, including the positive folder-option statement. B stands.

## spans.tsv offset check — flag raised then retracted

`spans.tsv` rows 54–56 give offsets **3 / 22431 / 22469** — first read as char offsets these looked 80 short, but that is the designed CONTEXT window, not a defect: `build-spans.py:44` `CONTEXT = 80`, `:119` `start = max(0, off − CONTEXT)`, docstring lines 17–18/25 spell out `offset = span's start` and `anchor char N = offset + quote's position in its span`. Re-verified on all three S106 spans: `form[offset:offset+len(span)] == span_file` exactly, quote at span-index 80 each time, `offset + 80` = 83 / 22511 / 22549 = the anchor chars. No defect; the bare column header `offset` (vs entries' `char N`) is a naming note only. Flag raised here was retracted after peer `R50ReopenRowS105` pointed at the docstring.

## Verification gaps

- Did not re-run `pdftotext` (capture is the authoritative .txt; live fetch prohibited by L0 `8d77e6c1`).
- `opened 2026-10-25` is the adoption date; staged opened was 2026-10-24 — disclosed in the lesson ("staged opened dates 2026-10-23 and 2026-10-24 replaced by 2026-10-25"). Acceptable.

VERDICT: row S106 sound — 11 cells, grounded anchor (83/22511/22549 all located, unique, in-limit), scope/teaches verified against the capture (0 引文核对; folder-option claim grounded), used-by exact, tier flip C→B executed per the staged row's own condition and B is the calibrated tier; the spans.tsv offset flag was retracted after re-verification showed the −80 is the designed CONTEXT window, not drift.

# QuarantineS105 — hand-check of chousa register row S105

Row under check: quarantine-slice line 12 (`S105  payload-absent`), matching
`/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/absent-defect-register.md:48`.

## Verdict: absent-as-written (not fabricated; a misquote of a real PDF table cell)

The row's three quoted spans are not verbatim in the local capture of the cited
URL under the frozen STRICT test (NFKC + whitespace collapse, case-sensitive):
**0/3 quotes located**. The quoted content is not invented — the third quote's
substance is in the cited PDF, split across two rendered lines by the two-column
`pdftotext -layout` output. Committed verdicts agree: round-42
`corpus/evidence/round42/quarantine-verdicts.tsv:13` = `absent` (same LCS
numbers as mine), round-43 `corpus/evidence/round43/absent-split.tsv:9` refines
to `misquote` (17/24). Not unreachable, so not unverifiable; not verbatim, so
not present.

## Register row (exact text)

`absent-defect-register.md` line 48:

| lane | round | id | class | locator | quotes (`<br>`-separated) |
|---|---|---|---|---|---|
| `chousa` | round3 | S105 | `payload-absent` | https://jaohfa.com/pdf/systematic_review.pdf | `情報源［Informationsources］6 全てのデータベース、研究登録、Webサイト、組織、文献リスト、研究を特定するために` (66 chars) · `and not, as a search engine's rendering of the same form has it,` (64 chars) · `それぞれの情報源が最後に調べられた日付を記載する` (24 chars) |

Register note: "cited source, companion URLs and local artifacts were all
checked; the quote is in none of them".

## Lane SOURCES row

`corpus/SOURCES.md` has **no committed S105 row** (registry table ends at S095,
line 105; `grep -c S105` = 0). S105 is a quarantine-register id, not a registry
row; the lane's pointer map `.ufo/waves/round-45/assimilation/staged-map.tsv`
line 30 binds it to staged id S110:

```
S110	https://jaohfa.com/pdf/systematic_review.pdf	62be15a474e866e4bef6c9d5	39676	S105	absent	japanese-search-record-r38.md
```

(staged-map line 25's `S105 <empty url> 0` is a different, URL-less staged id —
distinct namespace, not this register row.)

## Capture evidence (local bytes only; no fetch)

Key check: `sha256("https://jaohfa.com/pdf/systematic_review.pdf")[:24]` =
`62be15a474e866e4bef6c9d5` → capture found:

- `/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache/62be15a474e866e4bef6c9d5.txt`
  61188 bytes, sha256 `960da5cf632dbd278ea941c54d83e3ed8f13657bcb4bcbbfc8d63c9d834acf4a`;
  UTF-8, 39676 chars, 622 lines (`wc -c -l` = `  622 61188`). Matches
  staged-map `capture_chars=39676` and verdicts.tsv's "39676-char capture",
  `pdftotext -layout` rendering of the PDF.
- `…/62be15a474e866e4bef6c9d5.pdf` (and identical `.raw`), 291615 bytes,
  sha256 `b4ff9d41fde4432260d4adea247a86efe911a61dd1f63034b31dc8b229270be6`.

## STRICT test (commands + observed output)

Test applied: `unicodedata.normalize("NFKC", s)`, `re.sub(r"\s+", " ", s)`,
case-sensitive `str.find`, run on the `.txt` capture (normalized 13798 chars)
and each quote (also NFKC-normalized; lengths unchanged: 66/64/24). Plus a
brute-force longest-common-substring scan per quote.

Observed:

| quote | located | LCS | LCS text | LCS byte offset in .txt |
|---|---|---|---|---|
| q1 `情報源［Informationsources］6 …ために` | no | 21/66 | `ト、組織、文献リスト、研究を特定するために` | 5920 (raw char 4022; norm char 1283) |
| q2 `and not, as a search engine's rendering …` | no | 6/64 | `earch ` | 6646 (raw char 4368; norm char 1505) — inside the PDF's word `search` |
| q3 `それぞれの情報源が最後に調べられた日付を記載する` | no | 17/24 | `それぞれの情報源が最後に調べられた` | 6290 (raw char 4192; norm char 1409) |

Exact register LCS numbers match the committed verdict (21 of 66, 6 of 64,
17 of 24) — the frozen decision-rule measurement reproduces.

## Why the quotes fail as written (raw capture lines)

`62be15a474e866e4bef6c9d5.txt` lines 67–70 (two-column layout; left column is
the PRISMA-style item, right column bullets):

```
67:                情報源                ト、組織、文献リスト、研究を特定するために ・検索したデータベース等の情報を全て記載する。
68:                ［Information   6   調べたり、助言を求めたりした情報源を記載 ・それぞれのデータベース毎に最後に検索した日の日付を記載する。
69:                sources］           する。それぞれの情報源が最後に調べられた ・ハンドサーチの有無を記載する。ハンドサーチを実施した場合はその方法を記載する。
70:                                    日付を記載する。 検索戦略 …
```

- q1 splices the item's Japanese heading (`情報源`, byte 5895), its split
  English bracket (`［Information` byte 6069 / `sources］` byte ~6360 — the
  joined form `Informationsources` occurs nowhere, `nt.find` = -1) and the
  left-column body (`全てのデータベース、研究登録、Web サイ` continues at byte
  5895 region) — a plausible reconstruction of the table cell, but never
  contiguous in the rendered capture.
- q2 is an English editorial parenthetical; only `earch ` (a substring of the
  PDF's word `search`) matches, at byte 6646.
- q3's tail `日付を記載する。` exists at byte 6497 (next rendered line) but
  interposed right-column text separates it from the prefix; closest raw run
  is 17/24. Same pattern in the capture's second table copy at bytes
  47473–48162 (lines ~451–455).

## Classification and reason

- **absent-as-written**: all three quoted spans fail verbatim containment in
  the only local capture of the cited URL; q3 is a misquote of real PDF
  content, q1 a re-joined cell, q2 near-wholly absent. Reason string, per
  committed verdict: "the three quotes are corrected to the PDF's own wording
  and re-checked; a re-render carrying them verbatim turns the row into
  present."
- Not unverifiable: capture exists (39676 chars), is not a bot wall or
  unrendered binary, and exceeds the longest quote (66 chars).
- C1 calibration note for the frozen round-48 predicate: this row is the
  provenance-boundary case where strict `absent` coexists with real content —
  consistent with both the round-42 `absent` verdict and the round-43
  `misquote` refinement; it supports refusing-as-written, not a fabrication
  call. No counterexample to the frozen C1 predicate arises from this row.

## Commands run (verbatim)

```sh
grep -n "S105" /home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/absent-defect-register.md
grep -c "S105" chousa-shokunin/corpus/SOURCES.md            # → 0
sed -n 1,35p .ufo/waves/round-45/assimilation/staged-map.tsv
ls -l  .qcache/62be15a474e866e4bef6c9d5.* ; sha256sum .qcache/62be15a474e866e4bef6c9d5.*
wc -c -l .qcache/62be15a474e866e4bef6c9d5.txt               # → 622 61188
python3 -c "import hashlib; print(hashlib.sha256(b'https://jaohfa.com/pdf/systematic_review.pdf').hexdigest()[:24])"  # → 62be15a474e866e4bef6c9d5
# python3: NFKC+whitespace-collapse find per quote; brute-force LCS; byte-offset map (results above)
```

Tooling: no installs; python3 stdlib only. Scratch: none created (no
`/tmp/chousa-r48-*` artifacts to clean).

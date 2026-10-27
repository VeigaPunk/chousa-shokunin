# R58ScribeEntryDraft — S101 carrier-alphabet entry draft (header / Observation / Limits)

Seat scope: draft only, in this report. No lane write, no entry file created in the lane;
no live fetch; C1 battery untouched. All runnable probes executed in a scratch clone of the
lane, deleted before yielding.

## Inputs read (read-only)

- `corpus/evidence/round58/claims.md` (freeze `9e73a031ab1ac3bac343de008850d7d87f9e5634`, base `b13ca7b5…`), `c2-count.py`, `c2/quotes.tsv`, `corpus/SOURCES.md` S101 row, `tools/build-spans.py`, `tools/capture-text.py`, `tools/inference-ground.py`, `corpus/evidence/round51/quote-substance-check.py`, `corpus/knowledge/normative-reference-chain-china-r57.md` (header shape).
- Lane at measurement: HEAD `718e8d2` (one commit after the freeze, adding only `controls/`); `git diff --stat 9e73a03..HEAD -- claims.md c1-count.py c2-count.py c2/quotes.tsv tools/build-spans.py tools/capture-text.py` printed no rows for those surfaces.
- Capture: `corpus/captures/6dc68fd6b32ce9c8dfcebce8.raw` sha256 `6063a3aff7a4081e93a685f2721e2cd6b477ba84a841211e298bcddd6d9fddf3`; defined form by pinned `capture-text.py` (sha256 `2c0140bc…`) sha256 `a8e3e7ad213b6ec50479542cda23612e7ae7ae5fd4506fba53a91f2f7e79f867`, 47356 bytes.
- All 12 frozen quotes occur exactly once in that form, at chars 315, 330, 590, 683, 734, 781, 797, 838, 965, 993, 1460, 11723; quotes 1, 2 and 10 begin at a line start (3 anchors). Quote lengths 13-36 chars (max 36).

## Draft (proposed entry text; content stands on the 12 frozen quotes only)

```markdown
source: S101 — 中国学术期刊（光盘版）检索与评价数据规范（修订本）, 哈尔滨工业大学-hosted copy — https://jc.hit.edu.cn/_upload/article/files/f7/54/711916924125a0682e3bc3ebb6ed/1f6f2731-8c87-4812-b7e2-9fad0069d508.doc — raw `6dc68fd6b32ce9c8dfcebce8` sha256 `6063a3aff7a4081e93a685f2721e2cd6b477ba84a841211e298bcddd6d9fddf3`; defined text form by pinned `tools/capture-text.py` (sha256 `2c0140bc04029c8faedc6c89a65bd657430d8b85f433406946567b70303e2573`); anchors at chars 315, 330, 590, 683, 734, 781, 797, 838, 965, 993, 1460, 11723 (receipt `corpus/evidence/round58/c2/spans.tsv`)
verified-at: 2026-10-27 (lane capture read at measurement; no live fetch this round — the round-57 r2 egress-scope L0 question remains open)
recheck: 180d
ground: the lane held S101's .doc but no entry for the reference-type/carrier alphabet it prints
adopted: round 58, lane claim R58-C2 (frozen `9e73a03`)

# Reference-type and carrier marks in S101 section 1．2

S101's section `1．2 参考文献类型及其标识` prints a three-layer marking scheme for
reference lists: a single-letter document-type alphabet, a two-letter alternative for a
described class of reference types, and carrier identifiers written beside the type mark in
bracketed notation. The document code is printed in a different heading of the same
specification.

#### Observation

- `1．2 参考文献类型及其标识` (S101, char 315, line start) opens the mark rules; the first rule `1．2．1 根据GB3469规定，以单字母方式标识以下各种参考文献类型：` (char 330, line start) makes the document-type mark a single letter under GB3469.
- A second rule, `建议以下列双字母作为标识：` (char 590), recommends a two-letter mark for the reference classes its own sentence names; the frozen composite `[DB/OL]—联机网上数据库(database online)；` (char 993, line start) carries a two-letter type mark (DB) with the carrier OL.
- Carrier marking is required on citation, not optional: `被引用为参考文献时需在参考文献类型标识中同时标明其载体类型` (char 683). The notation is fixed by `并以[文献类型标识/载体类型标识]表示` (char 797).
- Two carrier pairs are printed: `磁带(magnetic tape)—MT` (char 734) and `联机网络(online)—OL` (char 781).
- Three bracketed composites are printed: `[M/CD]—光盘图书(monograph on CD–ROM)；` (char 838), `[J/OL]—网上期刊(serial online)；` (char 965) and `[DB/OL]—联机网上数据库(database online)；` (char 993). Read against the notation rule (char 797), the slot before the slash is the type mark and the slot after it the carrier.
- A publication-element sequence printed for reference entries reads `出版地:出版者,出版年:起止页码(当整体引用时不注).` (char 1460): place, publisher, year, pages, with pages omitted when the whole item is cited.
- The document code is a field apart from the bracketed type/carrier mark: `与文献标志码(Document code)` (char 11723) is the second conjunct of a heading line that opens at char 11704, in a part of the specification disjoint from the anchored `1．2` fragments (chars 315-993). The frozen fragment binds 文献标志码 to the gloss Document code; the heading's first conjunct is outside the frozen set and is not asserted here.

#### Limits

- The frozen quote set is 12 fragments. The membership table itself (the type names and single letters printed after the rule at char 330), the two-letter membership beyond the `DB` composite, and carrier codes other than `MT`, `OL` and the `CD` shown inside `[M/CD]` are printed by S101 but lie outside the frozen set; this entry does not assert them.
- The class noun list that precedes `建议以下列双字母作为标识：` (printed earlier on the same source line, char 500) is outside the frozen fragment; the entry asserts the two-letter rule and the `DB` composite only.
- No live fetch was made this round: the source is the lane's committed `.doc` capture (`6dc68fd6b32ce9c8dfcebce8`), and character offsets are valid only for that raw digest and the defined text form the pinned capture-text produces from it.
- Scope is what S101 prints. This entry makes no present-day validity claim about GB3469, about any later revision of the marking scheme, or about whether journals currently enforce these marks.
- The template context of that publication element (the entry form's line beginning at char 1408) sits outside the frozen fragment and is not asserted.
- S101 is a university-hosted copy of the specification (SOURCES.md tier B carrier); the entry does not claim it is the issuing body's own copy.
```

The entry intentionally has no `#### Inference` section: that section is another seat's item
(`R58ExecC2Inference`), and the frozen counter refuses an entry without one (finding F3).

## Verification actually run (scratch clone, lane unmodified)

Scratch: `/fast/scratch/hyaku/chousa-r58/R58ScribeEntryDraft/`; clone `git clone --shared --no-hardlinks <lane> lane` → `git rev-parse --show-toplevel` = `/fast/scratch/hyaku/chousa-r58/R58ScribeEntryDraft/lane`, short HEAD `718e8d2`.

1. Draft written to the clone at `corpus/knowledge/carrier-alphabet-china-r58.md`; S101 row's `used-by` cell (cell 10) appended with that path in the clone only (lane row still ends `corpus/knowledge/citation-count-semantics-r37.md`).
2. `python3 -B tools/build-spans.py --quotes corpus/evidence/round58/c2/quotes.tsv --out corpus/evidence/round58/c2 --cache corpus/captures` → rc 0, `SPANS_ROWS=12 WRITTEN=12`; TSV offsets are 235, 250, 510, 603, 654, 701, 717, 758, 885, 913, 1380, 11643 (= quote offset − 80).
3. Run A, builder manifest as committed: `python3 -B corpus/evidence/round58/c2-count.py --root <clone> --work workA` → rc 1:
   `CAPTURE_BOUND=0/12 ENTRY_QUOTES=0/12 … ANCHOR_BOUND=0/3 … REBUILD=MATCH`, twelve `ERROR CAPTURE_BIND:S101`, `C2=FAIL`.
4. Run B, same clone, TSV offset column replaced by the quote's occurrence char (315, 330, … 11723) from `form.txt`; `--work workB` → rc 1:
   `BOUND=1/1 QUOTE_ROWS=12/12 CAPTURE_BOUND=12/12 ENTRY_QUOTES=12/12` / `SUBSTANCE=PASS ANCHOR_BOUND=3/3 STRAY_IDS=- NEW_GROUND=yes REBUILD=FAIL` → `ERROR BUILDER_REBUILD_MISMATCH`, `C2=FAIL`.
5. Compatibility probe (scratch-only, not proposed text): `entry-probe.md` = the draft plus two `#### Inference` bullets quoting `被引用为参考文献时需在参考文献类型标识中同时标明其载体类型` and `[J/OL]—网上期刊(serial online)；`; `tools/inference-ground.py --entry entry-probe.md --spans <clone>/corpus/evidence/round58/c2/spans.tsv --counts /dev/null --registry <clone>/corpus/SOURCES.md` → `section=1 bullets=2 tokens=2 grounded=2` / `GROUND: PASS`, rc 0. Without that section the counter prints `FINDING INF_SECTION_ABSENT` (`INFERENCE_GROUND_FAIL`).

## Findings

- **F1 (blocking, frozen): the C2 predicate is unsatisfiable as frozen.** `tools/build-spans.py:149` writes `str(start)` where `start = off - 80` (`CONTEXT = 80`, line 43); its docstring (line 16) says "the `offset` column its start", i.e. span start. `corpus/evidence/round58/c2-count.py:101` requires `occurrences[0] == off`, i.e. the quote's occurrence offset. Runs A and B are the two horns: builder-identical manifest ⇒ `CAPTURE_BOUND=0/12` but `REBUILD=MATCH`; occurrence-offset manifest ⇒ `CAPTURE_BOUND=12/12` but `REBUILD=FAIL`. No manifest can satisfy both legs, so `C2=PASS` cannot be printed for any entry content. This is a contradiction between two frozen artifacts (counter and round-55 builder pin), reported, not fixed.
- **F2: registry binding is not yet present in the lane.** At HEAD the S101 row has 11 cells, `cells[7]='mined'`, but `cells[10]='corpus/knowledge/citation-count-semantics-r37.md'`; the counter therefore printed `REF_ID_UNBOUND=1` until the clone's cell 10 was appended (then `BOUND=1/1`). The registry edit belongs to `R58ExecC2Registry`; the lane was not modified.
- **F3: `INFERENCE_GROUNDED=no` in both runs is the absent `#### Inference` section, not a draft defect.** Probe 5 shows the draft plus two frozen-quote inference bullets yields `GROUND: PASS`.
- **F4: the quoted set is partial by design.** The single-letter membership table, the two-letter list beyond `DB`, and carrier codes beyond `MT`/`OL`/`CD` are printed by S101 but outside the frozen quotes; the Limits section says so instead of importing them.

## Unrun / out of scope

- `c1-count.py` (C1 seat); no C1 fixture, no builder change.
- No live fetch of the S101 URL (r57 r2 egress-scope L0 question open); no network at all.
- No entry file, registry row, manifest, span file, or counter change written to the lane.
- Full `C2=PASS` is unreachable as frozen (F1); a counter-repair decision is the L1's, not this seat's.
- `inference-ground` PASS was obtained only on a scratch probe entry; the lane entry will need the Inference seat's bullets.

VERDICT: S101 header/Observation/Limits draft (12 quotes, 3 line-start anchors, offsets 315-11723 on raw `6063a3af…`) survives every content and structural leg that can be measured — `CAPTURE_BOUND=12/12`, `ENTRY_QUOTES=12/12`, `ANCHOR_BOUND=3/3`, `SUBSTANCE=PASS`, `STRAY_IDS=-`, `NEW_GROUND=yes`, registry `BOUND=1/1` once cell 10 is appended — while the frozen C2 gate itself is falsified as satisfiable: the pinned builder's span-start `offset` and the counter's occurrence-offset `CAPTURE_BIND` are mutually exclusive with byte-identical `REBUILD`, so `C2=PASS` is unreachable and `INFERENCE_GROUNDED` remains the Inference seat's pending leg.

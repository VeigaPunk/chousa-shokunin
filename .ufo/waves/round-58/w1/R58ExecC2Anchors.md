# R58ExecC2Anchors — round-58 C2 anchor/offset/line-start audit

Seat: R58ExecC2Anchors (Chousa lane, round 58, w1). Scope: the 12 frozen S101 quotes of `corpus/evidence/round58/c2/quotes.tsv` — character offsets, uniqueness counts, line-start status in the DEFINED OLE text form — plus independent inspection of the declared offsets. No lane writes; lane tree unchanged (`git status --porcelain` → only pre-existing untracked `.ufo/` and `corpus/evidence/round58/controls/`).

## 1. Method and pinned inputs (all re-opened, digests re-computed)

```
sha256sum corpus/captures/6dc68fd6b32ce9c8dfcebce8.raw
  6063a3aff7a4081e93a685f2721e2cd6b477ba84a841211e298bcddd6d9fddf3  (== claims.md RAW_SHA)
sha256sum tools/capture-text.py
  2c0140bc04029c8faedc6c89a65bd657430d8b85f433406946567b70303e2573  (== claims.md CT_SHA)
sha256sum tools/build-spans.py corpus/evidence/round58/controls/build-spans-r55.py
  1ed2650af28ea8e392bc34f7259cfb58f93b05c7453aca60e86b170c59c80bf6  (both; == BUILDER_SHA)
git -C <lane> rev-parse HEAD → 9e73a031ab1ac3bac343de008850d7d87f9e5634 (freeze commit)
python3 tools/capture-text.py corpus/captures/6dc68fd6b32ce9c8dfcebce8.raw
  → rc=0, 47356 bytes / 27012 chars, form sha256 a8e3e7ad213b6ec50479542cda23612e7ae7ae5fd4506fba53a91f2f7e79f867
```
Builder-path form == counter-path form, byte-identical (27012 chars, same sha256). Form has 0 CR bytes / 469 LF, so no newline-translation ambiguity between the two paths. No live fetch. Scratch (only location written): `/fast/scratch/hyaku/chousa-r58/R58ExecC2Anchors/`, removed after the run.

## 2. Quote-by-quote table (independent computation)

`occ` = `re.finditer(re.escape(quote), form)` offsets; `count` = number of those offsets; `line_start` = `off==0 or form.rfind('\n',0,off)+1==off` (the counter's own ANCHOR predicate, `c2-count.py:115`); `builder_off` = what the PINNED builder writes into the manifest `offset` column (`max(0, occ-80)`, the span start — `build-spans.py:148`).

| # | quote | chars | count | occ offset | byte offset | line_start | builder_off | declared (s101-open.txt) |
|---|-------|-------|-------|-----------|-------------|-----------|-------------|--------------------------|
| 1 | `1．2 参考文献类型及其标识` | 14 | 1 | 315 | 721 | **yes** | 235 | 315, count 1 |
| 2 | `1．2．1 根据GB3469规定,以单字母方式标识以下各种参考文献类型：` | 36 | 1 | 330 | 758 | **yes** | 250 | 330, count 1 |
| 3 | `建议以下列双字母作为标识：` | 13 | 1 | 590 | 1278 | no (prev `，`) | 510 | 590, count 1 |
| 4 | `被引用为参考文献时需在参考文献类型标识中同时标明其载体类型` | 29 | 1 | 683 | 1513 | no (prev `当`) | 603 | 683, count 1 |
| 5 | `磁带(magnetic tape)—MT` | 20 | 1 | 734 | 1666 | no (prev `：`) | 654 | 734, count 1 |
| 6 | `联机网络(online)—OL` | 15 | 1 | 781 | 1739 | no (prev `，`) | 701 | 781, count 1 |
| 7 | `并以[文献类型标识/载体类型标识]表示` | 19 | 1 | 797 | 1767 | no (prev `，`) | 717 | 797, count 1 |
| 8 | `[M/CD]—光盘图书(monograph on CD–ROM)；` | 33 | 1 | 838 | 1882 | no (prev `：`) | 758 | 838, count 1 |
| 9 | `[J/OL]—网上期刊(serial online)；` | 27 | 1 | 965 | 2047 | no (prev ` `) | 885 | 965, count 1 |
| 10 | `[DB/OL]—联机网上数据库(database online)；` | 33 | 1 | 993 | 2087 | **yes** | 913 | 993, count 1 |
| 11 | `出版地:出版者,出版年:起止页码(当整体引用时不注).` | 27 | 1 | 1460 | 3274 | no (prev `.`) | 1380 | 1460, count 1 |
| 12 | `与文献标志码(Document code)` | 21 | 1 | 11723 | 19500 | no (prev `)`) | 11643 | 11723, count 1 |

Uniqueness: 12/12 occur exactly once → the builder's uniqueness precondition holds for all 12. Line-start anchors = **3** (rows 1, 2, 10) — exactly the `anchors<3` floor (`c2-count.py:134`), i.e. **zero margin**: shifting any of rows 1/2/10 off a line start drops the leg below floor.

Quote-set integrity: the 12 strings in `c2/quotes.tsv` are byte-identical to the `QUOTES` list frozen in `c2-count.py` (parsed via `ast.literal_eval`; `IDENTICAL: True`). Max length 36 = the counter's `len(quote)<=36` limit, exactly at the bound (row 2). Codepoints verified: `．`=U+FF0E, `，`=U+FF0C (fullwidth, NOT ASCII `,`), `—`=U+2014, `–`=U+2013 (row 8's `CD–ROM` uses EN-dash; rows 5/6/8/9/10 use EM-dash). A transcription with ASCII `,` in row 2 fails to match — my first fixture did exactly that; that failure was mine, not the source's.

## 3. Independent inspection of the DECLARED offsets — all match

The lane-owned receipt `corpus/evidence/round58/s101-open.txt` declares an offset and a count for all 12 quotes (row 7 inline as "Located quote … at character 797 (19 characters)"). Parsing those declarations and diffing against my independent computation:

```
ALL 12 DECLARED OFFSETS/COUNTS MATCH MY INDEPENDENT COMPUTATION: True
declared "19 characters" for the located quote: True (actual 19)
```
**12/12 declared offsets, 12/12 declared counts and the declared character length agree exactly; no mismatch.** The declared offsets are OCCURRENCE offsets. The receipt's form length (27,012 chars) and its "exactly once" statement also reproduce.

## 4. FINDING — the frozen C2 counter cannot reach `C2=PASS` (offset-column semantics)

`c2-count.py` holds two demands on the manifest `offset` column that cannot both hold: `c2-count.py:106-110` (CAPTURE_BIND) requires `occurrences[0] == off`, i.e. `off` = the quote's OCCURRENCE offset (and `len(occurrences)==1`); `c2-count.py:137-146` (REBUILD) requires the committed manifest to be byte-identical to a rebuild by the PINNED round-55 builder — whose `offset` column is the SPAN START (`max(0, occ-80)`, `build-spans.py:148`) = occurrence offset − 80 for every row here.

Measured on a scratch clone of the freeze commit (`git clone --no-hardlinks` of the lane, `git checkout 9e73a03`), building the real manifest with the pinned builder, then running the REAL frozen counter (`c2-count.py --root . --work <fresh>`):

* builder manifest as-is → `CAPTURE_BOUND=0/12  ANCHOR_BOUND=0/3  REBUILD=MATCH` → 12× `ERROR CAPTURE_BIND:S101`, `C2=FAIL`;
* same manifest with only the `offset` column rewritten to occurrence offsets → `CAPTURE_BOUND=12/12  ANCHOR_BOUND=3/3  SPAN_BYTES_OK=12/12  REBUILD=FAIL` → `ERROR BUILDER_REBUILD_MISMATCH`, `C2=FAIL`.

Every other leg passes in the second configuration (SUBSTANCE=PASS, INFERENCE_GROUNDED=yes, NEW_GROUND=yes, ENTRY_QUOTES=12/12, no stray ids) — `BUILDER_REBUILD_MISMATCH` is the single remaining error. Exhaustive 2-candidate enumeration (`satisfiability_proof.py`) confirms no manifest satisfies both legs: `occ != max(0, occ-80)` on all 12 rows (all occ ≥ 315).

This is a defect in the FROZEN PREDICATE, not in the data: the lane's convention is span-start. Confirmed from committed artifacts — the quote sits at position 80 within its own span file in 33/33 (r54), 16/19 (r55), 19/23 (r56) rows, and the r55/r56 counters derive registry anchors as `int(offset) + span.find(quote)` (`round55/c2-count.py:260`), with 10/10 registry `char N` cells across r54–r56 satisfying exactly that formula. The r58 C2 counter reads the same column under a different convention, so it rejects the lane's own builder output on all 12 rows.

Secondary: round-55's counter bound the registry `char N` anchor cell to the manifest offsets (`round55/c2-count.py:271-275`); round-58 replaced that with a self-contained line-start check and no longer validates the registry anchor cell. The pre-existing S101 row's anchor cell (`char 11170, 11205, 11993, 12161, 13247, 34374`) is in the LEGACY `.txt` sidecar coordinate system, not the defined OLE form — `char 34374` is beyond the 27,012-char OLE form entirely (the sidecar is 128,416 chars) — so it is not a usable occurrence-offset anchor here.

## 5. FINDING — C1's builder hardening collides with C2's `BUILDER_PIN`

C2 pins `tools/build-spans.py` to the round-55 sha256 (`c2-count.py:104-106`, `BUILDER_PIN`), while C1's claim is that `tools/build-spans.py` gains the hazard refusal behaviour (`claims.md` C1; `c1-count.py:165` defaults `--builder` to that same lane path). Any change to that file breaks C2's pin. Measured on a scratch clone with a minimal hardening edit applied and everything else held at the passing configuration:

```
ERROR BUILDER_PIN
ERROR BUILDER_REBUILD_MISMATCH
C2=FAIL
```
C1 and C2 cannot both be satisfied on one tree as written: C1 needs `tools/build-spans.py` changed, C2 needs it byte-identical to the round-55 file. This also means §4 is not fixable by editing the builder — that breaks `BUILDER_PIN` instead, and the frozen counter is not mine to edit.

## 6. Not run / out of scope

No live fetch; only the lane-owned committed capture was read. No edits to builder, counter, claims or quote set anywhere in the lane. The `--root` runs of the frozen counter were executed on scratch clones of freeze commit 9e73a03, never against the live lane tree. I did not evaluate quote entailment or entry prose (C2 substance/entailment seats).

## 7. Risks for the L1

1. **Blocking:** C2's frozen predicate is unsatisfiable as written (§4) — no manifest yields `C2=PASS`. If the wave targets `C2=PASS`, it fails on the predicate regardless of entry quality; the fix must come from the L1 (relax CAPTURE_BIND to the lane's span-start convention, or drop the REBUILD byte-equality leg), not from the executor.
2. **Blocking/ordering:** C1 and C2 both target `tools/build-spans.py` with incompatible requirements (§5); C1 first breaks C2's `BUILDER_PIN`, C2 first leaves C1's hazard refusal unimplemented.
3. **Fragile:** the ANCHOR floor is met with exactly 3/3 anchors — no slack.
4. **Pre-existing:** S101's registry anchor cell is bound to the legacy sidecar coordinate system and cannot serve as an occurrence-offset anchor for this manifest.

VERDICT: The anchor/offset/uniqueness/line-start work SURVIVES — all 12 frozen S101 quotes occur exactly once in the defined OLE form at offsets 315, 330, 590, 683, 734, 781, 797, 838, 965, 993, 1460, 11723, with 3 line-start anchors (rows 1, 2, 10) and every one of the 12 declared offsets in `s101-open.txt` independently confirmed — BUT the frozen C2 predicate it targets is FALSIFIED as satisfiable: the specific attack, reading the manifest `offset` column as the quote OCCURRENCE offset (CAPTURE_BIND) while simultaneously demanding byte-identity with a builder that writes the SPAN START (REBUILD), contradicts on all 12 rows, so `C2=PASS` is unreachable; and the C1 hardening of the same pinned file collides with C2's `BUILDER_PIN`. Both are findings against the frozen artifacts, for the L1 to integrate.

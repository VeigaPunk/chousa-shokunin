# R54W2ExecC2Rerun — C2 after-state falsification (round 54, wave 2)

Seat: `R54W2ExecC2Rerun` (leaf). Target: C2's after-state at L1 tip
`447cf7ed4dc1a3708518b99e9a5e62e177c11ce9`. Verified first that the attack surface is that tree:
`git diff --stat 447cf7ed4… HEAD -- corpus/ tools/` prints nothing (only `.ufo/` reports and W2 spec
landed afterwards), and working-tree `corpus/` is clean (`git status --porcelain` → only untracked
`.ufo/…`, `corpus/evidence/round54/census-end.txt`).
Frozen counter and builder are unchanged since the freeze: `git log --oneline -- corpus/evidence/round54/c2-count.py`
→ single commit `5a1a206` (the freeze); `git diff 5a1a2063… HEAD -- …/c2-count.py` → empty.
Scratch `TMPDIR=/fast/scratch/hyaku/chousa-r54/R54W2ExecC2Rerun`, `PYTHONDONTWRITEBYTECODE=1`, no
network, no tool installed (nothing needed).

## 1. The five specified commands (full output)

```
$ python3 corpus/evidence/round54/c2-count.py
ENTRIES=2/2 (min 2) REFUSED_ENTRIES=0
HELD_CITED=- HELD_BAD=0
BOUND=3/3 (min 2) REFUSED=0
BOUND_IDS=S121,S122,S123
REF_ID_UNBOUND=0
NEW_GROUND=2/2
QUOTE_ROWS=33 ON_BOUND=33/33
SPAN_IDS=3/3 (min 3 each)
QUOTES_IN_SPAN=33/33
QUOTES_IN_ENTRY=33/33
QUOTES_IN_LESSON=33/33
QUOTE_SHORT=33/33
SPAN_CONTEXT=33/33
CAPTURE_BOUND=33/33
SUBSTANCE=PASS
ANCHOR_BOUND=3/3
INFERENCE_GROUNDED=2/2
QUARANTINE_VERDICTS=3/3 (S080,S088,S096)
QUARANTINE_BLOCKED_ADOPTED=0
C2=PASS                                    EXIT=0

$ python3 corpus/evidence/round54/c2-count.py --lane-only
ENTRIES=2/2 (min 2) REFUSED_ENTRIES=0
HELD_CITED=- HELD_BAD=0
BOUND=3/3 (min 2) REFUSED=0
BOUND_IDS=S121,S122,S123
REF_ID_UNBOUND=0
NEW_GROUND=2/2
QUOTE_ROWS=33 ON_BOUND=33/33
SPAN_IDS=3/3 (min 3 each)
QUOTES_IN_SPAN=33/33
QUOTES_IN_ENTRY=33/33
QUOTES_IN_LESSON=33/33
QUOTE_SHORT=33/33
SPAN_CONTEXT=33/33
CAPTURE_BOUND=skipped
SUBSTANCE=PASS
ANCHOR_BOUND=3/3
INFERENCE_GROUNDED=2/2
QUARANTINE_VERDICTS=3/3 (S080,S088,S096)
QUARANTINE_BLOCKED_ADOPTED=0
C2=PASS                                    EXIT=0

$ python3 corpus/evidence/round54/build-spans.py --check
SPANS_ROWS=33 STALE=0                      EXIT=0

$ python3 corpus/evidence/round51/quote-substance-check.py corpus/evidence/round54/spans.tsv
IDS=3 QUOTES=33 FAILURES=0                 EXIT=0

$ python3 tools/inference-ground.py --entry …/source-type-taxonomy-r36.md --spans …/round54/spans.tsv \
    --counts /dev/null --registry …/corpus/SOURCES.md --root …/chousa-shokunin
GROUND entry=corpus/knowledge/source-type-taxonomy-r36.md section=1 bullets=5 tokens=6 grounded=6
GROUND: PASS                               EXIT=0
$ … --entry …/source-type-taxonomy-r37.md …
GROUND entry=corpus/knowledge/source-type-taxonomy-r37.md section=1 bullets=7 tokens=11 grounded=11
GROUND: PASS                               EXIT=0
```

## 2. Span rebuild from quotes.tsv into a scratch root, then cmp

```
S=…/R54W2ExecC2Rerun; mkdir -p $S/rebuild/corpus/evidence/round54
cp …/corpus/evidence/round54/quotes.tsv $S/rebuild/corpus/evidence/round54/
sha256sum both copies → 53edffa21d57c770fd4eab978fb2c75da49f12e153ce4fff266deb1d985eb3ac (identical)
$ python3 corpus/evidence/round54/build-spans.py --root $S/rebuild
QUOTE S121 char 477 spans/S121-1.txt        QUOTE S123 char 5576 spans/S123-1.txt
QUOTE S121 char 537 spans/S121-2.txt        QUOTE S123 char 5602 spans/S123-2.txt
QUOTE S121 char 1029 spans/S121-3.txt       QUOTE S123 char 11542 spans/S123-3.txt
QUOTE S121 char 1048 spans/S121-4.txt       QUOTE S123 char 14096 spans/S123-4.txt
QUOTE S121 char 1162 spans/S121-5.txt       QUOTE S123 char 4812 spans/S123-5.txt
QUOTE S121 char 1797 spans/S121-6.txt       QUOTE S123 char 4736 spans/S123-6.txt
QUOTE S122 char 13300 spans/S122-1.txt      QUOTE S123 char 4852 spans/S123-7.txt
QUOTE S122 char 14082 spans/S122-2.txt      QUOTE S123 char 21382 spans/S123-8.txt
QUOTE S122 char 15188 spans/S122-3.txt      QUOTE S123 char 82465 spans/S123-9.txt
QUOTE S122 char 16105 spans/S122-4.txt      QUOTE S123 char 82834 spans/S123-10.txt
QUOTE S122 char 16321 spans/S122-5.txt      QUOTE S123 char 3602 spans/S123-11.txt
QUOTE S122 char 17078 spans/S122-6.txt      QUOTE S123 char 424 spans/S123-12.txt
                                            QUOTE S123 char 490 spans/S123-13.txt
                                            QUOTE S123 char 5751 spans/S123-14.txt
                                            QUOTE S123 char 2512 spans/S123-15.txt
                                            QUOTE S123 char 2655 spans/S123-16.txt
                                            QUOTE S123 char 58840 spans/S123-17.txt
                                            QUOTE S123 char 59201 spans/S123-18.txt
                                            QUOTE S123 char 57965 spans/S123-19.txt
                                            QUOTE S123 char 8881 spans/S123-20.txt
                                            QUOTE S123 char 5982 spans/S123-21.txt
SPANS_ROWS=33 WRITTEN=33                   EXIT=0

$ cmp $S/rebuild/corpus/evidence/round54/spans.tsv …/round54/spans.tsv    → CMP_EXIT=0
$ diff -u committed rebuilt                                            → NO_DIFF
$ diff -u <(ls committed/spans) <(ls rebuilt/spans)                     → LIST_SAME (33 / 33)
per-file byte cmp over all 33 span files                               → MISMATCH_COUNT=0
sha256 over `sha256sum * | sort -k2` of each span tree                 → 47af2022…07130e0 both sides
```

**Zero mismatches: no finding from the rebuild.** `PYTHONDONTWRITEBYTECODE=1` was exported for every
command, so no `__pycache__` was dropped in the lane, and the builder wrote nothing outside `$S/rebuild`.

## 3. Independent re-derivation (own script, not build-spans) — CAPTURE_BOUND/SPAN_CONTEXT

33/33 rows: the span file is the exact slice at the recorded offset, the quote sits at `+80` with
80 characters of context either side, and the quote occurs exactly once in that form. First pass
(byte semantics) reported 12 apparent mismatches; they were mine: the S121/S122 `.txt` sidecars hold
877 and 688 CRLF pairs, so recorded offsets index the **newline-normalised** text form — the form the
frozen counter and builder both use (`read_text(encoding="utf-8")`) and that the Registry cells name
(“read as UTF-8 with newline normalisation”, `corpus/SOURCES.md:131-133`). S123's sidecar is LF-only.
Under the documented text-form semantics: `BAD= 0 ROWS= 33`.

## 4. Controls and a mutation battery — are the legs live at the tip?

`controls/build-c2-controls.py` re-run (TMPDIR in scratch) reproduces `controls/c2-controls.txt`
exactly: STAGED `BOUND=0/3 REF_ID_UNBOUND=6 HELD_BAD=1 C2=FAIL exit=1`; TOOLED `BOUND=3/3
REF_ID_UNBOUND=3 ANCHOR_BOUND=0/3 SUBSTANCE=FAIL C2=FAIL exit=1`.

Mutations on a full scratch copy of `corpus/` + `tools/` (`--root`), one leg each:

| # | mutation | observed | verdict |
|---|---|---|---|
| M1 | S121 anchor `char 1797`→`char 99999` | `ANCHOR_BOUND=2/3 C2=FAIL` | leg live |
| M2 | append `X` to `spans/S122-3.txt` | `CAPTURE_BOUND=32/33 C2=FAIL` | leg live |
| M3 | scope sentence replaced at **one** of its two sites in r37 | `C2=PASS` | presence-based, see F2 |
| M3b | same, replaced at **all** occurrences | `QUOTES_IN_ENTRY=32/33 C2=FAIL` | leg live |
| M4 | S121 `used-by` widened to both entries | `BOUND=1/3 C2=FAIL` | leg live |
| M5 | S088 verdict → `unverifiable` | `QUARANTINE_BLOCKED_ADOPTED=1 C2=FAIL` | leg live |
| M6 | one quote hollowed to 2 non-space chars (manifest+span consistent) | `SUBSTANCE=FAIL QUOTES_IN_ENTRY=32/33 C2=FAIL` | leg live |
| M7 | delete `spans/S123-4.txt` | `QUOTES_IN_SPAN=32/33 C2=FAIL` | leg live |
| M8 | stray `S199` added to r36 | `REF_ID_UNBOUND=1 C2=FAIL` | leg live |
| M9 | one row's `capture_sha256` → 64 zeros, span content real | `--lane-only` PASS / full `CAPTURE_BOUND=32/33 FAIL` | digest leg load-bearing, as documented |
| M10 | false Inference bullet appended to r37, quotes untouched | `C2=PASS` | counter is not an entailment check (claims.md "restated before data") |

## 5. Entailment / depth re-open of S121–S123 (semantic, by hand)

Every sweep the two entries print was re-run verbatim and reproduces:
`1 1797 1 15212` (r36 recheck); `3591 22007` + `[0,0,0,0,0,0,0,1,2,2,1,3,2,2,5,2,2,1,2]` +
`[0,0,0,0,0,0,0,0,1,0,0,0,0,2,1,1,1,0,1]` (r36 `#### Unknown` sweep); `[32, 0, 0, 0]` (r37 sweep);
`11542 32` (r37 recheck). Independently confirmed: 表Ａ．２ has exactly five carrier rows
(`磁带…ＭＴ` 59025, `磁盘…ＤＫ`, `光盘…ＣＤ`, `联机网络…ＯＬ`, `缩微资料…ＭＭ` 59201);
`主要责任者` 31; `国家标准委` twice in the portal form and `推荐性` once in the record form;
`附录`/`文献类型`/`[M]`/`[J]`/`EB/OL` = 0 in both authority forms — so r36's Inference that
neither authority page carries the type table, and r37's normative-`附录Ａ` vs informative-`附录Ｂ`
reading, both follow from the quoted text. Entry-declared lengths and digests match the files
(3591 / 22007 / 83061 characters; prefixes `4e46154f4a841d17`, `2d68faf7c724eb1b`, `13a34aa9bb107eef`).
Quarantine verdicts spot-checked: S080 — `标准号：` 0 and the joined string 0 in the S121 form,
values present as `发布 于`/`实施 于`; S088 — slash-joined carrier list 0, five separate rows once.

## 6. E3 (S101 cut) and base ground

`grep -o 'S[0-9]{3}'` over r37 → only `S123` (14×); `grep -c S101` → 0. S101's `used-by` cell is
`corpus/knowledge/citation-count-semantics-r37.md` both at `c49ffc6c` and at the tip (row printed from
both) — unchanged, as E3 states. Base ground legs: `git grep -l -e 'ISO 690:2021' -e '文献载体标识'
c49ffc6c -- corpus/knowledge` → nothing, exit 1; `GB/T 7714-2025` at base → exactly one file
(`citation-version-binding-r36.md`). QUALITY 100's premise (S101 `used-by` at `corpus/SOURCES.md:111`)
holds and is consistent with the cut; `HELD_CITED=- HELD_BAD=0` is the expected after-state.

## Findings (none breaks a frozen predicate leg)

- **F1 (low, naming).** Two entry-body `char N` pointers index *mid-string*, not the string start,
  unlike the other 43 body pointers I checked: `corpus/knowledge/source-type-taxonomy-r36.md:15`
  cites `char 575` for “主管部门为 国家标准委” (the value starts at 575, the phrase at 569) and
  `:18` cites `char 2993` for 「标准文献题录著录规则」 whose start is 2987. Both offsets land inside
  the claimed phrase, so no claim is false; only the “char N = start” convention is not uniform.
  Nothing checks entry-body offsets — `ANCHOR_BOUND` reads the Registry `anchor` cell only.
- **F2 (named limit, observed).** `QUOTES_IN_ENTRY` is presence-based. r37 quotes the scope clause at
  two sites (`:16` Observation, `:34` Inference); removing it from one leaves `C2=PASS` (M3),
  removing both fails (M3b). Reading, not a violation of the predicate's wording.
- **F3 (low, summary-cell scope).** `corpus/SOURCES.md:133` summarises “附录Ａ 表A.1 rows marked
  电子资源必备”; 表Ａ．１ is the type table and does carry an `电子资源必备` column (25×), so the cell
  is true, but the carrier table 表Ａ．２ that S123's quote set actually covers is named only in the
  entry, not in the row.
- **F4 (disclosed, worth knowing).** Span offsets for S121/S122 are offsets into the
  newline-normalised `.txt` form, not byte offsets into the capture file (877 / 688 CRLF pairs). An
  independent reader using byte semantics gets a different slice — my own first pass reported 12
  false mismatches. The Registry cells say “newline normalisation”, so it is disclosed, and
  counter+builder agree on the form.
- **F5 (named limit, observed).** Neither `REF_ID_UNBOUND` nor `inference-ground` refuses an entry
  that names a **bound** id it does not cite: appending a bullet-scoped `S121` to r37 (which has no
  `source: S121` line) still gives `REF_ID_UNBOUND=0 INFERENCE_GROUNDED=2/2 C2=PASS`. The predicate's
  wording (“except a bound id”) is satisfied literally; the per-entry “cites what it names” reading is
  not checked by either tool.
- **F6 (disclosed).** A false Inference bullet appended to r37 passes `C2=PASS` (M10) and
  `inference-ground` (tokens are lexical). Entailment is the Gate's, as claims.md states.

Credit note (not my call): `BOUND=3/3` ⇒ three bound documents, one per document; S101 earns none and
was not re-bound. Expansion credit is unaffected by F1–F6.

## What I did not do

Did not run C1's counter/supplement/forge (other seats), did not judge QUALITY 97-99 beyond reading
(the C2-relevant one is 100), did not run `pdf-crosscheck.py`, made no git/jj mutation anywhere, no
fetch. All lane reads were read-only; the only file I wrote is this report.

VERDICT: attacked C2's after-state at 447cf7e — counter (full + `--lane-only`), span builder, round-51
substance check, `inference-ground` on both entries, a byte-exact span rebuild from `quotes.tsv`
(0 mismatches, 33/33), an independent offset re-derivation, both negative controls and 13 mutation
probes plus a manual entailment re-open of S121–S123 — and it **survives** every frozen leg; F1–F6 are
naming/named-limit observations, none of which falsifies a predicate, target or control.

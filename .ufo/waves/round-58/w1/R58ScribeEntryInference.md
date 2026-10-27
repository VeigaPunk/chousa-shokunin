# R58ScribeEntryInference — S101 carrier-alphabet entry: Inference and Unknown draft

Base: lane HEAD `9e73a031ab1ac3bac343de008850d7d87f9e5634` (freeze). Leaf seat: no dispatch, no lane
writes. Read: `corpus/evidence/round58/claims.md`, `corpus/evidence/round58/c2-count.py`,
`corpus/evidence/round58/c2/quotes.tsv`, `corpus/captures/6dc68fd6b32ce9c8dfcebce8.raw`,
`tools/inference-ground.py`, `tools/capture-text.py`, `tools/build-spans.py`, `corpus/SOURCES.md`.

## Frozen bytes re-opened (hashed, not trusted from prose)

```
$ cd /home/vgpnk/Projects/shokunin/chousa-shokunin
$ sha256sum corpus/captures/6dc68fd6b32ce9c8dfcebce8.raw tools/capture-text.py tools/build-spans.py
6063a3aff7a4081e93a685f2721e2cd6b477ba84a841211e298bcddd6d9fddf3  corpus/captures/6dc68fd6b32ce9c8dfcebce8.raw
2c0140bc04029c8faedc6c89a65bd657430d8b85f433406946567b70303e2573  tools/capture-text.py
1ed2650af28ea8e392bc34f7259cfb58f93b05c7453aca60e86b170c59c80bf6  tools/build-spans.py
$ S=/fast/scratch/hyaku/chousa-r58/R58ScribeEntryInference
$ TMPDIR=$S python3 -B tools/capture-text.py corpus/captures/6dc68fd6b32ce9c8dfcebce8.raw > $S/form.txt; echo rc=$?
rc=0
$ wc -c < $S/form.txt
47356
```

The three digests equal `claims.md`'s RAW_SHA, CT_SHA and BUILDER_SHA. Defined-form offsets of the 12
frozen quotes (each exactly one occurrence): 315, 330, 590, 683, 734, 781, 797, 838, 965, 993, 1460,
11723. Line-start-bound rows: 1, 2 and 10, i.e. `ANCHOR_BOUND=3/3`, exactly the frozen floor.

## Draft — `#### Inference` (6 bullets, for the build seat to paste)

- Section `1．2 参考文献类型及其标识` (S101 span 1) and `1．2．1 根据GB3469规定，以单字母方式标识以下各种参考文献类型：` (S101 span 2) state the mapping, and `建议以下列双字母作为标识：` (S101 span 3) adds two-letter codes only for the database, computer-program and electronic-bulletin reference types, so the single-letter and two-letter markings form one layered alphabet in which DB/CP/EB extend the mapping instead of replacing its single letters.
- The carrier is a second, separately marked axis: `被引用为参考文献时需在参考文献类型标识中同时标明其载体类型` (S101 span 4) requires the carrier to be stated within the same marker, and `并以[文献类型标识/载体类型标识]表示` (S101 span 7) fixes the notation as two components in one bracket, the left naming the reference type and the right the carrier, so the second component is an attribute of the copy rather than a further document type.
- The printed examples instantiate that composition: `[M/CD]—光盘图书(monograph on CD–ROM)；` (S101 span 8) pairs the monograph marker with the CD carrier, the carrier rows `磁带(magnetic tape)—MT` (S101 span 5) and `联机网络(online)—OL` (S101 span 6) fix the two-letter carrier form, and `[J/OL]—网上期刊(serial online)；` (S101 span 9) pairs the serial marker with the online carrier; each bracket therefore reuses a letter printed in the 1.2.1 single-letter table (普通图书 M, 期刊文章 J) and appends a carrier code.
- The carrier annotation is conditioned on the carrier being non-paper: `对于非纸张型载体的电子文献` (S101 span 4) states the condition, and the paragraph closes by exempting `以纸张为载体的传统文献` (S101 span 10), so a paper-carried book keeps a bare single-letter marker; `[DB/OL]—联机网上数据库(database online)；` (S101 span 10) is the electronic case the rule addresses.
- The type marker is a slot in the entry layout rather than a free-standing label: the book template prints `[文献类型标识]` after the title, and the located layout line `出版地:出版者,出版年:起止页码(当整体引用时不注).` (S101 span 11) shows the marker consumed inside the entry punctuation, so section 1.2's alphabet is applied by section 1.3's format.
- The document-code field is a distinct field: `与文献标志码(Document code)` (S101 span 12) names it inside section 11's heading beside `中图分类号(CLC number)`, an article-level classification label, so its values belong to the article's content classification and supply nothing to the reference type or carrier axes of section 1.2.

## Draft — `#### Unknown` (6 bullets)

- Whether the cited GB3469 edition prints the same single-letter table: the capture asserts the mapping is per GB3469 and the lane holds no copy of that standard; no fetch is authorized this round, so table fidelity to GB3469 is untested.
- Whether a database on disc takes a CD combination: the located examples pair DB with MT and OL and pair CP with DK; no CD pairing for DB is printed, so no rule is derived for it.
- Whether the two-letter electronic type codes ever appear without a carrier component: the text conditions the carrier on non-paper electronic references but prints no bare DB, CP or EB bracket, so whether the slash is always present is unstated.
- Section 11.6's five document-code values (A–E, defined-form lines 218–222) lie outside the frozen twelve-quote set; this entry derives no relation between them and section 1.2's type or carrier markers, and no Inference bullet rests on them.
- The capture prints two parallel clause sets (1.2.3/1.2.4 at lines 59–78, 14.3.3/14.3.4 at lines 257–268) with 标识 in the first and 标志 in the second, and prints `CD–ROM` with U+2013 after a single U+2014 in 1.2.4 against `CD-ROM` with U+002D after a double U+2014 in 14.3.4; the byte difference is observed, its editorial intent is not stated.
- Whether carrier codes beyond the four listed exist is outside the frozen set: only MT and OL are frozen quote rows, and DK and CD are present in the span context at line 71 without a frozen citation row of their own.

## Checks actually run (scratch copy only; lane files never edited)

```
$ TMPDIR=$S python3 -B tools/inference-ground.py --entry entry6.md --spans spans.tsv --counts /dev/null \
    --registry corpus/SOURCES.md --root $S
GROUND entry=entry6.md section=1 bullets=6 tokens=16 grounded=16
GROUND: PASS
rc=0
$ TMPDIR=$S python3 -B corpus/evidence/round51/quote-substance-check.py $S/spans.tsv
IDS=1 QUOTES=12 FAILURES=0
rc=0
```

- `quotes_present 12 /12`: every frozen quote string occurs verbatim in the draft (each twice: in the
  drafted bullets and in an accompanying observation list).
- `S`-ids in the draft: `{S101}` only; `载体类型标识` is present (inside span-7's quote).
- Standalone extraction (trio + the two drafted sections, 21 lines) also prints `GROUND: PASS`
  16/16 with 12/12 quotes, so the draft does not depend on the build seat's Observation wording.

## Gates and frozen constraints

- Each of the six bullets cites at least one exact frozen quote string; span indices replace char
  offsets in bullets (see F1).
- A–E kept out of the inferences: only Unknown bullet 4 mentions them, as defined-form lines 218–222
  outside the frozen quote set, and states no relation to the section-1.2 markers.
- Entry header is assumed to satisfy the counter's trio (`source:`/`verified-at:`/`recheck:` as lines
  1–3); the draft's sections go below any observation block, never above the trio.

## Findings (against frozen files; findings, not fixes)

- **F1 — char offsets are grounding tokens.** The first draft cited `(S101, char 330)` etc.; every
  such citation failed: `FINDING INF_TOKEN_NOT_IN_SPAN bullet=1 token='330'` … `GROUND: FAIL`, because
  `grounding_tokens()` reads every 3+ digit numeral and the offset is not in any span. Char offsets are
  safe in Observation prose; in `#### Inference` cite span row indices (`span 4`, `span 10`).
- **F2 — `span_file` is manifest-relative.** `span_texts()` resolves `base = spans.parent`; a manifest
  column of `S101-01.txt` yielded `grounded=0`. Rewritten to `spans/S101-01.txt` → `grounded=16`. The
  build seat's `corpus/evidence/round58/c2/spans.tsv` must carry the `spans/` prefix, which also matches
  `c2-count.py`'s `spans/sfile` read.
- **F3 — anchor floor has no margin.** The frozen set sits at exactly `ANCHOR_BOUND=3/3` (rows 1, 2, 10
  are line-start); any offset drift in `spans.tsv` drops C2 on that leg alone.
- **F4 — registry used-by cell.** `corpus/SOURCES.md:111` cell 11 currently reads
  `corpus/knowledge/citation-count-semantics-r37.md`; `c2-count.py` requires `ENTRY_REL` in `cells[10]`,
  so the build seat must append `corpus/knowledge/carrier-alphabet-china-r58.md` there or get
  `REF_ID_UNBOUND`. Not written by this seat.
- **F5 — NEW_GROUND leg is spelling-vacuous.** The leg greps the traditional `載体类型标识` at the
  claim base: `git grep -l '載体类型标识' b13ca7b… -- corpus/knowledge` → `rc=1`; the simplified
  `载体类型标识` search also gives `rc=1`. Base absence is true, but a base holding only the simplified
  string could never trip the traditional-pattern grep, so the leg tests presence of the new entry more
  than newness of the ground.
- **F6 — evidence-format note.** The Unknown's U+2013/U+002D/U+2014 claims were verified on the defined
  form: line 71 prints `CD–ROM` (U+2013) with a single U+2014 separator, line 261 prints `CD-ROM`
  (U+002D) with `——`; that is text presence, not a statement about intent.

## Out of scope / unrun

- Not run: `c2-count.py` end-to-end (entry, `spans.tsv`, `spans/` and the registry edit are the build
  seat's writes; the lane currently holds no `carrier-alphabet-china-r58.md` and no `c2/spans.tsv`, so a
  lane run would fail on `ENTRY_MISSING`/`MANIFEST_MISSING`, not on this draft).
- Not run: `c1-count.py` and the C1 hazard battery (separate claim, separate seat), any live fetch
  (none authorized; the round-57 r2 egress-scope L0 question stays open), any git/jj mutation.
- The entry's final Observation block, its first-three-line trio, and `used-by` binding were not written
  here; the draft only fixes the Inference and Unknown sections.

## Touched surfaces

Writes: this report only. Reads: the files listed above plus `corpus/evidence/round51/quote-substance-check.py`.
Scratch `/fast/scratch/hyaku/chousa-r58/R58ScribeEntryInference` (form, scratch entry, counter-built span
copies, manifests) removed before yield; no install, no PATH write, no fleet-root write.

VERDICT: The assigned work — drafting the S101 carrier-alphabet entry's `#### Inference` and `#### Unknown`
sections so that each inference cites a frozen quote and the section-11 document-code field stays separate
from the section-1.2 type/carrier markers — **survives** on the checks run here: the lane's own
`inference-ground.py` prints `GROUND: PASS` with 16/16 tokens grounded on a scratch copy, and
`quote-substance-check.py` prints `IDS=1 QUOTES=12 FAILURES=0` against a span manifest rebuilt at the
frozen offsets; all 12 frozen quotes are carried verbatim, only S101 is cited, and the A–E values appear
only as an explicitly out-of-set Unknown. The C2 claim itself remains **inconclusive from this seat**: the
frozen `c2-count.py` was not run, because the entry file, `spans.tsv` and the S101 `used-by` cell are the
build seat's writes, and the draft's bearing on C2 is theirs to integrate.

# SourceEntryScribe — the S101 source entry for frozen C2 (round 60, wave 1)

Seat: `SourceEntryScribe`, scribe, leaf (no subagent dispatch). Bounded to the frozen claims
`corpus/evidence/round60-claims.md`, prior committed evidence, and the current counter/source.
Assignment's expected claim SHA: `09d8053f5f09a26c07f41286a7a885a2c21bff31b30f71963cceaa35d971a440`;
observed `sha256sum` of the frozen file: `65721569fc1336b159c7637acf476cda6f583bbd4b3a84aaadd239f7d02018d1`
(mismatch recorded in §9; the file was not edited by this seat).

Method: read the frozen C2 predicate, the committed counter, the committed S101 capture and its two
committed text forms, the r37 knowledge entry, the S101 registry row, the round-49 span ledger, the
round-59 Gate block, and the lane's span builder; then ran the counter and seven scratch controls
(§4), all inside `/fast/scratch/hyaku/chousa-r60/SourceEntryScribe` and removed before yield.

## Verdict

The **source-text side** of C2 verifies: S101 re-opens offline, the pinned text form reproduces
byte-identically from committed artifacts, and the type/carrier passage the claim names locates
exactly once (line 245, char 12960) inside a ≤25-word quote. The **measurement side** does not:
`corpus/evidence/round60/c2-count.py` prints `C2=PASS`, exit 0, on the untouched base
`b379919a873e7080a31ef92c7002f55f5374e2c6`, so the frozen "Base must fail because no round-60 entry
exists" clause has no witness, and the counter's `METADATA`/`LIMIT` legs bind only strings that the
pre-existing r37 entry already carries (`corpus/knowledge/citation-count-semantics-r37.md:5,8,9,74-80`).
A deliberately overreaching note appended to a candidate copy still prints `C2=PASS` (control C, §4).

Consequence for the lane: **C2 must not be admitted on this counter.** The note draft in §6 is what an
honest round-60 entry would say; §7 names the smallest predicate additions that would make the claim
measurable. Both statements are source-entry findings, not a ruling on the round.

## 1. What the frozen C2 predicate asks a source entry to establish

| Predicate clause (frozen text) | Artifact it must read | Observable | Status in the committed counter |
|---|---|---|---|
| "establish source digest … from committed S101 raw capture" | `corpus/captures/6dc68fd6b32ce9c8dfcebce8.raw` | sha256 = `6063a3af…ddf3` | implemented (`RAW_PIN=1/1`) |
| "… and quote locations … using the pinned capture-text form" | the defined form | form sha + one occurrence + line | partly: `FORM_PIN`, `QUOTE`, `LINE` — no location is written by the note or read from it |
| "verify the new entry's exact observation … against those source bytes" | the round-60 note | note's statements entailed by located quotes | **not implemented**: no note is identified, no note text is read |
| "and no overreach" | the note | no present-day-validity / CNKI-implementation claim | **not implemented** (control C passes) |
| "verify its S101 citation and metadata" | entry header | `source: S101 — https://jc.hit.edu.cn/`, `verified-at:`, `recheck:` | implemented as substring presence, satisfied by base |
| "and require the scorecard's declared disposition" | `SCORECARD.md` | declared round-60 disposition | **not implemented**: `grep -c SCORECARD corpus/evidence/round60/c2-count.py` = 0, and `SCORECARD.md` has no `Round 60` text at freeze time (`grep -c "Round 60" SCORECARD.md` = 0) |
| "Base must fail because no round-60 entry exists" | base bytes | `C2=FAIL` at base | **falsified**: base prints `C2=PASS`, exit 0 |

## 2. Verified source-entry facts (all offline, all reproducible)

- Source: S101 — 中国学术期刊（光盘版）检索与评价数据规范（修订本）, copy hosted by
  哈尔滨工业大学 — `https://jc.hit.edu.cn/_upload/article/files/f7/54/711916924125a0682e3bc3ebb6ed/1f6f2731-8c87-4812-b7e2-9fad0069d508.doc`.
- Capture: `corpus/captures/6dc68fd6b32ce9c8dfcebce8.raw`, sha256
  `6063a3aff7a4081e93a685f2721e2cd6b477ba84a841211e298bcddd6d9fddf3`; capture key equals
  `sha256(url)[:24]` (checked).
- Defined text form: `python3 -B tools/capture-text.py corpus/captures/6dc68fd6b32ce9c8dfcebce8.raw`
  → 27,012 characters, 469 lines, 0 U+FFFD, 0 NUL, 0 CR, sha256
  `a8e3e7ad213b6ec50479542cda23612e7ae7ae5fd4506fba53a91f2f7e79f867`.
  **This exact digest is committed twice**: `corpus/evidence/round54/S101-text-form.txt` (`6af11e9`)
  and `corpus/evidence/round59/s101-open.txt` (`026174e`). The wave copy
  `.ufo/waves/round-60/s101-open.txt` (untracked) is byte-identical. So the removed-and-reopened
  form is not a fresh unverifiable derivation: it is a re-derivation of committed bytes.
- Access date for this round's opening: **2026-10-27**, recorded in
  `.ufo/waves/round-60/s101-receipt.txt`; no live fetch was made (L0 `8d77e6c1` stays open).
- The quote the frozen counter pins is `c. 文献类型及载体类型标志；` — 1 occurrence, **line 245**,
  char 12960 (0-based start of `c. `), phrase `文献类型及载体类型标志` at char 12963. Word count for
  the CORPUS rule-1 ≤25-word test: 2 whitespace tokens, 11 CJK characters — inside the cap.
- The same capture states the carrier rule **twice, in two renderings, with different terminology**:

  | Passage | Line | Char | Wording of the identifier |
  |---|---|---|---|
  | 1.2.4 (early part of the capture) | 71 | 668 / 797 | `…参考文献类型标识…` / `并以[文献类型标识/载体类型标识]表示包括…` |
  | 14.3.4 (2006 part of the capture) | 261 | 13418 / 13551 | `…参考文献类型标志…` / `并以[文献类型标志/载体类型标志]表示包括…` |
  | 14.2(c) | 245 | 12960 | `c. 文献类型及载体类型标志；` |

  A note that quotes one rendering as the other is a misquote; the counter cannot see this, because it
  checks only that the 14.2(c) string occurs once in the form.
- The copy's self-description, for the scope sentence: `CAJ-CD B/T 1-2006` at lines 455 and 457 (2
  occurrences), and the imprint at line 468, which reads
  `1999年1月第1版\xa0\xa0 2006年6月第7次印刷 \xa0\xa0 印数\xa0\xa0 22601-27000` (NBSPs present — quote
  `2006年6月第7次印刷`, not the spaced line, or the quote will not resolve).
- All six S101 quote strings already used in r37's Observation resolve **exactly once** in the pinned
  form: `为便于文献的统计和期刊评价` (11972/line 217), `每一篇文章或资料应根据其内容性质标识一个文献标志码`
  (12007/217), `本规范推荐采用GB/T 7714中规定的顺序编码制格式著录,…作者-出版年制。` (12795/241),
  `文献类型及载体类型标志` (12963/245), `参照ISO 690及ISO 690-2，每一参考文献条目的末尾均以“.”结束。`
  (14049/270), `参考文献格式，参照ISO 690` (25123/406). So the existing entry's S101 observation is
  source-faithful **in the defined form**; the problem is its header line says the form is something
  else (§3).

## 3. Three locator spaces exist; only one is reproducible, and the registry names a retired one

The lane carries the same S101 passage addressed by three different offset systems. They do not agree,
and no artifact labels which one it is in.

1. **Registry `anchor` cell** (`corpus/SOURCES.md:111`, cell 7): `located quotes char 11170,
   char 11205, char 11993, char 12161, char 13247, char 34374`. These resolve in the **naive UTF-16LE
   decoding of the `.raw`** — verified: char 11170 lands on `为便于文献的统计和期刊评价…`, char 12161 on
   `文献类型及载体类型标志`, char 34374 on `15.7参考文献格式，参照ISO 690`. That form is the one the
   lane retired: `corpus/evidence/round49/build-spans.py:60-67` offers the `.txt` sidecar first and then
   `raw.decode("utf-16le", errors="replace")`, and the `.txt` sidecar does not hold the quote
   contiguously (probe: `t.count('文献类型及载体类型标志') == 0`), so the row's 12161 is
   `utf16le_text.find(quote)`.
2. **Round-49 span ledger** (`corpus/evidence/round49/spans.tsv`, S101 rows S101-1…S101-6): `offset`
   11166 / 12081 / 11945 / 34370 / 13167 — span *window* starts in the same retired space
   (`build-spans.py:132-148`: window = `form[max(0,off-80):off+len(quote)+80]`, clipped at CR for `.raw`).
3. **Defined form** (capture-text.py, sha `a8e3e7ad…`): quote start 12960, phrase 12963, line 245.
   This is the only space the round-60 counter pins, and the only one reproducible from a committed
   file with a stated recipe.

Counting commands and results:

```sh
# (a) the round-49 ledger reproduces against its own builder and the lane captures
python3 corpus/evidence/round49/build-spans.py \
  --root /home/vgpnk/Projects/shokunin/chousa-shokunin --cache .../corpus/captures --check
# -> SPANS_ROWS=31 STALE=0        exit 0

# (b) the same ledger is STALE against the lane's CURRENT defined-form builder
python3 tools/build-spans.py --quotes <copy of round49 quotes.tsv> --out <copy of round49 dir> \
  --cache .../corpus/captures --check
# -> SPANS_ROW_STALE spans/S100-1.txt … spans/S101-6.txt
#    SPANS_ROWS=31 STALE=9        exit 1
```

`tools/build-spans.py:1-12` states its form is the defined capture-text output and
`:22-24` states that the printed `QUOTE <id> char <N>` is "the value a Registry `anchor` cell's
`char N` must equal". For S101 that is now unsatisfiable in one step: the registry's cell is in space 1,
the builder prints space 3. `[INFERENCE]` the anchor cell was correct when written (round 54 era) and
became mislabelled when capture-text.py changed the text form; the defect is the unlabelled space, not
necessarily a wrong quote — the quoted text does occur, at other offsets.

Why this matters for C2: the frozen predicate asks the counter to "establish … quote locations" and to
check the new entry's observation "against those source bytes". The counter prints `LINE=245` but never
compares any locator written by the note or the registry against the form, so a note that carries a
registry-style `char 12161` for the 14.2(c) element would read as correct while pointing at a different
form. The note in §6 therefore states its form, its digest, and its offsets in the defined space.

## 4. Counter control matrix (scratch, candidate copies; lane untouched)

Base is `b379919a`. Script copied to a scratch lane root so that its `ROOT` (the script's checkout, see
§5) is the scratch copy; `--root` points at the candidate. Each line is the counter's own output.

| # | Candidate | Output | Exit | What it proves |
|---|---|---|---|---|
| A | base bytes, unmodified | `RAW_PIN=1/1 FORM_PIN=1/1 QUOTE=1/1 LINE=245 METADATA=1/1 LIMIT=1/1` `C2=PASS` | 0 | base passes → the frozen "base must fail" clause has no witness |
| B | base minus the `#### Unknown` version-in-force bullet (r37:79-80) | `… METADATA=1/1 LIMIT=0/1` `C2=FAIL` | 1 | `LIMIT` is a literal substring test on pre-existing text |
| C | base **plus** an overreaching note ("the captured specification proves that CNKI today applies … and that CAJ-CD B/T 1-2006 remains the version in force") | identical to A: `C2=PASS` | 0 | the counter is blind to overreach — the claim's "no overreach" leg does not exist |
| D | base minus its `source: S101` line | `… METADATA=0/1 LIMIT=1/1` `C2=FAIL` | 1 | metadata is a URL-prefix presence check |
| E | candidate root with **no** `.ufo/waves/round-60/s101-open.txt`; script root has one | `C2=PASS` | 0 | `FORM` comes from the script checkout, not `--root` |
| F | same as E but the candidate root's own form has the pinned quote reworded (`标志`→`标识`, sha `b8fe4ea6…`) | `C2=PASS` | 0 | a tampered form **under test** is invisible |
| G | the tampered form placed at the script checkout | `FORM_PIN=0/1 QUOTE=0/1 LINE=0 …` `C2=FAIL` | 1 | only the script-checkout form is ever read |

Read together: A–G show the counter's verdict is a function of (i) the script checkout's form file and
(ii) pre-existing substrings in the entry. Nothing about a round-60 note enters the computation.

## 5. Predicate gaps, each with its line

`corpus/evidence/round60/c2-count.py`:

- `:7-8` — `FORM` and `ENTRY` are module constants; `:13` rebinds `raw` and `entry` from `--root` but
  leaves `form=ROOT/'.ufo/waves/round-60/s101-open.txt'` on the module `ROOT`. `--root <lane-copy>` is
  therefore half-bound (controls E/F).
- `:13` — `--work` is parsed and never used: the counter creates no scratch and writes nothing. That is
  safe for scratch discipline, but the flag advertises a contract it does not honour; a future gate that
  needs scratch must not assume it.
- `:17` — `metadata` = `body.startswith('\n# ')` and four substrings. The r37 header already satisfies
  all five; `body.startswith('\n# ')` is satisfied by any leading-blank-line file.
- `:18` — `scoped` = `'#### Unknown' in body` and one generic sentence. Both are in the base entry
  (`r37:74,79-80`). The claim's "records the existing knowledge entry's S101 source-quote limit" is not
  what this tests: r37's actual recorded limit is the ISO-vs-GB/T register quote at `r37:84-86`.
- No `SCORECARD.md` read; no git/diff read; no note identity. The claim's "new entry" and "scorecard's
  declared disposition" have no code path.

## 6. Draft correction note (exact bytes) — the source entry an honest C2 would land

Placement: inside `corpus/knowledge/citation-count-semantics-r37.md`, after `#### Unknown`
(`r37:74-86`), because the frozen counter pins that path (`c2-count.py:8`). Every quoted string below
was checked to occur exactly once in the pinned form; every offset is in the **defined form** and is
restated with its form digest so it cannot be confused with the registry's retired space (§3).

```markdown
#### Correction — round 60: what S101 states about the type/carrier notation

Source: S101, re-opened offline on 2026-10-27 (no fetch) from the lane's committed capture
`corpus/captures/6dc68fd6b32ce9c8dfcebce8.raw` (sha256
`6063a3aff7a4081e93a685f2721e2cd6b477ba84a841211e298bcddd6d9fddf3`), read through the defined
text form `python3 -B tools/capture-text.py` (27,012 characters, sha256
`a8e3e7ad213b6ec50479542cda23612e7ae7ae5fd4506fba53a91f2f7e79f867`).

(a) The copy states the type/carrier rule twice, and the two renderings use different terms for the
identifier itself:
- section 1.2.4 — `对于非纸张型载体的电子文献，当被引用为参考文献时需在参考文献类型标识中同时标明其载体类型。`
  and `并以[文献类型标识/载体类型标识]表示包括了文献载体类型的参考文献类型标识：` (line 71; chars 668 and 797).
- section 14.3.4 — `对于非纸张型载体的电子文献，当被引用为参考文献时需在参考文献类型标志中同时标明其载体类型。`
  and `并以[文献类型标志/载体类型标志]表示包括了文献载体类型的参考文献类型标志。` (line 261; chars 13418 and 13551).
- section 14.2(c) lists the element as `c. 文献类型及载体类型标志；` (line 245; char 12960).

(b) Scope. Every statement in (a) is a statement of this copy's text. The capture prints
`CAJ-CD B/T 1-2006` (lines 455 and 457) and the imprint `2006年6月第7次印刷` (line 468).
[INFERENCE] The 1.2.4 rendering predates the 2006 revision; the capture prints no revision code
beside it. None of this establishes that this revision is the version in force, and none of it
establishes that CNKI applies these identifiers to the records it counts.

(c) Recorded limit of this entry's S101 evidence, not repaired here. The register row's anchor
offsets (`char 11170` … `char 34374`, `corpus/SOURCES.md` row S101) address the retired naive
UTF-16LE decoding of the `.raw`; every quote in (a) is located in the defined form above, where the
corresponding passages sit at `char 11972`, `char 12007`, `char 12795`, `char 12963`, `char 14049`
and `char 25123`. The register quote that put "GB/T 7714" into the 15.7 parameter-table sentence is
absent as written: the capture names GB/T 7714 in 14.1 and ISO 690 in 14.4 and in the parameter table.
```

Sentence → located-quote map (for a reviewer to check without re-deriving anything):

| Note sentence | Form line | Form char | Occurrences |
|---|---|---|---|
| 1.2.4 rule sentence | 71 | 668 | 1 |
| 1.2.4 bracketed notation | 71 | 797 | 1 |
| 14.3.4 rule sentence | 261 | 13418 | 1 |
| 14.3.4 bracketed notation | 261 | 13551 | 1 |
| 14.2(c) element | 245 | 12960 | 1 |
| `CAJ-CD B/T 1-2006` | 455, 457 | 26616, 26685 | 2 (both cited) |
| `2006年6月第7次印刷` | 468 | 26965 | 1 |
| `GB/T 7714` in 14.1 | 241 | 12795 | 4 in the document; the 14.1 one is cited, the parameter-table one is the absent quote |

Draft self-review against the frozen claim's own wording: it separates the copy's statements from
present-day validity and from CNKI implementation (§b); it records the existing entry's S101
source-quote limit (§c, both the ISO-vs-GB/T quote and the locator-space limit); it repairs no counter
and asserts no new ground. It does **not** by itself make `c2-count.py` discriminate (control C), so it
must not be landed as a PASS-bearing artifact without §7's predicates.

## 7. Smallest predicate additions that would gate this note

The frozen predicate's four clauses map onto four checks; all are offline and cheap. I did not
implement them (seat bounds: writes only this report) — this is the operable spec for the counter's
next version, to be declared before data.

1. **Note identity, not entry identity.** Compute the round-60 diff of
   `corpus/knowledge/citation-count-semantics-r37.md` between the frozen base and the candidate
   (`git diff --no-renames <base> -- <path>`), require one added section whose heading starts
   `#### Correction — round 60`, and score the note's own bytes. Base then fails by construction
   (no such section), restoring the claimed before→after.
2. **Every quote in the note must resolve in the pinned form.** Extract each backticked span of
   ≥12 characters from the added section and require `form.count(span) == 1`. This is the machine-
   checkable part of "exact observation": it kills a fabricated quote (the class the register already
   produced for GB/T 7714) and kills the 标志/标识 substitution in either direction. It cannot judge
   entailment, so it does not replace the reviewer.
3. **Scope sentence present, and no validity verb in the note's own voice.** Require the declared
   scope sentence (a fixed string, e.g. the `None of this establishes that this revision is the
   version in force` clause) and require that the added section contains none of a short frozen verb
   list applied to `CNKI|在行|现行|currently applies|remains the version in force`. Both lists frozen
   before data; the second is a blacklist, so it is a guard, not a proof.
4. **Disposition.** Require `SCORECARD.md` to carry a round-60 disposition row for C2 whose verdict
   token is one of the frozen set, and require it to cite the counter's own output token. Without this
   the predicate clause has no artifact at all (`grep -c "Round 60" SCORECARD.md` = 0 today).
5. **Isolation.** Bind `FORM` from `--root` (or take `--form` explicitly and pin it), and either use
   `--work` for scratch or delete the flag. Controls E and F show why: today a candidate can be scored
   against another checkout's bytes.

Build the do-nothing control before data: run the new counter on base (must be non-zero) and on base
plus an overreaching note (must be non-zero under check 3's blacklist). Controls B–D in §4 are the
receipts that the current legs are presence tests, not gates.

## 8. Registry effect, census, and the §2b observable

- **No S101 cell may change for a re-open.** CORPUS rule 2 allows in-place change of `status`,
  `recheck`, `used-by` only; `opened` stays `2026-10-25`. `used-by` already lists r37
  (`corpus/SOURCES.md:111`, cell 12 = `corpus/knowledge/citation-count-semantics-r37.md,
  corpus/lessons/round-58.md, corpus/lessons/round-59.md`). So the round's re-opening of S101 leaves
  **no registry observable**; its only evidence is the wave receipt (`.ufo/waves/round-60/s101-open.txt`
  + `s101-receipt.txt`) and the round lesson's `## Gate`.
- If the L1 wants a registry signal for the round, the single conforming one is appending the round-60
  lesson to `used-by` once it exists:
  `…, corpus/lessons/round-59.md` → `…, corpus/lessons/round-59.md, corpus/lessons/round-60.md`;
  `status` stays `mined`, `recheck` stays `180d`. Log it old→new in the lesson (§2b rule 2).
- Current census (read-only; run from the fleet root):
  `./scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin chousa` →
  `chousa ok …/chousa-shokunin/corpus/SOURCES.md`, exit **0**, five pre-existing `W04` duplicate-URL
  warnings (S051, S053, S073, S074, S075). Registry rows: `grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md` = **133**. I hold no independent before baseline; the L1's
  `corpus/evidence/round60/census-start.txt` is the pair.
- Frontier: S101 remains a `docs`/tier-`B`, `mined` row. Its `teaches` cell reads "the data
  specification whose fields and type identifiers **underlie** Chinese journal evaluation and citation
  statistics" — a present-day causal claim the copy does not state; the copy states a purpose
  (`为便于文献的统计和期刊评价`, line 217). The note in §6 restates the copy's own wording, and
  re-anchoring the row's offsets is left as a separate registry correction (new row or an in-place
  `recheck` change, per rule 2) rather than smuggled into the knowledge entry.

## 9. Freeze integrity

- Assigned immutable SHA: `09d8053f5f09a26c07f41286a7a885a2c21bff31b30f71963cceaa35d971a440`.
- Observed: `65721569fc1336b159c7637acf476cda6f583bbd4b3a84aaadd239f7d02018d1`
  (`sha256sum corpus/evidence/round60-claims.md`). The file is untracked (`git status --porcelain`
  shows `?? corpus/evidence/round60-claims.md`); I did not edit it. Two sibling seats (`S101Reopen`,
  `C2CounterAudit`) report the same observed digest, so this is a shared observation, not a local
  accident. Cause and correct digest are **unresolved**; the canonical judge should reconcile before
  binding any verdict to the assigned hash. I did not treat the mismatch as permission to reinterpret
  the claims: the analysis above uses the file as found.

## 10. Boundaries, non-findings, scratch

- No external/live fetch; the only source bytes read are lane-owned captures and committed artifacts.
- No write outside this report. No commits, no git/jj mutation. Read-only git used: `log`, `show`-free
  queries via `git log --oneline -- <path>`; `git rev-parse HEAD`, `git status`.
- Scratch: `/fast/scratch/hyaku/chousa-r60/SourceEntryScribe` (lane copy for controls A–G, round-49
  ledger copy, span-check output). Removed before yield; `ls` after removal returns empty.
- Not my seat, not run: `c1-count.py`, the C1 builder leg, the round-49/54/55 falsification suites,
  the live-source hand-check, QUALITY adjudication of the §6 draft (a reviewer's duty; the frozen claim
  itself conditions any depth credit on a non-author QUALITY gate).
- Peer overlap, recorded not duplicated: `w1/C2CounterAudit.md` reports the base-pass counterexample,
  the `--root`/`FORM` mix and the same freeze-SHA mismatch; `w1/S101Reopen.md` reports the offline
  reopen and the same digest discrepancy. This seat adds the source-entry layer: the three locator
  spaces and their measured disagreement, the dual 标志/标识 rendering, the exact-bytes note draft with
  a sentence→quote map, the registry effect, and the counter's control matrix including the overreach
  and tampered-form legs (C, E, F) that neither peer ran.

## Appendix A — commands and outputs

```text
$ python3 corpus/evidence/round60/c2-count.py --root /home/vgpnk/Projects/shokunin/chousa-shokunin \
    --work /fast/scratch/hyaku/chousa-r60/SourceEntryScribe
RAW_PIN=1/1 FORM_PIN=1/1 QUOTE=1/1 LINE=245 METADATA=1/1 LIMIT=1/1
C2=PASS                                  exit 0

$ sha256sum corpus/captures/6dc68fd6b32ce9c8dfcebce8.raw .ufo/waves/round-60/s101-open.txt \
    corpus/evidence/round54/S101-text-form.txt corpus/evidence/round59/s101-open.txt
6063a3aff7a4081e93a685f2721e2cd6b477ba84a841211e298bcddd6d9fddf3  …/6dc68fd6b32ce9c8dfcebce8.raw
a8e3e7ad213b6ec50479542cda23612e7ae7ae5fd4506fba53a91f2f7e79f867  …/round-60/s101-open.txt
a8e3e7ad213b6ec50479542cda23612e7ae7ae5fd4506fba53a91f2f7e79f867  …/round54/S101-text-form.txt
a8e3e7ad213b6ec50479542cda23612e7ae7ae5fd4506fba53a91f2f7e79f867  …/round59/s101-open.txt

$ python3 - <<'EOF'   # quote location, word cap, form metrics
t=open('.ufo/waves/round-60/s101-open.txt',encoding='utf-8').read(); q='c. 文献类型及载体类型标志；'
i=t.index(q); print(i, t.count(q), len(q.split()))
EOF
12960 1 2                      # chars 27012, lines 469, U+FFFD 0, NUL 0, CR 0

$ python3 corpus/evidence/round49/build-spans.py --root …/chousa-shokunin --cache …/corpus/captures --check
SPANS_ROWS=31 STALE=0          exit 0

$ python3 tools/build-spans.py --quotes S/r49/quotes.tsv --out S/r49 --cache …/corpus/captures --check
SPANS_ROW_STALE spans/S100-1.txt … SPANS_ROW_STALE spans/S101-6.txt
SPANS_ROWS=31 STALE=9          exit 1
```

Controls A–G (§4) were run with the script and form copied into
`/fast/scratch/hyaku/chousa-r60/SourceEntryScribe/lane{,2,3}` so the lane checkout was never the
measured `ROOT`; verbatim outputs are in §4's table.

```text
$ ./scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin chousa
chousa W04 S051 … S053 … S073 … S074 … S075 …
chousa ok /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/SOURCES.md   exit 0

$ grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md
133
$ grep -c "Round 60" SCORECARD.md
0
$ grep -c SCORECARD corpus/evidence/round60/c2-count.py
0
```

## Appendix B — files read (no modifications)

`corpus/evidence/round60-claims.md`; `corpus/evidence/round60/c2-count.py`; `.ufo/waves/round-60/`
{s101-open.txt, s101-receipt.txt, c2-before.txt, w1/C2CounterAudit.md, w1/S101Reopen.md};
`corpus/captures/6dc68fd6b32ce9c8dfcebce8.raw` and `.txt`; `corpus/evidence/round54/S101-text-form.txt`;
`corpus/evidence/round59/s101-open.txt` and `corpus/lessons/round-59.md` (`## Gate`);
`corpus/knowledge/citation-count-semantics-r37.md`; `corpus/SOURCES.md` (row S101, nearby rows);
`corpus/evidence/round49/{spans.tsv,spans/S101-*.txt,build-spans.py}`;
`corpus/evidence/round57/refetch.tsv` (line 66); `tools/capture-text.py`, `tools/build-spans.py`;
`SCORECARD.md` (round verdict headers, round-58 verdict, no round-60 block); `CORPUS.md` (Shape/Rules);
`/home/vgpnk/Projects/shokunin/.ufo/prompts/chousa-round-60.md`.

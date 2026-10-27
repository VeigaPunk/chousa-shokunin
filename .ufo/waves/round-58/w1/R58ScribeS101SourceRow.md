# R58ScribeS101SourceRow — S101 row vs the opened capture and frozen quote set

Report only. My write is this file; scratch `/fast/scratch/hyaku/chousa-r58/R58ScribeS101SourceRow/` (removed before yielding). Lane and fleet were read-only; no fetch, no git/jj mutation, no install. Freeze `9e73a031ab1ac3bac343de008850d7d87f9e5634`, claim base `b13ca7b5c8bbb40d2d29a37fb443c64ca043f791`.

## 1. Frozen inputs re-measured (this seat, not by the counters)

```
sha256sum corpus/captures/6dc68fd6b32ce9c8dfcebce8.raw → 6063a3aff7a4081e93a685f2721e2cd6b477ba84a841211e298bcddd6d9fddf3
sha256sum tools/build-spans.py tools/capture-text.py  → 1ed2650af28ea8e392bc34f7259cfb58f93b05c7453aca60e86b170c59c80bf6
                                                        2c0140bc04029c8faedc6c89a65bd657430d8b85f433406946567b70303e2573
python3 -B capture-text.py 6dc68fd6b32ce9c8dfcebce8.raw > form.txt   rc=0, 47,356 bytes = 27,012 chars,
  form sha256 a8e3e7ad213b6ec50479542cda23612e7ae7ae5fd4506fba53a91f2f7e79f867
cmp form.txt corpus/evidence/round54/S101-text-form.txt → BYTE_IDENTICAL
```

All three pins match claims.md, and my independent run reproduces the committed round-54 target of the SCORECARD pointer corrections byte for byte (raw→form conversion is deterministic; capture-text writes only to stdout — `tools/capture-text.py:450`).

## 2. Row as it stands — `corpus/SOURCES.md:111`

11 cells / 12 pipes; `status`=mined, `kind`=docs, `tier`=B, `opened` 2026-10-25, `recheck` 180d; `used-by` holds one path: `corpus/knowledge/citation-count-semantics-r37.md`.
Scope cell names "the data specification whose fields and **type identifiers** underlie Chinese journal evaluation and citation statistics" — the 1.2.x alphabet is inside the stated scope, so no scope edit is needed.
Anchor cell still reads "section 11 (文献标志码), section 14.1 and 14.4 (参考文献) and the 15.7 parameter table (UTF-16LE text of the raw .doc capture); located quotes char 11170, 11205, 11993, 12161, 13247, 34374" — see F1.
Registry count `grep -c '^| S[0-9]' corpus/SOURCES.md` → `133` (round-57 closed at 133): this round adds no row.

## 3. Proposed edit — used-by only, old → new

- old cell: `corpus/knowledge/citation-count-semantics-r37.md`
- new cell: `corpus/knowledge/citation-count-semantics-r37.md, corpus/knowledge/carrier-alphabet-china-r58.md`
- new line 111 tail: `… | mined | 2026-10-25 | 180d | corpus/knowledge/citation-count-semantics-r37.md, corpus/knowledge/carrier-alphabet-china-r58.md |`

Justified by measurement, not convention:

- Counter predicate `corpus/evidence/round58/c2-count.py:62` (`len(cells)!=11 or cells[7]!='mined' or ENTRY_REL not in cells[10]`): OLD → `unbound=True`; NEW → `cells=11, status=mined, unbound=False`; the other ten cells byte-stable, 12 pipes, still one line (splice probe on a scratch copy of SOURCES.md).
- Gate parser `tools/research-gate.sh:3440-3453` splits on `,`, trims, compares token to entry path; reproduction of that loop on the new cell prints `token[0]=<corpus/knowledge/citation-count-semantics-r37.md>`, `token[1]=<corpus/knowledge/carrier-alphabet-china-r58.md>`.
- Real counter on the lane tree (work in scratch): `ENTRIES=0/1 BOUND=0/1 REF_ID_UNBOUND=1 … C2=FAIL`, exit 1 (pre-edit receipt). Scratch root carrying the edit plus a 12-quote entry: `ENTRIES=1/1 BOUND=1/1 REF_ID_UNBOUND=0`.
- Order (existing entry first, new appended last) matches the registry's multi-entry cells (`S003`’s r24 pair, `S096`/`S118` style), comma+space.

Not proposed: any other cell. The 1.2 anchor gap is F1 and belongs to the append-only correction channel.

## 4. Why no new SOURCES row is needed

- Same source object: same URL, same `.raw` key/digest (`6dc68fd6…` / `6063a3af…`), same copy of the document. Nothing was opened or fetched this round; the row is already `mined`.
- For a held row the binding is the used-by cell (QUALITY 100, `corpus/QUALITY.md:943`; enforced by the round-58 counter at `:62`). A second row would bind nothing new.
- A new row for the same URL is a duplicate: the census emits `W04 duplicate url … across scopes` (`corpus/evidence/round58/census-start.txt`, five such lines, `EXIT=0`), and URL duplication was the ground that held alone in round 52’s refusal (QUALITY 93, `corpus/QUALITY.md:929`).
- Row count stays 133; the 12-quote manifest names S101 and the entry, so provenance is at the entry/spans level, not a new id.

## 5. Gate quote — ≤25 words and located

`corpus/lessons/round-58.md` does not exist yet (`ls` → absent; round-57 is the newest lesson), so there is no Gate text to inspect as written. Pin data for the seat that lands it:

- recommended Gate quote: `被引用为参考文献时需在参考文献类型标识中同时标明其载体类型` — **char 683** of the defined form, unique (`count=1`), **1** whitespace word under `tools/quote-reopen.py`’s `norm()`/`MAX_WORDS=25` (`:61,:83-85`), 29 characters, not line-start. It is the sentence the entry’s carrier distinction rests on.
- line-start locators for the alphabet: `1．2 参考文献类型及其标识` char 315 (2 words, 14 ch) and `1．2．1 根据GB3469规定，以单字母方式标识以下各种参考文献类型：` char 330 (2 words, 36 ch).
- if a ≤25-CHARACTER reading of the Gate rule is applied, the char-bound-safe alternative is `并以[文献类型标识/载体类型标识]表示` char 797 (1 word, 19 ch).
- tool agreement: `capture-text.py <raw> --locate '<quote>'` → `LOCATED count=1 offset=683` (also 330, 797, 11723) exit 0, equal to independent `form.find`. Cite with the quote: raw sha256 `6063a3af…`, tool pin `2c0140bc…`, form sha256 `a8e3e7ad…`.
- Unrun: `quote-reopen.py` itself (it fetches; no fetch authorized).

## 6. Findings (reported, none fixed; frozen files untouched)

**F1 — the row’s anchor cell is the pre-round-54 form and is dead in the defined form.** `char 11170` lands on an English reference-list line (`'ilizing the ocean current to generate electricity was propos'`), `char 34374` is past the form’s end (form 27,012 chars). The six offsets do resolve in a whole-file UTF-16LE decode (64,512 chars; e.g. 11170 → `为便于文献的统计和期刊评价…`), which no lane command prints. Superseded only by `chousa-shokunin/SCORECARD.md:2735-2748` (“Round 54 pointer corrections”, nine `correction:` lines, e.g. `char34374->char25123`). Those lines cover 11, 14.1/14.4 and 15.7 — **none names section 1.2**, so row plus corrections carry no anchor for the new entry’s own section; qualifier 89/97 (`corpus/QUALITY.md:937`) is satisfied by form-name only. Any widening must go through the append-only channel; my item allows the used-by cell alone, so I do not propose one.

**F2 — the single-letter block sits outside every frozen span.** `M\nC\nN\nJ\nD\nR\nS\nP\nG\nB\nO\nK` occupies chars **444-467**; the 1.2.1 window is 250-446 and ends at the first `M`; `1．2．2 …建议采用单字母“Z”` is at 469-496, also outside. Consequence: the entry may state the alphabet in prose, but a `#### Inference` bullet must not use the letter→genre mapping as a backticked/quoted grounding token — `tools/inference-ground.py` reads spans only.

**F3 — the NEW_GROUND leg tests a different character than it greps.** `c2-count.py:153` greps `載体类型标识` (U+8F09, traditional) while `new_ground` tests `载体类型标识` (U+8F7D). Measured at base: `git grep -l '载体类型标识' b13ca7b5… -- corpus/knowledge` → exit 1 and `載体类型标识` → exit 1, so claims.md’s “absent from the base” holds for both spellings today, but the predicate would not notice a simplified-spelling collision.

**F4 — two frozen legs have zero slack.** `ANCHOR_BOUND` is exactly 3/3 (315, 330, 993) and the longest quote is exactly 36 chars against the `<=36` cap (`c2-count.py:99`). Re-cutting one anchor or one character kills C2.

**F5 — `C2=PASS` is unreachable with C2’s own pinned builder (offset semantics conflict).** `c2-count.py:101` requires `occurrences[0]==int(offset)` (quote occurrence), while the pinned builder writes `start = max(0, off - CONTEXT)` (`tools/build-spans.py:142`), and `c1-count.py:136` independently requires `offset == form.find(quote)-CONTEXT` (span start). Both branches run in the scratch root:

```
branch A  committed manifest = builder output (235 250 510 603 654 701 717 758 885 913 1380 11643)
          → 12× "ERROR CAPTURE_BIND:S101", CAPTURE_BOUND=0/12, ENTRY_QUOTES=0/12, ANCHOR_BOUND=0/3, REBUILD=MATCH, C2=FAIL
branch B  same span files, offsets rewritten +80 (315 330 590 683 734 781 797 838 965 993 1460 11723)
          → BOUND=1/1 REF_ID_UNBOUND=0, CAPTURE_BOUND=12/12, ENTRY_QUOTES=12/12, SUBSTANCE=PASS,
            ANCHOR_BOUND=3/3, INFERENCE_GROUNDED=yes, REBUILD=FAIL (BUILDER_REBUILD_MISMATCH), C2=FAIL
```

Every span file matches byte for byte in both branches; only the offset column is exclusive. (`NEW_GROUND=no` in that root is missing git history at BASE — a probe artifact, not evidence.) This corroborates the sibling verdict `R58ScribeEntryDraft` from a second, independently built root.

**F6 — C1 and C2 pin one path to opposite jobs.** `c1-count.py:165` defaults `--builder` to `LANE/tools/build-spans.py`; `c2-count.py:68` pins that same file to the round-55 sha `1ed2650a…`. A hardened builder landing at that path breaks `BUILDER_PIN`; the file staying unhardened keeps C1’s safe legs on the unhardened tool. C1’s discriminating copy is byte-identical: `sha256sum corpus/evidence/round58/controls/build-spans-r55.py` → `1ed2650a…`.

**F7 — exact-match punctuation budget for the entry author.** Frozen quotes carry U+FF0E `．`, U+FF1A `：`, U+FF1B `；`, U+FF0C `，`, U+2014 `—` and U+2013 `–` (`CD–ROM`). Any hyphen or fullwidth substitution fails the byte-exact bind.

**F8 — two frozen quotes are off-spine but mandatory.** char 1460 is a 14.1 element-order tail (`出版地:出版者,…`), and char 11723 is a fragment of the §11 heading `11中图分类号(CLC number)与文献标志码(Document code)`. They locate the layout and the separate document-code field; neither carries an alphabet or a carrier code.

## 7. Unrun (not claimed)

- `tools/research-gate.sh` verify-all and its selftests (code read only; not run).
- `tools/quote-reopen.py` (live fetch; not authorized).
- full `C2=PASS` — unreachable per F5; the lane also has no entry and no manifest yet (`corpus/evidence/round58/c2/` holds only `quotes.tsv`).
- C1 battery, C1/C2 after-receipts (other seats).
- `inference-ground` on a lane entry (entry does not exist; my PASS came from a scratch probe entry).

VERDICT: The S101 `used-by` old→new append (`corpus/knowledge/citation-count-semantics-r37.md` → `…, corpus/knowledge/carrier-alphabet-china-r58.md`) survives every check I could run — counter predicate, gate tokenizer, registry count 133 unchanged, no new SOURCES row justified — and the frozen S101 ground itself re-verifies (12/12 quotes unique at 315…11723, 3 line-start, form byte-identical to round-54’s pin); the attack that lands is on the frozen predicate, not the row: C2’s `CAPTURE_BIND` and its own pinned builder demand mutually exclusive `offset` semantics (branches A/B run), so `C2=PASS` is falsified as satisfiable and the row’s stale anchor cell (F1) leaves the new entry’s section unanchored outside the append-only correction channel.

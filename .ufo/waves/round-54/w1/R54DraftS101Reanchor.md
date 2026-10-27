# R54DraftS101Reanchor — S101 `anchor` cell re-pointed into the defined text form

Seat: leaf scribe, round 54 wave 1. Scope: the `anchor` cell of lane row S101 (`corpus/SOURCES.md:111`) and the six round-49 S101 span rows. The row is not rewritten; no predicate, target, counter or control of R54-C1/R54-C2 is proposed for change.

## Provenance (re-derived this round, no fetch)

| item | value | how |
|---|---|---|
| capture | `…/.qcache/6dc68fd6b32ce9c8dfcebce8.raw`, 129024 bytes, sha256 `6063a3aff7a4081e93a685f2721e2cd6b477ba84a841211e298bcddd6d9fddf3` | `sha256sum` |
| tool | `tools/capture-text.py` at `8a7d0f137a352000d78704ba5695ded8857104fe` (C1 candidate), tree clean for it | `git -C $L log -1 --format=%H -- tools/capture-text.py`; `git status --porcelain -- tools/capture-text.py` → empty; `git diff --stat 8a7d0f1 HEAD -- tools/capture-text.py` → empty at HEAD `9caf8fc` |
| defined form | 27012 code points / 47356 bytes / 470 lines, sha256 `a8e3e7ad213b6ec50479542cda23612e7ae7ae5fd4506fba53a91f2f7e79f867` | `python3 tools/capture-text.py RAW > $S/form.txt`; second run `cmp`-identical |
| old form | `raw.decode('utf-16-le',errors='replace')`: 64512 code points, 243 `\x0b`, 263 U+FFFD | python |
| defined-form sanity | `\x0b`=0, U+FFFD=0, no control char below 0x20 other than tab/newline | python over `form.txt` |
| lane check baseline | `ANCHORED=7/7 UNANCHORED=0 BAD=0` rc 0 | `python3 corpus/evidence/round53/pointer-anchor-check.py --root $L` |

## Six phrases: old offset → count in defined form → new offset

Old offsets reproduce the row's `char N` exactly in the UTF-16LE decode (`u.find(q)`), so the cell is internally consistent and its parenthetical form label is accurate about what it measured. Each phrase occurs **once** in the defined form and on one line there (`t.count(q)`=1, `'\n' not in t[o:o+len(q)]`), so each is locatable.

| # | row `char N` | phrase (≤25 words, ≤160 chars) | count | new offset | line |
|---|---|---|---|---|---|
| 1 | 11170 | 为便于文献的统计和期刊评价 | 1 | 11972 | 217 |
| 2 | 11205 | 每一篇文章或资料应根据其内容性质标识一个文献标志码 | 1 | 12007 | 217 |
| 3 | 11993 | 本规范推荐采用GB/T 7714中规定的顺序编码制格式著录,也可采用GB/T 7714中规定的作者-出版年制。 | 1 | 12795 | 241 |
| 4 | 12161 | 文献类型及载体类型标志 | 1 | 12963 | 245 |
| 5 | 13247 | 参照ISO 690及ISO 690-2，每一参考文献条目的末尾均以“.”结束。 | 1 | 14049 | 270 |
| 6 | 34374 | 参考文献格式，参照ISO 690 | 1 | 25123 | 406 |

Every old offset is dead in the defined form: `t[old:old+len(q)] == q` is False for all six and 34374 exceeds the form's length (27012) — the defined form is main story CP 0..ccpText, the UTF-16LE decode carries headers, footnotes and trailing streams. `--locate` agreed on all six, e.g. `python3 tools/capture-text.py $RAW --locate '为便于文献的统计和期刊评价'` → `LOCATED count=1 offset=11972` rc 0; tool and independent python agree on every offset.

## Round-49 span manifest (`corpus/evidence/round49/spans.tsv` rows 20-25)

Span files are UTF-16LE-form slices (`u.find(span)`), not defined-form slices (`t.find(span)`):

| span | manifest offset | quote | UTF-16LE slice at | defined-form slice at | `\x0b` in span |
|---|---|---|---|---|---|
| S101-1.txt | 11166 | q2 | 11166 | **no** | 3 |
| S101-2.txt | 11166 | q1 | 11166 | **no** | 2 |
| S101-3.txt | 12081 | q3 | 12081 | **no** | 6 |
| S101-4.txt | 11945 | q4 | 11945 | 12747 | 0 |
| S101-5.txt | 34370 | q5 | 34370 | 25119 | 0 |
| S101-6.txt | 13167 | q6 | 13167 | 13969 | 0 |

The three that are not slices at all are exactly the three carrying `\x0b` (0x0B line break), which the defined form renders as a newline; the other three survive only at shifted offsets. An offset correction cannot repair them: they are the wrong form's bytes and would need rebuilding.

## Draft correction lines (intended lane path: `SCORECARD.md`, new append-only section `## Round 54 pointer corrections`)

Round-53 anchored form `correction: FILE:LINE PTR -> TARGET anchor: "TEXT"`, TEXT ≥12 chars occurring exactly once in TARGET (`corpus/evidence/round53/pointer-anchor-check.py:26-32`). The mapping rides in the PTR token (`char<old>->char<new>`) because the anchor group must end the line; TARGET is the defined text form, so the anchor proves the new offset is the quote's first character in that form.

```text
correction: corpus/SOURCES.md:111 char11170->char11972 -> corpus/evidence/round54/S101-text-form.txt anchor: "为便于文献的统计和期刊评价"
correction: corpus/SOURCES.md:111 char11205->char12007 -> corpus/evidence/round54/S101-text-form.txt anchor: "每一篇文章或资料应根据其内容性质标识一个文献标志码"
correction: corpus/SOURCES.md:111 char11993->char12795 -> corpus/evidence/round54/S101-text-form.txt anchor: "本规范推荐采用GB/T 7714中规定的顺序编码制格式著录,也可采用GB/T 7714中规定的作者-出版年制。"
correction: corpus/SOURCES.md:111 char12161->char12963 -> corpus/evidence/round54/S101-text-form.txt anchor: "文献类型及载体类型标志；"
correction: corpus/SOURCES.md:111 char13247->char14049 -> corpus/evidence/round54/S101-text-form.txt anchor: "参照ISO 690及ISO 690-2，每一参考文献条目的末尾均以“.”结束。"
correction: corpus/SOURCES.md:111 char34374->char25123 -> corpus/evidence/round54/S101-text-form.txt anchor: "参考文献格式，参照ISO 690"
```

Line 4 note: the bare phrase is 11 characters, one short of MIN=12, so the anchor is extended by the next code point (`；`) — it still starts at 12963 and occurs once.

**Prerequisite the L1 must land with them** (I may not write production files) — the target file, tool-produced, byte-identical to my measurement:

```text
python3 tools/capture-text.py /home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache/6dc68fd6b32ce9c8dfcebce8.raw > corpus/evidence/round54/S101-text-form.txt
# expect 47356 bytes, sha256 a8e3e7ad213b6ec50479542cda23612e7ae7ae5fd4506fba53a91f2f7e79f867
```

Both states measured on a scratch mirror (`$S/mirror`: lane `SCORECARD.md` + `corpus/README.md` + the seven existing targets, six lines appended):

```text
$ python3 corpus/evidence/round53/pointer-anchor-check.py --root $S/mirror   # no S101-text-form.txt
BAD_ANCHOR corpus/SOURCES.md:111 char11170->char11972 -> corpus/evidence/round54/S101-text-form.txt anchor='为便于文献的统计和期刊评价' len=13 occurrences=0
… (six BAD_ANCHOR lines, occurrences=0)
ANCHORED=7/13 UNANCHORED=6 BAD=6            rc=1
$ cp form.txt $S/mirror/corpus/evidence/round54/S101-text-form.txt
$ python3 corpus/evidence/round53/pointer-anchor-check.py --root $S/mirror
ANCHORED=13/13 UNANCHORED=0 BAD=0           rc=0
```

Rejected alternative target, the citing entry `corpus/knowledge/citation-count-semantics-r37.md`: measured counts 1, 2, 0, 2, 1, 1, so three anchors fail the exactly-once test.

## Findings (reported, not patched)

1. **Two text forms for one capture, both called "the text form".** The C1 tool prints the defined form; the lane's span machinery still resolves this `.doc` in the UTF-16LE decode — `corpus/evidence/round54/build-spans.py:107-113` (`raw_form`: `return b.decode("utf-16le", errors="replace")` for any non-zip raw) and `corpus/evidence/round54/c2-count.py:122-133` (`form_text` → `bs.raw_form(b)`), with the anchor leg at `c2-count.py:239-243`. After these corrections land, S101's `char N` are defined-form while `spans.tsv` and `ANCHOR_BOUND` would read UTF-16LE: a *bound* S101 would fail `CAPTURE_BOUND`/`ANCHOR_BOUND`. R54-C2 holds S101 (`HELD`, no new span), so the frozen counter is untouched this round; the conflict binds the first round that tries to bind this document, and the repair belongs in `build-spans.py`'s `raw_form`, not in the row.
2. **The `.txt` sidecar is not a usable form here**: 157816 bytes, sha256 `d4e7e5adc9f723d6…`, 14486 U+FFFD, none of the six quotes present (`t.find(q) == -1`). Only the `.raw` carries the text, so the builder's first form is skipped and the UTF-16LE fallback is what every S101 span was made from.
3. **Round-42's `S096` verdict is superseded by the defined form.** `corpus/evidence/round42/receipts/verdict.txt:13` says `unverifiable` because "the local capture is a binary office document"; the tool now reads that capture and locates q2 and q4 at `count=1`, supporting round-49's hand verdict `absent-as-written` (q1 splices section 14, q3 puts GB/T 7714 where the capture says ISO 690) over `unverifiable`. Evidence for the quarantine verdict, which is another seat's call.
4. The row's parenthetical form label is stale once the six lines land, and no anchored `correction:` can carry a prose relabel (an ASCII `->` line without a trailing anchor is `UNANCHORED`). The L1 should add one prose line (no `->`); the check ignores it by design, so it is *not* evidence.

## Out of scope / not done

No row rewrite, no span rebuild, no counter run (`c1-count.py`/`c2-count.py` untouched — the counters are the L1's measurement), no fetch, no production write, no LibreOffice run. The `used-by` cell is `R54DraftRows`'s; my lines name only the `anchor` cell's pointers. Scratch `/fast/scratch/hyaku/chousa-r54/R54DraftS101Reanchor/` removed on exit; no `soffice.bin` started by this seat; no tool installed or upgraded.

VERDICT — attacked the S101 `anchor` cell against the C1 candidate's defined text form: all six UTF-16LE `char N` are dead in that form (one out of range), each phrase locates exactly once at 11972/12007/12795/12963/14049/25123, six anchored `correction:` lines score `ANCHORED=13/13` on a mirror once the defined-form dump lands (7/13, `BAD=6` without it), and the three round-49 S101 spans carrying `\x0b` are not slices of the defined form at all — the row is repairable, its spans are not.

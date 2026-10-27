# R58ExecC2Inference — S101 carrier-alphabet observation/inference/unknown outline

Seat scope: draft the compact O/I/U outline for the S101 carrier-alphabet entry from the 12 frozen quotes and the document sections only; run `inference-ground.py` on a scratch entry/manifest; report unsupported inferences and the exact grounded quote mapping. No lane edits (all writes were to my scratch and to this report).

Scratch: `/fast/scratch/hyaku/chousa-r58/R58ExecC2Inference/` (removed on yield).

## 1. Sources actually opened (lane-owned, no fetch)

| item | value |
|---|---|
| freeze commit | `9e73a031ab1ac3bac343de008850d7d87f9e5634` (lane HEAD at read time `5da0a6375a554e1229492a8cb0b9695bd8e85456`) |
| claim base | `b13ca7b5c8bbb40d2d29a37fb443c64ca043f791` |
| S101 raw | `corpus/captures/6dc68fd6b32ce9c8dfcebce8.raw`, sha256 `6063a3af…df3` — verified, matches the frozen pin |
| defined text form | `python3 -B tools/capture-text.py <raw>` → 27012 chars; byte-identical to the lane's already-committed `corpus/evidence/round54/S101-text-form.txt` (sha256 `a8e3e7ad213b6ec50479542cda23612e7ae7ae5fd4506fba53a91f2f7e79f867`) |
| frozen quotes | `corpus/evidence/round58/c2/quotes.tsv`, 12 rows, identical to the `QUOTES` list inside `c2-count.py` |

## 2. Grounded quote mapping (exact)

Quote offsets are in the 27012-char defined form. `span` = the committed span files that contain the quote.

| # | offset | span | quote |
|---|---|---|---|
| Q1 | 315 | 1,2 | `1．2 参考文献类型及其标识` |
| Q2 | 330 | 1,2 | `1．2．1 根据GB3469规定,以单字母方式标识以下各种参考文献类型：` |
| Q3 | 590 | 3 | `建议以下列双字母作为标识：` |
| Q4 | 683 | 4,5 | `被引用为参考文献时需在参考文献类型标识中同时标明其载体类型` |
| Q5 | 734 | 4,5,6,7 | `磁带(magnetic tape)—MT` |
| Q6 | 781 | 5,6,7,8 | `联机网络(online)—OL` |
| Q7 | 797 | 5,6,7,8 | `并以[文献类型标识/载体类型标识]表示` |
| Q8 | 838 | 6,7,8 | `[M/CD]—光盘图书(monograph on CD–ROM)；` |
| Q9 | 965 | 9,10 | `[J/OL]—网上期刊(serial online)；` |
| Q10 | 993 | 9,10 | `[DB/OL]—联机网上数据库(database online)；` |
| Q11 | 1460 | 11 | `出版地:出版者,出版年:起止页码(当整体引用时不注).` |
| Q12 | 11723 | 12 | `与文献标志码(Document code)` |

All 12 occur exactly once in the defined form (`text.find` count 1 each). Q2 contains **U+FF0C FULLWIDTH COMMA**, not ASCII `,`; Q8 contains **U+2013 EN DASH** inside `CD–ROM`; Q5–Q10 contain **U+2014 EM DASH**. A hand-typed entry silently loses Q2 and fails `ENTRY_QUOTES` — this is the single most likely way a hand-written entry breaks.

Every one of the 12 is carried in my drafted Inference section (Q12 is additionally carried in Observation). Ground run:

```
$ python3 -B tools/inference-ground.py --entry entry3.md --spans out/spans.tsv \
    --counts /dev/null --registry corpus/SOURCES.md --root .
GROUND entry=entry3.md section=1 bullets=6 tokens=13 grounded=13
GROUND: PASS   (exit 0)
```

## 3. The outline (drafted, byte-exact generator `gen_entry.py`)

**Observation** — six bullets: the `1．2` section head and its `1．2．1` single-letter rule; the 电子文献类型标识 two-letter column (DB/CP/EB); the `1．2．4` carrier rule and its four-pair list; the `[文献类型标识/载体类型标识]` bracket and the three worked examples; the entry template with `[文献类型标识]` as an optional slot; section 11's `中图分类号(CLC number)与文献标志码(Document code)` head and rule 11.1.

**Inference** — six bullets: type alphabet and carrier alphabet are two separate mechanisms; the electronic two-letter column is separate from the single-letter column; the carrier alphabet is two letters from a fixed list; the slash form is a compound of two identifiers; the type identifier is one optional entry slot while the document code is a separate per-article field; the electronic column and the carrier list answer different questions.

**Unknown** — seven bullets: the name→letter pairing (never adjacent text); the five A–E codes of 11.6; the paper-carrier exemption (window truncates it); the `Z` fallback rule; the second parallel statement of the same rules (§14.3, outside every window); GB3469 itself not captured; present-day validity out of scope.

## 4. Unsupported inferences I excluded (and why)

1. **Name→letter pairing.** The capture renders table cells one per line (`普通\n图书\n…` then `文献类型\n标识\nM\nC\n…`), so a type name and its letter are never adjacent text. §1.2.1 lists 12 letters (M C N J D R S P G B O K) against 12 type names; §14.3.1 lists 10 letters (M C N J D R S P G K) against 10 names — **the two lists are not the same**. The pairing is not asserted anywhere in the entry.
2. **`载体类型标识` / `文献类型标志` confusion.** The located §1.2 family uses 标识 (`文献类型标识`, `载体类型标识`); the §14.3 family uses 标志 (`文献类型标志`, `载体类型标志`) and `CD-ROM` (ASCII hyphen) and `——` (double em dash). The two families are textually distinct and both exist in the capture. Only §1.2 is inside a located window, so the entry says nothing about §14.3.
3. **The five document codes A–E.** Present in the capture at char 12045 but in no window (S101-12 covers 11643–11824). Recorded as unknown.
4. **The `Z` fallback rule.** At char 469, in the *gap* between windows S101-2 [250,446) and S101-3 [510,683). Present in the form, absent from every span. Recorded as unknown.
5. **The paper-carrier exemption.** The full sentence occurs twice in the form (chars 1081, 13825) but S101-10's window cuts it at `…不必注明其载` (4 chars short). The entry quotes only the truncated, located form.
6. **Table shape.** I did not claim a "two-column table": `capture-text.py` flattens the OLE Word text, and the cell/row marks (U+0007, 54 occurrences in the raw) are not preserved in the defined form. The entry says the names and letters stand one per line, which is what the form shows.
7. **Every quoted string was re-checked verbatim** against the defined form: all 17 quoted strings have `form.count == 1` except the truncated paper sentence (`== 2`, because the sentence repeats in §14.3), and each is present in at least one committed span.

## 5. Frozen-counter findings (evidence only — no lane edits)

### 5a. The pinned builder and the frozen C2 counter disagree on the `offset` column — C2 is unreachable as frozen

`tools/build-spans.py` (sha256 `1ed2650a…`, the pinned round-55 builder) writes **`offset` = the span start** (`build()`: `start = max(0, off - CONTEXT)`; `lines.append(... str(start) ...)`), and `CONTEXT = 80`. The frozen `c2-count.py` requires the opposite: `occurrences[0] != off` → `CAPTURE_BIND`, where `occurrences` are the *quote* offsets, and it recomputes `expected = form[max(0,off-80) : off+len(quote)+80]` for `SPAN_BYTES`, plus `form.rfind('\n',0,off)+1==off` for the anchor count.

Measured on the builder's own output (every row differs by exactly 80 = `CONTEXT`):

```
S101 manifest_off=235 quote_true_off=315 match=False spanbytes_ok=False   … (all 12 rows, delta=80)
```

And the leg-by-leg result, same spans, two conventions:

| manifest convention | CAPTURE_BIND | SPAN_BYTES | anchors | REBUILD |
|---|---|---|---|---|
| builder's (span start) | **0/12** | **0/12** | **0/3** | MATCH |
| quote offset | 12/12 | 12/12 | 3/3 | **FAIL** |

Full counter runs in a scratch clone of the lane (`git clone --local` of the lane; `git rev-parse --show-toplevel` = the clone):

- builder-produced manifest → `CAPTURE_BOUND=0/12 ANCHOR_BOUND=0/3 ENTRY_QUOTES=0/12 … C2=FAIL` (12× `CAPTURE_BIND:S101`; `REBUILD=MATCH`).
- quote-offset manifest → `CAPTURE_BOUND=12/12 ANCHOR_BOUND=3/3 ENTRY_QUOTES=12/12 SUBSTANCE=PASS INFERENCE_GROUNDED=yes NEW_GROUND=yes REBUILD=FAIL` (`ERROR BUILDER_REBUILD_MISMATCH`).

The two legs are **mutually exclusive**: `REBUILD` demands the committed manifest be byte-identical to the pinned builder's output (span-start offsets), while `CAPTURE_BIND`/`SPAN_BYTES`/anchors demand quote offsets. I confirmed the third possibility is also closed — a scratch builder patched to write `str(off)` gives `REBUILD=MATCH` and all content legs green, but then `ERROR BUILDER_PIN` (sha256 ≠ the frozen pin). So no committed manifest satisfies the frozen C2 predicate as written. **This is a finding against the frozen counter, not a fix; claims.md is not mine to reinterpret.**

Note the historical precedent is the *other* convention: round-52's `c2-count.py` reads `offsets.setdefault(sid, set()).add(int(offset) + span.find(quote))` — i.e. it adds the quote's position inside the span to the recorded offset, treating the recorded offset as a span start. Round-58's counter dropped that correction.

### 5b. C1 and C2 cannot both hold the same `tools/build-spans.py` bytes

C1's counter defaults `--builder` to `tools/build-spans.py` and *requires* it to change (the r55 builder fails 6 of 7 refusal legs and deletes the FOREIGN fixture). C2's counter requires `sha256(root/'tools/build-spans.py') == 1ed2650a…` (`BUILDER_PIN`) **and** rebuilds the manifest with that same file. Modifying the builder by one byte (simulated in the scratch clone) yields `ERROR BUILDER_PIN` + `ERROR BUILDER_REBUILD_MISMATCH`. C1 and C2 as frozen are in direct conflict on one file; C2's own text claims they are "independent of C1's tool change".

### 5c. Minor: `NEW_GROUND` tests two different strings

Line 153 greps the base tree for **traditional** `載体类型标识` (U+8F09) while line 154 requires **simplified** `载体类型标识` (U+8F7D) in the new entry. Both are absent from the base's `corpus/knowledge` (verified: `git grep -l` rc=1 for each), so the leg is green here — but a base that carried only the simplified form would pass the "absent from base" half. Low severity at this base; flagged, not fixed.

## 6. What I ran (commands and observed output)

```
$ sha256sum corpus/captures/6dc68fd6b32ce9c8dfcebce8.raw
6063a3aff7a4081e93a685f2721e2cd6b477ba84a841211e298bcddd6d9fddf3
$ python3 -B tools/capture-text.py <raw> > form.txt     # rc=0, 27012 chars
$ sha256sum form.txt corpus/evidence/round54/S101-text-form.txt
a8e3e7ad…f867  (both identical)
$ python3 -B tools/build-spans.py --quotes corpus/evidence/round58/c2/quotes.tsv \
    --out out --cache corpus/captures
QUOTE S101 char 315 … SPANS_ROWS=12 WRITTEN=12   (rc=0)
$ python3 -B tools/inference-ground.py --entry entry3.md --spans out/spans.tsv \
    --counts /dev/null --registry corpus/SOURCES.md --root .
GROUND entry=entry3.md section=1 bullets=6 tokens=13 grounded=13 / GROUND: PASS   (rc=0)
$ python3 -B corpus/evidence/round51/quote-substance-check.py out/spans.tsv
IDS=1 QUOTES=12 FAILURES=0   (rc=0)
$ python3 -B corpus/evidence/round58/c2-count.py --root <scratch clone> --work <fresh>
  builder manifest → C2=FAIL (CAPTURE_BOUND=0/12, REBUILD=MATCH)
  quote-offset manifest → C2=FAIL (CAPTURE_BOUND=12/12, REBUILD=FAIL)
  quote-offset builder → C2=FAIL (REBUILD=MATCH, ERROR BUILDER_PIN)
```

Not run (no authorization / out of scope): any live fetch; the round-57 r2 egress-scope L0 question (left open, no fetch); `c1-count.py` against a candidate hardened builder (that is the C1 executor's seat); any lane write other than this report; any git/jj mutation of the lane (the scratch clone's commits were confined to the clone and were reset).

## 7. Bottom line for the L1

The **entry content is ready and defensible**: an O/I/U outline whose every quoted string is byte-verbatim against the committed capture, whose 12 frozen quotes each bind to a unique offset and to at least one committed span, and which passes `inference-ground.py` (13/13 tokens grounded) and `quote-substance-check.py` (0 failures) with zero unsupported inferences. My draft is byte-generated from `quotes.tsv` specifically so the U+FF0C / U+2013 / U+2014 punctuation cannot drift.

The **C2 predicate itself is not satisfiable as frozen**: `c2-count.py`'s `CAPTURE_BIND`/`SPAN_BYTES`/anchor legs demand quote offsets, its `REBUILD` leg demands the pinned builder's span-start offsets, and `BUILDER_PIN` freezes the builder bytes that C1 is required to change. Three independent legs, each individually blocking. Integrating C2 as frozen yields `C2=FAIL` for any entry, including a perfect one.

VERDICT: the S101 carrier-alphabet outline (Observation/Inference/Unknown, 12 frozen quotes, exact quote→span mapping, unsupported inferences excluded) **survives** on content — `inference-ground.py` GROUND: PASS 13/13, `quote-substance-check.py` 0 failures, every quoted string byte-verbatim in the committed capture; but the attack "C2=PASS is reachable with the frozen counter" is **falsified** — the frozen `c2-count.py` is internally unsatisfiable (quote-offset `CAPTURE_BIND`/`SPAN_BYTES`/anchors vs span-start `REBUILD`, plus `BUILDER_PIN` against C1's required edit), so C2 measures `FAIL` for every entry, and the claim's "C2 is independent of C1's tool change" is **falsified**. The remaining item (whether the quote set or the counter's offset convention is the intended one) is **inconclusive** from my seat — it is a lane-owner decision on frozen artifacts, which I did not alter.

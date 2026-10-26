# R52SimplifyCapture — YAGNI review of the C1 tool and the round-52 C1 counter

Leaf simplifier, wave 1. Lane `/home/vgpnk/Projects/shokunin/chousa-shokunin` read-only, no lane
file edited. Scratch `/fast/scratch/hyaku/chousa-r52/R52SimplifyCapture`, removed on exit.
Subjects, final validation: `tools/capture-text.py` (135 lines, `8e1ac6e4…b3e9`) and
`corpus/evidence/round52/c1-count.py` (341 lines, `4ec29333…101cbaa`).

**Intervening changes, disclosed (not mine).** The tool moved three times while I worked: `3986a971`
at my start (= `git show HEAD:…`) → `1726cd04` (20:10) → `9efd1fd6` (20:14) → `8e1ac6e4` (20:15): a
root guard, `el.clear()` per end event, `bounded`/`MAX_PART = 256 MiB`, an escaping-target refusal,
`except MemoryError`. I re-ran the whole matrix on the last two digests (both `LEGS=9/9 C1=PASS`);
cited sites are lines **as of `8e1ac6e4`** and named by expression so a later revision can be
matched. Measured effect: `cb101e95…`, `e9761e99…` (`.xlsx`, officeDocument → `xl/workbook.xml`) went
`rc=0`/0 bytes → `rc=2 REFUSED … is not WordprocessingML`, inside the frozen refusal enumeration only
if a non-WordprocessingML main part counts as "no officeDocument relationship … or whose target is
missing". No change proposed; flagged for the L1.

## Method

Each candidate deleted alone in a scratch copy (diff: only the intended hunk); counter rerun with
`--tool <copy>`, `--seed 52`, `--work` in scratch, default `--per-leg`:

```
$ python3 corpus/evidence/round52/c1-count.py --tool $S/tools/base.py --seed 52 --work $S/w
PARAS/RUNS_ENTITIES/REVISIONS/LAYOUT/ALTCONTENT/MAIN_PART/LOCATE/REFUSE=PASS
REAL=PASS rc=0 count=1 locate=(0, 1, 8996) chars=19682
LEGS=9/9 / C1=PASS / exit=0
$ diff -q out/finalbase.txt out/<variant>.txt
IDENTICAL: d1 d2 d3 d5 d6 d8 d9 d10-escape d11-bounded d12-memory counter-d4 counter-d7 (all 12)
```

The legs distinguish none of them, so selection rests on out-of-leg probes built from the counter's
own `package()` helpers — packages no leg generates.

## Candidates on `8e1ac6e4`

| # | site | leg-exercised | deleting it (observed) | verdict |
|---|---|---|---|---|
| 1 | tool:129 `if a.locate else 0` | no | `--locate ''`: `count=0 offset=-1` → `count=12 offset=0`, exit 1 both | keep |
| 2 | tool:96 `stack and` | no | nothing on any input: identical receipt and identical P2 refusal | **delete (made)** |
| 3 | tool:69 `TargetMode != "External"`; :71-72 escaping target | no (new, sibling's) | exit 2 + REFUSED either way; reason becomes `'https:/example.invalid/x.docx' …` / `… is not in the package` | message-only; keep |
| 4 | tool:70 `posixpath.normpath(…)` | no (no leg makes a `./`/`../` target) | `./word/document.xml` package: found → `REFUSED … not in the package`, exit 2 | **live, keep** |
| 5 | tool:110 `ET.ParseError` in the tuple | no (no leg ships a malformed part) | malformed part: REFUSED exit 2 → traceback exit 1 | keep |
| 6 | tool:64-65 `except KeyError` | no (`REFUSE` "norel" ships a valid `_rels/.rels`) | zip without `_rels/.rels`: REFUSED exit 2 → `KeyError` traceback exit 1 | **predicate-required, keep** |
| 7 | tool:66-67 `_rels/.rels does not parse` | no | same rc and prefix, `unreadable package: syntax error…` | redundant refusal; keep |
| 8 | tool:92-93 root-not-`w:document` | no (new) | non-document root: REFUSED exit 2 → the pre-guard `''` exit 0 | keep (author's scope call) |
| 9 | tool:54/62/74 `bounded`+`MAX_PART`; :112 `except MemoryError` | no (no leg ships a >256 MiB part) | identical on every probe; a 2 GB part is read unbounded, an OOM is an uncaught traceback | keep (bomb/OOM guards) |
| 10 | counter:142 `sp == chr(ord(sp)) and` | no | none: identity for every 1-char string | **delete (made)** |
| 11 | counter:237-238 `except (KeyError, ValueError): return None` | no | garbage tool: `LOCATE=FAIL` line → `KeyError 'count'` traceback, no per-leg lines | keep |
| 12 | counter:253-254 `per_leg < 1` | no | `--per-leg 0` → vacuous `LEGS=9/9 C1=PASS`, no package generated | **keep: blocks a false pass** |

Candidate 2 died *because of* the sibling's guard: the only `start` event with an empty `stack` is the
root, a non-`w:document` root now refuses at :92 before any break element, and `w:document` is not in
`RUN_BREAKS`. On `3986a971` the same deletion crashed (`IndexError`); now base and d2 both print
`REFUSED … (root {…}workbook)`. The round's own edit subsumed the old guard; the one genuine lane trim
is at `tools/capture-text.py:96`:
`elif not fallback and el.tag in RUN_BREAKS and stack and stack[-1] == W + "r":` → drop `stack and`.

## Probe receipts (base vs. the variant that should differ)

```
P1 empty-quote   base/d2..d12 rc=1 'LOCATED count=0 offset=-1'  d1 rc=1 'LOCATED count=12 offset=0'
P2 root w:tab    base=d2..d12 rc=2 "REFUSED main part 'word/document.xml' is not WordprocessingML (…)"
P3 external      base rc=2 'REFUSED no officeDocument relationship in _rels/.rels' | d3 rc=2 "REFUSED officeDocument target 'https:/example.invalid/x.docx' is not in the package"
P4 dot-target    base rc=0 'alpha beta' | d5 rc=2 "REFUSED officeDocument target './word/document.xml' is not in the package"
P5 malformed     base rc=2 'REFUSED unreadable package: no element found: line 1, column 117' | d6 rc=1 'xml.etree.ElementTree.ParseError: same'
P6 no _rels      base rc=2 'REFUSED no _rels/.rels in the package' | d8 rc=1 'KeyError: "There is no item named \'_rels/.rels\' in the archive"'
P8 bad _rels     base rc=2 'REFUSED _rels/.rels does not parse: syntax error: line 1, column 0' | d9 rc=2 'REFUSED unreadable package: syntax error: line 1, column 0'
P9 escaping      base rc=2 "REFUSED officeDocument target '../word/document.xml' leaves the package root" | d10 rc=2 '… is not in the package'
P7 locate(garbage) base -> None | d7 raises KeyError 'count' | --per-leg 0: guarded "per-leg must be >= 1" exit 2, unguarded LEGS=9/9 PASS
```

P6 is the sharpest gap: the predicate's first refusal clause ("a zip with no officeDocument
relationship … exit 2 and a `REFUSED` stderr line") is satisfied by the `KeyError` arm, and the leg
named `REFUSE` never reaches it — its `norel` package carries a valid `_rels/.rels` with a
non-officeDocument Type. Same shape for #3-5, #8 (`../` and non-document roots), #9 (>256 MiB part).
Recording the gaps is mine; changing a leg, counter or predicate is not.

## Is the second docx reader in build-spans.py justified?

Yes — by separability, and by a measured difference in what the two functions are. Independence
holds mechanically: neither `c2-count.py` nor `build-spans.py` reads `tools/capture-text.py` (only
textual hit: build-spans.py:15, its docstring), and `c2-count.py:89-90` imports the builder by path.
The claims' separability sentence is explicit that C2 goes through "the round-52 span builder, which
carries its OWN `.docx` reader (`build-spans.py` `docx_text`), and never runs
`tools/capture-text.py`" — an import would make a frozen sentence false: an erratum, not a trim.

They are not one function twice: the tool is *partial* (refuses), the builder's `raw_form` is *total*
(never refuses; falls back to UTF-16LE). Census of every zip `.raw` in the read-only cache (8 of 2596):

```
3a8b4597 tool_rc=0 len=19682 builder=19682 equal=True   # pinned NIPH capture
b825f17c tool_rc=0 len=18841 builder=18841 equal=True
cb101e95 tool_rc=2 len=0     builder=0     equal=True*  # xlsx; e9761e99 identical (*same bytes, other verdict)
9990f370/6fef2cd8/bcaebc1a/68a1f5a9 tool_rc=2 len=0 builder=1220633/33838/3259926/2802790 equal=False
```

(`*` same bytes, different verdict.) They agree byte-for-byte where a package is a readable
WordprocessingML part — including the claim's 19682 characters — and diverge only at the boundary,
where the builder has no refusal vocabulary. An import would not remove that: the builder still needs
a form for bytes the tool rejects (refusal comes later, as "quote not exactly once in any form"), and
would need a bytes interface the path-based tool lacks — a C1-frozen edit for ~29 lines
(`build-spans.py:76-104`).

Tradeoff: the duplication has already drifted — `TargetMode` filtering (tool only, :69), dangling-target
order (tool refuses at :76; the builder's `next()` takes the first officeDocument rel and `z.read` then
fails → `None`), and partial-vs-total. Each drift is benign for C2 today only because the
quote-exactly-once test rejects those forms; if ever single-sourced, the honest shape is
`text_form(bytes)` in the tool with the path/stdout wrapper on top — a round-53 erratum.

## Contract, footprint, tradeoff

`LEGS=9/9 C1=PASS`, `REAL … chars=19682` unchanged under every variant; predicate, legs, target and
controls untouched; both lane files byte-identical to the digests above. Deletions exist only in
scratch (counter:142, tool:96), each proven neutral by the identical receipt; the other ten candidates
are unexercised guards, not dead weight — "no leg exercises it" and "deletable" differ.
VERDICT: attacked 14 unexercised branches in the C1 tool and its counter — two are provably dead and
deleted in scratch (tool:96, subsumed by the sibling's new root guard; counter:142, an identity); the
rest each change an exit code, a package or a counter verdict; the build-spans second reader is
justified by the frozen separability sentence plus a measured partial-vs-total difference.

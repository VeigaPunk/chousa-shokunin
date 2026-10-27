# R53CritForgeC2 — first falsification of the frozen C2 counter (round 53, wave 1)

Attacked: `corpus/evidence/round53/c2-count.py` (frozen, not modified). Everything below was
built only under `/fast/scratch/hyaku/chousa-r53/R53CritForgeC2/root` and run with
`--root` pointing there; nothing in the lane was written except this report. No tool was
installed (no install expected). `TMPDIR=/fast/scratch/hyaku/chousa-r53/R53CritForgeC2`
for every counter run.

## 1. The cheapest lane bytes that print `C2=PASS`

Scratch root contains: `corpus/SOURCES.md` (Registry with exactly three NEW rows), two
existing entries (`corpus/knowledge/western-instrument-alignment-r50.md`,
`corpus/knowledge/quality-control-guideline-issued-text-r48.md`), `corpus/lessons/round-53.md`,
`corpus/evidence/round53/quotes.tsv` + `spans.tsv` + `spans/` (derived by the frozen
`build-spans.py`), and a copy of `tools/inference-ground.py`.

Configuration (all shortcuts active at once):

- **Entries: 2 of 3** — `search-tracking-record-r40.md` does not exist; the lesson names it
  with `refused-entry corpus/knowledge/search-tracking-record-r40.md`.
- **Documents: 3 bound / 2 refused** — bound `S118` (QCG PDF), `S119` (release notice),
  `S121` (Cochrane Handbook ch.4, **navigation/boilerplate quote**); refused JMLA paper and
  NMPA copy (no row, no `source:` line, `refused-doc <url>` lines in the lesson).
- **Quotes: 3 distinct strings, 9 rows** — each bound id reuses ONE quote in all three of its
  rows (`三、主要思路及内容 …3` @336, notice `<title>` @10, `Skip to main content` @109).
- **Anchors: one `char N` per bound row** (N = the single shared quote offset per id).
- **Inference bullets quote the phrases but assert claims the counter never compares to them.**
- No `S###` token appears outside the bound ids; the lesson contains the three quote strings.

Observed run (verbatim):

```
$ TMPDIR=/fast/scratch/hyaku/chousa-r53/R53CritForgeC2 python3 \
    chousa-shokunin/corpus/evidence/round53/c2-count.py --root /fast/scratch/hyaku/chousa-r53/R53CritForgeC2/root
ENTRIES=2/3 (min 2) REFUSED_ENTRIES=1
BOUND=3/5 (min 3) REFUSED=2
BOUND_IDS=S118,S119,S121
REF_ID_UNBOUND=0
NEW_GROUND=2/2
QUOTE_ROWS=9 ON_BOUND=9/9
SPAN_IDS=3/3 (min 3 each)
QUOTES_IN_SPAN=9/9
QUOTES_IN_ENTRY=9/9
QUOTES_IN_LESSON=9/9
QUOTE_SHORT=9/9
SPAN_CONTEXT=9/9
CAPTURE_BOUND=9/9
SUBSTANCE=PASS
ANCHOR_BOUND=3/3
INFERENCE_GROUNDED=2/2
QUARANTINE_VERDICTS=0/0 ()
QUARANTINE_BLOCKED_ADOPTED=0
C2=PASS
exit=0
```

The spans manifest is the frozen `build-spans.py` output (cache `.txt` digests recorded,
slices exact):

```
$ python3 chousa-shokunin/corpus/evidence/round53/build-spans.py --root …/root
QUOTE S118 char 336 spans/S118-1.txt
QUOTE S119 char 10 spans/S119-1.txt
QUOTE S121 char 109 spans/S121-1.txt
QUOTE S118 char 336 spans/S118-2.txt
QUOTE S119 char 10 spans/S119-2.txt
QUOTE S121 char 109 spans/S121-2.txt
QUOTE S118 char 336 spans/S118-3.txt
QUOTE S119 char 10 spans/S119-3.txt
QUOTE S121 char 109 spans/S121-3.txt
SPANS_ROWS=9 WRITTEN=9
```

Quotes are byte-exact one-line captures: `Skip to main content` occurs exactly once at char
109 of `c9d1e74c3ac8d9eb332c9770.txt` (the Cochrane HTML .txt, line 27 — a skip-link/nav
item); `《药品临床综合评价质量控制指南（2024年版 试行）》发布_北京市卫生经济学会` at char 10 of
`cfa080b4046592eb9490a82c.txt` (the page `<title>`); `三、主要思路及内容 …3` at char 336 of
`16fe8487aa97b98576a0dbac.txt` (a table-of-contents row of the guideline PDF). Span files are
the exact slices: `S118-*` 272 B, `S119-*` 195 B, `S121-*` 194 B; digests
`927ff71c…d3a4`, `892da7ad…dfeb`, `722d3ce9…d97c` (sha256 of the three `.txt`).

## 2. Which shortcuts pass and which leg refuses each

| # | Shortcut | Result | What enforces / what lets it pass |
|---|---|---|---|
| 1 | Quote from navigation/boilerplate (Cochrane `Skip to main content`) | **PASSES** | `SUBSTANCE` floor is length-only (`quote-substance-check.py` MIN_CHARS=3, LONG_CHARS=12); no topicality check. |
| 2 | Same quote reused in all 3 rows of an id | **PASSES** | `SPAN_IDS` counts ROWS (≥3 per id), not distinct quotes; `PER_ID` never compares quote strings. |
| 3 | Third entry refused (2/3) | **PASSES** | `MIN_ENTRIES=2` + one `refused-entry` lesson line. Round 52 demanded exactly `len(texts)==3`; this is a real weakening. |
| 4 | Two documents refused (3 bound/5) | **PASSES** | `MIN_BOUND=3`, `BOUND+REFUSED=5`; refusal needs only no row + no `source:` line + `refused-doc` line. |
| 5 | One anchor offset per bound row | **PASSES** | `ANCHOR_BOUND` needs ≥1 `char N` per row and `N` in `offsets[id]`; reused quote collapses `offsets` to one value. |
| 6 | Inference bullet quotes a phrase but asserts something else/opposite | **PASSES** | `inference-ground.py` checks verbatim presence in spans + lexical polarity windows; unrelated assertions never flip. See demo E. |
| 7 | Hollow quote (`ab`) | REFUSED | `SUBSTANCE=FAIL` (HOLLOW_QUOTE). |
| 8 | Whole-capture span | REFUSED | `SUBSTANCE=FAIL` (OVERWIDE_SPAN), even though `CAPTURE_BOUND=9/9` slices still hold. |
| 9 | Invented digest (`0`×64) | REFUSED | `CAPTURE_BOUND=8/9`. |
| 10 | Unbound staged token (`S134` in an entry) | REFUSED | `REF_ID_UNBOUND=1`. |
| 11 | Refusing docs without `refused-doc` lesson lines | REFUSED | `BOUND=3/5 REFUSED=0` → `BOUND+REFUSED=3`. |

Demo runs (each a copy of §1 root with one mutation):

```
DEMO_A hollow quote (lane-only): exit 1   SUBSTANCE=FAIL
DEMO_B whole-capture span:      exit 1   CAPTURE_BOUND=9/9 SUBSTANCE=FAIL
DEMO_C invented digest:          exit 1   CAPTURE_BOUND=8/9
DEMO_D unbound S-token:         exit 1   REF_ID_UNBOUND=1
DEMO_E assert-opposite bullet:   exit 0   INFERENCE_GROUNDED=2/2 C2=PASS
DEMO_F no refused-doc lines:    exit 1   BOUND=3/5 (min 3) REFUSED=0
```

Demo E bullet: `- S121 carries the boilerplate navigation item `Skip to main content`, which
shows the chapter does not exist.` — `inference-ground` reports `GROUND: PASS` and the counter
prints `C2=PASS`: the assertion literally contradicts the quoted page while sharing none of
the phrase's content words, so the polarity machinery has nothing to flip.

## 3. Structural notes for the closure

- The `DOCS` tuple's **staged-id field is never read** by `c2-count.py`: binding keys only on
  the URL and the existing entry paths. Any new lane id (or the staged id itself) binds, and
  no correlation with the campaign package is checked.
- `QUOTES_IN_LESSON` is satisfied by the three quote strings appearing anywhere in the lesson;
  the L1 must not strip them when writing the real lesson.
- `BOUND` rows only need `status=mined`, `opened=2026-10-26`, `used-by` exactly equal to the
  sorted existing citing entries, and a `source: <id> — <url>` line in each citing entry;
  nothing inspects the row's `scope`/`teaches` prose.
- **Round-52 comparison**: round-52 `c2-count.py` required `len(texts) == 3` and "all three
  entries exit 0"; round 53 relaxes to `MIN_ENTRIES=2` plus a counted `refused-entry`, and
  allows up to 2 refused documents (round 52 allowed refusal but at a 3-bound floor from 4
  docs). The cheapest passing config therefore re-grounds only 3 of 5 docs and 2 of 3
  entries — a genuine weakening versus round 52's 3/3.

## 4. Hand spot-checks the closure must perform (not counted by the counter)

1. **Entailment** — for each inference bullet, read the quoted passage and decide whether the
   bullet's assertion follows. The counter verifies presence and lexical polarity only (§1
   bullets and demo E are designed to pass without entailment).
2. **Quote substance** — confirm each quote sits in the document BODY, not in navigation
   chrome (skip link), an HTML `<title>` element, or a table-of-contents row.
3. **Distinctness** — per bound id, require 3 *different* located quotes rather than 3 rows
   of one quote.
4. **Anchor coverage** — require 3 distinct offsets per id (one per quote), not one shared
   `char N`.
5. **Refusal honesty** — the two refused docs (JMLA paper, NMPA copy) are the deepest
   instruments; confirm the refusals are genuine (opened, failed) rather than avoidances.
6. **Staged correlation** — confirm the lane ids actually map to the package's staged entries
   (S117–S121), since the counter never checks the `DOCS` staged ids.

VERDICT: attacked the frozen C2 counter; built a 9-row span kit with 3 distinct cheap quotes
(one reused thrice per id, incl. Cochrane nav boilerplate), 2/3 entries, 2 refused docs, one
anchor offset per id, and non-entailment bullets — prints `C2=PASS` exit 0; hollow quotes,
whole-capture spans, invented digests and unbound S-tokens are each refused
(SUBSTANCE/CAPTURE_BOUND/REF_ID_UNBOUND).

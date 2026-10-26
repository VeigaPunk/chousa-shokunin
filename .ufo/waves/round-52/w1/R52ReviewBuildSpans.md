# R52ReviewBuildSpans — round-52 `build-spans.py` / `c2-count.py` vs round-51 originals

Seat: R52ReviewBuildSpans · 2026-10-26 · lane `chousa-shokunin`
Method: the two mandated `diff`s (all hunks enumerated below), unit probes on
`docx_text`/`raw_form` (imported from the r52 builder), an end-to-end CR fixture in
scratch, the NIPH capture comparison, and live `--check` / counter runs (TMPDIR set to
my scratch; counters only read). No tool installs made (none needed; pacman untouched).

## F1 LOW — predicate text differs from claims.md in one parenthetical

Normalized-whitespace diff of the `c2-count.py` docstring predicate vs the
`claims.md` R52-C2 predicate (2048 vs 2021 chars) — the only delta:

```
-(the -sweep -prints -how -many: -1
+(1
```

i.e. docstring "(the sweep prints how many: 1 at the freeze, S120)" vs claims.md
"(1 at the freeze, S120)". Every operative token (count 1, id S120, both
verdict exclusion lists, all other clauses) is identical; claims.md declares the
docstring canonical. Editorial divergence only — a `claims-erratum.md` line would
remove the delta. No counter behavior depends on it.

## F2 ANSWERED-OK — a docx form containing `\r` is safe

A docx form can contain `\r` only via character references: literal CRs in XML are
parser-normalized to LF, and `w:cr`/`w:p` emit `\n` by rule.

```
make_docx(<w:t>A&#xD;B NEEDLE C</w:t>) -> docx_text == 'A\rB NEEDLE C\n'
```

The r49 CR clip (code unchanged r51→r52, condition `fname.endswith(".raw")`, so it
covers docx raws) searches the last CR before the quote and the first after it, so a
span body is CR-free unless the quote itself contains CR — and a CR-bearing quote
cannot reach a span: `read_quotes` uses `read_text()` universal newlines (CR→LF, then
count 0 → refusal), and a bare CR in quotes.tsv splits the row (observed:
`exit 2 · need 4 non-empty tab cells, got 3`). End-to-end fixture (entity-CR docx in
scratch cache, `--root` at a scratch fixture):

```
QUOTE S113 char 109 spans/S113-1.txt   SPANS_ROWS=1 WRITTEN=1
span bytes CR-free: True | universal readback == disk: True
ft[o:o+len(span)] == span: True        --check: SPANS_ROWS=1 STALE=0 exit 0
```

No corruption path found; the exact-slice invariant survives entity CRs.

## F3 ANSWERED-OK — `raw_form` fallback on non-OOXML zip

| input | docx_text | raw_form |
|---|---|---|
| zip without `_rels/.rels` | None | UTF-16LE, U+FFFD garbage |
| zip whose rels lack officeDocument | None | UTF-16LE, U+FFFD garbage |
| corrupt `PK\x03\x04…` bytes | None | UTF-16LE garbage |
| OLE `.doc` magic `D0 CF 11 E0` | None | `== b.decode("utf-16le", errors="replace")` (round-48 path preserved) |
| valid OOXML, no text elements | `''` | `''` (correct empty form; refusal downstream) |

Garbage forms cannot hold a quote exactly once, so they end in the builder's
`refused` exit 1 / counter `CAPTURE_BOUND` miss — refusal, never a false bind.
Docstring nuance only: "for a zip … else UTF-16LE" — a PK zip that parses as OOXML
always yields the docx form (even empty), never UTF-16LE; that is the rule's intent.

## F4 OK — r51 contract preserved

- `OUT_HEADER` (7 columns) and the `build()` row shape byte-identical (no diff hunk).
- `capture_sha256` = sha256 of the FILE read (`.txt` or `.raw`) in both the builder
  `form_texts` and the counter `form_text` — a reader re-derives the form from the
  digest, as in r51.
- Form order `.txt` first, then raw form — unchanged; CR clip unchanged;
  `CONTEXT=80`, `MIN_PER_ID=3` and the entire `ok = …` expression untouched.
- `LANE = parents[3]` asserted to resolve to the lane root for both scripts.
- Counter registry cell indices verified against `corpus/SOURCES.md` header
  (`| id | source | kind | tier | scope | anchor | teaches | status | opened |
  recheck | used-by |`): `r[1]` first source cell, `r[5]` anchor, `r[7]` status,
  `r[8]` opened, `r[10]` used-by — all as the code reads them.
- quotes.tsv ids are the new LANE ids (S113 medsci, S114 chinagp, S115 NIPH,
  S116 archive), matching the planned staged→lane mapping; staged S111/S112 keep
  their existing lane rows (SinoMed, JAHBS) and are not carried over.

## F5 OK — NIPH form equality (the C2/C1 shared rule)

```
key 3a8b45977cd111e45e3980a5 · .raw 178056 B
builder raw_form len: 19682 | capture-text.py stdout len: 19682 | equal: True
REAL quote 'SRにおける文献検索期間について明記する' count: builder form 1, .txt sidecar 0
```

The garbage `.txt` sidecar cannot win the frozen `.txt`-first order for the NIPH
capture, and the builder's reader is byte-identical to the C1 tool on it.

## F6 OK — no r51 leg silently weaker

- `MIN_BOUND 5→3` over `7→4` documents is the frozen claim itself ("at least three"
  of four); proportionally stricter (75% vs 71%), and `nbound + refused == 4` retained.
- `HELD` was `set()` (empty) in r51 (diff hunk `81d81 < HELD: set[str] = set()`);
  dropping it from the `unb` sum is a behavioral no-op.
- Substance leg: r51 `subst = ev/"quote-substance-check.py"` (root-relative) → r52
  `LANE/corpus/evidence/round51/quote-substance-check.py`. Same script and thresholds
  (`MIN_CHARS=3`, `LONG_CHARS=12`, width cap `len(quote)+2*80+2`); identical under the
  default `--root`, strictly more robust under a fixture `--root`.
- `ALIASES = {ORIGINAL: ARCHIVE}` only ADDS a sweep-theme mapping (register rows
  naming the dead original count); live register yields exactly
  `reg_ids == {'S120': NIPH}` — matching the frozen "(1 at the freeze, S120)"; the
  alias is currently inert (no register row names the lifescience URL today).

## F7 Live machinery smoke (wave state at review time)

```
build-spans --check: SPANS_ROWS=38 STALE=0 (exit 0)
c2-count: ENTRIES=3/3 BOUND=4/4 (S113,S114,S115,S116) REF_ID_UNBOUND=0
  NEW_GROUND=3/3 QUOTE_ROWS=38 ON_BOUND=38/38 CAPTURE_BOUND=38/38
  QUOTES_IN_SPAN|ENTRY=38/38 QUOTE_SHORT=38/38 SPAN_CONTEXT=38/38
  SUBSTANCE=PASS ANCHOR_BOUND=4/4 INFERENCE_GROUNDED=3/3
  QUARANTINE_VERDICTS=0/1 (S120) QUOTES_IN_LESSON=0/38 → C2=FAIL exit 1
```

The two failing legs are the round-52 lesson content (quotes in lesson, S120
verdict line) — wave deliverables still owed, not counter defects.

## F8 LOW (hygiene) — counter bytecode side effect

`c2-count._builder()` (`exec_module`) writes `__pycache__/build-spans.cpython-*.pyc`
beside the source in `corpus/evidence/round52/` (observed: all three scripts' pyc
present). Untracked and gitignored (`git check-ignore` passes), so the tree stays
clean, but a "read-only" counter does create files in the lane; `sys.dont_write_bytecode`
in the counter would remove the side effect. [INFERENCE on the fix, mine]

## Residual risks (pre-existing, unchanged r51→r52)

- The used-by / `source:` citing set comes from the frozen `DOCS` list; an entry
  outside it citing a theme document escapes the `used == citing` check.
- The register sweep lane filter (backticked `chousa` in cell 2, round token in
  cell 3) could skip an unusually formatted theme-URL row.
- `verdict-gap.py` sits in round52 evidence unmentioned by claims.md — outside this
  seat's diff assignment, left to its owner. c1-count/c1-supplement not audited here.
- Live numbers are a snapshot; siblings are still drafting the lesson/entries.

VERDICT: attacked the r52 span builder and C2 counter against the r51 originals —
contract preserved (columns, file digests, form order, CR-clip sound for docx forms,
UTF-16LE fallback correct), no r51 leg silently weaker, predicate matches claims.md
except one editorial parenthetical (F1) and one bytecode-hygiene nit (F8); machinery
verified live (38/38 spans, 4/4 bound); no actionable defect in the diff.

# R53ReviewC2Counter — round-53 C2 counter + builder reviewed against round-52

Scope: `diff` r52→r53 of `corpus/evidence/round53/c2-count.py` and `build-spans.py`; the four
assigned questions. Everything read-only against the lane; fixtures under
`/fast/scratch/hyaku/chousa-r53/R53ReviewC2Counter/` (removed on exit). No tools installed.
`build-spans.py`: the diff is paths only (docstring, quotes path, usage line, `ev = …/round53`) —
no logic change; all findings below are about `c2-count.py` unless named.

## F1 MEDIUM — the "min 2 entries" flexibility is unreachable once all five rows are landed

`c2-count.py:180` `if len(hits) == 1 and citing:` (r52 had no `and citing`) skips the whole branch
when the only entries citing the document are absent; the REFUSED branch (`elif not hits:`,
`:188`) then never runs, so a row-backed document is neither BOUND nor REFUSED and the leg
`nbound + refused == len(by_doc)` (`:286`) cannot hold. The frozen predicate has no verdict for
that state either: BOUND needs `used-by` naming "exactly the existing entries citing it (at least
one)", REFUSED needs "no lane row". With the frozen DOCS map, E_STR is sole citer of JMLA, E_WIA
sole citer of COCHRANE, E_QCG sole citer of NOTICE and NMPA — so refusing any one entry strands
its exclusive document(s) as soon as their rows are landed, and any ENTRIES=2 configuration fails
the sum leg. A 2-entry pass additionally requires the refused entry's exclusive document to be
refused too (row absent + `refused-doc` line + no `source:` line). If the L1 lands the five rows
and refuses one entry, C2 always FAILs despite the claims' Target line `ENTRIES>=2`.

Repro (fixture lane root driven by the real counter via `--root`; `python3 <scratch>/limbo_repro.py`):

    == (a) COCHRANE row present, E_WIA refused-entry, refused-doc lines for all 5 URLs
    ENTRIES=2/3 (min 2) REFUSED_ENTRIES=1
    BOUND=0/5 (min 3) REFUSED=4        | exit 1
    == (b) same fixture, COCHRANE row absent
    ENTRIES=2/3 (min 2) REFUSED_ENTRIES=1
    BOUND=0/5 (min 3) REFUSED=5        | exit 1

All five documents satisfy the REFUSED conditions in (a); one is silently unclassified
(REFUSED=4, not 5). Predicate frozen — reported, not patched.

## F2 LOW-MEDIUM — registry() `split('|')` silently drops any row containing `\|` (fail-closed)

`c2-count.py:124` `rows.append([c.strip() for c in s.strip().split("|")[1:-1]])` splits on every
pipe: an escaped `\|` (or a raw `|`) in any cell widens the row to 12 cells, and the
`len(r) == 11` gates (`:179` binding hits, `:236` anchor loop) drop the row — the document is then
treated as row-less (REFUSED path, or F1 limbo if it also has zero citers). No cell-shift
false-bind is possible: the S id is the FIRST cell, and `base_ids` collects `r[0]` regardless of
width, so a `\|` at BASE_REV cannot bypass the new-since-BASE_REV gate — I hypothesized that
bypass and refuted it (`python3 <scratch>/reg_repro.py`):

    clean row cells: [11] ids: ['S100']
    row with \| in title cells: [12] ids: ['S100']
    base_ids: ['S100']

Latent today: no escaped pipe exists in `corpus/SOURCES.md` (regex search: no matches). Lane
precedent: registry row S043 records the round-27 falsifier class "escaped-pipe width
over-rejection" — the frozen counter's own parser re-introduces that family. Report-only (frozen).

## F3 LOW — refused-entry detector accepts prose (fail-open)

`c2-count.py:200-201`: `any("refused-entry" in l and p in l for l in lesson.splitlines())` matches
any line containing both strings, not a `refused-entry <path>` line. Repro (part (c) of
limbo_repro.py): the line "we considered, then rejected, writing a refused-entry line for
corpus/knowledge/western-instrument-alignment-r50.md …" → `counts as refused-entry: True`.
New vs r52 (r52 required all three entries and had no refusal concept).

## Q4 — predicate text: IDENTICAL, sentence for sentence

`pred_diff.py` extracts the R53-C2 paragraph from `claims.md` and the docstring sentence,
whitespace-normalized: claims 2239 chars, docstring 2914, a single opcode — `insert` at the tail,
where the docstring continues past the sentence with its own usage note (" `--lane-only` reads
lane bytes only: …"). No differing character inside the sentence.

## Q5 — form_text picks the .txt for PDFs; a UTF-16LE raw copy never wins a unique-.txt quote

`build-spans.py:116` `form_texts` lists `.txt` then the raw form; `:170` filters forms containing
the quote exactly once and `:175` takes `pick[0]` — the `.txt` wins whenever it is unique there.
Repro (`python3 <scratch>/forms_repro.py`):

    real QCG PDF (pdftotext sidecar per S077): .txt 61,909 B / .raw 415,245 B
      quotes bind to digest 927ff71c6d49.. == sha256(.txt); .raw digest is 7b600fe3ee9b..
    synthetic quote unique in BOTH .txt and the UTF-16LE decode of .raw
      manifest digest 758eb8a42a81.. == .txt digest → the .txt wins
    .txt absent → raw form used, digest = sha256(.raw) bytes, offsets in the decoded form
    c2-count.form_text(txt-digest) == .txt form: True
    c2-count.form_text(raw-digest) == raw_form: True

`c2-count.py:138-146` `form_text` is digest-keyed in the same .txt-first order, so CAPTURE_BOUND
re-derivation agrees with the builder in both branches. No defect.

## Legs silently weaker? None relative to the frozen predicate

- ENTRIES 3/3 → min 2 + refused-entry naming: the predicate itself says "at least two exist …
  named by a `refused-entry <path>` line"; the counter adds `len(texts) + len(refused_entries) ==
  3` (`:285`). Not weaker than the claim — but see F1: the 2-entry path is nearly unreachable.
- refused-doc now scans `source:` lines in ALL existing entries (`:189`, r52: citing entries
  only) — strengthening, predicate-conform ("in any existing entry").
- NEW_GROUND / INFERENCE_GROUNDED denominators over existing entries (`len(texts)`) — the
  predicate says "each existing entry" / "every existing entry". Aligned, not weaker.
- Verified preconditions: `git grep -l -e "tracking record" -e "information specialist" -e
  "质量控制指南" 5b550133… -- corpus/knowledge` → exit 1 (no BASE_REV knowledge file holds any
  term), so the NEW_GROUND gate's precondition holds; Registry header is exactly the 11 columns
  the cell indices assume (`id|source|kind|tier|scope|anchor|teaches|status|opened|recheck|used-by`
  — r[1] first source cell, r[5] anchor, r[7] status, r[8] opened, r[10] used-by); heading is
  `## Registry` with a space. Current lane state prints the expected before-shape: `ENTRIES=0/3
  (min 2) … C2=FAIL` exit 1.

## Residual risk / verification gaps

- The full C2 pass path is untested (entries/spans/lesson not landed yet — wave 1 build in
  flight); the QUARANTINE leg untested with real register rows (reg_ids empty at freeze, sweep
  prints 0); `tools/inference-ground.py` integration unexercised (no entries).
- F1 means the L1 must either land all three entries or, when refusing one, also refuse its
  exclusive document's row — worth flagging to the builders before integration.
- Scratch (fixtures + repro scripts) removed after this report; every receipt cited above is
  pasted output, no file references.

VERDICT: attacked the r53 C2 counter/builder diff — predicate text identical, form_text/.txt and
UTF-16LE behavior clean, no leg weaker than the frozen claim; found the min-2 ENTRIES path
effectively unreachable with all five rows landed (F1), silent `\|` row-drop in registry() (F2),
and a prose-loose refused-entry matcher (F3).

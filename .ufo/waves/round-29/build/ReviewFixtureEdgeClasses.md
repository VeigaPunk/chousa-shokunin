# ReviewFixtureEdgeClasses — edge-class fixture ground truth, wave 1

Axes: (a) label fidelity under the frozen contract, (b) page-grounded evidence,
(c) reproducibility (re-runnable command, wall time, byte pins).

Scope: the 10 fixture items in classes absent-truncated-token (4),
too-long-true-text (3), no-source-unregistered-id (1), no-source-own-work-row (2)
— `labels.tsv` joined to `items.tsv`; class counts match the claims.md table.

## Method

- `check_edge_classes.py` (copy + raw log in `build/ReviewFixtureEdgeClasses/`):
  imports the frozen `corpus/evidence/round29/c1-count.py` as a module and uses
  its `norm`, `found`, `registry_url`, `_Text` — the byte-exact reference
  pipeline, zero re-implementation drift.
- Fetch bounds mirrored from the contract: GET only, fragment removed, 30 s
  timeout, one retry (never needed), UA `chousa-quote-reopen-counter/r29`.
- Opened the five registry source URLs my classes touch: S008, S013, S019,
  S020, S044 — all 200 text/html, 4,877 to 464,179 bytes, 0.0 to 0.8 s each.

## Verdicts — 10 of 10 LABEL-OK

### absent-truncated-token — the cut string occurs exactly once in the
normalized page text and never at a valid boundary; the cut word continues with
an alphanumeric character, so the boundary rule must reject it:

| item | src | cut | occurrences | boundary-valid | cut-side neighbour |
|---|---|---|---:|---:|---|
| ad795e73 | S044 | end `…iterable pat` | 1 | 0 | `h` (paths.) |
| 98406fc4 | S013 | end `…must NOT be incl` | 1 | 0 | `u` (included.) |
| 4798287c | S008 | end `…seeks to ans` | 1 | 0 | `w` (answer.) |
| f98e78ae | S020 | start `he OWL …` | 1 | 0 | `T` before (The OWL) |

Each parent full quote (items db86a0d4, 27c5599c, f81a9ce8, 2cbd5af5) is
boundary-valid VERBATIM on the same page — the fixture truncated a true quote.

### too-long-true-text — `norm(quote).split()` count after frozen normalization:

- 5ba0e035 (S008): 34 words, true-on-page boundary-valid → TOO_LONG ✓
- a66931e8 (S013): 34 words, true-on-page boundary-valid → TOO_LONG ✓
- e2e2d1ce (S019): 35 words, true-on-page boundary-valid → TOO_LONG ✓

(TOO_LONG precedes UNREACHABLE/match in the frozen verdict order, so the label
holds regardless of presence; the "true text" premise also checks out.)

### no-source — against `corpus/SOURCES.md`:

- d3909bba: `S999` has no registry row; `registry_url("S999")` → None.
- 76b6a43c: `S001` row present, kind own-work, source cell
  `chousa research gate — tools/research-gate.sh (verify-all --json manifest
  append)` — no http(s) URL → NO_SOURCE.
- aff4afec: `S045` row present, kind own-work, source cell `Round27 canonical
  ancestor refusal diagnosis — .ufo/waves/round-27/residual/ResNoHarm.md` — no
  http(s) URL → NO_SOURCE.
- Positive control: `registry_url("S044")` → `https://docs.python.org/3/library/os.path.html`
  (lookup is not vacuously None).

## Located quotes (copied from the opened pages, access date 2026-10-23)

- https://docs.python.org/3/library/os.path.html — "Return the longest common
  sub-path of each pathname in the iterable paths."
- https://jsonlines.org/ — "Like the JSON standard a byte order mark (U+FEFF)
  must NOT be included."
- https://www.cochrane.org/authors/handbooks-and-manuals/handbook/current/chapter-02
  — "This is best done by clearly framing the questions the review seeks to answer."
- https://www.w3.org/TR/2013/REC-prov-o-20130430/ — "The OWL encoding of the
  PROV Ontology is available here."

## Re-run and pins

Command: `python3 check_edge_classes.py` → `EXIT=0`, wall 1.8 s; saved re-run
`run-2026-10-23.log` → `EXIT=0`, wall 2.03 s.
SHA-256: c1-count.py `cd509650…`, items.tsv `e6305beb…`, labels.tsv
`dda1b376…`, SOURCES.md `8bc10382…` (full hashes in the log).

## Provenance note

Lane HEAD at review time is `aa5e1a31` (design v3 freeze). Read-only diff
v2→v3: `c1-count.py` loses only the `--seed` option plus docstring lines; the
reference pipeline, items.tsv, labels.tsv, and SOURCES.md are byte-identical.
claims.md gains a v3 preamble; the tool contract and fixture table are
unchanged. Verdicts therefore describe the frozen v3 ground truth.

## Limits

- Boundary analysis runs on the normalized reference representation — the
  layer the contract's match rule names; raw-HTML substring evidence is not
  claimed.
- Each page fetched once; fixture authored and reviewed on the same day, so
  page drift between fixture freeze and this check is unmeasured but near-nil
  in-window.

# R54W2CritS101Cut — attack on the L1's S101 cut (claims-erratum E3)

Scope: was the L1 right to cut the W1 r37 draft's S101 leg (four carrier-alphabet quotes from the HIT
`.doc`, anchored "in the raw UTF-16LE text form")? Weighing the frozen span builder's `.raw`→UTF-16LE
rule, QUALITY 97, and whether the quotes could have been located in the defined OLE form and carried
by the frozen builder anyway. Leaf seat; no subagents; no installs. Lane tip measured: `25abbe82`.

## Attack method — counterfactual rig, not reading alone

Built a fake lane root under scratch (copies of `SOURCES.md`, the landed r37 entry, `round-54.md`,
`spans/`; symlinked `tools/` and `evidence/round51/`). Restored the W1 leg **exactly as drafted**:
extracted the fenced entry verbatim from `.ufo/waves/round-54/w1/R54DraftEntryStb.md:98-186`, added
its four QUOTE lines to `quotes.tsv`, regenerated `spans.tsv`/`spans/` with the frozen
`build-spans.py`, updated S101's `used-by` in the copied `SOURCES.md`, and appended the four quotes
to the copied lesson so `QUOTES_IN_LESSON` could not mask the leg under test.

## Evidence

1. **The frozen builder CAN slice the S101 quotes — but only from the undefined form.** Probe:
   `.qcache/6dc68fd6b32ce9c8dfcebce8.txt` (128,416 chars, 14,486 U+FFFD — the campaign's junk
   replace-decode of the OLE bytes) holds each quote **0 times**; the `.raw` UTF-16LE decode
   (64,512 chars, 263 U+FFFD) holds each **exactly once** (12303, 12392, 12682, 34265).
   `build-spans.py:170` picks the first form with `count==1`, and `form_texts` (`:116-127`) offers
   only `.txt` then `.raw`-via-`raw_form` (`:107-113`: `docx_text` for `PK` magic else UTF-16LE).
   The builder has no defined-form input at all. Counterfactual run produced real rows —
   `QUOTE S101 char 12303 spans/S101-1.txt` … `SPANS_ROWS=37 WRITTEN=37` — i.e. `spans.tsv` would
   have held four `S101` rows, `.raw` sha `6063a3af…`, offsets 12303/12312/12602/34265.

2. **The defined form exists and holds all four quotes** — `python3 tools/capture-text.py …raw`
   → exit 0, 27,012 chars, 0 U+FFFD; offsets 13105, 13194, 13484, 25014 (each count 1). So
   "locate them in the defined form" is possible; the question is whether the frozen rule can
   *carry* that. It cannot, twice over.

3. **Blocker A (the binding one): `ON_BOUND == n`.** `c2-count.py:291-295` requires `on_bound == n`
   over *every* manifest row, and `on_bound += bound.get(sid) == url` (`:221`). `bound` is built
   only for DOCS urls whose single row is `r[0] not in base_ids` (`:170-177`) — a *new* row. S101's
   row predates `BASE_REV` (round 49), so S101 is structurally unbindable and every S101 row burns.
   Counterfactual, all else green: `BOUND=3/3 HELD_CITED=S101 QUOTES_IN_SPAN=37/37
   CAPTURE_BOUND=37/37 SUBSTANCE=PASS … ON_BOUND=33/37 → C2=FAIL exit 1`.

4. **Blocker B: defined-form anchors are uncountable too.** `form_text` (`c2-count.py:123-132`)
   resolves the recorded digest to a **file** — `.txt` bytes or `.raw` bytes — never tool stdout;
   for the `.raw` digest the "capture text form" IS the UTF-16LE decode. Rewriting the four rows to
   defined-form span-start offsets (13025/13114/13404/24934): `CAPTURE_BOUND=33/37 → C2=FAIL`.
   So UTF-16LE offsets are the only ones the rule can verify — and they index the form QUALITY 97
   (`corpus/QUALITY.md:937`, landed this round) names undefined: new anchors there would re-mint
   exactly the Mistakes-row-2 defect the round just corrected with nine `correction:` lines.

5. **Blocker C: no-span citing fails grounding.** Deleting the four rows+files while keeping the
   entry's verbatim quotes: `HELD_CITED=S101 ON_BOUND=33/33 INFERENCE_GROUNDED=1/2 → C2=FAIL`.
   The only residue — cite `source: S101` with no quotes — drops the carrier-alphabet collision,
   which W1 called the entry's sharpest finding (`R54DraftEntryStb.md:33`).

6. **Contrast:** real tip, `python3 corpus/evidence/round54/c2-count.py` → `C2=PASS` exit 0.
   W1 never saw blocker A: its own report (`:85-86`) says c2-count was not run.

## Judgment

**Cut right — for a deeper reason than stated.** The L1's stated reason (anchors in the undefined
UTF-16LE form; builder has no OLE form) is a true blocker, but it is the *weakest* of three walls.
Even granting a defined-form-reading builder — the exact flip the Gate names (`round-54.md:45`) —
the frozen counter still fails `ON_BOUND`, because held-document quote rows are uncountable by
construction: binding requires a new row, S101's is old. The stated reason would have the leg die
at QUALITY 97; it actually dies earlier, at `on_bound == n`. The Gate's flip is also under-specified:
"the four quotes re-located in that form" cannot work until the counting rule is widened
(`on_bound` to count `held_ok` ids, and a digest-resolution rule for a derived form — e.g. a stored
`.ole.txt` or tool-stdout digest) in some future round's freeze. Neither half was changeable this
round: claims.md's admission rule forbids post-score rule changes, and W1 had already scored.

Smallest safe correction: none for round 54 — the cut was forced; record the flip as
*counter + builder*, not builder alone, in the next round's plan.

VERDICT: attacked the E3 S101 cut — survives: **cut right**, but the deepest blocker is
`ON_BOUND=n/n` (held rows uncountable), not only the undefined form the L1 named.

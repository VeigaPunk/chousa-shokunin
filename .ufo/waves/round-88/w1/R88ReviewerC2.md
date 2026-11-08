# R88ReviewerC2 — C2 attacks (round-88, calibration)

Revisions: base `f484d94f`; freeze/landing `4ea9d008abfd2e09cb51649a42678a78f52ac530`. All checks read
committed bytes only; tree built at `4ea9d008…` via `git archive`. Counter re-run:
`python3 -B corpus/evidence/round88/curation-r88.py --root <tree>` → exit 0, `SUPERSEDED_LIVE=0
UNENTAILED_TERM=0 MODIFIED_DEF_CITED=1 QUOTES_LOCATED=20/20 WARRANT_OK=17/17 TEACHES_CHECKED=1
TEACHES_FLAGGED=1 TEACHES_UNRESOLVED=0 LEGS=7/7`, `TEACHES_FLAGGED S024 … disposition=superseded by S031`,
`CURATION_R88=PASS`. Receipt: `receipts/curation-rerun.txt`.

## (a) "every named qid shares a distinctive content word" — OVERPROMISE (finding)

Re-derived all 17/17 matches independently (counter's `distinctive()`: `[a-z]{5,}` minus the 44-word
stopword set, compared against `[a-z]{5,}` tokens of each quote). Every row passes, but two rows rest on
exactly one shared word:

- `search-transparency-reporting` / "Linking a claim to its source" → Q7 shares only `{'evidence'}`.
  `evidence` is not stopworded (not in the 44-word list above) and is arguably the row's generic subject,
  not a distinctive content word `S018`-specific warrant. The quote's other content (`approaches that use
  citations, attribution, or quotations`) is in the row Do cell (`cite, attribute, or quote`) but the
  counter's check reduces this to the single token `evidence`.
- `search-transparency-reporting` / "Recording when a resource changed" → Q13 shares only `{'changed'}`.
  Q13 is the 7-token minimum quote ("Date on which the resource was changed."). The claim sentence says
  "shares a distinctive content word" — `changed` is the definitional verb; calling it "distinctive"
  is a stretch but not false.

More importantly, the predicate is weak in construct: a shared single incidental word (e.g. `provenance`)
suffices. I demonstrated a full-counter bypass: replace the "Naming what a resource derives from" row's
Do/Never with gibberish sharing only `provenance` (the one word also in the located Q1 quote) → counter
still prints `WARRANT_OK=17/17`, `LEGS=7/7`, `PASS`. Receipt: `receipts/a9-incidental-share.txt`.
The reasoning error is that the claim's sentence ("a padding qid fails") is true only because padding qids
are *unlocated*. A padding qid that happens to share one incidental word with the row (and is located,
e.g. re-worded from the same capture) would pass — the leg measures `any ∩ distinctive`, not substantive
linkage. This is residual/incidental-word weakness; the claim sentence promises more ("distinctive") than
the counter enforces. Does not break K1–K4 as worded (none bans an incidental single word), but it is a
finding against the stated wording.

Q3 check (a7): pre-repair "Naming…" row (base `f484d94f`, warrant `Q1, Q3 (S215)`): Q3's quote
`then we can say that the bar chart prov:wasDerivedFrom the dataset.` shares **zero** terms with the row
under the counter's own rule — consistent with the claims.md repair note. Q1 shares
`entities, property, provenance`. The repair removed a non-sharing warrant correctly.

## (b) Provenance repair (Q1, Q3 → Q1) — row still states Q1; narrowing invisible to counter (finding, informational)

Diff confirms exactly the one-cell change above (S215 = PROV-O). Post-repair row:
Do = "form the provenance chain with the derivation property where the chain's entities are set",
Never = "record a resource with no derivation link when the chain's entities are known", Warrant = `Q1 (S215)`.
Q1 = "Provenance chains comprising only Entities can be formed using the prov:wasDerivedFrom property." The
row still states what Q1 states (derivation property, chain of Entities). Q3 was an *example* (`the bar chart
prov:wasDerivedFrom the dataset`) showing the property in use; dropping it loses an illustrative instance, not
a term. The entry's `## Limits` says "PROV-O is a description of provenance relations, not a rule for when to
re-verify a source. The rows take only the derivation and generation/invalidation terms." — no sentence in
`## Limits` or `## Inference` depends on Q3's example. The removed warrant carried no teaching the row stated.

But: the counter cannot see dropped warrants by construction. `WARRANT_OK=17/17` counts rows, not per-qid
linkage breadth; FLOOR counts `located/total` per entry (Q3 still in the Located quotes table, still located,
so 7/7 stands). Taking a real qid off a row's warrant while keeping the quote row would keep `WARRANT_OK` at
`warrant_total` and `QUOTES_LOCATED` unchanged. The counter is blind to this narrowing *class*. Here the
removal is legitimate (Q3 never shared), but the counter has no leg that would catch an illegitimate one.
Worth stating as a residual counter-blindness finding; not a kill (no kill rule covers it, and the repair is
correct on the merits).

## (c) "a superseder disposes only when `mined`" — HOLDS under stress (no queued-only flagged row)

Tree census: 218 registry rows; 10 superseded targets. Only one row matches the TEACHES detector
(contrast + date term): S024 (`separate from publication or modification dates`), whose sole superseder is
S031 (`mined`). There is no flagged row whose only superseder is `queued`: the only `queued` superseders
(S032 → S021, S030 → S022) target rows whose `teaches` has no contrast/date match, so they never enter the
flagged set. The `queued` class therefore never exercises the disposal rule on this tree. However the
counter's rule is live in code: `mined_superseded_by` gates the disposal, and the F2 control flips S031 to
`rejected` to prove it. My own queued-stress: flip S031's status `mined→queued` in a tree copy → counter
prints `TEACHES_UNRESOLVED=1`, `LEG_FAIL TEACHES`, `CURATION_R88=FAIL`, exit 1. Receipt:
`receipts/c2-queued-superseder.txt`. So the sentence is genuinely enforced; the tree just has zero current
queued-only members to fail on. (S202 `rejected` → S198 exists but S198 has no contrast/date `teaches`,
so it too is inert.) F2-class behavior verified twice.

## Summary of findings

1. **Wording > enforcement (incidental-word weakness, §a):** "distinctive content word" is enforced as `≥1`
   `[a-z]{5,}` overlap minus a small stopword set. Single-generic-word matches (Q7 `evidence`, Q13
   `changed`) pass; a gibberish row sharing one incidental word (`provenance`) also passes with `PASS`.
   Counter-bypass receipt `receipts/a9-incidental-share.txt`. The claim sentence arguably promises more
   than the predicate delivers. Against the stated kill rules K1–K4: no kill — K1/K3/K4 are met, and K2
   (verbatim location) is untouched. The counter's Q3 repair shows the author knows the difference.
2. **Counter blindness to warrant removal (§b):** dropping a qid from a row's warrant cell changes neither
   `WARRANT_OK` (row-counted), `QUOTES_LOCATED` (quote-table counted), nor QID_SETS (quote-table pinned).
   No leg would register a narrowing that deleted teaching. The specific repair is sound and Q3 carried
   nothing the row stated, but the class is invisible to the instrument.
3. **Queued-superseder rule is exercised but has no live queued member (§c):** code path verified by
   mutation (`receipts/c2-queued-superseder.txt`); tree currently contains no flagged row with a queued-only
   superseder, so no on-tree false disposal is possible. Not a defect — a coverage note.

Tooling: no installs (stock python3 + git), nothing recorded as installed.

VERDICT: R88ReviewerC2 C2 held — counter meets K1–K4 on the landing tree and the queued-superseder rule is genuinely enforced; the warrant wording overpromises (single incidental word passes, demonstrated) and the counter is blind to warrant-cell removals, but neither fires a stated kill rule on this round's bytes.

# Round-10 lesson — a defect class is proven at the scale you certify: single-defect archive mutants, the counted-but-unverified audit, and one ledger for the carried limits (2026-10-16 UTC)

Round: chousa-shokunin round 10, one hardening/calibration move — archive-scale
negative controls (one broken archive record per defect class), the exempt-item
audit, and the r2–r9 limit-disposition ledger. All three artifacts landed inside
this seat's polling window: controls + controls README, the exempt audit (run
here), and `corpus/knowledge/hardening-r10.md` (sha256
`f5dc8889534a8527d5fd010c1f9e2493d4214f358566d0f1fea0e91ae1f3a2f0`, landed
2026-10-16T05:45:38Z). Fixture-led by design: no gate change (working-tree gate
sha256 equals the HEAD blob; `git diff --numstat tools/research-gate.sh` EMPTY,
re-derived at measurement time).

Source seat: lessons-distiller. Gate under measurement: `tools/research-gate.sh`
sha256 `46f5ddb39d5fafa220fb584121dba2f4a15e071a91fa42728849f3c7567c6ccd`
(selftest 85, the r8 revision; lane HEAD `d5c99c2` blob). Read-only archives
re-pinned: A `9033857d…`, B `6d8dbddd…`, C `e48fe70f…`. Archive records
re-pinned: A-r9.md `338918fc…`, B-r9.md `abfa5290…`, C-r9.md `97be0e69…`.
Controls re-pinned (sha256, all re-derived): `A-r9-span-not-found.md`
`5dedb73b…` + `.claims.jsonl` `0edb78ee…`; `A-r9-anchor-missing.md`
`e3490cf4…`; `B-r9-false-sweep.md` `69b7b08f…`;
`B-r9-rejection-missing-flip.md` `b0d488aa…`; `C-r9-dangling-ref.md`
`b24be0f0…`; `C-r9-structure-break.md` `21d77e6c…`; controls README
`23f47722…`. verified-at: 2026-10-16 05:37–05:46Z, from the lane cwd,
fresh-process CLI runs; working scratch (this note's draft, no run artifacts)
under `$HOME/.cache/chousa-tmp/r10-lessons/`, removed after the final write.
The controls README (landed after this seat's first runs) reproduces these
outcomes; this note's runs are its own.
recheck (from the lane cwd):
`bash tools/research-gate.sh verify-all corpus/fixtures/archives-r9/controls/<control>.md --root ..`
(no `--json`: it would write manifest lines into the receipts-writer's surface).

## The lesson

A verification review already certified *what the gate does on good inputs*
(rounds 2–9). Round 10 certifies the other half — *what the gate catches when
the artifact itself is wrong* — and the shape of that work is the lesson:
prove each defect class on the artifact class you actually certify, at its
scale; audit the items the checker counts but never checks; and terminate the
limits instead of carrying them. Six measurements:

1. **The controls enter the production shape.** Before this round every broken
   fixture in the lane was small-fixture scale (`chain-r3-broken.md` 1611 B /
   22 table rows, `sweeps-r5-broken.md` 1490 B, `full-r6-broken.md` 3793 B /
   37 rows, `integrity-r7-broken.md` 4464 B / 39 rows), and none was a
   variant of an archive record. The six new controls are single-defect
   mutants of the production records (`A/B/C-r9.md`; 44/45/48 table rows,
   built byte-verbatim from the read-only archives). Each composes `DRIFT`,
   exit 1, `drift-sections=1 findings=1`, with exactly one finding naming
   exactly its class, and the other four sections CLEAN (my fresh runs,
   verbatim lines trimmed):

   | control | class → finding | class tally | composed |
   |---|---|---|---|
   | `A-r9-span-not-found` | `CLAIM_SPAN_NOT_FOUND … id=A07` | `VERDICT_BEARING_CLAIMS=9/10` | `VERIFY_ALL sections=5 run=5 absent=0 drift-sections=1 findings=1 drift=1` |
   | `A-r9-anchor-missing` | `CHAIN_ANCHOR_NOT_FOUND … hop=2` | `RESOLVED_HOPS=5/7` | same composed line |
   | `B-r9-false-sweep` | `SWEEP_CLAIM_FALSE … id=SW1 hits=3 first=…/A-shokunin-tradition.md` | `VERIFIED_SWEEPS=0/1 REJECTIONS_OK=3/3` | same |
   | `B-r9-rejection-missing-flip` | `SWEEP_REJECTION_INCOMPLETE … id=R2 missing=flip` | `VERIFIED_SWEEPS=1/1 REJECTIONS_OK=2/3` | same |
   | `C-r9-dangling-ref` | `REF_UNRESOLVED … kind=claim id=C9 section=chain row=1 cell=from` | `INTEGRITY refs=15 resolved=13 unresolved=1` | same |
   | `C-r9-structure-break` | `NO_QUESTION severity=crit` | structure `verdict=DRIFT findings=1` | same |

   Together the six exercise all five composed sections (structure; claims;
   chain; sweeps, twice; integrity). A defect class demonstrated only on a toy
   fixture is not yet demonstrated where certification happens.

2. **"Names exactly its class" is two-sided, and the second side is the
   evidence.** Each run must fire in the class's section *and* stay silent in
   every other section: measured, all six runs had exactly one dirty section,
   so the drift is attributable to the injected defect and nothing else. The
   composed verdict line (`drift-sections=1 findings=1`) is the assertion; a
   control that also dirty-trips other sections would measure the record, not
   the class.

3. **The mutants preserve token shape and carry their provenance.** The
   mutations are minimal and shape-preserving: `keep four axes separate` →
   `keep five axes separate` (same length and boundaries); `not a universal
   rank ladder` → `not a universal certification ladder` (same token count);
   `C1` → `C9` (declared → undeclared, same id shape); one `flip_condition`
   cell emptied; `saved-*,*-snapshot-*` → `research/deep-research-2026-09-28/*.md`
   (a glob the directory really satisfies: 3 hits); the `## Question` section
   removed. Each control's diff against its base is exactly the defect cell(s)
   plus the `## Meta` `note` row (the `integrity-r7-broken.md` idiom; the
   `span-not-found` control additionally rebinds `claims_file` to its one-span
   claims copy, because a claim span is only expressible on the claims
   surface). The bases re-verified CLEAN in the same window (A/B/C
   `sections=5 run=5 absent=0 drift-sections=0 findings=0`, exit 0 each;
   claims 10/10; chain 6/7, 6/7, 7/8; sweeps 1/1 with rejections 4/4, 3/3,
   4/4; integrity 13/12/0, 14/13/0, 15/14/0). The README adds the generation
   asserts: every replacement occurs exactly once, and the new span/anchor
   text was asserted absent from the archive bytes. A mutant without its base,
   its delta, and a same-window CLEAN re-derivation is just another fixture.

4. **The exempt set is the counted-but-never-verified surface, and it can be
   audited against source bytes — instance by instance.** The records carry
   exactly 6 exempt items: three `blocked-no-fetch` chip hops (A hop7
   `コトバンク`, B hop7 `arxiv.org`, C hop8 `jstage.jst.go.jp`) and the three
   integrity tokens on those rows (A `C1`, B `C3`, C `C8`). Audit (this
   seat's independent re-derivation): each chip is byte-present in its
   archive (A:68, recurring at A:72; B:51 and B:72, as its note names both;
   C:103 — bare chips alone on their lines, not URLs, not local paths); the
   archives carry zero `http` strings (0/0/0) and no `saved-*` /
   `*-snapshot-*` / chip-named local file exists, so no local resolution is
   possible and `blocked-no-fetch` is the truthful status; the three exempt
   integrity tokens are DECLARED claim ids, so nothing dangling hides behind
   the blanket exemption. Six of six justified; zero findings. What stays
   named: the mode cannot check that a *different* exemption is truthful —
   the audit covers exactly these instances, not the class.

5. **A named limit is not a dispositioned limit — and this round terminates
   them.** Rounds 2–9 named limits and carried residuals in nine notes plus
   SCORECARD debt paragraphs — semantic support, location binding, source
   truth, external verification, in-root hardlink bypass, no source size cap,
   banner string, token-aligned shortening, non-ASCII fail-closed edges,
   `_`-adjacent gluing, flip-condition vacuity, omission limit, extraction
   fail-opens (case, id shape, duplicates, unscanned cells), pin blind spots,
   exit-code-only regressions, plus the r9 carries (claims-table `span`
   column, `path#quote:text` quirk, `A-r9.md:50` pointer-line defect,
   reframing residual) — with no single disposition map. The third artifact,
   `corpus/knowledge/hardening-r10.md`, is that map: **68 rows — by-design 38 ·
   carried 22 · closed 3 · finding 1 · operator 4** — each with a terminal
   disposition and evidence, plus a **27-item round-11 audit queue** (22
   carried + 1 finding + 4 operator) in cheapest-first order. Spot-checks
   here: row 9 (glued truncation) `closed(r4)` matches r4's measured
   before→after; row 16 (exempt-hop truthfulness) `by-design` plus the r10
   audit of the six actual instances matches §4 above; row 29 (omission
   limit) `carried` matches r6 naming it and r7 not taking it; row 53
   (`A-r9.md:50`) is the ledger's single `finding`; the declared counts
   re-count by grep (68 rows; 38/22/3/1/4) and the queue arithmetic closes
   (22+1+4 = 27). The durable point: carried residuals now have one terminal
   state each instead of being re-narrated every round, and the next audit
   starts from the map, not the search.

6. **When the canonical finding cannot fire alone, choose the smallest edit
   that isolates one finding.** The controls README reports a measured probe:
   `RECORD_SCHEMA_INVALID` cannot fire alone (it drags three companion
   findings into the same run), so the structure-break control removes the
   `## Question` section and isolates `NO_QUESTION` (crit) instead. The
   control's job is attribution, not maximal breakage.

## Cross-checks (what held)

- My fresh runs reproduce the controls README's recorded outcomes exactly
  (same finding ids, same per-class tallies, same composed lines; the runs
  differ only in their `ts`). This seat also re-derived each control's diff
  against its clean base (single defect + note row; the `span-not-found`
  claims copy differs in exactly one span, `four`→`five`).
- Holds at the unchanged gate, all re-derived by this seat in the same window:
  `--selftest` → `RESEARCH_GATE_SELFTEST: PASS (85 cases)` exit 0;
  `--drift` vs the committed r8 baseline → `GATE_DRIFT: none` exit 0;
  `verify-all` on the three records → CLEAN exit 0 each (tallies in §3);
  claims-r2 `17/17` CLEAN exit 0; claims-r9 `10/10` CLEAN exit 0; chain-r3
  `RESOLVED_HOPS=17/22` CLEAN exit 0; the r1 observable
  `VERDICT_BEARING_EXPORTS=3/3`; working-tree gate sha ==
  `git show HEAD:tools/research-gate.sh` sha (`46f5ddb3…`),
  `git diff --numstat tools/research-gate.sh` EMPTY.
- The exemptions audit (§4) agrees with the wave's own exempt-item capture
  (solo `verify-chain` / `verify-integrity` lines, re-run here), including
  the declared-id check on the three exempt tokens; the ledger's §2 reports
  the same 6/6.
- The ledger landed mid-window; its pins were re-checked here: its controls
  README sha `23f47722…` matches, and its §3 counts re-derive by grep as
  declared (68 rows; 38 by-design / 22 carried / 3 closed / 1 finding /
  4 operator). Its controls table agrees with §1 line-for-line.
- The thin lead from r9 that is still live: `corpus/fixtures/archives-r9/A-r9.md:50`
  (row C3) cites `…A-shokunin-tradition.md:76` while its span occurs at A:86
  (re-derived: the span greps at A:86; record sha unchanged `338918fc…`).
  The ledger dispositions it as its single `finding`; it remains invisible to
  every gate mode and is the fixtures seat's fix-or-absorb.

## Applying it (durable rules)

1. Prove each defect class on the artifact class you certify: mutate a
   production record (one defect per control), and assert the composed
   verdict names exactly the class — DRIFT + `drift-sections=1` + exactly the
   class's finding id + every other section CLEAN. The silence of the other
   sections is part of the evidence.
2. Keep the mutation minimal and shape-preserving; ship the provenance trio:
   parent sha, control sha, the byte-delta, plus a CLEAN re-derivation of the
   parent in the same battery window. When the canonical finding cannot fire
   alone, pick the smallest edit that isolates one finding.
3. Enumerate the counted-but-never-verified items (exempt hops/refs/sweeps)
   and justify each against source bytes; check that blanket exemptions hide
   no defect (declared-id check on exempt reference tokens); keep the
   class-level limit named — an audit covers instances, not the class.
4. Give every limit a terminal disposition in ONE ledger — fixed /
   by-design / carried / finding / operator — so the next audit starts from a
   map instead of re-searching nine notes; carried residuals deserve one
   disposition, not a per-round restatement.
5. A hardening round should end by producing the starting map for the audit
   that follows it: here the six class signatures, the audited exemption set
   (6/6), and the disposition ledger with its 27-item queue — the shape
   round 11's capstone audit should consume rather than re-derive.

## Defects and follow-ups (outside this seat's write scope)

- The ledger's §5 records a premise correction worth carrying: the dispatch
  named a `limit-ledger` seat, but no artifact under that name was observed
  on disk (searches at 05:44Z: the `corpus/` tree and `.ufo/round-10/`); the
  only on-disk enumeration was the scribe's draft, and `hardening-r10.md` §3
  is the ledger, reconciled against it. If a separate ledger artifact lands
  at integration, reconcile it against `hardening-r10.md` §3 rather than
  assuming agreement (my spot-checks found its arithmetic and pins sound).
- `corpus/fixtures/archives-r9/A-r9.md:50` (row C3) pointer-line defect
  persists at record sha `338918fc…` (pointer cites A:76; the row's span
  occurs at A:86; no gate mode pairs the two, so every composed verdict stays
  CLEAN). Re-verified as unchanged this round; the ledger's single `finding`;
  belongs to the fixtures seat or a future round.
- The controls README landed after this seat's first runs; its table matches
  the runs (no discrepancy). Its own "what this set does not cover" is
  honest and carried into the ledger: multi-defect interaction in one record,
  out-of-corpus refusals at archive scale, semantic drift inside stable
  fields, and the fact that six existence proofs are not a measured fraction
  of defect space.
- Round-10 receipts, `SKILL.md`/`corpus/README.md` updates and the admission
  verdict are other seats'/parent's artifacts, not measured here.

## Limits of this note

- One host, one gate revision (`46f5ddb3…`, selftest 85), artifact shas as
  listed; all CLI runs were read-only lane/local opens; no network; no
  `--json` (the manifest surface belongs to the receipts-writer).
- Re-derived this round: the six control runs, the three parent CLEAN runs,
  the six control diffs and their one-defect deltas, the exempt-item
  enumeration and source-byte justifications, all holds in §Cross-checks, and
  the ledger's pins, row count, disposition counts and four sampled
  dispositions. Not re-derived: the ledger's item-by-item completeness (the
  scribe's reconciliation owns that; my checks were arithmetic, row count and
  a sample), the receipts (none landed at writing), the archive-record
  conversion itself (r9's battery owns it), and fault sensitivity below the
  class level (the controls prove each class fires on one mutant; they do not
  measure how small a defect is still caught).
- No scalar score, no verdict about the round's admission.
# ScoutFrontierOverlap — does the r40 expectation-digest note name distinct ground?

## Assigned attack

Read the README coverage map and Frontier plus the two r39 receipt knowledge
entries; determine whether `corpus/knowledge/receipt-expectation-digests-r40.md`
names genuinely distinct ground or duplicates an existing note. Read-only seat;
this report is the only file written.

## Exact commands and observed output

```sh
$ sha256sum corpus/evidence/round39/expectations.jsonl
01cbdc3a8208a257e2b0ea4304c87a6d74be313a722cf667c5d126a4c29c583a
$ python3 -c "json receipt['expect_sha256'] for each committed r39 c1 receipt"
c1-base-s39001.json    → 3abd2dcb1766c404228cf3929024856240a93ea374760ab77a390b92c3fb6480
c1-after-s39011.json   → 3abd2dcb1766c404228cf3929024856240a93ea374760ab77a390b92c3fb6480
c1-mutenv-s39003.json  → 3abd2dcb1766c404228cf3929024856240a93ea374760ab77a390b92c3fb6480
c1-mutenv-s39013.json  → 3abd2dcb1766c404228cf3929024856240a93ea374760ab77a390b92c3fb6480
$ python3 corpus/evidence/round40/c1-count.py
R39_ACTIVE_RECEIPTS=6/6   (exit 0; all six rows print `ok VERIFY: ok`)
```

## Observed facts (committed bytes only)

**The r40 note's claimed ground** (`corpus/knowledge/receipt-expectation-digests-r40.md:7-23`):
a receipt's `expect_sha256` binds the *exact expectations-file bytes* (whole
file, streamed through `sha256_file`), not only the scenario rows the receipt
cites — so a receipt can refuse `expect-sha256-mismatch` while every row it
names still ties. The note records a concrete event: at r39 closure
`expectations.jsonl` was `01cbdc3a…` while four c1 receipts carried `3abd2dcb…`;
three refused `expect-sha256-mismatch` and the superseded draft
`c1-mutenv-s39003.json` refused first on `counter-sha256-mismatch`; three
replacements were reissued under `corpus/evidence/round40/receipts/` and the
originals preserved un-labelled. Limit: digest match = byte identity, not
authorship or truth. Every number re-derived above and confirmed against
`.ufo/waves/round-40/controls/r1-stale-before.txt` (3× expect-sha256-mismatch,
1× counter-sha256-mismatch, verbatim).

**vs `receipt-verifier-subject-r39.md`** (the r39 C2 entry): same receipt-integrity
family, different field set and different verifier checks. That note covers
`verifier_sha256` and `subject_counter`/`subject_counter_sha256` — receipts
binding *which verifier and which subject counter bytes* judged a run
(verify-receipts.py's `verifier-sha256-mismatch`, `subject-counter-unreadable`/
`subject-counter-sha256-mismatch`, FAMILIES generation binding, the
verifier-weakening debt from r38 Erratum 11). It never treats the
*expectations file* digest, the stale-expectation event, or receipt repair.
Overlap is family and umbrella-limit only (both say "integrity, not
authorship"); the held content is disjoint.

**vs `capture-bash-pin-r39.md`** (the r39 C1 entry): different domain entirely —
one pinned absolute `bash` for the capture grandchild and verify-all section
children (`BASH_PROVENANCE` refusal, 7/8→8/8, PATH-`env`-mutant discrimination
4/8). Receipts appear there only as measurement containers; nothing about
expectation digests. Disjoint.

**vs `receipt-binding-r38.md`** (nearest real overlap candidate, though an r38
note): it names `expect_sha256` once — "the frozen table, hashed before the
run and re-checked after" — inside a five-field binding model
(`gate_sha256_pre/post`, `counter_sha256`, `expect_sha256`,
`receipt_sha256`). That is the field's *existence*. The r40 note is the
field's *observed failure class and repair*: row-level ties surviving while
file-level bytes drifted, the per-receipt first-refusal map (expect vs
counter), and the disposition (3 regenerated / 1 superseded-preserved /
originals not re-labelled). None of that appears in the r38 note.

**Coverage map** (`corpus/README.md`): the r40 note is indexed exactly once —
row `corpus/README.md:1059` in the r32–r40 `| Entry | What it holds |
Evidence |` annex table (`:1041-1059`), with a Holds clause distinct from the
r38 (:1056) and two r39 (:1057-1058) rows. No second row or stale duplicate
reference exists (grep: one coverage row + one Frontier citation only).

**Frontier**: the r40 statement is a bare paragraph at `corpus/README.md:1038`,
immediately after the Round 38 paragraph (`:1026-1037`), in the house style of
rounds 33–38 (no `## Round40` heading). It names "expectation-file digest
identity" as "one narrow frontier subground" — a claim no earlier Frontier
paragraph makes (r37: claim-pin/env-scrub pins; r38: env pin + receipt
binding; nothing else covers expectation digests).

**Source-row dedup already handled**: `corpus/SOURCES.md:69` S059 re-opened
(used-by now includes the r40 note); `:84` S074 is the rejected duplicate-row
proposal for the same page, with flip condition — consistent with
`corpus/evidence/round40/claims.md:45` (erratum) and
`corpus/lessons/round-40.md:42`. The note does not open a duplicate source row.

**Verifier mechanism confirmed**: `corpus/evidence/round39/verify-receipts.py:73-79`
(`sha256_file` streams whole file bytes) and `:138-139`
(`receipt["expect_sha256"] != sha256_file(args.expectations)` →
`expect-sha256-mismatch`) — exactly the lines the note's `source:` header cites.

## Verdict

**Distinct ground, not a duplicate.** The r40 note holds content no existing
note holds: (a) the semantic distinction that `expect_sha256` binds whole-file
bytes rather than cited rows — stated nowhere else; (b) a newly exercised
failure class — a receipt refusing while its scenario rows still tie — first
observed at r39 closure; (c) the repair disposition of the four stale c1
receipts. Both r39 entries are disjoint on subject; the r38 binding note names
the field but covers none of (a)-(c). The README indexes it once with a
non-duplicate Holds clause, and the Frontier paragraph advances subground not
claimed by any prior paragraph.

## Adjacent gaps found (flagged, not in scope to fix)

- **No Round 39 Frontier paragraph exists.** `corpus/README.md` goes Round 38
  (`:1026-1037`) → Round 40 (`:1038`) directly; the two r39 notes are indexed
  only in the annex table. A coverage gap for the records owner, unrelated to
  the dedup verdict.
- The `## Coverage map` main table (`:3-…`) ends at r30
  (`knowledge/quote-reopen-r30.md`, `:68`); r32+ entries live in the unheaded
  annex table at `:1041`. Pre-existing structure, noted for the planner.

## Confidence and installs

High — every claim re-derived from committed bytes (sha256sum, receipt JSON
fields, the committed counter run, verbatim control files). Installs/updates:
none (pre-installed read/grep/bash/python3/sha256sum only).

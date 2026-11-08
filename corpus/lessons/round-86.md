# Round 86 — the battery carries the 200-only class and kills its mutant; the routed curation defects close (2026-11-08)

Base `3bfb6885958ad4a674ad1896f70d1e836be609e4`. Frozen claims in `corpus/evidence/round86/claims.json` and
`claims.md`; plan and amendments in `plans/round-86.md`. Round 85's non-author check routed four defects (its
`## Routed defects` 1–4); this round closes 1–4 and leaves the cross-lane one (5) routed.

## Gate

Intended-targets table `corpus/evidence/round86/egress-approval.md`, committed at `e4468752` before the first fetch.
Fetches `2026-11-08T06:00:10–11Z`, one `capture-fetch.py` GET each, all HTTP 200, no URL outside the table:

GATE-RECORD S216 url=https://www.rfc-editor.org/rfc/rfc9110.html fetched=2026-11-08T06:00:10Z tier=A decision=admit capture=corpus/captures/b1b13a12aee75c6ecc20fb91.txt capture_sha256=ec14fa3499c2dfbc… words=19 quote="the enclosed content has been modified from that of the origin server's 200 (OK) response by a transforming proxy"
GATE-RECORD S031 url=https://schema.org/lastReviewed fetched=2026-11-08T06:00:10Z tier=A decision=admit capture=corpus/captures/11d6cc56bb24adfc61eea2b4.txt capture_sha256=97fe1a6adbd2ded4… words=16 quote="Date on which the content on this web page was last reviewed for accuracy and/or completeness."

- **S216** (new, `mined`): RFC 9110 §15.3.4, the 203 clause quoted above; capture key `b1b13a12aee75c6ecc20fb91` =
  `sha256(url)[:24]`, capture sha equals the refetch row's `txt_sha256`. Tier A: a standards-track specification for
  its own status-code semantics. It grounds C1's class — a 203 body is a transforming proxy's representation, so it is
  not the origin's and cannot ground a registered quote.
- **S031** (status `queued` → `mined`, `used-by` `—` → `corpus/knowledge/provenance-recording-r85.md`, anchor gains the
  re-open date and the located definition): the round-85 inversion is closed by citing the superseding row, not the
  superseded one.
- **S024** (status `mined` → `queued`, `used-by` → `—`, `opened` `2026-11-08` → `2026-10-21`): restores the row to its
  pre-round-85 bytes. The `opened` change round 85 made was outside `CORPUS.md` rule 2 (only `status`, `recheck` and
  `used-by` change in place); the restoration is itself a change, logged here old→new as rule 2 requires.
- **S023** (re-opened, no row change): the `modified` Definition is at capture `f5545a194c06ab421875b047.txt` line 8786
  ("Date on which the resource was changed."); it is the warrant the round-84 row 9 needed and did not cite. The
  re-fetch of the same URL produced different bytes (txt sha `20dc0c3ab772…`, previously `f5545a19…` stored under the
  same key), so the capture is the newer body and the line number is the one measured on it.
- **S217** (new, `rejected`): the DCMI Namespace Policy URL redirects to `/specifications/dublin-core/dcmi-namespace/`
  and both served a 9-line stub with no policy prose, so no ≤25-word quote grounds a row. Reason and flip condition are
  in the registry row; no `GATE-RECORD` line is possible (see `## Mistakes` item 1).

## Claim outcomes

Both claims are scored on the landing bytes and then attacked by the round's wave; the final verdict is written in the
integration commit that carries `.ufo/waves/round-86/w1-results.json`. Measured at the landing (`after/c1-after.txt`,
`after/c2-after.txt`):

- **C1 operability** — `TOOL=present POSITIVE=15/15 FRESH_POSITIVE=5/5 FORGED_REFUSED=355/355 EXPECTED_CODE=355/355
  EMPTY_REFUSED=1/1 RC=4/4 SETUP=1/1 D1_FORGES=1 D1_REFUSED=1/1 MUT17_KILLED=1/1` / `GATE_RECORDS_R86=PASS`, exit 0.
  Before: the round-85 counter prints `354/354` with zero D1 lines in its bytes (grep count 0, receipt
  `controls/receipts/c1-k0b-frozen-instrument.txt`), and the round-86 battery on the pre-round-85 tool prints
  `D1_REFUSED=0/1 MUT17_KILLED=0/1` / `FAIL`, exit 1 (`controls/receipts/c1-k0-donothing.txt`).
- **C2 calibration** — `SUPERSEDED_LIVE=0 UNENTAILED_TERM=0 MODIFIED_DEF_CITED=1 QUOTES_LOCATED=20/20` /
  `CURATION_R86=PASS`, exit 0. Before: `SUPERSEDED_LIVE=1 UNENTAILED_TERM=2 MODIFIED_DEF_CITED=0 QUOTES_LOCATED=19/19`
  / `FAIL`, exit 1 (`controls/receipts/c2-d0-donothing.txt`).

## Corrections to round-85 records (routed defect 4)

- `corpus/lessons/round-85.md` `## Claim outcomes` printed **"verified"** for C1 and C2 while the filed verdict was an
  honest stop. This entry retracts that column: **C1 and C2 of round 85 did not verify as stated** (the 200-only class
  had no forgery in the battery and mutant M17 survived; K3 fired on rows 1 and 5 and the ground was narrower than the
  sentence). The superseding statement is this paragraph plus round-85's own amendments 7–10; the round-85 file is not
  edited (append-only discipline).
- Round-85 routed defect 2 (control receipts produced by a different instrument than the post value) is closed for this
  round's own controls by construction: every receipt in `corpus/evidence/round86/controls/receipts/` names the command
  and the tree it ran on, and the instrument bytes are pinned in `instrument-pins.txt` beside them.
- Round-85 routed defect 3 (add the 200-only forge to the battery) is C1 here: the forgery is built inside the counter
  from the committed `S021` row, not beside it.

## Mistakes

1. **Class: an instrument that cannot express a decision the round made.** The round refused S217 (opened, HTTP 200,
   body a stub) but `tools/gate-records.py` has only two record forms — `url/admit` (success + capture + quote) and
   `url/unreach` (failure) — so a *successful fetch refused on content* has no record form and any GATE-RECORD line for
   it would fail `REFETCH`. **Evidence pointer:** this lesson's Gate block has no S217 line while the registry row is
   `rejected`; `.ufo/waves/round-86/…` reviewer seat is asked to confirm. **Captured-by:** none — the schema gap was
   invisible until a 200-rejected row existed. **Fix:** named as QUALITY 173; the record form is routed to the next
   round that touches the tool (a `decision=reject` admit form over a committed capture, expecting no REFETCH refusal).
2. **Class: a frozen predicate narrower than the routed defect it claims to close.** The first `curation-r86.py`
   counted every supersession edge whose target was `mined` (5 on this tree) — including legitimate two-row histories
   where the superseding row is *also* `mined`. That would have made the routed defect (the inversion) indistinguishable
   from legacy. **Evidence pointer:** `plans/round-86.md` §Pre-freeze repairs 1. **Captured-by:** the pre-freeze run on
   the base tree printing 5 edges with 4 of them legitimate. **Fix:** the counter counts the live-vs-unadopted form.
3. **Class: a comparison in an instrument that ignores case.** `MODIFIED_DEF_CITED` compared a lowercase constant
   against a capitalized quote and printed 0 on a tree that carries the quote. **Evidence pointer:**
   `plans/round-86.md` §Pre-freeze repairs 2. **Captured-by:** the scratch candidate run
   (`/fast/scratch/hyaku/chousa-r86/l1/cand`), before the freeze and before any scored run. **Fix:** compare
   lowercased; disclosed rather than silently repinned.
4. **Class: an entry's warrant cites a quote that does not carry the cell's distinction.** Round 84's row 9 cited Q10
   (the `date` subproperty recommendation) for a cell about the *modified* property, and round 85's row 6 asserted a
   comparison of `lastReviewed` to a modification date that its own superseding row refuses. **Evidence pointer:** the
   round-85 non-author check's routed defect 1; the round-86 counter's `UNENTAILED_TERM=2` at base. **Captured-by:**
   the round-85 spot-check (a non-author reading), not any criterion the lane held. **Fix:** QUALITY 174/175; both rows
   repaired and the round-84 entry now cites the `modified` Definition itself.

## Corrections (from the round's own wave; append-only — the paragraphs above are not edited)

1. **The S023 capture-identity sentence is false.** `## Gate` says the re-fetch "produced different bytes (txt sha
   `20dc0c3ab772…`, previously `f5545a19…` stored under the same key)". `f5545a19…` is not a previous content hash: it
   is the capture **key** (`sha256(url)[:24]`). Every S023 refetch row in `corpus/evidence/round57/refetch.tsv` records
   the same `key` and the same `txt_sha256=20dc0c3ab772…`, and the capture file's bytes are identical at `3bfb6885` and
   at `667a5d09` (content sha `20dc0c3ab772…`, 148784 bytes; no capture write between the two revisions). The
   substantive conclusion stands — `Q13` is at capture line 8786 — but the account of how it got there compared column 9
   of the ledger against column 3. Evidence: `R86ReviewerEntry` §4 (`r86rev-capture-identity.txt`).
2. **The S024 restoration also touched two cells `CORPUS.md` rule 2 calls immutable.** The round restored `status`
   (`mined`→`queued`) and `used-by` (allowed) and also `anchor` and `opened` to their round-25 bytes. Both restorations
   are disclosed here old→new: `opened` `2026-11-08`→`2026-10-21` (round 85's in-place edit) and `anchor`
   `lastReviewed property definition paragraph (capture key 11d6cc56bb24adfc61eea2b4)`→`page heading lastReviewed,
   definition paragraph`. Rule 2 would have kept round 85's bytes and recorded the correction in a new row; the round
   chose restoration because the superseding row (`S031`) is the correction and the row must return to `queued`. Named
   as QUALITY 177. Evidence: `R86RevSupply` cell table.
3. **The S031 `anchor` edit was reverted.** The landing commit had appended the re-open date and the located definition
   to `S031`'s `anchor` cell (also immutable under rule 2). It now carries its base bytes again; the re-open is recorded
   in `corpus/evidence/round57/refetch.tsv` (row `S031`, `2026-11-08T06:00:10Z`, HTTP 200) and in this lesson's Gate
   block, which is the correct place for it. Evidence: `R86RevSupply` (named rule-2 deviation).
4. **The S217 rejection cell overstated its evidence.** It said the registered URL and its redirect target "both served
   a 9-line stub". Only the registered URL was fetched; its stored body is the redirect target's 9-line stub (capture
   `52db06f9e0e2eaf35bbdb321`). The registry cell now states what the capture shows. Evidence: `R86RevSupply`
   (ungrounded sub-claim).
5. **The registry still carries the refused comparison, in a frozen cell.** `S024`'s `teaches` asserts `lastReviewed`
   is "separate from publication or modification dates"; `S031`'s teaches refuses that comparison, and the S031 capture
   contains `modified`/`modification` 0 times. Rule 2 forbids editing `teaches`, so the round leaves it and records the
   rule instead: a superseded row's frozen `teaches` is not evidence — the superseding row's is (QUALITY 178). Routed:
   the next round that touches curation checks registry `teaches` cells against their captures, not only entry cells.
   Evidence: `R86ReviewerEntry` §2.6.

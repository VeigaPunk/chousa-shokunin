# Round 87 — settlement paragraph the L1 pastes after WAVE-DONE (DRAFT)

> **DRAFT — do not paste until the integration commit lands.**
> Author: seat `R87ScribeLesson` (scribe). Sources read: the eleven wave seat reports present in
> `.ufo/waves/round-87/w1/` (R87ExecRepro, R87ExecHarm, R87ExecForge, R87ExecC2Forge, R87MutCounter,
> R87ReviewerC1, R87ReviewerC2, R87CriticClaims, R87ScoutRegistry, R87SentinelScope, R87ConnectorSiblings),
> the frozen predicate set `corpus/evidence/round87/claims.md`, the landing revision `e6e920a4`, and this seat's
> receipts under `.ufo/waves/round-87/w1/R87ScribeLesson/receipts/`.
>
> **Committed-referent warning.** This draft reads the L1's **uncommitted** working-tree plan amendments
> (`plans/round-87.md` Amendments 1–5) and QUALITY additions (187–188). If the integration commit does not land
> them, every sentence below that names an amendment has no committed referent and must be rewritten.

## Seat tally

- **Fired (2):** `R87ExecC2Forge` (C2), `R87ReviewerC2` (C2).
- **Held (9 seats, 13 verdict lines):** `R87ExecRepro` (C1, C2), `R87ExecHarm` (C1), `R87ExecForge` (C1),
  `R87MutCounter` (C1, C2), `R87ReviewerC1` (C1), `R87CriticClaims` (C1, C2), `R87ScoutRegistry` (C2),
  `R87SentinelScope` (C1, C2), `R87ConnectorSiblings` (C1, C2).

Evidence: `.ufo/waves/round-87/w1/R87ScribeLesson/receipts/r14-verdicts-read.txt` (every `VERDICT` line, verbatim).

## The paragraph to paste

> Round 87's wave fired C2 and held C1. C2 fired on two seats: `R87ExecC2Forge` showed the round-87 curation
> counter accepts two in-class forgeries — a one-word junk quote (`"validity"`) that replaces the real `Q11` while
> restoring the floor count and leaving the warrant resolved, and the truncation of `Q11` to the bare verbatim word
> `"range"` (`.ufo/waves/round-87/w1/R87ExecC2Forge/receipts/receipt-A1c-strong-junk.txt`,
> `…/receipt-A1d-truncate-to-junkword.txt`) — and `R87ReviewerC2` showed the frozen sentence overstates the
> counter's guarantee in two further places, the per-qid sharing conjunct on the r85 row *Naming what a resource
> derives from* and the structural, status-blind supersession disposition
> (`.ufo/waves/round-87/w1/R87ReviewerC2/receipts/r05-native-warrant-multi-qid.txt`,
> `…/r06-teaches-rejected-superseder.txt`); C2's predicate still prints
> `SUPERSEDED_LIVE=0 UNENTAILED_TERM=0 MODIFIED_DEF_CITED=1 QUOTES_LOCATED=20/20 … WARRANT_OK=17/17 … LEGS=7/7` /
> `CURATION_R87=PASS` and refuses all four routed forgeries (`FORGERY_REFUSED=4/4`), so the firing is against the
> sentence's wording and is discharged by plan Amendments 1–3. C1 held on every C1 seat: the frozen line re-derives
> at `e6e920a4` with `D1_EXPECTED=3 D1_FORGES=3 D1_REFUSED=3/3 D2_FORGES=3 D2_REFUSED=3/3 MUT_ADMIT_KILLED=1
> MUT_UNREACH_KILLED=1 DERIVE_NEG=1 LEGS=15/15` and no committed record moves
> (`.ufo/waves/round-87/w1/R87ExecRepro/receipts/01-gate-records-r87.txt`, `…/05-harm-recheck.txt`), with the leg
> count guarding appends rather than executions and the class width being non-200 rather than 203, so C1 holds at
> the property Amendment 4 records.

## Per-fired-claim line (one sentence each, seat + receipt path)

- **C2 — `R87ExecC2Forge`** — the curation counter accepts two in-class forgeries, a one-word junk quote that
  replaces `Q11` and restores the count (`QUOTES_LOCATED=20/20 … WARRANT_OK=17/17 LEGS=7/7 CURATION_R87=PASS`,
  exit 0) and the truncation of `Q11` to the bare verbatim word `"range"` (same line, exit 0) —
  `.ufo/waves/round-87/w1/R87ExecC2Forge/receipts/receipt-A1c-strong-junk.txt`,
  `.ufo/waves/round-87/w1/R87ExecC2Forge/receipts/receipt-A1d-truncate-to-junkword.txt`.
- **C2 — `R87ReviewerC2`** — the frozen sentence overstates the counter's guarantee in two places: the r85 row
  *Naming what a resource derives from* names `Q1, Q3` and counts `WARRANT_OK` although `Q3` shares no distinctive
  word with the row's cells, and a flagged row is disposed as superseded by a row whose own status is `rejected` —
  `.ufo/waves/round-87/w1/R87ReviewerC2/receipts/r05-native-warrant-multi-qid.txt`,
  `.ufo/waves/round-87/w1/R87ReviewerC2/receipts/r06-teaches-rejected-superseder.txt`.

## Pre-conditions before this paragraph may be pasted

Each is a finding in `.ufo/waves/round-87/w1/R87ScribeLesson.md`; each must be discharged by the integration
commit, or the paragraph above must be rewritten to drop the referent.

1. Land `plans/round-87.md` Amendments 1–5 and `corpus/QUALITY.md` 187–188 (currently uncommitted —
   `git status --short` shows ` M plans/round-87.md`, ` M corpus/QUALITY.md`).
2. Correct the Gate block's egress sentence: the committed table's own bound is `>= 2026-11-08T1` (0 rows) and the
   column is `fetched_utc`, not `fetched` — `.ufo/waves/round-87/w1/R87ScribeLesson/receipts/r09-egress-predicate.txt`.
3. Correct "**S216** (re-opened; row unchanged)": the `used-by` cell changed —
   `.ufo/waves/round-87/w1/R87ScribeLesson/receipts/r06-registry-rows.txt`.
4. Restore `Q_FLOORS=…13/13 floor13,…7/7 floor7` to the quoted C2 outcome line, or mark the quotation as a field
   selection — `.ufo/waves/round-87/w1/R87ScribeLesson/receipts/r10-quoted-lines.txt`.
5. Commit `corpus/evidence/round87/census-start.txt` and `census-end.txt`, each stating the revision it was
   computed against — `.ufo/waves/round-87/w1/R87ScribeLesson/receipts/r11-census-receipts.txt`.
6. Re-word intake rows 1, 2, 4 and 5, which say "fixed" where Amendments 1–4 narrow the property —
   `.ufo/waves/round-87/w1/R87ScribeLesson/receipts/r14-verdicts-read.txt`.
7. Correct the appended `corpus/README.md` coverage row: "four mined mistakes" → the lesson's count, and "the
   two-sentence spot-check intake" → the eight-row table.
8. Fix Mistake 1's pointer (`SURVIVOR N-deny-width` is in no receipt; the committed receipt prints
   `EQUIVALENT_ON_TREE N-deny-width rc=0 GATE_RECORDS_R87=PASS`), Mistake 2's pointer (`plans/round-87.md` contains
   no "12" and Pre-freeze repair 7 lists no rows), Mistake 3's fix (name QUALITY 181's `sha256sum` comparison as the
   failable check), and QUALITY 184's back-reference (`Mistakes 3` → `Mistakes 4`) —
   `.ufo/waves/round-87/w1/R87ScribeLesson/receipts/r15-mistake-pointers.txt`.

VERDICT: R87ScribeLesson C1 held — the claim's predicate re-derives at `e6e920a4` with the frozen line and no committed record moves, but the lesson's C1 prose still asserts a verdict that is "a count of executed legs" and that the `M2` shape changes the verdict, which the wave's `E1`/`E4`/`E5`/`E7` probes and the L1's own plan Amendment 4 falsify, so C1 holds at the narrowed property and the settlement prose must carry that narrowing.
VERDICT: R87ScribeLesson C2 fired — two seats fired the frozen C2 sentence's wording (an accepted junk-quote forgery, an accepted quote truncation, a per-qid sharing conjunct the counter does not enforce, and a status-blind supersession disposition) while the predicate itself still prints PASS and refuses 4/4, so the discharge is plan Amendments 1–3, which are still uncommitted in the working tree.

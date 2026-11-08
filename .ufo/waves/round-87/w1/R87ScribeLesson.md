# R87ScribeLesson — round-87 lesson settlement sections: audit of the L1's draft against committed bytes

Seat: `R87ScribeLesson` (scribe; leaf member — no subagent dispatch, no production edit, no lane/fleet git
mutation, no network). Lane root `/home/vgpnk/Projects/shokunin/chousa-shokunin`. Nothing outside this seat's
folder `.ufo/waves/round-87/w1/R87ScribeLesson/` was written; the lesson, plan, QUALITY and every corpus file
were read only. Scratch `/fast/scratch/hyaku/chousa-r87/R87ScribeLesson/` was deleted before this report was
written; every receipt cited below was copied into `receipts/` first.

Revisions read: base `6495ef88`, egress `b7db0714`, freeze `c033577b`, landing `e6e920a4`, wave-spec `abf7ea58`.
The lesson was audited at working-tree sha256 `fea7c4647706433a3dfcf7c3aea2991dd3845b41cb730aba20716eb9dbc093f5`
(receipt `receipts/r13-gate-verify-final.txt`); the L1 was still editing it during this seat's audit, so each
finding below is stated against the bytes named in its own receipt.

---

## (a) The `## Gate` block, against `gate-records.py verify` and the registry rows

**Gate block: PASS on the tool check, with three named divergences from the committed bytes.**

Command and observed line (receipt `receipts/r01-gate-records-verify.txt`, re-bound at
`receipts/r13-gate-verify-final.txt`):

```
$ python3 tools/gate-records.py verify --root . --repo . corpus/lessons/round-87.md
GATE_RECORD corpus/lessons/round-87.md:13 S216 OK
GATE_RECORDS files=1 records=1 ok=1 fail=0
exit=0
```

The single `GATE-RECORD` line in the lesson verifies OK under the landed subject tool, at line 13.

Registry rows (receipt `receipts/r06-registry-rows.txt`, `git diff 6495ef88 e6e920a4 -- corpus/SOURCES.md`):

| claim in the Gate block | committed bytes | verdict |
|---|---|---|
| `S216.used-by` `corpus/evidence/round86/claims.md` → `…round86/claims.md, …round87/claims.md` | exactly that diff hunk, and nothing else in the S216 row changes | **matches** |
| `S218` appended, `own-work`, tier A, `mined`, `used-by corpus/evidence/round87/claims.md` | row `S218` reads exactly that | **matches** |
| "218 rows" | 218 rows at `e6e920a4` (`receipts/r11-census-receipts.txt`), base 217 + 1 | **matches** |
| "Both columns are byte-identical to round 86's attempt: `raw_sha256=d431760660ea…` and `txt_sha256=ec14fa3499c2…` on attempts 1 and 2" | both `S216` rows carry `d431760660ea44e13…` and `ec14fa3499c2dfbc…`; `git diff --stat 6495ef88 e6e920a4 -- corpus/captures/` is empty | **matches** |
| "the §15.3.4 clause at capture line 12267" | capture line 12267 is `indicates that the request was successful but the enclosed content has been`; the §15.3.4 heading is at line 12261 | **matches** (the quoted 22-word string starts at 12267) |
| "census exit 0 before and after, same five pre-existing `W04` warnings" | census-end.txt shows exit 0 with the same five `W04`s; **the before-receipt is not committed and its mtime is 76 s *after* the end receipt** | **diverges — see finding G3** |

**Finding G1 — the Gate's egress bound is not the committed table's bound, and the table's own bound is vacuous.**
The Gate block says the egress table is "committed at `b7db0714` before the first fetch (the commit precedes every
`refetch.tsv` row whose `fetched` is `2026-11-08T06:50:40Z`)". That is a true statement about the row
`S216` attempt 2 (`fetched_utc` = `2026-11-08T06:50:40Z`, commit `b7db0714` at `2026-11-08T03:50:27-03:00` = 06:50:27Z).
But the committed table's own sentence (`corpus/evidence/round87/egress-approval.md:4-5`) reads "whose `fetched` is
`2026-11-08T1` or later", and read literally against the ledger that bound selects **zero rows**
(receipt `receipts/r09-egress-predicate.txt`: `>= 2026-11-08T1` → 0 rows; `>= 2026-11-08T06` → 5; `>= 2026-11-08T06:50` → 1).
The ledger's column is `fetched_utc`, not `fetched`. The behaviour was compliant — every round-87 fetch is inside the
table (`R87SentinelScope` F1, clean) — but the artefact's own self-check could never have detected a violation.
The lesson's Gate block as written therefore **does not reproduce the committed artefact's own claim**, and the
defect is unrecorded at the landing revision: `Mistake 6` and `QUALITY 188` exist only in the L1's uncommitted
working tree, and `plans/round-87.md`'s five amendments are also uncommitted (`git status --short` → ` M` on
`plans/round-87.md` and `corpus/QUALITY.md`). The L1 must land the amendment, the criterion and the Mistake
together with the integration commit, or the settlement paragraph will cite amendments that no reader of the
committed tree can see.

**Finding G2 — the lesson says the S216 row is "unchanged"; the row's `used-by` cell changed.**
Gate block: "**S216** (re-opened; row unchanged)". The `used-by` cell gained `corpus/evidence/round87/claims.md`
in the same commit (receipt `receipts/r06-registry-rows.txt`). The lesson's own registry-changes list two
paragraphs below records that change, so the block contradicts itself; "row unchanged" is true only of the
row's `status`, `recheck`, `scope`, `anchor` and `teaches` cells. This is the QUALITY 181 class (an identity
field compared against the wrong column) recurring inside the lesson's own text.

**Finding G3 — the "census exit 0 before and after" claim rests on two receipts that are not committed, and the
"before" receipt's mtime is after the "after" receipt's.**
`corpus/evidence/round87/census-start.txt` and `census-end.txt` are untracked (`git ls-files corpus/evidence/round87/`
lists neither; receipt `receipts/r07-census.txt`), and their mtimes invert the naming:
census-end `03:53:49`, census-start `03:55:05`, landing commit `03:52:30` (receipt `receipts/r11-census-receipts.txt`).
A reader of the committed tree therefore has no census receipt at all, and the file that asserts "before" carries
the later timestamp. The content is right — census-start records the base `6495ef88` registry computed from a base
archive, so the base-state census is correct by construction — but the *ordering* claim is not evidenced. Same
defect class as `R87SentinelScope` F5. The fix is to commit both receipts with the integration commit and to state
in each which revision it was computed against.

**Finding G4 — the C2 line quoted in `## Claim outcomes` is not the line the counter prints.**
The lesson quotes `SUPERSEDED_LIVE=0 UNENTAILED_TERM=0 MODIFIED_DEF_CITED=1 QUOTES_LOCATED=20/20 WARRANT_OK=17/17
TEACHES_CHECKED=1 TEACHES_FLAGGED=1 TEACHES_UNRESOLVED=0 LEGS=7/7`. The counter's actual line (receipt
`receipts/r10-quoted-lines.txt`, re-run at `receipts/r03-c2-counter-at-landing.txt`) also carries
`Q_FLOORS=search-transparency-reporting-r84.md=13/13 floor13,provenance-recording-r85.md=7/7 floor7` between
`QUOTES_LOCATED=20/20` and `WARRANT_OK=17/17`. The C1 line, by contrast, is byte-identical to the counter's
(receipt `receipts/r12-after-vs-remeasure.txt`: C1 lines IDENTICAL). The C2 quotation is a field subset, not the
printed line, and it drops exactly the field that carries routed defect 4's floors (13/7) — the two numbers the
claim's own predicate names. The `Q_FLOORS` field must appear in the quoted line or the quotation must be marked
as a field selection.

---

## (b) The `## Mistakes` items 1–4: class · evidence pointer · captured-by · fix, and a failable check per fix

All four items carry the four required fields. The check that each fix names:

| item | class | evidence pointer | captured-by | fix | the check the fix names, and whether it can fail |
|---|---|---|---|---|---|
| 1 | counter whose "independent" second derivation calls the same helper | the first `mutate-r87.py` run — `SURVIVOR N-deny-width` on the self-referential variant, and the design review before that run | round-86 critic's `T4` finding; no criterion covered the two-derivations rule | `count_203_rows` parses the two committed files on its own path (QUALITY 182), and `mutate-r87.py`'s `T4-truncate` shows the width leg failing `1/3 floor3` | **`mutate-r87.py`'s `T4-truncate`** → `LEG_FAIL D1_WIDTH 1/3 floor3` (committed receipt `controls/receipts/c1-mutants.txt`). **Can fail** ✓ |
| 2 | a rule scoped by vocabulary over-fires | the probe run recorded in `plans/round-87.md` §Pre-freeze repairs 7 (12 flagged rows listed before the fix) | the pre-freeze probe (no criterion existed; QUALITY 169's dry-run rule is the class) | the leg requires a *contrast phrase* as well as the term, and requires a disposition rather than a clean registry (QUALITY 183) | **the `T-teaches-contrast` mirror** → `LEG_FAIL TEACHES checked=2 flagged=2 unresolved=1` (committed receipt `controls/receipts/c2-controls.txt`, re-run receipt `receipts/r04-c2-controls.txt`). **Can fail** ✓ |
| 3 | a capture-identity sentence written from the attempt number instead of the hashes | `grep -P '^S216\t' corpus/evidence/round57/refetch.tsv` → two rows, one `raw`/`txt` pair | QUALITY 181 (compare identity columns column-to-column before writing a sentence about them), applied before the commit rather than after | the sentence now cites both columns and the empty capture diff | **`git diff --stat 6495ef88 e6e920a4 -- corpus/captures/`** → empty (receipt `receipts/r05-egress-vs-fetch.txt`). **Can fail** ✓ — but note the fix's own check is a *state*, not a command that fails *for this lesson*; the empty diff is the observation, and QUALITY 181's `sha256sum` check is the failable form. See finding M3. |
| 4 | a battery's parse of `--tool` output attributed a stale expected code to the wrong class | the smoke run's `FORGED_REFUSED=362/362` after the differentiator was placed on the unreach branch only | **none** — the shape error was caught by the smoke run before the freeze | the differentiator is appended in the `unreach` branch only (QUALITY 184) | **the D8 differentiator's branch placement** — `gate-records-r87.py:135` sits inside `elif form == "unreach":`, and the differentiator's expected code is `REFETCH` (line 414-417), matched by `code in v[1]` (line 462). **Can fail** ✓ structurally, but see finding M4. |

**Finding M1 — the fix of item 1 is checked by a mutation whose own receipt the lesson mislabels; the underlying
claim of item 1 survives.**
Item 1 says the first `count_203_rows` was `return len(_qualifying_203(root))`, so narrowing the helper would move
both sides. The fix names `mutate-r87.py`'s `T4-truncate` as the witness, and the committed receipt does show
`KILLED T4-truncate … LEG_FAIL D1_WIDTH 1/3 floor3` — but `T4-truncate` narrows the **builder** while
`count_203_rows` stays independent, so it witnesses the *repaired* shape, not the defect. The defect's own witness
is `N-deny-width`, the `EQUIVALENT` entry in `mutate-r87.py:57-60` — and there the committed receipt prints
`EQUIVALENT_ON_TREE N-deny-width rc=0 GATE_RECORDS_R87=PASS`, i.e. the self-referential variant **passes**, exactly
as `R87ReviewerC1` §(b) E1 and `R87CriticClaims` §(c) found. The lesson's evidence pointer says the first run
printed `SURVIVOR N-deny-width`; that string exists in `corpus/QUALITY.md:1135` and in this lesson, and in **no
receipt** — `grep -rn "SURVIVOR N-deny-width" corpus/ plans/ .ufo/waves/round-87/` returns only those two prose
files plus this report (receipt `receipts/r15-mistake-pointers.txt`). QUALITY 182's "Shown able to fail: the
self-referential variant prints `SURVIVOR N-deny-width`
in the first mutation run" is therefore an unbacked receipt line. What the committed battery prints for that mutant
id is `EQUIVALENT_ON_TREE`, and the mutant is labelled `EQUIVALENT` in the instrument's own comment: "Degenerate on
THIS tree, reported not counted". The honest form: the two-derivations property is witnessed by `T4-truncate`
killing `D1_WIDTH 1/3`; the self-referential variant is **equivalent on this tree**, and its survival is the
tautology family `R87ReviewerC1` measured, not a killed mutant.

**Finding M2 — item 2's evidence pointer cites a list that is not in the file it names.**
The pointer is "`plans/round-87.md` §Pre-freeze repairs 7 (12 flagged rows listed before the fix)". `plans/round-87.md`
§Pre-freeze repairs 7 lists **no rows and no count** — `grep -n "12" plans/round-87.md` returns nothing
(receipt `receipts/r09-egress-predicate.txt` is the egress probe; the plan probe is recorded in the report's
`## Findings`). The number 12 is nonetheless **independently reproducible from the committed bytes** by my own
re-derivation (receipt `receipts/teaches-counts.txt`): a term-only rule over live (non-superseded) rows flags
exactly 12 rows — `S028, S097, S102, S105, S115, S118, S121, S122, S124, S125, S136, S147` — all `mined`, and
`S024` is the one row the contrast rule reaches. So the *count* is right and the *pointer* is wrong: the pointer
should be the receipt that carries the list (a new committed probe receipt), not the plan's repair paragraph,
which never contained it.

**Finding M3 — item 3's fix names no command that can fail, only a state that happens to hold.**
"**Fix:** the sentence now cites both columns and the empty capture diff." The empty diff is an observation about
the tree, not a check that fails when the lesson is wrong; the check that *can* fail for this mistake is QUALITY
181's `sha256sum` the capture at both revisions before writing any sentence about capture identity. Item 3 is the
only one of the four whose fix, read strictly, names no failing command; the other three name a mutant, a mirror
and a branch placement. Against the seat brief's rule — "each fix must name a check that can fail" — item 3 is
**asserted rather than shown** and should be restated as the `sha256sum` comparison.

**Finding M4 — item 4's "Captured-by: none" leaves the class uncaptured by any criterion at the landing revision,
and QUALITY 184 cites the wrong lesson mistake.**
Item 4 says "**Captured-by:** none — the shape error was caught by the smoke run before the freeze." That is
honest, but it means the class was captured by nothing committed. QUALITY 184 (committed at `e6e920a4`) cites
"`lessons/round-87.md` Mistakes 3" — while the lesson's Mistakes 3 is the capture-identity item and the
differentiator item is **Mistakes 4**. `git show e6e920a4:corpus/QUALITY.md` shows the same mis-citation at line
1151. The back-reference points at the wrong mistake in the same tree it cites.

**Finding M5 — items 5 and 6, added to the working tree during this audit, are well-formed; item 5's fix is
backed by a failable check, item 6's by a failable command.**
Item 5 (the plan's mechanism sentence vs the measured leg-accounting width) names `R87ReviewerC1` §(b)'s `E1`, `E4`,
`E7`, `E8` — each a mutant that **fails or survives** and is therefore a check that can fail (receipt
`receipts/r14-verdicts-read.txt` cites the seat verdicts; the E-series receipts are copied under
`receipts/cited/`). Item 6 (the egress table's vacuous closure bound) names
`awk -F'\t' '$5 >= "<bound>"' corpus/evidence/round57/refetch.tsv` and my own probe shows the written bound returns
0 rows while `>= 2026-11-08T06` returns 5 — a check that demonstrably fails on the artefact it judges
(receipt `receipts/r09-egress-predicate.txt`). Both items carry class · evidence pointer · captured-by · fix.

---

## (c) The `## Spot-check intake`: all eight items of round 86's routed-defect and conformance list, one row each

Round 86's non-author check (`corpus/lessons/round-86-verifier-spotcheck.md`) carries five routed defects
(lines 88-96) and three conformance notes (lines 98-107) — **eight items**. The lesson's intake table has
**eight rows, one per item**, in the same order: routed 1-5, conformance 1-3. Every row has a disposition and a
pointer. No item is dropped, merged or duplicated.

Row-by-row audit of the dispositions against committed bytes:

| row | disposition claimed | pointer | audit |
|---|---|---|---|
| 1. `D1` one record wide | **fixed** — class is every qualifying committed row (3), an independent width count, a `>= 3` floor | `gate-records-r87.py` (`_qualifying_203`, `count_203_rows`); `c1-mutants.txt` `KILLED T4-truncate` | pointer resolves ✓ (`count_203_rows` at :294, `EXPECTED_LEGS=15` at :41, floor `>= 3` at :544); `KILLED T4-truncate` in the committed receipt ✓. **But "fixed" is now contradicted by the wave**: `R87ReviewerC1` §(a) measures the class as *non-200*, not 203, with two builder/counter divergences, and `R87CriticClaims` finds the `T4-record-keyed` mutant does not instantiate the class it claims. The row must read "fixed at the narrowed property" once Amendment 4 lands. |
| 2. mutant-derivation and SETUP are printed fields | **fixed** — verdict is leg-accounted; `M2` and `M5` shapes now change the verdict | `c1-mutants.txt` `KILLED M2-credit-mutant`, `KILLED M5-drop-setup` | both killed in the committed receipt ✓, but `R87CriticClaims` §(c) measures the committed `M2` mutant as a **denial** (`derived=0`), not the credit shape, and the two-point credit variant passes. "M2 … changes the verdict" is not witnessed by the frozen battery. Same amendment as row 1. |
| 3. a `decision=reject` 203 record is accepted | **fixed** — the unreach form refuses every 2xx; new `D2` class from the same rows | `tools/gate-records.py` `check()` unreach branch; `D2_REFUSED=3/3`; `c1-harm-unreach.txt` `moved=0` | verified independently: `success = kv["curl_rc"] == "0" and 200 <= int(kv["http"]) < 300` (`tools/gate-records.py:252`) and `D2_REFUSED=3/3` at landing (receipt `receipts/r02-c1-battery-at-landing.txt`); harm sweep `files=11 records=28 moved=0` (receipt `receipts/r08-harm.txt`). **This row holds.** One caveat: the harm sweep's `files=10 records=27` in the frozen receipt becomes `files=11 records=28` at landing (the lesson's own Correction 2 records this) ✓ |
| 4. C2 floors unimplemented; `MODIFIED_DEF_CITED` is presence | **fixed** — per-entry floors (13/7), a warrant-linkage leg over 17 decision rows | `curation-r87.py` `FLOOR`/`WARRANT`; `c2-controls.txt` `FORGERY_REFUSED=4/4` | pointer resolves ✓ (`FLOORS` at :42-45, `FLOOR` leg at :200, `WARRANT` at :227); `FORGERY_REFUSED=4/4 R86_ACCEPTED_FORGERY=4/4` re-run ✓ (receipt `receipts/r04-c2-controls.txt`). **But "fixed" is contradicted by the wave**: `R87ExecC2Forge` fired C2 on A1c/A1d, and `R87ReviewerC2` fired C2 on F1/F2. Three clauses of C2's frozen sentence were narrowed by Amendments 1-3. The row must read "fixed at the narrowed property". |
| 5. registry `teaches` never read against its capture | **fixed as a machine-checked leg with a disposition rule**, not by editing the frozen cell | `curation-r87.py` `TEACHES`; S218 row | pointer resolves ✓ (`TEACHES` leg at :229, `CONTRAST`/`DATE_TERMS` at :49-50); the S218 row exists and is `own-work`/A/`mined` ✓; the leg does read the teaches cell against its own capture (`capture_text` → `miss`), and `S024` is flagged with a named disposition ✓. **But the disposition rule is structural, not status-checked** (`R87ReviewerC2` F2: `S198` is disposed by `S202`, which is `rejected`) — Amendment 3's narrowing. Same fix as rows 1, 2, 4. |
| conformance 1. census ran after the landing commit in round 86 | **avoided** — this round's start census ran before any edit and is recorded in the report | report `Sources & frontier` | **the claim as written is not supported by committed bytes.** The census receipts are untracked and their mtimes invert the naming (finding G3); the receipt that asserts "before" was written *after* the landing commit; and the pointer is to the round's report, which does not exist yet (`.ufo/reports/round-87/chousa.md` — absent, receipt `receipts/r11-census-receipts.txt`). The substance (base-state census correct by construction) holds; the *ordering* and the *pointer* do not. |
| conformance 2. the dispatched prompt has a truncated run-15 quote | **carried** — template defect, operator-owned | report `Sources & frontier` | **carried correctly.** Verified: `.ufo/prompts/chousa-round-87.md:143` ends `…shokunin style bu…`, byte-identical to `.ufo/prompts/chousa-round-86.md:143` — the truncation persists into this round's dispatch. The pointer is to the report, which is not yet written; the checkable pointer is the prompt line itself. |
| conformance 3. `corpus/README.md` frontier text ends at round 6 | **carried, indexed** — this round appends a coverage row rather than rewriting the frontier prose | `corpus/README.md` | **carried correctly and the index is real.** `git diff 6495ef88 e6e920a4 -- corpus/README.md` appends a `## Round-86 / round-87 coverage appended 2026-11-08` section with five rows and leaves the round-1-6 frontier prose untouched ✓. One stale item in the appended row: it says the lesson has "four mined mistakes" and "the two-sentence spot-check intake" — the working-tree lesson now has **six** mistakes and the intake is an eight-row table. The README row needs the count corrected before landing. |

**Finding S1 — four of the eight rows say "fixed" where the wave narrowed the property.** Rows 1, 2, 4 and 5 are
discharged by Amendments 4 (rows 1-2), 1-2 (row 4) and 3 (row 5) in the L1's *uncommitted* working tree. As the
lesson stands, the table claims the routed defects are closed unconditionally while the same tree's plan says three
of C2's clauses and three of C1's clauses were narrowed. The table's dispositions and the plan's amendments must
be reconciled in one commit; a reader of the committed tree must not find "fixed" beside a narrowing.

**Finding S2 — the census conformance row's disposition is asserted against bytes that do not support it.** See
G3 and S-row-1 above.

**Finding S3 — the appended README coverage row miscounts the lesson it indexes.** "four mined mistakes" and
"the two-sentence spot-check intake" against a lesson with six mistakes and an eight-row table.

---

## (d) The settlement paragraph the L1 will paste after WAVE-DONE — DRAFT

> **DRAFT — not for pasting until the integration commit lands. Author: seat `R87ScribeLesson`; this draft reads
> only the eleven wave seat reports present in `.ufo/waves/round-87/w1/` at `2026-11-08` (R87ExecRepro, R87ExecHarm,
> R87ExecForge, R87ExecC2Forge, R87MutCounter, R87ReviewerC1, R87ReviewerC2, R87CriticClaims, R87ScoutRegistry,
> R87SentinelScope, R87ConnectorSiblings), the frozen predicate set `corpus/evidence/round87/claims.md`, the
> landing revision `e6e920a4`, and this seat's own receipts under
> `.ufo/waves/round-87/w1/R87ScribeLesson/receipts/`. It also reads the L1's *uncommitted* working-tree plan
> amendments and QUALITY additions; if they are not landed, the sentences below have no committed referent.**

**Seats that fired (2):** `R87ExecC2Forge` — C2; `R87ReviewerC2` — C2.
**Seats that held (9 of 11 seats, 13 verdict lines):** `R87ExecRepro` (C1, C2), `R87ExecHarm` (C1),
`R87ExecForge` (C1), `R87MutCounter` (C1, C2), `R87ReviewerC1` (C1), `R87CriticClaims` (C1, C2),
`R87ScoutRegistry` (C2), `R87SentinelScope` (C1, C2), `R87ConnectorSiblings` (C1, C2).

**C2 fired** — `R87ExecC2Forge` showed that the round-87 curation counter accepts two in-class forgeries: a
one-word junk quote (`"validity"`) that replaces the real `Q11` and restores the count while the warrant still
resolves (`QUOTES_LOCATED=20/20 … WARRANT_OK=17/17 LEGS=7/7 CURATION_R87=PASS`, exit 0), and the truncation of
`Q11` to the bare verbatim word `"range"` (same line, exit 0), both in
`.ufo/waves/round-87/w1/R87ExecC2Forge/receipts/receipt-A1c-strong-junk.txt` and
`…/receipt-A1d-truncate-to-junkword.txt`; `R87ReviewerC2` showed that the same counter's frozen sentence overstates
its own guarantee in two further places — the r85 row `Naming what a resource derives from` names `Q1, Q3` and
counts `WARRANT_OK` although `Q3` shares no distinctive word with the row's cells
(`…/R87ReviewerC2/receipts/r05-native-warrant-multi-qid.txt`), and a flagged row is disposed as superseded by a
row whose own status is `rejected` (`…/R87ReviewerC2/receipts/r06-teaches-rejected-superseder.txt`).

**C1 held** — every C1 seat re-derived the frozen line at `e6e920a4` (`TOOL=present POSITIVE=15/15 FRESH_POSITIVE=5/5
FORGED_REFUSED=362/362 EXPECTED_CODE=362/362 EMPTY_REFUSED=1/1 RC=4/4 SETUP=1/1 D1_EXPECTED=3 D1_FORGES=3
D1_REFUSED=3/3 D2_FORGES=3 D2_REFUSED=3/3 MUT_ADMIT_DERIVED=1 MUT_ADMIT_KILLED=1 MUT_UNREACH_DERIVED=1
MUT_UNREACH_KILLED=1 DERIVE_NEG=1 LEGS=15/15` / `GATE_RECORDS_R87=PASS`, exit 0; my own re-run reproduces it
byte-identically at `.ufo/waves/round-87/w1/R87ScribeLesson/receipts/r02-c1-battery-at-landing.txt`) and the harm
sweep moves no committed record — but `R87ReviewerC1` and `R87CriticClaims` both measured that the verdict counts
*appends*, not executions, and that the class width is *non-200*, not 203, so the held verdict rests on the
narrowed property recorded in plan Amendment 4, not on the landed sentence.

**C2 held at the predicate** — the frozen line prints and all four routed forgeries are refused
(`FORGERY_REFUSED=4/4 R86_ACCEPTED_FORGERY=4/4`; receipts `receipts/r03-c2-counter-at-landing.txt` and
`receipts/r04-c2-controls.txt`), so C2's K1 and K3 hold at `e6e920a4`; the firing is against the *wording* of the
frozen sentence, which plan Amendments 1-3 narrow.

**The settlement paragraph (draft text):**

> Round 87's wave fired C2 and held C1. C2 fired on two seats: `R87ExecC2Forge` showed the curation counter accepts
> two in-class forgeries — a one-word junk quote that replaces the real `Q11` while restoring the floor count and
> leaving the warrant resolved, and the truncation of `Q11` to the bare verbatim word `"range"`
> (`.ufo/waves/round-87/w1/R87ExecC2Forge/receipts/receipt-A1c-strong-junk.txt`,
> `…/receipt-A1d-truncate-to-junkword.txt`) — and `R87ReviewerC2` showed the frozen sentence overstates the
> counter's guarantee in two further places, the per-qid sharing conjunct on the r85 row `Naming what a resource
> derives from` and the structural, status-blind supersession disposition
> (`.ufo/waves/round-87/w1/R87ReviewerC2/receipts/r05-native-warrant-multi-qid.txt`,
> `…/r06-teaches-rejected-superseder.txt`); C2's predicate still prints
> `SUPERSEDED_LIVE=0 UNENTAILED_TERM=0 MODIFIED_DEF_CITED=1 QUOTES_LOCATED=20/20 … WARRANT_OK=17/17 … LEGS=7/7` /
> `CURATION_R87=PASS` and refuses all four routed forgeries (`FORGERY_REFUSED=4/4`), so the firing is against the
> sentence's wording and is discharged by plan Amendments 1-3. C1 held on every C1 seat: the frozen line re-derives
> at `e6e920a4` with `D1_EXPECTED=3 D1_FORGES=3 D1_REFUSED=3/3 D2_FORGES=3 D2_REFUSED=3/3 MUT_ADMIT_KILLED=1
> MUT_UNREACH_KILLED=1 DERIVE_NEG=1 LEGS=15/15` and no committed record moves
> (`.ufo/waves/round-87/w1/R87ExecRepro/receipts/01-gate-records-r87.txt`,
> `…/05-harm-recheck.txt`), with the leg count guarding appends rather than executions and the class width being
> non-200 rather than 203, so C1 holds at the property Amendment 4 records.

**Pre-conditions the L1 must satisfy before pasting (each is a finding in this report):** land
`plans/round-87.md`'s Amendments 1-5 and `corpus/QUALITY.md` 187-188, or the sentences above have no committed
referent; correct the Gate block's egress sentence to the artefact's own bound or record the divergence; correct
"row unchanged" for `S216`; restore the `Q_FLOORS` field to the quoted C2 line; commit `census-start.txt` and
`census-end.txt` with the revisions they were computed against; and re-word the four intake rows that say "fixed"
where a narrowing applies.

---

## Findings

| # | finding | kind | evidence |
|---|---|---|---|
| G1 | The Gate block's egress bound (`>= 2026-11-08T06:50:40Z`, one row) is not the committed table's own bound (`>= 2026-11-08T1`, **0 rows**); the artefact's closure predicate is vacuous and names a column the ledger does not have (`fetched` vs `fetched_utc`). The defect is recorded only in the L1's uncommitted working tree (Mistake 6, QUALITY 188). | claim-vs-bytes | `receipts/r09-egress-predicate.txt`; `receipts/r05-egress-vs-fetch.txt` |
| G2 | "**S216** (re-opened; row unchanged)" — the row's `used-by` cell changed in the same commit, as the lesson's own registry-changes list records two paragraphs later. | internal contradiction | `receipts/r06-registry-rows.txt` |
| G3 | "census exit 0 before and after" rests on two **uncommitted** receipts whose mtimes invert the naming (start 76 s after end, both after the landing commit). | receipt hygiene | `receipts/r07-census.txt`; `receipts/r11-census-receipts.txt` |
| G4 | The quoted C2 outcome line omits `Q_FLOORS=…13/13 floor13,…7/7 floor7`, the field carrying routed defect 4's floors; the C1 line is byte-exact. | fidelity | `receipts/r10-quoted-lines.txt`; `receipts/r12-after-vs-remeasure.txt` |
| M1 | Item 1's pointer cites `SURVIVOR N-deny-width`, a string no receipt contains; the committed receipt prints `EQUIVALENT_ON_TREE N-deny-width rc=0 …=PASS` for that mutant id, and the instrument labels it `EQUIVALENT`. QUALITY 182's "Shown able to fail" line rests on the same unbacked string. | claim-vs-bytes | `corpus/evidence/round87/controls/receipts/c1-mutants.txt`; `corpus/evidence/round87/mutate-r87.py:57-60,133` |
| M2 | Item 2's pointer names `plans/round-87.md` §Pre-freeze repairs 7 as carrying the 12 flagged rows; that paragraph lists no rows and the file contains no "12". The count is independently reproducible (12 live rows) — the pointer is what is wrong. | dead pointer | `receipts/teaches-counts.txt` |
| M3 | Item 3's fix names no command that can fail, only the empty capture diff — a state, not a check. QUALITY 181's `sha256sum` comparison is the failable form. | asserted fix | `receipts/r05-egress-vs-fetch.txt` |
| M4 | Item 4 records "Captured-by: none", and QUALITY 184 cites "`lessons/round-87.md` Mistakes 3" while the differentiator item is Mistakes 4. | cross-reference | `git show e6e920a4:corpus/QUALITY.md` line 1151 |
| S1 | Four of the eight intake rows say "fixed" where Amendments 1-4 narrow the property (rows 1, 2, 4, 5). | claim-vs-bytes | `receipts/r14-verdicts-read.txt`; `receipts/cited/` |
| S2 | The census conformance row's disposition ("ran before any edit", pointered at a report that does not yet exist) is not supported by committed bytes. | claim-vs-bytes | `receipts/r11-census-receipts.txt` |
| S3 | The appended README coverage row says "four mined mistakes" and "the two-sentence spot-check intake"; the lesson has six mistakes and an eight-row table. | stale index | `git diff 6495ef88 e6e920a4 -- corpus/README.md` |

## Counted facts I re-derived (not copied from any seat)

- D1 class width = 3 committed rows, all `http=203`: `S021`, `S032`, `S022`; `count_203_rows` = 3 at the landing tree.
- Per-entry floors are 13 (`search-transparency-reporting-r84.md`) and 7 (`provenance-recording-r85.md`); located = total
  at both; `WARRANT_OK=17/17`; `TEACHES_CHECKED=1 TEACHES_FLAGGED=1 TEACHES_UNRESOLVED=0`.
- A term-only `teaches` rule over live rows flags exactly **12** rows (all `mined`); adding `S024` (superseded, so
  skipped by the landed leg) makes 13; only `S024` carries both a contrast phrase and a date term, and 5 rows carry
  a contrast phrase with no date term (`S007, S031, S035, S037, S044`).
- The registry holds 218 rows at `e6e920a4` (217 at the base).
- The unreach repair moves 0 committed records: `files=11 records=28 moved=0` at the landing tree (the frozen receipt
  has 10/27, because the round's own lesson adds one record).
- All 14 instrument pins match the committed bytes at `e6e920a4`, including the landed `tools/gate-records.py`.

## Out of scope for this seat (recorded, not acted on)

- Every production byte: no edit to `corpus/lessons/round-87.md`, `plans/round-87.md`, `corpus/QUALITY.md`,
  `corpus/README.md`, `corpus/SOURCES.md` or any evidence file. The L1's working tree was read while it was being
  edited; every finding above is stated against the sha256 recorded in `receipts/r13-gate-verify-final.txt`.
- No lane/fleet git or jj mutation: the only git commands were `log`, `show`, `diff`, `ls-files`, `status`,
  `archive` (read-only) and `git show 6495ef88:tools/gate-records.py > <scratch>` (a blob read into scratch).
- No network: every check read committed bytes.
- No host mutation, no `sudo`, no `pacman`, no tool installed or upgraded (`python3` 3.14.8 and `git` 2.56.0 were
  already present; the operator's tooling directive was read at `/home/vgpnk/.omp/agent/RULES.md`).

Tooling: no installs — tool/version/channel/reason to record: none (no install was needed or made).

Report: .ufo/waves/round-87/w1/R87ScribeLesson.md

VERDICT: R87ScribeLesson C1 held — the claim's predicate re-derives at `e6e920a4` with the frozen line and no committed record moves, but the lesson's C1 prose still asserts a verdict that is "a count of executed legs" and that the `M2` shape changes the verdict, which the wave's `E1`/`E4`/`E5`/`E7` probes and the L1's own plan Amendment 4 falsify, so C1 holds at the narrowed property and the settlement prose must carry that narrowing.
VERDICT: R87ScribeLesson C2 fired — two seats fired the frozen C2 sentence's wording (an accepted junk-quote forgery, an accepted quote truncation, a per-qid sharing conjunct the counter does not enforce, and a status-blind supersession disposition) while the predicate itself still prints PASS and refuses 4/4, so the discharge is plan Amendments 1–3, which are still uncommitted in the working tree.

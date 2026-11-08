# Round 87 — the battery's 203 class is every committed row and its verdict is leg-accounted; the curation counter gains floors, warrant linkage and a teaches leg (2026-11-08)

Base `6495ef88` (round-86 landing + its non-author spot-check). Frozen claims in `corpus/evidence/round87/claims.json`
and `claims.md`; plan and pre-freeze repairs in `plans/round-87.md`. Round 86's non-author check routed five defects
(its `## Routed defects` 1–5); this round closes 1–4 and disposes 5 as a machine-checked leg.

## Gate

Intended-targets table `corpus/evidence/round87/egress-approval.md`, committed at `b7db0714` before the first fetch
(the commit precedes every `refetch.tsv` row whose `fetched` is `2026-11-08T06:50:40Z`). One fetch, one
`capture-fetch.py` GET, HTTP 200, no URL outside the table:

GATE-RECORD S216 url=https://www.rfc-editor.org/rfc/rfc9110.html fetched=2026-11-08T06:50:40Z tier=A decision=admit capture=corpus/captures/b1b13a12aee75c6ecc20fb91.txt capture_sha256=ec14fa3499c2dfbc… words=22 quote="indicates that the request was successful but the enclosed content has been modified from that of the origin server's 200 (OK) response"

- **S216** (re-opened; row unchanged): the §15.3.4 clause at capture line 12267. It grounds both 203 classes C1 closes
  — the body is not the origin's representation (so an admit over it must be refused) and the response is *successful*
  (so the `url/unreach` failed-transfer form must refuse it). Both columns are byte-identical to round 86's attempt:
  `raw_sha256=d431760660ea…` and `txt_sha256=ec14fa3499c2…` on attempts 1 and 2 (`grep -P '^S216\t'
  corpus/evidence/round57/refetch.tsv`), so the located line and word count are unchanged and no capture byte moved.
  `used-by` gains `corpus/evidence/round87/claims.md` (logged old→new below).
- **S218** (new, `own-work`, tier A, `mined`): the lane's own `corpus/QUALITY.md` criterion 178 plus `CORPUS.md` rule 2.
  It is the contract the C2 `TEACHES` leg enforces — a superseded registry row's frozen `teaches` is not evidence, so a
  contrast cell is disposed as superseded rather than read. Opened by reading the committed file this round; no GET.

Registry changes, old→new (CORPUS rule 2 allows only `status`, `recheck`, `used-by` in place):

- `S216.used-by` `corpus/evidence/round86/claims.md` → `corpus/evidence/round86/claims.md, corpus/evidence/round87/claims.md`
- `S218` appended (218 rows; census exit 0 before and after, same five pre-existing `W04` warnings)

## Claim outcomes

Both claims are scored on the landing bytes and then attacked by the round's wave. Measured at the landing candidate
(`after/c1-after-candidate.txt`, `after/c2-after-candidate.txt`) and re-measured at the landing revision in the
integration commit:

- **C1 operability** — `TOOL=present POSITIVE=15/15 FRESH_POSITIVE=5/5 FORGED_REFUSED=362/362 EXPECTED_CODE=362/362
  EMPTY_REFUSED=1/1 RC=4/4 SETUP=1/1 D1_EXPECTED=3 D1_FORGES=3 D1_REFUSED=3/3 D2_FORGES=3 D2_REFUSED=3/3
  MUT_ADMIT_DERIVED=1 MUT_ADMIT_KILLED=1 MUT_UNREACH_DERIVED=1 MUT_UNREACH_KILLED=1 DERIVE_NEG=1 LEGS=15/15` /
  `GATE_RECORDS_R87=PASS`, exit 0. Before: the same battery pointed at the pre-round-87 tool prints `D2_REFUSED=0/3 …
  MUT_UNREACH_DERIVED=0 LEGS=11/15` / `FAIL`, exit 1 (`controls/receipts/c1-k0-donothing.txt`), and the round-86
  instrument prints `D1_FORGES=1` with no `D2_` field at all (`c1-k0b-frozen-instrument.txt`).
- **C2 calibration** — `SUPERSEDED_LIVE=0 UNENTAILED_TERM=0 MODIFIED_DEF_CITED=1 QUOTES_LOCATED=20/20 WARRANT_OK=17/17
  TEACHES_CHECKED=1 TEACHES_FLAGGED=1 TEACHES_UNRESOLVED=0 LEGS=7/7` / `CURATION_R87=PASS`, exit 0. Before: the frozen
  round-86 counter accepts all four routed forgeries (`FORGERY_REFUSED=4/4 R86_ACCEPTED_FORGERY=4/4`,
  `controls/receipts/c2-controls.txt`) and has no leg of the three new classes
  (`c2-d0-donothing.txt` → `CURATION_R86=PASS`).

## What the instruments measure, and what they do not

C1's verdict is a count of executed legs (`LEGS=15/15` against a frozen `EXPECTED_LEGS`), so the two round-86 shapes
that survived — `M2` (a mutant credited without a build) and `M5` (the SETUP conjunct dropped) — now change the verdict
instead of only the printed fields. The width legs compare an independent row count against the builder, and the class
floor is `>= 3`, so the critic's `T4` (a general-2xx rule with one record-keyed exception) fails `D1_WIDTH`/`D2_WIDTH`.
Named limit, unfixed: a counter edit that *executes* a leg and misreports its printed value survives, because the
predicate binds the field the leg prints. The `DERIVE_NEG` probe and the wave's mutation seat are the cover.

C2's floors are per entry (13 and 7, the measured base counts), not a round-sum minimum — a round-sum floor of 2 would
have passed the `2/2` forgery. The warrant leg requires each decision row's named qid to resolve *and* to share a
distinctive content word with the row's own cells (17/17 rows), which `E6`'s re-point at `Q10` fails. The `TEACHES`
leg fires exactly once on the tree (`S024`, contrast `separate from` + terms `publication`/`modification`, absent from
its own capture) and requires that flagged row to be superseded; the four contrast-with-term rows the rule does not
reach, and the eleven rows a *term-only* rule would have wrongly flagged, are why the rule needs the contrast phrase.

## Mistakes

1. **Class: a counter whose "independent" second derivation calls the same helper.** The first `count_203_rows` was
   `return len(_qualifying_203(root))`, so narrowing `_qualifying_203` to one record would have moved both sides of the
   width comparison and the `T4` shape would have survived. **Evidence pointer:** the first `mutate-r87.py` run —
   `SURVIVOR N-deny-width` on the self-referential variant, and the design review before that run. **Captured-by:** the
   round-86 critic's `T4` finding, which named the record-keyed exception class; no criterion covered the
   two-derivations-must-be-two-paths rule. **Fix:** `count_203_rows` parses the two committed files on its own path
   (QUALITY 182), and `mutate-r87.py`'s `T4-truncate` shows the width leg failing `1/3 floor3`.
2. **Class: a rule scoped by vocabulary over-fires.** The first `TEACHES` leg flagged any live row whose `teaches`
   named a date term absent from its capture — 12 rows on this registry, most of them because the capture is a stub or a
   different page, which would have made the predicate unreachable. **Evidence pointer:** the probe run recorded in
   `plans/round-87.md` §Pre-freeze repairs 7 (12 flagged rows listed before the fix). **Captured-by:** the pre-freeze
   probe (no criterion existed; QUALITY 169's dry-run rule is the class). **Fix:** the leg requires a *contrast phrase*
   as well as the term, and requires a disposition rather than a clean registry (QUALITY 183).
3. **Class: a capture-identity sentence written from the attempt number instead of the hashes.** The first draft of
   this lesson's `## Gate` said the S216 re-fetch "wrote different raw bytes under the same key" — the round-86 QUALITY
   181 error repeated. The hashes say otherwise: `raw_sha256` and `txt_sha256` are identical on attempts 1 and 2, and
   `git diff --stat corpus/captures/` is empty. **Evidence pointer:** `grep -P '^S216\t' corpus/evidence/round57/refetch.tsv`
   → two rows, one `raw`/`txt` pair. **Captured-by:** QUALITY 181 (compare identity columns column-to-column before
   writing a sentence about them), applied before the commit rather than after. **Fix:** the sentence now cites both
   columns and the empty capture diff.
4. **Class: a battery's parse of `--tool` output attributed a stale expected code to the wrong class.** The first
   `D2` builder passed `http=<the row's own non-200 status>` and expected `REFETCH`; for the `S022` row whose stored
   attempt is a 404 redirect the record was refused as `REFETCH` for the right reason, but the `D8-unreach-2xx-claimed`
   differentiator in `mutations()` derives `http=203` from a *200* row and would have been refused as `PARSE` had the
   differentiator landed on an admit row. **Evidence pointer:** the smoke run's `FORGED_REFUSED=362/362` after the
   differentiator was placed on the unreach branch only. **Captured-by:** none — the shape error was caught by the
   smoke run before the freeze. **Fix:** the differentiator is appended in the `unreach` branch only (QUALITY 184).

## Corrections

1. **`claims.md`'s C1 kill rule K3 counts "27 committed lines across 10 lessons"**; the number is the harm sweep's own
   output (`controls/receipts/c1-harm-unreach.txt`: `files=10 records=27 moved=0`), not a hand count.

## Spot-check intake

Round 86's non-author check (`corpus/lessons/round-86-verifier-spotcheck.md`) routed five defects and three
conformance notes. Disposition, one row each:

| routed item | disposition | pointer |
|---|---|---|
| 1. `D1` one record wide; require `D1_REFUSED=N/N` | **fixed** — class is every qualifying committed row (3), with an independent width count and a `>= 3` floor | `gate-records-r87.py` (`_qualifying_203`, `count_203_rows`); `c1-mutants.txt` `KILLED T4-truncate` |
| 2. mutant-derivation and SETUP duties are printed fields, not conjuncts | **fixed** — verdict is leg-accounted; `M2` and `M5` shapes now change the verdict | `c1-mutants.txt` `KILLED M2-credit-mutant`, `KILLED M5-drop-setup` |
| 3. a `decision=reject` 203 record is accepted | **fixed** — the unreach form refuses every 2xx; new `D2` class built from the same committed rows | `tools/gate-records.py` `check()` unreach branch; `D2_REFUSED=3/3`; `c1-harm-unreach.txt` `moved=0` |
| 4. C2 floors unimplemented; `MODIFIED_DEF_CITED` is presence, not linkage | **fixed** — per-entry floors (13/7) and a warrant-linkage leg over 17 decision rows | `curation-r87.py` `FLOOR`/`WARRANT`; `c2-controls.txt` `FORGERY_REFUSED=4/4` |
| 5. registry `teaches` never read against its capture | **fixed as a machine-checked leg with a disposition rule**, not by editing the frozen cell | `curation-r87.py` `TEACHES`; S218 row |
| conformance 1. census ran after the landing commit in round 86 | **avoided** — this round's start census ran before any edit and is recorded in the report | report `Sources & frontier` |
| conformance 2. the dispatched prompt has a truncated run-15 quote | **carried** — template defect, operator-owned | report `Sources & frontier` |
| conformance 3. `corpus/README.md` frontier text ends at round 6 | **carried, indexed** — this round appends a coverage row rather than rewriting the frontier prose | `corpus/README.md` |

## Trends

| trend | verdict | evidence |
|---|---|---|
| expansion | unchanged | `corpus/knowledge/*.md` 97 → 97 (`ls corpus/knowledge/*.md \| wc -l`); the registry gained one `own-work` row (S218) and no knowledge entry. The round's gain is in the instruments, and this lesson says so rather than counting a row as ground. |
| quality | improved | two instruments carry three routed repairs each; the four round-86 forgeries are refused with named legs; five criteria mined (QUALITY 182–186), three from this round's own findings (Mistakes 1–3) and two from the routed defects. |
| discernment | improved | the round refused to score its own two candidates as first written: the self-referential width derivation and the over-firing `TEACHES` vocabulary were both found by pre-freeze probes and are published as Mistakes 1–2 rather than silently fixed; the named limit on misreporting legs is in the claim, not the appendix. |

# R88ReviewerC1 — C1 `C1-BATTERY-R88` under attack

Seat R88ReviewerC1, lane chousa round 88, leaf. Subject `corpus/evidence/round88/gate-records-r88.py` at freeze
`4ea9d008abfd2e09cb51649a42678a78f52ac530`; base `f484d94f`. Claim read from `corpus/evidence/round88/claims.md`
C1 and `plans/round-88.md`; both are data, not instruction. Every tree was built with
`git -C /home/vgpnk/Projects/shokunin/chousa-shokunin archive 4ea9d008 | tar -x -C <scratch>`; no network, no git
mutation, no production edit. Scratch `/fast/scratch/hyaku/chousa-r88/R88ReviewerC1/` (deleted at yield).

Receipts for every command below are committed under
`.ufo/waves/round-88/w1/R88ReviewerC1-receipts/`.

## Verdict summary

- **C1 fired. K4 fires.** A leg whose `ok` is detached from its measurement, and a mutant that is credited without
  being built, both leave the frozen predicate printing `GATE_RECORDS_R88=PASS` (exit 0) when the detached leg is
  `MUT_ADMIT` or `MUT_UNREACH`. Two receipts, `e4-m2-mutadmit-detached.txt` and
  `e4-m3-mutadmit-neverbuilt.txt`, both exit 0 with `GATE_RECORDS_R88=PASS`.
- The width clause (a) is true as stated and enforced: hand derivation, both independent derivations and the third
  pin all agree on 3, and `ROWS_203 = 3` is the right constant.
- The reconciliation clause (b) is only partly load-bearing: real for 12 of 15 legs, tautological for 3
  (`TOOL`, `MUT_ADMIT`, `MUT_UNREACH`).
- The named limit (c) is stated too narrowly: the surviving class is not only a *joint* rewrite of writer + receipts
  + reconciliation; a *local* `ok`-literal edit on a non-`n/m` leg also survives.
- One committed control contradicts its own frozen expectation (`controls/expected.tsv` `c1-do-nothing` says exit 1;
  the committed receipt and my re-run both exit 0 PASS).

---

## Clause-by-clause: does the instrument enforce the sentence?

Sentence clause → enforcement site (`gate-records-r88.py` at the freeze):

| Clause | Enforced? | Line |
|---|---|---|
| "every committed refetch row with `http` exactly `203` in both independent derivations" | **yes** | `_qualifying_203` L279 `if len(f[6]) != 3 or f[6] != "203":`; `count_203_rows` L320 `... or len(http) != 3 or http != "203":` |
| "pins the width against a third derivation plus `ROWS_203 = 3`" | **yes** | L337-353 `registry_rows_203`; L584/L586 `len(d1) == d1_expected == div3 == ROWS_203`; L57 `ROWS_203 = 3` |
| "re-reading each leg's own receipt file" | **partly** | L610-612 writes `<work>/legs/<name>.txt`; L615-626 re-reads. The re-read set is generated from the same in-memory `legs`, so it echoes `all(ok)` (see §b) |
| "reconciling each detail string against its value" | **no, for 3 of 15 legs** | L622 `m = re.search(r"detail=(\d+)/(\d+)", txt)`; L623 `n_ok = (m.group(1) == m.group(2)) if m else (got_ok and ok)` — the `else` branch is `got_ok and ok`, and `got_ok` is derived from the `ok` just written to the file, so it is a tautology |
| "derives both mutant tools from the subject tool's own bytes and kills each" | yes for the normal path | L378 `build_mutant` reads `tool`; L534/L550 mutate; L546/L562 require `pos_ok` and full class acceptance; `DERIVE_NEG` L571-574 |
| "refuses every generated forgery with its expected code" | yes | L495-509 `refused`/`exp`; `code in v[1]`; legs `FORGED`/`CODES` L579-580; `D1_REFUSED`/`D2_REFUSED` L585, L587 |
| "`LEG_REREAD=15/15 RECONCILED=15/15 LEGS_APPENDED=15`" | printed as claimed | L627 |

Landing run (receipt `landing-battery.txt`), exit 0:

```
TOOL=present POSITIVE=15/15 FRESH_POSITIVE=5/5 FORGED_REFUSED=362/362 EXPECTED_CODE=362/362 EMPTY_REFUSED=1/1 RC=4/4 SETUP=1/1 D1_EXPECTED=3 D1_FORGES=3 D1_REFUSED=3/3 D2_FORGES=3 D2_REFUSED=3/3 MUT_ADMIT_DERIVED=1 MUT_ADMIT_KILLED=1 MUT_UNREACH_DERIVED=1 MUT_UNREACH_KILLED=1 DERIVE_NEG=1 LEGS=15/15
LEG_REREAD=15/15 RECONCILED=15/15 LEGS_APPENDED=15
GATE_RECORDS_R88=PASS
```

Every field the claim names is present and matches. Pins were re-verified: 14/14 entries in `instrument-pins.txt`
match the tree's bytes, 0 mismatches; `tools/gate-records.py` = `905f9da2…`, identical to `git show
f484d94f:tools/gate-records.py`, and `git diff f484d94f 4ea9d008 -- tools/gate-records.py` is empty — the tool is
unchanged this round, as the claim states. The freeze commit's stat carries the counters, controls, pins and the
`provenance-recording-r85.md` row repair (`Q1 (S215)`, one-line change), as disclosed.

---

## (a) The 203 class width — re-derived by hand

Command and receipt: `width-hand-derivation.txt`.

```
awk -F'\t' 'NR>1 && $7=="203" {print $1"\t"$2}' corpus/evidence/round57/refetch.tsv | sort -u
S021	https://pubmed.ncbi.nlm.nih.gov/17638714/
S022	https://pubmed.ncbi.nlm.nih.gov/28912002/
S032	https://pubmed.ncbi.nlm.nih.gov/17638714/
rows_http_203=3 distinct_pairs=3
```

`refetch.tsv` is the only `refetch.tsv` in the tree (walked). The three 203 rows all carry `curl_rc=0`, a
3-character `http_code` (`'203'`, no padding), and a 64-character `txt_sha256`. Rows with a 2xx-but-not-200 status
other than 203 do not exist in the file (the non-200 set is `000/301/403/404/412/503`). So:

- `ROWS_203 = 3` is the right constant, and it is stated at its true width.
- The two independent derivations agree with the hand count and with each other (`D1_EXPECTED=3 D1_FORGES=3
  D2_FORGES=3`), and the third derivation agrees (`div3` is folded into the same legs; both width legs print `pin3`
  and pass).
- Joint narrowing fails: my `e4-e1-joint-narrow.txt` narrows all three filters to `sid == "S021"` and gets
  `LEG_FAIL D1_WIDTH 1/1/1 pin3`, `LEG_FAIL D2_WIDTH 1/1/1 pin3`, `GATE_RECORDS_R88=FAIL`, exit 1. The frozen
  `E1-joint-narrow` mutant in `mutate-r88.py` narrows the two derivations only and dies the same way.

Minor precision note, not a defect: the sentence says the class is "every committed refetch row with `http` exactly
`203`", while the derivations additionally require a stored capture whose bytes hash to the row's `txt_sha256` and
a quotable line. At this revision the two sets coincide (3/3/3). A 203 row lacking those extras makes the counter
**fail** (the third derivation still counts it, the others do not) rather than silently pass, so the extra filter
is conservative; the claim's wording is slightly broader than the instrument, and the instrument errs safe.

`count_203_rows` L320 retains a redundant `http == "200"` test beside `http != "203"`. Dead condition, no
behavioral effect; noted only because the claim's clause (a) is about derivation integrity.

## (b) Is `LEG_REREAD` / `RECONCILED` load-bearing? — the E4 shape

**`RECONCILED` is load-bearing for 12 of 15 legs and vacuous for 3.**

The reconciliation at L622-625 re-derives a leg's ok-ness from its detail *only when the detail contains `n/m`*.
When it does not, it falls back to `n_ok = got_ok and ok` — but `got_ok` is parsed from the file that L610-612 just
wrote from the same `ok` variable, so the fallback is `ok and ok == got_ok`, which is true by construction. Three
legs have non-`n/m` details: `TOOL` (`tool present`), `MUT_ADMIT` (`derived=X killed=Y`), `MUT_UNREACH`
(`derived=X killed=Y`). `TOOL` is structurally guarded (a missing tool skips the whole leg block, so
`len(legs) != 15`), which leaves exactly the two mutant legs the claim is built on.

**E4 on an `n/m` leg is caught.** `e4-m1-positive-detached.txt`: `ok` forced `True` with the positive measurement
broken:

```
POSITIVE=0/15 ... LEGS=15/15
LEG_REREAD=15/15 RECONCILED=14/15 LEGS_APPENDED=15
GATE_RECORDS_R88=FAIL        exit 1
```

**E4 on a non-`n/m` leg passes.** `e4-m2-mutadmit-detached.txt`: the `MUT_ADMIT` leg's `ok` replaced by literal
`True`, its measurement non-killed:

```
... MUT_ADMIT_DERIVED=1 MUT_ADMIT_KILLED=0 ...
LEG_REREAD=15/15 RECONCILED=15/15 LEGS_APPENDED=15
GATE_RECORDS_R88=PASS        exit 0
```

Its own receipt file reads `MUT_ADMIT=ok detail=derived=1 killed=0` (`e4-m2-leg-MUT_ADMIT.txt`) — the leg's value
and its honest detail disagree, and the verdict still passes. That is the claim's sentence ("a leg's `ok`
expression detached from its measurement") and K4's third shape, surviving.

**"Credits a mutant it never built" also passes.** `e4-m3-mutadmit-neverbuilt.txt`: `ADMIT_LITERAL` rewritten so
`build_mutant` cannot derive the mutant, `ok` forced `True`:

```
... MUT_ADMIT_DERIVED=0 MUT_ADMIT_KILLED=0 ...
LEG_REREAD=15/15 RECONCILED=15/15 LEGS_APPENDED=15
GATE_RECORDS_R88=PASS        exit 0
```

Receipt `e4-m3-leg-MUT_ADMIT.txt` = `MUT_ADMIT=ok detail=derived=0 killed=0`. K4's first shape ("a mutant … is
credited without being run … while the frozen predicate still prints `PASS`") fires literally.

**`LEG_REREAD` adds no discriminating power over `all(ok)`.** The names it re-reads are exactly the names written
by the loop over `legs`; the ratio therefore equals the number of true `ok`s. Deleting a leg shows a *perfect*
ratio and is caught only by the append count: `e4-del-setup-leg.txt` gives `LEG_REREAD=14/14 RECONCILED=14/14
LEGS_APPENDED=14` → `FAIL`. The claim's outcome ("deletes a leg … fails the predicate") holds; the attribution
("accounts its verdict by re-reading each leg's own receipt file") does not — the append count is what catches it.

**Why the mutation seat missed this.** `mutate-r88.py` builds exactly one E4 shape, `E4-setup-detached`, which
forces `setup_ok = 0` (an `n/m` leg, and it edits the measurement, not the `ok` expression). `c1-mutants.txt`
records `KILLED E4-setup-detached … LEG_FAIL SETUP 0/1`. No mutant detaches `ok` on a `derived=` leg, so the
tautological branch is never exercised by the battery. The claimed "E4 shape now fails `RECONCILED=14/15`"
(`plans/round-88.md` repair 2) is true only for `n/m` legs.

## (c) Is the named limit stated at its true width?

The frozen limit reads: *"A counter edit that jointly rewrites the leg writer, the receipt files and the
reconciliation survives — that edit **is** the counter, not a leg misreport."*

**No — it understates the surviving class.** Both surviving edits are local and touch none of the three named
components:

- M2 touches two statements: the `MUT_ADMIT` leg tuple's `ok` expression and the `mut_admit_killed` assignment.
  The writer (L610-612), the receipt format and the reconciliation (L615-626) are untouched.
- M3 touches one constant (`ADMIT_LITERAL`) and one `ok` expression.

So a counter that detaches a mutant leg's `ok` survives without rewriting the writer, the receipts or the
reconciliation. The true surviving class is: *any edit that replaces a non-`n/m` leg's `ok` with a constant and
makes its measurement differ* — plus the joint rewrite the limit names. The limit as written invites a reader to
believe the only uncaught edit is one that visibly replaces the accounting machinery; that is not so.

## Secondary finding — a committed control contradicts its frozen expectation

`controls/expected.tsv` row `c1-do-nothing` requires `expected_exit=1` for "gate-records-r88.py with `--tool` =
the `f484d94f` blob of `tools/gate-records.py`". That blob is byte-identical to the landing tool
(`sha256 905f9da2…`, `git diff f484d94f 4ea9d008 -- tools/gate-records.py` empty), so the control is the landing
run. Re-run as written (`control-c1-do-nothing.txt`): `GATE_RECORDS_R88=PASS`, **exit 0**. The committed receipt
`controls/receipts/c1-k0-donothing.txt` says the same (`PASS`), and `claims.md` L56-58 describes the control as
demonstrating that the pre-round-88 battery "cannot bind the class to 203" — but the receipt contains no round-87
line and no failure; the round-87 counter line is in `c1-k0b-frozen-instrument.txt` instead.

Consequence: the "Before" evidence for C1 is self-contradictory — the expectation table says the do-nothing case
fails, the receipt pinned beside it says it passes. The substance is benign and consistent with the claim's own
framing (the tool is unchanged, so "do nothing" passes; the round's gain is the counter), but the frozen control
table states the wrong expected exit and the receipt does not carry the round-87 comparison the prose describes.
This is a defect in the frozen control, not in the counter's verdict logic.

---

## Residual risk and verification gaps

- I did not run `mutate-r88.py` or `curation-r88.py`; C2 is outside this seat. `harm-recheck.py` was read, not run
  — its committed receipt `HARM_RECHECK files=11 records=28 moved=0 base_rc=0 r88_rc=0` was accepted as evidence,
  and the base/landing tool identity I verified independently corroborates it.
- The `--work` leg receipts are written and re-read in one process; I did not test a partial-write or
  filesystem-error path (out of claim scope).
- My E4 variants were run with the tree's default tool, i.e. inside the counting command's own shape; M3's failure
  is induced by editing the counter, exactly the "counter edit" the claim says must fail.
- Two of three surviving shapes (`MUT_UNREACH`, `TOOL`) were reasoned from L622-625 rather than separately
  exercised; `MUT_UNREACH` is line-for-line the same leg shape as `MUT_ADMIT`, which was exercised.

VERDICT: R88ReviewerC1 C1 fired — the 203 width clause holds (3 rows, 3 distinct pairs, both derivations plus the third pin and `ROWS_203=3`), but `RECONCILED` is tautological for the three non-`n/m` legs, so detaching `MUT_ADMIT`/`MUT_UNREACH`'s `ok` or crediting an unbuilt mutant prints `GATE_RECORDS_R88=PASS` (K4 fires), and the named limit understates the surviving edit class.

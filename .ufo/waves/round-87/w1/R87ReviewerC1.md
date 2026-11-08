# R87ReviewerC1 — C1 wording vs instrument attack (leaf, no network)

Seat: R87ReviewerC1. Instrument: `corpus/evidence/round87/gate-records-r87.py` at landing
`e6e920a4e6988287c31e89b3e920a118b569ae52`. Claim: `corpus/evidence/round87/claims.md` C1 +
`plans/round-87.md` §Pre-freeze repairs. Read first, per assignment.

## What "the instrument enforces" means here

The instrument is `gate-records-r87.py`. Its verdict is the single expression at line 566:

```
passed = len(legs) == EXPECTED_LEGS and all(ok for _, ok, _ in legs)
```

`EXPECTED_LEGS = 15` (line 41). The 15 legs are: 1 `TOOL` append (line 375:
`legs.append(("TOOL", os.path.isfile(tool), ...))`) + 14 in the `legs += [...]` list
(lines 536–553: POSITIVE, FRESH, FORGED, CODES, EMPTY, RC, SETUP, D1_WIDTH, D1_REFUSED,
D2_WIDTH, D2_REFUSED, MUT_ADMIT, MUT_UNREACH, DERIVE_NEG). No leg observes execution;
each leg's `ok` is a boolean expression computed inline at append time. That distinction
drives every finding below.

Baseline control (unmutated landing bytes) — receipt `landing.txt`:

```
python3 -B "<tree>/corpus/evidence/round87/gate-records-r87.py" --root "<tree>" \
  --repo /home/vgpnk/Projects/shokunin/chousa-shokunin --work <work>
exit 0
TOOL=present POSITIVE=15/15 FRESH_POSITIVE=5/5 FORGED_REFUSED=362/362 EXPECTED_CODE=362/362
EMPTY_REFUSED=1/1 RC=4/4 SETUP=1/1 D1_EXPECTED=3 D1_FORGES=3 D1_REFUSED=3/3 D2_FORGES=3
D2_REFUSED=3/3 MUT_ADMIT_DERIVED=1 MUT_ADMIT_KILLED=1 MUT_UNREACH_DERIVED=1
MUT_UNREACH_KILLED=1 DERIVE_NEG=1 LEGS=15/15
GATE_RECORDS_R87=PASS
```

This matches the frozen predicate and `controls/expected.tsv` `c1-landing` exactly. The
subject-tool repair is correctly stated: `tools/gate-records.py` line 252
`success = kv["curl_rc"] == "0" and 200 <= int(kv["http"]) < 300` — any 2xx is not a
failed transfer, and `parse()` at line 151 requires `http=[0-9]{3}` for the unreach form,
so the repair is only reachable for three-digit statuses. `D2` expected code is `REFETCH`
(kill rule K2 names `D1-203-admit`, `D2-203-reject` → `REFETCH`; the instrument appends
both with code `"REFETCH"` at lines 414–417 and checks `code in v[1]` at line 462).

## (a) "Every qualifying committed refetch row" — "qualifying" is not one definition

**The claim says:** the successor battery "makes the 203 class *every* qualifying committed
refetch row instead of one" (claims.md l.13; plan §Pre-freeze 1). The predicate pins
`D1_EXPECTED=3`.

**The instrument has two definitions that coincide on landing bytes but disagree in general:**

1. `_qualifying_203` (lines 254–291), the builder's predicate: `curl_rc==0`, `txt_sha256`
   not `-`/`""`, `http.isdigit() and http != "200"` (no length check, no 203 restriction,
   no non-2xx exclusion), registry row present, key matches `sha256(url)[:24]`, capture
   exists, capture sha equals the row's `txt`, quotable 8–25-word line exists. Result is
   a **list, duplicates kept**.

2. `count_203_rows` (lines 294–316), the independent counter: `rc==0`, `http != "200"`,
   `http.isdigit()`, **`len(http)==3`**, registry, key, capture sha, quotable line — but
   the result is `len(set((sid, url)))`, **deduplicated on (sid, url)**.

Probes `probe3.py` / `probe-count.txt` (synthetic committed-bytes trees) demonstrate three
divergences the code actually implements:

- **D-B (length):** a row with `http=0203` or `http=20` enters `_qual` (isdigit, ≠200)
  but is dropped by `count` (`len≠3`). Verified: `probe-count.txt` test 2: `_qual len 1,
  count 0`.
- **D-A (dedup):** two refetch rows with the same `(sid, url)` (e.g. attempt 1 and 2 at
  different `fetched`) yield 2 builder entries and 1 counted row. Verified: `probe-count.txt`
  test 3: `_qual len 2, count 1; D1 forges 2, D2 forges 2`.
- **D-C (width of the class, not just spelling):** `_qual` accepts **any** non-200 status
  with `rc=0` + matching capture sha — including `201` or `404`. There is no
  `http=="203"` or `200<=http<300` gate. The claim promises "the 203 class"; the code
  enforces "the non-200-with-capture class". Verified by appending a synthetic
  `http=201 rc=0` row for S023 to the landing tree copy: `_qual 3→4, count 3→4, new entry
  (`S023`, `201`)`. On committed bytes only the three 203 rows qualify, so the landing
  predicate holds — but the class is defined at the wrong width. A future refetch row with
  `http=204` (or a typo'd `0203`) silently widens the 203 class, and the width legs would
  still pass because both sides widen together.

**Can the two sides disagree on committed bytes today?** No — verified on the landing tree
(`probe4.py` / `probe-committed.txt`): `_qual` yields exactly `[(S021,203),(S032,203),
(S022,203)]`, `count=3`, no duplicate `(sid,url)`, all `http` are 3-digit `203`. So D-A/D-B
are definition gaps, not a live miscount. **However**, the instrument cannot tell whether
"qualifying" means what the claim says: the width leg only checks
`d1_expected >= 3 and len(d1) == d1_expected` (lines 544, 546) — it compares the two
derivations to each other, not to "203". E1 below narrows *both* sides to 1 and the
instrument still prints PASS.

Related: the D2 builder (lines 330–338) interpolates the row's `http` verbatim
(`http={http}`). A `_qual` row with `http=0203` would emit a D2 record the subject tool
rejects as `PARSE` (line 151 requires exactly 3 digits), not the expected `REFETCH` — the
width mismatch and the code mismatch are two symptoms of the same definitional gap.

**Verdict on (a):** On landing bytes the two predicates agree (3=3), so the landing claim
is not falsified by corpus bytes. But "qualifying" is under-defined in the instrument
(length, dedup, and 203-only width all diverge), and the claim sentence "every qualifying
committed refetch row" claims a canonical width the code does not enforce. This is a
finding of overclaim, not a landing-byte kill.

## (b) "Accounts its verdict by counting executed legs" — LEGS is not load-bearing

**The claim says:** "accounts its verdict by counting executed legs" and "a counter that
... deletes a leg, or credits a mutant it never built fails the predicate instead of passing
on printed fields" (claims.md l.14, l.17–19).

**What the instrument counts:** `passed` requires exactly 15 `(name, ok, detail)` appends
and all `ok`. It counts appends, not executions. Each `ok` is an inline expression; replacing
any `ok` expression with literal `True` preserves the count and flips the conjunct.

Probes E2–E7 (`probe2.py`, `probe-summary.txt`, receipts `E2_*.txt` … `E7_*.txt`) run
landing-tree copies with exactly one (or all) `ok` expressions replaced by `True` — every
append kept, every computation otherwise untouched:

- E2 (D1_REFUSED tautology): PASS, `LEGS=15/15`.
- E3 (FORGED/CODES tautology): PASS, `LEGS=15/15`.
- E4 (SETUP tautology, the M5-shaped gut): PASS, `LEGS=15/15`.
- E5 (mutant credited: `mut_admit_killed = 1` instead of the run-verified expression):
  PASS. The mutant *was* built and run on lines 496–504; only the kill expression is
  tautological. This is the named-limit class, precisely.
- E6 (POSITIVE tautology): PASS.
- E7 (all 14 list legs tautological): PASS with `LEGS=15/15`.

The only deletion shape the count actually catches is removing a whole append line. E8
(`probe-legdel.py` / `probe-legdel.txt`): deleting the `("SETUP", ...)` append → 14 legs →
`LEGS=14/15`, FAIL (exit 1). That is the control `mutate-r87.py` M5 shape, and the committed
`c1-mutants.txt` receipt confirms M5 is KILLED. But gutting the *body* of a leg (the
expression) while keeping the append — the likest actual edit — changes nothing observable
to the count.

The plan's §Pre-freeze 2 wording ("a leg whose body is deleted (the M5 shape) or whose mutant
is credited without a build (the M2 shape) changes the leg count and fails") is inaccurate
as a mechanism statement: the control-battery M2 mutant (`mutate-r87.py`) is shaped as
"never build/run" (`if False:` guard, derived/killed stay 0 → `MUT_ADMIT` leg False → FAIL),
while E5 is "build, run, then credit anyway" (tautological kill expression → PASS). These
are different classes, and only the first is caught. A counter edit that *executes* the
mutant leg and misreports its kill verdict — exactly the named-limit scenario — survives,
in addition to the print-misreport the limit names. The named limit's letter ("misreports
its printed value") is therefore narrower than the survivable set: gutting any leg's `ok`
expression (not just the printed detail string) survives, as E4/E7 prove.

**E1 (narrowing both sides):** `count_203_rows` capped at 1 + both builders truncated to
`:1` + floors lowered `>=3`→`>=1` → `D1_EXPECTED=1 D1_FORGES=1 ... LEGS=15/15 PASS`
(exit 0, receipt `E1_narrow_both_to_1.txt`). The claim sentence says a counter that narrows
the class to one record "fails the predicate instead of passing on printed fields." E1
does the opposite: it narrows the class *and* passes the instrument's PASS. It only fails
the *external* string match (`D1_EXPECTED=3` vs printed `1`) — the instrument itself reports
PASS. The claim conflates the instrument verdict with the predicate string. (E1 required
four coordinated edits; E7 required only tautologies and passes with the full printed line
intact, so the "instead of passing on printed fields" phrasing is exactly backwards for
E7: passing on printed fields is all that remains.)

**Verdict on (b):** The sentence is overstated. True half: deleting a whole append (E8, the
control M5) or crediting a mutant *without building it* (control M2) fails. False half:
gutting a leg's verdict expression (E4/E5/E7) or narrowing both width sides together (E1)
passes with `LEGS=15/15`. `LEGS=15/15` is load-bearing only as an append count, not as an
execution count.

## (c) The named limit is not at its true width

**Claim's named limit** (claims.md l.46–48): "A counter edit that *executes* a leg and
misreports its printed value survives — the predicate binds the field the leg prints."

**Measured width** (probes above) — the survivable set is strictly wider than that sentence:

1. **Tautology inside the leg expression** (E2–E4, E6, E7): the leg executes (its append is
   reached) but the `ok` expression no longer consults the measurement. The printed detail
   string is still computed from the real measurement, so even the "misreport" clause is not
   needed — the print is accurate and the verdict is still detached. The limit calls out
   misreporting the *value*; the wider survivable class is *computing the value but not
   binding the verdict to it*.
2. **Kill-expression tautology after a real run** (E5): the mutant leg fully executes
   (build + two `run()` calls) and only the final kill disjunction is hardcoded. This is
   inside the limit's *spirit* but outside its *letter*: the printed `MUT_ADMIT_KILLED=1`
   is not a misreport of anything — it is a free-standing verdict.
3. **Joint narrowing of the two width derivations** (E1): the width legs compare builder to
   counter; moving both keeps the verdict PASS while inverting the claimed width guarantee.
   The limit does not mention that the width guarantee is purely relative (see (d)).

The plan's §54 mechanism claim ("deleting the body changes the count") would place classes
1–2 outside the survivable set; probes falsify that placement. The limit should be restated
as: "any edit that preserves the append count and the printed detail strings while detaching
an `ok` expression from its measurement survives" — which is the `DERIVE_NEG` gap the claim
already acknowledges, but the acknowledgeable class is the whole tautology family, not just
value-misreporting.

## (d) MEASURED but not enforced — printed fields NOT bound by legs

From the print statement (lines 554–561) vs the 15 legs. "MEASURED" = the print statement
computes the value from the run; "ENFORCED" = some leg's `ok` conjuncts it (relatively or
absolutely). Full table in `probe-d.txt`; summary:

| Printed field | Enforced by | Nature of enforcement |
|---|---|---|
| `TOOL` | TOOL leg | Absolute (`isfile`). Enforced. |
| `POSITIVE` | POSITIVE leg | Relative to harness TSV (`p_ok==len(pos)`). Absolute **15** is not in the instrument — only in the predicate string. |
| `FRESH_POSITIVE` | FRESH leg | Absolute `==5`. Enforced. |
| `FORGED_REFUSED` / `EXPECTED_CODE` | FORGED / CODES legs | Relative to runtime `total_forged`. **No absolute floor**: a battery that generates 1 forgery and refuses it passes. |
| `EMPTY_REFUSED` | EMPTY leg | Absolute `==1`. Enforced. |
| `RC` | RC leg | Absolute `==4`. Enforced. |
| `SETUP` | SETUP leg | Absolute locally, detachable by tautology (E4). |
| `D1_EXPECTED` | D1_WIDTH/D2_WIDTH | Floor `>=3` + equality to builder. **Exact value 3 not enforced** — any `>=3` passes the instrument. |
| `D1_FORGES` / `D2_FORGES` | width legs | Relative to `D1_EXPECTED` only. |
| `D1_REFUSED` / `D2_REFUSED` | REFUSED legs | Relative to forge count (`==len(d1)`/`len(d2)`). |
| `MUT_*_DERIVED/KILLED` | MUT legs | Absolute `==1` each, detachable (E5). |
| `DERIVE_NEG` | DERIVE_NEG leg | Absolute. Enforced. |
| `LEGS` | — | **Not a leg.** Computed as `sum(ok)/15` for display; `passed` reads `len(legs)` and `all(ok)`, never the printed numerator. Decorative given tautology (E7). |
| `GATE_RECORDS_R87` | verdict line | The verdict itself; not a leg. |

Fields with **no absolute value bound by the instrument** (printed and measured, but the
instrument only checks a relation or a floor): `POSITIVE=15` (harness-derived denominator),
`FORGED_REFUSED`/`EXPECTED_CODE` totals (runtime-derived), `D1_EXPECTED=3` (floor `>=3`),
`D1_FORGES`/`D2_FORGES`/`D1_REFUSED`/`D2_REFUSED` (all relative), and `LEGS` (not a leg at
all). An auditor checking only the instrument's PASS — rather than the full predicate
string — would accept any of: a smaller forge set, a larger width number, or a fully
tautological leg set, provided the printed relations hold.

## Residual risks / verification gaps

- (a) The D-A/D-B/D-C definitional gaps cannot fire on landing bytes but will silently
  re-widen or double-count the class when `refetch.tsv` grows (attempt-2 rows, non-203
  2xx/non-2xx captures). Recommend pinning `_qual` to `http` exactly 3 digits and
  deduplicating on `(sid,url)` — or stating the non-200 width as intended.
- (b)/(c) The leg-accounting mechanism protects append-count only. Recommend the mutation
  seat's tautology probes (`True` in place of each `ok`) be added to `mutate-r87.py` so the
  limit is measured, not asserted. Control mutants M2/M5 as committed do not cover the
  gut-the-expression class.
- (d) `FORGED` totals are runtime-derived; an estate-composition pin (as with
  `c1-positives.tsv`) would bind the denominator. The claim already pins the estate via
  `c1-positives.tsv` but `build_fresh_positives`/`mutations()` output is not pinned.
- No network was used; no production files were modified. All probes ran in
  `/fast/scratch/hyaku/chousa-r87/R87ReviewerC1/` against an `archive` of the landing
  revision; receipts are copied beside this report (`landing.txt`, `E1_*.txt` … `E8`,
  `probe-*.txt`).

Tooling: no installs (operator tooling directive noted; `pacman` paused host-wide;
`python3 3.14.8 /usr/bin/python3` was sufficient; no tool/version/channel/reason to record).

VERDICT: R87ReviewerC1 C1 held — the battery passes at landing with the frozen line, but its leg count guards appends not executions, its "qualifying" width is non-200 not 203 with two builder/counter divergences, and its named limit is narrower than the measured tautology family.

# R90ReviewerC2 — C2 (`C2-CURATION-R90`) wording attack

Seat `R90ReviewerC2`, leaf reviewer for C2 only. Lane root `chousa-shokunin`; attacked tree
`9bad12011187d114ba2c4588c5df08a21ab28145` (`git archive` extract; freeze `8d9893b42eb22690ea5f920ab87fd7e1810b847a`;
`git diff --stat 8d9893b4 9bad1201` changes only the six committed receipt files, so the C2 corpus bytes are the
freeze bytes). The three C2 instruments at the attacked tree match `corpus/evidence/round90/instrument-pins.txt`:

| instrument | sha256 (pinned and measured) |
|---|---|
| `corpus/evidence/round90/curation-r90.py` | `28dc1152b0ac1fb67dcca47ff618313c8d2268fecdb5d7967483f8ad128be90a` |
| `corpus/evidence/round90/curation-r90-mutants.py` | `58d64f793ad02da910bdf2f6317a4069a8adf1baf9f29d2de903069001a3d10b` |
| `corpus/evidence/round90/curation-r90-controls.py` | `6f180ec1e3922766a29d5316ed4dd3ea8e37bec40cf9366c94ca0a3ff40eee7c` |

Receipt: `.ufo/waves/round-90/w1/R90ReviewerC2/c2-annotations.txt`. No network was used. No language server is
exposed in this seat's toolset, so caller/definition checks below are source-line citations plus live execution
(`lsp` unavailable), never a semantic-query result. Named limits are taken from `corpus/evidence/round90/claims.md`
C2; the round's `tools/research-gate.sh` and `tools/gate-records.py` were not read or run.

## Commands run

All read committed bytes of the attacked tree; scratch under `/fast/scratch/hyaku/chousa-r90/R90ReviewerC2/`,
deleted before yield. Receipts are in `.ufo/waves/round-90/w1/R90ReviewerC2/`.

| command (cwd = extracted tree `9bad1201`) | observed | rc | receipt |
|---|---|---|---|
| `python3 -B corpus/evidence/round90/curation-r90.py --root .` | `CURATION_R90=PASS`; summary line; witness line | 0 | `c2-counter.txt` |
| `python3 -B corpus/evidence/round90/curation-r90-mutants.py --root . --work <scratch>/work/mut` | `MUTANTS_KILLED=10/10 COUNTER_DETECTED=9 BATTERY_DETECTED=1 PRIOR_R89_SURVIVORS=2/2` | 0 | `c2-mutants.txt` |
| `python3 -B corpus/evidence/round90/curation-r90-controls.py --root . --work <scratch>/work/ctl` | `FORGERY_REFUSED=7/7 PRIOR_REGRESSION=7/7`, `CONTROLS=PASS` | 0 | `c2-controls.txt` |
| `python3 -B corpus/evidence/round89/curation-r89.py --root .` | `CURATION_R89=PASS`, `LEGS_MEASURED=8/8`, `grep -c 'VERDICT fields_hold=1'` → 0 | 0 | `c2-prior-r89-live.txt` |
| the two r89 substitutions (below) applied to a copy of `curation-r89.py` | both `CURATION_R89=PASS` | 0 | `c2-prior-subst-live.txt` |
| probe A: scratch counter, `curation-r90.py:328` WITNESS leg ok forced `True`, then the mutant battery | identical `MUTANTS_KILLED=10/10 …` line; M6/M7 fail only on `LEG_FAIL VERDICT` | 0 | `c2-probe-witness-leg.txt` |
| probe B: scratch counter, `__main__` exits 3 (no leg evaluated), then the mutant battery | identical `MUTANTS_KILLED=10/10 …` line; every non-M5 mutant `no-verdict` | 0 | `c2-probe-crash-kill.txt` |
| probe C: scratch counter, caller substitutions `if locates(quote, cap):` → `if cap is not None:`, `if unentailed_row(cells, joined):` → `if False:` | `CURATION_R90=PASS`, `DETECTOR_WITNESS=8/8` (named limit 3, confirmed) | 0 | `c2-probe-caller-bypass.txt` |
| probe D: scratch tree, r85 decision cell carries `modified` (absent from the entry's located quotes) | `UNENTAILED_TERM=2`, two `LEG_FAIL UNENTAILED` labels for one row, one label not in the row | 1 | `c2-probe-unentailed-double.txt` |
| mixed diff/pin commands | pins match; registry 218→219, `1 0 corpus/SOURCES.md`; before-receipt `grep -c 'CURATION_R89=PASS'` → 0 | 0 | `c2-annotations.txt` |

Live counter line (`c2-counter.txt`):

```
SUPERSEDED_LIVE=0 UNENTAILED_TERM=0 MODIFIED_DEF_CITED=1 QUOTES_LOCATED=20/20 Q_FLOORS=search-transparency-reporting-r84.md=13/13 floor13,provenance-recording-r85.md=7/7 floor7 WARRANT_OK=17/17 DUP_QIDS=0 TEACHES_CHECKED=1 TEACHES_FLAGGED=1 TEACHES_UNRESOLVED=0 SUP_CLAUSE_CHECKED=0 SUP_UNRESOLVED=0 LEGS_MEASURED=10/10 VERDICT fields_hold=1
VERDICT fields_hold=1 legs_ok=10/10 DETECTOR_WITNESS=8/8
CURATION_R90=PASS
# rc=0
```

## Clause-by-clause

1. **`CURATION_R90=PASS` (exit 0).** Held. `c2-counter.txt` `CURATION_R90=PASS`, `# rc=0`.
2. **`LEGS_MEASURED=10/10`.** Held. Same line; the ten legs are FLOOR, SUPERSEDED, UNENTAILED, DEF_CITED,
   WARRANT, TEACHES, SETUP, DUPQID, WITNESS, VERDICT (`curation-r90.py:274-349`), and `EXPECTED_LEGS = 10`
   (`:72`) is the count `passed` checks (`:367`).
3. **An output line containing `VERDICT fields_hold=1`.** Held. It is on the summary line and on the
   `DETECTOR_WITNESS` line; both are printed from the single `fields_hold` measurement
   (`curation-r90.py:336-357,365-366`), not a literal.
4. **The verdict leg is appended before the summary and is one of the ten legs `passed` requires.** Held by
   source order and by execution: `legs.append(("VERDICT", …))` is `curation-r90.py:348`, the summary `print(…)`
   begins `:350`, and `passed` is `:367` over `all(ok for … in legs)`. The append is load-bearing in the battery:
   M3 (`passed` without `and fields_hold`, TEACHES forced true) is killed by the VERDICT leg alone —
   `c2-mutants.txt`: `KILLED M3-verdict-legs … LEG_FAIL VERDICT fields_hold=0 legs_ok=9/9`. M2 (every leg's `ok`
   forced true on the broken tree) is likewise killed only by `LEG_FAIL VERDICT`.
5. **`DETECTOR_WITNESS=8/8`.** Held. `witness()` holds eight assertions, fire and silent for each of `locates`,
   `unentailed_row`, `teaches_miss`, `dup_qid` (`curation-r90.py:160-175`), and `not witness_bad` also enters
   `fields_hold` (`:347`), so the token cannot be 8/8 while the verdict is computed over a dirty witness.
6. **Each detector fires and stays silent.** Held at function scope. The four constant substitutions M6–M9 each
   print `LEG_FAIL WITNESS 7/8 bad=1` (`c2-mutants.txt`), so every witness row has a live instance and each
   substitution trips exactly one direction. Named limit 3 was checked, not assumed: caller substitutions that
   bypass the functions leave the witness at 8/8 and the counter at PASS (`c2-probe-caller-bypass.txt`).
7. **Carried fields.** Held exactly: `DUP_QIDS=0 WARRANT_OK=17/17 QUOTES_LOCATED=20/20 TEACHES_FLAGGED=1
   TEACHES_UNRESOLVED=0 SUP_CLAUSE_CHECKED=0 SUP_UNRESOLVED=0` on the live line.
8. **Mutant line and the two prior survivors.** The values are held: `c2-mutants.txt` prints exactly
   `MUTANTS_KILLED=10/10 COUNTER_DETECTED=9 BATTERY_DETECTED=1 PRIOR_R89_SURVIVORS=2/2`, `# rc=0`. Both prior
   substitutions were independently reproduced against the r89 bytes — `c2-prior-subst-live.txt`: `=== subst-0
   rc=0 === … CURATION_R89=PASS`, `=== subst-1 rc=0 === … CURATION_R89=PASS`; the anchored edits are
   `curation-r90-mutants.py:204-207`. The clause *"die against the round-90 counter on `LEG_FAIL WITNESS`"* is
   observed in the landed transcript (`KILLED M6-locate-true … LEG_FAIL WITNESS 7/8 bad=1`, M7 likewise) but is
   **not enforced by the counting command** — finding F1.
9. **Controls line.** Held: `c2-controls.txt` `FORGERY_REFUSED=7/7 PRIOR_REGRESSION=7/7`, `CONTROLS=PASS`,
   `# rc=0`; all seven `OK <case>` lines name a `LEG_FAIL` leg and the prior counter's refusal. The SUP mirror
   prints `LEG_FAIL TEACHES checked=2 flagged=2 unresolved=0 sup_unresolved=1`, so named limit 4's non-vacuity
   claim is exercised on the mirror (the live registry remains `SUP_CLAUSE_CHECKED=0`).
10. **Before: r89 prints `CURATION_R89=PASS` with `LEGS_MEASURED=8/8` and no `VERDICT fields_hold=1`.** Held:
    `c2-prior-r89-live.txt` shows `LEGS_MEASURED=8/8`, `CURATION_R89=PASS`, `# rc=0`, and
    `grep -c 'VERDICT fields_hold=1'` → `0`. (The r89 counter appends a VERDICT *leg* — `curation-r89.py:316` —
    but never prints its `fields_hold`; the distinction the claim draws is the printed token, and that is absent.)
11. **Harm (C2 kill rule K3).** Held: `c2-annotations.txt` — the two curated entries move 0 lines from the base;
    `corpus/SOURCES.md` is `1 0` (218→219 rows) and the only added line is the `+| S220 | …` row, whose last cell
    is its `used-by` cell (`corpus/evidence/round90/claims.md`). No other registry cell moved.

## Findings

### F1 — Medium — `falsifies-wording` — the mutants battery does not enforce "die on `LEG_FAIL WITNESS`"

Exact command: `python3 -B corpus/evidence/round90/curation-r90-mutants.py --root . --work <scratch>/work/probeA`
(cwd = a scratch copy of the attacked tree with only `curation-r90.py:328` changed from
`legs.append(("WITNESS", not witness_bad, …))` to `legs.append(("WITNESS", True, …))`; `fields_hold` still carries
`not witness_bad` at `:347`).

Receipt: `.ufo/waves/round-90/w1/R90ReviewerC2/c2-probe-witness-leg.txt`. Observed line (rc 0):

```
MUTANTS_KILLED=10/10 COUNTER_DETECTED=9 BATTERY_DETECTED=1 PRIOR_R89_SURVIVORS=2/2
```

with

```
  LEG_FAIL VERDICT fields_hold=0 legs_ok=9/9        (M6-locate-true)
  LEG_FAIL VERDICT fields_hold=0 legs_ok=9/9        (M7-unentailed-empty)
```

and no `LEG_FAIL WITNESS` line for either. Cause: `curation-r90-mutants.py:184` is
`dead = p.returncode != 0 or verdict_of(p.stdout) != "CURATION_R90=PASS"`; the `LEG_FAIL` lines are only printed
(`:196-199`), never asserted, so the count is identical when the two survivors die on a different leg. At the
attacked bytes the clause is true (`c2-mutants.txt`: both M6 and M7 print `LEG_FAIL WITNESS 7/8 bad=1`), but the
counting command cannot distinguish that from a regression that moves the detection to VERDICT. The claim wording
attributes a specific leg to the death; the instrument counts only exit status. A future regression of this clause
would still print the frozen after-line.

### F2 — Low — `verification-gap` — `MUTANTS_KILLED=10/10` is produced by a counter that never evaluates its predicate

Exact command: the same battery against a scratch copy whose `__main__` is `sys.exit(3)` (so no leg, no verdict,
no predicate runs). Receipt: `.ufo/waves/round-90/w1/R90ReviewerC2/c2-probe-crash-kill.txt`, rc 0. Observed:

```
KILLED M1-dead-teaches tree=base rc=3 no-verdict
KILLED M6-locate-true tree=base rc=3 no-verdict
…
MUTANTS_KILLED=10/10 COUNTER_DETECTED=9 BATTERY_DETECTED=1 PRIOR_R89_SURVIVORS=2/2
```

A crash (`no-verdict`, rc != 0) counts as `KILLED` under `curation-r90-mutants.py:184`, although its docstring
(`:4`) requires "the counter's own frozen predicate must FAIL on it". The attacked transcript is honest — all ten
genuine mutants print `CURATION_R90=FAIL` (`c2-mutants.txt`) — but the token is exit-status evidence, not
predicate evidence.

### F3 — Low — `instrument-doc` — the two new batteries' module docstrings contradict the code they document

`curation-r90-controls.py:2-7` says "curation-r89-controls — the round-89 C2 forgery control battery … the
round-88 counter ACCEPTS it (the do-nothing evidence)", while the code wires `before=R89` (`:86,201,226`) and
requires the prior to REFUSE (`:238-239`, inline comment `:235-237`: "the prior counter must refuse them too (a
regression hold)"). `curation-r90-mutants.py:2,22` still titles the battery "curation-r89-mutants" and gives the
usage path `corpus/evidence/round89/curation-r90-mutants.py`; its mutant list (`:16-20`) names only M1–M5 while the
`MUTANTS` table has M1–M4b, M5, M6–M9. The frozen token `PRIOR_REGRESSION=7/7` matches the code and claim, so
this is drift in files added this round, not a token falsification; it misdescribes what the prior leg measures.

### F4 — Low — `evidence-mismatch` — the cited before-receipt does not print the verdict it is cited for

`corpus/evidence/round90/claims.md` C2 "Before" says the two substitutions "print `CURATION_R89=PASS`
(survivors): receipts `controls/receipts/c2-prior-landing.txt`, `controls/receipts/c2-subst-before.txt`". The
committed `c2-subst-before.txt` (copied verbatim to `cited-c2-subst-before.txt`; sha256
`a813e0296caf0c48757122ab308db424215b90664f1e4c2d1a15ccf4d7243319`) contains only the derived markers
`SURVIVOR_PRIOR r89-subst-0 rc=0` / `…subst-1 rc=0`; `grep -c 'CURATION_R89=PASS'` on it is `0`
(`c2-annotations.txt`). The fact itself is true and I reproduced the missing lines independently
(`c2-prior-subst-live.txt`: both `CURATION_R89=PASS`, rc 0), but the cited receipt does not carry the quoted
token; a reader cannot verify the Before from the receipt alone.

### F5 — Low — `diagnostic-contract` — one unentailed row is reported twice, once with a term absent from the row

`curation-r90.py:247-250` keeps the r89 per-term loop after the term quantification moved into `unentailed_row`
(`:149-150`, which already returns `any(… for term in DEFECT_TERMS)`). The append sits inside both, so one matching
row appends once per term and carries the loop's term label regardless of which term matched.

Exact command: `python3 -B corpus/evidence/round90/curation-r90.py --root .` against a scratch copy whose r85
decision cell reads `state the modified transformation from one entity into another` (no located quote in either
entry contains `modif`). Receipt: `.ufo/waves/round-90/w1/R90ReviewerC2/c2-probe-unentailed-double.txt`, rc 1.
Observed:

```
SUPERSEDED_LIVE=0 UNENTAILED_TERM=2 … LEGS_MEASURED=8/10 VERDICT fields_hold=0
LEG_FAIL UNENTAILED provenance-recording-r85.md Recording a derivation's direction term=modification; provenance-recording-r85.md Recording a derivation's direction term=modified
```

The row contains `modified`, not `modification`, so the first label is an artifact of the outer loop; the same row
is counted twice. The leg's boolean is unchanged (still false) and no frozen value moves (`UNENTAILED_TERM=0` on
the clean tree), but the printed field and the `LEG_FAIL UNENTAILED` labels are not a row/term report.

## Residual risk and verification gaps

- **Runtime.** Every run used one canonical interpreter, `/usr/bin/python3` 3.14.8 (`c2-annotations.txt`); no
  alternate interpreter or runtime was used. Same-identity rerouting and saturation claims do not arise in C2.
- **Named limit 3 is real and load-bearing.** The probe: caller substitutions that bypass the four functions
  leave `DETECTOR_WITNESS=8/8` and `CURATION_R90=PASS` (`c2-probe-caller-bypass.txt`). The witness guards the
  function bodies only, exactly as the limit says; no amendment is needed, but "each detector fires and stays
  silent" is function-scoped, not caller-scoped.
- **Named limit 4 holds.** `SUP_CLAUSE_CHECKED=0` on the live registry; the only non-vacuity is the battery mirror
  (`LEG_FAIL TEACHES checked=2 … sup_unresolved=1`).
- **F1 and F2 are the same one-line criterion** (`curation-r90-mutants.py:184`). The current transcript backs
  both the `CURATION_R90=FAIL` and the `LEG_FAIL WITNESS` lines, so the landing bytes are not misreported; the
  exposure is that neither fact is a predicate of the counting command.
- `fields_hold` (`curation-r90.py:336-347`) restates every non-VERDICT leg condition, so on the genuine counter
  the VERDICT leg's `fields_hold == prior_ok` conjunct is tautological; the leg is load-bearing only because
  `passed` retains `and fields_hold` (`:367`) and because `len(legs) == EXPECTED_LEGS`. The claim's sentence does
  not assert more than that, but the redundancy means a joint edit of `fields_hold` and the legs is the harness.
- I did not re-derive quote content beyond the counter's own 20/20 and the controls; the carried-field values are
  the counter's printed measurements. I did not run C1 or C3 (out of seat scope), and no `lsp` device was available
  for semantic reference checks.

VERDICT: R90ReviewerC2 C2 fired — every claimed value reproduces exactly at `9bad1201` (PASS/`LEGS_MEASURED=10/10`/`DETECTOR_WITNESS=8/8` rc 0; mutants `10/10` with `2/2` prior survivors; controls `7/7`+`7/7` rc 0; entries and registry harm clean), but the clause "die on `LEG_FAIL WITNESS`" is not enforced by the mutants battery — a scratch copy with the WITNESS leg forced ok still prints the identical `MUTANTS_KILLED=10/10 …` line while M6/M7 die only on `LEG_FAIL VERDICT` (F1).

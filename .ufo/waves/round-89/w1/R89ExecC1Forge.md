# Seat R89ExecC1Forge — C1 forge report (round 89, lane chousa)

Frozen base `ac0a0892c15de11fb28d3208f2b287687c00477e`, cloned to
`/fast/scratch/hyaku/chousa-r89/R89ExecC1Forge/repo` (a `git archive` tree lacks `.git`,
so the counter's repo-dependent legs spuriously fail there — see receipts/baseline.txt for
the clone-run baseline: `GATE_RECORDS_R89=PASS`, `MUTANTS_KILLED=11/11
TOOL_MUTANTS_CAUGHT=2/2`, harm `moved=0`, tool sha256 `905f9da2…` matches the claim).
Method: apply candidate counter-state edits to a *copy* of `gate-records-r89.py` (plus a
few `--tool` substitutions against the pristine counter), run it, and record whether the
frozen predicate stays green. `SURVIVED` = `GATE_RECORDS_R89=PASS`, rc=0.

## Forgery results

### (a) Cross-check detachments

| Forge | Shape | Verdict |
|---|---|---|
| a1 | `FORGED_REFUSED` printed +1, legs honest | **REFUSED** — `UNCROSSCHECKED FORGED … FORGED_REFUSED=363/362`, `CROSSCHECK=14/15`, `LEG_FAIL SUMMARY 14/15`, rc=1 |
| a2 | `MUT_ADMIT_DERIVED` printed +1 | **REFUSED** — `UNCROSSCHECKED MUT_ADMIT … MUT_ADMIT_DERIVED=2`, rc=1 |
| a3 | `DERIVE_NEG` printed 1 (vacuous on healthy tree — measured value already 1) | **SURVIVED** trivially; see a3b below (non-vacuous) |
| a3b | `derive_neg` measured 0, leg `ok` detached, printed 0 | **REFUSED** — `UNRECONCILED DERIVE_NEG detail=0/1 receipt_ok=True rederived=False` + `UNCROSSCHECKED`, rc=1 |
| a4 | D1_WIDTH detail forged to `3/3/1 pin3` with `ok=True`, `DIV3` honest (=3) | **REFUSED** — `UNRECONCILED D1_WIDTH … rederived=False` and `UNCROSSCHECKED D1_WIDTH … DIV3=3`, rc=1 (this is the E7d boundary: only the honest `DIV3` catches it) |
| a5 | SUMMARY receipt detail rewritten to `{len}/{len}`, ok forced true | **SURVIVED** — pass, but vacuous as designed *on the healthy tree*: on a healthy tree `cross_ok/len` already equals `len/len`, so the rewrite is a no-op. Non-vacuous version a5b (detail `999/15`) → **REFUSED** `UNRECONCILED SUMMARY … rederived=False`, rc=1 |
| a5c | a1's broken cross-check + SUMMARY ok forced true | **REFUSED** — `CROSSCHECK=14/15`, rc=1; the SUMMARY leg does not carry the verdict alone, the cross-check count does |
| a6 | joint rewrite: `div3=1`, both width details rewritten `3/3/3 pin3`, `DIV3`/`D1_EXPECTED` forged to 3 | **SURVIVED** — pass, expected: this is the named-limit-1 joint rewrite ("that edit *is* the counter"). Not a finding against C1 as written; logged as the disclosed boundary. |

### (b) Per-format re-derivation

| Forge | Shape | Verdict |
|---|---|---|
| b1 | D1_WIDTH detail forged to name D2's numbers (`len(d2)/…`) | **SURVIVED** — pass, but numerically vacuous: `len(d2) == len(d1) == 3` on this registry, so the swap is indistinguishable from the truth. Non-vacuous b1b (detail `2/2/2 pin2`, ok true) → **REFUSED** `UNCROSSCHECKED D1_WIDTH … D1_FORGES=3 … pin=2/3`, rc=1 |
| b2 | `div3` narrowed to 1 and printed honestly (`3/3/1 pin3`) | **REFUSED** — `LEG_FAIL D1_WIDTH/D2_WIDTH 3/3/1 pin3`, rc=1 |
| b3 | `ROWS_203` pin moved 3→4, details honest (`3/3/3 pin4`) | **REFUSED** — cross-check `pin=4/4` vs measured `pin4` mismatch → `LEG_FAIL D1_WIDTH/D2_WIDTH`, rc=1 |
| b4 | `div3 = d1_expected` (self-referential third derivation) | **SURVIVED** — pass. This is the disclosed named-limit-3 class ("agreement between a receipt and its own detail, not the truth of the measurement expression"). The claim *names* this limit; the report confirms it is real and undisguised. Not a K2/K4 finding as worded — but C1's sentence "each leg's re-derived numbers must equal the fields the summary printed" is read by the counter as intra-counter agreement only, so any future claim that wants div3 to be an *independent* witness must say so explicitly. |

### (c) `DERIVE_NEG`

| Forge | Shape | Verdict |
|---|---|---|
| c1 | subject tool rewritten to use `r[6] == "2" + "00"` (usable literal survives via concatenation); pristine counter pointed at it | **REFUSED** — `LEG_FAIL MUT_ADMIT derived=0 killed=0`, rc=1. String concatenation is *not* found by the mutant builder's exact-substring search; the literal genuinely disappears, so the negative result is honest. A concatenation still counts as survival of a usable literal semantically, but the claim only promises builder-detectability — the refused verdict comes from the honest mutant-leg failure, not from a shortcut |
| d3 | same, with the literal left in a trailing comment (`# r[6] == "200"`) | **REFUSED** — the builder finds the commented literal, derives a mutant, which then fails to kill (`killed=0`) → `LEG_FAIL MUT_ADMIT/MUT_UNREACH`, rc=1. The refusal is earned by measurement, not by the derivation succeeding or failing vacuously |

### (d) `TOOL` leg

| Forge | Shape | Verdict |
|---|---|---|
| d1 | `--tool` a directory | **REFUSED** — `TOOL=absent … LEGS=0/16`, `UNCROSSCHECKED TOOL detail=tool present TOOL=- want=absent`, `LEG_FAIL TOOL`, rc=1 |
| d2 | `--tool` a symlink to the pristine base blob | **SURVIVED** — pass. A symlink to identical bytes *is* the tool (`os.path.isfile` follows the link); "tool path is a symlink" is not by itself a forgery. A symlink to *different* bytes would be caught by the same legs that catch a different `--tool` file (cf. `mutate-r89.py` TOOL_MUTANTS caught) |

## Findings against C1's K2/K4

**None.** Every non-vacuous, non-joint forgery — summary-field detachments (a1, a2, a3b),
detail+ok forgery with honest DIV3 (a4), SUMMARY receipt forgery (a5b), cross-check over a
forged SUMMARY (a5c), wrong-number width detail (b1b), honest narrowed derivation (b2), moved
pin constant (b3), concatenation and comment literals (c1, d3), and directory tool (d1) —
is refused with a named `UNRECONCILED`/`UNCROSSCHECKED`/`LEG_FAIL` line, rc=1.
The two passes are both inside the claim's disclosed named limits: a6 (joint rewrite) =
named limit 1; b4 (self-referential honest derivation) = named limit 3. a3/a5/b1 first-round
"passes" were vacuous construction artifacts on the healthy tree and each has a refused
non-vacuous sibling above. No accepted forgery → no K2/K4 finding against C1 was fired.

Rows observed where the counter's printed reason matters, all from `receipts/forge-round1.tsv`
and `receipts/forge-round2.log`; commands in the Driver section.

## Driver

- Tree: scratch clone at `ac0a0892c15de11fb28d3208f2b287687c00477e` (see baseline note above).
- `python3 -B corpus/evidence/round89/gate-records-r89.py --root $REPO --repo $REPO --work $W`
- `python3 -B corpus/evidence/round89/mutate-r89.py --root $REPO --repo $REPO --work $W`
- `python3 -B corpus/evidence/round89/harm-recheck.py --root $REPO --repo $REPO --base-tool $W/base-tool.py` (base blob from `f8fa55ec:tools/gate-records.py`)
- Forges: `forge.py` / `forge2.py` under the scratch dir, each spawning a mutated copy of
  the counter (or the pristine counter with a substituted `--tool`) and asserting PASS/FAIL.
  Per-forge stdout was captured in `receipts/forge-round1.log` / `forge-round2.log`.

## Tooling

No installs or upgrades. `python3` stdlib only; pacman untouched per the orchestrator ruling.

## Receipts

- `receipts/baseline.txt` — pristine counter + mutant battery (+harm) on the frozen tree
- `receipts/forge-round1.tsv`, `receipts/forge-round1.log` — round-1 forgeries (a1–d1) with verdict, rc, diagnostics
- `receipts/forge-round2.log` — round-2 non-vacuous forgeries (a3b, a5b, a5c, b1b, b4, d2, d3)

VERDICT: R89ExecC1Forge C1 held — every non-vacuous non-joint forgery is refused with a named line; the only passes are the disclosed joint-rewrite and honest-self-referential-derivation limits.

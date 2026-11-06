# R82MutationGate — seat report (round 82, wave 1)

Mutation test of the C1 gate patch and of both frozen counters, against the candidate landing bytes
`b4a41d251b488f06b4a6ab01a11bc12ce72edd20`. Full tables, witnesses and restoration evidence:
`.ufo/waves/round-82/w1/R82MutationGate/mutants.md` (same folder holds every receipt cited below).
Leaf seat: no production edit, no lane/fleet git mutation, no network, scratch deleted at exit.

## Baseline (the landed bytes, before any mutation)

- C1 counting command — `cd <landing tree> && python3 -B corpus/evidence/round82/k2-gate-r82.py --root .`
  → `RUNLINES=2/2 K2_REFUSED=11/11 HOLD_REFUSED=9/9 CLASS_REFUSED=24/24 POSITIVE=6/6`, `K2_GATE=PASS`, rc 0.
  Receipt: `.ufo/waves/round-82/w1/R82MutationGate/c1-landing-count.txt` (gate sha256 `0d8ac50f…`).
- C2 counting command — `cd <landing tree> && python3 -B corpus/evidence/round82/depth-r82.py --root .`
  → `DEPTH_R82 entries=1 ok_entries=1 rows=9 located_quotes=11 fresh_sources=4`, `DEPTH_R82=PASS`, rc 0.
  Receipt: `.ufo/waves/round-82/w1/R82MutationGate/c2-landing-count.txt`.
- Control battery on the prefreeze base (the scoring fixture) — `HYAKU_SCRATCH=… bash repo38/corpus/evidence/round82/run-controls-r82.sh 04bff4f9 <out>`
  → `CONTROLS_AS_EXPECTED=14/14`, rc 0; all 14 rows `expected == observed`.
  Receipt: `.ufo/waves/round-82/w1/R82MutationGate/receipts/control-battery-pristine-summary.tsv`.

## Findings

**F1 — C1 gate patch: 15 of 23 single mutants killed.**
Command per mutant: `python3 -B <tree>/corpus/evidence/round82/k2-gate-r82.py --root <tree>`
(one replacement in the round-82 hunks of `tools/research-gate.sh`, tree = landing archive).
Receipt: `.ufo/waves/round-82/w1/R82MutationGate/gate-mutants.tsv` (mutant, mutated sha256, counter rc, summary line,
catching manifest rows) and `gate-run.log`/`gate-run2.log`/`gate-run3.log`.
Observed examples — MG17 (invert `nres`): `RUNLINES=2/2 K2_REFUSED=7/11 HOLD_REFUSED=9/9 CLASS_REFUSED=19/24 POSITIVE=6/6`,
`K2_GATE=FAIL`, rc 1, killed by `F2-1,F2-2,F2-4,F2-5,V2C-emdash,V2C-na-upper,V2C-tbd,V2C-undeclared-w9,V2C-undeclared-w9-withsec`;
MG12 (heading restricted to `Rejections`): `K2_REFUSED=10/11 … POSITIVE=5/6`, `K2_GATE=FAIL`, rc 1, killed by
`F4-5,P4-alt-section-complete,V4S-kept-rejections,V4S-rejected`.

**F2 — 8 gate survivors no manifest row catches; 4 admit declared-vocabulary K2 cells.**
Command: same counter, mutant trees MG09/MG10/MG11/MG23; receipts
`.ufo/waves/round-82/w1/R82MutationGate/receipts/gate-survivor-MG*.txt` (all `RUNLINES=2/2 … POSITIVE=6/6`,
`K2_GATE=PASS`, rc 0 — byte-identical verdicts to pristine).
Witnesses (one cell changed in `item4-pass.md`, item-4 Run line run on pristine and mutant gate):
W1 `"n/a"` → pristine rc 1 `REJECTIONS_OK=0/1` DRIFT, mutant rc 0 `REJECTIONS_OK=1/1` CLEAN;
W2 `'none'`, W3 `*TBD*`, W4 `n_a` identical pattern. Receipts
`receipts/witness-W1-flip-dquote-pristine.txt` / `…-mutant.txt` (and W2–W4).
These four values are inside the frozen declared vocabulary (quotes / `*` / `_` are folded off before comparison);
no `c1-manifest.tsv` row carries such a cell, so a gate missing those folds still prints the exact landing fractions.

**F3 — 3 gate survivors would misrefuse well-formed negatives (harm direction).**
MG14/MG15/MG16 (drop `SW_CLAIMS[cid]`, `SW_IDS[cid]`, sweep-cell token match). Witnesses W5–W7 (one cell changed in
`item2-pass.md`): pristine rc 0 CLEAN `VERIFIED_SWEEPS=1/1`; mutant rc 1
`FINDING SWEEP_NEGATIVE_UNRESOLVED … claim=N1 sweep=- names no sweep row this mode re-ran`.
Receipts `receipts/witness-W5-resolve-claimid-*.txt`, `…W6-resolve-ids-cid-*.txt`, `…W7-resolve-token-*.txt`.
No K2 form passes; the frozen manifest simply has no positive record for these arms (the positives resolve through
`SW_CLAIMS`), so a frozen counter could not distinguish them.

**F4 — 1 gate survivor is output-text only; the selftest catches it, the manifest does not.**
MG21 (drop `placeholder=reason:..` from the finding obs), manifest verdict unchanged (PASS, rc 0,
`receipts/gate-survivor-MG21-drop-placeholder-annotation.txt`); witness W8: pristine obs
`id=R1 missing=flip placeholder=reason:present,flip:placeholder`, mutant obs `id=R1 missing=flip`, rc 1 both.

**F5 — selftest probes (two runs, seat budget): `claims-lane-fallback` is a hardlink artifact; the five new cases
catch MG21 but not MG09.**
Command: `bash tools/research-gate.sh --selftest` in the mutant tree. Receipts
`selftest-MG09-drop-dquote-fold.log`, `selftest-MG21-drop-placeholder-annotation.log` (287/294 lines, 280 cases,
0 `skip-case`). Observed: MG09 `RESEARCH_GATE_SELFTEST: FAIL (1/280 cases)`, sole `FAIL-case claims-lane-fallback
exit=1 want=0`; MG21 `FAIL (2/280 cases)` = that same case plus `FAIL-case sweeps-fail-placeholder-cells`.
Cases 53–57 (the five round-82 cases) are all `ok-case` under MG09; case 53 is the killer under MG21.
The shared failure is setup, not gate: `tools/research-gate.sh:1825` refuses `nlink != 1`, and my `cp -al` trees give
`PROVINCE.md` nlink 24 (`stat -c '%h'`); `repo38/PROVINCE.md` nlink 1. Both runs restored the gate file
(`restored_ok: true`, sha256 `0d8ac50f…`), reported in `selftest-MG09.json` / `selftest-MG21.json`.

**F6 — C1 counter `k2-gate-r82.py`: only 2 of 11 mutants killed by the frozen 14-control battery.**
Command: `HYAKU_SCRATCH=<scratch>/<mutant> bash repo38/corpus/evidence/round82/run-controls-r82.sh <mutant-commit> <out>`
(one mutated counter per commit of the `38f5af82` tree; the driver archives `REV` from the repo containing it).
Receipt: `.ufo/waves/round-82/w1/R82MutationGate/counter-mutants.tsv`; per-mutant control receipts in
`counter-receipts/<mutant>/summary.tsv`.
Killed: MK10 (hold-only PASS) by `c1-k0-donothing` FAIL→PASS (`RUNLINES=2/2 K2_REFUSED=0/11 HOLD_REFUSED=9/9
CLASS_REFUSED=2/24 POSITIVE=5/6`, `K2_GATE=PASS`, rc 0 in `counter-receipts/MK10-hold-only-PASS/c1-k0-donothing.txt`);
MK11 (accept every row) by `c1-k0-donothing`, `c1-f1-blanket-refuse`, `c1-f2-wrong-finding-keyed`, all FAIL→PASS
(`counter-receipts/MK11-accept-every-row/*.txt`).
Survivors (9): drop `FROZEN_RUNLINE`, accept rc 2, drop the verify-mode union, positives-only PASS, drop the CLEAN
string, refuse-rc-only, accept rc 0, drop the positive group, one-Run-line PASS — each leaves all 14 observed values
equal to expected. The C1 controls are all FAIL-expected, so they constrain the counter only against a PASS.

**F7 — C2 counter `depth-r82.py`: 5 of 11 mutants killed; E2/E4/E6/E7, the `Warrant` column and `ROUND_START` survive.**
Command: the same committed driver with the mutated `depth-r82.py` committed. Receipt: `counter-mutants.tsv`;
kills: MD1 by `c2-d2-fabricated-quotes` FAIL→PASS (`ENTRY … ok=yes … fails=-`, `DEPTH_R82=PASS`, rc 0,
`counter-receipts/MD1-drop-E3-capture/c2-d2-fabricated-quotes.txt`), MD4 by `c2-d4` and `c2-d6`, MD6 by
`c2-d5-four-rows` (`rows=4`, PASS, rc 0), MD9 by `c2-d4`, MD10 by `c2-d6`. Survivors: MD2 (drop the refetch
freshness floor; `c2-d3` still fails E3,E4,E6,E7), MD3 (E6), MD5 (E4), MD7 (E7), MD8 (E2), MD11 (Warrant column) —
each leaves 14/14 observed values equal to expected.

**F8 — neither the landing predicate nor the battery pins most counter checks.**
Command: `python3 -B mutcounters/<mutant>.py --root <landing tree>` (mutated counter against the landed bytes).
Receipt: `.ufo/waves/round-82/w1/R82MutationGate/method/counter-mutants-landing.json` (plus the counter bytes in
`mutcounters/`, sha256 equal to each mutant's recorded `mut_sha256`).
Observed: 10/11 k2-gate mutants still print `RUNLINES=2/2 K2_REFUSED=11/11 HOLD_REFUSED=9/9 CLASS_REFUSED=24/24
POSITIVE=6/6`, `K2_GATE=PASS`, rc 0; only MK3 (drop the verify-mode union) prints `HOLD_REFUSED=7/9`, `K2_GATE=FAIL`,
rc 1. All 11 depth mutants print `DEPTH_R82 entries=1 ok_entries=1 rows=9 located_quotes=11 fresh_sources=4`,
`DEPTH_R82=PASS`, rc 0. Combined with F6/F7: the landing artifact pins one k2 check, the battery pins two k2
PASS-formula mutants and five depth checks, and the remaining checks (k2: FROZEN_RUNLINE, rc 2, CLEAN string,
finding id, rc 0, positives group, one Run line; depth: E2, E4, E6, E7, `Warrant` column, `ROUND_START`) are pinned
by neither.

## Tooling

No tool installed or upgraded (uv/pacman/npm untouched); pacman guard respected.

## Verdicts

VERDICT: R82MutationGate C1 held — the landed counting command prints the exact target fractions (`11/11 9/9 24/24 6/6`, PASS, rc 0) and the gate patch kills 15/23 mutants; the selftest leg was not re-measured on pristine landing (seat budget: two selftest runs, both on mutants).
VERDICT: R82MutationGate C2 held — the landed counting command prints `entries=1 ok_entries=1 rows=9 located_quotes=11 fresh_sources=4` PASS rc 0; 5/11 counter mutants are killed by the frozen battery, the rest are coverage gaps, not falsifications.

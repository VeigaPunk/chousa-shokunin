# R82MutationGate — mutation report (round 82, wave 1)

Seat `R82MutationGate`. Bytes attacked: candidate landing `b4a41d251b488f06b4a6ab01a11bc12ce72edd20`
(`tools/research-gate.sh` sha256 `0d8ac50f2695b8df9300905dd44ea70668dd047912633226f8bababe7570d92a`) and the
two frozen counters (`k2-gate-r82.py` sha256 `4d6ba0556f674972d836434cbbc8f7c188b41473ad7d505d24cd208d517ab3af`,
`depth-r82.py` sha256 `726d3ed942f18c7c5845e4a376069f0b257cfb4a57c96f680b8f8daa946eb6de`, both equal to
`corpus/evidence/round82/instrument-pins.txt`). Controls/driver inside the landing tree are byte-equal to the pins
(`run-controls-r82.sh` `74940be2…`). No network was used; no production file was edited; every probe ran on a
`git archive` extraction under `/fast/scratch/hyaku/chousa-r82/R82MutationGate/` (hardlinked per-mutant trees, one
fixture git repo `repo38` whose base commit `04bff4f90173f00bc9f7220f7f244cf479f4fd80` is the prefreeze tree
`38f5af82…`). Every mutation was reverted after its probe and the pristine sha256 re-checked (assertion in the
harness; restored values recorded below). Scratch was deleted before yield; all cited receipts were copied into
`.ufo/waves/round-82/w1/R82MutationGate/`.

Detectors, exactly as run:

- Gate mutants: `python3 -B <mutant-tree>/corpus/evidence/round82/k2-gate-r82.py --root <mutant-tree>`
  (cwd = mutant tree). Baseline on the pristine landing tree: `RUNLINES=2/2 K2_REFUSED=11/11 HOLD_REFUSED=9/9
  CLASS_REFUSED=24/24 POSITIVE=6/6`, `K2_GATE=PASS`, rc 0 — `.ufo/waves/round-82/w1/R82MutationGate/c1-landing-count.txt`.
- Counter mutants: `HYAKU_SCRATCH=<scratch>/<mutant> bash <repo38>/corpus/evidence/round82/run-controls-r82.sh
  <mutant-commit> <out>` from `repo38`. The driver archives the revision from the repo that contains the driver
  (`LANE=$(cd "$(dirname "$0")/../../.." && pwd)`), so each mutant is a commit of the prefreeze tree with exactly one
  counter file changed; `REV` is that commit (the committed driver is byte-identical).
  Pristine battery baseline on `repo38` base: `CONTROLS_AS_EXPECTED=14/14`, rc 0
  (`receipts/control-battery-pristine-summary.tsv`).

---

## A. C1 gate patch — 23 single mutants

Each mutant is one replacement in the round-82 hunks of `tools/research-gate.sh`; "killed" = the frozen counter's
verdicts changed (it FAILs, rc 1); the last column names the manifest rows whose verdict flipped to `bad`.
Full observed summary line and rc per mutant: `gate-mutants.tsv`. Full counter output for every survivor:
`receipts/gate-survivor-<mutant>.txt`.

| mutant | mutation | mutated sha256 (12) | verdict | manifest rows that catch it |
|---|---|---|---|---|
| MG01-drop-na | drop `n/a` from the placeholder list | e07eeedfe2df | killed | F2-3,F2-6,F4-2,V2W-na-dot,V2W-na-upper,V4F-na-backtick,V4F-na-upper,V4R-na-upper |
| MG02-drop-none | drop `none` | 51d5f7909a10 | killed | F4-3,V4F-none-dot,V4R-none-upper |
| MG03-drop-tbd | drop `tbd` | 7b5911c0e239 | killed | V4F-tbd-upper,V4R-tbd |
| MG04-drop-unknown | drop `unknown` | 9c879a6e00fc | killed | V4F-unknown |
| MG05-drop-qmark | drop `?` | 1c9ea14aa530 | killed | V4F-qmark |
| MG06-drop-emdash | drop `—` | 8432a7464ff8 | killed | V4F-emdash |
| MG07-drop-period-strip | drop `while … *.` period strip | 6ef0378c8636 | killed | V2W-na-dot,V4F-ellipsis,V4F-none-dot |
| MG08-drop-backtick-fold | drop backtick folding | aad01aa5b477 | killed | V4F-na-backtick |
| MG09-drop-dquote-fold | drop double-quote folding | 6daadb476674 | **SURVIVED** | — |
| MG10-drop-squote-fold | drop single-quote folding | 2ff27ab3ffe9 | **SURVIVED** | — |
| MG11-drop-star-fold | drop `*` folding | aa6a15d73a1c | **SURVIVED** | — |
| MG12-restrict-heading | reject-heading match only `Rejections` | 480f080bc75b | killed | F4-5,P4-alt-section-complete,V4S-kept-rejections,V4S-rejected |
| MG13-drop-placeholder-junk | drop placeholder→junk in `sweep_token_class` | 896ecf438a88 | killed | F2-3,F2-6,V2W-na-dot,V2W-na-upper |
| MG14-drop-SW_CLAIMS | drop `SW_CLAIMS[cid]` arm | 7a8c9d5c7b8c | **SURVIVED** | — |
| MG15-drop-SW_IDS-cid | drop `SW_IDS[cid]` arm | 507411caba51 | **SURVIVED** | — |
| MG16-drop-token-match | drop `SW_IDS[token]` match | 88555a2c6130 | **SURVIVED** | — |
| MG17-invert-nres | `nres=0` → `nres=1` | 61f6e5becd84 | killed | F2-1,F2-2,F2-4,F2-5,V2C-emdash,V2C-na-upper,V2C-tbd,V2C-undeclared-w9,V2C-undeclared-w9-withsec |
| MG18-negative-info | negative finding severity `warn` → `info` | 379d2fe75e4f | killed | same nine item-2 K2/class rows (rc 0 where 1 is required) |
| MG19-reason-placeholder-absent | `rp != present` → `rp == absent` | 48f9d9d6d202 | killed | F4-4,V4R-na-upper,V4R-none-upper,V4R-tbd |
| MG20-flip-placeholder-absent | `fp != present` → `fp == absent` | 77287ed0d400 | killed | F4-1,F4-2,F4-3,V4F-ellipsis,V4F-emdash,V4F-na-backtick,V4F-na-upper,V4F-none-dot,V4F-not-applicable,V4F-qmark,V4F-tbd-upper,V4F-todo,V4F-unknown |
| MG21-drop-placeholder-annotation | drop `placeholder=reason:..` obs text | 3a5a68a5ea0f | **SURVIVED** | — |
| MG22-read-Rejections-only | `table_rows "$rsec"` → `table_rows Rejections` | 4d80e7a8e807 | killed | F4-5,P4-alt-section-complete,V4S-kept-rejections,V4S-rejected |
| MG23-drop-underscore-fold | drop `_` folding | 8a91e0b8e1d5 | **SURVIVED** | — |

Tally: 15 killed / 23; 8 survivors.

### Survivors and what they admit (witnessed, not inferred)

Witness records are built from the frozen fixtures (`item4-pass.md`, `item2-pass.md`) with one cell changed; the
item-4 / item-2 Run line is executed on the pristine landing gate and on the mutant gate. Pristine gate sha256
`0d8ac50f…`; mutants as listed. Receipts: `receipts/witness-W<n>-*.md` (record), `…-pristine.txt`, `…-mutant.txt`.

| survivor | K2 form admitted (frozen vocabulary) | witness | pristine | mutant |
|---|---|---|---|---|
| MG09 | flip/reason cell `"n/a"` — a declared value after quote folding, K2 (a)/(b) | W1-flip-dquote | rc 1, `REJECTIONS_OK=0/1`, DRIFT | rc 0, `REJECTIONS_OK=1/1`, CLEAN |
| MG10 | flip cell `'none'` | W2-flip-squote | rc 1, `REJECTIONS_OK=0/1`, DRIFT | rc 0, `REJECTIONS_OK=1/1`, CLEAN |
| MG11 | flip cell `*TBD*` | W3-flip-star | rc 1, `REJECTIONS_OK=0/1`, DRIFT | rc 0, `REJECTIONS_OK=1/1`, CLEAN |
| MG23 | flip cell `n_a` (→ `na` after `_` folding) | W4-flip-underscore | rc 1, `REJECTIONS_OK=0/1`, DRIFT | rc 0, `REJECTIONS_OK=1/1`, CLEAN |
| MG14 | not a pass-through: misrefuses a negative claim resolved only by a Sweeps row `claim_id` (K3-harm direction) | W5-resolve-claimid | rc 0, CLEAN, `VERIFIED_SWEEPS=1/1` | rc 1, `FINDING SWEEP_NEGATIVE_UNRESOLVED … claim=N1` |
| MG15 | same, resolved only by a Sweeps row whose id equals the claim id | W6-resolve-ids-cid | rc 0, CLEAN | rc 1, `SWEEP_NEGATIVE_UNRESOLVED claim=W1` |
| MG16 | same, resolved only by the sweep cell naming a declared Sweeps id | W7-resolve-token | rc 0, CLEAN | rc 1, `SWEEP_NEGATIVE_UNRESOLVED claim=N1 sweep=W1` |
| MG21 | no K2 form; the finding keeps its id and rc but loses which cell was a placeholder | W8-annotation | `… obs=id=R1 missing=flip placeholder=reason:present,flip:placeholder` | `… obs=id=R1 missing=flip` (rc 1 both) |

The four value forms in W1–W4 are inside the frozen declared vocabulary (claims.md: lower-case, drop backticks,
quotes, `*`, `_`, collapse whitespace, strip trailing periods, then compare). The landed gate refuses all four
(pristine column); a landed gate missing any one fold would still print the frozen landing fractions because no
`c1-manifest.tsv` row carries a quoted, starred or underscored placeholder cell. That is a manifest-coverage gap,
not a C1 falsification.

### Selftest probes (seat budget: two runs)

Both runs executed `bash tools/research-gate.sh --selftest` in the mutant tree (287-line log each), 280 cases, 0
skipped, exit 1. `claims-lane-fallback` fails in **both** runs with `observed=refused source=PROVINCE.md at=-`;
that is my hardlink-tree artifact, not a gate defect: the gate refuses a source with `nlink != 1`
(`tools/research-gate.sh:1825`: `nlink=$nlink multi-linked source refused`), and every file in a `cp -al` mutant
tree has nlink 24 (`stat -c '%n nlink=%h' mut-trees/mu09/PROVINCE.md` → `nlink=24`; `repo38/PROVINCE.md` → `nlink=1`).

| mutant | selftest verdict | new sweeps cases 53–57 | mutant-caused failure |
|---|---|---|---|
| MG09 (dquote fold) | `FAIL (1/280 cases)` | all five `ok-case` | none — the five new cases do **not** catch it; sole failure is `claims-lane-fallback` (artifact) |
| MG21 (annotation) | `FAIL (2/280 cases)` | case 53 `sweeps-fail-placeholder-cells` **FAIL-case** | case 53 (expects `placeholder=reason:…`), plus the same artifact |

So the selftest catches the annotation regression (MG21) but not the double-quote folding gap (MG09); neither is
caught by the frozen counting command.

---

## B1. C1 counter `k2-gate-r82.py` — 11 mutants

Scored by the committed 14-control battery at the prefreeze base. "killed" = a control's observed PASS/FAIL
differs from its committed expected value. Observed lines and rc: `counter-receipts/<mutant>/<control>.txt`;
pristine column: `counter-receipts/battery-pristine-baseline/summary.tsv` (`14/14`).

| mutant | mutation | commit | verdict | killer control |
|---|---|---|---|---|
| MK1-drop-FROZEN_RUNLINE | drop the frozen Run-line equality check | 2d14589c | SURVIVED | — |
| MK2-accept-rc2 | accept rc 2 as a refusal | 10dab673c | SURVIVED | — |
| MK3-drop-verify-union | drop the verify-mode finding union on item-2 refusals | f928a4a8 | SURVIVED | — |
| MK4-positive-only-PASS | PASS iff the positive group is full | 5167a4e0 | SURVIVED | — |
| MK5-drop-CLEAN | drop `RESEARCH_GATE: CLEAN` from the pass-row test | 211e47bf | SURVIVED | — |
| MK6-refuse-rc-only | refusal needs only rc 1 (finding id ignored) | b2f997f4 | SURVIVED | — |
| MK7-refuse-accepts-rc0 | refusal accepts rc 0 when the finding id is printed | a5d03668 | SURVIVED | — |
| MK8-drop-positive-group | drop the positive group from the PASS formula | 73be9ae9 | SURVIVED | — |
| MK9-one-runline-ok | PASS with only one Run line found | 05819cf0 | SURVIVED | — |
| MK10-hold-only-PASS | PASS iff the hold group is full | 06e1ea76 | killed | c1-k0-donothing FAIL→PASS (`K2_GATE=PASS`, rc 0 where the base gate scores `K2_REFUSED=0/11 CLASS_REFUSED=2/24`) |
| MK11-accept-every-row | every manifest row scored ok | 26f432fd | killed | c1-k0-donothing, c1-f1-blanket-refuse, c1-f2-wrong-finding-keyed, all FAIL→PASS |

Tally: 9 survived / 11. The two kills are the only mutations that make the counter PASS a control that must FAIL.
Every *row-level* weakening survives, because the battery's only C1 data points are four FAIL-expected trees.

Landing re-certification — `python3 -B mutcounters/<mutant>.py --root <landing tree>` (the mutated counter run
against the landed bytes; receipt `method/counter-mutants-landing.json`): **10 of 11 mutants still print the exact
landing line** `RUNLINES=2/2 K2_REFUSED=11/11 HOLD_REFUSED=9/9 CLASS_REFUSED=24/24 POSITIVE=6/6`, `K2_GATE=PASS`,
rc 0. Only MK3 (drop the verify-mode union) fails at landing: `HOLD_REFUSED=7/9`, `K2_GATE=FAIL`, rc 1. So the
landing artifact pins exactly one check of the eleven, the control battery pins the PASS-formula totality (MK10,
MK11), and eight weakenings (FROZEN_RUNLINE, rc-2, CLEAN string, finding-id, rc-0, positives group, positives-only
PASS, one-Run-line) are pinned by neither.

## B2. C2 counter `depth-r82.py` — 11 mutants

| mutant | mutation | commit | verdict | killer control(s) |
|---|---|---|---|---|
| MD1-drop-E3-capture | quote need not occur in the capture | 8ed51f7a | killed | c2-d2-fabricated-quotes FAIL→PASS (`DEPTH_R82=PASS`, rc 0; rows=5 quotes=5/5) |
| MD2-drop-ROUND_START | drop the refetch freshness floor | b3ed8854 | SURVIVED | — (c2-d3 still fails E3,E4,E6,E7) |
| MD3-drop-E6 | drop coverage | ec3b41b2 | SURVIVED | — |
| MD4-drop-E5 | drop content checks | 23dbd478 | killed | c2-d4-duplicate-cells, c2-d6-placeholder-cells FAIL→PASS |
| MD5-drop-E4 | drop novelty | 3880cfa2 | SURVIVED | — |
| MD6-row-floor-1 | body-row floor 5 → 1 | f98fdfd6 | killed | c2-d5-four-rows FAIL→PASS (`rows=4`, `DEPTH_R82=PASS`, rc 0) |
| MD7-drop-E7 | drop new-ground | 9f301ac9 | SURVIVED | — |
| MD8-drop-E2 | drop warrant→quote linkage | 26fa01c7 | SURVIVED | — |
| MD9-E5-drop-duplicate-half | keep word/placeholder, drop duplicate-row check | f3615f01 | killed | c2-d4-duplicate-cells FAIL→PASS |
| MD10-E5-drop-placeholder-half | keep duplicate-row check, drop word/placeholder | f1016b05 | killed | c2-d6-placeholder-cells FAIL→PASS |
| MD11-drop-warrant-column | E1 need not carry a `Warrant` column | 8e9719e7 | SURVIVED | — |

Tally: 5 killed / 11. E3, E5 (both halves), the row floor are pinned; E2, E4, E6, E7, the `Warrant` column and the
`ROUND_START` freshness floor are not.

Landing re-certification — same command shape with the mutated `depth-r82.py`: **all 11 mutants still print**
`DEPTH_R82 entries=1 ok_entries=1 rows=9 located_quotes=11 fresh_sources=4`, `DEPTH_R82=PASS`, rc 0. The landed
entry does not exercise any single check in the rejecting direction, so none of the eleven weakenings changes the
landing verdict; six (E2, E4, E6, E7, `Warrant` column, `ROUND_START`) are also invisible to the control battery.

---

## C. Restoration evidence

- Gate trees: every probe restored `tools/research-gate.sh` from the pristine bytes and asserted sha256
  `0d8ac50f2695b8df9300905dd44ea70668dd047912633226f8bababe7570d92a` (harness `gate_mutants.py` /
  `capture_survivors.py` / `witnesses.py`; the selftest runs report `restored_ok: true`,
  `selftest-MG09.json`, `selftest-MG21.json`). The untouched root extraction still hashes to `0d8ac50f…`.
- Counter fixture: each mutant is a commit of `repo38`; after the last probe the tree was restored to the pristine
  counters and the restore committed — worktree sha256 `4d6ba055…` (`k2-gate-r82.py`) and `726d3ed9…`
  (`depth-r82.py`), base gate `d5d48128…`, `git status --porcelain` empty, HEAD `d74684b2` (`restore counter after
  MK10/MK11`). `repo38` base commit `04bff4f9` is the `38f5af82` tree; per-mutant commit shas in
  `counter-mutants.tsv`.
- The lane repo itself was only read (`git archive`); no commit, branch or index was touched.

## D. What this means for the frozen evidence (coverage findings, no kill-rule firing)

1. **CG-1 (C1 manifest, value folding).** The manifest pins the placeholder *values* (n/a, none, tbd, unknown, ?,
   emdash, period stripping, backticks) but not the quote / `*` / `_` folds. A gate missing any of those folds
   passes `K2_GATE=PASS` at landing and scores 24/24 class rows; witnessed W1–W4. K2 (a)/(b) forms that the frozen
   counting command would mis-count as refused.
2. **CG-2 (C1 manifest, negative-resolution arms).** No manifest row exercises `SW_CLAIMS[cid]`, `SW_IDS[cid]` or
   the sweep-cell token match in the *accepting* direction: the positives resolve through `SW_CLAIMS`, so dropping
   either other arm is invisible (MG14/MG15/MG16 survived). The effect is false refusals of well-formed records
   (W5–W7), i.e. K3-harm, not a K2 pass.
3. **CG-3 (C1 counter, control battery).** The four frozen C1 controls are all FAIL-expected; they kill a counter
   only when it emits PASS. Nine of eleven internal weakenings survive. The battery does not pin `FROZEN_RUNLINE`,
   rc-2 handling, the verify union, the CLEAN string, finding-id matching, rc-0 refusals, the pass formula's group
   set, or the Run-line count.
4. **CG-4 (C2 counter, control battery).** E2/E4/E6/E7, the `Warrant` column and the freshness floor have no
   isolating control; six of eleven weakenings survive. Note the E5 halves are each individually load-bearing
   (d4 kills one, d6 the other).
5. **CG-5 (selftest vs manifest).** The selftest's five new cases catch MG21 (annotation text) but not the
   quote-fold gap (MG09); the counting command catches neither. The two detectors are complementary, and neither
   is complete for the K2 vocabulary it claims.
6. **CG-6 (landing re-certification of the counters).** Run against the landed bytes, the mutated counters keep
   printing the landing predicate: 10/11 k2-gate mutants (`K2_GATE=PASS`, rc 0 — only MK3's verify-union drop
   fails, `HOLD_REFUSED=7/9`) and 11/11 depth mutants (`DEPTH_R82=PASS`, rc 0). The landing predicate therefore
   pins at most one of the twenty-two checks; the control battery pins a further three (k2 PASS-formula totality,
   depth E3/E5/row-floor). The remaining checks are pinned by neither the landing artifact nor the controls.

No kill rule of `corpus/evidence/round82/claims.md` fired in this seat: the landed bytes were never modified, the
landing counting commands print the exact target fractions (C1 `11/11 9/9 24/24 6/6`, PASS, rc 0; C2
`entries=1 ok_entries=1 rows=9 located_quotes=11 fresh_sources=4`, PASS, rc 0), and every mutant was restored.

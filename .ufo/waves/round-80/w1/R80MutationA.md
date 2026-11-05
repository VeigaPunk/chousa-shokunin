# Wave 1 seat R80MutationA — mutation test of the round-80 instruments

Seat: `R80MutationA` (mutation-tester, leaf). Round 80, lane `chousa`.
Base revision `b7803829922770b890e9f4efdd30d12c3695439a`; frozen claim set read first
(`corpus/evidence/round80/claims.md`, C1 operability / C2 calibration); the non-author closure of
round 79 (`corpus/lessons/round-79-verifier-spotcheck.md`) read before scoring.

Instrument bytes measured (committed bytes; `git show <rev>:<path> | sha256sum`, unchanged at the
lane's landed tip `e3820839d67e44d1344c8dd4730b16b5fd39b706`):

| instrument | sha256 |
|---|---|
| `corpus/evidence/round80/gate-grounding-check.py` | `d9e426216665a098cd90adf8fbf5e5dd62e02dc7b5b707c322b404b3eb55c553` |
| `corpus/evidence/round80/matrix-battery-v7.py` | `35351b2328bb6a284da13e61240a6ec598f39a148b8d8948d4e3d60dd78d914d` |

**Result.** Instrument 1 `7/8` mutants killed; instrument 2 `3/5` killed deterministically, `1/5`
killed only stochastically, `1/5` survived. Three defects in the *pristine* bytes were found while
mutation-testing them (F1, F2, F3 below), one of which makes the C1 counting command fail its own
frozen predicate on the legitimate matrix in 1 of 5 measured runs.

Everything below ran in `/fast/scratch/hyaku/chousa-r80/R80MutationA/` (`git clone --shared` of the
lane; every fixture commit made in that clone after asserting `git rev-parse --show-toplevel` printed
it). No lane, fleet or frozen artifact was written; no network; nothing installed (no pacman
transaction, no `uv tool`, no PATH directory touched). Scratch deleted before yield; every receipt
cited is copied under `.ufo/waves/round-80/w1/R80MutationA/` and hashed in
`MANIFEST.txt` (84 files).

## 1. What a mutant can and cannot show here

A mutant that no detector can kill is decoration. So each mutant is a single behaviour-bearing edit
to the instrument, and the detector is the instrument's own declared counting command run on a state
whose correct verdict is known independently:

* instrument 1 — `python3 -B corpus/evidence/round80/gate-grounding-check.py --rev <state>`;
* instrument 2 — `python3 -B corpus/evidence/round80/matrix-battery-v7.py --matrix <M> --work <W>
  --runs 1 --fresh <N> --rev <state>`, with `M` = the legitimate matrix, the round-79
  structure-identity oracle, and (for one probe) a mark-blind matrix built by this seat.

Killed = the mutant's `(exit code, predicate line)` differs from the pristine instrument's on a state
where the pristine instrument is known correct. A mutant that only fails the *clean* state is killed
by the positive control (it is a broken instrument, not a hole).

## 2. Fixture for instrument 1

The counter reads committed bytes only (`git show <rev>:<path>`), so states are commits.

The lane has since landed the real AFTER state — `e3820839` carries
`corpus/lessons/round-80.md` with four `GATE-RECORD` lines (S199–S202) and registry rows
`S200/S201/S202` whose `teaches` cells open `supersedes S196/S197/S198`. So the primary grid runs on
**committed AFTER bytes**, with one defect per extra commit:

| state | revision (scratch clone) | the one defect |
|---|---|---|
| `real-clean` | `e3820839…` | none — the landed C2 state |
| `real-tree-rev` | `35df8929…` | S201 `rev=` is a **tree** object of the base commit |
| `real-prefix-rev` | `531daa92…` | S201 `rev=` = base 12-hex prefix + 28 zeros |
| `real-absent-quote` | `312fa533…` | S201 `quote=` is a 25-word string absent from line 1054 |
| `real-off-by-one` | `a43e4ae4…` | S201 `line=1055` (the true line is 1054) |
| `real-wordcount` | `7f6aa835…` | S201 `words=24` (the quote is 25 words) |
| `real-bound-27` | `00c7112c…` | S201 quote is a 27-word substring, `words=27` |
| `real-no-record` | `c2731774…` | S201's `GATE-RECORD` line deleted |
| `real-tip-defect` | `baa3c8ce…` | S199 (an audited tip with no superseder) quote altered |

Each defect was verified to trip exactly the rule it targets under the pristine counter (predicate
lines in `grounding-real/PRISTINE.txt`, lines 16–104). A first synthetic AFTER fixture (four records
built by this seat on the freeze commit) gave the identical grid; it is kept as
`fixture/round-80.after-clean.md` + `summary-grounding.txt` for the record.

Pristine on `real-clean`:

```
grounding-real/PRISTINE.txt:16  exit=0
GATE_GROUNDING=PASS unresolved=0 superseded_resolved=3 audited=S199,S200,S201,S202
```

that is the frozen C2 predicate, on committed bytes, run by this seat.

## 3. Instrument 1 — 8 mutants, 7 killed

Mutant sources (full bytes, sha256 in `MANIFEST.txt`): `mutants/m80-M*.py`.

Exit grid (0 = printed `GATE_GROUNDING=PASS`, 1 = `FAIL`); full predicate lines per cell in
`summary-grounding-real.txt`, per-instrument receipts in `grounding-real/<mutant>.txt`:

| mutant | clean | tree | prefix | absent | off1 | words | b27 | norec | tip |
|---|---|---|---|---|---|---|---|---|---|
| PRISTINE | 0 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 |
| M1 r1-drop | 0 | **0** | 1 | 1 | 1 | 1 | 1 | 1 | 1 |
| M2 prefix-resolves | 0 | **0** | **0** | 1 | 1 | 1 | 1 | 1 | 1 |
| M3 r3-substring-skip | 0 | 1 | 1 | **0** | **0** | 1 | 1 | 1 | **0** |
| M4 line-off-by-one | **1** | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 |
| M5 words-equality-drop | 0 | 1 | 1 | 1 | 1 | **0** | 1 | 1 | 1 |
| M6 bound-drop | 0 | 1 | 1 | 1 | 1 | 1 | **0** | 1 | 1 |
| M7 audited-empty | **0** | 1 | 1 | 1 | 1 | 1 | 1 | 1 | **0** |
| M8 r2-drop | 0 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 |

**Score 7/8.** Per-mutant evidence (receipt, line, exit, observed predicate line):

| mutant | detector state | receipt | observed |
|---|---|---|---|
| M1 (drop R1 `cat-file -e`) | `real-tree-rev` | `grounding-real/M1-r1-drop.txt:27` | exit 0, `PASS unresolved=0 superseded_resolved=3 audited=S199,S200,S201,S202`; the `ROW S201` line records `location=corpus/QUALITY.md:1054@8bff97f2…` — a **tree**, never a commit |
| M2 (12-hex prefix resolves) | `real-tree-rev`, `real-prefix-rev` | `grounding-real/M2-prefix-resolves.txt:27`, `:38` | exit 0 both; the prefix is resolved to the full rev and the record then audits clean |
| M3 (skip R3 substring) | `real-absent-quote`, `real-off-by-one`, `real-tip-defect` | `grounding-real/M3-r3-substring-skip.txt:49`, `:60`, `:104` | exit 0; a quote that occurs nowhere on the named line is scored `record=ok` |
| M4 (`idx = line` not `line-1`) | `real-clean` (positive control) | `grounding-real/M4-line-off-by-one.txt:16` | exit 1, `FAIL unresolved=7` on correct records — the mutant is a broken instrument, killed by the fixture |
| M5 (drop `words != int(...)`) | `real-wordcount` | `grounding-real/M5-words-equality-drop.txt:71` | exit 0 while the record states 24 and the quote holds 25 |
| M6 (drop `words > 25`) | `real-bound-27` | `grounding-real/M6-bound-drop.txt:82` | exit 0 with a 27-word quote |
| M7 (every row superseded) | `real-tip-defect`, `real-clean` | `grounding-real/M7-audited-empty.txt:68`, `:12` | exit 0, `PASS unresolved=0 superseded_resolved=3 audited=` — an ungrounded audited tip, and the audit set empty |
| M8 (drop R2) | — | `grounding-real/M8-r2-drop.txt` | identical to pristine on all nine states — **survived** |

## 4. Instrument 2 — 5 mutants, 3 killed deterministically

Mutant sources: `mutants/v7-N*.py`. Detectors: `corpus/evidence/round76/loader-matrix-v3.py`
(legit), `.ufo/waves/round-79/w1/R79ExecC/matrix-structure-identity.py` (oracle), and
`mutants/probe-mark-blind.py` (this seat's matrix: the real matrix's exit codes, always-full marks).
All runs use `--runs 1 --fresh 2` unless the receipt name says `fresh0`. Every run's full stdout is in
`v7/<label>.txt`; the tabulated form is `summary-v7.txt`.

Baselines measured by this seat (the round's control `controls/v7-legit-matrix-after.txt` is one run;
I ran five legitimate-matrix and seven oracle runs):

| baseline | runs | `BATTERY=PASS` | receipt |
|---|---|---|---|
| pristine × legit | 5 | 4 | `v7/pristine-legit.txt:221` exit 0; `v7/pristine-legit-rep1.txt:221` exit **1** |
| pristine × structure-identity oracle | 7 | **0** | `v7/pristine-oracle.txt:221` … `v7/pristine-oracle-rep6.txt:221`, all exit 1 |

| mutant | legit matrix | structure-identity oracle | verdict |
|---|---|---|---|
| N1 no fresh leg | exit 1, `fresh_positive=0/0 fresh_forgers=0/0 … oracles_rejected=4/5` (`v7/N1-no-fresh-leg\|legit.txt:173`) | exit 1 (`…\|oracle.txt:173`) | **killed** — the predicate cell collapses to `0/0` and the payload-decode oracle stops being rejected without the fresh leg |
| N2 one draw reused per group | exit 1 `fresh_positive=0/2 fresh_forgers=0/2` (`…\|legit.txt:173`) | **exit 0, `BATTERY=PASS … fresh_positive=2/2 fresh_forgers=2/2`** in 3 of 10 runs (`…\|oracle-rep6.txt:221`, `rep7:221`, `oracle.txt:221`) | **live hole** — the PASS line is reachable by the oracle, not reproducibly: 7 of 10 oracle runs still print FAIL |
| N3 accept an oracle that reaches PASS | exit 1 (`…\|legit.txt:173`) | exit 1 with `--fresh 2` (`…\|oracle.txt:173`), but **exit 0 `BATTERY=PASS` with `--fresh 0`** (`v7/N3-oracle-blind\|oracle-fresh0.txt:173`) | **killed** (fresh-0 probe is deterministic; with `--fresh 2` the fresh leg masks it) |
| N4 score only exit codes | exit 1 *only* because the fresh draw collided (`…\|legit.txt:173`) | exit 1, byte-identical line to pristine (`v7/N4-exit-code-only\|oracle.txt:221` vs `v7/pristine-oracle-rep1.txt:221`) | **survived** — no mandated detector separates it |
| N5 verdict ignores fresh counts | exit 0 `PASS` with `fresh_positive=1/2 fresh_forgers=1/2` (`…\|legit.txt:221`) | **exit 0 `BATTERY=PASS` with `fresh_positive=0/2`** (`v7/N5-verdict-ignores-fresh\|oracle.txt:221`) | **killed** — the oracle reaches the PASS line deterministically |

**Score 3/5 deterministic** (N1, N3, N5). N2 is killed only sometimes — it is the one mutant whose
defect is exactly the channel that hands the oracle the PASS line, and the oracle is a committed
artifact, so this is a finding, not a pass.

The mark-blind probe (a matrix that returns the legitimate matrix's exit codes while printing twelve
`PASS` case lines and `LOADER_MATRIX=12/12 MATRIX=PASS`) is refused by the pristine battery —
`v7/pristine-markblind|fresh0.txt:173` exit 1, `forgers_rejected=0/11` — because the forger clause
requires *fewer than full marks*. Under N4 the same matrix is scored `forgers_rejected=11/11`
(`v7/N4-exit-code-only\|markblind-fresh0.txt:173`) and only the oracle leg still refuses it (4/5).
So the marks clauses are load-bearing for the printed counts, not for the exit code (F2).

## 5. Findings

**F1 — (C1, blocking-class) the fresh leg's results are keyed by subject name, and the name space is
not disjoint across groups.** `score()` builds `results = {name: []}` and the fresh names are
`f"{base_name}#{i}"` for both groups, so when the fresh positive and the fresh forger of index `i`
are drawn from the same base they collide: both entries are scored from one pooled observation list
and both MISS. The legitimate matrix then prints `fresh_positive=1/2 fresh_forgers=1/2` and exits 1.

*Command*: `python3 -B corpus/evidence/round80/matrix-battery-v7.py --matrix
corpus/evidence/round76/loader-matrix-v3.py --work <scratch> --runs 1 --fresh 2 --rev 0b2494f7…`
*Receipt*: `v7/pristine-legit-rep1.txt` — line 11 `MATRIX RUN FORGER ref-counter#1 … matrix_exit=1
marks=8/12/FAIL`, line 12 `MATRIX RUN POSITIVE ref-counter#1 … matrix_exit=0 marks=12/12/PASS`, line
42 `MATRIX SUBJECT POSITIVE ref-counter#1 MISS`, line 221
`BATTERY=FAIL forgers_rejected=11/11 positive=2/2 fresh_positive=1/2 fresh_forgers=1/2
oracles_rejected=5/5`, line 222 `# exit: 1`.
Observed rate: 1 of 5 pristine legitimate runs (the other four print the exact frozen predicate,
`v7/pristine-legit.txt:221`, exit 0). A correct matrix therefore fails the C1 counting command's own
predicate on some runs — the draw is not scored per subject, it is scored per name.

**F2 — (C1) the marks half of the forger clause is not exercised by the enumerated set, so
exit-code-only scoring is indistinguishable on both mandated detectors.** N4 (score only exit codes)
is indistinguishable from pristine on the legitimate matrix and on the structure-identity oracle
(`v7/N4-exit-code-only|oracle.txt:221` equals `v7/pristine-oracle-rep1.txt:221` line for line). It takes
a matrix that exits 1 while claiming `12/12 MATRIX=PASS` — `mutants/probe-mark-blind.py` — to make the
marks clause bite at all: pristine refuses that matrix as `forgers_rejected=0/11`
(`v7/pristine-markblind|fresh0.txt:173`), N4 counts it `11/11`
(`v7/N4-exit-code-only|markblind-fresh0.txt:173`) and is still refused only by the oracle leg. So the
clause is live code, but no *enumerated* subject can distinguish it, so N4 survives every detector
built from the committed subject set; its difference appears only on a matrix this seat had to build.

**F3 — (C1) the verdict ignores two of the four counted groups under N5, and the structure-identity
oracle then reaches the PASS line.** The docstring's RECEIPT LEG says the verdict is bound to the exit
code; the fresh counts are not in it (`v7/N5-verdict-ignores-fresh|oracle.txt:221` exit 0,
`fresh_positive=0/2`). The frozen predicate line catches this, the exit code does not — i.e. the
"verdict bound to the exit code" is a claim about the *line*, not about the process status.

**F4 — (C2) R2 is strictly redundant with R3, hence unkillable.** No input distinguishes
`mutants/m80-M8-r2-drop.py` from pristine over nine states (`grounding-real/M8-r2-drop.txt`). An
absent path yields `text is None` → `""` → zero lines → R3's range check fires. R2 is observability
(its message names the path), not a scored guard; a record that names an absent path is reported
under R3 when R1 is dropped (M1 on `real-prefix-rev`, `grounding-real/M1-r1-drop.txt:33`).

**F5 — (C2) R1's failure message is wrong for the hole it closes.** M1 accepts a **tree** object and
prints `record=ok … @8bff97f27d98` (`grounding-real/M1-r1-drop.txt:22`); the pristine counter refuses
it with `R1 revision 8bff97f27d98 does not resolve` (`grounding-real/PRISTINE.txt:22`) — but a tree
rev *does* resolve; it is simply not a commit. The guard holds; the sentence a reader sees is false
about the reason.

**F6 — (C2) `audited=` is the only cell that kills M7.** Under M7 an ungrounded audited tip prints
`GATE_GROUNDING=PASS unresolved=0 superseded_resolved=3 audited=` (`grounding-real/M7-audited-empty.txt:68`).
Two of the three cells the C2 predicate names (`PASS unresolved=0 superseded_resolved=3`) are
satisfied; only the fourth (`audited=S199,S200,S201,S202`) refuses it. The counter is correct as
written and the frozen predicate as written is what kills the mutant — recorded so nobody narrows the
predicate to the first three cells.

**F7 — (C1, observation) the C1 predicate is a per-run observation, not a property of the matrix.**
Among the five pristine legitimate runs, `fresh_positive` was `2/2` four times and `1/2` once — the
once being F1's name collision. The frozen predicate `fresh_positive=2/2 fresh_forgers=2/2` therefore
holds per run, not per matrix; the round's control receipt is one sample of a distribution that
includes FAIL. Any future closure sentence of the form "v7 accepts the legitimate matrix" needs a run
count, not a single receipt.

## 6. Mutation scores

| instrument | mutants | killed | killed only stochastically | survived |
|---|---|---|---|---|
| `gate-grounding-check.py` (`d9e42621…`) | 8 | **7** (M1–M7) | 0 | 1 (M8, F4) |
| `matrix-battery-v7.py` (`35351b23…`) | 5 | **3** (N1, N3, N5) | 1 (N2 — the fresh-draw channel; the oracle printed the PASS line in 3 of 10 runs) | 1 (N4, F2) |

Reading: the C2 counter's four declared rules are all live — each has a mutant that only its own check
kills, and the clean state is only reachable with every rule intact. The C1 battery's *oracle*
protection is live (7/7 pristine refusals, N3 and N5 provably break it); its *subject scoring* is not
uniformly live: the marks clauses (F2) and the fresh-draw independence (N2) can be removed without any
mandated detector noticing, and its own name key (F1) can fail the legitimate matrix.

## 7. Limits of this seat's evidence

* The frozen predicate cells are compared on the printed line and the exit code; I did not evaluate
  whether the *subjects* the fresh leg draws are semantics-preserving (that is the critic/labrat
  channel, recorded in the round's limits).
* Instrument 1's primary grid is on the landed AFTER bytes (`e3820839`); if the lane lands further
  edits to `corpus/lessons/round-80.md` the defect commits no longer reproduce byte-for-byte — the
  copied fixtures under `fixture/` keep the exact inputs.
* Ten of the 36 v7 detector receipts are repetitions of two baselines (five legitimate-matrix runs,
  seven oracle runs, counting the first of each); they exist to measure the draw's variance and are
  cited as such, not as independent confirmations.
* Some receipts in this folder were committed by the lane mid-flight (`b20af227` landed the w1
  folder while this seat was still running), so a handful show as worktree modifications. This seat
  wrote only this folder and never committed; `MANIFEST.txt` hashes the current worktree bytes, which
  are the authoritative receipts.
* No tool was installed or upgraded, so there is no tooling line to record.

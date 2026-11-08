# R91ExecC1Repro — C1 reproduced from a clean tree at carrier C3

Seat `R91ExecC1Repro`, claim **C1 (operability)**. Attacked tree: a `git clone --shared` of the lane checked out at
`67954adc599bd605705d94a1ea7abb582491a907` (carrier C3). Freeze `F` = `4d00d7519290569879f853d7122b82a927cda1f3`.
Scratch `/fast/scratch/hyaku/chousa-r91/R91ExecC1Repro/` (deleted at yield). No production edit, no lane/fleet
git/jj mutation, no network, no `pacman`, no tool installed.

The lane working tree is at `0c85c9ace7bcd611b3e3299e8868f5af71da9732` (HEAD), not C3; the attacked tree is the
clone. The C1 read-base files are byte-identical between the two for the paths that matter, so the dual-base runs
read C3 bytes:

```
control-driver-r91.py  live=49102204fa9698df97f2f8ac467468ee57dff1a358e934d52654821cd880b40c  clone=same
controls/expected.tsv  live=f62921b60ceed00fe147350d433c16fe18a17c00af369e7416030592f06562d7  clone=same
instrument-pins.txt    live=b3908ee2a24a13ca592b5aa01c6bc28b186cd4059a39371fd08b0301c5b169ac  clone=same
nine receipts under controls/receipts/: all nine hashes identical live vs clone
```

Revisions and hashes are in `receipts/revs.txt`.

## Summary

| step | command (cwd `$S/repo` unless stated) | exit | key observed line |
|---|---|---|---|
| a | `python3 -B corpus/evidence/round91/control-driver-r91.py verify --root . --repo . --rev 4d00d751… --receipts-rev 67954adc… --work $S/verify` | **0** | `COMMITTED_OK=6/6 EXACT_OK=6/6 PIN_OK=6/6 FRESH_OK=6/6 PINNED_FILES=6 CONTROL_DRIVER_R91=PASS` |
| b | `python3 -B corpus/evidence/round91/control-forgeries-r91.py --work $S/forge` | **0** | `FORGERY_REFUSED=6/6 PRIOR_ACCEPTED=6/6 POSITIVE=pass` |
| c, as literally written | the (a) script path is clone-relative: `python3 -B corpus/…/control-driver-r91.py verify --root /home/vgpnk/Projects/shokunin/chousa-shokunin --repo $S/repo …` | **1** | `… PINNED_FILES=5 CONTROL_DRIVER_R91=FAIL` (INSTRUMENT_UNPINNED + SELF_DRIFT over 11 root-escaping paths) |
| c, lane-resident driver | `python3 -B /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/…/control-driver-r91.py verify --root /home/vgpnk/Projects/shokunin/chousa-shokunin --repo $S/repo …` | **0** | `RECEIPT SELF_PIN OK rev=4d00d751… receipts_rev=67954adc…` + `CONTROL_DRIVER_R91=PASS` |
| d | `sha256sum corpus/evidence/round91/controls/receipts/*.txt` before/after (a) | diff **0** | 9/9 hashes identical; no new file |

Step (c) as literally written **does not pass**; the same dual-base triple with the driver taken from the
read-base tree **does pass**. Finding F1 below gives the exact lines, the isolation run and the code cause.

## (a) frozen counting command on a clean clone at C3 — PASS, exit 0

Command:

```
cd /fast/scratch/hyaku/chousa-r91/R91ExecC1Repro/repo
python3 -B corpus/evidence/round91/control-driver-r91.py verify \
  --root . --repo . \
  --rev 4d00d7519290569879f853d7122b82a927cda1f3 \
  --receipts-rev 67954adc599bd605705d94a1ea7abb582491a907 \
  --work /fast/scratch/hyaku/chousa-r91/R91ExecC1Repro/verify
```

Full stdout (receipt `receipts/a-verify-both-bases-clean-clone.stdout`, exit code in `receipts/run-log.txt`):

```
BASES root=/fast/scratch/hyaku/chousa-r91/R91ExecC1Repro/repo repo=/fast/scratch/hyaku/chousa-r91/R91ExecC1Repro/repo
RECEIPT c1-gate-r89 OK committed+exact+pin+fresh
RECEIPT c1-mutants-r89 OK committed+exact+pin+fresh
RECEIPT c1-harm OK committed+exact+pin+fresh
RECEIPT c1-harm-setup OK committed+exact+pin+fresh
RECEIPT c2-prior-landing OK committed+exact+pin+fresh
RECEIPT c2-prior-controls OK committed+exact+pin+fresh
RECEIPT PINS OK 6/16 pinned files byte-identical
RECEIPT SELF_PIN OK rev=4d00d7519290569879f853d7122b82a927cda1f3 receipts_rev=67954adc599bd605705d94a1ea7abb582491a907
COMMITTED_OK=6/6 EXACT_OK=6/6 PIN_OK=6/6 FRESH_OK=6/6 PINNED_FILES=6 CONTROL_DRIVER_R91=PASS
```

Exit **0**. The frozen expected line (`COMMITTED_OK=6/6 EXACT_OK=6/6 PIN_OK=6/6 FRESH_OK=6/6`) and the required
`RECEIPT SELF_PIN OK rev=… receipts_rev=…` line are both present. The extra token `PINNED_FILES=6` sits between
`FRESH_OK=6/6` and `CONTROL_DRIVER_R91=PASS`; the claim's sentence does not forbid it. `6/16` is the count of the
six required files (five distinct row instruments after `c1-harm`/`c1-harm-setup` dedupe, plus `expected.tsv`)
checked against a 16-row `instrument-pins.txt`; it is not a partial pin pass.

## (b) forgery battery — PASS, exit 0

Command:

```
cd /fast/scratch/hyaku/chousa-r91/R91ExecC1Repro/repo
python3 -B corpus/evidence/round91/control-forgeries-r91.py \
  --work /fast/scratch/hyaku/chousa-r91/R91ExecC1Repro/forge
```

Full stdout (receipt `receipts/b-forgeries.stdout`):

```
OK dup-header-exit: r91 rc=1 (HEADER_DUPLICATE:exit), r90 rc=0
OK dup-header-computed: r91 rc=1 (HEADER_DUPLICATE:computed_against), r90 rc=0
OK instrument-stub: r91 rc=1 (INSTRUMENT_PIN_MISMATCH:fx-tool.sh), r90 rc=0
OK expected-swap: r91 rc=1 (INSTRUMENT_PIN_MISMATCH:expected.tsv), r90 rc=0
OK missing-expected_exit: r91 rc=1 (MISSING_HEADER:expected_exit), r90 rc=0
OK extra-receipt: r91 rc=1 (UNSCORED_RECEIPT), r90 rc=0
OK positive: r90 rc=0 r91 rc=0
FORGERY_REFUSED=6/6 PRIOR_ACCEPTED=6/6 POSITIVE=pass
```

Exit **0**. All six classes refused by r91, accepted by the unchanged r90 driver, pristine fixture accepted by both.

## (c) the QUALITY-202 dual-base form — literal command FAILS, lane-driver form PASSES

### (c-literal) exactly as the seat spec writes it, run from `$S/repo`

Because the script path is relative and the cwd is `$S/repo`, this executes the **clone's** driver while `--root`
names the lane. Command:

```
cd /fast/scratch/hyaku/chousa-r91/R91ExecC1Repro/repo
python3 -B corpus/evidence/round91/control-driver-r91.py verify \
  --root /home/vgpnk/Projects/shokunin/chousa-shokunin \
  --repo /fast/scratch/hyaku/chousa-r91/R91ExecC1Repro/repo \
  --rev 4d00d7519290569879f853d7122b82a927cda1f3 \
  --receipts-rev 67954adc599bd605705d94a1ea7abb582491a907 \
  --work /fast/scratch/hyaku/chousa-r91/R91ExecC1Repro/verify2
```

Full stdout (receipt `receipts/c-literal-command.stdout`), exit **1**:

```
BASES root=/home/vgpnk/Projects/shokunin/chousa-shokunin repo=/fast/scratch/hyaku/chousa-r91/R91ExecC1Repro/repo
RECEIPT c1-gate-r89 OK committed+exact+pin+fresh
RECEIPT c1-mutants-r89 OK committed+exact+pin+fresh
RECEIPT c1-harm OK committed+exact+pin+fresh
RECEIPT c1-harm-setup OK committed+exact+pin+fresh
RECEIPT c2-prior-landing OK committed+exact+pin+fresh
RECEIPT c2-prior-controls OK committed+exact+pin+fresh
RECEIPT PINS FINDING INSTRUMENT_UNPINNED:../../../../../fast/scratch/hyaku/chousa-r91/R91ExecC1Repro/repo/corpus/evidence/round91/controls/expected.tsv
RECEIPT SELF_PIN FINDING SELF_DRIFT ../../../../../fast/scratch/hyaku/chousa-r91/R91ExecC1Repro/repo/corpus/evidence/round91/control-driver-r91.py@4d00d7519290569879f853d7122b82a927cda1f3,../../../../../fast/scratch/hyaku/chousa-r91/R91ExecC1Repro/repo/corpus/evidence/round91/controls/expected.tsv@4d00d7519290569879f853d7122b82a927cda1f3,../../../../../fast/scratch/hyaku/chousa-r91/R91ExecC1Repro/repo/corpus/evidence/round91/controls/receipts/c1-before.txt@67954adc599bd605705d94a1ea7abb582491a907,../../../../../fast/scratch/hyaku/chousa-r91/R91ExecC1Repro/repo/corpus/evidence/round91/controls/receipts/c1-gate-r89.txt@67954adc599bd605705d94a1ea7abb582491a907,../../../../../fast/scratch/hyaku/chousa-r91/R91ExecC1Repro/repo/corpus/evidence/round91/controls/receipts/c1-harm-setup.txt@67954adc599bd605705d94a1ea7abb582491a907,../../../../../fast/scratch/hyaku/chousa-r91/R91ExecC1Repro/repo/corpus/evidence/round91/controls/receipts/c1-harm.txt@67954adc599bd605705d94a1ea7abb582491a907,../../../../../fast/scratch/hyaku/chousa-r91/R91ExecC1Repro/repo/corpus/evidence/round91/controls/receipts/c1-mutants-r89.txt@67954adc599bd605705d94a1ea7abb582491a907,../../../../../fast/scratch/hyaku/chousa-r91/R91ExecC1Repro/repo/corpus/evidence/round91/controls/receipts/c2-before.txt@67954adc599bd605705d94a1ea7abb582491a907,../../../../../fast/scratch/hyaku/chousa-r91/R91ExecC1Repro/repo/corpus/evidence/round91/controls/receipts/c2-prior-controls.txt@67954adc599bd605705d94a1ea7abb582491a907,../../../../../fast/scratch/hyaku/chousa-r91/R91ExecC1Repro/repo/corpus/evidence/round91/controls/receipts/c2-prior-landing.txt@67954adc599bd605705d94a1ea7abb582491a907,../../../../../fast/scratch/hyaku/chousa-r91/R91ExecC1Repro/repo/corpus/evidence/round91/controls/receipts/c3-before.txt@67954adc599bd605705d94a1ea7abb582491a907
COMMITTED_OK=6/6 EXACT_OK=6/6 PIN_OK=6/6 FRESH_OK=6/6 PINNED_FILES=5 CONTROL_DRIVER_R91=FAIL
```

`BASES root=… repo=…` does name both bases. The eleven `SELF_DRIFT` entries are exactly the driver, the
expectations file and the nine receipt files; every entry is prefixed `../../../../../fast/…`, i.e. it escapes
`--root`.

### (c-intent) same triple, driver taken from the read-base tree — PASS, exit 0

This is the exact command shape of R90SentinelScope F3 (`python3 -B <lane>/corpus/evidence/round90/control-driver-r90.py
verify --root <lane> --repo <clone>`), now with the r91 driver:

```
cd /fast/scratch/hyaku/chousa-r91/R91ExecC1Repro/repo
python3 -B /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round91/control-driver-r91.py verify \
  --root /home/vgpnk/Projects/shokunin/chousa-shokunin \
  --repo /fast/scratch/hyaku/chousa-r91/R91ExecC1Repro/repo \
  --rev 4d00d7519290569879f853d7122b82a927cda1f3 \
  --receipts-rev 67954adc599bd605705d94a1ea7abb582491a907 \
  --work /fast/scratch/hyaku/chousa-r91/R91ExecC1Repro/verify-c2
```

Full stdout (receipts `receipts/c-intent-lane-driver.stdout` and `receipts/c-intent-lane-driver-cwd-clone.stdout`;
the second is the same run from cwd `$S/repo`):

```
BASES root=/home/vgpnk/Projects/shokunin/chousa-shokunin repo=/fast/scratch/hyaku/chousa-r91/R91ExecC1Repro/repo
RECEIPT c1-gate-r89 OK committed+exact+pin+fresh
RECEIPT c1-mutants-r89 OK committed+exact+pin+fresh
RECEIPT c1-harm OK committed+exact+pin+fresh
RECEIPT c1-harm-setup OK committed+exact+pin+fresh
RECEIPT c2-prior-landing OK committed+exact+pin+fresh
RECEIPT c2-prior-controls OK committed+exact+pin+fresh
RECEIPT PINS OK 6/16 pinned files byte-identical
RECEIPT SELF_PIN OK rev=4d00d7519290569879f853d7122b82a927cda1f3 receipts_rev=67954adc599bd605705d94a1ea7abb582491a907
COMMITTED_OK=6/6 EXACT_OK=6/6 PIN_OK=6/6 FRESH_OK=6/6 PINNED_FILES=6 CONTROL_DRIVER_R91=PASS
```

Exit **0**. So the round-90 sentinel's failing dispatch form is repaired; the failure in the previous subsection is
not a failure of the `--root`-relative relpaths themselves but of the executed driver's location.

### (c-isolation) the driver's own location is the sole cause

Same as (c-literal) but with all three read paths passed explicitly at `--root`, so the defaults cannot point into
the clone:

```
cd /fast/scratch/hyaku/chousa-r91/R91ExecC1Repro/repo
python3 -B /fast/scratch/hyaku/chousa-r91/R91ExecC1Repro/repo/corpus/evidence/round91/control-driver-r91.py verify \
  --root /home/vgpnk/Projects/shokunin/chousa-shokunin \
  --repo /fast/scratch/hyaku/chousa-r91/R91ExecC1Repro/repo \
  --expected /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round91/controls/expected.tsv \
  --receipts /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round91/controls/receipts \
  --pins /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round91/instrument-pins.txt \
  --rev 4d00d7519290569879f853d7122b82a927cda1f3 \
  --receipts-rev 67954adc599bd605705d94a1ea7abb582491a907 \
  --work /fast/scratch/hyaku/chousa-r91/R91ExecC1Repro/verify-D2
```

Full stdout (receipt `receipts/c-literal-explicit-root-flags.stdout`), exit **1**:

```
BASES root=/home/vgpnk/Projects/shokunin/chousa-shokunin repo=/fast/scratch/hyaku/chousa-r91/R91ExecC1Repro/repo
RECEIPT c1-gate-r89 OK committed+exact+pin+fresh
RECEIPT c1-mutants-r89 OK committed+exact+pin+fresh
RECEIPT c1-harm OK committed+exact+pin+fresh
RECEIPT c1-harm-setup OK committed+exact+pin+fresh
RECEIPT c2-prior-landing OK committed+exact+pin+fresh
RECEIPT c2-prior-controls OK committed+exact+pin+fresh
RECEIPT PINS OK 6/16 pinned files byte-identical
RECEIPT SELF_PIN FINDING SELF_DRIFT ../../../../../fast/scratch/hyaku/chousa-r91/R91ExecC1Repro/repo/corpus/evidence/round91/control-driver-r91.py@4d00d7519290569879f853d7122b82a927cda1f3
COMMITTED_OK=6/6 EXACT_OK=6/6 PIN_OK=6/6 FRESH_OK=6/6 PINNED_FILES=6 CONTROL_DRIVER_R91=FAIL
```

Only the executing driver's own path remains outside `--root`, and that alone fails the run. The literal triple is
therefore unsatisfiable with this instrument unless the driver file itself sits under `--root` (or is copied there).

## (d) `verify` wrote nothing to the receipts directory — proven

`sha256sum corpus/evidence/round91/controls/receipts/*.txt` before and after run (a), same clone:

```
a0c69090541a51a2a6e89ea42ded151c85989bae6bef61fbf9f20419f86fd5b7  c1-before.txt
b0964dfd6eae4c35fb4f753b8e45c86f1d764da2a7a6c49172771ade463c2178  c1-gate-r89.txt
cf2ef0959b21ed2b7f35edb5154207321a8aec68f9da386c2c8428b2ce7509fb  c1-harm-setup.txt
4cb0ba3459621dd1d223510dc977f2c97b61daa199bc25fbf270535f9d70040a  c1-harm.txt
1b247c19d75aef6f1c41de4af4d1ebc7e135dd288afbd9444fae0d66b48fac1e  c1-mutants-r89.txt
d9783e1a265c6fc329409fe66773db86f1d6b1cc9d74034bb40b4c296e5b4b4a  c2-before.txt
71d2187dd2cdc964858425250f105111b60c71a5c6cdc7782420badbff4de74c  c2-prior-controls.txt
474a1dc4fb17d6d6a4f60653bc347bfa5a4729f379471a89118f1c9511b9cec0  c2-prior-landing.txt
5728153dc065759048952d9dad59c4409db02f06b64a1cfc3338ffe31d993185  c3-before.txt
```

The after list is byte-identical (receipts `d-receipts-before.sha256`, `d-receipts-after.sha256`; `diff` produced
`d-receipts-diff.txt` of size 0, exit 0). File count stayed 9 and `git -C $S/repo status --porcelain` was empty
after the run.

## Invariance matrix — r91 measured against r90's five rows

Same freeze/carrier revisions as (a). r91 rows: A = (c-intent), B and E run explicitly, C = (a), D = (c-literal).

| row | script | `--root` | `--repo` | r90 (R90SentinelScope) | r91 measured | r91 exit |
|---|---|---|---|---|---|---|
| A | lane | lane | clone | **FAIL** (SELF_DRIFT) | **PASS** | 0 |
| B | lane | lane | lane | PASS | PASS | 0 |
| C | clone | clone | clone | PASS | PASS | 0 |
| D | clone | lane | clone | PASS | **FAIL** (INSTRUMENT_UNPINNED + SELF_DRIFT) | 1 |
| E | clone | clone | lane | **FAIL** (SELF_DRIFT) | **PASS** | 0 |

r90 rows are quoted from `.ufo/waves/round-90/w1/R90SentinelScope/receipts/c1-invocation-matrix.txt` (`A_scriptLANE…`,
`E_scriptCLONE…`); r91 receipts: A `c-intent-lane-driver.stdout`, B `matrix-b.stdout`, C
`a-verify-both-bases-clean-clone.stdout`, D `c-literal-command.stdout`, E `matrix-e.stdout`. The pair
(script tree, `--root`) is the discriminator: r91 requires the executed driver to live under `--root`; r90 required
everything to live under `--repo`.

## Finding F1 — the seat spec's literal (c) command prints FAIL at exit 1 on correct bytes (high, operability / dispatch; not a frozen kill rule)

**Exact command / receipt / observed line / exit.** Command and full stdout are in §(c-literal); receipt
`.ufo/waves/round-91/w1/R91ExecC1Repro/receipts/c-literal-command.stdout`; observed summary line
`COMMITTED_OK=6/6 EXACT_OK=6/6 PIN_OK=6/6 FRESH_OK=6/6 PINNED_FILES=5 CONTROL_DRIVER_R91=FAIL` at **exit 1**;
finding lines `RECEIPT PINS FINDING INSTRUMENT_UNPINNED:../../../../../fast/…/repo/corpus/evidence/round91/controls/expected.tsv`
and `RECEIPT SELF_PIN FINDING SELF_DRIFT` over 11 root-escaping paths (driver, expected, 9 receipts).

**Expectation it violates.** The seat spec says this form "must PASS with a `BASES root=… repo=…` line naming both
bases". `BASES` is printed, but the run fails.

**Cause (code, at C3).** `control-driver-r91.py`: `HERE = os.path.dirname(os.path.abspath(__file__))` (line 40) and
`DEFAULT_EXPECTED` / `DEFAULT_RECEIPTS` / `DEFAULT_PINS` under it (lines 41–43), consumed as argparse defaults
(lines 282–284). Reads therefore come from the tree the **executing script** lives in, not from `--root`;
`pin_report()` nonetheless resolves `rel_for(root, expected)` (line 225) and `self_pin()` resolves
`rel_for(root, __file__)` and every receipt against `--root` (lines 256–259). When the script, expected file and
receipts live outside `--root`, `rel_for` yields `../../../../../…`, the pin lookup misses (`INSTRUMENT_UNPINNED`)
and `git show <rev>:<escaping path>` fails for every entry (`SELF_DRIFT`). The isolation run shows the driver's own
path alone suffices to fail the run.

**Scope.** (a) and (b) are unaffected: the frozen counting command at `--root . --repo .` passes 6/6×4 with the
required `SELF_PIN OK rev=… receipts_rev=…`, and the battery is 6/6/6/positive. No C1 kill rule fires in the
evidence: K1 not fired (predicate met), K2 not fired (six classes refused, positive accepted, r90 accepts),
K3 not fired (receipt hashes unchanged; no genuine row moved), K4 not fired by these runs. What is not closed is
plan routed defect 2 (QUALITY 202) in the form this seat was told to run: the `--root`-relative relpath repair makes
the round-90 sentinel's form A pass, but the read locations remain script-anchored, so matrix row D (executing
driver outside `--root`) fails — the inversion of r90, where D passed and A failed. Row D is the triple whose script
tree is not the read base; row A is the coherent one. A caller following the dispatch text verbatim reproduces
the r90 F3 symptom on the other matrix row.

**Smallest corrections (recommendation only; no production edit made).** Either dispatch the absolute path of the
read-base tree's driver (`$L/corpus/evidence/round91/control-driver-r91.py`, cwd irrelevant) — measured PASS; or, in
a future round, derive the three defaults from `--root` and refuse a driver outside `--root` with a `SETUP` line
instead of scoring it as `SELF_DRIFT` (rebasing the defaults alone is not enough: the `__file__` term still escapes).

## Observations (measured or code-read; no claim impact)

- `RECEIPT PINS OK 6/16` is 6 checked files of 16 pinned rows (five distinct row instruments after dedupe plus
  `expected.tsv`), and `PINNED_FILES=6` is the same count. The frozen sentence does not name a denominator, so this
  is not a deviation; recorded so a reader does not take `6/16` for a partial pin pass.
- Code-read only: receipts are read inside the same per-row loop as that row's fresh run (`main`, verify branch),
  not preloaded before the first fresh run. The literal clause "every receipt is read from disk before any fresh
  run" is therefore not implemented as a six-file preload; each committed receipt is read before **its own** fresh
  run, and (d) shows the six committed instruments do not write the receipts directory. Not exercised with an
  adversarial fixture (no unrun check is claimed as passed).
- Concurrent sibling activity: lane `git status --porcelain` changed only by the disappearance of the untracked
  directory `.ufo/waves/round-91/w1/R91ExecC3Repro/` between my two snapshots (that seat's own output folder);
  no tracked file moved and the nine lane receipts hashes are identical before/after (`lane-status-before.txt`,
  `lane-status-after.txt`, `lane-receipts-before.sha256`, `lane-receipts-after.sha256`; diffs of size 0). My own
  output folder `w1/R91ExecC1Repro/` was created after that snapshot and is the only expected addition.

## Safety and hygiene

- Scratch only under `/fast/scratch/hyaku/chousa-r91/R91ExecC1Repro/`; fixture work dirs passed explicitly with
  `--work`; no write under `/tmp`; no write to the lane except this report and its receipt folder; no lane/fleet
  git/jj mutation; clone at C3 left clean (`git status --porcelain` empty); scratch deleted before yield.
- No network request; no `pacman`; no tool installed or upgraded; no host service or sysctl touched.

## Receipts (copied into `w1/R91ExecC1Repro/receipts/`, `SHA256SUMS` inside)

| file | what it is |
|---|---|
| `a-verify-both-bases-clean-clone.stdout` | (a) full stdout, exit 0 |
| `b-forgeries.stdout` | (b) full stdout, exit 0 |
| `c-literal-command.stdout` | (c) as written, exit 1 — F1 |
| `c-literal-explicit-root-flags.stdout` | (c-isolation), exit 1 — driver path alone |
| `c-intent-lane-driver.stdout`, `c-intent-lane-driver-cwd-clone.stdout` | (c-intent) full stdout, exit 0 |
| `matrix-b.stdout`, `matrix-e.stdout` | invariance rows B and E, exit 0 each (A/C/D above) |
| `d-receipts-before.sha256`, `d-receipts-after.sha256`, `d-receipts-diff.txt` | (d) 9/9 hashes, empty diff |
| `lane-receipts-before.sha256`, `lane-receipts-after.sha256`, `lane-receipts-diff.txt` | lane receipts untouched |
| `lane-status-before.txt`, `lane-status-after.txt` | lane status snapshots (sibling churn noted) |
| `revs.txt` | lane/clone/freeze/carrier revs and instrument hashes |
| `run-log.txt` | commands, work dirs, exit codes |
| `prior-r90-invocation-matrix.txt` | copy of `.ufo/waves/round-90/w1/R90SentinelScope/receipts/c1-invocation-matrix.txt` (the r90 rows quoted above) |

VERDICT: R91ExecC1Repro C1 held — the frozen `--root . --repo .` verify prints PASS with `COMMITTED_OK=6/6 EXACT_OK=6/6 PIN_OK=6/6 FRESH_OK=6/6` and `SELF_PIN OK rev=F receipts_rev=C`, the forgery battery prints `FORGERY_REFUSED=6/6 PRIOR_ACCEPTED=6/6 POSITIVE=pass`, and the receipts dir is byte-identical before/after, so no frozen clause or kill rule fires; however the seat's mandatory step (c) as literally written (clone-resident driver, `--root` at the lane) prints `CONTROL_DRIVER_R91=FAIL` at exit 1 on correct bytes while the round-90 sentinel's lane-resident-driver form of the same triple passes, a half-closed QUALITY 202 recorded as F1.

# R92ExecMutations — mutation battery on the three r92 instruments

Seat: `R92ExecMutations` (mutation-tester, leaf). Scratch: `/fast/scratch/hyaku/chousa-r92/R92ExecMutations`
(`S` below). Clone: `git clone --shared /home/vgpnk/Projects/shokunin/chousa-shokunin $S/repo`,
`git -C $S/repo checkout 16ccf7693c61b8ffe392fc757352304f239bfcad` (carrier C5). HEAD verified
`16ccf7693c61b8ffe392fc757352304f239bfcad`; `git -C $S/repo rev-parse --show-toplevel` = `$S/repo`
(`ASSERT_OK=1` in `R92ExecMutations-receipts/repo-state.txt`). All runs used cwd `$S/repo`; all
`--work`/`TMPDIR` outputs lived under `$S`; no lane or sibling byte was edited.

Method: for each mutant, pristine bytes were copied to `$S/mut/<id>/<instrument>`, one textual change
applied there, the mutant deployed **over the clone's instrument path only** (the counter resolves the
instrument from its own directory, so a copy in `$S/mut` alone is invisible), the matching behavioral
detector run, then the pristine bytes restored with `git -C $S/repo checkout -- <one path>` and the
sha256 re-checked against the pin. Every detector was first run on pristine bytes (baseline) and again
after restoration. Mutant diffs: `R92ExecMutations-receipts/diffs.txt`; hashes:
`hashes.txt`/`pristine-hashes.txt`; exact commands and exits: `run-ledger.md`.

Detector choice. C1's frozen `verify` predicate was reproduced as a baseline, but it is not used as the
mutant detector: `self_pin` compares the driver's own bytes to the blob at `--rev`, so any byte change
to `control-driver-r92.py` is killed by pin drift rather than by behavior. The behavioral C1 detector
is the three-class forgery battery, which never pins the driver. C2/C3 detectors are the counters and
their batteries; neither pins its own bytes.

## Baselines (pristine C5 bytes)

| receipt | command (cwd `$S/repo`) | observed line | exit |
|---|---|---|---|
| `base/verify.out` | `python3 -B corpus/evidence/round92/control-driver-r92.py verify --root . --repo . --rev 42e0337822a508208800f98faa3a63c6af9f8c27 --receipts-rev 16ccf7693c61b8ffe392fc757352304f239bfcad --work $S/work/base/verify-work` | `COMMITTED_OK=6/6 EXACT_OK=6/6 PIN_OK=6/6 FRESH_OK=6/6 PINNED_FILES=7 CONTROL_DRIVER_R92=PASS` (+ `RECEIPT SELF_PIN OK rev=42e03378… receipts_rev=16ccf769…`) | 0 |
| `base/forgeries.out` | `python3 -B corpus/evidence/round92/forgeries-r92.py --work $S/work/base/forgeries` | `FORGERY_REFUSED=3/3 POSITIVE=pass` | 0 |
| `base/curation.out` | `python3 -B corpus/evidence/round92/curation-r92.py --root $S/repo` | `… LEGS_MEASURED=14/14` then `CURATION_R92=PASS` | 0 |
| `base/c2ctl.out` | `python3 -B corpus/evidence/round92/curation-controls-r92.py --root $S/repo --work $S/work/base/c2ctl-work` | `CONTROLS=PASS FORGERY_REFUSED=4/4 PRIOR_ACCEPTED=4/4 CARRIED_F1_F4=refused-by-both DUPCOUNT_R91=1 DUPCOUNT_R92=1 PRIOR_REGRESSION=4/4` | 0 |
| `base/tally.out` | `python3 -B corpus/evidence/round92/skill-tally-r92.py --root $S/repo --selftest corpus/evidence/round92/controls/selftest-r92.txt` | `TALLY_ROWS=8 STALE_TALLIES=0/8 EXPECTED_CASES=283 EXPECTED_SKIPPED=0 OTHER_OCCURRENCES=2 CASE_RANGE_BASHENV=273-275 CASE_RANGE_BASH_PIN=282-283 CASE_RANGE_OK=2/2 MISLABELED=0 OTHERS_OK=1 LEGS=3/3` then `SKILL_TALLY_R92=PASS` | 0 |
| `base/c3ctl.out` | `python3 -B corpus/evidence/round92/skill-tally-r92-controls.py --root $S/repo --work $S/work/base/c3ctl-work` | `CONTROLS=PASS OLDPROSE_REFUSED=1/1 PRIOR_ACCEPTED=1/1 STALE_REFUSED_BOTH=1/1` | 0 |

Claim-literal path probes (see Findings F1/F2):

| receipt | command | observed | exit |
|---|---|---|---|
| `base/forg-missing.out` | `python3 -B corpus/evidence/round92/control-forgeries-r92.py --work $S/work/base/forg-missing-work` | `python3: can't open file '…/control-forgeries-r92.py': [Errno 2] No such file or directory` | 2 |
| `base/c2ctl-claim.out` | `python3 -B corpus/evidence/round92/curation-r92-controls.py --root . --work $S/work/base/c2ctl-claim-work` | `python3: can't open file '…/curation-r92-controls.py': [Errno 2] No such file or directory` | 2 |

## C1 mutants (driver; detector = `forgeries-r92.py`)

### M1 — `read_pins` last-wins (duplicate-path raise removed)

Diff (`diffs.txt`): removes `if path in pins: raise SystemExit(f"SETUP PIN_DUPLICATE path={path}")`.
Deployed sha `9d2828137e949ef4e3b0d3e4eaf8b6b9248b353e2e351f9e3e172dabb51a9d4a`.
Command: `python3 -B corpus/evidence/round92/forgeries-r92.py --work $S/work/M1/forg` → exit `1`.
Observed (`M1/forg.out`):
`FAIL dup-pin-path: r92 rc=1 (PIN_DUPLICATE), r91 mechanism proven=True`
with `… RECEIPT PINS FINDING INSTRUMENT_PIN_MISMATCH:pins.txt … CONTROL_DRIVER_R92=FAIL`;
`FORGERY_REFUSED=2/3 POSITIVE=pass`.
The duplicate is no longer refused by the duplicate-path guard; the only remaining refusal on that
fixture is the incidental fixture self-pin drift caused by appending the row. Killed (the named
`PIN_DUPLICATE` finding is gone). Restored sha `1cc948b0…`; restored run exit `0`,
`FORGERY_REFUSED=3/3 POSITIVE=pass`.

### M2 — `instrument_rels` returns only the first rel

Diff: `return rels` → `return rels[:1]`. Deployed sha
`3ebc06d7a0f080c4582d3ae8d20f1a0a906aa2f2618d443aa5f81401d76fea12`.
Command: `… forgeries-r92.py --work $S/work/M2/forg` → exit `1`.
Observed (`M2/forg.out`):
`FAIL second-script-unpinned: r92 rc=1 (INSTRUMENT_UNPINNED:elsewhere.sh), r91 mechanism proven=True`,
`… PINNED_FILES=3 … CONTROL_DRIVER_R92=FAIL`, `FORGERY_REFUSED=2/3 POSITIVE=pass`.
The second script is never added to `wanted`; the residual rc=1 comes from the fixture self-pin drift
after the pin row was dropped, not from the second-script check. Killed. Restored sha `1cc948b0…`;
restored exit `0`, `FORGERY_REFUSED=3/3`.

### M3 — `pin_report` wanted set drops the pins-file entry

Diff: deletes `wanted[rel_for(root, pins_path)] = "pins"`. Deployed sha
`3f9e1e15b7ec66ac2e41d67844657c594feda8ff03d6ec3c619b59243324e5a8`.
Command: `… forgeries-r92.py --work $S/work/M3/forg` → exit `1`.
Observed (`M3/forg.out`):
`FAIL pins-rewrite: r92 rc=0 (INSTRUMENT_PIN_MISMATCH:pins.txt), r91 mechanism proven=True`
with `… RECEIPT PINS OK 4/5 pinned files byte-identical … CONTROL_DRIVER_R92=PASS`;
`FORGERY_REFUSED=2/3 POSITIVE=pass`.
The S5 forgery — one instrument and its pin row edited coherently — is fully accepted by the mutant
(rc 0, PASS). Killed. Restored sha `1cc948b0…`; restored exit `0`, `FORGERY_REFUSED=3/3`.

## C2 mutants (curation; detectors = clean counter + `curation-controls-r92.py`)

For M4/M5/M6/M8 the clean counter must stay PASS (the mutant is not allowed to be trivially broken);
the kill is the battery case that must print the named `LEG_FAIL`.

### M4 — Located-quotes scan routed back through `data_lines`

Diff: `for ln, cells in quote_lines(section_lines(text, "Located quotes")):` →
`data_lines(...)`. Deployed sha
`c08079b29ab7071c05e80da7f5e89d22f55af07bd352723ba002fa126b5521e9`.
Clean: `curation-r92.py --root $S/repo` exit `0`, `CURATION_R92=PASS` (`M4/clean.out`).
Controls: `… curation-controls-r92.py --root $S/repo --work $S/work/M4/ctl` exit `1`; observed
(`M4/ctl.out`):
`FAIL s1-forged-header-row: r92 CURATION_R92=PASS (LEG_FAIL QSHAPE), r91 CURATION_R91=PASS`
and `CONTROLS=FAIL FORGERY_REFUSED=3/4 …`. The forged qid-first row is dropped before the shape test
again. Killed. Restored sha `81310bba…`; restored clean exit `0`, restored controls exit `0`
(`CONTROLS=PASS FORGERY_REFUSED=4/4`).

### M5 — live decision-width check silently drops the row

Diff: removes `decision_width.append((rel, ln.strip(), f"cells={len(cells)}"))` from the width branch,
leaving the silent `continue`. Deployed sha
`58c25b520065730b72c1fab07977f8a2b5977a948475f6b5fea62b274cb58a16`.
Clean exit `0`, `CURATION_R92=PASS` (`M5/clean.out`). Controls exit `1`; observed (`M5/ctl.out`):
`FAIL s2-wide-decision-row: r92 CURATION_R92=PASS (LEG_FAIL WARRANT), r91 CURATION_R91=PASS`;
`CONTROLS=FAIL FORGERY_REFUSED=3/4 …`. The five-cell row is again invisible (count stays at the pinned
11+6). Killed. Restored sha `81310bba…`; restored clean `0`, controls `0` (4/4).

### M6 — `source_link` substring used-by test

Diff: `(entry in tokens or entry_rel in tokens)` → `(entry in cells[10] or entry_rel in cells[10])`.
Deployed sha `700e6b06c2ea0a95e0645eb745f5d3dacb8834fd2ba4571cd56ec5eb387f0b47`.
Clean exit `0`, `CURATION_R92=PASS` (`M6/clean.out`). Controls exit `1`; observed (`M6/ctl.out`):
`FAIL s3-substring-usedby: r92 CURATION_R92=PASS (LEG_FAIL SOURCE), r91 CURATION_R91=PASS`;
`CONTROLS=FAIL FORGERY_REFUSED=3/4 …`. The `.md.bak` sibling path now satisfies the join. Killed.
Restored sha `81310bba…`; restored clean `0`, controls `0` (4/4).

### M8 — USED_BY leg made vacuous while the summary stays PASS

Diff: `legs.append(("USED_BY", not used_by_unlinked, …))` → `legs.append(("USED_BY", True, "0"))`.
Deployed sha `8bc8eda58d6d82851c5db944ebe08e7381b9511be2dd5ef18f72b16b55234fa3`.
Clean exit `0`, `CURATION_R92=PASS` with `LEGS_MEASURED=14/14` (`M8/clean.out`) — the summary still
prints PASS, as the mutant requires. Controls exit `1`; observed (`M8/ctl.out`):
`FAIL s4-unlinked-usedby: r92 CURATION_R92=FAIL (LEG_FAIL USED_BY), r91 CURATION_R91=PASS`
with the actual r92 fails `LEG_FAIL VERDICT fields_hold=0 legs_ok=13/13`;
`CONTROLS=FAIL FORGERY_REFUSED=3/4 …`. The named `LEG_FAIL USED_BY` finding is gone; the forged tree
is still refused by the `fields_hold` gate (see F6). Killed by the battery's named-code requirement.
Restored sha `81310bba…`; restored clean `0`, controls `0` (4/4).

## C3 mutants (tally; detectors = `--selftest` + `skill-tally-r92-controls.py`)

### M9 — tally scope document-wide again

Diff: both tally loops changed from `for ln in gates_text.splitlines():` to
`for ln in text.splitlines():` (one logical scope change, two loop sites). Deployed sha
`0e7a73b51d2259d0f7a46dd2abb4ace0c58045bc2ab1e16ce88d5facc0b70c40`.
Selftest: exit `1`; observed (`M9/self.out`):
`TALLY_ROWS=9 STALE_TALLIES=0/9 EXPECTED_CASES=283 EXPECTED_SKIPPED=0 OTHER_OCCURRENCES=3 CASE_RANGE_BASHENV=273-275 CASE_RANGE_BASH_PIN=282-283 CASE_RANGE_OK=2/2 MISLABELED=0 OTHERS_OK=0 LEGS=2/3`
`LEG_FAIL OTHERS expected={('161', '0'): 1, ('256', '0'): 1} observed={('256', '0'): 1, ('161', '0'): 1, ('215', '0'): 1}`
`SKILL_TALLY_R92=FAIL`. The out-of-section 215 tail tally is counted again. Controls exit `1`
(`M9/c3ctl.out`): `FAIL stale-tally: r91 SKILL_TALLY_R91=FAIL (rc=1), r92 SKILL_TALLY_R92=FAIL (rc=1)`
(the doc-wide denominator prints `STALE_TALLIES=1/9`, not the case's required `1/8`), and
`CONTROLS=FAIL … STALE_REFUSED_BOTH=0/1`. Killed. Restored sha `ac5bf547…`; restored selftest `0`
(PASS), restored controls `0`.

### M10 — others-multiset comparison deleted

Diff: `others_ok = other_counts == EXPECTED_OTHERS` → `others_ok = True`. Deployed sha
`ef088a4cb86fe885cb2937783b24aa9a335a719d3e341973560ef712954379f9`.
Selftest: exit `0`, PASS with the exact baseline field line (`M10/self.out`) — the clean tree cannot
see the deletion. Controls exit `1`; observed (`M10/c3ctl.out`):
`FAIL deleted-other: r91 SKILL_TALLY_R91=PASS (rc=0), r92 SKILL_TALLY_R92=PASS (rc=0)`;
`CONTROLS=FAIL …`. r92 now accepts the deleted-161 tree. Killed by the controls. Restored sha
`ac5bf547…`; restored selftest `0`, restored controls `0`.

### M11 — rename-only control (`other_counts` → `prior_counts`)

Behavior-preserving rename of one local variable at all four occurrences. Deployed sha
`b81d17de541ffb1c2821f0f80ced3fb1a687bbe508162a0365e7caaa23387f95`.
Selftest exit `0` (`M11/self.out`) with the byte-identical field line; controls exit `0`
(`M11/c3ctl.out`): `CONTROLS=PASS OLDPROSE_REFUSED=1/1 PRIOR_ACCEPTED=1/1 STALE_REFUSED_BOTH=1/1`.
**SURVIVED** — required control showing the detectors are behavioral, not blanket refusals. Restored
sha `ac5bf547…`; restored runs exit `0`.

## Battery totals

`MUTANTS_KILLED=9/9` (M1, M2, M3, M4, M5, M6, M8, M9, M10); `SURVIVORS=1/1` (M11);
`INCONCLUSIVE=0`; no unexpected survivor. Named probes were 9 mutants plus 1 rename control; the
tasking's expected `8/9` denominator does not match that named set (F4).

## Findings (exact command / receipt / observed line + exit)

**F1 — C1 claim names a script C5 does not carry.** Command
`python3 -B corpus/evidence/round92/control-forgeries-r92.py --work …` exits `2` with
`can't open file '…/control-forgeries-r92.py': [Errno 2]` (`base/forg-missing.out`). `git ls-tree`
shows `forgeries-r92.py`; the committed file prints `FORGERY_REFUSED=3/3 POSITIVE=pass` exit `0`.
Already recorded by `R92ExecC1Repro.md` F1; this seat reproduces it independently.

**F2 — C2 claim names a battery C5 does not carry.** Command
`python3 -B corpus/evidence/round92/curation-r92-controls.py --root . --work …` exits `2` with
`can't open file '…/curation-r92-controls.py': [Errno 2]` (`base/c2ctl-claim.out`). The committed
name is `curation-controls-r92.py` (pinned); it prints `CONTROLS=PASS` exit `0`. Already recorded by
`R92ExecC2Repro.md` Finding 1; reproduced here.

**F3 — C2 controls summary token differs from the frozen predicate.** Frozen:
`PRIOR_REGRESSION=7/7`; observed summary
`… DUPCOUNT_R91=1 DUPCOUNT_R92=1 PRIOR_REGRESSION=4/4` (`base/c2ctl.out`). The literal string
`PRIOR_REGRESSION=7/7` appears only in the nested regression detail line
`OK regression: FORGERY_REFUSED=7/7 PRIOR_REGRESSION=7/7 rc=1`. A substring gate passes; a
summary-line gate fails. Already recorded by `R92ExecC2Repro.md` Finding 2.

**F4 — tasking tally arithmetic.** The named probe set is nine mutants plus the M11 control (ten
runs). Observed: `MUTANTS_KILLED=9/9 SURVIVORS=1/1`; the expected `MUTANTS_KILLED=8/9 SURVIVORS=1/9
(M11)` is not reproducible from the named set (it would require either a tenth named mutant or one
numbered mutant to survive besides M11). Reported as observed; no mutant result was adjusted to fit.

**F5 — literal mutation sites for M4/M5 are inert; the live sites were mutated.** At C5 `data_lines`
already skips `qid`-first cells (line 152) and `table_rows` has no call sites (only the `def` at line
174 and a docstring mention at line 11); the S2 repair lives in `main` (lines 338–341), not in the
helper the docstring names. M4 therefore restores the shared filter by routing the Located-quotes scan
back through `data_lines`, and M5 removes the live width record. Both are behavior-bearing and killed.
Coverage note: dead `table_rows` still carries the old silent drop; a future edit that routes decision
rows through it would reintroduce S2 silently. This is not a C2 predicate violation at C5.

**F6 — M8 kill-power nuance.** With the USED_BY leg forced true, the s4 forged tree still exits `1`
as `LEG_FAIL VERDICT fields_hold=0 legs_ok=13/13` because `fields_hold` repeats
`and not used_by_unlinked`. The battery kills M8 only because it requires the named
`LEG_FAIL USED_BY` line. For refusal, the leg duplicates the verdict gate; for the named finding it
is the only source. Recorded for the L1; no contract change made.

**F7 — incidental refusals in M1/M2.** The forgery fixtures append/drop pin rows without recomputing
the fixture self-pin, so those mutant runs still exit `1` on `INSTRUMENT_PIN_MISMATCH:pins.txt`
(M1) / `PINNED_FILES=3` (M2). The kill is attributed only to the missing named code
(`PIN_DUPLICATE`, `INSTRUMENT_UNPINNED:elsewhere.sh`), never to the incidental self-pin drift.

## Restoration / host guard

* Per-mutant restored sha256 equals the `instrument-pins.txt` row:
  driver `1cc948b0d3cac43109afdc53bc8658c8a00fed8dceba89c8f1df00c606d4848b`,
  curation `81310bba8c8878e3cbb9026cd5a87f42fe0e79beb51ab8160c5adfc1ff644166`,
  tally `ac5bf5475becb81a9095174dbc2a07206246edc9323ad32b31a68cd59e9a4b1d`.
* `repo-state.txt`: `HEAD=16ccf7693c61b8ffe392fc757352304f239bfcad`,
  `git status --porcelain` empty after all restores (so the six committed receipts were not written:
  the C1 verify/fresh runs stayed under `--work`), `rev-parse --show-toplevel` assertion `ASSERT_OK=1`.
* Disclosure: the toplevel assertion was recorded after the last restore rather than before the first
  `git checkout`; the only mutating git commands were the ten single-path
  `git -C $S/repo checkout -- corpus/evidence/round92/<instrument>` restores, and the byte hashes plus
  empty status confirm no cross-tree or lane effect.
* No fixture repositories were created; no lane file was edited; scratch removed after receipts were
  copied.
* Tooling: no installs or upgrades; no network, no pacman, no sudo.

## Receipts (copied to `R92ExecMutations-receipts/`)

`base/` (8 `.out` + 8 `.rc`), `M1/`–`M11/` (mutant and restored-detector `.out`),
`diffs.txt`, `hashes.txt`, `pristine-hashes.txt`, `repo-state.txt`, `run-ledger.md`.

VERDICT: R92ExecMutations C1 held — all three C1 mutants are killed by `forgeries-r92.py` (mutant 2/3 refusals, exit 1; restored 3/3, exit 0; driver sha restored to `1cc948b0…`), with the frozen command's `control-forgeries-r92.py` name absent at C5 (exit 2, F1).
VERDICT: R92ExecMutations C2 held — all four C2 mutants are killed by `curation-controls-r92.py` (mutant 3/4, exit 1, clean counter still PASS; restored 4/4, exit 0; curation sha restored to `81310bba…`), with the frozen command's `curation-r92-controls.py` name absent (F2) and the summary printing `PRIOR_REGRESSION=4/4` against the frozen `7/7` (F3).
VERDICT: R92ExecMutations C3 held — M9 is killed by the `--selftest` run (`OTHER_OCCURRENCES=3`, `OTHERS_OK=0`, exit 1) and M10 by the controls (`deleted-other: r92 PASS`, exit 1), while the rename-only M11 survives with byte-identical output (exit 0), proving the detector is behavioral rather than a blanket refusal.

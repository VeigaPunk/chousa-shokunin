# R90ExecC1Repro — C1 reproduced from a clean tree

Seat `R90ExecC1Repro` (leaf). Lane root `/home/vgpnk/Projects/shokunin/chousa-shokunin`.
Scratch `S=/fast/scratch/hyaku/chousa-r90/R90ExecC1Repro` (deleted before yield).
No network, no installs, no `sudo`, no pacman; nothing written outside `S` and this wave folder.

## Tree under attack

```
git clone --shared /home/vgpnk/Projects/shokunin/chousa-shokunin $S/repo
git -C $S/repo checkout 9bad12011187d114ba2c4588c5df08a21ab28145
git -C $S/repo rev-parse HEAD
9bad12011187d114ba2c4588c5df08a21ab28145
```

Frozen predicates read first: `corpus/evidence/round90/claims.md`, `plans/round-90.md`; machine form
`.ufo/waves/round-90/claims.json` present at the tree (added by the freeze commit).

Instrument bytes at the tree (identification only):

```
3a64f377894a0736bd103e6a63493745c09faf4eb5a799b8b56f6e5cfabd086a  corpus/evidence/round90/control-driver-r90.py
009022f1eed16ed42ee665c0814ba2809ba461bc6ac310b598beef4d49bdd181  corpus/evidence/round90/control-forgeries-r90.py
37cbfaa456565d70b128a86153a484b3fe626eb7bac1fc94b2e1d109cc20f376  corpus/evidence/round90/controls/expected.tsv
```

## (a) C1 verify leg — command, observed lines, exit

```
cd $S/repo
python3 -B corpus/evidence/round90/control-driver-r90.py verify --root $S/repo --repo $S/repo \
  --rev 8d9893b42eb22690ea5f920ab87fd7e1810b847a \
  --receipts-rev 9bad12011187d114ba2c4588c5df08a21ab28145 --work $S/work
```

Receipt: `R90ExecC1Repro/a-verify.txt` (also `a-verify-run2.txt`, `a-verify-run3.txt`).

```
RECEIPT c1-gate-r89 OK committed+exact+pin+fresh
RECEIPT c1-mutants-r89 OK committed+exact+pin+fresh
RECEIPT c1-harm OK committed+exact+pin+fresh
RECEIPT c1-harm-setup OK committed+exact+pin+fresh
RECEIPT c2-prior-landing OK committed+exact+pin+fresh
RECEIPT c2-prior-controls OK committed+exact+pin+fresh
RECEIPT SELF_PIN OK all scoring bytes equal their blobs at --rev
COMMITTED_OK=6/6 EXACT_OK=6/6 PIN_OK=6/6 FRESH_OK=6/6 CONTROL_DRIVER_R90=PASS
EXIT=0
```

No `RECEIPT … FINDING` line was printed. The four counts match the frozen sentence exactly
(`COMMITTED_OK=6/6 EXACT_OK=6/6 PIN_OK=6/6 FRESH_OK=6/6`) and the token `CONTROL_DRIVER_R90=PASS`
is printed with exit 0.

## (b) C1 forgery battery — command, observed lines, exit

```
cd $S/repo
python3 -B corpus/evidence/round90/control-forgeries-r90.py --root $S/repo --work $S/forge \
  --rev 8d9893b42eb22690ea5f920ab87fd7e1810b847a
```

Receipt: `R90ExecC1Repro/b-forgeries.txt` (also `b-forgeries-run2.txt`, `b-forgeries-run3.txt`).

```
OK B2-substring: r90 refused (TOKEN_DETACHED:LEG_REREAD=16/160,FRESH_TOKEN_DETACHED:LEG_REREAD=16/160), r89 accepted
  r90 rc=1  prior rc=0
OK B1-committed: r90 refused (TOKEN_DETACHED:LEG_REREAD=0/16), r89 accepted
  r90 rc=1  prior rc=0
OK B3-no-pin: r90 refused (PIN_MISSING), r89 accepted
  r90 rc=1  prior rc=0
OK B3b-stale-pin: r90 refused (PIN_MISMATCH:0000000000000000000000000000000000000000), r89 accepted
  r90 rc=1  prior rc=0
OK B4-harm-vacuity: r90 refused (PREDICATE_SHORT:records=0<1,FRESH_PREDICATE_SHORT:records=0<1), r89 accepted
  r90 rc=1  prior rc=0
OK C-duplicate-key: r90 refused (DUPLICATE_KEY:records,FRESH_DUPLICATE_KEY:records), r89 accepted
  r90 rc=1  prior rc=0
OK POSITIVE: accepted by both drivers
  r90 rc=0  prior rc=0
FORGERY_REFUSED=6/6 PRIOR_ACCEPTED=6/6 POSITIVE=pass
CONTROL_FORGERIES_R90=PASS
EXIT=0
```

Every class printed `OK`; no `CASE_DEVIATION` line. `FORGERY_REFUSED=6/6 PRIOR_ACCEPTED=6/6
POSITIVE=pass` matches the frozen sentence; exit 0. The six prior runs are `prior rc=0` — the unchanged
round-89 driver accepts each fixture, so the fixtures do prove the prior state (K2's precondition).

## (c) The committed receipt is read before any fresh run; nothing under `receipts/` moves

Code order inside `verify` (line numbers from the tree's `control-driver-r90.py`): the receipt body is read
at **line 238** (`text = open(path, encoding="utf-8").read()`), the pin header is taken from that same text
at 239, and only then is this row's instrument re-run at **line 265**
(`frc, ftext = run_instrument(cmd, root)`), with the fresh output written to `--work` (`work/fresh-<case>.out`).
The write to the receipt happens only in the `emit` branch; the `verify` branch opens receipts in read mode
only.

Measured, across run 3 (a full `verify` + `forgeries` pair between the two snapshots):

```
$ stat -c '%Y %n' corpus/evidence/round90/controls/receipts/*.txt   > out/mtimes-baseline3.txt
[run (a) verify; run (b) forgeries]
$ stat -c '%Y %n' corpus/evidence/round90/controls/receipts/*.txt   > out/mtimes-after3.txt
$ diff -u mtimes-baseline3.txt mtimes-after3.txt
MTIMES_UNCHANGED_ACROSS_RUN3=yes
$ sha256sum -c out/sha-baseline3.txt --quiet
SHA_UNCHANGED_ACROSS_RUN3=yes
$ git -C $S/repo status --porcelain
STATUS3=EMPTY
```

Receipts: `R90ExecC1Repro/mtimes-baseline3.txt`, `mtimes-after3.txt`, `mtime-diff-run3.txt` (0 bytes),
`sha-baseline3.txt`, `git-status.txt` (0 bytes). Nine receipt files, byte-identical before and after both
legs; the tracked tree is clean, so neither leg wrote under `controls/receipts/` (no K3 harm).

Four direct probes isolate each leg on copies of the committed receipts (each in its own `--receipts` dir
and its own `--work`):

| probe | mutation | observed line | exit | receipt |
|---|---|---|---|---|
| A | `c1-gate-r89.txt`: `LEG_REREAD=16/16` → `16/160` | `RECEIPT c1-gate-r89 FINDING TOKEN_DETACHED:LEG_REREAD=16/160` with `COMMITTED_OK=5/6 EXACT_OK=5/6 PIN_OK=6/6 FRESH_OK=6/6` | 1 | `probeA.txt` |
| B | `c2-prior-controls.txt` deleted | `RECEIPT c2-prior-controls FINDING MISSING_RECEIPT,MISSING_HEADER:case,MISSING_HEADER:exit,PIN_MISSING` | 1 | `probeB.txt` |
| C | one byte appended in-tree to `c1-gate-r89.txt` | `RECEIPT SELF_PIN FINDING SELF_DRIFT corpus/evidence/round90/controls/receipts/c1-gate-r89.txt` with `COMMITTED_OK=6/6 … PIN_OK=6/6 FRESH_OK=6/6` | 1 | `probeC.txt` |
| D | `records=0` appended as a body line of `c1-harm.txt` | `RECEIPT c1-harm FINDING DUPLICATE_KEY:records` | 1 | `probeD.txt` |

Probe A is the decisive ordering evidence: the fresh re-run of `gate-records-r89.py` prints `16/16`, so
`FRESH_OK=6/6` — yet the row fails on the **committed** bytes. A fresh-only verifier would have passed it
(K4's "the committed receipt not read" is not the case). Probe A also left every probe-dir hash unchanged
(`PROBE_A_DIR_UNCHANGED=yes`, `sha256sum -c`). Probe B is the missing-receipt negative; probe C shows the
self-pin leg fires on a one-byte in-tree move while all six row legs still pass, so `SELF_PIN` is live and
independent; probe D shows `DUPLICATE_KEY` on a required key carried twice with different values.

Probe C's appended line was removed with `git checkout -- …/c1-gate-r89.txt` in the scratch clone only;
`STATUS_AFTER_RESTORE=EMPTY` and `SHA_RESTORED_OK`. That restore is the sole reason
`mtimes-before.txt` differs from `mtimes-final.txt`:

```
-1794132663 corpus/evidence/round90/controls/receipts/c1-gate-r89.txt
+1794132750 corpus/evidence/round90/controls/receipts/c1-gate-r89.txt
```

no other file moved, and mtime-level identity across run 3 (above) is the clean measurement.

## Committed receipts vs expectations (headers, pins, non-vacuity)

`expected.tsv` carries exactly six scoring rows; all six committed receipts exist and none is extra:

| case | `# exit=` / expected | `# computed_against=` | non-vacuity field |
|---|---|---|---|
| c1-gate-r89 | 0 / 0 | 8d9893b42eb22690ea5f920ab87fd7e1810b847a | `GATE_RECORDS_R89=PASS LEG_REREAD=16/16 CROSSCHECK=15/15` |
| c1-mutants-r89 | 0 / 0 | 8d9893b4… | `MUTANTS_KILLED=11/11 TOOL_MUTANTS_CAUGHT=2/2` |
| c1-harm | 0 / 0 | 8d9893b4… | `HARM_RECHECK files=15 records=31 moved=0` → `records>=1` holds (31) |
| c1-harm-setup | 2 / 2 | 8d9893b4… | `HARM_RECHECK_ERROR base-tool missing: …` |
| c2-prior-landing | 0 / 0 | 8d9893b4… | `CURATION_R89=PASS` |
| c2-prior-controls | 0 / 0 | 8d9893b4… | `CONTROLS=PASS FORGERY_REFUSED=7/7` |

The harm row is non-vacuous: `records=31` (not 0), and the setup negative re-derives `exit=2`. Copies:
`R90ExecC1Repro/receipts/` (six scored receipts + `c1-prior-driver.txt` + `expected.tsv`), fresh re-runs
`R90ExecC1Repro/fresh/fresh-*.out`.

The pin lives in the emitted receipts, not in `verify`: `git diff 8d9893b4 9bad1201 -- …/receipts/` is
exactly six receipt files, 7 insertions / 7 deletions, each row's `# computed_against=` moving from
`f8fa55ec94cb34e7b572a9d87d7f62d88bc80bf8` to the freeze revision. `verify` minted nothing.

## Unchanged subjects (the round's stated invariant)

```
git diff f54a45ed197dd475af50d82e43a22df3d2e99782 9bad12011187d114ba2c4588c5df08a21ab28145 -- tools/
TOOLS_DIFF_EMPTY=yes
```

`tools/gate-records.py` and `tools/research-gate.sh` are byte-identical between base and tree, so no domain
record could move and the harm row's `moved=0` is a statement about a non-empty population
(`records=31`), not about an edited subject.

## Reproducibility

`verify` run three times (runs 1, 2, 3) and `forgeries` three times; every run printed the same count line,
the same seven `OK`s, and the same footer, exit 0 each time. `diff a-verify.txt a-verify-run3.txt` and
`diff b-forgeries.txt b-forgeries-run3.txt` each differ on exactly one line — the appended `EXITn=` marker;
runs 2 and 3 are otherwise byte-identical to run 1.

## Observations (no kill; for the C1 owner's judgement)

1. **`c1-harm-setup.txt` carries an emitting-run scratch path.**
   `HARM_RECHECK_ERROR base-tool missing: /fast/scratch/hyaku/chousa-r90/emit2/absent-tool.py` (committed)
   vs `…/R90ExecC1Repro/work/absent-tool.py` (fresh re-run). Only `HARM_RECHECK_ERROR` is a required token,
   so the row passes and `FRESH_OK=6/6` counts it. Instantiation of named limit (2): the fresh-agreement leg
   is exit + required-token + predicate agreement, not body-byte agreement. This row can never reproduce its
   body text on another host. Not a deviation from the frozen sentence as worded; named here so the limit is
   measured rather than assumed.
2. **`EXACT_OK` is the token/predicate count over committed receipts**, computed by a second pass that does
   not re-check `# exit=`; the `# exit=` leg is counted under `COMMITTED_OK`. Both are 6/6 here, so the two
   readings coincide on this set.
3. **The forgery battery's `--root` flag does not steer the r90 driver.** `run_new` passes
   `--root os.path.abspath(HERE/../../..)` — the driver's own tree — while the fixtures' instruments are
   absolute stub paths inside `--work`, and the `--root` argument only feeds the round-89 prior run. Correct
   for these fixtures; a reader assuming `--root` selects the tree measured by r90 would be wrong.
4. `receipts/` holds nine files, six of which are scored rows; `c1-prior-driver.txt`, `c2-subst-before.txt`,
   `c3-before.txt` are before-state evidence cited by `claims.md` and are not verified by the driver.

## Deviations from the frozen expected values

None for C1. All four counts, the `PASS` token, the `SELF_PIN OK` line and the exit are exactly as frozen;
all six forgery classes are refused by r90 and accepted by r89; the positive fixture is accepted by both.

VERDICT: R90ExecC1Repro C1 held — `verify` printed `COMMITTED_OK=6/6 EXACT_OK=6/6 PIN_OK=6/6 FRESH_OK=6/6 CONTROL_DRIVER_R90=PASS` (exit 0) and `forgeries` printed `FORGERY_REFUSED=6/6 PRIOR_ACCEPTED=6/6 POSITIVE=pass` (exit 0) from a clean clone at 9bad1201, with the committed receipts read and never written (mtimes/hashes unchanged, tree clean) and probes A–D isolating each leg.

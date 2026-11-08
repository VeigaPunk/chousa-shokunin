# R92RevPrior — BEFORE-state reproduction (round 92)

Seat revenger; task = independently reproduce the BEFORE state the claims rest on, from committed bytes only.
Scratch: `/fast/scratch/hyaku/chousa-r92/R92RevPrior` (deleted before yield).
Base clone checked out at `d7780fef…`; carrier clone at `16ccf769…` (HEAD = `16ccf7693c61b8ffe392fc757352304f239bfcad`).
All commands run with absolute paths or inside scratch; no lane/fleet mutation, no network, no sudo.

## Axes
C1 operability · C2 calibration · C3 freshness.

## (a) C1 BEFORE — r91 mechanism attestation, executed

Target: `/fast/scratch/hyaku/chousa-r92/R92RevPrior/base/corpus/evidence/round91/control-driver-r91.py` (base `d7780fef`).

Command:

```
python3 - <<'PY'  (imports control-driver-r91.py, executes its functions)
```

Receipt: `.ufo/waves/round-92/w1/receipts/c1-mechanisms.txt` (exit 0).

Observed (verbatim lines):

- (i) `read_pins` (r91 `control-driver-r91.py:70-84`, body line 83
  `pins[parts[1].strip()] = parts[0]`): a pins file with two rows for `fx-tool.sh`
  (`a`*64 then `b`*64) yields `entries=1`, `fx-tool.sh=b*64…`. The duplicate path
  collapses to one entry, last-wins; no `PIN_DUPLICATE` guard exists in the r91 source
  (`"PIN_DUPLICATE" in src` → `False`). A duplicate pin path is accepted silently.
- (ii) `instrument_rel` (r91 lines 119-127, `return rel` at line 126 on the *first* matching
  token): row instrument `python3 -B @ROOT@/fx-tool.sh && bash @ROOT@/elsewhere.sh` returns
  `'fx-tool.sh'`. `elsewhere.sh` is never returned and therefore never pinned/checked.
- (iii) `pin_report` (r91 lines 212-239). Wanted-set lines are only
  `wanted[rel] = row["case"]` (instrument rel) and
  `wanted[rel_for(root, expected)] = "expectations"`. `'instrument-pins' in pin_report body`
  → `False`. There is no wanted entry for the pins file itself, so a coherently rewritten
  pins table passes.

C1 forgery battery re-run at carrier (the trees it builds persist under the scratch work dir):

```
python3 -B …/carrier/corpus/evidence/round92/forgeries-r92.py --work $S/c1battery
```

Receipt: `receipts/c1-forgeries-rerun.txt`, exit 0:

```
OK dup-pin-path: r92 rc=1 (PIN_DUPLICATE), r91 mechanism proven=True
OK second-script-unpinned: r92 rc=1 (INSTRUMENT_UNPINNED:elsewhere.sh), r91 mechanism proven=True
OK pins-rewrite: r92 rc=1 (INSTRUMENT_PIN_MISMATCH:pins.txt), r91 mechanism proven=True
OK positive: r92 rc=0 (r91 verify is not run: the prior pin-checks against the real table, so a fixture PASS is unclaimable)
FORGERY_REFUSED=3/3 POSITIVE=pass
```

This matches the frozen C1 statement exactly. No r91 verify PASS is claimed (impossible against
the real table — the battery states this in its own output), and none was manufactured here.

## (b) C2 BEFORE — r91 accepts all four S forgeries

Frozen battery re-run first so its own forged trees exist:

```
python3 -B …/carrier/corpus/evidence/round92/curation-controls-r92.py --root $S/carrier --work $S/c2controls
```

Receipt: `receipts/c2-controls-rerun.txt`, exit 0. Tail lines:

```
OK s1-forged-header-row: r92 CURATION_R92=FAIL (LEG_FAIL QSHAPE), r91 CURATION_R91=PASS
OK s2-wide-decision-row: r92 CURATION_R92=FAIL (LEG_FAIL WARRANT), r91 CURATION_R91=PASS
OK s3-substring-usedby: r92 CURATION_R92=FAIL (LEG_FAIL SOURCE), r91 CURATION_R91=PASS
OK s4-unlinked-usedby: r92 CURATION_R92=FAIL (LEG_FAIL USED_BY), r91 CURATION_R91=PASS
OK duplicate-count: r91 UNENTAILED_TERM=1 r92 UNENTAILED_TERM=1
OK regression: FORGERY_REFUSED=7/7 PRIOR_REGRESSION=7/7 rc=1
CONTROLS=PASS FORGERY_REFUSED=4/4 PRIOR_ACCEPTED=4/4 CARRIED_F1_F4=refused-by-both DUPCOUNT_R91=1 DUPCOUNT_R92=1 PRIOR_REGRESSION=4/4
```

Note: the first four lines of that battery (`nonq-row`, `status-rejected`, `used-by-blank`,
`ubiquitous-warrant`) print `FAIL … refused-by-both` — those are the F1–F4 classes r91 already
refuses, documented by the battery itself as correct carried verdicts, not failures of this round.
`PRIOR_ACCEPTED=4/4` (the four S-classes) is as frozen.

Independent re-derivation — r91 counter directly on each S tree (trees persisted from the battery run,
rebuilt by it, not by me):

```
for t in s1-forged-header-row s2-wide-decision-row s3-substring-usedby s4-unlinked-usedby:
  python3 -B $S/base/corpus/evidence/round91/curation-r91.py --root $S/c2controls/$t
```

Receipt: `receipts/c2-before-rerun.txt`. Every tree exits 0 and prints
`CURATION_R91=PASS` with `LEGS_MEASURED=13/13`, e.g.:

```
### s1-forged-header-row
…
VERDICT fields_hold=1 legs_ok=13/13 DETECTOR_WITNESS=11/11
CURATION_R91=PASS
EXIT=0
```

(same `CURATION_R91=PASS` / `EXIT=0` for s2, s3, s4). Four of four — re-derived, not just quoted.

After-state on the pristine landing tree re-checks (carrier):

```
python3 -B …/carrier/corpus/evidence/round92/curation-r92.py --root $S/carrier
```

Receipt: `receipts/c2-after.txt`, exit 0: `LEGS_MEASURED=14/14 … CURATION_R92=PASS` — as frozen.

## (c) C3 BEFORE — r91 passes the deleted-161 tree

Frozen battery re-run:

```
python3 -B …/carrier/corpus/evidence/round92/tally-controls-r92.py --root $S/carrier --work $S/c3controls
```

Receipt: `receipts/c3-controls-rerun.txt`, exit 0:

```
OK old-prose-carried: r91 SKILL_TALLY_R91=FAIL, r92 SKILL_TALLY_R92=FAIL
OK stale-tally: r91 SKILL_TALLY_R91=FAIL (rc=1), r92 SKILL_TALLY_R92=FAIL (rc=1)
OK deleted-other: r91 SKILL_TALLY_R91=PASS (rc=0), r92 SKILL_TALLY_R92=FAIL (rc=1)
CONTROLS=PASS OLDPROSE_REFUSED=1/1 PRIOR_ACCEPTED=1/1 STALE_REFUSED_BOTH=1/1
```

Independent re-derivation on the battery's own `deleted-other` tree (the 161→160 edit inside
`## Gates`, built exactly as `tally-controls-r92.py:88` does it):

```
python3 -B $S/base/corpus/evidence/round91/skill-tally-r91.py --root $S/c3controls/deleted-other \
  --selftest $S/carrier/corpus/evidence/round92/controls/selftest-r92.txt
```

Observed: `TALLY_ROWS=9 STALE_TALLIES=0/9 EXPECTED_CASES=283 EXPECTED_SKIPPED=0 OTHER_OCCURRENCES=3
CASE_RANGE_BASHENV=273-275 CASE_RANGE_BASH_PIN=282-283 CASE_RANGE_OK=2/2 MISLABELED=0 LEGS=2/2`,
then `SKILL_TALLY_R91=PASS`, exit 0. (Note `TALLY_ROWS=9` / `LEGS=2/2` — the r91 counter is
document-wide and unpinned, so the deleted in-`## Gates` other does not change its verdict.)
Re-derived, not just quoted.

After-state (carrier):

```
python3 -B …/carrier/corpus/evidence/round92/skill-tally-r92.py --root $S/carrier --selftest …/selftest-r92.txt
```

Receipt: `receipts/c3-after.txt`, exit 0: `TALLY_ROWS=8 … OTHER_OCCURRENCES=2 … CASE_RANGE_OK=2/2
MISLABELED=0 OTHERS_OK=1 LEGS=3/3 SKILL_TALLY_R92=PASS` — as frozen.

## (d) Comparison with the committed before receipts — FINDING

The task names committed before receipts `corpus/evidence/round92/controls/receipts/c{1,2,3}-before.txt`
"at the carrier". They do not exist:

```
git cat-file -e 16ccf769…:corpus/evidence/round92/controls/receipts/c1-before.txt
  → fatal: path does not exist in '16ccf769…', rc=128
```

The same negative result holds for `c2-before.txt` / `c3-before.txt` at the carrier, at the freeze
`42e03378`, and at base `d7780fef` (all rc=128). The carrier actually carries only six receipts:
`c1-gate-r89.txt`, `c1-harm-setup.txt`, `c1-harm.txt`, `c1-mutants-r89.txt`,
`c2-prior-controls.txt`, `c2-prior-landing.txt` — all r89-era verifier receipts pin-*ing* old
instruments (`computed_against=42e03378…`, i.e. they are the r92 *after* receipts of the six
`expected.tsv` rows), none of them a r91-before measurement of the C1/C2/C3 S-classes.

So there is no line in a committed `c{1,2,3}-before.txt` to compare against: the before states
above were re-derived from the instruments themselves (§a–c), and the plan's §"Before states"
(`plans/round-92.md:31-35`) documents *why* no such receipts exist for C1 (r91 verify cannot PASS a
fixture, so the battery does mechanism attestation instead of a fabricated `PRIOR_ACCEPTED=6/6`),
for C2/C3 the before numbers are the battery lines re-derived in §b/§c. A reader who trusts the
ticket's "(d)" premise would cite a file that was never emitted — flagged here as a finding against
the *ticket wording*, not against any claim: no claim sentence asserts that `c*-before.txt`
files exist; the claims' Before sections name the mechanisms and the battery verdicts, both of
which reproduce exactly as shown.

Also recorded for the integration owner: §b's four r91-carried lines (`nonq-row`,
`status-rejected`, `used-by-blank`, `ubiquitous-warrant`) print `FAIL` only in the sense that those
classes are refused by *both* counters (the battery's own header says these `FAIL` lines are the
correct carried verdicts); the seat reports them as observed exit 1 output, not as regressions.

## Receipts copied to wave output
`receipts/c1-mechanisms.txt`, `receipts/c1-forgeries-rerun.txt`, `receipts/c2-controls-rerun.txt`,
`receipts/c2-before-rerun.txt`, `receipts/c2-after.txt`, `receipts/c3-controls-rerun.txt`,
`receipts/c3-after.txt` (mirrored at the top level of `.ufo/waves/round-92/w1/`). Scratch under
`/fast/scratch/hyaku/chousa-r92/R92RevPrior` was removed after copying.

## Verdict trailer
VERDICT: R92RevPrior C1 fired — r91 read_pins last-wins, instrument_rel first-only, and pin_report's wanted set lacking the pins file were each re-derived by executing the r91 functions, matching the frozen mechanism attestation.
VERDICT: R92RevPrior C2 fired — curation-r91.py prints CURATION_R91=PASS (exit 0) on all four S forged trees rebuilt by the frozen battery (PRIOR_ACCEPTED=4/4), while r92 refuses each.
VERDICT: R92RevPrior C3 fired — skill-tally-r91.py prints SKILL_TALLY_R91=PASS (exit 0) on the deleted-161 tree while r92 refuses it with LEG_FAIL OTHERS.

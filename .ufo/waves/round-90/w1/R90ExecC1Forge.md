# R90ExecC1Forge — C1 forged-receipt attack on the round-90 control driver

Seat `R90ExecC1Forge` (leaf; no subagent, no orchestration call). Lane root
`/home/vgpnk/Projects/shokunin/chousa-shokunin`. Scratch `S=/fast/scratch/hyaku/chousa-r90/R90ExecC1Forge`
(deleted before yield). Tooling: none installed or upgraded (no pacman, no `uv`, no network); the host's
`python3`, `git`, `bash`, `sha256sum` were sufficient. Nothing written outside `S` and this wave folder.

Frozen predicates read first: `corpus/evidence/round90/claims.md` (every kill rule and named limit) and
`plans/round-90.md`; `.ufo/waves/round-90/claims.json` present at the tree.

## Tree under attack

```
git clone --shared /home/vgpnk/Projects/shokunin/chousa-shokunin $S/repo
git -C $S/repo checkout 9bad12011187d114ba2c4588c5df08a21ab28145
git -C $S/repo rev-parse HEAD   ->  9bad12011187d114ba2c4588c5df08a21ab28145
git -C $S/repo rev-parse master ->  9bad12011187d114ba2c4588c5df08a21ab28145
```

Instrument bytes at the tree (identification only, match `instrument-pins.txt`):

```
3a64f377894a0736bd103e6a63493745c09faf4eb5a799b8b56f6e5cfabd086a  corpus/evidence/round90/control-driver-r90.py
009022f1eed16ed42ee665c0814ba2809ba461bc6ac310b598beef4d49bdd181  corpus/evidence/round90/control-forgeries-r90.py
4967755433f19b8ca5f070dcae377ba23989ae6c7971afa4d9936b06c3b3d3c8  corpus/evidence/round90/harm-recheck-r90.py
```

## Baseline — both scored commands held at the attack revision

**(B1)** `cd $S/repo && python3 -B corpus/evidence/round90/control-driver-r90.py verify --root . --repo . --rev 8d9893b42eb22690ea5f920ab87fd7e1810b847a --receipts-rev 9bad12011187d114ba2c4588c5df08a21ab28145 --work $S/work/verify1`
→ exit **0**, last line `COMMITTED_OK=6/6 EXACT_OK=6/6 PIN_OK=6/6 FRESH_OK=6/6 CONTROL_DRIVER_R90=PASS`.
Receipt `R90ExecC1Forge/verify-scored.txt`. All six rows print `OK committed+exact+pin+fresh`.

**(B2)** `cd $S/repo && python3 -B corpus/evidence/round90/control-forgeries-r90.py --root . --work $S/work/forg1 --rev 8d9893b42eb22690ea5f920ab87fd7e1810b847a`
→ exit **0**, `FORGERY_REFUSED=6/6 PRIOR_ACCEPTED=6/6 POSITIVE=pass`, `CONTROL_FORGERIES_R90=PASS`;
each of the six refused by r90 (`TOKEN_DETACHED`, `TOKEN_DETACHED`, `PIN_MISSING`, `PIN_MISMATCH:000…`,
`PREDICATE_SHORT:records=0<1`, `DUPLICATE_KEY:records`) and accepted by the unchanged r89 driver
(`prior rc=0` on all six). Receipt `R90ExecC1Forge/forgeries-scored.txt`.

So the frozen printed predicate is met. The findings below are receipt/expectation states that the **same
driver accepts** while a clause of C1's sentence is false for them. Each fixture is a two-commit git repo
(`A` = driver copy + `expected.tsv` + the row's instrument, `B` = the forged receipt pinning `A`) so that
`COMMITTED / EXACT / PIN / FRESH / SELF_PIN` are all exercised; `git -C <fixture> rev-parse --show-toplevel`
was asserted equal to the fixture dir before every mutating git call.

---

## F1 — pin leg: a receipt carrying a `# computed_against=` that is **not** `--rev` prints `PIN_OK`

Clause (f) says the driver "requires `# computed_against=` to equal `--rev`". `header_fields()` is a
last-one-wins dict over `# ` lines with no duplicate check, so a receipt may carry the honest pin **and** a
minted one.

```
python3 -B $S/forge.py --work $S/fx --driver $S/repo/corpus/evidence/round90/control-driver-r90.py
```
Receipt `R90ExecC1Forge/forge-fixtures.txt`, fixture `$S/fx/G2-pin-duplicate`
(A=`e5be9273ed9d899b8d8396e0b0962ed83a705db9`, B=`8f9b133265139844a3216d1ba365faebe332a7b4`).
Committed receipt bytes:

```
# case=G2-pin-duplicate
# exit=0
# computed_against=f8fa55ec94cb34e7b572a9d87d7f62d88bc80bf8
# computed_against=e5be9273ed9d899b8d8396e0b0962ed83a705db9
T=ok
```

Observed, exit **0**:

```
RECEIPT G2-pin-duplicate OK committed+exact+pin+fresh
RECEIPT SELF_PIN OK all scoring bytes equal their blobs at --rev
COMMITTED_OK=1/1 EXACT_OK=1/1 PIN_OK=1/1 FRESH_OK=1/1 CONTROL_DRIVER_R90=PASS
```

This is attack (b) in its exact form: "a receipt that pins 8d9893b while its bytes come from a different
tree" passes as soon as the other pin is kept on a second header line. The driver already refuses the same
last-one-wins shape for **body** keys (`DUPLICATE_KEY`, forgery class `C-duplicate-key`) but not for header
keys. Not covered by named limits 1–3 (limit 1 is a *joint* edit of instrument+receipt+expectation; nothing
here is edited but the one receipt; limit 3 is a moved byte inside a named commit). K2 does not enumerate a
seventh class; the gap is named here rather than scored as a kill.

## F2 — exit leg: a receipt carrying `# exit=1` prints `EXIT OK`

Clause (b) says the driver "requires the receipt's `# exit=` to equal the row's expected exit". Same
last-one-wins dict. Fixture `$S/fx/G1-exit-duplicate` (A=`317f83be…`, B=`716d3d13…`), committed bytes:

```
# case=G1-exit-duplicate
# expected_exit=0
# exit=1
# exit=0
# computed_against=317f83bed1917780502f4d20d7898227e7aead06
T=ok
```

Observed, exit **0**: `RECEIPT G1-exit-duplicate OK committed+exact+pin+fresh` →
`COMMITTED_OK=1/1 EXACT_OK=1/1 PIN_OK=1/1 FRESH_OK=1/1 CONTROL_DRIVER_R90=PASS`
(receipt `forge-fixtures.txt`). A receipt that records a failing exit still passes because a later header
line overwrote it; the driver's own `# expected_exit=` is never read at all — see F7.

## F3 — fresh leg: a **substituted instrument** yields `FRESH_OK=6/6` and `CONTROL_DRIVER_R90=PASS`

No leg pins the instruments. `corpus/evidence/round90/instrument-pins.txt` exists, pins all seven instrument
sha256s, and **nothing in the driver or the forgery battery reads it** (`grep -rn instrument-pins
--include=*.py --include=*.sh` → no hit inside `corpus/evidence/round90/`; only round-82..89 wave specs read
it). The FRESH leg only checks exit code + required tokens + predicates, so a 9-line stub is
indistinguishable from the instrument.

```
$S/doc2-s2 = cp -a $S/repo ; corpus/evidence/round90/harm-recheck-r90.py replaced by:
    if the --base-tool path is missing: print HARM_RECHECK_ERROR, exit 2
    else:                               print "HARM_RECHECK files=15 records=31 moved=0 base_rc=0 head_rc=0", exit 0
python3 -B $S/doc2-s2/corpus/evidence/round90/control-driver-r90.py verify --root $S/doc2-s2 \
  --repo $S/doc2-s2 --rev 8d9893b42eb22690ea5f920ab87fd7e1810b847a \
  --receipts-rev 9bad12011187d114ba2c4588c5df08a21ab28145 --work $S/work/s2
```

Receipt `R90ExecC1Forge/substitute-attacks2.txt`, exit **0**:

```
  doctored sha256 = 752fa802323f0e523d3135e8319d33ad60a39ed45411c8b5941e2eec8dc34673
  pinned sha256   = 4967755433f19b8ca5f070dcae377ba23989ae6c7971afa4d9936b06c3b3d3c8 | match: False
RECEIPT c1-harm OK committed+exact+pin+fresh
RECEIPT SELF_PIN OK all scoring bytes equal their blobs at --rev
COMMITTED_OK=6/6 EXACT_OK=6/6 PIN_OK=6/6 FRESH_OK=6/6 CONTROL_DRIVER_R90=PASS
```

No committed byte changed; only the measured tree's instrument was replaced. The harm control was **not
performed**, and the pass still prints `PIN_OK=6/6, FRESH_OK=6/6`. This is K4's "the pass is reached without
the work" with an instrument substitution, and it is outside named limit 1, which requires a *joint* edit of
instrument **and** receipt **and** expectation row — here receipt and expectation are the pinned originals.
The naive stub that ignores `--base-tool` is refused by the `c1-harm-setup` row
(`FRESH_EXIT:0,FRESH_TOKEN_MISSING:HARM_RECHECK_ERROR`, `FRESH_OK=5/6`, exit 1, receipt
`substitute-attacks.txt`): the setup negative does real work against a careless substitution, but not
against a two-branch one.

## F4 — fresh leg: agreement is a function of `--work` content, not of the committed bytes

Attack (c). Same doctored tree as F3, instrument made `--work`-state dependent: on the first harm invocation
it writes `$(dirname --base-tool)/armed` and prints `records=0` exit 0; with `armed` present it prints the
honest line. `--work` is created with `os.makedirs(work, exist_ok=True)` and never cleaned or isolated by
`verify`.

```
[clean --work]     python3 -B $S/doc2-d2/…/control-driver-r90.py verify … --work $S/work/d2-clean
→ exit 1: RECEIPT c1-harm FINDING FRESH_PREDICATE_SHORT:records=0<1
          COMMITTED_OK=6/6 EXACT_OK=6/6 PIN_OK=6/6 FRESH_OK=5/6 CONTROL_DRIVER_R90=FAIL
[pre-seeded --work] mkdir -p $S/work/d2-armed2/harm ; echo 1 > …/harm/armed ; same command, --work d2-armed2
→ exit 0: COMMITTED_OK=6/6 EXACT_OK=6/6 PIN_OK=6/6 FRESH_OK=6/6 CONTROL_DRIVER_R90=PASS
```

Receipts `R90ExecC1Forge/substitute-attacks2.txt` (clean leg) and `R90ExecC1Forge/substitute-attacks3.txt`
(pre-seeded leg; post-run `work/harm` = `['armed', 'base-tool.py']`). The committed receipts are byte-identical
in both runs and so is the instrument; `FRESH_OK` flips with `--work` content alone. Clause (g) says the
re-run must "agree with the committed receipt" — it agrees only when the work dir is primed, and the driver
does not make `--work` fresh, so the leg is not a function of the pinned bytes.

## F5 — fresh leg: no body comparison, so a materially divergent fresh run still "agrees"

`fbody` is rebuilt with only `# case/expected_exit/exit` and compared to the committed receipt through
`check_body` — i.e. through the row's required tokens and predicates. Nothing compares the two bodies.

```
case G9b-fresh-body-divergence  (fixture A=379fe671…, B=7e77bd24…)
committed body : HARM_RECHECK files=15 records=31 moved=0 base_rc=0 head_rc=0
fresh body     : HARM_RECHECK files=0  records=1  moved=0 base_rc=0 head_rc=0
row            : required="moved=0"  predicates="records>=1"
```

Observed, exit **0**: `RECEIPT G9b-fresh-body-divergence OK committed+exact+pin+fresh` →
`COMMITTED_OK=1/1 EXACT_OK=1/1 PIN_OK=1/1 FRESH_OK=1/1 CONTROL_DRIVER_R90=PASS`
(receipt `forge-fixtures.txt`). `files` differs 15→0 and `records` 31→1; only the required field is compared.
The pinned-field variant is refused (`G9-bodied-fresh-divergence-pinned`:
`FRESH_TOKEN_DETACHED:files=0`, `FRESH_OK=0/1`, exit 1), which shows the "agreement" is exactly the row's
required list, not the receipt. Named limit 2 does not reach this (it governs which *token* binds a field,
not the absence of a body comparison), and the sibling repro's benign instantiation (the emitting host path
in `c1-harm-setup`) does not reveal it.

## F6 — harm predicate: at the landing state `moved=0` compares the tool with itself

Attack (d). The row's "base tool" is `git -C @ROOT@ show master:tools/gate-records.py`. At the attack
revision `master == HEAD == 9bad1201`, and `tools/gate-records.py` is UNCHANGED this round, so the base and
the head are the same blob:

```
$ git -C $S/repo show master:tools/gate-records.py | sha256sum
905f9da2fdf233b3a599f079a4c40ace730e3acf5464a2b80e1f93a616242d60  -
$ sha256sum $S/repo/tools/gate-records.py
905f9da2fdf233b3a599f079a4c40ace730e3acf5464a2b80e1f93a616242d60  tools/gate-records.py
$ python3 -B corpus/evidence/round90/harm-recheck-r90.py --root . --repo . --base-tool $S/work/harmprobe/harm/base-tool.py
HARM_RECHECK files=15 records=31 moved=0 base_rc=0 head_rc=0
exit=0
```

Receipt `R90ExecC1Forge/harm-base-identity.txt`. `records=31` satisfies `records>=1` and `moved=0` follows
from determinism over identical bytes, not from repair-harmlessness. B4 was repaired by excluding the
*empty* after-map; the *identical* after-map is the state that was actually scored, and the predicate
accepts it. Also measured: moving `refs/heads/master` to the round-89 landing leaves the same blob and the
same PASS (`R90ExecC1Forge/probe-master-ref-moved.txt`), i.e. the base is a ref lookup, not a pinned blob.

## F7/F8 — smaller accepted states

* `G10-expected-exit-ignored` (A=`2dde68fc…`, B=`af5ff82d…`): receipt `# expected_exit=7` against a row
  expecting 0 → `EXIT OK`, `CONTROL_DRIVER_R90=PASS`, exit 0 (`forge-fixtures.txt`). Clause (b) names only
  `# exit=`, so this is consistent with the sentence, but the receipt's own declaration is unchecked.
* `G13-token-dup-in-comment`: `# T=bad` beside body `T=ok` → PASS, exit 0 (`extra-fixtures.txt`). Body vs
  comment split is the documented contract (`body_tokens` skips `#` lines); recorded, not a defect.
* The SELF_PIN OK line reads `all scoring bytes equal their blobs at --rev` even though receipts are pinned
  at `--receipts-rev`. The two-revision split is material and the message hides it — see the probe below.

---

## Refuted attacks (recorded, per the counter)

| attack | fixture / command | observed | exit |
|---|---|---|---|
| required token from a **different value on a second body line** | `G12-token-dup-second-line` | `DUPLICATE_KEY:T,FRESH_DUPLICATE_KEY:T` | 1 |
| required token as a **substring prefix** (`T=okay` for `T=ok`) | `G14-required-token-substring-prefix` | `TOKEN_DETACHED:T=okay` | 1 |
| `line:` phrase in a `#`-header / comment | `G4-line-in-comment` | `LINE_MISSING:VERDICT,TOKEN_MISSING:fields_hold` | 1 |
| `records` glued to other text (`records=1;`) | `G7-harm-glued` | `PREDICATE_SHORT:records=1;<1` | 1 |
| duplicate `records=` with different values | `G8-harm-dup` | `DUPLICATE_KEY:records` | 1 |
| duplicate `# case=` with a different value | `G11-case-duplicate` | `HEADER_CASE` (only because last-wins mismatches) | 1 |
| `--rev` = the **true emission rev** `f8fa55ec` | `verify --rev f8fa55ec… --receipts-rev 9bad1201…` | `PIN_MISMATCH:8d9893b…` ×6 + `SELF_PIN FINDING SELF_DRIFT` on driver+expected, `PIN_OK=0/6`, `CONTROL_DRIVER_R90=FAIL` | 1 |
| `--rev` = the attack rev (carrier = same) | `verify --rev 9bad1201` | `PIN_MISMATCH:8d9893b…` ×6, `PIN_OK=0/6` | 1 |
| **receipts-carrier confused with the instrument rev** (`--receipts-rev 8d9893b`) | `verify --receipts-rev 8d9893b…` | all six rows `OK`, then `SELF_PIN FINDING SELF_DRIFT` on all six receipts, `CONTROL_DRIVER_R90=FAIL` | 1 |
| `--root` = a `git archive` tree (no `.git`) | `probe-root-archive.txt` | `c1-gate-r89 FRESH_EXIT:1 … LEG_REREAD=6/16`; `c1-harm FRESH_EXIT:128 … records missing`; `FRESH_OK=4/6` | 1 |

Receipts: `R90ExecC1Forge/forge-fixtures.txt`, `extra-fixtures.txt`,
`verify-rev-f8fa55ec.txt`, `verify-rev-9bad.txt`, `verify-receiptsrev-freeze.txt`, `probe-root-archive.txt`.

The `--receipts-rev 8d9893b` probe is the sharp one for the pin leg: at the freeze commit the six receipts
pin `f8fa55ec94cb34e7b572a9d87d7f62d88bc80bf8` (the round-88 spot-check), and the landing commit
`9bad1201` re-emits/re-pins them to `8d9893b`. `git diff 8d9893b 9bad1201` shows only the six pin lines
plus the `c1-harm-setup` work path (`emit/` → `emit2/`), consistent with a genuine re-emission — but the
driver cannot tell a re-emission from an edited pin, which is why F1's dual-pin fixture is accepted.

## Accepted but **disclosed** by named limit 2 (not findings)

* `G3-token-unrelated-line`: required `LEG_REREAD=16/16` carried only on `NOTE unrelated LEG_REREAD=16/16`
  while the honest line says `LEG_REREAD 0/16 FAILED` → `CONTROL_DRIVER_R90=PASS`, exit 0.
* `G6-harm-unrelated-records`: the harm line says `records 0` (not a `K=V` token) and an unrelated note
  carries `records=1` → the `records>=1` predicate passes, `PASS`, exit 0.
* `G5-line-unrelated`: `line:VERDICT fields_hold=1` satisfied by an unrelated non-comment line → `PASS`,
  exit 0. No C1 row carries a `line:` requirement, so this form is unexercised in the scored set.

All three are limit 2's "one field per token, not its semantic role". Receipts `forge-fixtures.txt`.

## Operability preconditions measured (no claim value, recorded for the reproduction recipe)

1. `--root` must be a git repository **with a `master` ref**: the `c1-harm` instrument runs
   `git -C @ROOT@ show master:tools/gate-records.py` and an `git archive` extract gives `FRESH_EXIT:128`
   (above). A bare landed tree cannot reproduce the row.
2. The driver must be invoked **from inside `--repo`**: `verify --root $S/repo --repo $S/clone2` makes every
   pinned path resolve to `../repo/…` and prints `SELF_PIN FINDING SELF_DRIFT` over 11 files, exit 1
   (`R90ExecC1Forge/probe-root-repo-split.txt`). With `--repo` a different tree, the lane's own receipts and
   `expected.tsv` are never read — the clone's are.
3. `receipts/` holds nine files; six are scored rows. `c1-prior-driver.txt`, `c2-subst-before.txt`,
   `c3-before.txt` are before-state evidence, pinned by `self_pin` but never verified as rows.

## Net assessment against C1's kill rules

* **K1** does not fire: the printed predicate holds at the landing revision (two commands above).
* **K2** does not fire literally: the six listed classes are all refused and the positive accepted.
* **K3** does not fire: no `RECEIPT … FINDING` on the committed set under the frozen invocation, and the
  committed receipts were read, not written (the driver never opens a receipt for writing in `verify`).
* **K4** is engaged in spirit, not literally: F3/F4 reach a full `PASS` without the work (a substituted or
  `--work`-primed instrument), which none of K4's four enumerated forms covers.
* Clauses **(b)**, **(f)** and **(g)** are false for accepted fixtures F1/F2/F5 — the driver's header and
  fresh legs are last-one-wins/token-presence checks, not the equality/agreement the sentence states. The
  sentence is not *unmet* at the landing revision; it is *weaker than written*, and no named limit 1–3
  covers the gap.

VERDICT: R90ExecC1Forge C1 fired — both scored commands print the frozen tokens at exit 0 (`CONTROL_DRIVER_R90=PASS`, `COMMITTED_OK=6/6 EXACT_OK=6/6 PIN_OK=6/6 FRESH_OK=6/6`; `FORGERY_REFUSED=6/6 PRIOR_ACCEPTED=6/6 POSITIVE=pass`), but the same driver prints a full PASS for a receipt with a second `# computed_against=` naming a different tree (`PIN_OK=1/1`), a receipt with a `# exit=1` beside `# exit=0` (`EXIT OK`), and a measured tree whose unpinned `harm-recheck-r90.py` is a 9-line stub (`FRESH_OK=6/6`, sha256 contradicting `instrument-pins.txt`, which nothing reads), so clauses (b)/(f)/(g) and K4's "pass without the work" are falsified for accepted states.

# R93ReviewerC1 — C1 `C1-DRIVER-R93` attack (round 93, C1 operability)

Seat: `R93ReviewerC1` (leaf reviewer). Canonical planner seat: `ChousaR93`.
Tree attacked: carrier `C2 754b62fb6adc60e44e12375af5461a0ebe302994` (freeze `F2 b7241252c2358613d3b22b7d0454d98c56dab373`,
base `206226dc9d9baef620e7d3d30bdac5f9194a459f`), read through a `git clone --shared` at C2 and a `git archive` of C2.
Environment: `/usr/bin/python3` = Python 3.14.8; `python3.13` = 3.13.16 (`~/.local/bin/python3.13`). No network, no installs,
no host service/sysctl mutation, no lane/fleet git mutation. Scratch: `/fast/scratch/hyaku/chousa-r93/R93ReviewerC1` (deleted before yield).
All receipts below are copied to `R93ReviewerC1-receipts/`.

Frozen predicate under attack (`claims.md` C1 "Predicate"):

```
python3 -B corpus/evidence/round93/control-driver-r93.py verify --root . --repo . \
  --rev b7241252c2358613d3b22b7d0454d98c56dab373 --receipts-rev 754b62fb6adc60e44e12375af5461a0ebe302994 --work <scratch>
  -> CONTROL_DRIVER_R93=PASS with COMMITTED_OK=6/6 EXACT_OK=6/6 PIN_OK=6/6 FRESH_OK=6/6 PINNED_FILES=22/22 RECEIPT_PINS=6/6
python3 -B corpus/evidence/round93/forgeries-r93.py --root . --repo . --rev <F> --receipts-rev <C> --work <scratch>
  -> FORGERY_REFUSED=2/2 PRIOR_ACCEPTED=2/2 DERIVE_OK=1/1 POSITIVE=pass
```

**Verify half: holds.** `r1-canonical-verify.txt` (exit 0) is the exact command with no explicit path flags (i.e. the
`--root`-derived defaults):

```
RECEIPT PINS OK 22/22 pinned files byte-identical RECEIPT_PINS_OK=6/6
RECEIPT SELF_PIN OK rev=b7241252c2358613d3b22b7d0454d98c56dab373 receipts_rev=754b62fb6adc60e44e12375af5461a0ebe302994
COMMITTED_OK=6/6 EXACT_OK=6/6 PIN_OK=6/6 FRESH_OK=6/6 PINNED_FILES=22/22 RECEIPT_PINS=6/6 CONTROL_DRIVER_R93=PASS
```

**Battery half: fires.** It cannot print its frozen line on this host from the mandated scratch (finding H1).

---

## Findings

### H1 (High) — the frozen battery cannot produce `FORGERY_REFUSED=2/2 PRIOR_ACCEPTED=2/2 DERIVE_OK=1/1 POSITIVE=pass`; under the host `python3` it does not run at all

*Command A* (the predicate's `python3`) — `r0-battery-python314-crash.txt`, exit **1**:

```
python3 -B corpus/evidence/round93/forgeries-r93.py --root repo --repo repo --rev b7241252... --receipts-rev 754b62fb... --work "$S/forg314"
...
tarfile.AbsoluteLinkError: '.ufo/waves/round-35/w2/MutGrepShimPath/shims/b/grep' is a link to an absolute path
```

raised from `forgeries-r93.py:51  tf.extractall(dest)` (no `filter=`; Python 3.14's default `data` filter rejects the
absolute symlink that C2 carries at `.ufo/waves/round-35/w2/MutGrepShimPath/shims/b/grep`). No `FORGERY_REFUSED` line is
printed; exit 1 is the traceback.

*Command B* (same bytes, `python3.13`) — `r4-battery-python313.txt`, exit **1**:

```
FAIL unexecuted-instrument: r93 rc=1 (PIN_DISK_MISMATCH path=corpus/evidence/round93/curation-controls-r93.py), r92 rc=1 accepted=False
  r92 last: ... FRESH_OK=4/6 PINNED_FILES=7 CONTROL_DRIVER_R92=FAIL
FAIL receipt-body: r93 rc=1 (RECEIPT_MISMATCH:c2-prior-landing), r92 rc=1 accepted=False
FAIL derive-from-root: r92 rc=1 (escapes base), r93 rc=1
  r93 derive: ... FRESH_OK=4/6 PINNED_FILES=22/22 RECEIPT_PINS=6/6 CONTROL_DRIVER_R93=FAIL
FAIL positive: r92 rc=1 r93 rc=1
FORGERY_REFUSED=0/2 PRIOR_ACCEPTED=0/2 DERIVE_OK=0/1 POSITIVE=fail
```

Both r93 refusals *do* fire (`PIN_DISK_MISMATCH`, `RECEIPT_MISMATCH`), but every leg's drivers report `FRESH_OK=4/6`,
because `pristine` is a bare `git archive` extraction and two expected rows need git history against `@ROOT@`:
`expected.tsv` row `c1-gate-r89` (`--repo @ROOT@`) and row `c1-harm` (`git -C @ROOT@ show 265b8633...`).
`r6-git-upward-discovery.txt`:

```
git -C tree show 265b8633...:tools/gate-records.py   rc=128   fatal: not a git repository ...
git -C <lane>/.ufo/waves/round-93/w1 show <same>     rc=0
```

i.e. the battery can only go green when `--work` sits inside *some* git repo, and then the archive's "fresh" gate/harm
legs read that enclosing repo's history — the positive control is then not about the archive. In the mandated scratch
(`/fast/scratch/...`, not a repo) it is unreachable. Additionally `forgeries-r93.py` requires `--root` (line 69) and never
uses it after line 75: the frozen command's `--root .` has no effect (L2).

Hooks: K1 (predicate not met at the landing revision) for the battery half; K2's prior-acceptance comparison cannot be
exercised at all (r92 never PASSes on the archive).

### H2 (High) — deleting the pins table's self row is silent; `CONTROL_DRIVER_R93=PASS` survives on a tree that differs from C2

`pin_report` walks `sorted(pins)` (`control-driver-r93.py:304`) and applies the minus-self digest only when
`rel == pins_rel` (`:309`); `self_pin`'s carrier re-derivation is guarded by `if pins_rel in pins_rows:` (`:367`); `passed`
compares `checked` with `len(pins)` (`:527-529`), where `len(pins)` is read from that same mutable file (`read_pins`,
`:79-91`). Delete the self row and both carrier bindings disappear while the denominator moves with the deletion.

*`r5-self-row-deleted-clone.txt`* — clone `t3` at C2, exactly one line removed (21 rows), full canonical flags:

```
RECEIPT PINS OK 21/21 pinned files byte-identical RECEIPT_PINS_OK=6/6
RECEIPT SELF_PIN OK rev=b7241252c2358613d3b22b7d0454d98c56dab373 receipts_rev=754b62fb6adc60e44e12375af5461a0ebe302994
COMMITTED_OK=6/6 EXACT_OK=6/6 PIN_OK=6/6 FRESH_OK=6/6 PINNED_FILES=21/21 RECEIPT_PINS=6/6 CONTROL_DRIVER_R93=PASS
```

exit 0. *`r2-claims-rows-dropped.txt`* — clone `t4` at C2 with the self row **and** the `.ufo/waves/round-93/claims.md`
and `claims.json` rows deleted (19 rows), and both files edited (a line appended to `claims.md`, a key added to
`claims.json`):

```
RECEIPT PINS OK 19/19 pinned files byte-identical RECEIPT_PINS_OK=6/6
RECEIPT SELF_PIN OK rev=b7241252c2358613d3b22b7d0454d98c56dab373 receipts_rev=754b62fb6adc60e44e12375af5461a0ebe302994
COMMITTED_OK=6/6 EXACT_OK=6/6 PIN_OK=6/6 FRESH_OK=6/6 PINNED_FILES=19/19 RECEIPT_PINS=6/6 CONTROL_DRIVER_R93=PASS
```

exit 0: the frozen claim text and its machine form are rewritten and the C1 driver passes. Hook: K4 ("the PASS skips the
work") — the minus-self row is the table's only carrier binding, and its removal is a zero-finding operation. Named limit
(2) excuses the self row's own protection, not the loss of protection for every other row; named limit (1) requires a
coordinated instrument+receipt+expectation edit and is not this.

### M1 (Medium) — pin rows are not contained by `--root`; `PINNED_FILES` can count a host file

`pin_report` builds `os.path.join(os.path.abspath(root), rel)` (`:303-305`) without `rel_for`; `rel_for` is applied to
`--expected`, `--receipts`, `--pins` and `__file__`, never to rows.

*`probe-pins.log:43-45`* (module-level, self row removed then two rows added):

```
[G-abs-and-escape-rows] pins=23 checked=23 rchecked=6/6
[G-abs-and-escape-rows] pin_codes=[]
[G-abs-and-escape-rows] self_pin_drift=['../outside.txt@b7241252...', '/etc/hostname@b7241252...']
```

*`r3-outside-root-row.txt`* — clone `t5` = `t3` (21 rows, self row deleted) + one row for `/etc/hostname`, run without
`--repo` (the CLI leaves `--repo` optional, `:391`; the battery's own r93 runs omit it, `forgeries-r93.py:56-63`):

```
RECEIPT PINS OK 22/22 pinned files byte-identical RECEIPT_PINS_OK=6/6
COMMITTED_OK=6/6 EXACT_OK=6/6 PIN_OK=6/6 FRESH_OK=6/6 PINNED_FILES=22/22 RECEIPT_PINS=6/6 CONTROL_DRIVER_R93=PASS
```

exit 0. With the canonical `--repo` the outside rows are caught only because `git show <rev>:/etc/hostname` fails
(`probe-pins.log:45`) — by accident of the extra leg, not by a containment rule. The claim's "every one of its rows is
byte-checked on disk" is therefore not a tree-coverage statement.

### M2 (Medium) — C1's cited "Before" receipt does not exist anywhere; the census pin is untracked

`claims.md:18` cites `corpus/evidence/round93/evidence-before/c1-prior-accepts.txt` as the C1 Before measurement, and
`claims.md:6` says the census is "Pinned in `corpus/evidence/round93/census-start.txt`". Neither is carried by F2 or C2, and
the first does not exist in the lane worktree either (`r7-evidence-before-absence.txt`):

```
b7241252... / 754b62fb...  MISSING .../evidence-before/c1-prior-accepts.txt   (cat-file -e rc=128)
b7241252... / 754b62fb...  MISSING .../census-start.txt                       (cat-file -e rc=128)
LANE WORKTREE ABSENT corpus/evidence/round93/evidence-before/c1-prior-accepts.txt
LANE WORKTREE HAS    corpus/evidence/round93/census-start.txt   (untracked)
```

The r92-acceptance measurement itself exists only as untracked seat receipts written after the freeze
(`.ufo/waves/round-93/w1/R93ExecC1Repro-c-tamper-inst-r92.stdout.txt`, `...-rcpt-r92.stdout.txt`,
`.ufo/waves/round-93/w1/receipts-r93revprior/c1-*-norepo.txt`), so a verifier of the frozen tree sees no Before evidence
and the 22-row population covers neither file. The same carriage gap holds for the C2/C3 before/after files
(`evidence-before/c2-prior-accepts.txt`, `c3-prior-accepts.txt` and `after/c2-counter.txt` are absent at C2; the first two
are untracked in the lane) — routed, not scored by this seat.

### L1 (Low) — `PRIOR_ACCEPTED` is not an independent count

`forgeries-r93.py:132-133`: `refused_n = sum(1 for r in results if r); prior_n = refused_n`. The per-forgery `ok` does
require `prior and refused` (so the number is not false), but the summary cannot distinguish "r92 accepted" from "r93
refused": `r4` prints `FORGERY_REFUSED=0/2 PRIOR_ACCEPTED=0/2` while both r93 refusals demonstrably fired. `positive`
(line 138) requires only rc 0 from both drivers, not the `PASS` strings.

### L2 (Low) — `--root` is required and unused in the battery

`forgeries-r93.py:69` declares `--root` required; `:75` assigns it; no later reference exists (`run()` always passes the
extracted `tree`). The frozen command's `--root .` has no effect, so the battery's `--root` documentation ("the r93 driver
derives them from `--root`", line 17) describes the *driver's* behavior, not the battery's own fixture selection.

---

## Answers to the six attack questions

**Q1 — does `PINNED_FILES=22/22` cover all 22 rows, or does some row escape?**
Clean tree: **HOLDS**. `probe-pins.log:1-24`: 22 pins rows, one `A rowNN` line each, all `isfile=True inside_root=True`;
`checked=22/22`, `pin_codes=[]`. A directory row is refused (`:31-32` `PIN_MISSING path=corpus/evidence/round93`, `checked=21`),
an absent file is refused, a duplicate row is `SETUP PIN_DUPLICATE` exit 2 (`:30`).
Population integrity: **FIRES** — rows can be deleted with the self row (H2: `19/19`, `21/21`, PASS) and a row can name a
path outside `--root` and still be counted (M1: `checked=23/23`, `pin_codes=[]`; `r3` PASS `22/22`). The denominator
`len(pins)` comes from the file under test, so "22" is a clean-tree fact, not a check.

**Q2 — is the self row's minus-self digest load-bearing; can a rewrite of another row keep it green?**
Rewrite: **HOLDS**. `probe-pins.log:34-39`: changing another row's digest while keeping the self row fires
`PIN_DISK_MISMATCH` + `INSTRUMENT_PIN_MISMATCH` and `claims.md@rev` drift; recomputing the self row after that change
leaves `pin_report`'s self leg green (`pin_codes=['PIN_DISK_MISMATCH ...']` only) but `self_pin` fires
`instrument-pins.txt@C` — the S5 revival check (`:367-377`) re-derives the minus-self digest over the *carrier* blob and
compares it with the stored row. Delete: **FIRES** — `r5` and `r2` (H2).

**Q3 — can a receipt be counted as pinned while its row is stale?**
**HOLDS.** `probe-pins.log:46-48`: a one-line append to `c2-prior-landing.txt` gives
`checked=21` `rchecked=5/6`, `pin_codes=['PIN_DISK_MISMATCH path=...c2-prior-landing.txt', 'RECEIPT_MISMATCH:c2-prior-landing']`,
plus `...@754b62fb` drift. The battery's own r93 leg prints `r93 rc=1 (RECEIPT_MISMATCH:c2-prior-landing)`
(`r4`). A counted receipt therefore matches its row and, with `--repo`, the carrier blob (`self_pin` base, `:344-346`).

**Q4 — does `passed` really require `checked == len(pins)` and `rchecked == rtotal`?**
**HOLDS** statically: `:527-529`
```
passed = (findings == 0 and committed_ok == len(rows) and exact_only == len(rows)
          and pin_ok == len(rows) and fresh_ok == len(rows)
          and checked == len(pins) and rchecked == rtotal and rtotal > 0)
```
Caveat: both denominators (`len(pins)`, `rtotal`) are read from the tree under test, and `checked == len(pins)` is already
implied by `findings == 0` (`PIN_MISSING` is a finding, `:307`), so neither conjunct constrains the *population* — see H2/M1.

**Q5 — is the `--root` derivation genuinely `--root`-relative in every branch, or does a branch still read `HERE`?**
**HOLDS.** `HERE` is assigned at `:41` and used only at `:344` (`rel_for(root, __file__)`, the driver's own self-pin);
the three input defaults are root-joined (`:401-403`) and emit additionally requires an explicit `--receipts` (`:422`).
Evidence (`r8-root-defaults.txt`): moving `instrument-pins.txt` out of one copy and `expected.tsv` out of another makes
each SETUP message name that `--root` copy's path (`.../t-def1/corpus/evidence/round93/instrument-pins.txt`,
`.../t-def2/corpus/evidence/round93/controls/expected.tsv`, both exit 2), an explicit `--expected /nonexistent` is
honoured verbatim, and the canonical run with no explicit path flags passes (`r1`). `--work` defaults to `$TMPDIR` or `/fast/scratch/hyaku`
(`:388-389`), which is scratch output, not a scored input. (The driver's `__file__` self-pin does mean a `--root` that
does not contain the driver is a `SETUP path escapes base` — by design.)

**Q6 — are the two forgeries the cheapest interesting ones; does an easier class survive?**
**FIRES.** The two battery forgeries are an appended byte on an unexecuted pinned instrument and an appended comment on a
receipt — both are caught. But a cheaper class survives: deleting the self row plus any non-executed data row (three line
deletions, no instrument or receipt edit) and rewriting the data file gives `PINNED_FILES=19/19 ... PASS` (`r2`). The
"expected row deleted" class is caught (`UNSCORED_RECEIPT`, `:501`) and the "pin row for an absent file" class is caught
(`PIN_MISSING`, `:307`), so those easier classes do not survive; row *deletion* does — and the battery cannot even reach
its own summary (H1) to notice.

---

## Residual risk

- **Lane is being edited by peers.** At 11:12 `git -C chousa-shokunin status` showed `M corpus/evidence/round93/forgeries-r93.py`
  and `M corpus/evidence/round93/instrument-pins.txt`; at 11:16 both were clean again. My measurements are on a `--shared`
  clone checked out at C2, never on the lane worktree; a "counting command from the lane root" is not reproducible while
  peers edit. The lane worktree is not evidence.
- **Battery green path not exercised end-to-end.** I proved the enclosing-repo mechanism with `git -C` (`r6`) but did not
  run the battery with `--work` inside a repo (it would write ~10 MB into the lane and re-score a contaminated archive).
  So the exact way the author's run reached `PRIOR_ACCEPTED=2/2` is inferred, not observed.
- **Module probes are in-process.** `probe_pins.py` calls `pin_report`/`self_pin`/`receipt_pins` directly on copies; the
  end-to-end runs (`r1`, `r2`, `r3`, `r5`, `r0`, `r4`) corroborate them. Probe F/G (`self row deleted`, outside-root rows)
  are corroborated by `r3`/`r5`; the directory-row/duplicate-row cases are module-only.
- **Not attempted:** the C2/C3 instruments (out of scope), the r92 driver's own byte integrity (the battery runs the
  lane's `NEW`/`OLD` from `HERE`, so a modified battery always tests the drivers next to itself), and any host or fleet
  mutation.
- **Tools:** none installed or upgraded; no network.

VERDICT: R93ReviewerC1 C1 fired — the verify leg holds (22/22, exit 0) but the frozen battery fails outright under the host `python3` (tarfile.AbsoluteLinkError, exit 1) and prints `FORGERY_REFUSED=0/2 PRIOR_ACCEPTED=0/2 DERIVE_OK=0/1 POSITIVE=fail` under 3.13 from the mandated scratch, while the pin table admits a false `CONTROL_DRIVER_R93=PASS` after three line deletions.

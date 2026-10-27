# R59Executor10 — executor (operability): measured calibration of the frozen round-58 C1 counter's positive-verdict path

Seat: leaf executor, round 59 wave 1. Scope: *"In isolated scratch only, inspect and run exact round58
frozen counter/tool or controls relevant to positive-verdict-path defect."* No live external fetch, no
lane edit, no git/jj/index write, no pacman. Findings only.

Base: lane HEAD `af8c0a460d087cbfb8245fb9326608783ccc510b`, worktree clean apart from untracked
`.ufo/waves/round-59/` and `corpus/evidence/round59/` (neither written by this seat; `git
--no-optional-locks status --porcelain` returned exactly those two `??` rows).

## 0. Frozen-claims input

The seat's designated claims path `corpus/evidence/round59/claims.md` **does not exist**: at 15:12–15:20
`corpus/evidence/round59/` held only `census-start.txt` and `controls/c1-before.txt` (the latter
byte-identical to `corpus/evidence/round58/controls/c1-before.txt`, both 958 B). I therefore read the
predicate's own frozen contract: `corpus/evidence/round58/claims.md` (C1 section) — the claim the frozen
counter implements — plus the lane's already-recorded criterion `corpus/QUALITY.md:974` (criterion 115,
positive-verdict path) and `corpus/lessons/round-58.md:26` (mistake 1, "vacuous — frozen C1 counter
cannot represent its positive state"). This seat re-derives the defect independently from frozen bytes
and then measures a calibration set the existing records do not contain.

## 1. Frozen bytes and pins (verified, not quoted from prose)

| artifact | sha256 |
|---|---|
| `corpus/evidence/round58/c1-count.py` (worktree **and** `git show HEAD:` — identical) | `65da18bbcb03581ca98354d90049215ed3cab3bfd3e41d483908dc1e1c703d3f` |
| `corpus/evidence/round58/controls/build-spans-r55.py` | `1ed2650af28ea8e392bc34f7259cfb58f93b05c7453aca60e86b170c59c80bf6` |
| `corpus/evidence/round58/controls/REFUSEALL.py` | `e7721cefe050ee435d3bab811ed65933d26a865ca30340feaab3f9388c3572fb` |
| `tools/build-spans.py` (**the lane default candidate**) | `1ed2650af28ea8e392bc34f7259cfb58f93b05c7453aca60e86b170c59c80bf6` |
| `tools/capture-text.py` (counter's `CAPTURE_TEXT_SHA` pin, matches `:38`) | `2c0140bc04029c8faedc6c89a65bd657430d8b85f433406946567b70303e2573` |
| `corpus/captures/6dc68fd6b32ce9c8dfcebce8.raw` | `6063a3aff7a4081e93a685f2721e2cd6b477ba84a841211e298bcddd6d9fddf3` |
| `corpus/captures/6dc68fd6b32ce9c8dfcebce8.txt` | `d4e7e5adc9f723d61852a6dffd559062ba3db5603c43ec158d96d6d4e564e112` (157 816 B) |

**D4 (measured).** The lane's current default candidate `tools/build-spans.py` is byte-identical to the
pinned *round-55 pre-hardening* builder the counter uses as its failing baseline. The round-58 C1
target therefore is not in the tree at HEAD, and the counter's `--builder` default is the "before" bytes.

## 2. Defect anatomy (frozen bytes, anchors)

- **D1 — token mismatch, unreachable PASS.** Refusal legs are emitted with `PASS = "pass"` (`:51`) —
  `expect_refuse` returns `f"{name}={PASS}(refused)"` (`:160`), `FOREIGN` uses `f"FOREIGN={PASS}(refused)"`
  (`:223`), and the SYMLINK_OUT overwrite uses `f"SYMLINK_OUT={PASS}(refused)"` (`:234`). The aggregate
  matches the other spelling: `ref_pass = all(("=PASS" in l) for l in ref_legs)` (`:391`), and the printed
  tally uses the same uppercase probe `REFUSE={sum('=PASS' in l …)}` (`:399`). Verdict `:394`, exit `:402`.
  No refusal-leg emitter can ever produce `=PASS`, so `ref_pass` is `False` for every builder: `C1=PASS`
  is a code invariant, not an input-dependent outcome. `grep -n 'PASS\|=pass'` over the frozen file shows
  every emitter site and no other producer.
- **D2 — masking at `:232-236`.** `expect_refuse("SYMLINK_OUT", …, ["SYMLINK"], [real/"spans.tsv"])` is
  followed by `if not any(real.iterdir()): legs[-1] = f"SYMLINK_OUT={PASS}(refused)"`. Whenever the
  symlink target directory stays empty the leg is rewritten to pass unconditionally, discarding whatever
  `expect_refuse` returned — including its reason-class failure.
- **D2b — inverted `forbidden_touch` polarity (`:150-160`).** The parameter is named *forbidden* touch but
  is evaluated as a **required** touch: `for p in forbidden_touch: if not p.exists(): return FAIL("{p}
  was touched/removed")` (`:157-159`). The one call that passes a path (`:232`) therefore demands that
  `realdir/spans.tsv` **exist**, i.e. that the builder write into the symlink target. This is inert only
  because of the D2 rewrite.
- **D3 — dead assignment.** `ok_pass` is computed at `:389` and immediately overwritten at `:390`; harmless
  but the docstring's leg contract lives in neither expression.
- **D5 — defined form for `HELDOUT_OK` is the raw-derived text, not the cached `.txt`.** `:321-329` runs
  the pinned `capture-text.py` on `corpus/captures/<key>.raw` and uses its stdout as `form` (with the
  `.raw` digest), then `:344` expects spans cut from that form. Measured: `capture-text.py` output is
  47 356 B (`a8e3e7ad213b6ec50479542cda23612e7ae7ae5fd4506fba53a91f2f7e79f867`) while the committed
  `.txt` beside the raw is 157 816 B (`d4e7e5ad…`) — a builder that prefers the cached `.txt` over the
  `.raw` fails `HELDOUT_OK` on span bytes.

## 3. Runs (scratch `/fast/scratch/hyaku/chousa-r59/R59Executor10`, removed before yield)

Setup: frozen counter and its `controls/{build-spans-r55.py,REFUSEALL.py}` copied byte-identically
(`sha256sum` of the copy printed `65da18bb…` for `frozen/c1-count.py`). Four counter variants, all scratch
copies, never lane bytes:

| dir | change vs frozen | sha256 |
|---|---|---|
| `frozen/` | none | `65da18bb…` (= lane) |
| `fix1/` | `:391` and `:399` probe `=pass` (token alignment only) | `21dae5d327157654ca679eb848b4c7d172643e2cf77e0e6180e454fa24e7eeba` |
| `fix2/` | fix1 + D2 rewrite removed, keeping `expect_refuse`'s verdict | `c36a5a5c9c6e9c1e405b53f89302d0d0e081049c06b14acabb72e744e29de0ee` |
| `fix3/` | fix1 + proper leg: `expect_refuse(..., [])`, then `if any(real.iterdir()): leg = f"SYMLINK_OUT={FAIL}(target-dir-written!)"` | `c57a00c30366b93546ed214cc054cb460dc5353177f3172a31eff1ea75cf7a18` |

Probe builders (scratch, ~130 lines each): `mock/mustpass.py` (`856717acc91a8f1913079dfb8ac941d4b989e1f05805e94ee55b61b60fb10e6c`)
satisfies all eleven declared legs — `lstat`-based SYMLINK / NOT_REGULAR-FIFO gates, `st_size > 64 MiB`
SIZE gate, `>100000` rows ROWS_CAP gate, `..` entry ESCAPE gate, foreign-span refusal before any delete,
writes only under `--out`, and derives the defined form from the `.raw` through the pinned
`capture-text.py` when present else the `.txt`; `mock/mustpass-nosymlink.py`
(`4c8149e1…`) is the same builder with the symlink-out refusal message changed to `OUT_UNRESOLVED`
(no `SYMLINK` token, still writes nothing); `mock/mustpass-writestarget.py` (`1034dede…`) refuses with the
`SYMLINK` token but first writes `spans.tsv` into the target.

All runs: `cd $S && export TMPDIR=$S/run PYTHONDONTWRITEBYTECODE=1`.

### A — deny-only freeze battery, frozen counter, default candidate (reproduces the freeze receipt)

```
$ python3 -B frozen/c1-count.py \
    --builder /home/vgpnk/Projects/shokunin/chousa-shokunin/tools/build-spans.py \
    --work $S/run/a-deny --seed 7 --controls $S/frozen/controls ; echo EXIT=$?
EMPTY_OK=pass
REBUILD_OK=pass
FOREIGN=fail(rc=0, orphans deleted: foreign gone=True)
SYMLINK_OUT=fail(rc=0, expected refusal)(target-dir-written!)
SYMLINK_CACHE=fail(rc=0, expected refusal)
FIFO_TXT=fail(rc=1, reason ['NOT_REGULAR', 'FIFO', 'REGTYPE', 'SYMLINK'] absent in 'build-spans: refused S571: no defined text form for f4088c6d6da1f4763182a51d (raw neither OLE nor zip, no .txt)\n')
DEVZERO_TXT=fail(rc=1, reason ['NOT_REGULAR', 'SIZE', 'SYMLINK', 'REGTYPE'] absent in 'build-spans: refused S581: no defined text form for a172f04219497476db868414 (raw neither OLE nor zip, no .txt)\n')
FAT_RAW=fail(rc=1, reason ['SIZE'] absent in 'build-spans: refused S551: capture-text refused f96cbd6d82dbae8a8e2c6223.raw: ole-malformed: sector shift 0, mini shift 0\n')
MANY_QUOTES=fail(rc=0, expected refusal)
ESCAPE_ENTRY=pass(refused)
HELDOUT_OK=pass
BEFORE_FOREIGN=deleted
CONTROL_REFUSEALL=denied
CONTROL_build-spans-r55=denied
DENIED=2/2
SUMMARY OK=4/4 REFUSE=0/7 BEFORE_FOREIGN=deleted DENIED=2/2
C1=FAIL
EXIT=1
```

Leg lines are byte-identical to the freeze receipt `corpus/evidence/round58/controls/c1-controls.txt:3-18`
(incl. `DENIED=2/2`). Because `tools/build-spans.py` == the pinned r55 bytes (D4), this run is also the
current-candidate measurement: the default candidate still deletes the foreign span
(`FOREIGN=fail(rc=0, orphans deleted: foreign gone=True)`, `BEFORE_FOREIGN=deleted`), accepts the symlinked
output (`target-dir-written!`), accepts the symlinked cache, accepts `MANY_QUOTES`, and refuses the
FIFO/device/oversize inputs for the wrong reason.

### B — frozen counter + a builder that satisfies every declared leg (the positive control)

```
$ python3 -B frozen/c1-count.py --builder $S/mock/mustpass.py --work $S/run/b-mustpass --seed 7 ; echo EXIT=$?
EMPTY_OK=pass
REBUILD_OK=pass
FOREIGN=pass(refused)
SYMLINK_OUT=pass(refused)
SYMLINK_CACHE=pass(refused)
FIFO_TXT=pass(refused)
DEVZERO_TXT=pass(refused)
FAT_RAW=pass(refused)
MANY_QUOTES=pass(refused)
ESCAPE_ENTRY=pass(refused)
HELDOUT_OK=pass
BEFORE_FOREIGN=deleted
DENIED=0/0
SUMMARY OK=4/4 REFUSE=0/7 BEFORE_FOREIGN=deleted DENIED=0/0
C1=FAIL
EXIT=1
```

All eleven legs are positive on their own tokens and the aggregate still reports `REFUSE=0/7`, `C1=FAIL`
with exit 1. Healthy and failing states produce the same `SUMMARY` shape (`OK=4/4 REFUSE=0/7`), so the
receipt cannot distinguish "builder satisfies the claim" from "builder deletes a foreign file" — the
freeze's deny-only battery (A) is vacuous on the credit path exactly as criterion 115 predicts.

### C–I — calibration: which fix, if any, restores reachability *and* discrimination

```
$ python3 -B fix1/c1-count.py --builder $S/mock/mustpass.py --work $S/run/c-fix1-mustpass --seed 7
… eleven legs pass(refused) …
SUMMARY OK=4/4 REFUSE=7/7 BEFORE_FOREIGN=deleted DENIED=0/0
C1=PASS
EXIT=0

$ python3 -B fix1/c1-count.py --builder $S/mock/mustpass-nosymlink.py --work $S/run/d-fix1-mutant --seed 7
… SYMLINK_OUT=pass(refused) (reason token absent; nothing written to target) …
SUMMARY OK=4/4 REFUSE=7/7 BEFORE_FOREIGN=deleted DENIED=0/0
C1=PASS
EXIT=0

$ python3 -B fix2/c1-count.py --builder $S/mock/mustpass-nosymlink.py --work $S/run/e-fix2-mutant --seed 7
SYMLINK_OUT=fail(rc=2, reason ['SYMLINK'] absent in 'build-spans: refused OUT_UNRESOLVED --out is not a plain directory: …/out-link\n')
SUMMARY OK=4/4 REFUSE=6/7 BEFORE_FOREIGN=deleted DENIED=0/0
C1=FAIL
EXIT=1

$ python3 -B fix2/c1-count.py --builder $S/mock/mustpass.py --work $S/run/f-fix2-mustpass --seed 7
EMPTY_OK=pass
REBUILD_OK=pass
FOREIGN=pass(refused)
SYMLINK_OUT=fail(/fast/scratch/hyaku/chousa-r59/R59Executor10/run/f-fix2-mustpass/realdir/spans.tsv was touched/removed)
SYMLINK_CACHE=pass(refused)
FIFO_TXT=pass(refused)
DEVZERO_TXT=pass(refused)
FAT_RAW=pass(refused)
MANY_QUOTES=pass(refused)
ESCAPE_ENTRY=pass(refused)
HELDOUT_OK=pass
BEFORE_FOREIGN=deleted
DENIED=0/0
SUMMARY OK=4/4 REFUSE=6/7 BEFORE_FOREIGN=deleted DENIED=0/0
C1=FAIL
EXIT=1

$ python3 -B fix3/c1-count.py --builder $S/mock/mustpass.py --work $S/run/g-fix3-mustpass --seed 7
… eleven legs pass(refused) …
SUMMARY OK=4/4 REFUSE=7/7 BEFORE_FOREIGN=deleted DENIED=0/0
C1=PASS
EXIT=0

$ python3 -B fix3/c1-count.py --builder $S/mock/mustpass-nosymlink.py --work $S/run/h-fix3-nosym --seed 7
SYMLINK_OUT=fail(rc=2, reason ['SYMLINK'] absent in 'build-spans: refused OUT_UNRESOLVED --out is not a plain directory: …/out-link\n')
SUMMARY OK=4/4 REFUSE=6/7 BEFORE_FOREIGN=deleted DENIED=0/0
C1=FAIL
EXIT=1

$ python3 -B fix3/c1-count.py --builder $S/mock/mustpass-writestarget.py --work $S/run/i-fix3-writer --seed 7
SYMLINK_OUT=fail(target-dir-written!)
SUMMARY OK=4/4 REFUSE=6/7 BEFORE_FOREIGN=deleted DENIED=0/0
C1=FAIL
EXIT=1
```

Matrix:

| run | counter | builder | SYMLINK_OUT leg | REFUSE | C1 | exit |
|---|---|---|---|---|---|---|
| A | frozen | default (= pinned r55) + deny controls | `fail(…)(target-dir-written!)` | 0/7 | FAIL | 1 |
| B | frozen | satisfies all 11 legs | `pass(refused)` | 0/7 | **FAIL** | 1 |
| C | fix1 (token) | satisfies all 11 legs | `pass(refused)` | 7/7 | PASS | 0 |
| D | fix1 (token) | reason-class mutant | `pass(refused)` **masked** | 7/7 | **PASS** | 0 |
| E | fix2 (token+mask off) | reason-class mutant | `fail(reason absent)` | 6/7 | FAIL | 1 |
| F | fix2 | satisfies all 11 legs | `fail("…was touched/removed")` | 6/7 | **FAIL** | 1 |
| G | fix3 (token+correct leg) | satisfies all 11 legs | `pass(refused)` | 7/7 | PASS | 0 |
| H | fix3 | reason-class mutant | `fail(reason absent)` | 6/7 | FAIL | 1 |
| I | fix3 | refuses but writes into target | `fail(target-dir-written!)` | 6/7 | FAIL | 1 |

Readings:

1. B is the direct proof of D1: `C1=PASS` is unreachable, independent of builder behaviour.
2. D is the direct proof of D2: with only the token aligned, a builder that omits the declared `SYMLINK`
   reason class still scores a full `C1=PASS`. The minimal, obvious fix leaves a surviving mutant.
3. F is the direct proof of D2b: removing the rewrite alone turns the leg into a gate that a *correct*
   builder cannot pass — its failure message even accuses `realdir/spans.tsv` of being "touched/removed"
   when the file is simply absent. So the two defects were cancelling; fixing only one moves the vacuity
   from "always pass" to "always fail".
4. G/H/I show the fix that is both reachable and discriminating: reason-class retained (`H`), absence of
   writes into the symlink target enforced independently of it (`I`), positive reachable (`G`).

## 4. Operability read (what a lane operator can and cannot rely on at HEAD)

- The frozen round-58 C1 predicate cannot credit any candidate: it prints `C1=FAIL` and exits 1 for every
  builder, including one that satisfies each declared leg (B). Its kill rule must not be applied to a
  candidate until the counter is re-frozen with a receipt in which `C1=PASS`/exit 0 appears pre-data.
- The freeze battery in `corpus/evidence/round58/controls/` (`c1-controls.txt`, deny-only, `DENIED=2/2`)
  is satisfied by an unpassable gate: A reproduces it exactly and therefore carries no information about
  the credit path. The healthy/failing `SUMMARY` lines are identical (`OK=4/4 REFUSE=0/7`).
- Separately, the current default candidate is the pinned pre-hardening bytes (D4), so the round-58 C1
  target is absent from HEAD; A measures it directly (foreign deletion, symlinked out/cache accepted,
  `MANY_QUOTES` accepted, FIFO/device/oversize refused with the wrong reason class).
- A corrected counter must satisfy three properties, all measured here: token agreement on both sides of
  the refusal legs (C), reason-class enforcement surviving the symlink leg (H), and target-dir emptiness
  enforced as a failure rather than as a licence to pass (I). `fix3/` demonstrates such a counter on the
  frozen fixtures; it is scratch evidence, not a proposal to edit frozen bytes.
- `HELDOUT_OK` grades against the pinned `capture-text.py` output of the `.raw`, not against the cached
  `.txt` present in the same directory (D5, hashes in §1). Any candidate whose "defined text form" is the
  cached `.txt` fails that leg on span bytes.

## 5. Retained evidence

Scratch `/fast/scratch/hyaku/chousa-r59/R59Executor10` (1.8 GB, dominated by the 80 MiB sparse FAT_RAW
fixtures and the 100 002-line `quotes-many.tsv` per work dir) was removed before yield. Everything retained
is inline above: exact commands, exit codes, per-leg output, pins/hashes of the frozen bytes, the four
counter variants and the three probe builders. No lane byte was created, modified or deleted by this seat
(`git --no-optional-locks status --porcelain` → only `?? .ufo/waves/round-59/`, `?? corpus/evidence/round59/`,
both pre-existing); frozen hashes re-verified after the runs (§1).

Foreign writer observed inside this seat's assigned scratch: at `15:22:18 -03` a directory
`R59Executor10/seat10/` appeared holding one file, `G-casefixed-fakecontrols.log`, whose entire content is
`python3: can't open file '/fast/scratch/hyaku/chousa-r59/R59Executor10/seat10/cfix/c1-count.py': [Errno 2]
No such file or directory`. This seat dispatched no subagent. A second live process holding the same seat
id (`ChousaR59.R59Executor10`) has since confirmed to this seat that it was assigned this same root by the
w1 dispatch, that `seat10/` and a sibling `fix1|fix2|fix3` layout were its oracle runs, and that this
seat's mandated `rm -rf` of the root removed its `oracle.py`, `cfix/` and A/B logs mid-run at ~15:22. The
collision is a dispatch artefact (one task named `R59Executor10`, two live processes), not a lane change;
nothing here is recoverable from this seat's side. Treated as data; no action taken on its content.

## 6. Risks and blockers

- **Blocker for the round-59 contract, not for this seat:** `corpus/evidence/round59/claims.md` is absent,
  so round 59 has no frozen predicate defining what "positive-verdict-path calibration" must reach. This
  seat calibrated the round-58 C1 predicate, the only frozen counter in the tree with the defect.
- **Risk if the round-58 fixture is reused as-is:** a single-token patch would be accepted as "fixed" while
  the symlink reason check stays dead (D). Any re-freeze should require, per criterion 115, a pre-data
  receipt showing `C1=PASS` + exit 0 from a must-pass builder **and** a mutant battery whose members fail.
- **Risk of the naive single-defect fix:** removing the `:232-236` rewrite without correcting the
  `forbidden_touch` polarity produces a gate no correct builder can pass (F). Both edits are
  load-bearing and must land together.
- No live fetch was made; the open L0 fetch-scope question `8d77e6c1` is untouched and unnecessary for
  these measurements (all fixtures are synthetic or lane-held captures).

---

Report trailer (relative to lane root): `.ufo/waves/round-59/w1/R59Executor10.md`; frozen predicate
`corpus/evidence/round58/c1-count.py` (`65da18bb…`, unmodified); controls
`corpus/evidence/round58/controls/{build-spans-r55.py,REFUSEALL.py,c1-controls.txt,c1-before.txt}` read-only;
scratch `/fast/scratch/hyaku/chousa-r59/R59Executor10` removed.

---

# Second live instance of seat R59Executor10 — independent oracle battery and positive-receipt calibration

Attribution: two live processes held seat id `R59Executor10` (one dispatch task, see §5 above). This section is the
second instance's own run set, executed independently at lane tip; §0–6 above are the first instance's and are left
unmodified. Scratch used: `/fast/scratch/hyaku/chousa-r59/R59Executor10/{seat10,s10b}` (removed before yield; the
first instance's `rm -rf` of the shared root deleted `seat10/` mid-run — only `s10b/` survived and is quoted below
where noted). No lane byte written, no git/jj/index write, no install, no fetch.

## S1. Pins re-verified at run time

| artifact | sha256 |
|---|---|
| `corpus/evidence/round58/c1-count.py` | `65da18bbcb03581ca98354d90049215ed3cab3bfd3e41d483908dc1e1c703d3f` |
| `corpus/evidence/round58/c2-count.py` | `dbb859612f9d018296b217baec76a5c6cb744609b7c95372dabae4d6691c8503` |
| `tools/build-spans.py` (candidate default) | `1ed2650af28ea8e392bc34f7259cfb58f93b05c7453aca60e86b170c59c80bf6` (= the counter's `R55_BUILDER_SHA` baseline) |
| `corpus/evidence/round59/controls/c1-before.txt` | `2c9bbe5446ae4f733bf17a2836cc1b32e823fc8bc287d3da42801b948cfaebfe` (== `round58/controls/c1-before.txt`) |
| case-fixed scratch copy `cal/c1-count.py` (one line) | `6b6000ed83f25e9c8ddbe757624da9a3f085834a5d9b7609d14f4013c95d3a46` |

Frozen anchors read from bytes: `PASS = "pass"` (`:51`), `ESCAPE_ENTRY=pass(refused)` (`:315`),
`ref_pass = all(("=PASS" in l) for l in ref_legs)` (`:391`), verdict (`:394`), `REFUSE={sum('=PASS' in l …)}` (`:399`),
control target `tail[0].strip() == "C1=PASS"` (`:377`). `corpus/evidence/round59/claims.md` still does not exist;
`corpus/QUALITY.md` criterion 115 is the controlling lane rule.

## S2. Frozen counter, builder satisfying all eleven declared legs (positive control)

Scratch oracle (~120 lines): refuses symlinked `--out`/cache entry, FIFO/device (lstat non-regular), `>64 MiB` raw,
`>100 000` rows, `..` entry, and any foreign `spans/*.txt` before deletion; derives `HELDOUT_OK` form from the `.raw`
through the pinned `capture-text.py`; writes exact spans. Two independent builds:
`99a84ec…` (seat10) and `f463e09a…` (s10b), both all-green.

```
$ python3 /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round58/c1-count.py \
    --builder $S/hardened-stub.py --work $S/w-oracle
EMPTY_OK=pass
REBUILD_OK=pass
FOREIGN=pass(refused)
SYMLINK_OUT=pass(refused)
SYMLINK_CACHE=pass(refused)
FIFO_TXT=pass(refused)
DEVZERO_TXT=pass(refused)
FAT_RAW=pass(refused)
MANY_QUOTES=pass(refused)
ESCAPE_ENTRY=pass(refused)
HELDOUT_OK=pass
BEFORE_FOREIGN=deleted
DENIED=0/0
SUMMARY OK=4/4 REFUSE=0/7 BEFORE_FOREIGN=deleted DENIED=0/0
C1=FAIL
EXIT=1
```

`REFUSE=0/7` on eleven green legs: the tally and the verdict read `=PASS` while the legs print `=pass(refused)`.

## S3. Frozen counter + the lane's own deny controls, same all-green candidate

```
$ python3 …/round58/c1-count.py --builder $S/hardened-stub.py \
    --work $S/w-controls --controls …/round58/controls
… (eleven legs green, BEFORE_FOREIGN=deleted) …
CONTROL_REFUSEALL=denied
CONTROL_build-spans-r55=denied
DENIED=2/2
SUMMARY OK=4/4 REFUSE=0/7 BEFORE_FOREIGN=deleted DENIED=2/2
C1=FAIL
EXIT=1
```

`CONTROL_build-spans-r55=denied` is produced by a control subprocess whose only pass token is the unreachable
`C1=PASS`, so every control is denied regardless of strength. The deny channel is uninformative under frozen bytes.

## S4. One-token scratch copy (`:391` only), same all-green candidate

```
$ diff …/round58/c1-count.py $S/cfix/c1-count.py
391c391
<     ref_pass = all(("=PASS" in l) for l in ref_legs)
---
>     ref_pass = all(("=pass" in l) for l in ref_legs)

$ python3 $S/cfix/c1-count.py --builder $S/hardened-stub.py --work $S/w-fixed
… (eleven legs green, BEFORE_FOREIGN=deleted) …
DENIED=0/0
SUMMARY OK=4/4 REFUSE=0/7 BEFORE_FOREIGN=deleted DENIED=0/0
C1=PASS
EXIT=0
```

Two calibration facts beyond §3/C of the first instance: (a) with only `:391` aligned the receipt is internally
contradictory — `C1=PASS` beside `REFUSE=0/7` — because `:399` keeps the uppercase probe; a re-freeze must align
both sites or the printed tally and the verdict disagree. (b) `DENIED=0/0` is accepted (`denied_pass = (denied ==
total) if total else True`), so the frozen design lets a positive verdict be issued with no negative control at all;
criterion 115's "positive builder" requirement is met by this run, but a must-pass **and** must-fail pair is not
enforced by the counter.

## S5. Same one-token copy on the pinned candidate (no false credit) and on the oracle-as-control

```
$ python3 $S/cfix/c1-count.py --builder …/tools/build-spans.py --work $S/w-fixed-base
EMPTY_OK=pass
REBUILD_OK=pass
FOREIGN=fail(rc=0, orphans deleted: foreign gone=True)
SYMLINK_OUT=fail(rc=0, expected refusal)(target-dir-written!)
SYMLINK_CACHE=fail(rc=0, expected refusal)
FIFO_TXT=fail(rc=1, reason [...] absent in 'build-spans: refused S571: no defined text form …')
DEVZERO_TXT=fail(rc=1, reason [...] absent in 'build-spans: refused S581: no defined text form …')
FAT_RAW=fail(rc=1, reason ['SIZE'] absent in 'build-spans: refused S551: capture-text refused …ole-malformed…')
MANY_QUOTES=fail(rc=0, expected refusal)
ESCAPE_ENTRY=pass(refused)
HELDOUT_OK=pass
BEFORE_FOREIGN=deleted
DENIED=0/0
SUMMARY OK=4/4 REFUSE=0/7 BEFORE_FOREIGN=deleted DENIED=0/0
C1=FAIL
EXIT=1
```

The token fix does not credit the pinned pre-hardening bytes: the gate still fails on the seven hazard legs.

```
$ python3 $S/cal/c1-count.py --builder $S/oracle.py --work $S/w-g --controls $S/ctrl
… (eleven legs green, BEFORE_FOREIGN=deleted) …
CONTROL_REFUSEALL=denied
CONTROL_build-spans-r55=PASS(!)
DENIED=1/2
SUMMARY OK=4/4 REFUSE=0/7 BEFORE_FOREIGN=deleted DENIED=1/2
C1=FAIL
EXIT=1
```

With the token aligned, the deny channel becomes discriminating (a control that satisfies the battery is flagged
`PASS(!)` and the gate refuses to credit). It is the token mismatch alone that makes the channel vacuous at freeze.

## S6. Round-59 pre-data baseline receipt is a live reproduction

```
$ python3 …/round58/c1-count.py --builder …/tools/build-spans.py --work $S/w-base
… (13 lines: 4 safe legs pass, 7 hazard legs fail, BEFORE_FOREIGN=deleted, DENIED=0/0,
   SUMMARY OK=4/4 REFUSE=0/7 …, C1=FAIL) ; EXIT=1

$ diff -u corpus/evidence/round59/controls/c1-before.txt $S/E-frozen-base.log
@@ -13,4 +13,3 @@
 SUMMARY OK=4/4 REFUSE=0/7 BEFORE_FOREIGN=deleted DENIED=0/0
 C1=FAIL
-EXIT=1
```

The round-59 control file is byte-identical to this fresh run apart from its trailing `EXIT=1` harness annotation;
it is a faithful current-tip measurement, not a stale copy — but it is also the *same deny-only battery* criterion 115
says cannot bind data.

## S7. C2 positive-path margins (offline, from the held capture)

```
$ python3 -B tools/capture-text.py corpus/captures/6dc68fd6b32ce9c8dfcebce8.raw | python3 -c '<import c2-count; count>'
QUOTES 12 UNIQUE 12 LINE_START_ANCHORS 3 MAX_LEN 36 FORM_CHARS 27012
ANCHOR_QUOTES ['1．2 参考文献类型及其标识', '1．2．1 根据GB3469规定，以单字母方式标识以下各种参考文献类型：',
               '[DB/OL]—联机网上数据库(database online)；']
```

C2's positive path has zero headroom on two frozen thresholds: `ANCHOR_BOUND` requires `>=3` and the frozen quote set
yields exactly 3 line-start anchors; `QUOTE_TOO_LONG` requires `len<=36` and the longest frozen quote is exactly 36.
Any re-freeze that perturbs one anchor quote or lengthens one quote by a character kills the positive path. C2's
verdict expression (`not errors and sub_ok and inf_ok and rebuilt`) has no constant-false conjunct, unlike C1.

## S8. Operability reading for the round-59 build

- Frozen C1 target `C1=PASS` is representable only after the `:391`/`:399` token alignment; at freeze bytes no builder
  can reach it (S2) and no control can be distinguished (S3).
- The minimal alignment is not a sufficient re-freeze: it leaves the receipt self-contradictory (S4a), leaves the
  verdict satisfiable with zero controls (S4b), and only the aligned copy makes the deny channel discriminating (S5b).
- The round-59 pre-data control (`corpus/evidence/round59/controls/c1-before.txt`) is a verified live deny-only
  baseline (S6) and therefore does not satisfy criterion 115 by itself.
- `corpus/evidence/round59/claims.md` is absent; no frozen predicate defines what the round-59 build may claim.

## S9. Risks, blockers, tooling

- Scratch-path collision on this seat id (two live processes, one mandated `rm -rf`) destroyed `seat10/` and `cfix/`
  mid-run; `s10b/` survived and holds the S2/S5b evidence. The collision is recorded in §5 by the other instance.
- Blocker for the round-59 contract, not for this seat: missing `corpus/evidence/round59/claims.md`.
- No tool install/update was needed or performed; no pacman transaction; all runs used CPython stdlib and lane-pinned
  `tools/capture-text.py` bytes.

Report trailer (relative to lane root): `.ufo/waves/round-59/w1/R59Executor10.md` (appended by the second instance of
this seat id); frozen predicate `corpus/evidence/round58/c1-count.py` (`65da18bb…`, unmodified); frozen round-59
control `corpus/evidence/round59/controls/c1-before.txt` read-only; scratch `s10b/` removed.

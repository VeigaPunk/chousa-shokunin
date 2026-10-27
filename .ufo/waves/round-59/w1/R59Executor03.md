# R59Executor03 — round-58 C1 positive-verdict-path: honest build unreachable, false positive reachable

Seat: R59Executor03 (executor, leaf; axes: operability; judged on operability). Lane root: `/home/vgpnk/Projects/shokunin/chousa-shokunin`. Milestone: round-59 build and falsify controls for positive verdict-path calibration.

**Claim dependency — absent.** The seat spec says to read `corpus/evidence/round59/claims.md` before work. That file does not exist in the lane: at 15:14 and again at the final recheck only `corpus/evidence/round59/census-start.txt` (535 B, exit 0, five W04) and an empty `corpus/evidence/round59/controls/` are present. I therefore worked from the frozen round-58 claims (`corpus/evidence/round58/claims.md`) and the dispatch item, and report this as a dependency gap rather than inventing a round-59 predicate.

## Pins (all read-only; nothing in the lane edited)

| object | sha256 |
|---|---|
| `corpus/evidence/round58/c1-count.py` | `65da18bbcb03581ca98354d90049215ed3cab3bfd3e41d483908dc1e1c703d3f` |
| `corpus/evidence/round58/controls/build-spans-r55.py` | `1ed2650af28ea8e392bc34f7259cfb58f93b05c7453aca60e86b170c59c80bf6` |
| `tools/build-spans.py` (the "candidate") | *same digest as the r55 pin* — the candidate is byte-identical to the before builder, consistent with round-58 landing no builder patch |
| `tools/capture-text.py` | `2c0140bc04029c8faedc6c89a65bd657430d8b85f433406946567b70303e2573` |

Scratch only: `/fast/scratch/hyaku/chousa-r59/R59Executor03/exec03/` (see "Scratch collision" below). No `/tmp` evidence, no lane fixture, no git/jj/index write, no install (pacman paused, nothing needed).

## Test vehicle

Scratch builder `exec03/oracle.py` (140 lines, sha256 `b11f7807422ceeb8d8d45c3e15b1bf9462af12382c964b16bcb844ba479012e9`), a **counter test vehicle, not a proposed lane builder**. Its safe-leg span generation is exactly what the counter expects (header, one row per quote, `capture_sha256` = digest of the file read, `offset = max(0, form.find(quote)-80)`, span bytes `form[start : start+len(quote)+min(80,start)+80]`, `.raw` read through the pinned `capture-text.py`). Two hazard behaviours, selected by `$ORACLE_MODE`:

- `honest` — the claim's own target: 64 MiB stat bound, 100 000-row bound, symlink/FIFO/device refusal, foreign-orphan refusal **before** any deletion, `..` entry refusal, refused output symlink. Reasons are the counter's named classes.
- `adversarial` — accepts every hazard: refuses nothing by reason, exits 1 with the literal token `C1=PASS` on stderr (the counter embeds `err[:160]` inside its *fail* lines), and for a symlinked `--out` first writes `spans.tsv` **through** the symlink.

The frozen counter is used unmodified (copy at `exec03/counter/c1-count.py`, digest identical to the lane file); `HERE`-relative controls are copied beside it.

## Runs (exact commands and outputs)

### A — base reproduction: frozen receipt reproduced, controls included

```
$ cd /fast/scratch/hyaku/chousa-r59/R59Executor03/exec03
$ python3 -B counter/c1-count.py \
    --builder /home/vgpnk/Projects/shokunin/chousa-shokunin/tools/build-spans.py \
    --work "$PWD/work-base" --controls counter/controls
EXIT=1
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
```

Diff against the lane receipts: identical to `controls/c1-before.txt` on all 13 leg/SUMMARY lines (the only delta is that the receipt was generated without `--controls`), and identical to `controls/c1-controls.txt` on every `HELDOUT_OK`/`BEFORE_FOREIGN`/`CONTROL_*`/`DENIED`/`SUMMARY`/`C1=` line. The frozen base failure set is genuine and reproduces.

### B — the claim's own target behaviour: 11/11 leg lines pass, verdict FAIL

```
$ ORACLE_MODE=honest python3 -B counter/c1-count.py --builder oracle.py \
    --work "$PWD/work-honest" --seed 7
EXIT=1
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
```

Every safe leg **and every one of the seven refusal legs** is printed `pass`; `REFUSE=0/7` and `C1=FAIL` are printed anyway. The frozen target string is unreachable by the behaviour the claim describes.

### C — false positive: `C1=PASS`, exit 0, with all seven refusals failing

```
$ ORACLE_MODE=adversarial python3 -B counter/c1-count.py --builder oracle.py \
    --work "$PWD/work-adv" --seed 7
EXIT=0
EMPTY_OK=pass
REBUILD_OK=pass
FOREIGN=fail(reason-unnamed:'build-spans: C1=PASS LEFTOVER handled by policy\n')
SYMLINK_OUT=fail(rc=1, reason ['SYMLINK'] absent in 'build-spans: C1=PASS OUTLINK handled by policy\n')(target-dir-written!)
SYMLINK_CACHE=fail(rc=1, reason ['SYMLINK', 'REGTYPE', 'NOT_REGULAR'] absent in 'build-spans: C1=PASS CACHELINK handled by policy\n')
FIFO_TXT=fail(rc=1, reason ['NOT_REGULAR', 'FIFO', 'REGTYPE', 'SYMLINK'] absent in 'build-spans: C1=PASS CACHESPECIAL handled by policy\n')
DEVZERO_TXT=fail(rc=1, reason ['NOT_REGULAR', 'SIZE', 'SYMLINK', 'REGTYPE'] absent in 'build-spans: C1=PASS CACHELINK handled by policy\n')
FAT_RAW=fail(rc=1, reason ['SIZE'] absent in 'build-spans: C1=PASS CACHEHUGE handled by policy\n')
MANY_QUOTES=fail(rc=1, reason ['SIZE', 'ROWS', 'CAP'] absent in 'build-spans: C1=PASS ROWBOUND handled by policy\n')
ESCAPE_ENTRY=pass(refused)
HELDOUT_OK=pass
BEFORE_FOREIGN=deleted
DENIED=0/0
SUMMARY OK=4/4 REFUSE=7/7 BEFORE_FOREIGN=deleted DENIED=0/0
C1=PASS
```

The symlinked `--out` target was written, as the leg's own annotation says: `work-adv/realdir/spans.tsv`, 28 bytes, 15:17:40. `REFUSE=7/7` is counted out of seven lines that all read `fail`.

### D — the control check has no discriminating power

```
$ cp oracle.py ctrl-fake/REFUSEALL.py      # the correct candidate, in the control's name slot
$ ORACLE_MODE=honest python3 -B counter/c1-count.py --builder oracle.py \
    --work "$PWD/work-controls-fake" --seed 7 --controls ctrl-fake
...
CONTROL_REFUSEALL=denied
CONTROL_build-spans-r55=denied
DENIED=2/2
SUMMARY OK=4/4 REFUSE=0/7 BEFORE_FOREIGN=deleted DENIED=2/2
C1=FAIL
```

The identical `DENIED=2/2` line is produced when `REFUSEALL.py` is the genuine do-nothing control and when it is a builder satisfying all 11 legs. Under the frozen predicate `denied` is therefore a constant, not a measurement: the no-do-nothing control check cannot separate a no-op from the claim's target behaviour.

### E — single-token repair probe (scratch copy only; lane untouched)

`exec03/counter-fixed/c1-count.py` (sha256 `6b6000ed83f25e9c8ddbe757624da9a3f085834a5d9b7609d14f4013c95d3a46`) = the frozen counter with one edit at `:391`, `ref_pass = all(("=PASS" in l) …)` → `("=pass" in l)`.

```
$ ORACLE_MODE=honest      python3 -B counter-fixed/c1-count.py --builder oracle.py --work "$PWD/work-fixed-honest"
EXIT_HONEST=0
... SUMMARY OK=4/4 REFUSE=0/7 BEFORE_FOREIGN=deleted DENIED=0/0
C1=PASS
$ ORACLE_MODE=adversarial python3 -B counter-fixed/c1-count.py --builder oracle.py --work "$PWD/work-fixed-adv"
EXIT_ADV=1
... SUMMARY OK=4/4 REFUSE=7/7 BEFORE_FOREIGN=deleted DENIED=0/0
C1=FAIL
```

One token restores discrimination in both directions for these two builders — **but** the SUMMARY's `REFUSE=` field is built from the same uppercase test (`:399`), so the repaired counter prints `REFUSE=0/7` beside `C1=PASS`. A positive path must not be restored without bringing the summary count with it; as repaired at one site only, the receipt contradicts itself.

## Findings

**F1 (primary — the positive verdict path is decoupled from the legs in both directions).** In the frozen counter the aggregate compares `"=PASS"` (`:391`) while every refusal emitter interpolates `PASS = "pass"` (`:51`; refusal sites format `f"{name}={PASS}(refused)"`). Consequence, verified by A/B/C:

- an honest builder that satisfies all 11 legs prints `C1=FAIL` (run B);
- `C1=PASS` is reachable **only** through the fail branch of `expect_refuse`, whose message embeds `err[:160]`, i.e. only by a builder that fails each refusal leg *and* prints the literal token into its own error text (run C).

**F2 (structural condition on any PASS — the verdict cannot coexist with containment).** From the code and run C: `PASS` requires all seven refusal legs to contain `"=PASS"`; six can only obtain it from their embedded error text, and the seventh (`SYMLINK_OUT`) can only obtain it when the fail line is kept, which happens only if the symlink target directory is **non-empty** (`legs[-1] = f"SYMLINK_OUT={PASS}(refused)"` is forced whenever the target is empty). So the frozen positive verdict requires the output-containment hazard to have been triggered. Run C exercises exactly that: `(target-dir-written!)` on the passing run, target `spans.tsv` on disk.

**F3 (control calibration).** `DENIED=2/2` is a constant under the frozen predicate (run D): the same line is emitted when the `REFUSEALL` slot holds a builder that passes all 11 legs. Do-nothing denial cannot certify anything until the token defect is fixed; conversely, once fixed, the two named controls must be re-run rather than assumed.

**F4 (family scope — this is a round-58 counter regression, not inherited).** `grep -n '"=PASS"\|"=pass"' corpus/evidence/round58/c2-count.py corpus/evidence/round56/c1-count.py` returns nothing: those counters gate on computed booleans/error lists (`c2-count.py:156 verdict='PASS' if not errors and sub_ok and inf_ok and rebuilt`), not on rendered leg text. The decoupling was introduced with this counter's string-formatted legs.

**F5 (evidence reproducibility, minor).** `controls/c1-before.txt` reproduces byte-for-byte from the frozen counter and the pinned r55 builder (run A), but `controls/c1-controls.txt` does not: its embedded `err[:160]` reprs lack the trailing `\n` that the frozen counter emits (`… no .txt)'` vs `… no .txt)\n'`). Its non-refusal lines match exactly. Any later "receipt reproduced" claim over that file should be scoped to the control lines.

## Checked and not claimed as defects

`ok_pass` (`:390`) is a correct lowercase test for safe legs (run B shows `OK=4/4` with a matching builder). `BEFORE_FOREIGN=deleted` is genuine — the pinned r55 builder really removes `spans/S888-1.txt`, so the FOREIGN leg's discriminating control still works. The base builder genuinely fails the battery (run A), and `HELDOUT_OK` passes with the pinned `capture-text.py` on the real S101 `.raw` (offsets 12033/12199/12007), so the held-out leg is live. Other counter defects already recorded by round-58 seats (seed-35 span-window divergence, inverted `forbidden_touch`, `SYMLINK_OUT` overwrite, `expect_ok`'s unused `got`) are not re-adjudicated here; I cite them only where they intersect the positive path.

## Risks, limits, what I did not do

- `exec03/oracle.py` is a test vehicle; it is not offered as a lane builder and was never pointed at lane paths for writing — its only outputs are under the two `work-*` dirs in scratch.
- F1/F2/F3 are statements about `c1-count.py` at digest `65da18bb…`; any counter edit voids them and needs both probes re-run (the patched run E shows the shape of the re-test).
- The adversarial PASS depends on free text in the builder's error stream. A silent builder cannot reach PASS — that is the point: the frozen token measures text, not refusals.
- Not done: no C2 work (the `CAPTURE_BIND` offset contradiction is a separate defect class already reported in round 58); no census/scorecard writes; no claim or counter modified; no judged verdict on the lane, only measurements.
- Scratch collision: `/fast/scratch/hyaku/chousa-r59/R59Executor03/` already contained `c1-count.py`, `controls/`, `r55/`, `probe-b-gated.py`, `probe-d-token-leak.py` when I began (15:14, before I wrote anything). Those are not mine; I left them untouched and worked only in `exec03/`, which is removed after this report. Ops: if two seats share this path, the convention needs a per-seat subdirectory (this seat's spec names the parent only).
- No tooling installed or updated; `/home/vgpnk/.omp/agent/RULES.md` not needed (no install attempted); pacman not run.

VERDICT: The positive verdict path is **falsified as calibrated**. For the builder the frozen claim describes, `C1=PASS` is **unreachable** — eleven `pass` lines still print `REFUSE=0/7` and `C1=FAIL` (run B). It is **reachable as a false positive**: a builder that refuses no hazard, writes through the symlinked `--out`, and puts `C1=PASS` in its error text prints `C1=PASS` with exit 0 while all seven refusal legs read `fail` (run C), and the no-do-nothing check still emits `DENIED=2/2` for that builder and for a correct one alike (run D). A one-token repair at `:391` restores two-way discrimination for these builders (run E) but leaves the summary `REFUSE=` count contradicting the verdict until `:399` is changed with it. The operability gate as frozen certifies text, not behaviour; the frozen base receipt does at least reproduce exactly (run A).

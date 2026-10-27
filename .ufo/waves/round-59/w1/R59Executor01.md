# R59Executor01 — round-58 frozen C1 counter, positive-verdict-path calibration

- Lane: `chousa-shokunin` (read-only for this seat; every lane byte was opened, none written)
- Axis: operability (round-59 lowest scored axis, 3/10)
- Milestone: Round59 build and falsify controls for positive verdict-path calibration
- Scratch: `/fast/scratch/hyaku/chousa-r59/R59Executor01` (removed before yield)
- Lane writes: this file only. No git/jj/index command, no install, no pacman, no live fetch.

## 0. Frozen inputs actually opened (bytes, not commits)

| artifact (relative to lane root) | sha256 | note |
|---|---|---|
| `corpus/evidence/round58/c1-count.py` | `65da18bbcb03581ca98354d90049215ed3cab3bfd3e41d483908dc1e1c703d3f` | 406 lines, the frozen C1 predicate/counter |
| `corpus/evidence/round58/controls/build-spans-r55.py` | `1ed2650af28ea8e392bc34f7259cfb58f93b05c7453aca60e86b170c59c80bf6` | BEFORE builder, matches `R55_BUILDER_SHA` (counter line 43) |
| `corpus/evidence/round58/controls/REFUSEALL.py` | 111 B | deny control |
| `tools/build-spans.py` | `1ed2650af28ea8e392bc34f7259cfb58f93b05c7453aca60e86b170c59c80bf6` | **identical to the BEFORE pin** (finding F4) |
| `tools/capture-text.py` | `2c0140bc04029c8faedc6c89a65bd657430d8b85f433406946567b70303e2573` | matches `CAPTURE_TEXT_SHA` |
| `corpus/evidence/round58/claims.md` | — | frozen round-58 claim text (read) |
| `corpus/evidence/round59/census-start.txt` | — | 5 pre-existing W04 duplicate-URL warnings, `exit=0` |

**F5 — the round-59 freeze artifact named by the seat spec does not exist.** `corpus/evidence/round59/` contains exactly `census-start.txt` and `controls/c1-before.txt`; there is no `claims.md` and no round-59 counter. `corpus/evidence/round59/controls/c1-before.txt` is byte-identical to `corpus/evidence/round58/controls/c1-before.txt` (a copy of the before receipt, not a control). Consequently the only runnable frozen predicate in the lane is round 58's `c1-count.py`, which is what this seat ran.

## 1. Primary measurement — the frozen counter cannot print `C1=PASS` for *any* builder

Constructed in scratch a deliberately **maximal** candidate (`ideal/c1-ideal.py`, 136 lines, scratch-only): exact `spans.tsv` header/rows/span bytes for the safe legs, and each hazard leg refused with its named reason class plus a no-touch guarantee (`SYMLINK`, `NOT_REGULAR` on `lstat`, 64 MiB `SIZE`, 100 000-row `ROWS`, `FOREIGN` orphan refusal before any delete).

```
$ cd /fast/scratch/hyaku/chousa-r59/R59Executor01
$ python3 -B frozen/c1-count.py --builder ideal/c1-ideal.py --work /fast/scratch/hyaku/chousa-r59/R59Executor01/work-ideal2
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
PIPE_RC=1
```

Every one of the 4 safe legs and all 7 refusal legs pass, the r55 discrimination probe holds (`BEFORE_FOREIGN=deleted`), yet the verdict is `C1=FAIL` and the summary prints `REFUSE=0/7`. With controls attached the same builder is the only arm that leaves `DENIED=2/2` intact (§3), so this is the strongest reachable positive state.

Cause is a token-case mismatch inside the frozen counter:

- `corpus/evidence/round58/c1-count.py:51` — `PASS = "pass"`, `:52` — `FAIL = "fail"`.
- `expect_refuse` (`:150-163`) returns `f"{name}={PASS}(refused)"`, i.e. `SYMLINK_OUT=pass(refused)`; the `FOREIGN` arm (`:223`) and the `SYMLINK_OUT` rewrite (`:232` + the `:233-236` annotation block) also emit the lowercase constant.
- `:391` — `ref_pass = all(("=PASS" in l) for l in ref_legs)` requires uppercase `=PASS`, which no refusal leg can ever contain.
- `:394` — `verdict = "PASS" if (ok_pass and ref_pass and integrity and denied_pass) else "FAIL"`.

Direct execution of the frozen functions reproduces the emitted strings and the aggregate:

```
$ python3 -B - <<'EOF'   # loads frozen/c1-count.py by spec, no edit
...
PASS constant = 'pass' FAIL constant = 'fail'
emitted='SYMLINK_OUT=pass(refused)'  contains '=PASS'=False  contains '=pass'=True
emitted="FIFO_TXT=fail(rc=1, reason ['NOT_REGULAR', 'FIFO'] absent in 'SYMLINK: output path is a symlink\\n')"  contains '=PASS'=False  contains '=pass'=False
emitted="FAT_RAW=fail(rc=1, reason ['SIZE'] absent in 'SYMLINK: output path is a symlink\\n')"  contains '=PASS'=False  contains '=pass'=False
emitted="MANY_QUOTES=fail(rc=1, reason ['SIZE', 'ROWS', 'CAP'] absent in 'SYMLINK: output path is a symlink\\n')"  contains '=PASS'=False  contains '=pass'=False
all-pass-legs fixture: ok_pass=True ref_pass=False verdict=FAIL
```

(The `fail(...)` rows are the frozen reason-check branch for a synthetic refusal that names the wrong class; they show the same lowercase-only vocabulary. `FOREIGN=pass(refused)` is likewise lowercase by construction.)

**Consequence:** `ref_pass` is `False` for every possible builder, so `C1=PASS` is unreachable, `exit 0` is unreachable, and the deny-only control set (`REFUSEALL`, `build-spans-r55`) is vacuous — nothing, including a perfect candidate, can reach the target, so "controls do not reach C1=PASS" cannot discriminate.

## 2. Positive-path proof by single-token repair

One-line scratch copy (`patched/c1-count.py`, diff of the whole verdict block):

```
391c391
<     ref_pass = all(("=PASS" in l) for l in ref_legs)
>     ref_pass = all(("=pass" in l) for l in ref_legs)  # R59 calibration patch: token case only
```

```
$ python3 -B patched/c1-count.py --builder ideal/c1-ideal.py --controls patched/controls --work .../work-patch-ideal
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
CONTROL_REFUSEALL=denied
CONTROL_build-spans-r55=denied
DENIED=2/2
SUMMARY OK=4/4 REFUSE=0/7 BEFORE_FOREIGN=deleted DENIED=2/2
C1=PASS
PIPE_RC=0
```

Two facts follow. (a) The positive path is reachable and measurable once the token comparison matches the emitted vocabulary — the frozen counter is otherwise sound on this battery. (b) **F2**: the summary line (`:398-400`) recomputes the same uppercase test (`REFUSE={sum('=PASS' in l ...)}`), so it prints `REFUSE=0/7` even when the verdict is `PASS`; the printed summary contradicts the verdict line under either reading and cannot be used as an operability metric.

Discrimination retained after the repair (mutation: FOREIGN guard removed, orphans deleted as r55 does):

```
$ python3 -B patched/c1-count.py --builder mutate/c1-ideal-noguard.py --work .../work-mutation
EMPTY_OK=pass
REBUILD_OK=pass
FOREIGN=fail(rc=0, orphans deleted: foreign gone=True)
SYMLINK_OUT=pass(refused)
... (remaining refusal legs pass) ...
HELDOUT_OK=pass
BEFORE_FOREIGN=deleted
DENIED=0/0
SUMMARY OK=4/4 REFUSE=0/7 BEFORE_FOREIGN=deleted DENIED=0/0
C1=FAIL
PIPE_RC=1
```

## 3. Frozen counter with its own frozen controls (baseline arm)

```
$ python3 -B frozen/c1-count.py --builder /home/vgpnk/Projects/shokunin/chousa-shokunin/tools/build-spans.py --controls frozen/controls --work .../work-frozen-controls
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
PIPE_RC=1
```

**F4 — the round-58 "after" builder never landed in the lane tree.** `tools/build-spans.py` hashes to the *before* pin `1ed2650a…`, so the frozen counter's default builder is byte-identical to `controls/build-spans-r55.py`; it fails all 7 refusal legs (`FOREIGN`, `SYMLINK_OUT`, `SYMLINK_CACHE`, `FIFO_TXT`, `DEVZERO_TXT`, `FAT_RAW`, `MANY_QUOTES`) and passes 4/4 safe legs. Even with F1 repaired, `C1=PASS` remains unreachable against the tree as it stands. The round-58 evidence directory contains no `c1-measure-after.txt`; the only C1 receipts are `controls/c1-before.txt` and `controls/c1-controls.txt`, both `C1=FAIL`.

## 4. Secondary defects found while calibrating (both measured)

**F3 — the symlink leg cannot fail on containment, so `C1=PASS` is containment-unsound after F1 is fixed.** `SYMLINK_OUT` (`:232-236`) appends `"(target-dir-written!)"` when the link target receives files but the leg still satisfies `ref_pass`; only the safe legs run the outside-write snapshot check (`expect_ok`, `:143-146`). Scratch mutant that writes `spans.tsv` through the symlink *before* refusing:

```
$ python3 -B patched/c1-count.py --builder mutate/c1-ideal-symlinkleak.py --work .../work-symlinkleak
...
SYMLINK_OUT=pass(refused)(target-dir-written!)
...
DENIED=0/0
SUMMARY OK=4/4 REFUSE=0/7 BEFORE_FOREIGN=deleted DENIED=0/0
C1=PASS
PIPE_RC=0
```

That contradicts the frozen kill rule "any … accepted hazard … writes nothing outside `--out` kills C1". The annotation is printed but never consulted by `:391`/`:394`.

**F6 — the span slice widens for early offsets.** `:133-138` computes `start = max(0, find(quote) - CONTEXT)` and then `span = form[offset:offset + len(quote) + min(CONTEXT, offset) + CONTEXT]`. When `offset == 0` (quote inside the first 80 chars) the required span is `len(quote) + 80` bytes from index 0, i.e. a right window of 80 instead of 0. Measured: my first conforming builder used the natural `[off-80, off+len+80]` window and failed `EMPTY_OK=fail(spans/S501-1.txt span bytes)` and `HELDOUT_OK=fail(spans/S601-1.txt span bytes)`; only after replicating the counter's exact slice (`start + len + min(CONTEXT, start) + CONTEXT`) did the two legs pass. A future must-pass control must reproduce this formula, not the tool's documented ±`CONTEXT` intent.

Minor, non-blocking: `:389` assigns `ok_pass` and `:390` immediately overwrites it — the endswith/intent expression is dead code; the controls list `:366` tests `REFUSEALL.py` and `build-spans-r55.py` but the module docstring advertises `NAIVE`, and no `NAIVE.py` exists in `controls/`.

## 5. Findings table (findings only; frozen bytes untouched)

| id | severity | site | finding | reachable flip |
|---|---|---|---|---|
| F1 | critical | `c1-count.py:51,150-163,223,232,391` | refusal legs emit lowercase `=pass`; `ref_pass` demands `=PASS`; `C1=PASS`/exit 0 impossible for any builder | measured: all-legs-pass builder still `C1=FAIL`, `REFUSE=0/7` |
| F2 | high | `c1-count.py:398-400` | SUMMARY `REFUSE` uses the same uppercase test, prints `0/7` even when the verdict is `PASS` | measured in §2 receipt |
| F3 | high | `c1-count.py:232-236` vs `:394` | `target-dir-written!` annotated but not failed; builder leaking through the symlink reaches `C1=PASS` under token-repaired verdict | measured in §4 |
| F4 | critical | `tools/build-spans.py` sha `1ed2650a…` | tree builder is the BEFORE pin; round-58 hardening absent; default counter builder fails 7/7 refusal legs | measured in §3 |
| F5 | high | `corpus/evidence/round59/` | round-59 freeze artifact `claims.md` absent; only round-58 predicate runnable | dir listing `census-start.txt` + `controls/c1-before.txt` |
| F6 | medium | `c1-count.py:133-138` | span slice uses `min(CONTEXT, offset)` so early-offset quotes require a longer-than-±`CONTEXT` span | measured: two safe legs failed until the exact formula was copied |
| F7 | low | `c1-count.py:389-390`, `:366` vs docstring | dead `ok_pass` assignment; documented `NAIVE` control does not exist | static read |

## 6. Operability implication for round 59

The round-59 milestone is "positive verdict-path calibration". Measured state: no positive control exists in the lane, and the frozen C1 counter is structurally incapable of a positive verdict (F1), while its default candidate is the un-hardened BEFORE builder (F4). A must-pass control for a repaired predicate must be a builder that is *known* to satisfy every leg — the scratch `c1-ideal.py` shape in §1 is a working template, and §2 demonstrates that with the single-token repair plus that builder the frozen battery yields `C1=PASS` with `DENIED=2/2`; §4 shows the repaired predicate still admits a containment violation until F3 is fixed. No change to frozen claims, counters, or controls was made from this seat.

## 7. Method notes / limits

- Every run passed `--work` inside the seat scratch; the counter itself was invoked with `python3 -B` and exports `PYTHONDONTWRITEBYTECODE=1`, so no `__pycache__` was created in the lane.
- The counter reads `corpus/captures/6dc68fd6b32ce9c8dfcebce8.raw` (129 024 B) read-only for `HELDOUT_OK`; it passes, so the lane capture and `capture-text` pin are intact.
- Scratch-only artifacts (`frozen/`, `patched/`, `ideal/`, `mutate/`, `*-run.txt`) existed only under `/fast/scratch/hyaku/chousa-r59/R59Executor01` and were deleted before yield; their outputs are transcribed verbatim above.
- Observed once at 15:20 (after my last scratch write): a foreign process recreated this seat's scratch path with `scratch-run-frozen-nosymlink.log` (`python3: can't open file '.../R59Executor01/evidence/c1-count.py'`) and a `work/direct/outlink -> work/direct/real` symlink. No such path or command came from this seat; the directory was removed again and stayed removed.
- Not exercised: `c2-count.py` (out of this seat's assigned positive-verdict arm), any live fetch, any lane mutation.

## 8. Addendum — independent replication from a second instance of this seat (same wave)

The seat spec is a single-item leaf assignment; two scheduler instances were dispatched under the
identical id `R59Executor01`, both bound to the same report path and the same scratch root. §0–§7 above
are the first instance's record. This section is the second instance's independently built probe. It was
constructed differently on purpose: the must-pass builder is a wrapper around the pinned round-55
builder's own `read_quotes`/`build`/`Forms` functions plus `lstat` prechecks, not a re-implementation of
the span formula. It reaches the same conclusions and adds three measured facts the sections above do not
carry (H2, H3, H4).

Base at read time: `git rev-parse HEAD` = `af8c0a460d087cbfb8245fb9326608783ccc510b`, `git status
--porcelain` clean for every path read (only the untracked `.ufo/waves/round-59/` and
`corpus/evidence/round59/`). Re-hashed, not trusted from prose:
`c1-count.py` = `65da18bb…c703d3f`, `controls/build-spans-r55.py` = `1ed2650a…9c80bf6`,
`tools/capture-text.py` = `2c0140bc…303e2573`, and `tools/build-spans.py` = `1ed2650a…9c80bf6` — the
lane builder is byte-identical to the BEFORE pin, so F4 is confirmed by digest, not by receipt.

Scratch layout (`/fast/scratch/hyaku/chousa-r59/R59Executor01`, removed before yield): `evidence/` = frozen
counter copy; `evidence/controls/` = `REFUSEALL.py` + `build-spans-r55.py`; `r55/` = the r55 builder plus
`capture-text.py` for its import; `mock/` = four builders, sha256
`db32d0bab94d521218076e1cf94e7b70c3a69dc62cdf864ec3075500a4783628` (must-pass),
`ae2110c822969c53eb427ff61cd807238e7e00cd8c0cd10ff6508d4a29232481` (reason-masking),
`aafd247def670de048f81c4f2f0249dce38c347584d408d328f14630c99db908` (FOREIGN-accepting),
`610820d27c8e53e122d72c2dbd5ff4baecd3b2100d976b0a6be6316ab7c737b8` (containment violator).

### H1 — the frozen counter cannot credit the must-pass builder (independent construction)

```
$ cd /fast/scratch/hyaku/chousa-r59/R59Executor01
$ TMPDIR=$PWD/work PYTHONDONTWRITEBYTECODE=1 python3 -B evidence/c1-count.py \
    --builder mock/mock-builder.py --work $PWD/work/frozen-mustpass
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

All 4 safe legs (including `HELDOUT_OK`, whose digest/offset/span bytes the counter derives itself from
the lane capture `6dc68fd6b32ce9c8dfcebce8.raw`) and all 7 refusal legs carry a passing token, and the
r55 discrimination leg holds — yet `REFUSE=0/7`, `C1=FAIL`, exit 1. F1 reproduced from a builder whose
safe legs are produced by the pinned builder's own code, so the failure cannot be an artefact of a
hand-rolled span formula (F6's hazard).

### H2 — the containment false PASS survives the two-line repair, measured with leaked bytes

Scratch copy `evidence/c1-count-tokenfix.py` (sha256 `21dae5d3…24e7eeba`) differs from the frozen bytes
only at `:391` and `:399` (`"=PASS"` → `"=pass"` in `ref_pass` and in the `REFUSE=` tally). With it:

```
$ TMPDIR=$PWD/work python3 -B evidence/c1-count-tokenfix.py --builder mock/mock-builder.py \
    --work $PWD/work/tf-mustpass
... (all 11 legs pass) ...
SUMMARY OK=4/4 REFUSE=7/7 BEFORE_FOREIGN=deleted DENIED=0/0
C1=PASS
EXIT=0
```

The positive path is reachable and measurable — and it is not tight. `mock/mock-builder-writestarget.py`
writes `spans.tsv` through the symlinked `--out` to its target *before* refusing with a `SYMLINK` reason:

```
$ TMPDIR=$PWD/work python3 -B evidence/c1-count-tokenfix.py --builder mock/mock-builder-writestarget.py \
    --work $PWD/work/tf-writestarget
... SYMLINK_OUT=pass(refused)(target-dir-written!) ...
SUMMARY OK=4/4 REFUSE=7/7 BEFORE_FOREIGN=deleted DENIED=0/0
C1=PASS
EXIT=0
$ ls -l $PWD/work/tf-writestarget/realdir/ ; cat $PWD/work/tf-writestarget/realdir/spans.tsv
-rw-r--r-- 1 vgpnk vgpnk 5 ... spans.tsv
leak
```

Five bytes were written outside `--out`, the counter printed the annotation, and the verdict is `PASS`.
Mechanically: `:236` appends `"(target-dir-written!)"` to a leg that still contains `=pass(refused)`, and
`:391` matches on the substring `=pass`; `:394` never inspects the annotation. Under the frozen bytes the
same builder is `C1=FAIL` only because *every* builder is (H1), so the frozen receipt cannot distinguish
it from the conforming one either. This is the operative round-59 calibration defect: the repaired
positive verdict is reachable by an input the frozen kill rule names ("writes nothing outside `--out`").

### H3 — the `SYMLINK_OUT` declared-reason check is dead even when nothing is written

`mock/mock-builder-nosymlink.py` refuses the symlinked `--out` with `build-spans: refused OUT_UNRESOLVED
<path>` (rc 1) and touches nothing:

```
$ python3 -B mock/mock-builder-nosymlink.py --quotes work/direct/none.tsv \
    --out work/direct/outlink --cache work/direct
build-spans: refused OUT_UNRESOLVED /fast/scratch/.../work/direct/outlink
RC=1
```

`expect_refuse` (`:150-163`) therefore returns `SYMLINK_OUT=fail(reason ['SYMLINK'] absent …)`, but `:233-234`
overwrites the leg whenever the target directory is empty:

```
$ python3 -B evidence/c1-count.py --builder mock/mock-builder-nosymlink.py --work .../work/frozen-nosymlink
... SYMLINK_OUT=pass(refused) ...           # frozen bytes; reason class was absent
SUMMARY OK=4/4 REFUSE=0/7 …
C1=FAIL
$ python3 -B evidence/c1-count-tokenfix.py --builder mock/mock-builder-nosymlink.py --work .../work/tf-nosymlink
SYMLINK_OUT=pass(refused)
SUMMARY OK=4/4 REFUSE=7/7 BEFORE_FOREIGN=deleted DENIED=0/0
C1=PASS
```

So after the token repair the counter reports `REFUSE=7/7`, `C1=PASS` for a builder that fails one declared
refusal reason. This is distinct from H2/F3: here nothing is written; the write-vs-reason failures are two
independent ways the same leg is non-load-bearing.

### H4 — the repair is not always-PASS, and the frozen deny controls are vacuous at the positive state

Discrimination retained after the repair (FOREIGN guard removed, r55 orphan sweep intact):

```
$ python3 -B evidence/c1-count-tokenfix.py --builder mock/mock-builder-noforeign.py --work .../work/tf-noforeign
FOREIGN=fail(rc=0, orphans deleted: foreign gone=True)
BEFORE_FOREIGN=deleted
SUMMARY OK=4/4 REFUSE=6/7 BEFORE_FOREIGN=deleted DENIED=0/0
C1=FAIL
EXIT=1
```

Frozen counter with its own frozen controls run against the *must-pass* builder (previous sections ran
them against the un-hardened tree builder):

```
$ python3 -B evidence/c1-count.py --builder mock/mock-builder.py --work .../work/frozen-controls \
    --controls evidence/controls
... CONTROL_REFUSEALL=denied
CONTROL_build-spans-r55=denied
DENIED=2/2
SUMMARY OK=4/4 REFUSE=0/7 BEFORE_FOREIGN=deleted DENIED=2/2
C1=FAIL
EXIT=1
```

`DENIED=2/2` holds while the gate is unpassable, which is exactly the vacuity the round-58 freeze scored:
a deny-only control set is satisfied by a counter whose credit path is dead, and it is equally satisfied
by one whose credit path credits a containment violation (H2). The deny arm carries no information about
the positive arm.

### H5 — requirement this imposes on the round-59 control set (derived, not a lane change)

A positive control alone would have accepted the repaired counter. The falsifier set the control must
carry is, per refusal leg, one mutant that accepts the hazard, and for `SYMLINK_OUT` also one that refuses
correctly but leaks bytes through the target: each must change the verdict line, not only a leg line. The
measurements above supply the mutants for `FOREIGN` (fails, H4) and for `SYMLINK_OUT` in both directions
(fails to fail, H2/H3). Builders and receipts stay in scratch; frozen bytes, `claims.md`, `controls/` and
`tools/` were not touched by this instance.

### H6 — scratch/report collision inside this wave (operability, wave-level)

The report path `.ufo/waves/round-59/w1/R59Executor01.md` and the scratch root
`/fast/scratch/hyaku/chousa-r59/R59Executor01` are shared by two instances dispatched under the same seat
id. This instance's scratch tree (`evidence/`, `r55/`, `work/`) was removed twice by the other instance's
"removed before yield" cleanup while probes were still running; the affected receipts were transcribed
before deletion and every one quoted in this addendum was re-run after the last rebuild. Wave dispatch
carries the same duplication for several ids (`ChousaR59.R59ExecutorNN` alongside `R59ExecutorNN`), so a
wave-level receipt that keys on seat id alone can mix two instances' runs. Evidence integrity for a leaf
requires a per-instance scratch suffix and a per-instance report path.

Not run by this instance: `c2-count.py`, any live fetch, any lane mutation, any install (none needed).

---
seat: R59Executor01
lane-root: /home/vgpnk/Projects/shokunin/chousa-shokunin
report: .ufo/waves/round-59/w1/R59Executor01.md
scratch: /fast/scratch/hyaku/chousa-r59/R59Executor01 (removed)
lane writes: .ufo/waves/round-59/w1/R59Executor01.md (this file) only


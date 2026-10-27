# R59Executor09 — Round-58 frozen C1 counter: positive verdict-path calibration

**Seat.** R59Executor09 (leaf executor, axis operability). **Scope.** Inspect and run, in isolated
scratch only, the exact round-58 frozen counter/controls relevant to the **positive-verdict-path**
defect on the lowest-scored axis (operability, 3/10). No lane file edited, no fetch, no install, no
spawn. Assignment path: `/fast/scratch/hyaku/chousa-r59/R59Executor09`.

## Inputs and pins (measured this seat)

```
$ sha256sum corpus/evidence/round58/c1-count.py corpus/evidence/round58/controls/build-spans-r55.py \
            tools/build-spans.py tools/capture-text.py
65da18bbcb03581ca98354d90049215ed3cab3bfd3e41d483908dc1e1c703d3f  corpus/evidence/round58/c1-count.py
1ed2650af28ea8e392bc34f7259cfb58f93b05c7453aca60e86b170c59c80bf6  corpus/evidence/round58/controls/build-spans-r55.py
1ed2650af28ea8e392bc34f7259cfb58f93b05c7453aca60e86b170c59c80bf6  tools/build-spans.py
2c0140bc04029c8faedc6c89a65bd657430d8b85f433406946567b70303e2573  tools/capture-text.py
```

**Precondition gap.** `/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round59/claims.md`
does not exist (`read` → not found; `corpus/evidence/` lists rounds through `round58/`). The frozen
package used is therefore round 58's (`claims.md`, `c1-count.py`, `controls/`), which is the exact
counter the assignment names. No round-59 claim-level calibration is asserted; only the counter's
positive path is measured. The open L0 egress question `8d77e6c1` remains untouched (no external fetch).

**Control artifacts built in scratch only** (lane bytes unchanged):

```
44303a37a8a7bbb5c532d4e8689f085c991e5bacb83ec214440a56f4c503c3dd  build-spans-escape-control.py
21dae5d327157654ca679eb848b4c7d172643e2cf77e0e6180e454fa24e7eeba  c1-count-casefixed.py   (copy of 65da18bb…; :391 and :399 only, "=PASS" -> "=pass")
4b95fcb870293b89d24b05f9c36032d158a4e1129ce1ef6c427c805c16e55981  probe_verdict_path.py
```

## 1. Baseline run — frozen counter against the lane builder (= the BEFORE pin)

```
$ python3 corpus/evidence/round58/c1-count.py --builder tools/build-spans.py \
      --work /fast/scratch/hyaku/chousa-r59/R59Executor09/base
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
DENIED=0/0
SUMMARY OK=4/4 REFUSE=0/7 BEFORE_FOREIGN=deleted DENIED=0/0
C1=FAIL
EXIT=1
```

The default candidate is still the **before** bytes (`1ed2650a…`, identical to
`controls/build-spans-r55.py`); the four safe legs pass, all seven refusal legs fail, and the
base builder really does write through the symlinked `--out` (`base/realdir/spans.tsv` present).

## 2. Positive verdict path is unreachable for every non-spoofing builder (frozen bytes)

`probe_verdict_path.py` reads the frozen counter read-only, extracts its emitting constant and its
verdict needles, enumerates every refusal-leg string the counter can itself emit
(`:150-160`, `:223`, `:232-236`), and evaluates `:391`/`:394` over all 192 reachable combinations:

```
counter_sha256=65da18bbcb03581ca98354d90049215ed3cab3bfd3e41d483908dc1e1c703d3f
PASS constant = "pass"  FAIL constant = "fail"
ok_pass needle = '=pass'  ref_pass needle = '=PASS'  summary needle = '=PASS'
verdict expression present: True

reachable refusal-leg combinations enumerated: 192
max REFUSE count over all reachable legs: 0/7
combinations where ref_pass is True (necessary for C1=PASS): 0
max-REFUSE leg set:
  FOREIGN=pass(refused)
  SYMLINK_OUT=pass(refused)
  SYMLINK_CACHE=pass(refused)
  FIFO_TXT=pass(refused)
  DEVZERO_TXT=pass(refused)
  FAT_RAW=pass(refused)
  MANY_QUOTES=pass(refused)
EXIT=0
```

Cause: `PASS = "pass"` (`:51`) is the only token every refusal leg emits, while
`ref_pass = all(("=PASS" in l) …)` (`:391`) and the SUMMARY count (`:399`) test the uppercase
literal. **No *honest* candidate builder can print `C1=PASS` or exit 0 under these bytes**; the
frozen target `C1=PASS` (claims.md) is unsatisfiable for a candidate that actually refuses, and
`C1=FAIL` is not evidence about a candidate.

**Correction (measured after this section was first written).** "Unreachable for every builder" is
too strong: the reason-absent failure branch interpolates the *candidate's own stderr* into the leg
(`:150-160`, `:223`) and `ref_pass` (`:391`) is a plain substring scan, so a candidate can satisfy
the uppercase needle with its own output while failing all seven refusal checks. On the frozen bytes
a spoofing candidate reaches `C1=PASS`, exit 0 (§6). The positive path is therefore both
false-negative (honest candidates) and false-positive (echoing candidates); the leg-string probe's
192/192 result only covers non-spoofing stderr.

## 3. Positive-path control: an escaping builder that satisfies every leg *token*

`build-spans-escape-control.py` deliberately violates the symlink-refusal semantics: when `--out`
is a symlink it **writes `spans.tsv` through the link and then refuses** with `SYMLINK`; otherwise
it refuses the symlink/FIFO/oversize/row/foreign/entry fixtures and delegates normal work to the
lane builder. Frozen counter first:

```
$ python3 corpus/evidence/round58/c1-count.py --builder ./build-spans-escape-control.py \
      --work /fast/scratch/hyaku/chousa-r59/R59Executor09/esc-frozen
EMPTY_OK=pass
REBUILD_OK=pass
FOREIGN=pass(refused)
SYMLINK_OUT=pass(refused)(target-dir-written!)
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
--- escaped artifact ---
ESCAPED THROUGH THE SYMLINKED --out
```

All eleven legs report success tokens; the verdict is still `C1=FAIL` / exit 1 (P2). Now the same
builder against the **scratch-only** counter copy whose only change is the refusal needle at `:391`
and `:399` (lane copy still hashes `65da18bb…`):

```
$ python3 ./c1-count-casefixed.py --builder ./build-spans-escape-control.py \
      --work /fast/scratch/hyaku/chousa-r59/R59Executor09/esc-casefixed
EMPTY_OK=pass
REBUILD_OK=pass
FOREIGN=pass(refused)
SYMLINK_OUT=pass(refused)(target-dir-written!)
SYMLINK_CACHE=pass(refused)
FIFO_TXT=pass(refused)
DEVZERO_TXT=pass(refused)
FAT_RAW=pass(refused)
MANY_QUOTES=pass(refused)
ESCAPE_ENTRY=pass(refused)
HELDOUT_OK=pass
BEFORE_FOREIGN=deleted
DENIED=0/0
SUMMARY OK=4/4 REFUSE=7/7 BEFORE_FOREIGN=deleted DENIED=0/0
C1=PASS
EXIT=0
--- escaped artifact ---
ESCAPED THROUGH THE SYMLINKED --out
```

`C1=PASS` is credited to a builder whose first act on a symlinked `--out` is to write into the link
target. The escape is annotated at `:236` (`"(target-dir-written!)"`) but never read by the verdict
(`:391-394`); `expect_refuse`'s `forbidden_touch` (`:161-164`) tests `not p.exists()` and therefore
fails a correct refusal, after which `:233-236` overwrites the leg. This is the positive-weight
counterpart of the base run: containment is not part of the pass predicate.

## 4. The positive verdict is gated on a destructive control artifact

Copying the case-fixed counter into a scratch directory **without** its sibling `controls/`
(the counter resolves `BEFORE_BUILDER = HERE/"controls"/"build-spans-r55.py"`, `:355-360`) and
re-running the all-legs-pass escape control:

```
$ python3 no-baseline/c1-count-casefixed.py --builder ./build-spans-escape-control.py \
      --work /fast/scratch/hyaku/chousa-r59/R59Executor09/nobase-run
EMPTY_OK=pass
REBUILD_OK=pass
FOREIGN=pass(refused)
SYMLINK_OUT=pass(refused)(target-dir-written!)
SYMLINK_CACHE=pass(refused)
FIFO_TXT=pass(refused)
DEVZERO_TXT=pass(refused)
FAT_RAW=pass(refused)
MANY_QUOTES=pass(refused)
ESCAPE_ENTRY=pass(refused)
HELDOUT_OK=pass
BEFORE_FOREIGN=absent
DENIED=0/0
SUMMARY OK=4/4 REFUSE=7/7 BEFORE_FOREIGN=absent DENIED=0/0
C1=FAIL
EXIT=1
```

`integrity` (`:392`) requires `BEFORE_FOREIGN=deleted` — i.e. the counter's own pinned **before**
builder must exist and must be destructive — so an honest candidate in any tree lacking that control
file is scored FAIL. The positive verdict depends on a control artifact, not on the candidate.

## 5. Control denial is a crash, not a scored refusal

```
$ python3 corpus/evidence/round58/c1-count.py \
      --builder corpus/evidence/round58/controls/REFUSEALL.py \
      --work /fast/scratch/hyaku/chousa-r59/R59Executor09/refuseall
Traceback (most recent call last):
  File ".../corpus/evidence/round58/c1-count.py", line 406, in <module>
    sys.exit(main())
  File ".../corpus/evidence/round58/c1-count.py", line 212, in main
    foreign.write_bytes(b"foreign evidence bytes\n")
FileNotFoundError: [Errno 2] No such file or directory: '.../refuseall/out-empty/spans/S777-1.txt'
EXIT=1
```

`:212` writes the FOREIGN fixture into `out-empty/spans/`, which exists only if the candidate passed
`EMPTY_OK`; an early-refusing builder crashes the counter before any leg line. The control loop
(`:376-381`) calls the absence of a `C1=` line `denied`, so `DENIED=n/n` cannot distinguish "control
scored FAIL" from "counter crashed" — the deny-only control set is vacuous for positive-path
calibration.

## 6. Correction — `C1=PASS` is reachable on the frozen bytes by echoing the needle

`expect_refuse`'s reason-absent branch (`:150-160`) and the FOREIGN branch (`:223`) splice up to
160/200 characters of the candidate's stderr into the leg string; `ref_pass` (`:391`) and the
SUMMARY count (`:399`) then substring-scan that assembled string for `=PASS`. A candidate that emits
no declared reason token and fails every refusal check, but prints `=PASS` in its stderr, is credited
`C1=PASS`.

Candidate: `scratch/spoof-builder.py`, sha256
`1a3aad9b25a2c12f274b98a36b065a5155d06ceeb15ab963637efee59d7981fe`. It refuses every hazard with
`build-spans: refused undifferentiated refusal, no reason token: X=pass? =PASS forged` (contains none
of `SYMLINK`, `NOT_REGULAR`, `FIFO`, `REGTYPE`, `SIZE`, `ROWS`, `CAP`, `777`, `foreign`), and on a
symlinked `--out` it writes `spans.tsv` through the link *before* refusing — the exact hazard the leg
exists to forbid. Safe legs delegate to the pinned byte-identical builder (`base/build-spans.py`,
sha256 `1ed2650a…`).

Command and full output on the frozen bytes (`65da18bb…`):

```
$ python3 -B corpus/evidence/round58/c1-count.py --builder scratch/spoof-builder.py \
      --work scratch/work/spoof-frozen
EMPTY_OK=pass
REBUILD_OK=pass
FOREIGN=fail(reason-unnamed:'build-spans: refused undifferentiated refusal, no reason token: X=pass? =PASS forged\n')
SYMLINK_OUT=fail(rc=2, reason ['SYMLINK'] absent in 'build-spans: refused undifferentiated refusal, no reason token: X=pass? =PASS forged\n')(target-dir-written!)
SYMLINK_CACHE=fail(rc=2, reason ['SYMLINK', 'REGTYPE', 'NOT_REGULAR'] absent in 'build-spans: refused undifferentiated refusal, no reason token: X=pass? =PASS forged\n')
FIFO_TXT=fail(rc=2, reason ['NOT_REGULAR', 'FIFO', 'REGTYPE', 'SYMLINK'] absent in 'build-spans: refused undifferentiated refusal, no reason token: X=pass? =PASS forged\n')
DEVZERO_TXT=fail(rc=2, reason ['NOT_REGULAR', 'SIZE', 'SYMLINK', 'REGTYPE'] absent in 'build-spans: refused undifferentiated refusal, no reason token: X=pass? =PASS forged\n')
FAT_RAW=fail(rc=2, reason ['SIZE'] absent in 'build-spans: refused undifferentiated refusal, no reason token: X=pass? =PASS forged\n')
MANY_QUOTES=fail(rc=2, reason ['SIZE', 'ROWS', 'CAP'] absent in 'build-spans: refused undifferentiated refusal, no reason token: X=pass? =PASS forged\n')
ESCAPE_ENTRY=pass(refused)
HELDOUT_OK=pass
BEFORE_FOREIGN=deleted
DENIED=0/0
SUMMARY OK=4/4 REFUSE=7/7 BEFORE_FOREIGN=deleted DENIED=0/0
C1=PASS
EXIT=0
```

Every refusal leg is `fail(...)`; the SUMMARY asserts `REFUSE=7/7`; the verdict is `C1=PASS`,
exit 0. Reproduced twice (pre-wipe run and an atomic re-run after the scratch collision described
under Limits / hygiene), byte-identical.

Consequence: P1's remedy (match the needle case) is necessary but not sufficient, and §2's universal
claim must be read as "no non-spoofing candidate". A sound predicate needs per-leg typed results
(boolean + canonical reason enum) and must never scan prose containing candidate-controlled bytes.

## 7. Two more leg-level leniencies (frozen bytes)

(a) **The SYMLINK_OUT leg does not check the refusal reason.** Candidate `scratch/wrong-builder.py`
refuses every hazard with the token-free reason `build-spans: nope`:

```
$ python3 -B corpus/evidence/round58/c1-count.py --builder scratch/wrong-builder.py \
      --work scratch/work/wrong-frozen
EMPTY_OK=pass
REBUILD_OK=pass
FOREIGN=fail(reason-unnamed:'build-spans: nope\n')
SYMLINK_OUT=pass(refused)
SYMLINK_CACHE=fail(rc=2, reason ['SYMLINK', 'REGTYPE', 'NOT_REGULAR'] absent in 'build-spans: nope\n')
FIFO_TXT=fail(rc=2, reason ['NOT_REGULAR', 'FIFO', 'REGTYPE', 'SYMLINK'] absent in 'build-spans: nope\n')
DEVZERO_TXT=fail(rc=2, reason ['NOT_REGULAR', 'SIZE', 'SYMLINK', 'REGTYPE'] absent in 'build-spans: nope\n')
FAT_RAW=fail(rc=2, reason ['SIZE'] absent in 'build-spans: nope\n')
MANY_QUOTES=fail(rc=2, reason ['SIZE', 'ROWS', 'CAP'] absent in 'build-spans: nope\n')
ESCAPE_ENTRY=pass(refused)
HELDOUT_OK=pass
BEFORE_FOREIGN=deleted
DENIED=0/0
SUMMARY OK=4/4 REFUSE=0/7 BEFORE_FOREIGN=deleted DENIED=0/0
C1=FAIL
EXIT=1
```

`expect_refuse` already returned `fail(reason [...] absent in 'build-spans: nope')` for that leg, but
`:233-236` overwrites it with `SYMLINK_OUT=pass(refused)` whenever the symlink target directory stays
empty — discarding the reason result. Any candidate `rc != 0` passes this leg for the wrong reason.

(b) **The deny loop cannot discriminate.** With `--controls` pointing at a directory whose
`build-spans-r55.py` slot is the candidate that passes all eleven legs (§A above, renamed), the
frozen counter reports:

```
CONTROL_REFUSEALL=denied
CONTROL_build-spans-r55=denied
DENIED=2/2
SUMMARY OK=4/4 REFUSE=0/7 BEFORE_FOREIGN=deleted DENIED=2/2
C1=FAIL
EXIT=1
```

The "control" is the same bytes that satisfy every leg; it is denied only because `:391` makes
`C1=PASS` unreachable. With §5 (crash-as-denial) this makes `DENIED=n/n` carry no calibration signal
under the frozen bytes.

## 8. Reproduction fidelity of this seat's runs

The frozen counter against the lane pinned builder reproduces the frozen round-59 before receipt
exactly: its stdout equals `corpus/evidence/round59/controls/c1-before.txt` minus the trailing
`EXIT=1` line (the round-58 and round-59 receipt copies are the same bytes, sha256 `2c9bbe54…`).

```
$ python3 -B corpus/evidence/round58/c1-count.py --builder tools/build-spans.py \
      --work scratch/work/before-repro
EMPTY_OK=pass
REBUILD_OK=pass
FOREIGN=fail(rc=0, orphans deleted: foreign gone=True)
SYMLINK_OUT=fail(rc=0, expected refusal)(target-dir-written!)
SYMLINK_CACHE=fail(rc=0, expected refusal)
FIFO_TXT=fail(rc=1, reason ['NOT_REGULAR', 'FIFO', 'REGTYPE', 'SYMLINK'] absent in 'build-spans: refused S571: ...')
DEVZERO_TXT=fail(rc=1, reason ['NOT_REGULAR', 'SIZE', 'SYMLINK', 'REGTYPE'] absent in 'build-spans: refused S581: ...')
FAT_RAW=fail(rc=1, reason ['SIZE'] absent in 'build-spans: refused S551: ...')
MANY_QUOTES=fail(rc=0, expected refusal)
ESCAPE_ENTRY=pass(refused)
HELDOUT_OK=pass
BEFORE_FOREIGN=deleted
DENIED=0/0
SUMMARY OK=4/4 REFUSE=0/7 BEFORE_FOREIGN=deleted DENIED=0/0
C1=FAIL
EXIT=1
receipt_lines_without_EXIT == counter_stdout: True
```

(Abbreviated reason excerpts only; the pre-wipe diff of the full 15 lines was `16d15 < EXIT=1`.)
So the scratch execution is faithful to the frozen package, and `tools/build-spans.py` is still the
round-55 before bytes (`1ed2650a…`): no candidate hardening has landed in the lane.

## Findings (reported, nothing edited)

| # | severity | location | finding | evidence |
|---|---|---|---|---|
| P1 | critical | `c1-count.py:51,150-160,223,232-236,391,399` | Refusal legs emit lowercase `=pass`; verdict requires uppercase `=PASS`; `C1=PASS`/exit 0 unreachable for **any non-spoofing** builder (P6 carves out echoed stderr); SUMMARY also prints `REFUSE=0/7` beside a possible PASS | §2 (192/192 non-spoofing combos, 0 ref_pass), §1, §3 |
| P2 | critical | `c1-count.py:232-236` vs `:391-394` | With only the token case repaired, a builder that writes through the symlinked `--out` before refusing is credited `C1=PASS`; `(target-dir-written!)` is emitted but unread | §3 (`C1=PASS`, EXIT=0, escaped artifact bytes) |
| P3 | high | `c1-count.py:355-360,392` | Positive verdict is gated on the counter's sibling destructive r55 control (`BEFORE_FOREIGN=deleted`): an honest candidate in a tree without that file scores FAIL | §4 (`BEFORE_FOREIGN=absent` → `C1=FAIL`) |
| P4 | high | `c1-count.py:212,376-381` | Early-refusing control crashes at `:212` (no leg/C1 line); "denied" is absence-of-verdict, so the do-nothing control clause does not discriminate | §5 |
| P5 | high | `c1-count.py:161-164,233-236` | `forbidden_touch` is inverted (fails when the path is absent, passes when present); the SYMLINK_OUT leg is then overwritten, so a correct refusal reads as failure and a leak reads as refusal | §3 source inspection + prior R58 seats |
| P6 | critical | `c1-count.py:150-160,223,391,399` | Reason-absent leg text interpolates candidate stderr; the `"=PASS"` substring lets a candidate that fails all seven refusal legs (and writes through the symlink) reach `C1=PASS`, exit 0 **on the frozen bytes** | §6 (full output; `spoof-builder.py` `1a3aad9b…`) |
| P7 | high | `c1-count.py:233-236` | SYMLINK_OUT discards its reason check: any `rc != 0` with an empty symlink target passes (`build-spans: nope` → `pass(refused)`) | §7(a) |
| P8 | high | `c1-count.py:376-381,391` | Deny loop vacuous under frozen bytes: the all-legs candidate placed in a control slot is reported `denied`; `DENIED=2/2` cannot certify calibration | §7(b) |

## Calibration implication for the round-59 target (proposal only)

A repaired C1 predicate needs, at minimum, all of: (1) refusal-leg token case matched to emission
(`:391`/`:399`) — necessary but not sufficient; (2) the containment signal made load-bearing:
`(target-dir-written!)` must force FAIL (and `forbidden_touch` must test `exists()`); (3) a
must-pass control that is containment-honest, so the escape control above is denied — today the two
are indistinguishable once P1 is fixed; (4) integrity decoupled from the before-builder artifact, or
the control pinned self-contained; (5) control denial distinguished from crash; (6) per-leg typed
results (boolean + canonical reason enum) instead of substring scans over leg text that contains
candidate-controlled stderr — otherwise an echoing builder reaches `C1=PASS` (P6), which is strictly
worse than the unreachable path; (7) the SYMLINK_OUT leg must verify the refusal reason rather than
`rc != 0` plus an empty target directory (P7). My escape-control (`44303a37…`), this run's
`spoof-builder.py` (`1a3aad9b…`), `wrong-builder.py` and the leg-string probe (`4b95fcb8…`) are
reusable falsifiers: a calibrated counter must deny the spoof/wrong-reason builders *and* credit the
honest full-legs candidate.

## Limits / hygiene

- Lane read-only for this seat: only `read`/`grep`/`sha256sum` against lane files; every run passed
  `--work` inside this seat's scratch. Lane writes: this report only. No `git`/`jj` mutation.
- **Duplicate seat instance / shared scratch.** Two live instances of seat R59Executor09 were
  dispatched into the same scratch root. The other instance's baseline run used
  `--work /fast/scratch/hyaku/chousa-r59/R59Executor09/base`; the seat root was rmtree'd at ~15:19
  and again at ~15:23, deleting this instance's first-round logs and `base/` copy. This instance
  re-created its probes and re-ran the full measurement set atomically; every result quoted in §3,
  §6, §7 and §8 is from the final runs. The same collision pattern was reported to this seat for
  foreign `positive-path/` bytes under `.../R59Executor07/` (not this seat's writes; replied to
  `R59Executor07-2`, nothing deleted). No sibling scratch files were written or removed.
- No install was needed (Python 3.14.8 present); `/home/vgpnk/.omp/agent/RULES.md` install rules were
  therefore not exercised, and pacman was not run.
- Not exercised: `c2-count.py` (out of this seat's assignment), any live fetch, any claim-level
  calibration (round-59 claims absent).
- Scratch `/fast/scratch/hyaku/chousa-r59/R59Executor09` removed after the final runs; all outputs
  above are transcribed verbatim, including the escaped-artifact bytes.

---
seat: R59Executor09
lane-root: /home/vgpnk/Projects/shokunin/chousa-shokunin
report: .ufo/waves/round-59/w1/R59Executor09.md
scratch: /fast/scratch/hyaku/chousa-r59/R59Executor09 (removed)
lane writes: .ufo/waves/round-59/w1/R59Executor09.md (this file) only

# R58ScribeCounterReceipt — chousa round 58, seat leaf (report only)

Base: lane `9e73a031ab1ac3bac343de008850d7d87f9e5634` (freeze); claim base `b13ca7b5…`. Frozen bytes
re-hashed, not read from prose: `c1-count.py` = `65da18bbcb03581ca98354d90049215ed3cab3bfd3e41d483908dc1e1c703d3f`
(identical at freeze and at observed lane HEAD `718e8d2`, which adds only committed control files);
`tools/build-spans.py` = `1ed2650af28ea8e392bc34f7259cfb58f93b05c7453aca60e86b170c59c80bf6` =
`controls/build-spans-r55.py` = pinned r55. No install, no fetch, no lane/git mutation; my counter copy was
byte-identical. Scratch `S=/fast/scratch/hyaku/chousa-r58/R58ScribeCounterReceipt` (removed before yield);
each probe below is a scratch probe — **not** a lane candidate, **not** a proposed patch.
## 1. Lane behaviour the frozen C1 measures (tool surface)
Lane receipt `corpus/evidence/round58/controls/c1-before.txt` (committed at freeze; read, not produced, by me):
```
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
SUMMARY OK=4/4 REFUSE=0/7 BEFORE_FOREIGN=deleted DENIED=0/0
C1=FAIL
```
At freeze the C1 operand is the **unmodified** r55 builder, so all seven declared hazard classes are unrefused
at base: foreign `spans/S777-1.txt` deleted as an orphan; symlinked `--out` written through (rc 0); symlinked
cache `.txt` read (rc 0); FIFO/device refused only incidentally ("no defined text form"), no type gate; the
80 MiB `.raw` read in full before a malformed-file error, no size gate; 100,001-row `quotes.tsv` accepted
(rc 0). `BEFORE_FOREIGN=deleted` reproduces in my runs below (pinned bytes, sha verified) — declared battery
only, not a general security conclusion.
## 2. Counter failure A — a builder satisfying every declared leg is refused
Probe B = scratch front-end with exactly the six declared gates (symlink / FIFO / size / row-cap /
foreign-before-orphan), delegating to a byte-copy of pinned r55 (`$S/r55/build-spans.py` `1ed2650a…`,
`capture-text.py` `2c0140bc…` beside it):
```
$ python3 $S/c1-count.py --builder $S/probe-b-gated-r55.py --work $S/work-b
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
Cause, frozen bytes: refusal legs emit `PASS = "pass"` (`:51`, `:160` `f"{name}={PASS}(refused)"`, `:223`,
`:234`) while the verdict greps the other token (`:391` `ref_pass = all(("=PASS" in l) …)`); the tally repeats
it (`:399`). `ref_pass` is `False` for any candidate whose legs read `pass`, so `C1=PASS` (`:394`, exit `:402`)
is unreachable for an honest builder — `REFUSE=0/7` over seven passing legs. Sibling seat
`R58ScribeMistakeMine` reached the same unreachability by another mock; this is the reproduction.
## 3. Counter failure B — the only demonstrated route to `C1=PASS` credits an attacker
Probe D = scratch builder that writes `spans.tsv` **through** a symlinked `--out` then exits 1, keeps the
foreign `S777-1.txt` while naming no reason class, and refuses the rest for no declared reason; its only lever
is the literal token `=PASS` in stderr — builder-controlled text the verdict greps:
```
$ python3 $S/c1-count.py --builder $S/probe-d-token-leak.py --work $S/work-d
EMPTY_OK=pass
REBUILD_OK=pass
FOREIGN=fail(reason-unnamed:'build-spans: refused token =PASS\n')
SYMLINK_OUT=fail(rc=1, reason ['SYMLINK'] absent in 'build-spans: refused token =PASS\n')(target-dir-written!)
SYMLINK_CACHE=fail(rc=1, reason ['SYMLINK', 'REGTYPE', 'NOT_REGULAR'] absent in 'build-spans: refused token =PASS\n')
FIFO_TXT=fail(rc=1, reason ['NOT_REGULAR', 'FIFO', 'REGTYPE', 'SYMLINK'] absent in 'build-spans: refused token =PASS\n')
DEVZERO_TXT=fail(rc=1, reason ['NOT_REGULAR', 'SIZE', 'SYMLINK', 'REGTYPE'] absent in 'build-spans: refused token =PASS\n')
FAT_RAW=fail(rc=1, reason ['SIZE'] absent in 'build-spans: refused token =PASS\n')
MANY_QUOTES=fail(rc=1, reason ['SIZE', 'ROWS', 'CAP'] absent in 'build-spans: refused token =PASS\n')
ESCAPE_ENTRY=pass(refused)
HELDOUT_OK=pass
BEFORE_FOREIGN=deleted
DENIED=0/0
SUMMARY OK=4/4 REFUSE=7/7 BEFORE_FOREIGN=deleted DENIED=0/0
C1=PASS
EXIT=0
$ ls -la $S/work-d/realdir → spans/ + spans.tsv (43 bytes, written through the symlink)
```
Seven `fail(reason … absent)` lines plus a written-through symlink target yield `C1=PASS`, exit 0,
`REFUSE=7/7`. The substring tests (`:391`, `:399`) and the `(target-dir-written!)` append (`:234-237`) read
whole leg lines, which embed builder stderr — the kill rule ("any missing refusal reason … kills C1") is
defeated where it must bite. Both directions are counter arithmetic, not builder properties.
## 4. Counter crash — the always-refuse control is "denied" by crash, not by a leg outcome
```
$ python3 $S/c1-count.py --builder $S/controls/REFUSEALL.py --work $S/work-refuseall
EXIT=1   stdout: (empty)
stderr: File "…/c1-count.py", line 212, in main → foreign.write_bytes(b"foreign evidence bytes\n")
        FileNotFoundError: … '/…/work-refuseall/out-empty/spans/S777-1.txt'
```
`:212` assumes the candidate created `out/spans` on the first leg; any candidate failing `EMPTY_OK` without it
aborts before one `LEG` or `C1=` line. `CONTROL_REFUSEALL=denied` (`c1-controls.txt`, `DENIED=2/2`) is thus a
no-stdout crash, not a verdict: that control clause is vacuous.
## 5. Secondary counter defects (frozen bytes; first one demonstrated)
- `:234-237` can append the violation marker to a string still reading `pass`: probe C (writes through the
  symlink, then exits nonzero with `SYMLINK`) prints `SYMLINK_OUT=pass(refused)(target-dir-written!)`.
- `expect_refuse` (`:150-161`) inverts the forbidden-touch test — `:159` `if not p.exists(): … "was
  touched/removed"` reports an absent file as removed; only `SYMLINK_OUT` supplies that list and its result is
  overwritten at `:234`, so the check is inert.
- `HELDOUT_OK` passes `snapshot(work)` **after** the build (`:345`): the outside-`--out` check is vacuous.
- Dead code: `ok_pass` assigned `:389`, overwritten `:390`; `expect_ok`'s `got`/`want` (`:120-122`) unused.
- Control provenance: at freeze `git status` showed `REFUSEALL.py`, `build-spans-r55.py`, `c1-controls.txt`,
  `c2-controls.txt` untracked; now committed at `718e8d2` (a later seat, not me), bytes unchanged (`1ed2650a…`).
## 6. Report-ready concise description (what failed and why)
> At freeze the C1 operand (`tools/build-spans.py`, sha `1ed2650a…`) is byte-identical to the pinned r55 builder,
> so the seven declared hazard classes are unrefused at base: the foreign `spans/S###-N.txt` is deleted as an
> orphan, a symlinked `--out` is written through (rc 0), a symlinked cache input is read (rc 0), FIFO/device
> inputs are refused only incidentally ("no defined text form"), the 80 MiB `.raw` is read in full before a
> malformed-file error, and a 100,001-row `quotes.tsv` is accepted (rc 0) — an operability gap on the declared
> battery, not a security conclusion. The counter cannot receipt either outcome: refusal legs emit `PASS="pass"`
> (`c1-count.py:51/160/223/234`) while the verdict and tally grep `=PASS` (`:391/399`), so a builder passing all
> eleven legs prints `REFUSE=0/7`, `C1=FAIL`, exit 1; the only route found to `C1=PASS`, exit 0 is a builder
> leaking `=PASS` into stderr, naming no reason class and writing through the symlinked `--out` (`REFUSE=7/7`
> over seven `fail(…)` lines). It also aborts with `FileNotFoundError` (`:212`) when a candidate creates no
> `out/spans` — how its always-refuse control is "denied" — and `:234` can tag a `pass` line
> `(target-dir-written!)`. No C1 after-measurement exists; the verdict line is unusable as a receipt either way.
## 7. Out of scope, unrun, untouched
- Unrun: any live fetch (none authorized; round-57 r2 egress-scope L0 question still open); `c2-count.py` and the
  C2/S101 entry (not this seat's surface); the real round-58 hardened builder (executors own it); text-size caps
  and broader races, which C1 expressly does not claim.
- Untouched: `claims.md`, both counters, `controls/`, `tools/`, all git/jj state, fleet root, sibling lanes; no
  planner role taken (L1 holds the canonical seat). Writes: this report only. All probe fixtures lived under `$S`
  and are removed; the commands and outputs above are the durable record.

VERDICT: Two concrete attacks on the frozen C1 gate at `9e73a03`. (a) *Token leak* — a scratch builder naming
no declared reason class that writes `spans.tsv` through a symlinked `--out` while emitting `=PASS` in stderr is
credited `C1=PASS`, `REFUSE=7/7`, exit 0: **survives**, defeating the stated kill rule. (b) *Honest builder* —
the counter **falsifies** a builder passing all eleven declared legs (`REFUSE=0/7`, `C1=FAIL`, exit 1);
`C1=PASS` is unreachable without the token. It also **crashes** (`FileNotFoundError`, `:212`) on any candidate
failing `EMPTY_OK` without `out/spans`, so the always-refuse control's denial is a crash. The lane's operability
state is **inconclusive as a scored gate** (base fails all seven hazard classes; no after-receipt exists and none
can be produced under these frozen bytes); the claim verdict is L1's, not this seat's.

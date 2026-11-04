# R78ExecB — `--work` contract control, both directions (QUALITY 142 → 144)

Seat: leaf executor, round 78 wave 1. Read-only against the lane tree; every artifact below is
under `.ufo/waves/round-78/w1/R78ExecB/`. Scratch `/fast/scratch/hyaku/chousa-r78/R78ExecB/`
was deleted after the receipts were copied. No instrument was edited; no frozen receipt was
amended; no tool was installed or upgraded (so there is no tool/version/channel row to record).

Frozen revision: lane `HEAD` at measurement was `01b444b7` (`round-78: freeze the two claims
against the controls commit`); the controls commit named in `claims.md`, `93e0432e`, is an
ancestor of it (`git merge-base --is-ancestor 93e0432e HEAD` → 0). The three instrument
digests were re-checked before any run and match the frozen table exactly:

| instrument | measured sha256 | claims.md |
|---|---|---|
| `corpus/evidence/round78/work-contract.py` | `e51d8917…ffa8a0` | match |
| `corpus/evidence/round78/matrix-battery-v5.py` | `5545a471…2b5af0` | match |
| `corpus/evidence/round77/matrix-battery-v4.py` | `155fafb1…106a3d` | match |

## 1. The control, direction BEFORE (`--battery` = v4) — exit 1

```
$ python3 -B corpus/evidence/round78/work-contract.py \
    --battery corpus/evidence/round77/matrix-battery-v4.py \
    --work /fast/scratch/hyaku/chousa-r78/R78ExecB/wc-v4
BATTERY_PATH=/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round77/matrix-battery-v4.py
BATTERY_SHA256=155fafb16b6931449abefb60575029f273959ba4e94a4db48ac22e525f106a3d
CASE A rc=0 sentinel_survived=no dir_exists=no
CASE B rc=1 traceback=yes stderr_first=Traceback (most recent call last):
CASE C rc=1 traceback=yes stderr_first=Traceback (most recent call last):
WORK_CONTRACT=FAIL survived=no unwritable_exit=1 file_exit=1
```

**exit code: 1** (1.5 s wall). Receipt: `R78ExecB/work-contract-before-v4-r78execb.txt`.

This reproduces the committed pre-freeze receipt
`corpus/evidence/round78/controls/work-contract-before-v4.txt` line-for-line: `diff` of my
stdout against that file (work path normalised, `# ` comment lines stripped) is empty, rc 0.

## 2. The control, direction AFTER (`--battery` = v5) — exit 0

```
$ python3 -B corpus/evidence/round78/work-contract.py \
    --battery corpus/evidence/round78/matrix-battery-v5.py \
    --work /fast/scratch/hyaku/chousa-r78/R78ExecB/wc-v5
BATTERY_PATH=/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round78/matrix-battery-v5.py
BATTERY_SHA256=5545a4718690a80e5d3d6611e43132fdd5cb4dcd67e87be9a27ed44c032b5af0
CASE A rc=1 sentinel_survived=yes dir_exists=yes
CASE B rc=2 traceback=no stderr_first=matrix-battery-v5: cannot create --work /fast/scratch/hyaku/chousa-r78/R78ExecB/wc-v5/b/nested: [Errno 13] Permission denied:
CASE C rc=2 traceback=no stderr_first=matrix-battery-v5: cannot create --work /fast/scratch/hyaku/chousa-r78/R78ExecB/wc-v5/c: [Errno 17] File exists: '/fast/scratch/hyaku/chousa-r78/R78ExecB/wc-v5/c'
WORK_CONTRACT=PASS survived=yes unwritable_exit=2 file_exit=2
```

**exit code: 0** (1.5 s wall). Receipt: `R78ExecB/work-contract-after-v5-r78execb.txt`.

Against `controls/work-contract-after-v5.txt` the only diff is the two `stderr_first=` tails,
and only because the two runs named different absolute `--work` paths, which shifts where the
control's 120-character truncation cuts the identical diagnostic. Every decision field
(`CASE A/B/C` rc and flags, `WORK_CONTRACT=`) is identical.

**Reading note on `CASE A rc=1`:** case A's return code is deliberately unconstrained by the
control (`ok = survived and rc_b == 2 and …`); only `survived` counts. On v5, `rc=1` is the
battery *refusing* the a1 identity forger — the intended v5 behaviour, and the same refusal
that makes `forge-battery.py` count it. It is not a setup failure. The before direction's
`CASE A rc=0` is v4 *accepting* that same forger (round 77's defect), not a stronger result.

## 3. Independent confirmation, outside the control

Probe: `.ufo/waves/round-78/w1/R78ExecB/probe-work-contract.py` (30 checks, fail-closed: any
unmet check prints `FAIL` and the process exits 1). Receipts: `probe-independent.txt`,
`probe-results.json`.

```
$ python3 -B .ufo/waves/round-78/w1/R78ExecB/probe-work-contract.py \
    --lane /home/vgpnk/Projects/shokunin/chousa-shokunin \
    --scratch /fast/scratch/hyaku/chousa-r78/R78ExecB/probe
… 29 × ok, 1 × FAIL …
PROBE=FAIL checks=30 failed=1 names=P5.run-dir-cleaned
# exit: 1
```

The single failure is a real defect, §4. What the 29 passing checks establish:

**(a) The v5 run leaves the caller's sentinel byte-identical.** The sentinel is a payload a
text-mode round-trip would mangle — `b"the caller put this here\r\n\x00tab\there   \ntrailing
spaces   \nno final newline"`, sha256 `0d0780cd07a5e3cbe5370864e2f7e2b4c609fc0613dd87c726dc65226158edcd`
(the control only compares `read_text()`, so byte identity is strictly stronger). Measured on
both battery outcomes, with a full directory manifest (`relpath → sha256`, directories and
symlinks included) captured before and after:

- `P1` forger-refused run, `rc=1`: sentinel sha unchanged; `manifest-unchanged: added=[]
  removed=[]`; no `r78-*` entry left; `stderr_lines=0`.
- `P2` **PASS** run against the legitimate positive matrix `corpus/evidence/round76/loader-matrix-v3.py`,
  `rc=0`, last line `BATTERY=PASS forgers_rejected=11/11 positive=2/2 oracle=REJECTED`:
  sentinel sha unchanged; `manifest-unchanged: added=[] removed=[]`. A PASS run therefore
  leaves the caller's directory exactly as it found it, not merely a refused one.
- `P6` the same through a symlinked `--work`: the link itself survives
  (`is_symlink=True`, target unchanged), the target's manifest is unchanged.

**(b) A `--work` that is a regular file exits 2 with a one-line diagnostic and no traceback.**
`P3`, file `regular-file` holding `b"not a directory\nsecond line\n"`:

- `rc=2`, `stderr` is exactly one non-empty line, `stdout` is empty;
- the line is `matrix-battery-v5: cannot create --work <path>: [Errno 17] File exists: '<path>'`;
- `"Traceback" not in stderr`;
- the file's own bytes are unchanged (`sha=46e03d0f…89b81`), i.e. the failure is
  could-not-evaluate, not a truncation.

That exit code is the one the instrument documents (`Exit: 0 BATTERY=PASS · 1 BATTERY=FAIL ·
2 usage/env`). Two adjacent shapes also hold: an unwritable `--work` (`P4`, `rc=2`, no
traceback) and an unwritable *parent* of `--work` (`P4`, `Errno 13`, one line).

**(c) The before direction really is destructive, measured without the control** (`P1`-style
payload, `v4` invoked directly): `rc=0` with `BATTERY=PASS forgers_rejected=11/11 positive=2/2
oracle=REJECTED`, and afterwards `ls --work` → `No such file or directory` — directory and
sentinel both gone. Receipt `v4-direct-destroy.txt`. So the control's `CASE A
sentinel_survived=no dir_exists=no` is the battery's `finally: shutil.rmtree(work)` at
`matrix-battery-v4.py:256-257`, and v5's replacement of it with `shutil.rmtree(run)` at
`matrix-battery-v5.py:324-325` (where `run = work/"r78-"+token_hex(8)`, line 291) is what the
control scores.

## 4. Defect found (reported, not repaired)

**`matrix-battery-v5.py` leaks its own run directory on the missing-subject exit.** The order in
`main()` is: `run = work / ("r78-" + secrets.token_hex(8))` (291), `run.mkdir()` (292-293), then
the subject-existence guard, which returns before the `try:` at 307:

```
303:    for _group, _name, source in subjects:
304:        if not pathlib.Path(source).resolve().is_file():
305:            print(f"matrix-battery-v5: missing subject {source}", file=sys.stderr)
306:            return 2
307:    try:
```

A missing subject therefore exits 2 leaving an empty `r78-<hex>` directory inside the caller's
`--work`. Measured (`P5`) with a scratch copy whose sha256 is asserted equal to the frozen
instrument's (`5545a471…2b5af0`, `P5.copy-is-instrument` ok), so the executed code is the
committed code, and with the caller's sentinel present:

```
P5.exit: rc=2
P5.no-traceback: matrix-battery-v5: missing subject …/corpus/evidence/round74/correction-count.py
FAIL P5.run-dir-cleaned: left=['caller-file.txt', 'r78-5e95d5fe70d063da'] leaked_dir_empty=True inside=[]
P5.sentinel-bytes: checked
```

Severity and scope, stated exactly:

- It **creates** debris; it **deletes nothing the caller owns** and does not damage the
  sentinel, so the QUALITY 144 harm (a caller's data destroyed, or a setup failure reported as
  a traceback at exit 1) does not occur on this path.
- It is new in v5: v4's equivalent early return at `matrix-battery-v4.py:238-239` precedes its
  `try:`, but v4 created no directory before that point, so it leaked nothing there.
- The frozen C1 predicate (`forge-battery.py`) never reaches it — its subjects all exist — and
  the `--work` contract control never reaches it either (its three cases are: sentinel present,
  unwritable dir, path is a file). So this is invisible to both scored surfaces, which is
  exactly why it is a carried observation rather than a claim failure.
- Contract reading: QUALITY 144 says "creates and deletes only its own run directory". It does
  delete only its own directory; on this one exit path it fails to delete it. The literal
  predicate in `claims.md`/144 is `WORK_CONTRACT=PASS survived=yes unwritable_exit=2
  file_exit=2`, and that predicate is met.
- I did not edit the instrument: `claims.md` freezes it, and a rule changed after a seat scores
  it is not the claim's rule.

## 5. Risks / limits of this seat's evidence

1. The missing-subject path is only reachable on the committed instrument by removing a subject
   from the read-only lane tree, so §4 rests on a byte-identical scratch copy; the copy's digest
   is recorded, but the run was not on the committed path itself.
2. The control's `CASE A` accepts any return code; a reader must not read `rc=1` on v5 as a
   control failure (see §2). Nothing in the control distinguishes "refused the forger" from
   "failed for another reason at exit 1" — `survived` alone carries case A.
3. `stderr_first` is truncated at 120 characters, so two runs of the control on paths of
   different length cannot be diffed byte-for-byte; I normalised the path and compared the
   decision fields instead (§2).
4. Inherent to any such harness and untested here: `SIGKILL`/`SIGTERM` between `run.mkdir()`
   and the `finally` leaves the run directory behind, and v5 leaves a caller-named `--work`
   that it had to create in place (empty) rather than removing it — deliberate, and the safe
   direction.
5. Every measurement is this host's (`Linux 7.2.11-arch1-1`, `python3` 3.14) and this lane
   revision (`01b444b7`, controls `93e0432e`); the receipts record both.

## Files

- `.ufo/waves/round-78/w1/R78ExecB.md` (this report)
- `.ufo/waves/round-78/w1/R78ExecB/work-contract-before-v4-r78execb.txt` (control, exit 1)
- `.ufo/waves/round-78/w1/R78ExecB/work-contract-after-v5-r78execb.txt` (control, exit 0)
- `.ufo/waves/round-78/w1/R78ExecB/probe-work-contract.py` (independent probe, fail-closed)
- `.ufo/waves/round-78/w1/R78ExecB/probe-independent.txt`, `probe-results.json`,
  `probe-independent.stderr.txt` (empty)
- `.ufo/waves/round-78/w1/R78ExecB/v4-direct-destroy.txt`,
  `v4-direct-destroy.stderr.txt` (empty)

Scratch `/fast/scratch/hyaku/chousa-r78/R78ExecB/` deleted.

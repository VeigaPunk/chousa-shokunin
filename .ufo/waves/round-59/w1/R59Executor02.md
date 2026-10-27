# R59Executor02 — round-58 frozen C1 counter: positive-verdict-path defect

Lane: `/home/vgpnk/Projects/shokunin/chousa-shokunin` (read-only for this seat; no lane file was
edited, no git/jj write). Scratch: `/fast/scratch/hyaku/chousa-r59/R59Executor02` (removed during
the run; see Evidence retention). No network. Axis: operability.

## 0. Inputs actually used, and one missing input

- The dispatch names `corpus/evidence/round59/claims.md` as the frozen claims. **It does not
  exist.** `corpus/evidence/round59/` contains only:

  ```
  corpus/evidence/round59/controls/c1-before.txt
  corpus/evidence/round59/census-start.txt
  ```

  `census-start.txt` is the 5-line W04 duplicate-URL census with `exit=0`; it carries no predicate.
- Work therefore used the frozen predicate that the round-59 item names: **round-58's frozen C1
  counter** `corpus/evidence/round58/c1-count.py` under `corpus/evidence/round58/claims.md` (present,
  frozen at `b13ca7b5…`). The counter copy in scratch is byte-identical to the lane file:

  ```
  $ sha256sum counter/c1-count.py /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round58/c1-count.py
  65da18bbcb03581ca98354d90049215ed3cab3bfd3e41d483908dc1e1c703d3f  counter/c1-count.py
  65da18bbcb03581ca98354d90049215ed3cab3bfd3e41d483908dc1e1c703d3f  /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round58/c1-count.py
  ```
- The counter's pinned "before" control was copied with it:
  `counter/controls/build-spans-r55.py` sha256 `1ed2650af28ea8e392bc34f7259cfb58f93b05c7453aca60e86b170c59c80bf6`.

**Context finding C0.** The lane's own `tools/build-spans.py` is byte-identical to that pinned
before-control (so the counter's default `--builder` *is* the builder the claim pins as the
must-fail baseline; the round-58 hardened candidate was never landed), and round-58 carries no
`c1-measure-after.txt` receipt:

```
$ sha256sum tools/build-spans.py corpus/evidence/round58/controls/build-spans-r55.py
LANE_BUILDER_SHA=1ed2650af28ea8e392bc34f7259cfb58f93b05c7453aca60e86b170c59c80bf6  tools/build-spans.py
R55_CONTROL_SHA=1ed2650af28ea8e392bc34f7259cfb58f93b05c7453aca60e86b170c59c80bf6  corpus/evidence/round58/controls/build-spans-r55.py
$ diff -u corpus/evidence/round58/controls/build-spans-r55.py tools/build-spans.py && echo IDENTICAL
IDENTICAL
$ ls corpus/evidence/round58/ | grep -i measure      # no output
```

## 1. The frozen aggregate against the frozen leg emitters

Verbatim source lines of the copied frozen counter:

```
c1-count.py:51: PASS = "pass"
c1-count.py:52: FAIL = "fail"
c1-count.py:147:     return f"{name}={PASS}"                     # expect_ok success
c1-count.py:160:     return f"{name}={PASS}(refused)"            # expect_refuse success
c1-count.py:384:     ok_legs = [l for l in legs if l.split("=")[0] in
c1-count.py:386:     ref_legs = [l for l in legs if l.split("=")[0] in
c1-count.py:389:     ok_pass = all(l.endswith("(pass)") or l.endswith(")") and f"{FAIL}" not in l and "=pass" in l for l in ok_legs)
c1-count.py:390:     ok_pass = all(("=pass" in l) for l in ok_legs)
c1-count.py:391:     ref_pass = all(("=PASS" in l) for l in ref_legs)
c1-count.py:394:     verdict = "PASS" if (ok_pass and ref_pass and integrity and denied_pass) else "FAIL"
c1-count.py:398:     print(f"SUMMARY OK={sum('=pass' in l for l in ok_legs)}/{len(ok_legs)} "
c1-count.py:399:           f"REFUSE={sum('=PASS' in l for l in ref_legs)}/{len(ref_legs)} "
```

(Line 400 continues `f"BEFORE_FOREIGN={before} DENIED={denied}/{total}")`.)

Every leg emitter uses lowercase `PASS = "pass"` (`:51`, `:147`, `:160`), and the FOREIGN pass path
also uses it. The safe-leg aggregate at `:390` therefore searches the same lowercase token it is
given, but the hazard-leg aggregate at `:391` and the `REFUSE=` count at `:399` search **uppercase**
`=PASS`. Since `ref_legs` always contains the seven hazard legs (`FOREIGN`, `SYMLINK_OUT`,
`SYMLINK_CACHE`, `FIFO_TXT`, `DEVZERO_TXT`, `FAT_RAW`, `MANY_QUOTES`), `ref_pass` is `False` for any
genuine all-refusals-pass run.

Function-level measurement (imports the frozen copy; no counter side effects):

```
$ python3 -B probe/expr_probe.py
PASS_CONST='pass' FAIL_CONST='fail'
expect_refuse(named)='GENUINE=pass(refused)'
expect_refuse(unnamed,'=PASS')="FORGED=fail(rc=1, reason ['SYMLINK'] absent in 'denied by guard C1=PASS')"
... (source lines above) ...
[compensating] OK_LEGS=4/4 REF_LEGS=7/7 ok_pass=True frozen_ref_pass=False caseless_ref_pass=True frozen_REFUSE_COUNT=0/7
[forge] OK_LEGS=4/4 REF_LEGS=7/7 ok_pass=True frozen_ref_pass=True caseless_ref_pass=True frozen_REFUSE_COUNT=7/7
```

## 2. Measured: a builder that satisfies every frozen leg still gets `C1=FAIL`

Scratch probe `probe/b-compensating.py` (sha256 `5d99a5216df1748a5e04fba1b212387d7b7e4c4e492a9ae80cb24099a768c663`):
builds byte-exact spans for the safe legs, resolves `.raw` through the lane's pinned
`tools/capture-text.py`, refuses FOREIGN before deleting, refuses symlinked out, symlinked cache,
FIFO, `/dev/zero` symlink, 80 MiB raw by SIZE, >100 000 quotes by ROWS, and `..` entries — all with
the frozen reason classes.

```
$ cd /fast/scratch/hyaku/chousa-r59/R59Executor02
$ python3 -B counter/c1-count.py --builder probe/b-compensating.py \
    --work /fast/scratch/hyaku/chousa-r59/R59Executor02/work/abs2 --seed 7 ; echo "EXIT=$?"
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

All four safe legs pass, all seven hazard legs pass, integrity passes, controls vacuously pass —
`ok_pass=True`, `ref_pass=False`. **`C1=PASS` is unreachable for any builder that passes the frozen
battery**, because the verdict token the emitters produce (`=pass(refused)`) is not the token
`:391` searches (`=PASS`).

## 3. Measured: the only reachable `C1=PASS` is a failing-legs path

`probe/d-forge.py` (sha256 `23b41d232ba61af2e12e91e77caaf894b4b7a8729b2d493ddc883d17eea358bc`)
runs the compensating builder, and on every refusal (a) writes `marker.txt` through the resolved
`--out` and (b) replaces stderr with `build-spans: denied by generic guard C1=PASS (no named reason
class)` and exits 1. No named reason class is ever printed, and on the symlink-out fixture it writes
into the symlink target.

```
$ python3 -B counter/c1-count.py --builder probe/d-forge.py \
    --work /fast/scratch/hyaku/chousa-r59/R59Executor02/work/abs4 --seed 7 ; echo "EXIT=$?"
EMPTY_OK=pass
REBUILD_OK=pass
FOREIGN=fail(reason-unnamed:'build-spans: denied by generic guard C1=PASS (no named reason class)\n')
SYMLINK_OUT=fail(rc=1, reason ['SYMLINK'] absent in 'build-spans: denied by generic guard C1=PASS (no named reason class)\n')(target-dir-written!)
SYMLINK_CACHE=fail(rc=1, reason ['SYMLINK', 'REGTYPE', 'NOT_REGULAR'] absent in 'build-spans: denied by generic guard C1=PASS (no named reason class)\n')
FIFO_TXT=fail(rc=1, reason ['NOT_REGULAR', 'FIFO', 'REGTYPE', 'SYMLINK'] absent in 'build-spans: denied by generic guard C1=PASS (no named reason class)\n')
DEVZERO_TXT=fail(rc=1, reason ['NOT_REGULAR', 'SIZE', 'SYMLINK', 'REGTYPE'] absent in 'build-spans: denied by generic guard C1=PASS (no named reason class)\n')
FAT_RAW=fail(rc=1, reason ['SIZE'] absent in 'build-spans: denied by generic guard C1=PASS (no named reason class)\n')
MANY_QUOTES=fail(rc=1, reason ['SIZE', 'ROWS', 'CAP'] absent in 'build-spans: denied by generic guard C1=PASS (no named reason class)\n')
ESCAPE_ENTRY=pass(refused)
HELDOUT_OK=pass
BEFORE_FOREIGN=deleted
DENIED=0/0
SUMMARY OK=4/4 REFUSE=7/7 BEFORE_FOREIGN=deleted DENIED=0/0
C1=PASS
EXIT=0
```

Every hazard leg on that output is a `fail(...)` line: no named reason class was emitted, and the
symlink-out target was written. `:391` matches only because `expect_refuse()`'s reason-absent branch
embeds captured stderr (`{err[:160]!r}`, `:156`) and the FOREIGN branch embeds `{err!r}` (`:224`).
Case-insensitive matching alone would not fix this: the `[forge]` line above shows
`caseless_ref_pass=True` as well. The verdict must be carried as a structured boolean, not
recovered by substring search over message text.

## 4. Leg-integrity holes found while exercising the battery

**(a) `SYMLINK_OUT` verdict is overwritten regardless of refusal** (`c1-count.py` FOREIGN block end /
SYMLINK_OUT block):

```
    legs.append(expect_refuse("SYMLINK_OUT", proc, ["SYMLINK"], [real / "spans.tsv"], ))
    if not any(real.iterdir()):
        legs[-1] = f"SYMLINK_OUT={PASS}(refused)"
    else:
        legs[-1] += "(target-dir-written!)"
```

The `expect_refuse` verdict is discarded whenever the target dir stays empty — rc and reason class
are not consulted. Measured with `probe/NOOP.py` (sha256 `2729dc2d…`, exits 0, creates `out/spans`
and writes nothing, never touches a symlinked out):

```
$ python3 -B counter/c1-count.py --builder probe/NOOP.py \
    --work /fast/scratch/hyaku/chousa-r59/R59Executor02/work/noop ; echo "EXIT=$?"
EMPTY_OK=fail(no spans.tsv)
REBUILD_OK=pass
FOREIGN=fail(rc=0, orphans deleted: foreign gone=False)
SYMLINK_OUT=pass(refused)
SYMLINK_CACHE=fail(rc=0, expected refusal)
FIFO_TXT=fail(rc=0, expected refusal)
DEVZERO_TXT=fail(rc=0, expected refusal)
FAT_RAW=fail(rc=0, expected refusal)
MANY_QUOTES=fail(rc=0, expected refusal)
ESCAPE_ENTRY=fail(rc=0, written=False)
HELDOUT_OK=fail(no spans.tsv)
BEFORE_FOREIGN=deleted
DENIED=0/0
SUMMARY OK=1/4 REFUSE=0/7 BEFORE_FOREIGN=deleted DENIED=0/0
C1=FAIL
EXIT=1
```

**(b) `REBUILD_OK` passes on a builder that produces nothing.** The leg only compares
`snapshot(out)` before/after the second run; with `NOOP` no `spans.tsv` is ever produced and
`REBUILD_OK=pass`. As a standalone leg it does not discriminate a rebuild from an empty directory.

**(c) `FOREIGN` failure text is inverted for the rc=0 case.** `NOOP` prints
`FOREIGN=fail(rc=0, orphans deleted: foreign gone=False)` — the foreign file was *not* deleted; the
failure is "accepted the input" (`:214`).

**(d) Dead assignment.** `ok_pass` is computed at `:389` and immediately overwritten at `:390`; the
first expression is unsound for `EMPTY_OK=pass` (it requires the string to end with `(pass)` or `)`),
so only the accidental overwrite keeps safe legs meaningful.

## 5. Crash instead of verdict (operability)

`c1-count.py:212` — `foreign.write_bytes(...)` — assumes `out-empty/spans` exists. If the builder
did not produce a spans directory on `EMPTY_OK`, or if `--work` is relative (the counter then hands
relative paths to a builder it runs with `cwd=str(work)`), the counter raises and prints **no leg
lines and no `C1=` line**:

```
$ python3 -B counter/c1-count.py --builder probe/b-compensating.py --work work/rel ; echo "EXIT=$?"
...
  File ".../counter/c1-count.py", line 212, in main
    foreign.write_bytes(b"foreign evidence bytes\n")
FileNotFoundError: [Errno 2] No such file or directory: 'work/rel/out-empty/spans/S777-1.txt'
EXIT=1

$ python3 -B counter/c1-count.py --builder counter/controls/REFUSEALL.py \
    --work /fast/scratch/hyaku/chousa-r59/R59Executor02/work/refuseall ; echo "EXIT=$?"
...
FileNotFoundError: [Errno 2] No such file or directory: '/fast/scratch/.../work/refuseall/out-empty/spans/S777-1.txt'
EXIT=1
```

Consequently the official `REFUSEALL` control is "denied" by crash, not by measurement, and a
harness that equates a non-zero exit with `denied` cannot distinguish crash from verdict:

```
$ python3 -B counter/c1-count.py --work .../work/abs-controls --seed 7 --controls .../counter/controls
CONTROL_REFUSEALL=denied
CONTROL_build-spans-r55=denied
DENIED=2/2
SUMMARY OK=4/4 REFUSE=0/7 BEFORE_FOREIGN=deleted DENIED=2/2
C1=FAIL
```

Default `--builder` (lane `tools/build-spans.py`) produced leg lines, `SUMMARY` and `C1=` values
identical, as displayed, to the 12 leg lines of `controls/c1-before.txt` (`REFUSE=0/7`, `C1=FAIL`,
`BEFORE_FOREIGN=deleted`), ~40 s wall.

## 6. Stored-form hazard for any positive-verdict builder

`HELDOUT_OK` correctly derives the text form from the `.raw` capture via the pinned
`capture-text.py` (raw sha256 `6063a3aff7a4081e93a685f2721e2cd6b477ba84a841211e298bcddd6d9fddf3`,
matching the frozen C2 raw pin; 129 024 B). The sibling sidecar
`corpus/captures/6dc68fd6b32ce9c8dfcebce8.txt` (157 816 B, sha256 `d4e7e5ad…`) is **not a text
form**: it begins with U+FFFD followed by the OLE signature bytes and does not contain the frozen
quote `本规范共设置以下五种：` (`quote_in_txt False`). A scratch builder that preferred `.txt` was
refused with `build-spans: refused quote not found for S601`; switching to `.raw` made `HELDOUT_OK`
pass. Any future positive-verdict builder must not trust a same-key `.txt` sidecar.

## Findings

| id | finding | source |
|----|---------|--------|
| F1 | Hazard-leg aggregate searches uppercase `=PASS` while emitters produce lowercase `=pass(refused)`; `ref_pass` is False for every builder that genuinely passes the battery, so `C1=PASS` is unreachable on the all-legs-pass path. | `c1-count.py:51,147,160,391,399`; §1, §2 |
| F2 | `ref_pass` becomes True only when a *failing* leg's embedded stderr contains `=PASS`; a forged control reaching `C1=PASS`/exit 0 with all seven hazard legs failing was measured. Verdict must not be recovered from message text (case-insensitive search still fails this). | `c1-count.py:156,224,391`; §3 |
| F3 | `SYMLINK_OUT`'s verdict is overwritten to `pass(refused)` on an empty target dir, ignoring rc and reason class; a no-op builder that exits 0 obtains the leg. | `c1-count.py:233-236`; §4a |
| F4 | `REBUILD_OK` passes on an empty output (no `spans.tsv`); not discriminating by itself. | §4b |
| F5 | Missing spans dir / relative `--work` crashes at `c1-count.py:212`; no leg lines, no `C1=` line, so controls are "denied" by absence. | §5 |
| F6 | Counter default `--builder` is byte-identical to the pinned before-control (`1ed2650a…`); the round-58 hardened builder is not in the lane and no after-receipt exists. | C0 |
| F7 | `corpus/captures/…6dc68fd6b32ce9c8dfcebce8.txt` is not the defined text form while `.raw` plus `capture-text.py` is; sidecar-trusting builders get refused on `HELDOUT_OK`. | §6 |
| F8 | `ok_pass` dead/unsound first assignment at `:389`; benign only because `:390` overwrites it. | §4d |

Operability consequence: the round-58 C1 gate cannot signal success at all, and its only reachable
success signal is triggered by refusal-message text, i.e. the gate is not a positive-verdict control
surface. A frozen re-issue needs (i) one structured per-leg boolean, (ii) leg text emitted without
being searched for the verdict, (iii) no verdict overwrite on `SYMLINK_OUT`, and (iv) a crash-free
missing-spans path.

## Evidence retention

All commands above were run from `/fast/scratch/hyaku/chousa-r59/R59Executor02` on this host
(`python3` 3.14, no network). Scratch held `counter/` (frozen counter + controls copies), `probe/`
(five probe controls + `expr_probe.py` + the captured `.out` files), and `work/` (counter work
dirs). Verbatim outputs are reproduced in §§1–6; the outputs above were captured from those runs
and are the retained record. The scratch tree was removed during the run — when the final leg-line
re-diff was attempted the directory was already absent (`ls: cannot access
'/fast/scratch/hyaku/chousa-r59/R59Executor02': No such file or directory`), so the removal was
external, not a write of this seat; probe sources can be reconstructed from the descriptions and
hashes below. Probe sha256s:

```
5d99a5216df1748a5e04fba1b212387d7b7e4c4e492a9ae80cb24099a768c663  probe/b-compensating.py
23b41d232ba61af2e12e91e77caaf894b4b7a8729b2d493ddc883d17eea358bc  probe/d-forge.py
2729dc2d08c4590ddff653eabbf4c473ab6a9feb1e59aec24c6ba972a9ba77fa  probe/NOOP.py
db52ba7820b778aeb2e5c4530c37b4f036a32cd13dd7a5b53f78c9de37d96c5f  probe/expr_probe.py
65da18bbcb03581ca98354d90049215ed3cab3bfd3e41d483908dc1e1c703d3f  counter/c1-count.py (= lane file)
```

Lane files changed: none. Tool installs/updates: none. Blockers: none; the named round-59
`claims.md` is absent (C0), so the round-58 frozen predicate was used.

Report: `.ufo/waves/round-59/w1/R59Executor02.md`

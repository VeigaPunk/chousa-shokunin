# CritC1Seq — R61-C1 call-sequence forge (critic, wave w1)

Scope: attack R61-C1 by call-sequence inference under the amended shuffle (A1). Lane read-only; forge, fixtures and
logs lived in /fast/scratch/hyaku/chousa-r61/CritC1Seq (deleted before yield). No installs, no network, no git writes.
Lane check after runs: `git -C <lane> status --porcelain -- tools corpus/evidence/round61` printed nothing.

## Findings

1. **Frozen command (random seed, no `--seed`): best call-sequence forge = 15/20 at all 5 seeds.** Seeds were drawn by
   the counter: 4281664984, 4051996151, 3000344513, 482477860, 639963194. Every seed gave `LEGS=15/20 C1=FAIL`.
2. **The one leg above the do-nothing stub is H08.** The stub (exit 2, no writes) scores 14/20 (ablation below). The
   sequence forge's only gain is the repeated-run fingerprint of H07/H08: the third invocation in one leg directory
   carries `--replace`, which no other leg presents at that run index.
3. **Channel used for the 15:** the builder's own invocation log `<work>/.seq.jsonl` (in the parent of its cwd) gives
   the run index within the leg directory, plus the builder's own `sys.argv` flags. The decision key is
   `(run_index, sorted flags)`; nothing else is read in this condition (no `/proc`, no `/dev/shm`, no fixture input).
   The shuffled order is not learnable from it: the sibling count `k` is logged but unused.
4. **If the seed is on argv (`c1-count.py ... --seed N`), the forge scores 20/20 at 5 of 5 seeds (62101–62105).** It reads
   the counter's argv with `ps -o args= -p <ppid>`, regex `--seed (\d+)`, replays
   `random.Random(N*7919+1).shuffle(list(range(18)))` and maps the k-th leg directory to its group. Logged groups matched
   the replayed order (seed 62101: order `[1,0,8,17,15,...]`; forge saw grp 1,0,8 at k=1,2,3). A1's secret order does
   not survive a visible seed. The frozen counting command passes no `--seed`, so the frozen count is not broken this way;
   reruns and regress workflows that pass `--seed` are.
5. **The admission sweep does not catch that forge.** `grep -nE 'getppid|/proc/|c1-count|round61|leg-|argv\[0\]'` on the
   20/20 forge exits 1 (no match), because `ps` replaces `/proc`. The sweep is a string filter, not a control.
6. **Parent-memory channel is closed here.** A child cannot read its ancestor's memory: `memprobe.py` printed
   `child_read_parent_mem regions=0 marker_hits=0 err=PermissionError(13, 'Permission denied')` (ptrace_scope=1), while the
   parent still held its marker. The seed cannot be lifted from the counter's heap by a builder child.
7. **Repeated runs and two-name groups (fingerprints as logged):**
   - P02/P03: one invocation (docx). P03 has no invocation of its own, so no sequence fingerprint. P03 passes under refusal
     (no `__pycache__` written), so a do-nothing stub also passes P03; it does not discriminate.
   - H07/H08: three invocations in one leg dir: `(0,[])`, `(1,[])`, `(2,['--replace'])`. The third is unique: H08 flips.
   - P04: `(0,[])`, `(1,['--check'])`, `(2,['--check'])`. Visible, but P04 still fails under refusal (its first run must
     produce the golden tree).
   - P06: `(0,[])`, `(1,[])`. The second run collides with H07's second run `(1,[])`: sequence-ambiguous. P06 fails anyway.
8. **Counter observation (calibration).** A builder that writes nothing makes P04 fail through the counter's own
   exception path, not the predicate: `counter exception FileNotFoundError: .../out/spans` (c1-count.py line 314,
   `sorted((fx.out / "spans").iterdir())`). Under a refusing builder P04's verdict is not a measured pass or fail.

## Runs (all `python3 -B corpus/evidence/round61/c1-count.py --builder <forge> --work <fresh> --keep`, TMPDIR in scratch)

| run | builder | seed | output |
|---|---|---|---|
| def1..def5 | forgeB (sha256 aac58340…bf8ce4) | random (no --seed) | `LEGS=15/20 C1=FAIL` ×5 |
| seed62101..62105 | forgeB | `--seed` visible | `LEGS=20/20 C1=PASS` ×5 |
| ablation | forgeB with the `--replace` rule removed | random | `LEGS=14/20 C1=FAIL` |
| base-def | base `tools/build-spans.py` (blob 072415ad, file sha 1ed2650a…) | random | `LEGS=7/20 C1=FAIL` (matches controls/c1-before.txt) |

Default forge, per leg (all 5 seeds identical in pattern): PASS P03, H07, H08, H09, H10, H11, H12, H13, H14, H15, H16,
H17, H18, H19, H20 (15). FAIL P01 (rc 2), P02 (rc 2), P04 (counter exception), P05 (rc 2 where 1 is required),
P06 (rc 2,2).

## The forge (the entire attack; base builder appended after the `from __future__` line; scratch copy deleted)

```python
import json as _fj, os as _fo, pathlib as _fp, random as _fr, re as _fre, subprocess as _fsp, sys as _fs
_fcwd = _fp.Path(_fo.getcwd())
_flog = _fcwd.parent / ".seq.jsonl"
_fargv = _fs.argv[1:]
_fflags = sorted(f for f in ("--check", "--replace") if f in _fargv)
_fprev = _flog.read_text().splitlines() if _flog.exists() else []
_frun = sum(1 for ln in _fprev if _fj.loads(ln)["dir"] == _fcwd.name)
_fcls = [_frun, _fflags]
_fk = sum(1 for p in _fcwd.parent.iterdir() if p.is_dir())
_fact = "golden" if _fcls == [2, ["--replace"]] else "refuse"
_fgrp = None
_fppid = _fsp.run(["ps", "-o", "ppid=", "-p", str(_fo.getpid())], capture_output=True, text=True).stdout.strip()
_fcmd = _fsp.run(["ps", "-o", "args=", "-p", _fppid], capture_output=True, text=True).stdout if _fppid else ""
_fseed = _fre.search(r"--seed (\d+)", _fcmd)
if _fseed:  # seed visible: replay the counter's shuffle and index the leg group by sibling count
    _forder = list(range(18))
    _fr.Random(int(_fseed.group(1)) * 7919 + 1).shuffle(_forder)
    _fgrp = _forder[_fk - 1]
    _fact = "golden" if (_fgrp <= 4 or (_fgrp == 5 and _fcls == [2, ["--replace"]])) else "refuse"
with _flog.open("a") as _f:
    _f.write(_fj.dumps({"dir": _fcwd.name, "cls": _fcls, "k": _fk, "seed_visible": bool(_fseed), "grp": _fgrp, "act": _fact}) + "\n")
if _fact == "refuse":
    _fs.exit(2)
if _fseed:
    _fs.dont_write_bytecode = True
_fs.argv = _fs.argv[:1] + [a for a in _fargv if a != "--replace"]
```

`refuse` = exit 2 before any write; `golden` = unmodified base code. The 20/20 variant's group table is the
counter's `plan` order read from c1-count.py lines 585–590: groups 0–4 golden, group 5 (H07/H08) golden only for
`(2,--replace)`, groups 6–17 refuse. It is a token forge by construction; it bounds the channel, it is not a candidate.

## Information channels, status

| channel | status | what it carried |
|---|---|---|
| parent-dir sibling count `k` | used (logged) | position only; order unknown without seed: 0 bits in default condition |
| parent-dir invocation log (`.seq.jsonl`) | used | run index within leg dir; with argv flags gives H08 and P04 r2 fingerprints |
| builder argv flags | used | `--check`, `--replace` |
| `ps -o args= -p <ppid>` (counter argv) | used in seed-visible run | `--seed N` when passed: full order → 20/20 |
| `/proc/<ppid>/mem` | measured: PermissionError | blocked (ptrace_scope=1, child cannot read ancestor) |
| `/dev/shm` | probe only: write, read back, removed | not needed; no leg information beyond the parent dir |
| builder environment | read from source (c1-count.py 248–249): PATH, HOME, LANG, LC_ALL only | no seed, no leg (not run) |
| fixture timestamps | not measured; creation order equals `k` by construction | no order information (INFERENCE from source) |
| fixture input (q.tsv, cache, out) | not used in the forge | would identify every leg (INFERENCE; a full-input forge is not built) |

## Limits and INFERENCE

- A better sequence-only policy using earlier legs' fingerprints (set difference at the last position) could add at most
  one leg per seed. INFERENCE; not built.
- Five seeds, one forge, one machine. Counter ran with `--keep`; forge and fixtures deleted afterward.
- The 14/20 ablation equals the exit-2 stub recorded in controls/c1-controls.txt. My forge reaches it plus H08 only.

## Verdict

Under the frozen random-seed command the call-sequence channel lifts a do-nothing builder from 14/20 to 15/20 (H08 only);
the shuffle order itself is not learned. With the seed visible on argv the same channel reaches 20/20.

VERDICT: SEQ_FORGE_BEST=15/20 over 5 seeds

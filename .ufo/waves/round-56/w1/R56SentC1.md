# R56SentC1 — hazard review: round-56 C1 counter, gate, battery, probes, controls

Surface: `corpus/evidence/round56/{c1-count.py,c1-gate.py,battery/*.py,probes/*.py,controls/*.py}` at lane rev 46e1758
(claims frozen at 41c5892). Method: static read of every write/spawn/temp path, one full frozen run with
`TMPDIR=$S --work $S/w1`, one SIGINT mid-run (real and stand-in `soffice`), and two demos that run the lane gate's
literal `HOOK` string on scratch fixtures. Lane untouched; no predicate/target/counter/control changed; no tool installed.

Baseline (operability, this host): `python3 corpus/evidence/round56/c1-count.py --work $S/w1` → rc 0, 309 s,
`RUNS=124`, P1 FORKEXEC and P2 DIRFD `DENIED` (1,'FAIL'×4) at seeds 7/56, `CANDIDATE=2/2 KILLED=9/9 DENIED=2/2
C1=PASS`. The frozen target reproduces; only the wall time differs from the claims' 132 s pass (host at its 100-job cap).

## F1 — MEDIUM: read boundary bypassable by `dir_fd` **without** `chdir`; P2 closes one variant only

Exploit: `open(cwd/"zz","w")` (run dir, in `ALLOW`) → `os.symlink(OUTSIDE, TOOLDIR/"zz")` (`os.symlink` is not an
event `HOOK` inspects) → `fd=os.open(TOOLDIR)` (allowed) → `os.open("zz", O_RDONLY, dir_fd=fd)`. The `open` audit
event carries the path string only, never `dir_fd`, so `allowed()` (`c1-gate.py:100-110`) resolves `realpath(cwd/zz)`
= the decoy inside the run dir while the kernel follows `TOOLDIR/zz` outside.

    $ cd $H/run; R55_ALLOW="$H/run:$H/hook.py:$H/tool:/usr" python3 $H/hook.py $H/tool/probe.py
    BYPASS_READ OUTSIDE-CONTENT-42 / BYPASS_UNLINK gone= True / BYPASS_RENAME ok= True
    HOOK_DID_NOT_STOP_ME          rc=0
    $ python3 c1-gate.py --tool $S/gatetool/probe2.py --seed 7 --per-leg 2 --work $S/w5   # in situ, real gate
    GENOLE=FAIL no spans.tsv      # rc 0: tool ran past the read, no AUDIT_FORBIDDEN
    $ cat $S/gatetool/leak.txt → IN-SITU-OUTSIDE-SECRET-7

Impact: `c1-gate.py:4-6` infers that denying `os.chdir` closes the dir_fd gap ("a cwd change lets a `dir_fd`-relative
open resolve outside…"); chdir is one enabler, not the enabler, and no probe exercises the no-chdir form. C1's frozen
predicate is unaffected (P2 DENIED, reproduced). Smallest remediation (round 57, gate-side): check the opened fd's
`/proc/self/fd/N` target after every `open`, or deny `os.symlink`/`os.link` and re-resolve; report only for round 56.

## F2 — MEDIUM: mutation syscalls are unaudited, so the hook is a read/spawn boundary, not a write boundary

`BAD` (`c1-gate.py:93-95`) holds spawn/exec/socket/ctypes; `PATHS` (`:96`) holds `open`, `os.listdir`, `os.scandir`.
`os.mkdir/remove/rename/rmdir/unlink/link/symlink/truncate/chmod` are in neither, so they are legal on any path:

    BYPASS_UNLINK gone= True / BYPASS_RENAME ok= True   # os.remove / os.rename outside ALLOW, no denial
    # in situ through the gate: $S/gt-outside/victim.txt deleted, $S/gt-outside/newdir created; legs then judge

Impact: `--tool` is caller-chosen (`:440`) and the JUNK control proves an outside dir can be a battery, so such a tool
can delete/rename lane evidence or the read-only `.qcache` captures while the receipt still prints the sha256 the driver
took *before* the runs (`c1-count.py:188`). My run wrote nothing because the eight frozen entries are honest — nothing
enforces that. Smallest remediation: add the mutation events to the `PATHS` check (one tuple edit), and re-hash after
the runs (F3).

## F3 — LOW/MEDIUM: no post-run purity assertion; a battery entry keeping state beside itself writes into the lane

The hook allows the tool's own directory (`:202`), so `flip.state` beside `junk-flip0.py` is silently legal; only the
control builder refuses an in-lane `OUTDIR` (`controls/build-c1-junk.py:15`):

    $ python3 controls/build-c1-junk.py $S/junk && python3 c1-gate.py --tool $S/junk/junk-flip0.py --seed 7 --per-leg 2 --work $S/w7
    $ cat $S/junk/flip.state → 7        # 7 tool calls: GENOLE 1 + OLEPIN 1 + REFUSE 4 + REGRESS 1
    $ python3 controls/build-c1-junk.py $L/…/round56/battery/junk → OUTDIR must lie outside the lane

Impact: the same entry inside `battery/` would create `battery/flip.state` in the lane and survive untracked; the driver
never re-reads lane state. My run: `find $L/corpus/evidence/round56/battery -newer $S/stamp` → 0 files. Smallest
remediation: after the last `R.run`, recompute the sha256s printed at `c1-count.py:185-188` and exit 2 `BATTERY_MUTATED`.

## F4 — LOW: SIGINT/timeout kills the direct child only; `soffice` is orphaned and its tree is deleted underneath

    $ python3 c1-count.py --work $S/w2 & … kill -INT $drv; wait → driver_rc=130
    $ find $S/w2 -maxdepth 3 → ./gates/{G,M1..M9}.py  ./runs/015b38d38551cce6/g/{hook.py,gen-g-695425564,soffice-profile}
    $ PATH=$S/fakebin:$PATH … & kill -INT; sleep 2; pgrep -af fakebin/soffice
    23686 /bin/sh …/fakebin/soffice -env:UserInstallation=file://…/w3/runs/d60951ecbba5dcb9/g/soffice-profile …
    $ TMPDIR=$S python3 c1-count.py  # default --work, SIGINT: root r56c1-htxeu6t4 gone, same child alive

`subprocess.run` (`c1-count.py:128-131`, `c1-gate.py:186-188,420`) kills only its own child; no `start_new_session`, no
`killpg`. With `--work` the in-flight run dir survives (partial OLE tree + private profile); with the default the
`finally` `rmtree` (`c1-count.py:285-286`) deletes the root while the orphan holds it. Same shape on the 1800 s driver
timeout and the gate's 300/600 s timeouts. Impact: one leaked `soffice.bin` per interrupt, no lane write.
Remediation: `start_new_session=True` at both spawn sites and `os.killpg` before any `rmtree`.

## F5 — LOW (operability): relative `--work`, `--work` at a file, and no lane-root guard

    $ TMPDIR=$S python3 c1-gate.py --work relwork --seed 7 --per-leg 2
      File "c1-gate.py", line 181, in __init__ … ValueError: relative paths can't be expressed as file URIs
      $ ls $S/relwork → hook.py      # written into the cwd-derived relative dir before the crash
    $ python3 c1-count.py --work $S/run1.out → FileExistsError: … 'run1.out'   # traceback, not usage error
      $ python3 c1-count.py --work $S/w1 → usage: --work must be empty          # rc 2, clean

Neither `c1-count.py:159-161` nor `c1-gate.py:454-456` refuses a `--work` inside `LANE` (both control builders do:
`build-c1-junk.py:15`, `build-c2-controls.py:63`). No receipt is affected — every frozen one passes an absolute scratch
path. Remediation: `resolve()` plus a `LANE in work.parents` refusal before the first write, in both files.

## F6 — INFO: TMPDIR honoured everywhere, no hardcoded `/tmp`

`mkdtemp` `c1-count.py:159`, `c1-gate.py:454`; children get `TMPDIR=<work>` (`:125`) and `TMPDIR=<run>/tmp`
(`c1-gate.py:201,417`); `soffice` uses a private `-env:UserInstallation` under the work dir and inherits that `TMPDIR`.
Grep for `/tmp`, `/var/tmp`, `/dev/shm`, `gettempdir` across all seven files: no hit outside docstrings.

    $ TMPDIR=$S PATH=$S/fakebin2:$PATH python3 c1-gate.py --seed 7 --per-leg 2
    /fast/scratch/hyaku/chousa-r56/R56SentC1/r56gate-w4rylpy6     # root under TMPDIR, polled mid-run
    ENV_CHANGED soffice did not write an OLE g0.doc               # after: 0 roots left, no r56* name in /tmp
    ~/.config/libreoffice mtime 2026-10-22 (pre-existing; never touched by these runs)

## F7 — INFO: P2's `mkdir` is confined but trusts its cwd

`p2-dirfd.py:16` makes `p2sub` under `os.getcwd()`; the driver runs tools with `cwd=<run dir>` (`c1-count.py:128-131`),
so it lands where the driver `rmtree`s (`:135`); it survives only because the hook's `os._exit(97)` pre-empts the
probe's `rmdir`:

    $ python3 c1-gate.py --tool probes/p2-dirfd.py --seed 7 --per-leg 2 --work $S/w6
    GENOLE=FAIL rc=97 b'AUDIT_FORBIDDEN os.chdir\n'  OLEPIN=FAIL rc=97 …  REFUSE=FAIL NOFORM: rc=97  REGRESS=FAIL rc=97 …
    $ find $S/w6 -maxdepth 2 -name p2sub → run1-…/p2sub run2-…/p2sub run3-…/p2sub run4-…/p2sub

Under the frozen invocation there is no leak; run by hand from the lane root it would create (and normally remove)
`p2sub` in the lane. Remediation: refuse a cwd outside `R55_ALLOW` before the mkdir, or use `mkdtemp` under `TMPDIR`.

## Containment receipts for my own runs

`--work $S/w1`, `TMPDIR=$S`. `git status --porcelain` before/after differs only by sibling report files under
`.ufo/waves/round-56/w1/`; all 21 lane files whose mtime falls in my window (01:57–02:03) are that dir's `*.md`;
`find $L/tools -newer $S/stamp` → empty; lane battery → 0 files newer. After the clean run: `w1/gates/` (10 gate
copies) and `w1/runs/` (124 dirs created, 124 removed at `c1-count.py:135`, 0 left); no `r56c1-*`, no `soffice.bin`
naming my scratch. Caveat for other seats: `find -newer` is unreliable here — `.ufo/waves/round-33/…/keep-s9001/root/*.md`
carry future mtimes (2026-11-09/11-29), so the mtime-window query, not `-newer`, is the trustworthy form.

VERDICT: attacked the round-56 C1 driver/gate/battery/probe/control surface for write containment, temp paths, signal
cleanup and hook closure — the frozen C1 verdict SURVIVES (CANDIDATE=2/2 KILLED=9/9 DENIED=2/2, C1=PASS, 124 runs, lane
and CACHE untouched, no /tmp use), while the gate's *read boundary* is FALSIFIED: a `dir_fd` open needs no `chdir` (F1,
in situ) and mutation syscalls go unaudited (F2) — reported, not patched.

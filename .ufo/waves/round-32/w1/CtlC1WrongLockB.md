# C1 wrong-lock controls — CtlC1WrongLockB

## Axes and result

- **Operability:** interoperability with an independent exclusive `flock(2)` holder on the manifest, not merely serialization among identical gate processes.
- **Coverage:** whether frozen C1 distinguishes wrong inode, per-process inode, wrong lock family, and a non-flock spin lock.
- **Result:** all four controls **MISSES** on both fresh seeds. None reaches `APPEND_SERIALIZED=24/24`; no wrong-lock escape was observed. These are control-predicate results, not candidate admission or a canonical judgment.

## Scope and provenance

Lane: `/home/vgpnk/Projects/shokunin/chousa-shokunin`.
Scratch prefix **S**: `/fast/scratch/hyaku/chousa-r32/w1/CtlC1WrongLockB/`.
Evidence prefix **A**: `.ufo/waves/round-32/w1/CtlC1WrongLockB/`, relative to the lane.
All abbreviated evidence paths below are relative to **A**.

Read first: `corpus/evidence/round32/claims.md:1-117`, then both counter docstrings. C1's required object, lock family, and critical-section lifetime are at `claims.md:23-28`; frozen target is at `claims.md:36-40`.

Commands observed:

```text
timeout 20 df -h /fast
exit 0: /dev/nvme1n1p2 804G total, 568G used, 236G available, 71% used

timeout 20 sha256sum /home/vgpnk/Projects/shokunin/chousa-shokunin/tools/research-gate.sh /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round32/c1-count.py /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round32/c2-count.py
exit 0:
0bc318b3e74ac0ad45f4b34154e886d84aebf44673612afab6de5e0b0ff11258  tools/research-gate.sh
9e787e80b215f6522335c639d5e1b2e60d0a5812b83a9760daf8be9f78415885  corpus/evidence/round32/c1-count.py
b6626b2cb81b2aeaf66a8ff11a06c030612bf4e264dc128f290021c4aa71f54c  corpus/evidence/round32/c2-count.py

timeout 20 git show 4111607c857bc29ff31883bc095ae00afb527e50:corpus/evidence/round32/c1-count.py | timeout 20 sha256sum
exit 0: 9e787e80b215f6522335c639d5e1b2e60d0a5812b83a9760daf8be9f78415885  -
```

The copied base has the required base SHA-256, and every receipt's `counter_sha256` matches the frozen commit (`*.json:3`). Neither counter was edited. No candidate implementation was run.

## Controls built

Each control started as a copy of **S**`research-gate.sh`, which is byte-identical by SHA-256 to the required base. Only the append-block control mechanism was changed.

| Control | Scratch gate | Relevant lines | SHA-256 |
|---|---|---|---|
| (a) sibling `PATH.lock` flock | `sibling-flock-gate.sh` | 3192-3208 | `cddd8cae755620da69c9f61ddc5bd6931de15becd4b2252093266cb1ef7e06c7` |
| (b) per-process `PATH.lock.$$` flock | `per-process-flock-gate.sh` | 3192-3208 | `f02db76766f29106e967155ee19addec5272cca3c00f0634b98d43c0845db249` |
| (c) Python POSIX `fcntl.lockf` on PATH | `posix-lockf-gate.sh` | 3189-3209 | `bf1b9c06f050d84dc5b2443cc10235ea52ab0accce634f94486c15ac067f2863` |
| (d) mkdir spin lock at `PATH.lock` | `mkdir-spin-gate.sh` | 3192-3216 | `13f387cf3095804242eb1d869b9dd0b2ddb672472f01f4ed0a201dddf6cba3f7` |

(a)/(b) wrap the existing last-byte probe and append with `flock -x`, unlock, and descriptor close, but lock the wrong inode. (c) opens the manifest `O_WRONLY|O_CREAT|O_APPEND`, holds `fcntl.lockf(fd, LOCK_EX)` across a `tail -c1` probe and `os.write`, then closes it. This is deliberately a POSIX record lock, not a manifest flock. (d) wraps the original block with mkdir/rmdir; acquisition is bounded to 1,000 attempts, sleeping 0.01 seconds after a failed attempt. None is offered as a correct implementation.

Hashes were recorded with `timeout 20 sha256sum` over the five named scratch gates (exit 0); the four control hashes are also independently stamped by the frozen counter in each receipt at line 5.

## Exact scoring method

`S/score-control.py` selects only the four named controls, draws two fresh `secrets.randbits(63)` seeds per control, and invokes the unmodified frozen counter. The four independent control scorers were submitted together through the parallel tool wrapper:

```text
timeout --kill-after=10s 850s python3 /fast/scratch/hyaku/chousa-r32/w1/CtlC1WrongLockB/score-control.py sibling-flock
timeout --kill-after=10s 850s python3 /fast/scratch/hyaku/chousa-r32/w1/CtlC1WrongLockB/score-control.py per-process-flock
timeout --kill-after=10s 850s python3 /fast/scratch/hyaku/chousa-r32/w1/CtlC1WrongLockB/score-control.py posix-lockf
timeout --kill-after=10s 850s python3 /fast/scratch/hyaku/chousa-r32/w1/CtlC1WrongLockB/score-control.py mkdir-spin
```

All four scorer commands exited 0. Each inner counter command exited **1**, the defined predicate-miss exit, not a harness error. Every solo reference exit was 0 (`receipt.json:7`).

For every row below, the full executed inner command is preserved verbatim in `<stem>.command.json:5`, cwd at line 4, exit code at line 6, gate/counter hashes at lines 7-8. Its form was:

```text
env C1_TMP=/fast/scratch/hyaku/chousa-r32/w1/CtlC1WrongLockB C2_TMP=/fast/scratch/hyaku/chousa-r32/w1/CtlC1WrongLockB TMPDIR=/fast/scratch/hyaku/chousa-r32/w1/CtlC1WrongLockB timeout --kill-after=10s 400s prlimit --nproc=2000 --as=2147483648 --fsize=983040 -- python3 /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round32/c1-count.py --gate /fast/scratch/hyaku/chousa-r32/w1/CtlC1WrongLockB/<control>-gate.sh --seed <seed> --receipt /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-32/w1/CtlC1WrongLockB/<stem>.json
```

The form above uses placeholders only to avoid duplicating eight long commands; the `.command.json` files contain actual paths and numbers, not placeholders.

## Counts, classes, receipts, and per-trial lines

Every row's receipt is `<stem>.json:3-19`; raw count and per-class stdout are `<stem>.stdout.txt:1-5`; **all 24 per-trial lines, including exact failure arrays, are `<stem>.trials.txt:1-24`**. The latter is a rendering of the frozen receipt's `trials`, not a modified counter.

| Control | Fresh seed | APPEND_SERIALIZED | F_unterminated | L_empty | L_terminated | L_unterminated | Verdict | Evidence stem |
|---|---:|---:|---:|---:|---:|---:|---|---|
| sibling flock | 6215270098090743748 | 12/24 | 12/12 | 0/4 | 0/4 | 0/4 | MISSES | `sibling-flock-s6215270098090743748` |
| sibling flock | 7199539608062276134 | 12/24 | 12/12 | 0/4 | 0/4 | 0/4 | MISSES | `sibling-flock-s7199539608062276134` |
| per-process flock | 4661176348059719223 | 6/24 | 6/12 | 0/4 | 0/4 | 0/4 | MISSES | `per-process-flock-s4661176348059719223` |
| per-process flock | 1519897881203437156 | 5/24 | 5/12 | 0/4 | 0/4 | 0/4 | MISSES | `per-process-flock-s1519897881203437156` |
| POSIX lockf | 7774156660351681216 | 12/24 | 12/12 | 0/4 | 0/4 | 0/4 | MISSES | `posix-lockf-s7774156660351681216` |
| POSIX lockf | 8068104468809364743 | 12/24 | 12/12 | 0/4 | 0/4 | 0/4 | MISSES | `posix-lockf-s8068104468809364743` |
| mkdir spin | 5985335950195587660 | 12/24 | 12/12 | 0/4 | 0/4 | 0/4 | MISSES | `mkdir-spin-s5985335950195587660` |
| mkdir spin | 9091431053534308447 | 12/24 | 12/12 | 0/4 | 0/4 | 0/4 | MISSES | `mkdir-spin-s9091431053534308447` |

### Strongest counterexamples and why the counter rejects them

1. **Sibling lock:** all free-writer trials pass on both seeds, but all 24 held-lock trials fail across the two runs. Example: `sibling-flock-s6215270098090743748.trials.txt:2` reports `trial=01 class=L_terminated pass=false fails=["appended-under-cooperating-lock", "prefix-rewritten"]`. The common sidecar serializes these gates, but does not exclude an independent holder on the manifest inode. **Impacted axes:** operability; coverage of lock-object identity.
2. **Per-process lock:** all held-lock trials fail, plus 6/12 and 7/12 free trials fail. Example: `per-process-flock-s4661176348059719223.trials.txt:2` reports `trial=01 class=F_unterminated pass=false fails=["blank-line", "invalid-json-line"]`. Each gate locks an inode no other gate uses, leaving both cooperation and inter-gate delimiter races unprotected. **Impacted axes:** operability; coverage of unique-per-writer false locking.
3. **POSIX lockf:** all free trials pass, but all held-lock trials fail. Example: `posix-lockf-s7774156660351681216.trials.txt:2` reports `trial=01 class=L_unterminated pass=false fails=["appended-under-cooperating-lock"]`. On this host/filesystem the POSIX lock does not cooperate with the counter's flock holder, despite sharing the target path. **Impacted axes:** operability; coverage of lock-family substitution.
4. **mkdir spin:** all free trials pass, but all held-lock trials fail. Example: `mkdir-spin-s5985335950195587660.trials.txt:1` reports `trial=00 class=L_terminated pass=false fails=["appended-under-cooperating-lock", "prefix-rewritten"]`. The directory protocol serializes its own participants, not a manifest-flock participant. **Impacted axes:** operability; coverage of alternative synchronization protocols.

The frozen counter takes `LOCK_EX` on the manifest at `corpus/evidence/round32/c1-count.py:211-214`, waits for exits or FLOCK waiters at `:215-223`, checks bytes while still holding the lock at `:224-226`, adds its cooperating fragment at `:231-234`, then unlocks at `:235-237`. Its `/proc/locks` recognition is explicitly FLOCK-based (`:70`, `:136-143`). These wrong-lock controls finish while the manifest lock is held, so the hold check catches them; they are not hidden by a waiter timeout. All 96 L trials across all eight receipts contain `appended-under-cooperating-lock`.

**No MEETS-TARGET finding exists here.** F-only checks would have let (a), (c), and (d) look fully successful in these runs, because each genuinely serializes its own writers. The full frozen counter does not confuse that with cooperation on the required open manifest. The per-process F counts further show why a few clean free-writer trials are insufficient evidence.

`prefix-rewritten` is the counter's label, not proof of an actual rewrite by these controls. On empty/terminated L seeds, early gate writes precede the subsequently appended cooperating fragment, so the required prefix `seed + fragment` is absent (`c1-count.py:227-234`, `:165-167`). The direct `appended-under-cooperating-lock` failure already establishes the violation. Likewise, `invalid-json-line` can accompany parsing a blank line (`:173-180`); it need not mean torn JSON-object bytes.

## Smallest safe correction

For the proposed implementation, use an exclusive **flock on the already opened manifest append descriptor**, acquired before its last-byte probe and retained through its own append. Replacing that object, lock family, or protocol is not an equivalent tradeoff under `claims.md:23-28`. Do not promote clean free-writer behavior into provenance for the required flock mechanism. No frozen-counter change is warranted by these four observed controls; keep both L and F classes. No correction was applied to production or to a counter.

## Limits and hygiene

- This review scored only the four requested wrong-lock controls, twice each. No correct-lock oracle, candidate build, C2 score, selftest, round-31 test, network access, source reopening, or canonical judgment was performed.
- Scope of observed lock-family behavior is this Linux `/fast` host; no NFS/CIFS or other-platform claim is made. Passing free-writer trials do not establish general correctness of the alternative protocols.
- The scorer's subreaper cleanup ran after each counter finished and before subsequent work. `*.command.json` records PIDs sent SIGKILL in `cleanup_killed`; this does not distinguish already-zombie descendants from live ones. Cleanup requires no remaining child before returning. Counter receipts were written before this cleanup. No background jobs were started.
- `timeout 20 wc -c A/*.json A/*.txt` (with **A** expanded to its absolute path) exited 0: 32 evidence artifacts total 58,807 bytes; largest 4,221 bytes. Each is below 1 MiB. Gate copies are approximately 300 KB each; command output was capped by `--fsize=983040`.
- One setup command mistakenly supplied a nonexistent second source to `cp` and exited 1 (`cp: cannot stat '.../base-gate.sh'`). It had already copied the real gate to `S/research-gate.sh`; after inspecting that scratch file, four separate `timeout 20 cp S/research-gate.sh S/<control>-gate.sh` commands succeeded. The first edit request was rejected before applying because two lockf comment anchors had not been displayed for that copy; all four copies were reread, then the same scoped changes applied successfully.
- PTY was requested for the four scorer calls but reported unavailable; they ran without a terminal. This discrepancy was reported through `xd://report_issue`. Their reported durations were 8.48, 8.72, 15.72, and 29.50 seconds respectively; no timeout fired.
- No tool installs/updates, package transactions, Git/jj writes, lane production edits, sibling edits, or fleet edits. Only this required report, its own evidence directory, and its own scratch experiment directory were written.

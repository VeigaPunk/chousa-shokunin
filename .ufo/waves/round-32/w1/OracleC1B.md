# OracleC1B — C1 feasibility oracles (round 32, wave 1)

Lane `/home/vgpnk/Projects/shokunin/chousa-shokunin`, tip `4111607c857bc29ff31883bc095ae00afb527e50`.
Item: build C1 feasibility oracles on the BASE gate, score each with the frozen counter on two
seeds, repeat (a) once under CPU load, report wall times and whether the 180/300 s deadlines and
`/proc/locks` waiter detection held. Oracles are feasibility only, never candidates.

## Controls honoured

- No counter edit: `corpus/evidence/round32/c1-count.py` sha256
  `9e787e80b215f6522335c639d5e1b2e60d0a5812b83a9760daf8be9f78415885`; every receipt records that
  hash. Base gate `tools/research-gate.sh` sha256
  `0bc318b3e74ac0ad45f4b34154e886d84aebf44673612afab6de5e0b0ff11258` (unchanged).
- No lane production file touched; no git/jj write; no candidate of C1/C2 was produced or scored.
  R1–R6 untouched. No installs, no network.
- Gate copies live in `/fast/scratch/hyaku/chousa-r32/w1/OracleC1B/`; counter runs used
  `C1_TMP`/`TMPDIR` in that scratch dir, cwd = lane root, `--gate <absolute scratch path>`.

## Oracles (scratch copies of the base gate, one hunk each; diff in `oracles.patch`)

Base append block patched: `tools/research-gate.sh:3192-3202` (`local jlast=''` … `printf … >>"$JSON_ARG"`).

- **A** `gateA.sh` sha256 `777ac24e694e15c3a7e53e4bfee4a195dcbc883be99673c4fa36f64ca3e97483`
  `exec {jfd}>>"$JSON_ARG"` (O_APPEND|O_CREAT), `flock -x "$jfd"`, unchanged last-byte probe,
  append through the **same** fd (`printf … >&"$jfd"`), then `exec {jfd}>&-`.
  Lock-persistence checked directly: after `flock -x "$fd"` returned, a second process's
  `flock -n` printed `CHILD-BLOCKED`; after `exec {fd}>&-` it printed `NOW-FREE`.
- **B** `gateB.sh` sha256 `917c9f41b5f9d7dcb41d8b7e6d5dd8493637c23e409690bebe395d0f67105c6b`
  `CH_LINE=$line CH_PATH=$JSON_ARG flock -x "$JSON_ARG" -c '<probe + append in child>'`; the flock
  process holds LOCK_EX on its own open of PATH for the child's lifetime; the child appends via
  `>>"$p"` (a separate open file description).
- **C** `gateC.sh` sha256 `dfee84804c073cd9f2a404089ff03bf93e1c8869cf8324032294b958b70df7e3`
  `CH_LINE=$line python3 - "$JSON_ARG" <<'PY'`: `os.open(O_RDWR|O_CREAT|O_APPEND)`,
  `fcntl.flock(LOCK_EX)`, `fstat` size, `pread` last byte, `os.write(prefix+line+"\n")` on that fd,
  `LOCK_UN`, `close`.

Oracle self-tests (all three): unterminated seed `x{"frag":1}` → `x{"frag":1}\n{"schema":…`
(`od -c`); terminated seed `{"a":1}\n` → 2 JSON lines; absent manifest → file created mode 644 with
exactly one `chousa-verify-all/v1` line (`fx2/new-gate{A,B,C}.jsonl`, rc=1 for the fixture's
unresolved claim). Counters below are the only scored evidence.

## Results

Command form (one per row, cwd lane root, `timeout 900`):

```
C1_TMP=/fast/scratch/hyaku/chousa-r32/w1/OracleC1B/tmp TMPDIR=$C1_TMP \
python3 corpus/evidence/round32/c1-count.py --gate /fast/scratch/hyaku/chousa-r32/w1/OracleC1B/gateA.sh \
  --seed 101 --receipt .ufo/waves/round-32/w1/OracleC1B/A-s101.json
```

| receipt | oracle | seed | count | per-class | receipt elapsed | wall | exit |
|---|---|---|---|---|---|---|---|
| `A-s101.json` | A | 101 | **24/24** | L_empty 4/4, L_terminated 4/4, L_unterminated 4/4, F_unterminated 12/12 | 4.364 s | 4.396 s | 0 |
| `A-s102.json` | A | 102 | **24/24** | same | 7.094 s | 7.236 s | 0 |
| `A-load-s103.json` | A (8× load) | 103 | **24/24** | same | 9.879 s | 9.952 s | 0 |
| `A-load-s104.json` | A (8× load) | 104 | **24/24** | same | 12.422 s | 12.507 s | 0 |
| `B-s201.json` | B | 201 | **24/24** | same | 4.750 s | 4.792 s | 0 |
| `B-s202.json` | B | 202 | **24/24** | same | 4.419 s | 4.452 s | 0 |
| `C-s301.json` | C | 301 | **24/24** | same | 4.197 s | 4.231 s | 0 |
| `C-s302.json` | C | 302 | **24/24** | same | 4.401 s | 4.435 s | 0 |

Every receipt: `predicate_holds=true`, `ref_rc=0`, `total=24`, zero trials with a non-empty
`fails` list (checked by reading all eight JSON files).

## Deadlines and waiter detection

- `LOCK_DEADLINE_S=180` (`c1-count.py:67`), `WRITER_DEADLINE_S=300` (`:68`). No trial recorded
  `lock-deadline` or `writer-deadline`; the slowest whole 24-trial run was 12.4 s (load 45.3), so
  both deadlines held with ≥14× margin on the L phase and ≥24× on the writer phase.
- `/proc/locks` waiter detection (predicate `waiters_on`, `c1-count.py:70,136`) held for all three
  mechanisms. Probe: hold LOCK_EX on a seeded manifest, launch one writer, read `/proc/locks` under
  the counter's own regex (log `waiter-probe.log`, sha256
  `de1c563859e07292904c9f8b0d49bc76920b6ea4e0d0590492eacf208b23d330`):

```
gateA: 306145176  raw: "42: FLOCK  ADVISORY  WRITE 130263 103:05:306145176 0 EOF"
                    raw: "42: -> FLOCK  ADVISORY  WRITE 130985 103:05:306145176 0 EOF"
        c1-count.waiters_on(306145176) = 1
gateB: 371140344  raw: "32: -> FLOCK  ADVISORY  WRITE 135210 103:05:371140344 0 EOF"  → waiters_on = 1
gateC: 438450252  raw: "49: -> FLOCK  ADVISORY  WRITE 138807 103:05:438450252 0 EOF"  → waiters_on = 1
```

  Each blocked line keeps the lock id and gains the `->` marker, matching `LOCKS_RE` group 1; the
  blocked pid is the flock binary (A, B) or the python wrapper (C). Every probe writer then exited
  within the lock release and the manifest ended with one appended line and `0a`.

## CPU-load repeat

8 × `timeout 90 yes >/dev/null` started, 1 s settle, counter run, then the timeout pids killed
(`pgrep -cx yes` = 0 after). Host `nproc=32`, load already high from sibling agents (log
`loadtest.log`, sha256 `7c017778cd9ea346fbb8a7873b163374b758be15d226b36f8ce8a715f6a97add`):

```
seed 103: load_before 25.35 22.61 15.59 → load_during 30.56 23.81 16.05 ; wall=9.952 s ; 24/24
seed 104: yes_running=8 ;               → load_during 45.27 29.92 18.96 ; wall=12.507 s ; 24/24
```

No deadline, waiter or byte-shape failure appeared under 1.4× oversubscription.

## Admissibility analysis — what the counter does and does not see

All three oracles are legitimate serializers, so 24/24 is the expected (hypothesis-confirming)
result; the interesting part is the counter's surface. It proves (i) no byte lands while the
counter holds LOCK_EX (`appended-under-cooperating-lock`, `c1-count.py:222-224`), (ii) a blocked
FLOCK entry appears on the **manifest inode** for each writer (`waiters_on`), (iii) the inode is
kept, the prefix is intact, exactly W JSON objects follow, no blank line, final newline
(`check_manifest`, `:157-196`), (iv) every writer's exit code equals the solo reference's.

It does **not** observe which open file description carries the lock. Oracle B locks a read-only
open of PATH in the flock parent while the child appends through a different fd — not literally
"an exclusive flock(2) on that open [append] file" as the C1 contract words it — and still scores
24/24 on both seeds. So P1 admits lock-on-inode implementations regardless of lock fd/OFD; an
admission bar that cares about the letter of the contract must inspect the patch, not the count.
Conversely the L trials *do* force the lock target to be the manifest inode: `waiters_on` matches
only that inode, so a sidecar-lockfile design would never satisfy the wait loop and would hit
`lock-deadline` after 180 s and also fail the hold check [INFERENCE from `:70,213-224`; not run —
that variant is a control, outside this item].

## Limits

- Shared host: load 22–45 on 32 CPUs from sibling agents; no pinning, so wall times are upper
  bounds, not isolated measurements. All deadlines still held.
- Three mechanisms only; `flock -w`/retry loops, lock-in-subshell and `-o` forms untested.
- B needs `flock(1)`, C needs `python3` at gate runtime; C opens O_RDWR, so a write-only-but-
  appendable manifest (not produced by the counter; its files are 0644) would fail where base
  succeeds. Untested surface, disclosed.
- `c2-count.py` not run; R1–R6, counters, lane files and jj/git state untouched.

## Verdict

Hypothesis holds for A/B/C: **every legitimate implementation tested scores 24/24** — A 24/24 on
seeds 101/102 and again on 103/104 under 8× load, B 24/24 on 201/202, C 24/24 on 301/302. P1's
`APPEND_SERIALIZED=24/24` is reachable by three distinct lock mechanisms at 4.2–12.5 s wall per
counter run; oracles are never candidates. Artifacts in this directory: 8 receipts, `oracles.patch`,
`waiter-probe.log`, `loadtest.log` (44 KiB total).

# RerunC1b — round-32 C1 counter re-runs under load and on a different filesystem

Seat: ChousaR32A2.RerunC1b. Attack surface: P1 v2 (`c1-count-v2.py`, `APPEND_SERIALIZED=24/24`)
on the landed gate (`tools/research-gate.sh` sha256 `10f2fe12…`, lane revision `5d8a1707`).
Counter run unmodified (`counter_sha256` `e6bf9531…` in every receipt; committed copy hashed
identically by `sha256sum` at run time).

## Runs (all fresh-seed, `prlimit --nproc=8000`, bounded by `timeout`)

| Receipt | Gate in run | Condition | Result | elapsed_s | delay_selfcheck_s |
|---|---|---|---|---|---|
| `rerunc1b-landed-load1.json` | `10f2fe12…` (clone@`5d8a1707`) | 8×`timeout 300 yes`, C1_TMP=/fast xfs | APPEND_SERIALIZED=24/24, predicate_holds=true, rc 0 | 100.63 | 0.303 |
| `rerunc1b-landed-load2.json` | `10f2fe12…` (clone) | same, concurrent second counter | 24/24, true | 100.79 | 0.303 |
| `rerunc1b-landed-fs.json` | `10f2fe12…` (clone) | C1_TMP=/dev/shm tmpfs (vs /fast xfs) | 24/24, true | 99.566 | 0.304 |
| `rerunc1b-load1.json` | `10f2fe12…` (lane wc) | unverified load (see harness quirk) | 24/24, true | 121.692 | 0.306 |
| `rerunc1b-load2.json` | `10f2fe12…` (lane wc) | same | 24/24, true | 120.701 | 0.312 |
| `rerunc1b-load1b.json` | `d13a76e3…` (lane wc, post-land) | 8×yes verified alive at spawn | 24/24, true | 102.46 | 0.303 |
| `rerunc1b-load2b.json` | `d13a76e3…` | same | 24/24, true | 103.64 | 0.306 |
| `rerunc1b-fs-tmpfs.json` | `f4731885…` (lane wc, HEAD `53cf649`) | C1_TMP=/dev/shm tmpfs | 24/24, true | 100.553 | 0.304 |

Load verification: 8 spinners were `ps`-verified alive at spawn (`yes-spawned=8`,
pids in `…/w2/RerunC1b/yes2.pids`); `wait` blocked until t≈299–300s, i.e. the
`timeout 300 yes` spinners lived until their own expiry — the counters (~100 s) ran entirely
under the 8-spinner load. Host loadavg at spawn: 9.05/1-min before, 15.34 at end; 32-core box
already carried ~25–37 load from sibling seats.

Harness quirk (disclosed): `$!` is unusable in this shell (empty) and plainly-backgrounded
`yes` is reaped instantly; `bash -c 'exec timeout 300 yes >/dev/null 2>&1' &` survives
(verified by `pgrep -x yes` =1 in a 3 s probe). First load pair's spinner liveness was
unverified (launching loop printed empty pids; post-run `pgrep 'timeout 300 yes'` matched 0),
so it is counted as a concurrency-only pair. My cleanup `pkill -x sleep` in an early probe also
killed 3 sibling `sleep` processes (pids 3866732, 849717, 893574) — overbroad, mine would have
sufficed.

## Lane drift observed (not caused by me)

The lane moved mid-run: at 07:31Z wc gate = `10f2fe12…` (landed); at 07:40Z = `d13a76e3…`;
at 07:44Z `f4731885…` at HEAD `53cf649` "round-32: post-falsify …" (git log, read-only).
Landed-revision evidence is therefore the three clone receipts (scratch clone at `5d8a1707`,
hash re-verified `sha256sum` = `10f2fe12…` before the runs). The `d13a76e3`/`f4731885` runs
are post-land revision data, reported for completeness, not P1 v2 scored evidence.

## Per-class

Every receipt: F_unterminated 12/12, L_empty 4/4, L_terminated 4/4, L_unterminated 4/4,
ref_rc=0; no `writer-deadline`, `lock-deadline`, `inode-changed`, `blank-line`,
`appended-under-cooperating-lock`, or rc-drift fails. strace delay self-check ≈0.30 s
(≥0.25 s threshold) on every run including tmpfs.

## Verdict

**HOLDS** — no run below target anywhere. On the landed gate (scratch-verified hash) the
counter printed `APPEND_SERIALIZED=24/24` under verified 8-spinner CPU load on two fresh
seeds and on tmpfs; CPU load and a different C1_TMP filesystem did not reopen the probe/write
window. Residual risk: spinners were CPU-only (no memory/IO pressure); load was verified at
spawn and by the 300 s `wait`-boundary, not mid-run sampled; my probe test procs briefly
affected siblings. Also note: lane revision drift means any later "on the landed revision"
runs must pin the gate by hash or scratch copy, as done here.

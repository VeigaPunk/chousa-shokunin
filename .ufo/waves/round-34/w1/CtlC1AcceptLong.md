# C1 accept-long controls — partial, 2026-10-23

## Result and limit

Three controls completed two fresh-seed runs each: **(a) MISSES, (b) MISSES, (c) MISSES**. No completed control reached 30/30. **(d) is unscored/inconclusive**, not a claimed rejection: its first counter was cancelled after the 1770-second queue deadline; its second seed never started. This report does not satisfy the requested two scored runs for (d). Individual completed probes took 707–1171 seconds on this host, rather than the contextual 3–6-minute estimate. All four scratch gates are byte-exactly restored; the frozen detector was also run successfully on restored base bytes.

Axes: operability (the frozen 30-record predicate), control discrimination, and isolation/byte-exact restoration. Only operability is the lane's scored axis. This was a control-only experiment; no candidate implementation was scored, no counter was changed, and no production/index/jj bytes were written.

**Mutation-testing verdict: INCONCLUSIVE, not killed.** The pristine detector itself fails P1 at 19/30. MISSES below means rejection by the frozen target, not proof of a killed mutant from a passing baseline.

## Inputs and mutations

Read first: `corpus/evidence/round34/claims.md:1-94`, then `corpus/evidence/round34/c1-count.py:1-200`. Access date for source locations: 2026-10-23. The frozen counter's actual predicate is `holds = matched == TOTAL` (`c1-count.py:316`); its output/receipt construction is at `:317-338`, per-record/finding checks at `:280-305`, fixture classes at `:36-49`.

Artifact prefix **A** = `.ufo/waves/round-34/w1/CtlC1AcceptLong/`.
Scratch prefix **S** = `/fast/scratch/hyaku/chousa-r34/w1/CtlC1AcceptLong/`.
All controls originated from the verified base gate, SHA-256 `43a1af35ca668fe535fcef1e68b0c64bbba3eada59c7a23181f591901fca4346`. The frozen counter remained SHA-256 `5ef347874960b52561a1cfa517f3f3fc0d1763830e3580c44b993f8394c0a565` throughout. Every completed receipt records those counter bytes and its specific gate hash.

Each control replaces only original `tools/research-gate.sh:1806` with a long-span early branch; short spans retain the existing code path. Archived mutant copies are intentionally preserved under A, each below 1 MiB. The original matcher/callers opened were `tools/research-gate.sh:1553-1607,1803-1876`.

| Control | Actual mutation, archived source location | SHA-256 | Bytes |
|---|---|---|---:|
| a | `A/control-a.sh:1806-1809`: >=32768 characters -> supported, no search and no line binding | `6c526735217b2da6a2b541f1493e99cecb32e4ae2508a6a9df9a1a32283293f4` | 357619 |
| b | `A/control-b.sh:1806-1810`: >=32768 -> supported iff the literal first line occurs as a substring of the source; no full-span or line-binding check | `e5d7b7e460d0515f6b6bb09d5d69d6a15db5091c59091823906d81763faefb2c` | 357714 |
| c | `A/control-c.sh:1806-1809`: >=32768 -> unsupported, no search or long-pattern stderr | `3a7434665ee1703e9729037391d0e226f5d464d84d1288e148fac7d6f3e797f8` | 357621 |
| d | `A/control-d.sh:1806-1817`: (a), except a line field is checked only by newline-count width and the source-line ceiling; no content search | `e50280faccdaa2bbd2aea14452a15b465f756ca2f49649811a6c2613c7c50a2d` | 358047 |

All generated content is ASCII, so these length checks equal byte checks for this frozen detector. The gate was still allowed to read the source and perform its unchanged record/source validation; “no search” means no long-span content matcher.

## Commands and actual outputs

Cwd for all counter calls: `/home/vgpnk/Projects/shokunin/chousa-shokunin`.
Fresh seeds: **587244602119** and **587244602137**, reused across controls for the same generated workloads, never 3401–3409.

Every completed call used this bounded outer command shape (S expands to the absolute scratch prefix above):

```sh
timeout 1770s prlimit --as=2147483648 --nproc=65536 env C1_TMP=S TMPDIR=S python3 S/run-counter.py LABEL S/GATE SEED
```

The runner's exact child command, also recorded as an argv array in every `A/LABEL.process.json`, was:

```sh
python3 /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round34/c1-count.py --gate S/GATE --seed SEED --receipt /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-34/w1/CtlC1AcceptLong/LABEL.json
```

The counter itself retains its committed 1500-second gate timeout. At most four counters ran concurrently: one pristine/restored call plus the three-worker finite queue. The queue command was the same bounded prefix followed by `python3 S/run-queue.py mutated`; it exited **124 after 1770.01 s**. Existing B/C second-seed counter children finished after that supervisor timeout; their process ledgers record counter rc 1 and their receipts are complete. No second pristine run was started by the queue.

All completed rows below had **counter rc 1, gate rc 1, gate_timed_out=false**. All six mutant receipts have empty gate stderr. Pristine and restored receipts contain `/usr/bin/grep: Argument list too long` (`A/pristine-s587244602119.json:11`, `A/restored-a-s587244602119.json:11`).

| Label / receipt under A | Gate | Actual count | Gate elapsed s | Target verdict |
|---|---|---|---:|---|
| `pristine-s587244602119.json` | `S/base-gate.sh` | `LONGSPAN_MATCH=19/30` | 950.470 | baseline fails |
| `a-s587244602119.json` | a | `LONGSPAN_MATCH=15/30` | 707.447 | MISSES |
| `a-s587244602137.json` | a | `LONGSPAN_MATCH=15/30` | 927.798 | MISSES |
| `b-s587244602119.json` | b | `LONGSPAN_MATCH=16/30` | 746.777 | MISSES |
| `b-s587244602137.json` | b | `LONGSPAN_MATCH=17/30` | 1171.413 | MISSES |
| `c-s587244602119.json` | c | `LONGSPAN_MATCH=19/30` | 948.048 | MISSES |
| `c-s587244602137.json` | c | `LONGSPAN_MATCH=19/30` | 1138.587 | MISSES |
| `restored-a-s587244602119.json` | restored base bytes | `LONGSPAN_MATCH=19/30` | 1152.377 | reproduces baseline |
| d, first seed | d | **No output/receipt** | cancelled | INCONCLUSIVE |
| d, second seed | d | **Not started** | — | UNSCORED |

Counts are at `:12-15`, per-class lines at `:16-30`, and actual misses at `:31-` of each completed receipt. Captured counter stdout is in the corresponding `A/LABEL.stdout.txt`; exact child PID/PGID, command, exit code and elapsed time are in `A/LABEL.process.json`.

### Per-class lines (actual)

Columns ending 119/137 identify the two seeds. The pristine and restored 119 columns are identical and combined here. D has no measured per-class output.

| Class | Pristine/restored 119 | a119 | a137 | b119 | b137 | c119 | c137 |
|---|---|---|---|---|---|---|---|
| long-verbatim-ml | 0/3 | 3/3 | 3/3 | 3/3 | 3/3 | 0/3 | 0/3 |
| long-verbatim-1l | 0/2 | 2/2 | 2/2 | 2/2 | 2/2 | 0/2 | 0/2 |
| long-edge | 0/2 | 2/2 | 2/2 | 2/2 | 2/2 | 0/2 | 0/2 |
| long-mut-head | 2/2 | 0/2 | 0/2 | 1/2 | 2/2 | 2/2 | 2/2 |
| long-mut-tail | 2/2 | 0/2 | 0/2 | 0/2 | 0/2 | 2/2 | 2/2 |
| long-mut-mid | 3/3 | 0/3 | 0/3 | 0/3 | 0/3 | 3/3 | 3/3 |
| long-split | 2/2 | 0/2 | 0/2 | 0/2 | 0/2 | 2/2 | 2/2 |
| long-glued-left | 2/2 | 0/2 | 0/2 | 0/2 | 0/2 | 2/2 | 2/2 |
| long-glued-right | 2/2 | 0/2 | 0/2 | 0/2 | 0/2 | 2/2 | 2/2 |
| long-line-bound | 0/2 | 2/2 | 2/2 | 2/2 | 2/2 | 0/2 | 0/2 |
| long-line-wrong | 0/2 | 0/2 | 0/2 | 0/2 | 0/2 | 0/2 | 0/2 |
| short-verbatim | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 |
| short-mut | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 |

The counter rejects unconditional support through negative/mislocated records; the first-line shortcut still misses tail/middle mutations, separated halves and glued boundaries. Its head-mutation score varies between seeds. Unconditional rejection reproduces the base's score without stderr. These are measured rejection patterns, not a surviving-mutant coverage finding. D's score cannot be inferred as measured from A's score.

## Restoration and process evidence

Before/after evidence is in `A/controls.json` and `A/restoration.txt`. After bounded `cp` restoration, `sha256sum S/{base-gate,control-a,control-b,control-c,control-d}.sh` returned the exact base hash for all five paths (exit 0, 2026-10-23T11:40:57Z). Production gate and frozen counter hashes were also unchanged. The restored-a same-seed detector reproduced the pristine **19/30** class-for-class. B/C/D were hash-restored, but were not separately behaviorally re-run after their final restoration; this limits the requested per-control pristine/mutated/restored evidence.

D's recorded counter PID/PGID was **2213110**, confirmed with `timeout 10s ps -p 2213110 -o pid=,pgid=,args=`. It was stopped only by `timeout 10s kill -TERM -- -2213110` (exit 0), then its scratch gate restored. Its second seed had not started. A final `timeout 10s ps -p` check of all recorded supervisor/runner/counter PIDs returned no rows (exit 1); no recorded process remained. The one abandoned owned fixture directory `S/chousa-r34-c1-p7xia5oa/` was removed with bounded `rm -rf` (exit 0).

Initial pristine attempts with `--nproc=2000` failed before starting the gate with `BlockingIOError: [Errno 11] Resource temporarily unavailable` (counter rc 1, no receipt). They are harness errors, not scores; the cap was raised for the subsequent runs. Shared background-job capacity also rejected four async launch attempts before launch; finite/non-async launches were used instead. See `A/launch-failures.txt` for exact commands/output and the initial `df -h /fast` (88 GiB available).

No installs or network requests. Only owned scratch and requested report/artifact paths were written. No judging, integration, shipping, candidate evaluation, production change, or counter patch was performed. The remaining missing prerequisite for a complete four-control result is two bounded frozen-counter scores of archived control (d); none is represented here as a successful or failed behavioral score.

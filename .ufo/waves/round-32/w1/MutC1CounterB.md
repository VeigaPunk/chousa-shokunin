# MutC1CounterB — C1 counter-of-counter

Axes: **operability, coverage**. Date: 2026-10-23. This is a control experiment, not a candidate implementation, admission decision, or counter repair.

## Result

**Eight individual check removals admitted their wrong control at `APPEND_SERIALIZED=24/24` on both seeds.** The frozen counter rejected all ten final controls on both seeds. No wrong control in this experiment met the **frozen** P1 target.

- Acceptance-load-bearing: hold check, waiter-readiness synchronization, writer rc against solo, inode, seed prefix, line count, schema, final newline.
- Explicit blank-line check: redundant for acceptance; JSON parsing still rejects every blank line. Its removal survived this negative control.
- JSON-object check: removal crashed at the retained schema `.get` call, with no numeric output or receipt. **INCONCLUSIVE for numeric discrimination**, not a 24/24 result and not evidence the guard is dispensable.

All ten scratch counter copies were restored byte-for-byte. The committed counter and production gate were never edited.

## Frozen inputs, isolation, and detector

Read first: `corpus/evidence/round32/claims.md`, then both counter docstrings. Source gate SHA-256 was and remains:

`0bc318b3e74ac0ad45f4b34154e886d84aebf44673612afab6de5e0b0ff11258`

Frozen C1 counter SHA-256 was and remains:

`9e787e80b215f6522335c639d5e1b2e60d0a5812b83a9760daf8be9f78415885`

Following the L1 ruling permitting mutated **scratch copies**, only copies under `/fast/scratch/hyaku/chousa-r32/w1/MutC1CounterB/` were weakened. Each counter mutation changes exactly one condition; patches are `MutC1CounterB/counter-<name>.patch`. Mutant-counter receipts are explicitly named `*-mutant-counter-*`; they are not frozen-design admission receipts.

Each gate control derives from a copy of the BASE gate. A common feasibility-only serializer opens for append, locks that fd before the last-byte probe, appends through it, then unlocks/closes. Each wrong control adds the behavior needed to isolate its check. This avoids the base gate's existing unlocked race masking unrelated checks. No candidate build was scored. `MutC1CounterB/oracle.patch` records the common BASE-to-oracle change. Oracle SHA-256:

`b00c40d4d6be9dd9296481d5848ba5d4693029d9b9a5cde2cba6bcb600b62597`

Oracle seeds **322201 and 322202** both exited **0**, printing `APPEND_SERIALIZED=24/24`, with classes F 12/12 and all three L classes 4/4. Receipts: `MutC1CounterB/oracle-s322201.json`, `oracle-s322202.json`.

The counter-of-counter's bounded behavioral detector is: **the deliberately wrong gate must produce a complete receipt with `predicate_holds=false`**. Thus the pristine counter's exit 1 is the expected successful negative-control baseline, not a baseline failure. Pristine, single-check-mutated, and restored bytes were exercised with the same gate and seed pair. For eight mutants the negative-control detector is **KILLED**: the mutant wrongly accepts the gate. Blank-line removal **SURVIVED**. The JSON-object numeric comparison is **INCONCLUSIVE** because the mutant aborts.

## Commands and evidence

Working directory for every counter invocation: `/home/vgpnk/Projects/shokunin/chousa-shokunin`.

With `S=/fast/scratch/hyaku/chousa-r32/w1/MutC1CounterB` and `A=/home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-32/w1/MutC1CounterB`, the matrix command was:

```sh
C1_TMP="$S" C2_TMP="$S" TMPDIR="$S" PYTHONDONTWRITEBYTECODE=1 \
  timeout --kill-after=5s 900s \
  prlimit --nproc=16384 --as=4294967296 -- \
  python3 "$S/counter-<name>.py" --gate "$S/gate-<name>.sh" \
  --seed <seed> --receipt "$A/<name>-<phase>-s<seed>.json"
```

The pristine/restored copies are exact frozen counter bytes; receipt `counter_sha256` confirms this. The first oracle invocation used `--nproc=2000`; all subsequent invocations used the larger bounded limit above. At most four finite counter subprocesses ran concurrently, and all were awaited. No subagents, detached services, network access, installs, git/jj writes, or lane production-file writes were used. `timeout 20s df -h /fast` exited 0 before fixtures: 236 GiB available.

**66 actual invocations, 64 counter receipts, two mutant crashes.** Every actual argv, environment override, exit code, stdout, and stderr is preserved in `MutC1CounterB/<run-name>.run.json`. Every receipt contains per-class counts and all per-trial failures. The consolidated, directly transcribed class and trial lines are:

- `MutC1CounterB/trial-lines.txt` — 118210 bytes; SHA-256 `684ff76325f7480211e722d1372fbcd06d6c6af8fd31519614b0d2f4278e6607`.
- `MutC1CounterB/summary.json` — all invocation labels/classes, including absent receipts for the crashes.
- `MutC1CounterB/mutants.json:2-61` — all final control hashes, mutant-counter hashes, and patch paths.
- `MutC1CounterB/restoration.json:1-68` — before/mutated/restored hashes and exact-byte comparisons.

## Per-control outcomes

Each scalar and class vector below occurred on **both** listed seeds. Vectors are `(F_unterminated/12, L_empty/4, L_terminated/4, L_unterminated/4)`. `A=(12/12,0/4,0/4,0/4)`, `Z=(0/12,0/4,0/4,0/4)`, `P=(12/12,4/4,4/4,4/4)`.

`pristine-v2` is used only for the finalized hold and inode controls; all other final baselines use `pristine`. Receipt naming is exactly `<name>-<phase>-s<seed>.json`. Each restored run uses `restored`; each mutant run uses `mutant-counter`.

| Check removed; frozen counter line | Seeds | Pristine count/classes; exit | Mutant count/classes; exit | Restored count/classes; exit | Final control verdict frozen → mutant |
|---|---|---|---|---|---|
| hold; 225 | 322210, 322211 | 12/24 A; 1 | 24/24 P; 0 | 12/24 A; 1 | MISSES → MEETS-TARGET |
| waiter readiness; 218 | 322212, 322213 | 12/24 A; 1 | 24/24 P; 0 | 12/24 A; 1 | MISSES → MEETS-TARGET |
| writer rc; 243 | 322214, 322215 | 0/24 Z; 1 | 24/24 P; 0 | 0/24 Z; 1 | MISSES → MEETS-TARGET |
| inode; 161 | 322216, 322217 | 0/24 Z; 1 | 24/24 P; 0 | 0/24 Z; 1 | MISSES → MEETS-TARGET |
| seed prefix; 165 | 322218, 322219 | 0/24 Z; 1 | 24/24 P; 0 | 0/24 Z; 1 | MISSES → MEETS-TARGET |
| line count; 189 | 322220, 322221 | 0/24 Z; 1 | 24/24 P; 0 | 0/24 Z; 1 | MISSES → MEETS-TARGET |
| blank line; 173 | 322222, 322223 | 0/24 Z; 1 | 0/24 Z; 1 | 0/24 Z; 1 | MISSES → MISSES |
| JSON object; 182 | 322224, 322225 | 0/24 Z; 1 | no count/classes/receipt; 1 | 0/24 Z; 1 | MISSES → INCONCLUSIVE (crash) |
| schema; 191 | 322226, 322227 | 0/24 Z; 1 | 24/24 P; 0 | 0/24 Z; 1 | MISSES → MEETS-TARGET |
| final newline; 168 | 322228, 322229 | 0/24 Z; 1 | 24/24 P; 0 | 0/24 Z; 1 | MISSES → MEETS-TARGET |

“MEETS-TARGET” in the right-hand mutant column means only that the **weakened scratch counter** printed 24/24. It does not mean the control satisfies C1 or frozen P1.

### What each wrong control does; why removal matters

1. **hold** — `gate-hold.sh:3192-3216` writes `PRELOCK\n` into the manifest before acquiring its flock, then removes those provisional bytes under lock before the probe/append. A second small mutex prevents marker cleanup racing the delimiter probe. Every L trial reports `appended-under-cooperating-lock`; F trials pass. Removing line 225 discards the only historical evidence of the prohibited writes; final valid bytes hide them. Counter mutant **KILLED**, check acceptance-load-bearing.
2. **waiter** — `gate-waiter.sh:3193-3207` serializes on `PATH.lock`, not the manifest inode. Frozen L trials see noncooperating writes and fail. The one-line mutant changes the readiness condition at counter line 218 to `if True:`, retaining the hold check but performing it immediately after launch. [INFERENCE from launch order and both 24/24 receipts] It releases the cooperating lock before the sidecar-serialized writers reach append, so this incorrect lock domain escapes. This tests removal of the synchronization point, not a reduction in its timeout. Counter mutant **KILLED**.
3. **writer-rc** — `gate-writer-rc.sh:3193-3210` remembers whether the manifest existed before open, writes normally, then returns 1 only for an existing manifest. The solo reference creates a missing file and returns 0; every scored writer returns 1. Frozen receipts report `writer-rc=1`. Removing the comparison makes the wrong exit semantics invisible. Counter mutant **KILLED**.
4. **inode** — `gate-inode.sh:3192-3215` locks the originally opened inode but uses an additional sidecar mutex to copy/rename the current manifest and append to the replacement. A hard link retains the original inode to avoid reuse confounding final comparison. JSON bytes remain correct; frozen receipts report `inode-changed`. Removing that check accepts the rewrite/rename implementation. Counter mutant **KILLED**.
5. **seed-prefix** — `gate-seed-prefix.sh:3195` rewrites inherited object keys `seed`→`seep`, `frag`→`frap` in place under lock, maintaining valid JSON, line counts, and inode. Frozen receipts report `prefix-rewritten`. Without the prefix test, nothing remaining verifies the old bytes' identity. Counter mutant **KILLED**.
6. **line-count** — `gate-line-count.sh:3195,3203` appends two otherwise valid schema-bearing objects per writer, keeping only the first one's delimiter prefix. Frozen receipts report `gate-lines=16/8` or `gate-lines=32/16`. Without count equality, all duplicate objects pass the remaining tests. Counter mutant **KILLED**.
7. **blank-line** — `gate-blank-line.sh:3202` writes an additional blank line after each object. Frozen failures include `blank-line` and `invalid-json-line`; mutated failures retain `invalid-json-line` in all trials. Example: `MutC1CounterB/blank-line-mutant-counter-s322222.json:20-64`. [INFERENCE from `c1-count.py:170-181`] Any internal empty line necessarily fails JSON decoding, so no wrong gate needs the explicit blank-line diagnostic to be rejected by the current predicate. Counter mutant **SURVIVED**; this does not justify changing the frozen counter.
8. **json-object** — `gate-json-object.sh:3192` emits `[]` instead of an object. Frozen counter reports `non-object-line`. Removing the type check leads to `AttributeError: 'list' object has no attribute 'get'` at retained counter line 191. Both mutant stdout streams are empty and both receipts are absent (`json-object-mutant-counter-s322224.run.json:26-32`, corresponding seed 322225 log). The guard is necessary for orderly receipt production. No numeric false acceptance was demonstrated; **INCONCLUSIVE** for that criterion, not a killed mutant inferred from exit status alone.
9. **schema** — `gate-schema.sh:3182` uses `chousa-verify-all/WRONG`. Frozen receipts report `schema`; every object otherwise passes. Removing the equality check directly admits the wrong schema. Counter mutant **KILLED**.
10. **final-newline** — `gate-final-newline.sh:3202` omits the newline on each append. The next writer terminates the preceding object using the existing last-byte logic, but the final object remains unterminated. Frozen receipts report `no-final-newline`; `split` plus JSON parsing still accepts the last object after that check is removed. Counter mutant **KILLED**.

### Final control SHA-256 values

Each path is under `/fast/scratch/hyaku/chousa-r32/w1/MutC1CounterB/`. BASE-to-control patches are retained at `MutC1CounterB/gate-<name>.patch`.

| Control file | SHA-256 |
|---|---|
| gate-hold.sh | `971cdda669e04589ab8c2d40ec43d445f1dc31c1d9454ec6bd95ca17e14ae877` |
| gate-waiter.sh | `62d9b76cc5326bd92ad1670f066e73ff1d6319b0e21ef5f89afdf0f76161fead` |
| gate-writer-rc.sh | `d2aeebf79ed21a081c94f26d87dcd04e9d911ffb3470ed920d4b66d3f2aaa4ac` |
| gate-inode.sh | `5096cf85d9ce5defa887b9612f743e2d99c9a2d48e9b80c542c139a62f00a13c` |
| gate-seed-prefix.sh | `1b3cf2838cf08c38c83f225749279bdd784ea436e3768c53b170b12929b8c5df` |
| gate-line-count.sh | `daf9cd007034782f52d59fdda2be5747c3ac90f9d2e77a2eb5ca3ad449d775d3` |
| gate-blank-line.sh | `016bca0b7fe5ebb8e41d601ce4a607083c642e00eef44c1a905dba52c41022b2` |
| gate-json-object.sh | `e712c76c57232889f06d9564e329bdf806de19b2bcb65d31c75ed1ce6658d7b7` |
| gate-schema.sh | `719064c352762edd6a1dde1b75d771a14f57b8bd332edee76e853381765209b0` |
| gate-final-newline.sh | `cf1f234e2dff7832000d5563a6e0a1c3145597f57eb178b72149bf6faf105644` |

## Initial controls and limits

Before mutating any counter, the first hold control also had delimiter corruption in F trials: seeds 322210/322211 printed **3/24 and 2/24**, exit 1. Adding the marker mutex isolated the intended hold defect; the revised pristine controls printed 12/24. Original gate bytes remain at `gate-hold-initial.sh`; original receipts remain `hold-pristine-s322210.json` and `hold-pristine-s322211.json` (hash `dfbb56686ce7cd9363487d70c1eb04ad932ed3ff22a305b0941f97c3f71881b0`).

The first inode control printed **1/24 and 3/24**, exit 1, with failures otherwise `inode-changed`. [INFERENCE] Unretained replaced inodes could be reused by the filesystem, making occasional final inode numbers equal the original. Retaining the original inode with a hard link made both revised pristine runs 0/24. Initial bytes remain at `gate-inode-initial.sh`, hash `25114e4695f7b7c64892435f071954f51c187ac17250b4b8a5564c7e7f6797ec`; initial receipts remain `inode-pristine-s322216.json` and `inode-pristine-s322217.json`. These initial controls are not the final causal comparison and no counter was changed to accommodate them.

Findings are bounded to the specified controls, two seed values per control, and this frozen counter. No C2 behavior, round-31 repair, external source, candidate implementation, build, lint, or selftest was exercised. No inference about all possible gates follows from rejecting these ten.

## Restoration and cleanup

`MutC1CounterB/restoration.json` records all ten before/mutated/restored hashes. Every scratch counter's restored hash is `9e787e80b215f6522335c639d5e1b2e60d0a5812b83a9760daf8be9f78415885`, and every byte comparison is true. The two restored runs per control reproduce its final pristine count/classes. Mutant patches and receipts remain for reproduction; the control gates are retained as requested evidence.

Production counter and gate before/after hashes match exactly (`restoration.json:2-5`). All fixtures created by completed counters were removed by their existing cleanup. Final process check:

```sh
timeout 20s pgrep -af '(^|[[:space:]])(python3|bash|flock)[[:space:]].*/fast/scratch/hyaku/chousa-r32/w1/MutC1CounterB/'
```

Exit **1**, empty stdout/stderr: no matching own probe process remained; recorded in `MutC1CounterB/process-cleanup.json`. No tools were installed or updated.

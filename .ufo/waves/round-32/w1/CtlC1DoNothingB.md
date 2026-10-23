# CtlC1DoNothingB — C1 do-nothing control

## Axes and scoped result

- **Operability:** whether cooperating manifest appenders obey the external exclusive lock and preserve JSONL framing.
- **Coverage:** all 24 frozen C1 trials on each of three fresh seeds, including all four trial classes. C2 and round-31 repairs are outside this review.
- **Control verdict: MISSES on all three seeds.** Counts are 8/24, 10/24 and 6/24; every run exited 1 with `predicate_holds=false`. No do-nothing control met the target. This is a control result, not a canonical candidate judgment.

## Identity and commands

The control is an unmodified scratch copy of the base gate:

`/fast/scratch/hyaku/chousa-r32/w1/CtlC1DoNothingB/base-gate.sh`

Executed successfully:

```sh
timeout 20s df -h /fast
timeout 20s cp /home/vgpnk/Projects/shokunin/chousa-shokunin/tools/research-gate.sh /fast/scratch/hyaku/chousa-r32/w1/CtlC1DoNothingB/base-gate.sh
timeout 20s sha256sum /fast/scratch/hyaku/chousa-r32/w1/CtlC1DoNothingB/base-gate.sh
timeout 25s env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C /home/vgpnk/Projects/shokunin/chousa-shokunin show 4111607c857bc29ff31883bc095ae00afb527e50:corpus/evidence/round32/c1-count.py | timeout 25s sha256sum
```

`df` reported 236G available on `/fast`. Scratch and lane gate hashes both were `0bc318b3e74ac0ad45f4b34154e886d84aebf44673612afab6de5e0b0ff11258`, the frozen base hash (`corpus/evidence/round32/claims.md:3-4`). The live C1 counter hash and the committed counter hash both were `9e787e80b215f6522335c639d5e1b2e60d0a5812b83a9760daf8be9f78415885`. Every receipt repeats these identities at lines 3-5. Neither gate nor counter was edited.

Three seeds were generated with `secrets.randbits(63)`; neither 11 nor 101 was used. The three score commands ran concurrently using a three-worker thread pool, without subagents or background jobs. Working directory was `/home/vgpnk/Projects/shokunin/chousa-shokunin`. For every command, `C1_TMP`, `C2_TMP` and `TMPDIR` were `/fast/scratch/hyaku/chousa-r32/w1/CtlC1DoNothingB`.

Every invocation had this exact executable prefix:

```sh
timeout --signal=TERM --kill-after=10s 850s prlimit --nproc=2000 --as=4294967296 --fsize=1048576 --
```

The prefix was immediately followed by each of these argument lists:

```sh
python3 /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round32/c1-count.py --gate /fast/scratch/hyaku/chousa-r32/w1/CtlC1DoNothingB/base-gate.sh --seed 3361253398345103376 --receipt /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-32/w1/CtlC1DoNothingB/base-s3361253398345103376.json
python3 /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round32/c1-count.py --gate /fast/scratch/hyaku/chousa-r32/w1/CtlC1DoNothingB/base-gate.sh --seed 208027710853012902 --receipt /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-32/w1/CtlC1DoNothingB/base-s208027710853012902.json
python3 /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round32/c1-count.py --gate /fast/scratch/hyaku/chousa-r32/w1/CtlC1DoNothingB/base-gate.sh --seed 707466369828645966 --receipt /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-32/w1/CtlC1DoNothingB/base-s707466369828645966.json
```

Full expanded commands, environment, cwd, exit codes, elapsed times and exact stdout/stderr are preserved in `.ufo/waves/round-32/w1/CtlC1DoNothingB/commands.json`. Each stderr was empty; solo reference exit code was 0 in each receipt (line 7).

## Counts and per-class output

All receipt paths below are relative to the lane root.

| Seed | APPEND_SERIALIZED | F_unterminated | L_empty | L_terminated | L_unterminated | Exit | Verdict |
|---|---|---|---|---|---|---|---|
| 3361253398345103376 | 8/24 | 8/12 | 0/4 | 0/4 | 0/4 | 1 | MISSES |
| 208027710853012902 | 10/24 | 10/12 | 0/4 | 0/4 | 0/4 | 1 | MISSES |
| 707466369828645966 | 6/24 | 6/12 | 0/4 | 0/4 | 0/4 | 1 | MISSES |

Receipt evidence: `.ufo/waves/round-32/w1/CtlC1DoNothingB/base-s3361253398345103376.json:10-19`, `base-s208027710853012902.json:10-19`, and `base-s707466369828645966.json:10-19` in the same directory. Target is 24/24, not a sum across runs (`corpus/evidence/round32/claims.md:36-40`).

## Per-trial output

Trial ids are the counter's zero-based ids. `PASS` means an empty `fails` array; otherwise every recorded failed check is listed verbatim.

### Seed 3361253398345103376 — MISSES

Source: `.ufo/waves/round-32/w1/CtlC1DoNothingB/base-s3361253398345103376.json:20-235`.

```text
trial=0  L_unterminated FAIL appended-under-cooperating-lock
trial=1  F_unterminated FAIL blank-line, invalid-json-line
trial=2  L_empty        FAIL appended-under-cooperating-lock, prefix-rewritten
trial=3  F_unterminated PASS
trial=4  L_unterminated FAIL appended-under-cooperating-lock
trial=5  F_unterminated PASS
trial=6  L_empty        FAIL appended-under-cooperating-lock, prefix-rewritten
trial=7  F_unterminated PASS
trial=8  F_unterminated PASS
trial=9  L_terminated   FAIL appended-under-cooperating-lock, prefix-rewritten
trial=10 F_unterminated PASS
trial=11 L_terminated   FAIL appended-under-cooperating-lock, prefix-rewritten
trial=12 F_unterminated PASS
trial=13 F_unterminated PASS
trial=14 L_empty        FAIL appended-under-cooperating-lock, prefix-rewritten
trial=15 L_unterminated FAIL appended-under-cooperating-lock
trial=16 L_terminated   FAIL appended-under-cooperating-lock, prefix-rewritten
trial=17 L_terminated   FAIL appended-under-cooperating-lock, prefix-rewritten
trial=18 F_unterminated FAIL blank-line, invalid-json-line
trial=19 L_empty        FAIL appended-under-cooperating-lock, prefix-rewritten
trial=20 F_unterminated FAIL blank-line, invalid-json-line
trial=21 F_unterminated FAIL blank-line, invalid-json-line
trial=22 L_unterminated FAIL appended-under-cooperating-lock, blank-line, invalid-json-line
trial=23 F_unterminated PASS
```

### Seed 208027710853012902 — MISSES

Source: `.ufo/waves/round-32/w1/CtlC1DoNothingB/base-s208027710853012902.json:20-227`.

```text
trial=0  L_unterminated FAIL appended-under-cooperating-lock
trial=1  L_unterminated FAIL appended-under-cooperating-lock
trial=2  F_unterminated FAIL blank-line, invalid-json-line
trial=3  F_unterminated PASS
trial=4  L_terminated   FAIL appended-under-cooperating-lock, prefix-rewritten
trial=5  L_empty        FAIL appended-under-cooperating-lock, prefix-rewritten
trial=6  L_empty        FAIL appended-under-cooperating-lock, prefix-rewritten
trial=7  L_terminated   FAIL appended-under-cooperating-lock, prefix-rewritten
trial=8  F_unterminated PASS
trial=9  F_unterminated PASS
trial=10 F_unterminated PASS
trial=11 L_empty        FAIL appended-under-cooperating-lock, prefix-rewritten
trial=12 L_unterminated FAIL appended-under-cooperating-lock
trial=13 F_unterminated PASS
trial=14 F_unterminated PASS
trial=15 L_unterminated FAIL appended-under-cooperating-lock
trial=16 F_unterminated PASS
trial=17 L_terminated   FAIL appended-under-cooperating-lock, prefix-rewritten
trial=18 L_empty        FAIL appended-under-cooperating-lock, prefix-rewritten
trial=19 L_terminated   FAIL appended-under-cooperating-lock, prefix-rewritten
trial=20 F_unterminated PASS
trial=21 F_unterminated PASS
trial=22 F_unterminated PASS
trial=23 F_unterminated FAIL blank-line, invalid-json-line
```

### Seed 707466369828645966 — MISSES

Source: `.ufo/waves/round-32/w1/CtlC1DoNothingB/base-s707466369828645966.json:20-243`.

```text
trial=0  F_unterminated PASS
trial=1  L_unterminated FAIL appended-under-cooperating-lock, blank-line, invalid-json-line
trial=2  F_unterminated PASS
trial=3  L_terminated   FAIL appended-under-cooperating-lock, prefix-rewritten
trial=4  L_terminated   FAIL appended-under-cooperating-lock, prefix-rewritten
trial=5  F_unterminated FAIL blank-line, invalid-json-line
trial=6  L_empty        FAIL appended-under-cooperating-lock, prefix-rewritten
trial=7  L_unterminated FAIL appended-under-cooperating-lock
trial=8  F_unterminated FAIL blank-line, invalid-json-line
trial=9  F_unterminated PASS
trial=10 L_unterminated FAIL appended-under-cooperating-lock, blank-line, invalid-json-line
trial=11 L_empty        FAIL appended-under-cooperating-lock, prefix-rewritten
trial=12 F_unterminated PASS
trial=13 L_empty        FAIL appended-under-cooperating-lock, prefix-rewritten
trial=14 F_unterminated FAIL blank-line, invalid-json-line
trial=15 F_unterminated FAIL blank-line, invalid-json-line
trial=16 F_unterminated PASS
trial=17 L_terminated   FAIL appended-under-cooperating-lock, prefix-rewritten
trial=18 F_unterminated PASS
trial=19 L_terminated   FAIL appended-under-cooperating-lock, prefix-rewritten
trial=20 L_empty        FAIL appended-under-cooperating-lock, prefix-rewritten
trial=21 L_unterminated FAIL appended-under-cooperating-lock
trial=22 F_unterminated FAIL blank-line, invalid-json-line
trial=23 F_unterminated FAIL blank-line, invalid-json-line
```

## Counterexample, interpretation and smallest safe correction

**Strongest observed counterexample:** seed 707466369828645966, trial 1, an unterminated manifest under the cooperating exclusive lock, recorded `appended-under-cooperating-lock`, `blank-line`, and `invalid-json-line` (`base-s707466369828645966.json:28-38`). The hold check failed in all 36 L trials across the three receipts. Thus the free-writer successes cannot let this do-nothing control reach 24/24. [INFERENCE] They demonstrate schedule-dependent valid framing, not evidence of locking.

The mechanism is grounded in the opened base implementation: `tools/research-gate.sh:3192-3199` probes the last byte, conditionally prefixes a newline, then appends with `printf >>`, without an exclusive lock in that block. The counter explicitly checks seed bytes while its lock is held (`corpus/evidence/round32/c1-count.py:210-226`).

Diagnostic qualifications matter:

- `prefix-rewritten` means the expected `seed + cooperating fragment` is not the file's initial prefix (`c1-count.py:165-167,227-234`); it does **not** prove existing bytes were rewritten. [INFERENCE] With the observed premature appends, the cooperating fragment can instead land after gate lines.
- `invalid-json-line` alongside `blank-line` need not be a second independent corrupt object: the parser tries every line, including blanks (`c1-count.py:173-181`). No `prefix-glued` failure was recorded; no glued-line claim is made.
- Prefix mismatch returns immediately, so later framing checks are not reached for those trials (`c1-count.py:165-167`). Missing diagnostic labels there do not establish those properties.

**Smallest safe correction, not implemented or scored:** [INFERENCE] open the manifest for append, take an exclusive `flock(2)` on that opened manifest before the last-byte probe, and retain it through delimiter decision and append using the held descriptor. Preserve existing bytes and inode; do not substitute a sidecar lock or lock only the final write. This is a fixable base implementation defect, not a demonstrated counter defect. No frozen-counter amendment is indicated by these three control runs; they establish rejection of this control only.

## Limits and bounds

Only this unmodified base control was scored; no C1/C2 candidate implementation or feasibility oracle was run. No C2, no-harm, selftest, or round-31 counter result is claimed. No network requests, installs, production-file edits, or Git/JJ state writes were performed.

`.ufo/waves/round-32/w1/CtlC1DoNothingB/bounds.json` records a successful `timeout 20s stat` (exit 0): scratch gate 306617 bytes, command evidence 3249 bytes, receipts 4025 / 3890 / 4161 bytes. It also records an empty final `/proc` scan for processes carrying this seat's exact `C1_TMP`; the earlier exact-gate-argv scan was empty too. Counter cleanup is explicit in `c1-count.py:246-247,296-297`. All supporting artifacts are in the owned artifact directory; the only external scratch artifact is the owned base-gate copy.

# Serializing `verify-all --json` manifest appends with flock (round 32)

source: S060 (Python `fcntl` documentation, `fcntl.flock(fd, operation)` and `LOCK_EX`); contract
`corpus/evidence/round32/claims.md` §C1 (design v2); prior race `corpus/knowledge/json-delimiter-r24.md:66-71`
verified-at: 2026-10-23 (round-32 gate; counter receipts under `.ufo/waves/round-32/measure/`)
recheck: on-release (from the lane root: `python3 corpus/evidence/round32/c1-count-v2.py --seed <n>`; needs strace(1), flock(1) and /proc/locks)

## The defect

Round 24 made `verify-all --json PATH` terminate an unterminated last line before appending its own
JSON line. The probe (read the last byte) and the append were two unlocked steps, so two writers
that both saw an unterminated last line both prefixed a newline and left a blank line
(`json-delimiter-r24.md:66-71`; round 25 saw it in 2 of 6 seeded runs). The gate assumed one writer
per manifest.

## The fix

The append is one critical section on the manifest itself: the gate opens PATH for append on a
dedicated file descriptor (O_APPEND; the file keeps its inode and its bytes), takes a blocking
exclusive lock with `flock -x` on that descriptor, reads the last byte, writes its line through the
same descriptor, and closes it, which releases the lock. A host without `flock(1)` cannot
serialize, so the gate refuses to write the manifest there (exit 2) rather than append unlocked.
S060 documents the call shape this relies on: `flock()` takes a file descriptor, and `LOCK_EX`
acquires an exclusive lock.

Why the manifest and not a sibling `PATH.lock`: a lock on another file only coordinates writers
that all agree to lock that other file. Locking the manifest means any tool that already locks the
file it appends to — the counter's cooperating writer, a python `fcntl.flock` caller — is excluded
without knowing the gate's convention. **[INFERENCE]** from the contract and the call shape; S060
does not state it.

## How it is measured

`corpus/evidence/round32/c1-count-v2.py` runs 24 trials: 12 where the counter itself holds
`LOCK_EX` on the manifest while 8 gate writers start (empty, terminated and unterminated seeds) and
12 with 16 unlocked writers on an unterminated seed. Every gate writer runs under strace with each
write to the manifest delayed 300 ms. The delay is what makes the test bite: without it, a gate
that locks only around the probe and unlocks before writing scored 24/24 in the round-32 control
wave, because its append lands microseconds after the unlock while the next writer's probe takes
milliseconds. With the delay that control scores 0/24.

## Limits

- flock(2) locks are advisory. A writer that does not lock the manifest is not excluded.
- A holder that never releases blocks the gate indefinitely; the contract sets no timeout.
- NFS and other network filesystems were not tested.
- The counter checks the bytes and the lock's effect on cooperating writers. It cannot see which
  open file description holds the lock: an oracle that locked a second open of the same file also
  scored 24/24 (`.ufo/waves/round-32/w1/OracleC1B/v2-rescore.md`). That oracle excludes cooperating
  writers just as well, but it is not the letter of the contract; the landed gate's descriptor use
  is checked by review, not by the counter.

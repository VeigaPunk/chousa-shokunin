# Serializing JSON manifest appends with `flock` (round 32)

source: S0XX-fcntl (reserved citation slot; L1 assigns the S id; intended row: Python `fcntl` documentation, https://docs.python.org/3/library/fcntl.html, `fcntl.flock(fd, operation)` and `LOCK_EX`; row and `used-by` backlink pending); frozen contract `corpus/evidence/round32/claims.md` §C1; prior race `corpus/knowledge/json-delimiter-r24.md:66-71
verified-at: 2026-10-23 (draft checked against the frozen C1 contract, counter docstring, and round-24 race record; source row assignment remains pending)
recheck: 365d (from the lane root: `python3 corpus/evidence/round32/c1-count.py`; re-read C1 and the assigned fcntl/flock row after a gate or filesystem change)

> Draft only, not ready for admission: replace the S0XX-fcntl slot with L1's assigned mined row and ensure its `used-by` names `corpus/knowledge/manifest-append-lock-r32.md` (QUALITY.md:17-27). The Python source scope reported for this slot is the file-descriptor API and `LOCK_EX`; it does not establish advisory-lock or NFS behavior.

## The defect

The round-24 record identifies the last-byte probe and append as two unlocked operations. Its observation records 16 parallel appenders across 3 runs on an unterminated manifest: all wrote 16 objects each run and no line was glued, but one run had a blank line because two appenders both prefixed a newline. The gate assumed one writer per manifest; the proposed candidate fix was `flock` around the probe and append (`corpus/knowledge/json-delimiter-r24.md:66-71`). This is the historical record, not a reproduction in this draft.

## C1 contract

For `verify-all RECORD --root ROOT --json PATH`, the gate opens PATH for append (creating it when absent), takes an exclusive `flock(2)` on that opened manifest, and holds it from before reading the last byte until after writing its own line. A cooperating writer holding an exclusive lock on PATH excludes both the gate's probe and append. Existing bytes are not rewritten, the manifest keeps its inode, and every appended line is one JSON object on its own line; nothing else in `verify-all` changes (`corpus/evidence/round32/claims.md:23-28`; counter docstring `corpus/evidence/round32/c1-count.py:9-16`).

## Why lock the opened manifest, not a sibling file

C1 names the opened manifest itself as the lock target, and the fcntl source slot documents `flock(fd, operation)` on a file descriptor (`corpus/evidence/round32/claims.md:23-26`; `S0XX-fcntl`, assigned anchor pending). This puts the lock on the file whose bytes are probed and appended. A sibling lock file is a separate coordination path: it only coordinates writers that all choose and lock that same sibling; it is not itself a lock on the manifest. **[INFERENCE]** This comparison follows from the C1 target and the descriptor API; it is not established by the pending source row.

## Cooperating-writer boundary

The explicit C1 guarantee is for a cooperating writer that also holds an exclusive lock on PATH (`corpus/evidence/round32/claims.md:25-28`). **[INFERENCE]** `flock` is advisory: a writer that ignores the lock, or locks some other path, is outside that exclusion guarantee and may still change the manifest. The Python fcntl source slot does not itself establish this advisory semantic; the source row must not be cited for more than its documented API scope.

## Limits and evidence status

- **NFS:** no NFS filesystem was exercised, and the pending fcntl source does not establish NFS behavior. Treat it as unknown here; this draft does not extend the local C1 contract to NFS or another network filesystem.
- **Non-cooperating writers:** outside the guarantee above; this is a contract limit, not a claim that arbitrary writes are prevented (`corpus/evidence/round32/claims.md:23-28`).
- **Hostile holder:** **[INFERENCE]** C1 defines no holder authentication, fairness, deadline, or recovery. A hostile process can fail to follow the append protocol or withhold its lock; this design is cooperative serialization, not access control.
- **No result claimed:** P1 is a frozen predicate, not an observed result in this draft. It requires `APPEND_SERIALIZED=24/24` on each of two fresh-seed runs and no lower run on the landed revision (`corpus/evidence/round32/claims.md:36-40`). This seat did not run the counter or a candidate gate.

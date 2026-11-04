# R77CriticA — reachability of the v4 battery's own predicate

Seat: R77CriticA (critic, leaf; no subagents, no network, no production edits).
Frozen predicate set: `corpus/evidence/round77/claims.md` (read first). Instrument verified before
use: `sha256(corpus/evidence/round77/matrix-battery-v4.py)` =
`155fafb16b6931449abefb60575029f273959ba4e94a4db48ac22e525f106a3d`, equal to the hash in claims.md.
Scratch: `/fast/scratch/hyaku/chousa-r77/R77CriticA/` (deleted before yield; receipts copied here).

Question asked: can a MATRIX reach
`BATTERY=PASS forgers_rejected=11/11 positive=2/2 oracle=REJECTED` (exit 0) **without scoring any
subject correctly**? Yes — three independent channels reach it (A1, A2, A7). Two further channels are
reachable but stop short of the exit code (A5d receipt forgery; A6 ptrace is closed).

## 1. Attempts, exact commands, exit codes

All runs: `python3 -B /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round77/matrix-battery-v4.py --matrix <probe> --work /fast/scratch/hyaku/chousa-r77/R77CriticA/w-<id>`

| id | probe matrix | channel | exit | final line |
|---|---|---|---|---|
| A1 | `a1-hash-identity.py` | subject **content hash** (salt is a strippable suffix) | **0** | `BATTERY=PASS forgers_rejected=11/11 positive=2/2 oracle=REJECTED` |
| A2 | `a2-srcread-contract.py` | `/proc/<ppid>/cmdline` → judge source → `CONTRACT` cells + content hash | **0** | same PASS line |
| A3 | `a3-count-only.py` | invocation count + valid table (control) | 1 | `BATTERY=FAIL forgers_rejected=7/11 positive=0/2 oracle=REJECTED` |
| A4 | `a4-observe.py` | channel census | 1 | `BATTERY=FAIL …` |
| A5 | `a5-fd-inject.py` | in-band write to `/proc/<ppid>/fd/1` | 1 | `BATTERY=FAIL …` (0 injected lines survive) |
| A5b | `a5b-detached-append.py` | detached helper appends to the judge's receipt | 1 | `BATTERY=FAIL …` (appends overwritten by later judge writes) |
| A5c | `a5c-exact-line-append.py` | same, payload = exact predicate line | 1 | `BATTERY=FAIL …` (overwritten) |
| A5d | `a5d-detached-survives.py` | detached helper, fds closed, appends after judge exit | 1 | judge's own `BATTERY=FAIL …` retained **and** 26 exact predicate lines appended at EOF |
| A6 | `a6-ptrace.py` | `/proc/<ppid>/mem`, ptrace | 1 | `BATTERY=FAIL …`; `mem_open=PermissionError` |
| A7 | `a7-order-from-digest.py` | printed `ORDER` digest is a **permutation digest** over 13! | **0** | `BATTERY=PASS forgers_rejected=11/11 positive=2/2 oracle=REJECTED` |

A1, A2 and A7 never open a case, never execute a subject, never build a fixture: they read bytes and
print the contract table with fabricated `PASS` cells. Receipts: `rcpt-a1.txt`, `rcpt-a2.txt`,
`rcpt-a7.txt`.

## 2. F1 — the salt is a strippable suffix; identity survives (A1)

`salted_copy()` writes `source.read_bytes() + b"\n# salt <hex>\n"`. Stripping the trailing salt line
recovers the lane file byte-for-byte, so `sha256(pre-salt bytes)` is a public constant. Two known
positive hashes suffice; everything else is a forger.

Evidence (`rcpt-a1.txt`, 26 matrix calls):
```
22 FORGER   exit=1 marks=11/12/FAIL content=ok
 4 POSITIVE exit=0 marks=12/12/PASS content=ok
```
Random-named directory and random salt do not touch identity: the salt is appended, not woven in.
The battery's docstring claims "a subject or oracle cannot read its own identity from `argv` or its
path" — true, and irrelevant: the matrix does not need `argv` or the path, it has the bytes.

**Impacted axes:** C1 order leg; QUALITY 137 (answer-key hygiene); QUALITY 139 (outer-battery entropy).
**Smallest safe correction:** rewrite the copy per salting (behaviour-preserving: random comment
injection at random offsets + AST identifier renaming), so no published hash matches; and record in
the limits that a matrix that reads the lane tree can still classify by AST shape.

## 3. F2 — the judge's source is one `/proc` read away (A2)

`/proc/<ppid>/cmdline` exposes
`…/corpus/evidence/round77/matrix-battery-v4.py --matrix <self> --work <dir>`. Reading that file and
`ast.literal_eval`-ing `CONTRACT` yields the twelve `expected_rc`/`expected_failed` cells. Evidence:
`a2-calls.log` — 26 lines, each
`ppid_cmdline_battery=…/matrix-battery-v4.py contract_lines=12 subject_sha=… positive=False`, and the
battery exits 0 with the PASS line.

This is the exact channel QUALITY 137 recorded for r75 (`R75Scout` F7: "a candidate that reads the
parent's `/proc/<ppid>/cmdline` can import the matrix's own `CASES` table"). It is still open at the
outer battery, and the claims' phrase "the battery's independently stated `expected_rc`/
`expected_failed` cells" is independent only of the *subject's* assertions, not of the *matrix*.

**Impacted axes:** C1 content leg; QUALITY 137, 139.
**Smallest safe correction:** derive the cells per run from a freshly salted case rather than from a
constant in the judge's source, or state the limit explicitly (the content leg is twin-proven not to
be the discriminating closure: `controls/twin-no-content.txt` still prints `BATTERY=PASS`).

## 4. F3 — the printed `ORDER` digest *is* the permutation, and 13! is small (A7)

`score()` prints
`hashlib.sha256("|".join(name for _g, name, _s in order).encode())`.
That is a digest **of the permutation**, not of the seed. Thirteen names is a constant
13! = 6 227 020 800 domain, and the matrix is allowed `MATRIX_TIMEOUT=300` s per call.

Measured (`perm.c`, OpenSSL incremental SHA-256, OpenMP over the first two positions, 32 threads):

| instrument | wall | core-seconds |
|---|---|---|
| first version (`perm-out.txt`) | 243.0 s | 7385.6 |
| optimized (`perm-out2.txt`) | 33.6 s | 312.6 |

Live recovery inside the battery (`a7-calls.log`):
```
perm digest=8f9f58337713 secs=11.8
perm digest=dc84852c77bd secs=59.1
```
Both recovered orders match the battery's own `MATRIX RUN` lines position-for-position:
- run 0: `successor-counter constant-pass size-map ref-counter tree-identity hang seed-leak
  diff-only harness-source subject-map order-twelve constant-fail naive-grep`
- run 1: `hang order-twelve ref-counter naive-grep seed-leak constant-pass diff-only harness-source
  size-map successor-counter constant-fail tree-identity subject-map`

The matrix then answers by position (`LOADER_MATRIX=12/12 MATRIX=PASS` for the two positives,
`11/12 MATRIX=FAIL` for the other eleven), never running the subject. Battery wall 105.6 s, exit 0,
final line exactly `BATTERY=PASS forgers_rejected=11/11 positive=2/2 oracle=REJECTED`
(`rcpt-a7.txt`).

Budget margin is real but not a defence: `rcpt-a7-run0only.txt` is the same attack with the
unoptimized instrument, where run 0's digest was recovered in 264.1 s — inside the 300 s cap — and
the second run's digest fell outside it, so that run failed. With 22× faster enumeration both runs
fit comfortably.

**Impacted axes:** C1 order leg (this is the leg's stated secrecy), QUALITY 139.
**Smallest safe correction:** one line — print `hashlib.sha256(seed.to_bytes(8, "big"))` instead of
the permutation digest. The seed is already drawn; its digest reveals nothing about the order and
makes the claims sentence "the seed digest is printed, the permutation is not" true.

## 5. F4 — the judge's stdout is writable by its child; the receipt is not a verdict (A5d)

The child can open `/proc/<ppid>/fd/1` (the receipt file under `>` capture) and write. In-band writes
are destroyed by the judge's later writes at its own offset (A5, A5b, A5c). A detached helper that
closes the inherited pipes and appends ~2 s after the last call survives:

`rcpt-a5d.txt` — exit 1, judge's own line still present (`grep -c '^BATTERY=FAIL'` = 1) **and**
`grep -cx 'BATTERY=PASS forgers_rejected=11/11 positive=2/2 oracle=REJECTED'` = **26**; the file's
last three lines are two copies of the predicate line. A verifier that reads `tail -1`, or greps for
the predicate line, is fooled while the battery exited 1.

QUALITY 126 names this class explicitly ("…or that clean up after the run with a detached helper").
The outer battery neither detects nor prevents it, and the round's receipts record no exit code.

**Impacted axes:** C1 evidentiary binding; QUALITY 126, 139.
**Smallest safe correction:** the predicate must be bound to the exit code, and receipts must record
it (`…; rc=$?; echo EXIT=$rc`); the receipt tail must never be the verdict. The battery cannot stop a
same-uid child from appending, so this must be a verifier rule plus a recorded limit.

## 6. Negatives — what the battery does close

- **A3, count-only:** `BATTERY=FAIL forgers_rejected=7/11 positive=0/2` — the per-run permutation does
  kill blind invocation-count scripting; the narrow C1 clause holds. The committed oracles are
  likewise rejected in every run (`ORACLE summary-only/contract-table/block-position REJECTED`).
- **A6, ptrace:** `/proc/<ppid>/mem` → `PermissionError`; `ptrace_scope=1`. The in-memory permutation
  and the `verdict` variable are not reachable from the child.
- **A4 census (what *is* reachable):** parent `cmdline`, `cwd`, `exe`, `environ` (14 125 bytes), the
  subject's pre-salt size (`subject_bytes`), and — when stdout is captured to a file — the judge's
  own `ORDER` and completed `RUN` lines. `PYTHONUNBUFFERED=1` is ambient here, which is why the
  digest is on disk at call 0; with block-buffered stdout the digest channel would need the 8 KB
  buffer to flush first.

## 7. Frozen-text defects (reported, not edited)

1. claims.md: "the seed digest is printed, the permutation is not" — the implementation prints
   `sha256("|".join(permuted names))`, i.e. the permutation's digest. F3 shows it is invertible
   inside the battery's own per-call budget.
2. claims.md recorded limit: "A matrix that reads the battery's own source can recover the order" —
   source reading yields the name set and the contract, never the order (drawn at run time from
   `secrets.randbits(64)`). The order leaks through the printed digest, not the source. The limit
   names the wrong channel and thereby understates the real one.
3. claims.md: "the battery's independently stated `expected_rc`/`expected_failed` cells" — the cells
   are constants in a file the matrix can read (A2). Independence holds against the subject's own
   assertions only.
4. `matrix-battery-v4.py` docstring, Answer-key hygiene: the paragraph covers `argv` and path only;
   content identity (F1), the judge's source (F2), the permutation digest (F3) and receipt writes (F4)
   are all outside it and all demonstrated.

## 8. Verdict on C1

The predicate line is reachable with exit 0 by three matrices that score nothing (A1, A2, A7), so the
PASS line certifies shape, not evaluation. C1's *first clause* — immunity to call-count scripting — is
true and measured (A3). C1 as written is therefore not falsified, but it must not be read as
"the battery cannot be passed by a forgery": the closure it proves is order-blindness for scripts that
do not read their input. The frozen predicate is honest only if the limits say so and the digest is
fixed; as it stands the claims' limits name the wrong channel and the battery prints an invertible
answer key.

**Impacted axes:** C1 (operability, order leg, content leg, evidentiary binding); QUALITY 126, 135,
137, 139.

## 9. Tooling and environment record

- No package installs, no pacman, no network. `gcc` and OpenSSL headers were already present; `perm`
  was built in scratch with `gcc -O3 -march=native -fopenmp -Wno-deprecated-declarations -o perm
  perm.c -lcrypto`. Host python3 = 3.14.8, 32 CPUs, `ptrace_scope=1`.
- No lane, fleet or sibling-repo writes; no git/jj mutation anywhere. Only this wave folder and the
  seat report were written. Scratch removed before yield.

## 10. Receipts

`rcpt-a1.txt` … `rcpt-a7.txt` (battery output per attempt, verbatim), `rcpt-a7-run0only.txt`
(budget-marginal variant), `a2-calls.log`, `a7-calls.log`, `a4-census.txt` (condensed census;
`a4-obs.log` left in scratch), `a5*-inject.log`, `a6-ptrace.log`, `perm.c`, `perm-out.txt`,
`perm-out2.txt`, `bench-perm.py`, and the ten probe matrices.

# R83ExecHarm — C2 K3 (harm) and K4 (exit contract) on the landed tool

Seat `R83ExecHarm`, round 83, lane `chousa`. Attacked revision `aca2a781ef2db375881c21bf407e153f786ac61f`
(archive tree in scratch, `git archive … | tar -x`). The tool under test is `tools/gate-records.py`, blob
`2a59aca7bb50f86f14c44a8293f728c829888a46` — identical at the scored landing `81b8117` and at the tip
(`git rev-parse` both revisions; `git diff --stat 81b8117 aca2a78 -- tools/gate-records.py` is empty; receipt
`08-tree-integrity-and-tool-identity.txt`). No tool was installed or upgraded. Nothing in the lane was edited by this
seat; the only files written are under `.ufo/waves/round-83/w1/R83ExecHarm/` and the `/fast` scratch, which was
removed after the receipts were copied here.

General command form for every measurement below:

```
python3 tools/gate-records.py verify --root <archive-tree> \
    --repo /home/vgpnk/Projects/shokunin/chousa-shokunin <FILE...>
```

## 1. Sweep over committed history (assigned step 1)

Scope: the 130 files under `corpus/lessons/` plus every committed file at `aca2a78` whose first text is
`GATE-RECORD` (`git -C … grep -l -E '^[[:space:]]*GATE-RECORD aca2a78…` → 31 files: 4 lessons and 27 `.ufo`/corpus
artifacts). An independent reimplementation of the frozen class (`lead_strip` over Cf + `^GATE-RECORD(?:\s|$)`)
over all 218 committed files containing the token finds exactly the same 92 in-class lines the tool counts, so no line
is silently skipped and none is counted twice (receipt `10-class-completeness.txt`).

Lessons, one invocation per file (receipt `01-lessons-sweep.tsv`):

```
126 files: GATE_RECORDS files=1 records=0 ok=0 fail=0, exit 1
  4 files: round-80.md records=4 ok=4, round-81.md records=6 ok=6, round-82.md records=5 ok=5,
           round-83.md records=3 ok=3 — all exit 0
```

The 15 records the frozen claim counts for rounds 80–82 are 15/15 `OK`; the round-83 Gate block is 3/3 `OK`. Combined
over all 31 record-bearing files (`03-combined-31-files.txt`, per-file table `09-per-file-table.txt`):

```
GATE_RECORDS files=31 records=92 ok=73 fail=19
exit 1
```

Per-file totals: `corpus/lessons/round-80.md 4/4`, `round-81.md 6/6`, `round-82.md 5/5`, `round-83.md 3/3`; the 27
non-lesson files carry 74 records, 55 `OK` and the 19 `FAIL` detailed in §2. Predicate (b) in its exact form from
inside the archive (`python3 tools/gate-records.py verify --root . corpus/lessons/round-83.md`) prints
`records=3 ok=3 fail=0`, exit 0.

## 2. Every FAIL decided from bytes (assigned step 2)

Receipt `04-fail-bytes-by-hand.txt` shows each record line and the bytes that decide it. Full list, 19 lines:

| file:line | code | determination from bytes |
|---|---|---|
| `.ufo/…/fixture/round-80.real-wordcount.md:21` | WORDS | `words=24`; the quote has 25 tokens. Genuine defect, correct code. |
| `.ufo/…/fixture/round-80.real-bound-27.md:21` | QUOTE_LEN | 27 tokens (`words=27` matches), > 25. Genuine defect. |
| `.ufo/…/fixture/round-80.real-off-by-one.md:21` | LINE | `line=1055` is blank in `b7803829:corpus/QUALITY.md`; the quote is on 1054. Genuine defect. |
| `.ufo/…/fixture/round-80.real-absent-quote.md:21` | LINE | record says `bytez`; line 1054 says `bytes`. Genuine defect. |
| `.ufo/…/fixture/round-80.real-tip-defect.md:19` | LINE | record says `is recording forgeable`; blob line 222 says `is fully forgeable`. Genuine defect. |
| `.ufo/…/fixture/round-80.real-prefix-rev.md:21` | LINE,REV | `rev=b780382992270000…0000` is 40 hex but not an object (`git cat-file -t` rc≠0). Genuine defect; LINE is appended by the same branch. |
| `.ufo/…/fixture/round-80.real-tree-rev.md:21` | LINE,REV | `rev=8bff97f2…` is a **tree**, not a commit (`git cat-file -t` prints `tree`); REV is correct. |
| `.ufo/waves/round-80/w1/R80CriticA.md:336` | LINE,REV | `rev=b7803829…` is a 9-char prefix, `path=corpus/lessons/does-not-exist.md` is absent at every rev. This is round-80's deliberately planted bogus record — a real catch. |
| `corpus/evidence/round80/gate-grounding-check.py:13` | PARSE | docstring usage template `GATE-RECORD <id> rev=<40-hex> …`: no S-id, no form. |
| `.ufo/…/R80ConnectorA/chousa--…gate-grounding-check.py.blob:13` | PARSE | verbatim copy of the same template. |
| `.ufo/…/mutants/m80-M1…m80-M8.py:13` (8 lines) | PARSE | the same usage template inside each mutant's docstring. |
| `.ufo/waves/round-80/w1/R80ReviewerB.md:124` | PARSE | prose paragraph line: `GATE-RECORD in the round-80 lesson is audited (tested by the same fixture…)`. |

No FAIL is a record that meets the checks. The seven fixture lines are the round-80 mutation battery's deliberate
single-field mutations of the four genuine S199–S202 records (`fixture/real-records.txt:1-4`, all `OK`); each fails
exactly and only the check corresponding to its mutation. The critic line is a planted bad record. The eleven PARSE
lines are not records at all (placeholder usage text and prose) — the tool's declared class says such lines are
"checked, never skipped", and PARSE is the documented code for them.

**K3 on committed records: no firing.** All 15 claimed positives and the round-83 three pass, and no committed
`GATE-RECORD` line that meets every check prints `FAIL`.

## 3. Side effects (assigned step 3)

Traced command (strace 7.2, full syscall set, `-f -s 4096`), over `round-80.md round-81.md round-83.md`
(18 records: 4 rev, 13 admit, 1 unreach), output `GATE_RECORDS files=3 records=18 ok=18 fail=0`, exit 0
(receipt `07-side-effect-audit.txt`, raw trace kept in scratch only):

- Network: `socket|connect|bind|listen|accept|sendto|recvfrom|sendmsg|recvmsg` — **0 calls**.
- Opens that are not `O_RDONLY`: **only** `12 × openat("/dev/null", O_RDWR)` by the git children (opened and closed
  before each exec). No regular file in the lane, the archive, the repo or `$HOME` is opened for writing.
- `unlink/unlinkat/rename/renameat/mkdir/chmod/utime/truncate/link/symlink/mknod/ftruncate` — **0 calls**.
- `write()` — 59 calls, **all on fd 1** (the tool's stdout and each git child's `capture_output` pipe).
- Execve: the tool plus 12 `git -C <lane> cat-file` invocations, 12/12 subcommand `cat-file` (`-t` / `blob` only).
  Source grep agrees: exactly three `subprocess.run` calls, all `git … cat-file`
  (`07-side-effect-audit.txt`).
- `--root` tree content sha256 is identical before and after all runs to a fresh extraction of the same revision;
  no file under the archive tree is newer than the pre-run marker.

Concurrent lane activity, recorded so it is not misattributed: other round-83 seats wrote 400+ files under
`.ufo/waves/round-83/w1/` during this audit, `.git/index` was rewritten at 18:14:52 by a sibling's index operation,
and the **working copy** of `tools/gate-records.py` (mtime 18:16:00) differs from the committed tip blob — a sibling's
in-flight repair of a different finding (Unicode digits). The guard below is still present in that working copy
(line 121), so the repair does not touch this finding. See `08-tree-integrity-and-tool-identity.txt`.

## 4. K3 finding — FIRED

**The tool refuses a genuine rev-form record whose quote begins with an ASCII double quote.**

Fixture (`06a-k3-edge-battery.txt`, `06b-k3-guard-isolation.txt`), built from committed bytes at the tip:

```
GATE-RECORD S199 rev=aca2a781ef2db375881c21bf407e153f786ac61f path=corpus/README.md line=490 words=9 quote="modulo documented integrity findings" prediction measured out to zero
```

The named line exists and is exactly the quoted text (1397-line blob; `cat -A` shows
`"modulo documented integrity findings" prediction measured out to zero$`). Every documented check passes:

- REGISTRY S199 has an 11-column row; WORDS 9 = 9 tokens; QUOTE_LEN 9 ∈ [1,25];
- REV `aca2a78` is a commit and `corpus/README.md` is a blob at it; LINE: the normalized quote occurs in line 490.

Landed tool, exact command:

```
python3 tools/gate-records.py verify --root <archive-tree> --repo /home/vgpnk/Projects/shokunin/chousa-shokunin \
    edge/rev-quote-leading-dq.md
GATE_RECORD rev-quote-leading-dq.md:1 S199 FAIL PARSE
GATE_RECORDS files=1 records=1 ok=0 fail=1
rc=1
```

Isolation. The same record with the quote started one character later (`modulo …`, so the quote no longer begins with
`"`) prints `S199 OK`, rc 0. A scratch copy of the tool differing by exactly one token — removing
`or quote.startswith('"')` from the rev-form branch — prints `S199 OK`, rc 0 on the failing fixture and still prints
18/18 `OK` on the four lessons. The guard is the only thing that refuses the record.

The refusal is not in the docstring. The rev form is documented as
`GATE-RECORD S<id> rev=<40 hex> path=<repo-relative path> line=<n> words=<n> quote=<text to end of line>`, and the
normalization section explicitly maps `U+201C/U+201D -> "` — i.e. a straight double quote inside a quote is within
the documented domain, and no check forbids it as the first character. `PARSE` is defined as "the line fits none of
the three forms"; this line fits the rev form. Sending a genuine record to `PARSE` is therefore a harm under C2 K3.

Scope, stated plainly: **no committed record exhibits the defect** — a scan of all 92 in-class committed lines finds
0 rev records whose quote begins with `"` (`10-class-completeness.txt`). The firing rests on a fixture line authored
in this seat's scratch whose rev, path, line and quote are committed lane bytes; if the L1 reads K3 as limited to
records committed in the lane, the same bytes are the residual in §6.1 and the defect remains unfixed either way.
The practical harm is that a lesson quoting a committed line that begins with `"` (e.g. `corpus/README.md:490` or
`:697`) cannot record it, and the tool reports `FAIL PARSE` on a legitimate record.

## 5. K4 (exit contract) — HELD

Boundary battery (`05-k4-exit-contract.txt`), all with the landed tool:

| input | observed | exit |
|---|---|---|
| empty file | `records=0 ok=0 fail=0` | 1 |
| nonempty file, no in-class line (inline-code, list-item, blockquote, comment mentions only) | `records=0` | 1 |
| genuine rev record with BOM + zero-width space prefix | `S199 OK` | 0 |
| genuine rev record with leading spaces | `S199 OK` | 0 |
| bare `GATE-RECORD` line | `? FAIL PARSE` | 1 |
| tab after `GATE-RECORD` | `S199 FAIL PARSE` | 1 |
| rev record CRLF line ending | `S199 OK` | 0 |
| rev record trailing spaces | `S199 OK` | 0 |

Across the whole sweep no run printed a `FAIL` line with exit 0: the 19-FAIL combined run exits 1, every per-file
run with `fail>0` exits 1, and exit 0 occurs only when `records >= 1` and every record is `OK` (126 no-record lessons
exit 1; the 4 record-bearing lessons exit 0 only with `fail=0`). Reordering keys (both forms), a full 64-hex
`capture_sha256`, a 1-word quote and a 25-word quote all print `OK`; a 26-word quote prints `QUOTE_LEN` and exits 1.

## 6. Residuals (out-of-class, listed separately)

1. **§4 is the defect.** If the L1 does not count a scratch-authored record line as "a genuine record", this is the
   residual: an undocumented `quote.startswith('"')` refusal of a documented rev-form value; 0/92 committed lines
   exercise it.
2. **Whitespace asymmetry.** The declared class admits `GATE-RECORD` followed by any whitespace, but `parse` requires
   a literal single space (`^GATE-RECORD (S\d{3,}) ` and `head.split(" ")`). A tab after the token is in-class yet
   prints `FAIL PARSE` (tested: `05-k4-exit-contract.txt`). No committed line uses a tab (0/92).
3. **Non-record prose is flagged.** Column-0 prose or a usage template beginning with the token is in-class and
   prints `FAIL PARSE`. This is by design ("checked, never skipped") and accounts for 11 of the 19 sweep FAILs; it is
   noise only when the tool is pointed at non-lesson files, not a false FAIL on a record.
4. **Unicode digits** are being repaired by a sibling in the working copy (not the landed blob); outside this seat's
   scope, noted so the L1 does not read my 18/18 as covering it.

## Files and behavior

No lane code, registry, capture, claims, counter, fixture or receipt was modified. Written by this seat: this report
and the receipts `01`–`10` in `.ufo/waves/round-83/w1/R83ExecHarm/`. Behaviour measured, never asserted: all numbers
above come from the exit codes and summary lines in those receipts.

VERDICT: R83ExecHarm C2-K3 fired — the landed tool prints `FAIL PARSE` on a rev-form record that meets every docstring check (quote = committed `corpus/README.md:490` at `aca2a78`, which begins with an ASCII double quote), isolated to the undocumented `quote.startswith('"')` guard, with 0/92 committed records exercising it.
VERDICT: R83ExecHarm C2-K4 held — no input without an in-class record exits 0 and no run printed `FAIL` with exit 0 across 130 lessons, 27 other record-bearing files and the boundary battery.
VERDICT: R83ExecHarm C1 n/a — depth claim not touched by this seat.

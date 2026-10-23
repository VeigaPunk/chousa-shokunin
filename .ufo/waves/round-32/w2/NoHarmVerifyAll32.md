# NoHarmVerifyAll32 — single-writer `verify-all --json`: base vs landed gate

Seat: ChousaR32A2.NoHarmVerifyAll32 (leaf, wave 2 FALSIFY). Target: verify-all --json behaviour on the
landed gate vs base for single-writer use — same records, fresh manifests (absent / empty / terminated /
unterminated / NUL-terminated), manifest bytes and exit codes, r24 delimiter cases, --json line schema.

Revisions measured (bound exactly): base gate `0bc318b3e74ac0ad45f4b34154e886d84aebf44673612afab6de5e0b0ff11258`
from `7a7259f0ad41a68068131bfa422a829db9fd1b55`; landed gate `10f2fe12043c6f1565c7d7b9446ee0c4dc11e9649aa3350dcab96f8a2ccb4098`
from `5d8a170795dcf48c3746a4f03dee9cfe32812834` (verified with `sha256sum` on the copies;
`git show HEAD:tools/research-gate.sh | sha256sum` = 10f2fe12…). I ran no C1/C2 counter, so this seat
contributes no counter receipt; the receipts below are the matrix runs.

**Verdict: HOLDS** (single-writer no-harm for C1; no contract violation reproduced). Two declared
differences, both outside a broken-contract reading — details below.

## Method

Scratch: `/fast/scratch/hyaku/chousa-r32/w2/NoHarmVerifyAll32/` with `base/tools/research-gate.sh` and
`landed/tools/research-gate.sh`, a shared hermetic fixture (`tpl/`: `lib/primary.md`,
`noise/chat-export-sources.md`, `claims.jsonl`, records A–G), and a fresh fixture copy per run.
Every run: `cd <fresh fixture> && CHOUSA_NOW_EPOCH=1790000000 timeout 900 bash <gate> verify-all
rec<X>.md --claims claims.jsonl --json manifest.jsonl --root .` (record B: `verify-all claims.jsonl
--json manifest.jsonl --root .`). `CHOUSA_NOW_EPOCH` pins `TS_UTC`, so timestamps are identical by
construction instead of masked. In manifest bytes I masked only `"gate_sha256"` (the gate's own
declared volatile field; it must differ because the gates differ) and, where stated, the additive
chain tally key documented below. Records: A pin-shaped (integrity DRIFT via dangling sweep C9), B a
claims JSONL used as its own claims surface, C unresolved hop with resolvable citation, D unresolved
hop with absent anchor, E resolved hop with absent anchor, F like A but integrity-clean with a
resolvable unresolved hop, G like F with absent anchor.

`matrix.tsv` records 66 runs: the A–E × six-state set twice (60), plus A/wore and A/dir per gate.
Two further rows carry the label `nodir` — a harness slip in which the relative manifest argument
reran the absent state; the real missing-manifest-dir case was run separately (below). Beyond the
matrix: missing manifest dir, non-writable dir, empty read-only manifest, sequential double append,
a flock-free PATH, and one strace run per gate.

## What holds

1. **Exit codes identical, every single-writer case.** A 1/1, B 0/0, C 1/1, D 1/1, E 1/1 across all
   six seed states; write-only manifest 2/2; manifest-is-directory 2/2; missing manifest dir 2/2
   (both print `research-gate: manifest directory not found: <dir> (--json)` as the first stderr
   line, modulo the path; only the trailing usage text differs — direct run, no file created);
   non-writable dir 2/2 with no file created; empty read-only manifest 2/2 with size 0; sequential
   double append 1/1 then 1/1. (`matrix.tsv` cols 6–7; `extra.txt`, `extra2.txt`.)

2. **Fresh-manifest bytes.** After masking only `gate_sha256`, 24/30 cases are byte-identical once
   the additive chain tally `,"resolvable":N` (15 bytes) is removed from the landed line
   (`final-summary.txt`). The 6 exceptions are record C, the one record with a resolvable
   unresolved hop — the C2 semantic (see item 6). Record B, whose section set has no chain, is
   **fully byte-identical after masking `gate_sha256` alone** (`final-summary.txt` last line: True).

3. **r24 delimiter matrix, both gates** (`delimiter-bytes.txt`, record A):
   absent → created 0644, 1 line, 0 blank; empty → 1 line, 0 blank; terminated → 2 lines, prior
   bytes `{"prior":true}` intact, 0 blank; unterminated → newline inserted, 2 lines, 0 blank, 0
   glued objects; NUL → `{"prior":true}\0\n{…}`, 2 newline-lines, 0 blank, prior line still invalid
   JSON (r24 named limit, unchanged); CR → `…\r\n{…}`, 2 lines, 0 blank. Inode unchanged in 30/30
   seeded cases (`matrix.tsv` cols 10–11; anomaly count 0). Sequential two appends onto an
   unterminated seed: 3 lines, 0 blank, same inode, empty stderr, both gates (`extra.txt`).
   The tty-free blank check is GNU `grep -ac '^$'`, avoiding the NUL false blank.

4. **Append is syscall-for-syscall the documented critical section** (`strace-landed-append.txt`):
   `openat("manifest.jsonl", O_WRONLY|O_CREAT|O_APPEND, 0666)` → `flock(10, LOCK_EX)` (flock(1)
   helper on the inherited fd) → probe `openat("manifest.jsonl", O_RDONLY)`; only flock/openat were
   traced, the append itself is observed in the manifest bytes. Base trace has 0 `flock(` calls
   (`strace-base-flock-count.txt` 0). Single-writer byte outcomes are nonetheless identical as item
   2/3 show.

5. **--json line schema unchanged at line and section level.** Top-level key order and per-section
   key order are equal in all 30 cases (`schema-order.txt`, `ALL_TOP_AND_SECTION_KEY_ORDER_EQUAL=True`).
   The only shape change is one tally key: chain tallies gain `"resolvable"` (last position) whenever
   the chain section runs, e.g. base `{"hops":1,"verified":1,"exempt":0,…,"drift":0}` vs landed
   `{…,"drift":0,"resolvable":0}` (`schema-order.txt` tally_key_deltas). This is inside `tallies`, the
   part the target allows to vary, and it is C2's audit count, not a new top-level field.

6. **The one exit-code/verdict divergence is C2's designed surface, not C1.** Record F (clean apart
   from `| 1 | C1 | S1 | unresolved | quote | line1 primary material |`): base `RESEARCH_GATE: CLEAN` rc 0,
   landed `RESEARCH_GATE: DRIFT` rc 1 plus one `FINDING CHAIN_EXEMPT_RESOLVABLE severity=warn
   surface=chain obs=hop=1 status=unresolved source=lib/primary.md …` (`stdout-base-F.txt`,
   `stdout-landed-F.txt`, `manifest-*-F.jsonl`). Record G (same row, anchor absent): both CLEAN rc 0
   (`stdout-*-G.txt`). So a resubmitted verify-all record can flip CLEAN→DRIFT exactly when it marks a
   hop unavailable while its citation resolves — the stated C2 contract. Consumers of verify-all see
   this, not just verify-chain callers.

7. **Failure modes that differ only in wording.** Unopenable manifest (write-only, or empty + 0400):
   both gates exit 2, write nothing, leave bytes untouched (`matrix.tsv` A/wore size 15→15, inode
   same; `extra2.txt` size 0); base says `manifest append failed: manifest.jsonl`, landed says
   `manifest open failed: manifest.jsonl`, preceded by bash's own `… line 3199/3292: manifest.jsonl:
   Permission denied`. Exit codes and the no-write property agree; the message is not a pinned token.

## Declared differences (not scored as breaks)

- **`resolvable` tally key** on every chain-running record (item 5). Additive inside `tallies`;
  changes the manifest line by 15 bytes even when no hop is exempt.
- **Host without flock(1)**: landed exits 2 with `research-gate: flock(1) unavailable; manifest not
  written: manifest.jsonl` and creates no manifest; base exits 0 and appends one line
  (`extra.txt`, PATH = symlink farm without `flock`). This is the documented fail-closed policy
  (`tools/research-gate.sh:3287-3290` at HEAD 10f2fe12), but it is a real single-writer behaviour change
  on such a host.

## Limits

- Single writer only; concurrency/lock exclusion belongs to the C1 counter and selftest 229/230 —
  not re-run here. Single live host, `/fast` filesystem; flock-on-NFS-unsupported was not simulated.
- The lane working tree moved while I measured: at the end of the run `tools/research-gate.sh` in the
  working tree was `d13a76e3722647965e039c1ac286a166be75c63c0cd5a0e17ad2eef42013edd7`, 22 lines ahead
  of HEAD 10f2fe12, adding a `/proc/$$/fd/N` probe and a post-lock unreadable refusal to this very
  append block (`git --no-optional-locks diff -U1 -- tools/research-gate.sh`). My receipts bind to
  10f2fe12; that in-flight repair (symlink-retarget probe; found by SentinelC1After per its comment)
  is not covered by this verdict and changes no single-writer observation above.
- No lane production file, jj state or Git index was written; only this receipt directory was
  created. Pre-existing working-tree modifications (`SKILL.md`, `corpus/*`, `tools/research-gate.sh`)
  are other seats'/L1's; I did not touch them.

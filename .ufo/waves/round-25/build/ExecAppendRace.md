# Round 25 — concurrent JSON manifest append

Named axis: operability. Clone base observed as `b820e4e40ce52deedf53b191140cd7b08ddda929`.

## Measurement

- Ran 16 concurrent copies of `bash tools/research-gate.sh verify-all corpus/fixtures/full-r6.md --json /tmp/chousa-r25-ExecAppendRace/m.jsonl --root /home/vgpnk/Projects/shokunin`, six iterations per condition; each writer returned 0.
- Empty-manifest control (truncate to zero before each iteration): runs 1–6 each had 0 blank lines, 0 invalid JSON lines, 16 nonblank JSON lines (`json.loads` per nonblank line).
- Reproduction precondition from `corpus/knowledge/json-delimiter-r24.md:66-71`: seed `m.jsonl` with `b'{"prior":true}'` (no final newline) before each iteration. Runs 1–6: blank lines `0,1,1,0,0,0`; invalid JSON lines `0,0,0,0,0,0`; nonblank JSON lines `17` each (seed + 16 writer records). Measured defect: **2/6 runs** had one blank line; all 96 writers exited 0.
- Counting used Python's `json` module to parse every nonblank line. The empty control confirms the unterminated seed is material; it is the documented round-24 race condition, not a finding of 0/6 under the wrong initial state.

## Root cause and candidate

- [INFERENCE] `tools/research-gate.sh:2497-2504` probes the manifest's last byte with `tail`, decides at 2501–2502 whether to prefix `\n`, then appends at 2504, with no lock covering probe plus append. Two writers can both observe the same unterminated EOF and both prefix; the later prefix follows the preceding record's terminator, creating a blank line. The symptom is not caused by separate delimiter/body `printf` calls: delimiter and body are already in the one `printf` expression at 2504.
- Candidate is a `flock` on an append-open manifest descriptor, held across the last-byte probe and write. It is **not landed**. Patch: `/tmp/chousa-r25-ExecAppendRace/candidate-append-race.patch`.
- Risk: `flock` is advisory and needs the runtime `flock` utility; it serializes cooperating gate writers, not unrelated writers that ignore the lock. No candidate-patch execution or gate selftest was requested/run.

## Retained files and hashes

- Clone output `m.jsonl` (final iteration; empty-manifest control was not retained): `dc966ba87cf0b3d74db019a28efef491316aa4972f053231cf93936accc972a6`.
- Candidate patch `candidate-append-race.patch`: `aa11483b3732cc83238e51db1df67251550f60512a6874e05e0d78e45f2b05c1`.
- No source file was changed in the clone; no tools were installed.

VERDICT: Reproduced the documented unterminated-manifest race in 2/6 sixteen-writer runs; supplied an unlanded lock-based candidate patch.
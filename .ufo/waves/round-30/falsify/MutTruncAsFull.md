VERDICT: pass — KILLED: both mutated runs scored below 27/27; pristine and restored runs passed.
Axes: operability tested; coverage not exercised. Mutant: `_read_response` accepts every empty read as complete; expected detector: C 2 rejects deadline-truncated bodies.
Actual `QUOTE_REOPEN_FETCH_BOUND_MATCH`: pristine 27/27 (exit 0), run 1 25/27 (exit 1), run 2 26/27 (exit 1), restored 27/27 (exit 0).
Misses: run 1 `drip-body` 1/3 and `stall-body` 1/1, both ABSENT instead of UNREACHABLE; run 2 `drip-steady` 1/2, VERBATIM instead of UNREACHABLE. Other kinds had no misses; all misses passed time and address checks.
SHA-256 before/restored/source: `47a657e72f38f9424748a000b3bd218e26b6a601192b68e06a916471222a1201`; mutated: `98f54c7c5c2111fcb9e6ef6b11a13b92076952c75554ac56364f48915ae4ef0d`. Required input hashes matched before scoring.
Patch: [mutant.patch](MutTruncAsFull/mutant.patch). Receipts: [pristine](MutTruncAsFull/pristine.json), [run 1](MutTruncAsFull/run1.json), [run 2](MutTruncAsFull/run2.json), [restored](MutTruncAsFull/restored.json).
Exact bounded commands, exit codes, outputs and hashes: [evidence.json](MutTruncAsFull/evidence.json); every detector ran from the lane root with a 300 s timeout and memory/process limits.
Restoration: exact-byte `cmp` exit 0; process search found no remaining probe children (exit 1). No tools installed or updated; no network fetches.

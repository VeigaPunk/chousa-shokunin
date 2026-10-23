VERDICT: pass — KILLED; both mutant runs scored 86/106, below the required 106/106.
Axes: coverage measured; operability bounded to 300 s, 2 GiB address space and 4096 processes; C 2 not scored.
Mutation: remove only `"title"` from `SKIP`; patch: `.ufo/waves/round-30/falsify/MutTitleKept/mutant.patch`. Exact detector commands, exit codes and supplied input hashes: `.ufo/waves/round-30/falsify/MutTitleKept/evidence.json`.
Output: pristine and restored `QUOTE_REOPEN_HEADLESS_MATCH=106/106` (exit 0); mutant runs 1 and 2 `QUOTE_REOPEN_HEADLESS_MATCH=86/106` (exit 1). Receipts: `.ufo/waves/round-30/falsify/MutTitleKept/{pristine,run1,run2,restored}.json`.
Misses in each mutant receipt, all `title-window`, expected `ABSENT`, got `VERBATIM`: `closed-head` 6; `headless-body` 5; `headless-nobody` 5; `headless-text` 4. All other kinds matched.
SHA-256 before/restored: `47a657e72f38f9424748a000b3bd218e26b6a601192b68e06a916471222a1201`; mutant: `5d8e14447aa4a2249752245e071ead44cdbc20eea7056da9f881af8b016ee2b7`. `cmp` exit 0, `RESTORATION_BYTES_EQUAL`; lane tool, counters and harness hashes unchanged.
Initial timing-wrapper attempt exited 127 because `/usr/bin/time` was absent; no detector started. Direct bounded retries succeeded. No installations; final process search found no matching Python detector or harness process (exit 1).

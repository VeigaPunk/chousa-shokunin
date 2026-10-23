# D2 — backlog-128 receipts

Copied every source `bl*.json`, plus the generating `c2-count.py` and `qr_harness.py`, from `/fast/scratch/hyaku/chousa-r30/w2/RerunC2B/bl/` into `.ufo/waves/round-31/build/ExecD2Backlog/bl/`. No `__pycache__` was copied. `bl/manifest.tsv` lists all 20 source files with byte count, SHA-256 and nanosecond-resolution UTC source mtime. `timeout 120 cmp "$src_file" "$copy"` returned 0 for every receipt and both scripts; aggregate output: `ALL COPIES BYTE-IDENTICAL`.

## Counter and harness provenance

The frozen round-30 files are from commit `abfdf93274d0c70e02465e22abcf029dea59efb9` (“design v4 before data”). Its frozen `c2-count.py` SHA-256 is `0a59e3736fed8ef4cf7b00a75955eccfd0336c8a0ca84bee23402408b727f88f`; both `diff -u` against scratch `c2-count.py` and `cmp` returned 0. Thus the counter bytes are the frozen-v4 bytes (the scratch copy was not modified). Each receipt itself labels `design` as `v3`; that stale/internal label is retained as evidence, while its `counter_sha256` matches the v4-commit file. The frozen harness SHA-256 is `e2be0dd16da5b2bf03430772831763e56c6ff6dd6a44063bb05c909b284f50d4`; scratch/receipt harness SHA-256 is `91475cbedab620ca058e366515763c32bec19c0ab6a9700d72f5a780fe5aeb2e`. `diff -u` returned 1 and showed exactly one added line in the server class: `request_queue_size = 128`. Therefore the runs used frozen counter bytes with a modified scratch harness, not an unmodified frozen harness. Every receipt records tool SHA-256 `47a657e72f38f9424748a000b3bd218e26b6a601192b68e06a916471222a1201`.

## Receipt tally

All receipts record label `QUOTE_REOPEN_FETCH_BOUND_MATCH`, `predicate_holds: true`, and `n=t=27`; each binds the same tool, counter and harness hashes above. The harness backlog setting is 128 for each, established by the common scratch harness hash and the one-line diff.

| Receipt | Score | Backlog |
|---|---:|---:|
| `bl1.json` | 27/27 | 128 |
| `bl2.json` | 27/27 | 128 |
| `bl3.json` | 27/27 | 128 |
| `bl4.json` | 27/27 | 128 |
| `bl5.json` | 27/27 | 128 |
| `bl6.json` | 27/27 | 128 |
| `bl7.json` | 27/27 | 128 |
| `bl8.json` | 27/27 | 128 |
| `bl9.json` | 27/27 | 128 |
| `bl10.json` | 27/27 | 128 |
| `bl11.json` | 27/27 | 128 |
| `bl12.json` | 27/27 | 128 |
| `bl13.json` | 27/27 | 128 |
| `bl14.json` | 27/27 | 128 |
| `bl15.json` | 27/27 | 128 |
| `bl16.json` | 27/27 | 128 |
| `bl17.json` | 27/27 | 128 |
| `bl18.json` | 27/27 | 128 |

## What the receipts show and do not show

The 18 JSON receipts document 18 successful 27/27 runs of the recorded tool and frozen-v4 counter bytes when run with the backlog-128 scratch harness; their recorded tool, counter and harness hashes are consistent across all rows. They do not provide a matched same-seed run using the unmodified harness or per-connection evidence attributing any delay to the listen queue. Thus they establish the result under the altered harness, not the causal mechanism for earlier misses; the claim that backlog overflow caused those misses remains [INFERENCE], not a finding isolated by these receipts.

## Exact evidence and commands

- Source files and original mtimes: `/fast/scratch/hyaku/chousa-r30/w2/RerunC2B/bl/`; retained copies and manifest: `.ufo/waves/round-31/build/ExecD2Backlog/bl/manifest.tsv` and sibling files.
- Receipt field extraction: `timeout 90 python3 - <<'PY' ...` over sorted `bl*.json`; all 18 output rows reported `QUOTE_REOPEN_FETCH_BOUND_MATCH | v3 | True | n=27 t=27 frozen=27`, counter SHA `0a59…`, harness SHA `91475…`, tool SHA `47a657…`, and cap 20.0 / slack 1.5.
- Frozen comparison: `timeout 60 diff -u <round30>/qr_harness.py <scratch>/qr_harness.py` exited 1 with only the `request_queue_size = 128` addition; `timeout 60 diff -u <round30>/c2-count.py <scratch>/c2-count.py` exited 0 with no output. Frozen-v4 commit blob hashes were checked with `git show abfdf93:<path> | sha256sum` and matched the current frozen counter/harness hashes above.
- No round-30 files were changed. No build, test, lint, formatter or counter was run; no tools were installed or updated.

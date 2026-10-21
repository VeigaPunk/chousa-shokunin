# Round 26 — ExecReaderCensus

Base: private clone `/tmp/chousa-r26-ExecReaderCensus-3`, observed HEAD `f361d12e44687841e30ec35710ddb366c6f795e0`; measured `tools/research-gate.sh` SHA-256 `985a63200ca4c5712806d8752ba27a8f3448b026f773659079e71ca602e56ef7`.

Method: each sample used a fresh `python3` wrapper, `subprocess.run(['bash', gate, mode, path, '--root', root], capture_output=True, timeout=300)`, `resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss`, wall seconds. Single-run sequence avoids cross-mode contention. All large inputs were exactly 1,048,576 LF bytes (SHA-256 `b3a2d81c390e0531dbcf0dec082c4ca96d26f26aa9a26a26e80b5f00fa9f48e3`); tiny controls were 4 LF bytes (SHA-256 `545c38b0922de19734fbffde62792c37c2aef6a3216cfa472449173165220f7d`). Claims modes used `.jsonl`; others `.md`; each was passed in the positional input slot shown by usage. No 8 MiB input was run.

| Mode (CLI) | 4-byte control RSS/time | 1 MiB RSS/time | 8 MiB linear-excess estimate RSS/time |
|---|---:|---:|---:|
| `verify` | 12,416 KiB / 0.011 s | 86,572 KiB / 66.651 s | 605,664 KiB / 533.131 s |
| `verify-claims` | 11,880 / 0.009 s | 11,604 / 53.578 s | 11,880 / 428.561 s |
| `verify-chain` | 12,396 / 0.009 s | 87,376 / 68.425 s | 612,236 / 547.337 s |
| `verify-sweeps` | 12,420 / 0.009 s | 86,640 / 67.805 s | 606,180 / 542.377 s |
| `verify-integrity` | 12,164 / 0.011 s | 87,664 / 67.418 s | 616,164 / 539.267 s |
| `verify-all` | 12,128 / 0.034 s | 87,596 / 151.061 s | 615,872 / 1,208.250 s |
| `verify-metadata` | 12,124 / 0.012 s | 284,980 / 10.878 s | 2,194,972 / 86.940 s |

Estimate is conditional linear growth above control: `control + 8 × max(0, 1MiB − control)` separately for RSS and elapsed. It is not an 8 MiB observation. `verify-claims` RSS stayed within control noise; the blank JSONL has no claims/source reads. `verify-all` blank input ran the structure path only. The record modes returned the same RC for control/large: verify 1, claims 0, chain 1, sweeps 0, integrity 0, all 1, metadata 1.

## Out-of-C1 reader debt (base line references)

- `tools/research-gate.sh:409-424` `load_sections` streams the record into `LINES[]` at 412, then scans the full array; its second pass retains section text by repeated `SEC_BODY` appends at 442, 448, 454, 460, 475. Callers: `verify_record:804`, `verify_chain:1629`, `verify_sweeps:1918`, `verify_integrity:2176`, `verify_all:2614`; verify-all also launches per-section subprocesses at 2661-65. This whole-record line-array path is outside metadata-only C1.
- Section-body copies are separate debt: `table_rows:479-513` copies `SEC_BODY` into `body` (481) and iterates via `<<<"$body"` (513), with per-row `headers`/`cols` arrays (495, 505). Other body here-strings: `section_nonempty_prose:547-557` (554), `scope_decl_screen:757-783` (782), verify-all Meta parse at 2617-31 (2631). Their size follows selected structured sections; the newline-only runs do not exercise populated sections.
- `verify-claims`/`verify-chain` separately slurp each cited source: `hay=$(cat ...)` at 1381-82 and 1697-98. Token matching copies `hay` into a local at 1278, forms prefix/suffix substrings at 1290-91, and pipes it to grep at 1298; chain heading/line scans use `<<<"$hay"` at 1548, 1562 and quote fallback/nearest probes at 1552, 1569-83. Out of C1; source size refusal is at 1187-91. Blank mode inputs exercise none of these source-file paths.
- `--drift` is outside the measured public-mode set: `run_drift:3031-39` appends baseline lines into `body` (3033); `gate_drift_report:2940-45` materializes baseline/capture strings into `base[]`/`new[]` (2944-45), then compares them. Name as separate baseline-parser debt.
- Row-derived caches (`verify_sweeps:1934-75,1989-2043`; `integ_cell:2151-60`) store table rows/tokens/glob matches, not every input line. `FINDING_LINES`/mode result arrays retain emitted records, not a raw whole-file line array.
- The search `mapfile|readarray|LINES\+=|lines\+=|while IFS= read -r` found no `mapfile`/`readarray`; `scan_secrets:669-690` and the claims JSONL loop `1327-1443` stream input lines rather than retaining the raw file. Some other `while read` loops consume already-buffered section strings or row output, so the syntax alone is not evidence of a whole-file slurp.

C1 target is specifically metadata's bounded snapshot read at `2363-73`, followed by the line array at `2383-87`; the header scan can break at `## ` only after building that array. The 1 MiB metadata result extrapolates to about 2.09 GiB / 86.94 s by the formula above. Baseline evidence has a discrepancy: `corpus/evidence/round26-measure-before.log:4` records 2,238,736 KiB / 90.6 s for s1, while `round26-claims.md:29-32` summarizes 2,240,704 KiB / 86.9 s; this census does not reconcile them.

Evidence/work boundary: fixtures reside in `/tmp/chousa-r26-ExecReaderCensus-3-runs.aEtjad`; no lane source or clone files were edited and no patch was produced. LSP was not available in the mounted tool inventory; shell definitions/callers were located with `grep` and read by line. No installs; no build, lint, formatter, or general selftest was run.

VERDICT: The C1 allocation is confirmed by the requested 1 MiB measurement; distinct whole-record, section-copy, cited-source, and drift-buffer paths remain out-of-scope debt, with 8 MiB values explicitly extrapolated only.
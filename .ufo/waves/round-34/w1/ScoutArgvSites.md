# ScoutArgvSites — unbounded record/source data on exec argv or in the environment

Read-only recon of `tools/research-gate.sh` at lane tip `70feb5eacc959eb98071461fe89f0b892c0810d8` (gate SHA-256 `43a1af35ca668fe535fcef1e68b0c64bbba3eada59c7a23181f591901fca4346`, 7857 lines; matches `corpus/evidence/round34/claims.md:4`). Access date 2026-10-23. Production body is lines 1–3933 (`run_selftest` starts at 3934). No install. `c1-count.py` was not run, and the gate was not executed.

Commands (exit 0): `sha256sum` and `wc -l` on the gate; `git rev-parse HEAD`; `getconf PAGE_SIZE` → `4096`; `getconf ARG_MAX` → `2097152`; `bash --noprofile --norc -c 'type grep; type sed; type printf; type tr'` → `/usr/bin/grep`, `/usr/bin/sed`, printf is a shell builtin, `/usr/bin/tr`. Shebang is `#!/usr/bin/env bash` (`tools/research-gate.sh:1`). A Python scan of non-comment production lines listed every `grep`/`sed`/`tr`/`readlink`/`stat`/`cat`/`bash` invocation that expands a variable; call sites of `tok_span_at`, `tok_span_all`, `line_probe`, `longest_token`, `chain_anchor_at`, `chain_nearest`, `chain_probe` were then read. `export ` in production is only lines 1557 and 1587 (the word `export` at 898 is a finding id). No `eval` of record data.

## Threshold (why 32 KiB)

`/usr/include/linux/binfmts.h:15` (2026-10-23): `#define MAX_ARG_STRLEN (PAGE_SIZE * 32)`. With the measured page size that is 131072. `ARG_MAX` (2097152) is the total, not the single-string cap. Under `local LC_ALL=C` (`:1556`, `:1586`), each span byte is appended as `\x` plus two hex digits (`:1563-1566`, `:1590-1593`): 4 bytes of pattern per span byte. 32768 × 4 = 131072. This recon did not re-exec grep; `claims.md:23-26` records a prior measurement that a span of 32768 bytes or more fails that exec with "Argument list too long". The JSONL line that holds `span` is read with no length cap (`:1636`, `:1698`). `SOURCE_READ_MAX_BYTES` (`:308`, 8388608) caps the source file before `cat`, not the span.

## Payload on an exec argv

| id | path:line | argv | data | modes that reach it | 32 KiB+ can reach this argv? | C1 |
|---|---|---|---|---|---|---|
| A1 | `tools/research-gate.sh:1578` | `grep -a -z -b -o -P -- "$regex"` | span, 4×, one string | verify-claims via `:1806`; verify-chain quote via `:2000`; verify-all only by re-exec of those modes (`:3352`, `:3470`, `:3471`) | yes, whenever the function is called with a span ≥32768 | **claimed** for the `:1806` caller |
| A2 | `:1605` | same construction | same span | verify-claims `:1827` only (no chain/sweeps caller) | the construction would, but on this gate `:1827` sits inside the `:1806` success branch (`:1806-1827`), so a ≥32768 span never gets here | **claimed** call site; dead for long spans until A1 returns success |
| A3 | `:1865` | `grep -Fn -m1 -e "$tok"` | longest space/tab token of the span's first line (`:1860-1863`, `longest_token` `:1384-1390`) | verify-claims miss path; verify-all claims child | only if that token itself is ≥32768 and the first line is absent from the source (`line_probe` empty). A verbatim long span whose first line is present does not reach `-e` | **out of claim** (`CLAIM_SPAN_NOT_FOUND` probe) |
| A4 | `:2024` | same `-e "$tok"` | longest token of the quote anchor's first line | verify-chain, resolved hop, `PROBE_KIND==quote` and anchor missing (`:2189-2190`); verify-all chain child | same token-length condition | **out of claim** |

A1 callers, observed:

- `:1806` `tok_span_at "$hay" "$span"` in `verify_claims`. Hay is the source body (`:1804-1805`), passed to builtin `printf` and then to grep's stdin, not to grep's argv.
- `:2000` `tok_span_at "$hay" "$text"` is the `quote)` arm of `chain_anchor_at` only. `heading)` (`:1973-1997`) and `line)` (`:2004-2011`) compare in the shell. `chain_probe` (`:2103`) calls `chain_anchor_at` for resolved hops (`:2160`) and for exempt unresolved/blocked-no-fetch/labelled-dead hops (`:2203`). Default kind when none is named is `quote` (`:1961` `ak=${kind_claim:-quote}`). Anchor text is the chain cell `anchor`/`anchor_text`/`span`/`fragment`/`locator` or the `to#` fragment (`:1932-1948`), uncapped.

A2 is the line-binding matcher. `tok_span_all` has no other caller. A fix that makes `:1806` return success for a long span would then put that same span on the `:1605` argv when `"line"` is present.

A3 is the `else` of `tok_span_at` (`:1854-1872`), and only for `expect` of `supported` or `contradicted` (`:1857`). `expect=unsupported` skips it (`:1874`). `claims.md` not-claimed list names this probe. C1 records use `expect=supported` (`c1-count.py` docstring), so the miss path is entered after A1 fails, but `line_probe` of a present first line returns before `-e`.

`verify-sweeps` does not call `tok_span_at`, `tok_span_all`, `line_probe`, or `grep -e`/`-P`. The gate's own header (2026-10-23, `tools/research-gate.sh:144`): "a content sweep carries no probe the gate could re-run." `claims.md:86` says verify-sweeps uses the same helpers; that sentence is not true of this file. Sweeps are out of claim either way.

## Named in the brief, but not an unbounded argv

**`line_probe` (`:1376-1381`).** The needle is used only in `[[ $hay == *"$needle"* ]]` and `${hay%%"$needle"*}`. It is not an exec argument. The prefix before the needle is passed to `count_nl` (`:1369-1373`): builtin `printf '%s'` piped to external `tr -dc '\n' | wc -c` (stdin, not argv). Callers: `:1861` (claims miss probe) and `:2020` (chain quote miss). A ≥32 KiB first line can be the needle (shell only). A ≥32 KiB source prefix can reach `tr`'s stdin when a short span matches late, or on the verbatim-long miss path after A1 fails. `count_nl` of the span itself (`:1573-1574`, `:1601-1602`) runs only after grep has already returned a match, so a ≥32768 span does not reach it on this gate.

**`sed -n` expressions.**

- `:1837` `sed -n "${start_line},${end_line}p"` — decimal line numbers from the match, and only after A1 succeeds, and only for `expect=contradicted`. A ≥32768 span does not reach it today. The marker is tested in the shell (`:1842` `[[ $region == *"$m"* ]]`), not on argv. Out of claim (`claims.md` "expect=contradicted markers on long spans").
- `:1869` and `:2029` `sed -n "${nearer}p"` — `nearer` is a line number from `line_probe` or from `cut -d: -f1` of grep `-n` output. The span bytes are not the sed expression. Out of claim (context probe).

**`export` (`:1557`, `:1587`).** `local LC_ALL=C; export LC_ALL`. The exported value is the constant `C`, not record or source bytes. It is in the environment of the child grep on both the claimed path and the chain-quote path. No other production `export` copies record data into the environment. Inherited process environment is passed through, but the gate does not place span/source bytes there. Selftest `export`s at `:4015-4016` and `:5727` are below `run_selftest` and are not on verify-claims/chain/sweeps/all.

**printf into a subshell.** `printf` is a bash builtin in the shell the shebang starts, so `printf '%s' "$hay"` (`:1578`, `:1605`, `:1837`, `:1865`, `:1869`, `:2024`, `:2029`) does not exec and is not subject to `MAX_ARG_STRLEN`. The external process in those pipelines is grep, sed, `tr`, `head`, or `cut`. Hay (source, ≤8 MiB) is their stdin. Display truncations `printf '%.60s'` / `%.80s` (`:1921`, `:1870`, `:2030`, `:2193`) are also the builtin.

## Path strings on exec argv (not span bytes)

No script-side length cap before these execs. A ≥32 KiB string reaches the argv; it is under `MAX_ARG_STRLEN` (131072) and over a typical `PATH_MAX`, so the exec can start and the path operation then fails. This is not the C1 pattern.

- `:1423` `readlink -f -- "$cand"`, then `:1461` `stat -c '%s %h %d' -- "$canon"` (and `:1487` `file_size_bytes` → `:784-785` `stat` if that stat fails). `cand` is the claim/chain source field, including the not-found relative case (`:1420-1421`). Modes: verify-claims, verify-chain (`chain_probe`), verify-all declared-claims resolution (`:3444`). Out of claim.
- `:701` `readlink -f -- "$cand"` in `ptr_resolves_meta`. An absolute record pointer always reaches it (`:692-693`); a relative pointer reaches it only when `-e`/`-L` is already true (`:694-697`), which a ≥32 KiB relative path is not. Mode: structure `verify` via `check_pointer`. Not a verify-claims/chain/sweeps content path.
- `:2377` `readlink -f -- "$base"`, `:2379` `realpath -m -- "$base"`, `:2381` fallback `readlink`. `base` is the sweep location's directory prefix (token with a slash, cut at the first glob character, `:2365-2375`). A slash-free 32 KiB token becomes `dir=.` and does not reach this argv. `for m in $pat` (`:2399`) is shell globbing, not exec; `printf '%s\n' "$pat"` (`:2404`) is the builtin. Mode: verify-sweeps, and verify-all's sweeps child. Out of claim. This is the only sweeps site where a ≥32 KiB record field can be an exec argv, and only as a directory prefix.
- `:1804` and `:2100` `cat -- "$path"` run only after `claim_source_path` has accepted an existing readable file. That path is a resolved filesystem path, not the raw span. [INFERENCE] a path that already exists is not ≥32 KiB.
- `:3352` `bash "$SELF" "$mode" "$@" --root "$ROOT"` puts the record or claims path on bash's argv, never the span. verify-all.
- CLI file operands (`grep -- "$record"` at `:897`, `:906`, `:3415-3416`; `sha256sum -- "$record"` at `:3495`; `head -n 5 -- "$record"` at `:873`) are invoker paths, not bytes from inside the record.

## Stdin only (constant argv, ≥32 KiB payload possible on the pipe)

Not exec argv and not the environment. Pattern or script is a literal, or is operator environment rather than the record:

- `:649` `grep -qiE "$DEAD_MARK_RE"` — `DEAD_MARK_RE` is a constant (`:647`); the row is a here-string.
- `:817-820` `scope_norm`: record Meta scope/domain value on stdin of `sed`/`tr`; scripts are literals. Structure `verify`.
- `:902` Meta body here-string to `grep -qiE` with a literal pattern.
- `:970` `grep -qiE "$AGG_ERE"` — pattern is `CHOUSA_AGGREGATOR_ERE` or the default at `:325` (operator environment in, not record data out). The source row is a here-string.
- `:527`, `:561`, `:572`, `:3437`: table/meta cells on stdin of `sed` with literal scripts.
- `:2659` integrity cell text on stdin of `tr`.
- `:2992-2994` metadata `source_value` on stdin of `grep -oE`/`-xE` with literal patterns. Not one of the four asked modes.
- `:3355-3377` grep of the child gate's stdout (`VAS_OUT`) with literal patterns.

## Limits

- Not re-measured: the exact `execve` comparison (`>` vs `>=`, NUL included). Local facts are the header macro, page size, and the 4× construction. The 32768 failure point is `claims.md`'s prior probe, not a run from this seat.
- Selftest (from `:3934`) was not inventoried beyond confirming its `export`s are outside the four modes.
- `set -euo pipefail` is on (`:292`). Whether the process-substitution failure at `:1578` aborts the shell was not re-run; `claims.md` says the claim still prints `observed=unsupported`.
- Spans above 65536, non-letter bytes, and `expect=contradicted` hit the same A1 construction with no extra cap; they are outside the frozen count (`claims.md:85-88`).

# RevGrepSites — grep-invocation census of research-gate.sh (round-35, wave 2)

Gate scored: `tools/research-gate.sh` sha256
`1f2fb4f522d9a670b49dd61ad1369f55ee012f3b0d38050654be45a71aaef617`
(the landed gate; verified by `sha256sum`, receipt `w2/RevGrepSites/gate-sha.txt`).
Access date 2026-10-23. Scratch: `/tmp/hyaku/chousa-r35/w2/RevGrepSites/`.

## Method

Every line matching `\bgrep\b` (minus comments) was enumerated (73 lines;
`w2/RevGrepSites/site-map.txt`), then each was classified as invocation vs
non-invocation and mapped to its enclosing function and shell context.
Bypass vectors searched explicitly: `command grep`, `egrep`/`fgrep`,
`env … grep`, `xargs grep`, `find -exec grep`, bare `/usr/bin/grep`,
`bash -c`/`sh -c` bodies, `eval`, backticks, `source`/`.`, `python3 -c` /
`awk` / `perl` bodies, `timeout`/`flock`/`nice`/`stdbuf` wrappers, `export -f`
of `grep`, variable-indirected command names (`"$X" "$@"` where X could be
`grep` — none; `GREP_BIN` is assigned only inside `grep_pin_init`).

Result of the vector search: **no `command grep`, no `egrep`/`fgrep`, no
`env`/`xargs`/`find -exec` grep, no `eval`, no backticks, no `source`, no
`bash -c`/`sh -c`/`python3 -c` body containing grep, no `timeout`-wrapped
grep, no `export -f grep`.** Every grep invocation in the file is a bare-word
`grep` inside a shell function → bash resolves it to the `grep()` wrapper
defined at :351 (`grep() { command "$GREP_BIN" "$@"; }`), and every
sub-shell context used (pipeline stage, `$(...)`, `< <(...)`, herestring,
`VAR=x grep`) still runs functions. `ns_run` (:5880) and `verify_all_section`
(:3504) and all selftest harnesses re-exec `bash "$SELF"` / `bash "$NS_SELF"`,
so children re-run `grep_pin_init` (:8039) and re-pin before use.

## Invocation census

All 68 invocation sites (full table in `site-map.txt`; pin block itself
excluded — it invokes `$GREP_BIN`/`"$cand"`, not `grep`):

| Lines | Enclosing function | Context |
|---|---|---|
| 688 | `section_nonempty_prose` | `$(... \| grep -c .)` |
| 718 | `line_has_mark` | herestring |
| 942, 966, 971, 975, 1039 | `verify_record` | pipeline / file / herestring |
| 1687 | `tok_span_offsets_direct` | `< <(printf \| grep -a -z -b -o -P)` |
| 1716 | `tok_span_offsets_chunk` | `< <(printf \| grep -a -z -b -o -P)` |
| 1762 | `token_matcher_require` | `printf \| grep` probe |
| 2017 | `verify_claims` | `$(... \| grep -Fn -m1 \| head \| cut)` |
| 2176 | `chain_nearest` | same shape |
| 3144, 3146 | `metadata_registry_check_source` | `$(printf \| LC_ALL=C grep …)` |
| 3507–3529 (7 sites) | `verify_all_section` | `$(grep … <<<"$VAS_OUT")` |
| 3567–3568 | `verify_all` | `$(grep -c -- file)` |
| 3867–3869 | `gate_canonical_capture` | `$(grep -c -- file)` |
| 3913 | `gate_drift_scan` | `$(printf \| grep -oE)` |
| 4188–7428 | selftest helpers `tcase…tchain_audit` | `$(grep … <<<"$out")` |
| 5265–5268 | `tall` | plain file greps |
| 6394, 6396 | `r24_case` | `$(grep -a -c)` / pipeline |
| 7042–7070 | `metadata_registry_*` | herestrings |
| 7572, 7590–7591, 7620–7621 | `c1lk_verify` | `/proc/locks` + file greps |

Non-invocations on grep-bearing lines: :364 (`*"GNU grep"*)` case pattern),
:384 (path list), :388 (`command -v grep` lookup only), :1763 (printf text),
:7240 (`grep() { return 2; }` — the selftest's own fault-injection stub in a
subshell, deliberate and scoped).

No `grep` executes before `grep_pin_init` (:8039): everything before it is a
function body; `metadata_iso_date` (called at :8030) contains no grep;
`--help`/usage paths exit before :8039.

## Tripwire proofs (all with gate sha `1f2fb4f5…`)

Shim: `/tmp/hyaku/chousa-r35/w2/RevGrepSites/shim/bin/grep` — appends to
`trip-path.log`, then `exec /usr/bin/grep`. BASH_ENV shim defines `grep()`.

- `PATH=shim/bin:/usr/bin:/bin bash gate verify-claims claims.jsonl --root fix`
  → rc=1 DRIFT, `trip-path.log` = **0 bytes**, echo
  `GATE_GREP: path=/usr/bin/grep source=default version="grep (GNU grep) 3.12-modified"` (artifacts `t1.out/t1.err`).
- `BASH_ENV=bash_env.sh bash gate verify-claims …` → `trip-fn.log` = **0 bytes**.
- Same PATH shim across `verify`, `verify-chain`, `verify-sweeps`,
  `verify-integrity`, `verify-metadata`, `--pin`, `--drift` → all tripwires 0.
- `PATH=shim/bin … bash gate --selftest` →
  `RESEARCH_GATE_SELFTEST: PASS (256 cases, 0 skipped)`, rc=0, both tripwires
  **0 bytes** (`selftest-shim.out`). This covers every census line including
  the `ns_run`/unshare re-exec and the c1lk flock harness.

Verdict for the census question: **every grep invocation site is pinned by
the `grep()` wrapper; no site bypasses it.** Under a PATH shim the pinned
default `/usr/bin/grep` still runs everywhere (verified empirically, all
modes + selftest).

## FINDING (residual bypass, attack surface beyond c1-count's scenarios)

The wrapper pins *the name* `grep`, but dispatches through two un-pinned
function-resolved words. An attacker who can inject shell functions —
`BASH_ENV` (exactly the channel the counter's own S2/S9 exercise) or exported
`BASH_FUNC_*` env vars — defeats the pin without touching `grep`:

1. **`command()` shadow defeats the dispatch.** `grep()` calls
   `command "$GREP_BIN" "$@"`; bash resolves `command` as a function before
   the builtin. `BASH_ENV` defining `command()` logged all 5 matcher calls
   of `verify-claims` (`trip-cmd.log`), and a `command()` that returns 1 for
   `*grep*` made the gate fail-closed (`rc=2`, "GNU grep with -z/-P support
   is required" in `b3.err` — the pin path was never executed). Exported
   `BASH_FUNC_command%%` (no `BASH_ENV` at all) intercepts identically
   (`trip-env.log`, 5 calls). A hostile `command()` can run any binary or
   fabricate matcher output; the pinned binary need not run.
2. **`head()` shadow defeats provenance verification.** `grep_pin_verify`
   (:361) pipes `"$cand" --version | head -n 1`. `BASH_ENV` defining
   `head() { printf 'grep (GNU grep) 9.9-shim\n'; }` made a stub that
   self-reports `pi-uu-grep` **pass verification** as
   `RESEARCH_GATE_GREP` (trip-stub.log shows the stub then invoked as the
   pin). So the "refuses a pin it cannot verify" half of C1 is also
   fabricable: the verification output is attacker-controlled.

Same defect class: any builtin the pin path calls by bare name (`head`,
`printf`, `command`, `stat`-adjacent) can be function-shadowed. Fix
direction [INFERENCE]: use `builtin command "$GREP_BIN"` (or exec the path
directly — `command` is only there to skip functions, which a named function
bypasses anyway), and capture `"$cand" --version` via a mapfile/`read`
without `head`, or `builtin head`/absolute paths.

Scoping note: these bypasses are not covered by c1-count S1–S9 (which probe
only `grep`-named shims), so P1=9/9 can still hold on this gate — but the
claim text "every grep call in this shell runs that absolute path through the
wrapper" is false in the presence of BASH_ENV/exported-function injection,
the same channel the counter itself ships. The C1 threat model already
admits BASH_ENV (S2/S9), so this is an honest gap in the pin, not an exotic
environment.

## Limits

- Fixture spanned both matchers (short span → :1687 direct; 42006-byte span
  → :1716 chunk) plus `token_matcher_require` :1762; `chain_nearest` :2176
  and `metadata_registry_check_source` :3144/3146 were exercised only by the
  selftest run, not by my fixture.
- The `command()`/`head()` findings were demonstrated on `verify-claims`
  and `grep_pin_verify` only; the same shadow applies process-wide by
  construction. `date -u -r` at :329 and similar pre-init calls are equally
  shadowable but are not grep sites.
- No runtime is claimed for modes outside the shipped gate; all evidence is
  this host, bash 5.x, GNU grep 3.12-modified.

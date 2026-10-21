# ScoutDateCallers — C2 caller map, locale scopes, and the two failing sites

Assigned item: C2 — map callers of `metadata_iso_date` / `metadata_add_days` and the dynamic
locale scopes. Static read-only; no test, gate, selftest, or runtime execution performed.

Receipt (read-only): `git rev-parse HEAD` = `64eec5d41c7cf7f17f5ce1e968e28b3769952596`
(declared round27 base); `sha256sum tools/research-gate.sh` =
`c2c813f1b425bc4e74625a2607eaca1b97addf9898f834e88af8f1fe2143abc6`.
That digest is the exact digest recorded for the r26 target in
`.ufo/waves/round-26/falsify/FDateAsOfUsage.md` and `FDateHugeCadence.md`, so the accepted
FDateAsOfUsage / FDateHugeCadence failures are on these bytes; nothing is rerun here.
`corpus/evidence/round27-regressions.py` sha256 = `2e5fc8af…ed9a`.
Tools installed/updated: none (static read-only item; no package, network, or service action).

All line numbers are `tools/research-gate.sh` in that tree unless stated.

## 1. Leaf date code (no locale pin on any of these functions)

| symbol | lines | locale-sensitive text handling |
|---|---|---|
| `metadata_iso_date` | 2295–2308 | 2296 shape regex `^([0-9]{4})-([0-9]{2})-([0-9]{2})$`; 2297–2298 `$((10#…))` on the matched text |
| `metadata_days_from_civil` | 2310–2321 | arithmetic only |
| `metadata_civil_from_days` | 2324–2336 | arithmetic + `printf` |
| `metadata_days_from_iso` | 2338–2341 | 2339 character slicing, 2340 `$((10#…))` |
| `metadata_add_days` | 2343–2359 | 2345 `metadata_iso_date`; 2346 digits regex `^[0-9]+$`; **2348 `digits=${digits##+(0)}`**; 2350 7-digit bound; 2351 `$((10#$digits))` |

Shell prerequisites: `set -euo pipefail` (255) and `shopt -s extglob` (256). `+(0)` at 2348 is
the only extglob construct used in a parameter expansion; the other `+(` hits (470, 688, 1551)
are ERE group operators in `=~`, and 2385/2594 are numeric `([0-9]+)` groups.

## 2. Complete caller census (repo-wide, excluding `.ufo/` and `.git/`)

`metadata_iso_date` — 5 call sites, all inside this file:

| # | site | enclosing locale scope | status |
|---|---|---|---|
| 1 | 6297 top-level `--as-of` validation (`if (( AS_OF_ARG_SET ))`, 6295–6298) | **none** — inherited process `LC_ALL`/`LANG` | unpinned; the only caller the r26 receipts observed failing |
| 2 | 2720 recheck-token classification | `verify_metadata`, pinned at 2539 | protected dynamically |
| 3 | 2739 literal recheck due date | `verify_metadata`, 2539 | protected dynamically |
| 4 | 2747 `verified_first` guard before day-add | `verify_metadata`, 2539 | protected dynamically |
| 5 | 2345 internal guard in `metadata_add_days` | inherits its caller; the only external caller (2748) is inside 2539 | protected only transitively |

`metadata_add_days` — exactly one call site: 2748 (inside `verify_metadata`, 2539), guarded by
`metadata_iso_date "$verified_first"` at 2747.

`metadata_days_from_iso` — exactly one call site: 2755, after `due_date` was produced by
`metadata_iso_date`/`metadata_add_days` (or is `unknown`/`on-release`, in which case it is not
reached because the branch requires `freshness == current`).

`metadata_days_from_civil` — 2340, 2353, 2355, 2550. `metadata_civil_from_days` — 2358.

No other file in `corpus/`, `tools/`, `lessons/`, or `knowledge/` calls these functions.
`corpus/SOURCES.md:45` only describes them (S035). The r26/r27 harnesses
(`round26-date-differential.sh`, `round27-regressions.py`) reimplement independent oracles and
drive the CLI; they do not source the gate. No external contract is exported.

## 3. Dynamic locale scopes (the map the claim asks for)

| scope site | form | dynamic extent | date relevance |
|---|---|---|---|
| 2539 `verify_metadata` | `local LC_ALL=C` (not exported) | every callee of `verify_metadata`, including 2720/2739/2747/2748→2345/2346/2348/2352-2353 and 2755→2340, plus 2550 slicing/arithmetic | the only protection for entry-side date parsing and for `${AS_OF_ARG:0:4}`-style slicing at 2549 |
| 2366 `metadata_registry_load` | `local LC_ALL=C` (not exported) | registry table parsing and the `/proc/$$/fd` probes at 2385 | no date call; do not remove |
| 1283–1284 `tok_span_at` | `local LC_ALL=C; export LC_ALL` | callee scope + child `sed`/`grep` env | unrelated to dates; the exported form is unnecessary for pure-bash regex |
| 2789 `json_escape` | `local LC_ALL=C` | its own loop and `printf` | unrelated to dates |
| 754, 3266 | `LC_ALL=C sed` / `LC_ALL=C sort` | subprocess only | unrelated |

Global state: `LC_ALL` is never set at top level. The leaf date functions carry no pin, so
caller #1 (6297) executes under the operator's inherited locale — the r26 baseline
(`LANG=en_US.UTF-8`, `LC_ALL`/`LC_CTYPE`/`LC_COLLATE` unset).

Mechanism [INFERENCE from bash semantics, not run this round]: a `local LC_ALL=C` assignment
resets bash's own locale for builtins (including `[[ =~ ]]`) for the dynamic extent, which is
why the entry-side paths are protected while 6297 is not. The only *observed* r26 datum is the
top-level failure; `FDateAsOfUsage.md` itself marks the entry-side protection as inference.
Therefore the fix must not rely on that inference — it should be enforced in the leaf.

## 4. Failure mechanisms (accepted r26 ground truth, not rerun)

FDateAsOfUsage (unpinned CLI, calls 6297 → 2296–2298):
`[0-9]` under `en_US.UTF-8` admits non-ASCII numeric code points, the match succeeds, `10#`
then fails on the matched text. The failing expansion discards the whole `if (( AS_OF_ARG_SET ))`
compound, so `|| die_usage` (exit 2) never runs; execution falls through to `verify_metadata`,
where 2550 aborts under `set -e` → exit 1, no stdout, raw `line 2297` / `line 2550` diagnostics.
A caller reading exit 1 sees DRIFT for a usage error.

FDateHugeCadence (`metadata_add_days`, 2348 → 2350):
`${digits##+(0)}` performs a longest-prefix extglob match whose recursion grows with the
leading-zero run, and it executes *before* the 7-digit bound at 2350. Observed: 64k zeros
8.77 s; ≥68k zeros SIGSEGV (139) with no output, losing every entry's verdict in a directory
scan. 128 KiB of zeros is under the 8 MiB reader cap, so the bound cannot protect the strip.

The all-zero cadence is a distinct branch: r27's `allzero-128k` expects `due=<verified date>`
and `freshness=current`, so the normalization must map an all-zero run to `0`, not to unknown.

## 5. Suggested change (leaf hardening; smallest cut that satisfies the claim text)

```
 metadata_iso_date() {
+  local LC_ALL=C
-  [[ $1 =~ ^([0-9]{4})-([0-9]{2})-([0-9]{2})$ ]] || return 1
+  [[ $1 =~ ^([0123456789]{4})-([0123456789]{2})-([0123456789]{2})$ ]] || return 1
   local year=$((10#${BASH_REMATCH[1]})) month=$((10#${BASH_REMATCH[2]}))
   local day=$((10#${BASH_REMATCH[3]})) maxday=31
   ...
 metadata_add_days() { # VALID_DATE DECIMAL_DAYS -> META_DATE_RESULT; out of range = 1
+  local LC_ALL=C
   local date=$1 digits=$2 year month day start last_day amount
   metadata_iso_date "$date" || return 1
-  [[ $digits =~ ^[0-9]+$ ]] || return 1
-  # Normalize decimal text before bounding; only supported-sized values reach arithmetic.
-  digits=${digits##+(0)}
+  [[ $digits =~ ^[0123456789]+$ ]] || return 1
+  # One linear pass strips the leading-zero run: extglob +(0) recursed per zero and
+  # overflowed the stack before the digit bound below could apply.
+  [[ $digits =~ ^0*([0123456789]*)$ ]] || return 1
+  digits=${BASH_REMATCH[1]}
   [[ -n $digits ]] || digits=0
   (( ${#digits} <= 7 )) || return 1
   amount=$((10#$digits))
```

Invariants this preserves: the empty→`0` mapping (2349) — so `0…0d` stays amount 0; the
7-digit bound (2350) and `10#` decimal parsing (2351, needed by `08d`/`09d`); calendar,
leap, max-span/overflow, and overdue-strictness logic are untouched; `metadata_iso_date` still
returns 1 for empty input (used at 2720/2747 with `''`).

Deliberately not changed: 2539/2366 pins (still needed for 2698/2715/2744/2385), the `10#`
conversions, the `recheck` alternation at 2721, the option parsing 6281–6298, and the
last-wins duplicate `--as-of` behaviour (r26 F2 is a spec gap, outside C2's stated repair).

Why not instead add `LC_ALL=C` at top level: an unlocalized assignment would export for the
whole script and change collation/slicing for unrelated code; and it would not enforce the
"ASCII under any inherited locale" grammar for the function itself. Why not wrap only 6297:
it leaves `metadata_add_days`'s `[0-9]` and extglob strip caller-dependent.

Validation of the linear-strip shape [reported by FDateHugeCadence, not rerun here]: the
`^0*([0-9]*)$`-style replacement there was measured at 256k zeros in 0.19 s, exit 1, correct
`due`. Making the class `[0123456789]` is equivalent under the new `local LC_ALL=C` and is
strict even if the pin is ever dropped.

## 6. Expected observable outcomes (mapped to persisted controls)

`corpus/evidence/round27-regressions.py` (C2 block, lines 92–120):

| control (line) | expected after fix |
|---|---|
| `leading-128k-zeros` (94), 131072 zeros + `90d`, V 2026-01-02, as-of 2026-10-21 | `due=2026-04-02 freshness=overdue`, exit 1, exactly one `^RESEARCH_GATE: ` and one `^META entry=` |
| `allzero-128k` (95) | `due=2026-01-02 freshness=current`, exit 0 |
| `huge-magnitude` (96), 40 nines | `due=unknown freshness=unknown`, exit 0 |
| `max-span` (97) `0003652058d` | `due=9999-12-31`, current |
| `overflow-span` (98), `max-date-overflow`, `invalid-verified-date` | unknown, exit 0 |
| `decimal08`, `decimal09-overdue` | decimal, `10#` semantics unchanged |
| `leap-1900/2000/2028/2100` | Feb 28 + 1d rolls as before |
| `ascii-cli-{C,en_US.UTF-8}-{２０２６-10-21, ٢٠٢٦-10-21, 2026-10-2１}` (114–119) | exit 2, one `--as-of must be a valid YYYY-MM-DD date` on stderr, none of `invalid integer` / `arithmetic syntax` / `cannot change locale`, zero `^RESEARCH_GATE: ` lines |

In-gate selftest C2 nodes (5983–6136, `metadata_asof_case` / `metadata_asof_usage_case`):
`metadata-asof-large-cadence` (36 nines → unknown), `leap-2028` (`0001d`), `date-overflow`
(`9999-12-31` + `1d`), `invalid-verified-date`, `boundary` (`as-of == due` stays current), and
the three usage cases at 6083–6088 must stay byte-identical in expectation.

`corpus/evidence/round26-date-differential.sh`: builds ASCII `--as-of` values only, copies
`os.environ` without touching `LC_ALL` (90–105), so results must be unchanged by the leaf fix.

## 7. Coupling and no-harm notes

- `round27-regressions.py:70` extracts the `metadata_asof_usage_case` helper by the literal
  regex `^  metadata_asof_usage_case\(\).*?^  }\n`; the C2 edit is confined to 2295–2359, but
  do not re-indent that helper (C1 lane owns its body).
- The `en_US.UTF-8` controls require that locale to exist on the runner. r26 observed
  `C`, `C.utf8`, `en_US.utf8` installed. If absent, bash itself prints
  `cannot change locale` at process start, which the control forbids; that would be an
  environment failure, not gate behaviour. The `C` row is the authoritative one.
- `local LC_ALL=C` in `metadata_iso_date` also covers `metadata_add_days`'s re-validation at
  2345, but the explicit pin in `metadata_add_days` is still wanted for its own `[0-9]` regex
  and for any future caller.
- Do not remove `shopt -s extglob` (256) as part of this fix: it is global shell state and the
  claim does not ask for it; the single construct is replaced in place.

## 8. Unrun checks (L1/executor only; I ran none)

1. `bash tools/research-gate.sh --selftest` once after integration (C1 full selftest owner).
2. `python3 corpus/evidence/round27-regressions.py --gate tools/research-gate.sh` on an
   isolated base archive (with the accepted long-token baseline skip per round27 claims) and
   on the final tree.
3. `bash corpus/evidence/round26-date-differential.sh tools/research-gate.sh` (isolated copy).
4. The locale matrix under `C`, `C.UTF-8`, and `en_US.UTF-8` for the three Unicode-digit
   tokens (the regression script covers C and en_US.UTF-8; `C.UTF-8` is an extra margin).

## 9. Observed / inference / open

Observed (this round, static): caller census, line numbers, locale-scope extents, and the
digest match with the r26 target.
Inference: that `local LC_ALL=C` at 2539 fully protects the entry-side `=~` sites under
UTF-8 — reported as inference in r26 and not re-observed here; the leaf fix makes it moot.
Open: none for the caller map. The duplicate `--as-of` last-wins gap (r26 F2) remains
unchanged by design; the claims do not include it in C2's repair set.

# ScoutDateZero — C2 leading-zero decimal normalization, safe alternatives

Seat: ChousaR27.ScoutDateZero (leaf, static read-only). Base observed: committed
master `64eec5d41c7cf7f17f5ce1e968e28b3769952596` (`git show 64eec5d:tools/research-gate.sh`).
No production edit, clone, patch, Git/jj write, gate/selftest/regression/date-differential
run, network, host-file, `/proc`, debugger, or live-process probe. No tools installed or
updated. All line numbers below are committed-base line numbers; the lane-root working
tree currently has uncommitted C1 additions above line 6000 only, so the metadata region
is byte-identical to the base.

## Assigned question

C2: analyze safe alternatives for the leading-zero decimal normalization in
`metadata_add_days` without recursion/termination on a very long zero run, preserving
the existing decimal, all-zero, range and overflow semantics. No execution.

## Observed facts (source of base `64eec5d`)

Current implementation, `tools/research-gate.sh:2343-2358`:

```
2343  metadata_add_days() { # VALID_DATE DECIMAL_DAYS -> META_DATE_RESULT; out of range = 1
2344    local date=$1 digits=$2 year month day start last_day amount
2345    metadata_iso_date "$date" || return 1
2346    [[ $digits =~ ^[0-9]+$ ]] || return 1
2347    # Normalize decimal text before bounding; only supported-sized values reach arithmetic.
2348    digits=${digits##+(0)}
2349    [[ -n $digits ]] || digits=0
2350    (( ${#digits} <= 7 )) || return 1
2351    amount=$((10#$digits))
...
2357    ((amount <= last_day - start)) || return 1
2358    metadata_civil_from_days "$((start + amount))"
```

- `shopt -s extglob` is global at `:256`; `+(0)` at `:2348` is the only extglob
  construct in the file (`grep -nF '+('` returns only `:2348`). The strip therefore
  runs before the `:2350` seven-digit bound, so the bound cannot protect it.
- Locale scope: `verify_metadata` pins `local LC_ALL=C` at `:2539`; the only caller
  of `metadata_add_days` is `:2747-2748` inside that dynamic scope. The cadence token
  itself is captured at `:2741-2742` (`^([0-9]+)d$`) under the same pin.
- `metadata_iso_date` (`:2295-2307`) has **no** function-local locale pin and is also
  called from the top-level `--as-of` validation at `:6295-6297`, outside
  `verify_metadata`'s scope. This is the separate FDateAsOfUsage site (C2 locale), not
  the normalization site, but a normalization fix must not depend on it.
- `metadata_add_days` is called only from `:2748`; plain mode (`--as-of` absent)
  never enters the freshness block at `:2737`, so the strip is opt-in.
- Accepted r26 receipt (not rerun): `.ufo/waves/round-26/falsify/FDateHugeCadence.md`
  records SIGSEGV/exit 139 with no output at ≥68,000 leading zeros, 8.77 s at 64,000
  zeros, and `MISMATCH 0 of 24` for its `[[ $digits =~ ^0*([0-9]*)$ ]]` candidate
  including 256k zeros at 0.19 s and correct 16k/64k/256k outputs. That receipt is the
  empirical ground truth for this item; I did not reproduce it.
- r27 synthetic controls observed (file in flight during read; snapshot mtime
  2026-10-21 11:39:12, size 10046) in `corpus/evidence/round27-regressions.py:96-104`:
  `leading-128k-zeros` (131072 zeros + `90d`, verified 2026-01-02, as-of 2026-10-21,
  due 2026-04-02, exit 1), `allzero-128k` (131072 zeros + `d`, due = verified
  2026-01-02, current, exit 0), `huge-magnitude` (40 nines → unknown), `max-span`
  (`0003652058d` from 0001-01-01 → 9999-12-31, current), `overflow-span`
  (`3652059d` → unknown), `max-date-overflow`, `decimal08`, `decimal09-overdue`.
  The Unicode `--as-of` controls are at `:117-122` and require exit 2 with no
  arithmetic diagnostics.

## Semantics the replacement must preserve (derived from :2346-2358)

| Input class | Required behavior | Reason |
|---|---|---|
| ASCII digits only, nonempty | accepted | `:2346` guard |
| All zeros, any length (incl. 128 KiB) | significant text empty → decimal `0`; `:2349` sets `0`; due = verified date; range check passes | r27 `allzero-128k` |
| Leading zeros + ≤7 significant digits | value = significant suffix; `:2350` passes; `:2357` decides range | r26 z40/`0003652058` controls |
| ≥8 significant digits | rejected by the 7-digit bound → `return 1` → `due=unknown freshness=unknown` | max span is 3,652,058 (<10^7); `0003652059` is the first overflow |
| `08`, `09`, `010`, `0777` | decimal 8/9/10/777, never octal | `10#` at `:2351` |
| Non-ASCII digits (U+FF10 etc.) | must not reach arithmetic; fail closed (`return 1`) rather than `10#` error | FDateAsOfUsage; `[0-9]` range admits 1050 code points in en_US.UTF-8 per the r26 enumeration |
| Non-digit / empty token | `return 1` (empty must stay `return 1`, not 0) | `:2346` contract |

The 7-digit bound is exactly sufficient: the largest representable span is
3,652,058 days (0001-01-01 → 9999-12-31), which the r27 `max-span` control encodes as
`0003652058`. Eight or more significant decimal digits can never pass `:2357`.

## Alternatives evaluated (static)

| # | Technique | Stack/termination | Locale | Evidence | Verdict |
|---|---|---|---|---|---|
| A | `digits=${digits##+(0)}` (current) | **unsafe**: extglob longest-prefix matcher recurses with the zero-run length (r26 receipt) | extglob syntax, locale-independent | accepted SIGSEGV receipt | reject |
| B | `[[ $digits =~ ^0*([0123456789]*)$ ]]` then `digits=${BASH_REMATCH[1]:-}` | no recursion; one ERE pass, `0*` is a DFA scan; capture is a plain substring | literal bracket list matches only the ten listed characters (POSIX: a bracket expression of literal chars matches those chars) | r26 candidate measured 256 KiB → 0.19 s, 24/24 oracle | **recommended (minimal)** |
| C | `[[ $digits =~ ^0*([0123456789]{0,7})$ ]]` then capture / `0` | as B, and the 7-digit bound is structural (the capture itself can never exceed 7 chars) | as B | same ERE engine; bound is a constant-size interval | equivalent, slightly tighter |
| D | `zeros=${digits%%[!0]*}; digits=${digits#"$zeros"}` (keep `:2350`) | no recursion; fixed-length pattern, only a trailing `*`, which bash's matcher short-circuits; O(n) bracket probes | `[!0]` is a literal class; locale-independent | same idiom already in production at `:2418`, `:2426`, `:2493` on registry lines | **safe fallback; no long-run measurement** |
| E | `while [[ $digits == 0* ]]; do digits=${digits#0}; done` | each iteration copies the remaining string → O(n²) bytes (128 KiB ≈ 8 GiB of copying at n=131072) [INFERENCE] | fine | — | reject on cost |
| F | per-character loop `${digits:i:1}` | O(n) bash interpreter iterations; 131072–8M iterations [INFERENCE] | fine | — | reject on cost |
| G | pass `10#000…090` directly, or `printf '%d'` | `10#` on unbounded text terminates/errors; r26 `nobound` control observed `10#: invalid integer constant` at 40 nines and a silent 2^64+90 wrap to 90 | fine | accepted negative control | reject |
| H | external `sed`/`tr` per entry | correct but forks per entry; `tr -s 0` would also collapse interior zeros (`100`→`10`) and change semantics | process-dependent | — | reject |

Why B is safe (not merely observed): the pattern has one unbounded quantifier over a
single-character class and one bounded literal class, so the matcher's work is a
per-character state walk, not per-character recursion; the capture is materialized once.
Why C is equivalent: `^0*` greedily consumes every leading zero, `[0123456789]{0,7}`
consumes the at-most-seven significant digits, and `$` then forces the string to end, so
a token with ≥8 significant digits cannot match; an all-zero token matches with an empty
capture and must be mapped to `0`. Why D is safe: the only repetition in `[!0]*` is the
trailing star, and bash's matcher returns immediately after a trailing star, so the cost
is a fixed probe per start position; no pattern grows with the input.

## Suggested change (for the C2 executor; exact text)

Minimal form, keeping the existing guard, bound and arithmetic order unchanged:

```
  [[ $digits =~ ^[0123456789]+$ ]] || return 1
  ...
  # Capture the significant suffix in one ERE pass; extglob recurses on long zero runs.
  [[ $digits =~ ^0*([0123456789]*)$ ]] || return 1
  digits=${BASH_REMATCH[1]:-}
  [[ -n $digits ]] || digits=0
  (( ${#digits} <= 7 )) || return 1
```

Plus `local LC_ALL=C` as the first declaration of `metadata_add_days` (defense in
depth; the caller already pins it, and the pin makes the `${#digits}` byte count and
`10#` deterministic). Keep `amount=$((10#$digits))` and the `:2357` range check
untouched. Do **not** rely on extglob and do not remove `shopt -s extglob` globally.

Tighter variant (single pass; the seven-digit bound becomes structural and `:2350`
becomes redundant and may be deleted):

```
  [[ $digits =~ ^0*([0123456789]{0,7})$ && -n $digits ]] || return 1
  digits=${BASH_REMATCH[1]:-}
  [[ -n $digits ]] || digits=0
```

The `&& -n $digits` preserves the old empty-token rejection, because the ERE alone
would match an empty string. If the executor prefers no regex at all, form D with the
ASCII literal guard is semantically identical:

```
  [[ $digits =~ ^[0123456789]+$ ]] || return 1
  local zeros=${digits%%[!0]*}
  digits=${digits#"$zeros"}
  [[ -n $digits ]] || digits=0
  (( ${#digits} <= 7 )) || return 1
```

Two hardening details that apply to any captured form:

- Use a literal class `[0123456789]`, not `[0-9]`. Under `en_US.UTF-8`, `[0-9]` is a
  collating range that admitted 1050 code points in the r26 enumeration; a literal
  list is the declared ASCII grammar. With the new `local LC_ALL=C` the two are equal
  today, but the literal class keeps the helper safe if the pin is ever moved or the
  helper is reused.
- Write `${BASH_REMATCH[1]:-}`. A group that participates with an empty match (the
  128 KiB all-zero cadence) is assigned an empty string in bash [INFERENCE from bash
  semantics]; `:-` makes the code independent of that detail under `set -euo pipefail`,
  turning a hypothetical unset element into the intended `0` path instead of an abort.

## Alignment with the current executor candidate (observed in its clone, not verified)

`.ufo/waves/round-27/work/ExecDates/tools/research-gate.sh` currently contains
`local LC_ALL=C` in `metadata_iso_date` and `metadata_add_days`, and replaces `:2348`
with `[[ $digits =~ ^0*([0-9]*)$ ]]` / `digits=${BASH_REMATCH[1]}`. That is the
r26-measured candidate and satisfies the non-termination requirement. The two edits
above (`[0123456789]`, `:-`) are the only hardening I would add; the separate
`{0,7}` variant is optional. Its added selftests (`metadata-asof-128k-zero-prefix`,
`metadata-asof-all-zero-cadence`, locale-selected Unicode usage case) match the r27
control intents. No claim is made here that that working tree passes anything; it was
not executed.

## Expected outcomes against the r27 controls (if the suggested change lands)

| Control | Path | Expected |
|---|---|---|
| `leading-128k-zeros` | `0*` consumes 131072 zeros, capture `90`, length 2, amount 90, range passes | `due=2026-04-02 freshness=overdue`, exit 1, one `META` line, one anchored verdict |
| `allzero-128k` | capture empty → `0`, amount 0 | `due=2026-01-02 freshness=current`, exit 0 |
| `huge-magnitude` | 40 significant digits fail the 7-digit bound | `due=unknown freshness=unknown`, exit 0 |
| `max-span` | capture `3652058`, equal to `last_day - start` | `due=9999-12-31 freshness=current`, exit 0 |
| `overflow-span` | amount 3,652,059 > span | `due=unknown`, exit 0 |
| `max-date-overflow` | verified 9999-12-31, span 0 | `due=unknown`, exit 0 |
| `decimal08` / `decimal09-overdue` | capture has no leading zero; `10#` | 2026-01-09 current; 2026-01-10 overdue at as-of 2026-01-11 |
| Unicode `--as-of` | `metadata_iso_date` pin (executor change) rejects before `10#` | exit 2, usage message, no verdict, no `invalid integer constant`/`arithmetic syntax error` |
| plain mode | freshness block never entered | output identical to base |

## Not run (L1 owns after integration)

`python3 corpus/evidence/round27-regressions.py --gate tools/research-gate.sh`;
`bash corpus/evidence/round26-date-differential.sh`;
`bash tools/research-gate.sh --selftest`; any 8 MiB-scale timing probe. The r26
long-token crash reproduction was not rerun; it is cited from the accepted receipt.

## Remaining unknowns

- ERE scan cost at the 8 MiB reader cap: the receipt's three points (16k/64k/256k →
  0.02/0.03/0.19 s) do not determine the exponent; an 8 MiB zero run is plausibly
  multi-second [INFERENCE, low confidence]. The required 128 KiB control is far below
  that. Form D (glob) likely has a smaller constant but has no long-run receipt.
- `${BASH_REMATCH[1]}` definedness for an empty participating group under `set -u`
  [INFERENCE]; `:-` removes the dependency.
- Literal bracket-list locale behavior outside glibc/bash [INFERENCE from POSIX
  bracket semantics; not probed].
- `corpus/evidence/round27-regressions.py` was being written while I read it; the case
  names and values above are from the 11:39 snapshot and must be read from the final
  file at run time.

## Correction appended after creation — grep justification only

The sentence in "Observed facts" saying that `grep -nF '+('` returns only `:2348` is
wrong and is withdrawn. `+(` also occurs as an ERE quantifier immediately before a
group at `:470`, `:688`, `:1551`, `:2385` and `:2594`. The narrow check is:
`git show 64eec5d:tools/research-gate.sh | grep -nF '+(0'` returns exactly `:2348`.
The `*(` matches at `:769`, `:771`, `:836`, `:2525`, `:2715`, `:2744`, `:2909` and
`:2911` are quantifier-plus-group text inside `=~` right-hand sides or `grep -E`
patterns, where extglob syntax is not active. The substantive statement therefore
stands: the base has one extglob use (`+(0)` at `:2348`), and no other report claim
depends on the withdrawn wording.

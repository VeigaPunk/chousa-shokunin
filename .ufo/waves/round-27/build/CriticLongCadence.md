# CriticLongCadence — C2 attack on decimal normalization: long leading-zero runs, huge magnitudes, all-zero cadences (round 27, attempt 1)

Seat `ChousaR27.CriticLongCadence`. This is advice for the author lane only, not an admission. Judged on freshness (C2), with operability and calibration as side axes.
Base: `64eec5d4`. Static read only. I ran no gate, selftest, or differential. I installed no tools.
Patch status when I looked: `.ufo/waves/round-27/patches/` and `work/` did not exist yet, so no ExecDates diff was available. The attacks below target the base code and the fix shapes the ExecDates prompt describes ("stack-safe decimal normalization that preserves arbitrary leading zeros"). They also target the r26 sandbox candidate.

## Attack surface (base)

- `tools/research-gate.sh:2348`: `digits=${digits##+(0)}`. This is the only extglob operator in the file. I grepped for `+( *( ?( @( !(` and every other hit is an ERE inside `=~`. Extglob is enabled globally at `:256`.
- `:2346` guard `^[0-9]+$` → `:2348` strip → `:2349` empty→0 → `:2350` bound `${#digits} <= 7` → `:2351` `10#` → `:2357` range check against 9999-12-31.
- Only one caller: `:2748`, under `--as-of`, inside `verify_metadata`'s dynamic `local LC_ALL=C` (`:2539`). Plain mode never reaches `metadata_add_days`.
- Accepted r26 receipt (`.ufo/waves/round-26/falsify/FDateHugeCadence.md:46-53`): SIGSEGV at ≥68,000 zeros. At 64k zeros a run took 8.77 s, which is quadratic growth.

## Counterexamples a fix must survive

Every row uses a synthetic entry with `verified-at: V checked` and `recheck: <token>`. The expected values come from Python `date + timedelta(int(tok,10))`; an overflow means `unknown`.

| # | token (Z = `"0"*131072`, which is 128 KiB) | V → as-of | must yield | defect it catches |
|---|---|---|---|---|
| K1 | Z+`90d` | 2026-01-02 → 2026-10-21 | `due=2026-04-02 freshness=overdue`, rc1, `FINDING META_RECHECK_OVERDUE` | recursive strip (crash or slow); a length pre-bound placed before the strip (would give `unknown`) |
| K2 | Z+`90d` | 2026-01-02 → 2026-04-02 | `due=2026-04-02 freshness=current`, rc0 | strict `>` overdue semantics |
| K3 | Z+`d` (all zeros) | 2026-10-20 → 2026-10-21 | `due=2026-10-20 overdue`, rc1 | empty-after-strip treated as invalid; must normalize to 0 |
| K4 | Z+`d` | 9999-12-31 → 9999-12-31 | `due=9999-12-31 current`, rc0 | zero span at the upper boundary (`0 <= last_day-start = 0`) |
| K5 | Z+`10d` / `000100d` | 2026-01-02 | 2026-01-12 / 2026-04-12 | over-stripping: `${d//0/}`, `${d##*0}`, or a trailing strip turns 10 into 1 or "" |
| K6 | `"0"*65536+"1"+"0"*65536+"d"` | 2026-01-02 | `unknown`, rc0 | a global zero delete would give 1 day; the true value is 10^65536 |
| K7 | Z+`3652058d` | 0001-01-01 → 9999-12-31 | `due=9999-12-31 current` | maximum representable span, combined with a long prefix |
| K8 | Z+`3652059d` | 0001-01-01 | `unknown` | overflow by one |
| K9 | Z+`18446744073709551706d` (2^64+90) | 2026-01-02 | `unknown`, **not** 2026-04-02 | dropping the 7-digit bound makes `10#` wrap (r26 nobound mutant `:170`) |
| K10 | `"9"*131072+"d"` | 2026-01-02 | `unknown`, rc0, no stderr | linear path for long *non-zero* tokens; no `10#` on unbounded text |
| K11 | `d`, `0x5d`, `-1d`, `٩٠d` | any | `recheck=unscheduled due=unknown` | strip regex accepting empty input; non-ASCII digits |

All of K1–K11 must also produce exactly one `^RESEARCH_GATE: ` line, empty stderr, and an rc in {0,1}.

## Findings on candidate fixes

**F1 — r26 sandbox candidate `[[ $digits =~ ^0*([0-9]*)$ ]]; digits=${BASH_REMATCH[1]}` (FDateHugeCadence.md:107). Fixable defect.**
- The strip depends on POSIX submatch disambiguation: `0*` versus `[0-9]*` both accept leading zeros. glibc happened to give the zeros to `0*` (the r26 run was 24/24, and 256k zeros took 0.19 s), but nothing in the pattern forces that. If group 1 kept the zeros, the K1, K3 and K7 rows would silently become `unknown` with no crash. That is a calibration regression the selftest might not notice.
- The `[[ … ]]` result is unchecked. When a bash `=~` fails it clears `BASH_REMATCH`, so `digits=""` and then `:2349` sets it to `0`. Any non-match would therefore silently become a zero-day cadence (`due=verified`, which reads as `freshness=current`). That is a false-fresh result, not an unknown.
- Smallest safe correction: write the pattern so it has only one parse, and fail closed:
  `[[ $digits =~ ^0*([1-9][0-9]*)?$ ]] || return 1; digits=${BASH_REMATCH[1]:-0}`
  Keep the `:2346` `^[0-9]+$` guard before it, so the empty string is never accepted (K11). Keep `(( ${#digits} <= 7 ))` *after* it (K1, K9).

**F2 — loop strip `while [[ $digits == 0* ]]; do digits=${digits#0}; done`. Reject.** Each iteration copies the remainder, so 128 KiB costs about 131072 × 64 KiB ≈ 8 GiB of memmove [INFERENCE, static]. At the 8 MiB reader cap (`:271`) it is effectively non-terminating. It gives the same "slower, less bounded mode" harm that r26 recorded at 64k.

**F3 — non-regex strip `zeros=${digits%%[!0]*}; digits=${digits:${#zeros}}`. Acceptable alternative.** It uses no extglob operator, and the match is a bracket plus a trailing `*`, so it exits early at the first non-zero character. Time is O(n) and stack depth is constant [INFERENCE, static; never measured]. For an all-zero token, `zeros` is the whole token and `digits` becomes `""`, which `:2349` turns into 0 (K3). It does not allocate glibc `regexec` submatch state, so its memory use is lower than F1. Choose F1-corrected or F3, and record which one was measured.

**F4 — "bound the raw length first" (for example, refuse tokens over 7 characters or over some KiB). Reject.** It breaks K1, K3 and K7. The claim requires that "a long decimal cadence with leading zeros must compute its representable value". Only the *normalized* length may be bounded.

**F5 — "drop the 7-digit bound and rely on the `:2357` range check". Reject.** `10#` wraps or errors before the range check runs (K9, K10). The 7-digit bound is correct because the largest span, 3,652,058 days, has 7 digits.

**F6 — `$((10#$digits))` on the raw token (leading zeros contribute nothing, so no strip). Reject.** User text reaches arithmetic without a length bound, and K9 wraps.

## Making the control independent (calibration)

- **Stack-size masking.** The old crash depends on `ulimit -s`; the receipt was taken at 8192 KiB. Under a larger or unlimited stack, base code produces the *correct* K1 output, only slowly (≈37 s by quadratic extrapolation from 8.77 s at 64k [INFERENCE]). A control that checks only output and rc therefore loses its independence from the bug. The regression script and selftest SHOULD put a wall-clock cap on the K1 run (≈10 s) and SHOULD NOT raise `ulimit -s`.
- **Exact size.** "128KiB" means 131072 zeros, not the 128,000 used in the r26 table. Generate the fixture at runtime with `printf`/`head -c … /dev/zero | tr`, or with Python `"0"*131072`. A heredoc literal would add 128 KiB to `research-gate.sh` and shift `gate_sha256`.
- **Expectation strength.** `metadata_asof_case` (`:5983-6008`) matches by substring. K1 MUST expect `due=2026-04-02 freshness=overdue` and rc1, plus the FINDING line. Expecting `due=unknown` would weaken the claim. `metadata-asof-large-cadence` (`:6108-6116`, 36 nines) and `leap-2028` (`0001d`) stay unchanged.
- **Baseline skip scope.** The counting script's base-archive skip (claims `:22`) MUST name only the crash-reproducing long-zero cases (K1–K5, K7 at 128 KiB). K8–K11 and the short cases are safe on the base and must still run there. The final run must have no skip path.

## Residual limitations (inherited; report them, do not claim them fixed)

- Tokens near the 8 MiB cap still pass through capturing EREs at `:2715` and `:2741`, and through the F1 regex if it is chosen. glibc allocates O(n) submatch state for these, roughly tens of MiB per call [INFERENCE]. Only the 128 KiB case is required; do not claim near-cap time or memory behavior without measuring it.
- `metadata_add_days` relies on the caller's dynamic `LC_ALL=C` for `[0-9]`. If ExecDates adds a helper-local C locale (the CriticLocale domain), it should cover this function too, or use explicit `[0123456789]` lists. Do not disable extglob globally to fix `:2348`; just remove the operator.

## Impacted axes

Freshness (primary). Operability: exit 139 falls outside the 0/1/2 contract, and one bad entry wipes every other verdict in the directory. Calibration: the F1 ambiguity and unchecked match, and the stack-masked control.

## Checks not run (for L1)

- `bash tools/research-gate.sh --selftest`
- `python3 corpus/evidence/round27-regressions.py --gate tools/research-gate.sh` on the base archive (with the named skip) and on the integrated tree
- `bash corpus/evidence/round26-date-differential.sh`
- the plain-mode frozen hash and rc
- the K1 wall-time cap under the default `ulimit -s`

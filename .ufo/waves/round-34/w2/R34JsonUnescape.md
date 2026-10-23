# R34JsonUnescape — differential test of rewritten `json_unescape` (landed vs base)

Seat: chousa lane r34 w2 residual falsify call. Scope: ExecC1BuildC landed gate
`3026a4e5bb4c44c01982fd67bd0140df36384942` (`tools/research-gate.sh`, SHA-256
`772a1d8e4d94dbf3…3e58`) vs base gate `b8053900` (SHA-256 `43a1af35…4346`,
=`git show b8053900:tools/research-gate.sh`). Both SHAs verified at extraction time.

## What I did

1. Extracted both `json_unescape` definitions verbatim (lines 1329–1380 landed,
   1329–1367 base) into scratch harnesses:
   - `/fast/scratch/hyaku/chousa-r34/w2/R34JsonUnescape/harness_landed.sh`
   - `/fast/scratch/hyaku/chousa-r34/w2/R34JsonUnescape/harness_base.sh`
   - Verbatim extraction verified: `diff` of sed-sliced gate lines vs harness body
     reported `LANDED_FN_VERBATIM` / `BASE_FN_VERBATIM` (bash 5.3.20).
2. Generated corpus of **1070 random JSON string bodies** (`gen_corpus.py`, seed
   20261023): sizes 0–64357 bytes (3 595 246 bytes total; **80 cases ≥16 KiB**,
   max ≈63 KiB). Coverage: escapes `\\ \" \/ \b \f \n \r \t`; `\uXXXX` valid
   (ASCII, BMP, high-plane), surrogate pairs, lone surrogates, swapped/malformed
   pairs; invalid hex (`\u12G4`, `\u123`, bare `\u`); trailing lone backslash;
   invalid escapes (`\q`, `\x`, `\ `, `\1`…); empty body; long plain runs and
   escape-dense runs up to 64 KiB.
3. Differential run (`run_diff.sh`, `xargs -P8`, per-case `timeout 120`):
   - `LC_ALL=C`: **1070/1070 OK** — byte-identical stdout (`cmp`), equal exit
     codes (all 0/0), no timeouts. Summary: `out_c_locale/summary.txt`.
   - `en_US.UTF-8` (LANG default): **1070/1070 OK** — same. Summary:
     `out_enUS_utf8/summary.txt`. No `nonok.txt` files were produced (absent).
4. Reference sanity (not differential): landed output vs Python `json.loads`
   decode for the 445 non-surrogate corpus cases — **439/445 byte-identical**;
   the only 6 mismatches are `\u0000`-containing cases where bash variables
   cannot hold NUL (truncates to empty) — behavior identical in **both** gates
   (same `printf -v c '%b' "\\$(printf '%03o' …)"` line in both), so not a
   regression. 139 cases were not JSON-parseable (deliberate invalid escapes) —
   excluded by design.

## Timing (median of 3 runs, LC_ALL=C, serial, clean machine)

| input (escape-dense) | landed | base | ratio |
|---|---|---|---|
| 16 KiB (`long16.in`) | 0.064 s | 0.265 s | 4.1× |
| 32 KiB (`long32.in`) | 0.207 s | 0.925 s | 4.5× |
| 64 KiB (`long64.in`) | 0.776 s | 3.744 s | 4.8× |
| 64 KiB plain (`plain64.in`) | 0.003 s | 3.402 s | ~1100× |

Base scales superlinearly (16→32→64 KiB: 0.265→0.925→3.744, ≈4× per doubling =
quadratic); landed is near-linear. All timing runs exited rc=0 (raw `timing.txt`
in artifact dir). Note: an earlier pre-differential calibration on a loaded
machine showed base 64 KiB at 21.3 s; clean-run numbers above are the reported
ones.

## Findings (by severity)

- **No actionable finding.** The rewrite is byte-identical to the base gate on
  all 1070 differential cases in both `LC_ALL=C` and `en_US.UTF-8`, with
  identical exit codes (0/0). Surrogate handling (lone + pair → `?`/`??`,
  never combined to astral) is unchanged from base. `\u0000` NUL truncation is
  unchanged from base.

## Residual risk / verification gaps

- Differential + reference covers the declared input space but is not an
  exhaustive spec audit (e.g., surrogate pairing semantics are inherited from
  base, not fixed — out of scope for this differential).
- Timing numbers are wall-clock on a shared host; ratios are the signal, not
  absolute seconds.

## Artifacts / installs

- Lane artifact dir: `.ufo/waves/round-34/w2/R34JsonUnescape/` —
  `timing.txt`, `summary_c_locale.txt`, `summary_enUS_utf8.txt` (all <1 MiB).
- Full scratch working set (corpus, harnesses, scripts, outputs):
  `/fast/scratch/hyaku/chousa-r34/w2/R34JsonUnescape/`.
- No tools installed (no installs recorded for this run).

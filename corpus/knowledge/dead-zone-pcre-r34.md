# The PCRE dead zone under the argv limit (round 34, attempt 2)

Source: S065 (pcre2limits(3), PCRE2 10.49, installed `/usr/share/man/man3/pcre2limits.3.gz`,
sha256 `a3ea2c67…74bd6`; re-opened 2026-10-23, pins unchanged).

## The two ceilings of the one-pattern span matcher

`verify-claims` transports a span to grep(1) as one PCRE pattern of four bytes per span byte
(one `\xHH` escape each). Two independent ceilings bound that path:

1. **execve(2) per-string limit** — `MAX_ARG_STRLEN` is 32 pages (131072 bytes including NUL);
   the pattern for a span of 32768 bytes is 131072 argv bytes, so exec fails with E2BIG
   ("Argument list too long"). Round 34 C1's surface (S064).
2. **PCRE2 compiled-pattern ceiling** — "approximately 64 thousand code units" for the 8/16-bit
   libraries (S065). On this host the ceiling binds at a span of 32765 bytes — **before** the
   argv ceiling. The per-byte code-unit ratio is build-specific and not claimed (ExecC2Rerun D3).

Measured on this host (2026-10-23, gate `772a1d8e`, probes in
`/fast/scratch/hyaku/chousa-r34-a2/probe/`): a pattern for a **32764-byte** span compiles and
matches; **32765, 32766 and 32767** fail with `grep: regular expression is too large` (grep
exits 2, no occurrence is reported). The failure is length-only: space-joined words,
newline-dense, punctuation-dense, single-byte and escape-dense spans all fail in the same
3-byte window. Spans of 32768 bytes and more take the chunk matcher (round 34 C1) and verify.

## Consequence (fixed)

Spans of **32765..32767 bytes** — three lengths just under the argv limit — read
`observed=unsupported` with `CLAIM_SPAN_NOT_FOUND` even when the source holds the span
verbatim. The SCORECARD's planned-r35 entry had hypothesised the window "about 28000–32767";
the measured window is exactly three lengths. Fix: `TOK_DIRECT_SPAN_MAX` lowered from 32767 to
32764 so the window routes onto the chunk matcher (design v4, `claims-a2.md`; counter
`c2-count.py`, `DEADZONE_MATCH=37/37` on seeds 5011/5023/5033/5047, gate `a6307edf…`).

## Limits

- The 32765 boundary is a host measurement (PCRE2 10.49-1, default build); another PCRE2 build
  may bind a few bytes earlier or later. The lane's selftest pins THIS host's window with cases
  at 32765, 32766 and 32767 bytes; on a host with a lower ceiling the 32764 ceiling itself
  would need re-measuring (the counter's short-control classes would catch a shift upward, not
  downward).
- The chunk matcher's probe is the span's first 4096 bytes; sources where a 4096-byte chunk
  occurs hundreds of times could be slow (named limit carried from C1).
- Quote anchors in `verify-chain` share the matcher; a 32765..32767-byte quote anchor now
  resolves where before it read `anchor-missing` (disclosed behaviour change of the same class
  as C1's: a false-negative E2BIG/large-pattern error becomes a verdict).

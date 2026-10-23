# R34 Review — ExecC1BuildC (ruled 3026a4e5bb4c44c01982fd67bd0140df36384942)

Reviewer: ChousaR34.R34ReviewPatchC (UFO-FSD seat). Scope: line-by-line review of the landed
candidate patch (tools/research-gate.sh, SHA-256 `772a1d8e4d94dbf3a44a64bf850b1324e51546eeb62abcd7b3ec585f0e003e58`),
attacking the long-span matcher (`tok_span_offsets_chunk`/`tok_span_offsets_direct`), the rewritten
`json_unescape`, the hex-pattern build, and selftest. All experiments ran in
`/fast/scratch/hyaku/chousa-r34/w2/R34ReviewPatchC/` (clone at tip + clone at base `b8053900`).
No lane/fleet writes; no tools installed.

## What I ran

1. Selftest on the tip clone: `bash tools/research-gate.sh --selftest` →
   `RESEARCH_GATE_SELFTEST: PASS (253 cases, 0 skipped)`, rc 0 (53.87 s). Acceptance met.
2. Counter v3 (`corpus/evidence/round34/c1-count-v3.py`, sha256 `970cf9a7…2da2a`) on the landed
   gate, two fresh seeds, `C1_TMP`/`TMPDIR` in scratch, `LC_ALL=C`:
   - seed 912345678 → `LONGSPAN_MATCH=42/42`, `predicate_holds:true`, gate_rc 1 with
     `RESEARCH_GATE: DRIFT`, elapsed 47.47 s; receipt `receipt-s912345678.json`.
   - seed 912345679 → `LONGSPAN_MATCH=42/42`, `predicate_holds:true`, gate_rc 1, elapsed 34.34 s;
     receipt `receipt-s912345679.json`.
   Per-class 17/17 classes perfect in both runs (`misses: []`).
3. Differential base-vs-landed on 15 short-span fixtures (64 B–32767 B, boundaries/glue/mutations/
   multi-line/line-binding/special chars): 14/15 identical verdicts. The one difference, fixture
   `s7` (32767-byte present, delimited): **both** gates read `unsupported` — not a patch regression
   (see finding F2).
4. Contract battery on the landed gate: 28 long-span fixtures spanning the whole claimed range
   32768–65536 (verbatim, glued-left/right/both, mutations at offsets 0/100/4095/4096/center/last,
   split-after-chunk, split-inside-chunk, first/second-occurrence line binding, mislocated lines,
   occurrence at file start/end, hay==span, hay<span, spans with backslash/quote/tab/newline,
   periodic overlapping occurrences, 32768/65536/65537 lengths). Within the claimed range **every
   verdict matched the round-4/31 contract** — including `L17` (exactly 32768), `L19` (exactly
   65536), and second-occurrence line binding (`P2` → `at=lines:1966-3931`, `require`).
   `L13` mislocated produced `FINDING CLAIM_LINE_MISMATCH … obs=id=L13` (driver_summary.txt line 3).
5. `json_unescape` old-vs-new differential: 3000 random JSON bodies (valid/invalid `\u`,
   surrogates, `\u0000`, trailing lone backslash, `\U` etc.) → **0 output differences**.
6. Hex-pattern build `tok_hex_pattern` vs base per-character loop for bytes 1..255 → **0
   differences**; end-to-end parity for spans containing `'`/`\` (fixtures p1–p4) → identical
   verdicts on base and landed.
7. Grep enumeration microtest: chunk pattern `\x61(?=\x61\x61)` on `aaaaaaaaaa` reported **all**
   overlapping start offsets (0..7), so `-o` with a 1-byte-consuming pattern does not skip
   candidates — the "every-occurrence enumeration" premise holds. Periodic overlapping occurrence
   (`P1`, `(` + "ab"*17000 + `)`, span "ab"*17000) correctly read `supported`.

## Findings (severity order)

### F1 — selftest "long-span" cases never exercise the chunk matcher (Low, coverage)
The new selftest cases (lines 7825‑7855) label themselves "long spans … above the limit", but the
fixture span is `ls_span=$(printf 'w%04d ' {1..4999}); ls_span="$ls_span"w0500` → **29999 bytes**,
below `TOK_DIRECT_SPAN_MAX=32767` (line 1582). They run the **direct** matcher only; the chunk path
(`tok_span_offsets_chunk`) is exercised by nothing in `--selftest`. A regression in the chunk
matcher would pass selftest (it is covered only by the counter, which is outside the selftest).
Inline comment at 7825‑7835 ("These cases pin the contract rules on a span above the limit") is
inaccurate; commit message says "cases 252-253" while the block comment says 252‑254 (case counter
reaches 253). Evidence: selftest run output; `wc -c` of the constructed span = 29999; probe
table below (direct works ≤32761, chunk is the only path ≥32768).

### F2 — dead zone 32762–32767 B: direct path fails (grep PCRE2 compile limit), not argv (Info, outside claim)
Probed `grep -P` with the built hex pattern for spans N=29999..32768 on identical hay:
N=32761 (pattern 131044 chars) **OK**; N=32762+ fail with `grep: PCRE2: error compiling pattern
…: regular expression is too large`; N=32768 (131072 chars) also fails. So the direct matcher is
actually limited at ~32761 bytes by PCRE2 compiled-pattern size, not by execve E2BIG as the
comments (1567‑1572, 1582) and design state. Consequently spans of 32762–32767 bytes that are
present verbatim read `observed=unsupported` on the landed gate (confirmed end-to-end: `L18`,
32766 B, `observed=unsupported` + `CLAIM_SPAN_NOT_FOUND`, stderr `grep: regular expression is too
large`). This band is **below** the C1 contract floor (32768), so no claimed verdict is violated; it
is a latent gap if any future claim approaches the boundary. Base behaves identically (not a
regression).

### F3 — no verdict divergence found within the claimed contract (primary result)
For every input tested in 32768..65536, the patched gate's verdict equals the contract: verbatim
delimited → `supported`; single-byte change anywhere (before/inside/after the 4096-byte chunk, at
4095/4096, center, last) → `unsupported`; glued-left/right/both → `unsupported`; split halves
(including split inside the chunk) → `unsupported`; `"line"` binding to the second delimited
occurrence → `supported` with `at=` on the bound occurrence; line naming neither → `mislocated`
with `CLAIM_LINE_MISMATCH` naming the id. Chunk confirmation uses whole-span byte equality under
LC_ALL=C (byte offsets; `-b` offsets from `grep -z`), and the resume logic reproduces the base
`-o` non-overlapping order (verified on periodic/overlapping occurrences: F1 #7, `P1`).

## Residual risk / verification gaps
- Unclaimed surfaces not tested here: sources with non-ASCII/NUL content, spans >65536 (one
  informational 65537 case passed), `verify-chain`/`verify-sweeps` long anchors, `expect=contradicted`
  long markers.
- The counter measures 42/42 on two fresh seeds, but per the frozen design the C1 verdict is
  `unverified` this round because five wave-1 controls are held and may not be substituted; this
  review only attacks what landed — independent operability measurement only.
- No stderr noise from the chunk path in any run (grep errors only occur in the direct-path dead
  zone, F2).

## Artifacts
- Scratch: `driver.py`, `driver_summary.txt`, `receipt-s912345678.json`, `receipt-s912345679.json`,
  `base-gate.sh`, `clone/` (tip), `baseclone/` (b8053900), fixtures under `fixtures/`, `fxL25/`,
  `fxL24/`, `fxP1/`, `fxP2/`, `fxL18/`, `fxapos/`.
- Report: `.ufo/waves/round-34/w2/R34ReviewPatchC.md` (this file).

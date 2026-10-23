# ExecC1BuildC — C1 candidate C (chunked long-span matcher), round 34 wave 1

Base: `70feb5eacc959eb98071461fe89f0b892c0810d8` (lane `master`), gate
`tools/research-gate.sh` SHA-256 `43a1af35ca668fe535fcef1e68b0c64bbba3eada59c7a23181f591901fca4346`
(unchanged since lane base `b8053900…`). Sandbox clone:
`/fast/scratch/hyaku/chousa-r34/w1/ExecC1BuildC/repo`.

**Deliverables.** Patch `candidate-C.patch` (248 lines, 7 hunks) and the patched
gate `candidate-C-gate.sh`, both in
`.ufo/waves/round-34/w1/ExecC1BuildC/`; patched gate SHA-256
`772a1d8e4d94dbf3a44a64bf850b1324e51546eeb62abcd7b3ec585f0e003e58`.

**Control rule respected:** I never ran `c1-count.py`, `c1-count-v2.py` or
`c1-count-v3.py` (or any counter) against this candidate. All probe numbers
below come from my own harness (`probe-longspan.sh`, shipped) with my own
fixtures; no counter file was read or edited.

## 1. What the base does wrong (re-measured, not assumed)

Command (in the clone, base gate, own fixture):
`bash orig-research-gate.sh verify-claims /tmp/p33/claims.jsonl --root /tmp/p33`
— one claim, 33000-byte span copied verbatim from the source. Result: rc 1,
18.4 s, `CLAIM id=L1 … observed=unsupported`, stderr
`tools/research-gate.sh: line 1553: /usr/bin/grep: Argument list too long`.

Measured ceilings (probe `probe-pcre.sh`/`probe-limit.sh`, recorded below):
* single argv string (MAX_ARG_STRLEN, 32 pages) refuses a 131072-byte string —
  the hex pattern is 4 bytes per span byte, so span ≥ 32768 bytes is refused
  at exec (E2BIG);
* PCRE2 refuses earlier still, and the failure point is **content-dependent**:
  a hex pattern of 131040 chars built from two alternating bytes is accepted,
  the same length built from random bytes fails with
  `grep: regular expression is too large`; uniform `\x61` repeated was accepted
  to 131056 chars (span 32764) and refused at 131060 (span 32765).

## 2. What candidate C changes

Two hunks on the matcher, one on the JSON decoder, one selftest block.

**(a) Long spans — chunk probe + whole-span confirmation** (`tok_span_offsets`,
`tok_span_offsets_direct`, `tok_span_offsets_chunk`; `tok_span_at`/`tok_span_all`
now consume an offset stream and keep the base boundary and line rules
unchanged, `tools/research-gate.sh:1553-1690`):
* a span of ≤ `TOK_DIRECT_SPAN_MAX`=32767 bytes keeps the base one-pattern
  matcher, byte-identical (the pattern TEXT is identical: `tok_hex_pattern`
  is a linear `od|tr|sed` build, measured equal to the base per-character
  `printf -v hex '%02x'` loop for every byte value 01..ff, and for a random
  4096-byte span the two pattern strings are equal — `PATTERN_IDENTICAL=yes`);
* a longer span is probed with its own first `TOK_CHUNK_BYTES`=4096 bytes,
  as one literal byte plus a PCRE lookahead over the rest of the chunk: the
  lookahead reports the chunk's start offset at *every* position, including
  overlapping ones (a plain `-o` reports only non-overlapping matches and
  could skip a real occurrence — measured: `a(?=aa)` on `aaaa` gives 0 and 1,
  plain `aa` gives 0 and 2);
* every candidate offset is then confirmed by comparing the hay bytes at that
  offset with the WHOLE span (`[[ ${hay:offset:slen} == "$span" ]]`, LC_ALL=C,
  quoted RHS = literal compare). A chunk match alone is not the span: this
  confirmation is what makes a mutated, split or glued span read absent;
* confirmed offsets are emitted left to right and, after an accepted
  occurrence, candidates that start before its end are skipped, so the
  occurrence set and order are the base `grep -o` (greedy non-overlapping) set;
* `tok_span_at`/`tok_span_all` keep the base boundary rules (`tok_left_ok`,
  `tok_right_ok`) and the base line arithmetic (`count_nl(before)+1`,
  `+ count_nl(span)`), so short-span verdicts are unchanged by construction.

**(b) `json_unescape` made linear** (L1 request, `tools/research-gate.sh:1329-1381`):
runs of ordinary characters are consumed with one regex match each instead of
one `${s:i:1}` per byte; the escape branches keep the exact base decoding
(including a malformed `\u`, a trailing lone backslash and the surrogate `?`
rule) and each branch advances the index exactly as the base `for` loop did.
Measured byte-identical on 615 inputs (400 random escape soup, 200
`json.dumps` bodies, 15 edge cases incl. `\uD800`, `\uZZZZ`, `\`, `\u00e9`,
`\ud83d\ude00`): `UNESCAPE_IDENTICAL=yes`.

**(c) selftest cases 252-253** (appended after the r33 block; the base selftest
ended at 251, so the new cases are the next free numbers). They build a
36 KB span with one `printf`, then pin: verbatim → supported; one byte changed
mid-span → unsupported; glued to a word character → unsupported; the `"line"`
field binding the second of two occurrences → supported `at=line:3`; a line that
names neither → `mislocated` + `CLAIM_LINE_MISMATCH`.

## 3. Evidence (exact commands, rc, output)

* Patched selftest, in the clone:
  `bash tools/research-gate.sh --selftest` → **EXIT=0**,
  `RESEARCH_GATE_SELFTEST: PASS (253 cases, 0 skipped)`, 33.7 s
  (base on the same host: `PASS (251 cases, 0 skipped)`; logs
  `selftest-base.log`, `selftest-candidate.log`).
* Short spans byte-identical to base — differential, same fixture, both gates,
  `diff` of the `CLAIM`/`FINDING CLAIM_LINE_MISMATCH`/`VERDICT_BEARING` lines:
  `SHORT_SPANS_IDENTICAL=yes` (12 records: verbatim and one-byte-mutated spans
  of 64, 65, 300, 1000, 4096 bytes, plus a `"line"`-bound and a line-wrong
  case). Fixture `shortfix/`, outputs `s-base.out`, `s-cand.out`.
* Long spans, same 15-record fixture on both gates (`base.out`, `cand.out`):
  base `VERDICT_BEARING_CLAIMS=3/15`, candidate `5/15`; the two records that
  moved are the verbatim long span (`LG1`: base `unsupported` → candidate
  `supported at=lines:1-527`) and the 32768-byte edge (`EG1`: `unsupported` →
  `supported at=lines:1-510`); every mutated / split / glued / line-wrong long
  record still reads `unsupported`/`mislocated` on both gates. (The 15-record
  fixture has only 2 truly-present long spans; this is a behaviour probe, not
  the counter.)
* Per-record timing, own 15-record probe, candidate gate
  (`probe-longspan.sh repo/tools/research-gate.sh probefix`, 3.0 s total):

  | record | rc | observed | elapsed |
  |---|---|---|---|
  | EDGE-16384 | 0 | supported | 0.08 s |
  | EDGE-16385 | 0 | supported | 0.08 s |
  | EDGE-32767 | 0 | supported | 0.24 s |
  | EDGE-32768 | 0 | supported | 0.24 s |
  | LONG-VERBATIM (33000 B) | 0 | supported | 0.25 s |
  | LONG-MUT-HEAD | 1 | unsupported | 0.23 s |
  | LONG-MUT-MID | 1 | unsupported | 0.24 s |
  | LONG-MUT-TAIL | 1 | unsupported | 0.25 s |
  | LONG-SPLIT | 1 | unsupported | 0.26 s |
  | LONG-GLUED-LEFT | 1 | unsupported | 0.24 s |
  | LONG-GLUED-RIGHT | 1 | unsupported | 0.24 s |
  | LONG-LINE-BOUND | 1 | mislocated | 0.27 s |
  | LONG-LINE-WRONG | 1 | mislocated | 0.26 s |
  | SHORT-VERBATIM | 0 | supported | 0.04 s |
  | SHORT-MUTATED | 1 | unsupported | 0.04 s |

  For comparison, base on ONE 33000-byte verbatim span was 18.4 s and still
  read `unsupported`. `LONG-LINE-BOUND` reads `mislocated` because my probe
  fixture names line `4`, which falls *inside* the first (527-line) occurrence
  rather than exactly on the second occurrence's range — the gate is behaving
  as specified (a bound claim must name the occurrence's exact start-end
  lines); the selftest case 253 covers the correctly-named range and passes.
* Competence of the two new selftest fixtures: `claims-longspan` (3 records,
  36 KB span) and `claims-longspan-line` (2 records) both run inside the
  passing selftest; their expected strings are quoted in the patch.

## 4. Verdict this item asks for

Candidate C is **built and meets its stated contract on every probe I ran**:
a 32768..65536-byte span present verbatim now reads `observed=supported`
(0.25 s/record), a mutated / split / glued one reads `unsupported`, the
`"line"` field binds a long span to the named occurrence and otherwise reads
`mislocated` with `CLAIM_LINE_MISMATCH`, and spans ≤ 32767 bytes are
differentially identical to the base gate. It is **not scored**: per the
binding control rule no seat runs the counter against a candidate, so
`LONGSPAN_MATCH=…/30` is the L1's to measure after the control receipts.

## 5. Risks and limits

1. **Unscored by the counter.** The Candidate-Build seats are forbidden the
   counter, so P1 is unmeasured here; I make no claim about the 30/30 count.
2. **Content-dependent PCRE2 ceiling.** The one-pattern direct path is used for
   spans ≤ 32767 bytes, as at base. For diverse content PCRE2 rejects hex
   patterns far below the argv limit (measured: a 112000-char pattern of random
   escapes is refused = 28000-byte span), so base — and this candidate, by
   construction — still reads `unsupported` for some 28000..32767-byte spans.
   That band is outside the frozen contract (≥32768) and outside the counter's
   classes; a dynamic "did grep refuse the pattern?" fallback to the chunk path
   is the obvious next step (not implemented, to keep base parity for the short
   band exact).
3. **Chunk anchor cost on pathological content.** Cost per long record is
   O(chunk occurrences × span length): the probe finds every start offset of the
   span's first 4096 bytes, and each candidate costs one full-span byte compare.
   For random-vocabulary sources this is 1-3 candidates (measured 0.23-0.27 s
   per record). A 64 KiB span over a 1.7 MB source holding ~24 near-copies is
   ~24 candidate compares (still linear in the number of copies), but a span
   whose first 4096 bytes are highly repetitive (all-`a`) would give thousands
   of candidates; not measured, not covered by the counter's fixtures.
4. **Probe chunk fixed at 4096 bytes.** Longer spans are located by their
   prefix only; the whole-span confirmation is what makes this sound, and a
   prefix is guaranteed to occur wherever the span occurs.
5. **`json_unescape` rewrite is exercised only by the selftest and my 615-case
   differential probe.** It is byte-identical on all of them, but it is a shared
   reader: any residual difference would show up as a claim-parsing change.
6. **Timing headroom not measured against the frozen counter v3** (37 long
   records, up to 65536 bytes, sources ~1.7 MB, 1500 s gate bound): the linear
   `json_unescape` and the linear hex build remove the 58.7 s + 18.1 s
   per-64 KiB-span costs L1 reported, and my per-record numbers are 0.25 s, but
   I did not run that fixture.

## 6. Files changed (all inside my own directories)

* `.ufo/waves/round-34/w1/ExecC1BuildC/candidate-C.patch` — unified diff
  (a/tools/research-gate.sh → b/tools/research-gate.sh), 248 lines.
* `.ufo/waves/round-34/w1/ExecC1BuildC/candidate-C-gate.sh` — the patched gate,
  SHA-256 `772a1d8e…e003e58`.
* `.ufo/waves/round-34/w1/ExecC1BuildC/selftest-candidate.log` — PASS (253).
* `.ufo/waves/round-34/w1/ExecC1BuildC/probe-longspan.sh` — the probe harness.
* No lane production file, lane jj state or fleet file was touched; the patch
  was developed only in `/fast/scratch/hyaku/chousa-r34/w1/ExecC1BuildC/repo`.

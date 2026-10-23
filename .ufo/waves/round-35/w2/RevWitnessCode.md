# RevWitnessCode — static+live review of tools/mechanism-witness.py (round 35, C2)

Scope: the witness tool's stamp regex and function-span extraction, trace size,
timeout cleanup, JSON contract, exit codes, `--tmp`. Verdict on whether a
witness bypass can still satisfy P2's witness bar: **yes — demonstrated twice**.

Environment: bash 5.3.20, GNU grep 3.12 at /usr/bin/grep, python 3.14.8.
Gate pinned for all runs: sha256 `1f2fb4f522d9a670b49dd61ad1369f55ee012f3b0d38050654be45a71aaef617`
(re-derived `sha256sum tools/research-gate.sh`, 2026-10-23).

Baseline (landed gate, seed 3501):
`WITNESS=pass OUTPUT=9/9 STAMPS chunk=9 direct=1 (long records=8)`, exit 0, ~5.6 s.
Note `stamps` counts entry-line traces, not calls: 9 stamps vs 8 long records —
the `>=` predicate tolerates it, but "one stamp per call" is already false on
the landed gate (a second matcher pass exists for `line:`-keyed claims).

## F1 — CRITICAL: col-0 first-occurrence hijack = witness bypass with real matcher dead

`matcher_entry_lines` (tools/mechanism-witness.py:89-101) takes the FIRST line
starting `tok_span_offsets_chunk()` / `tok_span_offsets_direct()` and picks the
first non-blank/non-comment/non-`}` line after it as the "entry stamp". It is
not syntax-aware. A column-0 line inside the *dispatcher* body:

```
tok_span_offsets_chunk() { :; }
```

is (a) a legal nested function definition (verified `bash -n`), which at
runtime silently redefines the real matcher to a no-op before any call, and
(b) the parser's first col-0 occurrence, so the "chunk entry" becomes whatever
line follows the decoy.

Demonstrating input (artifact `gateA-decoy.sh`,
sha256 `5f3f48947dd92e7eb9bb616a755024678547546ab43a0c0417fa300f45b176a6`):
landed gate + 6 lines inside `tok_span_offsets` after `local hay=$1 span=$2`:

```
tok_span_offsets_chunk() { :; }
  if (( ${#span} > TOK_DIRECT_SPAN_MAX )); then
    printf '%s' "$hay" | python3 <helper> "$span"   # bytes.find exact search
    return 0
  fi
```

Measured:
```
python3 tools/mechanism-witness.py --gate gateA-decoy.sh --seed 3501
WITNESS=pass OUTPUT=9/9 STAMPS chunk=10 direct=1 (long records=8)  exit 0
```
The chunk matcher under test (real def, line 1716 in the patched file) is both
shadowed to `:;` and unreachable (the shortcut returns first). The witness
counts the per-call `if` line at parser-chosen entry 1690. This is a THIRD
keyed-engine class: cheaper than K1 (six lines, same helper), output-full,
witness-pass. It satisfies every P2 witness condition while running zero chunk
calls. Unlike the stated limit (claims.md:108 "an engine that knows it is
traced"), gate A does not detect tracing — it exploits a line-regex parser,
and the redefinition is gratuitous extra damage.

## F2 — CRITICAL (inside stated limit, but cost ≈ 0): static stderr forgery

The stamp scan (lines 269-280) treats any stderr line containing
`WITNESS@@<gate_abspath>:<N> ` as a call. The marker is a constant, `$0` is the
gate's own absolute path, and `N` is knowable by reading oneself. Gate B
(artifact `gateB-forge.sh`, sha256
`02c33b293ae7ae0e83b374dadfbde81100a767b97e73930ec4712efbe6cb58f2`) runs the
same python shortcut plus one static line in the dispatcher:

```
for _wi in 1 2 3 4 5 6 7 8 9; do printf '@@WITNESS@@%s:%s \n' "$0" "1725" >&2; done
```

Measured: `WITNESS=pass OUTPUT=9/9 STAMPS chunk=90`, exit 0. The engine never
inspects PS4/BASH_XTRACEFD — the forgeries are unconditional, so this is weaker
than "knows it is traced" but equally effective; the doc's own caveat is the
only cover.

## F3 — HIGH: trace file unbounded — 297 MiB for ONE 9-record run

`bash -x` traces post-expansion text, so `local hay=$1 span=$2` lines embed the
whole corpus file + 32 KiB span, and `$(tok_hex_pattern …)` substitutions embed
16 KiB patterns. Replica with a KEPT trace (driver
`trace_size.py`, kept at
`/tmp/hyaku/chousa-r35/w2/RevWitnessCode/keep/w35wit-keep-00000dad-81oem2yf/`):

```
elapsed=5.4s rc=1 trace_bytes=310949670 longest_line=105226
entry_lines={'chunk': 1699, 'direct': 1677} stamps={'chunk': 9, 'direct': 1}
```

~311 MB per witness run; one `c2-count` battery ≈ 0.9–1.0 GB written and
deleted unread. No cap, no warning, no receipt field. On a constrained TMPDIR
this is a disk-fill hazard; a hostile gate can grow it without limit (it
prints to stderr, which shares the file). A 105 KB single line also defeats
any line-oriented downstream tooling.

## F4 — HIGH: environment scrubbing asymmetric with c1-count — ambient env kills P2

Witness scrubs only `CHOUSA_*` (line 258); the C1 counter scrubs `CHOUSA_*`
AND `RESEARCH_GATE_*` (c1-count.py:88). Demonstrated:

```
RESEARCH_GATE_GREP=/bin/false python3 tools/mechanism-witness.py --gate <landed> --seed 1
WITNESS=fail OUTPUT=0/9 ... gate_rc=2   exit 1
```

An ambient bad `RESEARCH_GATE_GREP` makes the LANDED gate fail its own witness
inside c2-count → P2 dead on that host. Similarly `BASH_XTRACEFD` is not
scrubbed: verified `exec 7>xfd.log; BASH_XTRACEFD=7 bash -x …` writes all
xtrace to fd 7, nothing on stderr → stamps 0/0 → landed gate false-fails.
`BASH_ENV`/`ENV`/`SHELLOPTS`/`TMPDIR` likewise pass through (BASH_ENV can run
arbitrary code at gate startup).

## F5 — MEDIUM: exit-code + JSON contract drift

- Doc: "2 harness error". Observed: unhandled exceptions (fixture `generate`
  failure, `p.stdout` decode is fine but `--json` write failure, OSErrors)
  propagate as traceback → **exit 1**, receipt written without a `witness`
  key — indistinguishable from an honest witness fail.
- Receipt schema varies by path. Key sets measured:
  normal run: 15 keys incl. `output_full, gate_rc, stamps, drift, elapsed_s`;
  `unparseable`: 9 keys — no `output_full/gate_rc/stamps/drift/elapsed_s`
  (receipt `run/receipt-unparseable.json`, `WITNESS=unparseable`, exit 1);
  `timeout`: adds only `witness/output_match/output_total` — same hole.
  c2-count survives via `.get()`; any consumer indexing `["output_full"]` dies.
- `--tmp` is a mkdtemp PARENT that must already exist; not documented, and the
  whole root (fixture + trace) is `rmtree(ignore_errors=True)` even on
  timeout/error — the only forensic artifact vanishes on exactly the runs a
  reviewer most wants to keep. Also `fixture_root_prefix` in the receipt is
  only `basename(root)[:6]` — `w35wit` — useless for locating the (deleted) dir.

## F6 — MEDIUM: same-semantics gate styles false-fail the witness

Unit probes on `matcher_entry_lines` (bash-5.3 verified against real traces):

- `fn()\n{\n  local x\n}` (brace on own line): entry = the `{` line, which
  `bash -x` never stamps (verified: K&R probe stamps `local`, not `{`) →
  `witness=fail` on every correct gate written that way.
- `function tok_span_offsets_chunk() {` (valid bash): parser returns `{}` →
  `witness=unparseable`.
- >60 lines of leading comments/blank in a body: scan window `start+1..start+60`
  (line 95) misses the first executable → key absent → unparseable.
- A col-0 *comment* line `tok_span_offsets_chunk() is discussed…` before the
  real def: picks the def-header line as entry; verified bash does NOT trace
  definition-header lines → stamps=0 → false fail.
- Bare `}` in the preface (e.g. comment-free closer of an early group) →
  `break` skips the fn → unparseable.

None affects the landed gate (its defs are `fn() {` at col 0, entry 1699/1677),
but K-variant or rewritten engines in this exact style get a false `fail` —
which counts as "separated" under c2-count's rule (`witness=fail` +
`output_full` counts toward separation!). A K&R-styled but *honest* engine
would be credited as separated without the witness testing anything.

## F7 — LOW: timeout/cleanup, regex edge cases

- `subprocess.run(timeout=1500)` kills only the direct bash child. Verified:
  a `setsid` grandchild outlives the kill (`revenant` file created 6 s after
  the run returned at 2 s). A daemonizing gate's children keep writing the
  trace after "cleanup". No pipe-drain stall on py3.14 (verified separately).
- `stamp_re = WITNESS@@(.*?):(\d+) `: a gate path containing `:NNN ` makes
  `group(1)` truncate → all stamps skipped → false fail (edge; needs `:` in
  path). Only the FIRST `WITNESS@@` per line is searched — fine for PS4.
- `m.group(1) != gate` compares against `abspath`, but BASH_SOURCE prints the
  invoked path; a wrapper-gate exec'ing a real file would stamp the real
  file's path → stamps missed → false fail (c2-count always passes the real
  file, so inert there).
- Stamps are counted per line-hit, so an entry line inside a loop or a hot
  line like the `if` in F1 inflates counts; `>=` papers over it both ways.

## What holds

- Landed gate: witness pass on seed 3501, entry lines 1699/1677, rc=1+drift
  correctly required by `output_full`. Trace-based stamps on the real file do
  count matcher entries (9 chunk vs 8 long records = one extra pass).
- The `>= long_records` predicate is robust to over-counting; the F1/F2
  attacks are parser/forgeability defects, not counting defects.

## Verdict

The tool scores the landed gate correctly, but the mechanism witness is
defeatable by a *static* six-line patch (F1) that neither detects tracing nor
calls the chunk matcher — it hijacks a line-text parser — and by unconditional
stderr forgery (F2). Under c2-count's scoring, F1 yields
`output_full=true, witness=pass` = NOT separated: a candidate gate can carry
the shortcut and still pass P2's witness bar. Claims.md's stated limit covers
engines that *know* they are traced; F1 needs no such knowledge, and the
"calls the matcher once for show" clause doesn't cover a matcher that is
redefined to `:;` and never entered. Recommend: parse function spans with
`bash -n`-verified extents (or anchor on the def line `N` plus require the
entry stamp AND the `done < <(grep …)` region), hash-anchor the matcher body
into the receipt, and deduplicate `WITNESS@@` lines by content.

## Artifacts

All under `/tmp/hyaku/chousa-r35/w2/RevWitnessCode/` (own-dir copies of the
two patched gates also at `.ufo/waves/round-35/w2/RevWitnessCode/`):

- `gateA-decoy.sh` sha256 5f3f4894…, `gateB-forge.sh` sha256 02c33b29…,
  `span_search.py`, `mkvar.py`, `trace_size.py`, receipts
  `run/receipt-{3501,A,B,envleak,unparseable}.json`.
- Kept 297 MiB trace: `keep/w35wit-keep-00000dad-81oem2yf/_trace.log`
  (left in /tmp per the 1 MiB artifact cap; `trace_bytes=310949670`).

Not verified (time box): C1 counter not run; `dz-edge` boundary-1l route not
single-stepped; slen R1/R2 reviewed only via probe script (correct).
Report: .ufo/waves/round-35/w2/RevWitnessCode.md

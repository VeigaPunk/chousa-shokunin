# `--json` manifest delimiter edge (round 24)

source: S001 tools/research-gate.sh (verify-all setup check "manifest unreadable"; the append block opening `# A manifest whose last byte is not '\n'`; selftest cases 134–136), landed gate sha256 `752e4e38…`; S013 https://jsonlines.org/ §"3. Line Terminator is '\n'" and §"2. Each Line is a Valid JSON Value" (page read 2026-10-19); receipts corpus/evidence/json-r24-20261019T213117Z-{demo,selftest,battery,drift}.log; round-20 named debt (seat 24) closed
verified-at: 2026-10-19 (round 24; before/after counting command re-run live against the pre-round gate b5d0f93d… and the landed gate; three single-edit mutants each fail their pinning case)
recheck: 90d (`bash tools/research-gate.sh --selftest` — cases 134–136 pin the arms; re-open S013 §3 for a format revision)

## The defect

`verify-all --json PATH` appended `printf '%s\n' "$line" >>PATH`. The `\n`
terminates the new line; it does not separate it from the previous one. A
manifest whose last byte is not `\n` therefore received
`{"prior":true}{"schema":"chousa-verify-all/v1",...}` on one line — neither
object parses, and the append-only manifest is corrupted by the append that
was meant to extend it.

Why such a manifest is legitimate input, not operator error: the JSON Lines
definition makes the final terminator optional — "Including a line
terminator after the last JSON value in a file is strongly recommended but
not required." (S013, §3). A conforming writer may leave it off; an appender
must not assume it.

## The fix

1. Setup: a non-empty manifest the gate cannot read is refused before any
   write (`research-gate: manifest unreadable: …`, exit 2). Without this, a
   write-only manifest (mode 0200) read as "no last byte" and was still
   glued — found by the round's L2 reviewer, reproduced, fixed (case 136).
2. Append: the manifest's last byte is read as hex
   (`tail -c1 -- PATH | od -An -tx1`); if the manifest is non-empty and that
   byte is not `0a`, the new line is prefixed with `\n`. The hex read matters:
   a first draft used `-n $(tail -c1 -- PATH)`, and bash command substitution
   drops NUL bytes, so a NUL-terminated manifest was still glued (with a bash
   warning on stderr) — measured during the round, replaced before landing
   (case 135).

The prior bytes are never rewritten (append-only holds: line 1 stays
byte-identical, case 134 asserts it; case 136 asserts the refused manifest is
byte-unchanged).

Controls (receipt `…-demo.log`, landed gate): last byte `}`, `\r`, NUL → 2
lines, 0 blank, 0 stderr bytes; an empty manifest gets exactly one line and
no blank line (S013 §2: "a blank line is not" a valid value); a
newline-terminated manifest is appended to unchanged (2 lines, 0 blank); a
write-only manifest exits 2 with its bytes unchanged.

## Measurement

| state | command | output |
|---|---|---|
| before (gate b5d0f93d…) | the counting command in `…-demo.log` | `MANIFEST_LINES=1 INVALID_JSON_LINES=1` |
| after (gate 752e4e38…) | same | `MANIFEST_LINES=2 INVALID_JSON_LINES=0` |
| selftest | `bash tools/research-gate.sh --selftest` | `PASS (136 cases, 0 skipped)`; cases 1–133 `cmp` byte-identical vs the r23 receipt |
| mutant m1 (prefix arm → `if false`) | selftest on a full lane copy | `FAIL (2/136)` — cases 134, 135 |
| mutant m2 (old `$(tail -c1)` probe) | same | `FAIL (1/136)` — case 135 |
| mutant m3 (unreadable refusal → `if false`) | same | `FAIL (1/136)` — case 136 |
| battery | 8 masked runs, pre vs landed gate | ALL IDENTICAL |
| drift | `--drift corpus/evidence/gate-baseline-r12-20261019T115519Z.json` | `GATE_DRIFT: none` |

## Named limits

- Observation: a last byte of `\r` (a CRLF file truncated mid-terminator) is
  treated as "not `\n`" and gets a `\n` prefix; the result `…\r\n{…}` parses
  (S013 §3: surrounding whitespace is ignored).
- Observation: a NUL last byte gets the `\n` prefix; the prior line was
  already not valid JSON, and the gate does not repair prior lines.
- Observation (named debt, not fixed): the probe and the append are two
  operations with no lock. 16 parallel appenders × 3 runs onto an
  unterminated manifest wrote 16 objects each run and no glued line, but one
  run wrote one blank line (two appenders both prefixed) — receipt
  `…-demo.log` §concurrency. The gate assumes one writer per manifest; a
  `flock` around probe + append is the candidate fix.
- Observation: case 135 needs `grep -a` — GNU grep treats a NUL as a line
  break in a binary file, so a bare `grep -c '^$'` counts a phantom blank
  line.
- The `--drift` truncated-baseline item from the round-20 named debt was
  re-measured at the round-24 opening as not a defect (`LOG.md` round-24
  opening): every truncation form exits 1 with `GATE_DRIFT: <tokens>`.

Round 32 update (2026-10-23, appended): the "named debt, not fixed" concurrency observation above
is closed on gate `10f2fe12…`: the probe and the append now run under one `flock -x` on the
manifest's open file (`knowledge/manifest-append-lock-r32.md`). The text above is kept as the
round-24 record.

# Attack09 — C1 frozen-case overflow-exit: nearby receipt bypass outside the frozen case

Seat: Attack09 (lane chousa round65, leaf critic). Freeze `f99de3bdfaaf9b4c4fa85cc55dd37b9df2ee90fd`.
Subject: claim C1, counter `corpus/evidence/round65/c1-count.py`, reference validator
`corpus/evidence/round65/controls/ref-receipt-pin.py` (sha256 `0719d717…315fa2`, copied byte-identical
to scratch for execution). Base `d6ed8155e9b4735639a2cf0a3e479c62f2056195`. Target
`tools/receipt-pin.py` is absent at freeze (before-control state, verified).
No frozen bytes altered; all probes bounded and confined to scratch; only `git -C <lane> cat-file` reads.
Detailed evidence: `.ufo/waves/round-65/w1/Attack09/` (report.md, attack09-results.tsv, attack09-receipt-*.txt).

## Axes

1. **Counterexample strength** — does a nearby forged/malformed receipt bypass the consistency predicate outside the `overflow-exit` case?
2. **Detection** — does the frozen counter (or by inheritance the frozen reference) detect it?
3. **Claim impact** — fixable defect against the frozen claim, or a tradeoff already priced in?
4. **Boundedness/provenance** — probes isolated, evidence reproducible.

## Frozen counter branch inspection

The `overflow-exit` case is `v.replace('EXIT=0','EXIT=256')`, expected rc=1. Reference rejects it via
`re.fullmatch(r'EXIT=(?:0|[1-9][0-9]{0,2})',lines[1])` + `int(lines[1][5:])>255`. The exit branch is
token-tight for what it checks: every exit variant probed (`00`, `0256`, `300`, `+0`, ` 0`, `0 `,
`pass`, 20-digit) is REJECTED (`RECEIPT_PIN=FAIL header/body`, rc=1). No bypass lives in the exit token branch itself.

Structural limit of the counter: all 20 case receipts are derived from one LF-only template `v` by
`str.replace`, written with `Path.write_text`. Counter source contains no `\r`, `\u2028`, `\x0b`, `\x0c`.
The case set has no CRLF/Unicode-separator/blank-slack variant. These classes are unreachable by construction.

## Counterexamples (executed)

Valid baseline `v` = `REVISION=d6ed…6195\nEXIT=0\nSHA256=<h> SKILL.md\n\nmeasured output\n`, `<h>` =
sha256 of `git cat-file blob d6ed…:SKILL.md`. Each variant run against the reference copy with
`--root <lane> --revision d6ed…6195`. Full table: `attack09-results.tsv`; receipts: `attack09-receipt-*.txt`.

| Variant | Verdict | Meaning |
|---|---|---|
| `byp-crlf` | ACCEPT rc=0 | CRLF line endings accepted (`splitlines` tolerance) |
| `byp-u2028` / `byp-u2029` | ACCEPT rc=0 | Unicode LINE/PARAGRAPH SEPARATOR accepted |
| `byp-vtab` / `byp-formfeed` | ACCEPT rc=0 | `\x0b` / `\x0c` separators accepted |
| `byp-dbl-sep` | ACCEPT rc=0 | two blank separator lines accepted |
| `byp-body-smuggle` | ACCEPT rc=0 | forged second `REVISION/EXIT/SHA256` block inside body accepted |
| `byp-nul-body` | ACCEPT rc=0 | NUL byte in body accepted |
| `byp-trailing-blanks` | ACCEPT rc=0 | trailing blank body lines accepted |
| `sem-forged-exit-7` | ACCEPT rc=0 | self-reported EXIT unauthenticated (by design) |
| 17 detection controls (BOM, exit-token variants, revision upper/trailing-space, separator=space, empty body, digest-line double space, path trailing-space/dot-slash/double-slash) | REJECT rc=1 | branch coverage holds where probed |

Reproduced the frozen positive control in-environment: counter vs reference copy = `CASES=20/20 C1=PASS`, exit 0 (work dir in scratch, removed by the counter itself).

## Verdict

- **Bypass exists and is nearby:** 9 malformed receipts, each one edit away from the frozen template, outside all 20 frozen cases, receive `RECEIPT_PIN=PASS` (rc=0) from the frozen reference validator. Strongest single counterexample: `byp-u2028` — a receipt byte-stream that does not contain a single LF, violating the claim's stated POSIX line format, is judged fully consistent.
- **Frozen counter detection: NO.** The counter is an exact-match oracle over 20 receipts it builds LF-only; none of the 9 classes can ever be constructed by it. A conforming target (the reference scores 20/20) inherits the same tolerance, and nothing in C1 can ever observe it.
- **Claim impact: tradeoff already priced in, not a fixable defect against the freeze.** C1's own text scopes it to "interface/consistency coverage, not a claim to cryptographic execution authentication or general parser safety." These counterexamples are exactly general-parser-safety gaps; the predicate (20/20 exact match), denominator, and target are untouched. No freeze change, no counter edit, no predicate rewrite warranted.
- **Smallest safe correction:** none to the freeze. For L1 integration notes only: record CRLF/U+2028/blank-slack/body-smuggle as known accepted-malformed classes of the reference validator; if a future round wants line-ending strictness, it must be a *new* claim with its own counter — do not smuggle it into round65's frozen 20.

## Provenance / bounds

- Probes: 28 bounded validator invocations (timeout 30s each) + 1 counter run, all under `/fast/scratch/hyaku/chousa-r65/Attack09` with explicit TMPDIR; scratch deleted after evidence copy. No network, no lane writes, no git/jj mutation (read-only `git -C` cat-file only).
- Environment: Python 3.14.8 (system), git (system). **No tools installed** this seat.
- `splitlines()` behavior verified on the executing interpreter.

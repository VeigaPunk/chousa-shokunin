# Attack05 — C1 wrong-revision adjacent bypass: round-65 w1 findings

**Verdict: frozen counter does NOT detect the bypass.** Nearby forged/malformed receipts with
non-canonical line endings (CRLF, lone CR, mixed separator CRLF) are accepted by the reference
validator (`RECEIPT_PIN=PASS`, exit 0) and fall outside all 20 frozen C1 cases and outside the
frozen `wrong-revision` case. Post-acquisition state (reference as target) still reports
`CASES=20/20 C1=PASS` while this malformed receipt class passes.

**Counterexample.** Canonical receipt bytes for BASE blob SKILL.md, EOLs rewritten to `\r\n` (or `\r`),
headers/digest/path otherwise exact → reference validator exits 0 PASS. Root cause:
`Path.read_text()` universal-newline translation + `str.splitlines()` normalize `\r` before any check.
Probes (bounded, isolated, scratch-only; frozen bytes hashed unchanged before/after):

- 16 candidates run against `controls/ref-receipt-pin.py`: 3 EOL forgeries + `no-trailing-nl` bypass;
  `nul-body` and `body-fake-header` pass by design (opaque body); all 10 header-field mutations detected.
- Frozen counter, absent target: `CASES=0/20 C1=FAIL` exit 1 (matches before control).
- Frozen counter, reference as `--tool`: `CASES=20/20 C1=PASS` exit 0 (matches positive control).
- Hypothetical frozen `crlf`/`cr-only` cases (expected exit 1) would fail the reference (got rc=0):
  pure coverage gap, cheaply catchable.

**Impacted axes.** C1 predicate coverage only; claims.md already disclaims general parser safety, so
this is a fixable coverage defect, not a contradiction. No execution-authenticity claim involved (out of
scope by design). Per freeze/kill rule, frozen cases/predicate/denominator unchanged this round.

**Smallest safe correction** (future round; no frozen-byte changes): add `crlf`/`cr-only`/
`mixed-sep-crlf` frozen cases (exit 1); harden target to byte-read, split on `b'\n'` only, reject `\r`;
document opaque-body smuggling boundary for downstream parsers.

Full detail and machine-readable probe results: `Attack05/report.md` and
`Attack05/attack05-probe-results.json`. Scratch `/fast/scratch/hyaku/chousa-r65/Attack05` deleted on exit.

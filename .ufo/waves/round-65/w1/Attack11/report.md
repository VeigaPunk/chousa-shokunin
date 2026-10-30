# Attack11 — C1 frozen case `no-digest` attack (round65)

Seat: Attack11 (critic). Lane: chousa round65. Freeze `f99de3bdfaaf9b4c4fa85cc55dd37b9df2ee90fd`.
Scope: attack the frozen `no-digest` counter case by constructing nearby forged/malformed
receipts *outside* the 20 frozen cases; state whether the frozen counter detects them.
Only bounded isolated probes against the frozen reference validator
(`corpus/evidence/round65/controls/ref-receipt-pin.py`) and read-only git. No frozen bytes
altered, no production writes, no tests/batteries run.

## Verdict

**The `no-digest` attack surface is closed; no nearby bypass of the digest binding exists.
The frozen counter does not cover (and cannot cover) the full malformed-receipt space, but
the reference validator rejects every digest-shape-shifted "effective no-digest" variant I
constructed. Three format-laxity inputs are *accepted* by the reference validator; none
weakens the digest binding, and each is a documented tradeoff, not a C1 predicate break.**

## Evidence

Probe battery: 18 nearby candidates run against the frozen reference validator
(`probe-results-attack11.txt`, full table; receipts in this folder). Sanity checks:
frozen counter = 20/20 PASS against the reference tool, 0/20 `missing-target` against the
absent target, both as frozen. The frozen `no-digest` case itself: reference returns
`rc=1 RECEIPT_PIN=FAIL header/body`, exactly the frozen expectation.

### Rejected (rc=1) — digest shape-shifting near no-digest all fail

| Candidate | Validator result |
|---|---|
| `SHA256=` empty value | FAIL `digest header` |
| `SHA256=  ` whitespace value | FAIL `digest header` |
| `SHA256= ` blank-after-space | FAIL `digest header` |
| `SHA256: ` colon keyword | FAIL `digest header` |
| `sha256=` lowercased key | FAIL `digest header` |
| tab instead of space before path | FAIL `digest header` |
| `SKILL.md.` path typo | FAIL `blob/digest` |
| `%2e%2e/` percent-encoded traversal | FAIL `blob/digest` |
| `//SKILL.md` double slash | FAIL `path` |
| `./SKILL.md` dot prefix | FAIL `path` |
| separator line = single space | FAIL `header/body` |
| `EXIT=+0` / `EXIT= 0` | FAIL `header/body` |
| uppercase REVISION | FAIL `header/body` |

None of these 18 names appears in the frozen case list, yet the reference validator rejects
each. A forged receipt that removes, blanks, renames, or re-encodes the digest header cannot
pass. The header parse (`re.fullmatch(r'SHA256=([0-9a-f]{64}) (.+)')`), the strict path
check (`is_absolute`, `..` in parts, `str(rel)==m[2]`), and the blob-at-revision digest
binding have no differential I could exploit near no-digest.

### Accepted (rc=0) — three format laxities, binding intact

1. **CRLF receipt** (`evidence-crlf-pass.txt`) — `splitlines()` strips `\r\n`; accepted.
2. **Appended forged second receipt in body** (`evidence-appended-forged-body-pass.txt`) —
   valid header block followed by a fake `REVISION=000…/EXIT=1/SHA256=000… forged.md` block
   in the body. The docstring claims "exactly one of each header"; the code only validates
   the top header block and treats everything after the first blank line as opaque body.
3. **Missing trailing newline / extra blank tail** — body nonempty check is lax by design.

## Does the frozen counter detect them?

**No — and by construction it cannot.** `c1-count.py` hardcodes 20 cases; none of the 18
candidates above is among them, so the counter never feeds these inputs to any target. This
is not a counter defect under the frozen predicate: C1 is "interface/consistency coverage,
not a claim to … general parser safety" (claims.md). The arbiter for out-of-case behavior
is the reference validator, which accepts only the three lax-format cases and rejects every
digest-binding attack.

## Fixable defect vs tradeoff

- **Tradeoff (canonical judge should accept):** CRLF, blank-tail, and missing-trailing-newline
  acceptance. `splitlines()`-based parsing deliberately normalizes line endings; binding
  strength is unchanged. C1's predicate is unchanged by these.
- **Fixable defect, out of C1 scope:** body appending a second forged receipt block passes
  despite the docstring's "exactly one of each header" claim. A body that embeds a full
  header block could confuse a downstream consumer that scans for the *last* header block.
  Smallest safe correction (future round, NOT this freeze): reject any body line matching
  `^(REVISION|EXIT|SHA256)=` — one-line change in the validator, plus one new frozen case
  (`forged-body-block`, expect rc=1). Do not touch frozen bytes for this.

## Constraints honored

- Probes were isolated, bounded (timeout 20s each), and read-only git (`git -C … cat-file` only).
- Scratch `/fast/scratch/hyaku/chousa-r65/Attack11/` deleted after receipts copied here.
- No installs needed; no network; no fleet/sibling/source-tree writes.
- Frozen validator, counter, and claims bytes untouched; freeze `f99de3b…` intact.

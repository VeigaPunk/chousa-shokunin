# Attack18 — C1 frozen case `no-separator`: nearby malformed-receipt bypass

Seat: Attack18 (leaf, no subagent dispatch). Lane chousa round65, freeze f99de3bdfaaf9b4c4fa85cc55dd37b9df2ee90fd.
Scope: inspect the frozen counter branch for `no-separator` and the prefreeze reference validator;
construct nearby forged/malformed receipts *outside* that one case; state whether the frozen counter
detects them. Bounded isolated probes only; no frozen bytes altered; no production writes.

## Inspected artifacts (read-only)

- Frozen counter: `corpus/evidence/round65/c1-count.py` (20 fixed cases; `no-separator` =
  valid receipt with the blank separator line deleted, expected rc=1).
- Prefreeze reference validator: `corpus/evidence/round65/controls/ref-receipt-pin.py`.
- Frozen controls: `controls/c1-positive.txt` (20/20 with the reference), `c1-before.txt`,
  `always-pass.py` (3/20), `always-fail.py` (17/20).
- Blob digest for crafting: `git cat-file blob d6ed8155:SKILL.md` →
  SHA256 `4355e16a5d8d16057496f005df7382ca287863712ed2e3abb25f61c60008ce1a`.

## Root cause of the bypass class

The reference validator frames the receipt with `text.splitlines()`. CPython `splitlines()`
splits on `\n`, `\r`, `\r\n`, `\v`, `\f`, `\x1c`, `\x1d`, `\x1e`, `\x85`, `\u2028`, `\u2029` —
not just `\n`. The frozen format (claims.md) is newline-line-structured:
`REVISION` / `EXIT` / `SHA256 <path>` lines, one empty separator line, nonempty output.
Its header checks (`lines[0] ==`, `re.fullmatch(EXIT=...)`, `re.fullmatch(SHA256=...)`) and its
separator check (`lines[3]` truthy) all operate on `splitlines()` output, so raw receipts that
contain no `\n` framing at all are re-framed into well-formed-looking lines and pass. The body
check `'\n'.join(lines[4:]).strip()` additionally tolerates a leading empty body line, and nothing
enforces the singular "empty separator" (two blank lines pass).

## Counterexample (strongest local evidence)

Crafted receipts (raw bytes in `attack18-receipt-*.txt`), all run against the frozen reference
with `--root <lane> --revision d6ed8155…6195`, 20 s timeout each:

| variant | frozen-counter nearest case | reference verdict |
|---|---|---|
| `cr-only-framing` — receipt bytes contain **no `\n` at all**; `\r` is the line boundary | `no-separator` (both attack the separator/line framing) | **ACCEPT rc=0** |
| `formfeed-framing` — `\f` (0x0c) line boundaries | same region | **ACCEPT rc=0** |
| `vertical-tab-framing` — `\v` (0x0b) line boundaries | same region | **ACCEPT rc=0** |
| `nel-u2028-framing` — U+2028 LINE SEPARATOR boundaries (valid UTF-8) | same region | **ACCEPT rc=0** |
| `double-separator` — two blank separator lines ("empty separator" is singular) | `no-separator` | **ACCEPT rc=0** |
| `body-blank-then-text` — body begins with an empty line | `no-body` | ACCEPT rc=0 (arguably legal output) |
| `no-final-newline` — valid receipt, no trailing newline | none exact | ACCEPT rc=0 (benign) |
| `space-separator` (control) | `no-separator` | REJECT rc=1 `header/body` |
| `bom-prefix` (control) | `no-revision` region | REJECT rc=1 `header/body` |
| `forged-digest-cr-framing` (control: wrong digest + `\r` framing) | `wrong-digest` | REJECT rc=1 `blob/digest` |

Full transcript: `attack18-evidence-probe-results.txt`.

Key asymmetry the controls expose: a separator line containing one space is rejected, while a
receipt whose *entire raw framing* is carriage returns — no newline bytes anywhere — is accepted.
The framing check is weaker than the content check.

## Does the frozen counter detect it?

No. The frozen counter feeds only its 20 fixed cases; none exercises `\r`/`\v`/`\f`/U+2028
framing or a doubled separator, and its acceptance logic (`returncode` + `RECEIPT_PIN=PASS` /
`RECEIPT_PIN=FAIL ` prefix) is per-case. I re-ran the frozen counter once against the reference
(bounded, isolated, scratch `--work`): `CASES=20/20 C1=PASS` exit 0
(`attack18-evidence-counter-ref-run.txt`; matches frozen `c1-positive.txt`) — while the same
reference binary accepts all five malformed-framing receipts above. So `C1=PASS` is fully
compatible with the validator accepting out-of-spec receipts; the predicate saturates without
covering this malformation class. This is a fixable defect in the tool to be *acquired*
(`tools/receipt-pin.py`), not a flaw in the frozen counter, predicate, or claims: claims.md
already scopes C1 as "interface/consistency coverage, not a claim to cryptographic execution
authentication or general parser safety."

## Impacted axes

- **C1 (operability)**: score untouched (historical 3/10 per freeze); predicate, denominator,
  counter unchanged. Finding constrains only what a 20/20 target certifies: header/digest/path
  consistency on newline-clean receipts, not raw-format framing safety.
- **Depth/C2**: unaffected; no knowledge-entry implication.
- Downstream risk (not a scored axis here): any consumer treating `RECEIPT_PIN=PASS` as
  "well-formed receipt per frozen format" would be wrong for 4+ malformation families.

## Smallest safe correction

Apply to the validator at acquisition time (`tools/receipt-pin.py`), never to frozen bytes:

1. Frame with `text.split('\n')` instead of `text.splitlines()` — rejects `\r`-only, `\v`, `\f`,
   U+2028/U+2029 framings (all become too-few-lines or fail the anchored header regexes, since
   `re.fullmatch` already pins each header line exactly).
2. Enforce the singular separator on the split result: require `lines[3] == ''` and
   `lines[4] != ''` (or equivalently one regex `fullmatch` over the raw text with a single
   `\n\n` separator). This rejects `double-separator` while keeping `no-final-newline` behavior.

No change to the frozen counter, cases, controls, or claims is needed or proposed; the counter's
20 cases still pass against a validator with these two edits (its receipts are `\n`-framed).

## Method / hygiene

- Probes bounded: 11 direct validator invocations (≤20 s each) + 1 frozen-counter run; all
  read-only against lane git (`git -C <lane> cat-file` only).
- Scratch `/fast/scratch/hyaku/chousa-r65/Attack18/` deleted after evidence copy; receipts copied
  to this folder as `attack18-receipt-*.txt`. No `/tmp` evidence. No installs needed
  (python3 3.14 + git + coreutils already present); no tools installed this seat.
- Frozen files unmodified (verified by not writing to any path outside this output folder and scratch).

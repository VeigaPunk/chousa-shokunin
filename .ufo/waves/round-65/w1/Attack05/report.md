# Attack05 — C1 frozen-case wrong-revision: nearby forged/malformed receipt bypass

Seat: Attack05 (leaf, no dispatch). Lane: chousa round65. Freeze: f99de3bdfaaf9b4c4fa85cc55dd37b9df2ee90fd.
Scope: attack the C1 frozen counter via the reference validator only; bounded isolated probes in
/fast/scratch/hyaku/chousa-r65/Attack05 (deleted on exit). Frozen bytes untouched (sha256 recorded below).
No production writes; no git mutations; no network.

## Verdict

The frozen counter **does NOT detect** the bypass. A receipt with non-canonical line endings
(CRLF, lone CR, or mixed separator CRLF) — malformed framing outside the 20 frozen cases and outside
the frozen `wrong-revision` case — is accepted by the reference validator with `RECEIPT_PIN=PASS` exit 0.
The frozen 20 cases never exercise line endings, so the predicate reports `CASES=20/20 C1=PASS`
(post-acquisition state) while this malformed receipt class passes.

## Counterexample (strongest, from local evidence)

Canonical receipt `v` (as built by c1-count.py from BASE blob SKILL.md), rewritten with CRLF:

```
REVISION=d6ed8155e9b4735639a2cf0a3e479c62f2056195\r\n
EXIT=0\r\n
SHA256=<sha256(SKILL.md blob)> SKILL.md\r\n
\r\n
measured output\r\n
```

- `python3 -B corpus/evidence/round65/controls/ref-receipt-pin.py --receipt crlf.txt --root <lane> --revision d6ed...` → **rc=0, `RECEIPT_PIN=PASS`** (bypass).
- Same for `cr-only` (all `\r`) and `mixed-sep-crlf` (headers LF, separator/body CRLF).
- Root cause: `pathlib.Path.read_text()` opens in text mode with universal-newline translation, and
  `str.splitlines()` splits on any line boundary — every `\r` is silently normalized before any check.
  The format's "exact ordered" header framing is therefore only enforced over already-normalized lines.
- Frozen-counter overlap: **none** of the 20 cases (`valid, nonzero-valid, max-exit, no-revision,
  wrong-revision, short-revision, no-exit, negative-exit, overflow-exit, word-exit, no-digest,
  wrong-digest, short-digest, missing-blob, traversal, absolute, duplicate, no-separator, no-body,
  upper-digest`) varies line endings.

## Probe results (reference validator, `--revision` = BASE, read-only git)

| case | rc | detected | note |
|---|---|---|---|
| crlf | 0 | NO | bypass — non-canonical EOL accepted |
| cr-only | 0 | NO | bypass |
| mixed-sep-crlf | 0 | NO | bypass |
| no-trailing-nl | 0 | NO | accepted (weaker; trailing newline arguably optional) |
| bom | 1 | yes | `\ufeff` breaks lines[0] equality |
| leading-blank | 1 | yes | strict positional headers |
| upper-revision | 1 | yes | exact string equality to --revision |
| revision-space | 1 | yes | |
| exit-padded / exit-plus | 1 | yes | anchored regex |
| sep-space | 1 | yes | separator must be empty |
| path-trail-space | 1 | yes | git cat-file blob lookup fails |
| path-tab | 1 | yes | regex requires single literal space |
| empty-path | 1 | yes | `(.+)` requires 1+ chars |
| nul-body | 0 | NO | by design (body opaque) |
| body-fake-header | 0 | NO | by design: a forged second header block rides inside the opaque body |

Full machine-readable results: `attack05-probe-results.json` (same folder).

## Counter-level probes (frozen counter, scratch work dirs, TMPDIR in scratch)

1. Absent target (current frozen state): `CASES=0/20 C1=FAIL missing-target`, exit 1 — matches the
   frozen before control `controls/c1-before.txt`.
2. Reference as `--tool`: `CASES=20/20 C1=PASS`, exit 0 — reproduces frozen `controls/c1-positive.txt`.
3. Hypothetical: had `crlf`/`cr-only` been frozen cases with expected exit 1, the reference would have
   failed them (got rc=0) — the laxness is real and cheaply catchable; its absence is pure coverage gap.

## Impacted axes

- **C1 operability predicate (R65-C1)**: threatened in coverage, not in the frozen cases themselves.
  A target that is byte-for-byte the reference passes 20/20 while accepting CRLF-framed forgeries.
  Per the freeze/kill rule the 20 cases, predicate, and denominator must not change this round; the
  gap is admissible evidence for a *future* round's claim, not a rewrite of this one.
- **Claim boundary**: claims.md already disclaims "general parser safety"; this attack lands exactly
  in that disclaimed gap (EOL canonicalization), so it is a fixable defect of coverage, not a
  contradiction of the stated claim scope. It does NOT touch execution authenticity (out of scope by design).

## Smallest safe correction (for L1 integration; do not alter frozen bytes)

1. Future counter revision: add frozen cases `crlf`, `cr-only`, `mixed-sep-crlf` (expected exit 1,
   token `RECEIPT_PIN=FAIL `), and optionally `bom`/`leading-blank` (already detected; pins behavior).
2. Target-side hardening: read the receipt as **bytes**, split on `b'\n'` only, and reject any `\r`
   (or any byte outside the allowed grammar) before parsing; keep `splitlines`-free framing.
3. Document that the receipt body is opaque and may embed arbitrary header-looking lines
   (`body-fake-header` probe), so downstream consumers must parse only up to the first blank line.

## Evidence integrity

- Frozen files hashed before/after probes (unchanged):
  - c1-count.py `454286e8b89d5dbf3029c6d22b77c47bb9302903a94d7206eeaf1b93059d3dae`
  - claims.md `b9dbca57f4ca1af351459410e1fb7793668fe647c20278d26765b85485ab2fc5`
  - controls/ref-receipt-pin.py `0719d7175da072454f514e0eea52b266f66c2246a085f4ea824793f634315fa2`
- Scratch `/fast/scratch/hyaku/chousa-r65/Attack05` deleted after receipts copied here.
- Tools: system python3 only; no installs this seat.

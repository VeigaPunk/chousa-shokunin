# Probe15 — round65 receipt-pin traversal probe (isolated fixture)

## Scope
Leaf seat Probe15, lane chousa round65. One surface only: path-traversal / canonical-path
handling of the round65 receipt format, probed via the prefreeze reference
`corpus/evidence/round65/controls/ref-receipt-pin.py` (production `tools/receipt-pin.py`
may not exist yet — not required for this probe). No full battery run. No production writes.

## Method
- Scratch repo created at `/fast/scratch/hyaku/chousa-r65/Probe15/repo` (single commit,
  one blob `file.txt`). Scratch deleted after receipts were copied out.
- Expected outcomes derived **independently** from the frozen format in
  `corpus/evidence/round65/claims.md` (C1): `REVISION` must equal caller `--revision`
  (full lowercase 40 hex); `EXIT` decimal 0..255; `SHA256` 64 lowercase hex plus a
  **canonical relative POSIX path**; blank separator; nonempty output; exit codes
  0 consistent / 1 invalid / 2 usage-environment. No expectations were copied from the
  reference implementation.
- 23 cases (20 receipt cases + 3 argv/usage cases) run with argv and stdout/exit preserved
  verbatim in `probe15-traversal-results.jsonl`.

## Result
`cases=23 mismatches=0`, driver exit 0. Reference behavior matches the independently
derived contract on every traversal and consistency probe.

### Traversal surface (all correctly rejected, exit 1)
| case | receipt path field | expected | actual |
|---|---|---|---|
| t02 | `/etc/passwd` (absolute) | 1 | 1 |
| t03 | `../escape.txt` (dotdot lead) | 1 | 1 |
| t04 | `sub/../../file.txt` (dotdot mid) | 1 | 1 |
| t05 | `./file.txt` (dot prefix, non-canonical) | 1 | 1 |
| t06 | `a//file.txt` (double slash) | 1 | 1 |
| t07 | `.` (normalizes to empty) | 1 | 1 |
| t08 | `file.txt/` (trailing slash) | 1 | 1 |
| t09 | `..` (dotdot only) | 1 | 1 |
| t10 | `file.txt\0.txt` (NUL lookalike) | 1 | 1 |

Notable: the canonical-path rule rejects not only `..`/absolute escapes but also benign
non-canonical spellings (`./`, `//`, trailing slash). This matches "canonical relative
POSIX path" in the frozen format and is the intended strictness, but any production
fixture generator must emit already-canonical paths or it will fail its own receipts.

### Consistency probes (all exit 1)
t01 valid path → 0. Revision mismatch (t11, t20), digest mismatch (t12), EXIT=256 (t13),
missing blank separator (t14), whitespace-only body (t15), swapped headers (t16),
duplicate header (t17), missing blob (t18), tree-as-path (t19) all → 1 as derived.

### Usage/environment (all exit 2)
u01 missing `--revision`, u02 uppercase revision, u03 non-hex revision → argparse `p.error`
→ exit 2, matching the frozen 0/1/2 contract.

## Evidence (this folder)
- `probe15-traversal-results.jsonl` — per-case argv, exit, stdout, stderr (23 rows).
- `probe15-traversal-fixture.py` — self-contained driver (creates repo, receipts, runs
  reference, compares against independent expectations).
- `t01-valid.receipt`, `t03-dotdot-lead.receipt`, `t05-dot-prefix.receipt` — preserved
  receipt samples.

## Risks / notes for L1
- Expectations were derived from the frozen claims text; the reference was treated as the
  system under test, not the oracle. 23/23 agreement is consistency evidence, not proof
  the reference is the intended C1 oracle — the round's counter `c1-count.py` remains the
  authority (not run here per seat scope).
- No tools installed this wave (fixture used system `python3` + `git` only).
- No git/jj mutations, no network, no production writes; scratch removed after copying
  receipts.

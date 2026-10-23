# CtlNoReaderC2 — C2 no-reader control report

Seat: `ChousaR31.CtlNoReaderC2` (godspeed lane).
Control: `/fast/scratch/hyaku/chousa-r31/CtlNoReaderC2/ctl-no-reader-c2.sh`
(`gate_sha256 3906bc…dc1b`). It NEVER opens any source file under `--root`;
it reads only the claims JSONL (`json` parse, no filesystem access to `src/`).

## Results (5 fresh seeds)

| control | counter | seed | score | receipt |
|---|---|---|---|---|
| no-reader c2 | `c2-count.py` | 9001 | 86/120 | `controls/CtlNoReaderC2/receipt-seed9001.json` |
| no-reader c2 | `c2-count.py` | 9002 | 86/120 | `controls/CtlNoReaderC2/receipt-seed9002.json` |
| no-reader c2 | `c2-count.py` | 9003 | 86/120 | `controls/CtlNoReaderC2/receipt-seed9003.json` |
| no-reader c2 | `c2-count.py` | 9004 | 86/120 | `controls/CtlNoReaderC2/receipt-seed9004.json` |
| no-reader c2 | `c2-count.py` | 9005 | 86/120 | `controls/CtlNoReaderC2/receipt-seed9005.json` |

Deterministic: identical per-class verdicts on all 5 seeds. `predicate_holds=false` in every receipt. Baseline (do-nothing base gate): 50/120.

## Decision policy (features used)

For each claim, from the JSONL record alone (`id`, `source`, `span`, `sha256`, key order ignored):

1. `sha256` absent → `observed=supported`. (Only class N1 lacks the field; N1 is always span-present → 16/16.)
2. `sha256` not matching `^[0-9a-f]{64}$` → `observed=invalid`. (Catches all 14 I1 variants: upper/short/long/prefixed/nonhex/spaced.)
3. `sha256 == sha256(span.encode('utf-8'))` → `observed=stale`. (Catches all 10 S3 hash-of-span.)
4. Remaining valid-format `sha256` → `observed=stale`. Dominant per-claim policy: among the 80 valid-format non-span-hash claims the hidden truth is 46 stale (S1 16 + S2 12 + S4 10 + S5 8) vs 34 correct-sha (R1 24 + R2 10); any other constant verdict scores worse (supported → 24, unsupported → 10). Catches all 46.

Score = 16 + 14 + 10 + 46 = 86/120.

## Findings — leaks beyond the format-invalid class and the hash-of-span class

- **Structural leak 1 (N1 ⇒ no-sha ⇒ supported, 16 pts):** the generator emits exactly one class without `sha256`, and that class is always span-present. A no-reader control earns 16 by the mere *presence* of the field — no content check.
- **Structural leak 2 (blob dominance, 46 pts):** among valid-format shas, stale outnumbers correct-sha 46:34, so a no-reader control that *never verifies a single hash* still correctly labels 46/56 stale claims. This is the main reason the no-reader control (86) beats the base gate (50).
- **Cross-claim sha equality (S5):** adds nothing. Blanket-stale already catches all 8 S5; duplicate groups (owner + S5) cannot be disambiguated without file bytes, and owner misclassification exactly offsets any gain.
- Boundaries of the class: the remaining 34 (R1/R2) require the true source bytes — a no-reader control cannot reach better than 86 on this fixture.

## Tooling

No tools installed (vanilla `bash` + `python3`); no pacman/uv/npx actions. No network used.

## Verdict

**design holds** — no-reader controls cannot approach 120/120 (max 86/120, deterministic); the C2 core (hashing exact source bytes) is not skippable without reading files. The fixture does leak 86/120 to a claims-only reader via the two structural leaks above, so the counter is a weak discriminator against weak controls; that is a fixture/tester concern for the axis critic, not a break of the claim's contract.

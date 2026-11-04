# R74Critic — counter-discrimination attack on the r74 loader matrix

Seat R74Critic-2 · lane chousa-shokunin · frozen revision verified: `git rev-parse HEAD` =
`1eaa30ad248bbd3bd7469b2c17295fcda5fc02bb`, the four read artifacts
(`corpus/evidence/round74/correction-count.py`, `corpus/evidence/round74/loader-matrix.py`,
`corpus/evidence/round73/c2-count.py`, `corpus/evidence/round74/claims.md`) porcelain-clean,
git blob hashes == HEAD blobs. No lane/fixture-index mutation; fixtures lived only in
`/fast/scratch/hyaku/chousa-r74/R74Critic/work/` (matrix-created, removed after receipt copy).

Axes attacked (godspeed): fixed-behavior discrimination, context-dependent (order) forgery,
positive replication, negative-control fidelity, fail-closed coverage honesty, digest anchoring.

## Bounded probes (all authorized; six concurrent loader-matrix runs, one work dir each)

| counter scored | matrix exit | result | per-case (PASS/FAIL) |
|---|---|---|---|
| r74 `correction-count.py` | 0 | `LOADER_MATRIX=9/9 C1=PASS` | all 9 PASS |
| r73 `c2-count.py` (original) | 1 | `LOADER_MATRIX=3/9 C1=FAIL` | unchanged/replace-equal/receipt-change PASS; 3×append + 3×delete FAIL |
| forge always-pass | 1 | `4/9 C1=FAIL` | only unchanged+3×append PASS |
| forge always-fail (C2-6) | 1 | `4/9 C1=FAIL` | only 3×delete+replace-equal PASS |
| forge always-fail (C2-7) | 1 | `1/9 C1=FAIL` | only receipt-change PASS |
| **forge order-oracle** | **0** | **`LOADER_MATRIX=9/9 C1=PASS`** | **all 9 PASS, zero lane reads** |

Every run's `COUNTER_SHA256=` receipt was recomputed and matched the scored file
(digest_anchored=True ×6). r74 receipt: `COUNTER_SHA256=9334721a5e7a4080255b478771bf5443739738fb1936b40c116da28d7fa8ac41`.

## Findings

- **F1 — positive replication.** The r74 successor scores 9/9 exit 0 with each case's
  (rc, single failed-id) exactly as the matrix expects (deletes/replace → C2-6,
  receipt → C2-7, rest clean). C1's positive conjunct reproduces from a critic-owned scratch.
- **F2 — negative control reproduced with the claimed mechanism.** r73's `load()` reads
  `int(parts[0])` (the *added* column) as deletions and falls back `else 0` (fail-open).
  Observable split: clean appends get spurious `deleted=1` → C2-6 falsely FAILs (append
  rejection); real deletions get `col0="0"` → C2-6 falsely PASSes (deletion acceptance).
  Exactly the 3/9 pattern claims.md describes. replace-equal/receipt-change are column-blind
  and pass under both counters — they cannot isolate the defect, consistent with the claim.
- **F3 — every fixed behavior is rejected.** No constant (rc, failed-id-set) output passes
  all nine cases: 4/9, 4/9, 1/9 for the three forges. The matrix's contract — rc plus
  exactly one expected failed id plus exactly 7 checks — pins observable behavior uniquely.
- **F4 — full-mark forge exists (counterexample).** `forge-order-oracle.py` scores
  `LOADER_MATRIX=9/9 C1=PASS` exit 0 while never reading `--lane`, git, or any file: it
  counts its own invocations against the matrix's fixed deterministic case order. The matrix
  is a behavior-only discriminator and is provenance-blind. Mitigation already present: it
  prints `COUNTER_SHA256` of the scored file before any case, so a forged 9/9 is detectable
  iff the digest is checked. **Smallest safe correction:** integration (L1) must verify the
  receipt digest equals sha256 of the frozen `corpus/evidence/round74/correction-count.py`
  (`9334721a…8ac41`) and never rest on the `LOADER_MATRIX=9/9` line alone. No frozen artifact
  change required; not a claim-broadening finding (scope stays nine cases).
- **F5 — coverage honesty note, not a defect.** r74's fail-closed `else 1` on a nonnumeric
  deletion cell is unreachable in all nine cases (`--numstat` prints `-` only for binary
  files; the three PATHS are always text). Direction is strictly safer than r73's fail-open
  `else 0`, but no case certifies it — correctly outside the claim's nine-case scope.
- **F6 — cosmetic, frozen.** r74 counter's argparse description still says
  "round-73 C2 counter (frozen)" (inherited from r73). No action; frozen artifact.

## Verdict

Counter discrimination itself holds: the frozen matrix separates r73 (3/9) from r74 (9/9)
over real committed fixtures through the public CLI and rejects all constant-behavior forges.
The one real hole is provenance blindness (F4), closed by the digest receipt provided the
digest is actually verified at integration. Historical r73 admission stays rejected: its own
9-case score is 3/9. No hidden regression, duplicate authority, or identity change found.
No claim broadening; the nine-case scope stands.

## Evidence (absolute paths)

- Receipts: `/home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-74/w1/R74Critic/`
  — `r74-counter.log`, `r73-original.log`, `forge-always-pass.log`, `forge-always-fail6.log`,
  `forge-always-fail7.log`, `forge-order-oracle.log`, plus the four forge sources.
- Scored frozen artifacts (lane, HEAD-verified blobs):
  `/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round74/loader-matrix.py`
  (blob `8143ce2bcf5739901a999783fadb23691522f4c3`),
  `/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round74/correction-count.py`
  (blob `c113b5c2ba50fe877d21f5e6051284474dc6fd92`, sha256 `9334721a…8ac41`),
  `/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round73/c2-count.py`
  (blob `0ca1853afbd44e648d3e7fcd8fb03c8792c6dbbb`).
- Scratch `/fast/scratch/hyaku/chousa-r74/R74Critic/` removed after receipt copy.

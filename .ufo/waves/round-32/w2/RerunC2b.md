# RerunC2b — W2 falsification, round-32 C2 (exempt-hop audit)

Seat: ChousaR32A2.RerunC2b. Access date 2026-10-23.
Target: re-run `c2-count-v2.py` on the landed gate with `--keep` on two fresh seeds; audit
hidden truth — all-`resolved` record vs base gate, original record vs landed gate.

## Setup (all verified by sha256)

- Landed clone: `git clone` lane → `checkout 5d8a1707…`; gate `10f2fe1204…b4098` ✓ (context value).
- Base gate: `git show 7a7259f0…:tools/research-gate.sh` → `0bc318b3e7…11258` ✓ (context value).
- Counter `8ec1a1ed…` unchanged. Scratch: `/fast/scratch/hyaku/chousa-r32/w2/RerunC2b/`;
  `C2_TMP`/`TMPDIR` = `$D/tmpA|tmpB` (outside every lane root); receipts in this dir.

## Counter runs (every run reported)

| run | seed | output | rc | receipt |
|---|---|---|---|---|
| A-first | (fresh) | `EXEMPT_AUDIT_MATCH=132/132`, all classes full | 2* | none — receipt dir missing at write time; harness error, gate itself scored 132/132 |
| B-first | — | `mkdtemp` fail (tmp2 parent absent) | 2 | none — no gate run happened |
| A | 15123522876773114482 | `EXEMPT_AUDIT_MATCH=132/132`, `RECORD_CHECKS=ok`, gate_rc=1 | 0 | `c2-landed-runA.json` (predicate_holds=true) |
| B | 12633912059466704036 | `EXEMPT_AUDIT_MATCH=132/132`, `RECORD_CHECKS=ok`, gate_rc=1 | 0 | `c2-landed-runB.json` (predicate_holds=true) |

Commands were
`prlimit --nproc=8000 timeout 900 python3 corpus/evidence/round32/c2-count-v2.py --gate tools/research-gate.sh --receipt .ufo/waves/round-32/w2/RerunC2b/c2-landed-run{A,B}.json --keep /fast/scratch/hyaku/chousa-r32/w2/RerunC2b/keep{A,B}`
from the lane root. No run on the landed gate printed below 132.

## Hidden-truth audit (`audit.py`, results `audit-results.json`)

Truth map reconstructed by importing the committed counter and calling `generate(tmp, seed)`;
the regenerated record is byte-identical to the kept record (e.g. A: sha256
`99d92b9c…1fa3` both files), so hid→(class,truth) is exact.

### Base gate `0bc318b3` on all-`resolved` record (132 statuses rewritten; `rewrote=132`)

Both seeds identical result:
- `RESOLVED_HOPS=60/132`, `RESEARCH_GATE: DRIFT (… verified=60 exempt=0 anchor-missing=42
  refused=24 invalid=6 findings=72 drift=72)`, rc=1.
- Verified set **exactly** R1(12)+R2(12)+R3(12)+F1(12)+E5(12): `verified_minus_expected=[],
  expected_minus_verified=[]`, no duplicate CHAIN lines.
- Non-verified per class: E1/E8/E9/E10/E11/E12 `anchor-missing/mismatch` (42); E2 missing
  file, E3 external URL, E6 undeclared id, E7 out-of-corpus `refused/refused` (24);
  E4 bare path with no anchor `invalid/invalid` (6). E4 stays unverified — the
  "no citation" hop is not silently verified by the old gate.
- Raw: `base-A.out`, `base-B.out`.

### Landed gate `10f2fe12` on the original kept record

Both seeds identical result:
- rc=1, exactly one `RESEARCH_GATE: DRIFT` line, 132 CHAIN lines (one per hop, no dups),
  no FINDING naming a hop outside the record.
- **Every E-class hop** (E1–E12, 84 hops incl. E5's rejected/not-applicable rows):
  `observed=exempt … verdict=exempt`, and **zero findings** name any E-class hop
  (`E_bad=0`). E5 rows print `anchor=- at=-` — unread, per contract.
- R1–R3 (36): `observed=resolvable` with exactly one `FINDING CHAIN_EXEMPT_RESOLVABLE`
  each (`resolvable_findings=36`); F1 (12): `verified/match`, no finding
  (`nonE_bad=0`).
- Summary: `hops=132 verified=12 exempt=84 … findings=36 drift=36 resolvable=36`.
- Raw: `landed-A.out`, `landed-B.out`.

Fixture integrity: keep trees hold 115 + 115 + 2 rewritten-record files only — the gates
mutated nothing (`rewrote` files are mine, placed as new names).

## Verdict

**HOLDS.** No below-target run on the landed gate (two receipted 132/132 + one
pre-receipt 132/132). The base-gate compat check verifies exactly R1–R3/F1/E5 (60),
refusing or invalidating every E-class hop including E4's anchor-less citation. The
landed gate's exempt arm prints `observed=exempt` with no finding for all 84 E-class
hops on both seeds. Nothing falsified; no contract violation found.

## Limits / residual risk

- Two seeds; the audit re-derives truth from the counter's own `generate()`, so a bug in
  the generator's hidden-truth model itself (e.g. a class that is secretly resolvable in
  a way the resolved arm would also miss) is out of scope of this check.
- The first A run's 132/132 had no receipt (harness error, rc=2 from `--receipt` write
  after the gate ran); it is reported here for completeness per "report every run".
- Base-gate run used the base gate alone in `baselane/` (extracted file, sha-pinned);
  verify-chain needs no other lane files.
- No installs. Scratch dir `/fast/scratch/hyaku/chousa-r32/w2/RerunC2b/` left intact for
  re-inspection.

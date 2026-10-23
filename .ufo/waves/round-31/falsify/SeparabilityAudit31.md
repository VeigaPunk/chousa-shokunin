# SeparabilityAudit31 — separability claim and the L1's one-sided builds

Round 31, WAVE 2 FALSIFY. Lane commit `8070f92b` (design v2) / controls `86188116` /
C1 `c17948a` / C2 `6d0ae19` / tip `ee1024f`. All runs 2026-10-23. Scratch:
`/fast/scratch/hyaku/chousa-r31/w2/SeparabilityAudit31/` (clone of the lane at `ee1024f`).
No lane byte mutated; no git/jj write; no tool installed or updated.

## What was attacked

1. Identity of `.ufo/waves/round-31/measure/c1only-build.sh`.
2. Identity of `.ufo/waves/round-31/measure/c2only-build.sh`.
3. The four-cell separability matrix with fresh seeds (each counter on each one-sided
   build), plus base-gate and tip-gate controls.
4. Provenance of the recorded separability receipts, and whether the archived builds
   are usable as gates where they are committed.

## 1. `c1only-build.sh`

    sha256sum measure/c1only-build.sh
    3b5279eb0f312b41b0e5b6fec56d021a3c3525fb18af148650caa65fb8abbc3b
    git show c17948a:tools/research-gate.sh | sha256sum
    3b5279eb…babc3b          cmp: identical

Byte-identical to the gate at the C1 commit `c17948a` — no copy drift. Differencing:
- `c1only` vs base `8070f92b` gate (`ac1315dd`): 11 hunks, all C1 additions.
- `base + ExecC1Impl/c1.patch` (`6c581ccf`) vs `c1only`: exactly one hunk — the L1's
  string-equality compare (`[[ $l1 == "$line_n" && $l2 == "$line_m" ]]`).
- `c1only` vs tip (`c23d7537`): 11 hunks, all C2 additions (`sha256`, `stale`,
  `CLAIM_SOURCE_REVISION_MISMATCH`, C2 selftest cases 216–224). No C2 code present
  (`grep -c 'sha_pin\|sha_present\|sha_actual'` = 0; `CLAIM_SOURCE_REVISION_MISMATCH` = 0).
Selftest: 219 cases when run from a `tools/`-shaped path (PASS), base is 215 + 4 C1 cases.

## 2. `c2only-build.sh`

    sha256sum measure/c2only-build.sh
    a221983580f757e1c3d515bee66144603c5aa300c30708b22869d39ebe3b2434

**No commit's gate equals it** (`git rev-list --all`, 153 revisions, none matched) — expected,
because C2 landed on top of C1 and no C2-only commit exists. It is nonetheless reproducible
exactly: `base 8070f92b` gate (`ac1315dd`) + `ExecC2Impl/c2.patch` = `41b294fd…`; differencing
`41b294fd` against `c2only` yields exactly 4 hunks, and each is an L1 C2 fix byte-identical to
the tip's code:
- add `json_has_key()` (needed to see a *present* non-string `sha256`),
- `sha_present=1; sha_pin='-'` when the key is present but not a string → `observed=invalid`,
- fail-closed hash (`[[ $sha_actual =~ ^[0-9a-f]{64}$ ]] || sha_actual=unreadable`),
- `bad="sha256 malformed (not 64 lowercase hex characters)"`.

`c2only` vs tip: 10 hunks, every one a C1-only removal (finding-ID header, doc text,
`--help` line, `tok_span_all`, `linef` locals, `line` grammar, binding block, 4 C1 selftest
cases). `grep -c 'CLAIM_LINE_MISMATCH\|tok_span_all'` = 0. Applied on top of `c1only`,
`c2.patch` fails 4/11 hunks (context drift) — that is why the L1's landed C2 differs from the
raw patch; the `c2only` file is the correct "tip minus C1" reference.
Selftest: 224 cases when run from a `tools/`-shaped path (PASS), base 215 + 9 C2 cases.

## 3. Four-cell table (fresh seeds, frozen counters, receipts in this dir)

Counters: `c1-count.py` sha `c3aca35d…`, `c2-count.py` sha `1064fdb3…` (both equal the tip
commit's bytes and the lane working tree's bytes).

| counter \ build | C1-only (`3b5279eb`) | C2-only (`a2219835`) |
|---|---|---|
| C1 counter | **120/120**, 120/120 (seeds 880011001, 880011011) | **50/120**, 50/120, 50/120 (880011002, 880011013, 880011061) |
| C2 counter | **50/120**, 50/120, 50/120 (880011003, 880011012, 880011062) | **120/120**, 120/120 (880011004, 880011014) |

Controls: base gate `ac1315dd` → C1 50/120, C2 50/120 (880011021/22). Tip gate `c23d7537`
→ C1 120/120 ×2, C2 120/120 ×2 (880011031–34). Same cross-cells also run through the
committed paths (`.ufo/waves/round-31/measure/c1only-build.sh`, `c2only-build.sh`) from the
lane root: 50/120 and 50/120 (880011071/72).

Expectation from `claims.md` Separability ("must print their before values (50/120)") is met
on two fresh seeds per cross-cell plus one extra; every counter on its own build is 120/120.
**The cross-cell is not merely 50 by arithmetic: its per-class vector is identical to the base
gate's** (C1: B1 12/12, B2 12/12, B3 12/12, B4 6/6, M1–M6 0, I1 0/12, U1 8/8; C2: R1 24/24,
R2 10/10, N1 16/16, S1–S5 0, I1 0/14). So each build behaves exactly like the do-nothing gate
on the other claim, not "partly".

Cross-field probe on the tip (hand fixture, scratch): `{"line":"2","sha256":<correct>}` →
supported; `{"line":"3","sha256":<correct>}` (span on line 2) → mislocated +
`CLAIM_LINE_MISMATCH`; `{"line":"3","sha256":<stale>}` → `stale` (`FINDING
CLAIM_SOURCE_REVISION_MISMATCH`), line binding skipped — matches C2 contract item 2
(“before and regardless of the span check”). `"line":5` (non-string) → invalid on tip and
`c1only`; `c2only` ignores it as an unknown key → supported, i.e. base behaviour, no leak.

## Findings

- **F1 (provenance, minor).** `measure/sep-c2-on-c1only.json` records `"gate":
  "tools/research-gate.sh"` with `gate_sha256=3b5279eb…`. That path today holds the tip gate
  (`c23d7537…`); replaying the recorded command literally now yields 120/120, not 50/120. The
  bytes are preserved (sha matches `measure/c1only-build.sh`), so nothing is mis-scored — but
  the receipt's gate path is stale. Smallest correction: name `measure/c1only-build.sh` in the
  receipt (no re-run needed; `gate_sha256` already disambiguates).
- **F2 (operability, minor).** The archived builds only reproduce their own selftest from a
  `tools/`-shaped path. Run in place (`bash .ufo/waves/round-31/measure/c1only-build.sh
  --selftest`) → `FAIL (2/219)`; `c2only-build.sh` → `FAIL (2/224)`; both failures are
  lane-root derived (`claims-lane-fallback`, `ptr-lane-abs` resolve `LANE_ROOT` to
  `.ufo/waves/round-31`, which has no `PROVINCE.md`). Copied to `<tree>/tools/` both PASS
  (219 / 224). The counters are unaffected (both cross-cells rerun through the committed
  paths give 50/120). Not a landing defect; a caveat for anyone selftesting the archive in place.
- **F3 (coverage of the frozen counters, not of the landing).** `base + c2.patch` alone scores
  **120/120** on the C2 counter (880011041), and `base + c1.patch` alone scores **120/120** on
  the C1 counter (880011051). So the L1's hardening rules (non-string `sha256` → invalid,
  fail-closed unreadable hash; string vs numeric line compare) are not exercised by either
  frozen counter — they are exercised by the gates' own selftests. Counters are frozen; no
  re-scale. Consequence for reading P1/P2: a 120/120 does not by itself certify those rules.
- **F4 (attribution asymmetry, not a defect).** The C1-only build is a real commit
  (`c17948a`); the C2-only build is a hand-assembled file with no matching commit, and its
  `json_has_key` helper is a function that the C1 patch introduced. Measured separability still
  holds (C1 counter 50/120 on it), but "C2 adds only `sha256`" is backed by a reference build,
  not by a checkout.

## Verdict

**Holds.** `c1only-build.sh` is byte-identical to the gate at `c17948a`; `c2only-build.sh` is
exactly `base(8070f92b) + c2.patch + the L1's 4 C2 fixes` and exactly tip-minus-C1. The
separability claim reproduces on fresh seeds: cross-cells 50/120 with per-class vectors equal
to the base gate's, own-cells 120/120, base 50/50, tip 120/120. No hidden regression, no
identity change, no re-scaled count. Only provenance/operability nits (F1, F2) and a
counter-coverage limit (F3).

## Limits

- Falsify wave is single-seat and read-only on the lane; findings were produced from a clone.
- The frozen counters' seeds I used are new (880011×); the L1's recorded seeds were not reused.
- The C2-only build cannot be checked against a commit (none exists); its verification is the
  two diffs above, not a hash-to-commit match.
- In-place selftest failures (F2) were measured, not inferred; I did not attempt a
  `CHOUSA_ROOT` workaround (the gate scrubs `CHOUSA_*` under the counters only).

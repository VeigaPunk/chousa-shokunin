# FRegistryNoId — C3 no-S-id (legacy) path, round 26 attempt 1

Seat `ChousaR26R.FRegistryNoId` (scout; author-lane advice, not a judge).
Target: C3 relation/grammar case — "no S-id in `source:` → `META_SOURCE_NO_ROW_ID`
info (legacy-compatible)", clean unless `CHOUSA_STRICT=1`
(`corpus/evidence/round26-claims.md:99`, spec-v1 correction `:133-141`).

## Revisions measured

| role | revision | `tools/research-gate.sh` sha256 |
|---|---|---|
| target (from `round26-measured-revision.json`) | `0e9784bd52eca456b24d0bc40921480a47f91a2b` | `c2c813f1…2143abc6` (equals the pinned input) |
| claim base | `ba3333254dd337658a4f25e7a9471f9cf4e4567e` | `985a6320…f91532` |

Both trees came from `git archive <rev> | tar -x` into
`/tmp/chousa-r26-falsify-FRegistryNoId/{tree,base}`; the moving working tree was
not graded. Base registry: `git show ba33332…:corpus/SOURCES.md` (sha256
`bfd47b5d…`). Scripts and raw logs: `/tmp/chousa-r26-falsify-FRegistryNoId/{run.sh,run.log,pop.sh,pop.log}`.

## Commands and exits

- `bash run.sh` → exit 0. It ran 15 fixtures × `CHOUSA_STRICT` ∈ {0,1}, 4 strict-value forms, `--as-of` composition, an entry outside `--root`, directory mode, a no-flag hold, and the base `--registry` rejection.
- `bash pop.sh` → exit 0. It ran the frozen 29 with the base registry under strict 0 and 1, a stripped r24 entry, and a replica of the probe's noid control.
- An inline loop comparing target and base `verify-metadata` on the frozen 29 without a flag, under strict 0 and 1, exited 0.

Not run: selftest, build, lint, `round26-measure.sh`, the 8 MiB probe, and mutations.

## Observed: the claim holds as stated (not falsified)

Each case below uses `verify-metadata F --root W --registry REG`.

| fixture | strict=0 | strict=1 |
|---|---|---|
| legacy prose + hex commit (`legacy.md`) | rc0 CLEAN, `NO_ROW_ID` info | rc1 DRIFT drift=1, entry `verdict=drift` |
| empty `source:` | rc0 CLEAN, info | rc1 DRIFT |
| non-ids `s001 S01 S-001 S_001 _S001 S001x 9S001` | rc0 CLEAN, info | rc1 DRIFT |
| S001 only in `verified-at`/`recheck`/body/after blank/`## ` heading | rc0 CLEAN, info | rc1 DRIFT |
| S001 on an indented line after a blank line (continuation ended) | rc0 CLEAN, info | rc1 DRIFT |
| CRLF legacy | rc0 CLEAN, info | rc1 DRIFT |
| fullwidth digits `S００１` | rc0 CLEAN, info | rc1 DRIFT |
| `S001 plus legacy prose` (mined, used-by matches) | rc0 findings=0 | rc0 findings=0 (no `NO_ROW_ID`) |
| legacy + bare `verified-at` | rc1, `NO_ROW_ID` info + `VERIFIED_AT_BARE` warn | rc1 drift=2 |
| legacy + `--as-of 2026-10-21` | rc0, `due=2027-01-18 freshness=current verdict=clean` + info | rc1 |
| legacy outside `--root` | rc0 CLEAN, info | — |
| dir {good, legacy} | rc0 CLEAN; only legacy carries info | rc1; only `legacy.md verdict=drift` |
| `CHOUSA_STRICT` = `true`/`yes`/`01`/` 1` | rc0 CLEAN (only the literal `1` is strict; `research-gate.sh:287,398`, header `:11`) | — |

Holds:
- **No flag.** Target and base output (timestamp line dropped) plus rc are byte-identical on all 15 fixtures under strict 0 and 1. On the frozen 29, strict=0 gives sha16 `3f83ba48…` rc1 drift=3 on both trees, and strict=1 gives `f4197c26…` rc1 drift=33 on both.
- **Base.** The base gate rejects `--registry` with rc 2.
- **Frozen 29 with the base registry, strict=0.** rc1 DRIFT findings=57 drift=3. `NO_ROW_ID`=24, exactly the 24 pre-r24 entries. Other registry findings=0, and all 5 r24+ entries are `verdict=clean`. The drift=3 is the pre-existing count with no flag, so the registry adds 24 info findings and no drift.
- **Probe noid control replica** (`round26-measure.sh:195,200-201`), with `CHOUSA_STRICT` unset or 0: rc0, `NO_ROW_ID` present → ok.

## Calibration findings (all exits observed)

**N1 — Elsevier PII/DOI tokens are read as S-ids. Spec-conformant, but it is a false positive.**
- `source: Lancet https://doi.org/10.1016/S0140-6736(20)30183-5` gives rc1 DRIFT at strict=0, with `FINDING META_SOURCE_ROW_MISSING severity=warn … source_id=S0140 registry row missing`.
- `…/science/article/pii/S0140673620301835` gives rc1 with `source_id=S0140673620301835`.
- An entry with a mined, used-by-matching `S001` plus such a URL (`pii-mined.md`) also gets rc1 `ROW_MISSING` for the PII token.

So a legacy source that has no registry S-id is not always CLEAN, even without strict. The cause is the spec-v1 correction itself: "`S` + three or more digits, standalone ASCII alphanumeric/underscore boundaries", where `/` and `-` count as boundaries. The implementation matches the spec (`research-gate.sh:2474`), so this is a spec-level calibration defect rather than code divergence. Frozen exposure is 0: `rg 'pii/S|10\.1016/S|S0[0-9]{3}-'` over the base and target `corpus/` returned no hits. It is a live risk for any future entry that cites ScienceDirect or Elsevier journals.

**N2 — A duplicated `source:` key silently discards an S-id.**
`source: S001` followed by `source: legacy prose replaced` gives rc0 CLEAN with `NO_ROW_ID` info at strict=0. The registry check never sees S001 because the last key wins (`research-gate.sh:2664-2665` resets `source_value`). This overlaps the `FHeaderDuplicates` seat. The spec does not define duplicate keys.

**N3 — By design, "no S-id" cannot fail an r24+ entry without strict.**
`citation-chain-fidelity-r24.md` with every `S[0-9]{3,}` removed gives rc0 CLEAN at strict=0 (`NO_ROW_ID` info plus the pre-existing `ROOT_PARENT` info), and rc1 at strict=1. Strict is not usable as a population gate: on the frozen 29 it drifts 57 findings, 24 of them legacy `NO_ROW_ID`.

The checker has no per-entry era signal, so the most basic criterion-6 violation (an r24+ entry with no S-id) is invisible under the non-strict mode used by `C3_POP_R24PLUS_CLEAN`. That count therefore cannot detect an r24+ entry that has lost all its ids. The claim scopes legacy entries out (`round26-claims.md:115-117`), so this is a disclosed trade-off, not a regression. It should still be named as a C3 calibration limit rather than read as criterion-6 coverage.

**N4 — Double count when `source:` is absent.**
`no-source.md` emits both `META_SOURCE_ABSENT` warn and `META_SOURCE_NO_ROW_ID` info, so strict=1 gives drift=2 for one defect (strict=0: rc1 drift=1). The spec wording "no S-id in `source:`" is ambiguous when the key is missing. This is a minor tally inflation, and the verdict is unchanged.

**N5 — The probe's noid control depends on the environment (probe only).**
`round26-measure.sh` does not unset `CHOUSA_STRICT` (no match for `STRICT` in the file). The exact replica of its noid control gives rc1 → `control=MISS` under an inherited `CHOUSA_STRICT=1`. The selftest isolates this (`research-gate.sh:6145` sets `CHOUSA_STRICT=0`). Production behavior is correct; only the probe's `C3_CONTROLS_CAUGHT` can drop to 4/5 depending on the caller's environment.

## Inference / unknowns

- [INFERENCE] N1 is the likeliest real-world false positive for this lane's research sources; that frequency is not measured.
- The 3 non-strict drifts on the frozen 29 were not attributed per entry, because they are identical with no flag on both trees.
- No mutation was run, so the kill of the `NO_ROW_ID` arm is not shown here (owned by the mutation seats).

Tool installs/updates: none.

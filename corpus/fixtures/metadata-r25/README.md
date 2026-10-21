# Round-25 `verify-metadata` fixtures

Hand-derived from spec v1 in `corpus/evidence/round25-claims.md` (lines 20–40). The 18 defect mutants cover all six finding IDs plus alternate key-placement/value forms. Six additional edge cases pin accepted CRLF, BOM-title, continuation, and recheck forms. Mutation files and those six edge cases use the header and first `## Claim` from `corpus/knowledge/claim-support-states-r24.md`; `control-citation-fidelity.md` and `control-contextual-admission.md` use the matching header and first heading from `corpus/knowledge/citation-chain-fidelity-r24.md` and `corpus/knowledge/contextual-source-admission-r24.md`, respectively, while `control-claim-support.md` uses the first seed. Each fixture is under 40 lines and applies only its named mutation (controls have none). `source-continuation.md` intentionally uses an empty `source:` line followed by a source-value continuation.

`normal` means `CHOUSA_STRICT` unset; `strict` means `CHOUSA_STRICT=1`. Each cell gives the exact expected per-entry `META` line in normal / strict mode, followed by finding IDs and exit status. `—` means no finding. Outcomes below are spec-v1 expectations, written by hand; this fixture author did not execute the gate.

| File | Expected META line (normal / strict) | Expected FINDING IDs | Exit (normal / strict) |
|---|---|---|---|
| `missing-source.md` | `META entry=missing-source.md source=absent verified_at=dated recheck=scheduled verdict=drift` / same | `META_SOURCE_ABSENT` | 1 / 1 |
| `missing-verified-at.md` | `META entry=missing-verified-at.md source=present verified_at=absent recheck=scheduled verdict=drift` / same | `META_VERIFIED_AT_ABSENT` | 1 / 1 |
| `missing-recheck.md` | `META entry=missing-recheck.md source=present verified_at=dated recheck=absent verdict=drift` / same | `META_RECHECK_ABSENT` | 1 / 1 |
| `undated-verified-at.md` | `META entry=undated-verified-at.md source=present verified_at=undated recheck=scheduled verdict=drift` / same | `META_VERIFIED_AT_UNDATED` | 1 / 1 |
| `undated-verified-at-slash.md` | `META entry=undated-verified-at-slash.md source=present verified_at=undated recheck=scheduled verdict=drift` / same | `META_VERIFIED_AT_UNDATED` | 1 / 1 |
| `recheck-from-no-colon.md` | `META entry=recheck-from-no-colon.md source=present verified_at=dated recheck=absent verdict=drift` / same | `META_RECHECK_ABSENT` | 1 / 1 |
| `command-only-recheck.md` | `META entry=command-only-recheck.md source=present verified_at=dated recheck=unscheduled verdict=clean` / `META entry=command-only-recheck.md source=present verified_at=dated recheck=unscheduled verdict=drift` | `META_RECHECK_UNSCHEDULED` | 0 / 1 |
| `unrecognized-recheck.md` | `META entry=unrecognized-recheck.md source=present verified_at=dated recheck=unscheduled verdict=clean` / `META entry=unrecognized-recheck.md source=present verified_at=dated recheck=unscheduled verdict=drift` | `META_RECHECK_UNSCHEDULED` | 0 / 1 |
| `root-parent-recheck.md` | `META entry=root-parent-recheck.md source=present verified_at=dated recheck=scheduled verdict=clean` / `META entry=root-parent-recheck.md source=present verified_at=dated recheck=scheduled verdict=drift` | `META_RECHECK_ROOT_PARENT` | 0 / 1 |
| `indented-source.md` | `META entry=indented-source.md source=absent verified_at=dated recheck=scheduled verdict=drift` / same | `META_SOURCE_ABSENT` | 1 / 1 |
| `indented-verified-at.md` | `META entry=indented-verified-at.md source=present verified_at=absent recheck=scheduled verdict=drift` / same | `META_VERIFIED_AT_ABSENT` | 1 / 1 |
| `fenced-source.md` | `META entry=fenced-source.md source=absent verified_at=dated recheck=scheduled verdict=drift` / same | `META_SOURCE_ABSENT` | 1 / 1 |
| `fenced-recheck.md` | `META entry=fenced-recheck.md source=present verified_at=dated recheck=absent verdict=drift` / same | `META_RECHECK_ABSENT` | 1 / 1 |
| `source-below-heading.md` | `META entry=source-below-heading.md source=absent verified_at=dated recheck=scheduled verdict=drift` / same | `META_SOURCE_ABSENT` | 1 / 1 |
| `verified-at-below-heading.md` | `META entry=verified-at-below-heading.md source=present verified_at=absent recheck=scheduled verdict=drift` / same | `META_VERIFIED_AT_ABSENT` | 1 / 1 |
| `empty-recheck.md` | `META entry=empty-recheck.md source=present verified_at=dated recheck=unscheduled verdict=clean` / `META entry=empty-recheck.md source=present verified_at=dated recheck=unscheduled verdict=drift` | `META_RECHECK_UNSCHEDULED` | 0 / 1 |
| `malformed-source-key.md` | `META entry=malformed-source-key.md source=absent verified_at=dated recheck=scheduled verdict=drift` / same | `META_SOURCE_ABSENT` | 1 / 1 |
| `bom-source-first-line.md` | `META entry=bom-source-first-line.md source=absent verified_at=dated recheck=scheduled verdict=drift` / same | `META_SOURCE_ABSENT` | 1 / 1 |
| `crlf.md` | `META entry=crlf.md source=present verified_at=dated recheck=scheduled verdict=clean` / same | `—` | 0 / 0 |
| `bom-first-line.md` | `META entry=bom-first-line.md source=present verified_at=dated recheck=scheduled verdict=clean` / same | `—` | 0 / 0 |
| `source-continuation.md` | `META entry=source-continuation.md source=present verified_at=dated recheck=scheduled verdict=clean` / same | `—` | 0 / 0 |
| `recheck-iso-date.md` | `META entry=recheck-iso-date.md source=present verified_at=dated recheck=scheduled verdict=clean` / same | `—` | 0 / 0 |
| `recheck-90d.md` | `META entry=recheck-90d.md source=present verified_at=dated recheck=scheduled verdict=clean` / same | `—` | 0 / 0 |
| `recheck-on-release.md` | `META entry=recheck-on-release.md source=present verified_at=dated recheck=scheduled verdict=clean` / same | `—` | 0 / 0 |
| `control-claim-support.md` | `META entry=control-claim-support.md source=present verified_at=dated recheck=scheduled verdict=clean` / same | `—` | 0 / 0 |
| `control-citation-fidelity.md` | `META entry=control-citation-fidelity.md source=present verified_at=dated recheck=scheduled verdict=clean` / `META entry=control-citation-fidelity.md source=present verified_at=dated recheck=scheduled verdict=drift` | `META_RECHECK_ROOT_PARENT` | 0 / 1 |
| `control-contextual-admission.md` | `META entry=control-contextual-admission.md source=present verified_at=dated recheck=scheduled verdict=clean` / same | `—` | 0 / 0 |

Correction (L1 integration, 2026-10-21): the first differential run
(`bash corpus/evidence/round25-meta-differential.sh` → `AGREE=50/54`) found two
derivation errors, adjudicated against spec v1's text. (1) This table's
`control-citation-fidelity.md` row expected no finding, but the control is a
byte copy of `knowledge/citation-chain-fidelity-r24.md`'s header, whose
`recheck:` passes `--root ..` → `META_RECHECK_ROOT_PARENT` info (strict:
drift, exit 1); row corrected. (2) The oracle tokenized on whitespace only and
missed `--root ..` followed by a closing backtick; fixed in
`corpus/evidence/round25-meta-oracle.py` `has_parent_root`. The gate matched
spec v1 in all 54 cells; the receipt is `corpus/evidence/round25-meta-differential.log`.
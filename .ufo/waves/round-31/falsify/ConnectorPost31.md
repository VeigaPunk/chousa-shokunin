# ConnectorPost31 — adjacency after landing (round 31, WAVE 2 FALSIFY)

Axes: coverage (C1 line binding), operability (C2 revision pin). Attack target: `ConnectorSiblings31.md` adjacency claims vs the landed gate, plus `PROVINCE.md` ownership.

## Evidence checked
- Landed gate `tools/research-gate.sh:1460-1461`: `sha256` must match `^[0-9a-f]{64}$` (strict 64 lowercase hex; uppercase/short/prefixed values are invalid).
- Landed gate `tools/research-gate.sh:1503-1513`: hashes exact source bytes with `sha256sum`; boundary refusals precede hashing; stale finding prints `pin=<12> actual=<12>`.
- Landed gate `tools/research-gate.sh:1523-1564`: C1 requires a boundary-delimited occurrence starting on line N and ending on line M; existence-only line checks are insufficient.
- Sibling conventions re-checked: kumitate `scripts/cite-check.mjs` PIN_RE `7-40` hex + `digest.startsWith` (prefix pins); kasegi `corpus/instruments/anchorcheck.py` PIN `7-40` hex against `git show` blobs (git-object identity); kagi `corpus/drift-pins.sh`/`inrow-pins.tsv` accepts `reproduces-normalized`; kotoba `verifiers/verify_skill_checklist.py` hashes normalized box text and `check_substrate_pins.py` accepts uppercase hex.

## Verdict
Holds. No sibling duplicates C1/C2 wholesale; C1 remains the only text-placement check, and C2 remains a new carrier for an existing digest mechanism. The divergences are declared, not bugs:
- prefix pins (7-40 hex) vs C2 strict 64 hex;
- git-blob identity vs C2 bytes-read;
- normalized reproduction vs C2 byte-exactness;
- case-insensitive hex vs C2 lowercase-only.

## Report-not-absorb list
Do not absorb into chousa: prefix/short pins, git-revision pins, normalized-hash acceptance, uppercase hex, existence-only line checks. Keep C1 boundary-delimited placement and C2 exact-byte lowercase-64-hex pins. `PROVINCE.md` still describes the lane's ownership (`claim-vs-source verification`); no province change needed.

## Proposed move (one, bounded)
Improve operability without harming coverage: print the full 64-hex computed digest (not the current 12-hex prefix) in `CLAIM_SOURCE_REVISION_MISMATCH`, matching kasegi's full expected/actual output and making re-pinning self-service. Frozen counter parsing is unaffected (`FINDING_RE` keys on `obs=id=<id>` followed by whitespace).

## Limits
Read-only inspection only; no gate/counter/selftest executed by this seat; sibling classifications rest on the cited code paths.
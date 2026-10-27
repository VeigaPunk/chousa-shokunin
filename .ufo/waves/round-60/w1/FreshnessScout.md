# FreshnessScout — Round 60 scoped finding

## Finding

**Freshness verdict: unchanged / current validity unprovable.** The round-60 S101 material is fresh as an *offline capture check*, not as evidence that the cited specification remains in force. The frozen C2 predicate verifies the pinned raw capture digest, pinned text-form digest, and presence of one selected quote; it does not check the source's present-day status, re-fetch it, or verify a source-update date. Accordingly, C2=PASS cannot be interpreted as a freshness/current-validity pass.

## Evidence

- Frozen claim C2 explicitly limits itself to S101's offline capture and says external truth remains unknown; it requires reopening S101 offline, not a live check (`corpus/evidence/round60-claims.md:13-17`). Its intended distinction is appropriate for the available evidence.
- The current `corpus/evidence/round60/c2-count.py:6-21` pins S101 raw SHA-256 `6063a3af…fddf3` and text-form SHA-256 `a8e3e7ad…e79f867`, then checks the exact quote `c. 文献类型及载体类型标志；`, entry metadata, and a scoped Unknown statement. No freshness age, status/recheck field value, change signal, or current-authority predicate is checked. I ran the counter with isolated scratch work: `RAW_PIN=1/1 FORM_PIN=1/1 QUOTE=1/1 LINE=245 METADATA=1/1 LIMIT=1/1; C2=PASS` (exit 0). This proves the specified offline conditions only.
- The committed S101 reopening record (`corpus/evidence/round59/s101-open.txt:1-5`) identifies the HIT-hosted document and says it was captured 2026-10-23 and re-opened 2026-10-25. Those are capture/reopening dates, not a date of issuance or evidence of continuing validity. The opened text's carrier notation is present at line 71, but its text cannot establish current validity.
- The prior non-author spot-check explicitly admitted S101 only as source evidence and rejected current GB 3469 status/legal force as unsupported (`corpus/lessons/round-59-verifier-spotcheck.md:28-29`). The extant knowledge entry also records version-in-force as unknown (`corpus/knowledge/citation-count-semantics-r37.md:79-80`). This prior limitation is consistent with the current counter's scope; it is not evidence that the source has since been refreshed.

## Freeze identity warning

The dispatcher-specified frozen claim SHA was `09d8053f5f09a26c07f41286a7a885a2c21bff31b30f71963cceaa35d971a440`. Read-only `sha256sum` of the present `corpus/evidence/round60-claims.md` returned `65721569fc1336b159c7637acf476cda6f583bbd4b3a84aaadd239f7d02018d1`. Thus I cannot verify that the on-disk claims file is the claimed immutable freeze. I did not alter it. Any claim-admission conclusion dependent on this freeze should be held pending integrator resolution of the identity discrepancy; this scout's analysis is of the visible file and the specified current counter/source only.

## Boundaries

No external fetch was made. No assertion is made about whether S101 remains current or authoritative today; resolving that requires authorized access to a current authoritative source. No lane/source files were changed.
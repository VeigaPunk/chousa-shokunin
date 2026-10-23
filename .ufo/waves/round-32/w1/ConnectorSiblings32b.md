# Sibling-overlap scan — chousa C1/C2 (round 32 wave 1)

Scope: read-only scan of `/home/vgpnk/Projects/shokunin/*-shokunin` (excluding chousa corpus/live and reports noise) for (a) advisory file locking / concurrent JSONL appends and (b) auditing declared-unavailable or exempt citations/links. No counters were run; no lane/fleet state was mutated.

## Axes (chousa)
- Operability (C1): `verify-all … --json PATH` manifest append serialization.
- Coverage (C2): exempt-hop audit in `verify-chain`.

## (a) Advisory file locking / concurrent JSONL appends

| Lane | Path:line | What it does | Overlap with C1 |
|---|---|---|---|
| kagi | `corpus/knowledge/handler-on-disk-state.md:103-108`, `control-plane-hardening.md:104` | Shell `the-janitor` verbs take `flock 9` on a separate `client.lock` fd held across request/start/stop; documents wedge recovery and warns never delete/replace the lock file in place. | Adjacent concept only. Uses a *separate* lock file, not flock on the appended manifest fd. Does not implement C1 and must not be copied as-is: C1 contract requires the lock to cover the manifest's last-byte probe and append on the same open fd. Could inform operator-facing wedge docs only. |
| tameshi | `tools/trace-inputs.py` (WRITE_FLAGS_RE, `O_APPEND`) | Classifies write-mode opens (incl. `O_APPEND`) in strace traces; drops write-opened paths from read buckets. | Verification harness only, not an implementation. Useful to confirm a candidate gate opens the manifest with append semantics, but does not serialize writers. |
| kama | `tools/sources-append-only.py` | Audits append-only `SOURCES.md` registry rows between revisions (immutable cells). | Conceptual overlap (append-only discipline) but no concurrency/locking. Could reuse invariant style, not the mechanism. |
| (all other lanes) | — | No `fcntl`/`LOCK_EX` usage in any sibling `tools/` (grep `*/tools` for `LOCK_EX`/`fcntl.` returned none). | No duplicate implementation of C1 found. |

## (b) Auditing declared-unavailable / exempt citations/links

| Lane | Path:line | What it does | Overlap with C2 |
|---|---|---|---|
| kotodama | `tools/check-source-access.py` (whole file; BYPASS regex + `flagged()`) | Audits `corpus/SOURCES.md` rows whose source/anchor/teaches contains access-bypass markers; requires such rows to have status `rejected` and forbids citation of their S-id in `corpus/knowledge`. | Closest conceptual analogue: it enforces truthfulness of a declared-unavailable/unusable source. Domain differs (access bypass vs citation-chain exempt statuses). Could reuse the audit shape (flagged set → status check + citation scan), but not the predicate. |
| kotodama | `tools/gates/provenance-audit.py` | Checks corpus entry provenance headers (`topic`/`sources`/`couples`) and calibration vocabulary. | Adjacent provenance audit, not exempt-citation audit. No duplicate. |
| kotodama | `tools/source-audit-inventory.py` | Counts `to-verify` markers; explicitly non-adjudicating inventory. | Not C2; could reuse marker-counting style only. |
| kama | `tools/citation-provenance.py` (`git_blob`, `check`) | Verifies revision-qualified `cite(rev,path,sha256=...)` tokens against git blobs. | Provides reusable git-blob verification primitive for "would verify if resolved" checks, but does not handle exempt/unavailable statuses. |
| kama | `tools/report-landing-audit.py` | Audits round reports for unresolvable/omitted commit citations. | Commit-citation audit, not chain-hop exemption. |
| tsukuroi | `tools/check-section-citations.py` | Validates section-citation errata bindings against pinned headings/rows/quotes. | Citation-locator audit, not declared-unavailability. |
| mori | `tools/mori-evidence-loss.py` | Verifies retained evidence copies against recorded SHA-256 and named git commits. | Evidence-retention audit; could reuse commit/blob comparison, not exemption logic. |
| (all other lanes) | — | No use of `CHAIN_EXEMPT`, `blocked-no-fetch`, or `labelled-dead` outside chousa (`grep */tools` returned only chousa). | No duplicate of C2 found. |

## Non-obvious move
A compatible synthesis: reuse kama's `git_blob`/revision verification primitive and kotodama's two-leg audit shape (status requirement + citation scan) as the *read-only* basis for C2's "would verify if resolved" test, while keeping C1's lock strictly on the manifest fd (not kagi's separate lock file). This improves coverage (C2) by grounding the resolvable check in an existing, tested git-blob lookup, and improves operability (C1) by avoiding a lock-file indirection that the C1 counter's cooperating-lock hold check would reject. Risk: kama's lookup assumes a git lane and revision-qualified paths; C2's sources include local paths and declared ids, so the primitive must be adapted to chousa's `claim_source_path`/`SRC_PTR` resolution, and must not add network reads (URL sources stay unread). Verification: C1 counter 24/24 under `--gate` with manifest fd locked; C2 counter 120/120 with only U-hop resolvable findings; no-harm selftest/verify-claims/verify-chain unchanged.

## Limits
- Scan was tool/corpus-knowledge scoped; full-text searches over `corpus/live` and `reports` were deliberately excluded as noise. Some sibling work may exist only in reports; not claimed absent there.
- No candidate implementation was built or scored; control rule honored.
source: S036 — tools/research-gate.sh verify_metadata registry checks; corpus/evidence/round26-claims.md Claim3 and its contract correction. S039 — W3C PROV-DM Recommendation2013-04-30, §5.2.1 Derivation (optional generation and usage details), https://www.w3.org/TR/2013/REC-prov-dm-20130430/#term-Derivation.
verified-at: 2026-10-21 — checked the registry-link spec and its planted missing-row, not-mined, used-by, bare-date and no-id controls; the final measured revision and findings are owned by SCORECARD.md Round26.
recheck: 90d — cwd=lane root; `bash tools/research-gate.sh verify-metadata corpus/knowledge/registry-link-r26.md --root . --registry corpus/SOURCES.md`; frozen controls: `bash corpus/evidence/round26-measure.sh "$PWD" c3`.

# A two-sided provenance link is still not source support

## What the screen establishes

QUALITY6 requires a new entry's `source:` S-id to exist in SOURCES.md, be
`mined`, and have a `used-by` token naming the entry; `verified-at:` also says
what was checked. `--registry` checks those **local declaration relations**.
It does not execute the entry's command or fetch a cited URL.

W3C PROV-DM permits explicit generation and usage details for entities in a
derivation (S039, §5.2.1). Treating this lane's source/used-by pair as a
two-sided provenance record is an analogy [INFERENCE], not a PROV-DM rule.
PROV-DM does not prescribe this registry, the mined status, or these findings.

## Disposition table

| finding | reading | action |
|---|---|---|
| META_SOURCE_ROW_MISSING | cited standalone S-id has no registry row | open the source and curate the real row, or correct an actual typo with an erratum |
| META_SOURCE_NOT_MINED | cited row is queued/rejected | do not flip status merely to pass; decide admission against scope and support, then log old→new |
| META_SOURCE_USEDBY_MISSING | mined row does not name this exact rooted repo-relative entry path | verify attribution, then log a truthful used-by change; same basename elsewhere is not identity |
| META_VERIFIED_AT_BARE | date says nothing about the check | state what was actually checked; do not invent a recheck |
| META_SOURCE_NO_ROW_ID (info) | no S-id to evaluate | legacy-compatible information, not retroactive rejection of pre-r24 entries |

The ids follow the owning SOURCES contract (`S`+three-or-more digits).
New entry decisions use the prospective r24+ population, not all historical
notes. A manual `--registry` run can expose older metadata, but it must not be
reported as retroactive failure of an admission bar that did not yet bind.

## Limits

A queued row, an absent backlink, and a false supporting source are different
problems. Correct metadata can still cite an irrelevant or false source.
This screen does not check source scope/tier, URL/path+anchor completeness,
source opening, support or truth; it is **not the whole criterion6 verifier**.
QUALITY7/8 and a reviewer still judge those. A `used-by` edit is bookkeeping,
not new knowledge; only an actual opened/supported entry can justify mining.

## Withdrawal of implementation admission — 2026-10-21 (append-only)

**The Round26 checker is not admitted.** The intended local relation above
is not reliably established by measured implementation
`0e9784bd52eca456b24d0bc40921480a47f91a2b`. Its five frozen positive entry
results and five negative controls reproduce, but concrete counterexamples
survive outside them (`evidence/round26-inherited-after.log`).

Reports under `.ufo/waves/round-26/falsify/` own the failures:
`FRegistryHeaderless.md` — stale header columns can accept an unnamed table
or misbind real columns, hiding or inventing findings;
`FRegistryIdBoundary.md` / `FRegistryAbsentRow.md` — occurrence rescanning
can invent standalone IDs from glued text;
`FRegistryRegistryDeny.md` — the advertised refusal guarantee fails on a
filesystem-path class inherited from the pointer-oriented helper.
`FNoTrade.md` / `FOverlap.md` also expose registry parsing/token-scan
resource amplification. The 8MiB snapshot cap bounds input bytes only,
not parser memory/time. The oracle itself differs on whitespace and some
table shapes (`FRegistryBareVerified.md`, `FRegistryHeaderless.md`).

No absence of these findings establishes correct metadata, source support,
or safety. This file is retained as a withdrawn implementation candidate
and falsifiable method proposal, not admitted expansion or a capability.
No control population or declared threshold was weakened to report green.

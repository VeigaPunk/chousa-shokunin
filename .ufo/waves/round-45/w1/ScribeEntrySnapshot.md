# ScribeEntrySnapshot — re-grounded evidence-snapshot-coverage-r40.md draft

Seat: `L1Chousa45.ScribeEntrySnapshot` (scribe, leaf). Item: draft the lane's
re-grounded `corpus/knowledge/evidence-snapshot-coverage-r40.md` from the
train.json capture, recounting the seven figures and fixing the arithmetic.

## Behavior

- Read (read-only): staged source
  `/home/vgpnk/Projects/shokuknow/merge/chousa/knowledge/corpus/knowledge/evidence-snapshot-coverage-r40.md`
  and `evidence-archive-field-policy-r41.md`; `corpus/evidence/round45/claims.md`
  (frozen); `corpus/SOURCES.md`; `CORPUS.md`; `c3-count.py`; wave spec.
- Recounted all seven figures from the on-disk capture
  `/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache/974299ae4b5f3bdb808b36a9.txt`
  (no fetch). Verified size and sha256.
- Drafted the entry (fenced block below). No production writes, no git/jj
  mutations, no network, no tools installed, no scratch dir created.

## Observed runs (verbatim decisive output; all read-only)

```
$ wc -c /home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache/974299ae4b5f3bdb808b36a9.txt
10184813 /home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache/974299ae4b5f3bdb808b36a9.txt
$ sha256sum /home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache/974299ae4b5f3bdb808b36a9.txt
ae5eda7c42ddf1695ef185a7ba1bc716928f5adf57103e4f78aae5f9afe00f9c  /home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache/974299ae4b5f3bdb808b36a9.txt
```

Recount (json.load of the capture; `ev` = answers carrying `cached_source_url`;
`cl` = records carrying `cached_original_claim_url`; empty = falsy, mirroring
`c3-count.py`'s `rederive`):

```
records: 3068
evidence_with_field (answers carrying cached_source_url): 6511
evidence_nonempty: 6510
evidence_empty: 1
claims_with_field (records carrying cached_original_claim_url): 2531
claims_nonempty: 1145
claims_empty: 1386
claims_empty breakdown: None = 1343 ; '' = 43
evidence nonempty rate: 0.999846 (99.98%)
claim nonempty rate:    0.452390 (45.24%)
rate ratio: 2.210
empty ratio claim/evidence: 1386 = 10^3.14
```

## Verdict

- All seven figures reproduce exactly from the capture: 3,068 records; 6,511
  with the field; 6,510 non-empty; 1 empty; 2,531 claim fields; 1,145
  non-empty; 1,386 empty. Size 10,184,813 bytes; sha256 matches claims.md.
  No figure differs — draft proceeds.
- The "two orders of magnitude" sentence was arithmetically false: the two
  *rates* differ by factor 2.210 (99.98% vs 45.24%), not orders. The pair
  that differs by orders is the empty counts: 1,386 ÷ 1 = 1,386 ≈ 10^3.14,
  i.e. *more than three orders of magnitude*. Draft states exactly that.
- The claim-level "empty" count = 1,343 null + 43 empty strings (the counter's
  `claims_empty` counts falsy values); noted in the draft for auditability.
- Staged entry's S132 id, amendment claim to
  `evidence-pool-versioning-r39-amendment-2026-10-23.md` (not held by the
  lane), and the two-orders sentence all removed; Unknown resolved by pointing
  to `corpus/knowledge/evidence-archive-field-policy-r41.md` (claim-level:
  empty = none taken, best-effort per README; evidence-level: comprehensive
  caching per paper, so the single empty field is anomalous; per-record cause
  stays unrecorded).

## The drafted entry (verbatim, fenced)

```
# How much of the corpus is actually bound to a snapshot

source: S084 — https://raw.githubusercontent.com/MichSchli/AVeriTeC/main/data/train.json — the `answers` items' `cached_source_url` field and the records' `cached_original_claim_url` field — 3,068 records, 10,184,813 bytes, read 2026-10-25
verified-at: 2026-10-25
recheck: 365d — re-download the file and re-count the empty `cached_source_url` and `cached_original_claim_url` fields (ran 2026-10-25)
ground: Q17 — how large is the share of AVeriTeC citations with no archived capture; what an empty archive field means is read from corpus/knowledge/evidence-archive-field-policy-r41.md

#### Observation

- **The per-citation binding is effectively universal.** Of the 6,511 evidence
  entries in the file that carry `cached_source_url`, **6,510 hold a non-empty
  archive.org URL and 1 is empty**.
- **The claim-level binding is not.** Of the 3,068 records, 2,531 carry a
  `cached_original_claim_url` field, and of those **1,145 are non-empty and
  1,386 are empty** (1,343 null and 43 empty strings) — the claim's own
  original URL is archived for well under half of the records that have the
  field at all.

#### Inference

- **The answer to Q17 is "it depends which binding you mean", and the two
  bindings differ in their empty-field counts by more than three orders of
  magnitude: 1 empty evidence-level archive field versus 1,386 empty
  claim-level fields (1,386 ÷ 1 = 1,386 ≈ 10^3.14).** The instrument that
  matters for verifying a *claim against its evidence* — the archived copy of
  each cited source — is present almost always (6,510 of 6,511, 99.98%). The
  instrument that binds the *claim itself* to the page it first appeared on is
  present for under half (1,145 of 2,531, 45.2%). A lane that assumes "the
  corpus snapshots everything" would be wrong about the claim's own
  provenance, and a lane that assumes "the corpus snapshots nothing" would be
  wrong about its evidence.
- **This is the shape the lane's own pin already has, now measured.** The
  lane's r31 `sha256` fixes one file's bytes; AVeriTeC fixes each *cited
  URL*'s state at build time. The measurement shows that the per-citation
  binding is what corpus builders actually achieve, and that the claim-level
  binding is the hard part — which is where a lane's attention should go if
  it wants to catch a claim that was altered after publication.
- **The single empty evidence entry is worth more than the 6,510 that are
  filled.** It is the case a corpus can get wrong in a way that is invisible
  to any count of the filled ones, and it is the case the lane's own
  "location binding" gap would miss.

#### Unknown

- **The counts are for the training split only.** The development and test
  splits were not opened, and the released data may not be the same data the
  corpus paper describes.
- **Whether an empty `cached_source_url` means "no archive exists" or "no
  archive was taken" is resolved by `corpus/knowledge/evidence-archive-field-policy-r41.md`**:
  at the claim level, the README documents `cached_original_claim_url` as
  best-effort ("Where possible, an archive.org link to the original claim
  url"), so an empty value records that no archive was taken, not that no
  archive exists; at the evidence level, the paper states the corpus caches
  all pages used as evidence, so the single empty evidence-level field is an
  anomaly relative to documented behavior. Why that particular capture was
  skipped is not recorded in the corpus.
- The figures are a count of fields, not a measure of whether the archived
  capture *matches* what the annotator read; that would need a comparison
  against the archive itself.

---
```

## Gates / touched surfaces

- Only file written: this report. No lane production file was modified; the
  draft above is delivered for the milestone's edit.
- No scratch dir under /tmp was created; nothing to delete.

## Findings

- The staged entry's counts are fully reproducible from the capture on disk
  (sha256 matches claims.md's construction check), so the re-grounding needs
  no fetch.
- The staged entry's `source:` carried S132, but the freeze binds train.json
  to S084 (`c3-count.py` `BINDINGS`), and SOURCES.md has no S132 row; the
  draft uses S084 only, per the freeze.
- The claim-level empty count conflates null and empty-string values (1,343 +
  43); the counter defines empty as falsy, so both count — stated in draft.
- `counts.json` does not yet exist in `corpus/evidence/round45/` (the
  counter expects it; creating it is out of this seat's scope).

## Out of scope

- Creating `counts.json`, `spans.tsv`, SOURCES rows S082-S084, or landing the
  entry file — milestone edits, not scribe writes.

## Artifacts

- This report: `.ufo/waves/round-45/w1/ScribeEntrySnapshot.md` (lane-relative).
- Source of truth read: staged `evidence-snapshot-coverage-r40.md` (merge/chousa)
  and field-policy entry; capture `974299ae4b5f3bdb808b36a9.txt`.

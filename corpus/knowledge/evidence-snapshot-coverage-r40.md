# How much of a verification corpus is actually bound to a snapshot

source: S084 — https://raw.githubusercontent.com/MichSchli/AVeriTeC/main/data/train.json — the answers' `cached_source_url` field and the records' `cached_original_claim_url` field — 3,068 records, 10,184,813 bytes, capture sha256 `ae5eda7c42ddf1695ef185a7ba1bc716928f5adf57103e4f78aae5f9afe00f9c`
verified-at: 2026-10-25
recheck: 365d
ground: a corpus that documents an archive link per citation — how many of its stored values are in fact archive links, and how many claims carry one? Counted from an on-disk capture; the counts and the capture digest are committed in `corpus/evidence/round45/counts.json`. The filename is the package's label, not a lane round number.

#### Observation

- The file holds 3,068 records (S084).
- Of the evidence answers, 6,511 carry the key `cached_source_url`: 6,510 hold a non-empty value and 1 is empty (S084).
- The key is absent from 1,968 of the 8,479 answers, and only 386 of those are unanswerable: 1,582 answers name a `source_url` and carry no archive field at all, 1,491 of them a real source rather than `Metadata` (S084, recounted by the lane in round 45).
- The non-empty values are not all archive links: 5,959 are web.archive.org URLs (counted as values that begin `http(s)://web.archive.org/`; one malformed value that repeats a truncated prefix before the archive URL is not counted) and 551 are not. Of those 551, 429 are the literal placeholder `Metadata` (answers whose source is metadata, not a page); the rest are other archivers (archive.ph 41, perma.cc 27, archive.vn 6) and a tail of live or malformed addresses (S084, recounted by the lane in round 45).
- 8 of the web.archive.org values wrap an archive.is or archive.md address — the double-archived form the corpus's own guideline says returns a 404 at archive.org (S084; `corpus/knowledge/evidence-archive-field-policy-r41.md`).
- The single empty answer (record index 1175, a boolean answer) has an empty `source_url` too: there was no source URL to archive (S084).
- Of the 3,068 records, 2,531 carry `cached_original_claim_url`: 1,145 non-empty and 1,386 empty (S084).

#### Inference

- Counted over the field, the evidence-level binding looks near-universal (6,510 of 6,511 filled, 99.98%); the claim-level binding is present for 1,145 of 2,531 records (45.2%), so the filled rates differ by a factor of about 2 and the empty counts by more than three orders of magnitude (1,386 against 1). Lane arithmetic.
- Counted over the citations, it is not near-universal. Of the 7,572 answers that name a real source (a `source_url` other than `Metadata`), 5,959 (78.7%) carry a web.archive.org link, the target the README names; the rest carry no archive field, a placeholder or another archiver. Lane arithmetic over S084.
- The one empty evidence field is not an archiving gap: it belongs to an answer with no source URL. A reader who counts empty archive fields to find missing snapshots finds the wrong case; the missing snapshots sit in answers that lack the field and among filled values that are not archive links.
- For claim-vs-source verification, the per-citation archive is the instrument to check against, and it must be checked by value, not by presence: a filled field may be a placeholder, another archiver, or a link the corpus itself says returns a 404. Lane inference.

#### Unknown

- The counts are for the training split only; the development and test splits were not opened.
- Whether each web.archive.org value resolves, and whether it holds the state the annotator read, was not checked (no fetch this round).
- Why a claim's archive is missing is not recorded per record; see `corpus/knowledge/evidence-archive-field-policy-r41.md` for what the documentation does and does not say.

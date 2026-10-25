# CritRejectDecision — round 45 wave 2 (falsify)

Seat: L1Chousa45.CritRejectDecision. Item attacked: the round's one reject — the staged
`evidence-pool-versioning-r39-amendment-2026-10-23.md` (staged S127, S128), refused in
`corpus/lessons/round-45.md` `## Gate` and in the SOURCES.md screening note.

## Verdict

**reject over-cautious** — with one caveat noted below. The two stated grounds are
factually true but are framing/editorial defects that the round's own admission standard
(re-grounded, not copied) already repaired in the two *admitted* entries; every quote is
located in the on-disk captures; a same-theme third entry was practicable.

## 1. The reject's stated reasons — verified true

- "It amends a base entry the lane does not hold": TRUE. `glob
  chousa-shokunin/corpus/knowledge/evidence-pool-versioning-r39*` → no files; grep
  `evidence-pool|pool-versioning` over the lane corpus → only the round-45 README/SOURCES
  notes about this reject. The base exists only in the staged package
  (`merge/chousa/knowledge/corpus/knowledge/evidence-pool-versioning-r39.md`, MERGE-REPORT.md
  line 33, round-4 new-file).
- "Its prose ids point at other documents in lane numbering": TRUE. Lane SOURCES.md rows:
  S071 = GNU coreutils `env(1)` manual; S079 = RFC 7089 Memento; S081 = NDL E2867; S082 =
  AVeriTeC README (this round); no S095 exists. The amendment's `S071` (RFC 7089),
  `S082` (NDL timestamp-in-URL) and `S095` (pin note) are wrong in lane numbering and also
  in the staged append's (staged S084 = RFC 7089, S095 = NDL E2867, no S071 row). The
  references are rhetorical prose analogies; each names its document in words, so a
  re-binding (S071→S079, S082→S081, drop S095) is unambiguous.

## 2. Quote location — all located, no fetch

Cache names = sha256(url)[:24] + ".txt" (verified by computing the hashes):

- `https://fever.ai/dataset/averitec.html` → `b73f7e8dd5b0ace740e48046.txt` (12,775 B,
  sha256 `603f9b42ccbafcb8885679e905b2aed5946fb211c29bba0423e27558cc87528b`) — PRESENT.
  - "An archive.org link for the source url" — line 249 (`cached_source_url` field).
  - "Where possible, an archive.org link to the original claim url" — line 225
    (`cached_original_claim_url` field).
  - "Our best estimate for the date the claim first appeared" — line 219 (`claim_date`).
  - Four-labels sentence — lines 142–143, verbatim: `...four labels: "Supported",
    "Refuted", "Not Enough Evidence", "Conflicting Evidence/Cherry-picking".` The amendment
    inserts "and" before the last label — one-word deviation, substance identical.
  - Hunter_Biden worked example — lines 290–293.
- `https://arxiv.org/html/2505.17978v2` → `78761b633aee2289e5874ce9.txt` (126,093 B,
  sha256 `35bdf1c1cbc337d4c93ce7c8f2ed51635894903ed1cf4c15d6d6acc9ecc7480c`) — PRESENT.
  - Mitigation sentence ("contextual dependence, temporal leakage, and evidence
    insufficiency, via claim normalization, temporally constrained evidence annotation, and
    a two-stage sufficiency check") — line 222, Abstract.
  - "…using only online evidence published before the claim's date" — line 272
    (the amendment's ellipsized "limited … to those published before the claim's date"
    matches meaning).
  - κ=0.742 and 74.7% on QA pairs — line 222, **Abstract** (also 275/277, 757/761).

## 3. The one substantive defect in the quotes — S128 anchor

The staged row S128 (and the amendment header) anchor to "Appendix H.1 Details of
Experiments". The paper's ToC (lines 150–154 and 4369–4432): `H Details of Experiments / H.1
Model Implementation / H.2 Experiment Environment and Packages`. H.1 is Model Implementation;
the quoted figures are from the Abstract. Anchor error confirmed — but it is a locator
correctable to "Abstract".

## 4. Why the rejection was over-cautious

- The lesson's own Gate admits both entries after re-grounding ("Re-grounded, not copied:
  the staged inference … was narrowed"; "the staged '6,510 hold a non-empty archive.org
  URL' and 'two orders of magnitude' were wrong and are replaced by the recount"). The
  amendment's defects (orphan framing, id re-binding, verbatim wording, anchor) are the
  same class — all fixable against the same on-disk captures, no fetch needed.
- The SOURCES.md screening note itself counts it: "Identified 3 candidate entries on the
  AVeriTeC archive-field theme, screened 3, included 2, excluded 1." The item was a
  same-theme candidate; the S127 (dataset page) quotes sit exactly on the theme ("what an
  AVeriTeC archive field documents") and are located — the same precondition the round's C3
  applied to its four adopted quotes.
- Refusing the whole entry rather than re-grounding it was stricter than the round's own
  demonstrated bar.

## 5. Caveats that keep this short of "reject wrong"

- The S128 (AVerImaTeC) quotes are **off-theme**: they document temporal constraints and
  annotation consistency, not archive fields. A "third entry on the same theme" is carried
  by the S127 half; the S128 leg would need re-scoping or exclusion.
- The frozen C3 counts exactly two entries / three rows (ENTRIES=2/2, S082–S084); a third
  entry is not scored by any frozen counter and would grow the census (a construction check,
  not a predicate) — so the flip (adopt base + amendment together, or land S127 as a fresh
  standalone entry with verbatim quotes, id re-binding and corrected anchor) is the needed
  shape, not adoption as-staged.

## 6. Smallest safe correction (reported, not applied)

Land `evidence-pool-versioning-r39-amendment-2026-10-23.md`'s S127 content as a fresh,
document-bound entry (or adopt base+amendment together): quote the four-label sentence
verbatim (drop the inserted "and"); re-bind prose ids to lane S079/S081 and drop the ghost
S095; correct the S128 anchor to the Abstract (H = "Details of Experiments", H.1 = Model
Implementation) and either re-scope S128 to the theme or drop it; keep all six+ located
spans with their capture sha256s (`603f9b42…`, `35bdf1c1…`).

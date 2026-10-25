# CritRejectPoolAmendment — round 45 wave 1

Seat: L1Chousa45.CritRejectPoolAmendment. Verdict: **REFUSE** the staged
`evidence-pool-versioning-r39-amendment-2026-10-23.md` as an adoption candidate this
round. Evidence and reasoning below.

## Item

Staged entry `/home/vgpnk/Projects/shokuknow/merge/chousa/knowledge/corpus/knowledge/evidence-pool-versioning-r39-amendment-2026-10-23.md`
(sha256 `0486b1aa5624548b85a7144562eaabd3f5d16bac1e8b9ed8e8828fd704ff2dab`).

## Check 1 — base entry not held by the lane: CONFIRMED

Lane corpus `/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/knowledge/` (glob,
58 files) contains **no** `evidence-pool-versioning-r39.md` and no `evidence-pool-*`
file at all. The base exists only in the staged package
(`merge/chousa/knowledge/corpus/knowledge/evidence-pool-versioning-r39.md`, round 4 new-file
per MERGE-REPORT.md line 33). The amendment declares itself (line 8) "a dated amendment
to wave 4's `corpus/knowledge/evidence-pool-versioning-r39.md`; it adds to that entry and
does not replace it." Landing it alone would create an orphan row whose base never landed.

Cascade: `evidence-snapshot-coverage-r40.md` (an official C3 adoption target, staged id
S132 → lane S084) likewise declares itself an amendment of this amendment, so refusing this
entry also breaks that chain unless handled together.

## Check 2 — prose id mapping: S071/S082/S095 point at wrong/non-existent documents

Lane registry (`chousa-shokunin/corpus/SOURCES.md`): registry rows end at **S081**;
grep `^\| S(08[2-9]|09[0-9]|1[0-9][0-9]) \|` → no matches (no S082–S199). Lane S071 row
= GNU coreutils `env(1)` manual (env -u/--unset).
Staged append (`merge/chousa/SOURCES.append.md`): no S071 row; S082 = PRISMA-S (doi
10.1186/s13643-020-01542-z); S095 = NDL WARP E2867 (`current.ndl.go.jp/e2867`);
S127 = AVeriTeC Dataset page (`fever.ai/dataset/averitec.html`); S128 = AVerImaTeC
(`arxiv.org/html/2505.17978v2`).

| prose id | amendment uses it as | lane id holds | staged id holds | verdict |
|---|---|---|---|---|
| S071 | RFC 7089 Memento | GNU coreutils env(1) manual (S071) | none | WRONG (correct lane id: S079) |
| S082 | NDL timestamp-in-URL scheme | none (S082 absent) | PRISMA-S paper | WRONG (correct lane id: S081) |
| S095 | lane's own pin note (bytes, not time) | none (S095 absent) | NDL E2867 paper | WRONG in both numberings |
| S127 | fever.ai/dataset/averitec.html | none (S127 absent) | AVeriTeC Dataset page | correct by document in staged numbering |
| S128 | arxiv.org/html/2505.17978v2 | none (S128 absent) | AVerImaTeC paper | correct by document in staged numbering |

## Check 3 — quotes present in on-disk captures: CONFIRMED (with defects)

Cache names = sha256(url)[:24]+".txt"; both exist, no fetch performed.

- `https://fever.ai/dataset/averitec.html` → `b73f7e8dd5b0ace740e48046.txt`, present,
  12,775 bytes, sha256 `603f9b42ccbafcb8885679e905b2aed5946fb211c29bba0423e27558cc87528b`
- `https://arxiv.org/html/2505.17978v2` → `78761b633aee2289e5874ce9.txt`, present,
  126,093 bytes, sha256 `35bdf1c1cbc337d4c93ce7c8f2ed51635894903ed1cf4c15d6d6acc9ecc7480c`

Offsets below are in whitespace-normalized, tag-stripped text. All quotes FOUND:

FEVER capture:
1. "An archive.org link for the source url" — ws 3526 (`cached_source_url : An archive.org
   link for the source url`).
2. "Where possible, an archive.org link to the original claim url" — ws 2790.
3. "Our best estimate for the date the claim first appeared" — ws 2546.
4. Four-labels sentence — ws 829, contiguous: `The Claims in AVeriTeC are classified into
   four labels: "Supported", "Refuted", "Not Enough Evidence", "Conflicting
   Evidence/Cherry-picking".` — **deviation**: the amendment inserts "and" before the last
   label; the capture has commas throughout (one-word verbatim difference; substance
   identical).
5. Wikipedia archive example `web.archive.org/web/20230323135844/https://en.wikipedia.org/wiki/Hunter_Biden`
   — ws 4838 and 5350 (worked-example JSON).

arXiv capture:
6. Abstract mitigation sentence, contiguous: "We mitigate common challenges in fact-checking
   datasets such as contextual dependence, temporal leakage, and evidence insufficiency, via
   claim normalization, temporally constrained evidence annotation, and a two-stage
   sufficiency check." — ws 2481.
7. "…only online evidence published before the claim's date" — ws 6708 (amendment's
   ellipsized "limited … to those published before the claim's date" matches meaning).
8. κ=0.742 and 74.7% on QA pairs — ws 2821/2856, in the **Abstract**.
9. **Anchor defect**: the S128 row says "Appendix H.1 Details of Experiments"; the paper's
   ToC shows `H Details of Experiments / H.1 Model Implementation / H.2 Experiment
   Environment and Packages` (ws 1141–1164). H.1 is Model Implementation, not "Details of
   Experiments", and the quoted figures come from the Abstract, not H.1.

## Commands run (decisive output)

- `glob` lane `corpus/knowledge/**` → 58 files, no `evidence-pool-*`.
- `grep '^\| S(08[2-9]|09[0-9]|1[0-9][0-9]) \|' chousa-shokunin/corpus/SOURCES.md` →
  "No matches found".
- `grep '^\| S071 \|' merge/chousa/SOURCES.append.md` → "No matches found".
- sha256 of URL strings → `b73f7e8dd5b0ace740e48046.txt`, `78761b633aee2289e5874ce9.txt`;
  both exist (sizes 12,775 and 126,093).
- Python quote search over both captures (raw, whitespace-normalized, tag-stripped): results
  above. No scratch files created; no tools installed (no pacman/uv/cargo; not needed).

## Reject reason

The entry is a dated amendment to `evidence-pool-versioning-r39.md`, which the lane's corpus
does not hold (staged only), so landing it now creates an orphan row whose base never landed;
its prose refs S071/S082/S095 point at wrong or non-existent documents in lane numbering
(lane S071 is the coreutils env(1) man page; the correct Memento lane id is S079, NDL E2867
is S081, and no S082/S095 rows exist), even though S127/S128 map correctly by document in
the staged append and every quote is present in the on-disk captures.

## Flip condition

Adopt the base `evidence-pool-versioning-r39.md` and this amendment together as fresh
document-bound lane rows (S127 → `fever.ai/dataset/averitec.html`, S128 →
`arxiv.org/html/2505.17978v2`), rewrite the cross-references to lane ids S079/S081 (dropping
the phantom S082/S095), fix the S128 anchor to the Abstract (naming H as "Details of
Experiments", H.1 = Model Implementation), and restore the capture's comma-separated
four-label wording (or quote it verbatim).

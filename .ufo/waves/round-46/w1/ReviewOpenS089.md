# ReviewOpenS089 — lane source S089 opened, its three quotes located

Item given: open S089 (AVerImaTeC arXiv HTML) this round and locate the quotes that
ground its Registry row; report capture digest/length, per-quote char offset,
occurrence count, 120-char flanks, a ≤25-word verbatim anchor, the section each
sits in, and which staged sentences the source supports / contradicts.
No fetch. Read-only on `/home/vgpnk/Projects/shokuknow`.

## Capture identity

```
path   /home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache/78761b633aee2289e5874ce9.txt
sha256 35bdf1c1cbc337d4c93ce7c8f2ed51635894903ed1cf4c15d6d6acc9ecc7480c
bytes  126093    chars (UTF-8) 125537    lines 4690
url    https://arxiv.org/html/2505.17978v2   (sha256(url)[:24] = 78761b633aee2289e5874ce9)
```
Note: the page spells the dataset **AVerImaTeC** (bytes 7–17: `41 56 65 72 49 6d 61 54 65 43`,
capital `I` 0x49). A literal search for `AVeriMaTeC` (lowercase i) returns **0** hits in this capture.

Section map used below (char offsets, from `\n N Title\n` headings and the appendix list):
Abstract ≤3463 · §1 Introduction 3463 · §2 8697 · §3 13073 · §4 16439 · §5 Dataset Statistics 20834 ·
§6 24762 · §7 28121 · Appendix E Inter-Annotator Agreement 100271 · Appendix H 111899 (H.1 Model Implementation 111912).

## Q1 — `temporally constrained evidence annotation`

- offset **3022** · occurrences **1** · section **Abstract** (3062 < §1 at 3463) · verdict **located**
- left 120: `checking datasets such as contextual dependence, temporal leakage, and evidence insufficiency, via claim normalization, `
- right 120: `, and a two-stage sufficiency check. We assess the consistency of the annotation in AVerImaTeC via inter-annotator studi`
- anchor (11 words, n=1, off 3001): `claim normalization, temporally constrained evidence annotation, and a two-stage sufficiency check`

## Q2 — sentence about evidence `published before the claim’s date`

- offset **7137** · occurrences **1** (the phrase `before the claim` also n=1, at 7147) · section **§1 Introduction** · verdict **located**
- exact bytes of the apostrophe: **U+2019 = `e2 80 99`**; the 33-char quote is 35 bytes.
- verbatim sentence: `annotators convert the verification rationale from the articles into QA pairs, while being restricted to using only online evidence published before the claim’s date.`
- left 120: `onvert the verification rationale from the articles into QA pairs, while being restricted to using only online evidence `
- right 120: `.⏎Given the multimodal nature of the task, both questions and answers may involve images. Finally, we conduct two rounds`
- anchor (11 words, n=1, off 7096): `restricted to using only online evidence published before the claim’s date`

## Q3 — reported kappa / QA-pair consistency figures

- Abstract locus: offset **3200** (`κ = 0.742 …`; `0.742` at 3204, `74.7` at 3239) · section **Abstract** · verdict **located**
- left 120: `e sufficiency check. We assess the consistency of the annotation in AVerImaTeC via inter-annotator studies, achieving a `
- right 120: `.⏎We also propose a novel evaluation method for evidence retrieval and conduct extensive experiments to establish baseli`
- anchor (9 words, n=1, off 3200): `κ = 0.742 \kappa=0.742 on verdicts and 74.7 %`
- Further loci in the same capture: §5 Dataset Statistics, `Inter-Annotator Agreement.` at 23370 —
  `Randolph’s … free-marginal multi-rater κ` then `We obtained an agreement score of κ = 0.742 \kappa=\mathbf{0.742}` (0.742 at 23992),
  `AVeriTec … reported agreement of 0.619` (24100), `Using Fleiss’ κ \kappa , a more traditional metric, our annotation process
  achieves an agreement score of 0.450` (24114; 0.450 at 24220), `The recall rate is 74.7 % \mathbf{74.7\%} and the precision is
  67.2 % \mathbf{67.2\%}` (24577; 67.2 at 24640). Appendix E restates `We achieved an agreement score of 0.742` (101282).
- occurrence counts: `0.742` 7× (3204 3217 7641 7647 23992 24013 101282) · `74.7` 6× (3239 3246 7711 7718 24596 24611)
  · `0.450` 2× · `0.619` 2× · `67.2` 2×. The capture duplicates every figure in LaTeX (`\kappa=0.742`), so a span must
  reproduce the duplication verbatim.
- anchor for the §5 metric-dependence sentence (10 words, n=1, off 23954): `We obtained an agreement score of κ = 0.742 \kappa=\mathbf{0.742}`

## Verdicts

| quote | offset | n | section | verdict |
|---|---|---|---|---|
| `temporally constrained evidence annotation` | 3022 | 1 | Abstract | located |
| `published before the claim’s date` | 7137 | 1 | §1 Introduction | located |
| `κ = 0.742 … / 74.7 % consistency on QA pairs` | 3200 | 1 | Abstract (also §5 23988, App. E 101282) | located |

## Staged sentences S089 actually supports

1. Amendment Observation: "They mitigate 'contextual dependence, temporal leakage, and evidence
   insufficiency, via claim normalization, temporally constrained evidence annotation, and a
   two-stage sufficiency check'" — **supported verbatim**, Abstract 3001–3073. S089 supports
   *three* named failure modes, not two.
2. Amendment Observation: "Annotation consistency is reported as κ=0.742 on verdicts and 74.7 % on
   QA pairs" — **supported as the Abstract's own wording** (3200–3260), and **materially incomplete**:
   §5 reports the same verdict labels at `Fleiss’ κ … 0.450` and pairs `74.7 %` recall with
   `67.2 %` precision. The staged sentence names no metric (Randolph free-marginal) and no second figure.
3. Amendment `recheck`: the phrase "temporally constrained evidence annotation" is unchanged — **supported** (n=1, 3022).
4. Amendment Inference, "the constraint is operational" — **supported in substance**: Appendix H.1 at
   113866, `limiting all returned web pages published before claim dates` (and §1 at 7096, `restricted to …`).

Not supported by this source at all: every S088-scoped sentence (`cached_source_url`,
`cached_original_claim_url`, `claim_date`, the fourth label). This capture has **0** occurrences of
`cached`, `snapshot`, `wayback`, `revision`, `dump`; its single `archive.org` hit (14603–14661) is a
footnote saying "all source pages are archived on the internet archive", with no per-citation field.

## Contradictions (staged vs capture)

**X1 — fabricated quotation (HIGH).** Staged amendment: `web pages returned as evidence
"limited ... to those published before the claim's date"`. The capture has no such wording. §1 says
`being restricted to using only online evidence published before the claim’s date`; Appendix H.1 says
`limiting all returned web pages published before claim dates`. The token `limited` occurs 3× and
never in this construction: 2491 (`remain limited, as they often consist of synthetic claims`),
41808 (`AVerImaTeC has a relatively limited scale`), 74547 (NeurIPS checklist, `access to the model is
limited in some way`). The lane copy already dropped it (`grep 'limited'` on
`corpus/knowledge/evidence-pool-versioning-r39-amendment-2026-10-23.md` → `[]`); the merge package still carries it.

**X2 — row scope miscounts the source (HIGH, lands in the Registry).** Staged Registry row S128, col 5:
"the corpus authors' own account of **the two failure modes** a verdict must survive — temporal leakage
and evidence insufficiency". Capture Abstract: "contextual dependence, temporal leakage, and evidence
insufficiency" — three, with contextual dependence first. `c3-count.py` reads only url/status/used-by
from the row, so the counter cannot catch this; it is copied verbatim into `corpus/SOURCES.md`.

**X3 — source line over-narrows the sections (MEDIUM).** Staged `source:` line: "the Abstract, and
Appendix H.1 Details of Experiments". Q1 and Q3 are Abstract; Q2 (7137) is **§1 Introduction**, outside
both named sections. The lane entry's own line is already correct (names chars 3022, 3204, 3239, 7137,
no section claim), so the merge package's line must not be copied back.

**X4 — document name (LOW).** Staged row names "AVeriMaTeC"; the capture's own title is "AVerImaTeC"
(capital I, 0x49). One-character bibliographic mismatch in the row's title cell.

## Manifest / counter state (observed, read-only)

```
python3 corpus/evidence/round46/c3-count.py        → QUOTE_ROWS=11/11 QUOTES_IN_SPAN=11/11
  QUOTES_IN_ENTRY=11/11 CAPTURE_BOUND=11/11 REF_ID_UNBOUND=0 REF_BOUND=2/2
  CITES_BOUND=0/5 C3=FAIL (exit 1)
python3 corpus/evidence/round46/c3-count.py --lane-only → same, CAPTURE_BOUND=skipped, C3=FAIL (exit 1)
```
- Both committed S089 spans are exact slices: `spans/S089-1.txt` (42 chars, `ct[3022:3064]` ✓) and
  `spans/S089-2.txt` (33 chars / 35 bytes with `e2 80 99`, `ct[7137:7170]` ✓).
- `CITES_BOUND=0/5` because `corpus/SOURCES.md` still has no `| S085 |`…`| S089 |` rows (`grep -n '^| S08[5-9]'` → no match).
- The manifest is at exactly 11 rows (2 + 3 + 2 + 2 + 2). The κ/QA-pair quote **cannot** become a fourth
  S089 span without breaking the frozen `QUOTE_ROWS=11`; it belongs in entry prose with char pointers
  (3204, 3239, and optionally 23988 / 24220 / 24640).
- Live-tree caveat: an earlier run printed `REF_ID_UNBOUND=2`; the same command minutes later printed
  `0` with no change of mine. Siblings are editing the entries; every count above is a snapshot.

## Findings by severity

- **HIGH** X1 fabricated quotation ("limited …") — must not be re-imported from the merge package.
- **HIGH** X2 S128 row scope says two failure modes where the source names three — will ship as row truth.
- **MEDIUM** X3 source-line section list excludes §1 Introduction, where Q2 lives.
- **MEDIUM** Q3 staging reports only the favourable metric (0.742 / 74.7 %); the same capture's §5 gives
  Fleiss κ 0.450 and precision 67.2 %. Not a contradiction (the Abstract does say 0.742 / 74.7 %), but an
  entry about how durable a support verdict is should carry the metric dependence.
- **LOW** X4 title spelling `AVeriMaTeC` vs `AVerImaTeC`.
- **LOW** LaTeX duplication in every figure (`\kappa=0.742`), so future span text must keep it verbatim;
  the char offsets are stable only while sha `35bdf1c1…` is the capture.

## Commands run (verbatim, trimmed)

```
sha256sum …/.qcache/78761b633aee2289e5874ce9.txt
  35bdf1c1cbc337d4c93ce7c8f2ed51635894903ed1cf4c15d6d6acc9ecc7480c
wc -c / wc -m   126093 / 125537
python3 str.find / re.finditer over the UTF-8 decode (offsets above)
python3 slice check  ct[3022:3064] == spans/S089-1.txt True ; ct[7137:7170] == spans/S089-2.txt True
grep -n '^| S08[5-9]' corpus/SOURCES.md      (no match, exit 1)
python3 corpus/evidence/round46/c3-count.py [--lane-only]   (output above, exit 1)
```
No installs; no network; nothing written outside this report.

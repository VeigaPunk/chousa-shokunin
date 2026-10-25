# ScribeEntryBase — re-grounded base entry for the evidence-pool versioning theme

Item: draft the lane's re-grounded version of the staged
`evidence-pool-versioning-r39.md` (S085 FEVER dataset page, S086 ACL paper,
S087 Zenodo record) at `corpus/knowledge/evidence-pool-versioning-r39.md`,
every Inference bullet cited and grounded, every grounding token verbatim in
the capture, staged text corrected where the captures disagree, campaign
cross-references and S-ids outside S079–S089 removed.

Verdict: draft complete and verified; NOT landed (production write is the
executor's seat). `tools/inference-ground.py` on the draft: `section=1
bullets=6 tokens=12 grounded=12`, `GROUND: PASS`, exit 0. Strict audit under
the frozen rule (every backticked/quoted 2+ word phrase, every 3+ digit numeral
or percentage, each checked against the captures cited in its own bullet):
`TOTAL 12 BAD 0`. All 7 base-entry rows of the committed spans manifest are
carried verbatim by the draft.

## Commands and verbatim output (trimmed to decisive lines)

1. Capture sizes and digests (`wc -c`, `sha256sum`):
```
4146  e18eeb26a5a5902e10f0e0b25a9886d99bbbafcf8adfb85b7846bbd569d1ba92  5a631adb18988a1a2421ce75.txt
60153 c508913aba177ae4d33b29b7076f305bbac578a1ea11d39e30ddee2d787d563f  1c15b611118dee97e4105fcf.txt
5676  dfc3e0f50dc2fd7c896790a8ef30babb0992eb6d4c4b9a473c13c093277e00ed  7800e2e1e2df3bc124b6b83e.txt
```
2. `grep -c -i "revision" 5a631adb…txt` → `0`; same over `1c15b611…txt` → `0`
   (python scan). `grep -o -i exhaustive 1c15b611…` → `0` occurrences.
3. Contiguity probes (`grep -boF`, byte offsets; S086 has multi-byte chars so
   char = byte − Δ, Δ grows to 44 by mid-file):
```
S085 1271 Pre-processed Wikipedia Pages (June 2017 dump) | 2360 A list of evidence sets
S085 2394 [Annotation ID, Evidence ID, Wikipedia URL, sentence ID] | 2593 for internal use only and are not used for scoring
S085 757 185,445 claims | 1478 19,998 claims | 4047 refs/heads/live build 385 | 4073 Last updated: 2026-04-02
S086 15301 used the June 2017 Wikipedia dump, processed (char 15269) | 1869 0.6841 in Fleiss
S086 6755 95.42% precision and 72.36% recall | 42097 recall of 72.36% (char 42011)
S086 5547 31.75% of the claims | 5855 16.82% of cases | 5942 12.15% of the claims
S086 20905 91.2% (char 20861) | 20881 We found that 91.2% (char 20847) | 20972 of the examples were annotated correctly (char 20928)
S086 21854 except two annotators achieved > 90% precision | 21985 recall > 70% in evidence | 42202 by the super-annotators
S087 102 4925954 | 171 "conceptdoi": "10.5281/zenodo.4925953" | 294 Fact Extraction and VERification
S087 383 2018-04-03 | 468 185,445 claims | 4929 "key": "wiki-pages.zip"
```
   Byte→char corrections used in the entry: S086 15301→15269, 6755→6741,
   42097→42011, 5547→5534, 5855→5842, 5942→5929, 20905→20861.
   (`grep -boF` prints bytes; the entry records chars, matching the manifest.)
4. Non-contiguity that breaks the staged text (measured, not inferred):
   - `We used the June 2017 Wikipedia dump` → **not contiguous**. The capture
     reads `We` + 27 spaces (column padding) + `used the June 2017 Wikipedia
     dump, processed` (char 15269).
   - `91.2 % of the examples` → **not contiguous**. The capture reads
     `We found that 91.2%` (char 20847) with the percent sign attached, then a
     newline, then `of the examples were annotated correctly` (char 20928).
   - `all except two annotators achieved > 90 % precision … recall > 70 %` →
     **not one span**. The capture has `except two annotators achieved > 90%
     precision` (char 21810) and `recall > 70% in evidence` (char 21941) in
     different columns; there is no `90 %` or `70 %` with a space.
   - The staged Unknown's `exhaustive` phrase occurs **0** times in S086. The
     capture's own wording is `by the super-annotators` (char 42116), plural.
5. Tool run on the draft with a temporary 7-column spans manifest pointing at
   the three captures:
```
GROUND entry=draft.md section=1 bullets=6 tokens=12 grounded=12
GROUND: PASS                      EXIT=0
```
   (Run twice: first run FAILed on the `capture char N` numerals inside the
   Inference bullets — `NUM_RE` read `2360`, `6741`, … as tokens, and they are
   not in any capture. Fixed by moving all offsets into Observation, which
   `inference_ground.py` does not parse. That is the single design constraint
   a future entry must respect: **no prose offsets in Inference**.)
6. Manifest alignment (each of the 7 base-entry rows, `quote in draft`):
```
S085 off=2360   True  A list of evidence sets
S085 off=1271   True  Pre-processed Wikipedia Pages (June 2017 dump)
S086 off=15269  True  used the June 2017 Wikipedia dump, processed
S086 off=42011  True  recall of 72.36%
S086 off=20847  True  We found that 91.2%
S087 off=171    True  "conceptdoi": "10.5281/zenodo.4925953"
S087 off=4929   True  "key": "wiki-pages.zip"
```
7. `python3 corpus/evidence/round46/c3-count.py --lane-only` (read-only):
```
ENTRIES=2/2  CITES_BOUND=0/5  QUOTE_ROWS=11/11  QUOTES_IN_SPAN=11/11
QUOTES_IN_ENTRY=11/11  CAPTURE_BOUND=skipped  REF_ID_UNBOUND=0
REF_BOUND=2/2  C3=FAIL                                                       EXIT=1
```

## Findings for Main (routing, not acted on)

- **F1 (conflict).** `corpus/knowledge/evidence-pool-versioning-r39.md` was
  already written by another seat at 07:25 while this draft was in flight
  (mtime `Oct 25 07:25`, 5451 B). Its title differs and its `ground:` line
  reads "adopted from the shokuknow merge package (`merge/chousa`, staged
  `evidence-pool-versioning-r39.md`)": a **campaign cross-reference**, which
  this seat's instruction says to remove. My draft removes it.
- **F2.** The landed entry's Unknown keeps "annotator-produced exhaustive set"
  (line 27) though `exhaustive` occurs 0× in the S086 capture, and its
  header cites "the label-validation sentence (char 20847)" while the sentence
  it quotes is at 20847 — that one is right; the defect is the `exhaustive`
  wording plus the `"adopted from"` provenance line.
- **F3.** `CITES_BOUND=0/5` at 07:32 means the landed entries' `source:` lines
  do not yet bind the five ids to the five URLs in the form the counter wants
  (my draft writes one `source:` line per id, URL second, anchor third). Not
  my scope; flagging so the C3 verdict is not read as closeable on
  `ENTRIES=2/2` alone.
- No fetch, no network, no production write, no git/jj mutation. No tool
  installed. Scratch deleted.

## Draft (deliverable text, 38 lines)

```markdown
# What makes a support verdict durable, and how the FEVER release binds it

source: S085 — https://fever.ai/dataset/fever.html — the Data Format section evidence field (capture char 2360) and the Download Links list (capture char 1271); build refs/heads/live build 385, last updated 2026-04-02
source: S086 — https://aclanthology.org/N18-1074.pdf — section 3.1 on the dump (capture char 15269), the 3.4.2 figures (capture char 6741), the 3.4.3 validation (capture char 20637) and the super-annotator comparison (capture char 21810) — ACL Anthology PDF, read 2026-10-25
source: S087 — https://zenodo.org/api/records/4925954 — the record's doi, conceptdoi and files fields (capture char 146, 186, 4937) — Zenodo REST, publication_date 2018-04-03
verified-at: 2026-10-25
recheck: 365d
ground: what makes a support verdict durable, and how a later corpus binds each citation to an archived state. Read off three on-disk captures of the FEVER release — the dataset page, the ACL paper and the Zenodo record — with no fetch. It follows `corpus/knowledge/evidence-archive-field-policy-r41.md` in shape: what the field documents, not what it proves. The filename is the package's label, not a lane round number.

#### Observation

- The release states that "FEVER (Fact Extraction and VERification) consists of 185,445 claims" generated by altering Wikipedia sentences and verified without knowledge of the source sentence (S085, capture char 704, 757).
- The data format gives the evidence field as "A list of evidence sets (lists of [Annotation ID, Evidence ID, Wikipedia URL, sentence ID] tuples) or a [Annotation ID, Evidence ID, null, null] tuple if the label is NOT ENOUGH INFO", and adds that the two ids are "for internal use only and are not used for scoring" (S085, capture char 2360, 2593).
- The pool ships as a dated artefact: the download list names "Pre-processed Wikipedia Pages (June 2017 dump)" (S085, capture char 1271), the page carries "refs/heads/live build 385" and "Last updated: 2026-04-02" (S085, capture char 4047, 4073), and the replication files concatenate to the development set's "19,998 claims" (S085, capture char 1478).
- The paper records the dump, but not as the staged draft quoted it. In the two-column capture the subject "We" ends the left column and the right-column line reads "used the June 2017 Wikipedia dump, processed", so the contiguous slice begins at "used" (S086, capture char 15269). The staged "We used the June 2017 Wikipedia dump" is not one contiguous slice of this capture.
- The same shape recurs in the validation figures. The capture reads "We found that 91.2%" with the percent sign attached, and breaks the line before "of the examples were annotated correctly" (S086, capture char 20847, 20928); the staged "91.2 % of the examples" is not contiguous, because the percent sign carries no space and the phrase is split across a line.
- The paper's located figures: "0.6841 in Fleiss" kappa for claim-verification classification (S086, capture char 1869), "95.42% precision and 72.36% recall" in evidence retrieval (S086, capture char 6741), "31.75% of the claims" with more than one appropriate sentence, "16.82% of cases" needing composition, and "12.15% of the claims" drawing evidence from multiple pages (S086, capture char 5534, 5842, 5929).
- The authors' own check chose 227 examples and found 91.2% annotated correctly; against the super-annotators the capture reads "except two annotators achieved > 90% precision" and "recall > 70% in evidence" retrieval (S086, capture char 20637, 21810, 21941). The clauses sit in different columns, so the two slices are recorded separately rather than reconstructed into one sentence.
- The Zenodo record carries doi "10.5281/zenodo.4925954" beside `"conceptdoi": "10.5281/zenodo.4925953"`, with publication_date "2018-04-03" and title "Fact Extraction and VERification"; its files list holds `"key": "wiki-pages.zip"` beside train.jsonl and shared_task_dev.jsonl (S087, capture char 146, 171, 383, 294, 4929, 4710, 4464).
- RFC 7089, lane S079, binds a prior state with a response header rather than a hash: it says a Memento-Datetime "constitutes a promise that the resource state reflected in the response will no longer change" (S079, capture char 14896, committed capture d0c4a09a9de32cb91d5e3797.txt).
- The NDL Current Awareness E2867 explainer, カレントアウェアネス-E No.519, lane S081, states the move to a URL that embeds the capture timestamp and gives `warp.ndl.go.jp/web/20250102112233` as its example (S081, capture char 2604, committed capture 0034b800811072de3980e85b.txt).

#### Inference

- The tuple is the binding, and its scored half is a page title plus an index: the evidence field is a list of "[Annotation ID, Evidence ID, Wikipedia URL, sentence ID]" tuples while the ids are not used for scoring, so what survives a verdict is the URL and the sentence number (S085, the Data Format section). A per-page revision is not part of that tuple.
- Durability comes from freezing the pool, not from stamping each citation: the pages ship as "Pre-processed Wikipedia Pages (June 2017 dump)" and the deposit holds wiki-pages.zip beside the labels under one concept doi (S085, the Download Links list; S087, the files list). A lane record that pins its own file bytes but not the pool's date is pinning the weaker half.
- The evidence-selection step is the weaker link, and the release gives the number: the label step agrees at "0.6841 in Fleiss" kappa while retrieval is stated at "95.42% precision and 72.36% recall", so a verdict inherits a recall figure that its own record does not carry (S086, the inter-annotator and retrieval figures). The paper restates it as "recall of 72.36%" against the super-annotators' evidence (S086, the super-annotator comparison).
- Multi-sentence and multi-page evidence is the ordinary case, not the edge: "31.75% of the claims" had more than one appropriate sentence, "16.82% of cases" required composition, and "12.15% of the claims" drew on several pages (S086, the annotation-consistency paragraph). A record shape carrying one span models the minority of that corpus.
- The authors' own check measures the label layer, not the evidence layer: 227 examples produced 91.2% correct labels, while the precision and recall figures describe retrieval (S086, the validation section). A support verdict can therefore quote an accuracy for its labels and none for its evidence set.
- The deposit dates the artefact, not the pages inside it: record 4925954 carries its own revision field that moves with the deposit, and the description still says 185,445 claims drawn from Wikipedia with no page identifier beyond a URL and an index (S087, the description and files fields). A citation bound this way inherits the dump's date but not a page's state.

#### Unknown

- Whether a verdict survives a later edit to a page inside the pool is not addressed. The deposit versions the artefact, and a tuple keeps pointing at the same title and sentence index after the underlying page changes; no source opened here says how that case is handled.
- Whether the authors considered a per-page revision id and rejected it is not stated. The word "revision" occurs zero times in the S085 capture and zero times in the S086 capture; its only occurrence in S087 is Zenodo's own record revision, which is not a page binding.
- The super-annotator comparison is two contiguous slices, not one span, and the staged single-sentence quote is not recorded. A phrase the staged Unknown attributed to related search-method literature does not occur in this capture at all: "exhaustive" occurs zero times.
- The 72.36% is measured against the super-annotators' evidence, not against a truth; the capture says "by the super-annotators" (S086, capture char 42116).
- No live fetch this round: no archive link, TimeGate or Zenodo file was opened, so whether the deposited pool file resolves today is unknown. The newer family releases listed on the page (FEVEROUS, AVERITEC, AVERITEC 2.0, AVERIMATEC) were not opened, and whether any adds a revision binding is unknown.
```

# ScoutProvinceFit — province check, the two C3 staged entries

item: judge both staged entries group by group against chousa's province; name every sentence
that must be cut on adoption; decide whether base Obs 4 crosses into model evaluation.
scope: read-only; no lane production write, no git/jj mutation, no shokuknow tool, no fetch.

## Rubric (verbatim, deciding clauses)

- `PROVINCE.md:3-11` — Owns "question framing; source hierarchy (primary / secondary /
  aggregator / unsourced); citation chaining and hop resolution; claim-vs-source verification;
  … this lane's own corpus and gates." Refuses "model-quality or evaluation claims (→ kengaku);
  orchestration, multi-agent dispatch and agent lifecycle (→ kumitate …)".
- `kengaku-shokunin/PROVINCE.md:3` — "**Domain:** LLM/model research & evaluation"; its own
  table routes "**chousa** | research method — … this lane holds neither method nor duplicates it".
- `kumitate-shokunin/PROVINCE.md` Adjacent — "Research method → chousa."

**Test applied — the subject decides, not the venue.** A sentence about how a verdict binds to
a source state, how a corpus records its evidence, or how far a corpus can be trusted is
chousa's. A sentence about a *system's* accuracy is kengaku's. S086 is an ACL paper, but it is
read here as a primary source on citation binding, not as eval literature.

## Verdict: both entries are in province. Zero sentence-groups are out of province.

Base — `/home/vgpnk/Projects/shokuknow/merge/chousa/knowledge/corpus/knowledge/evidence-pool-versioning-r39.md`

| # | group | province | deciding sentence |
|---|---|---|---|
| F1 | frontmatter + ground | IN | "continues wave 3's `claim-support-test-r37-amendment`" — method continuity |
| F2 | Obs 1, binding = URL + sentence id | IN | "evidence field is 'a list of evidence sets … [Wikipedia URL, sentence ID] tuples'" |
| F3 | Obs 2, durability from freezing the pool | IN | "The durability comes from freezing the pool, not from stamping the citations" |
| F4 | Obs 3, 0.6841 / 95.42 / 72.36 / 31.75-16.82-12.15 | IN (seam S1) | "Inter-annotator agreement was 0.6841 in Fleiss kappa" — human annotation, not a model's |
| F5 | Obs 4, "the authors measured the labels themselves" | IN (below) | "Of 227 examples annotated by the authors, '91.2 % … annotated correctly'" |
| F6 | Inf 1, Q11's mechanism | IN | "(a) freezing the evidence pool to a dated dump, (b) depositing … under a citable … identifier" |
| F7 | Inf 2, differs from the lane's r31 sha256 pin | IN | "The lane's r31 `sha256` pin fixes the *bytes of one file*" |
| F8 | Inf 3, evidence-selection is the weaker link | IN (cut C2) | "the sharpest available argument for a lane record to carry its **evidence set**" |
| F9 | Inf 4, multi-sentence sets; record shape | IN | "is the shape a lane evidence record should adopt" |
| F10 | Unknowns | IN (cut C3, C4) | "Whether a verdict survives the pool's own revision history is not addressed" |

Amendment — `…/evidence-pool-versioning-r39-amendment-2026-10-23.md`

| # | group | province | deciding sentence |
|---|---|---|---|
| A1 | frontmatter + ground | IN | "**This is a dated amendment** to wave 4's `evidence-pool-versioning-r39.md`" |
| A2 | Obs 1, `cached_source_url` + worked example | IN | "`cached_source_url`, described as 'An archive.org link for the source url'" |
| A3 | Obs 2, `claim_date` | IN | "Each claim has a `claim_date`" |
| A4 | Obs 3, fourth label | IN | "'Conflicting Evidence/Cherry-picking' … FEVER's three plus a state for a claim that is misleading" |
| A5 | Obs 4, mitigations, restriction, κ/74.7 | IN (cut C5) | "Annotation consistency is reported as κ=0.742 on verdicts and 74.7 % on QA pairs" |
| A6 | Inf 1, per-citation archived copy | IN (cut C6) | "pair every live evidence URL with a timestamped archive.org capture … and date the claim" |
| A7 | Inf 2, same shape as the lane's pin | IN (cut C7) | "the lane's `S095` amendment already noted that its own pin fixes bytes and not time" |
| A8 | Inf 3, fourth label answers the blind spot | IN (cut C8) | "it is a claim-level judgement over a set of per-citation verdicts" |
| A9 | Inf 4, date is a claim property | IN | "a lane record should not accept a source published after the claim it is being used to support" |
| A10 | Unknowns | IN | "The archive captures are 'where possible'"; "No figure for the *evidence-selection* step … was read" |

Nothing here invokes kumitate's ground (dispatch, lifecycle, route), kasegi's (claim package,
scope) or kagi's (secret). Nothing is reported out.

## Obs 4 — does NOT cross into model evaluation

The objects are **human annotators and the authors' own re-annotation**, not a system. S086
(`1c15b611118dee97e4105fcf.txt`): "As a final quality control step, we chose 227 exam- ples and
annotated them for accuracy of the labels and the evidence provided. We found that 91.2%"; and
§3.4.2 "We randomly selected 1% of the data to be annotated by super-annotators". The claims are
corpus-label reliability — the "how far to trust it for which scope" job `CORPUS.md` gives a
registry row.

The crossing sentence sits one line further in the source — "a manual error analysis of the
baseline system (Section 5.8)" — and **the entry does not carry it. It must not.** Any adopted
sentence putting a *system's* precision/recall beside these numbers is kengaku's.

**Seam S1 (the one real risk):** base Obs 3 and Inf 3 call 95.42 % "precision" and 72.36 %
"recall" without naming the comparator. The paper's comparator is regular annotators *against*
super-annotators: "We compared the regular annotations against this set of evidence and the
precision/recall was 95.42% and 72.36% respectively" (line 210). Unnamed, both read as system
metrics and become kengaku's by subject. **Required: name the comparator in both bullets**; the
landed base entry still omits it in Obs 3 and Inf 3.

## Sentences that must be cut on adoption (non-province grounds, all still binding)

- **C1 (as landed, REQUIRED FIX)** — base Obs 2: "the word 'revision' does not appear in the
  data-format section … (`S085`)". A negative claim must carry its sweep (`CORPUS.md`). Verified
  true — `grep -c revision 5a631…txt` → `0`, exit 1, whole capture — but no command is named.
- **C2** — staged base Inf 3: "misses something **a judge would have counted**". Cut "a judge";
  the comparator is the super-annotators' set, not a truth. (Landed base drops it.)
- **C3** — staged base Unknown 2: the quoted "Ideally, exhaustive search strategies should
  retrieve all references…" is **absent from S086** (`grep -c Ideally` → `0`). Unlocatable
  quote; cut. (Landed base replaced it.)
- **C4** — staged base Unknown 2: "**one super-annotator's** exhaustive set". Source has
  super-annotators, plural (1 % of the data). Cut the singular.
- **C5** — staged amendment Obs 4: "limited … to those published before the claim's date". The
  capture says "restricted to using only online evidence published before the claim’s date"
  (line 272, curly apostrophe); "limited" is not that sentence. Rewrite to the capture's bytes.
- **C6** — staged amendment Inf 1: "(round 1's `S071`, round 2's `S082`)". Lane `S071` is the
  coreutils `env(1)` manual, `S082` the AVeriTeC README; RFC 7089 is `S079`, WARP E2867 `S081`.
  Cut, re-bind by document.
- **C7** — staged amendment Inf 2: "the lane's `S095` amendment". No `S095` row exists (registry
  ends `S084`); the point is `corpus/knowledge/citation-version-binding-r36.md`. Cut.
- **C8** — staged amendment Inf 3: "the same shape as the aggregator finding from wave 2". No
  file or line named; unfalsifiable attribution. Cut the clause.
- **C9 (accuracy note)** — 74.7 % appears twice: abstract "74.7 % consistency on QA pairs" but
  § "recall rate is 74.7 % and the precision is 67.2 %" (lines 222, 761). "Consistency" without
  precision overstates; name the re-annotation recall.

None of C1–C9 is a province defect; the province verdict does not change.

## Command log (cwd `/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache`)

```
$ wc -c → 4146 5a631…  60153 1c15…  5676 7800…  12775 b73f…  126093 7876…
$ grep -c revision 5a63…txt → 0 (exit 1, whole capture: the negative claim is true)
$ grep -n "internal use only|Pre-processed Wikipedia Pages|list of evidence sets" 5a63…txt
162: Pre-processed Wikipedia Pages (June 2017 dump)
210: evidence : A list of evidence sets (lists of [Annotation ID, Evidence ID, Wikipedia URL, sentence ID] tuples) or a
212: (the Annotation ID and Evidence ID fields are for internal use only and are not used for scoring .
$ grep -n FEVEROUS\|AVERITEC\|AVERIMATEC 5a63…txt → 56: FEVEROUS (2021)  58: AVERITEC (2024)  60: AVERITEC 2.0 (2025)  62: AVERIMATEC (2026)
$ grep -o "conceptdoi[^,]*" 7800…txt → "conceptdoi": "10.5281/zenodo.4925953"; grep -c wiki-pages.zip → 1
$ sed -n '205,218p' 1c15…txt → "annotated by super-annotators … the precision/recall / was 95.42% and 72.36% respectively." | "As a final quality control step, we chose 227 exam- ples … We found that 91.2%"
$ grep -c Ideally 1c15…txt → 0 ; grep -o "used the June 2017 Wikipedia dump[^.]*" → "used the June 2017 Wikipedia dump, processed"
$ grep -n "0.742\|74.7" 7876…txt → 222: κ = 0.742 on verdicts and 74.7 % consistency on QA pairs | 275: … free-marginal κ of 0.742 over 100 re-annotated claims | 761: recall rate is 74.7 % … precision is 67.2 %
$ grep -n "published before the claim" 7876…txt → 272: … restricted to using only online evidence published before the claim’s date.
$ grep -n "classified into|Hunter_Biden" b73f…txt → "classified into four labels: "Supported", "Refuted", "Not … | 290: "source_url": "https://en.wikipedia.org/wiki/Hunter_Biden", 293: "cached_source_url": "…/web/20230323135844/https://en.wikipedia.org/wiki/Hunter_Biden"
$ grep -o "best estimate…" b73f…txt → "best estimate for the date the claim first appeared."
$ python3 slice 1c15…txt at the eight cited offsets → 6741 '95.42% precision and 72.36% recall in evi-\nde' | 1869 '0.6841 in Fleiss κ. For   ex' | 5534 '31.75% of the claims more' | 5842 '16.82% of cases. Fur-' | 5929 '12.15% of the claims, this evidence' | 15269 'used the June 2017 Wikipedia dump, processed ' | 20847 'We found that 91.2%' | 42011 'recall of 72.36%'
$ grep -rn "S095" corpus/knowledge corpus/SOURCES.md → only the amendment's own prose pointer
$ grep -nE "^\| S09" corpus/SOURCES.md → none (registry ends S084)
```

## State at read time (matters for Main)

Both entries landed under `corpus/knowledge/` while this scout ran — base
`evidence-pool-versioning-r39.md`, amendment `…-amendment-2026-10-23.md`, both
`verified-at: 2026-10-25`. They already apply C2–C8 and carry the char offsets I spot-checked
(all eight slice correctly). Left on the landed text: **C1** (sweep for the negative "revision"
claim) and **S1** (name the annotator-vs-super-annotator comparator in Obs 3 and Inf 3).
Stage-id trap for the row work: the staged `SOURCES.append.md` S085–S089 are GB/T 7714, CiNii
and J-STAGE rows — adopting by id arithmetic would file the FEVER dataset page under the
Chinese citation standard; the claim's S085–S089 binding must be by document only.

## Confidence and unknowns

- High: all twenty province calls (rubric clauses, deciding sentences and seam test all quoted).
- High: Obs 4 does not cross (both source sentences quoted; the baseline-system sentence is
  provably absent from the entry).
- Medium: "super-annotators" plural (C4) rests on the §3.4.2 sentence; how many super-annotators
  covered the 1 % sample is not stated in the capture.
- Unresolved: whether kengaku would claim the annotation-reliability framing anyway. Its province
  says "LLM/model research & evaluation"; a human-annotation kappa is not a model measurement,
  and `QUALITY.md:600` (criterion 65) plus r41's corpus-value counting already make dataset-shape
  facts this lane's ground. I did not route to kengaku — no seat authority.

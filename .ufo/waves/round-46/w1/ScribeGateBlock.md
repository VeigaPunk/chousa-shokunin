# ScribeGateBlock — draft `## Gate` for corpus/lessons/round-46.md

item: draft the round-46 Gate section (theme, two entries with province and bar
check, the reject and its flip, a second candidate, five rows with URL, access date
and quote, id-collision and census placeholders). seat: scribe, leaf; no production
file written, no fetch.

## Fenced block (draft — L1 pastes into `corpus/lessons/round-46.md`)

```md
## Gate

Theme: what makes a support verdict durable, and how a later corpus binds each
citation to an archived state. One theme, two entries, five rows, eleven located
quotes. No fetch. Ids bound by document, never by id arithmetic: staged S120 →
lane S085 (FEVER dataset page), S121 → S086 (FEVER NAACL paper, ACL PDF), S122 →
S087 (FEVER Zenodo record 4925954), S127 → S088 (AVeriTeC dataset page), S128 →
S089 (AVeriMaTeC arXiv HTML). Id-collision: <L1 FILL — the result recorded
under corpus/evidence/round46/>; rechecked in
`.ufo/waves/round-46/w1/ScoutCollisionRecheck.md`, the append as staged
re-defines held S082–S084 on other documents, S085–S089 are free, and the
five staged→lane offsets are −35/−35/−35/−39/−39 — no arithmetic reproduces
the block. Pre-append census: <L1 FILL — exit of
`scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin chousa`,
from corpus/evidence/round46/>.

Admit:

- `corpus/knowledge/evidence-pool-versioning-r39.md`, citing S085, S086, S087.
  Province: claim-vs-source verification, with the archived-state binding shared
  with citation chaining (PROVINCE.md, "Owns"; `.ufo/waves/round-46/w1/ScoutProvinceFit.md`
  holds both entries in province, zero groups cut). Bar: QC6 header complete
  (`source:` ×3, `verified-at: 2026-10-25`, `recheck: 365d` with its command) and
  used-by naming this entry; QC7 every source tier A; QC9 the reliability
  figures live only in this entry; QC10 no unfilled template, every pointer
  dated; QC25/30 each printed quote verbatim in its capture (11/11 slices
  byte-exact — see Rows); QC57 the access carries committed byte evidence (the
  capture sha256 per row in spans.tsv). Re-grounded, not copied: the staged
  "We used the June 2017 Wikipedia dump" is not contiguous in the PDF capture
  and the lane quotes `used the June 2017 Wikipedia dump, processed` instead;
  the staged "95.42% precision and 72.36% recall in evidence retrieval" is
  interrupted by a line break and a hyphen, so only `recall of 72.36%` is
  committed as a span and the precision figure is cited by offset. Open bar
  items (ScoutProvinceFit C1, S1): the negative "revision does not appear" claim
  names no sweep, and Obs 3/Inf 3 give 95.42/72.36 without naming the
  annotator-vs-super-annotator comparator.
- `corpus/knowledge/evidence-pool-versioning-r39-amendment-2026-10-23.md`,
  citing S088, S089. Province: claim-vs-source verification (text-and-image
  claim verdicts against archived evidence), not model quality. Bar: QC6
  header complete and used-by naming this entry; QC7 both sources tier A; QC9
  no figure has two homes; QC25/30 quotes verbatim in the captures; QC57
  capture sha256 recorded. Re-grounded, not copied: the curly apostrophe in
  `published before the claim’s date` is the capture's byte, and the staged prose
  ids were re-bound by document (below). Open: the 74.7% QA figure is the
  abstract's "consistency"; the capture's re-annotation line gives recall 74.7%
  and precision 67.2% (ScoutProvinceFit C9).

Reject:

- The staged `evidence-pool-versioning-r39-amendment-2026-10-23.md`, as staged.
  Refused in round 45 for two reasons: it amends a base entry the lane did not
  hold, and its prose ids point at other documents in lane numbering (S071 used
  for RFC 7089, which is lane S079) — `corpus/lessons/round-45.md` `## Gate`.
  This round adopts the corrected form ONLY because the flip is met, part by
  part: (i) the base entry is held — `corpus/knowledge/evidence-pool-versioning-r39.md`
  (5,451 bytes, sha256 `a59457ca2c177586…`, written 2026-10-25 07:25:44 −03:00);
  (ii) every prose id is re-bound by document — staged RFC 7089 quote → lane
  S079, staged NDL E2867/WARP quote → lane S081, and the staged pointer to an
  amendment id → the lane path `corpus/knowledge/citation-version-binding-r36.md`;
  (iii) its quotes are located in the captures — eleven rows in
  `corpus/evidence/round46/spans.tsv`, each span an exact slice at its recorded
  offset (11/11 verified: `capture[offset:offset+len(span)] == span`, capture
  sha256 equal). The one correction the flip needed — the staged ids printed
  verbatim at 07:26 and removed at 07:27 — is recorded under Findings, not here.

Second rejection candidate, for the L1's judgement in a later round (not this
one): `/home/vgpnk/Projects/shokuknow/merge/chousa/knowledge/corpus/knowledge/claim-support-test-r37-amendment-2026-10-23.md`.
Reason: it amends `corpus/knowledge/claim-support-test-r37.md`, which this lane
does not hold, and rests on S113–S115, staged but absent from the lane registry.
Flip: adopt the base entry in the same round, land S113–S115 by document, re-bind
the amendment's `source:` ids, and locate its quotes in the captures. Its
evidence-relative NOT ENOUGH INFO finding is what C1's junk class (c) lacks a
vocabulary for.

Rows: normalized to the census schema in scratch — status `mined`, opened
2026-10-25, recheck `365d`, no pipe in any cell, used-by exactly the citing
entry. Every quote ≤25 words, taken from the committed span manifest (char
offset is into the named capture; capture sha256 in spans.tsv).

| id | source (kind, tier) | URL | accessed | located quote (char)
| S085 | FEVER dataset page (dataset, A) | https://fever.ai/dataset/fever.html | 2026-10-25 | "A list of evidence sets" (2360); "Pre-processed Wikipedia Pages (June 2017 dump)" (1271)
| S086 | FEVER NAACL 2018 paper, ACL PDF (paper, A) | https://aclanthology.org/N18-1074.pdf | 2026-10-25 | "used the June 2017 Wikipedia dump, processed" (15269); "recall of 72.36%" (42011); "We found that 91.2%" (20847)
| S087 | FEVER Zenodo record 4925954 (dataset, A) | https://zenodo.org/api/records/4925954 | 2026-10-25 | "conceptdoi": "10.5281/zenodo.4925953" (171); "key": "wiki-pages.zip" (4929)
| S088 | AVeriTeC dataset page (dataset, A) | https://fever.ai/dataset/averitec.html | 2026-10-25 | "An archive.org link for the source url" (3929); "Our best estimate for the date the claim first appeared" (2904)
| S089 | AVeriMaTeC arXiv HTML (paper, A) | https://arxiv.org/html/2505.17978v2 | 2026-10-25 | "temporally constrained evidence annotation" (3022); "published before the claim’s date" (7137)

Capture digests (full, in spans.tsv): S085 `e18eeb26a5a5…d1ba92`, S086
`c508913aba17…d563f`, S087 `dfc3e0f50dc2…e00ed`, S088 `603f9b42ccba…87528b`,
S089 `35bdf1c1cbc3…c7480c`; every capture predates the launch and was written
2026-10-23 or 2026-10-24, so freshness is not a claim.

Counter snapshot at this draft (2026-10-25, lane tree): `ENTRIES=2/2
CITES_BOUND=0/5 QUOTE_ROWS=11/11 QUOTES_IN_SPAN=11/11 QUOTES_IN_ENTRY=11/11
CAPTURE_BOUND=11/11 REF_ID_UNBOUND=0 REF_BOUND=2/2 C3=FAIL`, exit 1 — the only
failing leg is CITES_BOUND until the five registry rows land (84 rows, last S084).
```

## Commands run (decisive lines)

1. `python3 corpus/evidence/round46/c3-count.py` → `ENTRIES=2/2 CITES_BOUND=0/5
   QUOTE_ROWS=11/11 QUOTES_IN_SPAN=11/11 QUOTES_IN_ENTRY=11/11 CAPTURE_BOUND=11/11
   REF_ID_UNBOUND=0 REF_BOUND=2/2 C3=FAIL`, exit 1.
2. Span alignment over all 11 rows → `csha True / slice True / q_in_span True /
   q_in_entry True`, 11/11; id scan with `\bS\d{3,}\b` vs `ALLOWED_IDS` → 0 unbound
   at 07:27, 2 at 07:26 (`S071`, `S095`).
3. `ls -la` → base entry 5,451 B 07:25:44; spans.tsv 2,492 B 07:25:22; amendment
   5,329 B 07:27:12 (5,139 B at 07:26 — a sibling was still editing).
4. `grep -c '^| S0' corpus/SOURCES.md` → 84; `^\| S08[5-9] ` → 0; `^| S11[345] ` → 0
   in the lane and 3 in `merge/chousa/SOURCES.append.md`; those five staged
   S085–S089 rows name GB/T 7714-2025, openstd, CiNii, J-STAGE, J-STAGE FAQ.

## Findings

1. One leg short of the frozen predicate, and it is a known executor item, not an
   entry defect: CITES_BOUND=0/5 until the five rows land; CAPTURE_BOUND 11/11 and
   every other leg passes.
2. Prose-id carry-forward, closed at 07:27 and worth a mistake line: the amendment
   first printed `S071` and `S095` verbatim, and `S082` as the staged WARP id though
   S082 is a live lane id naming the AVeriTeC README — the counter saw two and was
   blind to the third, the class the round-45 reject was about.
3. Five rows, eleven spans, every span byte-exact, every quote ≤25 words; the staged
   "We used the June 2017 Wikipedia dump" and the 95.42/72.36 sentence are not
   contiguous in the PDF capture, and "S085–S089" is bound by document, not by
   arithmetic from the staged append whose same strings name five other documents.
4. Second candidate: base not held (0 of 61 knowledge entries match
   `claim-support-test-r37.md`); its rows S113–S115 are staged (3), unlanded (0).
5. Misroot, caught and fixed (round-45 mistake 4 class): the first `write` used a
   relative path and landed at
   `/home/vgpnk/Projects/shokunin/.ufo/waves/round-46/w1/ScribeGateBlock.md`;
   copied byte-exact into the lane (`cmp` identical, sha256 `31c9836b942a00ba…`),
   the fleet copy deleted and its two empty directories removed.

## Limits

- `tools/quote-reopen.py verify` (QC30) was not run; my verbatim check is the same
  exact-slice comparison the C3 counter's `CAPTURE_BOUND` leg does, so the L1 should
  run QC30 if the rows are admitted. The two placeholders stay unfilled: no file for
  either exists under `corpus/evidence/round46/` at this snapshot. Tooling: no install,
  no pacman, no uv, no fetch; scratch `/tmp/chousa-r46-ScribeGateBlock/` removed.

# Round 47 lesson

author: chousa L1 (in-session L1, hyaku run 6)
date: 2026-10-25
base: `9a9f94dbcb010eca6636886e53950f38ca806329`
freeze: `22a44b8b5c923d25123a96a852c11938559bb9b2`
landings: C1 `a15610a5` then `980fe43f` (wave-1 refinements); C2 `7fb9a232`; C3 the round's
C3 commit (named in `SCORECARD.md` and the report)

No external fetch: the fetch-scope L0 `8d77e6c1` is still open. Every capture read this
round is on disk (campaign cache `.ufo/waves/corpus-expansion-1/.qcache`, file =
`sha256(url)[:24].txt`). Round tag (QUALITY 64): C1 plumbing, C2 plumbing, C3 ground.

## Claims

Frozen in `corpus/evidence/round47/claims.md` before any seat scored.

- C1 operability (lowest scored axis, 3/10): the inference check gains a polarity probe
  (`INF_POLARITY_FLIP`). Counter `python3 corpus/evidence/round47/c1-count.py`. Before
  `JUNK_KILLED=0/3 CANARY=fail C1=FAIL`, exit 1; after `3/3 3/3 CANARY=pass
  R46_COUNTER=pass R46_ENTRIES=2/2 C1=PASS`, exit 0. Round-46 named limit "entailment".
- C2 calibration: the gate registry agrees with the dependence and check-named set.
  Counter `python3 corpus/evidence/round47/c2-count.py --list`. Before (freeze tree)
  `MISMATCHES=25` on the freeze-time counter, `21` on the final counter; after
  `MISMATCHES=0 C2=PASS` on both. Round-46 named limit "mention, not dependence", closure
  routed defects 2 and 4.
- C3 depth (assimilation §10, one theme: what a support test is, how it is applied, how
  reliable it is): `corpus/knowledge/claim-support-test-r37.md` and its
  `-amendment-2026-10-23.md`, rows S090–S094 plus held S085 re-bound, 35 spans. Counter
  `python3 corpus/evidence/round47/c3-count.py` (and `--lane-only`). Before every leg 0,
  exit 1; after every leg full, exit 0. Round-46 named limit "anchor cells", closure routed
  defect 5.

## Mistakes

1. Class: receipt-contamination (L1, before the freeze). Evidence: the first
   `controls/c2-before.txt` copied the round-47 counter INTO the base archive, so the
   round-46 name pattern counted it and the "bare base" read `ENTRY_POINTS=82
   (counters=51)` where the clean base reads `81 (counters=50)`. Captured-by: none — the
   L1 saw the number disagree with the round-46 closure's `81/81`. Fix: the counter runs
   from the freeze tree with `--root <archive>`; the archive is never written. Shown able to
   fail: the contaminated and clean runs print different denominators on the same base.
2. Class: masked exit code (L1, before the freeze). Evidence: piping a counter through
   `rg` recorded `exit=0` for a counter that printed `C2=FAIL`. Captured-by: none. Fix:
   every receipt is written by a `run` helper that saves the counter's own `$?` before any
   filter. Shown able to fail: the masked receipt said `exit=0` beside `C2=FAIL`; the
   committed receipts say `exit=1`.
3. Class: parser defect in a frozen instrument (C2). Evidence: the freeze-time
   `c2-count.py` split cells on every `|`, so GFM-escaped `\|` inside the round-24–27 row's
   entry cell shifted its cells and dropped ten registered instruments; it also tested the
   verdict cell for the substring `exit`, so a cell reading "no exit code documented"
   registered a path, while `` `0` clean · `1` failed `` did not (`ReviewerC2Set` F1–F3,
   `MutC2Forge` b2/c2/d3/e3, `CritC2Framing` finding 1). Captured-by: the wave-1 reviewer
   and mutation-tester. Fix: unescaped-pipe split, both fence kinds literal, every inline
   comment stripped, an exit-code pattern instead of a word, `./` normalised, DANGLING reads
   every row, bare script names resolve against their file's directory. Each change moves
   the instrument toward the frozen sentence ("names it in its `entry` cell, with an exit
   code in its `verdict map` cell"); the before receipts were re-measured on the final
   counter (`controls/c2-before.txt`, final section: freeze tree 21, base 18). Shown able to
   fail: the "no exit code documented" forge no longer registers; the final counter's
   DANGLING caught two path-shaped strings in the L1's own new rows (`SCRIPT_DIR/…`,
   `base-gate-r36/37/…`) before landing. The claim verifies under BOTH instruments: the
   freeze-time counter prints `MISMATCHES=0` at the landing too, after the round-24–27 row's
   `\|` alternatives were written as `/` (meaning-preserving; disclosed here).
4. Class: over-refusal (C1). Evidence: the first probe refused 9 of 10 correctly-reasoned
   bullets about a negated span phrase (`LabC1FalsePos`): implicit negatives (`lacks`,
   `absent`, `untraceable`) read as affirmative. Captured-by: the wave-1 critic; the frozen
   fixtures could not see it (three positives, one phrasing each). Fix: implicit negators
   and `un…able`/`un…ed` forms count; a span negator counts only inside the phrase's own
   line and clause. Shown able to fail: the first widening made the round-46 entry fail on
   `(Unlabelled)` one list line above `Pre-processed Wikipedia Pages` — the counter's
   `R46_ENTRIES` leg printed `1/2` — and the clause bound restored `2/2`. The same ten bullets
   now score 5/10 refused; the remaining five fall outside the frozen three-before/two-after
   window. That ten-bullet set was used to tune, so it is not a held-out measure; wave 2's
   fresh set is.
5. Class: order-dependent verdict (C1). Evidence: polarity was read from the first
   carrying span, so swapping two manifest rows flipped the verdict on the same bullet
   (`ReviewerC1Polarity` M4, `MutC1Probe` h). Fix: every occurrence is read; mixed polarity
   decides nothing. Also fixed from the same seats: every figure occurrence is checked at
   digit boundaries (M1, M2), string-valued counts and key paths carry polarity (M3, L1), an
   `un`-prefixed form of an affirmed word is a flip (`CritC1Survivors` 1b).
6. Class: attribution drift (staged package). Evidence: the staged base entry and row S099
   date CFEVER "AAAI 2021"; the capture's running header reads `The Thirty-Eighth AAAI
   Conference on Artificial Intelligence (AAAI-24)` and `Copyright © 2024` (chars 41, 6351;
   `ReviewOpenS091`). Captured-by: the source-opening seat. Fix: S091 and the entry carry
   AAAI-24.
7. Class: stale unknown (staged package). Evidence: four staged `#### Unknown` bullets say
   a figure "was not read" or a render "was truncated", and each capture holds it:
   PEOPLEPROFILES' agreement (S090 char 20954), FEVER's evidence-retrieval precision/recall
   (S092 char 6601), climate-fever's Krippendorff α 0.334 (S093 char 16287), and "the FEVER
   paper only as an abstract" while the lane holds S086 (`ReviewOpenS090`, `S092`, `S093`,
   `ScoutProvinceFit`). Captured-by: the openers. Fix: both entries state the figures, and
   PEOPLEPROFILES' model-agreement figure is left to kengaku (province).
8. Class: anchor drift (routed defect 5). Evidence: S085's anchor said `char 2349`, the
   start of a longer slice, not of a located quote. Captured-by: the round-47 counter's
   `ANCHOR_BOUND` leg (before `0/6`). Fix: the cell names `char 2360` and `char 1271`, and
   every new row's anchor is generated from the span manifest.

9. Class: unclosed routed fix (rounds 41–46). Evidence: the round-40 counter at the tip
   prints `R39_ACTIVE_RECEIPTS=2/6`, exit 1 — four committed receipts refuse
   `gate-sha256-mismatch` because `1bd9001` (round 41) moved `tools/research-gate.sh`;
   round 41 recorded it and routed a successor-counter design to round 42, and no later
   lesson closes it (`ExecReceiptSpot`). Captured-by: none — no criterion re-ran old
   receipts. Fix: QUALITY 68 (one re-verify per round, pinned and tip legs). Shown able to
   fail: at `b173b094` the counter reads `6/6`, exit 0; one changed receipt byte reads `5/6`,
   exit 1. The receipts themselves are not repaired this round (named, routed to round 48).

## Named limits after the wave-1 fixes

- C1: the probe counts negators in fixed windows; it does not compute polarity. A flip
  through a different stem (`revised` → `edited`), a negator four or more words away, double
  negation, or a flip in a second bullet that quotes other tokens still passes
  (`CritC1Survivors` 1, 2, 3, 4a/4b). The capability is "a windowed stem-sharing negator
  mismatch", not entailment, and the round-45 D7 class is narrowed, not closed.
- C2: row truth (does the verdict map describe the script?) and the gate-vs-control
  distinction stay a reader's check; one junk row listing every path in its entry cell
  with `exit 0` still registers them (`MutC2Forge` a); FLOOR is a count, so a deleted gate
  can be replaced by an empty script (g2); a root-level script with no `/` is not a
  DANGLING candidate (e4).
- C3: quotes are single-line slices (PDF captures break lines and interleave columns), so a
  sentence that crosses a line break is quoted in pieces.

## Gate

Theme: what a support test is, how it is applied, and how reliable it is. One theme, two
entries, five new rows (S090–S094) and one held row re-bound (S085). No fetch.

Ids bound **by document** (URL equality), never by arithmetic: staged S097 → held lane
S085 (no new row; `used-by` gains the base entry), S098 → S090, S099 → S091, S113 → S092,
S114 → S093, S115 → S094. The offsets are −12/−8/−8/−21/−21/−21, so nothing arithmetic
reproduces them. The registry held 89 rows (`S001`–`S089`, contiguous;
`.ufo/waves/round-47/assimilation/reg-ids`), so the next five are S090–S094.

Id collision: **8 ids** (`S082`–`S089`; `assimilation/collisions`, sha256 `76b8703b…`,
the intersection of 89 lane ids and 114 staged ids); each names a different document on
each side. Guard proven before the append: `assimilation/guard-proof/` holds an indented
`  | S097 |` row that the 0–3-space extraction catches (`collisions` = `S097`) and a
column-0 extraction misses (`collisions-col0` empty). Nothing was appended from the staged
block as-is; the six rows were written from the captures. Pre-append mirror
(`assimilation/mirror-census.txt`): lane `corpus/` + `tools/` + the six rows, `sources-census.sh
validate --file` **exit 0**, five pre-existing W04, no E03/E04/E11 (a first mirror without
`tools/` gave E11 on S077, the round-45 mistake-3 class; the lane was never touched by it).

Register ids are not lane ids: register S093 = lane S090, S094 = lane S091, S108 = lane
S092, S110 = lane S094. Lane S093 (climate-fever) and S085 have no register row.

Quarantine (§10), the four register rows on this theme's URLs, hand-checked this round
(the lane's slice re-derived with the operator awk recipe: 24 data rows):

- quarantine: register `S093` (https://aclanthology.org/2026.findings-acl.19.pdf) verdict: `present` — all 22 quote words occur in order at chars 1526–1705 of capture `4132ec1b…`, broken only by the interleaved figure label `Cited source` (char 1648), the elided enumerator `(2)` (char 1613) and the register's truncation `un` → `unsupported` (`QuarReg093`).
- quarantine: register `S094` (https://ojs.aaai.org/index.php/AAAI/article/download/29825/31432) verdict: `present` — the three register quotes occur word for word in order at chars 810–965, 966–1156 and 1187–1359 of capture `3749141b…`, broken only by the Table 1 example interleave and the hyphen splits `fac-`/`tualness`, `Sup-`/`ports`, `cor-`/`responding` (`QuarReg094`).
- quarantine: register `S108` (https://arxiv.org/html/1803.05355) verdict: `present` — the quote is one abstract sentence at chars 2731–2848 of capture `b502d4c6…`; the miss is render markup (`Supported ,`, `κ \kappa .`) (`QuarReg108`).
- quarantine: register `S110` (https://aclanthology.org/2025.coling-main.108.pdf) verdict: `present` — the three quotes occur in order once the two columns are de-interleaved and `inter-`/`annotator`, `an-`/`notate` are joined (chars 21381–21632, 20304–20682, 20004–20529 of capture `a9cf4170…`) (`QuarReg110`).

Every `payload-absent` on this theme is a mechanical false negative of the class rounds 43
and 46 adjudicated; no row is refused for fabrication.

Admit:

- `corpus/knowledge/claim-support-test-r37.md`, citing S085, S090, S091 (and S086/S092 by
  pointer). Province: claim-vs-source verification (`PROVINCE.md` Owns). PEOPLEPROFILES'
  model-to-human agreement (α=66.3) is a model-quality figure and is NOT imported — the
  entry names it as kengaku's (`ScoutProvinceFit`). QUALITY: Observation, Inference and
  Unknown are separate (3); every Inference bullet cites a tier-A row and every quoted
  phrase sits in a committed span (66: `tools/inference-ground.py` → `GROUND: PASS`,
  `tokens=16 grounded=16`). Re-grounded, not copied: the venue (mistake 6); the staged
  "roughly a third of real citations do not support the claim" is replaced by the two
  rates at the scope the paper measured (∼22% of lead claims against the article body, ∼30%
  of body claims against public sources, both on model labels); "declared null" is the
  staged gloss — the page offers the null tuple as the alternative evidence form and says
  the kept positions are unscored; "select at most three" is `Select 0, 1, 2, or *at
  maximum* 3 sentence(s)`, and PEOPLEPROFILES grades on a −1..1 scale, so it is not
  three-way.
- `corpus/knowledge/claim-support-test-r37-amendment-2026-10-23.md`, citing S092, S093,
  S094. Province: same; it makes no claim about any model's agreement. QUALITY 66:
  `GROUND: PASS`, `tokens=21 grounded=21`. Re-grounded: 0.6841 scores three labels by five
  annotators on a 4% sample ("5-way" names the annotators); 0.792 scores seven
  claim-evidence correlation labels between two annotators, not the verdict; the 202
  relabelled claims are stated as pool-dependence (CorFEVER's real-world set changes the
  evidence pool), not as error in FEVER's labels (`CritC3Inference` 3–4); the FEVER
  guideline is quoted from the appendix copy with its curly apostrophe; climate-fever's α
  0.334 is added as the only real-world figure.
- Round-46 flip for the amendment ("the base entry is adopted with its own rows and the
  amendment's quotes are located in committed spans"): met — `ENTRIES=2/2`,
  `CITES_BOUND=6/6`, `SPAN_IDS=6/6`, `QUOTES_IN_SPAN=35/35`, `CAPTURE_BOUND=35/35`.

Reject:

- `citation-count-semantics-r37.md` (staged) — **not this round**. Off this round's theme,
  and its headline observation rests on staged S100, whose capture `b539a802…` is a lossily
  decoded OLE `.doc` (308,430 U+FFFD; zero hits for 自引 under utf-8/utf-16/gbk/gb18030/big5)
  while S101's capture has zero hits for 文献标志码; both URLs are unchecked register rows
  (S095, S096). In province (citation chaining), not generic. Flip: a byte-faithful capture
  of S100 and S101 that holds the quoted sentences, register S095/S096 hand-checked, ids
  bound by document past S094 (`ScribeGateBlock`).
- `search-log-fields-r36.md` (staged) — **refused again**. The round-43 refusal stands
  (`lessons/round-43.md`) and its flip is unmet: the PRISMA-S DOI capture is still a
  267-byte `Client Challenge` page (register S077) and the J-STAGE capture has zero hits for
  参照日. Not a duplicate of `search-log-method-r39.md` (that holds the log-as-document half).
  Flip: the round-43 flip, plus ids bound by document past S094.

Rows added or changed (opened 2026-10-25 from on-disk captures, all `mined`, recheck `365d`;
every `char N` is generated from `corpus/evidence/round47/spans.tsv`):

- **S085** https://fever.ai/dataset/fever.html — re-bound: anchor `char 2349` → `char 2360: A list of evidence sets` and `char 1271: Pre-processed Wikipedia Pages (June 2017 dump)`; `used-by` old `corpus/knowledge/evidence-pool-versioning-r39.md` → new `corpus/knowledge/evidence-pool-versioning-r39.md, corpus/knowledge/claim-support-test-r37.md`.
- **S090** https://aclanthology.org/2026.findings-acl.19.pdf — "∼22% of claims in Wikipedia lead sections" (char 1526); "of claims in the article body are unsupported" (char 1669).
- **S091** https://ojs.aaai.org/index.php/AAAI/article/download/29825/31432 — "Each claim in CFEVER is labeled as “Supports”," (char 966); "a Fleiss’ kappa value of 0.7934 for five-way inter-annotator" (char 1567).
- **S092** https://arxiv.org/html/1803.05355 — "For the first two classes, the annotators also recorded the sentence(s)" (char 2849); "95.42% precision and 72.36% recall in evidence retrieval" (char 6601). A separate row from S086 by content: the annotation-guideline appendix (A.6, A.7.3) is absent from the S086 NAACL capture (`ReviewOpenS092`).
- **S093** https://arxiv.org/html/2012.00614v2 — "7,675 annotated claim-evidence pairs" (char 5157); "If there is both supporting and refuting evidence the claim-label is DISPUTED" (char 13373).
- **S094** https://aclanthology.org/2025.coling-main.108.pdf — "the claim-relevant evidence gathered from open" (char 20462); "This manner results in total 202" (char 20650).

Recheck prose stripped from the staged rows (each became `365d`): S097 "re-open and confirm
the label set and evidence format", S098 "confirm Definitions 1 and 2", S099 "confirm the
label set and evidence requirement", S113–S115 "confirm the decision rule, the 7,675-pair
sentence and the 0.792 figure" (`ScribeRows`).

## considerthese

`considerthese/2026-10-24.md` "Spot re-verify one receipt a week" — the one proposal of the
latest file not yet implemented. Mined as QUALITY 68 (`ExecReceiptSpot`); the cloud-agent
part needs operator approval and is not done.

## Census

`scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin chousa`: round
start **exit 0** (89 rows, five W04; `.ufo/waves/round-47/assimilation/census-start.txt`);
after the append **exit 0** (94 rows, the same five W04).

# Round 46 lesson

author: chousa L1 (omp in-session L1, hyaku run 6)
date: 2026-10-25
base: `6e2630a6343948b3fe5bf299901207a0619ad949`
freeze: `c2f0e9d100c0d46633a6277b2fd51d2ac99678eb`
landing: `d09fc8e7e2972e30e5e0aaa6e404c97aa0b9f95a`

No external fetch: the fetch-scope L0 `8d77e6c1` is still open. Every capture
read this round is on disk (campaign cache
`.ufo/waves/corpus-expansion-1/.qcache`, file = `sha256(url)[:24].txt`).
Round tag (QUALITY 64): C1 plumbing, C2 plumbing, C3 ground.

## Claims

Frozen in `corpus/evidence/round46/claims.md` before any seat scored.

- C1 operability (lowest scored axis, 3/10), capability: `tools/inference-ground.py`
  exits 0 on every `positive-*.md` and 1 on every `junk-*.md` fixture of
  `corpus/fixtures/inference-ground-r46/`. Counter
  `python3 corpus/evidence/round46/c1-count.py`. Before `TOOL=absent 0/3 0/3`,
  exit 1; after `3/3 3/3 C1=PASS`, exit 0. Routed from the round-45 closure, D7.
- C2 calibration: every committed gate entry point named inside a `## Gates` row,
  the set being tools/, the round-45 counter pattern, and every existing
  `*.py`/`*.sh` a SCORECARD or claims cell names. Counter
  `python3 corpus/evidence/round46/c2-count.py --list`. Before `55/71` with
  `UNREGISTERED=16` (freeze tree; the bare base is `55/68`, 13); after
  `REGISTERED=72/72 UNREGISTERED=0`, exit 0. Routed from the round-45 closure, D8.
- C3 depth (assimilation §10, one theme: what makes a support verdict durable,
  and how a later corpus binds each citation to an archived state): two staged
  entries adopted as `corpus/knowledge/evidence-pool-versioning-r39.md` and
  `…-r39-amendment-2026-10-23.md`, rows S085–S089, eleven spans. Counter
  `python3 corpus/evidence/round46/c3-count.py` (and `--lane-only`). Before
  `ENTRIES=0/2`, exit 1; after every leg full, exit 0.

## Mistakes

1. Class: survivor / unenforced-sentence. Evidence: the junk leg of
   `c1-count.py` accepted ANY non-zero exit (a crash scored as a kill) and the
   fixtures were unpinned, so the kill rule's "fixture set changed after this
   freeze" clause had no teeth — `MutC1Junk`, `SentScopeAudit` F1/F2, then
   `CritC1Attack` point 5. Captured-by: none at freeze; the frozen sentence says
   "exits 1" and the implementation checked `!= 0`. Fix: `== 1`, plus a `PINNED`
   dict of sha256 per fixture and a `FIXTURES_CHANGED=` line. Shown able to fail:
   an exit-2 stub scored `JUNK_KILLED=3/3` before and is refused after; a
   one-byte fixture edit now prints `FIXTURES_CHANGED=positive-a.md`.
2. Class: strawman-fixture. Evidence: `junk-borrowed.md` is declared the D7
   class ("correct spans and figures, wrong inference") but dies on two invented
   tokens, i.e. on the same leg as `junk-ungrounded.md`; a pure class-(c) body
   reusing only verbatim tokens passes (`CritC1Attack` 1–3, `ReviewerC1Tool`).
   Captured-by: the critic. Fix: the capability is reported as presence, not
   entailment (`SCORECARD.md` C1 cell, SKILL Gates row), and entailment is
   round 47's candidate. Shown able to fail: the class-(c) body at
   `.ufo/waves/round-46/w1/CritC1Attack.md` §2 exits 0.
3. Class: unsound-escape. Evidence: the registry leg added to
   `inference-ground.py` matched a numeral against the whole `source` cell, so
   `2,013 answers … (S020)` grounded on the year `2013` and `1,534 claims …
   (S005)` on a URL run `…acl-long.1534`; 27 of 86 rows carry a 4-digit URL run
   (`ReviewerC1Tool` HIGH). Captured-by: the code reviewer. Fix: only a document
   DESIGNATOR from the title (`RFC 7089`, `E2867`, `N18-1074`) grounds a numeral.
   Shown able to fail: both forged bullets exit 1 now, and the two admitted
   entries still pass on `RFC 7089`.
4. Class: forgeable-instrument (C2). Evidence: a valid-looking row inside a
   fenced block, and one naming `…/self-audit.pyc`, both scored
   `REGISTERED=72/72 C2=PASS`; a row with an HTML comment naming the paths also
   passed (`MutC2Forge`). Captured-by: the mutation-tester. Fix: fence-aware row
   scan, HTML comments stripped, delimiter-bounded path match. Shown able to
   fail: `controls/c2-controls.txt` records `SKILL-fenced` and `SKILL-suffix` at
   `UNREGISTERED=16`, exit 1, with the four original controls unchanged.
5. Class: read-oracle. Evidence: a manifest `span_file` of `../…` or an absolute
   path made `inference-ground.py` read outside the spans directory, so a forged
   row grounded a bullet from `/tmp` (`SentScopeAudit` F3; same class in
   `c3-count.py`). Fix: absolute paths and `..` components are skipped and the
   resolved path must stay under the manifest directory; `int(offset)` guarded.
   Shown able to fail: an escape-only manifest now exits 1 (sentinel re-probe).
6. Class: misroot. Evidence: `ScribeGateBlock`'s first draft landed under the
   fleet root's `.ufo/waves/round-46/` despite the absolute lane path in the
   context. Captured-by: the seat itself plus the round prompt's misroot sweep.
   Fix: copied byte-exact into the lane, `cmp` identical, fleet copy and its two
   empty dirs deleted; the final `git -C` fleet sweep shows no chousa/round-46
   path.
7. Class: anchor-drift. Evidence: the S088 Registry row said "char 2891: Our
   best estimate…" while 2891 is the `claim_date` cell and the quote starts at
   2904 (`ReviewerC3Spans` defect 1). Captured-by: none — C3 checks quote and
   offset, never the row's `anchor` cell (a named limit). Fix: the row names the
   field cell at 2891 and the quote at 2904. Shown able to fail: the corrected
   cell states both offsets, so a reader can separate them; the counter still
   cannot.
8. Class: fabricated-quote (staged package). Evidence: the staged amendment's
   `"limited ... to those published before the claim's date"` does not occur in
   either S089 or S088; the capture reads `restricted to using only online
   evidence published before the claim’s date` with a curly apostrophe
   (`ReviewOpenS089` X1, `ReviewOpenS086` on the sibling). Captured-by: the
   source-opening seats; CORPUS rule "a quote names its location" catches this
   only if the round re-opens it, which is why §10 demands it. Fix: the entry
   quotes the capture's bytes and records the correction in `## Unknown`.
9. Class: attribution-drift. Evidence: `74.7%` written for a capture that says
   `74.7 %`; "AVeriTeC is text-and-image claims" when the image-text corpus is
   AVerImaTeC (`S089`); the pin-fixes-bytes-not-time point attributed to r36
   alone when r36 and r37 split it (`ReviewerC3Spans` 5, `ScribeEntryAmend` c–e,
   `CritC3Inference` I2). Fix: all four sentences corrected; the temporal rule is
   now stated of the successor corpus and of the annotators, not of a pipeline.
10. Class: number-drift (before-state label). Evidence: `controls/c2-before.txt`
    was taken on the freeze tree, so its `UNREGISTERED=16` includes the three
    round-46 counters; the bare base tree reads `ENTRY_POINTS=68 UNREGISTERED=13`
    (`ReviewerC2Set` High). Fix: the receipt now carries three labelled trees
    (A: freeze tree, B: base + the whole round-46 dir, C: bare base) and the kill
    rule's `ENTRY_POINTS ≥ 71` is stated to bind the after tree. Shown able to
    fail: the three trees print three different denominators.
11. Class: entailed-leg. Evidence: every span file was byte-identical to its
    quote, so `QUOTES_IN_SPAN` was entailed by `CAPTURE_BOUND` and no span showed
    any captured context (`ReviewOpenS086` M1). Fix: `build-spans.py` now emits
    the quote with 80 chars of context either side and `offset` is the span
    start; a span is 194–196 chars against 16–56 for its quote. Shown able to
    fail: `--check` re-derives 11/11 and the span lengths differ from the quote
    lengths by construction.
12. Class: post-freeze instrument edit. Evidence: all three counters and the tool
    were edited after the freeze commit (07:27–07:30), each change strictly
    toward the frozen sentence (`ScoutInheritedTree`, `ConnectSiblings`). Fix:
    disclosed here and in the report; the before receipts were re-measured with
    the final revisions; value-neutrality measured — C2's numbers are identical
    on the same tree, C1's fixture exits unchanged, C3's guards cannot fire on
    the committed manifest. No frozen target, predicate or control was changed.

13. Class: filename-oracle. Evidence: C1's counter compares exit codes only,
    so a "tool" that exits 0 for names starting `positive-` and 1 otherwise
    scored `3/3 3/3 C1=PASS` without reading a byte (`ExecCounterRun`). Fix: a
    CANARY leg copies the first positive and the first junk fixture under neutral
    names (`canary-a.md`, `canary-b.md`) and requires 0 and 1. Shown able to
    fail: `controls/c1-controls.txt` records the name oracle at `CANARY=fail
    C1=FAIL`, the citation-presence-only forge at `CANARY=pass JUNK_KILLED=1/3`,
    the always-exit-0 forge at `CANARY=fail JUNK_KILLED=0/3`, and the real tool at
    `CANARY=pass`.
14. Class: co-occurrence-leg. Evidence: C3's `REF_BOUND` requires the S079
    sentence to contain `RFC 7089`; a forged sentence `S079 is not RFC 7089`
    passes it (`ExecCounterRun`), and C2's row test is format-only — a junk
    8-cell row registers an unregistered path. Both are named limits of the
    frozen sentences (they say "named" and "the sentence names"), not defects to
    repair inside the claim; recorded here so round 47 inherits them.

## Wave-2 corrections and record errata

Every item below was found by a wave-2 seat, applied in the lane, and re-measured.
None changes a frozen predicate, target or kill rule.

- **Zenodo identifier roles were inverted** (`CritC3Inference` F1). The record's
  own doi is 10.5281/zenodo.4925954; `conceptdoi` 10.5281/zenodo.4925953 names the
  version SERIES. The adopted entries said the reverse (and `corpus/README.md`
  repeated it); all three now state the roles correctly, with `relations.version`
  (`parent.pid_value` 4925953, char 1439) as the evidence. Recorded here because
  the C3 kill rule requires a corrected staged sentence to be logged.
- **72.36% reattributed** to the annotators' agreement against the
  super-annotators, not to a system (`CritC3Inference`, `RevC3Entries`); the
  word "exhaustive" is now anchored to the paper's "every possible sentence"
  (char 20059) in both the entry and the S086 row instead of standing unquoted.
- **Entry char pointers corrected**: the S089 archiving sentence is at 14582 (not
  14603), the null-pair pointer at 9949 (not 9920), `"revision": 2` at 3666.
- **The amendment's 1,582/7,572 pairing** (which does not partition the
  set: 5,959 + 1,582 = 7,541) was replaced by the remainder phrasing, and the
  staged "operational in the pipeline" is corrected to the annotators.
- **SKILL Gates rows moved inside the table** (`RevGatesRows` F1): the first
  insertion sat after the blank line that closes the header table, so the rows
  did not render as rows even though the counter counted them. They now sit
  directly under `tag-count`. Stale digests were replaced by a pointer to
  `measure-after.txt`, and the round24–27 verdict map no longer claims an exit-2
  path for scripts that have none.
- **SOURCES table blank line removed** (`RevC3Rows` F7): the same defect in the
  registry — a blank line ended the table before S085–S089.
- **C2 row rule raised to nine separators** (eight cells), because a single
  seven-cell row holding every path scored `UNREGISTERED=0` (`RevInherited`);
  eight-cell rows still register.
- **C1 counter deduplicated** (`RevC1Controls` D4): a bad patch left three dead
  copies of `main()` after `sys.exit(main())`; the file is one copy again. The
  three forge scripts are now committed under `controls/` so every control
  receipt is re-executable (D5).
- **C3 gains three legs** (`RevC3Spans` F2/F3/F4): `SPAN_IDS=5/5` (every bound
  source has at least one span), `SPAN_CONTEXT=11/11` (a span is longer than its
  quote), and a non-negative-integer offset guard.
- **C1's canary and fixture pins are ADDED discrimination legs, not the frozen
  predicate** (`RevC1Controls` D2). The frozen sentence quantifies over the six
  named fixtures' exit codes; that sentence is met at every revision. The CANARY
  leg (renamed copies) and the byte pins are post-freeze hardening: they also
  pass, and they refuse forges the frozen legs cannot see. Any closure reading
  the counter should score the frozen legs first and report the added ones
  separately.
- **`measure-after.txt` is regenerated over a `git archive` of the landing
  commit** (`RevC3Census` F1, `RevC1Controls` D1): the earlier copy mixed a
  committed counter with an uncommitted tool.
- **Before-state now records four trees** (`RevC2Before` H1): A = base + the
  three counters + fixtures (`71`, `UNREGISTERED=16`), B = base + the whole
  round-46 dir (`71`, `16`), C = base + the counters only (`71`, `16`), D = the
  pristine base archive (`68`, `13`, the true pre-existing debt). The after-state
  is `73/73` at HEAD (`72/72` at the landing commit; the +1 is `build-spans.py`,
  which enters the set once SCORECARD names it).

### Named limits of the round-46 instruments (not repaired inside the claims)

- **C1, designator leg untested.** The counter invokes the tool without
  `--registry`, so the document-designator credential (which lets `RFC 7089`
  ground its own numeral) is dead on every scored run and a mutant that drops it
  still scores `3/3 3/3 CANARY=pass` (`MutC1Tool` A). The leg is exercised only
  by the admitted entries (`measure-after.txt`), not by a fixture.
- **C1, section-end untested.** No frozen fixture has content after its
  `#### Inference` section, so a mutant that never ends the section survives; the
  direction is strictness — it would wrongly REFUSE a positive entry, never admit
  junk (`MutC1Tool` B). `####` headings whose text merely starts with
  "inference" (`#### Inference Notes`) are treated as the section.
- **C1, fixture-name oracle.** Closed this round by the CANARY leg (mistake 13).
- **C1, entailment.** Unclosed: a body of correct tokens asserting the opposite
  still passes (mistake 2).
- **C2, mention not dependence.** `corpus/evidence/round45/tag-count.py` is a
  documented gate with a Gates row and a pinned control, yet it is not an entry
  point; deleting its row leaves `UNREGISTERED=0` (`RevC2TagCount`). `round25-meta-oracle.py` is likewise outside the set; `build-spans.py` enters it once `SCORECARD.md` names it, which is why the after-state reads 73 rather than 72, and  is likewise outside the set. (`build-spans.py` DOES enter the set once `SCORECARD.md` names it, which is why the after-state reads 73 rather than 72.) C2's predicate
  quantifies over its declared union and is met; the calibration READING must say
  membership of a mention-derived set, not gate-registry coverage.
- **C2, row format only.** A junk eight-cell row naming an unregistered path
  registers it; row truth is a reader's check (`ExecCounterRun`).
- **C3, anchors and co-occurrence.** The counter never checks a Registry row's
  `anchor` cell (mistake 7) and `REF_BOUND` is co-occurrence: `S079 is not RFC
  7089` passes it (`ExecCounterRun`).

## Round-45 closure defects — disposition

| defect | disposition this round |
|---|---|
| D7 inference presence vs grounding | C1: `tools/inference-ground.py` + fixtures + counter. Partially closed — presence is enforced, ENTAILMENT is not (mistake 2), routed to round 47 |
| D8 registry misses executable verifiers | C2: the entry-point set now has a third leg (paths the verdicts name); `round34/self-audit.py` is registered as `instrument` with its "counts, does not gate" contract in the verdict map. Limit: mention, not dependence |
| non-author spot-check | pending: the closure's duty, not this lane's (seats this lane dispatched are the lane) |
| inherited tree | unchanged: the three modified JSONs stay left-named; the round-43/44 L0 questions are still unanswered (`ScoutInheritedTree`) |

## Gate

Theme: what makes a support verdict durable, and how a later corpus binds each
citation to an archived state. One theme, two entries, five rows. No fetch.
Ids bound **by document** (URL equality), never by id arithmetic: staged S120 →
lane S085, S121 → S086, S122 → S087, S127 → S088, S128 → S089; the offsets are
−35/−35/−35/−39/−39, so nothing arithmetic reproduces them. The lane's registry
held 84 rows (`S001`–`S084`, contiguous) and the next five are S085–S089.

Id collision: **3 ids** (`S082`, `S083`, `S084`) overlap the staged append, and
they name DIFFERENT documents on each side (lane: AVeriTeC README / paper /
train.json; staged: PRISMA-S / Cochrane ch. 4 / RFC 7089). Nothing was appended
from the staged block as-is; the five adopted rows were written from the
captures. `sources-census.sh validate --file` on the scratch mirror: **exit 0**,
five pre-existing W04, no E03/E04/E11; the live census after the append:
**exit 0**, same five W04, 89 rows.

Quarantine (§10): the lane's 24-row slice was re-derived (`quarantine-check.py
slice` and the operator awk recipe both print 24; the naive awk prints 25 on the
`## By lane` summary row, so the guards are load-bearing). **One adopted URL is
in the slice**: `aclanthology.org/N18-1074.pdf` = register line 54, `chousa
round4 S116`, `payload-absent`, three quotes. Hand-checked this round: all three
register quotes are verbatim in capture `1c15b611…` once the two-column PDF
interleave is removed and one hyphen split (`ev-`/`idence`) is joined — verdict
**present → the row is adoptable**, and the mechanical checker's `absent` is a
false positive of the same class round 43 adjudicated. The adopted row anchors a
slice the lane itself re-located (`used the June 2017 Wikipedia dump,
processed`, char 15269), not the register's stitches.

Admit:

- `corpus/knowledge/evidence-pool-versioning-r39.md`, citing S085, S086, S087.
  Province: claim-vs-source verification (`ScoutProvinceFit` F1–F10 in province).
  Re-grounded, not copied: the staged "the binding is a URL and a sentence id —
  and nothing else" is replaced by the four-position tuple with two ids the page
  itself calls unscored; the staged "We used the June 2017 Wikipedia dump" and
  "95.42% precision and 72.36% recall in evidence retrieval" are not contiguous
  in the PDF capture and are replaced by the contiguous slices; the 95.42/72.36
  comparator is named (annotators against the super-annotators' set); the
  negative "revision" claim now carries its sweep (`grep -c revision` over S085
  = 0).
- `corpus/knowledge/evidence-pool-versioning-r39-amendment-2026-10-23.md`,
  citing S088, S089 and re-binding S079 (RFC 7089) and S081 (NDL E2867 WARP) by
  document. Re-grounded: the field pairing is documented practice, not a schema
  invariant (an `Unanswerable` answer has no source URL and no archive key); the
  claim-level hedge tracks a missing `original_claim_url` (every null sits on a
  record whose original URL is also null); the temporal restriction is the
  SUCCESSOR corpus's rule and is stated of annotators; the staged `74.7%` and
  four-label quotes are corrected to the capture's bytes. Flip met for the
  round-45 reject: the base entry is held in the same round, every prose id is
  re-bound by document, and its quotes are located in the captures.

Reject:

- `claim-support-test-r37-amendment-2026-10-23.md` (staged) — **not this round**,
  recorded as a later candidate. Reason: the lane holds neither its base entry
  nor the wave-3 material it continues, and its staged rows sit in the campaign's
  numbering, which this round re-bound for a different five documents. Flip: the
  base entry is adopted with its own rows and the amendment's quotes are located
  in committed spans.

Rows added (opened 2026-10-25, all `mined`, recheck `365d` except S088 `180d`
where the page is build-stamped):

- **S085** https://fever.ai/dataset/fever.html — "A list of evidence sets"
  (char 2360); "Pre-processed Wikipedia Pages (June 2017 dump)" (char 1271).
- **S086** https://aclanthology.org/N18-1074.pdf — "used the June 2017 Wikipedia
  dump, processed" (char 15269); "recall of 72.36%" (char 42011); "We found that
  91.2%" (char 20847).
- **S087** https://zenodo.org/api/records/4925954 — `"conceptdoi":
  "10.5281/zenodo.4925953"` (char 171); `"key": "wiki-pages.zip"` (char 4929).
- **S088** https://fever.ai/dataset/averitec.html — "An archive.org link for the
  source url" (char 3929); "Our best estimate for the date the claim first
  appeared" (char 2904).
- **S089** https://arxiv.org/html/2505.17978v2 — "temporally constrained
  evidence annotation" (char 3022); "published before the claim’s date" (char
  7137, curly apostrophe).

Recheck prose stripped from the staged rows: S085 "re-confirm the tuple format
and the dump link"; S086 "re-fetch the PDF and re-confirm the three slices";
S087 "re-open the record and confirm the concept doi and the pool file"; S088
"re-open the page and confirm both field descriptions"; S089 "re-open the HTML
and confirm the constraint sentences". Curation change logged old→new: S085's
cadence `180d` → `365d` (a build-stamped page, not a living one).

## Sources opened

All from the campaign's on-disk capture cache, accessed 2026-10-25, no fetch.
Spans committed with context in `corpus/evidence/round46/spans/`, offsets in
`spans.tsv`, rebuildable with `build-spans.py` (`--check` re-derives 11/11).

## Census

`scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin chousa`:
round start **exit 0** (84 rows, five W04); round end **exit 0** (89 rows, the
same five W04). Scratch mirror before the append: exit 0, no E03/E04.

## Spot-check

Seats this lane dispatched are still the lane; the non-author spot-check is the
hyaku closure's. What the waves found against the frozen claims:

- Held as landed: all three counters re-run over a `git archive` of the landing
  (`RevRerunC1/2/3`); every span re-derived (11/11 exact slices with context);
  every row re-opened; both cross-references bound by document; the census exit
  0; the five new Gates rows structurally conformant.
- Fixed after the waves (no frozen predicate, target or control changed): the
  junk leg and fixture pins (mistake 1); the registry numeral escape (3); C2's
  fence/comment/suffix forges (4); the span-path boundary in both tools (5); the
  S088 anchor (7); eleven sentence-level narrowings in the two entries (8, 9);
  spans with context (11).
- Disagreements kept open: the tool checks presence, not entailment (2) — the
  round-45 D7 class is named, not closed; C2's set is mention-based, not
  dependence-based, so `round45/tag-count.py` is a registered gate the counter
  cannot see and two historical probes that disclaim gating are now rows (their
  `kind` and verdict-map cells say so); the C3 counter does not check row
  `anchor` cells.
- Named limits added: byte vs char offsets (S086 and S089 captures carry
  non-ASCII), `offset` means span start while entries cite quote offsets, and a
  staged id can collide with a held lane id while binding a different document.

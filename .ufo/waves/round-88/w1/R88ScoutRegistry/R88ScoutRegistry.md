# R88ScoutRegistry — C2 registry reconnaissance (round 88, wave 1)

Seat `R88ScoutRegistry`. Leaf member (no subagent dispatch). Read-only reconnaissance of C2's `teaches` leg and the
campaign-package collision, at the freeze revision.

- Base / landed bytes read: `4ea9d008abfd2e09cb51649a42678a78f52ac530` (the freeze commit; there is no separate
  landing commit this round).
- Tree built at: `git -C /home/vgpnk/Projects/shokunin/chousa-shokunin archive 4ea9d008abfd2e09cb51649a42678a78f52ac530 | tar -x -C /fast/scratch/hyaku/chousa-r88/R88ScoutRegistry/tree` → exit 0.
- Scratch: `/fast/scratch/hyaku/chousa-r88/R88ScoutRegistry/` (removed after this report was written).
- All receipts cited below are copied into this folder as `receipt-*.txt`; each names the exact command and its exit code.
- No network was used. No production file, lane git/jj state, sibling repo, `MANIFEST.json`, `considerthese/`, or
  `/home/vgpnk/Projects/shokunin/scripts` was written. No tool was installed or upgraded.
- Confidence scale used below: **high** = measured by a committed instrument or by an independent re-derivation whose
  bytes differ from the counter's; **medium** = measured but dependent on an assumption stated inline.

---

## 0. Baseline: the frozen predicate holds at the freeze revision

```
$ cd /fast/scratch/hyaku/chousa-r88/R88ScoutRegistry/tree
$ python3 -B corpus/evidence/round88/curation-r88.py --root .
SUPERSEDED_LIVE=0 UNENTAILED_TERM=0 MODIFIED_DEF_CITED=1 QUOTES_LOCATED=20/20 Q_FLOORS=search-transparency-reporting-r84.md=13/13 floor13,provenance-recording-r85.md=7/7 floor7 WARRANT_OK=17/17 TEACHES_CHECKED=1 TEACHES_FLAGGED=1 TEACHES_UNRESOLVED=0 LEGS=7/7
TEACHES_FLAGGED S024 terms=publication,modification disposition=superseded by S031
CURATION_R88=PASS
exit 0
```

Every field the frozen predicate names is present and equal to the expected value. `TEACHES_CHECKED=1`,
`TEACHES_FLAGGED=1`, `TEACHES_UNRESOLVED=0`, `LEGS=7/7`. Receipt: `receipt-registry.txt` (my independent
re-derivation) and the run above.

Control battery, five round-87 forgeries, all refused by the r88 counter and accepted by the frozen r87 counter:

```
$ TMPDIR=$W python3 -B tree/corpus/evidence/round88/curation-r88-controls.py --root tree --work $W
OK POSITIVE / A1c-junk-substitute / A1d-truncate / caseG-relabel / F2-rejected-superseder / B1b-padding-qid
FORGERY_REFUSED=5/5 R87_ACCEPTED_FORGERY=5/5
CONTROLS=PASS
exit 0
```
Receipt: `receipt-controls.txt`. Note the control battery prints `FORGERY_REFUSED=5/5` and `R87_ACCEPTED_FORGERY=5/5`;
the frozen claim's K3 names the field `FORGERY_REFUSED=5/5` and the prose names "refuses all five round-87
forgeries" — both are satisfied by this receipt.

**So C2's predicate (K1) is not violated at the freeze revision, and K3 is not violated.** The findings below are
about *how* the `TEACHES` leg reaches its verdict, not about the verdict itself.

---

## (a) The supersession graph — every `supersedes S0NN —` edge with both statuses

Re-derived independently from `corpus/SOURCES.md` at the freeze revision (218 rows, 11 cells each, no malformed rows).
Receipt: `receipt-registry.txt`, `receipt-superseders.txt`, `receipt-edge-completeness.txt`.

| edge | superseder status | target status | mined superseder? |
|---|---|---|---|
| S029 → S019 | mined | queued | yes |
| S030 → S022 | queued | queued | **no** |
| S031 → S024 | mined | queued | yes |
| S032 → S021 | queued | queued | **no** |
| S033 → S020 | mined | queued | yes |
| S073 → S070 | mined | mined | yes |
| S176 → S171 | mined | mined | yes |
| S200 → S196 | mined | mined | yes |
| S201 → S197 | mined | mined | yes |
| S202 → S198 | rejected | rejected | **no** |

`EDGES_TOTAL=10`. Three edges have a **non-mined superseder**: S030→S022, S032→S021, S202→S198.

**Is any of them the disposal edge for the one flagged row? No.** The flagged row is **S024**, and its disposal edge
is **S031 → S024**, where S031 is `mined`. The three non-mined edges target S022, S021 and S198 — none of them is
S024, so no non-mined superseder disposes the flagged row. The disposition the counter prints
(`TEACHES_FLAGGED S024 … disposition=superseded by S031`) is a genuinely mined superseder. **Confidence: high.**

`SUPERSEDED_LIVE=0`: no row is `mined` while its superseder is not — consistent with the edge table, where every
mined target (S070, S171, S196, S197) has a mined superseder.

Edge extraction is complete: all 10 edges are in the `teaches` cell (column 6); four rows *also* carry the phrase in
another column (S073 col 5; S200/S201/S202 col 1) but their `teaches` cell repeats it, so no edge is missed and no
edge is double-counted. Every edge target resolves to an existing row (`EDGES_WITH_MISSING_TARGET=[]`). No row's
`teaches` cell mentions "supersedes" without matching the counter's pattern.

---

## (b) The superseding row's own read — measured, and where it is *not* measured

The claim says the `TEACHES` leg "requires every flagged row to be disposed by a `mined` superseding row whose own
`teaches` reads in its own capture". Two things must therefore be true of the superseding rows: (i) which ones carry a
contrast phrase and a date term, and (ii) whether each such term reads in that row's own capture.

### (b1) Which superseding rows carry a contrast phrase and a date term?

`CONTRAST = ("separate from", "no comparison", "independent of", "distinct from")`;
`DATE_TERMS = ("publication", "published", "modified", "modification", "created", "issued")`.

- Superseding rows carrying a **contrast phrase**: **1 of 10** — **S031** (`no comparison`).
- Superseding rows carrying a **date term**: **0 of 10**.
- Superseding rows carrying **both**: **0 of 10** → `SUPERSEDERS_WITH_BOTH=0`.

Receipt: `receipt-superseders.txt` (per-row teaches cell, contrast phrases, date terms, own capture presence and key).

### (b2) Does each term read in its own capture?

Vacuous as measured, because no superseding row names a date term at all. But the one superseding row that *does*
carry a contrast phrase, S031, is worth reading closely. S031's own capture (key `11d6cc56bb24adfc61eea2b4`,
`corpus/captures/11d6cc56bb24adfc61eea2b4.txt`, 1193 bytes — the Schema.org `lastReviewed` page) contains:

> `Date on which the content on this web page was last reviewed for accuracy and/or completeness.`

S031's teaches cell is `supersedes S024 — lastReviewed records the date a web page was last reviewed for accuracy
and/or completeness; no comparison to other date properties claimed`. Six of its content words are **absent** from its
own capture: `claimed, comparison, other, properties, records, supersedes` — the capture contains no occurrence of
`comparison`, `publication`, `modification`, `claimed`, `properties` or `records` (each `grep -c` = 0).
Receipt: `receipt-s031-ownread.txt`.

### (b3) FINDING — the superseder-own-read clause is dead code; the shipped counter cannot fail it

This is the load-bearing finding of the seat.

The counter has a second loop, `teaches_sup_unresolved`, intended to check the superseding row's own `teaches`
against its own capture. **It never executes for any row.** The reason is a case mismatch: the loop matches
`re.match(r"supersedes (S\d{3,}) —", tl)` against `tl = cells[6].lower()`, and the pattern's `S` is uppercase, so a
lowercased cell (`supersedes s024 —`) never matches. The *first* loop, at line 158, matches against the **raw** cell
and therefore does find all 10 edges — which is why the mined-superseder disposal works while the superseder-own-read
check does not.

Instrumented proof (a copy of the counter with a probe added; both gates run over all 218 rows):

```
$ python3 -B exp/probe-counter.py --root tree
PROBE_SUPERSEDER_GATE rows=218 raw_cell_matches=10 lowercased_cell_matches=0 case_insensitive_matches=10
PROBE_RAW_HITS=['S029','S030','S031','S032','S033','S073','S176','S200','S201','S202']
PROBE_LOWER_HITS=[]
```
Receipt: `receipt-supclause-instrumented.txt`, `receipt-probe-run.txt`.

Behavioural proof without instrumentation. Take a tree where a superseding row's own `teaches` names date terms its
own capture cannot read, and where that row is disposed by a *third* mined row (so the main `teaches` loop cannot
flag it). Tree `exp/t3`: S031's teaches gains `publication or modification`; a new mined row S219 supersedes S031.

Shipped counter:
```
$ python3 -B tree/corpus/evidence/round88/curation-r88.py --root exp/t3
SUPERSEDED_LIVE=0 … TEACHES_CHECKED=2 TEACHES_FLAGGED=2 TEACHES_UNRESOLVED=0 LEGS=7/7
TEACHES_FLAGGED S024 terms=publication,modification disposition=superseded by S031
TEACHES_FLAGGED S031 terms=publication,modification disposition=superseded by S219
CURATION_R88=PASS
exit 0
```

Same tree, counter with the single-character fix (`re.I` on that one `re.match`):
```
$ python3 -B exp/casefixed-counter.py --root exp/t3
… TEACHES_CHECKED=2 TEACHES_FLAGGED=2 TEACHES_UNRESOLVED=0 LEGS=6/7
TEACHES_SUP_UNRESOLVED S031 terms=publication,modification
LEG_FAIL TEACHES checked=2 flagged=2 unresolved=0 sup_unresolved=1
CURATION_R88=FAIL
exit 1
```

The shipped counter **accepts** a tree in which a superseding row's own `teaches` names date terms that its own
capture does not read; the fixed counter **refuses** the same tree. The differential is exactly the dead clause.
Receipts: `receipt-supclause-proof.txt` (regex-level proof), `receipt-supclause-dead.txt`.

**Scope of the finding.** This does **not** change the verdict on the landing tree: on the base tree the case-fixed
counter also prints `CURATION_R88=PASS`, `LEGS=7/7` (`receipt-supclause-instrumented.txt`, second run) because S031
names no date term on the base tree, so the clause has nothing to check even when it fires. The finding is therefore
about **coverage of the claim's wording, not about a wrong base-tree verdict**: the claim states the leg requires the
superseding row's own `teaches` to read in its own capture, and the shipped counter does not enforce that requirement
on any tree. It is the *named* requirement in the claim sentence and in `plans/round-88.md` §5 ("also requires the
superseding row's own `teaches` to read in its own capture"), so a reviewer should treat it as load-bearing prose that
the instrument does not currently back.

**Confidence: high** — proven at the regex level, by instrumentation over all 218 rows, and by a two-sided behavioural
differential on a tree where the two counters disagree.

**Not claimed:** that this falsifies C2's predicate as frozen. The predicate's printed fields are met (K1 does not
fire), and K3/K4 as written are not violated — the leg does flag exactly one row (S024) and does dispose it by a mined
superseder (S031), so the K4 "dead detector" test (a leg satisfied by flagging nothing) is **not** met either. This is a
wording-coverage finding for the wave, and it is the honest report.

---

## (c) The qid-set pin and the token floor against the registry

Both routed entries re-derived independently (own parser, own capture lookup), compared against the counter's frozen
`QID_SETS` and `MIN_TOKENS = 7`. Receipts: `receipt-registry.txt`, `receipt-k2-verbatim.txt`.

### (c1) qid-set pin — exact match on both entries

| entry | carried qids | pinned qids | set equal? | missing | extra |
|---|---|---|---|---|---|
| `search-transparency-reporting-r84.md` | Q1–Q13 (13) | Q1–Q13 (13) | **yes** | none | none |
| `provenance-recording-r85.md` | Q1–Q7 (7) | Q1–Q7 (7) | **yes** | none | none |

The pinned set for each routed entry is **exactly** the set of qids the entry carries at `4ea9d008`. The pin is
satisfied on its own terms: a caseG-shaped relabelling (`Q10` deleted, a duplicate of `Q13` re-labelled `Q14`) changes
the carried set and therefore breaks the equality. **Confidence: high.**

### (c2) Token floor — 20/20 located quotes, minimum exactly 7, none below floor

Per-quote token counts (whitespace-normalised, as the counter counts):

- r84: Q1=17, Q2=9, Q3=17, Q4=16, Q5=15, Q6=13, Q7=15, Q8=18, Q9=10, Q10=24, Q11=9, Q12=9, **Q13=7**
- r85: Q1=12, Q2=10, Q3=11, Q4=19, Q5=20, Q6=17, Q7=16

`TOTAL_LOCATED=20`, `MIN_TOKEN_COUNT=7` (r84 `Q13`, *"Date on which the resource was changed."*), and
`BELOW_FLOOR_ANY=[]` — no located quote is under `MIN_TOKENS = 7`. The floor sits exactly on the measured minimum, so
it is the measured value rather than a round number, and the A1c/A1d one-word substitutions fall below it. **Confidence:
high.**

### (c3) Warrant leg — all 17 rows resolve and share a distinctive term

Re-derived per decision-table row: every named qid resolves to a located quote of that entry, and every one shares a
distinctive (non-stopword, ≥5 chars) word with the row's Do/Never cells. `WARRANT_OK=17/17` — 11 rows in r84 and 6
in r85, matching the counter's `17/17`. The repaired row reads `Q1 (S215)` and shares
`{entities, property, provenance}`; r85 `Q3`'s quote (*"then we can say that the bar chart prov:wasDerivedFrom the
dataset."*) shares no distinctive term with that row, confirming the freeze repair was necessary under the every-qid
rule. **Confidence: high.**

### (c4) K2 verbatim check — 20/20 quotes are verbatim in their own row's capture

Stricter than the counter's own lookup: for each of the 20 quote rows, the quote is required to appear in the capture
of **the registry row's own URL** (first URL in that row's `source` cell that has a capture), not merely in some
capture.
`QUOTES_TOTAL=20 LOCATED_VERBATIM_IN_OWN_URL_CAPTURE=20 BAD=0`. **K2 does not fire. Confidence: high.**
Receipt: `receipt-k2-verbatim.txt`.

---

## (d) Collision check against the campaign package

`/home/vgpnk/Projects/shokuknow/merge/chousa/SOURCES.append.md` **exists** (148,997 bytes, staged
2026-10-24, `<!-- corpus-expansion-1 :: staged rows for lane chousa -->`). It was read **read-only**; nothing in
`shokuknow` was written. Its `MERGE-REPORT.md` states verbatim: *"Staged by `corpus-expansion-1`. **Nothing was
written into the lane repo.**"* — the L1's question of whether it was assimilated this round is answered separately;
what follows is only the measured collision.

### (d1) The census extractor over the lane registry — clean

```
$ bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh census --file tree/corpus/SOURCES.md
file rows 218 / tier.A 139 / tier.B 59 / tier.C 20 / tier.invalid 0
FLEET status.mined 182 / status.queued 12 / status.rejected 24 / status.invalid 0 / missing 0
exit 0
$ bash … validate --file tree/corpus/SOURCES.md
file W04 S051 duplicate url www.w3.org/TR/2017/REC-html52-20171214/syntax.html across scopes
file W04 S053 duplicate url docs.python.org/3/library/socket.html across scopes
file W04 S073 duplicate url www.gnu.org/software/coreutils/manual/coreutils.html across scopes
file W04 S074 duplicate url docs.python.org/3/library/hashlib.html across scopes
file W04 S075 duplicate url www.gnu.org/software/coreutils/manual/coreutils.html across scopes
file ok …/corpus/SOURCES.md
exit 0
```
The five W04 warnings are byte-identical to the frozen `corpus/evidence/round88/census-start.txt` receipt
(also 5 W04 lines, same ids, same URLs) — no new census finding on the lane registry. Receipts:
`receipt-census-lane.txt`, `receipt-validate-lane.txt`.

### (d2) The census extractor over the campaign file — reads **0 rows**, and validate raises E12 on all 114

```
$ bash … census --file /home/vgpnk/Projects/shokuknow/merge/chousa/SOURCES.append.md
file rows 0
FLEET rows 0
exit 0
$ bash … validate --file …/SOURCES.append.md
114 × E12   (row-shaped source outside the ## Registry section)
exit 1
```
The file has **no `## Registry` heading** (`grep -c '## Registry'` = 0), and the extractor only counts rows inside that
section (`sources-census.sh:547,611`). So the file is invisible to the extractor as a registry: `rows=0`, and
validate reports 114 × E12. Receipts: `receipt-census-campaign.txt`, `receipt-census-campaign-validate.txt`.

### (d3) The id sets, and the collision count

- Lane registry at `4ea9d008`: **218 rows, ids S001–S218**, all unique, no duplicates.
- Campaign package: **114 rows, ids S082–S195**; 113 well-formed (11 cells) + **S097 malformed at 13 fields**
  (an embedded `|` splits `SUPORTS|REFUTES|NOT ENOUGH INFO` across three cells) → E01.
- **ID intersection = 113 of 113 well-formed campaign ids (100%).** `CAMP_ONLY_IDS=0` — the campaign's id space is
  entirely contained in the lane's.

Breaking the 113 down by what the lane already holds at that id:

| class | count | meaning |
|---|---|---|
| A — same id, same URL | **4** (S100, S101, S102, S103) | harmless duplicate |
| B — same id, **different** source; URL also in the lane under another id | **57** | hard id collision + duplicate content |
| C — same id, **different** source; URL not in the lane | **52** | hard id collision, new content |
| D — id not in the lane | **0** | — |

**Measured collision count: 113 of 113 campaign ids (100%) collide with existing lane ids; of those, 109 are *hard*
collisions (the lane's row S### already names a different source), and 4 are benign same-id/same-URL duplicates.**
At URL level, 61 of 113 campaign rows (54.0%) name a URL the lane already holds. Every campaign id is in the range
S082–S195, which the lane has since filled with rows opened 2026-10-25 → 2026-11-04, while the campaign rows were
opened 2026-10-23/24 — the campaign was staged against an 81-row registry (its own `MERGE-REPORT.md`: *"lane registry
currently holds **81** rows; first staged id is **S082**"*), and the lane has since grown to 218.
Receipts: `receipt-campaign-authoritative.txt`, `receipt-campaign-reconciled.txt`, `receipt-campaign-idmap.txt`.

### (d4) What the extractor says if the rows were appended

Appending the 114 campaign rows into the lane's `## Registry` section and re-running `validate`:

```
$ bash … validate --file exp/append/corpus/SOURCES.md
E03 duplicate id            × 113
E09 invalid recheck         × 113
E01 fields=13               × 1    (S097)
E04 duplicate url in scope  × 10
E11 missing used-by         × 321
W04 duplicate url across scopes × 59 ; W01 tierC mined used-by × 7
exit 1
```
Receipt: `receipt-census-appended.txt`.

Two structural incompatibilities beyond the id collision, both measured:

- **E09 × 113**: every campaign row's `recheck` cell is `NNd — <prose>`, e.g. `180d — re-open the chapter-04 URL and
  confirm section 4.5 still reads …`. The lane's own convention is a bare `180d` (109 rows) or the symbolic
  `on-release` (108 rows); the extractor's E09 accepts only ISO date, `NNd`, or a symbolic cadence. So all 113
  campaign rows are E09-invalid under the lane's own schema.
- **E11 × 321**: 121 `used-by` path mentions across the campaign rows, of which **64** do not exist in the lane tree
  (the lane already holds 22 of the campaign's 55 knowledge files, but under different names/versions — 22 present, 33
  absent, and **0 of the 22 byte-identical**).

Receipts: `receipt-e09-e11-causes.txt`, `receipt-knowledge-absorption.txt`.

---

## Summary of findings, by confidence

**High confidence**

1. **The superseder-own-read clause of the `TEACHES` leg is dead code.** `curation-r88.py:250` matches
   `supersedes (S\d{3,}) —` against a lowercased cell, so it never matches; `teaches_sup_unresolved` is always
   empty. Proven by instrumentation (10 raw-cell matches, 0 lowercased matches over 218 rows) and by a two-sided
   differential: on a tree where a superseding row's own `teaches` names date terms its own capture cannot read, the
   shipped counter prints `CURATION_R88=PASS` (exit 0) while the one-character-fixed counter prints
   `LEG_FAIL TEACHES … sup_unresolved=1` / `CURATION_R88=FAIL` (exit 1). **The claim's sentence requires this
   condition; the instrument does not enforce it on any tree.** The base-tree verdict is unaffected (the fixed
   counter also passes the base tree), so C2's printed predicate and K3/K4 are unaffected — this is a
   wording-coverage finding for the wave, not a verdict falsification.
   Receipts: `receipt-supclause-instrumented.txt`, `receipt-supclause-proof.txt`, `receipt-supclause-dead.txt`,
   `receipt-probe-run.txt`.

2. **The supersession graph is sound and the disposal edge is genuinely mined.** 10 edges; the only flagged row is
   S024; its disposal edge is S031 → S024 with S031 `mined`; the three non-mined-superseder edges (S030→S022,
   S032→S021, S202→S198) target other rows. `SUPERSEDED_LIVE=0`. Receipts: `receipt-registry.txt`,
   `receipt-superseders.txt`, `receipt-edge-completeness.txt`.

3. **The qid-set pin and the token floor are exactly as claimed.** Both entries' carried qid sets equal the pinned
   sets; 20/20 quotes located; the measured minimum is exactly 7 tokens (r84 `Q13`), no quote below the floor.
   Receipts: `receipt-registry.txt`, `receipt-k2-verbatim.txt`.

4. **K2 holds on a stricter reading than the counter's own.** 20/20 quotes are verbatim in the capture of their own
   registry row's URL. Receipt: `receipt-k2-verbatim.txt`.

5. **Campaign package collision = 113 of 113 well-formed campaign ids (100%).** 109 are hard id collisions (the
   lane's row at that id already names a different source), 4 are benign same-id/same-URL. Zero campaign-only ids.
   The package also has one malformed row (S097, 13 fields), all 113 rows are E09-invalid on `recheck` under the
   lane's own schema, and the file is invisible to the extractor (`rows=0`, no `## Registry` heading; validate =
   114 × E12). 61 of 113 rows name a URL the lane already holds; 64 of 121 `used-by` paths are missing from the lane
   tree; 22 of 55 campaign knowledge files already exist in the lane, none byte-identical.
   Receipts: `receipt-campaign-authoritative.txt`, `receipt-campaign-reconciled.txt`,
   `receipt-census-appended.txt`, `receipt-e09-e11-causes.txt`, `receipt-knowledge-absorption.txt`.

**Medium confidence**

6. The claim's K4 "the leg requires at least one flagged row and a named disposition for it, and the disposition's
   superseder is `mined`" is **met** on the base tree (S024 flagged, disposed by mined S031) — so the dead clause in
   finding 1 does not make the leg a no-op detector at the freeze revision. Medium because the reading of "a named
   disposition" against the printed line is a judgement.

## Remaining unknowns

- Whether `merge/chousa/` was assimilated this round is the L1's call (the package's own report says nothing was
  written; the lane's 218 rows are all dated after the package's 2026-10-23/24 opened dates, which is consistent with
  independent growth rather than assimilation). I report the measured collision count only, as instructed.
- Whether the campaign's 52 new-content rows (class C) should be re-numbered into the lane's free id space
  (S219–S270) or dropped is a curation decision, out of this seat's scope.
- I did not test whether the dead superseder clause can be reached by any *other* mutation shape than the one in
  finding 1; the differential in finding 1 is sufficient to establish the clause's unreachability, which is the
  stronger property.

## Limits / touched surface

- Files written: this report and 25 `receipt-*.txt` files plus one copy of `scout_registry.py`, all inside
  `/home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-88/w1/R88ScoutRegistry/`. Nothing else.
- Scratch under `/fast/scratch/hyaku/chousa-r88/R88ScoutRegistry/` (tree, `exp/` mutation fixtures, control work
  dir) was deleted before this report was written.
- The only mutation fixtures built were inside scratch copies of the tree (`exp/t1`, `exp/t2`, `exp/t3`,
  `exp/append`) and two patched counter copies (`exp/probe-counter.py`, `exp/casefixed-counter.py`). The committed
  counter at `corpus/evidence/round88/curation-r88.py` was not modified; the patched copies differ from it by one
  `re.I` flag and one added probe respectively.
- No network access; no `pacman`, `uv tool`, `npx` or PATH-directory install; no host sysctl, service, or sudo.
- No git/jj mutation of any lane, fixture repo, or sibling repo; the archive was read via `git archive` only.
- LSP: no language server for this tree answered a file, so the Python sources were located and read by line range
  (`curation-r88.py:3-299`, `curation-r88-controls.py:36-162`). This is recorded as a tooling limitation; the
  behavioural evidence above does not depend on it.

VERDICT: R88ScoutRegistry C2 fired — the frozen predicate and all five forgery refusals hold at 4ea9d008, but the claim's stated superseder-own-read requirement is dead code in `curation-r88.py:250` (case-mismatched regex over a lowercased cell), so the shipped counter accepts a tree a one-character-fixed counter refuses.
VERDICT: R88ScoutRegistry C2 n/a — the campaign-package collision is measured at 113/113 campaign ids colliding (109 hard) and reported to the L1 without a verdict, since assimilation is the L1's call.

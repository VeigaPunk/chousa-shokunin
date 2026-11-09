# R96ConnectorSiblings — cross-lane pattern scan (read-only)

Seat: connector, round 96, lane chousa. Attacked tree: `2db151c5ea0883de0b9dc8d95c6fac1755e1056a`
(shared clone at `/fast/scratch/hyaku/chousa-r96/R96ConnectorSiblings/repo`, never repacked).
Siblings searched: the 20 `*-shokunin` repos listed by
`ls -d /home/vgpnk/Projects/shokunin/*-shokunin | grep -v '/chousa-shokunin$'` (`/home/vgpnk/Projects/shokunin`), chousa excluded.
No sibling repo was written. Receipts: every `R96ConnectorSiblings-*.txt` in this directory.

`OVERLAPS=2` — one cross-lane overlap per pattern; neither duplicates C2's subject matter, and C1's mechanism is
pre-existing fleet craft rather than a chousa invention.

## Pattern 1 — knowledge entries / SOURCES rows on search peer review, PRESS, deduplication

`OVERLAPS=1` (convention, not subject matter).

- **Subject matter: 0 hits, 20/20 siblings.** `grep -rlnE 'Peer Review of Electronic Search|PRISMA-S|PRESS (EBC|2015|[Ee]vidence)|PRESS guideline'`
  over `corpus/knowledge/*.md`, `corpus/SOURCES.md`, `SKILL.md`, excluding `.ufo/`, `reports/`, `node_modules/`
  → `0` files. Widened to `grep -rli PRISMA` over the same three surfaces → `0` files. No sibling holds PRESS,
  PRISMA-S, or a search-deduplication row. C2's subject matter is genuinely unheld elsewhere.
  (`R96ConnectorSiblings-scan-p1.txt`.)
- **Convention overlap (kaidoku).** `kaidoku-shokunin/corpus/lessons/round-13.md:54` documents a `corpus/SOURCES.md`
  *search note* that "records its exact query, first-10-result boundary, **deduplicated screening counts**, exclusions,
  and stop rationale", instantiated at `corpus/SOURCES.md:294` ("screened 5 deduplicated work/index records …
  included 1, excluded 4"). That is the same accounting shape as C2's `## Searches` + PRISMA-S item-16 row, in a
  different domain (RE literature, human prose, not a machine-re-runnable table). Different mechanism, adjacent convention.

## Pattern 2 — in-memory `--selftest` over the tool's own decision function, scored by a mutant battery

`OVERLAPS=1` (same mechanism, established).

- **`--selftest` is fleet standard, not new.** Tools carrying the flag in their own `tools/`: kama 77, kotodama 38,
  mado 31, mori 56, souji 17, tameshi 57, tsukuroi 109. SKILL.md registry lines mentioning `--selftest`: 17 of 20
  siblings register at least one (tsukuroi 1126, kaidoku 262, kake 134, mori 125, mado 124, kengaku 122, tameshi 113,
  tabi 102, kama 97, kotoba 74, kotodama 71, souji 66, kumitate 64, kagi 55, revenger 51, kasegi 37, lore 7).
  Chousa itself had 5 before this round (`git show bbf64970:tools/*.py` → `assimilate-rows.py`, `claims-audit-v2.py`,
  `claims-audit.py`, `freeze-check.py`, `lane-preflight.py`); `search-rerun.py` is the 6th.
  (`R96ConnectorSiblings-scan-p2.txt`.)
- **The mechanism is tameshi's declared domain.** `tameshi-shokunin/SKILL.md:3` — "Verification-fixture craft for
  'hermetic suites', **'mutation testing'**, and 'gate fixtures'". Its SKILL.md:74 already reports the exact shape
  C1 installs: "`surface-census.sh` 16-case selftest vs 10 single-edit mutants → 8/10". Its knowledge corpus holds
  the governing rules for both pre-freeze fixes chousa made locally: `witness-equivalence-rule.md`,
  `r43-survivor-resolution-rule.md` (the `m34` equivalent-mutant removal, plan P1), `oracle-anchored-survivors.md`
  and `guard-kill-closure.md` (the three stand-in oracles), `counter-population-binding.md`, `mutation-score-semantics.md`.
  tsukuroi runs the largest battery apparatus (`MutGate/`, `MutBattery/`, `ReviewBattery/` across rounds 84–100).

## Findings

### F1 — C1 predicates reproduce exactly; "same `evaluate`" is literally true. **No falsifier.**

```
python3 -B tools/search-rerun.py --selftest
  → SEARCH_RERUN_SELFTEST: PASS cases=32/32                                     exit=0
python3 -B corpus/evidence/round96/selftest-controls-r96.py --root . --work <scratch> --no-regression
  → POSITIVE=1/1 DO_NOTHING_REFUSED=1/1 MUTANTS_KILLED=23/23 ORACLES_REJECTED=3/3 NO_WRITE=1/1 CASES=32
  → SELFTEST_CONTROLS=PASS                                                      exit=0
grep -c '^| `search-rerun` (r96 re-registration' SKILL.md  → 1  (row at SKILL.md:180, kind cell `gate`)
```
Receipts `R96ConnectorSiblings-c1-selftest.txt`, `-c1-battery.txt`.
The case split is the claimed 14/8/10 (`p01..p14`, `m01..m08`, `j01..j10`). The shared-decision claim holds
literally: `evaluate` is defined at `tools/search-rerun.py:353`, called by `verify` at `:399` and by the selftest's
judgement helper at `:490` and `:511`; the judgement cases build their rows through `parse_text` (`:475`), the same
parser `verify` uses, so not only the decision code but the row shape is shared.
Each of the 23 mutants is applied one site at a time and each prints `FAIL` (battery lines
`CASE mutant m… rc=1 KILLED failed=…`).
*Not checked by me:* the `--no-regression` leg (K5) and the round-95 tools; the 10-minute default battery was not
re-run — I report only the groups I exercised.

### F2 — C2 numbers reproduce, including the Q4 digest, re-derived with GNU grep at base. **No falsifier.**

```
# independent re-run, not the lane's tool:
git -C <clone> archive bbf64970 corpus/captures | tar -x -C <scratch>   # 91 captures
/usr/bin/grep -l -F/-P -e <expr> corpus/captures/*.txt | LC_ALL=C sort
  Q1=2  Q2=2  Q3=3  Q4=4  Q5=1  Q6=0  Q7=3  Q8=0
  Q4 digest = 075e02644f9c115cab201076e652ae646fc0fe85331c6f79943cc1e47aff3500   (entry: sha256:075e02644f9c115c…)
```
Receipt `R96ConnectorSiblings-f2-searches.txt`. GNU grep 3.12-modified, `--engine fixed` = `-F`, `regex` = `-P`.
Structural counts: 31 `GATE-RECORD` lines = 30 with `quote=` + 1 `decision=reject` (`curl_rc=22 http=403`, the
PRESS guideline); 30 Located-quotes rows equal to the 30 gate-record quotes, same order, one-to-one; 8 decision rows.
Receipt `R96ConnectorSiblings-c2-structure.txt`. Tiers: S223 = B, S224 = A; S224's capture is byte-identical to S222's
(`sha256 86f1aacd…`), and `refetch.tsv` carries a real second 200 for S224 at `2026-11-09T00:43:50Z` — so the
"re-opened under a second scope" wording matches the record. Both scope cells are supported by the opened bytes.
Receipts `-c2-counting.txt`, `-c2-scope.txt`, `-c2-battery.txt` (`ENTRY_CONTROLS=PASS`, exit 0).

### F3 — **Headline: the entry's declared sentence group `L24–L25` joins a RIGHT-column fragment to a LEFT-column one.**

The entry states (`corpus/knowledge/search-peer-review-dedup-r96.md:24`): "Consecutive fragments (L4-L6, L7-L8,
L9-L10, L11-L13, L14-L16, L17-L18, L19-L23, **L24-L25**, L26-L29) are read as one sentence from the text form's line
order, not located as one string."

Measured on `corpus/captures/e94691f583d644da14661ec1.txt` (split at each line's largest whitespace gap):

```
168: LEFT=[forum. A guideline statement was published including an]   RIGHT=[Survey respondents and forum participants recommended]
169: LEFT=[assessment form, guidance on its use and recommendations]  RIGHT=[that peer review should occur after the MEDLINE search]   ← L24
171: LEFT=[LIGHTNING TALKS / PRÉSENTATIONS ÉCLAIR]                    RIGHT=[99]                                                        ← page footer
173: LEFT=[has been developed but before other database searches are] RIGHT=[2015 Guideline Statement (http://www.sciencedirect.com/]  ← L25
```

`L24` is the right half of line 169; `L25` is the left half of line 173. They are four lines apart and in different
columns. The sentence is therefore **not** "read from line order": the group is a cross-column join, which is exactly
what the frozen claim's own kill rule K3 names ("a quote located only by joining text across columns"). The receiving
row is decision row 3's Do cell ("after the MEDLINE search has been developed and before the other database searches
are developed"). Receipt `R96ConnectorSiblings-f5-columns.txt`.

Scope of the finding, stated honestly: each *fragment* is genuinely locatable alone, and the reconstruction is
probably the document's real sentence — the left column is ungrammatical at exactly that seam
(`:169` ends "…recommendations", `:173` resumes "has been developed…", and `L24`'s words are the missing clause).
What is false is the **entry's description of its own method**, and with it any reviewer's ability to reproduce the
grouping from "line order". The other eight groups are same-column (L4–L8 RIGHT, L9–L18 RIGHT, L19–L23 RIGHT,
L26–L29 LEFT, L30 RIGHT), so this is a single-site defect, not a systemic one.

### F4 — `gate-records` cannot see F3: it matches normalized *whole* capture text, not a line.

`tools/gate-records.py:243-245` — `text = norm(fh.read())` … `if not quote.strip() or norm(quote) not in text:` and
`norm` (`:92-94`) is `" ".join(s.split())`, i.e. newline-collapsing. The `url/admit` form therefore accepts a quote
that spans line or column boundaries; only the `rev` form has a per-line rule (`:44` `LINE  rev form: … does not
occur in that one line`). Consequence: the entry's "every quote below is located within one column line" and the
claim's K3 are **unenforced by the instrument that scores them**. Currently they happen to hold
(30/30 quotes are single raw-line substrings, 0 failures), so this is an instrument gap, not a live falsehood —
but it is an *unlisted* limit. Receipt `R96ConnectorSiblings-f3-quote-locator.txt`.

### F5 — Decision row 1's Lane cell names a record field the gated schema forbids.

Cell (`:66`): "a chousa search record says which seat or person reviewed the expression before it ran, or that nobody
did". The only search-record format the lane gates on is fixed:
`HEADER = ["id","engine","where","expression","rev","searched","hits","hit_set"]` (`tools/search-rerun.py:90`) with
strict equality at `:162`. Witness — splice a `reviewer` column into the entry's own `## Searches` and run the gate:

```
SEARCH_RERUN_ERROR HEADER columns ['id','engine','where','expression','rev','searched','hits','hit_set','reviewer']
  != ['id','engine','where','expression','rev','searched','hits','hit_set']
exit=2
```

Receipt `R96ConnectorSiblings-f4-schema.txt`. So the entry's own 8 searches cannot record who reviewed them, and the
row describing that capability describes a field no instrument accepts. The claim's wording survives this ("every
Lane cell is filled") — which is the point: `filled` is the weakest check in the sentence and it passes on a cell that
cannot be executed. Six other Lane cells do map onto implemented instruments (per-source counts = item 15, sets,
digests), so this is again a single site.

## What chousa should route but not absorb

1. **Mutant-battery design → tameshi.** C1's equivalence judgement (`m34`, plan P1) and its oracle set are instances
   of rules tameshi already holds (`witness-equivalence-rule.md`, `r43-survivor-resolution-rule.md`,
   `oracle-anchored-survivors.md`, `guard-kill-closure.md`, `counter-population-binding.md`). chousa should cite those
   rather than carry its own equivalence doctrine; it should not absorb mutation methodology as a chousa competence.
2. **Search-record review attribution → its own tool, not a prose cell.** Either add a `reviewer` field to
   `search-rerun.py` (with a battery mutant and a self-test case) or narrow row 1's Lane cell to the wave-report
   instrument that exists today. Do not leave a decision row pointing at a field the parser refuses.
3. **Standing per-column check → the r95 entry's rule, applied backwards.** The lane's capture corpus is
   `pdftotext -layout` two-column throughout; a per-line (or per-column) quote check would have caught F3 at authoring
   time. That belongs in `gate-records`' `url/admit` form, not in another prose limit.

## Bounded proposed move (one)

**Narrow decision row 1's Lane cell to an instrument that exists, and add the missing limit.** Concretely: replace
"a chousa search record says which seat or person reviewed the expression before it ran, or that nobody did" with a
statement true of the current format (e.g. the round's review seat names the reviewer in its wave report; the record
schema has no reviewer field, `tools/search-rerun.py:90`), and add a named limit that the `url/admit` quote check is
over normalized whole text, so per-column-line location is asserted, not enforced.

- *Affected axes*: C2 depth (a row and a limit stop asserting more than their instruments) — improves.
  C1 operability — untouched (no tool change, no new case, battery and selftest unaffected).
  Contract/substrate — untouched (wording only; 8 rows, 30 quotes, 31 records unchanged).
- *Risks*: a reviewer could read the narrowing as content loss; it is not, because the claim sentence only requires
  Lane cells be filled and the Do cell (the warranted part) is unchanged. Adding the limit slightly lengthens the
  entry; it does not change any count `gate-records` checks.
- *Verification*: `gate-records.py verify` must still print `records=31 ok=31 fail=0`;
  `entry-controls-r96.py` must still print `WARRANT_TERMS=8/8 LANE_FILLED=8/8 … ENTRY_CONTROLS=PASS`;
  `search-rerun.py verify` must still print `rev_match=8/8` `SEARCH_RERUN: CLEAN`.

## Not checked / limits of this seat

- No network: `refetch.tsv` was read, never re-run; the S224 200 at `2026-11-09T00:43:50Z` was not re-fetched.
- C1's `--no-regression` leg and the round-95 instruments were not exercised; only the groups above.
- The three stand-in oracles' *implementations* were not read, only the battery's verdict lines.
- Paraphrase fidelity of the 8 decision rows is the wave reviewer's item (claims.md C2 limit (a)); I checked
  warrants, counts, columns and scope cells, not that every Do cell is the best paraphrase.
- No tool was installed or upgraded this round.

VERDICT: R96ConnectorSiblings C1 held — all three predicates reproduce at F (selftest 32/32 exit 0; battery 23/23 mutants, 3/3 oracles, NO_WRITE ok, exit 0; gate row count 1, kind `gate`) and the "same `evaluate`" claim is literally true (`:353` called by `:399` and `:490`/`:511`), though the mechanism is pre-existing tameshi-owned fleet craft rather than new.
VERDICT: R96ConnectorSiblings C2 fired — the entry's stated quoting method is false for its own `L24-L25` group ("read … from the text form's line order" joins a RIGHT-column fragment at line 169 to a LEFT-column fragment at line 173, four lines and one column apart), the frozen kill rule K3 names exactly that move, and `gate-records` cannot detect it because `url/admit` matches normalized whole text; separately, decision row 1's Lane cell names a `reviewer` field the fixed 8-column search-record schema refuses with `SEARCH_RERUN_ERROR HEADER` exit 2.

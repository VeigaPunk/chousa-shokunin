# R89ScoutRegistry — registry reconnaissance at the round-89 freeze

Seat: `R89ScoutRegistry` (leaf member — no subagents dispatched, no `agent://all`, no lane/fleet git or jj mutation, no commits or pushes).
Lane root: `/home/vgpnk/Projects/shokunin/chousa-shokunin`.
Subject revision: freeze `ac0a0892c15de11fb28d3208f2b287687c00477e` (there is no separate landing commit; the freeze carries both counters, their control batteries, the receipt driver and the pins). Base: `f8fa55ec94cb34e7b572a9d87d7f62d88bc80bf8`.
Scratch (every tree, work dir and fixture): `/fast/scratch/hyaku/chousa-r89/R89ScoutRegistry/` — deleted before yield.
Every receipt cited below is copied into this seat's output folder: `.ufo/waves/round-89/w1/R89ScoutRegistry/receipts/`.
No tool was installed or upgraded this round (nothing was needed — every check read committed bytes with the system `python3`/`bash`/`git`), so the tooling-authorization record for this seat is **empty**.

Read-only guarantee: no network call was made (a GET is a finding — none was made); no file under `/home/vgpnk/Projects/shokunin/scripts`, `/home/vgpnk/Projects/shokunin/.ufo/state`, `MANIFEST.json`, `considerthese/`, or any sibling repo was read-modified or written. The campaign repo `/home/vgpnk/Projects/shokuknow` was **read only** — nothing was adopted, edited or staged there.

---

## Summary of findings

| # | Item | Severity | One line |
|---|---|---|---|
| F1 | (a) supersession graph | **none (clean)** | 14 `supersedes S0NN —` occurrences over 10 distinct superseder rows; the counter's teaches-column matcher (`re.match`, anchored at position 0) finds exactly the same 10 — no edge is missed, and the 4 duplicate occurrences (S073 anchor cell, S200/S201/S202 source cells) are re-mentions of the same edges, not extra edges. |
| F2 | (a) non-mined superseders | **none (clean)** | 3 non-mined superseders: S030→S022 (`queued`), S032→S021 (`queued`), S202→S198 (`rejected`). None of the three targets is `mined`, so `SUPERSEDED_LIVE=0` is correct — no target is live while its superseder is unadopted. |
| F3 | (a) disposal edge for the flagged row | **confirmed** | The flagged row is **S024** (the only row with a contrast phrase + a date term in `teaches`). Its disposal edge is **S031→S024**, and S031 is `mined` — so the flagged row is genuinely disposed, and `TEACHES_UNRESOLVED=0` follows. |
| F4 | (b) `SUP_CLAUSE_CHECKED=0` | **confirmed, independently** | Re-derived with my own script: **0** superseding rows carry a contrast phrase **and** a date term, over all 11 cells of all 10 superseder rows (not just the teaches cell). The clause is vacuous on the real registry, exactly as the claim's named limit 4 states. |
| F5 | (c) registry diff | **clean — exactly two cells** | `git diff f8fa55ec ac0a0892 -- corpus/SOURCES.md` = 2 insertions / 2 deletions; a cell-level parse of both revisions finds exactly **2 changed cells**, both in the `used-by` column (S216, S218). All 221 prose (non-table) lines are byte-identical; row count 218 → 218; no id added or removed. |
| F6 | (d) campaign collision | **finding (collision = 114/114)** | `/home/vgpnk/Projects/shokuknow/merge/chousa/SOURCES.append.md` **exists** and holds 114 rows, ids **S082–S195** contiguous. Every one of the 114 ids **collides** with an existing lane registry row (S001–S218). The two files' rows with the same id are **not** the same rows (0 identical, 114 differing) — the campaign staged against an 81-row registry ("lane registry currently holds **81** rows", `first_id = S082`); the lane has since grown to 218 rows and reused that id space. Appending the package as-is would produce **113 × E03 duplicate-id** plus **1 × E01 malformed row**. |
| F7 | (e) census | **clean — 218 → 218, same five W04** | `sources-census.sh validate --root /home/vgpnk/Projects/shokunin chousa` exits **0** with the same five pre-existing W04 warnings (S051, S053, S073, S074, S075) and nothing else; `census` mode reports `rows 218` at both base and freeze with identical tier/status splits. |

---

## (a) Supersession graph, re-derived independently

**Method.** My own parser (`receipts/registry-recon.py`, output `receipts/registry-recon.json`) reads the 11-column table from a tree built at the freeze with
`git -C <lane> archive ac0a0892c15de11fb28d3208f2b287687c00477e | tar -x -C <scratch>/tree`, and searches **every cell of every row** for `supersedes\s+(S\d{3,})\s*—`, recording the column each occurrence sits in. This is deliberately broader than the counter's rule, so that a disagreement would surface rather than be masked.

```
$ cd /home/vgpnk/Projects/shokunin/chousa-shokunin
$ python3 -B receipts/registry-recon.py <scratch>/tree
exit=0
```

**Observed: 14 occurrences over 10 distinct superseder rows.** Every edge, with both statuses:

| superseder | superseder status | target | target status | marker cell | mined superseder? |
|---|---|---|---|---|---|
| S029 | mined | S019 | queued | teaches | yes |
| S030 | **queued** | S022 | queued | teaches | **no** |
| S031 | mined | S024 | queued | teaches | yes |
| S032 | **queued** | S021 | queued | teaches | **no** |
| S033 | mined | S020 | queued | teaches | yes |
| S073 | mined | S070 | mined | anchor **and** teaches | yes |
| S176 | mined | S171 | mined | teaches | yes |
| S200 | mined | S196 | mined | source **and** teaches | yes |
| S201 | mined | S197 | mined | source **and** teaches | yes |
| S202 | **rejected** | S198 | rejected | source **and** teaches | **no** |

The 14-vs-10 gap is fully explained: S073, S200, S201 and S202 each carry the marker **twice** (once in an earlier column, once in `teaches`), so they are 4 re-mentions of edges already counted, not extra edges. No other cell of any row contains a `supersedes S0NN —` marker (the only other `supersede`-shaped strings are the English words "superseded" in S166's anchor, S191/S206/S218's prose, and S217's scope phrase "how DCMI says it maintains and supersedes terms" — none is an edge).

**F1 — the counter's matcher finds the same 10 rows. No edge is missed.** `curation-r89.py:255` matches `re.match(r"supersedes (S\d{3,}) —", cells[6])` — the **raw** teaches cell, anchored at position 0. My independent enumeration of "rows carrying the marker in any cell" and "rows the counter's exact `re.match` accepts" both yield the identical list and the identical count:

```
counter-matched superseders (teaches col, re.match): ['S029','S030','S031','S032','S033','S073','S176','S200','S201','S202']  (10)
superseders (any cell, search):                          ['S029','S030','S031','S032','S033','S073','S176','S200','S201','S202']  (10)
```

This is the round-88 routed defect 4 repair working as intended: the round-88 counter matched the *lowercased* cell and got 0 matches over 218 rows; the raw-cell match gets 10. I checked the residual risk of case variants and of a marker not at position 0 of the teaches cell:

```
teaches cells containing 'supersede' NOT at position 0 (would be missed by re.match): ['S191','S206','S218']
lowercase-variant 'supersedes S...' anywhere: NONE (all occurrences are the canonical case)
```

S191/S206/S218 are the prose words "superseded" (no `S0NN` follows), so nothing is hiding behind the anchor. **F1: none (clean).**

**F2 — which edges have a non-mined superseder.** Three: **S030→S022** (S030 `queued`), **S032→S021** (S032 `queued`), **S202→S198** (S202 `rejected`). In all three the *target* is not `mined` either (S022 queued, S021 queued, S198 rejected), so none of them makes a superseded row live while its superseder is unadopted. The counter's `SUPERSEDED` leg therefore reports `SUPERSEDED_LIVE=0`, which is correct, not vacuous-by-construction:

```
$ python3 -B receipts/registry-recon.py <scratch>/tree   →  superseded_live-equivalent = 0
$ python3 -B <scratch>/tree/corpus/evidence/round89/curation-r89.py --root <scratch>/tree
SUPERSEDED_LIVE=0 UNENTAILED_TERM=0 MODIFIED_DEF_CITED=1 QUOTES_LOCATED=20/20
  Q_FLOORS=search-transparency-reporting-r84.md=13/13 floor13,provenance-recording-r85.md=7/7 floor7
  WARRANT_OK=17/17 DUP_QIDS=0 TEACHES_CHECKED=1 TEACHES_FLAGGED=1 TEACHES_UNRESOLVED=0
  SUP_CLAUSE_CHECKED=0 SUP_UNRESOLVED=0 LEGS_MEASURED=8/8
TEACHES_FLAGGED S024 terms=publication,modification disposition=superseded by S031
CURATION_R89=PASS
exit=0
```
(receipt `receipts/curation-r89-run.txt`; the lane's own counter was run read-only against the freeze tree — it writes nothing.)

**F3 — is any of them the disposal edge for the flagged row? Yes, and it is a mined one.** The flagged row is **S024** — the *only* row in the registry whose `teaches` carries a contrast phrase **and** a date term ("A last-reviewed date for accuracy is a property separate from publication or modification dates"; contrast `separate from`, terms `publication`+`modification`). Its own capture (`corpus/captures/11d6cc56bb24adfc61eea2b4.txt`, the Schema.org `lastReviewed` page) contains **none** of `publication|published|modified|modification|created|issued` — it says "Date on which the content on this web page was last reviewed for accuracy and/or completeness." So S024 is genuinely flagged.

Its disposal edge is **S031→S024**, and S031's status is `mined` — the only status the counter treats as disposing. The counter prints that disposition explicitly (`TEACHES_FLAGGED S024 … disposition=superseded by S031`), which matches QUALITY criterion 178 (a frozen `teaches` cell is not evidence; the superseding row's is). **F3: confirmed — the flagged row's disposal edge is S031, a mined superseder; none of the three non-mined superseders (F2) touches S024.**

---

## (b) Superseder-own-read population — `SUP_CLAUSE_CHECKED=0` confirmed or refuted

**Confirmed.** The claim's named limit 4 says the superseder-own-read clause is vacuous on the real registry because "no superseding row names a date term". I re-derived this with my own script rather than trusting the counter's print.

**Population — how many superseding rows carry a contrast phrase AND a date term?** **Zero**, over the broadest possible reading (all 11 cells of all 10 superseder rows, not just `teaches`):

```
superseders and why the SUP clause skips each:
  S029: contrast=NONE date_terms=NONE  -> skipped
  S030: contrast=NONE date_terms=NONE  -> skipped
  S031: contrast=['no comparison'] date_terms=NONE  -> skipped
  S032: contrast=NONE date_terms=NONE  -> skipped
  S033: contrast=NONE date_terms=NONE  -> skipped
  S073: contrast=NONE date_terms=NONE  -> skipped
  S176: contrast=NONE date_terms=NONE  -> skipped
  S200: contrast=NONE date_terms=NONE  -> skipped
  S201: contrast=NONE date_terms=NONE  -> skipped
  S202: contrast=NONE date_terms=NONE  -> skipped
```

The only superseder carrying a contrast phrase is **S031** ("no comparison to other date properties claimed") — but S031 names **no** date term from the counter's list (`publication, published, modified, modification, created, issued`), so the conjunction is empty. A broader scan for *any* date term in *any* cell of *any* superseder row also returns nothing:

```
SUPERSEDER rows — any cell naming a DATE_TERM:  (none)
contrast AND date-term co-occurrence over all superseder rows/cells = 0
```

**Does each term read in its own capture?** Vacuously: the population is empty, so there is no term to check. The instrument's own count agrees: `SUP_CLAUSE_CHECKED=0 SUP_UNRESOLVED=0` (receipt `receipts/curation-r89-run.txt`). **F4: `SUP_CLAUSE_CHECKED=0` is confirmed independently — the clause is vacuous on the real registry, exactly as disclosed; the claim's wording is accurate and its non-vacuity rests on the battery's `SUP-clause-mirror`, not on real rows.**

---

## (c) The two `used-by` edits — and that nothing else moved

```
$ git -C /home/vgpnk/Projects/shokunin/chousa-shokunin diff \
    f8fa55ec94cb34e7b572a9d87d7f62d88bc80bf8 ac0a0892c15de11fb28d3208f2b287687c00477e -- corpus/SOURCES.md
```

The diff is two `-|`/`+|` pairs on the S216 and S218 rows, and nothing else:

**Cell 1 — S216, `used-by`:**
- OLD: `corpus/evidence/round86/claims.md, corpus/evidence/round87/claims.md`
- NEW: `corpus/evidence/round86/claims.md, corpus/evidence/round87/claims.md, corpus/evidence/round89/claims.md`

**Cell 2 — S218, `used-by`:**
- OLD: `corpus/evidence/round87/claims.md`
- NEW: `corpus/evidence/round87/claims.md, corpus/evidence/round89/claims.md`

**F5 — no other registry cell moved.** Verified by parsing both revisions cell-by-cell rather than by reading the diff (a cell-level diff catches a change a text diff could hide behind a long row):

```
rowcount old=218 new=218
ids only in old: []
ids only in new: []
CELL CHANGED S216.used-by
CELL CHANGED S218.used-by
total changed cells: 2
prose lines old=221 new=221 identical=True
```

`git diff --numstat` reports `2  2  corpus/SOURCES.md`. All 221 non-table lines (the header, the `## Paths` section, the round-25 correction prose) are byte-identical between the two revisions. Neither `status`, `recheck`, nor any other column moved on any row, so the CORPUS.md rule-2 append-only discipline holds: only `used-by` changed, and only in the two rows the round lesson names.

**Whole-commit scope** (for completeness — the registry is the only modified tracked file in the commit):

```
$ git -C <lane> diff --name-status f8fa55ec ac0a0892
A  .ufo/waves/round-89/census-start.txt
A  .ufo/waves/round-89/claims.json
M  corpus/SOURCES.md
A  corpus/evidence/round89/…            (20 files: the six instruments, controls/, after/, claims.md, pins)
A  plans/round-89.md
```

**F5: clean — exactly the two `used-by` cells named in the claim, no other registry cell moved.**

---

## (d) Campaign collision, read-only

**The append file exists.** `/home/vgpnk/Projects/shokuknow/merge/chousa/SOURCES.append.md` — 120 lines, 114 registry rows, plus a header comment (`<!-- corpus-expansion-1 :: staged rows for lane chousa -->`) and the 11-column table header. **Emptiness is not the result here.**

Extraction used the 0–3-space-tolerant Markdown-row pattern (`^ {0,3}\| (S\d{3,}) \|`), the same shape the census and the counter use:

```
append_exists = True
append_ids_count = 114   append_ids_unique = 114   append_ids_dupes = []
lane_ids_count   = 218   lane_ids_unique   = 218   lane_ids_dupes   = []
lane_min = S001   lane_max = S218
```

**Collision count = 114 — every staged id collides with a live lane row.** The staged set is **S082–S195**, contiguous with no gaps; the lane registry is S001–S218.

```
collision_count_unique = 114
collision_ids   = S082 S083 S084 … S194 S195      (all 114)
append_only_ids = []                              (no staged id is free)
lane_only_ids   = 104 ids (S001–S081, S196–S218)
```

**The colliding rows are different rows, not the same rows.** A line-by-line comparison of the two files' rows sharing an id found **0 identical** and **114 differing**:

```
identical rows: 0
differing rows: 114
--- S082 first diff at 9 ---
  APP : | S082 | PRISMA-S: an extension to the PRISMA Statement …
  LANE: | S082 | AVeriTeC dataset README (Schlichtkrull et al., MichSchli/AVeriTeC) …
```

The cause is visible in the campaign's own `MERGE-REPORT.json` / `MERGE-REPORT.md`: the package was staged against a **81-row** lane registry (`existing_rows = 81`, `first_id = S082`, `renumbered = []`). The lane has since grown to 218 rows and reused S082–S195 for entirely different sources, so the staged numbering is stale — this is a **renumbering gap**, not a shared-id space.

**What appending the package as-is would do** (measured in a scratch copy of the freeze tree — the lane repo was not touched):

```
$ <scratch>/append-test/corpus/SOURCES.md  ← freeze tree + the 114 staged rows inserted before "## Paths"
$ sources-census.sh validate --file <that file> --root <scratch>/append-test
E01: 1    (S097 fields=13 — the row carries an escaped pipe, so it splits into 13 cells)
E03: 113  (duplicate id, every staged id)
E04: 10   (duplicate url+scope within scope)
E09: 113  (invalid recheck)
E11: 65   (used-by path missing on disk)
W01: 7    W04: 59
```

**Every one of those codes belongs to a campaign-staged row, not to a lane row** (verified by intersecting each code's id set with the staged set: `in_campaign` == `in_lane_only` for all of E01/E03/E04/E09/E11/W01, and W04's 54 extra ids are all staged). Two mechanisms produce the E09/E11 mass:

- **E09 (113):** the staged rows put a prose recheck instruction in the `recheck` cell (`180d — \`aaron papers fetch …\` then confirm …`), where the lane's own 218 rows use a bare `Nd`/symbolic cadence in every case (lane shapes: 109 symbolic + 109 `Nd`, **0** prose). The census accepts `Nd`, an ISO date, or a symbolic cadence — prose fails.
- **E11 (65):** the staged rows' `used-by` points at `corpus/knowledge/…` files that are only staged in the campaign repo's `knowledge/` and `amendments/` subtrees and are not present in the lane.

**F6 (finding, medium).** Collision count **114/114**; id lists: staged = **S082–S195** (114 ids, contiguous), lane = **S001–S218** (218 ids), `append_only = ∅`. The collision is not a benign overlap: the staged rows describe different sources under the same ids, the campaign's own report acknowledges an 81-row baseline, and a naive append yields 113 duplicate ids plus a malformed row. The package needs **renumbering** (or per-id reconciliation) before adoption. **Nothing was adopted, edited or staged in the campaign repo** — read-only throughout.

---

## (e) Census

```
$ cd /fast/scratch/hyaku/chousa-r89/R89ScoutRegistry
$ /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin chousa
chousa	W04	S051 duplicate url www.w3.org/TR/2017/REC-html52-20171214/syntax.html across scopes
chousa	W04	S053 duplicate url docs.python.org/3/library/socket.html across scopes
chousa	W04	S073 duplicate url www.gnu.org/software/coreutils/manual/coreutils.html across scopes
chousa	W04	S074 duplicate url docs.python.org/3/library/hashlib.html across scopes
chousa	W04	S075 duplicate url www.gnu.org/software/coreutils/manual/coreutils.html across scopes
chousa	ok	/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/SOURCES.md
exit=0
```

Receipt `receipts/census-validate.txt`. **Exit 0**, six output lines: the **same five pre-existing W04 warnings** (S051, S053, S073, S074, S075 — duplicate URL across scopes) and one `ok` line. No `E`-code of any kind, no new W-code.

**Row count 218 → 218.** `validate` prints findings, not a row count, so I ran `census` mode as well (same script, same root):

```
$ sources-census.sh census --root /home/vgpnk/Projects/shokunin chousa     → exit 0
chousa	rows	218
chousa	tier.A	139   tier.B	59   tier.C	20
chousa	status.mined	182   status.queued	12   status.rejected	24
```

and the same command against a base-revision tree:

```
$ sources-census.sh census --file <scratch>/base-tree/corpus/SOURCES.md --root <scratch>/base-tree   → exit 0
file	rows	218
file	tier.A	139   tier.B	59   tier.C	20
file	status.mined	182   status.queued	12   status.rejected	24
```

`diff` of the two census outputs is **empty** (identical rows and identical splits). The base `validate` output carries the same five W04 ids (only the lane label differs — `file` vs `chousa`, because `--file` was used). Receipts `receipts/census-census.txt`, `receipts/census-census-base.txt`, `receipts/census-validate-base.txt`.

**Cross-check against the committed receipt.** The freeze commit ships `.ufo/waves/round-89/census-start.txt`; its five W04 ids are **identical** to my live run's (`diff` of the W04 id sets: `W04 ID SETS IDENTICAL`), and the committed file's `ok` line names the same absolute registry path. The committed receipt is a faithful record.

**F7: clean — 218 rows at both revisions, same five pre-existing W04 warnings, validate exit 0.**

---

## Cross-checks against the frozen claim text (read-only corroboration)

Not the seat's assignment, but two facts the claim leans on were checked while the registry was open, and both hold:

- **Subject tool unchanged.** `git show <base>:tools/gate-records.py | sha256sum` and the same for the freeze both give `905f9da2fdf233b3a599f079a4c40ace730e3acf5464a2b80e1f93a616242d60` — the sha256 the claim states. The nine `instrument-pins.txt` entries (six instruments + `expected.tsv` + `run-controls.sh` + `c1-positives.tsv`) plus the subject-tool pin all verify against the freeze tree: `sha256sum -c corpus/evidence/round89/instrument-pins.txt` → **10 × OK, exit 0**.
- **S216's ground reads in its own capture.** The claim's 22-word quote is *not* byte-verbatim in `corpus/captures/b1b13a12aee75c6ecc20fb91.txt` (the capture wraps lines and interleaves blank lines), but it **is** present under whitespace normalisation, and it reads in the right section — §15.3.4 *203 Non-Authoritative Information*: "The 203 (Non-Authoritative Information) status code indicates that the request was successful but the enclosed content has been modified from that of the origin server's 200 (OK) response by a transforming proxy (Section 7.7)." The 22-word span the claim quotes is exactly that sentence's first clause. Capture is committed and present in the freeze tree (485 289 bytes).
- **S218's ground reads.** `corpus/QUALITY.md:1120` carries criterion 178 ("A frozen `teaches` cell is not evidence; the superseding row's is"), and the fleet-root `CORPUS.md` "SOURCES.md — where a shokunin learns" → Rules 2 carries the append-only rule. Note for the record: `CORPUS.md` lives at the **fleet root** (`/home/vgpnk/Projects/shokunin/CORPUS.md`), not inside `chousa-shokunin/`; S218's `source` cell names it as `CORPUS.md`, which resolves correctly from the lane's own scope.

---

## Remaining unknowns / limits of this seat

1. **The campaign collision is a byte-level id overlap only.** I did not adjudicate which of the two competing row-sets is correct for any id, and I did not open any source — the claim of "the staged rows describe different sources" is a **textual** difference (`0 identical, 114 differing` lines), not a judgement about which is right. Deciding that is the campaign owner's, not this seat's.
2. **The `E04`/`E09`/`E11` masses in the append test** are measured against the *current* census contract (`sources-census.sh` at the fleet root). If the campaign owner intends a different registry contract, those counts change; the E01 and E03 masses would not.
3. **`SUP_CLAUSE_CHECKED=0` is a fact about this freeze tree only.** A later row that supersedes with both a contrast phrase and a date term would make the clause fire; nothing here predicts that.
4. **No LSP server was available in this environment** for the Python instruments, so symbol-level tracing of `curation-r89.py` was done by direct source reading (`curation-r89.py:80-91` parser, `:154-166` supersession graph, `:233-267` teaches + superseder-own-read clauses) rather than by `definition`/`references` queries. Text search was used as the literal fallback and is recorded as such, not as semantic proof.

## Cleanup

`/fast/scratch/hyaku/chousa-r89/R89ScoutRegistry/` (trees, base tree, append-test copy, scripts, receipts) is deleted before yield. Every receipt cited above is copied first into `.ufo/waves/round-89/w1/R89ScoutRegistry/receipts/`. Nothing was written under `/tmp`, nothing was written outside `.ufo/waves/round-89/w1/R89ScoutRegistry/` and the scratch dir, and no lane or fleet git/jj command mutated anything.

VERDICT: R89ScoutRegistry C2 held — the registry reconnaissance confirms the two `used-by` cells and the five pre-existing W04 warnings are exactly as frozen, independently confirms `SUP_CLAUSE_CHECKED=0` as vacuous on the real registry, and the one new finding (a 114/114 id collision with the stale campaign merge package) is a campaign-side issue that does not move either frozen predicate.

# R84ConnectorSiblings — sibling-overlap scan (round 84, L1 chousa)

Seat: `R84ConnectorSiblings` (connector, leaf). Scope: read-only sibling-overlap scan across every
sibling lane repo at `/home/vgpnk/Projects/shokunin/<lane>-shokunin`, plus a behavioural probe of
sibling instruments against chousa's own bytes.

Lane root: `/home/vgpnk/Projects/shokunin/chousa-shokunin`.
Revisions read: base `408ae68f9e445fc911f713d5bbb3a64dda1ab9fe`, scored landing
`03bbb4580b39b442be69f998fae2db48d64b8c93`.
Scratch: `/fast/scratch/hyaku/chousa-r84/R84ConnectorSiblings/` (deleted before yield).
Receipts (copied): `.ufo/waves/round-84/w1/R84ConnectorSiblings/receipts/` — 33 files, each carrying
its own `# cmd:`, `# cwd:` and `# exit:` header lines.
Network: none used (this seat's item names no re-open; `corpus/evidence/round84/egress-approval.md`
was read but no row was fetched). Tooling: none installed (no tool needed beyond `git`, `grep`,
`python3`; pacman guard respected — no pacman transaction attempted).

---

## Q1 — Does any sibling hold a knowledge entry on search-transparency reporting?

**No.** Across all 20 sibling lanes' `corpus/knowledge/` and `corpus/SOURCES.md`, no sibling holds an
entry on search-transparency reporting (PRISMA checklist reporting, search-strategy reporting,
systematic-review search audit). Two sibling lanes touch the *terms* without holding the ground:

| sibling | file | what it actually holds | why it is not the same ground |
|---|---|---|---|
| kengaku | `corpus/knowledge/contamination-detection-and-transparency.md` | S001 = *Are LLM Benchmarks Already Contaminated? A Systematic Review* (GEM 2026, ACL Anthology). A systematic review **as a source**, about benchmark contamination. | "systematic review" here is the *topic*, not the *reporting method*. kengaku's own `PROVINCE.md:3` is "LLM/model research & evaluation". |
| kotodama | `corpus/knowledge/verification/citation-format-and-source-registry.md` | KTD-S-0003 = DCMI Metadata Terms 2020-01-20, used for a worldbuilding citation profile (lines 7, 18-19, 96, 165). | It cites the **same DCMI specification** as S023, but for bibliographic provenance. It never touches `dcterms:valid` or `dcterms:available` (grep: 0 hits) — precisely the two terms the new entry's rows 10 and 11 turn into decision rows. Its `PROVINCE.md:19` routes "general source-research method (chousa)" away. |

Byte-level check: every one of the new entry's 12 quotes was searched (whitespace-collapsed, curly
quotes folded) against **every file** of every sibling `corpus/knowledge/` tree → `quote-overlap hits: 0`.
The ground is genuinely unoccupied.

- Receipt: `receipts/q1-knowledge-transparency.txt`, `receipts/q1b-prisma-dcmi-knowledge.txt`,
  `receipts/f2-kotodama-dcmi.txt`, `receipts/quote-overlap-siblings.txt`.

## Q2 — Does any sibling hold a tool that verifies lesson Gate records / located quotes against committed captures?

**No sibling tool reads `GATE-RECORD` or `refetch.tsv`.** Exhaustive whole-repo sweep (all 20 sibling
repos, binary-excluded) for the literal `GATE-RECORD` returned hits in only two siblings, and every
hit is a **substring collision on a different artifact**:

- `tsukuroi-shokunin/corpus/QUALITY.md:125` + `corpus/lessons/round-26.md:64,87` — rule id
  `R26-GATE-RECORD-MISSING` (a *string* in a rule name, about a source row lacking a Gate record).
- `souji-shokunin/.ufo/waves/round-39/w1/W1ScoutOverlap.md:117` — souji's own scout had already
  adjudicated this at round 39: "`RECORD-MALFORMED` … did not appear. **Substring collision only.
  Adjacent.**"

The `refetch.tsv` sweep returned hits only in sibling *wave reports* that were themselves citing
chousa's path (mori `Mo86K01Conn.md:87` quotes chousa's round-57 lesson), never in a sibling
instrument.

**Two siblings nevertheless implement the same *class* of check, which is the sharper form of this
answer.** No sibling reads chousa's `refetch.tsv` schema (grep for `curl_rc` across every sibling
`tools/` and `scripts/` returns **only** chousa's own files), but:

- `tabi-shokunin/scripts/check-release-pins.mjs:40-49` — leg `f6-refetch`: an independent re-fetch
  receipt `corpus/evidence/round-29/release-pins/refetch/<id>.json` whose **seat differs** from
  `entry.fetched_by`, listing the same path at the stable tag with the receipt's `new_status` and
  `new_sha256`. Its own contract states the discipline chousa's `REFETCH` code also implements:
  "**Verdict per file is computed, never read from the receipt** … Copying old bytes in as new bytes
  therefore fails wherever the file changed" (`:46-47`), and the `f6-refetch` mutants
  (`tabi-shokunin/scripts/gate-mutants.json:206,214,222` — `pins-f6-refetch-seat`,
  `pins-f6-refetch-sha`, `pins-f6-refetch-all`) are the same anti-forgery class as chousa's
  `M03`/`M24` refetch-drift mutations.
- `kama-shokunin/tools/round43-health-audit.py:47-50,262-274` — leg `refetch`: a **live** fetch of
  each source URL must contain that source's frozen quotes, and "the counter cannot re-derive the
  quote". This is a *live* re-fetch leg where chousa's is a *committed-row* join.

So the fleet holds the **anti-forgery discipline** chousa's `REFETCH` code relies on (an independent
re-fetch, a different seat, and a verdict recomputed from bytes rather than read from the receipt) —
but in three different carriers, none of which reads chousa's `refetch.tsv` rows. The *discipline* is
sibling-held; the *schema* and the per-record join are not.

**But four siblings do hold functionally adjacent instruments.** This is the substantive answer to Q2 —
the capability shape exists in the fleet, in four different decompositions, and chousa's new tool is
the only one that joins *registry → capture → refetch → rev blob* in one per-record pass:

| sibling tool | what it binds | what it does **not** bind |
|---|---|---|
| `kotodama-shokunin/tools/check-gate-captures.py` | a Gate **table** row's sha256 → the named capture file's bytes (`CAPTURE-MISSING/ABSENT/SHA-MISMATCH`) | reads only markdown `\| … \|` rows whose first cell is a bare `S\d+`; **no** quote location, **no** refetch row, **no** rev form |
| `souji-shokunin/tools/souji-gate-check.py:11-13` | a located quote → the committed snapshot named on the same line, whitespace-collapsed | per-entry, not per-record; no registry→capture→refetch join; no ASCII-digit or word-count discipline |
| `mori-shokunin/tools/mori-anchor-check.py:12-15` | a quote → **one line** of a pinned copy + its word count | caller-supplied spec only; no registry, no capture key, no refetch, no rev form |
| `tsukuroi-shokunin/tools/check-pause-gate.py:94` | a gate's `capture_sha256` → the pinned capture's bytes | a JSON gate entry, not lesson Gate records; no quote location |

**Behavioural probe (this is the part a text grep cannot produce).** I ran three sibling instruments
against chousa's own round-84 bytes:

- `kotodama/tools/check-gate-captures.py chousa-shokunin/corpus/lessons/round-84.md …/corpus/captures`
  → `GATE-CAPTURES: 0 finding(s) in 0 row(s)`, **exit 0**. This is a **vacuous green**: chousa's Gate
  uses `GATE-RECORD` *lines*, so the tool's table-row scope rule selects **0 rows** (measured: `0`
  markdown table rows in chousa's `## Gate` section) and reports success. The same tool on an
  in-scope sibling lesson (`kotodama/corpus/lessons/round-97.md`) selects **9 rows** and reports
  `9 finding(s) in 9 row(s)` (all `CAPTURE-MISSING`, because I pointed it at the wrong evidence dir;
  the exit code is 1 because findings exist) — so the tool's row-selection works, it simply does not
  cover chousa's record form. **A sibling tool pointed at chousa's gate records exits 0 while
  checking nothing; the same tool on an in-scope lesson selects 9 rows and exits 1.**
- `mori/mori-anchor-check.py` against the new entry's own quotes on the committed PRISMA capture →
  `Q1 … verdict=ok located_on=17 occurrences=1 words_counted=17`, `Q3 … verdict=ok located_on=19
  occurrences=1 words_counted=17`, `Q2 … verdict=wordcount_mismatch located_on=18 words_counted=9
  words_recorded=7`. The tool independently **locates** the entry's quotes at their true capture
  lines — 17/18/19, the PRISMA item 6 / 7 / 8 / 16a rows of the committed checklist capture — with
  `occurrences=1` each, i.e. every PRISMA quote the entry declares is *uniquely* located in its
  capture. The `Q2` mismatch is the tool rejecting **my probe's** asserted count of 7 against the
  quote's true 9 words; the entry itself asserts no word count (its quote table has none), so
  nothing in the entry is wrong here — the point is that the true count of a quote the entry does
  not record must be recomputed by an independent reader.
- `mori/mori-anchor-check.py --check "modified-Def|8786|7|Date on which the resource was changed."`
  → `verdict=ok located_on=8786 occurrences=1 words_counted=7 words_recorded=7`, `ANCHOR_CHECK: PASS`, exit 0.

- Receipts: `receipts/f1-sibling-gate-tools.txt`, `receipts/q2-gate-record-tools.txt`,
  `receipts/sibling-refetch-family.txt` (RF1–RF4),
  `receipts/p1-kotodama-gate-captures.txt`, `receipts/p2-mori-anchor-check.txt`,
  `receipts/positive-control.txt`, `receipts/positive-control-2.txt`,
  `receipts/positive-control-3.txt`, `receipts/kotodama-in-scope.txt`,
  `receipts/mori-anchor-corrected.txt`.

## Q3 — Does the new entry or the new tool touch sibling province?

**No sibling province is touched.** `grep` for every sibling lane name in
`corpus/knowledge/search-transparency-reporting-r84.md` → `(none)`; same grep in
`tools/gate-records.py` → `(none)`.

The new entry names only chousa's own held entries as neighbours (`search-query-exposure-r51.md`,
`search-query-templates-r54.md`, `search-log-method-r39.md`, `search-tracking-record-r40.md`), and
chousa's `PROVINCE.md:5-8` owns exactly "search-strategy taxonomy … claim-vs-source verification …
citation chaining". The reverse direction is also clean: every sibling `PROVINCE.md` that names
"research method" routes it **to** chousa (kake `:42`, kasegi `:47`, kumitate `:32,48`, kotoba `:60`,
kotodama `:19`, souji `:116`, tabi `:186`, audio `:53`) — nobody claims it.

**One cross-province boundary is worth naming explicitly, because it is adjacent rather than
contained.** The new entry's row 7 (`Comparing evidence-based generation approaches | use a shared
taxonomy and unified benchmarks rather than isolated evaluation practices | … | Q8 (S018)`) states a
rule about *how to evaluate and compare LLM approaches*. `chousa/PROVINCE.md:10-11` refuses exactly
that: "**Refuses:** … model-quality or evaluation claims (→ kengaku)". The entry's own `## Limits`
(line 64) already bounds it: "The S018 survey is about evidence-based text generation with LLMs, not
systematic reviews; its taxonomy and metrics are for model evaluation, not for search reporting. The
rows keep only the attribution/traceability motivation." Row 7 is therefore *adjacent* to a refused
province and survives only on the Limits sentence, not on the row itself. The reviewer seat judged
row 7's **warrant** held (Q8 states the fragmentation and proposes the remedy); nobody has yet
adjudicated its **province** placement. It is not a kill rule under the frozen set (K2 is located,
K3 is warrant, K4 is ground), so it is reported, not fired.

- Receipts: `receipts/province-touch.txt`, `receipts/f3-research-method-own.txt`,
  `receipts/f5-s018-crossprovince.txt`, `receipts/decisive-checks.txt` (D6, D7).

---

## Non-obvious move (one, bounded) — a *locator* column the whole lane already uses, and the counter's blind spot it would close

Three seats have now measured two independent defects on the same artifact family, and neither
defect is visible to the frozen counters:

- `R84ReviewerEntry` fired C2 K3 on **row 9**: Q10 ("Recommended practice is to describe the date …")
  occurs **8 times** in the DCMI capture (measured: `grep -c` → 8) and does not by itself fix *which*
  date; the row's Do ("state the date on which the resource was changed") is stated by the
  **neighbouring Definition** at L8786 ("Date on which the resource was changed.", occurrence count
  **1**), which the entry never quotes.
- `R84CriticClaims` and `R84ExecRepro` both fired C1 K2 on the **setup leg**: a non-git `--repo`
  degrades to `FAIL LINE,REV` exit 1 instead of `GATE_RECORDS_ERROR` exit 2.

**The move.** The lane's own base corpus already carries the discipline that would have caught the
first defect, and 36 of the 95 base entries in `base-knowledge.txt` use it: **a per-quote locator**
(`char N` / `line N`). The new entry uses it **zero** times (measured: `grep -c` → 0 across
`char N|line N`). Meanwhile `depth-r84.py`'s E3 rule checks only that a quote *occurs* in the
normalized capture (`norm(qt) not in fr[src][1]`) — it never checks *uniqueness* and never records
where the quote was located, so an 8-fold-ambiguous quote passes as cleanly as a unique one.

The synthesis across the round's own proposals is therefore a **one-column change to the entry's
`## Located quotes` table** — add `locator` and put the true capture location in each cell — which:

1. **closes the K3 row-9 gap with a quote that is unique in its capture** (the `modified` Definition
   at L8786, occurrence count 1 — verified by `mori-anchor-check.py` at `verdict=ok located_on=8786
   occurrences=1`, exit 0) instead of the 8-fold-generic Q10 comment; and simultaneously lets rows
   8/10/11 carry `source` L10318 / `modified` L8786 / `valid` L11517 / `available` L3246, so the
   whole DCMI block stops relying on a generic sentence;
2. **is compatible with the frozen counter** — measured, not assumed: adding a `locator` column to a
   scratch copy of the entry leaves `depth-r84.py` output byte-identical
   (`ENTRY search-transparency-reporting-r84.md ok=yes rows=11 quotes=12/12 fails=-` /
   `DEPTH_R84 entries=1 ok_entries=1 rows=11 located_quotes=12 fresh_sources=3` / `DEPTH_R84=PASS`,
   rc 0 before and after), because `table()` keys off the header cells it needs and ignores an extra
   column. **The counter needs no amendment and no re-freeze.**
3. **costs nothing on C1**: it touches a knowledge entry's quote table, not `tools/gate-records.py`,
   and it leaves the 288-forgery battery and the 15 frozen positives untouched.

**Risks, stated honestly.** (a) The locator values are *my* readings of the committed captures; a
non-author must re-derive each one before it is written. (b) The locator column makes the entry's
warrant claims *stronger*, so it can only convert a K3 fire into a hold — it cannot create a new
kill, and it cannot rescue a scored revision (repairs after scoring do not rescue). (c) Adding a
column to a table the frozen counter parses is safe **only because** the counter was measured
tolerant; if a future counter requires an exact column set, this move must be re-measured.
(d) It does **not** address the C1 setup leg (K2) — that is a separate, already-filed defect in
`tools/gate-records.py:176-189` (`git_blob()` returning `None` on any `git` failure, with
`GATE_RECORDS_ERROR` reachable only at lines 277/281 for missing files).

**Verification (all measured; exact commands and exit codes in the receipts).**

```
# locator column is counter-compatible (scratch copy; frozen counter untouched)
python3 -B corpus/evidence/round84/depth-r84.py --root <copy>
  → ENTRY search-transparency-reporting-r84.md ok=yes rows=11 quotes=12/12 fails=-
    DEPTH_R84 entries=1 ok_entries=1 rows=11 located_quotes=12 fresh_sources=3
    DEPTH_R84=PASS                                                    (rc 0)
# same, after the locator column is added
  → byte-identical output, DEPTH_R84=PASS                            (rc 0)

# the replacement quote is unique in its capture and locatable
grep -c -F "Date on which the resource was changed." corpus/captures/f5545a194c06ab421875b047.txt   → 1
grep -c -F "Recommended practice is to describe the date, date/time, or period of time as recommended for the property Date, of which this is a subproperty." corpus/captures/f5545a194c06ab421875b047.txt → 8
python3 -B ../mori-shokunin/tools/mori-anchor-check.py --pin <capture> \
  --check "modified-Def|8786|7|Date on which the resource was changed."
  → anchor item=modified-Def span=8786 verdict=ok located_on=8786 occurrences=1 words_counted=7 words_recorded=7
    ANCHOR_CHECK: PASS items=1 ok=1                                    (rc 0)

# the entry currently carries no locator at all
grep -cE "char [0-9]+|line [0-9]+" corpus/knowledge/search-transparency-reporting-r84.md  → 0
# while 36 of the 95 base entries do
```

- Receipts: `receipts/verify-counter-compat.txt`, `receipts/dcmi-term-contexts.txt`,
  `receipts/final-checks.txt`, `receipts/mori-anchor-corrected.txt`.
- **Every command quoted above is re-run end-to-end in one pass** in
  `receipts/reproduce-report-commands.txt` (R1a…R10, each with its own `$` line and `[exit=N]`).
  All reproduce; the only non-zero exits there are *expected* and meaningful:
  `R4a` and `R5b` exit 1 because `grep -c` returns 1 on a **zero** count (the measurements that
  establish the absence of locators and of table rows), and `R5c` exits 1 because findings exist.

---

## Summary of findings

| # | finding | severity | inside a frozen kill rule? |
|---|---|---|---|
| 1 | **Sibling tool vacuous green.** `kotodama/check-gate-captures.py` exits 0 on chousa's round-84 lesson while selecting **0 rows** (chousa's Gate is `GATE-RECORD` lines, not table rows) — it verifies nothing about chousa's records and reports success. | medium (cross-lane) | no — no sibling instrument is in scope of C1/C2 |
| 2 | **New entry carries no per-quote locator**, while 36/95 base entries do; the *sibling* tool `mori-anchor-check.py` locates all three PRISMA quotes the entry declares at their true capture lines (17/18/19), each with `occurrences=1` — i.e. every one of them is already uniquely locatable, which is exactly the property the entry does not record and the counter does not check. | medium | partially — it is the mechanism behind the reviewer's C2 K3 row-9 fire |
| 3 | **Q10 ambiguity is structural**: 8 occurrences in one capture; the `modified` Definition (L8786, 1 occurrence) is the quote that actually warrants row 9 and is never quoted. | high for C2 K3 | yes — `R84ReviewerEntry` already fired it; this receipt supplies the occurrence counts and the located alternative |
| 4 | **Row 7 province adjacency**: an evaluation-practice rule about LLM approaches, inside a lane whose `PROVINCE.md:10-11` refuses "model-quality or evaluation claims (→ kengaku)". | low | no — no frozen rule covers province; reported, not fired |
| 5 | **Ground, tool and province are unoccupied, but the *discipline* is sibling-held.** 0 quote overlaps across every sibling knowledge tree; no sibling tool reads `GATE-RECORD` or chousa's `refetch.tsv` schema (grep `curl_rc` → only chousa's own files); every sibling `PROVINCE.md` routes research method *to* chousa. **However** tabi's `f6-refetch` (independent seat, "verdict … computed, never read from the receipt", mutants `pins-f6-refetch-{seat,sha,all}`) and kama's `refetch` leg (live fetch must contain the frozen quotes) implement the same anti-forgery class chousa's `REFETCH` code and its `M03`/`M24` mutations depend on. | informational — the C1 capability is **discipline-sibling-held, carrier-unique** | n/a |
| 6 | Stray dir `kumitate-shokinin` (one `n`) exists beside `kumitate-shokunin`; it holds no `corpus/knowledge`. Not a sibling lane. | informational | n/a |

The two files that would change under the proposed move — the entry's quote table and (for the K3
item only) the entry's row-9 warrant — are the **scored landing bytes**; per the frozen rules,
repairs after scoring do not rescue, so the move is offered for the *next* round and for the
non-author re-derivation, not as a fix to the scored revision.

VERDICT: R84ConnectorSiblings C1 n/a — sibling-overlap scan found no sibling instrument covering `GATE-RECORD`/`refetch.tsv` (the C1 setup-leg K2 fire was filed independently by R84ExecRepro and R84CriticClaims), but it produced a cross-lane false-green finding against a sibling tool that exits 0 on chousa's gate records while checking nothing.
VERDICT: R84ConnectorSiblings C2 n/a — the ground and the tool are unoccupied across all 20 sibling lanes, but the scan corroborates the reviewer's row-9 K3 fire with occurrence counts (Q10 ×8 vs the unique `modified` Definition at L8786) and shows the lane's own locator convention plus a sibling anchor tool would close it at zero counter cost.

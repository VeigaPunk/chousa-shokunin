# R87ScoutRegistry — registry reconnaissance for C2's `teaches` leg

Seat: `R87ScoutRegistry` (scout, leaf). Lane: chousa, round 87, wave w1.
Landed bytes read: `e6e920a4e6988287c31e89b3e920a118b569ae52` (committed tree at
`/home/vgpnk/Projects/shokunin/chousa-shokunin`).
Frozen predicate set read first: `corpus/evidence/round87/claims.md` (C1 K1–K4,
C2 K1–K4) and `plans/round-87.md` (pre-freeze repairs 1–7).
No production file was edited; no lane/fleet git or jj mutation; no network.

All work was done under `/fast/scratch/hyaku/chousa-r87/R87ScoutRegistry/`
(`tree/` = `git archive e6e920a4 | tar -x`, `work/` = scripts and fixtures).
The scratch dir is removed on yield. Every receipt cited below was copied into
`.ufo/waves/round-87/w1/R87ScoutRegistry/receipts/` before the scratch was
deleted.

Tooling: no install was needed or performed. `python3` (3.x, system),
`gawk` (system, `/usr/bin/gawk`), `bash`, and `git` were already present and
sufficient; `scripts/sources-census.sh` was executed read-only from the fleet
root. Nothing was installed via pacman (paused host-wide) or any other channel.

---

## (a) The teaches-rule population over all 218 rows

Re-derivation reproduces the counter's own algorithm exactly
(`corpus/evidence/round87/curation-r87.py:202-219`: `CONTRAST` =
`("separate from", "no comparison", "independent of", "distinct from")`,
`DATE_TERMS` = `("publication", "published", "modified", "modification",
"created", "issued")`; a row is *checked* when its `teaches` cell contains a
contrast phrase **and** a date term; it is *flagged* when the named date term
is absent from its own capture; it is *unresolved* when flagged and not
superseded).

```sh
S=/fast/scratch/hyaku/chousa-r87/R87ScoutRegistry
mkdir -p "$S/tree" && git -C /home/vgpnk/Projects/shokunin/chousa-shokunin \
  archive e6e920a4e6988287c31e89b3e920a118b569ae52 | tar -x -C "$S/tree"
python3 -B "$S/work/recon.py" "$S/tree" "$S/work/recon.json"   # exit 0
```

Receipt: `receipts/recon.json` (script: `receipts/recon.py`).

| quantity | value |
|---|---|
| registry rows in `corpus/SOURCES.md` (11 cells each) | **218** (0 dropped: `dropped_rows = []`) |
| rows carrying a **contrast phrase** (counter's `CONTRAST`) | **6** |
| rows carrying contrast phrase **AND** a date term (counter's `DATE_TERMS`) | **1** |
| rows **checked** (the leg's population) | **1** |
| rows **flagged** (capture lacks a named date term) | **1** |
| rows **superseded** (target of a `supersedes S0NN —` edge) | **10** (unrelated to the flag) |
| **unresolved** (flagged and not superseded) | **0** |

The six contrast rows: `S007, S024, S031, S035, S037, S044`.
The single contrast+date row, the single checked row, and the single flagged
row are all **`S024`**:

```
S024  status=queued  superseded_by=[S031]
teaches: "A last-reviewed date for accuracy is a property separate from publication or modification dates"
capture: corpus/captures/11d6cc56bb24adfc61eea2b4.txt (schema.org/lastReviewed)
missed terms: publication, modification   (both genuinely absent: grep -c → 0)
```

Its superseder **`S031`** (status `mined`) is the row the plan (§pre-freeze
repair 7) relies on for the disposition. `S031` also carries a contrast phrase
(`no comparison`) but **no** date term from `DATE_TERMS`, so it is never checked
by the counter.

Live counter at the landing revision (for reference):

```sh
cd /home/vgpnk/Projects/shokunin/chousa-shokunin && \
  python3 -B corpus/evidence/round87/curation-r87.py --root /home/vgpnk/Projects/shokunin/chousa-shokunin
# SUPERSEDED_LIVE=0 UNENTAILED_TERM=0 MODIFIED_DEF_CITED=1 QUOTES_LOCATED=20/20
# Q_FLOORS=... WARRANT_OK=17/17 TEACHES_CHECKED=1 TEACHES_FLAGGED=1 TEACHES_UNRESOLVED=0 LEGS=7/7
# TEACHES_FLAGGED S024 terms=publication,modification disposition=superseded by S031
# CURATION_R87=PASS                                    exit 0
```
Receipt: `receipts/counter-landing.txt`.

**The leg's population is one row out of 218.** This is not a claim defect on
its own — the claim's own text says the leg "flags a row whose `teaches` states
a contrast against a date-property term its own capture never contains" and
requires "at least one flagged row and a named disposition for it" (K4), which
`S024`/`S031` supply. But it bounds how much the leg can detect, and §(b)
below shows the single-row population is a consequence of the *vocabulary*, not
of the registry.

## (b) Over-fire and under-fire under a wider vocabulary

Requested wider contrast set: base `CONTRAST` + `rather than`, `not the same
as`, `other date properties`.

```sh
python3 -B "$S/work/wide.py" > "$S/work/wide.json"          # exit 0
```
Receipt: `receipts/wide.json` (script `receipts/wide.py`).

### (b1) Wider **contrast** vocabulary alone (date terms unchanged)

| | base | wide contrast | Δ |
|---|---|---|---|
| contrast rows | 6 | **15** | +9 |
| checked (contrast ∧ date term) | 1 | **1** | 0 |
| flagged | 1 | **1** | 0 |
| unresolved | 0 | 0 | 0 |

**No row newly flags.** The nine new contrast rows are `S067, S070, S078,
S086, S088, S154, S197, S201, S218` — each carries `rather than` but **none**
carries any of the six `DATE_TERMS`, so none enters the checked population.

### (b2) Wider **date-term** vocabulary (contrast unchanged)

Widening `DATE_TERMS` to date-*property* concepts (`publication date`,
`modification date`, `last modified`, `creation date`, `other date
properties`, `date properties`, `date fields`, `timestamp`, …):

| | base | wide date | wide both |
|---|---|---|---|
| checked | 1 | 2 | 2 |
| flagged | 1 (`S024`) | 2 (`S024`, **`S031`**) | 2 (`S024`, **`S031`**) |
| newly flagged | — | **`S031`** | **`S031`** |

**The one row that newly flags under the wider vocabulary is `S031`** — and it
is the *superseder*, live (`mined`, no superseder of its own), so widening the
vocabulary would turn `TEACHES_UNRESOLVED` from 0 to 1 and fail the leg.

Capture support for that new flag:

```
S031  status=mined  live=True  superseded_by=[]
teaches: "supersedes S024 — lastReviewed records the date a web page was last
          reviewed for accuracy and/or completeness; no comparison to other
          date properties claimed"
missing under wide date vocab: "other date properties", "date properties"
capture 11d6cc56bb24adfc61eea2b4.txt (646 chars, schema.org/lastReviewed):
  grep -c 'other date properties' → 0 ;  grep -c 'date properties' → 0
  the page's only date language is "Date on which the content on this web page
  was last reviewed for accuracy and/or completeness" and "Values expected to
  be one of these types: Date"
```

**Does the capture support the flag?** For `S031` the answer is *no, and the
flag would be a false positive against the source's actual meaning*: `S031`'s
teaches is a **negated** contrast ("**no** comparison to other date properties
claimed"). The capture's silence on "other date properties" is the very fact
the row asserts; requiring the capture to contain the phrase inverts the
claim. The counter's `DATE_TERMS` list never reaches `S031` only because
`other date properties`/`date properties` are not in it — a **vocabulary
accident, not a semantic reading**. Widening `CONTRAST` alone (as instructed)
does not reach `S031` because `DATE_TERMS` gates it out first.

### (b3) Over-fire measurement (substring and word-sense)

```sh
python3 -B "$S/work/precision.py" > "$S/work/precision.json"     # exit 0
```
Receipt: `receipts/precision.json`.

- **Substring over-fire (latent):** the counter matches `DATE_TERMS` as raw
  substrings, so `published` matches inside `unpublished`. Rows affected:
  **`S115`, `S120`, `S124`** (each says "unpublished data" / "unpublished
  material" / "unpublished studies", not "published"). **None of the three
  carries a contrast phrase**, so none is checked today and the defect is
  latent — it would fire the moment any of them gained a contrast phrase.
- **Word-sense over-fire (latent):** `S118`, `S125`, `S126` contain the token
  `issued` in a non-date sense — `S118` "the issued guideline sets the
  literature stage", `S125` "the NMPA issued the interim guideline by notice",
  `S126` "organized the formulation of the interim guideline, issued on June
  18, 2019" (this last one *is* a date usage). `S118`/`S125` are verb /
  participle matches against a date-property term list. Again none carries a
  contrast phrase, so the leg never reads them.
- **No word-sense over-fire is reachable today**: every `teaches` cell that
  contains a `DATE_TERMS` substring *and* a contrast phrase is a genuine
  date-property contrast (`S024` alone). The only date-term-in-a-non-date-sense
  rows the sweep found (`S091` "manually created claims", `S105` "CNKI's own
  published definition", `S115` "unpublished data", `S122` "published
  2025-12-02", `S216` "a transforming proxy modified the enclosed content")
  carry **no** counter contrast phrase, so the leg never reads them
  (`S216`'s `modified` is the verb, not the date property — and `S216` is the
  round's own C1 source row).

### (b4) Independent under-fire sweep (contrast ∧ date concept, counter-blind)

An independent sweep over all 218 rows for *any* date-concept word ∧ *any*
exclusionary relation (a wider relation list than `CONTRAST`) yields **29 rows
the counter does not catch**. All 29 are ordinary prose uses of the word
"date" (`S019` "assessed on a schedule", `S041` "magnitude", `S059` "hexdigest",
`S107` "the date and the search expression", …) — not date-*property*
contrasts. Only **one** row in the whole registry is a genuine
date-property contrast the counter's six-literal `DATE_TERMS` cannot see:
**`S031`** (see b2).

### (b5) Capability probes on live and rejected rows

Two fixtures on throwaway copies of the landing tree, running the committed
counter (receipts `live-out.txt`, `rejected-out.txt`; scripts `live.py`,
`rejected.py`):

- **Live row is caught.** Rewriting live/mined `S218`'s teaches to
  `a last-reviewed date is a property separate from publication or modification
  dates` yields `TEACHES_CHECKED=2 TEACHES_FLAGGED=2 TEACHES_UNRESOLVED=1`,
  `LEG_FAIL TEACHES`, `CURATION_R87=FAIL`, exit 1. The leg does not only fire
  on `S024`.
- **Rejected rows are read as claims.** The leg has **no status filter** — it
  reads `rejected` rows' `teaches` (a rejection rationale) as a source claim.
  Giving `S217` (status `rejected`) the same contrast teaches yields
  `TEACHES_FLAGGED S217 terms=publication,modification disposition=UNRESOLVED`,
  `LEG_FAIL TEACHES`, exit 1. This is an **over-fire surface**: the leg can be
  failed by a row the lane has explicitly refused. It is inert at the landing
  revision (no rejected row carries a counter contrast phrase + date term).

## (c) The supersession graph: edges, chains, cycles, missing targets

```sh
python3 -B "$S/work/collision.py" > "$S/work/collision.json"   # exit 0
```
Receipt: `receipts/collision.json`.

The counter builds `superseded_by` from **one** pattern applied to the
`teaches` cell only (`curation-r87.py:139`,
`re.match(r"supersedes (S\d{3,}) —", cells[6])`).

**All 10 edges** (superseder → target; the edge is what makes the target
non-live):

| superseder | superseder status | target | target status | target exists |
|---|---|---|---|---|
| S029 | mined | S019 | queued | yes |
| S030 | queued | S022 | queued | yes |
| S031 | mined | S024 | queued | yes |
| S032 | queued | S021 | queued | yes |
| S033 | mined | S020 | queued | yes |
| S073 | mined | S070 | mined | yes |
| S176 | mined | S171 | mined | yes |
| S200 | mined | S196 | mined | yes |
| S201 | mined | S197 | mined | yes |
| S202 | **rejected** | S198 | **rejected** | yes |

- **Chains of length > 1: none.** `chain_edges_len_gt_1 = []`. Every target
  (`S019, S020, S021, S022, S024, S070, S171, S196, S197, S198`) is itself
  never a superseder, so the graph is a flat set of 10 one-edge components.
- **Cycles: none** (`cycles = []`).
- **Edges whose target row does not exist: none**
  (`edges_with_missing_target = []`).
- **Edge-wording completeness:** every `supersedes S0NN` mention in the file
  (15 occurrences across 10 distinct targets, including two in prose —
  `S033 also supersedes S020:` at line 436, and duplicate mentions inside the
  `source` and `anchor` cells of `S073`, `S200`, `S201`, `S202`) is matched by
  the counter's regex: `missed_by_counter_regex = []`,
  `teaches_mentions_supersedes_not_matched = []`. Every occurrence uses the
  em-dash `—` (U+2014) after the id, matching the pattern's literal.

**Does the disposition rule handle a chain correctly? No — a chain launders.**

The rule is one line (`curation-r87.py:218-219`):

```python
if sid not in superseded_by:
    teaches_unresolved.append((sid, miss))
```

`superseded_by` is keyed by *target*, so **any** incoming edge disposes the
row, regardless of what the superseding row says or whether the chain's head
carries the contrast at all. Fixture (`chain2.py`, receipt
`chain2-out.txt`): make `S033` supersede `S031` (so `S033 → S031 → S024`) and
give `S031` the same unentailed contrast teaches. Result:

```
TEACHES_CHECKED=2 TEACHES_FLAGGED=2 TEACHES_UNRESOLVED=0 LEGS=7/7
TEACHES_FLAGGED S024 terms=publication,modification disposition=superseded by S031
TEACHES_FLAGGED S031 terms=publication,modification disposition=superseded by S033
CURATION_R87=PASS                                        exit 0
```

`S031` asserts a contrast its own capture refuses, and is disposed by `S033`,
whose teaches (`PROV-O records derivation and entity generation/invalidation
times separately; …`) says nothing about publication or modification dates
and whose own capture lacks both terms. The chain head launders the flag; the
leg passes. **The rule is correct on the flat graph that exists today (there
are no chains) and unsound the moment a chain appears** — which is exactly
what CORPUS rule 2 / QUALITY 178 require the leg to handle.

**The disposition also ignores the superseder's own status.** Fixture
(`disp.py`, receipt `disp-out.txt`): set `S031`'s status to `queued` (so the
superseder of the only flagged row is itself not mined). The leg still prints
`TEACHES_FLAGGED S024 … disposition=superseded by S031`,
`TEACHES_UNRESOLVED=0`, `CURATION_R87=PASS`, exit 0 — the flag is disposed by
a row that is not the live citation either. Note the leg's *other* leg
(`SUPERSEDED`, `curation-r87.py:136-145`) does consult status, but only for
the `mined`/`not-mined` pair — it never feeds the `teaches` disposition.

**A non-chain ordering case the rule handles correctly** (fixture `chain.py`,
receipt `chain-out.txt`): `S033 → S031 → S024` with `S031` left un-flagged
still prints `TEACHES_FLAGGED S024 … disposition=superseded by S031`,
`TEACHES_UNRESOLVED=0`, `PASS` — the intended behaviour, since `S031` is the
corrected row.

## (d) Collision check against the campaign package

The census extractor is `scripts/sources-census.sh` (fleet root, executed
read-only; it writes only stdout or `--out`, and none was used).

### Lane registry (read-only)

```sh
/home/vgpnk/Projects/shokunin/scripts/sources-census.sh census --root /home/vgpnk/Projects/shokunin \
  /home/vgpnk/Projects/shokunin/chousa-shokunin
# chousa-shokunin rows 218 | tier.A 139 tier.B 59 tier.C 20
# status.mined 182 status.queued 12 status.rejected 24
# FLEET rows 218 ... missing 0                     exit 0
/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --today 2026-11-08 \
  --root /home/vgpnk/Projects/shokunin /home/vgpnk/Projects/shokunin/chousa-shokunin
# 5 x W04 (same URL across scopes), then "chousa-shokunin ok"             exit 0
```
Receipts: `receipts/census-lane.txt`, `receipts/validate-lane.txt`.

### Campaign package (read-only, never written)

```sh
/home/vgpnk/Projects/shokunin/scripts/sources-census.sh census \
  --file /home/vgpnk/Projects/shokuknow/merge/chousa/SOURCES.append.md
# file rows 0 ... FLEET rows 0 ... missing 0                             exit 0
/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --today 2026-11-08 \
  --file /home/vgpnk/Projects/shokuknow/merge/chousa/SOURCES.append.md
# 114 x "file E12 S0NN row outside Registry section"                     exit 1
```
Receipts: `receipts/census-append.txt`, `receipts/validate-append.txt`.

**The append file has no `## Registry` heading** (its only headings are two
HTML comments), so the census extractor counts **0 rows** in census mode and
flags all 114 rows as `E12 row outside Registry section` in validate mode.
The file is a staged append block, not a registry section; the extractor
cannot read it as one.

### Id sets and collision

Id sets parsed with the census extractor's own row shape
(`^ {0,3}\| (S\d{3,}) \|`):

| set | count | range |
|---|---|---|
| lane registry ids | **218** | S001 … S218 |
| campaign-package ids | **114** | S082 … S195 |
| **intersection (id collision)** | **114** | S082 … S195 |
| append-only ids | **0** | — |
| lane-only ids | 104 | — |

**Every id in the campaign package collides with an id already in the lane
registry.** The append set is a strict subset of the lane id space. The
collision is *nominal only* — the two sets carry different content for the
same id. Partitioning the 114 append rows by where their URL lives in the lane
registry:

| bucket | count | ids |
|---|---|---|
| no URL at all (own-work rows) | **11** | `S105, S106, S107, S108, S179, S184, S188, S189, S191, S192, S194` |
| URL exists in the lane under the **same** id | **4** | `S100, S101, S102, S103` |
| URL exists in the lane under a **different** id (URL-level duplicate) | **56** | e.g. append `S084` ↔ lane `S079`, append `S085` ↔ lane `S121`, append `S088` ↔ lane `S097` |
| URL nowhere in the lane registry | **43** | — |

(Sum: 11 + 4 + 56 + 43 = 114.) Of the 114, **0** have an identical `teaches`
cell; **97** share the same `status` value.

Receipt: `receipts/remap.json` (script `receipts/remap.py`), plus
`receipts/collision.json`.

### Collision under the census extractor (merged fixture, scratch only)

Appending the package's rows into a copy of the lane registry under a
`## Registry` heading and validating:

```sh
/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --today 2026-11-08 \
  --root "$S/work" "$S/work/fixture-full"
# 113 x E03 duplicate id | 10 x E04 duplicate url within scope
# 113 x E09 invalid recheck | 65 x E11 missing used-by
# 1 x E01 (S097, fields=13) | 7 x W01 | 59 x W04        exit 1
```
Receipt: `receipts/validate-fixture-full.txt`.

- `E03 duplicate id` fires **113** times — every append id except `S097`,
  whose row has **13 cells** instead of 11 (an extra `|` in the row), so the
  extractor's `E01 fields=13` fires first and `next`s before the id check.
  `S097` is therefore the one colliding id the extractor does *not* report as
  `E03`; the true duplicate-id count is **114**.
- `E04 duplicate url within scope` fires 10 times — append rows whose URL
  **and** scope match a lane row (`S087`, `S088`, `S089`, `S098`, `S099`,
  `S101`, `S102`, `S103`, `S114`, `S115`). This is the census's *same-scope*
  duplicate rule; the 56 cross-id URL duplicates above are `W04`-class
  (across scopes) or unseen.
- `E09` (113) and `E11` (65) are the package's own column-format debt: its
  `recheck` cells carry trailing prose after the cadence
  (`180d — re-open the chapter-04 URL and confirm …`), and its `used-by` paths
  point at 34 knowledge files that do not exist in the lane tree
  (`corpus/knowledge/search-log-fields-r36.md`,
  `corpus/knowledge/citation-check-status-vocabulary-r48.md`,
  `corpus/knowledge/dated-compilation-as-currency-r47.md` — all confirmed
  absent from the lane).
- `shared` mode over lane + merged fixture reports **126** shared URLs
  (receipt `receipts/shared-lane-fixture.txt`) — the 114 append rows'
  contribution plus the lane's own 5 `W04` cross-scope duplicates.

**Nothing in the shokuknow tree was written.** The extractor was invoked with
`--file` (read-only) and against scratch copies only.

---

## Findings

**F1 (C2, under-fire / vocabulary).** The `TEACHES` leg's contrast vocabulary
is exactly the counter's four literals, and its date vocabulary exactly six.
Adding `rather than`, `not the same as`, `other date properties` to the
contrast set changes **nothing**: the checked population stays at 1 row and no
row newly flags, because the nine new contrast rows carry no `DATE_TERMS`.
The single live row the wider vocabulary reaches is `S031`, and only if
`DATE_TERMS` is widened to date-*property* concepts — where the new flag
would be a **false positive**, because `S031`'s teaches is the *negated*
contrast "no comparison to other date properties claimed" and the capture's
silence on that phrase is the fact the row asserts. The counter does not flag
`S031` by vocabulary accident, not by reading.
`receipts/wide.json`, `receipts/deep.json`.

**F2 (C2, chain unsoundness).** The disposition rule
(`if sid not in superseded_by`) treats *any* incoming `supersedes` edge as a
disposition and never inspects the superseding row. On a chain
`S033 → S031 → S024` with `S031` carrying an unentailed contrast, the leg
prints `TEACHES_UNRESOLVED=0` and `CURATION_R87=PASS` — the head of the chain
launders the flag. The landing graph has **no chains** (10 edges, 0 chains, 0
cycles, 0 missing targets), so this is latent, not live.
`receipts/chain2-out.txt`, `receipts/collision.json`.

**F3 (C2, disposition ignores superseder status).** Setting the superseder of
the only flagged row (`S031`) to `queued` leaves the flag disposed
(`disposition=superseded by S031`, `TEACHES_UNRESOLVED=0`, `PASS`, exit 0).
The flag is discharged by a row that is itself not the live citation. Latent
at the landing revision; the `SUPERSEDED` leg consults status but never feeds
the `teaches` disposition.
`receipts/disp-out.txt`.

**F4 (C2, over-fire surface: no status filter).** The leg reads `rejected`
rows' `teaches` — a rejection rationale — as a source claim. A `rejected` row
carrying a contrast + date term is flagged `UNRESOLVED` and fails the leg
(`receipts/rejected-out.txt`: `S217` → `LEG_FAIL TEACHES`, exit 1). Inert at
the landing revision; combined with F1's latent substring over-fire
(`published` ⊂ `unpublished` on `S115`, `S120`, `S124`) and word-sense
over-fire (`issued` as a verb/participle on `S118`, `S125`), the leg's failure
surface is wider than its one-row population suggests.

**F5 (d, collision).** The campaign package `SOURCES.append.md` carries ids
`S082…S195`, all **114** of which already exist in the lane registry with
different content (4 same-URL, 56 URL-duplicate under a different lane id, 0
identical `teaches`, 97 same status). Merged, the census extractor reports
**113 × E03 duplicate id** (the 114th, `S097`, is masked by its own
`E01 fields=13`), **10 × E04 duplicate url within scope**, plus 113 × E09 and
65 × E11 from the package's own column format. The package also cannot be
read as a registry at all: it has no `## Registry` heading, so the extractor
counts 0 rows in census mode and reports 114 × E12 in validate mode.
`receipts/remap.json`, `receipts/validate-fixture-full.txt`,
`receipts/validate-append.txt`, `receipts/census-append.txt`.

**Positive checks (no finding).** The landing counter passes with the frozen
line (`receipts/counter-landing.txt`); the `supersedes` edge set is complete
against every wording in the file, with no missing target, no cycle, no chain
(`receipts/collision.json`); the leg *does* catch an unentailed contrast on a
live mined row (`receipts/live-out.txt`); the append file's rows were never
written to.

## Receipt index

All under `.ufo/waves/round-87/w1/R87ScoutRegistry/receipts/`.

| receipt | what it shows |
|---|---|
| `recon.py`, `recon.json` | (a) teaches population over 218 rows; supersession edges; id sets |
| `deep.py`, `deep.json` | full `teaches` + capture-term table for every wide-contrast row; independent sweep |
| `wide.py`, `wide.json` | (b) base vs wide-contrast vs wide-date vs wide-both counts; newly-flagged rows |
| `precision.py`, `precision.json` | (b) substring / word-sense over-fire; under-fire property sweep |
| `collision.py`, `collision.json` | (c) the 10 edges with statuses; chains, cycles, missing targets; collision detail |
| `chain.py`, `chain-out.txt` | (c) chain fixture, benign ordering → `PASS` |
| `chain2.py`, `chain2-out.txt` | (c) chain fixture, laundering → `PASS` (unsound) |
| `disp.py`, `disp-out.txt` | (c) disposition ignores superseder status → `PASS` |
| `live.py`, `live-out.txt` | (b5) live mined row with unentailed contrast → `FAIL`, exit 1 |
| `rejected.py`, `rejected-out.txt` | (b5) rejected row read as a claim → `FAIL`, exit 1 |
| `remap.py`, `remap.json` | (d) 114-id collision, URL buckets, cross-id duplicates |
| `census-lane.txt` | (d) census over the lane registry → 218 rows, exit 0 |
| `validate-lane.txt` | (d) validate over the lane registry → 5 × W04 then `ok`, exit 0 |
| `census-append.txt` | (d) census over the campaign package → 0 rows (no `## Registry`), exit 0 |
| `validate-append.txt` | (d) validate over the campaign package → 114 × E12, exit 1 |
| `validate-fixture-full.txt` | (d) merged fixture → 113 E03, 10 E04, 113 E09, 65 E11, 1 E01, exit 1 |
| `shared-lane-fixture.txt` | (d) shared mode over lane + merged fixture → 126 shared URLs |
| `counter-landing.txt` | the committed counter at the landing revision → frozen line, `PASS`, exit 0 |

## Remaining unknowns

- The intended reading of the campaign package's `S082…S195` ids (whether
  they are a stale snapshot of an earlier lane numbering, or a package meant
  for a different lane) is not determinable from the file: it carries no
  `## Registry` heading, no provenance comment beyond
  `<!-- corpus-expansion-1 :: staged rows for lane chousa -->`, and no
  companion note. The 56 cross-id URL duplicates suggest an earlier lane
  numbering, but the file does not say so.
- Whether `S031`'s "no comparison to other date properties claimed" is meant
  as a *disclaimer of a comparison* (my reading, and the reading under which
  F1's widened flag is a false positive) or as a *contrast against* the
  `dateModified`/`datePublished` properties (under which it would be a true
  flag). The capture text supports the disclaimer reading — the page mentions
  only `lastReviewed` and the type `Date` — but the lane's own intent is not
  recorded anywhere I could read.
- The exact intended scope of the `teaches` leg (live rows only? mined rows
  only? rejected rows excluded?) is stated in `QUALITY.md` 178 / `CORPUS.md`
  rule 2 only as "a superseded row's frozen `teaches` is not evidence"; the
  counter's choice to read all 218 rows regardless of status is not itself
  contradicted by any committed text I could find.

---

VERDICT: R87ScoutRegistry C2 held — the leg's one-row population, its
chain-unaware and status-blind disposition, its missing status filter, and
the 114-id collision with the campaign package are all established from
committed bytes and named receipts, and none of them falsifies C2's frozen
predicate, which passes at the landing revision.

# ScoutCoverageGround — does the map already hold the r46-C3 theme?

Item: coverage check on `corpus/README.md` (map + `## Frontier`) and `corpus/knowledge/`
for FEVER / AVeriTeC / zenodo / archive / cached / Memento / durable / verdict; report what
version-binding and archive ground the lane already holds (file:line), say whether the C3
theme is ground the map does NOT hold, and draft the two map rows in the map's exact shape.
Base tree: HEAD `c2f0e9d100c0d46633a6277b2fd51d2ac99678eb`. No fetch; captures read only.

## Commands and decisive output

```
$ grep -rn -i -E 'FEVER|AVeriTeC|AVeriMaTeC|zenodo|memento|web\.archive' corpus/knowledge/
corpus/knowledge/citation-version-binding-r36.md:10,16   (Memento-Datetime, date-not-hash)
corpus/knowledge/citation-version-binding-r37.md:17      (URL-alone version anchor)
corpus/knowledge/evidence-archive-field-policy-r41.md:1,3 (AVeriTeC README field dictionary)
corpus/knowledge/evidence-snapshot-coverage-r40.md:3,13,21,28 (S084 field census)
# no FEVER line, no zenodo line, no AVeriMaTeC line before the r46 landing

$ grep -ric 'FEVER' corpus/knowledge/*.md | grep -v ':0$'
FEVER: zero files          # (pre-landing; now only the two r46 entries)
$ grep -ril 'zenodo' corpus/knowledge/  → zero files
$ grep -ril 'AVeriMaTeC' corpus/knowledge/ → zero files

$ grep -rn -i 'durab' --include=*.md corpus/ SKILL.md
corpus/knowledge/verify-all-r6.md:296        (manifest durability — receipts)
corpus/knowledge/hardening-r10.md:286        (durable rules — method)
corpus/lessons/*.md:53,129,169,158,199      (durability of receipts/records)
# no hit concerns the durability of a support verdict

$ grep -n -i 'pool.version\|evidence-pool\|successor corpus\|FEVER\|durable' corpus/README.md
README.md:1063   ... "the staged pool-versioning amendment is not adopted, with its flip"   (only hit)
$ grep -c -i 'conceptdoi\|zenodo\|fever\|72.36' corpus/README.md   → 0

$ grep -n 'S079 \|S080 \|S081 \|S082 \|S083 \|S084 ' corpus/SOURCES.md
89: S079 RFC 7089 (mined) | 90: S080 WARP FAQ | 91: S081 NDL E2867
92: S082 AVeriTeC README | 93: S083 AVeriTeC paper | 94: S084 train.json
$ grep -c 'S085\|S086\|S087\|S088\|S089' corpus/SOURCES.md → 0   (registry append not yet run)

$ git ls-files corpus/knowledge/evidence-pool-versioning-r39*.md  → (empty)
$ stat corpus/knowledge/evidence-pool-versioning-r39.md
... 5451 2026-10-25 07:25:44 -0300    # untracked, after HEAD 07:08:16 — concurrent executor
$ stat corpus/knowledge/evidence-pool-versioning-r39-amendment-2026-10-23.md
... 5139 2026-10-25 07:26:04 -0300    # untracked, same wave
```

Offset spot-check against the five captures (byte slices, `python3`; all `OK`):
`S085@1271` "Pre-processed Wikipedia Pages (June 2017 dump)", `S085@2360` "A list of evidence
sets", `S086@15269` "used the June 2017 Wikipedia dump, processed", `S087@171`
`"conceptdoi": "10.5281/zenodo.4925953"`, `S088@2904` "Our best estimate for the date the claim
first appeared", `S088@3929` "An archive.org link for the source url", `S088@1142`
`Conflicting Evidence/Cherry-picking`, `S089@3022` "temporally constrained evidence
annotation", `S089@7137` "published before the claim’s date" (curly apostrophe in the capture).

## Ground the lane already holds

Version-anchor **mechanism** (per citation, protocol level):
- `corpus/knowledge/citation-version-binding-r36.md:10` — Memento-Datetime "constitutes a
  promise that the resource state reflected in the response will no longer change";
  `:11` an archived body "may very well not be byte-to-byte the same"; `:12` veracity out of
  scope; `:16` a date of a prior state, not a byte hash; `:17` stability, not authenticity.
- `corpus/knowledge/citation-version-binding-r37.md:11` WARP monthly cadence; `:17` the
  capture timestamp in the URL is a version anchor the lane's byte hash is not; `:27` Gate quote.

Archive **field semantics** in a verification corpus:
- `corpus/knowledge/evidence-archive-field-policy-r41.md:11` `cached_source_url` stated without
  condition; `:12` `cached_original_claim_url` "Where possible"; `:13` paper caches evidence
  pages; `:15` 404 warning for double-archived links; `:19`-`:22` asymmetry, empty-field
  meaning, and "a filled archive field is a link, not proof that the archived capture resolves".

Archive **coverage counted by value**:
- `corpus/knowledge/evidence-snapshot-coverage-r40.md:13` 5,959 web.archive.org values, 551
  filled-but-not-archive; `:21` 5,959 of 7,572 (78.7%); `:28` resolution not checked.

Nearest prior "support verdict" ground (no version binding): `claim-support-states-r24.md:8-18`
(access / relevance / support / truth are four separately failable observations);
`chain-resolution-r3.md` (a hop's existence, not relay fidelity).

Map + registry rows for the above: `corpus/README.md:1061` (r36), `:1062` (r37), `:1063`
(r41), `:1064` (r40); `corpus/SOURCES.md:89-94`.

## Is the C3 theme held? No — not as a unit

The map holds three *adjacent* pieces (anchor mechanism, field semantics, coverage count) and
explicitly records the theme itself as rejected: `corpus/README.md:1063` ends "the staged
pool-versioning amendment is not adopted, with its flip". Absent ground, each verified zero:

1. **Corpus-level durability mechanism** — freeze the evidence pool to a dated dump, deposit
   pool + labels under a citable versioned identifier, bind each verdict to a URL + sentence id
   inside that pool. No lane file held FEVER or zenodo (`grep -c` = 0 for both over
   `corpus/knowledge/` and `corpus/README.md`), and no lane text states the concept-DOI /
   version-DOI distinction that makes the deposit citable.
2. **Successor-corpus per-citation binding** — pair each cited URL with a timestamped archived
   copy *and* date the claim, constraining evidence to sources published before the claim.
   r41 documents what the fields *say*; nothing held said a later corpus binds by that route,
   or that the claim date is what makes the archive meaningful. AVeriMaTeC: zero files.
3. **Verdict durability itself** — every `durab*` hit in `corpus/` concerns receipts, manifests
   or ledgers; none concerns a support verdict's dependence on a pool version.

Also missing: the evidence-selection reliability figures (72.36% recall vs 91.2% label
validation) that make "carry the evidence set, not just the verdict" arguable with a number.

## Draft rows (map shape quoted from `corpus/README.md:1062`)

Exemplar, verbatim (the tail table header is `| Entry | What it holds | Evidence |`, README:1041;
rows append after README:1064):

> | `knowledge/citation-version-binding-r37.md` | Round-44 note: a non-Western version anchor — the NDL WARP FAQ's archive cadence for national, public and private institutions, and the NDL current-awareness E2867 move to URLs that embed the capture timestamp (`warp.ndl.go.jp/web/20250102112233`); the cadence is the operator's own statement and not a Memento header, and the example URL is a citation form, not proof of byte identity; the staged S093 (Portico) half is not adopted, with its flip | `S080` (WARP FAQ capture), `S081` (NDL E2867 capture); `evidence/round44/claims.md` §C3; `lessons/round-44.md` `## Gate`; `.ufo/waves/round-44/w2/W2ReviewWarp.md` |

Draft row 1:

| `knowledge/evidence-pool-versioning-r39.md` | Round-46 note: what makes a support verdict durable inside a verification corpus — FEVER's `evidence` field as "A list of evidence sets" binding each verdict to a Wikipedia URL plus a sentence id inside a pool frozen by the shipped "Pre-processed Wikipedia Pages (June 2017 dump)" and the paper's own "used the June 2017 Wikipedia dump, processed", with the deposit versioned as an artefact by the Zenodo record's `"conceptdoi": "10.5281/zenodo.4925953"` beside the `"key": "wiki-pages.zip"` pool file; durability comes from freezing the pool, not from stamping each citation with a revision, and the evidence-selection step is the weaker link at "recall of 72.36%" against label validation at "We found that 91.2%"; the staged spaced figures (95.42% precision; the 31.75 / 16.82 / 12.15% evidence-shape shares) are located as capture offsets, not committed spans, and whether a verdict survives the pool's own revision history is left as an unknown | `S085` (dataset page chars 1271, 2360), `S086` (ACL PDF chars 15269, 20847, 42011), `S087` (Zenodo chars 171, 4929); `evidence/round46/spans.tsv`; `evidence/round46/claims.md` §R46-C3 |

Draft row 2:

| `knowledge/evidence-pool-versioning-r39-amendment-2026-10-23.md` | Round-46 note: how a successor corpus binds each citation to an archived state — AVeriTeC pairs every evidence answer's `source_url` with `cached_source_url` ("An archive.org link for the source url") and dates the claim through `claim_date` ("Our best estimate for the date the claim first appeared"), the restriction being operational as evidence "published before the claim’s date" under "temporally constrained evidence annotation" (κ = 0.742 on verdicts); the claim-level `cached_original_claim_url` stays best-effort, the corpus carries a fourth label `Conflicting Evidence/Cherry-picking`, and the archived capture is not established to be the state the annotator read; the round-45 reject is flipped — the base entry is now held and every prose id is re-bound by document (RFC 7089 = `S079`, NDL E2867 = `S081`), not by staged id arithmetic | `S088` (AVeriTeC page chars 1142, 2904, 3929), `S089` (arXiv HTML chars 3022, 7137); `evidence/round46/spans.tsv`; `evidence/round46/claims.md` §R46-C3 |

Both rows carry no pipe inside a cell. Draft rows cite no wave-seat report path because the
r46 reviewer files had not settled at read time; add the landing seat paths at commit.

## Findings for the row owner

- **F1 (map staleness, must fix with row 2):** `corpus/README.md:1063` still reads "the staged
  pool-versioning amendment is not adopted, with its flip". The round-45 flip condition is now
  satisfied (`corpus/lessons/round-45.md:167-172`), so that clause must be superseded in place
  the way r8's row handles a superseded pin, or the map will hold both "not adopted" and the
  adopting row.
- **F2 (concurrent landing, not my write):** both entries appeared untracked after HEAD
  (`07:25:44`, `07:26:04` vs HEAD `07:08:16`) from `ExecApplyEntries`; `SOURCES.md` still has
  zero `S085`–`S089` rows (`ExecRegistryMirror` in flight). Row 2 assumes the registry append
  lands; if it does not, `S088`/`S089` in the row are dangling.
- **F3 (prose-id check passes):** both landed entries bind by document — base cites `S079`
  (RFC 7089) and `S081` (NDL WARP URL renewal); amendment does the same and replaces the staged
  "S095 amendment" pointer with the r36 path. No staged S120–S122/S127/S128 token survives.

## Verdict

The theme is ground the coverage map does NOT hold: the map carries the *instruments* (Memento
stability, WARP timestamp URLs, AVeriTeC field wording, a value-counted archive census) and
records the theme's own entry as rejected, but holds neither the corpus-level durability
mechanism nor the successor-corpus per-citation binding. Two rows are due; one existing row
(README:1063) needs its "not adopted" clause superseded. No production file written by this seat.

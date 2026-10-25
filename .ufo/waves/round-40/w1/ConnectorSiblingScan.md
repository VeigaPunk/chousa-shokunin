# ConnectorSiblingScan — sibling-overlap for receipt provenance, source curation, and calibration

Seat: ConnectorSiblingScan (leaf connector). Round 40 wave 1. Read-only. No production edit, no sibling write, no tool install.

**Assigned attack.** Perform a read-only sibling-overlap scan for receipt provenance, corpus-source curation, and calibration work; report the owning lane for any adjacent surface rather than absorbing it.

**Axes named.** operability, calibration, depth. AXES.md also defines adjacency as "report, never absorb". This wave does not score adjacency, so the routing below is a calibration constraint on the two frozen claims, not a third claim.

**Verdict.** No adjacent surface is absorbed. The three phrases are homonyms. Chousa keeps only its own research-gate receipt bytes, its own `SOURCES.md` row S059, and its own R2–R5 self-assessment dispositions. One real cross-lane fact must stay a scope split, not be reconciled: the Python hashlib URL is shared by chousa S059 (admit, digest-of-bytes) and mori S065 (reject, sole revision-provenance).

## Commands and output

Tool installs: none. Pacman was not used. The host route table was not modified.

### 1. Fleet shared-URL census (hashlib only)

Command:

```
/home/vgpnk/Projects/shokunin/scripts/sources-census.sh shared --root /home/vgpnk/Projects/shokunin | awk -F'\t' 'BEGIN{IGNORECASE=1} $1 ~ /hashlib/ || $0 ~ /hashlib/'
```

Output:

```
docs.python.org/3/library/hashlib.html	shared	mori,chousa
```

The script's `shared` mode is defined at `scripts/sources-census.sh:38` as `url<TAB>shared<TAB>lane,lane,…` for a normalized URL present in at least two lanes. That script is fleet-owned census machinery (`scripts/sources-census.sh:1-7`, contract pointer `CORPUS.md` § SOURCES.md). Chousa does not own it and must not edit it.

### 2. Lane-local S059 cells

Command: a Python walk of every `/home/vgpnk/Projects/shokunin/*-shokunin/corpus/SOURCES.md`, printing the S059 source cell or `ABSENT`.

| Lane | S059 source cell |
|---|---|
| chousa | Python hashlib documentation — https://docs.python.org/3/library/hashlib.html |
| kaidoku | Official sigrok-dumps UART dataset README |
| kake | Render Docs: Docker on Render |
| kama | llama.cpp GGUF reference reader |
| kengaku | RFC 8259 numeric grammar |
| kotoba | opencode — Agent skills |
| kotodama | Swedish Sámi Parliament, Renmärken |
| kumitate | cmux docs, Agent integrations: oh-my-pi |
| mado | host terminal declarations, file bytes |
| mori | git-log(1) — https://git-scm.com/docs/git-log |
| souji | gitattributes `$GIT_DIR/info/attributes` |
| tabi | Playwright launch options |
| tameshi | Remote Caching (Bazel docs) |
| tsukuroi | L1 symlink listing and namespace emulation |
| audio, game-dev-2d, game-dev-3d, kagi, kasegi, lore, revenger | ABSENT |

Mori's hashlib row is **S065**, not S059 (`mori-shokunin/corpus/SOURCES.md:71`). Citing "S059" across lanes points at fourteen different sources.

### 3. Preserved r39 receipts outside the active manifest

Active rows in `corpus/evidence/round40/active-r39-receipts.tsv` all exist (6 files). Receipts under `corpus/evidence/round39/receipts/` and not in that manifest:

- `corpus/evidence/round39/receipts/c1-after-s39011.json`
- `corpus/evidence/round39/receipts/c1-base-s39001.json`
- `corpus/evidence/round39/receipts/c1-mutenv-s39003.json`
- `corpus/evidence/round39/receipts/c1-mutenv-s39013.json`

`c1-mutenv-s39003.json` is still a live C2 input: `corpus/evidence/round40/c2-count.py:60` requires the file, and `routed-defect-dispositions.json` R2 cites it. The other three are named as preserved originals in `corpus/evidence/round39/claims.md:196` and `corpus/knowledge/receipt-expectation-digests-r40.md:15`. Active-manifest exclusion is not absence of a reference.

## Owning lane per adjacent surface

### Receipt provenance — chousa keeps the research-gate binding only

| Surface | Owner | Why it is not this claim |
|---|---|---|
| `expect_sha256` of a research-gate counter receipt, re-checked by `corpus/evidence/round39/verify-receipts.py` and `corpus/evidence/round40/c1-count.py` | **chousa** | C1 predicate. The r40 note already limits it: a matching digest is byte identity of the supplied expectations file, not truth, authority, or authorship (`corpus/knowledge/receipt-expectation-digests-r40.md:13,19`). |
| Receipt-gated **removal** of stale or duplicate artifacts; `pushed` receipts; `refs/jj/keep/*` are not durable receipt roots | **souji** (`souji-shokunin/PROVINCE.md:3-17,25-30`) | Do not hand souji the four preserved r39 receipts. Souji removes lane artifacts only with its own receipt, and only stale generated output with no live references. These four still have live citations. Chousa's kill rule keeps superseded originals outside the active population and preserved (`corpus/evidence/round40/claims.md:9,19`; manifest comment line 2). |
| `.pkg.tar.zst` receipt discipline on pacman state | **tsukuroi** (`tsukuroi-shokunin/PROVINCE.md:8-9`) | OS package receipts. Not a research-gate digest. |
| `tac-check` offline receipt | **kagi**, and the surface is recorded absent (`kagi-shokunin/PROVINCE.md:10-17,37`) | Credential custody. Absence of the binary is not a chousa receipt miss, and chousa must not grow a substitute custody checker. |
| Reusable mutation-testing method; never edits a sibling's gate | **tameshi** (`tameshi-shokunin/PROVINCE.md:14-17`) | This wave's mutation seats attack temporary copies of chousa's verifier. That does not move `tools/research-gate.sh` to tameshi, and a pattern is not general until two independent lanes evidence it. |
| Evidence-ledger discipline for shipped-artifact RE | **revenger** (`revenger-shokunin/PROVINCE.md:3-7`) | Different ledger. Chousa's receipt is a counter-binding file, not an RE evidence id. |

**Contradiction, not a score.** "Receipt" in souji means permission to delete. "Receipt" in chousa C1 means permission to count a row as `VERIFY: ok`. Treating inactive as deletable would harm the preserved-original control and would falsify C2 R2, which requires `c1-mutenv-s39003.json` to remain.

### Corpus-source curation — chousa keeps its own row

| Surface | Owner | Route |
|---|---|---|
| Question, source hierarchy, citation chain, claim-vs-source check | **chousa** (`PROVINCE.md:3-8`, `SKILL.md:8-10`) | Method. `CORPUS.md` rule 3 says `SOURCES.md` must not become a second method. |
| This lane's registry row for hashlib digest semantics | **chousa S059** (`corpus/SOURCES.md:69`) | Re-opened this round. The scope cell already refuses a general SHA-256 text standard, a lowercase-output requirement, and the lane's revision-pin contract. |
| Same URL as sole support for which revision supplied the bytes | **mori S065**, tier C, rejected (`mori-shokunin/corpus/SOURCES.md:71`; `corpus/lessons/round-19.md:43`; re-rejected `corpus/lessons/round-22.md:27`) | Mori's flip is "admit A for narrow hash-call behavior, with separate revision-linkage evidence." Chousa's S059 is that narrow admit in chousa's registry. It does not flip mori's row, and mori's rejection does not flip chousa's. |
| Every other lane's `corpus/SOURCES.md`, including every other S059 | **that lane** | Each child lane curates its own registry (`PROTOCOL.md` `SOURCES.md` row; `CORPUS.md` census). Kumitate names its own registry (`kumitate-shokunin/PROVINCE.md:15`). Tameshi names its own (`tameshi-shokunin/PROVINCE.md:38`). |
| Contract text and `scripts/sources-census.sh` | **fleet / protocol** | Do not restate columns, do not census sibling registries as chousa work, and do not "repair" the shared hashlib hit by editing either row. |
| `SKILL.md` or prompt wording about sources | **kotoba**, if the defect is trigger or skill-file craft | Not this round's registry edit. |
| Fictional source-id resolution and in-world provenance chains | **lore** (CM-05, CM-06) | Not corpus `SOURCES.md`. Kotodama refuses general source-research method and names chousa. |

**Contradiction, not a score.** One URL, two tiers, two ids, two scopes. Collapsing them to one mined or rejected verdict would either over-claim revision provenance (harms calibration and depth) or withdraw the digest source the r40 knowledge entry cites (harms the sourced-claim binding). C1's counter never reads `SOURCES.md` (`claims.md` Separability), so a registry retier would not repair operability either.

### Calibration — chousa C2 is this lane's self-assessment only

| Surface | Owner | Route |
|---|---|---|
| Axis definition: SCORECARD/SHONEN match observed repo state | **fleet `AXES.md:15`**, applied per lane to its own scorecard | Chousa C2 is R2–R5 in `routed-defect-dispositions.json`, re-derived by `c2-count.py`. Evidence paths are chousa files plus `fleet:.ufo/reports/round-39/chousa.md`. |
| Model-quality, judge calibration, `plans/attrib_calibration.py`, `eval-prior-art-calibration.md` | **kengaku** (`kengaku-shokunin/PROVINCE.md:20,116,125-126`) | Chousa `PROVINCE.md:10-11` already refuses model-quality and evaluation claims. |
| Fleet liveness, wave settlement, lane-silence grades | **mori** (`mori-shokunin/PROVINCE.md:3-16`) | Not a SCORECARD mismatch count. |
| Cross-lane defect routing | **integrator / protocol** | This seat only names owners. It does not close a sibling scorecard. |

R4's `not-reproduced` test stays with `ReviewR4RoleMix` and `CriticR4Disposition`. This scan does not re-count roles. `ScoutProvinceBoundary` owns the general province-boundary item; this report only binds the three surfaces in the connector item.

## Proposed move

Keep the hashlib `shared` census line as a standing scope split. Do not add a chousa row that restates mori's rejection, do not edit mori S065, and do not retier either row because the other lane disagrees.

Do not file the four non-active r39 receipts as souji removal candidates. Preservation is part of the frozen C1 claim, and R2's counter still requires `c1-mutenv-s39003.json`.

That is one move. It improves **calibration**: the sourced claim cannot be read as "hashlib proves receipt provenance" or as a fleet-wide S059, and inactive receipts cannot be read as hygiene debris. It does not change `c1-count.py` or `c2-count.py`, so **operability** (the 6/6 byte check) and the C2 4/4 re-derivation stay as frozen. It does not widen the digest note, so **depth** stays the file-byte versus cited-row distinction already written at `receipt-expectation-digests-r40.md:13-19`.

## Risks

- A source seat can "falsify" chousa S059 by quoting mori S065. That quote falsifies only a revision-provenance reading. The r40 Limit section already denies that reading. A real falsifier would show the knowledge entry claiming authorship, truth, or commit identity from the digest.
- A souji census that treats "not in `active-r39-receipts.tsv`" as "no live references" would delete C2's R2 subject and the red-before originals. Live references are listed above.
- A fleet report that says "S059 hashlib" without the lane name cites the wrong source in 13 other lanes.
- kagi's `tac-check` row is historical and the binary is recorded absent. Routing there is ownership, not a live dependency this round can call.
- This scan is not a fifth C2 disposition and must not be counted by `c2-count.py`.

## Verification

Re-run command 1 and expect exactly `docs.python.org/3/library/hashlib.html	shared	mori,chousa`. Re-run command 2 and expect chousa's S059 cell to stay the hashlib page while mori's S059 stays git-log. Confirm the four non-active r39 receipt paths still exist and that `c2-count.py:60` still names `c1-mutenv-s39003.json`. Do not retier rows. Executor seats own the frozen counters; this seat did not re-score them.

## Artifact pointers

- This report: `/home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-40/w1/ConnectorSiblingScan.md`
- Shared-census definition: `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh:38`
- Chousa hashlib scope: `/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/SOURCES.md:69`
- Mori rejection: `/home/vgpnk/Projects/shokunin/mori-shokunin/corpus/SOURCES.md:71`
- Digest limit: `/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/knowledge/receipt-expectation-digests-r40.md:19`
- Active manifest: `/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round40/active-r39-receipts.tsv`
- R2 live reference: `/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round40/c2-count.py:60`
- Calibration axis: `/home/vgpnk/Projects/shokunin/AXES.md:15`

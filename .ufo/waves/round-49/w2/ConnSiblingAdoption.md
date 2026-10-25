# ConnSiblingAdoption — sibling adoption-pattern scan (round-49 w2)

Seat scope: how sibling lanes adopt their `merge/<lane>/` packages under addendum §10; is chousa's `tools/assimilate-rows.py` duplicating a sibling tool, or reusable by siblings? Read-only everywhere except this report; scratch `/dev/shm/chousa-r49-ConnSiblingAdoption` (deleted before handoff). No tool installs performed.

## 1. The §10 contract (verbatim source)
`.ufo/prompts/chousa-round-49.md:440-493` (Assimilation contract) and `:494-513` (scratch transformation):
- id-collision check with the 0–3-space extractor over registry and `SOURCES.append.md`; nonempty `collisions` → renumber **in scratch only, by document — the URL/anchor is the evidence, the id follows it, never arithmetic**; guard must be proven able to fail on an indented `S002` fixture (`:470-493`).
- no staged row appended as-is: normalize recheck to ISO date/`NNd`/cadence with stripped prose recorded in the Gate block; no literal/escaped `|`; `used-by` = exactly the admitted entries; status `mined`; validate a scratch mirror via `sources-census.sh validate --file` before the first append (`:494-513`).
- wave-4 quarantine-first for chousa/tabi/revenger/kotodama (`:529-533`).

## 2. How siblings adopt (artifact pattern)
All lanes use scratch `.ufo/waves/round-N/assimilation/` with one artifact family: `reg-ids`/`staged-ids`/`collisions` (0–3-space extractor + `comm -12`) plus a guard proof, a by-document renumber map, a quarantine slice, and a validate mirror.
- collision check + guard proof: kasegi r24 `corpus/lessons/round-24.md:38-45`; kaidoku r35 `round-35.md:30`; kama r34 `round-34.md:42-48`; kengaku r33 `round-33.md:17-21`; kake r48 `round-48.md:44-51`; mado r37 `round-37.md:68-71`; kotoba r67 `round-67.md:71-72`.
- by-document maps, never arithmetic: kasegi r26 `round-26.md:31`; kama r36 `round-36.md:61`; mado r35 `round-35.md:118-121`; mori r43 `round-43.md:102-105`; kotodama r72 `round-72.md:21-24`; kotoba r70 `round-70.md:45-49`; kumitate r60 `round-60.md:55-57`.
- validate mirror before append: kama r34 `round-34.md:52-58`, r36 `round-36.md:63-69`; kake r48 spotcheck `round-48-verifier-spotcheck.md:66-67` (its r51 lesson records a mirror-name bug at `round-51.md:170-182`).
- quarantine slices/hand-checks: kake r48 `round-48.md:88-93`; kasegi r24 `round-24.md:86-89`.

Committed sibling TOOLS (vs scratch-only recipes):
- **tameshi `tools/staged-id-guard.py`** — pre-adoption guard: identical 0–3-space `ROW_RE` (`:65-66`), URL-keyed document identity (`:99-121`), candidate-map validation (`:180-270`), selftest incl. indented-collision (T1) and held-document (T5) cases (`:280-304`); used r43/r44 (`round-43.md:80-86`, `round-44.md:83-86`).
- **kengaku `plans/sources_adopt.py`** — pre-adoption gate: id-collision (0–3-space anchor), 11-cell schema check, append-block construction with recheck normalization + stripped-prose reporting + `used-by` rewrite, exit map 0/2–9 (`:2-30`, `:43-58`); exercised r29–r31 (`round-29-verifier-spotcheck.md:52-55`, `round-30-verifier-spotcheck.md:99-103`, `round-31.md:64-67`).
- kasegi/kama/kaidoku/kake/mado/kotodama/kumitate/mori: scratch commands/artifacts per round only — no committed adopter tool.

## 3. Does chousa's tool duplicate a sibling tool?
Overlap: guard/collisions = tameshi; append-block builder + recheck normalization + `used-by` rewrite + refusals = kengaku. No sibling tool generates the full artifact family (`append.md` + `renumber.tsv` + `stripped.tsv` + simultaneous entry substitution) in one CLI. So there are now **three parallel implementations** of the same §10 pipeline (chousa, tameshi subset, kengaku subset) — genuine duplication across lanes, not reuse.

## 4. Reusable by siblings? Probe
CLI takes generic paths, writes only under `--out`. Probe on tameshi's real staged package (read-only), guard mode:

```
$ python3 /home/vgpnk/Projects/shokunin/chousa-shokunin/tools/assimilate-rows.py \
    --staged /home/vgpnk/Projects/shokuknow/merge/tameshi/SOURCES.append.md \
    --knowledge /home/vgpnk/Projects/shokunin/tameshi-shokunin/corpus/knowledge \
    --registry /home/vgpnk/Projects/shokunin/tameshi-shokunin/corpus/SOURCES.md \
    --opened 2026-10-25 --out /dev/shm/chousa-r49-ConnSiblingAdoption/tameshi-guard
COLLISIONS=8
EXIT=0
$ cat /dev/shm/chousa-r49-ConnSiblingAdoption/tameshi-guard/collisions
S153
S154
S155
S156
S157
S158
S159
S160
```

Matches tameshi's own r43 record (7 collisions S153–S159, `round-43.md:84`) plus the S160 collision its r44 lesson predicts as already-held (`round-44.md:84`). Guard mode works cross-lane with zero chousa-specific input.
Caveats: (a) `--knowledge` is argparse-required even without `--entry` — omitting it exits 2 (observed in the first probe attempt); (b) append mode assumes the fleet 11-cell schema (true for all lane registries, kake r48 `round-48-verifier-spotcheck.md:63`); (c) URL identity reuses `scripts/sources-census.sh` normalisation, so results are census-consistent.

## 5. Recommendation
No defect: the tool is this lane's C1 deliverable and stays. Report to Main that the §10 pipeline is implemented three times (chousa `assimilate-rows.py`, tameshi `staged-id-guard.py`, kengaku `sources_adopt.py`); promoting one shared builder to `/home/vgpnk/Projects/shokunin/scripts/` would serve all lanes, but that is an operator decision (fleet-repo writes are outside lane scope).

VERDICT: chousa tools/assimilate-rows.py — partly — it duplicates parts of two sibling tools (tameshi guard, kengaku builder) yet is reusable by siblings as-is (cross-lane probe passed), so the finding is consolidation opportunity, not a defect.

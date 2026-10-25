# ExecCollision — section-10 id-collision check, round 50 wave 1

Scope: the staged package `/home/vgpnk/Projects/shokuknow/merge/chousa` (read-only) against the live
lane registry. Write set (exactly): `.ufo/waves/round-50/assimilation/{reg-ids,staged-ids,collisions,guard-proof.txt}`
plus this report. No production file, no git index, no shokuknow write. Scratch `/dev/shm/chousa-r50-ExecCollision/` deleted.

## 1. The exact pipeline, as assigned, and its output

```
S=/home/vgpnk/Projects/shokuknow/merge/chousa
A=/home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-50/assimilation
mkdir -p "$A"
grep -oE '^ {0,3}\|[[:space:]]*S[0-9]{3,}' /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/SOURCES.md \
  | grep -oE 'S[0-9]+' | sort > "$A/reg-ids"
grep -oE '^ {0,3}\|[[:space:]]*S[0-9]{3,}' "$S/SOURCES.append.md" \
  | grep -oE 'S[0-9]+' | sort > "$A/staged-ids"
comm -12 "$A/reg-ids" "$A/staged-ids" > "$A/collisions"
```

| list | lines | first | last |
|---|---|---|---|
| `reg-ids` (corpus/SOURCES.md) | 103 | S001 | S103 |
| `staged-ids` (SOURCES.append.md) | 114 | S082 | S195 |
| `collisions` | **22** | S082 | S103 |

`wc -l` observed: `103`, `114`, `22`. No duplicate ids inside either list (`uniq -d | wc -l` → 0, 0).
The staged file's digest is still the round-49 pinned one: `sha256sum $S/SOURCES.append.md` →
`a6dec4a0086d3cf767d638d7e52fdda08f78d22b0b376049b0ad14ff0f8aa696` (matches the `a6dec4a0…` recorded in
`corpus/lessons/round-49-verifier-spotcheck.md:41`), so this is the same package, re-checked against a grown registry.

## 2. What the 22 collisions actually are

Classified by comparing the URL cell of the registry row and the staged row at the same id:

- **18 hard collisions** (same id, different document): S082–S099.
  e.g. S082 registry `https://raw.githubusercontent.com/MichSchli/AVeriTeC/main/README.md` vs staged
  `https://doi.org/10.1186/s13643-020-01542-z`; S084 registry `…/data/train.json` vs staged `https://www.rfc-editor.org/rfc/rfc7089.txt`.
- **4 duplicate-row collisions** (same id, same URL — a re-staged row, not a new document): S100, S101, S102, S103.
  e.g. S100 both `https://www.zcmu.edu.cn/__local/2/33/FC/FFA702D0F9381C8224BD74CB435_0E777725_C3A00.doc?e=.doc`.

Cause is arithmetic, not accident: `MERGE-REPORT.md:9` states "lane registry currently holds **81** rows; first staged id
is **S082**", but the registry holds **103** rows now. Round-49 recorded `COLLISIONS=14` against base
`414a2ec6:corpus/SOURCES.md` (95 rows, max S095; staged ids ≤ S095 = 14). Round 49 then added S096–S103
(`73ea811` 95 rows → `763b337` 103 rows), so 14 + 8 = **22**. The collision set is exactly
`{staged ids ≤ registry max}`.

## 3. Guard proof (PASS) — `assimilation/guard-proof.txt`

Fixtures in `/dev/shm/chousa-r50-ExecCollision/`: registry copy `| S001 | z |` + two-space-indented `  | S002 | y |`;
staged copy `| S002 | x |`. `cat -A` shows `| S001 | z |$` / `  | S002 | y |$`.

```
guarded  '^ {0,3}\|…' : reg-ids-copy = S001,S002 ; staged = S002 ; comm -12 → S002   (1 line)
column-0 '^\|…'       : reg-ids-copy = S001      ; comm -12 → (empty)                 (0 lines)
```

So the ` {0,3}` allowance is load-bearing: the indented row is caught by the assigned pattern and dropped by `^\|`.
On today's real bytes both patterns agree (both files have zero indented rows: `grep -cE '^ {1,3}\|'` → 0, 0), and
neither file has a 2-digit id (`grep -cE '^ {0,3}\|[[:space:]]*S[0-9]{1,2}[[:space:]]*\|'` → 0, 0), so the counts
above are not an artefact of either blind spot.

## 4. Renumber map I expect (document → lane id)

Registry max is S103 and S104–S107 are free (`grep -cE '^\| S10[4-7] \|' corpus/SOURCES.md` → 0 for each), and none
of the four documents is already held (registry has no hit for `9e5cdd215a414bf6b5694912018de4c8`, `citation-search`,
`rwxy.seu.edu.cn`, `bnu.edu.cn`). Ascending staged id gives:

| document | staged row(s) | lane id |
|---|---|---|
| ISTIC 引证检索 service page — `https://chaxin.las.ac.cn/service/citation-search` | S118 | **S104** |
| CNKI 管理员 manual — `https://gs.sxu.edu.cn/docs/2025-03/9e5cdd215a414bf6b5694912018de4c8.pdf` | S124 = S135 = S180 = S187 (one document, four staged rows, identical URL) | **S105** |
| CNKI 子账号 manual — `https://rwxy.seu.edu.cn/_upload/article/58/cc/5a2fdc1940cfa2522e82ba8b5d81/fb75a598-a343-48f2-bb42-5c6c411506bc.pdf` | S136 | **S106** |
| CNKI 教师 manual — `https://bs.bnu.edu.cn/docs/20160407183946745914.pdf` | S145 | **S107** |

The four rows are 11-cell rows, status `mined`, used-by: S118→`istic-citation-verification-r39.md`,
S124→`cnki-citation-check-r40.md`, S135→`citation-matching-semantics-r41.md`, S136 and S145→`citation-matching-semantics-r41.md`.
S180 and S187 also point at `cnki-citation-check-query-r47.md` and `citation-check-status-vocabulary-r48.md`, so the
single S105 row's `used-by` cell must name all four entries if it is adopted once — the C2 claim names only the three
r39/r40/r41 entries. All five entries exist only in the staged `knowledge/corpus/knowledge/` (none in `corpus/knowledge/`),
consistent with this wave drafting them.

## 5. Second-order hazard: the new ids collide with existing staged ids

The staged file already contains rows **S104, S105, S106, S107, S108** for unrelated material
(S104 护理论文报告质量 paper; S105–S108 the lane's own chain-resolution / citation-chain / exempt-hop / revision-binding
own-work rows). Assigning S104–S107 to the four documents is correct against the registry, but
`MERGE-REPORT.md`'s adopt checklist step 3 says "Append `SOURCES.append.md` to `corpus/SOURCES.md`" — doing that
wholesale would put two rows each at S104, S105, S106, S107 and 22 duplicate ids at S082–S103. Any append must be
row-selective and renumbered; nothing in the staged package may be carried over by its staged id.

## Risks / blockers

- The staged package cannot be appended as-is (22 registry collisions + 5 staged ids equal to the new lane ids). This is
  a packaging-time defect in the *merge report*, not in the frozen claims; C1/C2 predicates are untouched by it.
- `MERGE-REPORT.md:9`'s "81 rows" premise is stale by 22 rows; its `renumbered` list is empty (`first_id: S082`), so the
  package itself offers no renumber map — the map in §4 is mine, derived from the registry maximum.
- No blocker for the lane's own adoption: the four theme rows are collision-free once renumbered to S104–S107.

VERDICT — ran the assigned section-10 collision pipeline (103 registry ids, 114 staged ids, 22 collisions: 18 hard,
4 same-URL duplicate rows) and proved the `^ {0,3}\|` guard catches a two-space-indented row that `^\|` misses
(collisions S002 vs empty); renumber map ISTIC→S104, 管理员(S124/S135/S180/S187)→S105, 子账号→S106, 教师→S107,
with the staged S104–S108 ids flagged as a second-order collision to renumber, not carry over.

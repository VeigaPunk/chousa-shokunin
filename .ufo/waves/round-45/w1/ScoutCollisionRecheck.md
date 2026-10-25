# Scout report — id-collision recheck and renumber-map verification (round 45 w1)

Scout: `L1Chousa45.ScoutCollisionRecheck` (leaf; no dispatch, no fetch, no production writes).
Item: re-run the id-collision check independently; verify the by-document map; report which
documents the strings S082/S083/S084 name in the staged append.

## Files read (absolute paths)
- Registered registry: `/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/SOURCES.md`
- Staged append: `/home/vgpnk/Projects/shokuknow/merge/chousa/SOURCES.append.md`
- Committed wave artifacts: `/home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-45/assimilation/{collisions,reg-ids,staged-ids,renumber-map.tsv}`

## 1. Id-collision check (independent re-run)
Extraction pattern used: `^ {0,3}\|[[:space:]]*S[0-9]{3,}` (row start, optional 0-3 spaces,
`|`, optional space, `S` + 3+ digits). Python `re` (POSIX `[[:space:]]` translated to `\s`).

Verbatim decisive output (Python eval):
```
reg extracted: count 81 unique 81 first/last S001 S081
stag extracted: count 114 unique 114 first/last S082 S195
intersection (reg ∩ staged): []
committed collisions content repr: ''
reg-ids file == extracted unique: True
staged-ids file == extracted unique: True
```

Findings:
- Registered rows (SOURCES.md) hold exactly S001–S081 (81 unique); the file has no S082+ rows
  (last row S081 at SOURCES.md:91).
- Staged rows (SOURCES.append.md) hold exactly S082–S195 (114 unique).
- Intersection = empty. Committed `collisions` is empty — consistent.
- Committed `reg-ids` == extracted registered ids, `staged-ids` == extracted staged ids — the
  committed id lists match a fresh extraction, so the check inputs were current.

## 2. By-document map check (renumber-map.tsv)
Map rows (`staged_id → lane_id → url → bound_by → note`), verified against the staged rows:
| staged_id | lane_id | map URL | staged row contains map URL? |
|---|---|---|---|
| S139 | S082 | `https://raw.githubusercontent.com/MichSchli/AVeriTeC/main/README.md` | True |
| S140 | S083 | `https://arxiv.org/html/2305.13117v3` | True |
| S132 | S084 | `https://raw.githubusercontent.com/MichSchli/AVeriTeC/main/data/train.json` | True |

All three staged rows carry exactly the URL the map names (SOURCES.append.md:64, :65, :57);
`bound_by = url-equality` for all three. **Map holds on all 3 rows.**

## 3. What the strings S082/S083/S084 name in the staged append
- S082 → **PRISMA-S** extension (Rethlefsen et al., Systematic Reviews 10:39), DOI
  10.1186/s13643-020-01542-z (SOURCES.append.md:7).
- S083 → **Cochrane Handbook ch. 4** "Searching for and selecting studies"
  (`https://www.cochrane.org/authors/handbooks-and-manuals/handbook/current/chapter-04`)
  (SOURCES.append.md:8).
- S084 → **RFC 7089** Memento (`https://www.rfc-editor.org/rfc/rfc7089.txt`)
  (SOURCES.append.md:9).

None of these is an AVeriTeC document. The three lane-bound documents are the AVeriTeC
README (S139), the arXiv 2305.13117v3 paper (S140), and AVeriTeC data/train.json (S132).
So the lane ids S082–S084 are assigned by URL/name equality with the AVeriTeC documents, not
by id arithmetic on the staged append's S082–S084 strings — consistent with C3's "bound BY
DOCUMENT" requirement. (Registered lane S079 already holds RFC 7089 since round 44 —
SOURCES.md:89 — hence staged S084 is not bound to lane S079.)

## Verdict
- Id collision check: **no collisions** (registration S001–S081 vs staged S082–S195;
  intersection empty), matching the committed empty `collisions` file.
- Renumber map: **holds** — all three staged rows' URLs equal the map URLs; no row breaks.
- C3 binding semantics: confirmed — staged strings S082/S083/S084 name PRISMA-S, Cochrane
  Handbook ch.4, RFC 7089 respectively, all different from the AVeriTeC documents bound to
  lane ids S082/S083/S084.

## Commands run
1. `grep` (pattern above) on SOURCES.md and SOURCES.append.md — row-id extraction.
2. `read` on `collisions`, `reg-ids`, `staged-ids`, `renumber-map.tsv`.
3. Python eval: full extraction + intersection + comparison of committed id files + per-row
   map URL verification (output quoted above).
No tool installs/updates. No scratch files created (inline eval only); nothing to delete.
No network egress; on-disk sources only.

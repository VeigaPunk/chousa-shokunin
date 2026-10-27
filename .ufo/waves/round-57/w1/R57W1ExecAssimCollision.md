# R57W1ExecAssimCollision — section-10 collision check for the rows R57-C3 will append

Seat: executor (leaf; no dispatch). Lane `/home/vgpnk/Projects/shokunin/chousa-shokunin`, HEAD `e0e73e0` (read-only; dispatch tip `f9736a3` is an ancestor). Base `6656f077`. Scratch `/fast/scratch/hyaku/chousa-r57/R57W1ExecAssimCollision` (`TMPDIR`/`PYTHONDONTWRITEBYTECODE=1` set, **deleted before yield**). No network fetch, no tool install, no git/jj mutation, no write outside this report file — lane `git status --porcelain` shows only the L1's own ` M corpus/evidence/round57/refetch.tsv` and ` D .ufo/waves/round-57/w1.ready.partial`; `/home/vgpnk/Projects/shokuknow` was read-only, never written. Axes: **depth** (measured from real bytes, not remembered numbers) · **calibration** (guard proved, not asserted).

## 1. The recipe, run as written

`S=/fast/scratch/hyaku/chousa-r57/R57W1ExecAssimCollision`, `cd "$S"`, `set -o pipefail`:

```
grep -oE '^ {0,3}\|[[:space:]]*S[0-9]{3,}' /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/SOURCES.md \
  | grep -oE 'S[0-9]+' | sort > "$S/reg-ids"
grep -oE '^ {0,3}\|[[:space:]]*S[0-9]{3,}' /home/vgpnk/Projects/shokuknow/merge/chousa/SOURCES.append.md \
  | grep -oE 'S[0-9]+' | sort > "$S/staged-ids"
comm -12 "$S/reg-ids" "$S/staged-ids" > "$S/collisions"
```

Observed: `reg-ids count: 130 head: S001 tail: S130` · `staged-ids count: 114 head: S082 tail: S195` · `collisions count: 49 head: S082 tail: S130`.

| artifact | sha256 | lines | head → tail |
|---|---|---|---|
| `reg-ids` | `35dbc6b4fe1142ef2354727233f4c5b3fd5433a5a9018586e3d7ee4c94288fe4` | 130 | S001 → S130 |
| `staged-ids` | `9ce3b9c30cd1115797315c6aea6f00fa45b4ff141a9aa630059afe3cc6b8e2f9` | 114 | S082 → S195 |
| `collisions` | `763edf8bff7d74aa33674a9759156cd8fdb60dc7e0590a7136415c536c94f15c` | 49 | S082 → S130 |

`staged-ids` sha256 = the round-56 pin `9ce3b9c3…`; staged file digest = the round-49/50/51 pin `a6dec4a0086d3cf767d638d7e52fdda08f78d22b0b376049b0ad14ff0f8aa696` — the staged package has not moved. `reg-ids` is contiguous S001–S130 with no duplicate ids; `staged-ids` contiguous S082–S195, no duplicates. The L1 wrote **no** `.ufo/waves/round-57/assimilation/` this round (directory absent), so every number here is independently derived.

**Collision output (all 49, verbatim)**

```
S082 S083 S084 S085 S086 S087 S088 S089 S090 S091 S092 S093 S094 S095 S096 S097 S098 S099 S100
S101 S102 S103 S104 S105 S106 S107 S108 S109 S110 S111 S112 S113 S114 S115 S116 S117 S118 S119 S120
S121 S122 S123 S124 S125 S126 S127 S128 S129 S130
```

= the closed interval S082–S130 (49 = 130 − 82 + 1). Against round 56's committed `collisions` (45 lines) the delta is exactly `S127 S128 S129 S130` — the four rows round 56 wrote; the same residual hazard its seat filed (`.ufo/waves/round-56/w1/R56ExecCollision.md` §4.1: lane ids sit inside the staged package's id range). Class split by first source-cell URL: **identity (same id, same document) = 4** — S100 (zcmu.edu.cn CNKI 他引频次 .doc), S101 (jc.hit.edu.cn 数据规范), S102 (toho-shoten.co.jp CNKI KNS8.0), S103 (library.um.edu.cn CNKI AI 使用指南); **numbering-only = 45** (S082–S099, S104–S130). Across the two lists **60 URL-identity pairs** exist (a staged id and a *different* lane id name the same URL), e.g. staged `S157` == lane `S130` (nhc.gov.cn 管理指南（试行）PDF), staged `S185`/`S195` == lane `S118` (bjhea 质量控制指南 2024年版 试行), `S168` == lane `S127` (ttbz 工作流程指南), `S156` == lane `S128`, `S155` == lane `S129`, `S111`/`S133`/`S181` == lane `S113` (medsci PRISMA-S 解读) — the renumber-by-document pairs the lane has recorded since round 43.

## 2. "New ids S131+ must be absent from BOTH lists" — measured: holds on the lane side only

```
S131 in reg-ids: 0 | in staged-ids: 1
S132 in reg-ids: 0 | in staged-ids: 1
S133 in reg-ids: 0 | in staged-ids: 1
S134 in reg-ids: 0 | in staged-ids: 1
S135 in reg-ids: 0 | in staged-ids: 1
S136 in reg-ids: 0 | in staged-ids: 1
S137 in reg-ids: 0 | in staged-ids: 1
```

**Lane side SATISFIED.** Registry max is S130: the `## Registry` section (lines 7–141) holds exactly 130 id rows, first at line 11 `S001`, last at line 140 `S130`, zero duplicate ids; `git show 6656f077:corpus/SOURCES.md` gives the same 130 ids (last S130), so S131+ were free at the base too.

**Staged side NOT SATISFIED and unsatisfiable**: `staged-ids` runs to S195, so *every* candidate new lane id in S131–S195 collides numerically with a staged id by construction. Only ids ≥ S196 would be absent from both lists. This is a naming collision, not a document collision, and it is standing practice. Two measurements settle it:

1. **No candidate URL equals any staged row URL.** Every URL in `corpus/evidence/round57/refetch.tsv` for the round's candidate ids S131–S136 was compared with all 114 staged row URLs: zero identity matches (S131 nhc 2019 通知 page; S132 nhc 2021 通知 page; S133 tcmevidence/forten/nhc-search PDF; S134 hnysfww + nhei PDF; S135 takarabiomed + cpia + hnysfww; S136 takarabiomed + hnysfww + nhei PDF). Staged S131–S136 name entirely different documents (上市药品临床安全性文献评价指导原则 发布 / AVeriTeC train.json / PRISMA-S 解读 / PRISMA 2020 JMLA / CNKI 管理员手册 / CNKI 子账号手册).
2. **The lane numbers onward and resolves by document.** `corpus/lessons/round-50.md`:38 — "the three new ids S104–S106 collide with staged ids **by design**"; round-44 lesson:89 — "S079 is the next free lane id. Not staged-id minus 2."; round-43 lesson:56 — renumber by document, never by arithmetic. Round 56 wrote S127–S130 straight through the staged range and recorded the growth (45 → 49).

**Projection** (if C3 appends S131–S137, the ids the L1's fetch pass already used): `comm -12` → **56** collisions (S082–S137 contiguous); staged-only remainder 114 → 58 (first S138, last S195). Lane ids stay contiguous S001–S137.

## 3. Guard proof — the 0–3-space pattern catches an indented colliding row; column-zero does not

Fixture (mine, in scratch; `guard/registry-fixture-r57.md`, sha256 `ef772adf5a0b614825ae75c21649acc8aee3d516a5f07b40ba15c722cde18621`):

```
  | S131 | indented round-57 candidate row$      <- 2 leading spaces, id staged S131
| S077 | column-zero$                           <- column zero, id NOT staged (S077 < S082)
    | S133 | four-space-must-miss$               <- 4 spaces, must be missed
```

```
$ grep -oE '^ {0,3}\|[[:space:]]*S[0-9]{3,}' guard/registry-fixture-r57.md | grep -oE 'S[0-9]+' | sort
S077
S131
$ grep -oE '^\|[[:space:]]*S[0-9]{3,}'   guard/registry-fixture-r57.md | grep -oE 'S[0-9]+' | sort
S077
$ comm -12 guard/r57-ids staged-ids
S131
$ comm -12 guard/r57-ids-col0 staged-ids
(empty)
```

**Guard proved.** The two-space indented colliding row `  | S131 |` is caught by the 0–3-space pattern (`collisions` = S131) and missed by a column-zero-only pattern (empty). The four-space row S133 is correctly ignored by both (tolerance is 0–3, not indentation-agnostic). A second independent fixture with `  | S155 |` behaves identically (`guard/fixture-ids` sha256 `1516d40e584efac1a62106e8af18efbe1f30659072d7be4cb195979d7243c40b`, `guard/fixture-collisions` = `S155`).

Two calibration points on the **real** files: `grep -cE '^ {1,3}\|[[:space:]]*S[0-9]{3,}'` = **0** in `corpus/SOURCES.md` and **0** in `SOURCES.append.md` (every real id cell sits at column zero, so the 0–3 tolerance is safety margin only the fixture exercises); and the row anchor is load-bearing — `grep -cE '^ {0,3}S[0-9]{3,}'` = **4** prose hits in the registry, while requiring the closing pipe (`^ {0,3}\|[[:space:]]*S[0-9]{3,}[ \t]*\|`) gives **130 / 114 / 49**, byte-identical to the prompt pattern (`cmp` exit 0 on both id files).

## 4. Findings for the L1 (reported, nothing patched)

1. **`S131+` cannot be absent from the staged list** (staged runs to S195). The check that matters is the document one, and it passes: no candidate URL matches any staged row URL. The C3 rows may therefore be numbered S131 onward in the lane's ascending sequence, exactly as S127–S130 were in round 56, with the renumber-by-document rule and the collisions file kept honest (49 now, 56 after seven appends).
2. **Two staged ids already carry C3-relevant documents.** staged `S157` is lane `S130`'s exact URL (the nhc.gov.cn 药品临床综合评价管理指南（试行）PDF — the **2020** text, not the 2021年版 edition R3 requires), and staged `S174/S176/S185/S186/S195` are the 质量控制指南 family lane `S118/S119` already hold. A future R3 binding on the **2021年版** 管理指南 must therefore not be satisfied by S130's 2020 capture; the staged package cannot substitute.
3. **`refetch.tsv` reuses one id across several documents** (S133 for 3 distinct URLs, S135 for 5, S131/S132 for 4 each). The C3 counter keys candidate bindings by `(id, url)` from `refetch.tsv` and by the row's first source-cell URL, so a reused id is tolerable — but any registry row written for S131+ must carry **one** URL in its first source cell, and its `used-by` / `source:` pair must point at that same URL, or the id↔document binding breaks.
4. The C3 counter's `EXCLUDED` set is `{S127, S128, S129}` — **S130 is eligible** as a bound row. S130's document is the 2020（试行）管理指南 and, per the freeze-time checks, its capture lacks the `2021年版` token, so it cannot bind R3; recorded so the L1 does not try to make R3 bind through S130.

## 5. Scratch and hygiene

Scratch `/fast/scratch/hyaku/chousa-r57/R57W1ExecAssimCollision/` held `reg-ids`, `staged-ids`, `collisions`, `reg-ids-base`, `reg-ids-proj`, `guard/`. **Deleted before yield** (`rm -rf`); the numbers above carry sha256 so they can be re-derived. No tool installed or upgraded (coreutils, grep, git, python3 sufficed). No file outside this report was written; no fetch performed; no frozen counter, control or predicate edited.

**VERDICT: the section-10 collision check for R57-C3's pending rows SURVIVED — 49 collisions (S082–S130) from 130 lane ids × 114 staged ids; new ids S131+ free in the lane but numerically inside the staged range (no candidate URL equals any staged row URL); and the 0–3-space guard PROVED on a two-space indented `  | S131 |` row (caught) that a column-zero pattern misses.**

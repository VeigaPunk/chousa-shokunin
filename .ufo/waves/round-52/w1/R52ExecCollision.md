# R52ExecCollision — section-10 id-collision check + guard proof + by-document renumber map

seat: `R52ExecCollision` (leaf; no dispatch, no fetch) · date 2026-10-26 · base `00f8c7f5272a1d98b6d34913985fa4537e00aaf9`
writes: the four files I own in `.ufo/waves/round-52/assimilation/` + this report. Nothing else.
scratch `/fast/scratch/hyaku/chousa-r52/R52ExecCollision/`: created, trapped, removed.

## 1. The check, run verbatim

```
$ S=/home/vgpnk/Projects/shokuknow/merge/chousa; A=/home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-52/assimilation
$ mkdir -p "$A"
$ grep -oE '^ {0,3}\|[[:space:]]*S[0-9]{3,}' .../chousa-shokunin/corpus/SOURCES.md | grep -oE 'S[0-9]+' | sort > "$A/reg-ids"
$ grep -oE '^ {0,3}\|[[:space:]]*S[0-9]{3,}' "$S/SOURCES.append.md"            | grep -oE 'S[0-9]+' | sort > "$A/staged-ids"
$ comm -12 "$A/reg-ids" "$A/staged-ids" > "$A/collisions"
REG count: 112  first: S001  last: S112
STAGED count: 114  first: S082  last: S195
COLLISIONS count: 31
```

| list | lines | first | last | md5 | duplicates (`uniq -d`) |
|---|---|---|---|---|---|
| `reg-ids` | 112 | `S001` | `S112` | `2e99e5ed9f8995b79ed2e991c35cb756` | none |
| `staged-ids` | 114 | `S082` | `S195` | `d91867693dc4b0a4a901922ca8297c22` | none |
| `collisions` | **31** | `S082` | `S112` | `3ec9a23ca22a15030cec4850a07b53b5` | — |

The 31 collisions are contiguous `S082`–`S112`, the whole overlap of the staged range (staged
`S113`–`S195` do not collide with the lane today); `collisions` is `S082 … S112`, one id per line.

Registry maximum is not a grep artefact — same file parsed by the counter's own `registry()`
(`corpus/evidence/round52/c2-count.py:105`, `## Registry` only, 0–3 leading spaces):
`Registry-section rows: 112 min S001 max S112`; `S-rows OUTSIDE the Registry section: 0`;
`unique: 112 dupes: []`; `rows whose cell count != 11: [] total 0`.

## 2. Guard proof (one-time, before this lane's first append)

`assimilation/guard-proof.txt` (md5 `b72f19a219db13488bd9c9cd3bc20eed`), from two scratch fixtures —
a registry copy carrying `  | S002 | y |` (2-space indent) and a staged copy carrying `| S002 | x |`:

```
## indent-tolerant (the mandated pattern)  ^ {0,3}\|[[:space:]]*S[0-9]{3,}
reg ids:    S001 S002
staged ids: S002
collisions: S002
exit: NONEMPTY  (expect NONEMPTY -> S002 caught despite the 2-space indent)
## column-zero pattern ^\|
reg ids:    S001   <- indented S002 row is MISSED
staged ids: S002
collisions: ''
exit: EMPTY  (expect EMPTY: a naively column-anchored grep under-reports)
```

The guard holds in both directions: the mandated pattern catches an indented collision, and a
column-zero pattern would false-green it — the proof §10 asks for before anything appends.

## 3. Renumber map, BY DOCUMENT (staged → lane), ascending staged id from max `S112`

| document | staged | lane | counter doc URL (`DOCS :66-76`, `url_of :95`) | `cell[1]` must lead with | `used-by` must equal |
|---|---|---|---|---|---|
| 梅斯医学 PRISMA-S 解读 (中国循证医学杂志) | `S111` | **`S113`** | `www.medsci.cn/guideline/show_article.do?id=23e481c0052069d3` | `https://www.medsci.cn/guideline/show_article.do?id=23e481c0052069d3` | `corpus/knowledge/chinese-prisma-s-reception-r52.md` |
| 中国全科医学 PRISMA2020 条目清单 | `S112` | **`S114`** | `www.chinagp.net/CN/column/item185.shtml` | `https://www.chinagp.net/CN/column/item185.shtml` | `corpus/knowledge/chinese-prisma-s-reception-r52.md` |
| 国立保健医療科学院 `Reporting_Format_Jap_202404.docx` | `S125` | **`S115`** | `c2h.niph.go.jp/tools/system/Reporting_Format_Jap_202404.docx` | `https://c2h.niph.go.jp/tools/system/Reporting_Format_Jap_202404.docx` | `corpus/knowledge/japanese-search-record-niph-form-r52.md` |
| 日本語 PRISMA 2020 チェックリスト, archive copy | `S129` | **`S116`** | `web.archive.org/web/2024/https://www.lifescience.co.jp/yk/jpt_online/prisma/list_1.pdf` | **`https://web.archive.org/web/2024/https://www.lifescience.co.jp/yk/jpt_online/prisma/list_1.pdf`** — not the dead original | `corpus/knowledge/japanese-prisma-item-wording-r40.md` |

By document, not arithmetic: offsets are `+2, +2, −10, −13`. Two of the four (`S111`, `S112`)
collide today; all four renumber because ids continue the registry maximum. `S113`–`S116` are free
(`grep -cE '^ {0,3}\|[[:space:]]*S11[3-6][[:space:]]*\|' corpus/SOURCES.md` → 0).

Row-shape constraints read off the frozen counter; all four staged rows already pass the cell count
(`cells: 11`, no `|`/`\|` in any title): `len(r)==11` and `url_of(r[1])==url_of(doc)` (`:171`),
`r[7]=="mined"`, `r[8]=="2026-10-26"` (`OPENED`), `sorted(r[10].split(","))==citing` (`:174`), and
`source: <lane-id> — <doc URL>` verbatim in each citing entry (`:175`). Two in-place rewrites are
therefore needed: `[8]` reads `2026-10-23` on all four, and `used-by` names the *routing* entries,
not the C2 ones — `S111`/`S112` → `corpus/knowledge/chinese-search-log-r37-amendment-2026-10-23.md`,
`S125` → `corpus/knowledge/japanese-search-record-r38-amendment-2026-10-23.md`; only `S129`
already names `corpus/knowledge/japanese-prisma-item-wording-r40.md`.

## 4. No lane id — twin rows for a URL that already has its one row

| staged | URL / key | why no id | harm if appended anyway |
|---|---|---|---|
| `S133` (**asked**) | first URL identical to `S111` (`url_of` equality) | same document as the `S113` row | `hits` = 2 → `len(hits)==1` fails (`:171`), so the document is **neither bound nor refused** → `nbound+refused==4` fails → `C2=FAIL` |
| `S181` | same medsci URL | same document, tier-C publication record | same double-hit |
| `S138` | `www.lifescience.co.jp/…/list_1.pdf` (original) | same document as `S116` (its own text: both archives are one file, sha256 `ba9bc9c1…`) | no hit at all (see measurement), yet a second row for one document |
| `S137`, `S146` | `web.archive.org/web/timemap/link/…`, `web.archive.org/cdx/search/cdx?…` | metadata endpoints, not the document; different `url_of` keys | binds an endpoint as a source |

Measured by importing the counter (`url_of`):

```
DOC url_of ARCHIVE : web.archive.org/web/2024/https://www.lifescience.co.jp/yk/jpt_online/prisma/list_1.pdf
S111 cell[1] matches MEDSCI : True    S112 cell[1] matches CHINAGP: True
S125 cell[1] matches NIPH   : True
S129 cell[1] matches ARCHIVE: False   (it is the ORIGINAL: www.lifescience.co.jp/…/list_1.pdf)
S138 cell[1] vs ARCHIVE     : False
S137 -> web.archive.org/web/timemap/link/https://…/list_1.pdf
S146 -> web.archive.org/cdx/search/cdx?url=www.lifescience.co.jp/…/list_1.pdf&output=json
```

`ALIASES` (`:78`) rescues the dead original only for the register/theme scan (`:241`), never for the
bound leg — so `S116`'s source cell must carry the literal `web/2024/` URL. The staged entry already
does (`japanese-prisma-item-wording-r40.md` line 4).

## 5. Risks handed to the L1 (id surface only; nothing here is my call)

1. **Blocker-class:** staged `japanese-prisma-item-wording-r40.md` line 33 carries `S097`
   ("attachment (round 3's `S097`)") — the FEVER dataset, a different document. `REF_ID_UNBOUND`
   counts every non-bound `S\d{3,}` in the three entries and must be 0 (`:185`, `:275`), so that
   token must be re-pointed by document or rephrased; no renumber map can fix it.
2. Every id-bearing artefact follows the map, never the staged id: entry `source:` lines, the
   `spans.tsv` `staged-id` column (compared to `bound` keys, `:206`), `char N` anchors, `held`/
   `BODYONLY` bookkeeping. Round-51 §6.2 (adopter twin-id `held` label) is outside this seat: it
   concerns a renumber run, which I did not perform.
3. **Forward:** after this round the lane maximum is `S116`, so staged `S113`–`S116` (FEVER,
   climate-fever, CorFEVER, 动物实验) collide for any later adoption — renumber in scratch then.

## VERDICT

Ran §10 and proved the guard: 31 collisions (`S082`–`S112`) between a 112-row registry (max
`S112`) and 114 staged ids; the 2-space fixture collides while column-zero false-greens empty;
four documents map by document to `S113`/`S114`/`S115`/`S116`; `S133` (with `S181`, `S138`,
`S137`, `S146`) gets no lane id; `S129`'s row must lead with the `web/2024/` archive URL.

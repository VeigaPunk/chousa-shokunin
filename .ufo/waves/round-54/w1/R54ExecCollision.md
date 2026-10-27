# R54ExecCollision — Section-10 id-collision check with guard proof

seat: `R54ExecCollision` (executor, leaf) · lane: chousa · round 54, wave 1 · date: 2026-10-26
scope: re-derive the L1's four assimilation files independently and `cmp` them; prove the
Section-10 collision guard on a scratch fixture; state the renumber map by document; verify
the held S101 row by URL byte for byte.
scratch: `/fast/scratch/hyaku/chousa-r54/R54ExecCollision` (removed on exit).
Only file written under the lane: `.ufo/waves/round-54/assimilation/guard-proof.txt`
(plus this report). No production file, no other seat's report, no git index, no jj state,
no write to `/home/vgpnk/Projects/shokuknow`. No network, no LibreOffice run, no tool install
(the whole seat needed only `grep`, `awk`, `comm`, `cmp`, `sha256sum`, `python3`).

## 1. Independent re-derivation — all four L1 files reproduce byte for byte

Commands (the prompt's Section-10 commands; my own output dir):

```
grep -oE '^ {0,3}\|[[:space:]]*S[0-9]{3,}' /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/SOURCES.md \
  | grep -oE 'S[0-9]+' | sort > "$OUT/reg-ids"
grep -oE '^ {0,3}\|[[:space:]]*S[0-9]{3,}' /home/vgpnk/Projects/shokuknow/merge/chousa/SOURCES.append.md \
  | grep -oE 'S[0-9]+' | sort > "$OUT/staged-ids"
comm -12 "$OUT/reg-ids" "$OUT/staged-ids" > "$OUT/collisions"
awk -F'|' -v l='chousa' '$2 ~ ("`" l "`") && $3 ~ /round[0-9]+/ && $4 ~ /S[0-9]+/ {print $4, $5}' \
  /home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/absent-defect-register.md \
  > "$OUT/quarantine-slice"
```

Observed (fresh run, then `cmp` against the L1's files in
`.ufo/waves/round-54/assimilation/`):

```
  cmp OK: reg-ids
  cmp OK: staged-ids
  cmp OK: collisions
  cmp OK: quarantine-slice
 120 .../v-reg-ids
 114 .../v-staged-ids
  39 .../v-collisions
  24 .../v-quarantine-slice
```

sha256 (identical pairs, mine = L1's):

```
a875bed3894761e4fced68f3acb9aed8b5ca32d3cfebd8138c8b992ac0f08521  reg-ids
9ce3b9c30cd1115797315c6aea6f00fa45b4ff141a9aa630059afe3cc6b8e2f9  staged-ids
b605b00c48e5f9a9d89615dee937d4bbdd80612ca61f0e52bb4463bbf60f3eb4  collisions
1ec5a29fb97afc5a334282e48b41bc3dd59312f0c7e85c37b60f77b392a464be  quarantine-slice
```

**`collisions` is nonempty (39 ids, S082…S120)** — so the staged package must be renumbered in
scratch before any append. Registry ids are S001…S120, contiguous, no duplicates (120 ids,
min 1, max 120, missing `[]`); staged ids are S082…S195 (114). The live lane registry has
**zero** rows with 1–3 leading spaces (`grep -cE '^ {1,3}\|' corpus/SOURCES.md` → 0), so the
guard's tolerance is currently unexercised by the live file — the fixture below is what
makes it load-bearing before the first append.

Quarantine slice: 24 chousa data rows, exactly as the L1 wrote them; the three on theme URLs
are register `S080` (SAMR record, round1), `S088` (JMU copy, round2), `S096` (HIT
specification, round2). I re-derived the counter's own register→theme mapping and it yields
the same three: `reg_ids = ['S080','S088','S096']`.

## 2. The guard, proved

Fixture exactly as the seat spec words it — a registry copy with a two-space-indented
`  | S002 | y |` row and a staged copy with `| S002 | x |`:

```
--- registry-copy (cat -A):
  | S002 | y |$
--- staged-copy (cat -A):
| S002 | x |$
```

**Pattern A — the prompt's extractor `^ {0,3}\|[[:space:]]*S[0-9]{3,}`:**

```
reg-ids:      S002
staged-ids:   S002
collisions:   S002      (5 bytes, nonempty)
```

**Pattern B — the old column-zero-only extractor `^\|`:**

```
reg-ids.zero:      (empty, 0 bytes)
staged-ids.zero:   S002
collisions.zero:   (empty, 0 bytes)
```

The 0–3-space extractor gives a **nonempty** `collisions`; the column-zero-only pattern gives an
**empty** one. The guard behaves as the prompt states.

**Why this matters (the load-bearing part).** The census parser
`/home/vgpnk/Projects/shokunin/scripts/sources-census.sh` `row_pass()` matches rows with 0–3
leading ASCII spaces — line 615 `if (line !~ /^ {0,3}\|/) next`, line 616
`sub(/^ {0,3}/,"",line)` — so an indented row *is* a registry row to the census. On a
two-row fixture with the duplicate indented:

```
$ bash .../sources-census.sh validate --file ".../census3/corpus/SOURCES.md"
file    ok      .../census3/corpus/SOURCES.md                       exit=0
$ bash .../sources-census.sh validate --file ".../census3/corpus/SOURCES-with-indented.md"
file    E03     S002 duplicate id                                   exit=1
```

Indent boundary on the same fixture: E03 fires at indent 1, 2 and 3 and **not** at 4 — the
0–3-space extractor matches the census's own tolerance exactly. A column-zero-only extractor
would have shipped a duplicate-id registry row past the census.

Full transcript pasted into the lane file I was allowed to write:
`.ufo/waves/round-54/assimilation/guard-proof.txt`.

## 3. Renumber map, by document

Registry maximum is **S120**; S121/S122/S123 are free today (all three confirmed absent from
the 120 ids). The three new documents take the next three ids, in the order the two entries
cite them — the map is re-pointed **by document** (the URL is the evidence, the id follows it),
never by arithmetic:

```
staged id -> lane id    document                                     first source-cell URL
S085      -> S121       GB/T 7714-2025 record, 全国标准信息公共服务平台  https://std.samr.gov.cn/gb/search/gbDetailed?id=4507EFE13D37CB6AE06397BE0A0A601F
S086      -> S122       GB/T 7714-2025 在线预览 notice, openstd        http://openstd.samr.gov.cn/bzgk/std/newGbInfo?hcno=C6CE52E55AC09B9C79A20AEA77CEDD14
S093      -> S123       GB/T 7714-2025 full-text copy, 集美大学学报      https://xuebaobangong.jmu.edu.cn/zkb/Upload/Park/64b9ba1b-df55-4309-87d4-0d037a497bd0.pdf
```

All three staged ids are members of the 39-id collision set, so each **must** be renumbered.
None of the three URLs (or their hosts) is already registered in the lane registry —
`grep -c` for `std.samr.gov.cn`, `openstd.samr.gov.cn`, `xuebaobangong.jmu.edu.cn` in
`corpus/SOURCES.md` → 0, 0, 0 — so no E04 duplicate-URL conflict is in the way.

**S101 is HELD, verified by URL byte for byte:**

```
lane   S101 url: https://jc.hit.edu.cn/_upload/article/files/f7/54/711916924125a0682e3bc3ebb6ed/1f6f2731-8c87-4812-b7e2-9fad0069d508.doc
staged S101 url: https://jc.hit.edu.cn/_upload/article/files/f7/54/711916924125a0682e3bc3ebb6ed/1f6f2731-8c87-4812-b7e2-9fad0069d508.doc
byte-equal: True
sha256 lane  : 6dc68fd6b32ce9c8dfcebce84434d86a92e9841caad388b59986dba15eb0cdf4
sha256 staged: 6dc68fd6b32ce9c8dfcebce84434d86a92e9841caad388b59986dba15eb0cdf4
len lane/staged: 119 119
```

Same URL, same id → **staged S101 is not renumbered; the lane id stays S101**. Its staged row
still differs from the lane's in five cells:

| cell | lane S101 | staged S101 |
|---|---|---|
| anchor | `section 11 (文献标志码), section 14.1 and 14.4 (参考文献) and the 15.7 parameter table (UTF-16LE text of the raw .doc capture); located quotes char 11170, char 11205, char 11993, char 12161, char 13247, char 34374` | `section 11 (中图分类号与文献标志码) and section 14 (参考文献, 参考文献著录项目, 参考文献类型及其标志); document read 2026-10-23` |
| teaches | `…includes 文献类型及载体类型标志; section 14.1 recommends the GB/T 7714 顺序编码制 or 作者…` | `…includes 文献类型及载体类型标志 and 文献出处或电子文献的可获得地址, and the reference format is 参照 GB/T 7714 in either 顺序编码制 or 作者-出版年制…` |
| opened | `2026-10-25` | `2026-10-23` |
| recheck | `180d` | `180d — re-download the document and confirm section 14.2 still lists nine 著录项目 beginning with 主要责任者 and 文献题名 (ran 2026-10-23)` |
| used-by | `corpus/knowledge/citation-count-semantics-r37.md` | `corpus/knowledge/source-type-taxonomy-r37.md, corpus/knowledge/citation-count-semantics-r37.md` |

The staged `used-by` cell already names `corpus/knowledge/source-type-taxonomy-r37.md`; the
lane's cell does not. So if the r37 entry cites S101, the **held row's `used-by` must gain
`corpus/knowledge/source-type-taxonomy-r37.md`** — that is the old→new `used-by` update the
lesson must record (the C2 counter's `HELD_BAD` leg reads exactly this). Note the lane's
`used-by` is the *only* cell of the lane's S101 row that must change; the anchor's
`UTF-16LE text of the raw .doc capture` offsets are a separate, already-routed defect
(round-49 anchors in an undefined form) and are **not** mine to re-point here.

## 4. Findings the L1 must act on

1. **Stale `S075` token in the staged r37 entry — it will fail the counter.** The staged
   `source-type-taxonomy-r37.md` line 70 reads *"The authority's own portal serves no text for
   采标 standards (wave 1's `S075`)"*. `S075` is neither a bound id (S121/S122/S123) nor the
   held S101, so the C2 counter's `ID_RE = re.compile(r"\bS\d{3,}\b")` scan counts it in
   `REF_ID_UNBOUND` (I reproduced the counter's own scan on the staged text: r36 → `['S085',
   'S086']`, r37 → `['S093', 'S075']`; after the planned renumbering the first two become
   bound, but `S075` stays unbound). Worse, in the *lane* `S075` is a real, unrelated row —
   the GNU coreutils `mktemp(1)` manual — so carrying the token over silently mis-cites.
   The staged token means the campaign's own **wave-1** id for the openstd record: the
   campaign's wave-1 draft has `| S075 | GB/T 7714-2025 openstd record [5] | A | Chinese | the
   copyright boundary that makes the standard's text unreadable |`
   (`shokuknow/lanes/chousa/.deepresearch/20261023_172027_chousa-corpus-expansion/final_turn_001.md:19`),
   which the merge package renumbered to S086 (`shokuknow/lanes/chousa/ID-REMAP.md:17`,
   `| round1 | S083 | S086 |`). **The drafted lane entry must cite the openstd notice by its
   new lane id S122** (or drop the numeric token), never S075 and never the staged S086.
   This is a rename inside the new entry, not a change to any frozen predicate.

2. **Forward drift: S121/S122/S123 are already taken *inside the staged package*.** The staged
   package's own ids S121/S122/S123 name three *other* documents — FEVER dataset release
   page (S121), FEVER Zenodo record (S122), Bramer et al. "A systematic approach to searching"
   (S123). Nothing appends them this round (CORPUS.md rule 4: only rows a cited entry cites),
   but any later round that adopts them must renumber them past S123. I measured the effect
   of this round's own appends on the collision file: adding S121/S122/S123 to the registry
   takes `collisions` from 39 to 42 (the three newly colliding ids are exactly S121, S122,
   S123). The renumber map above is therefore only valid *after* this round's three rows land
   — the L1 should re-run the guard check with the updated registry before the append.

3. **The staged `S093` scope cell carries a dangling `S075` too** — staged
   `SOURCES.append.md:18` scope reads "…the authority serves no text (see S075), so this row
   is scoped to the reproduction and not to the standard". Same stale wave-1 token: in the
   lane it must point at the openstd notice's lane id **S122**. (The staged package contains
   no S075 row at all — its ids start at S082 — so the reference is unresolvable inside the
   package too.) The `used-by` cell of staged S093 names no entry, and staged S085/S086/S093
   each split into exactly 11 cells with no literal or escaped `|`, so no cell needs rewriting
   for the census beyond the S075 token.

4. **The three staged rows' `used-by` cells are empty/unusable as-is** (they name campaign
   paths, not lane paths) — the L1's hand-normalisation must set them to the lane entry paths
   `corpus/knowledge/source-type-taxonomy-r36.md` (for S121, S122) and
   `corpus/knowledge/source-type-taxonomy-r37.md` (for S123), matching what the counter
   requires (`used == citing`, `c2-count.py:171`).

## 5. What I did not touch, and what remains for the L1

- I did not renumber anything, did not modify `corpus/SOURCES.md`, did not draft the entries
  or the rows, and did not touch the frozen C1/C2 predicates, counters, controls or the
  registry — findings only.
- The held S101 row's `used-by` cell, the three new registry rows, the two entries and the
  lesson's quarantine verdict lines for register `S080`/`S088`/`S096` are the L1's to land.
- The quarantine verdicts for the three theme rows are still unlanded: the C2 counter's
  `QUARANTINE_VERDICTS` leg needs one canonical
  `register \`S0xx\` (round<N>) — <url> — verdict: <v> — <evidence>` line per register id
  (`VERDICT_RE` in `c2-count.py:82`); I confirmed the three ids the counter will look for
  are exactly S080, S088, S096.
- Not run (outside my seat): the C1/C2 counters, LibreOffice, the census on the real
  append block, `inference-ground.py`. The census was run only on scratch fixtures and read
  only on the live registry (baseline: `ok` + 5 W04, exit 0).

VERDICT: re-derived the L1's four Section-10 files independently and they are byte-identical
(cmp OK ×4, sha256 matched); proved the collision guard live on a scratch fixture (0–3-space
pattern → nonempty `collisions` = S002, column-zero pattern → empty, and the census's own
E03 fires at indent 1–3 only); fixed the renumber map by document (S085→S121, S086→S122,
S093→S123, S101 held with a byte-identical URL) and reported two defects the L1 must fix —
the stale `S075` token in the staged r37 entry and the staged package's own use of
S121/S122/S123 — without changing any frozen predicate, counter or target.

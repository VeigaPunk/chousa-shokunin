# R51ExecCollision — section-10 id-collision check, staged package vs lane registry

Seat: leaf executor, chousa r51 w1. Wrote only `.ufo/waves/round-51/w1/R51ExecCollision.md` and the four
assimilation artifacts below. No installs (none needed); no network; every source is the on-disk staged
package and lane registry.

## 1. The check, run exactly as assigned

```
S=/home/vgpnk/Projects/shokuknow/merge/chousa; A=/home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-51/assimilation; mkdir -p "$A";
grep -oE '^ {0,3}\|[[:space:]]*S[0-9]{3,}' /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/SOURCES.md | grep -oE 'S[0-9]+' | sort > "$A/reg-ids";
grep -oE '^ {0,3}\|[[:space:]]*S[0-9]{3,}' $S/SOURCES.append.md | grep -oE 'S[0-9]+' | sort > "$A/staged-ids";
comm -12 "$A/reg-ids" "$A/staged-ids" > "$A/collisions"
```
Observed: `wc -l` → reg-ids **106**, staged-ids **114**, collisions **25**.

- reg-ids first/last: `S001 … S106`; `cmp` against `seq -f 'S%03g' 1 106` → `CONTIGUOUS-1-106` (no gaps, so the
  registry maximum is S106 and the next free id is S107).
- staged-ids first/last: `S082 … S195`; `cmp` against `seq -f 'S%03g' 82 195` → `CONTIGUOUS-82-195`
  (114 unique ids; no staged id repeats).
- collisions first/last: `S082 … S106` — the whole overlap `S082..S106`, 25 ids.
- Both registries carry exactly two non-id table rows (header at lane SOURCES.md:9 / staged :5, separator at
  :10 / :6); table rows total 108 / 116, so id counts 106/114 are consistent and no header leaked in.

## 2. Guard proof (fixture in /dev/shm/chousa-r51-R51ExecCollision/, copied into guard-proof.txt)

Fixture: `reg-fixture.md` = `# fixture registry` / `## Registry` / `| S001 | a |` / `  | S002 | y |` (S002
indented two spaces); `staged-fixture.md` = `| S900 | x |` / `| S002 | x |` (column zero).

```
A) pattern ^ {0,3}\|[[:space:]]*S[0-9]{3,}
   reg: S001 S002   staged: S002 S900   collisions: [S002] count=1
B) pattern ^\|[[:space:]]*S[0-9]{3,}
   reg: S001        staged: S002 S900   collisions: []     count=0
C) same fixture through tools/assimilate-rows.py → stdout COLLISIONS=1, fk-out/collisions = [S002]
```
So the 0–3-space tolerance is load-bearing (B loses the indented row and reports a false clean), and the
candidate tool's own splitter behaves like A, not B. Full text: `.ufo/waves/round-51/assimilation/guard-proof.txt`
(19 lines, 890 B).

## 3. Tool agreement (`--cites` default, no `--entry`)

```
python3 .../tools/assimilate-rows.py --staged $S/SOURCES.append.md --knowledge $S/knowledge \
  --registry .../corpus/SOURCES.md --opened 2026-10-25 --out /dev/shm/chousa-r51-R51ExecCollision/out
→ COLLISIONS=25   EXIT=0
```
`cmp` of the three outputs against mine: `collisions` **IDENTICAL**, `reg-ids` **REG IDENTICAL**,
`staged-ids` **STAGED IDENTICAL** (byte sizes 125/530/570 on both sides). My grep and the tool's D2 splitter
agree on this package, indentation included.

## 4. What the 25 collisions actually are (classification, not just a count)

The staged numbering space starts at S082, inside the lane's occupied range, so the collision set is a
numbering overlap, not 25 documents counted twice. Comparing the source cell of each colliding id:

- **3 identity collisions — same document on both sides**: `S100`, `S101`, `S102` (identical title string,
  identical URL, same kind/tier: 中国知网他引频次查询方法说明 / 中国学术期刊（光盘版）检索与评价数据规范 /
  CNKI KNS8.0 利用ガイド). A merge must **dedupe these to one row**, not add a second row for the same document.
- **22 numbering collisions — same number, different document**, e.g.
  - `S082` lane = AVeriTeC dataset README / staged = PRISMA-S extension paper
  - `S085` lane = FEVER (2018) dataset release page / staged = GB/T 7714-2025 参考文献著录规则
  - `S105` lane = 知网学位论文学术不端行为检测系统使用手册（管理员）/ staged = chousa chain-hop resolution entry (own-work)
  - `S106` lane = “中国知网” 大学生论文管理系统使用手册（子账号）V5.0 / staged = chousa citation-chain fidelity entry (own-work)
  Each of these staged ids must be **renumbered before it can enter the lane**; carrying one over verbatim
  would silently attach staged content to an unrelated lane document.

## 5. Renumber map for the seven documents (registry maximum S106, ascending staged id)

| document (C2 list) | staged id | lane id | staged row |
|---|---|---|---|
| J-STAGE article, 日本健康教育学会誌 32(2):120-121 (喜屋武 享) | S109 | **S107** | SOURCES.append.md:34 |
| JAOHFA PRISMA 2020 別紙様式 (V)-4/(V)-5, 機能性表示食品 届出資料 | S110 | **S108** | SOURCES.append.md:35 |
| 实验动物与比较医学 2025;45(4):496-507 (郑卿勇 等), doi 10.12300/j.issn.1674-5817.2025.017 | S116 | **S109** | SOURCES.append.md:41 |
| 实验动物与比较医学 2025;45(1):101-111 (李腾飞 等), doi 10.12300/j.issn.1674-5817.2024.109 | S117 | **S110** | SOURCES.append.md:42 |
| SinoMed record ui=2026335073 (PRISMA-S 解读) | S119 | **S111** | SOURCES.append.md:44 |
| NIPH C2H Reporting_Format_Jap_202404.docx | S125 | **S112** | SOURCES.append.md:50 |
| 日本保健医療行動科学会雑誌 38(1) vol38_1_5.pdf (剱持・岡) | S126 | **S113** | SOURCES.append.md:51 |

Ordering is the ascending staged id (109,110,116,117,119,125,126) mapped onto 107+index; `grep -cE '^ {0,3}\|S(10[789]|11[0-3])\b'` on the lane registry returns **0**, so S107–S113 are all free. None of the
seven URLs occurs anywhere in the lane registry (checked by URL set membership), so all seven are genuinely
new rows and the map needs no dedupe step.

## 6. Body-only id collisions inside the three staged entries (the other half of section 10)

`source:` lines of the three entries cite only S109/S110 (r38:4-5), S116/S117/S119 (r39:4-6), S125/S126
(amendment:4-5). Six id occurrences in the bodies are body-only, and every one of them lands on a lane row of
a different document:

| entry:line | id cited | lane row that number names | referent the sentence describes |
|---|---|---|---|
| japanese-search-record-r38.md:54 | S105 | 知网学位论文学术不端 检测手册（管理员） | the lane's own claim/gate separation — `corpus/knowledge/claim-support-test-r37.md` (→ `claim-support-states-r24.md`); **no staged row and no lane row exists**, so file path only |
| chinese-search-record-r39.md:55 | S097 | J-STAGE 出版社向け Citation リンク機能 | the functional-foods notification form = staged **S110 → lane S108** |
| …amendment-2026-10-23.md:50 | S097 | as above | same form ("the functional-foods notification form (round 3's `S097`), which files 検索者 on a separate attachment") → **S110 → S108** |
| …amendment…:56 | S105 | 知网 管理员手册 | "Round 4's Chinese reporting module … requires 灰色文献の検索と記録" = staged **S116 → lane S109** (S116's teaches cell carries 是否手工检索、是否检索灰色文献) |
| …amendment…:72 | S105 | 知网 管理员手册 | same module → **S116 → S109** |
| …amendment…:72 | S106 | 知网 大学生论文管理系统手册（子账号）V5.0 | "the Chinese review's own published record" = staged **S117 → lane S110** (r39:61 describes S117 identically: databases, date range, term combination) |

Note the internal drift: the amendment numbers the Chinese review S106 while r39 numbers the same paper S117,
and the amendment numbers the functional-foods form S097 while it is S110 — the same stale-id family that makes
these six occurrences unsafe to carry. Recommended fix at integration: replace each with the lane id in the
right-hand column, or (for the r38:54 own-work reference) with the file path, since no registry row covers it.

## 7. Artifacts written (exactly four, all under the assimilation dir)

`reg-ids` 106 lines/530 B · `staged-ids` 114 lines/570 B · `collisions` 25 lines/125 B · `guard-proof.txt`
19 lines/890 B. Scratch `/dev/shm/chousa-r51-R51ExecCollision/` deleted after these outputs were pasted.

## Risks / blockers

- The 25-collision count is a property of the staged numbering space starting at S082: a re-run after the
  seven rows are renumbered must still show 25 unless the staged file itself changes.
- I did not renumber or edit the staged package or the lane registry; §5 and the referent column in §6 are
  proposals for the L1. I ran no build/lint/test.

VERDICT: built the section-10 collision check (106 reg / 114 staged / 25 collisions, byte-identical to the
candidate tool's own output) with a proven indentation guard (A count=1 vs B count=0), and attacked it into a
classification — 3 identity collisions to dedupe, 22 numbering collisions to renumber, plus six body-only
citations that would bind staged text to unrelated lane rows; the seven documents map cleanly onto free
S107–S113.

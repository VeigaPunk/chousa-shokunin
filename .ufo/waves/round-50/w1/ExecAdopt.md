# ExecAdopt — round 50 w1: adopter on the three admitted entries (as-staged vs body-ids-stripped)

Seat ExecAdopt (leaf). Read `skill://godspeed`, `/home/vgpnk/.omp/agent/RULES.md`; no tool installed or upgraded (pacman paused, untouched). Scratch `/dev/shm/chousa-r50-ExecAdopt/` used and removed (`ls -d` → "No such file or directory"). Inputs read-only (staged package, lane `corpus/SOURCES.md`); only lane write is this report.

## 1. Runs (exact commands, observed output)

```
python3 /home/vgpnk/Projects/shokunin/chousa-shokunin/tools/assimilate-rows.py \
  --staged /home/vgpnk/Projects/shokuknow/merge/chousa/SOURCES.append.md --knowledge /home/vgpnk/Projects/shokuknow/merge/chousa/knowledge \
  --registry /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/SOURCES.md --opened 2026-10-25 --out /dev/shm/chousa-r50-ExecAdopt/out1 \
  --entry corpus/knowledge/cnki-citation-check-r40.md --entry corpus/knowledge/citation-matching-semantics-r41.md --entry corpus/knowledge/istic-citation-verification-r39.md
COLLISIONS=22 · CITED=7 APPEND=6 HELD=1 · EXIT=0
# run 2, identical flags except: --knowledge /dev/shm/chousa-r50-ExecAdopt/know2 --out /dev/shm/chousa-r50-ExecAdopt/out2
COLLISIONS=22 · CITED=5 APPEND=4 HELD=1 · EXIT=0
```

## 2. Run 1 (as staged): body cross-reference ids become rows

```
staged_id	lane_id	action	url
S109	S104	append	www.jstage.jst.go.jp/article/kenkokyoiku/32/2/32_320208/_pdf/-char/ja
S111	S105	append	www.medsci.cn/guideline/show_article.do?id=23e481c0052069d3
S118	S106	append	chaxin.las.ac.cn/service/citation-search
S124	S107	append	gs.sxu.edu.cn/docs/2025-03/9e5cdd215a414bf6b5694912018de4c8.pdf
S135	S107	held	gs.sxu.edu.cn/docs/2025-03/9e5cdd215a414bf6b5694912018de4c8.pdf
S136	S108	append	rwxy.seu.edu.cn/_upload/article/58/cc/5a2fdc1940cfa2522e82ba8b5d81/fb75a598-a343-48f2-bb42-5c6c411506bc.pdf
S145	S109	append	bs.bnu.edu.cn/docs/20160407183946745914.pdf
```
append.md row heads (`id | first 60 chars of source cell`):
```
S104 | システマティックレビューの基礎（喜屋武 享）— 日本健康教育学会誌 32(2):120-121 — https://ww
S105 | 系统评价/Meta分析中文献检索报告清单（PRISMA-S）解读（郑卿勇）— 梅斯医学 指南・解读指南, from 中国
S106 | 引证检索（论文收录引用检索）服务说明 — 中国科学院文献情报中心 科技查新检索服务平台 — https://chaxin
S107 | 知网学位论文学术不端行为检测系统使用手册（管理员）— 中国知网, copy hosted by 山西大学 — https
S108 | “中国知网” 大学生论文管理系统使用手册（子账号）(V 5.0, 2014-03-10) — CNKI 科研诚信管理系统
S109 | “中国知网”大学生论文管理系统使用手册（教师）(mirror: 北京师范大学) — CNKI 科研诚信管理系统研究中心
```
stripped.tsv:
```
lane_id	column	stripped
S104	recheck	365d — re-download the PDF and confirm the contiguous run その日時，使用した検索式を同時に記録しておく is unchanged (ran 2026-10-23)
S104	opened	2026-10-23
S104	used-by	corpus/knowledge/japanese-search-record-r38.md
S105	recheck	180d — re-open the page and confirm the 简要介绍 still names the 16 条目 and the 中文数据库 challenge (ran 2026-10-23)
S105	opened	2026-10-23
S105	used-by	corpus/knowledge/chinese-search-log-r37-amendment-2026-10-23.md
S106	recheck	90d — re-open the service page and confirm the self-citation note still reads 按合作者排除自引标准统计他引次数 (ran 2026-10-23)
S106	opened	2026-10-23
S107	recheck	180d — re-download the PDF and confirm 6.1 引文核对 still reads "状态共分为三种类型" (ran 2026-10-23)
S107	opened	2026-10-23
S108	recheck	180d — re-download the manual and confirm the strings 引文核对 and 匹配 still occur zero times in its extracted text (ran 2026-10-24)
S108	opened	2026-10-24
S109	recheck	180d — re-download the manual and confirm 引文核对 still occurs zero times in its extracted text (ran 2026-10-24)
S109	opened	2026-10-24
```
Ids appended **for body cross-references**: `S109→S104` (J-STAGE Japanese paper), `S111→S105` (梅斯医学 PRISMA-S) — two full `mined` rows, `used-by` = the entry that only mentions them in prose. Entry tokens after run 1: `cnki: S076 S104 S105 S107` · `r41: S107 S108 S109` · `r39: S106`, i.e. "round 4's `S109`–`S111`" now reads as two lane ids of other documents and `S076` passes through unchanged (lane `corpus/SOURCES.md:86` `S076` = GNU `sed(1)` manual, not the J-STAGE row the sentence means).

## 3. Run 2 (body-only ids stripped, every `source:` line kept)

Two replacements in the scratch `cnki-citation-check-r40.md`, each asserted `count==1`; `source:` counts unchanged (`cnki 1, r41 3, r39 1`): `(round 4's \`S109\`–\`S111\`)` → `(round 4's evidence-insufficiency rows in \`corpus/knowledge/claim-support-test-r37.md\`)` (that file carries the FEVER third-state rows, `claim-support-test-r37.md:3,13,14`); `the same question wave 1's \`S076\` raised about J-STAGE` → `… \`corpus/knowledge/aggregator-vs-source-r36.md\` raised about J-STAGE` (J-STAGE matching at that file `:27-40`). Remaining token set before substitution: `['S124']`.
```
staged_id	lane_id	action	url
S118	S104	append	chaxin.las.ac.cn/service/citation-search
S124	S105	append	gs.sxu.edu.cn/docs/2025-03/9e5cdd215a414bf6b5694912018de4c8.pdf
S135	S105	held	gs.sxu.edu.cn/docs/2025-03/9e5cdd215a414bf6b5694912018de4c8.pdf
S136	S106	append	rwxy.seu.edu.cn/_upload/article/58/cc/5a2fdc1940cfa2522e82ba8b5d81/fb75a598-a343-48f2-bb42-5c6c411506bc.pdf
S145	S107	append	bs.bnu.edu.cn/docs/20160407183946745914.pdf
```
```
S104 | 引证检索（论文收录引用检索）服务说明 — 中国科学院文献情报中心 科技查新检索服务平台 — https://chaxin
S105 | 知网学位论文学术不端行为检测系统使用手册（管理员）— 中国知网, copy hosted by 山西大学 — https
S106 | “中国知网” 大学生论文管理系统使用手册（子账号）(V 5.0, 2014-03-10) — CNKI 科研诚信管理系统
S107 | “中国知网”大学生论文管理系统使用手册（教师）(mirror: 北京师范大学) — CNKI 科研诚信管理系统研究中心
```
```
lane_id	column	stripped
S104	recheck	90d — re-open the service page and confirm the self-citation note still reads 按合作者排除自引标准统计他引次数 (ran 2026-10-23)
S104	opened	2026-10-23
S105	recheck	180d — re-download the PDF and confirm 6.1 引文核对 still reads "状态共分为三种类型" (ran 2026-10-23)
S105	opened	2026-10-23
S106	recheck	180d — re-download the manual and confirm the strings 引文核对 and 匹配 still occur zero times in its extracted text (ran 2026-10-24)
S106	opened	2026-10-24
S107	recheck	180d — re-download the manual and confirm 引文核对 still occurs zero times in its extracted text (ran 2026-10-24)
S107	opened	2026-10-24
```
All four rows 11 cells, `status=mined`, `opened=2026-10-25`, recheck `90d/180d/180d/180d`, no `cellN-pipe` row. Substituted `source:` lines (C2's `source: <id> — <url>` shape holds): `r41:2 source: S105 — https://gs.sxu.edu.cn/docs/2025-03/9e5cdd215a414bf6b5694912018de4c8.pdf — \`# 6.1 引文核对\``; `r41:3 source: S106 — https://rwxy.seu.edu.cn/_upload/article/58/cc/…fb75a598-a343-48f2-bb42-5c6c411506bc.pdf`; `r41:4 source: S107 — https://bs.bnu.edu.cn/docs/20160407183946745914.pdf`; `cnki:4 source: S105 — https://gs.sxu.edu.cn/…de4c8.pdf`; `r39:4 source: S104 — https://chaxin.las.ac.cn/service/citation-search`. Entry tokens: `cnki [S105]` · `r41 [S105, S106, S107]` · `r39 [S104]`.

## 4. Does the map equal ISTIC S104 / 管理员 S105 (S124 append, S135 held) / 子账号 S106 / 教师 S107?

**Run 2: yes, exactly.** Registry maximum verified `S103` (`grep -oE '^\| S[0-9]+' corpus/SOURCES.md | grep -oE '[0-9]+' | sort -n | tail -3` → `101 102 103`), so the four documents start at S104 with no arithmetic shift; `S180`/`S187` (uncited here) share the same URL and would map `held` to the same id. **Run 1: no — shifted by two**: the unstripped body ids take S104/S105, giving ISTIC S106, 管理员 S107, 子账号 S108, 教师 S109 and admitting two unrelated documents. Stripping is what makes the map equal the plan, not cosmetics.

## 5. Used-by of the S105 row (管理员): observed vs required

Observed: `corpus/knowledge/cnki-citation-check-r40.md` — the S135 user is dropped, because `users` is computed only for the **appended** id (`assimilate-rows.py:322`, inside `if action != "append": continue`); the held id never contributes. Run 1 has the same defect at S107. Must be: `corpus/knowledge/citation-matching-semantics-r41.md, corpus/knowledge/cnki-citation-check-r40.md` (sorted). Consequence: `c2-count.py:157-167` groups the five `DOCS` pairs by URL so the 管理员 `citing` = both entries and the bound test is `used == citing`; with the tool's cell `nbound=3`, `refused=0`, and the accept test `nbound + refused == len(by_doc)` (`:262`) is `3 == 4` → **C2=FAIL as emitted**. The cell must be widened at integration.

## 6. Second undeclared loss on the same merge: tier and scope

The merged row takes the appended staged row's cells only. Staged `S124` is `tier B`, scope "what CNKI's own 引文核对 feature actually checks, and the three states it can report…"; `S135` is `tier A`, scope "**for CNKI's own 引文核对 matching behaviour** — how the feature decides that a pasted citation corresponds to a r…". Run 2's S105 row carries B and S124's scope/anchor/teaches; S135's tier upgrade and sharper scope are discarded, and `stripped.tsv` records neither `tier` nor `scope`, so the loss is invisible in the tool's own audit. The docstring's "Named limit" names only used-by; this is a second limit to report.

## 7. Pass-through ids the staged file does not hold

`S076` survives run 1 unchanged and is absent from `renumber.tsv` (`cited` is filtered by `t in staged`). `S119`, `S149`, `S170` occur **zero times** in these three entries; the body-only ids actually present are `S076`, `S109`, `S111`. `c2-count.py:71` has `HELD: set[str] = set()`, so any carried-over `S076` makes `unb>0` and fails C2.

## 8. Supplemental operability checks (tool's own gate; no judgement of C1)

`python3 tools/assimilate-rows.py --selftest` → `FIXTURES_SHA256=c5c56480e9f6a08d6a2077b6a11267a4cabf0bc0d3f726408a9bb0238283cd43`, `SELFTEST=PASS findings=26 expected=26`, exit 0. Determinism: run 2 into a fresh `out3` → `diff -r out2 out3` clean; run 2 into the existing `out2` → clean (`IDENTICAL after overwrite`).

## 9. What the L1 must do at integration

Take run 2's four rows, not run 1's six; hand-set S105 `used-by` to both entries (§5, or C2 cannot pass); decide and record the 管理员 tier/scope between S124 (B) and S135 (A) instead of inheriting B silently (§6); keep `S076`/`S109`/`S111` out of the entry bodies, describing them by lane path as the scratch copy does (§7); file run 2's `stripped.tsv` as the Gate block.

VERDICT — ran the adopter twice on the three admitted entries: the by-document map equals ISTIC S104 / 管理员 S105 (S124 append, S135 held) / 子账号 S106 / 教师 S107 only after the body-only ids are stripped (as staged it is shifted by two and admits two unrelated documents), and the S105 row's observed used-by is `corpus/knowledge/cnki-citation-check-r40.md` where it must be `corpus/knowledge/citation-matching-semantics-r41.md, corpus/knowledge/cnki-citation-check-r40.md`, with the held row's tier-A/scope cells also lost.

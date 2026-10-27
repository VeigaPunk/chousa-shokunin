# R53ExecCollision — section-10 id-collision check, census guard, renumber map

seat `R53ExecCollision` (chousa round 53, wave 1), 2026-10-26. Scope: the section-10 id-collision
census of the staging package against the lane registry, its guard proof, and the BY-DOCUMENT
renumber map for the five C2 documents. No predicate treated as changeable; no c1/c2 counter leg run;
no production file, no git/jj mutation, no network; nothing installed; shokuknow read-only. Writes:
`assimilation/{reg-ids,staged-ids,collisions,guard-proof.txt}` + this report; scratch removed after
the seat, every cited output pasted below first.

## 1. The assigned census (run verbatim; `S` = package, `A` = assimilation dir)
```
grep -oE '^ {0,3}\|[[:space:]]*S[0-9]{3,}' .../corpus/SOURCES.md | grep -oE 'S[0-9]+' | sort > "$A/reg-ids"
grep -oE '^ {0,3}\|[[:space:]]*S[0-9]{3,}' $S/SOURCES.append.md  | grep -oE 'S[0-9]+' | sort > "$A/staged-ids"
comm -12 "$A/reg-ids" "$A/staged-ids" > "$A/collisions"
```
```
REG: 116  STAGED: 114  COLL: 35
reg first/last: S001 / S116 | staged first/last: S082 / S195 | collisions first/last: S082 / S116
```
`wc -l`: 116 / 114 / 35 (collisions contiguous S082..S116). Registry matches are lines 11–126, all
inside `## Registry` (7..127), so the whole-file pattern is safe here; the adopter's own census on the
real inputs prints `COLLISIONS=35` (§4), agreeing with `comm`.

## 2. Guard proof (`guard-proof.txt`, pasted whole; scratch fixture removed)
```
fixtures
  reg.md    = "# fixture registry\n## Registry\n\n| id | source | kind |\n|---|---|---|\n| S001 | a | docs |\n  | S002 | y | docs |\n   | S003 | z | docs |\n    | S004 | w | docs |"
  staged.md = "# fixture staged\n\n| S002 | x | docs |"

PAT_A = ^ {0,3}\|[[:space:]]*S[0-9]{3,}   (the section-10 census pattern)
  reg-ids    = S001 S002 S003
  staged-ids = S002
  collisions = S002   (n=1)  <- the two-space-indented registry row DOES collide
  boundary: S004 at four leading spaces is matched by neither pattern

PAT_B = ^\|[[:space:]]*S[0-9]{3,}   (column-zero only)
  reg-ids    = S001
  staged-ids = S002
  collisions =   (n=0)  <- the indented row is missed, collision lost

tool on the same pair (no --entry):
  python3 tools/assimilate-rows.py --staged staged.md --knowledge . --registry reg.md --opened 2026-10-26 --out tool-out
  stdout: COLLISIONS=1  exit=0
  tool reg-ids=S001 S002 S003 | staged-ids=S002 | collisions=S002
```
The 0–3 bound is load-bearing (4 spaces escapes both patterns) but bites nothing live: every row line
in both files starts at column 0 (`grep -oE '^ *\|' | sort | uniq -c` → 118/116 rows, zero-indent).

## 3. What the 35 collisions are (document identity, not just ids)
`python3` over both files with the tool's first-URL semantics:
```
collisions 35
same-document-same-id: 4                  S100 S101 S102 S103
different-document, doc held elsewhere: 18 S084 S087 S088 S089 S092 S094 S095 S097 S098 S099
                                          S109 S110 S111 S112 S113 S114 S115 S116
different-document, doc NOT held: 13      S082 S083 S085 S086 S090 S091 S093 S096 S104 S105 S106 S107 S108
```
31 of 35 colliding ids name a different document across the two files (0 of 35 row tails
byte-identical); 44 staged rows in all re-stage documents the registry already holds —
`CITED=2 APPEND=0 HELD=2 TWIN=0 exit=0`, `S084 S079 held www.rfc-editor.org/rfc/rfc7089.txt`,
`S087 S096 held support.nii.ac.jp/ja/cir/manual_articles_detail`; an id never names a document (§5).

## 4. Renumber map for the five documents, BY DOCUMENT
Registry maximum S116 (line 126), next free **S117**; cited staged ids ascend S134 < S185 < S186 < S190
< S193 < S195. Observed, not assumed — adopter run with `--staged $PKG/SOURCES.append.md --knowledge
$PKG/knowledge --registry corpus/SOURCES.md --opened 2026-10-26` and the three round-53 entries
(`corpus/knowledge/{search-tracking-record-r40,western-instrument-alignment-r50,quality-control-guideline-issued-text-r48}.md`):
```
COLLISIONS=35
CITED=6 APPEND=5 HELD=0 TWIN=1
BODYONLY=3
exit=0
S134  S117  append  jmla.pitt.edu/ojs/jmla/article/download/1449/2061
S185  S118  append  www.bjhea.org.cn/ueditor/php/upload/file/20250115/1736907153935975.pdf
S186  S119  append  m.bjhea.org.cn/35/202501/1126.html
S190  S120  append  pharmwyp.com/posts/56814/…20190618_NMPA_…%882019%E5%B9%B4%E7%AC%AC27%E5%8F%B7%EF%BC%89.pdf
S193  S121  append  training.cochrane.org/handbook/current/chapter-04
S195  S118  twin    www.bjhea.org.cn/ueditor/php/upload/file/20250115/1736907153935975.pdf
```
| lane id | document | staged id(s) | action |
|---|---|---|---|
| S117 | JMLA PRISMA 2020/PRISMA-S common-questions paper (JMLA 110(2):253-257) | S134 | append |
| S118 | issued 质量控制指南（2024 年版 试行）PDF (bjhea.org.cn host) | S185 = row, S195 = twin | append + twin |
| S119 | release notice 《…》发布, m.bjhea.org.cn/35/202501/1126.html | S186 | append |
| S120 | pharmwyp copy of the 2019 NMPA notice (通告 2019年第27号) | S190 | append |
| S121 | Cochrane Handbook ch.4 (training.cochrane.org host) | S193 | append |

Uncontested: no registry row carries `bjhea`, `质量控制指南` or `chapter-04` (grep count 0 / no
match) and `HELD=0`, so only the twin rule shares an id. `used-by` is lane-relative only with
`--knowledge <pkg>/knowledge` (`S118 used-by: corpus/knowledge/quality-control-guideline-issued-text-r48.md,
corpus/knowledge/western-instrument-alignment-r50.md`); `--knowledge <pkg>` instead mints
`knowledge/corpus/knowledge/…` (`c1-count.py:303-305` uses the correct shape).

## 5. Collision-path probes on the real files (fixture entries in scratch, real registry+staged)
- (a) colliding id, document unheld (`source: S082 — https://doi.org/10.1186/s13643-020-01542-z`) →
  `CITED=1 APPEND=1`, `S082 S117 append`, entry rewritten to `S117`. Adopts correctly.
- (b) colliding id, document held elsewhere (`source: S116 — <staged S116 url>`): `CITED=1 APPEND=0
  HELD=1`, `S116 S109 held` — adopts nothing, as designed.
- (c) colliding id with a URL matching neither side (`source: S082 — https://example.org/third`):
  `CITED=0 APPEND=0`, **exit 0**, entry unchanged, only `WARN …: body-only id S082 is also a lane id
  and reads as that row` (+ `bodyclash.tsv`) — a header citation silently adopts nothing, no refusal.
- Real run's untouched body tokens `BODYONLY=3` (S094/S114/S130): `bodyclash` warns S094/S114, which now read as lane S094 (Improving Explainable Fact-Checking…) and S114 (中国全科医学 报告清单), not the staged rows the entry means; S130 has no lane row and warns nothing.

## Risks / notes for the L1 (reported, not patched)
1. 31 cross-document id collisions: citing any staged id ≤ S116 rests on URL equality, and probe (c)'s silent mode (exit 0, WARN only) is outside every frozen C1 leg as its docstring states.
2. Twin row built from the ascending-first staged row: S118 carries S185's scope/anchor/teaches;
   S195's scope (“search-and-selection quality control and the instruments it names”) and `指标 4`
   anchor are dropped; `used-by` does merge both entries.
3. S190's pharmwyp URL also sits at staged S144/S177 (a later citation becomes a twin of S120); the two
   Cochrane ch.4 hosts (staged S083 `www.cochrane.org`, cited S193 `training.cochrane.org`) stay
   distinct under the census URL identity; registry S004/S008 hold ch.24/ch.2 — no accidental `held`.
4. Staged S105–S108 name lane-local artifacts with no http(s) URL, so they can never be adopted by the
   URL-keyed path; none is cited this round.

VERDICT: ran the section-10 census (116 registry / 114 staged / 35 collisions, S082–S116, all
cross-file id reuse and 31 of them different documents), proved the guard (0–3-space pattern catches
a two-space-indented row, column-zero loses it, 4-space escapes), and confirmed BY DOCUMENT the map
S134→S117 (JMLA), S185→S118 with S195 twin→S118 (issued 质量控制指南), S186→S119 (release notice),
S190→S120 (pharmwyp NMPA copy), S193→S121 (Cochrane ch.4) — collision handling correct, retained
defects: the silent no-adoption path and the dropped twin scope text.

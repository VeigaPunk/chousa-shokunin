# Round 49 lesson

author: chousa L1 (hyaku run 7, `ChousaR49`)
date: 2026-10-25
base: `414a2ec6cde05a921dbdd9e02e7ae56b0db647ef`
freeze: `fe740e7838b338d17fec9338c909557e6e7fed7d`

No external fetch or network egress: L0 `8d77e6c1` remains open. Every source
re-opened below is an on-disk capture under the read-only campaign cache
`/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache`,
accessed 2026-10-25. This is the lane's first package-adoption round under
addendum section 10 (round 48 completed quarantine-first). C1 is plumbing; C2
is ground (QUALITY 64).

## Mistakes

| class | evidence pointer | captured-by | fix |
|---|---|---|---|
| A held-out label accepted on charity, then quoted verbatim as a measured figure | `corpus/lessons/round-47-verifier-spotcheck.md:29` accepted a05 as an over-refusal ("exit-level 3/12 incl. a05"); `corpus/lessons/round-48.md:34` quoted that line into the S095 Gate block; `corpus/lessons/round-48-verifier-spotcheck.md:43,46` ruled the a05 label false (W1 `DraftMistake.md`, `SweepA05.md`) | none — quote-fidelity rules check that a quote is in its source, not that the quoted figure is true | `corpus/evidence/round49/a05-check.py`: every lesson line carrying `3/12` with `a05` (and not the true `2/12 (p03, p04)`) must be named, with the true figure, in this lesson's Mistakes/Spot-check intake. Before the intake corrections below: `UNCORRECTED round-47-verifier-spotcheck.md:29`, `UNCORRECTED round-48.md:34`, exit 1; after: exit 0. |
| A span-quote counter that accepts a hollow quote (L1 freeze design, this round) | W1 `CritForgeC2.md` §1: a single-space quote, a whole-capture span and one self-consistent `char N` anchor pass every structural leg of the frozen `c2-count.py` (`C2=PASS` on a scratch root with zero re-grounding); the round-47 C3 counter shares the shape | QUALITY 60 (cheapest gate that scores full marks without the work) should have caught it before the freeze; it was not run against a hollow-quote control | `corpus/evidence/round49/quote-substance-check.py` (QUALITY 72): per id no quote under 3 non-space characters, at least one quote of 12 or more, and no span wider than its quote plus context. On the CritForgeC2 shape (single-space quote, 5000-char span) it prints `HOLLOW_QUOTE`, `OVERWIDE_SPAN`, `NO_SUBSTANTIVE_QUOTE`, exit 1; on this round's manifest `IDS=8 QUOTES=28 FAILURES=0`, exit 0. The frozen C2 counter is unchanged; the substance floor is reported beside it, not folded into it. |
| A fixed-input capability counter cannot tell a mechanism from a replay of its outputs | W1 `CritForgeC1.md`: a tool that replays the real tool's golden outputs for the pinned package passes `c1-count.py` (`C1=PASS`) with no adoption logic; same class as round-48's name-keyed control | QUALITY 60 again; the round-48 lesson named the class for C1 polarity but the round-49 freeze did not add a perturbed-input leg | Reported as the C1 counter's named limit. Supplementary, non-frozen evidence that the mechanism generalises: W1 `ExecToolMoreSets.md` (three entries outside the frozen sets, census ok on each mirror) and the W2 perturbed-package probes. A future capability counter carries a perturbed-input leg (QUALITY 72 note). |
| A criterion pointer naming a lesson row that does not exist | `corpus/QUALITY.md` criterion 69 ends "`corpus/lessons/round-48.md` Mistake 4"; that lesson's Mistakes table has two unnumbered rows at every revision (W1 `ExecQualityWindows.md`) | none | Pointer correction appended to criterion 69 (it rests on the round-48 `## Spot-check intake` rows 1–3). |

## Spot-check intake

| round-48 routed item | round-49 disposition |
|---|---|
| 1. a05 mislabel correction | Correction (append-only; the verifier spot-checks are not lane-owned): `round-47-verifier-spotcheck.md:29` and `round-48.md:34` carry "exit-level 3/12 incl. a05" — the true false-refusal count of the R47 tool on that set is 2/12 (p03, p04), and a05's refusal was correct (round-48 closure ruling (a)). `round-47-verifier-spotcheck.md:35`'s "2–3/12" reads 2/12 for the same reason. `SCORECARD.md:2545` already carries the dispute; the round-49 SCORECARD section states the ruling. `python3 corpus/evidence/round49/a05-check.py` → exit 0. |
| 2. P2 narrowing cost | QUALITY 69 gains the Named-limit sentence: the R48 two-word P2 look-back passes a plain denial whose negator sits three words before the affirmed stem; the frozen R48 set does not count that class. Demonstrated by W1 `DraftP2Limit.md` (a05 and an independent three-before denial both rc=0 under `tools/inference-ground.py`; a two-before control rc=1). No tool change this round. |
| 3. Uncommitted working-copy edits | `corpus/QUALITY.md`'s inherited criterion-69 sentence is true as written (W1 `ExecQualityWindows.md`: eight window probes at the stated inclusive boundaries) and lands under this round. The three R40/R41 JSON leftovers (two swarm registries re-rendered on 2026-10-24, a round-41 `cells.json` overwritten by a control-gate run on 2026-10-25 06:36) were reverted to the committed bytes; their pre-revert diffs are kept in `.ufo/waves/round-49/inherited/`. |
| 4. S093 quote hygiene | Kept visible: S093 is not on this round's theme and nothing citing it was adopted. |
| 5. W1 role-split floor | W1 of round 49 carries 2 connectors and 17 scribes beside the attack seats. |
| 6. SHONEN conversion for the operator | Unchanged; the report's SHONEN lines keep resolvable pointers. |

## Gate

Theme: **a citation index's data is a derived artefact** (source hierarchy:
aggregator versus source). Package `merge/chousa/` (read-only; `SOURCES.append.md`
sha256 `a6dec4a0…`). Two entries admitted with narrowing, one staged document
refused, two same-theme package entries not adopted.

### Collision check (section 10, 0–3-space pattern, scratch)

`reg-ids` 95 ids (S001–S095), `staged-ids` 114 ids; `comm -12` → 14 collisions:
S082 S083 S084 S085 S086 S087 S088 S089 S090 S091 S092 S093 S094 S095
(`.ufo/waves/round-49/assimilation/{reg-ids,staged-ids,collisions}`). Guard
proof: a scratch registry with an indented `  | S002 |` row and a staged `| S002 |`
row gives `collisions` = S002 with the 0–3-space pattern and an empty file with the
column-zero pattern (`.ufo/waves/round-49/assimilation/guard-proof/`). Renumbering by
document with `tools/assimilate-rows.py` (scratch `.ufo/waves/round-49/assimilation/adopt-final/renumber.tsv`,
NCPSSD refused before the run):

| staged id | lane id | URL |
|---|---|---|
| S087 | S096 | https://support.nii.ac.jp/ja/cir/manual_articles_detail |
| S088 | S097 | https://www.jstage.jst.go.jp/static/pages/ForPublishers/TAB2/-char/ja |
| S089 | S098 | https://www.jstage.jst.go.jp/static/pages/FAQs/TAB2/-char/ja |
| S092 | S099 | https://eric.ed.gov/?id=EJ1372738 |
| S100 | S100 | https://www.zcmu.edu.cn/__local/2/33/FC/FFA702D0F9381C8224BD74CB435_0E777725_C3A00.doc?e=.doc |
| S101 | S101 | https://jc.hit.edu.cn/_upload/article/files/f7/54/711916924125a0682e3bc3ebb6ed/1f6f2731-8c87-4812-b7e2-9fad0069d508.doc |
| S102 | S102 | https://www.toho-shoten.co.jp/export/sites/default/cnki/help/cnki-kns80.pdf |
| S103 | S103 | https://library.um.edu.mo/upload/databases/c1b0fa89e2809581b12c79b9c60ea1af.pdf |

The staged S100–S103 land on the same numbers by document, not by arithmetic.
The staged citation-count entry's ground line cited a campaign-era id that names
the lane's GNU sed manual row; it is re-pointed by document to S096.

### Re-opened sources (access 2026-10-25; captures written 2026-10-23; no fetch)

Every quote is byte-exact and occurs exactly once in its capture text form; the
two OLE `.doc` captures are read as the UTF-16LE text of the `.raw` file (their
`.txt` sidecars are lossy). Spans: `corpus/evidence/round49/spans.tsv`, derived by
`build-spans.py` from `quotes.tsv`.

| lane id | capture (form) | offset | located quote |
|---|---|---|---|
| S096 | `09fc63de41f293d43d631c46.txt` (.txt; sha256 `374d7dacf95c…`) | char 3599 | CiNii Researchの「参考文献」は、実際の論文の参考文献と必ずしも一致していません |
| S096 | `09fc63de41f293d43d631c46.txt` (.txt; sha256 `374d7dacf95c…`) | char 3707 | 参考文献数も、論文での掲載数ではなく同定・統合された分をカウントしています。 |
| S096 | `09fc63de41f293d43d631c46.txt` (.txt; sha256 `374d7dacf95c…`) | char 3752 | CiNii Researchでは、CiNii Articlesとは 文献の収録範囲が異なっており |
| S096 | `09fc63de41f293d43d631c46.txt` (.txt; sha256 `374d7dacf95c…`) | char 3801 | （それに伴って）別の手法で同定・統合処理を行っているため |
| S096 | `09fc63de41f293d43d631c46.txt` (.txt; sha256 `374d7dacf95c…`) | char 3577 | 随時増加していきます。 |
| S097 | `167e9db7dde3c998838e3469.txt` (.txt; sha256 `ba7b2aa64899…`) | char 2760 | J-STAGEが連携している外部サービス に登録されている引用文献および被引用文献には、J-STAGEでの記事公開から数日～2週間後にDOIによるリンクが作成されます |
| S097 | `167e9db7dde3c998838e3469.txt` (.txt; sha256 `ba7b2aa64899…`) | char 2607 | DOIがURLとして使用できるようになるには、J-STAGEでの公開から1日～数日程度かかります。 |
| S098 | `fea98dc5a5a486c988dd415c.txt` (.txt; sha256 `ead3a7dd4ba9…`) | char 29482 | システムが引用元の所在を特定できた文献にリンクを付与しています |
| S098 | `fea98dc5a5a486c988dd415c.txt` (.txt; sha256 `ead3a7dd4ba9…`) | char 29641 | 引用元の所在確認は、次の順で解析・検索を実施しています |
| S098 | `fea98dc5a5a486c988dd415c.txt` (.txt; sha256 `ead3a7dd4ba9…`) | char 29672 | 1.DOI（メタデータ項目） をもとに検索　例：10.xxxx |
| S098 | `fea98dc5a5a486c988dd415c.txt` (.txt; sha256 `ead3a7dd4ba9…`) | char 29749 | 3.引用文献の原文情報からDOIを検出して検索 |
| S098 | `fea98dc5a5a486c988dd415c.txt` (.txt; sha256 `ead3a7dd4ba9…`) | char 29775 | 4.引用文献の原文情報を書誌情報に解析して検索 |
| S099 | `32d1d24b24fce96d2a078ec0.txt` (.txt; sha256 `0288da6eab57…`) | char 1235 | leaving an unfamiliar website to search the open Web before investing attention in the site at hand |
| S099 | `32d1d24b24fce96d2a078ec0.txt` (.txt; sha256 `0288da6eab57…`) | char 1483 | Using a matched control design, students in treatment classrooms (n = 271) were compared to peers (n = 228) in regular classrooms. |
| S099 | `32d1d24b24fce96d2a078ec0.txt` (.txt; sha256 `0288da6eab57…`) | char 1694 | grew significantly in their ability to judge the credibility of digital content |
| S100 | `b539a80218080da56a75b624.raw` (.raw UTF-16LE; sha256 `46d1866ce9af…`) | char 1296 | 中国知网他引频次的查询需要使用《中国引文数据库》。 |
| S100 | `b539a80218080da56a75b624.raw` (.raw UTF-16LE; sha256 `46d1866ce9af…`) | char 1431 | 对于合作发文的参考文献中，如果引文出现了任一合作者，那么这条引文将被认定为自引 |
| S100 | `b539a80218080da56a75b624.raw` (.raw UTF-16LE; sha256 `46d1866ce9af…`) | char 2843 | “文献来源”等方式进行组合查询，注：被引频次为0的文献将不会显示 |
| S101 | `6dc68fd6b32ce9c8dfcebce8.raw` (.raw UTF-16LE; sha256 `6063a3aff7a4…`) | char 11205 | 每一篇文章或资料应根据其内容性质标识一个文献标志码 |
| S101 | `6dc68fd6b32ce9c8dfcebce8.raw` (.raw UTF-16LE; sha256 `6063a3aff7a4…`) | char 11170 | 为便于文献的统计和期刊评价 |
| S101 | `6dc68fd6b32ce9c8dfcebce8.raw` (.raw UTF-16LE; sha256 `6063a3aff7a4…`) | char 12161 | 文献类型及载体类型标志 |
| S101 | `6dc68fd6b32ce9c8dfcebce8.raw` (.raw UTF-16LE; sha256 `6063a3aff7a4…`) | char 11993 | 本规范推荐采用GB/T 7714中规定的顺序编码制格式著录,也可采用GB/T 7714中规定的作者-出版年制。 |
| S101 | `6dc68fd6b32ce9c8dfcebce8.raw` (.raw UTF-16LE; sha256 `6063a3aff7a4…`) | char 34374 | 参考文献格式，参照ISO 690 |
| S101 | `6dc68fd6b32ce9c8dfcebce8.raw` (.raw UTF-16LE; sha256 `6063a3aff7a4…`) | char 13247 | 参照ISO 690及ISO 690-2，每一参考文献条目的末尾均以“.”结束。 |
| S102 | `7809d5114330a60527436b07.txt` (.txt; sha256 `e9f66647ee5f…`) | char 13241 | 検索結果には、「篇名」「作者」「刊名」「发表时间」「被引」「下载」の他 |
| S102 | `7809d5114330a60527436b07.txt` (.txt; sha256 `e9f66647ee5f…`) | char 13514 | 「下载」はそれぞれ文献の公開時期、被引用回数、ダウンロード回数を示します。 |
| S102 | `7809d5114330a60527436b07.txt` (.txt; sha256 `e9f66647ee5f…`) | char 16123 | 当該文献を中心に年毎の参考、被引用の関係をビジュアルに提示 |
| S103 | `02aefcf570a7108e699d0990.txt` (.txt; sha256 `32a5907e701f…`) | char 892 | CNKI AI 根据相关文献，生成可信增强回答。 |
| S103 | `02aefcf570a7108e699d0990.txt` (.txt; sha256 `32a5907e701f…`) | char 953 | 来源数据库 |
| S103 | `02aefcf570a7108e699d0990.txt` (.txt; sha256 `32a5907e701f…`) | char 959 | 引用量 |
| S103 | `02aefcf570a7108e699d0990.txt` (.txt; sha256 `32a5907e701f…`) | char 3175 | 相关度、发表时间、被引次数和下载量 |

### Absent-defect register rows on the theme URLs (re-checked this round)

- register `S082` (CiNii manual) — verdict: absent-as-written. The register quote
  swaps 被引用文献's verb construction and splices a separate sentence; the
  substance is on the page (W1 `GroundS096.md`). The adopted row uses the lane's
  own located quotes above.
- register `S084` (J-STAGE FAQ) — verdict: absent-as-written. The register
  linearises the four-step list without its annotations; every step is present
  (W1 `GroundS098.md`).
- register `S086` (NCPSSD homepage) — verdict: absent-as-written for the cited
  homepage capture; both quotes are verbatim in the companion help-page capture
  (`c4e1446a42d0a709c34097be`, offsets 24872 and 25269; W1 `GroundS099.md`). Not
  fabricated. The homepage row is refused below.
- register `S095` (CNKI 他引频次 note copy) — verdict: absent-as-written. One of
  three quotes is verbatim; two drop 《》 and quotation marks (W1 `GroundS101.md`).
- register `S096` (data-specification copy) — verdict: absent-as-written. q2 is
  verbatim; q1 splices section 14 wording and q3 puts GB/T 7714 where the capture
  says ISO 690 (W1 `GroundS102.md`). The adopted entry records the ISO/GB/T split.

### Decisions

| item | decision | reason | flip |
|---|---|---|---|
| `corpus/knowledge/aggregator-vs-source-r36.md` | **admit, narrowed** | PROVINCE source hierarchy and citation chaining; new ground: an index's first-party statement that its reference list and count are matched items (S096), link-creation lag (S097), the resolution ladder by DOI vs reference text (S098), lateral reading as a tested outside-the-source move (S099). The aggregator-is-not-the-source conclusion itself was already held (`contextual-source-admission-r24.md`; W1 `CritTheme.md`) and earns no expansion credit. | — |
| `corpus/knowledge/citation-count-semantics-r37.md` | **admit, narrowed** | Province: how to scope an index's counter when citing it (not a model or evaluation claim; W1 `DraftEntryCCS.md`, `ConnSiblings.md` no overlap). Narrowed: copies and third-party guides only, ISO/GB/T split recorded, the derived-list admission not transferred to CNKI. | — |
| staged S091 NCPSSD homepage — refused-doc: https://www.ncpssd.cn/ | **refuse** | The bound homepage capture carries only a 登录/注册 header and the builder line; the access-model statements the staged entry rested on are in the help-page capture, a different URL (W1 `GroundS099.md`). | a row for the help-page URL, re-opened with its own capture, cited by an entry that needs it |
| `cnki-matching-modes-r42.md` | **reject this round** | Teaches the search platform's per-field matching modes, a different feature from citation counts; adopting it widens the theme (W1 `DraftGateRefusal.md`). | a frozen question about CNKI's search-platform matching taxonomy |
| `cnki-citation-check-r40.md` | **not adopted this round (admit-later)** | A citation-checking feature, adjacent but not evidence that index data is derived; its sources were not re-grounded this round (W1 `DraftGateRefusal.md`). | a frozen question on how a citation check compares a pasted reference with an index record |

### Rows appended (8, all `mined`, opened 2026-10-25)

Built in scratch by `tools/assimilate-rows.py`, then anchor cells rewritten to the
lane's located `char N` offsets and the S101 `teaches` cell corrected to the
section-14/parameter-table split. Normalisation stripped (lesson record, per section 10):

| lane id | column | stripped |
|---|---|---|
| S096 | recheck | 180d — re-open the NII manual and confirm both 注意書き notes under section G are still present (ran 2026-10-23) |
| S096 | opened | 2026-10-23 |
| S097 | recheck | 90d — re-open the TAB2 publisher page and confirm section 2 still reads "数日～2週間後にDOIによるリンクが作成されます" (ran 2026-10-23) |
| S097 | opened | 2026-10-23 |
| S098 | recheck | 90d — re-open the FAQ page and confirm the four-step 引用元の所在確認 list is unchanged (ran 2026-10-23) |
| S098 | opened | 2026-10-23 |
| S099 | recheck | 365d — re-open the ERIC record and confirm the abstract still carries the "lateral reading" sentence (ran 2026-10-23) |
| S099 | opened | 2026-10-23 |
| S100 | recheck | 180d — re-download the document and confirm 关于自引的说明 still reads "如果引文出现了任一合作者，那么这条引文将被认定为自引" (ran 2026-10-23) |
| S100 | opened | 2026-10-23 |
| S101 | recheck | 180d — re-download the document and confirm section 14.2 still lists nine 著录项目 beginning with 主要责任者 and 文献题名 (ran 2026-10-23) |
| S101 | opened | 2026-10-23 |
| S101 | used-by | corpus/knowledge/source-type-taxonomy-r37.md, corpus/knowledge/citation-count-semantics-r37.md |
| S102 | recheck | 180d — re-download the PDF and confirm section 5.6.1 still reads "被引用回数" (ran 2026-10-23) |
| S102 | opened | 2026-10-23 |
| S102 | used-by | corpus/knowledge/citation-count-semantics-r37.md, corpus/knowledge/chinese-search-log-r37.md |
| S103 | recheck | 180d — re-download the PDF and confirm section 2.1 still lists 引用量 and 下载量 (ran 2026-10-23) |
| S103 | opened | 2026-10-23 |
| S103 | used-by | corpus/knowledge/citation-count-semantics-r37.md, corpus/knowledge/chinese-search-log-r37.md |

Pre-append validation: the C1 counter's set-A mirror and W1 `ExecMirrorCensus.md`
validated the nine-row scratch block (census exit 0); the eight-row block validated in
`.ufo/waves/round-49/assimilation/validate/` (see `## Census`).

### Wave-2 narrowing

W2 `CritEntryAgg`, `CritEntryCCS` and `ReopenS096`–`ReopenS103` found glosses beyond the captures (an aggregator "never the source" rule the lane does not hold; rung 3 mis-described; "only because" exclusivity; an outbound count called inbound; the zero-row rule generalised beyond 高级检索; S103 attributed to the wrong university; scope/teaches cells outrunning captures). Both entries and six Registry cells were narrowed; quotes added at S096 chars 3577/3801 and S101 char 13247. See `corpus/evidence/round49/claims-erratum.md`.

### Outside spot-check

No dispatched seat is a non-author. The closure is asked to re-open at least one
admitted row (suggested: S101, the UTF-16LE `.doc` reading) and the refused NCPSSD row.


## considerthese

`considerthese/2026-10-25.md:55-56` proposes "Report a capture-age line": while
no fetch is allowed, freshness cannot move, so a report should state the age of the
newest capture the lane may read. Not implemented before (no `capture age` text in the
lane; W1 `MineConsider.md`). Grounded: newest file in the campaign capture cache is
2026-10-24 23:26:57 -03:00; this round's nine theme captures were written 2026-10-23
20:33–20:53 -03:00. Landed as QUALITY 71 with `corpus/evidence/round49/capture-age-check.py`,
shown able to fail: the round-48 report prints `FRESHNESS_CAPTURE_AGE=FAIL`, exit 1.

## Census

Command: `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin chousa`.

Round start (lane at `414a2ec6`):

```text
chousa	W04	S051 duplicate url www.w3.org/TR/2017/REC-html52-20171214/syntax.html across scopes
chousa	W04	S053 duplicate url docs.python.org/3/library/socket.html across scopes
chousa	W04	S073 duplicate url www.gnu.org/software/coreutils/manual/coreutils.html across scopes
chousa	W04	S074 duplicate url docs.python.org/3/library/hashlib.html across scopes
chousa	W04	S075 duplicate url www.gnu.org/software/coreutils/manual/coreutils.html across scopes
chousa	ok	/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/SOURCES.md
exit=0
```

After adoption (registry with S096–S103):

```text
chousa	W04	S051 duplicate url www.w3.org/TR/2017/REC-html52-20171214/syntax.html across scopes
chousa	W04	S053 duplicate url docs.python.org/3/library/socket.html across scopes
chousa	W04	S073 duplicate url www.gnu.org/software/coreutils/manual/coreutils.html across scopes
chousa	W04	S074 duplicate url docs.python.org/3/library/hashlib.html across scopes
chousa	W04	S075 duplicate url www.gnu.org/software/coreutils/manual/coreutils.html across scopes
chousa	ok	/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/SOURCES.md
exit=0
```

Rows 95 → 103 (`grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md`); tiers {'A': 89, 'B': 1, 'C': 5} → {'A': 92, 'B': 6, 'C': 5}; statuses {'mined': 71, 'queued': 19, 'rejected': 5} → {'mined': 79, 'queued': 19, 'rejected': 5}. Added by tier: A 3 (S096–S098), B 5 (S099–S103). Existing rows touched: none (no `status`/`recheck`/`used-by` change).

correction: corpus/lessons/round-49.md:20 (`IDS=8 QUOTES=28 FAILURES=0`) superseded by 31 — the same command prints `IDS=8 QUOTES=31 FAILURES=0` on the round-49 manifest (`corpus/evidence/round49/measure-after.txt`; round-50 `stale-count-check.py`).

# R53DraftReadme — corpus/README.md additions (round 53, wave 1)

Seat: R53DraftReadme (scribe). Lane: `/home/vgpnk/Projects/shokunin/chousa-shokunin`
at `6365f15` (claims frozen at `a6ff732`, adopter v4 candidate at `32aab5e`,
base `5b55013`). No network, no live fetch; every source is an on-disk capture.
No tool installed or upgraded.

Scope: (a) coverage-map rows for the three C2 entries with honest per-document
credit and the base sweep, (b) `## Frontier` disposition, (c) a one-line
adopter-v4 capability note. Draft only; the L1 integrates. I did not write any
lane file except this report.

## 1. What I ran (all outputs pasted as observed)

Base sweep, exactly as specified (no output, exit 1):

```
$ git -C /home/vgpnk/Projects/shokunin/chousa-shokunin grep -l -e 'tracking record' \
    -e 'information specialist' -e 质量控制指南 5b550133d79bc09c82d8965cce2e48c2598b8c3e \
    -- corpus/knowledge
RC=1
```

The five documents' URLs at the base (no output, exit 1), and confirmation the
registry and knowledge dir are unchanged base→HEAD:

```
$ git -C <lane> grep -l -e 'jmla.2022.1449' -e 'article/download/1449' -e 'bjhea.org.cn' \
    -e 'pharmwyp' -e 'training.cochrane.org/handbook/current/chapter-04' \
    5b550133d79bc09c82d8965cce2e48c2598b8c3e -- corpus/SOURCES.md corpus/knowledge
RC=1
$ git -C <lane> diff --stat 5b550133d79bc09c82d8965cce2e48c2598b8c3e HEAD -- corpus/SOURCES.md corpus/knowledge
(no output)
```

(The lane's Cochrane rows are chapters 24, 2, MECIR, IV and the LSR guidance —
`corpus/SOURCES.md:14,18,19,29,47` — not chapter 4.)

Capture keys, first 24 hex of sha256 of each URL, sidecars present:

```
S134 0ae65ac01b93119d3c2f3fed ['...pdf','...raw','...txt']
S185 16fe8487aa97b98576a0dbac ['...pdf','...raw','...txt']
S186 cfa080b4046592eb9490a82c ['...raw','...txt']
S190 0435b64f65c3ea7ddc6bb92e ['...pdf','...raw','...txt']
S193 c9d1e74c3ac8d9eb332c9770 ['...raw','...txt']
```

Adopter v4 run in scratch on the read-only package against the base registry
(this grounds the planned lane ids; it is NOT the C1 measurement — that is
`c1-count.py`):

```
$ git -C <lane> show 5b55013:corpus/SOURCES.md > $S/run/SOURCES.base.md   # 327 lines
$ python3 tools/assimilate-rows.py --staged <pkg>/SOURCES.append.md \
    --knowledge <pkg>/knowledge --registry $S/run/SOURCES.base.md \
    --opened 2026-10-26 --out $S/run/out \
    --entry corpus/knowledge/search-tracking-record-r40.md \
    --entry corpus/knowledge/quality-control-guideline-issued-text-r48.md \
    --entry corpus/knowledge/western-instrument-alignment-r50.md
COLLISIONS=35
WARN corpus/knowledge/search-tracking-record-r40.md: body-only id S094 is also a lane id and reads as that row
WARN corpus/knowledge/search-tracking-record-r40.md: body-only id S114 is also a lane id and reads as that row
CITED=6 APPEND=5 HELD=0 TWIN=1
BODYONLY=3
RC=0
$ cat $S/run/out/renumber.tsv
staged_id lane_id action url
S134 S117 append jmla.pitt.edu/ojs/jmla/article/download/1449/2061
S185 S118 append www.bjhea.org.cn/ueditor/php/upload/file/20250115/1736907153935975.pdf
S186 S119 append m.bjhea.org.cn/35/202501/1126.html
S190 S120 append pharmwyp.com/posts/56814/6.%E7%89%B9...%EF%BC%89.pdf
S193 S121 append training.cochrane.org/handbook/current/chapter-04
S195 S118 twin   www.bjhea.org.cn/ueditor/php/upload/file/20250115/1736907153935975.pdf
```
(The S190 row's percent-encoded URL is elided with `…` for width; the url column
above is otherwise verbatim.)

Term counts over the captures (python `str.count` on the whole `.txt`):

```
S185 (16fe8487…txt) chars=27609  PRISMA=0 灰色文献=0 灰色=0 未发表=0 内部资料=0
     期刊评审=0 文献检索=3 系统评价=7 数据库=3 PICOS=1 检索者=0 检索人=0 检索人员=0 由谁=0
S186 (cfa080b4…txt) 发布时间：2025年01月03日 来源：国家卫生健康委卫生发展研究中心; signing block 2024年12月31日
S190 (0435b64f…txt) 灰色文献=5 发表偏倚=3; duty passage names 会议论文、未发表的学位论文、产业报告、咨询报告
S134 (0ae65ac0…txt) 27,659 chars: 'search strategies for all databases'=1 (char 1206),
     'number of records identified from each information source'=1 (char 1334)
S193 (c9d1e74c…txt) alignment sentence at char 13494; unpublished-as-bias sentence at char 36710;
     'including the sources searched, when, by whom, and using which terms'=1 (char 112574)
S185 指标 4 under 文献研究 at char 18046: 在文献检索和筛选阶段，是否参照 Cochrane 等组织制定的…
```

## 2. Draft — `corpus/README.md` (append-only, after the round-52 section)

```markdown corpus/README.md
## Round53 coverage and frontier (2026-10-26)

| Note | Holds | Sources |
|---|---|---|
| `knowledge/search-tracking-record-r40.md` | Round-53 note (adopted by document from `merge/chousa/`; the entry the `## Search log` round-43 entry of `corpus/SOURCES.md` refused because its sentence was not a contiguous span, bound this round where the capture's text form carries that sentence once): what PRISMA-S asks a tracking record to carry and where — the 2009→PRISMA 2020/PRISMA-S change to reporting search strategies for all databases, registries and websites that were searched, PRISMA-S's count of records identified from each information source, and the flow diagram's two columns (identification via databases and registers in Column 1, via other methods in Column 2) | `S117`; `corpus/evidence/round53/spans.tsv`; `corpus/lessons/round-53.md` |
| `knowledge/quality-control-guideline-issued-text-r48.md` | Round-53 note (adopted by document): 国家药物和卫生技术综合评估中心's 《药品临床综合评价质量控制指南（2024年版 试行）》 in the form it was issued — the 循证指南/学术研究 taxonomy, inclusion 可根据评价主题确定 with PICOS as an option, 所检索的数据库应包括多个中、英文专业数据库, two independent screeners with a third arbitrating, a flow chart of counts and reasons; §1 文献研究的质量控制 returns 灰色文献, 灰色, 未发表, 内部资料 and 期刊评审 at 0 over the 27,609-character text form (文献检索 3, 系统评价 7, 数据库 3, PICOS 1, PRISMA 0), and 文献研究's 指标 4 asks whether search and screening referred to Cochrane 等组织's methods; the draft→issued change (应→可; 中、英文专业数据库→多个中、英文专业数据库); the release notice's signing date 2024年12月31日 and 发布时间 2025年01月03日, source 国家卫生健康委卫生发展研究中心; and the regulator's 2019 notice copy, which requires collecting 会议论文、未发表的学位论文、产业报告、咨询报告 and gives negative results as the reason | `S118`, `S119`, `S120`; `corpus/evidence/round53/spans.tsv`; `corpus/lessons/round-53.md` |
| `knowledge/western-instrument-alignment-r50.md` | Round-53 note (adopted by document): the instrument-to-instrument statement the lane held only as citations — Cochrane Handbook ch.4 §4.2.1, that conduct meets MECIR's searching expectations and the reporting aligns with the current reporting guidance for PRISMA and PRISMA-S, and §4.3.2, unpublished studies treated as a question of bias — read against the centre's issued guideline, which prescribes the same search work, points 指标 4 at Cochrane 等组织's methods and returns PRISMA 0 over its whole text form | `S121`, `S118`; `corpus/evidence/round53/spans.tsv`; `corpus/lessons/round-53.md` |
| `../tools/assimilate-rows.py` | Round-53 capability (adopter v4, landed `32aab5e`): a cited staged row is `held` only when a Registry row already carries its URL and `twin` when this run already minted that URL (the same lane id, nothing appended); the count line separates `HELD=` from `TWIN=`; every cited row's recheck — held and twin rows included — is validated before any row is built; a registry it cannot continue from is refused with exit 1 and every registry `REFUSED` line printed before any entry line, and is refused also with no `--entry`, while a sound registry with no `--entry` exits 0 | `corpus/evidence/round53/claims.md`; `corpus/evidence/round53/c1-count.py`; `corpus/evidence/round53/controls/` |

Coverage credit for round 53 is per document and is counted once per document, not
once per entry: the JMLA tracking-record commentary (`S117`), the centre's issued
quality-control guideline (`S118`, cited by both the quality-control entry and the
western-alignment entry), its release notice (`S119`), the regulator's 2019 notice
copy (`S120`) and Cochrane Handbook ch.4 (`S121`). The guideline's second staged row
(`S195`, the same URL as `S185`) is a `twin` and is not a sixth document, and earns
nothing. Credit is claimed for the documents the round's counter binds (`BOUND=n/5`
in `corpus/evidence/round53/c2-count.py`), not for the entries' count; a document the
lane already held would earn none, and none of the five was in the lane at the base —
no `corpus/knowledge` file carried the three sweep terms, and no Registry row or
knowledge file carried any of the five URLs at `5b55013`. Base sweep:
`git -C /home/vgpnk/Projects/shokunin/chousa-shokunin grep -l -e 'tracking record' -e 'information specialist' -e 质量控制指南 5b550133d79bc09c82d8965cce2e48c2598b8c3e -- corpus/knowledge`
→ no output, exit 1. Every source is an on-disk capture: with
`Q=/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache`, the five
URL keys are `0ae65ac01b93119d3c2f3fed`, `16fe8487aa97b98576a0dbac`,
`cfa080b4046592eb9490a82c`, `0435b64f65c3ea7ddc6bb92e` and
`c9d1e74c3ac8d9eb332c9770`, each with a `.txt` sidecar.

### Frontier

Advanced — what these documents move:

- **The search-record field set, now at instrument level.** Three instruments, not a field list: PRISMA-S's own authors' commentary states the change to reporting search strategies for every database, registry and website searched and the count of records identified from each information source, and allocates the flow diagram's Column 2 to other methods against Column 1's databases and registers (`S117`); the Cochrane Handbook chapter states that conduct meets MECIR's searching expectations and the reporting aligns with the current reporting guidance for PRISMA and PRISMA-S (`S121`); the centre's issued guideline prescribes the same search work — multiple Chinese and English databases, two independent screeners and an arbiter, a flow chart of counts and reasons — and asks in 文献研究's 指标 4 whether search and screening referred to Cochrane 等组织's methods, while PRISMA counts 0 over the whole text form (`S118`).
- **The re-runnable sweep.** `corpus/README.md:390-391` records the gap: the sweep re-run is a glob/existence check over the named locations, never the recorded command. The instrument now names the fields such a check would need — the strategy per source and the count per source (`S117`) — and the same chapter's §4.5 MECIR C36 (outside the entry's §4.2.1/§4.3.2 scope line) says the search process "including the sources searched, when, by whom, and using which terms" needs to be documented and the searches reproducible to the extent possible. The execution half is untouched: no gate, tool or counter changed this round.
- **Non-Western field rules, and the issued/draft boundary.** The round replaces a draft's wording with the issued text — 应→可, 中、英文专业数据库→多个中、英文专业数据库 — so the absent grey-literature field is now a property of the issued instrument rather than of its drafting, and the contrast with the regulator's 2019 notice for the same domain, which requires 会议论文、未发表的学位论文、产业报告、咨询报告 and gives negative results as the reason, is a contrast between two issued documents (`S118`, `S120`).

Left open — named, not closed:

- **Searcher identity.** The issued Chinese instrument names no searcher: 检索者, 检索人, 检索人员 and 由谁 each count 0 over its text form, and 指标 4 asks for the strategy and the screening flow, not who ran them. The western handbook's §4.5 names "by whom" among the fields to document, so the field exists on one side of the comparison only.
- **A national standard for either literature.** Still not established: the round reaches a centre-issued guideline and a regulator's notice, both domain instruments, and the guideline's own external reference is Cochrane 等组织's methods, not a reporting standard.
- **The Chinese PRISMA-S interpretation's item-by-item text.** Unchanged: order-only from SinoMed and the portal.
- **The publisher's current Japanese translation.** Untouched this round; the original URL still holds only a failed-fetch marker.
- **An imperfect search.** Untouched: the handbook treats unpublished studies as a bias question, and neither document states what a record must carry when a platform failed or a query was truncated.
- **Other capture forms.** Round 53 adds no reader (`build-spans.py` is round 52's builder with round-53 paths); `.xlsx` and `.pptx` captures stay unread, and an OLE `.doc` keeps the UTF-16LE form.
- **Newly named, not closed.** Whether provincial derivatives follow the issued wording; whether another Chinese clinical-methodology instrument names PRISMA-S; whether the handbook's alignment sentence survives the edition after 6.5.1; whether the centre's own host serves the issued text (the society's carrier is the corpus's only open copy, and the notice's own contact address is on the refusing domain).
```

Notes on the draft's honesty bounds: the rows state the entries' holdings and
the credit rule, not a C2 result; the counter is the operand measure and I did
not run it (no entry exists yet, so `ENTRIES=0/3` is the only reachable state —
`controls/c2-before.txt`). The `S117`–`S121` ids are the adopter's mapping on
the base registry (receipt in §1), provisional until the L1 re-runs it.

## 3. Gates

Run: base sweep (rc 1, no output); five-URL base grep (rc 1) and base→HEAD
`diff --stat` (empty); capture-key listing for all five URLs; one adopter run in
scratch (mapping, `CITED=6 APPEND=5 HELD=0 TWIN=1`); term/offset probes on the
five `.txt` sidecars quoted above.

Not run (not mine, and not reachable now): `c1-count.py` (C1's operand measure),
`c2-count.py` (needs the landed entries), `build-spans.py`, any quote-lint or
`inference-ground` run. No claim of a pass is made anywhere in this report.

## 4. Touched surfaces

Only `/home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-53/w1/R53DraftReadme.md`
(this report). Scratch `/fast/scratch/hyaku/chousa-r53/R53DraftReadme` created and
removed; `TMPDIR` set there for every command. No git/jj mutation anywhere, no
lane file, no package write.

## 5. Out of scope / left to the L1

- The `lessons/round-53.md` and `evidence/round53/` coverage rows (their content
  does not exist yet; I would have had to guess).
- `QUALITY.md` rows: the file's last entry is 90 (round 52), so the v4 capability
  row cites no QUALITY line.
- `refused-entry` / `refused-doc` lines, `used-by` cells, spans and the Gate
  block — all L1 integration or executor work.
- The entry text itself: I did not propose changing a predicate, target, counter
  or control, and did not touch the entries.

## 6. Findings

1. **Body-only id collision in the staged tracking entry (reported, not patched).**
   The adopter warns that body tokens `S094` and `S114` of
   `search-tracking-record-r40.md` are also lane ids. At the base, lane `S094` is
   an ACL/COLING paper and lane `S114` is the 中国全科医学 PRISMA 2020 checklist
   (`corpus/SOURCES.md:104,124`, unchanged since `5b55013`); in the package,
   `S094` is the NDL WARP FAQ and `S114` is the climate-fever dataset
   (`SOURCES.append.md:19,39`). So the body tokens can be assumed to mean neither
   lane row nor the package row the entry's prose describes (a local-copy/URL
   distinction; a grey-literature and hand-search requirement): landed unchanged,
   they read as the wrong lane documents. The adopter does not refuse them
   (`BODYONLY=3`, two `WARN` lines); the integrating seat must re-check each body
   cross-reference against the lane's own rows.
2. **`CITED=6` is six staged rows over five documents.** The twin is visible in
   the mapping (`S195→S118 twin`), so the credit paragraph counts five, and the
   issued guideline is credited once although two entries cite it (`used-by`
   must name both).
3. **The issuance facts are both in the notice**: signing block `2024年12月31日`
   and `发布时间：2025年01月03日 来源：国家卫生健康委卫生发展研究中心` (chars
   ~920 and ~501 of `cfa080b4…txt`). The guideline's own text form carries no
   issue date, so the draft credits the notice for it.
4. **The Cochrane chapter's §4.5 is outside the entry's scope line** (§4.2.1 and
   §4.3.2 only). The chapter does carry "by whom" and reproducibility at char
   112574/112057, but the entry does not quote them; the draft attributes §4.5 to
   the chapter and flags it as outside the entry's scope rather than as entry
   ground.
5. **`指标 4` is ambiguous inside the guideline** — four occurrences, of which
   only the one at char 18046 (under 文献研究) is the Cochrane reference; the
   other three are 主题遴选, 质控员 and dates. The draft names the subsection to
   avoid the wrong one.
6. **The guideline's text form is 27,609 characters** and matches the staged
   entry's counts exactly (PRISMA 0, 灰色文献 0, 文献检索 3, 系统评价 7, 数据库 3,
   PICOS 1), so the draft's numbers are measured, not copied.

VERDICT — Drafted the three round-53 coverage rows with per-document credit
(five documents, the twin excluded), the Frontier advance/open disposition and
the adopter-v4 capability line, grounding every id on one adopter run and every
number on the five capture sidecars; the base sweep returns nothing at
`5b55013` (exit 1), and the draft discloses the tracking entry's body-id
collision instead of patching it.

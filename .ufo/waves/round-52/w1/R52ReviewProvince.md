# R52ReviewProvince — province & QUALITY-bar review, round 52 w1

Seat R52ReviewProvince · 2026-10-26 · read-only seat: production untouched, only this file written.
Scratch `/fast/scratch/hyaku/chousa-r52/R52ReviewProvince` (removed at close). No tool installs (none needed). No network.

## Read (all opened this session)
- chousa `PROVINCE.md:3-13` — owns question framing, source hierarchy, citation chaining, claim-vs-source verification, search-strategy taxonomy; refuses orchestration → kumitate.
- `corpus/QUALITY.md:1-31` (criteria 1-8) and `:913-915` (criteria 85-86, round-51/52 counter criteria).
- `corpus/README.md` coverage map (rounds 1-30; r50 filename-drift correction at `:1078`).
- `corpus/SOURCES.md:121-124` — lane rows end at S112 (JAHBS) before `## Paths`; lane S111=SinoMed record, S112=JAHBS article.
- Staged entries under `/home/vgpnk/Projects/shokuknow/merge/chousa/knowledge/corpus/knowledge/`:
  `japanese-search-record-r38-amendment-2026-10-23.md` (NIPH half), `japanese-prisma-item-wording-r40.md`,
  `chinese-search-log-r37-amendment-2026-10-23.md`.
- Staged `SOURCES.append.md:36,37,50,51,54` — staged S111=medsci, S112=chinagp, S125=NIPH, S126=JAHBS, S129=wayback PRISMA.
- All 21 fleet `PROVINCE.md` files via grep (below); `tools/capture-text.py:3-21,50-63`.

## Sibling-ownership sweep
`grep '(?i)docx|capture|extract|text.form|tooling|conversion' /home/vgpnk/Projects/shokunin/*-shokunin/PROVINCE.md`
(gitignore:false — the first run with defaults returned nothing because the lane dirs are git-ignored; the rerun is the honest sweep). Observed:
- `docx`: **0 hits in all 21 provinces** — no lane claims OOXML/docx text-form derivation.
- kumitate `PROVINCE.md:3`: domain "orchestration & tooling — scopes OMP task/hub, ufo-fsd scripts & runtime"; its Adjacent routes "Research method → chousa". game-dev-3d `PROVINCE.md:76` confirms kumitate = "general orchestration and multi-agent tooling".
- kake Adjacent: "chousa owns research method and source hierarchy".
- kengaku `PROVINCE.md:262` and `:403`: "capture and citation method stay chousa's (`chousa-shokunin/PROVINCE.md:5-7,10-11`)".
- kaidoku = shipped-artifact RE (its extraction surfaces are REA artifact verbs); tabi = browser-session capture. Neither is a document text form.
- kotoba PROVINCE.md § Adjacent census, chousa row, pins chousa at `00f8c7f5272a1d98b6d34913985fa4537e00aaf9` — the assignment's base commit.

## Verdict per staged entry
1. **japanese-search-record-r38-amendment (NIPH half) — IN PROVINCE.** Search-strategy taxonomy: which fields a Japanese search record must carry (search window `S125`, database/provider/dates `S126`) and Q12's searcher-identity half. **NOT to absorb:** the NIPH form's cost-effectiveness machinery — section 3 追加的有用性 assessment framework, 製造販売業者 submission procedure, cost-effectiveness criteria. That is regulatory/health-economics ground; the row's scope cell already pins only "the search-record fields … requires" (`SOURCES.append.md:50`). The entry's prose stays on the search-record fields — verified.
2. **japanese-prisma-item-wording-r40 — IN PROVINCE.** Primary-translation wording of PRISMA 2020 items 6/7; settles Q12's Japanese half as a negative; the withdrawn-original-kept-visible + archive-locator discipline is source-hierarchy/hop craft, lane core. No sibling overlap.
3. **chinese-search-log-r37-amendment — IN PROVINCE.** Reception-vs-standard is source-hierarchy taxonomy applied to a literature; the per-source date field across three literatures is the lane's best-evidenced search-record requirement. **NOT to absorb:** medsci's portal/clinical content and chinagp's clinical articles — only the reporting-standard field text the rows scope (`SOURCES.append.md:36-37`; S111 tier B scoped to the portal's own descriptive blocks, attachment declared unopened).

QUALITY bar: all three carry `source:` (row + URL + anchor), `verified-at:`, `recheck: 180d … (ran 2026-10-23)` and `ground:` (criterion 6); Observation/Inference/Unknown separated (criteria 3, 8, `QUALITY.md:28-31`); claims falsifiable (criterion 1 — re-derived below); scoped tiers honest (criterion 7, `QUALITY.md:24-27`).

## Verdict on tools/capture-text.py — IN PROVINCE
Claim-vs-source verification needs one reproducible text form of a source; a .docx capture's `.txt` sidecar is U+FFFD garbage, so the tool is the source text form, the same instrument class as the gate's span/anchor checkers. Not kumitate's tooling (scoped to OMP/ufo-fsd orchestration, above) and not tabi's browser capture. Operability probes (TMPDIR=scratch; counters not run — C1/C2 seats own first falsification):
```
python3 chousa-shokunin/tools/capture-text.py .qcache/3a8b45977cd111e45e3980a5.raw   -> 19682 chars (= frozen C1/C2 number)
python3 chousa-shokunin/tools/capture-text.py <raw> --locate 'SRにおける文献検索期間について明記する'
    -> LOCATED count=1 offset=8996 rc 0
.qcache/3a8b45977cd111e45e3980a5.txt -> 168952 chars, 72117 U+FFFD  (= the docstring's round-51 figure, re-derived)
```

## Findings (severity-ordered; none touches a frozen C1/C2 predicate)
- **F1 (medium, entry text at integration).** The NIPH entry's worked-example quote (entry `:17` "文献検索期間2015年1月から2018年10月まで") is count=0 in the tool form: the form splits label and value — `文献検索期間\n\n2015年1月から2018年10月まで` (label offset 9181, value offset 9189). The quote came from the raw XML extraction the row names. At integration (S115): quote the two located pieces ('2015年1月から2018年10月まで' count=1 offset=9189) or name the form. Other anchors locate: 'SRにおける…明記する' offset 8996; 'ハンドサーチ等により' count=1 offset 9428. The section heading is not unique (システマティックレビューのリサーチクエスチョン ×6, first 685) — anchor the offset-8996 sentence, not the heading.
- **F2 (medium).** The PRISMA-JP entry's recheck sentence (`:6`) is not byte-contiguous in the sidecar form: the form wraps it across lines and writes `Web サイト` with a space; `完全な検索戦略を記載する` is count=1 offset 766. The recheck needs whitespace-normalized comparison or the wrapped bytes. The central negative re-derives clean: `検索者` count=0 in the 5328-char S129 `.txt` (entry `:23-24` verified).
- **F3 (medium).** The Chinese entry's quote (`:50`) `明确说明每一项来源的检索或查询日期` is count=0 in the S112 sidecar; the form's bytes are `明确说明每一项来源 的 检索或查询日期` (spaces around 的), count=1 offset 1707. Fix the entry quote to the form's bytes at integration (S114).
- **F4 (medium).** S111 anchors are non-unique in its sidecar: `为文献检索报告提供了包含16个条目的专项规范` ×2 (offsets 2377, 3484 — the page duplicates the abstract verbatim), the attachment filename ×3, `郑卿勇` ×3. Any span/anchor for S113 must pass an exact-once check; workable unique anchors exist: `简要介绍` count=1 offset 2264 (the very block the row names) and `下载请点击` count=1 offset 4996.
- **F5 (info, integration).** Staged ids collide with lane ids: staged S111/S112 are the lane's SinoMed/JAHBS rows. Remap at integration: staged S111→S113, S112→S114, S125→S115, S129→S116; staged S126 (JAHBS) is already lane S112, so the NIPH entry's body cite `S126` becomes `S112` — never carried over. Registry max S112 confirmed (`corpus/SOURCES.md:122` then `:124` `## Paths`).
- **F6 (info).** F1-F4 are exactly the round-51 routed classes "NIPH zip-member form" and "a content anchor for pointer corrections": the canonical form now exists, and every entry quote must be re-derived against it with an exact-once location before spans are cut.
- Second recheck quote of entry 1 verified: in the JAHBS `.txt`, `検索の開始日と終了日を記載すること` count=1 offset 11294; `Ovid` count=1 offset 11243.

## Residual risk / verification gaps
- c1-count.py, c2-count.py and build-spans.py not run here (other seats own falsification; the counters only read).
- The S111 attachment PDF was not opened (row is scoped to the portal's descriptive blocks — consistent with tier B).
- S129's 2024-archive revision currency stays unknown (the entry declares it in Unknown).
- One grep run with default gitignore:true silently searched nothing for the fleet glob; the negative claims rest on the gitignore:false rerun.

VERDICT: attacked the province fit of three staged search-record documents and tools/capture-text.py — all four in province with named non-absorb boundaries (HTA cost-effectiveness, portal clinical content, orchestration tooling all excluded); found 4 anchor-form defects (quotes not byte-exact or non-unique in the canonical capture forms) plus the staged-id remap, none touching the frozen C1/C2 predicates.

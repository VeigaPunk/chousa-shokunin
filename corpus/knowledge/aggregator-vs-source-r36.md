
# A citation index's reference list is derived from matching, and its links arrive late

source: S096 — https://support.nii.ac.jp/ja/cir/manual_articles_detail — section G 参考文献／被引用文献, the two 注意書き — capture 2026-10-23, re-opened 2026-10-25
source: S097 — https://www.jstage.jst.go.jp/static/pages/ForPublishers/TAB2/-char/ja — sections 1 and 2 — capture 2026-10-23, re-opened 2026-10-25
source: S098 — https://www.jstage.jst.go.jp/static/pages/FAQs/TAB2/-char/ja — the 引用元の所在確認 passage and its four-step resolution list — capture 2026-10-23, re-opened 2026-10-25
source: S099 — https://eric.ed.gov/?id=EJ1372738 — the abstract on ERIC record EJ1372738 — capture 2026-10-23, re-opened 2026-10-25
verified-at: 2026-10-25
recheck: 180d
ground: source hierarchy (PROVINCE.md: primary / secondary / aggregator) and citation chaining — the lane's chain CLEAN proves an anchor's existence one hop at a time, and the lane held no first-party statement from an index about how its own reference lists are derived
adopted: round 49 from the campaign package `merge/chousa/`, re-bound by document to S096, S097, S098 and S099 (the staged-to-lane id map and the refused NCPSSD homepage row are in `corpus/lessons/round-49.md` `## Gate`)

#### Observation

- **The index says so itself (Japanese).** NII's CiNii Research manual page on the
  article detail screen states
  "CiNii Researchの「参考文献」は、実際の論文の参考文献と必ずしも一致していません"
  (its 参考文献 are not necessarily the paper's own references): only references
  matched by the service's 同定・統合処理 are shown, and
  "参考文献数も、論文での掲載数ではなく同定・統合された分をカウントしています。"
  (the reference count is of the matched items, not the count printed in the
  paper). A second note says CiNii Research covers a different range of documents
  from CiNii Articles ("CiNii Researchでは、CiNii Articlesとは 文献の収録範囲が異なっており")
  and "（それに伴って）別の手法で同定・統合処理を行っているため" its lists need not
  match CiNii Articles'. Of the cited-by list (被引用文献) the page says only
  "随時増加していきます。" — it grows over time (S096).
- **Resolution is an ordered search (Japanese).** J-STAGE's FAQ for editors and
  publishers says "システムが引用元の所在を特定できた文献にリンクを付与しています"
  (links are attached to the works whose source the system located) and
  "引用元の所在確認は、次の順で解析・検索を実施しています": a DOI from the metadata
  (`1.DOI（メタデータ項目） をもとに検索　例：10.xxxx`), bibliographic metadata, a DOI
  detected in the reference text and searched ("3.引用文献の原文情報からDOIを検出して検索"),
  and last the reference text parsed into bibliographic data
  ("4.引用文献の原文情報を書誌情報に解析して検索"). Rungs 3 and 4 take the reference
  text as input; rung 3 then searches by an identifier, rung 4 by bibliographic
  fields (S098).
- **Links to partner-registered works arrive late (Japanese).** J-STAGE's
  publisher page says DOI links to citing and cited works registered in its
  partner services are made days to two weeks after the article appears
  (`J-STAGEが連携している外部サービス に登録されている引用文献および被引用文献には、J-STAGEでの記事公開から数日～2週間後にDOIによるリンクが作成されます`).
  Separately, a DOI resolves as a URL only after a short delay:
  "DOIがURLとして使用できるようになるには、J-STAGEでの公開から1日～数日程度かかります。" (S097).
- **Reading a source *about* the source (Western).** The ERIC abstract of a
  district-wide field study says students practised the lateral-reading
  heuristic,
  "leaving an unfamiliar website to search the open Web before investing attention in the site at hand",
  reports "Using a matched control design, students in treatment classrooms (n = 271) were compared to peers (n = 228) in regular classrooms.",
  and says treatment students "grew significantly in their ability to judge the credibility of digital content" (S099).

#### Inference

- An index's reference list cannot stand in for the paper's own reference list
  when a claim is about the paper. S096 is the index's own statement about its
  own derivation — the artefact for that scope, which is why the row is tier A
  under the lane's tier-for-this-scope rule
  (`corpus/knowledge/contextual-source-admission-r24.md`) — and it says
  `CiNii Researchの「参考文献」は、実際の論文の参考文献と必ずしも一致していません`
  and that the count is `同定・統合された分をカウントしています`: the list may
  equal the paper's when every reference matched, and nothing on the index says
  when it does.
- An empty or short cited-by list from an index is not evidence of absence. A
  hop checked against an index can be unresolved because the link has not been
  made yet — S097 dates it
  `J-STAGEが連携している外部サービス に登録されている引用文献および被引用文献には、J-STAGEでの記事公開から数日～2週間後にDOIによるリンクが作成されます`
  for partner-registered works, and S096's cited-by list grows over time — or
  because no rung located the work (S098); an empty list does not say which.
  Only the citing work's own reference list settles a negative hop.
- A chain record should say which rung resolved a hop, not only that it
  resolved. S098's ladder runs from `1.DOI（メタデータ項目） をもとに検索　例：10.xxxx`
  to `4.引用文献の原文情報を書誌情報に解析して検索`; identifier matches (rungs 1
  and 3) and bibliographic matches (rungs 2 and 4) are different kinds of hop and
  should not be pooled. The FAQ states a search order, not a reliability order;
  ranking the rungs is the lane's own judgement.
- S003 (SIFT) names investigating the source as one of its four moves; S099
  describes a classroom intervention built on the lateral-reading heuristic,
  `leaving an unfamiliar website to search the open Web before investing attention in the site at hand`,
  with a measured effect at abstract level. That pairing is the lane's
  inference: neither capture links SIFT and lateral reading.

#### Unknown

- Whether J-STAGE records which rung produced each link. The FAQ describes the
  ladder; the per-link rung was not observed, and no claim is made that a
  reader can recover it.
- Whether CNKI states the derived-list caveat in its own words;
  `corpus/knowledge/citation-count-semantics-r37.md` reads CNKI only through
  hosted copies and a third-party guide.
- The study's full text and effect sizes: S099 is scoped to the ERIC abstract.
- NCPSSD (国家哲学社会科学文献中心): the staged access-model claims (free after
  registration; full-text download for registered users only; foreign
  journals and 古籍 online-reading only) are in its help-page capture, not in
  the homepage capture the staged row named; that row is refused this round
  (flip: a row for the help-page URL, re-opened with its own capture).

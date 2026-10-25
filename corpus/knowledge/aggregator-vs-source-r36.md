
# A citation index's reference list is a derived artefact, and it is incomplete in time

source: S096 — https://support.nii.ac.jp/ja/cir/manual_articles_detail — section G 参考文献／被引用文献, the two 注意書き — capture 2026-10-23, re-opened 2026-10-25
source: S097 — https://www.jstage.jst.go.jp/static/pages/ForPublishers/TAB2/-char/ja — sections 1 and 2 — capture 2026-10-23, re-opened 2026-10-25
source: S098 — https://www.jstage.jst.go.jp/static/pages/FAQs/TAB2/-char/ja — the 引用元の所在確認 passage and its four-step resolution list — capture 2026-10-23, re-opened 2026-10-25
source: S099 — https://eric.ed.gov/?id=EJ1372738 — the abstract on ERIC record EJ1372738 — capture 2026-10-23, re-opened 2026-10-25
verified-at: 2026-10-25
recheck: 180d
ground: source hierarchy (PROVINCE.md: primary / secondary / aggregator) and citation chaining — the lane's chain CLEAN proves an anchor's existence one hop at a time, and the lane held no first-party statement from an index about how its own reference lists are derived
adopted: round 49 from the campaign package `merge/chousa/`, re-bound by document to S096, S097, S098 and S099 (the staged-to-lane id map and the refused NCPSSD homepage row are in `corpus/lessons/round-49.md` `## Gate`)

#### Observation

- **The operator says so itself (Japanese).** NII's CiNii Research manual states
  "CiNii Researchの「参考文献」は、実際の論文の参考文献と必ずしも一致していません"
  (its 参考文献 are not necessarily the paper's own references): only references
  matched by the service's 同定・統合処理 are shown, and
  "参考文献数も、論文での掲載数ではなく同定・統合された分をカウントしています。"
  (the reference count is of the matched items, not the count printed in the
  paper). A second note, "CiNii Researchでは、CiNii Articlesとは 文献の収録範囲が異なっており",
  says the two NII services cover and merge differently, so their lists need not
  match each other (S096).
- **Resolution is a heuristic ladder (Japanese).** J-STAGE's FAQ for editors and
  publishers says "システムが引用元の所在を特定できた文献にリンクを付与しています"
  (a link is attached only where the system located the cited work) and
  "引用元の所在確認は、次の順で解析・検索を実施しています": a DOI from the metadata
  (`1.DOI（メタデータ項目） をもとに検索　例：10.xxxx`), bibliographic metadata, a DOI
  detected in the reference text ("3.引用文献の原文情報からDOIを検出して検索"), and
  last the reference text parsed into bibliographic data
  ("4.引用文献の原文情報を書誌情報に解析して検索"). Rungs 3 and 4 work on the
  reference text, not on an identifier (S098).
- **The chain grows after publication (Japanese).** J-STAGE's publisher page
  says links to citing and cited works registered in its partner services are
  made days to two weeks after the article appears
  (`J-STAGEが連携している外部サービス に登録されている引用文献および被引用文献には、J-STAGEでの記事公開から数日～2週間後にDOIによるリンクが作成されます`),
  and that "DOIがURLとして使用できるようになるには、J-STAGEでの公開から1日～数日程度かかります。"
  (a DOI works as a URL only one to a few days after publication) (S097).
- **Reading a source *about* the source (Western).** The ERIC abstract of a
  district-wide field study defines lateral reading as
  "leaving an unfamiliar website to search the open Web before investing attention in the site at hand",
  reports "Using a matched control design, students in treatment classrooms (n = 271) were compared to peers (n = 228) in regular classrooms.",
  and says treatment students "grew significantly in their ability to judge the credibility of digital content" (S099).

#### Inference

- An index's reference list is derived from the source's list and is not
  equal to it: S096 says `CiNii Researchの「参考文献」は、実際の論文の参考文献と必ずしも一致していません`
  and that the count is only `同定・統合された分をカウントしています`. That is the
  lane's own tier rule — an aggregator is never the source — stated first-party
  by the aggregator, which supports scoping an index's reference list to the
  aggregator tier.
- The lane's chain check has a temporal blind spot. S097 dates the link
  creation `J-STAGEが連携している外部サービス に登録されている引用文献および被引用文献には、J-STAGEでの記事公開から数日～2週間後にDOIによるリンクが作成されます`,
  so a hop checked against an index can be unresolved only because the index
  has not yet linked the reference, and S096's count is a matched-item count:
  an empty cited-by list from an index is weaker evidence than an empty search
  of the sources themselves.
- Read together, the Japanese sources describe a resolution ladder whose
  bottom two rungs read reference text: S098 starts from `1.DOI（メタデータ項目） をもとに検索　例：10.xxxx`
  and ends with `4.引用文献の原文情報を書誌情報に解析して検索`. A chain record
  should therefore say how a hop resolved as well as that it resolved; a hop
  resolved by parsing reference text is a weaker evidential object than one
  resolved by DOI.
- S003 (SIFT) names investigating the source as one of its four moves; S099
  gives that kind of move a concrete, field-tested procedure, defining lateral
  reading as `leaving an unfamiliar website to search the open Web before investing attention in the site at hand`.
  For a lane whose chain exemptions are record-declared, it is the one method
  here that produces evidence about a source from outside the source; S099 is
  read at abstract level only.

#### Unknown

- Whether J-STAGE records which rung produced each link. The FAQ describes the
  ladder; the per-link rung was not observed, and no claim is made that a
  reader can recover it.
- Whether the derived-list caveat holds for Chinese indexes in their own
  words; `corpus/knowledge/citation-count-semantics-r37.md` reads CNKI only
  through copies and third-party guides.
- The study's full text and effect sizes: S099 is scoped to the ERIC abstract.
- NCPSSD (国家哲学社会科学文献中心): the staged access-model claims (free after
  registration; full-text download for registered users only; foreign
  journals and 古籍 online-reading only) are in its help-page capture, not in
  the homepage capture the staged row named; that row is refused this round
  (flip: a row for the help-page URL, re-opened with its own capture).

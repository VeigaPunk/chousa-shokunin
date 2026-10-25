
# A citation index's reference list is a derived artefact, and it is incomplete in time

source: S096 — https://support.nii.ac.jp/ja/cir/manual_articles_detail — section G 参考文献／被引用文献, the two 注意書き — manual page read 2026-10-23
source: S097 — https://www.jstage.jst.go.jp/static/pages/ForPublishers/TAB2/-char/ja — sections 1, 2, 11 and 14 — page read 2026-10-23
source: S098 — https://www.jstage.jst.go.jp/static/pages/FAQs/TAB2/-char/ja — the 引用元の所在確認 passage and its four-step resolution list — page read 2026-10-23
source: S099 — https://eric.ed.gov/?id=EJ1372738 — the abstract on ERIC record EJ1372738 — read 2026-10-23
verified-at: 2026-10-23
recheck: 180d — re-open the five URLs and confirm both CiNii 注意書き, the J-STAGE four-step list, the timing sentence and the NCPSSD item 7 are unchanged (ran 2026-10-23)
ground: frontier items 1 and 3 — citation-chain verification modes and source-tier adjudication; the lane's chain CLEAN proves an anchor's existence, exemption is record-declared, one hop at a time with no transitivity, and the lane holds no CJK row against which its own tier rule could be checked

#### Observation

- **The operator says so itself (Japanese).** NII's CiNii Research manual states
  that its 参考文献 "are not necessarily the same as the paper's own
  references" — only those matched by the service's 同定・統合処理 are shown —
  and that "the reference count … is of the matched items, not the count
  printed in the paper." The manual further notes that CiNii Research and
  CiNii Articles identify and merge differently, so the two services' lists
  need not match each other.
- **Resolution is a heuristic ladder (Japanese).** J-STAGE's publisher FAQ
  states that a citation link is attached only where the system could locate
  the reference's source, and confirms the location in this order: DOI from the
  metadata item; bibliographic metadata; a DOI extracted from the reference
  text; then the reference text parsed into bibliographic data. Steps 3 and 4
  are inference from text, not identifier resolution.
- **The chain grows after publication (Japanese).** J-STAGE states that DOI
  links to citation and cited-by works are created "from a few days to two
  weeks after" the article is published, and that a DOI can only be used as a
  URL 1 to a few days after publication.
- **A free primary-source channel with a real access model (Chinese).** The
  国家哲学社会科学文献中心 is built and operated by the Chinese Academy of
  Social Sciences Library; its help states that the service is free to the
  public after registration, that full-text PDF download is provided **only**
  to registered users, and that foreign journals and 古籍 are online-reading
  only.
- **Reading a source *about* the source (Western).** The lateral-reading
  heuristic — "leaving an unfamiliar website to search the open Web before
  investing attention in the site at hand" — was tested in a matched-control
  design (n=271 against n=228) and produced significant growth in students'
  ability to judge the credibility of digital content.

#### Inference

- Two independent operators, in the same literature, publish the same admission
  in different words: **an index's reference list is derived from the source's
  reference list, and is neither equal to it nor a superset of it.** That is
  the lane's own tier rule — an aggregator is never the source — arriving as
  a first-party statement from the aggregator, rather than as the lane's
  inference. It is the cleanest external support this round produced for
  scoping an aggregator row to tier C.
- The lane's chain check has a **temporal** blind spot that neither the
  lane's gate nor its corpus records. A hop checked against a citation index
  can be unresolved simply because the index has not yet ingested the
  reference, and the same index's own count for a paper is a *matched-item*
  count. A "0 inbound citations" reading is therefore not evidence of "nobody
  cites this" — it may be evidence that the index is two weeks behind, or that
  the reference string was matched by text parsing rather than by DOI.
- Read together, the Japanese sources describe a resolution ladder whose
  bottom two rungs are text inference. The lane's chain CLEAN should therefore
  record **how** a hop resolved, not merely **that** it resolved; a hop that
  resolved by rung 4 is not the same evidential object as one that resolved by
  DOI.
- The Chinese channel shows the cost of the lane's own tier rule applied to a
  genuinely open source: NCPSSD is free and authoritative but its full text is
  registration-gated, so it is a **tier-B** channel for claims about content
  the lane did not open, and a tier-A channel only for what it did open. This
  is the same distinction the lane already makes for free-but-incomplete
  sources, and it is why the Chinese rows in this round are scoped narrowly.
- Lateral reading is the technique the lane's held `S003` (SIFT) does not
  supply: SIFT is a heuristic list for a *known* source, whereas lateral
  reading prescribes *leaving* the source to read other sources about it. For
  a lane whose `verify-chain` exemption is "record-declared and unverifiable",
  that is the one method here that produces evidence about a source from
  outside the source.

#### Unknown

- Whether J-STAGE's four-step ladder records which rung produced each link.
  The FAQ describes the ladder but the per-link resolution rung was not
  observed; no claim is made that a reader can recover it.
- Whether the same derived-list caveat holds for Chinese indexes. CNKI returned
  a 381-byte shell to an automated fetch, so nothing about CNKI's
  reference-list or cited-by semantics was verified this round — see
  `CANNOT-ANSWER.md`.
- The APA full text of the lateral-reading study is paywalled; `S099` is scoped
  to the abstract, and the classroom effect size was not read.

---

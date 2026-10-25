# DraftEntryAgg — round-49 w1 report (draft of aggregator-vs-source-r36.md)

Scope: lane draft of the tool-rewritten adopt copy `.ufo/waves/round-49/assimilation/adopt/corpus/knowledge/aggregator-vs-source-r36.md` (staged S087,S088,S089,S091,S092 → lane S096..S100), re-grounded by document on the five bound captures, per seat instructions and QUALITY criteria 6–8, 10, 57, 66–67. No installation performed (RULES.md read; none needed). No production file, git index, or sibling surface touched; only this report was written.

## Commands and observed output

1. `python3 tools/inference-ground.py --entry /tmp/chousa-r49-DraftEntryAgg/aggregator-compact.md --spans /dev/null --counts /dev/null` (from lane root):

```
GROUND entry=aggregator-compact.md section=1 bullets=5 tokens=3 grounded=0
FINDING INF_TOKEN_NOT_IN_SPAN bullet=1 token='CiNii Researchの「参考文献」は、実際の論文の参考文献と必ずしも一致していません'
FINDING INF_TOKEN_NOT_IN_SPAN bullet=2 token='J-STAGEが連携している外部サービス に登録されている引用文献および被引用文献には、J-STAGEでの記事公開から数日～2週間後にDOIによるリンクが作成さ'
FINDING INF_UNGROUNDED bullet=3 token=''
FINDING INF_UNGROUNDED bullet=4 token=''
FINDING INF_TOKEN_NOT_IN_SPAN bullet=5 token='leaving an unfamiliar website to search the open Web before investing attention '
GROUND: FAIL
exit=1
```

Exit 1 as expected without a spans manifest (tool fails closed). Codes: `INF_TOKEN_NOT_IN_SPAN` for bullets 1/2/5 (tokens extracted, no spans to check); `INF_UNGROUNDED` for bullets 3/4 (their quotes are Japanese/Chinese-only, so the tool's `has_two_words` lexical rule extracts no token — QUALITY 66's named limit; grounding for those bullets is the manual verbatim check below).

2. Verbatim occurrence count of every Inference-section quote in its capture (each printed count must be 1):

```
1 09fc63de41f293d43d631c46.txt
1 09fc63de41f293d43d631c46.txt
1 167e9db7dde3c998838e3469.txt
1 fea98dc5a5a486c988dd415c.txt
1 fea98dc5a5a486c988dd415c.txt
1 fea98dc5a5a486c988dd415c.txt
1 76914d78c20094f677dea77d.txt
1 76914d78c20094f677dea77d.txt
1 32d1d24b24fce96d2a078ec0.txt
```

(capture keys: S096 09fc63de…, S097 167e9db7…, S098 fea98dc5…, S099 76914d78…, S100 32d1d24b…; quotes in TSV below, in order).

## Lane-bar checks

- Metadata header: `source: S0xx — <url>` shape kept exactly; S099 header narrowed (help-page URL removed — not a bound row); `verified-at`/`recheck` kept with NCPSSD item-7 reference replaced by the 登录/注册 header.
- Every `#### Inference` bullet cites ≥1 S-id and quotes a phrase found verbatim in that id's capture (count 1/1 above); quotes used affirmatively, no negation flip against the captures; figures kept out of Inference bullets.
- Support states kept distinct: capture-based observations vs identities inference vs unknowns; NCPSSD access-model claims (free-after-registration, PDF-download-gated, online-reading-only) are dropped, not silently kept — the homepage capture carries none of them, and the absent-defect register independently registers the same two help-page quotes as `payload-absent` for chousa round1 S086 (https://www.ncpssd.cn/) at `absent-defect-register.md:41`.
- No live-access claims: all reads are on-disk `.qcache` captures (no egress; L0 `8d77e6c1` open).
- No unfilled placeholders; observations/inference/unknown separated; removed claims recorded in Unknown.

## Findings

1. Staged entry over-claimed NCPSSD: the help-page access model was attributed to S099 although the bound row is the homepage; both claims now removed/narrowed (observation 4, inference bullet 4) and the open access-model question recorded in Unknown.
2. J-STAGE ladder is carried by S098 capture lines 2907/2923/2931 (`システムが引用元の所在を特定できた文献にリンクを付与しています`, steps 1–4), not by the publisher page; observation 2 now names S098.
3. Temporal/lateral quotes verified verbatim in S097 line 589 and S100 line 104 (incl. n=271/n=228 and "matched control design" in the abstract).
4. CiNii 注意書き verified verbatim in S096 lines 565/567 (matched-item count, no cross-service equality).
5. Tool run with `/dev/null` spans fails as designed; codes above are the ones the seat must report.

## Drafted entry (lane version; fenced)

```
# A citation index's reference list is a derived artefact, and it is incomplete in time

source: S096 — https://support.nii.ac.jp/ja/cir/manual_articles_detail — section G 参考文献／被引用文献, the two 注意書き — manual page read 2026-10-23
source: S097 — https://www.jstage.jst.go.jp/static/pages/ForPublishers/TAB2/-char/ja — sections 1, 2, 11 and 14 — page read 2026-10-23
source: S098 — https://www.jstage.jst.go.jp/static/pages/FAQs/TAB2/-char/ja — the 引用元の所在確認 passage and its four-step resolution list — page read 2026-10-23
source: S099 — https://www.ncpssd.cn/ — the site's 登录/注册 header and 资源 navigation — read 2026-10-23
source: S100 — https://eric.ed.gov/?id=EJ1372738 — the abstract on ERIC record EJ1372738 — read 2026-10-23
verified-at: 2026-10-23
recheck: 180d — re-open the five URLs and confirm both CiNii 注意書き, the J-STAGE four-step list, the timing sentence and the NCPSSD 登录/注册 header are unchanged (ran 2026-10-23)
ground: frontier items 1 and 3 — citation-chain verification modes and source-tier adjudication; the lane's chain CLEAN proves an anchor's existence, exemption is record-declared, one hop at a time with no transitivity, and the lane holds no CJK row against which its own tier rule could be checked

#### Observation

- **The operator says so itself (Japanese).** NII's CiNii Research manual states that its 参考文献 "are not necessarily the same as the paper's own references" — only those matched by the service's 同定・統合処理 are shown — and that "the reference count … is of the matched items, not the count printed in the paper." The manual further notes that CiNii Research and CiNii Articles identify and merge differently, so the two services' lists need not match each other.
- **Resolution is a heuristic ladder (Japanese).** J-STAGE's publisher FAQ (S098) states that a citation link is attached only where the system could locate the reference's source, and confirms the location in this order: DOI from the metadata item; bibliographic metadata; a DOI extracted from the reference text; then the reference text parsed into bibliographic data. Steps 3 and 4 are inference from text, not identifier resolution.
- **The chain grows after publication (Japanese).** J-STAGE states that DOI links to citation and cited-by works are created "from a few days to two weeks after" the article is published, and that a DOI can only be used as a URL one to several days after publication.
- **A national centre whose homepage gates access behind registration (Chinese).** The 国家哲学社会科学文献中心 is built by the Chinese Academy of Social Sciences Library (中国社会科学院图书馆承建); its homepage header asks visitors to 登录/注册 (log in / register), and the resource navigation lists 外文期刊, 外文图书 and 古籍. The homepage capture does not carry the access-model statements the staged draft attributed to the help page (free after registration; full-text PDF download only for registered users; foreign journals and 古籍 online-reading only), so those claims are dropped; the help URL is not a bound row this round.
- **Reading a source *about* the source (Western).** The lateral-reading heuristic — "leaving an unfamiliar website to search the open Web before investing attention in the site at hand" — was tested in a matched-control design (n=271 against n=228) and produced significant growth in students' ability to judge the credibility of digital content.

#### Inference

- Two independent operators, in the same literature, publish the same admission in different words: an index's reference list is derived from the source's reference list, and is neither equal to it nor a superset of it. S096 states `CiNii Researchの「参考文献」は、実際の論文の参考文献と必ずしも一致していません` and says the count is only `同定・統合された分をカウントしています`. That is the lane's own tier rule — an aggregator is never the source — arriving as a first-party statement from the aggregator, rather than as the lane's inference. It is the cleanest external support this round produced for scoping an aggregator row to tier C.
- The lane's chain check has a **temporal** blind spot that neither the lane's gate nor its corpus records. S097 states the links are created `J-STAGEが連携している外部サービス に登録されている引用文献および被引用文献には、J-STAGEでの記事公開から数日～2週間後にDOIによるリンクが作成されます`; a hop checked against a citation index can be unresolved simply because the index has not yet ingested the reference, and the same index's own count for a paper is a matched-item count. A '0 inbound citations' reading is therefore not evidence of 'nobody cites this' — it may be evidence that the index is two weeks behind, or that the reference string was matched by text parsing rather than by DOI.
- Read together, the Japanese sources describe a resolution ladder whose bottom two rungs are text inference. S098 states the system links only the works whose source it located (`システムが引用元の所在を特定できた文献にリンクを付与しています`) and resolves in a fixed order (`引用元の所在確認は、次の順で解析・検索を実施しています`), ending with the reference text parsed into bibliographic data (`4.引用文献の原文情報を書誌情報に解析して検索`). The lane's chain CLEAN should therefore record **how** a hop resolved, not merely **that** it resolved; a hop that resolved by rung 4 is not the same evidential object as one that resolved by DOI.
- The NCPSSD homepage gates access behind a user account, but its access model is unverified from S099. The homepage asks visitors to `请 登录 注册` and names `中国社会科学院图书馆承建` as the builder; it does not state that the service is free after registration, that full-text PDF download is restricted to registered users, or that foreign journals and 古籍 are online-reading only — the staged draft's help-page claims are not carried by the homepage capture, and the help URL is not a bound row, so no tier verdict is made for NCPSSD this round.
- Lateral reading is the technique the lane's held `S003` (SIFT) does not supply: SIFT is a heuristic list for a *known* source, whereas lateral reading prescribes *leaving* the source to read other sources about it — S100 defines it as `leaving an unfamiliar website to search the open Web before investing attention in the site at hand`. For a lane whose `verify-chain` exemption is 'record-declared and unverifiable', that is the one method here that produces evidence about a source from outside the source.

#### Unknown

- Whether J-STAGE's four-step ladder records which rung produced each link. The FAQ describes the ladder but the per-link resolution rung was not observed; no claim is made that a reader can recover it.
- Whether the same derived-list caveat holds for Chinese indexes. CNKI returned a 381-byte shell to an automated fetch, so nothing about CNKI's reference-list or cited-by semantics was verified this round — see `CANNOT-ANSWER.md`.
- Whether NCPSSD's access model is free-after-registration, PDF-download-gated, or online-reading-only for some categories; S099 (homepage) does not carry those statements, and the help page URL is not a bound row in this round's capture set.
- The APA full text of the lateral-reading study is paywalled; `S100` is scoped to the abstract, and the classroom effect size was not read.

---
```

## TSV — Inference-section grounding quotes (each occurs exactly once in its capture)

```
id	url	quote	entry
S096	https://support.nii.ac.jp/ja/cir/manual_articles_detail	CiNii Researchの「参考文献」は、実際の論文の参考文献と必ずしも一致していません	Inference bullet 1
S096	https://support.nii.ac.jp/ja/cir/manual_articles_detail	同定・統合された分をカウントしています	Inference bullet 1
S097	https://www.jstage.jst.go.jp/static/pages/ForPublishers/TAB2/-char/ja	J-STAGEが連携している外部サービス に登録されている引用文献および被引用文献には、J-STAGEでの記事公開から数日～2週間後にDOIによるリンクが作成されます	Inference bullet 2
S098	https://www.jstage.jst.go.jp/static/pages/FAQs/TAB2/-char/ja	システムが引用元の所在を特定できた文献にリンクを付与しています	Inference bullet 3
S098	https://www.jstage.jst.go.jp/static/pages/FAQs/TAB2/-char/ja	引用元の所在確認は、次の順で解析・検索を実施しています	Inference bullet 3
S098	https://www.jstage.jst.go.jp/static/pages/FAQs/TAB2/-char/ja	4.引用文献の原文情報を書誌情報に解析して検索	Inference bullet 3
S099	https://www.ncpssd.cn/	请 登录 注册	Inference bullet 4
S099	https://www.ncpssd.cn/	中国社会科学院图书馆承建	Inference bullet 4
S100	https://eric.ed.gov/?id=EJ1372738	leaving an unfamiliar website to search the open Web before investing attention in the site at hand	Inference bullet 5
```

(`S003` and `verify-chain` are cited designators, not grounding quotes, so they are not TSV rows.)

Out of scope for this seat: SOURCES.md registry rows/`used-by` updates, span-file compilation, and the C1/C2 counter runs (other seats). Scratch `/tmp/chousa-r49-DraftEntryAgg/` deleted on finish.

VERDICT: Drafted the lane version of aggregator-vs-source-r36.md re-grounded by document on on096–S100 (9 verbatim quotes, one occurrence each), narrowed the NCPSSD access-model claims the captures do not carry, and reported the inference-ground finding codes (INF_TOKEN_NOT_IN_SPAN ×3, INF_UNGROUNDED ×2 with spanless manifests) — draft complete.

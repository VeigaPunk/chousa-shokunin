# W2 ReviewRows — S096–S103 registry rows vs census schema and CORPUS.md row rules

Seat: ReviewRows (leaf, no subagents). Scope: the eight appended rows `SOURCES.md:106-113`
against SOURCES-CONTRACT-v1 (CORPUS.md `## SOURCES.md`), tier choices, duplicate URLs
(url_of normalisation), and used-by exactness. Frozen predicates untouched.

## 1. Validator (required command, run from lane checkout)

```
$ export TMPDIR=/dev/shm/chousa-r49-ReviewRows
$ bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin chousa
chousa	W04	S051 duplicate url www.w3.org/TR/2017/REC-html52-20171214/syntax.html across scopes
chousa	W04	S053 duplicate url docs.python.org/3/library/socket.html across scopes
chousa	W04	S073 duplicate url www.gnu.org/software/coreutils/manual/coreutils.html across scopes
chousa	W04	S074 duplicate url docs.python.org/3/library/hashlib.html across scopes
chousa	W04	S075 duplicate url www.gnu.org/software/coreutils/manual/coreutils.html across scopes
chousa	ok	/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/SOURCES.md   (exit=0)
```

No E-codes. The five W04 warnings all name ids <= S095 (pre-existing rows); none of
S096-S103. So: 11 cells per row (E01), valid unique ids (E02/E03), kind/tier/status
enums legal (E05-E07), opened 2026-10-25 is present-day (E08), rechecks legal (E09),
no community-at-A (E10), used-by paths exist (E11), no row outside `## Registry` (E12).
Rows sit inside the Registry section (`## Paths` starts after S103, SOURCES.md:115).

## 2. Duplicate URL vs older rows (url_of normalisation) — none

Census evidence: E04 (same URL+scope, non-rejected, no supersedes) is silent and W04
(same URL across scopes) names only older rows, so no new-row URL collides with ANY
registry row under the script's url_of (strip fragment, strip trailing slash, strip
scheme, lowercase host). Independent whole-file check:

```
$ for u in support.nii.ac.jp jstage.jst.go.jp eric.ed.gov zcmu.edu.cn jc.hit.edu.cn \
           toho-shoten.co.jp library.um.edu.mo; do grep -n "$u" corpus/SOURCES.md; done
106:| S096 | ... https://support.nii.ac.jp/ja/cir/manual_articles_detail |...   (only hit)
107:| S097 | ... https://www.jstage.jst.go.jp/static/pages/ForPublishers/TAB2/-char/ja
108:| S098 | ... https://www.jstage.jst.go.jp/static/pages/FAQs/TAB2/-char/ja          (distinct path)
109:| S099 | ... https://eric.ed.gov/?id=EJ1372738
110:| S100 | ... https://www.zcmu.edu.cn/__local/...C3A00.doc?e=.doc
111:| S101 | ... https://jc.hit.edu.cn/_upload/article/files/...doc
112:| S102 | ... https://www.toho-shoten.co.jp/export/sites/default/cnki/help/cnki-kns80.pdf
113:| S103 | ... https://library.um.edu.mo/upload/databases/c1b0fa89...pdf
```

Each URL occurs exactly once, on its own row. S097/S098 share the host but differ in
path, so no collision under url_of. The `?e=.doc` query is a Plone download marker,
not a credential/session URL (rule 6 respected).

## 3. Ids contiguous, new since BASE_REV

```
$ git show 414a2ec6cde05a921dbdd9e02e7ae56b0db647ef:corpus/SOURCES.md | grep -oE '^\| S[0-9]+' | tail -3
| S093 | S094 | S095
```

Base max = S095, so S096-S103 are the next unused ids, contiguous, never reused
(rule on ids; Gate mapping `lessons/round-49.md:55-62` shows staged S087/S088/S089/S092
-> S096-S099 and staged S100-S103 keeping their numbers by document).

## 4. used-by exactness — one gap on S096

`source:` lines vs used-by cells:

- `aggregator-vs-source-r36.md:4-7` names S096, S097, S098, S099; rows S096-S099
  used-by = `corpus/knowledge/aggregator-vs-source-r36.md` only. Exact.
- `citation-count-semantics-r37.md:4-7` names S100-S103; rows S100-S103 used-by =
  `corpus/knowledge/citation-count-semantics-r37.md` only. Exact.
- No other knowledge file cites S096-S103: `grep -rlc 'S09[6-9]|S10[0-3]' corpus/knowledge/`
  returns only those two entries. Lesson Gate mentions do not enter used-by by lane
  convention (round-24.md mentions S001 twice; S001 used-by lists only the knowledge
  entry, SOURCES.md:8).

FINDING (low): S096's used-by cell (SOURCES.md:106) omits a citing entry.
`citation-count-semantics-r37.md` body-cites S096 three times — :45-46 and :52-53 each
with the inline byte-exact quote `CiNii Researchの「参考文献」は、実際の論文の参考文献と必ずし
も一致していません`, and :75 `the CiNii admission (S096)`. The lane's own convention
counts body citations: S003's used-by (SOURCES.md:8) lists
`citation-chain-fidelity-r24.md`, whose only S003 link is 5 body mentions (no
`source: S003` line; its `source:` names S005). Per CORPUS.md, used-by is "paths of the
knowledge entries or lessons citing the row", so S096 should also name
`corpus/knowledge/citation-count-semantics-r37.md`. This does not break the frozen C2
predicate (binding is defined by the `source:` line; used-by "names the citing entry" —
satisfied), passes every census code, and is a legal in-place used-by change (rule 2,
logged old->new). Effect if left: an S096 recheck sweep will not surface r37 as a
consumer of the CiNii row.

Minor observation (not a defect): S101 kind=`docs` where `spec` is arguably the better
enum for 《中国学术期刊（光盘版）检索与评价数据规范》. Enum-legal, judgment cell, no rule broken.

## 5. Tier choices — right

Contract (CORPUS.md): A = primary/authoritative for the scope (official docs), B =
strong secondary, tier scoped, census only penalises inflation (E10).

- S096 (NII's own CiNii manual, support.nii.ac.jp), S097/S098 (JST's own publisher
  page and FAQ, jstage.jst.go.jp): kind=docs, tier=A — first-party official docs.
  Correct.
- S099 (ERIC record EJ1372738, paper, B): the APA full text is paywalled; the row
  scopes itself to "the statements in the abstract" and r36:80 keeps the full text out
  of scope. An index record is not the original paper, so B with a narrowed scope is
  the calibrated choice (A would overclaim first-party authority). Correct.
- S100 (CNKI's own note, university-hosted copy) and S101 (specification, HIT-hosted
  copy), tier=B: first-party content behind an unverified copy channel; B avoids
  claiming authority for the copy's provenance, and r37:70 discloses the hosting.
  Correct.
- S102 (東方書店 CNKI KNS8.0 guide) and S103 (澳門科技大學圖書館 CNKI AI guide), tier=B:
  third-party write-ups; S102's scope even disclaims first-party status. Correct.

No inflation anywhere; the A rows are exactly the first-party pages, matching the
frozen tier scheme (A for NII/J-STAGE first-party; B for ERIC abstract, copies,
third-party guides).

## 6. Row-rule spot checks (CORPUS.md shape + rules 1-2)

- anchor: every row carries section/heading plus located char offsets of quotes
  (SOURCES.md:106-113 anchor cells); all offsets in the anchor cells match Gate quote
  offsets row-for-row (round-49.md:77-104; e.g. S096 3599/3707/3752, S101 11170/11205/
  11993/12161/34374). Not bare homepages. Capture form+sha recorded per quote; same
  capture-anchored convention as the adopted S089-S094 rows.
- rule 1 Gate grounding: URL per row in the mapping table (round-49.md:55-62), access
  date "access 2026-10-25; captures written 2026-10-23; no fetch" (:66), located quotes
  (:77-104). All eight rows covered.
- rule 2 append-only: rows appended after S095, no older cell rewritten (validator
  clean; only status/recheck/used-by are mutable in place).
- the refused staged NCPSSD homepage never became a row: `grep -c ncpssd
  corpus/SOURCES.md` = 0; refused with URL in the register at round-49.md:133
  (`refused-doc: https://www.ncpssd.cn/`).
- recheck cadences 90d/180d/365d all match `NNd` (E09-clean); 365d has abundant older
  precedent (S002, S016...).

## Residual risk / gaps

- I did not re-run c1/c2 counters (other seats own them; measured C1=PASS C2=PASS in
  measure-after.txt). Quote byte-exactness inside captures and the span-file digest
  chain were not independently re-verified here — only anchor-offset correspondence.
- lsp device not used: no language server applies to a Markdown registry + bash
  validator; text/semantic checks above are the applicable method.
- The S096 used-by gap is the only actionable defect found; everything else in scope
  holds.

VERDICT: eight appended rows S096-S103 vs census schema/CORPUS row rules — partly —
schema, tiers, URL-dedup, id contiguity and Gate grounding all hold, but S096's used-by
cell omits body-citer corpus/knowledge/citation-count-semantics-r37.md (r37:45,52,75),
contrary to the lane's own body-citation convention (S003 precedent).

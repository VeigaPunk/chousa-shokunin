# CritTheme — C2 depth & expansion critique (round 49 w1)

Seat: `CritTheme` (`/skill:godspeed`). Target: frozen C2 (`corpus/evidence/round49/claims.md:48-85`),
staged adopt copy in `.ufo/waves/round-49/assimilation/adopt/corpus/knowledge/`, counted by `c2-count.py`.
No writes outside this report; no scratch dir created.

## 1. Counterexample (the strongest found)

The two entries claim to re-ground the theme BY DOCUMENT on nine on-disk captures, but as written their
quoted claim-sentences are **not present in the bound captures**:

- `aggregator-vs-source-r36.md:15-31` quotes **English translations**: "are not necessarily the same as the
  paper's own references", "the reference count … is of the matched items, not the count printed in the
  paper", "from a few days to two weeks after". The captures are Japanese; the actual text lives at
  `09fc63de….txt:565` (`※CiNii Researchの「参考文献」は、実際の論文の参考文献と必ずしも一致していません。…同定・統合された分をカウントしています。`) and `:567`, `167e9db7….txt:565,589`, `fea98dc5….txt:2923-2931`. No English sentence exists anywhere in the cache.
- `citation-count-semantics-r37.md:14-18` quotes the CNKI self-citation rule (`…认定为自引`); the bound
  capture `b539a80218080da56a75b624.txt` (the zcmu `.doc`) is an OLE binary whose text form is 40.5%
  U+FFFD and has **zero hits** for 自引/引文数据库/任一合作者 under utf-8/utf-16-le/utf-16-be/gbk/gb18030/big5
  (round-47 lesson `round-47.md:245-250` already refused this entry for exactly this).
- `citation-count-semantics-r37.md:24-28` quotes the spec fields (`文献类型及载体类型标志`, `GB/T 7714`…);
  the bound hit `.doc` capture `6dc68fd6….txt` has **zero hits** for all of them.
- `aggregator-vs-source-r36.md:32-37` quotes NCPSSD registration/download statements; the bound
  `ncpssd.cn` capture `76914d78….txt` lacks them (only 登录/注册 header, `:51`); they exist only in the
  help-page capture `c4e1446a….txt`, a different URL than the row's.

`c2-count.py:174-181` requires each span quote to be inside a span file that is an exact slice of the
capture text form at the recorded offset (`CAPTURE_BOUND`), and `:172` requires the quote inside the entry.
English paraphrase quotes therefore cannot satisfy the frozen predicate; the two `.doc` quotes cannot be
satisfied by any text form of the current captures. Under the C2 predicate, this is not a cosmetic defect:
`BOUND>=7` with quote legs n/n and anchor offsets at located quotes all fail for S096/S101/S102 (and
arguably S099 unless spans point at the help capture).

## 2. Evidence

Capture digests (sha256(url)[:24]; all nine exist in `.qcache`):
```
09fc63de41f293d43d631c46  support.nii.ac.jp/ja/cir/manual_articles_detail        (6421B txt)
167e9db7dde3c998838e3469  jstage.jst.go.jp/static/pages/ForPublishers/TAB2/-char/ja
fea98dc5a5a486c988dd415c  jstage.jst.go.jp/static/pages/FAQs/TAB2/-char/ja
76914d78c20094f677dea77d  www.ncpssd.cn/
32d1d24b24fce96d2a078ec0  eric.ed.gov/?id=EJ1372738
b539a80218080da56a75b624  www.zcmu.edu.cn/__local/…/…C3A00.doc?e=.doc   (OLE d0cf11e0)
6dc68fd6b32ce9c8dfcebce8  jc.hit.edu.cn/_upload/article/files/…/…9d508.doc      (OLE d0cf11e0)
7809d5114330a60527436b07  toho-shoten.co.jp/export/sites/default/cnki/help/cnki-kns80.pdf
02aefcf570a7108e699d0990  library.um.edu.mo/upload/…/c1b0fa89….pdf
```
String-present checks (Python `find`, run today): CiNii 同定・統合処理 @3675; J-STAGE pub
被引用文献リンク機能 @1959, ダークアーカイブ @1802, iThenticate @6346; J-STAGE FAQ 3/4 steps @29749/29775
(1/2 missing except `:2925-2931` with spacing); ERIC lateral reading @1217, Wineburg @823; toho 被引用回数
@13531; um 引用量 @959, 溯源 @780. Zero hits: zcmu for all 5 needles; hit for all 6 needles; ncpssd
for both quoted sentences. zcmu txt 308,430 U+FFFD = 40.5%; hit txt 14,486 = 11.3%; both raw are OLE
(magic d0cf11e0), no encoding decodes them without errors.

Prior verdicts (absent-defect-register.md, `chousa` rows): round1 S082 (CiNii), S084 (J-STAGE FAQ),
S086 (NCPSSD), round2 S095 (zcmu), S096 (hit) — all `payload-absent` (fabrication class).
`quote-lint-full-v5.json:1234-1250` agrees for zcmu. Round-47 lesson `round-47.md:244-250` rejected the
staged `citation-count-semantics-r37.md` with the same zero-hit evidence; its flip ("a byte-faithful capture
of S100/S101 that holds the quoted sentences") is unmet — digest unchanged, mtimes 2026-10-23.

Held ground (grep of lane corpus): no CiNii/J-STAGE/CNKI/被引/lateral-reading/self-citation anywhere in
`corpus/`; jstage appears only as an exempt chip host (`C-r9.md:43`). Held: the ladder and tier rule
(`knowledge/contextual-source-admission-r24.md:51-60`, SKILL.md:18), held S003=SIFT (`SOURCES.md:13`),
chain CLEAN = existence only (`knowledge/chain-resolution-r3.md`), "derived artifact at true tier" for the
lane's own converted records (`lessons/2026-10-16-verifying-conversion-not-original.md:31,146`).

## 3. Impacted axes

- **depth**: verifiable-detail & citation requirements not met as written for S096/S099/S101/S102 (4 of 9);
  S097/S098/S100/S103/S104 content is genuinely in-capture but quoted as translation paraphrase, so even
  these fail the verbatim-quote leg in the current rendering.
- **calibration**: both entries' `ground:` lines cite "(S076)" — a **staged** package id; after adoption
  lane S076 is the GNU sed manual (`SOURCES.md:86`), so the pointer would resolve falsely. `citation-count-
  semantics-r37.md:76` says CNKI's site "again this round" returned a shell — no fetch occurred this round
  (L0 open), so "again this round" is not supportable.
- **expansion**: the *conclusion* half ("aggregator is never the source"/tier rule) duplicates held ground;
  the *documentary/mechanism* half is new.

## 4. Smallest safe correction (no predicate change)

1. Quote the **actual capture bytes** (Japanese/Chinese) for S096-S100, marking translations as "loc. cit.
   (translated)" and not as quoted words — this is what `QUOTES_IN_SPAN` + `CAPTURE_BOUND` demand.
2. S101/S102: cannot be bound until an approved extraction renders the OLE `.doc`s to text and the quoted
   sentences appear in the cache (register flip); until then refuse them (lesson `refused-doc` lines) or
   move the claims to Unknown — the "as these copies state" scope is then honest.
3. Point the NCPSSD row/span at the help-page capture `c4e1446a…` (the URL actually carrying the quotes) or
   refuse S099 likewise.
4. Replace "(S076)" with the merge-package row identifier + URL so it survives adoption.

## 5. Claim-by-claim credit (duplicate vs new)

Duplicates (no credit): "aggregator is never the source" (A-vs-S Inf1) — held in contextual-source-admission-r24
+ SKILL.md; NCPSSD tier-B application (Inf4) — held tier-for-scope rule; 溯源-as-claim-to-source (CCS Inf3) —
held claim-support method; "derived artefact" for the lane's own records (r9 lesson) — different object.
New ground: CiNii matched-item counting & 同定・統合処理 filtering; J-STAGE four-step heuristic ladder; temporal
lag ("0 citations ≠ nobody cites") & resolution-rung recording; lateral reading vs held SIFT; CNKI
co-authorship self-citation rule (content new, but ungroundable on disk); 被引 vs 下载量 separation; 引文网络
graph; 文献标志码 A–E selection; CNKI AI 溯源 counters.

## Decision

Depth: improved content, **not yet verifiable as written** (6/9 in-capture, 4/9 quote-mismatched or
ungroundable). Expansion: improved on ≈7 new propositions; ≈3-4 duplicate/( (principle, tier application).
Counterexample stands: the staged entries cannot satisfy the frozen C2 counter without the corrections above.

VERDICT: attacked C2 depth/expansion — 4/9 bound documents (CiNii, NCPSSD, zcmu, hit) have no verbatim quote text in their bound captures as adopted (2 are undecodable OLE, 3-5 carry prior payload-absent verdicts), so depth is improved in content but fails as written; expansion is largely new with the aggregator≠source principle and tier-rule applications duplicating held ground; smallest safe correction is quote-actual-bytes + refuse/re-extract the two .docs + correct the S076 ground pointer.

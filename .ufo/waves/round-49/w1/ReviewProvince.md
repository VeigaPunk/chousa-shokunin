# ReviewProvince — round 49 w1 — province & QUALITY bar, two staged entries

Seat: ReviewProvince (leaf, no subagents). Date 2026-10-25. No scratch dir created (checks in-memory); no tools installed (pacman paused; none needed).
Read-only inputs: PROVINCE.md, corpus/QUALITY.md, corpus/README.md, frozen `corpus/evidence/round49/claims.md`, staged package, 10 captures, landed registry and entries, `corpus/lessons/round-49.md`. Only write: this file.
Package identity: `sha256sum` staged files → SOURCES.append.md `a6dec4a0086d3cf7…` (matches lesson `## Gate`), entries `29b9ad25…` / `68a8db1a…`.

## Entry 1 — aggregator-vs-source-r36.md (staged)

**Province: IN.** PROVINCE.md "Owns": source hierarchy (primary/secondary/aggregator/unsourced), citation chaining and hop resolution, claim-vs-source verification. No kengaku content (the ERIC study is a human-subject credibility study, not a model-quality/evaluation claim), no kasegi, no kumitate.

**Bullets that must narrow (as staged):**
1. ERIC bullet asserts outcome as fact: "was tested … and produced significant growth" — QUALITY 8 (support states): the abstract *reports* the outcome; truth is not established from "source states the claim", and the staged Unknown itself concedes the effect size was not read. Narrow to abstract-reported wording.
2. NCPSSD bullet: "free to the public after registration" — the help capture says 公益 + 注册后可使用; probe `免费` in the tag-stripped help text → False. "full-text PDF download only to registered users" overreaches item 7, which scopes download to 中文期刊论文 (PDF appears only in item 8).
3. `recheck: 180d — re-open the five URLs` — a live re-fetch under open L0 `8d77e6c1`; not runnable within the lane's no-fetch posture; must name the constraint (capture re-open or approval-gated live check).
4. `verified-at: 2026-10-23` bare — QUALITY 6 wants ISO date + what was checked.

**QUALITY criteria it fails as staged:** 6 (ids S087–S092 are staged ids; lesson `comm -12` shows staged ids collide with lane rows S082–S095 naming other documents → unbound tokens, REF_UNRESOLVED class); 7 (tier/scope checkable only after by-document renumber); 8 (bullet 1); 13 (recheck runnability); 25/30 (register rows on three of its URLs are flagged `payload-absent`).

**Document grounding (my checks):** CiNii capture `09fc63de41f293d43d631c46.txt:565` carries both 注意書き verbatim (matched-item display and count; :567 the CiNii Articles difference); J-STAGE publisher `167e9db7…txt:565` (DOI URL 1日～数日), `:589` (links 数日～2週間後), `:778` (Portico), `:834` (iThenticate); FAQ `fea98dc5…txt:2911-2931` (手動/自動検索 + four-step ladder); ERIC `32d1d24b…txt:104` raw line: "n = 271 … n = 228 … grew significantly in their ability to judge the credibility of digital content".

**Verdict: ADMIT-WITH-NARROWING.** Every load-bearing quote is in the held captures; the landed copy already applies the narrowing (ERIC re-worded as "reports … and says"; NCPSSD bullet moved to Unknown as a refused row with flip; re-bound to S096–S099; `recheck: 180d` bare cadence; re-opened 2026-10-25 noted per source line). Refusal would be wrong on the evidence.

## Entry 2 — citation-count-semantics-r37.md (staged)

**Province: IN.** What an index's counter counts is claim-vs-source verification (a number is a claim; the index is its source; the counting rule is its provenance) plus source hierarchy (copies/third-party guides tier B). The 期刊评价 string is quoted as the spec's own stated purpose — data, not an endorsement of evaluation methodology; no model-quality claim → not kengaku. No kasegi/kumitate content.

**Defects as staged:**
1. Mis-attribution (QUALITY 8, whose-statement): bullet 2 "CNKI's own guide describes the result list fields" and inference 2 "CNKI's own guide names them" — the document is 東方書店's third-party KNS8.0 guide (row scope: "third-party description, not CNKI's own documentation"). Landed copy: "A third-party guide to the CNKI interface (Japanese)".
2. Ground line cites `(S076)` — a campaign-era id that names the lane's GNU sed manual row (`corpus/SOURCES.md:86`), not the wave-1 CiNii finding; unbound token, fails the frozen C2 all-tokens-bound leg. Landed copy re-points it to S096 with an explicit `adopted:` note.
3. Bullets 1 and 3 rest on the two OLE `.doc` captures whose `.txt` text forms are lossy (txt-heads are U+FFFD runs) — exactly the register's r2 S095/S096 `payload-absent` rows. My byte search of the `.raw` files found every quoted string as UTF-16LE: zcmu 任一合作者@2902, 他引频次@2568, 中国引文数据库@2624, 被引频次为0的文献将不会显示@5722; hit 文献标志码@21844, 统计和期刊评价@22352, GB/T 7714@24000, 载体类型标志@24332, ISO 690@26498. Tool limit (QUALITY 25), not fabrication; binding must read the raw's UTF-16LE text (landed rows do).
4. The staged "deferred to GB/T 7714" inherits register r2 S096 q3's misreading; the capture's parameter table says ISO 690 (raw@26494 参照ISO) while section 14 has GB/T 7714. Landed copy records the split (bullet 2 + Unknown).
5. Same recheck/verified-at narrowing as entry 1.

**Verdict: ADMIT-WITH-NARROWING.** Landed copy: re-bound to S100–S103, third-party attribution fixed, ISO/GB-T split recorded, the CiNii derived-list admission explicitly not transferred to CNKI, plus a grounded new observation (被引频次为0的文献将不会显示, raw@5722).

## By-document register verdicts (independent; agree with lesson `## Gate`)

- r1 S082 (CiNii): registered quote swaps が/を and splices a sentence; correct text at `09fc…txt:547-571` → absent-as-written, not fabricated.
- r1 S084 (J-STAGE FAQ): steps present but formatting-split (`fea9…:2911-2931`) → absent-as-written.
- r1 S086 (NCPSSD): item 7 sentence verbatim in the help capture (my tag-stripped extraction of `c4e1…` line 318; lesson pins offsets 24872/25269); homepage capture `7691…` carries only 登录/注册 + 承建 line (grep) → refusal of the homepage row is grounded; flip (help-page row) is supported by my check.
- r2 S095 (zcmu) / r2 S096 (hit): quotes in `.raw` UTF-16LE, absent from lossy `.txt` → absent-as-written / tool-limit, not fabricated.

## Cross-cutting checks

- Landed registry rows S096–S103 (`corpus/SOURCES.md:106-113`): all `mined`, opened 2026-10-25, recheck cadences, used-by naming the citing entries; S101's teaches cell carries the section-14/parameter-table split.
- Lesson's "stripped" used-by values (`source-type-taxonomy-r37.md`, `chinese-search-log-r37.md`) name files that do not exist (glob: no match); landed S101/S102/S103 used-by cells carry only `citation-count-semantics-r37.md` — no dangling backlink.
- All S### tokens in both landed entries: entry 1 = S096–S099 + held S003; entry 2 = S100–S103 + S096. All bound. No stray tokens.
- Adopt-scratch `renumber.tsv` (S091→S099 ncpssd, S092→S100 ERIC) is the stale pre-refusal plan; the lesson's `adopt-final` map and the landed registry agree (S099=ERIC, S100=zcmu … S103=um, NCPSSD refused). No action; recorded so no seat "fixes" the landed ids back to the scratch map.

## Residual risk / verification gaps

- I verified load-bearing strings by independent byte search, not every `spans.tsv` offset (the frozen counter's job).
- CNKI first-party semantics remain unknown (381-byte shell; both entries and the lesson keep that unknown named).
- The staged "twenty searchable fields" claim is grounded in the toho capture (`7809…txt:484-486` "…被引频次 20 項目を検索対象とすることができます") but the landed entry dropped it — no action needed.

VERDICT: attacked both staged entries by document — every load-bearing quote verified against the ten held captures (two `.doc` text forms proven lossy with quotes recovered from raw UTF-16LE), staged ids S087–S103 proven unbound collisions and S076 a mis-point to the GNU sed row; both entries are in-province (source hierarchy / citation chaining / claim-vs-source, no kengaku/kasegi/kumitate spillover) and ADMIT-WITH-NARROWING, with the narrowing already landed in the re-bound production copies and the five register rows correctly dispositioned absent-as-written (none fabricated).

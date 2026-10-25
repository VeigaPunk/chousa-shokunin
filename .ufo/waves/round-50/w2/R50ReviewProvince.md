# R50ReviewProvince — province and QUALITY bar per landed entry (wave 2)

Attacked: the three LANDED C2 entries' province membership, per-bullet method-vs-product
content, and admission-bar conformance (QUALITY 1–79 where binding). Method: re-opened
every located quote against the committed captures, re-ran the frozen counters and each
entry-facing check, and compared each adopted entry against its staged source.

## Verification (commands run, observed output)

- Quotes: all 55 `spans.tsv` rows — `cap[off:off+len(span)] == span`, quote inside span,
  unique in capture, ≤25 words / ≤160 chars: `rows 55 bad []`, `quote-not-once: []`
  (python over `.qcache/*.txt`; offsets are span-window starts, CONTEXT=80 — peer flag
  R50ReopenRowS105 confirmed not a defect; entry `char N` quote offsets verified
  independently, all 12 ISTIC + 20 S105 + 3 S106 quotes at stated offsets, count=1 each).
- Sweeps (entry-stated commands reproduced): ISTIC capture `核对/匹配/查重/全文|原文/版本|快照|snapshot|更新时间|数据日期 = 0`,
  `复核 = 1 line (3 occurrences)`, `逐条 = 0`, `CNKI|知网 = 0`, `中国科学院 = 5`,
  `中国科学技术信息研究所 = 0`; S105 `未收录/匹配/算法/字段/标识符/未找到/无结果/无匹配/诚信档案/科研/人事 = 0`,
  §6.1 slice `30727 31262 535 [0×8]`, `引文核对 = 4` (S106: 0, 教师: 0, ISTIC: 0),
  `相似度 = 3 (whole file, 0 in §6.1)`, `琥珀 = 0`; S106 `辅助/查重/匹配 = 0`;
  refused 教师 capture `引文核对/核对 = 0`, `引文 = 9`, located `教师可查看的报告单…去除本人` char 8033.
- `python3 corpus/evidence/round50/c2-count.py` → `C2=PASS` (`CAPTURE_BOUND=55/55`,
  `ANCHOR_BOUND=3/3`, `INFERENCE_GROUNDED=3/3`, `QUARANTINE_VERDICTS=0/0`), rc 0.
- `inference-ground.py` on all three entries → `GROUND: PASS` (r40 10/10, r41 7/7, r39 13/13).
- `prose-check.py` → 0 hits; `quote-substance-check.py` → `IDS=3 QUOTES=55 FAILURES=0`;
  `decode-form-check.py` → `FORM_NAMED`; `name-collision-check.py` w2-spec → 0, w1-spec → 13 (reproduced);
  `cited-id-check.py` on `renumber.tsv` + staged entries → `CITED_IDS=PASS rows=5`.
- `git grep -c '引文核对' 3c51da77 -- corpus/knowledge` → 0 (NEW_GROUND true at BASE_REV).
- Refused-entry spot check: r46's tally falsified exactly as the Gate says — S175 capture is
  28,114 chars with 比对×25, not "13,527 … 比对 10"; r42's own text limits its modes to the
  search platform (refusals sound). S105 `.txt` sha256 `2197abe2…`, 83,384 B; PDF `d36191c7…`, 4,482,989 B — match entry header.

## Per-entry verdicts

| entry | province | QUALITY bar now | generic bullets |
|---|---|---|---|
| `cnki-citation-check-r40.md` | IN — claim-vs-source verification (vendor-stated comparison source + verdict granularity); 管理员 account/role content does NOT drift: `管理员中心 子账号管理 and 校内互检` (bullet 4) is one provenance clause identifying which product carries the feature, not account-management content | passes every binding check (6/7/8/9/10/13/23/25/29/30/57/66/67/72/74—Q74 n/a per-entry) | Observation bullet 2's four-column list is UI inventory, marginal keep (feeds Inference 3, the re-open-the-matched-work chaining point); bullet 4's sibling-manuals clause is the weakest, foldable into the provenance clause |
| `citation-matching-semantics-r41.md` | IN — source-hierarchy (which copy documents the feature is a product fact checked per copy) + claim-vs-source (verdict granularity vs undocumented matching method); no product description stands alone | passes the same set; two borderline nits below | none generic; every bullet carries a located quote or a counted absence |
| `istic-citation-verification-r39.md` | IN, narrowed — the IN substance is method: a third-party citation-verification artefact (bibliography-vs-index comparison, co-author exclusion standard, supplied-result re-check route). The fee/commission content DOES drift into product description where it carries no method weight | passes the same set | CUT/FOLD: Obs bullet 3 "one commission, one report" (pure form mechanics), bullet 6 "five works or fewer has its own price" (generic price line; its only consumer, Inference 1, re-quotes char 662 itself so nothing ungrounds), bullet 9 "turnaround in working days" (pure product SLA). Partial: bullet 5's certificate-price scaffolding is fee detail serving one contrast; fold the 50元 clause into the 其他-row quote. Keep 7–8 (reuse waiver + 复核 route = supplied-result verification boundary) |

## Findings

1. **HIGH — the landing leaves QUALITY 74 / Mistakes row 1 false at tip.**
   `python3 corpus/evidence/round50/stale-count-check.py` → `STALE_HITS=8 UNRESOLVED=2 …
   STALE_COUNT=FAIL`, exit 1, on committed HEAD (`c5b8dca`, tree at `74794db` + spec commit).
   Two unresolved hits: (a) `LOG.md:1803 says 28, receipt 31` — Spot-check intake row 2 and
   Mistakes row 1 claim a `correction:` line was appended to LOG.md; `grep -n 'correction'
   LOG.md` finds none, LOG.md ends at line 1807, and `git show 74794db --stat` lists no LOG.md
   change — the promised correction was never landed; (b) `corpus/README.md:1080 says 55` —
   the new round-50 "55-row manifest" coverage-map row matches the check's `<n>-row manifest`
   pattern and is compared against the round-49 receipt of 31, an unavoidable new hit (the
   check cannot distinguish manifests). The committed `stale-count-before.txt` records only
   the four pre-correction hits; the receipt QUALITY 74 names — `stale-count-after.txt` —
   exists nowhere (`find`/git history confirm; only `w1/ExecStaleCount.md` holds a scratch
   PASS). Effect: a committed check fails on committed bytes and QUALITY 74's "after them
   STALE_COUNT=PASS, exit 0 (`stale-count-after.txt`)" is falsified as landed.
2. **MEDIUM — r41 Observation bullet 4 uses S105 outside its row's scope (QUALITY 7 nit).**
   The bullet quotes the 管理员 copy's §3.7 option (`char 27587`, verified in capture under
   heading `3.7 仅去除第一作者本人文献`) and labels it `(S105)`, but S105's row scope cell
   names only `第6章 辅助功能, 6.1 引文核对` (SOURCES.md:115). Criterion 7 makes a claim
   resting outside its row's scope an inference; the bullet sits under `#### Observation`.
   Fix is administrative (widen the row's anchor to name §3.7, or mark the clause inference);
   the quote itself is verbatim and the statement true.
3. **MINOR — r41 `verified-at:` lacks "what was checked" (QUALITY 6 nit).**
   Line 5 is the bare date `2026-10-25`; r39/r40 carry the checked-object text the criterion
   requires ("ISO date + what was checked"). Criterion 66's metadata-screen precedent says key
   presence ≠ compliance; a reader can infer it, but the form is short of the other two.
4. **MINOR — r39's `source:` anchor header mislabels char 662's home.**
   `source: S104 … the 收费标准 rows (char 422, char 549, char 662, char 735, char 849)` — in the
   capture, char 662 (`1.委托5篇以内收录检索，检索费300元。`) sits in the `收费说明` text after the
   table, not a 收费标准 row (verified at capture offset 640ff). Quote verbatim, label loose.
5. **Nit — r40's `adopted:` line.** "rows numbered 124, 135, 180 and 187 all name this one
   document" is accurate, but `renumber.tsv` marks 124 append / 135 held; "cited by rows"
   would be tighter. Cosmetic only.

## Residual risk / verification gaps

- `QUARANTINE_VERDICTS=0/0` is vacuous by construction (no register row names a theme URL —
  my own `grep -c` over the register hosts also prints 0); the counter leg adds nothing.
- I did not mutation-test `inference-ground.py`'s CJK floor (peer `R50Mut*` lane) — my
  INFERENCE_GROUNDED evidence is the frozen counter + three direct runs.
- The §6.1-negative claims are copy-local; all entries scope them to "this copy states" —
  verified the scoping language is present in each bullet that relies on absence.

VERDICT: attacked province membership, bullet-level method-vs-product drift and the QUALITY
bar for all three landed entries — all three IN PROVINCE (ISTIC in-province as method with
three generic price/turnaround bullets to cut; no role-content drift in r40); QUALITY bar
survived per-entry except one HIGH landing defect — QUALITY 74's committed `stale-count-check.py`
now exits 1 (missing LOG.md correction + missing `stale-count-after.txt` receipt, plus one
unavoidable new-pattern hit at README:1080) — and a MEDIUM scope nit (r41's §3.7 use of S105)
plus a MINOR verified-at nit.

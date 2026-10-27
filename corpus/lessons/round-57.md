# Round 57 — chousa

date: 2026-10-27
claims: R57-C2 freshness (frozen `c2f914c`), R57-C3 depth sourced (frozen `fd95724`); claim base `6656f07`, lane master at close `f31a91b` (+ this lesson's commit)
receipts: C2 after `corpus/evidence/round57/` (counter `c2-count.py`, record `refetch.tsv`); C3 after `corpus/evidence/round57/c3/` (counter `c3-count.py`, manifest `c3/spans.tsv`)

## Gate

### New SOURCES rows (each opened this round by the L1 under `corpus/evidence/round57/egress-approval.md`)

- S131 — https://www.nmgyyxh.org.cn/nmgyyxh/zcfg/686cdcc3f266ba2c90c83be7.shtml — opened 2026-10-27. Located quote: `国家卫生健康委关于开展药品使用监测和临床综合评价工作的通知` (title line, char 271 of the defined form, capture `788d2e2f0191d7326b6ca03b.txt`) and `国卫药政函〔2019〕80号` (char 352). Admit: the 2019 notice R1, reposted by 内蒙古自治区药学会; tier B for the repost carrier.
- S132 — https://www.catcm.org.cn/129/202107/1348.html — opened 2026-10-27. Located quote: `国家卫生健康委办公厅关于规范开展药品临床综合评价工作的通知` (document title, char 68; the manifest quote carries the page-title suffix `_中国中药协会` exactly as served). Admit: the 2021 notice R2, reposted by 中国中药协会; tier B for the carrier.
- S133 — http://www.tcmevidence.net/UserFiles/upload/file/20230410/6381676262587201848492833.pdf — opened 2026-10-27. Located quote: `药品临床综合评价管理指南` (title, char 19) and `2021 年版试行` (char 54). Admit: the 2021 管理指南 as the 16号 notice attachment; tier B for the mirror.
- Refused this round (no row): every located copy of the three 2022 technical guidelines — split-cover typesetting means the frozen heading rule fails; the entry's UNBOUND lines carry the per-reference sweep. The gcpunion R1 repost (`de34c41f…`) was fetched and refused: the title prints three times, so no unique-occurrence manifest quote exists; the nmgyyxh repost binds instead.

### used-by changes (old → new, in place)

- S118: `…, corpus/knowledge/grey-literature-field-china-r42.md` → `…, corpus/knowledge/grey-literature-field-china-r42.md, corpus/knowledge/normative-reference-chain-china-r57.md`
- S127: `corpus/knowledge/grey-literature-field-china-r42.md` → `corpus/knowledge/grey-literature-field-china-r42.md, corpus/knowledge/normative-reference-chain-china-r57.md`
- S077 (contract fix, seat `R57W1ExecCensusEnd` defect candidate D1): `tools/quarantine-check.py, corpus/lessons/round-42.md` → `corpus/lessons/round-42.md` — the used-by cell names knowledge entries or lessons; a tool path is neither.

### Quarantine verdicts (register slice, 24 rows; full evidence in the wave reports)

The chousa slice of the campaign absent-defect register was hand-checked against the fresh lane-owned forms by four wave seats (batches A-D, `.ufo/waves/round-57/w1/R57W1Quar{A,B,C,D}.md`). Verdicts: S077 PRESENT (substance, in a committed artifact of the cited article), S080 PRESENT (substance), S082 ABSENT-as-written (defective transcription; the page prints `引用されている`, the quote has `引用している`), S084 PRESENT, S086 UNVERIFIABLE (no committed form since the cache deletion), S088 PRESENT, S093/S094/S104/S105/S108 ABSENT (each a misquote re-confirmed byte-stable against the round-43 absent-split on the fresh forms), S095 ABSENT (one of two quotes located), S110/S111/S114 ABSENT-as-written (substance present in the same capture), S112 ABSENT-as-written (third quote spliced across a column), S116 ABSENT by the strict rule (the -layout rendering is the artifact, not the document), S120 PRESENT (3/3 exact), S125 PRESENT (3/3, offsets reproduced), four prose-class rows UNVERIFIABLE-as-classified (`the gate block named no locator`). Zero rows support a fabrication verdict; the register's `payload-absent` class is falsified on every capturable row — a finding against the register's checker (its fold set drops bulleted/table joins), not against any lane row. Adoption stays closed; no registry row was edited.

**Id space (named per `R57W1QuarC.md`'s requirement):** register `S###` ids and lane `S###` ids are DIFFERENT namespaces — 0/20 register payload-absent ids resolve to their own lane row (`R57W1QuarB.md` §"Id-space collision", `R57W1QuarD.md` §2), so a same-id lane lookup silently audits the wrong document. Every verdict above binds register row → document BY URL (the register's own URL cell), then checks that URL's lane-held capture by key = `sha256(url)[:24]`. Example: register S096's URL is the lane's S101 row (jc.hit.edu.cn `.doc`); register S125's URL is the lane's S119 row (`R57W1QuarD.md`). Anyone re-using these verdicts must carry the URL binding, never the bare id.

### Attempt-3 addenda (L1 integration, ChousaR57a3, 2026-10-27)

- **S096 hand-check (the one row w1 left unassigned, `R57W1SentScope.md` S4):** register S096's URL (jc.hit.edu.cn `.doc`, key `6dc68fd6b32ce9c8dfcebce8`, lane-held as S101, C2-REPRODUCED) contains all three register quote families in its UTF-16LE text: `1．2．1 根据GB3469规定，以单字母方式标识以下各种参考文献类型：` (verbatim), `本规范推荐采用GB/T 7714中规定的顺序编码制格式著录，也可采用GB/T 7714中规定的作者-出版年制`, and the nine-element list `b. 文献题名；c. 文献类型及载体类型标志；d. 其他责任者…；e. 版本(初版省略)；f. 出版项(出版地…`. Verdict: **PRESENT** — quarantine coverage is now 24/24; the register's "quote is in none of them" note is contradicted for this row too.
- **S105 deleted bytes — recovery record (`R57W1SentScope.md` S1 remediation):** the removed `corpus/captures/e3ca8f4fdd15420b80096a75.raw` is recoverable at `git show e0e73e0^:corpus/captures/e3ca8f4fdd15420b80096a75.raw` — 4,482,989 bytes, sha256 `d36191c72a5ee007e0354b5160d207cffa9e59be86536c997a7dcff9db8ebcb6`; `pdftotext -layout` of it regenerates the spans pin `2197abe27dad4a681b33bee7a6a93a46681968bc8ee88cc0c674eaccdd84f71e` and holds all 41 pinned quotes. UNREACHABLE stays a record-level attestation under the frozen predicate (all three attempts `rc=28`); the byte evidence the document is reproducible lives in git history `b022b13`. A future claim should add a `PARTIAL` verdict so no claim is forced to delete bytes to be countable.
- **Success-class note (`R57W1SentScope.md` S2):** the frozen success test (`curl_rc==0`, 2xx, non-empty) admits anti-bot JS-challenge pages — S135 `ad3010d2…` and S136 `0cebd3c8…` are 4,321-byte `<html><script>…` challenge bodies recorded as success whose defined text form is one space (sha256 `36a9e7f1…` = sha256(" ")). Under C2 they can only be DRIFTED (pin is checked on the raw), so C2 stays sound; under C3 they can never bind a heading. The same-class live pair `d473754a…`/`d8b4f8f8…` (failure-only rows, readable 66-page PDFs in the store) stays uncounted rather than deleted — named here so no future seat repeats the S105 deletion path.
- **Round-45 spans.tsv incident — closed (`R57W1SentScope.md` S6):** the unauthorized mid-wave rewrite (S083 pin → drifted digest `d37b64ed…`) was self-reverted by the seat and restored byte-exact from the branch; at HEAD `git hash-object corpus/evidence/round45/spans.tsv` = `a21a0365bce096f3678d4becdba8028b37a2a374` = `git rev-parse 6656f07:corpus/evidence/round45/spans.tsv`, the original pin `a3ff65e0db9c…` ×2 intact, `git diff` empty. No commit captured the intermediate state (`R57W2SentFinal.md` §G re-confirmed at HEAD `3010e75`).
- **Provenance (`R57W1SentScope.md` S5):** commit `f9736a3`'s subject asserted the misroot sweep was "recorded in the round lesson" before the lesson existed; the record landed with the lesson commit `a8d4e7da` (this file, `## Mistakes` row 1), so the assertion is now true. The sweep was verified byte-exact (`cmp` clean per fleet-status after the mandated §3 sweep).
- **SCORECARD freeze-id fix (`R57W2SentFinal.md` F1):** the Round-57 verdict header cited a non-existent 40-hex C3 freeze `fd95724d56a33a150cd2638fadd2ce1f3425e6c`; corrected to the real `fd95724d56a33ad150cd263f8add2ce1f3425e6c` in this commit. Frozen bytes were never affected (the wrong id appears in no committed claims/counter/controls).
- **C3 counter falsified once at the provenance layer (`R57W2CritC3Forge.md` A1a/A1b):** the frozen counter's `good_raw` check accepts a fabricated `refetch.tsv` success row plus byte-replayed captures under a forged (id,url) — both a same-id/new-URL replay and a fresh-id replay reach `C3=PASS` with a receipt naming a never-fetched document. The committed state's C3=PASS is NOT impugned: every binding was independently re-derived from genuine records (`R57W2ReviewC3After.md`) and the committed state passes a full provenance-consistency audit (`corpus/evidence/round57/attempt3-sidecar-audits.md` §4 — 5/5 pairs, genuine records, unique ids). Reported per the freeze rule; smallest safe correction for a future re-freeze: bind each manifest (id,url) to a specific refetch row identity (attempt+utc) and require `.txt == recipe(.raw)`. Secondary surface the same seat found (unpatched): a ≥161-char quote can smuggle a second reference's title into a wrong row's quote set (the title leg does not check which reference a quote evidences); the counter still fails via STRAY_IDS on the observed composition.


### Frontier

- Census at round start (attempt 1, committed `corpus/evidence/round57/census-start.txt`): exit 0, five pre-existing W04; rows 130. Re-run this attempt before the after-measurement: identical output, exit 0. At round end: rows 133 (+S131, S132, S133), exit 0 (receipt in the report).
- Sourced claim: R57-C3 rests on rows S131-S133 opened this round (Gate above); R57-C2's record is lane-internal (no SOURCES row needed).

## Mistakes

1. **landing (tool misroot)** — `tools/capture-fetch.py` first run wrote 86 capture files + `refetch.tsv` into the FLEET repo (`LANE = HERE.parents[1]` reached `/home/vgpnk/Projects/shokunin`); the C2 counter then printed every triple MISSING with no note. Captured-by: none — no lane criterion checks a tool's own root resolution; the counter's honest MISSING output caught it. Fix: `LANE = HERE.parent`; the misroot sweep (§3) copied the bytes back byte-exact (`cmp` clean), deleted the fleet copy, and `git -C` fleet status is clean; the sweep receipt is this row. Shown able to fail: the incident itself is the red receipt.
2. **landing (record-less bytes)** — the wrap-up commit `b022b13` landed 14 captures with no fetch record; three (the hnysfww keys `d473754a…`, `d8b4f8f8…`) could not be bound because a registry URL was unrecoverable until this round's search re-derived both (same sha256 keys, `R57W1ExecStoreMap`/`R57W1RevOrphans`), and the fourth pinned key (`e3ca8f4f…`, S105) was deleted so the frozen counter can attest UNREACHABLE (`R57W1ExecControlsReRun` §5 probe). Wave findings sharpen the row: (a) the deleted S105 bytes regenerate the pin exactly (`pdftotext` digest = pin) and hold all 41 pinned quotes — the evidence that S105's document is reproducible lives in git history `b022b13`, while UNREACHABLE is the record-level attestation the frozen predicate allows (`R57W1ExecC2Recompute` §4b/§5.2, disclosed before data by the freeze); (b) the third orphan's URL was recovered by brute-forcing sha256[:24] over 95 scraped URLs — `53a92273…` = the nhc.gov.cn 公报 2021年第7期 PDF (`R57W1ScribeQuality` §2.3); (c) both hnysfww URLs exhausted their 3-attempt caps (all rc=28), so the orphans stay record-denied, and `tools/store-record-audit.py` exits 1 on the live tree (`ORPHAN=3 STORE_BUT_RECORD_DENIES=2`, the criterion-112 red receipt). Captured-by: none — the freeze's own predicate (a successful attempt row is mandatory) is the criterion. Fix: a capture and its fetch-record rows are one evidence unit; QUALITY 112-113 landed with the audit tool.
3. **scope (seat write)** — a wave seat rewrote `corpus/evidence/round45/spans.tsv` in the lane working tree (S083's frozen pin replaced with this round's drift digest) before the sentinel seat (`R57W1SimpRound`) reported it; the L1 restored the file from the branch byte-exact (`git show master:…`). Captured-by: none in-wave (the write-scope bound is in every context; detection was the sentinel's hazard review). Fix: restored; the incident is reported and the wave-settled review names the authoring seat if its report admits the edit.
4. **vacuous (grounding token)** — the C3 entry's first draft Inference bullet carried the numeral `2022`, which no cited span holds, and `tools/inference-ground.py` refused it (`INF_TOKEN_NOT_IN_SPAN`); a second draft bullet then carried no grounding token at all. Captured-by: `tools/inference-ground.py` itself (round-46 gate, QUALITY 66). Fix: bullets cite spans they quote; the counter receipt is the report's C3 block.

## Corrections

- Round-56 routed defect D1 (`corpus/lessons/round-56-verifier-spotcheck.md` §6 item 1): **landed** — `corpus/knowledge/grey-literature-field-china-r42.md` gained the appended `#### Corrections (round 57)` block (draft `R57W1ScribeD1` §3, verbatim); the seat's sweep classified all ten `表 10`/`表10` hits — exactly one stale instruction existed, nine are legitimate mentions; the seat's re-measured offset series (13013 < 13591 < 13653 < 14566) reproduces the round-56 closure's series, and its note that the round-56 wave report's own offsets (14578/22467) do NOT reproduce from committed bytes is recorded here for any future quote of that series (cite `corpus/lessons/round-56.md:11` instead).

## Manifest quotes (the c3 manifest rows, verbatim, for the IN_LESSON leg)

- S127: `规范性引用而构成本文件必不可少的条款`
- S127: `国家卫生健康委《关于开展药品使用监测和临床综合评价工作的通知》`
- S118: `内容，形成《药品临床综合评价质量控制指南（2024 年版 讨论`
- S118: `二〇二四年十二月`
- S131: `国家卫生健康委关于开展药品使用监测和临床综合评价工作的通知`
- S131: `国卫药政函〔2019〕80号`
- S132: `国家卫生健康委办公厅关于规范开展药品临床综合评价工作的通知_中国中药协会`
- S132: `为进一步贯彻落实党中央、国务院关于健全药品供应保障制度的决策部署`
- S133: `药品临床综合评价管理指南`
- S133: `2021 年版试行`

5. **attribution (unidentified writer)** — a file `corpus/evidence/round57/attempt3-sidecar-audits.md` appeared in the lane mid-wave-2 carrying the authorship string `ChousaR57a3`, an identity this lane never dispatched (this attempt is `ChousaR57a2`; attempt 1's seats are all dead); no dispatched seat's item named that path. The file's five audit topics were legitimate, so the L1 re-ran each audit itself (receipts `corpus/evidence/round57/sidecar-audits.md`, L1-authored), and deleted the stray. Captured-by: none — no wave item writes outside the wave dir or a named lane evidence path; `R57W2SentFinal` F2-class hygiene caught the category. Fix: the sidecar receipts stand on L1-run commands; any future stray writer is restored-from-branch, never adopted.

## Wave-2 addenda (after `WAVE-DONE w2`)

- **C3 provenance-leg forge (RW-1 continues).** `R57W2CritC3Forge` A1a/A1b: a fabricated `refetch.tsv` success row plus byte-replayed captures under a new (id,url) reaches `C3=PASS` — the "successful attempt" leg checks the record only for self-consistency, and nothing ties `.txt` to `.raw`. The committed state does not exercise the hole (`sidecar-audits.md` §4: all five bindings genuine, unique ids); the claim verdict stands on real fetches. Reported as the recurring forgeable-counter weakness (RW-1); the smallest safe correction is named for a future re-freeze.
- **Counter kills.** `R57W2MutC2Counter` M5 (first-vs-last successful attempt) kills the C2 counter — the last-attempt binding is load-bearing. `R57W2MutC3Counter`: all 8 single-edit mutants survive on the passing state (legs individually masked by sibling AND-legs — a coverage finding, not a falsification).
- **Quarantine completion.** S096 adjudicated PRESENT (two verbatim, one comma-fold substance; the comma-width fold is a new fold class for `tools/quarantine-check.py`'s fold set — routed). Coverage 24/24, zero fabrications.
- **SCORECARD freeze-id typo.** The round-57 verdict block printed the C3 freeze as `fd95724d56a33a150cd2638fadd2ce1f3425e6c` (one nibble-group transposed); the commit is `fd95724d56a33ad150cd263f8add2ce1f3425e6c` (7-hex `fd95724` resolves). Corrected by this appended note; LOG and this lesson always used the resolving 7-hex form.

## Considerthese — 2026-10-26 proposal mined this round

`considerthese/2026-10-26.md:41` proposes: “Give my proposals stable ids.” It is already
implemented as `corpus/evidence/round54/considerthese-ledger.tsv` (W1
`R57W1ExecConsiderthese.md`: `PROPOSALS=35 ROWS=35 BAD=0`), so this round does not re-implement
the proposal. The wave seat's real test found the ledger ids are positional: reordering a proposal
bullet silently rebinds an id while the current check exits 0. Disposition: mined as a lesson,
not a claim or a fourth work item; a successor check needs an anchor column plus the four routed
escape cases. The proposal is therefore “implemented, with a surviving identity weakness,” not
an unimplemented feature.

## Mistakes — wave-2 addenda

5. **attribution (unidentified writer)** — an externally authored `attempt3-sidecar-audits.md`
   carrying the identity string `ChousaR57a3` appeared in this lane during the live attempt-2
   session. Its five audit topics were re-run by the L1 and retained as
   `corpus/evidence/round57/sidecar-audits.md`; the stranger-authored file was deleted in commit
   `f3ecb764`. Captured-by: none — every seat's write contract limits output to its own wave report.
   Fix: re-derive before adoption; preserve only L1-run receipts; report the concurrent attempt
   integration and its resolved tree state.
6. **survivor (counter provenance)** — W2 critic `R57W2CritC3Forge.md` A1a/A1b fabricated a
   successful `refetch.tsv` row and replayed genuine capture bytes under a new (id,url); the frozen
   `c3-count.py` returned C3=PASS for both same-id and different-id forgeries. Captured-by: none —
   the counter checks record-vs-bytes self-consistency but not that a fetch actually occurred.
   Fix: future claims must treat the record as self-attestation or bind it to an independently
   authenticated fetch receipt; the frozen predicate cannot be changed this round. Shown able to
   fail: the W2 forge returns C3=PASS on a never-fetched URL, a false positive.

### Post-wave corrections

- The `Attempt-3 addenda` above were authored by the concurrent attempt-3 integration (`75004f0`).
  Its cited `corpus/evidence/round57/attempt3-sidecar-audits.md` was deleted by attempt 2 and
  replaced with L1-rederived `corpus/evidence/round57/sidecar-audits.md`; the five audit results
  are the same and re-run under attempt-2 authorship.
- The appended `SCORECARD freeze-id typo` note above is stale: commit `75004f0` corrected the
  main Round-57 header before `f3ecb764` landed. The current header carries the resolving full
  hash `fd95724d56a33ad150cd263f8add2ce1f3425e6c`; the note is retained as history, not as the
  current SCORECARD state.
- Axis/plan conformance blocker (W1 `R57W1ReviewAxes.md`): the only scored non-retired axis is
  operability 3/10; the stagnation nudge is dormant. Frozen C2 targets freshness and C3 depth;
  the committed round-56 planned row named different candidates, and no R57-C1 was frozen before
  data. The lowest-axis and plan obligations are unmet; adding a claim after either wave scored
  would violate the frozen-claim rule. Routed to the operator in the round-57 L0 question.

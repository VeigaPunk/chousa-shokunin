# ScribeGateBlock — round 47 w1 — `## Gate` draft for `corpus/lessons/round-47.md`

Item: draft the Gate section (theme; per-entry province + QUALITY check for the two adopted entries; id map by document with the 8-id collision list; round-46 flip condition for the amendment and which parts are met; ≥1 reject from the assimilation set with reason + flip; row-quote list and quarantine verdict lines left as marked slots). Scribe seat: no lane production file written; no fetch; no installs; scratch `/tmp/chousa-r47-ScribeGateBlock/` created and deleted.

Verdict: DRAFT READY (below). Rejects picked: BOTH `citation-count-semantics-r37.md` and `search-log-fields-r36.md`; neither is generic or sibling-domain, both fail on grounding (unreadable or wrong-page captures), and both are off this round's one theme.

## Commands run (decisive lines)

- `comm -12 <(sort -u reg-ids) <(sort -u staged-ids)` in `.ufo/waves/round-47/assimilation/` → `S082 S083 S084 S085 S086 S087 S088 S089`; reg-ids 89 unique, staged-ids 114 unique; `sha256sum collisions` → `76b8703b409bd759…`. `guard-proof/`: `collisions` = `S097`, `collisions-col0` empty (fixture `  | S097 |` indented two spaces → the column-0 extractor misses it, the guarded one catches it).
- `rg -o '^\| S(08[2-9]|09[0-4]) \| …' merge/chousa/SOURCES.append.md` → staged S082 PRISMA-S, S083 Cochrane ch.4, S084 RFC 7089, S085/S086 GB/T 7714-2025, S087 CiNii manual, S088/S089 J-STAGE, **S090 J-STAGE jjsme, S091 NSSD, S092 Lateral Reading, S093 GB/T 7714 copy, S094 WARP FAQ**.
- Capture probes (python, `.qcache/<sha256(url)[:24]>.txt`, counts of literal strings): S085 `5a631adb…` 4146 B `NOT ENOUGH INFO`×3 `null, null`×2 `build 385`×1 `2026-04-02`×1; S090 `4132ec1b…` `greater reason to believe`×2 `all else equal`×2 `do not select any sentences`×1 `22%`×2 `30%`×2; S091 `3749141b…` `30,012`×4; S092 `b502d4c6…` `0.6841`×3 (chars 2821, 6516, 18060) `stronger reason to believe`×3 `world-knowledge`×1; S093 `44be8711…` `7,675`×2 `1,535`×9 `Disputed`×4; S094 `a9cf4170…` `0.792`×1 `re-assign`×1 `202`×88 (noisy token).
- S092 context at char 18060: `3.4.1 5-way Agreement … 4% ( n = 7506 …) … annotated by 5 annotators … Fleiss κ … 0.6841`; `five-way`×0, `5-way`×3.
- `rg -n '^\| S085 ' corpus/SOURCES.md | rg -o 'char [0-9]+'` → `char 2349` (held anchor; claims.md:125 says no quote offset).
- Reject-candidate captures: PRISMA-S DOI `01f657b3…` 267 B, head `Client Challenge`, `copied and pasted`×0; Cochrane ch.4 `14aaa168…` 211326 B `copied and pasted`×1 `by whom`×1 `12 months`×4 `C36`×1 `C37`×1; J-STAGE jjsme `02b3b0e8…` 6333 B `参照日`×0 `必須`×0 `インターネット`×0; zcmu .doc `b539a802…` 1406840 B, `file` → `data`, 308430 U+FFFD, `自引/他引频次/任一合作者/中国引文数据库/合作发文` 0 under utf-8, utf-16le/be (both alignments), gbk, gb18030, big5; `soffice --headless --convert-to txt` copy → 0 hits; jc.hit .doc `6dc68fd6…` 157816 B, 14486 U+FFFD, `文献标志码/参考文献/为便于文献的统计` 0 (only `GB/T 7714`×2 utf-16); toho PDF `7809d511…` `被引`×6 `被引用回数`×1 `引文网络`×2 `专业检索`×3; um.edu.mo PDF `02aefcf5…` `溯源`×11 `引用量`×1 `下载量`×2 `来源数据库`×1 `根据相关文献`×1.
- `rg 'zcmu|jc.hit|toho|um.edu.mo|s13643-020-01542|chapter-04|jjsme' absent-defect-register.md` → line 37 `chousa round1 S077 payload-absent` (PRISMA-S DOI); line 45 `round2 S095` (zcmu); line 46 `round2 S096` (jc.hit).
- `rg -i 'CNKI|bibliometr|citation count|Chinese' */PROVINCE.md` (fleet) → only `mado-shokunin/PROVINCE.md:70,73` (desktop-plane documentation localization); no sibling owns CNKI citation semantics or search logs.
- `PYTHONDONTWRITEBYTECODE=1 python3 corpus/evidence/round47/c3-count.py` → `ENTRIES=0/2 CITES_BOUND=0/6 QUOTE_ROWS=0 (min 12) … ANCHOR_BOUND=0/6 INFERENCE_GROUNDED=0/2 QUARANTINE_VERDICTS=0/4 C3=FAIL` exit=1; `--lane-only` same legs, `C3=FAIL` (the printed exit=0 there was `tail`'s).
- `c3-count.py:65` `VERDICT_RE = register\s+`?(S\d{3,})`?.*?verdict[:=]?\s*`?(present|absent|unverifiable)`?`; `:62` map `S093→S090, S094→S091, S108→S092, S110→S094`.

## Findings

1. **Operability (slot safety):** the slot lines below are written so `VERDICT_RE` cannot match them (`verdict: ⟨SLOT …⟩`); pasted unfilled, the counter stays `QUARANTINE_VERDICTS=0/4`, so an unfilled slot cannot pass. A filler MUST NOT write any other line containing `register S0xx` followed by `verdict` and one of the three words (e.g. prose quoting the checker's `absent`) — it would be counted. Peer reports `QuarReg094.md:58` and `QuarReg108.md:62` already carry lines in the matching form; `QuarReg093.md` / `QuarReg110.md` carry verdicts in a different shape and need re-formatting.
2. **Calibration (second-order collision):** the collision file counts ids held at round START (8). After S090–S094 are appended, staged S090–S094 also name different documents, so 13 ids collide. The draft says so; anyone appending from the staged block by id would misbind five rows.
3. **Register ids are not lane ids:** register S093 = PEOPLEPROFILES = lane S090; lane S093 = climate-fever, which is not in the register. The draft puts this in the Gate block.
4. **Depth corrections the entry drafters need** (each is a staged sentence the captures or the held corpus contradict, so it gets a mistake line under claims.md:133): (a) the base entry's Unknown ("FEVER paper … only as an abstract") is stale, since the lane holds S086 (round 46) and S092; (b) the amendment's Unknown ("lane holds no figure for the reliability of the evidence step") is contradicted by held S086 `recall of 72.36%` (char 42011, round-46 Gate); (c) "0.6841 five-way Fleiss" means 5 annotators on 4% (n = 7506) (S092 char 18060), not five labels; (d) under QUALITY 66, every base Inference bullet and amendment Inference bullet 4 name no `S###`; the base quote "record-declared and unverifiable…" is lane-internal (`corpus/README.md:362`) and needs that path cited or dropped.
5. Out of scope / not done: row quotes, anchors and quarantine verdicts (left to the source-opening seats); no entry text written.

## Draft

```markdown
## Gate

Theme (assimilation §10, one theme): what a support test is, how it is applied, and how reliable it is. One theme, two entries, five new rows (S090–S094) and one held row re-bound (S085). No fetch: the fetch-scope L0 `8d77e6c1` is open; every capture is on disk.

Ids bound **by document** (URL equality), never by arithmetic. The offsets are −12/−8/−8/−21/−21/−21, so no arithmetic reproduces them:

| staged | lane | URL |
|---|---|---|
| S097 | S085 (held since round 46; no new row; `used-by` gains the base entry) | https://fever.ai/dataset/fever.html |
| S098 | S090 | https://aclanthology.org/2026.findings-acl.19.pdf |
| S099 | S091 | https://ojs.aaai.org/index.php/AAAI/article/download/29825/31432 |
| S113 | S092 | https://arxiv.org/html/1803.05355 |
| S114 | S093 | https://arxiv.org/html/2012.00614v2 |
| S115 | S094 | https://aclanthology.org/2025.coling-main.108.pdf |

The registry held 89 rows (`S001`–`S089`, contiguous; `.ufo/waves/round-47/assimilation/reg-ids`), so the next five are S090–S094.

Id collision: **8 ids** (`S082`–`S089`; `assimilation/collisions`, sha256 `76b8703b…`, the intersection of 89 lane ids and 114 staged ids). Every one names a DIFFERENT document on each side. Lane: AVeriTeC README / paper / train.json, FEVER page / NAACL PDF / Zenodo record, AVeriTeC page, AVerImaTeC. Staged: PRISMA-S, Cochrane ch. 4, RFC 7089, GB/T 7714-2025 ×2, CiNii manual, J-STAGE ×2. After this round's append, staged S090–S094 (J-STAGE jjsme, NSSD, Lateral Reading, a GB/T 7714 copy, WARP FAQ) also collide: 13 ids. Nothing was appended from the staged block as-is; the six rows are written from the captures. The extractor's indent guard is load-bearing: `assimilation/guard-proof` holds an indented `S097` row that the guarded extraction catches and the column-0 one misses.

Register ids are not lane ids: register S093 = lane S090, register S094 = lane S091, register S108 = lane S092, register S110 = lane S094. Lane S093 (climate-fever) and lane S085 are not in the register slice.

Quarantine (§10), four register rows on this theme's URLs, hand-checked this round:

- register S093 (lane S090) — verdict: ⟨SLOT: present | absent | unverifiable — capture, char range, why the checker missed⟩
- register S094 (lane S091) — verdict: ⟨SLOT⟩
- register S108 (lane S092) — verdict: ⟨SLOT⟩
- register S110 (lane S094) — verdict: ⟨SLOT⟩

A row hand-checked `absent` is refused, never adopted (claims.md kill rule).

Admit:

- `corpus/knowledge/claim-support-test-r37.md`, citing S085, S090, S091. Province: claim-vs-source verification (`PROVINCE.md` Owns). It makes no claim about model quality (kengaku's province); the 22/30 per cent figures are about Wikipedia citations. QUALITY bar:
  - 3 (Observation, Inference and Unknown kept separate): ⟨SLOT⟩.
  - 7 (each claim scoped to a tier-A row: S085, S090 and S091 are all tier A): ⟨SLOT⟩.
  - 66 (inference grounded): the staged Inference bullets name no `S###`; each now cites one, and every quoted phrase and figure sits in a cited span. The lane-internal quote "record-declared and unverifiable" cites `corpus/README.md:362`.
  - Corrected from staged: the Unknown "FEVER paper … only as an abstract" is replaced, since the lane holds S086 and S092. The staged ids S097–S099 are re-bound (`REF_ID_UNBOUND=0`). The recheck prose is stripped.
  - Check: `tools/inference-ground.py` exit ⟨SLOT⟩.
- `corpus/knowledge/claim-support-test-r37-amendment-2026-10-23.md`, citing S092, S093, S094. Province: same; "No claim is made here about any model's agreement" keeps it out of kengaku. QUALITY bar:
  - 66: Inference bullet 4 ("practical shape…") names no `S###` and now cites one; (S113)/(S114)/(S115) are re-bound to S092/S093/S094.
  - Corrected from staged: "0.6841 five-way Fleiss" becomes Fleiss κ 0.6841 over 5 annotators on 4% of claims (n = 7506), S092 §3.4.1. The Unknown "the lane holds no figure for the reliability of the evidence step" is corrected: held S086 carries `recall of 72.36%` (round 46), measured against the super-annotators' set. The figure `202` is anchored to the relabelling sentence, not a bare-token hit.
  - Check: `tools/inference-ground.py` exit ⟨SLOT⟩.
- Round-46 flip condition for the amendment (`lessons/round-46.md` `## Gate`, Reject): "the base entry is adopted with its own rows and the amendment's quotes are located in committed spans", given against staged rows "in the campaign's numbering".
  - Met by construction: the numbering part. Ids bind by document and no staged id survives in either entry.
  - Met at admission only if the counter shows it: the base entry adopted (`ENTRIES=2/2`); its own rows (`CITES_BOUND=6/6`); the amendment's quotes in committed spans (`SPAN_IDS=6/6`, `QUOTES_IN_SPAN=n/n`, `CAPTURE_BOUND=n/n`).
  - At draft time `c3-count.py` printed `ENTRIES=0/2 CITES_BOUND=0/6 QUOTE_ROWS=0`, `C3=FAIL`. At admission: ⟨SLOT: c3-count output, both modes⟩.

Reject:

- `citation-count-semantics-r37.md` (staged) — **not this round**. Reason: it is off this round's one theme. Its headline Observation (CNKI's co-author self-citation rule) rests on staged S100, and the S100 capture `b539a802…` is an OLE `.doc` decoded lossily: 1,406,840 B, 308,430 U+FFFD, and zero hits for 自引 / 任一合作者 under utf-8, utf-16, gbk, gb18030 or big5. The S101 capture `6dc68fd6…` has zero hits for 文献标志码 or 参考文献. Both URLs are unchecked register rows (S095 line 45, S096 line 46, `payload-absent`). The entry is in province (citation chaining; no sibling `PROVINCE.md` names it), not generic. Flip: a byte-faithful capture of S100 and S101 whose text holds the quoted sentences, with register S095/S096 hand-checked `present`, in a round whose theme is citation-count semantics, ids bound by document. The S102/S103 PDF captures alone (被引 ×6, 溯源 ×11) would ground only a narrower entry.
- `search-log-fields-r36.md` (staged) — **refused again**. The round-43 refusal stands (`lessons/round-43.md:43`) and its flip is unmet: the fetch-scope ruling is still open. The PRISMA-S DOI capture `01f657b3…` is still a 267-byte `Client Challenge` (register S077 line 37). The J-STAGE capture `02b3b0e8…` (6,333 B) has zero hits for 参照日. Only the Cochrane ch. 4 capture holds its quotes. It is in province (`PROVINCE.md` search-strategy taxonomy), not generic, and not a duplicate: `search-log-method-r39.md` (S078) holds the log-as-document half, not the field list. All three staged ids (S082, S083, S090) name other lane documents. Flip: the round-43 flip, plus ids bound by document past S094.

Rows added (opened ⟨SLOT: date⟩, all `mined`, recheck ⟨SLOT⟩) — URL, access date, ≤25-word located quote(s) with `char N`:

- **S085** https://fever.ai/dataset/fever.html — re-bound. The anchor `char 2349` is no quote offset (claims.md) → ⟨SLOT: quote(s), char N⟩
- **S090** https://aclanthology.org/2026.findings-acl.19.pdf — ⟨SLOT⟩
- **S091** https://ojs.aaai.org/index.php/AAAI/article/download/29825/31432 — ⟨SLOT⟩
- **S092** https://arxiv.org/html/1803.05355 — ⟨SLOT⟩
- **S093** https://arxiv.org/html/2012.00614v2 — ⟨SLOT⟩
- **S094** https://aclanthology.org/2025.coling-main.108.pdf — ⟨SLOT⟩

Recheck prose stripped from the staged rows (S097–S099, S113–S115): ⟨SLOT: staged prose → lane cadence, old→new⟩.
```

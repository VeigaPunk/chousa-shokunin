# R57W1ReviewEgress — egress compliance audit (round-57 approval table vs refetch.tsv and seat behavior)

Seat: reviewer (leaf). Base `6656f077`; C2 frozen `c2f914c`, C3 `fd95724`, tip at dispatch `f9736a3`. Read-only audit: I fetched nothing; every byte below came from committed lane files or the lane's own git objects. Scratch `/fast/scratch/hyaku/chousa-r57/R57W1ReviewEgress` deleted on yield (`trap rm -rf`); TMPDIR + PYTHONDONTWRITEBYTECODE set inside it.

Point-in-time scope: `refetch.tsv` is being appended live (mtime 05:48:20 -0300 at last check); audited snapshots taken 05:41 and 05:48. Seat reports audited: all 55 `.md` files in `.ufo/waves/round-57/w1/` present by ~05:58.

## 1. Method

- Pinned set recomputed from source, not from the claim text: `git ls-tree -r --name-only 6656f07` → 12 `corpus/evidence/**/spans.tsv` with a `capture_sha256` column; `git show <base>:<each>` → awk col 1-3, `sort -u` → **47 distinct (id,url,capture_sha256) triples**, ids S082–S130 minus S084/S095. Matches `SET=47` in `c2-count.py`.
- Refetch-side: `awk -F'\t' 'NR>1{print $1"\t"$2}' refetch.tsv | sort -u` → 71 pairs (54 ids) in the final snapshot.
- Set algebra (LC_ALL=C): `comm -12` pinned∪refetch = **47/47 covered**; `comm -23` refetch∖pinned = **24 non-pinned pairs**, all under new ids S131–S137.

## 2. Result — the table holds, with one disclosed defect class

**Every fetched URL is in-table.** The 24 non-pinned pairs are exactly the C3 candidate fetches the approval table's second row permits ("a public document a registered source cites by name — the documents S127's `2 规范性引用文件` names"), all behind new Registry ids S131–S137. Grounded by capture text, not by assertion:

| id | target ref | URLs (hosts) | bytes prove it |
|---|---|---|---|
| S131 | R1 〔2019〕80号 | nhc.gov.cn 201904, web.archive.org /2023/,/2024/, cmea-cmec.com | all attempts failed (412/404); scouts R1+R1Gov named the page |
| S132 | R2 〔2021〕16号 | nhc.gov.cn 202107, web.archive.org /2023/,/2024/, catcm.org.cn | catcm `.txt` opens `国家卫生健康委办公厅关于规范开展药品临床综合评价工作的通知` (capture a476f4128186c7976671ab54) |
| S133 | R3 管理指南 2021 | nhc.gov.cn cms-search, tcmevidence.net, forten-sp oss | tcmevidence `.txt` opens `药品临床综合评价管理指南（2021 年版试行）` (key 6f545e6c16b6b568ea3f591b) |
| S134 | R4 抗肿瘤 2022 | hnysfww article+data pdf, nhei.cn attach | hnysfww page `<title>` = `心血管病、抗肿瘤、儿童药品临床综合评价技术指南` hub (key 9695437cac165bb4b6145deb) |
| S135 | R5 心血管病 2022 | cpia.net.cn, takarabiomed 2540A, hnysfww pdf, gsdpf DOCX, wanfangdata, nhei d4c3a96d | ScoutR5 named cpia+phirda candidates; takarabiomed bytes landed |
| S136 | R6 儿童 2022 | hnysfww pdf, nhei 60c39855fa attach, takarabiomed 6170 | ScoutR5 named the nhei notice+attachments |
| S137 | R4–R6 carrier | phirda.com/artilce_28170.html?cId=2 | `.txt` opens `国家药物和卫生技术综合评估中心关于发布心血管病、抗肿瘤、儿童药品临…` (key d2a1cf3d2c385daee67c4afd) |

R7 is bound by held S118 per the frozen check — no fetch needed or made for it.

**Cap and schema hold**: no (id,url) exceeds 3 attempts (awk uniq count, empty violation set); every row has 9 fields, header intact. web.archive.org retries are alternate locations of the same named documents (nhc 412-blocked HTML pages) — same-document retries, in scope. nhei.cn `files/<hash>.pdf` URLs are attachments of one scout-named notice page — still the clause-named documents.

**Record↔store integrity (snapshot):** for every row with a recorded `raw_sha256`/`txt_sha256`, recomputed sha256 of `corpus/captures/<key>.{raw,txt}` matched — 0 mismatches at 05:41. One transient observed mid-write (`0cebd3c84…txt` = 1 byte at 05:40, correct 36a9e7f1… by 05:41:12) — the fetch tool rewrites `.txt` after `.raw`; readers racing live writes see partial state, [INFERENCE] ScribeLesson.md:26 saw the same race.

## 3. DEFECT — record-less bytes in the lane store (L1-side, already tracked)

Three committed captures have **no successful refetch.tsv row** — the table's `record` column is unmet for bytes that did land:

- `corpus/captures/53a92273a452a58f28368691.raw` (1.2 MB PDF, NHC 公报2021·07 reprinting R2; sha 460121b4…): **zero** rows. Its URL per ScoutR3:22 — `nhc.gov.cn/bgt/201807sgf/202109/…/1733795726978_35780.pdf` — appears in refetch.tsv NOWHERE. Bytes without any recorded attempt = strictly out-of-table.
- `d473754a0cbf8d3095255d5a.raw` (1.5 MB, 抗肿瘤 2022): rows exist (S135 hnysfww, attempts 1-2, both `curl_rc=28`, sha `-`) but the committed bytes' sha `47435e4b…` was never recorded.
- `d8b4f8f8829b813f16227893.raw` (1.3 MB, 儿童 2022): same pattern — failed-only rows, bytes' sha `1f84ddf0…` unrecorded.

All three were committed in `b022b13` "hyaku run9 wrap-up: remaining round-57 captures" (mtime ~03:21, *before* the f9736a3 refetch pass whose table requires a row per attempt). Head commit `e0e73e0` removed the analogous record-less S105 bytes "named in report" but **missed these three**. Frozen-claim posture is safe: C3's predicate binds only captures that ARE "the bytes of a successful attempt in refetch.tsv", so these orphans cannot bind R2/R4/R6 — the counter rejects them as designed. Peers already on it: `R57W1ReviewCaptures.md:46-50`, `R57W1RevOrphans` item, `R57W1ScoutR2Gaz.md:8,57`. Reported, not patched (frozen surfaces; my boundary forbids lane edits).

## 4. Seat-level egress — zero violations

Sweep of all 55 landed reports (`grep -nE '(curl|wget) …https?://|requests.|urllib|httpx|aiohttp'` + fetch-claim patterns + writes-to-store patterns): **no real curl/wget/HTTP invocation in any report, no seat claims a fetch, no seat wrote `corpus/captures/` or `refetch.tsv`**. Only hits are prose (ScoutR2Gaz:28 notes the nhc WAF 412; ScribeLesson:26 notes the txt-write race). The one borderline case is clean: `R57W1MutFetchTool` ran the recipe's curl through a PATH shim serving fixture bytes — "No network egress occurred" (its report:5), and its M5 mutant independently showed the tool's `scratch = env HYAKU_SCRATCH … else /tmp` leg writes debris outside the named scratch (operational hygiene note, not egress). Registry: exactly 1 of 65 seat items names a URL — `R57W1ScribeEntry` → S127's ttbz.org.cn URL (in refetch.tsv; re-open authorized). ScribeEntry.md:3,71 declares and uses only committed lane bytes — compliant even without fetching. Scouts used `web_search` only (table row 3 permits it). Verdict: the "forbidden this round except the L1's table" wall held for every landed seat.

## 5. Residual risk / verification gaps

- The store is live: fetches landing after 05:48 could introduce URLs my snapshots miss. A post-wave re-run of §1 set algebra is the cheap close.
- Rule-(b) location-by-search: the newest S131/S132/S135/S137 candidate URLs (cmea-cmec, catcm, wanfangdata, phirda, nhei d4c3a96d) were fetched in the last minutes; scouts R1Gov/R5 named cmea-cmec and phirda, but catcm.org.cn and wanfangdata appear in no landed report yet — their "located by a search" evidence should show in the L1's own Gate log/round-57 lesson when written. Cannot confirm that leg without the lesson (absent at audit time).
- The orphan bytes' original fetch time/URL is unrecorded by construction; provenance is inferable (scout hashes match) but not provable from the table.

VERDICT: attacked round-57 egress table conformance — the L1's fetch table is internally consistent (47/47 pinned covered, all 24 non-pinned pairs are clause-named documents under S131–S137, ≤3 attempts, record↔store shas match) and **0 seat-level egress violations**; survives with one L1-side defect already disclosed by peers: three captures (53a92273…, d473754a…, d8b4f8f8…) hold bytes no successful refetch row records.

# R57W1QuarA — Quarantine hand-check, batch A (chousa r57 w1)

Seat: executor (labrat). Rows: register S077, S080, S082, S084, S086, S088 (chousa slice).
Read-only. No lane, fleet-root or shokuknow write; no fetch; no tool install.

## 0. Method

Slice re-derived with the prompt's recipe (`/home/vgpnk/Projects/shokunin/.ufo/prompts/chousa-round-57.md:601`):
24 data rows (20 `payload-absent` + 4 prose). Register = `/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/absent-defect-register.md` (read-only).
Defined text form = the committed lane capture `corpus/captures/<sha256(url)[:24]>`; PDF raw → `pdftotext -layout` (the committed `.txt` is byte-identical to it, verified); HTML raw → the committed `.txt` (verified: campaign `html_to_text` + CRLF→LF == stored `.txt`, 3/3). Fold ladder = the eleven folds of `tools/quarantine-check.py` (copied into scratch, not edited).

## 1. **Load-bearing finding: the register's S-ids are NOT the lane's S-ids**

Following the seat recipe literally ("open the row in `corpus/SOURCES.md`") lands on the **wrong document**: lane `S080` is the NDL WARP FAQ, lane `S082` the AVeriTeC README, lane `S086` the FEVER PDF. Measured on the same-id lane rows, that reading gives **3 false ABSENTs** (S082/S086/S088: quote absent from an unrelated capture) + 3 unverifiable. The correct locator is the register row's own cited-source cell. Mapping used below:

| register id | cited source (register cell) | lane id | capture key | committed form |
|---|---|---|---|---|
| S077 | https://doi.org/10.1186/s13643-020-01542-z | **none** | 01f657b3d0ab045c494b3f92 | **absent** |
| S080 | https://std.samr.gov.cn/gb/search/gbDetailed?id=4507EFE13… | S121 | adf6ba934e813b2c326fa150 | `.txt` 6650 B / 4476 chars |
| S082 | https://support.nii.ac.jp/ja/cir/manual_articles_detail | S096 | 09fc63de41f293d43d631c46 | `.txt` 12901 B / 6421 chars |
| S084 | https://www.jstage.jst.go.jp/static/pages/FAQs/TAB2/-char/ja | S098 | fea98dc5a5a486c988dd415c | `.txt` 95733 B / 39633 chars |
| S086 | https://www.ncpssd.cn/ | **none** | 76914d78c20094f677dea77d | **absent** |
| S088 | https://xuebaobangong.jmu.edu.cn/…64b9ba1b….pdf | S123 | 0f33243fd7ac2fe88b85c1ba | `pdftotext -layout` 83061 chars |

`grep -c "s13643-020-01542-z" corpus/evidence/round57/refetch.tsv` → 0; `grep -c ncpssd …refetch.tsv` → 0: neither URL was in the C2 pinned set, so round 57 re-fetched neither.

## 2. Verdicts (6/6 rows, one each)

Rule applied, stated so the reader can re-run it: **PRESENT** = every constituent of the quoted span is present in the cited source's defined form (the span's own joining/punctuation may differ — a bulleted list rendered as one line, table padding, an ` / ` row separator); **ABSENT** = a constituent is not in the form, or the form contradicts it; **UNVERIFIABLE** = no committed form exists.

| reg id | verdict | evidence summary |
|---|---|---|
| **S077** | **PRESENT (substance)** | all 4 census quotes verbatim in a git-tracked committed artifact of the cited article (byte offsets 1441 / 14602 / 17793 / 18563). Lane store holds **no** capture for the cited DOI. |
| **S080** | **PRESENT (substance)** | quoted string: 0 occurrences. All three field/value pairs present in the cited page's 基础信息 block @1327–1401. The colon-joined string is present **exactly once in the sibling capture S122** (b9ca2a4f…, @13300). |
| **S082** | **ABSENT as written** (defective transcription, not fabrication) | quoted string 0 occurrences; longest common substring 17/43. Clause 2 `随時増加していきます。` verbatim @3577 — already cited by the lane's own S096 row. Head clause substitutes 引用している for the page's 引用されている. |
| **S084** | **PRESENT (substance)** | both quotes' components present contiguously @29547–29799; items 3 and 4 of quote 2 byte-exact @29749 / @29775 — the same anchors the lane's own S098 row cites. |
| **S086** | **UNVERIFIABLE (no committed form)** | no capture of the cited URL anywhere on this host; the campaign `.qcache` that held the companion help-page capture is deleted (0 files) and no copy of that page remains. |
| **S088** | **PRESENT (substance)** | all five rows of 表A.2 present contiguously @59025–59245 in the `-layout` form (labels @59025/59073/59116/59161/59201, codes @59063/59108/59153/59198/59243). |

## 3. Per-row evidence

**S077** — `grep -Fbo` in `/home/vgpnk/Projects/shokuknow/.deepresearch/20261023_171700_prisma-inspired-search-log-format-for-lanes/aaron_10_1186_s13643-020-01542-z.txt` (sha256 `20f6887699c8e3e10cd167758dbd075b33468bdc5cfaedfa13e69e97664493d7`, 110602 B, git-tracked):
`1441:each component of a search is completely reported and therefore reproducible.` · `14602:It is intended to guide reporting, not conduct, of the search.` · `17793:Include the search strategies for each database and information source, copied and pasted exactly as run.` · `18563:For each search strategy, provide the date when the last search occurred.` (dupes at 46293 / 65371). The cited-URL capture in the deleted cache was a 265-char WAF wall, not the article. The lane's own round-48 seat adjudicated this row PRESENT on this same artifact (`.ufo/waves/round-48/w2/QuarantineS077.md`). Caveat for the L1: the locating bytes are **not** in `corpus/captures` — a lane-store-only reader would call this row unverifiable.

**S080** — committed form (S121). The 基础信息 block, contiguous @1327–1401: `标准号 \n GB/T 7714-2025 \n \n \n 发布日期 \n 2025-12-02 \n \n \n \n \n 实施日期 \n\n 2026-07-01`; also `发布 于 2025-12-02` @1029, `实施 于 2026-07-01` @1048. `标准号：` occurs **0** times in the S121 `.txt` and 0 times in its `.raw` (the page uses `<dt>`/`<dd>` cells, no colon). The colon-form `标准号：GB/T 7714-2025` occurs exactly once in the whole lane store — in the **sibling** capture S122 (`b9ca2a4fdf9455867534f144`, openstd newGbInfo; its `.txt` is the raw HTML, the `标准号：` sits inside an `<h1>`), @13300, the anchor the lane's own S122 row already cites (`corpus/lessons/round-54.md` §All located quotes, "S122 | 13300 | 标准号：GB/T 7714-2025"). So the register row cut one page's rendering and cited another page's URL.

**S082** — committed form (S096), section G @3433: `参考文献（この論文が引用している文献）、被引用文献（この論文が引用されている文献）の一覧が表示されます。` @3448 → the register wrote `被引用文献（この論文を引用している文献）`, i.e. the **passive** gloss of 被引用文献 replaced by the **active** gloss the page gives 参考文献 (inverting the definition); then `現在表示している論文を引用している文献です。` @3552 and `随時増加していきます。` @3577. The register quote as written: 0 occurrences; longest common substring 17/43.

**S084** — committed form (S098): `1.手動検索` @29547, `・記事編集の原文問合わせ機能` @29557, `・記事一覧の引用リンク削除・問い合わせ機能` @29575, `2.自動検索` @29599, `・J-STAGE公開時にシステムで引用元の所在を検索` @29609, `1.DOI（メタデータ項目） をもとに検索` @29672, `2.書誌情報（メタデータ項目） をもとに検索` @29706, `3.引用文献の原文情報からDOIを検出して検索` @29749, `4.引用文献の原文情報を書誌情報に解析して検索` @29775. Quote 2 items 3 and 4 are byte-exact in the form; items 1–2 carry the page's own trailing annotations (`　例：10.xxxx`, `　項目：著者名、誌名、巻号ページなど`). The register's joined-line rendering of a bulleted list occurs 0 times; with bullets and whitespace removed it matches (probe: `True`).

**S086** — no committed form: key `76914d78c20094f677dea77d` absent from `corpus/captures`; `git rev-list --objects --all | grep 76914d78` → empty (never committed); `.qcache` is now an empty directory (`ls … | wc -l` → 0); `grep -rlF "谁有权限使用网站上的资源"` over the whole shokuknow tree → no file (the help-page capture `c4e1446a…` is gone), and both quote strings survive only inside json/register/md rows. The quotes are CNKI-style FAQ copy of the **companion** URL `https://ncpssd.org/service/help?mainTitle=常见问题` named in the campaign gate block, not of the cited homepage (round-48 seat: PRESENT there, byte offsets 26676 / 27523 — evidence since deleted). A re-fetch of the *cited* URL would still not carry them.

**S088** — committed form (S123, `pdftotext -layout`): 表A.2 电子资源载体和标识代码 header @58955; rows contiguous @59025–59245: `磁带（ｍａｇｎｅｔｉｃ ｔａzp）<pad>ＭＴ` @59025/59063, `磁盘（ｄｉｓｋ）<pad>ＤＫ` @59073/59108, `光盘（ＣＤ－ＲＯＭ）<pad>ＣＤ` @59116/59153, `联机网络（ｏｎｌｉｎｅ）<pad>ＯＬ` @59161/59198, `缩微资料（ｍｉｃｒｏｆｏｒｍ ｍａｔｅｒｉａｌｓ）<pad>ＭＭ` @59201/59243. The quoted string occurs 0 times: `de-wrapped` fails because the page pads `）␠␠␠␠ＭＴ` while the quote has `）ＭＴ`; `no-whitespace` fails because the quote's ` / ` separators survive whitespace removal and the page has none there. With whitespace **and** the ` / ` separators removed the quote matches contiguously (normalized offset 34917) — every character of the quoted carrier list is in the document.

## 4. Sharpest finding — the register's `payload-absent` (fabrication class) is falsified on every capturable row

For all four rows whose cited source the lane holds in committed bytes, the register's note ("cited source, companion URLs and local artifacts were all checked; the quote is in none of them") is false: the cited pages carry the passages, in the register's own order and wording, split only by the renderer's line/column structure — and the lane's own registry **already grounds the same passages under other ids**, with anchors that land byte-exactly in the freshly re-fetched forms (manifest offsets are span starts; the quote sits at offset+80 per `corpus/evidence/round54/build-spans.py:28-29`):

- S084 → lane S098's own anchors: manifest 29402/29561/29592/29669/29695 → quotes @29482/29641/29672/29749/29775, all land in the fresh form ✔ (the register's quote 2 items 3–4 are two of these anchors, byte-exact);
- S082 → lane S096's own anchor `随時増加していきます。` (manifest 3497 → @3577) lands — the register's second clause;
- S088 → lane S123's own anchor `缩微资料（ｍｉｃｒｏｆｏｒｍ ｍａｔｅｒｉａｌｓ）` (manifest 59121 → @59201) lands;
- S080 → lane S121's six anchors (manifest 397/457/949/968/1082/1717 → @477/537/1029/1048/1162/1797) all land; the register's own three field/value pairs are in the same form's 基础信息 block @1327–1401, and its colon-joined rendering is the **sibling** S122 page's string @13300.

So none of these four is a fabrication: each is the same page's content re-joined by the register's checker. The two rows without a committed form (S077, S086) were never fabrications either: S077's quotes are verbatim in a committed artifact of the cited article; S086's were verbatim in a campaign capture that the cache deletion removed. **No row in batch A supports a fabrication verdict.**

## 5. Bearing on the frozen claims — reported, not patched

Nothing here touches R57-C2's or R57-C3's predicate, counter, control or recipe; `python3 corpus/evidence/round57/c2-count.py --verbose` → `SET=47 VERDICTS=47/47 REPRODUCED=41 DRIFTED=5 UNREACHABLE=1 BYTE_BACKED=46 CONSISTENT=46/46 FLAGGED=0/0 C2=PASS` (exit 0), unchanged.

One calibration datum for C2's freshness axis: **S121 is counted DRIFTED, but the drift is not a page change.** The fresh re-fetch of that key is byte-identical to the lane's previously committed blob (`git cat-file -p fb794020… | sha256sum` → `ed4dde2ea950ba19…` == fresh `.txt`), the pin `4e46154f…` exists nowhere on this host (no file in `corpus/captures` hashes to it), and all six of the lane's recorded S121 anchors land at their cited offsets in the fresh form. The DRIFTED label therefore records "the pinned capture is gone", not "the page changed" — a different statement than C2's counter text reads as. Reported for the L1 to weigh; no counter, pin or lesson line was edited.

## 6. Commands run (all read-only)

- `awk -F'|' -v l='chousa' …` (slice, 24 rows); `awk` on the register for the six rows; `sha256(url)[:24]` per URL.
- `python3 tools/quarantine-check.py verdict --cache …/corpus/captures` (lane tool, unmodified, run against the lane store) → for the six: unverifiable/absent/absent/absent/unverifiable/absent on the *id-mismatched* URLs, confirming the collision from the tool's side.
- Scratch sweep (`sweep.py`, `substance.py`, `verify.py`): eleven folds + per-item/per-line substrings + longest-common-substring over each defined form; store-wide sweep over all 58 committed text forms for every quote token.
- `python3 tools/capture-text.py` not needed (no OLE/zip row in batch A).
- `pdftotext -layout` on the S123 raw; `diff` of campaign `html_to_text` output vs stored `.txt` (3/3 identical after CRLF→LF).
- `git cat-file -p fb794020…` / `git rev-list --objects --all | grep` for the old vs fresh S121 bytes and the two never-committed keys.
- `grep -rlF` over the shokuknow tree for the S077/S086 quote strings and the FAQ marker; `ls .qcache | wc -l`.
- `bash /home/vgpnk/Projects/shokunin/scripts/hyaku/disk-guard.sh status` → /tmp 3 %, /fast/scratch/hyaku 26 %.

**Tool installs: none** (no install was needed; nothing upgraded).

## 7. Scratch

Scratch root `/fast/scratch/hyaku/chousa-r57/R57W1QuarA/` (`TMPDIR=$PWD`, `PYTHONDONTWRITEBYTECODE=1`); it held only the sweep scripts, the extracted forms under `workall/` and one 6.6 KB copy of the old S121 `.txt`. **Deleted before yield** (`rm -rf -- /fast/scratch/hyaku/chousa-r57/R57W1QuarA`); nothing was written outside my own report file.

VERDICT: batch A hand-check — 6 rows adjudicated (S077 PRESENT, S080 PRESENT, S082 ABSENT-as-written, S084 PRESENT, S086 UNVERIFIABLE, S088 PRESENT); the register's `payload-absent`/fabrication class is falsified on every row with a committed form and no row supports a fabrication verdict, so the batch survives as a **finding against the register's checker, not against the frozen claims** (C2 still `C2=PASS`, unchanged).

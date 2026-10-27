# R57W1ScribeEntry — R57-C3: the `normative-reference-chain-china-r57.md` entry drafted, and every non-fetch leg of the frozen counter proved on lane bytes

Seat: scribe (leaf; no dispatch). Base `6656f077`; C3 frozen at `fd95724d`. No fetch by this seat (`curl`/`wget` unused): only committed bytes under `corpus/captures/` were opened. Every figure below was re-measured here; nothing inherited.

## 1. What I built

A 42-line entry draft for `corpus/knowledge/normative-reference-chain-china-r57.md` (§3) plus the Registry-row texts (§4) and the exact `build-spans.py` quote table (§5). It carries the fixed shape — title, provenance trio (`source: S127 — U` anchor plus one `source: X — U` per bound reference), `verified-at`, `recheck: 180d`, `ground`, `adopted: round 57`, then `#### Observation` (six bullets, each a located quote with its char offset and span file), `#### Inference` (three bullets, each citing an S id and grounded by a backticked phrase from that id's spans), `#### Limits`, `#### Province`.

Measured state of the draft: **BOUND=2/7 — R3:S133 and R7:S118**; the other five references carry `UNBOUND R<k> sweep:` lines built from this wave's own failed refetch rows. Two more bound documents reach the frozen floor of four. Nothing in the draft proposes a change to a predicate, target, counter, control or recipe.

## 2. Gates — what I ran and what it printed

All three runs used the **unmodified frozen counter** except where a copy is named; the copy mutates only `REFS`, `MIN_BOUND` and `LANE`, and never the lane file.

**Run A — draft with only the held R7 (the R3 block removed), root = scratch fixture:**
```
$ python3 corpus/evidence/round57/c3-count.py --root $S/fix
ENTRY=yes S127_CITED=yes NEW_GROUND=yes CLAUSE=yes
BOUND=1/7 (min 4) R7:S118
SWEPT=6/6 R1 R2 R3 R4 R5 R6
QUOTE_ROWS=11 IN_SPAN=11 IN_ENTRY=11 IN_LESSON=11 SHORT=11 CONTEXT=11 CAPTURE_BOUND=11
SUBSTANCE=PASS ANCHOR_BOUND=0/0 INFERENCE_GROUNDED=yes STRAY_IDS=-
C3=FAIL
```

**Run B — draft as shipped (§3, with the R3 candidate already landed), root = scratch fixture:**
```
$ python3 corpus/evidence/round57/c3-count.py --root $S/fix3 ; echo $?
ENTRY=yes S127_CITED=yes NEW_GROUND=yes CLAUSE=yes
BOUND=2/7 (min 4) R3:S133 R7:S118
SWEPT=5/5 R1 R2 R4 R5 R6
QUOTE_ROWS=13 IN_SPAN=13 IN_ENTRY=13 IN_LESSON=13 SHORT=13 CONTEXT=13 CAPTURE_BOUND=13
SUBSTANCE=PASS ANCHOR_BOUND=1/1 INFERENCE_GROUNDED=yes STRAY_IDS=-
C3=FAIL
1
```
Only the BOUND leg fails (2 < 4). Every quote leg, the clause row, the anchor leg, substance, inference grounding and the stray-id sweep already pass — so a landed document costs the L1 two manifest rows and one Registry row, not a rewrite.

**Run C — proof that the whole counter can reach `C3=PASS` on this skeleton**, using a scratch copy (`REFS` = R3 with the token `二〇二〇年十一月`, R7; `MIN_BOUND = 2`; `LANE` → the real lane, so `git show`/`git grep` still read the frozen base):
```
$ python3 $S/fix2/mut/c3-count-mut.py --root $S/fix2 ; echo $?
ENTRY=yes S127_CITED=yes NEW_GROUND=yes CLAUSE=yes
BOUND=2/2 (min 2) R3:S133 R7:S118
SWEPT=0/0 -
QUOTE_ROWS=13 IN_SPAN=13 IN_ENTRY=13 IN_LESSON=13 SHORT=13 CONTEXT=13 CAPTURE_BOUND=13
SUBSTANCE=PASS ANCHOR_BOUND=1/1 INFERENCE_GROUNDED=yes STRAY_IDS=-
C3=PASS
0
```

**Quote leg, per row** (`python3 tools/build-spans.py --quotes q.tsv --out … --cache corpus/captures` prints one line per accepted quote; all 13 accepted, each occurring exactly once in its form):
```
QUOTE S127 char 4696 spans/S127-1.txt   … QUOTE S127 char 5100 spans/S127-9.txt
QUOTE S118 char 3334 spans/S118-1.txt   QUOTE S118 char 3549 spans/S118-2.txt
QUOTE S133 char 19   spans/S133-1.txt   QUOTE S133 char 53   spans/S133-2.txt
SPANS_ROWS=13 WRITTEN=13
```
Longest quote 42 chars / 4 whitespace words (limits 160 / 25); every span file is quote ± ≤80 chars, so `quote-substance-check.py` (round 51) exits 0 on it (`SUBSTANCE=PASS` above). The clause sentence the freeze names starts at `b27ffd2f0161104c6a28c9f5.txt` char 4709 (`t.find("规范性引用而构成本文件必不可少的条款")`), i.e. 13 chars into the S127-1 quote whose own offset is 4696 — the counter only requires the clause inside the quote, so both numbers are consistent.

**Sweep across the whole capture store** (all 54 `corpus/captures/*.raw`, each PDF through the `.txt` form, OLE/zip through `tools/capture-text.py`, tested with the counter's own `heading_title` + `nows(token)` rules): the only captures that bind any of R1–R7 are `16fe8487aa97b98576a0dbac` (R7) and `6f545e6c16b6b568ea3f591b` (R3). R1, R2, R4, R5, R6 have **no** holder in the store.

## 3. The entry draft (deliverable — the L1 copies this block into `corpus/knowledge/normative-reference-chain-china-r57.md`)

```markdown
# The 药品临床综合评价工作流程指南 draft binds its user to seven national instruments through 2 规范性引用文件, and each can be bound only by the document's own printing of its title and edition

source: S127 — https://www.ttbz.org.cn/upload/file/20250407/6387963976070960491020144.pdf — 药品临床综合评价工作流程指南（2025 版）（征求意见稿）, served by the 全国团体标准信息平台: 1 范围, its 2 规范性引用文件 clause with the seven-reference list, and 3 术语和定义; text form `corpus/captures/b27ffd2f0161104c6a28c9f5.txt` read as UTF-8 with universal newlines
source: S118 — https://www.bjhea.org.cn/ueditor/php/upload/file/20250115/1736907153935975.pdf — the issued 药品临床综合评价质量控制指南（2024 年版 试行）, the R7 document below as the lane holds it: the title block, the drafting history and 附件一; text form `corpus/captures/16fe8487aa97b98576a0dbac.txt`
source: S13N — <URL of the row the L1 binds to R1, pasted with that row> — <its document title as its own cover prints it>; text form `corpus/captures/<key>.txt`
source: S133 — http://www.tcmevidence.net/UserFiles/upload/file/20230410/6381676262587201848492833.pdf — 药品临床综合评价管理指南（2021 年版试行）, the edition the R3 line names, served by tcmevidence.net: the cover block and 第四章 指南管理; text form `corpus/captures/6f545e6c16b6b568ea3f591b.txt`
verified-at: 2026-10-27 — S127, S118 and S133 re-opened read-only from lane-owned captures under `corpus/captures/` (no fetch of this entry's own documents by this seat); every backticked quote below occurs exactly once in its text form and at the char offset given, checked by `python3 tools/build-spans.py --quotes <this entry's quote table> --out corpus/evidence/round57/c3 --cache corpus/captures`
recheck: 180d — re-open the draft's 2 规范性引用文件 and confirm the seven lines and their 文号/edition tokens still read as quoted; for each bound row re-open its capture and confirm the title still prints as a line-heading with its edition token
ground: citation chaining — what a Chinese group standard's normative-reference clause binds a user of it to, and which of the named instruments the lane can show by document. The lane holds the issued quality-control guideline (`corpus/knowledge/quality-control-guideline-issued-text-r48.md`) and the draft's grey-literature source list (`corpus/knowledge/grey-literature-field-china-r42.md`), neither of which reports the clause; at this round's base no `corpus/knowledge` file held 规范性引用文件
adopted: round 57

#### Observation

- **The clause makes the listed documents binding clauses of the draft, and it states which edition applies.** Under 2 the draft prints `下列文件中的内容通过文中的规范性引用而构成本文件必不可少的条款。其中，注日期` (`S127`, char 4696, `spans/S127-1.txt`) and then `的引用文件，仅该日期对应的版本适用于本文件；不注日期的引用文件，其最新版本（包括` (char 4735, `spans/S127-2.txt`) — a dated reference binds the dated edition only, an undated one binds the latest.
- **R1 is cited by 文号 under the commission, and R2 by 文号 under its general office.** The list reads `国家卫生健康委《关于开展药品使用监测和临床综合评价工作的通知》（国卫药政函` (`S127`, char 4794, `spans/S127-3.txt`) with the number `〔2019〕80 号）` printed on the following line, and `国家卫生健康委办公厅《关于规范开展药品临床综合评价工作的通知》（国卫办药政发` (char 4847, `spans/S127-4.txt`) followed by `〔2021〕16 号）`. Neither line prints an edition year.
- **R3 is the management guideline, cited under the general office with an edition year.** `国家卫生健康委办公厅《药品临床综合评价管理指南》（2021 年版 试行）` (`S127`, char 4901, `spans/S127-5.txt`) — the one listed instrument the draft calls by the short name it also uses in its body (`《管理指南》`).
- **The R3 document the lane now holds prints its title alone on the cover and its edition beneath.** `药品临床综合评价管理指南` (`S133`, char 19, `spans/S133-1.txt`) and `（2021 年版试行）` (char 53, `spans/S133-2.txt`) — the 2021 edition, with 第四章 指南管理 closing `本指南自发布之日起施行` in the same text form.
- **R4-R7 are the centre's four technical and quality-control guides, and only R4's line prints the issuing body.** The block opens `国家药物和卫生技术综合评估中心（“国家卫生健康委卫生发展研究中心“）《抗肿瘤` (`S127`, char 4941, `spans/S127-6.txt`), and the remaining titles continue without a body: `《心血管病药品临床综合评价技术指南（2022` (char 5034, `spans/S127-7.txt`), `年版 试行）》《儿童药品临床综合评价技术指南（2022 年版 试行）》《药品临床综合` (char 5057, `spans/S127-8.txt`) and `评价质量控制指南（2024 年版 试行）》` (char 5100, `spans/S127-9.txt`).
- **The R7 document the lane holds prints its title as a heading of its own text.** The capture of `S118` opens with the line `药品临床综合评价质量控制指南` alone (char 0) and prints `（2024 年版 试行）` beneath it (char 18); its drafting history names the earlier form `内容，形成《药品临床综合评价质量控制指南（2024 年版 讨论` (`spans/S118-1.txt`, char 3334) `稿）》` and the settled one `控制指南（2024 年版 试行）》。` (`spans/S118-2.txt`, char 3549), so the held copy is the 试行 text of the 2024 edition.

#### Inference

- **A workflow written to the draft must treat the seven as binding, because the clause says so in its own words.** `S127` prints `规范性引用而构成本文件必不可少的条款`, and the sentence's subject is the content of the listed files, not a bibliography: on the clause's own dated/undated rule the seven enter the draft's requirements with the editions printed beside them.
- **R1 and R2 are the two references the clause's date limb cannot settle.** `S127` identifies them by 文号 (`国卫办药政发`) and prints no edition year, while the clause divides its references into dated and undated; a 文号 is a document number, not a date, so a reader cannot tell from the clause alone whether an amended notice supersedes the one named.
- **Binding is by document and edition, not by a title several documents share.** `S118` opens with `药品临床综合评价质量控制指南` alone and prints （2024 年版 试行） beneath it, while the draft's own drafting history carries the same title in its 讨论稿 form; a title string therefore cannot decide which file is the document the clause names, and the edition printed beside it is what separates them.

#### Limits

- **Heading versus citation printing.** Inside the draft the seven titles are printed as citations (`《…》`, 文号 in a parenthetical, continuation lines that repeat no body). None of those lines is a heading of the cited document, and the draft's own file cannot satisfy the heading test for any of them; that test is applied to each bound document's own text form.
- **Edition-token presence is a floor, not an identity test.** R1 and R2 print 文号 without a year; R3-R7 print a year with 试行 but no 文号. A captured document that prints neither the title as a line-heading nor the edition token cannot be bound to its reference even when it is plausibly the same instrument — the 2020 text of the management guideline states no 2021 edition token, so it cannot stand for R3 here.
- **What binding does not prove.** Binding shows that a lane-owned capture is the bytes of a successful attempt for that row's URL and that those bytes print the title as a heading plus the edition token; it does not show that the edition is the one in force, that its content is what the clause relies on, or that the document the standard means is the one fetched (the counter discloses the same limit in its docstring).
- **Body attribution for R5-R7 rests on the block's first line.** Only R4's line prints 国家药物和卫生技术综合评估中心（“国家卫生健康委卫生发展研究中心“）; R5-R7 continue the block without repeating a body, so their issuing body is read from R4's sentence and from the documents themselves, not from a printed 文号.
- **Text form is a layout rendering.** The clause's lines break inside titles and numbers (`（国卫药政函` / `〔2019〕80 号）`), so every quote here is bounded by where `pdftotext -layout` broke the line; a re-render with different wrapping would move the offsets, not the wording.
- UNBOUND R1 sweep: nhc.gov.cn 2019-04 notice page returned HTTP 412 to the campaign GET; the web.archive.org/web/2024 mirror returned 404 (both rows in refetch.tsv, key 9d57f9ca / 8146b1e3)
- UNBOUND R2 sweep: nhc.gov.cn 2021-07 notice page returned HTTP 412; the web.archive.org/web/2024 mirror returned 412 (refetch.tsv keys 2c2a982d / 676178c6)
- UNBOUND R4 sweep: no host located for the 抗肿瘤 technical guide in this wave's refetch rows
- UNBOUND R5 sweep: no host located for the 心血管病 technical guide in this wave's refetch rows
- UNBOUND R6 sweep: no host located for the 儿童 technical guide in this wave's refetch rows

#### Province

- The normative-reference structure of a Chinese group standard and what its clause binds a user of the standard to are chousa's (citation chaining, source hierarchy). What the seven instruments require of a drug clinical comprehensive evaluation, the grading systems they adopt, and whether the draft will be issued under a real T/CLPA number are adjacent ground this entry reports and does not hold.
```

**When the L1 binds more references**, per bound document: (a) add its `source: <id> — <first URL of that row>` line, replacing the placeholder `source: S13N` line; (b) delete that reference's `- UNBOUND R<k> sweep:` line (the counter requires `SWEPT == 7 − BOUND` exactly); (c) add ≥2 manifest quote rows of that id (one quote containing the title, one carrying the edition/文号); (d) paste every manifest quote into the lesson; (e) append the entry path to that row's `used-by`; (f) set the anchor from the built manifest, not from the `offset` column (see §4). Ids other than S127/S118/S133 must not appear in the entry unless bound.

## 4. Registry rows (per bound document; insert inside `## Registry`, never after the table)

Ready for R3 — this exact row is what Run B/C accepted (its anchor `char 19` is the quote offset, verified as `spans.tsv` offset 0 + `span.find(quote)` 19):

```
| S133 | 药品临床综合评价管理指南（2021 年版试行）— 国家卫生健康委办公厅 instrument, served by tcmevidence.net — http://www.tcmevidence.net/UserFiles/upload/file/20230410/6381676262587201848492833.pdf | docs | B | for the 2021 edition of the management guideline that the draft cites as R3: the cover block, the 制定依据 paragraph and 第四章 指南管理; the host is a third-party evidence site, so the tier is B | char 19 | what the 2021 edition prints on its cover and which notice its 制定依据 names | mined | 2026-10-27 | 180d | corpus/knowledge/normative-reference-chain-china-r57.md |
```

Template for each further bound reference (`<N>`, `<TITLE>`, `<ISSUER>`, `<U>`, `<TOKEN>`, `<OFF>` filled from the landed bytes):

```
| S13<N> | <TITLE>（<TOKEN>）— <ISSUER>, served by <host> — <U> | docs | B | for <what this copy prints that answers the R<k> line: cover block, edition token, 文号>; <why tier B: host or carrier> | char <OFF> | <what to re-open for> | mined | 2026-10-27 | 180d | corpus/knowledge/normative-reference-chain-china-r57.md |
```

Two mechanical traps, both measured here: (i) the row's **first** URL in the `source` cell is the one `c3-count.py` compares against the capture, so a row that lists the right document second binds nothing; (ii) the anchor's `char N` is the **quote** offset (`c3-count` computes `offset + span.find(quote)`), while `build-spans.py` writes the *span start* (`quote − 80` when context exists) — using the `offset` column gives `char 0` and fails `ANCHOR_BOUND`.

## 5. Quote table for `build-spans.py` (the 13 rows Runs A–C built)

```
id	url	quote	entry
S127	https://www.ttbz.org.cn/upload/file/20250407/6387963976070960491020144.pdf	下列文件中的内容通过文中的规范性引用而构成本文件必不可少的条款。其中，注日期	corpus/knowledge/normative-reference-chain-china-r57.md
S127	https://www.ttbz.org.cn/upload/file/20250407/6387963976070960491020144.pdf	的引用文件，仅该日期对应的版本适用于本文件；不注日期的引用文件，其最新版本（包括	corpus/knowledge/normative-reference-chain-china-r57.md
S127	https://www.ttbz.org.cn/upload/file/20250407/6387963976070960491020144.pdf	国家卫生健康委《关于开展药品使用监测和临床综合评价工作的通知》（国卫药政函	corpus/knowledge/normative-reference-chain-china-r57.md
S127	https://www.ttbz.org.cn/upload/file/20250407/6387963976070960491020144.pdf	国家卫生健康委办公厅《关于规范开展药品临床综合评价工作的通知》（国卫办药政发	corpus/knowledge/normative-reference-chain-china-r57.md
S127	https://www.ttbz.org.cn/upload/file/20250407/6387963976070960491020144.pdf	国家卫生健康委办公厅《药品临床综合评价管理指南》（2021 年版 试行）	corpus/knowledge/normative-reference-chain-china-r57.md
S127	https://www.ttbz.org.cn/upload/file/20250407/6387963976070960491020144.pdf	国家药物和卫生技术综合评估中心（“国家卫生健康委卫生发展研究中心“）《抗肿瘤	corpus/knowledge/normative-reference-chain-china-r57.md
S127	https://www.ttbz.org.cn/upload/file/20250407/6387963976070960491020144.pdf	《心血管病药品临床综合评价技术指南（2022	corpus/knowledge/normative-reference-chain-china-r57.md
S127	https://www.ttbz.org.cn/upload/file/20250407/6387963976070960491020144.pdf	年版 试行）》《儿童药品临床综合评价技术指南（2022 年版 试行）》《药品临床综合	corpus/knowledge/normative-reference-chain-china-r57.md
S127	https://www.ttbz.org.cn/upload/file/20250407/6387963976070960491020144.pdf	评价质量控制指南（2024 年版 试行）》	corpus/knowledge/normative-reference-chain-china-r57.md
S118	https://www.bjhea.org.cn/ueditor/php/upload/file/20250115/1736907153935975.pdf	内容，形成《药品临床综合评价质量控制指南（2024 年版 讨论	corpus/knowledge/normative-reference-chain-china-r57.md
S118	https://www.bjhea.org.cn/ueditor/php/upload/file/20250115/1736907153935975.pdf	控制指南（2024 年版 试行）》。	corpus/knowledge/normative-reference-chain-china-r57.md
S133	http://www.tcmevidence.net/UserFiles/upload/file/20230410/6381676262587201848492833.pdf	药品临床综合评价管理指南	corpus/knowledge/normative-reference-chain-china-r57.md
S133	http://www.tcmevidence.net/UserFiles/upload/file/20230410/6381676262587201848492833.pdf	（2021 年版试行）	corpus/knowledge/normative-reference-chain-china-r57.md
```
Build with `python3 tools/build-spans.py --quotes Q.tsv --out corpus/evidence/round57/c3 --cache corpus/captures`; the lesson must then carry all 13 quotes verbatim (`IN_LESSON` is counted, not assumed).

## 6. Findings (reported, not patched)

- **F1 — R3's document landed while this seat worked, and it satisfies every leg.** `refetch.tsv:104` is S133 attempt 2 on `http://www.tcmevidence.net/…/6381676262587201848492833.pdf`, rc 0 / http 200, `raw_sha256=c4bedad5…5eb`; the committed `.raw` hashes to exactly that, its `.txt` (21 401 bytes) to `ceef80d9…a7a0`, and a fresh `pdftotext -layout` of the committed raw is byte-identical to that `.txt` (`cmp` rc 0), so the form is complete, not truncated. The cover prints `药品临床综合评价管理指南` alone at char 19 and `（2021 年版试行）` at char 53 — the R3 title as a heading, the `2021年版` token present after whitespace removal.
- **F2 — one of S133's three URLs is a byte-identical duplicate of the held 2020 text.** `corpus/captures/6fe041ac…raw` sha256 = `d01795dd…8e7d` = `corpus/captures/a42feae4…raw` (the 2020 `管理指南（试行）`, S130's file), and the two `.txt` forms share sha256 `71fed1a3…688f`. That text prints no `2021年版`, so it cannot bind R3 — and because `c3-count.py` compares only the **first** URL of a row's source cell, a row opening with the nhc cms-search URL leaves R3 unbound even though the same row also holds the 2021 file.
- **F3 — S133's third URL cannot bind anything.** `c71776bc…` (forten-sp OSS) is an image scan: `pdftotext -layout` on the committed raw yields 2 bytes, so the `.txt` is the raw decoded, no title, no token.
- **F4 — attack on the binding rule with a real citer, survived.** `9695437c…` (S134, a 湖南药事服务网 article) prints all three technical-guide titles and `2022年版` (counts 2 / 2 / 5) and its `<title>` names them together — a citer, not a document. Under the frozen `heading_title` leg it binds none of R4/R5/R6 (no title ends a line after a ≤16-char prefix). The heading leg is what separates a document from an article about it; the count leg alone would have let it through.
- **F5 — the R1/R2 "latest version" reading is not derivable.** The clause divides references into dated and undated, but R1/R2 print 文号 with no year; the draft states this as an inference on the clause's own words, and refuses the step to "the latest amended notice supersedes the named one".
- **F6 — adjacent, unjudged (C2's leg, not mine):** S135's `ad3010d2…` raw is a 4 321-byte HTML page whose `.txt` is 1 byte. Whether that satisfies C2's `CONSISTENT` recipe (`html_to_text` for an HTML raw) is for the frozen C2 counter to print; I did not compute it and did not run the campaign's tooling.

## 7. Bounds incident — disclosed, and repaired

I made a boundary mistake in my own scratch setup and repaired it before doing anything else. I created `<scratch>/fix/corpus/SOURCES.md` as a **symlink** to the lane's `corpus/SOURCES.md`; a `write_text` in my fixture script then landed *through* the link, appending the entry path to the `used-by` cells of S118 and S127 and later an `S133` row in the lane's real file. Detected in the next cell with `git status --porcelain corpus/SOURCES.md` (showed ` M corpus/SOURCES.md`, diff = exactly my three edits). Restored from the frozen bytes with `git show HEAD:corpus/SOURCES.md > …/SOURCES.head.md` then `cat` back over the path — read-only plumbing, no `checkout`/`reset`/`commit`. Verified after: `git status --porcelain corpus/SOURCES.md` prints nothing and `git diff --stat corpus/SOURCES.md` prints nothing. The fixture link was replaced with a real copy (`cp`, never a link) before any further run. No other lane path was written by me; the other working-tree entries (`M corpus/evidence/round57/refetch.tsv`, new `corpus/captures/*` pairs) are the L1's own fetch work, not mine.

## 8. Bounds, tooling, scratch

- Writes: this report only (plus the transient, repaired superset in §7). No knowledge/registry/lesson/control/counter edit, no `git`/`jj` mutation, no fetch, no fleet-root, shokuknow or sibling-lane touch. The frozen `c3-count.py` was never edited; Run C used a copy in scratch whose `REFS`/`MIN_BOUND`/`LANE` alone differ.
- Tooling: **nothing installed or upgraded**; `pdftotext`/`pdfinfo` 26.08.0 were already present and are the frozen recipe's own tools.
- Scratch `/fast/scratch/hyaku/chousa-r57/R57W1ScribeEntry/` deleted before filing (`rm -rf -- "$S"`); `TMPDIR` and `PYTHONDONTWRITEBYTECODE` pointed there, nothing written to `/tmp`.

VERDICT: built the R57-C3 entry and its Registry rows — 2/7 bound (R3:S133, R7:S118), 5 sweeps, all 13 quote legs, SUBSTANCE and inference grounding green on the unmodified counter, and the new-row path proved to `C3=PASS` on a scratch copy — and attacked the heading leg with a real citer, an image-only PDF and a byte-duplicate 2020 text, all refused; survived, with only the BOUND floor (2 < 4) outstanding.

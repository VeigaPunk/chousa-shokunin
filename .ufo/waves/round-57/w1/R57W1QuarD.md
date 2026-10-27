# R57W1QuarD — Quarantine hand-check, batch D (chousa r57 w1)

Seat: executor. Scope: register rows S125, S116 (double-check vs batch C) + the four prose-class rows S100`-S103`; re-derive the slice row count. Read-only; **no edits** to lane, fleet root, or shokuknow.

## 1. Slice row count — re-derived: **24 data rows (20 payload-absent + 4 prose)** ✔

Recipe is the prompt's own (`/home/vgpnk/Projects/shokunin/.ufo/prompts/chousa-round-57.md:601`):

```sh
R=/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/absent-defect-register.md
awk -F'|' -v l='chousa' '$2 ~ ("`" l "`") && $3 ~ /round[0-9]+/ && $4 ~ /S[0-9]+/ {print $4, $5}' "$R"
```

→ 24 lines: 20 `payload-absent` (register lines 37–56) + 4 `the gate block named no locator, so no quote was checked` (register lines 269–272). `grep -c payload-absent` = 20, `grep -c 'named no locator'` = 4. The register's own `## By lane` summary (line 238) says `chousa | 20` — **stale** (it counts only the `## Rows` table); its header's "194 rows" is stale too. 24 is correct.

## 2. **Namespace collision (finding; affects every batch seat)**

The register's S-ids and the lane's `corpus/SOURCES.md` S-ids are **different registries**: 18/20 payload-absent register URLs exist in the lane registry under a *different* id, and 2 (register S077 `doi.org/10.1186/s13643-020-01542-z`, S086 `https://www.ncpssd.cn/`) exist nowhere in the lane registry (neither URL string is present in `corpus/SOURCES.md`, neither has a capture in `corpus/captures/`, and neither appears in `refetch.tsv`). Register→lane id for the rest: S125→**S124**, S116→**S086**, S120→S115, S114→S111, S111→S109, S112→S110, S110→S094, S108→S092, S105→S108, S104→S107, S093→S090, S094→S091, S095→S100, S096→S101, S088→S123, S084→S098, S082→S096, S080→S121 — **no register id matches its lane id**. So this item's "S125 (cnpharm HTML)" and batch C's "S116 (web.archive.org URL)" name the **lane** S125/S116, while the **register** rows S125/S116 are the gcpunion `.doc` and the aclanthology PDF. Both readings are adjudicated below; the choice is the L1's.

Peer seat R57W1ReviewQuarMethod measured the same collision and first reported "19 collisions + S095 no-lane-row"; on re-derivation I got 18 + S077/S086 absent — register **S095**'s URL *is* in `corpus/SOURCES.md` (as lane S100, the zcmu `.doc`, exact string match), so S095 is a collision like the rest, not an orphan. The peer re-checked, confirmed the zcmu URL is on lane row S100 (line 110), and corrected its report to 18 + S077/S086. The counts now agree, and the substantive conclusion is identical either way: 0/20 register ids resolve to their own lane row.

## 3. Verdict table — register-namespace rows S125 / S116 (the quarantine scope)

Defined form per the frozen C2/C3 rule (`corpus/evidence/round57/c2-count.py:135` `defined_form`): OLE/zip raw → `tools/capture-text.py` stdout; else the `.txt` (PDF → `pdftotext -layout`). Strict test = NFKC + whitespace collapse (round-42 frozen rule, `corpus/evidence/round42/claims.md:40`).

| reg id | committed capture (key) | form | quotes located | verdict |
|---|---|---|---|---|
| **S125** | `bdff491a75c6abeda1d9c01d.raw` (OLE `d0cf11e0`) | `capture-text.py` stdout, 13718 chars, 0 U+FFFD | **2/3** — q0 exact @4625, q1 exact @761, q2 not located | **mixed** (rule step 5: 0<2<3) → refuse-with-correction, **not** fabrication |
| **S116** | `1c15b611118dee97e4105fcf.raw` (`%PDF-`) | `.txt` = `pdftotext -layout`, 60030 chars | **0/3** in the defined `-layout` form | **absent by the strict rule** — but §5: the artifact is the rendering, not the document |
| **S120** (peer-measured, re-verified by me) | `3a8b45977cd111e45e3980a5.raw` (zip `PK\x03\x04`) | `capture-text.py` stdout (the `.txt` sidecar is zip bytes) | **3/3** exact @8996 / @9020 / @9428 | **PRESENT** — §5 |

q0/q1 match the register's quote cell **verbatim** (register line 56), at the same offsets the lane's own row for that URL (lane S124) already cites: `char 761, char 994, char 4625`. q2 differs from the source only by the source's own curly quotes — source `@994` = `查找时应当注意收集未公开发表的文献，即“灰色文献”，如会议论文…` vs register `…即灰色文献，如会议论文…` — a U+201C/U+201D omission in the register quote, not a fabrication; the eleven campaign folds cannot see it (`typographic` maps curly→ascii on *both* sides, and the quote has no marks at all).

## 4. Verdict table — lane-namespace rows S125 / S116 (the reading the item text names)

Both **REPRODUCED** by the frozen counter, and every lane-recorded anchor lands exactly:

```
python3 corpus/evidence/round57/c2-count.py --verbose | grep -E 'S116|S125'
CAPTURE S116 e84bfe97808591d23fe3266f pin=93558b6d4b0e REPRODUCED
CAPTURE S125 27d4865f201e99c1fed9f79b pin=cd65aa9e26b4 REPRODUCED
```

| lane id | URL / key | committed form | lane anchors land? | verdict |
|---|---|---|---|---|
| S125 | m.cnpharm.com `c280684.html` / `27d4865f201e99c1fed9f79b` | `.txt` html_to_text, **1673 chars**, sha256 prefix `cd65aa9e26b41d8a` (= `refetch.tsv` txt_sha256 = the lane row's recorded prefix) | ✔ `@242` byline `作者：郭婷 2019-06-18 来源：中国健康传媒集团-中国食品药品网`; `@371` `6月18日，国家药品监督管理局发布通告，发布《上市药品临床安全性文献评价指导原则（试行）》…`; `@780` `指导原则分为概述、方法学要点、报告撰写规范、指导原则所依据的参考文献和附录五个方面。…` | **PRESENT** (all three spans located, offsets reproduced) |
| S116 | web.archive PRISMA `list_1.pdf` / `e84bfe97808591d23fe3266f` | `.txt` `pdftotext -layout`, **5328 chars** (= the lane row's recorded "5328 characters") | ✔ `@475` `…文献を特定するために調べたり，助言を求めた情報`; `@592` `それぞれの情報源が最後に調べられた日付を記載する。 検索戦略 7`; `@641` `用いたフィルターや制限も含め，…`; `@753` `試験登録，Web サイトの完全な検索戦略を記載する。` | **PRESENT** (情報源 item 6 / 検索戦略 item 7 located) |

## 5. **Sharpest finding — the register's `payload-absent` (fabrication class) is falsified for S125 and S116**

Both register rows carry the *fabrication class*. Neither quote is fabricated.

* **S125 (gcpunion `.doc`)** — the campaign's `quote-lint.py:462 fetch()` renders **only** `%PDF-` (`pdftotext -layout`, line 497); every other type falls through to `data.decode("utf-8","replace")` (line 508). An OLE `.doc` was therefore **never rendered**: the store's `.txt` sidecar is a UTF-8 decode of the compound file (241510 chars, 40252 U+FFFD) containing **no** `检索策略` / `灰色文献` / `查找时应当注意` at all. `tools/capture-text.py` renders it, and 2 of the 3 quoted spans are then present **verbatim**. Round 42 recorded this row `unverifiable` ("OLE binary document … never rendered to text", `corpus/evidence/round42/quarantine-verdicts.tsv`); the lane's own row for that URL (lane **S124**) already cites the render with anchors **761, 994, 4625**.
* **S116 (aclanthology `N18-1074.pdf`)** — the committed `.txt` is `pdftotext -layout`, which interleaves the second column and hyphenates. Reading-order extraction of the **same committed `.raw`** locates all three register quotes strictly: `pdftotext corpus/captures/1c15b611118dee97e4105fcf.raw -` → `in 31.75% of the claims more` @4119, `resulting in inter-annotator agreement of 0.6841 in Fleiss κ …` @4457, `We used the June 2017 Wikipedia dump` @11760 (whitespace-collapsed offsets); the untruncated campaign quotes from `quote-lint-full-v5.json` also all locate there (5/5). The lane's own row for that URL (lane **S086**) documents the cause: "pdftotext -layout splits the two-column page, so the word completes as dence retrieval. at char 6784".
* **Corroboration (independent, peer seat R57W1ReviewQuarMethod, re-verified by me)** — register **S120** (c2h.niph `.docx`, key `3a8b45977cd111e45e3980a5`) is the same case a third time: the committed `.txt` sidecar is zip bytes (`PK\x03\x04`, `file` says "Zip archive data"), and `tools/capture-text.py` on the `.raw` locates all three register quotes **exact** at offsets 8996 / 9020 / 9428. The peer measured this first; I re-ran those three `--locate` calls myself and each returned `LOCATED count=1` (rc 0). So S120 = **PRESENT**, not `absent`.

So the register's `payload-absent` on both rows is an artifact of the checker's *form choice* (OLE never rendered; two-column PDF rendered with `-layout`), not evidence of a fabricated quote. Nothing here touches a frozen claim: under C2's numbering these captures are lane **S124** and **S086**, both **REPRODUCED**, and the DRIFTED set (S083 S087 S113 S114 S121) has `absent=0/m` on every row, so `FLAGGED=0/0` and `C2=PASS` stands unchanged (`SET=47 VERDICTS=47/47 REPRODUCED=41 DRIFTED=5 UNREACHABLE=1 BYTE_BACKED=46 CONSISTENT=46/46 FLAGGED=0/0 C2=PASS`, exit 0). Reported, not patched.

## 5b. Wave-level convergence — the same artifact, measured independently by three seats

Three seats now measure the same defect from disjoint rows — the strongest evidence this round produces that the register's `payload-absent` note ("cited source, companion URLs and local artifacts were all checked; the quote is in none of them") is unreliable as written.

| seat | rows | form that hid the quote | measured result |
|---|---|---|---|
| R57W1QuarD (this seat) | register S125 (`.doc`), S116 (two-column PDF) | OLE never rendered; PDF rendered with `-layout` | q0/q1 exact @4625/@761; all 3 locate in reading order @4119/@4457/@11760 |
| R57W1ReviewQuarMethod | register S120 (`.docx`) | `.txt` sidecar is zip bytes (`PK\x03\x04`) | 3/3 exact @8996/9020/9428 — **PRESENT**, re-verified by me |
| R57W1QuarA | register S080, S082, S084, S088 | register checker re-joined the page's own list/table rendering | S080/S084/S088 **PRESENT**; S080's quoted string occurs **0** times in the cited `std.samr` capture but **exactly once** in sibling `b9ca2a4f…` @13300 (lane S122, the `openstd.samr.gov.cn` page) — the register row cut one page's rendering and cited another page's URL |

I re-verified batch A's S080 cross-capture claim (`标准号：GB/T 7714-2025` → 0 hits in `adf6ba934e813b2c326fa150.txt`, 1 hit in `b9ca2a4fdf9455867534f144.txt` @13300 = lane **S122** = `http://openstd.samr.gov.cn/bzgk/std/newGbInfo?hcno=…`), its anchor convention against `corpus/evidence/round54/build-spans.py:28-29` (span = quote + 80 chars context either side, so the quote begins at `offset+80`), and its landing claims (lane S098 @29482, S096 @3577, S123 @59201, S121 @477/537/1029/1048/1162/1797 — all land).

**C2 calibration datum on lane S121** (batch A's finding; batch A corrected it and I re-verified every
clause; reported, not patched). S121 is counted DRIFTED. What that does and does not mean:

* The pin `4e46154f…` was the deleted `.qcache` blob — not a git object, no file here hashes to it
  (`git cat-file -p 4e46154f4a84` → "fatal: Not a valid object name"). And there is **no pre-round-57
  lane capture blob** to compare against: `git ls-tree --name-only 6656f077 corpus/captures/ | wc -l` →
  **0** (the base tree's `corpus/` holds QUALITY/README/SOURCES/evidence/fixtures/knowledge/lessons
  only), so "the re-fetch matches the lane's committed blob" compares two round-57 fetches and proves
  nothing about page stability. (Batch A caught this in its own first draft; I had repeated it.)
* The live rendering **did** change slightly: `.raw` 76252 → **76273** B (+21); `.txt` on disk 6626 →
  **6650** B (+24); LF-normalised 3591 → **3599** chars (+8). (My earlier "5773 bytes" was the fresh
  LF-normalised byte count — a base mismatch; like-for-like the fresh file is **larger**.)
* The delta lies entirely **after** the last pinned quote: all six round-54 span slices are
  **byte-identical in place** at their recorded offsets (S121-1 @397, -2 @457, -3 @949, -4 @968,
  -5 @1082, -6 @1717 — each `fresh[off:off+len(span)] == span`, verified directly), and the last quoted
  character ends at char **1826** of 3599.

So DRIFTED here records that the whole-file digest differs from a pin whose bytes no longer exist on this
host **and** that the live rendering differs slightly in its tail — it does **not** mean any pinned quote
changed or is absent (`absent=0/6`, hence `FLAGGED=0/0`), the same distinction C2's own `absent=0/m`
flagging logic makes. `C2=PASS` unchanged.

## 6. Prose-class rows S100`-S103` — UNVERIFIABLE as classified (never fabrication)

| reg id | register class cell (the reason the register itself names) | cited-source cell | verdict |
|---|---|---|---|
| S100` / S101` / S102` / S103` | "the gate block named no locator, so no quote was checked" | `#### Gate — S100` / `— S101` / `— S102` / `— S103` | **unverifiable** (all four) |

Corroboration: register lines 269–272; the campaign's lint JSON (`quote-lint-full-v5.json`) carries `{"lane":"chousa","round":"round3","id":"S100","verdict":"no-locator","detail":"#### Gate — S100"}` — the verdict is literally `no-locator`, not `ABSENT`. The cited-source cell holds a **gate heading, not a locator**, so there is nothing to fetch; each id also carries a stray trailing backtick (`S100\``), a malformed id. The lane's own gate tool agrees (`tools/quarantine-check.py verdict --cache corpus/captures` → all four `unverifiable`: "register unchecked family (the gate block named no locator, so no quote was checked): the quote was never checked; not a fabrication"). No quote of theirs was ever checked, so no fabrication verdict is available. Note the lane's own S100–S103 rows (zcmu / hit / toho / um) are *different documents* (lane S100/S101 hold register rows S095/S096's URLs) — no identity.

## 7. Cross-check against batch C

Batch C's item assigns S116 with "the committed form is what matters; record whether the archive snapshot content itself contains the quote" — that is the **lane**-namespace S116 (web.archive PRISMA), answered in §4: **PRESENT**, all four lane anchors land (5328 chars, `93558b6d4b0e`, REPRODUCED). The **register**-namespace S116 (aclanthology) is answered in §3/§5; batch C must not read §5's "quotes are in the document" as a licence to skip the `-layout` check, since the committed defined form does not contain them.

## 8. Risks / blockers

* **Namespace ambiguity is a wave-wide hazard**, not local to batch D: a seat that resolves "S125" in `corpus/SOURCES.md` (as the item texts do) audits a different document from the register row it must adjudicate. Batches A–D all carry this; the L1 should state one registry per row id.
* The lane's gate tool still refuses to render OLE/zip (`quarantine-check.py` verdict: "binary office document decoded as bytes, never rendered to text" for S095/S096/S120/S125), so its table cannot see the quotes `tools/capture-text.py` renders. Tool-coverage gap, reported not patched.
* 18/20 register payload-absent URLs have a committed capture in the new store; register **S077** and **S086** have none (URLs absent from the lane registry) → `unverifiable`, no capture, batch A's rows. Flagged, not adjudicated here.
* No egress: only committed bytes under `corpus/captures/` were read; `pdftotext` ran on a **committed `.raw`** copied into scratch. No tool was installed or upgraded (none needed).

## 9. Boundary

Only file written: this report. Lane `git status --porcelain` shows no modification by this seat (only the L1's `refetch.tsv` and other seats' wave reports); fleet root unmodified (0 lines); `shokuknow` unmodified by this seat. Scratch `/fast/scratch/hyaku/chousa-r57/R57W1QuarD/` (608 KB) deleted before yield per the round's scratch directive (`trap 'rm -rf -- "$S"' EXIT`); a second short-lived `R57W1QuarD2/` for the S120 re-verification also removed.

**VERDICT: the quarantine hand-check (batch D) — the slice re-derives to 24 rows (20 payload-absent + 4 prose) as claimed; the four prose rows survive as UNVERIFIABLE-as-classified with the register's own reason; register rows S125 and S116 do NOT survive as fabrications (their quotes are present in the committed source bytes once the OLE `.doc` is rendered and the two-column PDF is read in reading order), while the lane-namespace S125/S116 survive as PRESENT with every recorded anchor reproduced; no edits.**

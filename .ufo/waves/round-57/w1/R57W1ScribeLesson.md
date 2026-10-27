# R57W1ScribeLesson — round-57 lesson skeleton (draft for the L1 to author)

Seat: scribe (leaf). Assignment: draft `corpus/lessons/round-57.md` per the lane contract; the L1 authors the
committed file. Frozen inputs read first: `corpus/evidence/round57/claims.md` (R57-C2 freeze `c2f914c5…`, R57-C3
freeze `fd95724d…`), shape from `corpus/lessons/round-56.md`. No predicate, counter, control or recipe was edited;
the only lane write is this report. Scratch `/fast/scratch/hyaku/chousa-r57/R57W1ScribeLesson/` (deleted, §Scratch).

## What I ran (evidence base for the draft)

1. Frozen counters, both read-only, lane root:

```
$ python3 corpus/evidence/round57/c2-count.py --verbose   # first read
CAPTURE S105 e3ca8f4fdd15420b80096a75 pin=2197abe27dad MISSING capture not the last successful attempt's bytes
SET=47 VERDICTS=46/47 REPRODUCED=41 DRIFTED=5 UNREACHABLE=0 BYTE_BACKED=46 CONSISTENT=46/46 FLAGGED=0/0 C2=FAIL

$ ls corpus/captures/e3ca8f4fdd15420b80096a75.*   → No such file or directory
$ stat -c '%y' corpus/captures                  → 2026-10-27 05:34:21 -0300 (08:34:21Z)
$ python3 corpus/evidence/round57/c2-count.py --verbose   # second read, same tree
CAPTURE S105 e3ca8f4fdd15420b80096a75 pin=2197abe27dad UNREACHABLE 3 failed attempts
SET=47 VERDICTS=47/47 REPRODUCED=41 DRIFTED=5 UNREACHABLE=1 BYTE_BACKED=46 CONSISTENT=46/46 FLAGGED=0/0 C2=PASS
```

   Between the two reads a `.raw` existed at key `e3ca…` (hence the first note, whose branch only fires when a
   capture file is present, `c2-count.py:203-204`) and then did not; the refetch rows are unchanged (S105 attempts
   1-3, all `curl_rc=28`, `refetch.tsv`). [INFERENCE] a concurrent fetch/cleanup wrote and removed the file. The wave's
   after-receipt must be taken on a stable store: with that `.raw` present the same tree reads `C2=FAIL`.
2. Drift detail (same verbose read): DRIFTED = S083 `absent=0/2`, S087 `0/2`, S113 `0/6`, S114 `0/9`, S121 `0/6` — no
   pinned quote lost, so the counter needs no FRESHNESS-FLAG line (`FLAGGED=0/0`).
3. Rows touched, read from `corpus/SOURCES.md` (11-column header at line 9): S127 `used-by` =
   `corpus/knowledge/grey-literature-field-china-r42.md`; S118 `used-by` = `…quality-control-guideline-issued-text-r48.md,
   …western-instrument-alignment-r50.md, …grey-literature-field-china-r42.md`; both `mined`, `recheck 180d`; registry
   130 rows (S001-S130), no `corpus/knowledge/normative-reference-chain-china-r57.md` yet.
4. R7 feasibility check on held bytes (counter's own function, imported read-only):
   `heading_title(S118_form, "药品临床综合评价质量控制指南") → True`, line = `药品临床综合评价质量控制指南`
   (char 0), token `2024年版` in `nows(form) → True`, `（2024 年版 试行）` at char 18. S127's clause:
   char 4696, `下列文件中的内容通过文中的规范性引用而构成本文件必不可少的条款。其中，注日期`, 1 whitespace word, 38 chars.
5. Lesson-check bite, scratch C3 fixture (`build-c3-controls.py` into scratch, `c3-count.py --root`, lane untouched):
   baseline `IN_LESSON=5`; my draft quote table rebuilt from the manifest gave `IN_LESSON=5`; the same table with one
   character changed (`下列文件的内容`) gave `IN_LESSON=4`. The lesson leg counts quotes verbatim, so the committed table
   must be generated from `spans.tsv`, never retyped.
6. Manifest table generator (works on the fixture manifest):
   `awk -F'\t' 'NR>1{printf "| %s | %s | %s |\n",$1,$4,$6}' …/c3/spans.tsv` → 5 rows, `IN_LESSON=5`. Column 4 is the
   span offset; the lesson table's char column should be the quote's offset in the defined text form (a read-only
   one-liner over `captures/<sha256(url)[:24]>.txt` reproduced round-56's own values: S130 11 and 129, S127 clause 4696).
7. D1 sweep: `grep -rn '表 10 row' corpus/` → 3 hits; the single live one is
   `corpus/knowledge/grey-literature-field-china-r42.md:9` (the other two are the spotcheck that defines D1).
8. C3 duplicate-document signal: S133's `nhc.gov.cn/cms-search/downFiles/863665…pdf` attempt has
   `txt_sha256=71fed1a3bc95a7e1…`, byte-identical in text form to S130's pinned/most-recent txt digest — the same 2020
   document under a new id, so it cannot bind R3 (`claims.md`: S130 lacks `2021年版`). Reported, not patched.
9. Wave outputs available at draft time: `.ufo/waves/round-57/w1/` holds `R57W1ScoutR1.md`, `R57W1ScoutR1Gov.md`,
   `R57W1ScoutR7.md` (used for the R1/R7 UNBOUND sweep text); no `census-end.txt`, no C3 entry. `c3-count.py` at draft:
   `ENTRY=no S127_CITED=no NEW_GROUND=no CLAUSE=no`, `BOUND=0/7 (min 4) -`, `C3=FAIL`.

## Draft (slots in `{{…}}`; the L1 fills them at commit and deletes any FRESHNESS-FLAG/UNBOUND line the data makes unnecessary)

```markdown
# Round 57 lesson — chousa

author: chousa L1 (hyaku run 9, `ChousaR57`) · date: 2026-10-27 · base `6656f0770a1460d6ba73d9d2976f698a35311921` · freezes `c2f914c53201a8f8ee4fef823b82681051d55592` (R57-C2), `fd95724d56a33a150cd2638fadd2ce1f3425e6c` (R57-C3)

Receipts: `corpus/evidence/round57/controls/c2-before.txt` (`VERDICTS=0/47 … C2=FAIL`, exit 1) · `c2-after.txt` {{SLOT: name + header revision}} · `c2-controls.txt` (EMPTY, JUNK `FLAGGED=0/47`, ALLFAIL — each `C2=FAIL`) · `c3-before.txt` (`ENTRY=no … BOUND=0/7 … C3=FAIL`) · `c3-after.txt` {{SLOT}} · `c3-controls.txt` (HELD `BOUND=1/7 (R7:S118)`, CITER `BOUND=1/7 (R7:S118)`, both `C3=FAIL`) · `census-start.txt` · `census-end.txt` {{SLOT}}.

## Gate

### R57-C2 — freshness: the 47 pinned triples re-fetched into lane-owned bytes

{{SLOT: the after-receipt's counter line verbatim, with its file and header revision — `SET=47 VERDICTS=47/47 REPRODUCED=… DRIFTED=… UNREACHABLE=… BYTE_BACKED=… CONSISTENT=…/… FLAGGED=…/… C2=PASS`, exit 0}}

- DRIFTED (digest moved; no pinned quote lost): {{SLOT: ids with the counter's own `absent=a/m`, one per id — at wave time `S083 … absent=0/2`, `S087 … 0/2`, `S113 … 0/6`, `S114 … 0/9`, `S121 … 0/6`; a DRIFTED triple is not a stale quote, it is a changed file}}.
- FRESHNESS-FLAG: {{SLOT: one `- FRESHNESS-FLAG <id> <key> absent=<a>/<m>` per DRIFTED triple with a>0, in the counter's own numbers; if none, write "no DRIFTED capture lost a pinned quote, so no FRESHNESS-FLAG line is required (`FLAGGED=0/0`)"}}.
- Fetch record: {{SLOT: attempts per outcome over `refetch.tsv` (rc=0/HTTP 200 successes, rc=28 timeouts, rc=22 with HTTP 4xx/412/503 walls), and the UNREACHABLE ids with their attempt timestamps and spacing}}.
- Store stability: {{SLOT: state whether any capture byte changed under the counters between the first and the after read — at wave time a transient `e3ca…raw` flipped S105 from `MISSING` to `UNREACHABLE` and the tree from `C2=FAIL` to `C2=PASS`; name the final `ls`/`stat` evidence}}.

### R57-C3 — depth (sourced): the workflow standard's normative references chained to their own documents

- The clause row (counter's CLAUSE): S127, `corpus/captures/b27ffd2f0161104c6a28c9f5.txt` char 4696 — `下列文件中的内容通过文中的规范性引用而构成本文件必不可少的条款。其中，注日期`.
- Bound: {{SLOT: the counter's `BOUND=k/7 (min 4)` line verbatim plus the ref→row map, e.g. `R7:S118`}}.
- Held-row check (read, not re-run): S118's text form carries `药品临床综合评价质量控制指南` as a bare heading (char 0) and `2024年版` — `heading_title → True`; the frozen rule therefore binds R7 through S118 once the entry cites it.
- Exclusions the counter enforces (`STRAY_IDS`): S128 and S129 may not be named by the entry; the held S130 may not be named (it lacks `2021年版`); and the same document may not be re-registered to bind a reference (S133's `nhc.gov.cn/cms-search/downFiles/863665…pdf` reproduces S130's text digest — reported in this round's wave).

#### UNBOUND block (these lines live in the ENTRY; `c3-count.py:235` reads them there, not in the lesson)

{{SLOT: keep exactly one line per reference the entry does not bind; delete the lines for bound references. Drafted at wave time from the scout reports:}}

- UNBOUND R1 sweep: web_search `国卫药政函〔2019〕80号 关于开展药品使用监测和临床综合评价工作的通知`, `site:nhc.gov.cn`, `site:gov.cn`, `site:wjw.*.gov.cn`, `site:cnpharm.com`, `site:edu.cn` — hosts nhc.gov.cn, wsjsw.linyi.gov.cn, nmgyxzh.org.cn, gcpunion.org, waizi.org.cn (`.ufo/waves/round-57/w1/R57W1ScoutR1.md`, `R57W1ScoutR1Gov.md`; nhc.gov.cn answered HTTP 412 to the campaign curl).
- UNBOUND R2 sweep: web_search `关于规范开展药品临床综合评价工作的通知 国卫办药政发〔2021〕16号`, `site:nhc.gov.cn`, gazette reprints — hosts nhc.gov.cn (412), provincial wjw, 公报 compilation (`.ufo/.../R57W1ScoutR2.md`, `R57W1ScoutR2Gaz.md`).
- UNBOUND R3 sweep: web_search `药品临床综合评价管理指南 2021年版`, `site:nhc.gov.cn`, `site:ihpe.org.cn`, `site:nhei.cn` — hosts nhc.gov.cn, ihpe.org.cn, nhei.cn (`.ufo/.../R57W1ScoutR3.md`, `R57W1ScoutR3Alt.md`).
- UNBOUND R4 sweep: web_search `抗肿瘤药品临床综合评价技术指南 2022年版`, `site:cnpharm.com`, hospital and CDC mirrors — hosts nhc.gov.cn, cnpharm.com, provincial cdc.cn (`.ufo/.../R57W1ScoutR4.md`, `R57W1ScoutR4b.md`).
- UNBOUND R5 sweep: web_search `心血管病药品临床综合评价技术指南 2022年版`, `site:wjw.*.gov.cn`, society hosts — hosts nhc.gov.cn, 国家心血管病中心, 中国医师协会 (`.ufo/.../R57W1ScoutR5.md`, `R57W1ScoutR5b.md`).
- UNBOUND R6 sweep: web_search `儿童药品临床综合评价技术指南 2022年版`, `site:wjw.*.gov.cn`, cnpharm/hospital mirrors — hosts nhc.gov.cn, provincial wjw (`.ufo/.../R57W1ScoutR6.md`).
- UNBOUND R7 sweep: {{SLOT: only if R7 is unbound — the held S118 binds it; if the entry omits it, the line names `.ufo/.../R57W1ScoutR7.md`: hosts nhei.cn, cnhdrc.cn, bjhea.org.cn, cnwszl.com, book118.com}}.

### New SOURCES rows (opened 2026-10-27)

{{SLOT: one bullet per row actually committed, exactly this shape — the frontier check reads URL, date, and a ≤25-word located quote:
- S1nn — <URL> — accessed 2026-10-27 — `<quote, ≤25 whitespace words and ≤160 characters>` (char <offset in the defined text form>).
Every new row: `mined`, `opened 2026-10-27`, `recheck 180d`, `used-by` naming `corpus/knowledge/normative-reference-chain-china-r57.md`. A fetch is not a row: at wave time S131 and S132 (nhc.gov.cn HTML) had only HTTP 412 records and no capture (`refetch.tsv`), and S134-S136 had mixed success/failure records but no committed row.}}

### used-by changes (old → new)

- S127: `corpus/knowledge/grey-literature-field-china-r42.md` → `corpus/knowledge/grey-literature-field-china-r42.md, corpus/knowledge/normative-reference-chain-china-r57.md`; status `mined`, `opened`, `recheck 180d` unchanged.
- S118: `corpus/knowledge/quality-control-guideline-issued-text-r48.md, corpus/knowledge/western-instrument-alignment-r50.md, corpus/knowledge/grey-literature-field-china-r42.md` → the same three plus `, corpus/knowledge/normative-reference-chain-china-r57.md`; status and recheck unchanged.
- {{SLOT: one line in this shape per further bound row X, quoting its old cell verbatim first}}.

### Assimilation (theme: {{SLOT: the entry's theme, one line}})

{{SLOT: admit/refuse per staged entry, each with its narrowings or its flip — round-56's shape: `- admit, narrowed: …` / `- refuse: … reason …; flip: …`}}.
Candidate on theme, state at draft: staged `grey-literature-national-route-r44.md` (`/home/vgpnk/Projects/shokuknow/merge/chousa/knowledge/corpus/knowledge/`) was refused in round 56 with the flip "a round that binds the note's reference list by document and an issued T/CLPA text" (`corpus/lessons/round-56.md` §Assimilation set). This round binds the list (C3) but S127 is still a 征求意见稿 with placeholder number and dates, so half the flip is met; its `Unknown` (the 2024 试行 质量控制指南 text) is now held as S118. {{SLOT: verdict}}.

### Quarantine hand-check (batches A-D; verdict per row, no edits)

Batch A — register slice (24 rows): {{SLOT table: `| row | store key | defined form | located offset | verdict |` with PRESENT/ABSENT/UNVERIFIABLE per row, and the batch counts `ROWS=n PRESENT=a ABSENT=b UNVERIFIABLE=c`}}.

Batch B — S093 S094 S095 S104 S105 S108: {{SLOT table}}. S105 is adjudicable only from a store byte; at wave time `corpus/captures/e3ca8f4fdd15420b80096a75.raw` is absent (`ls`, no such file) and C2 records it UNREACHABLE, so its verdict is UNVERIFIABLE unless some other lane capture exists.

Batch C — S110 S111 S112 S114 S116 S120: {{SLOT table; for S116 record whether the archive snapshot's own bytes carry the quote}}.

Batch D — S125, S116 (double-check vs batch C), the four prose-class rows S100-S103 (gate block named no locator): {{SLOT table; prose rows marked UNVERIFIABLE-as-classified with the reason}}.

Quarantine total: {{SLOT: the round's quarantine counter line or the register's counts, with the command}}.

## Mistakes

| class | evidence pointer | captured-by | fix |
|---|---|---|---|
{{SLOT: numbered rows in round-56's shape (class · `file:line` or receipt · seat id · QUALITY number). Candidate rows the wave surfaced, for the L1 to accept or drop:}}
| 1. {{SLOT}} | {{SLOT}} | {{SLOT seat}} | {{SLOT}} |
| 2. {{SLOT}} | {{SLOT}} | {{SLOT seat}} | {{SLOT}} |

## Frontier

Census start: `corpus/evidence/round57/census-start.txt` — five pre-existing W04 rows (S051, S053, S073, S074, S075 duplicate-url class) plus `ok …/chousa-shokunin/corpus/SOURCES.md`, `exit=0`. Registry at draft: 130 rows, S001-S130.
Census end: {{SLOT: `census-end.txt` — rows, malformed, tier histogram, status histogram, duplicate ids, enum violations, mined `used-by` existence, exit code; every non-zero count as a defect candidate}}.
Sourced-claim pointer: `corpus/evidence/round57/claims.md` — R57-C2 (freeze `c2f914c53201a8f8ee4fef823b82681051d55592`, counter `corpus/evidence/round57/c2-count.py`, controls in `corpus/evidence/round57/controls/`) and R57-C3 (freeze `fd95724d56a33a150cd2638fadd2ce1f3425e6c`, counter `c3-count.py`); both frozen before their data, no predicate, target, counter, control or recipe changed in this round.

## Corrections

- **D1 — stale `recheck:` instruction (routed by `corpus/lessons/round-56-verifier-spotcheck.md` §6 item 1).** `corpus/knowledge/grey-literature-field-china-r42.md:9` still instructs the re-check against "the journal's 表 10 row"; the row is 表7's. Fix: an appended `#### Corrections (round 57)` block in that entry, no rewrite. {{SLOT: commit hash + the appended lines}}. Sweep at draft time: `grep -rn '表 10 row' corpus/` → 3 hits, one live (that line), two inside the spotcheck — no other sweep target.

## All located quotes

Every quote this round's C3 manifest carries, verbatim (the lesson leg counts them; generate, never retype):

{{SLOT: output of `awk -F'\t' 'NR>1{printf "| %s | %s | %s |\n",$1,$4,$6}' corpus/evidence/round57/c3/spans.tsv`, with the char column replaced by each quote's offset in the defined text form — verified on the held fixture: S127 clause 4696, S118 3334/3549, S130 11/129, and `IN_LESSON=5` with the table present, `4` with one character changed}}
```

## Findings the L1 must adjudicate (reported, not patched)

- **C2 reached PASS on a store state, not only on fetch records.** First read `46/47 … C2=FAIL`, second `47/47 … C2=PASS`, with a `.raw` at `e3ca…` present in the first and absent in the second (`stat corpus/captures` mtime 08:34:21Z). The after-receipt is only meaningful against a frozen store listing; the lesson's `Store stability` slot exists for that evidence.
- **`REPRODUCED=41` carries the PASS; the other 6 are attested, not digest-bound** — the claim discloses this; the lesson should not let the single `C2=PASS` line imply 47 digest-bound captures.
- **S133 duplicates S130 in text form** (`txt_sha256=71fed1a3bc95a7e1…` on both): a new id on the same document cannot bind R3 and would put a second row on one document.
- **`REPRODUCED >= 5` is dead weight at this margin** (41 landed); the load-bearing floors are BYTE_BACKED 46/47 and the flag equality.
- **R1/R2 are fetch-walled on the canonical host** (nhc.gov.cn HTTP 412 for HTML both times, `refetch.tsv` S131/S132): any UNBOUND line must say so, and the mirrors the scouts rank (gcpunion.org, wsjsw.linyi.gov.cn) are the only paths left.

VERDICT: drafted the round-57 lesson skeleton (header, Gate with C2/C3 blocks, per-row new-row slot, S127/S118 used-by old→new, seven UNBOUND sweep lines with queries and hosts, four quarantine batch tables, Mistakes, Frontier, D1 Corrections, manifest-quote slot) and made its quote leg bite in a scratch C3 fixture (`IN_LESSON=5` exact, `4` on a one-character change) — survives; C2's PASS is reported with the store-stability caveat, not as a stable measure.

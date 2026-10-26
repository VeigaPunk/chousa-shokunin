# R52W2CritGateDecisions — the lesson's `### Decisions` table, re-opened

Seat: `R52W2CritGateDecisions`, leaf (no subagent dispatch). Lane: `/home/vgpnk/Projects/shokunin/chousa-shokunin`.
Only write: this file. Scratch `/fast/scratch/hyaku/chousa-r52/R52W2CritGateDecisions`, removed at exit.
Tooling: no installs (operator rule read; nothing needed). Skill: `/skill:godspeed` (axes: capture re-open, flip staleness, province-dressing, admit repairs).
Forms: all offsets/counts below are in the canonical text reading used by the lane (default text mode, universal newlines), except where stated. I first read raw bytes and got offsets off by CRLF counts; in text mode every table number reproduced exactly. Captures are the read-only qcache; no fetch.

## 0. Method
Re-opened every refuse/admit-later row's capture behind its cited string, re-ran each flip condition against the cache, and re-read the three admitted entries against the repair each admit cell names. Commands below are what I ran (observed output after `→`).

## 1. Refuse rows — capture re-open

**r36 `search-log-fields-r36` (S082/S083/S090) — AGREE, capture call, flip still open.**
- `01f657b3d0ab045c494b3f92.txt` = 265 chars, head `Client Challenge … A required part of this site couldn't load` ✓.
- `14aaa168a5cb4d833ca78b0b.txt` 210,708 chars, `c9d1e74c3ac8d9eb332c9770.txt` identical 210,708 ✓.
- `02b3b0e812df68ca305c7bc3.txt` 3,542 chars, `参照` 0 ✓; PDF `58b1b5641ed80c3554e73727.txt` 6,242 chars, `参照` 11, `著者名（出版年）．文献名．URL（参照日）` once at 3785 ✓.
- Cache-wide: `copied and pasted exactly as run` 0/2,549 `.txt` ✓; newest capture `a190e843af842a48739defc5.txt` 2026-10-24 23:26:57 ✓; `SOURCES.append.md:15` still names `_article/-char/ja` ✓.
- Flip conjunct 1 (PRISMA-S full text with item 8 present): scanned all 8 files mentioning `PRISMA-S` — S134 JMLA (27), S111 portal (15), Cochrane ch.4 ×2 (11 each), SinoMed (6), and three misc (2/1/1: a Japanese SR-methods guide, a scoping-review reference list, an LLM paper). None is the PRISMA-S statement/checklist text; no `item 8`/machine-learning items appear in any. Conjunct still unmet, refusal not stale. **Weak point worth carrying:** the reason's premise that PRISMA-S "item 8" is the search-strategy item is unverifiable on disk (the statement's full text is absent); the flip's own first conjunct is the fix, so no decision change — noted, not blocking.

**r37 `chinese-search-log-r37` (S102/S103/S104) — AGREE, not a province call.**
- S102 `.txt` 17,317 chars, `专业检索` first at 3764 (3×); S103 8,590 chars, `文献溯源` first at 778 (2×); S104 68,091 chars, `护士进修杂志` first at 62 (4×) ✓.
- Twin-id: lane `corpus/SOURCES.md:112-113` URLs byte-identical to `SOURCES.append.md:27-28` (same two URLs character for character) ✓.
- Superseded: lane S114 (staged S112) carries `检索或查询日期` once at 1719 ✓ — the lead finding no longer stands. Flip (dated superseded appendix, S102/S103 held) is a re-entry form, not an admission trigger; not stale.

**grey-r40 — AGREE; the row is *openly* a province call, not dressed as capture.**
- `bdff491a75c6abeda1d9c01d.raw` head `d0cf11e0a1b11ae1` (OLE) ✓; `.txt` 241,510 chars, `灰色文献` 0; raw decoded UTF-16LE = 121,964 chars, `灰色文献` 7× (first at 53777), `检索策略` 11× ✓. `27d4865f201e99c1fed9f79b.txt` 1,673 chars ✓.
- S133 = S111: `SOURCES.append.md:36` and `:58` are the same medsci URL → one key ✓. C2 predicate (`claims.md` 67-82) "exactly one lane Registry row whose FIRST source-cell URL is the document's URL": verified each of the four bound URLs occurs in exactly one lane row (S113/S114/S115/S116) ✓, so an appended S133 would break it — the twin-id half is real, not province-dressing.
- Province half: the 2019 NMPA guideline's currency is NMPA/legal ground; no lane knowledge file and no wave-1 seat settles it (w1 grep: `R52ScoutPackageRest` F-group = "out of province for the spine"; `R52ReviewProvince` = same). Flip still open; not stale.
- Field claim already held: `chinese-search-record-r39.md` cites `灰色文献的检索与记录` (S109), which occurs once at 15310 in its capture (`fd468a36d78ff156b6200946.txt`) ✓.

**grey-r41 (S142) — AGREE, with one internal inconsistency to carry.**
- Staged file: 2,253 chars, 2 backtick spans, 0 double-quoted spans ✓ (so no staged claim had a located quote).
- Flip conjunct 1: no full-text copy. `be6963bbc94761282fea066e.txt` 19,351 chars; definition sentence `灰色文献是指未在同行期刊上公开发表的文献` once at 7176 ✓. Title page `eecde7d7993b1ee223ef28eb.txt` 5,553 chars, `灰色文献` 0; its `.raw` (370,113 B) holds the DOI 8× in HTML meta/links but no definition sentence, no `OpenGrey`, no body ✓. DOI `10.12290/xhyxzz.2023-0418` 0 in all 2,549 `.txt` (1 hit in that title-page `.raw` only).
- **Inconsistency:** the row's province-fit cell says "in (methodological practice), but a conduct claim, not a record field", yet the flip admits on a full-text copy + located quotes alone. If the conduct-vs-field note were binding, a full text would not flip it; if it is not, the note is inert. Refusal outcome unchanged, but the flip should state which bar governs.

## 2. Admit-later row — flip offset defect

**r40 `search-tracking-record-r40` (S134) — AGREE with the table's stated reason, but the flip's char 935 is in the wrong coordinate space.**
- `0ae65ac01b93119d3c2f3fed.txt` 27,659 chars. `number of records identified from each information source`: count 1; **raw-file offset 1334**, whitespace-collapsed offset 935. The full quoted sentence `PRISMA-S also recommends reporting …` is 0 byte-exact (capture has `recommends\n       reporting`) and 1 collapsed — W1/L1's "char 935" is a collapsed-text coordinate, not an offset in the stated form. The bare span is contiguous at 1334, so the repair is feasible, but "re-cut … at char 935" will fail any `text.find`-based locator on the real file (at 935 sits mid-sentence text). Fix: state 1334.
- Body ids: lane S069 = GNU grep manual (`SOURCES.md:79`) ✓, lane S094 = COLING paper (`:104`) ✓, S130 has no lane row ✓; S114 did not exist at BASE_REV — the parenthetical "registry max S112" is now stale after this round's admits (S114 exists as the 中国全科医学 row), though the mispointing substance stands.
- C2 frozen by document at exactly three ✓ (`claims.md` predicate: three entries, four documents).

## 3. Admit cells — repair check

**S115 NIPH admit — AGREE (no repair named; flip conditions hold).**
- `tools/capture-text.py` on `3a8b45977cd111e45e3980a5.raw` → exit 0, 19,682 chars; `--locate 'SRにおける文献検索期間について明記する。'` → `LOCATED count=1 offset=8996`; `使用したデータベース` 9408 once, `使用した検索式` 9419 once; 19496/19521 once. Section 7 at 19496 is the outside-experts field only; searcher sweep (`検索者/検索担当/誰が/検索日/最終検索/灰色文献/PRISMA-S/検索戦略`) = 0 each, `検索式` 1, `文献検索期間` 2, `データベース` 4 — the entry's "no searcher" claim holds. Entry never quotes the `.txt` sidecar (states its 168,952 chars/72,117 U+FFFD); staged correction (joined `文献検索期間2015年1月から2018年10月まで` → count 0) verified.

**S116 admit — AGREE; the named repair is present.**
- Repair: recheck re-cut to break-free `用いたフィルターや制限も含め，` (641, once) and naming `検索戦略`. Entry source line names `項目7 検索戦略 (char 619)`; located-quote list includes 641; recheck quotes `完全な検索戦略` and the 641 span. Verified: `検索戦略` at 619 (row label, with `7` in the 番号 column) and 769; `完全な検索戦略` once at 766; `項目7` 0; the broken staged string 0. All lesson S116 quote offsets (0/475/508/555/592/641/753/815/996) reproduce exactly.

**S113/S114 admit — AGREE; the named repair is present.**
- Repair: refuse if the entry quotes S111's item-by-item text (abstract-only capture) or re-inherits the `chinese-search-log-r37` base pointer. The admitted entry declares the attachment unread (its `#### Unknown` prints `CNKI/中国知网/万方/维普/SinoMed` all 0 in S111) and its `adopted:` note removes the amendment relation to the refused base entry. S111: `PRISMA-S` 15×, first `16` at 2389, `paymentAmount` at 4178, `灰色文献` 0, `检索者` 0 ✓. S112: `检索或查询日期` once at 1719 ✓.
- SinoMed truncation: `42bac8830527d6f1bb125c49.txt` (2,065 chars) holds `并针对中文` once at 1024 then whitespace/nav — the `数据库等本土化应用挑战提出实践建议` clause is absent there and present in S111 (count 2) ✓.

## 4. Verdict per row
admit S115 AGREE · admit S116 AGREE (repair done) · admit S113/S114 AGREE (repair done) · refuse r36 AGREE (capture; flip open; item-8 premise unverifiable) · admit-later r40 AGREE (flip offset 935 is collapsed-space; raw is 1334) · refuse r37 AGREE (twin-id + superseded, not province) · refuse grey-r40 AGREE (openly province + real twin-id) · refuse grey-r41 AGREE (flip conflates scope and capture).

VERDICT: attacked the Gate decisions table — all five refuse/admit-later rows' captures re-open to the stated strings and flips (none stale; grey-r40 is an honest province call, grey-r41's flip mixes scope and capture; r40's flip offset is a collapsed-space coordinate, raw 1334), and all three admits carry their named repairs, so every decision stands as written with two flip-text corrections (r40 offset 1334; grey-r41 flip scope bar) to carry.

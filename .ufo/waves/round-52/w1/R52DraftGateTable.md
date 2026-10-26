# R52DraftGateTable — assimilation Gate decisions table, round 52 (draft)

Seat: `R52DraftGateTable`, leaf (no subagent dispatch). Lane: `/home/vgpnk/Projects/shokunin/chousa-shokunin`.
Base: `00f8c7f5272a1d98b6d34913985fa4537e00aaf9`; registry max id `S112`
(`grep -o '^| S[0-9]\{3\} ' corpus/SOURCES.md | sort -V | tail -3` → `S110 S111 S112`; `awk '/^\| S[0-9][0-9][0-9] /{n++}'` → `rows 112`).
Only write: this file. No production file, entry, row, index or jj state touched. Nothing installed.
Scratch `/fast/scratch/hyaku/chousa-r52/R52DraftGateTable` (held the NIPH text form and its `--locate` receipt), removed at exit.
No network, no fetch: every capture read below is the frozen campaign cache
`/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache/` (newest file in it: `2026-10-24 23:26`, so nothing arrived after round 51).

Read for grounding: `corpus/lessons/round-51.md` (`### Decisions` 59-71, quarantine 73-90, located quotes 92-139),
`corpus/lessons/round-51-verifier-spotcheck.md` §6 (100-105), `PROVINCE.md`, `corpus/QUALITY.md`
(criteria 6, 8, 30, 37, 76, 82 referenced below), `corpus/SOURCES.md:112-113`,
`/home/vgpnk/Projects/shokuknow/merge/chousa/MERGE-REPORT.md`, `SOURCES.append.md` rows 7, 8, 15, 27-29, 36-37, 45, 50, 54-59, 67,
and the five staged entries named in the table (`knowledge/corpus/knowledge/*.md`).
The three admitted entries are **not on disk yet** (`ls corpus/knowledge | grep -i 'niph-form-r52\|prisma-s-reception-r52'` → none),
so the table states decisions, not entry text.

## Drafted section — intended lane path `corpus/lessons/round-52.md`, under `## Gate`

```markdown
### Decisions (every unadopted staged entry in the search-record neighbourhood; W1 `R52DraftGateTable`, re-checked by the L1 against the rows it names)

Admitted by document as three lane files: `corpus/knowledge/japanese-search-record-niph-form-r52.md` (staged S125 → lane S115),
`corpus/knowledge/japanese-prisma-item-wording-r40.md` (staged S129 → lane S116),
`corpus/knowledge/chinese-prisma-s-reception-r52.md` (staged S111, S112 → lane S113, S114).
Two of the three carry a named repair below; each repair is a one-cell rewrite, not new research.
The package's other entries in the neighbourhood:

| staged entry | documents (S-ids) | capture on disk (key, size) | province fit | decision | reason | flip |
|---|---|---|---|---|---|---|
| `japanese-search-record-r38-amendment-2026-10-23.md` — NIPH half | S125 | yes: `3a8b45977cd111e45e3980a5` (`.raw` 178,056 B ZIP `.docx`; its `.txt` sidecar is ZIP bytes — 168,952 chars, `文献検索` 0, 72,117 U+FFFD — and is not a text form; `tools/capture-text.py` on the `.raw` prints 19,682 chars, exit 0) | in: a Japanese national institute's own reporting-form fields | **admit** as `japanese-search-record-niph-form-r52.md` | round 51 refused this half for capture form only, and the form now exists: `python3 tools/capture-text.py <raw> --locate 'SRにおける文献検索期間について明記する。'` → `LOCATED count=1 offset=8996`; `使用したデータベース` 9,408 and `使用した検索式` 9,419 occur once each in the same form; tier A and on disk | refuse again if the tool's text form stops reproducing 19,682 chars at its pinned revision, or if the entry quotes the `.txt` sidecar instead of the tool form (criterion 76) |
| `japanese-prisma-item-wording-r40.md` | S129 | yes at the archive: `e84bfe97808591d23fe3266f` (`.txt` 5,328 chars / 10,106 B; `.pdf`/`.raw` 343,301 B) | in: PRISMA 2020's own Japanese wording | **admit** (lane S116), one named repair | the negative holds — `検索者` occurs 0 times in the `.txt` — and the archived copy is on disk; but the r51 flip is only half-met: the row is labelled `検索戦略` with number 7 at char 619, and the recheck's own string `用いたフィルターや制限も含め，すべてのデータベース，試験登録，Webサイトの完全な検索戦略を記載する` occurs **0** times (the capture breaks that sentence across lines and spells `Web サイト`), as does `項目7` | admit only with the recheck re-cut to a break-free span (`用いたフィルターや制限も含め，`, char 641, once) and naming `検索戦略`; refuse if the archive capture changes or the repair is skipped (criterion 30) |
| `chinese-search-log-r37-amendment-2026-10-23.md` — reception half | S111, S112 | yes: `453d492becd9a2f4632cb8dd` (`.txt` 8,804 chars / 14,135 B; `.raw` 276,803 B) and `cacddf3bbf780a4c7582bb17` (`.txt` 6,179 chars / 11,676 B; `.raw` 88,313 B) | in: a Chinese reception of PRISMA-S, and a Chinese journal's own checklist | **admit** as `chinese-prisma-s-reception-r52.md` (lane S113, S114) | this is the r51 flip's second branch — `ground:` cites S111/S112 directly and drops the base pointer; S112 carries the per-source `检索或查询日期` at char 1719 (once), the strongest on-theme Chinese field evidence the base reading lacked; S111 is the reception record (`PRISMA-S` 15×, `16` at 2,389, `paymentAmount` at 4,178) | refuse if the entry quotes S111's item-by-item text — the capture is abstract-only (`灰色文献` 0, `检索者` 0) because the attachment is sold — or if it re-inherits the `chinese-search-log-r37` base pointer |
| `search-log-fields-r36.md` | S082, S083, S090 | S082 `01f657b3d0ab045c494b3f92` (`.txt` 265 chars = "Client Challenge"); S083 `14aaa168a5cb4d833ca78b0b` (`.txt` 210,708 chars; a second host `c9d1e74c3ac8d9eb332c9770` = `training.cochrane.org`, same 210,708); S090 `02b3b0e812df68ca305c7bc3` (`.txt` 3,542 chars, `参照` 0) while the article PDF is `58b1b5641ed80c3554e73727` (`.pdf` 506,589 B; `著者名（出版年）．文献名．URL（参照日）` at char 3785, once) | in: it is the field list itself | **refuse** | neither conjunct of the r51 flip cleared: a scan of 2,549 `.txt` files finds `copied and pasted exactly as run` **0** times, and the newest capture in the cache is 2026-10-24 23:26; and the S090 row's `source` cell still names `_article/-char/ja` (`SOURCES.append.md:15`), the landing page whose text form holds `参照` 0 times — so 2 of its 3 legs still cannot be re-opened from the row as written | a PRISMA-S full-text capture with item 8 present, plus S090's cell re-pointed to `_pdf/-char/ja` — the PDF is already on disk at `58b1b564…`, so the re-point costs no fetch; then admit with the Cochrane leg unchanged |
| `search-tracking-record-r40.md` | S134 | yes: `0ae65ac01b93119d3c2f3fed` (`.txt` 27,659 chars / 27,737 B; `.pdf` 252,991 B) | in: a tracking record's columns | **admit-later** | tier A, capture present, sentence located once at char 935 (`number of records identified from each information source`); but the entry's quoted form `PRISMA-S also recommends reporting the number of records identified from each information source` occurs 0 times byte-exact (the `.txt` breaks the line after `recommends`), so it cannot enter as a located quote unmodified; and r52's C2 is frozen by document at exactly three, this being a fourth | admit in any round whose frozen by-document set names it (or under a C2 re-freeze), with the quote re-cut to the break-free span at char 935 and the body ids re-pointed: lane `S069` is the GNU grep manual and `S094` a COLING paper, `S114`/`S130` do not exist (registry max `S112`) — criterion 82 |
| `chinese-search-log-r37.md` | S102, S103, S104 | yes: `7809d5114330a60527436b07` (`.txt` 17,317 chars / 30,277 B; `专业检索` 3,764), `02aefcf570a7108e699d0990` (`.txt` 8,590 chars; `文献溯源` 778), `3d7b23e68f13add5cfae634b` (`.txt` 68,091 chars; `护士进修杂志` 62) | in | **refuse** | superseded: its lead finding (no Chinese-language search-log specification found) is contradicted by this round's admitted `chinese-prisma-s-reception-r52`, whose S112 item 6 requires the `检索或查询日期` of every source (char 1719, once); and 2 of its 3 documents are lane rows already — `S102` and `S103` sit in `corpus/SOURCES.md:112-113` with URLs byte-identical to `SOURCES.append.md:27-28`, so re-appending them is the twin-id duplicate (spot-check §6.2 `held` label) | only as a dated appendix whose heading is marked superseded, with `S102`/`S103` labelled `held` and not re-appended, all body ids stripped, and S112's item 6 cited as the correction |
| `grey-literature-and-chinese-search-record-r40.md` | S130, S131, S133 | S130 `bdff491a75c6abeda1d9c01d` (`.raw` 243,929 B OLE `.doc`; the `.txt` 241,510 chars is not the text form — `灰色文献` 0 there; UTF-16LE decode 121,964 chars, `灰色文献` 7×, `检索策略` 11×); S131 `27d4865f201e99c1fed9f79b` (`.txt` 1,673 chars / 3,945 B); S133 `453d492becd9a2f4632cb8dd` = S111's key | **out of province for its spine** (a regulator instrument's currency); in province only for the field sentence | **refuse** | the spine question — whether the 2019 NMPA guideline is still current — is NMPA/legal ground (PROVINCE: out of province, report, never absorb) and r52 settles nothing about it; S133 and S111 are one URL (`SOURCES.append.md:36` and `:58`, both `…/guideline/show_article.do?id=23e481c0052069d3`) and therefore one key, so appending S133 while the reception entry rests on S111 gives two rows for one page — and would break the frozen C2 predicate's `exactly one lane Registry row whose FIRST source-cell URL is the document's URL` for the 梅斯医学 page (`corpus/evidence/round52/claims.md:67-82`); the field claim is already carried by `chinese-search-record-r39` (`灰色文献的检索与记录`, char 15310 of S109's capture, once) | unchanged: the owning lane settles the guideline's currency and S133 is dropped in favour of the S111 row; re-stage as a currency record, not a field record |
| `grey-literature-and-chinese-search-record-r41.md` | S142 | yes: `be6963bbc94761282fea066e` (`.txt` 19,351 chars / 36,792 B; `.raw` 319,547 B) | in (methodological practice), but a conduct claim, not a record field | **refuse** | as staged it carries 2 backtick spans and 0 double-quoted spans in 2,253 characters, so no claim has a located quote; and the flip's first conjunct is unmet — no full-text publisher copy is in the cache: the same article's title page exists at `eecde7d7993b1ee223ef28eb` (5,553 chars, `灰色文献` 0, body absent) and `10.12290/xhyxzz.2023-0418` occurs 0 times in 2,549 `.txt` files | a full-text primary copy in the cache plus the entry rewritten with ≥1 located quote per claim — the definition sentence `灰色文献是指未在同行期刊上公开发表的文献` is at char 7,176, once |
```

## Flip checks, with the commands and what they printed

Every check below is against the frozen cache; no capture newer than `2026-10-24 23:26` exists, so no capture-dependent flip can have cleared by arrival.

**r36 — `search-log-fields-r36` (flip: PRISMA-S full text with item 8 + S090 cell re-pointed).**
`python3 - <<'PY'` over `glob('*.txt')` (2,549 files) counting `copied and pasted exactly as run` → `0`
(the same scan: `copied and pasted` → 3 hits, all other documents: Cochrane ch.4 `14aaa168…`, Bramer JMLA XML `2cef078d…`, Cochrane training `c9d1e74c…`; `Reporting literature searches` → 0).
S082's leg is the challenge page: `01f657b3d0ab045c494b3f92.txt[:300]` → `Client Challenge … A required part of this site couldn't load`.
S090: landing `02b3b0e8….txt` → `参照 0 … len 3542`; PDF `58b1b564….txt` → `参照 11 … 著者名（出版年）．文献名．URL（参照日） ※参照日の記載は必須とする．` at 3785.
Row cell unchanged: `SOURCES.append.md:15` URL ends `…/105_17/_article/-char/ja`. → both conjuncts still open; **refuse** stands.

**r40 — `search-tracking-record-r40` (flip: entry set / C2 re-freeze; no capture work).**
`0ae65ac0….txt` char 935 = `number of records identified from each information source`, count 1; the entry's full sentence with `\s+` collapsed is also 1, but byte-exact is 0 because the capture has `also recommends\n       reporting`.
C2 is frozen by document at three (`corpus/evidence/round52/claims.md`), none of which is this paper. → **admit-later**, flip restated with the quote repair.

**r37 — `chinese-search-log-r37` (flip: dated superseded appendix).**
Lane/append URL identity checked by machine: lane `corpus/SOURCES.md:112-113` and append `:27-28` yield the same two URLs character for character.
S112's field line: `cacddf3b….txt` `检索或查询日期` count 1 at 1719. → lead finding refuted; **refuse** stands.

**grey-r40 (flip: owning lane settles NMPA currency).**
`453d492b…` reached from two append rows (`:36` S111, `:58` S133) — one URL, one key. Currency: no r52 seat touches it; r52's theme is search-record documents.
`.doc` form: `bdff491a….raw[:16]` = `d0cf11e0a1b11ae1`; UTF-16LE decode `灰色文献` 7, `检索策略` 11; the `.txt` sidecar `灰色文献` 0. → **refuse** stands.

**grey-r41 (flip: primary copy + rewrite with located quotes).**
Staged file counted: 2,253 chars, 2 backticks, 0 double-quoted spans.
`eecde7d7….txt` = the article's title page only (5,553 chars; `灰色文献` 0); cache-wide `10.12290/xhyxzz.2023-0418` → 0; the definition sentence in the mirror `be6963bb….txt` count 1 at 7176. → **refuse** stands.

**Admitted three.** NIPH text form: `tools/capture-text.py <raw> > niph.txt` exit 0, `len` 19,682; `--locate 'SRにおける文献検索期間について明記する。'` → `LOCATED count=1 offset=8996`; `文献検索終了時点` 9,020, `使用したデータベース` 9,408, `使用した検索式` 9,419, each once.
S129: `e84bfe97….txt` `検索者` 0, `検索戦略` 2 (619), `用いたフィルターや制限も含め` 1 (641); `項目7` 0.
S111/S112: `453d492b….txt` `PRISMA-S` 15, `16` at 2389, `paymentAmount` at 4178, `灰色文献` 0; `cacddf3b….txt` `检索或查询日期` 1 at 1719, `检索策略` 2 (1756).

## Findings for the L1 (repairs, not new research)

1. **Two admitted rows quote spans that do not occur byte-exact.** S129's recheck quote spans line breaks and differs in `Web サイト`/`Webサイト`; S134's (admit-later) sentence spans a line break after `recommends`. Both must be re-cut to break-free spans before any `char N` is written (criteria 30, 76). Suggested spans are in the table.
2. **S129's label.** The capture's row is `検索戦略` **7**; `項目7` occurs 0 times, so the r51 flip is met only in substance. Name the row, not the string.
3. **S133 = S111.** One URL, one key, two staged ids. The reception entry rests on S111; grey-r40's S133 row must not be appended (twin-id, spot-check §6.2).
4. **Staged-vs-lane id collision is wider than the spec's warning.** Staged S102/S103 duplicate lane S102/S103 *and their URLs*; staged S120 is the FEVER dataset while quarantine row S120 is the NIPH form; staged S125 is the NIPH form, not `S120`. Any adopter that carries staged ids over breaks three rows at once (criterion 82).
5. **Numeric drift carried from r51.** r51 records S131 as `.txt, 1,858` chars; the same file measures **1,673** chars today (sha-stable, mtime 2026-10-23 21:20). Re-derive before the round cites r51's cell (criteria 37, 76).
6. **The NIPH `.txt` sidecar is not a form.** 168,952 chars of ZIP bytes (21 `PK\x03\x04` headers, 72,117 U+FFFD). The only citable form is the tool's 19,682-char output; criterion 76 form-tagging must say so.
7. **A second Cochrane capture exists** (`c9d1e74c…` = `training.cochrane.org/handbook/current/chapter-04`, 210,708 chars, identical length to `14aaa168…`). Harmless for r36's refusal, but two keys now hold one chapter — the same one-page-two-keys pattern that blocks S133.

## Limits

- I did not run `c1-count.py` or `c2-count.py` and make no claim about their scores; other seats own those.
- I did not read the three admitted entries' text (not on disk at this seat's time) — the table's admit reasons rest on the staged entries and the captures, not on the new files.
- No capture was re-fetched; every flip judgement is against the frozen cache, so a flip that needs a *new* source cannot have cleared by construction, and I say so per row.
- The 5,553-char title-page capture `eecde7d7993b1ee223ef28eb` is identified by content only (journal nav + article title); its URL key was not recovered from the cache (no key→URL index under `.ufo/waves/corpus-expansion-1/`), so grey-r41's flip is stated as "full text absent", not as "publisher host absent".

VERDICT: drafted the round-52 Gate decisions for the search-record neighbourhood — 3 admits (NIPH form, S129 wording, Chinese reception) with two named quote/label repairs, 4 refusals (r36, r37, grey-r40, grey-r41) and 1 admit-later (tracking record) — after re-running every r51 flip condition on disk: no capture-dependent flip cleared, `copied and pasted exactly as run` 0/2,549 `.txt`, S133/S111 one key, and two admitted/held quotes fail byte-exact.

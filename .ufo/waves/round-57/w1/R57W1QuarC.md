# R57W1QuarC — quarantine hand-check, batch C (S110 S111 S112 S114 S116 S120)

Read-only seat. No lane edit beyond this report, no fetch, no git/jj mutation, no tool install (nothing
needed). Scratch `/fast/scratch/hyaku/chousa-r57/R57W1QuarC/` deleted before yield (`rm -rf`, verified).

## Namespace finding — read before using any verdict below

Register `S###` cells and `corpus/SOURCES.md` `S###` cells are **different id spaces**; no register id holds
its own number in the lane. The chousa slice rows sit at `absent-defect-register.md:50-55` = register S110
S111 S112 S114 S116 S120 (my batch). Mapping each register row by its cited URL to the lane row holding the
same URL: reg S110 (aclanthology 2025.coling-main.108) → lane **S094**; reg S111 (slarc EN id=5290) → lane
**S109**; reg S112 (slarc CN id=5237) → lane **S110**; reg S114 (sinomed ui=2026335073) → lane **S111**;
reg S116 (aclanthology N18-1074) → lane **S086**; reg S120 (niph .docx) → lane **S115**.

My item's parenthetical "*For S116 (web.archive.org URL)*" is the **lane** S116 — a different document from
register S116. Both readings adjudicated below. Decisive: as register ids all six rows carry quoted spans; as
lane ids, lane S112 (jahbs.info), S114 (chinagp.net), S116 (web.archive.org) and S120 (cochrane ch04) have
**no register row at all**, so "locate the register's quoted span" would be unexecutable for 4 of 6. Batch D
found the same collision independently. **The L1 must name the id space in the round-57 quarantine block** —
"S116 absent" reads against the wrong document otherwise.

## Method (recipe = batches A/B/D)

store key = `sha256(url)[:24]`; defined form = `.txt` sidecar, except an OLE/zip `.raw` → `tools/capture-text.py`
stdout, and a PDF → `pdftotext -layout` of the same committed raw (the frozen recipe). Quotes located by exact
`str.find` and by a whitespace-removed fold (`nws`), offsets in the defined form. Verdict vocabulary = the
round-51 rule: `present` / `absent-as-written` (a character or unrendered markup differs, substance located) /
`fabricated` / `unverifiable`.

Recipe equality, using the frozen `c2-count.py:recipe_txt` imported (not re-implemented): `recipe_txt(raw)`
bytes == committed `.txt` for **12/12** keys (`regS110…regS120` + lane S110 S111 S112 S114 S116 S120). My own
first re-implementation disagreed on the two HTML captures and the docx; the counter's function is
authoritative and agrees. Recorded so nobody repeats it.

## Register-namespace verdicts

| reg id | committed defined form | quotes in defined form | reading-order `pdftotext` of the SAME `.raw` | verdict |
|---|---|---|---|---|
| S110 | `-layout` `.txt`, 82,876 chars | **0/3** | Q1 @14060-14178, Q2 @15637-15754, Q3 @13719-13838 (nws) | absent-as-written; substance present |
| S111 | `-layout` `.txt`, 52,208 chars | **0/1** | @12634-12656 `报告规范，研究者可参\n\n考 PRISMA 框架` | absent-as-written; substance present |
| S112 | `-layout` `.txt`, 50,952 chars | **0/3** | Q1 @8450-8538, Q2 @8539-8574; **Q3 absent** | absent-as-written; Q3 spliced |
| S114 | html_to_text `.txt`, 1,675 chars | **0/2** | n/a (HTML) | absent-as-written; only in an HTML comment |
| S116 | `-layout` `.txt`, 60,030 chars | **0/3** | Q1 @4467-4586, Q2 @11785-11820, Q3 @4129-4248 | absent-as-written; substance present |
| S120 | capture-text, 19,682 chars | **3/3 exact** @8996, @9020, @9428 | n/a (docx) | **present** |

- **S110** `a9cf41709b6fa5028332d98c` `%PDF-1.3` 807,648 B: the defined text interleaves the two columns, so no
  register quote is contiguous (longest runs 64/104, 43/101, 42/104); reading order of the same committed raw
  finds all three after whitespace collapse. Rendering artifact, never fabrication.
- **S111** `fd468a36d78ff156b6200946` `%PDF-1.4` 1,156,890 B: reading order gives `…可参\n\n考 PRISMA 框架`; the
  register writes `PRISMA框架` unspaced, so one space differs while the sentence is on the page. Round 51
  reached the same substance verdict for this document via a DEINT form (`corpus/lessons/round-51.md:83`).
- **S112** `c7266931a1731db3ff6ae77d` `%PDF-1.4` 1,140,215 B: Q1/Q2 substance present (`WebofScience` vs the
  page's `Web of Science`). Q3 `实验动物与比较医学, 2025, 45(1): 101-111  DOI: …` is **stitched**: the page has
  `实验动物与比较医学` @18 (running head), `2025, 45(1): 101-111` @36176, `DOI: 10.12300/j.issn.1674-5817.2024.109`
  @35949 as reference entry `[70] … Med, 2025, 45(1): 101-111. DOI: …` — never as one string.
- **S114** `42bac8830527d6f1bb125c49` HTML 20,142 B, defined form 1,675 chars (Flash-dependent page: its text
  says `此页面上的内容需要较新版本的 Adobe Flash Player`). Both register strings occur **only inside an HTML
  comment**, raw bytes **9192–9910** (719 B) holding `学科分类号： R-05;R-37;R348.3;R916.3` and
  `主题词： *评价研究;*研究报告;Meta分析;*清单;质量控制`; `学科分类号` and `R-05` are 0× in the defined form. The
  five terms *are* rendered but as a separate list under `查看主题词相同的文献，请选择：` (~1100), no label, no
  semicolons. Round 51's "no entry may quote them as displayed text" holds on the fresh bytes.
- **S116** `1c15b611118dee97e4105fcf` `%PDF-1.5` 460,896 B: reading order locates all three (Q1 keeps the page's
  `evi-\ndence` split; my offsets differ from the peer's 4119/4457/11760 by the extraction step, not the bytes).
  Round 46 already adjudicated this row "present → adoptable" once the interleave is removed.
- **S120** `3a8b45977cd111e45e3980a5` `PK\x03\x04` 178,056 B — **the `.txt` sidecar is zip bytes; do not read
  it**. `capture-text.py` stdout locates all three exactly at 8996 / 9020 / 9428, reproducing round 52's
  offsets character for character. **present**; the register's `payload-absent` is wrong for this row.

## Lane-namespace check (the item's literal S116 + the other five)

The six lane rows own 56 pinned manifest rows at SET_REV (7/7/16/9/9/8). All 56 quotes occur **exactly once**
in the fresh committed defined forms. Span-slice test (`form[offset:offset+len]` vs the base `spans/*.txt`):
**54/56 byte-identical**; the 2 exceptions are lane S114 `S114-7.txt` / `S114-8.txt`, differing only in
`3452`→`3481` (the `浏览` counter) with the quoted spans untouched. Every `char N` in the six `SOURCES.md`
anchor cells still lands on its quote: S110 11110/11211/11404; S111 695/934/1138/1078/1366; S112
10140/10146/11229/11243/11294/11348/11457; S114 1650/1707/1785/5530; S116 475/592/641/753; S120
7432/9949/13480/35599/36552.

Lane S114 (chinagp.net `cacddf3bbf780a4c7582bb17`) is the batch's one DRIFTED triple: pin `b1c3cd6a…` matches
neither fresh `.raw` (`56c2f612…`) nor fresh `.txt` (`3006510c…`), and the entire content delta is the view
counter (`3452` count 0, `3481` count 1 in the fresh text; the base span slice holds `3452`). All 9 pinned
quotes still occur → `absent=0/9`, so no FRESHNESS-FLAG is owed (`c2-count.py --verbose`: `CAPTURE S114
cacddf3bbf780a4c7582bb17 pin=b1c3cd6a5c22 DRIFTED absent=0/9`; my run's summary `SET=47 VERDICTS=46/47
REPRODUCED=41 DRIFTED=5 UNREACHABLE=0 BYTE_BACKED=46 CONSISTENT=46/46 FLAGGED=0/0 C2=FAIL` — the FAIL is S105
`MISSING capture not the last successful attempt's bytes`, outside this batch).

**S116 archive snapshot — does the snapshot content itself contain the quote? Yes.** The committed
`e84bfe97808591d23fe3266f.raw` is `%PDF-1.6`, 343,301 B; `pdfinfo`: `Title: 表1`, `Pages: 1`,
`CreationDate: Tue Sep 19 02:06:00 2023 -03`, `Producer: Adobe PDF library 15.00` — the archived payload is
the publisher's own one-page PDF, not a Wayback wrapper. Its `pdftotext -layout` equals the committed `.txt`
byte for byte (5,328 chars, sha256 `93558b6d4b0e…` = the pin → C2 REPRODUCED). That snapshot text carries the
lane's quotes — `情報源` label @453, `検索戦略` label @619, quotes @475 / @592 / @641 / @753 — and the negatives
hold in the fresh bytes: `検索者` `検索担当者` `司書` `誰が` each 0×, `http`/`版`/`出版` 0×.

## Notes for the integrating seat (reported, not patched)

- Lane S111 and lane S114 each had two refetch attempts with **different `.raw` digests** (`a65d33c3…`→
  `956b9ff4…`; `fe77ace1…`→`56c2f612…`, the latter with a different `.txt` too). C2's CONSISTENT leg compares
  only the last successful attempt, so an earlier attempt's differing bytes are invisible to the counter.
  Nothing in my batch contradicts the frozen predicate.
- Peer `R57W1QuarD` answered register S116 (0/3 `-layout`, 3/3 reading order) and register S120 (3/3 at
  8996/9020/9428) independently; my numbers agree on substance and on all three S120 offsets.
- No register row in this batch is a fabrication: 5 are rendering/markup artifacts, 1 is present.

VERDICT: Attacked the batch-C quarantine rows in both id spaces and built their fresh-byte evidence — 6/6
register rows adjudicated with offsets (S120 present 3/3; the other five absent-as-written with substance
located, none fabricated), 56/56 lane pinned quotes still land in the fresh committed forms, the web-archive
S116 snapshot content itself carries the quote; every verdict survives the fresh bytes.

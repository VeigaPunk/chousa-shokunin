# R52W2ReopenRowS113 — wave-2 falsify: re-open Registry row S113

Scope: every cell of `corpus/SOURCES.md:123` (S113, medsci.cn portal record), its 6 manifest spans,
its one citing entry, and the frozen C2 binding conditions. Tooling authorization: nothing
installed or upgraded (nothing needed; PATH untouched). Lane repo untouched; scratch was
`/fast/scratch/hyaku/chousa-r52/R52W2ReopenRowS113` (empty, removed at end).

## Provenance chain (all holds)

- Cache key = `sha256(url)[:24]`: `sha256("https://www.medsci.cn/guideline/show_article.do?id=23e481c0052069d3").hexdigest()[:24]` → `453d492becd9a2f4632cb8dd` — equals the capture file name. `sha256(bytes)` of the capture → `ad6b09f0599c5820a4d283c953d07f457f3f540edcb5ebc3406e50ae571cdc52` — equals `capture_sha256` in all six `spans.tsv:2-7` rows. Capture is 8,804 chars / 14,135 bytes — equals the row's "8804 characters".
- Anchor arithmetic: every span file is `t[off:off+len(q)+160]` (verified byte-for-byte for all six), `span.find(quote)==80` for all six, so `offset+80` = the row's `char N`: 1954+80=2034, 2248+80=2328, 2353+80=2433, 3059+80=3139, 4770+80=4850, 7207+80=7287. Each quote occurs **exactly once** in the capture (`find_all` returned a single index each). Consistent with `build-spans.py` `CONTEXT = 80`.
- `python3 corpus/evidence/round52/build-spans.py --check` from the lane root → `SPANS_ROWS=38 STALE=0`, exit 0.
- `python3 corpus/evidence/round52/c2-count.py` → `C2=PASS` exit 0, `BOUND_IDS=S113,S114,S115,S116`, `ANCHOR_BOUND=4/4`, `ON_BOUND=38/38`, `SUBSTANCE=PASS`.
- Frozen binding conditions (claims.md:77-81) hold for S113: the medsci URL occurs in exactly one row (`count==1` in SOURCES.md); `git cat-file` at BASE_REV `00f8c7f` → 0 `| S113 ` rows, and spans.tsv / the entry do not exist there; status `mined`; `opened 2026-10-26`; `used-by` = exactly the entries with a `source: S113 ` line (`grep -l` → only `chinese-prisma-s-reception-r52.md:3`, which carries `source: S113 — https://…`).
- Freeze/landing integrity: `git diff --stat 37468ead..HEAD` on SOURCES.md / quotes.tsv / spans.tsv / the entry = the e769c03 additions only (+112, 0 deletions); `git log e769c03..HEAD -- <those files>` is empty. Erratum E1-E4 concern C1 tooling only — nothing post-freeze touches this row, entry, or manifest.

## Per-cell verdicts

- **source/title/URL — holds.** Capture `<title>` (char 51): `系统评价/Meta分析中文献检索报告清单（PRISMA-S）解读 -指南&解读指南-MedSci.cn`; record heading at char 2028; record object (char ~2680-2990) literally carries `id=23e481c0052069d3` and `guiderFrom=中国循证医学杂志` — the row's "portal record id" and "source journal" are in the capture body, not just the URL. First (only) URL is the capture's URL (key verified).
- **kind docs — holds.**
- **tier B — holds.** The page is a commercial portal's record of a journal article — carrier, not document; same article's SinoMed index record (S111) is also B; SKILL.md:28 states the primary>secondary>aggregator hierarchy is the lane's own construction, SKILL.md:37 scopes A/B/C per row. The row's own teaches cell concludes "a carrier of the abstract and a pointer to the text, not the text".
- **scope — holds.** Abstract block (char 2328/2433), dates (`发布日期： 2026-04-25` at char 2238; byline 2034; `guiderPublishedTime` 3139), attachment name (char 4850) — all in the capture. "Not the reading's item text": `条目` occurs 2×, both inside the abstract's `16个条目` phrase; no item enumeration. "Not the journal's own page": `http` occurs 1× (the `img.medsci.cn` cover), `originalUrl=, linkOutUrl=,` empty. Note: `商业` occurs 0×; "commercial portal" rests on the self-description `梅斯医学是面向医生的综合互联网平台…药械企业…精准数字化医学传播解决方案` (char 7287+) — defensible, but interpretation not capture vocabulary (F4).
- **anchor — holds with a gap.** All five listed `char N` are exact single-occurrence quote offsets. But the manifest has six S113 spans; the sixth (`S113-6`, portal self-description, char 7287) is quoted in the entry Observation yet absent from the row's anchor enumeration (F3).
- **teaches — one real defect.** The SinoMed-cutoff parenthesis is grounded (`chinese-search-record-r39.md:18`: abstract "breaks off mid-sentence after `并针对中文` (char 1024)"); "no original URL" holds; the author `郑卿勇` appears only inside filename strings (3×) and the record object's `author=` field is empty. But "carries the reading's abstract **to its last clause** on Chinese-database challenges" is false against the cited capture (F1 below).
- **status mined / opened 2026-10-26 / recheck 180d — holds.** Sibling-consistent (S111/S112 same values); the recheck's first step runs clean (`STALE=0` above).
- **used-by — holds.** Exactly one entry, exactly the row's value.

## Findings by severity

- **F1 (Medium) — the teaches cell's abstract boundary is falsified by the row's own capture.**
  `SOURCES.md:123` teaches: "carries the reading's abstract to its last clause on Chinese-database challenges"; entry `chinese-prisma-s-reception-r52.md:23` (Inference): "The portal record adds the abstract's last clause and nothing of the item text." The visible 简要介绍 block (chars 2264-2663) is A B C **D**: after C ends `…提出实践建议。` (ends char 2500; the complete C occurs exactly 2× — chars 2433 and 3540), the block continues with a further sentence at char 2500: `本文旨在为国内学者、期刊编辑及审稿人提供清晰、实用的PRISMA-S应用指引，以期提升我国SR文献检索部分的报告质量，促进SR研究的规范化与国际化。` (occurs 4×: chars 2084, 2500, 2914, 3619 — byline-area summary, the block, the record object's `summary=` field, the `content=` HTML copy). So the Chinese-database clause is **not** the abstract's last clause as this record presents it: relative to SinoMed the record adds C's tail **and all of sentence D** — D is even the record object's own `summary=` field. The Observation "carries the … abstract in full" (entry:15) is true; the boundary claims are not. The lane under-claims ground it holds — no fabrication — but the sentence a reader takes away ("the abstract ends at the Chinese-database clause") is wrong.
- **F2 (Low) — "names the article only as an attachment file" is loose.** The record names the article as its title four ways (`<title>` char 51, heading char 2028, `title=` field ~2737, plus filenames). The supported claim is that the article's **text** is present only as the attachment (author only inside filename strings; `author=` empty). Entry:16 same wording.
- **F3 (Low) — anchor cell lists 5 of 6 span offsets** (omits char 7287 / span `S113-6`). Manifest and entry are complete; the row's enumeration is not.
- **F4 (Note) — "commercial portal"** is the capture's self-description read as commerce (`药械企业`, `数字化医学传播解决方案`, `updatedBy=梅斯平台小助手`, APP promo), not a capture word (`商业` 0×).

## Draft rewording (for the L1; touches SOURCES.md:123 teaches cell and entry:23/:16 only — no frozen predicate, counter, control or target)

```text
# corpus/SOURCES.md:123 (teaches cell)
the portal record carries the reading's abstract in full — past the clause the lane's
SinoMed record cuts off (并针对中文数据库等本土化应用挑战提出实践建议。) through a further
closing sentence (本文旨在为国内学者…规范化与国际化。, also the record object's summary= field),
names the article's text only as an attachment file (the author appears only in the file name;
author= is empty) and gives no original URL, so it is a carrier of the abstract and a pointer
to the text, not the text

# corpus/knowledge/chinese-prisma-s-reception-r52.md:23 (Inference bullet, first sentence)
- **The portal record adds the abstract's tail past the SinoMed cutoff, not a last clause.**
  `S113` carries "并针对中文数据库等本土化应用挑战提出实践建议。" (char 2433), which the SinoMed
  record cuts off, and then a further sentence (char 2500) that is also the record object's
  `summary=` field; it lists the article as the attachment … and the lane can say the reading
  proposes practice advice for Chinese databases and cannot say what that advice is.
```

## Residual risk and verification gaps

- S111's capture was not re-opened; the SinoMed cutoff is taken from `chinese-search-record-r39.md:18` (lane state, that row is another seat's assignment). S114-S116, the lesson, QUALITY 87-90, README and the C1 counters are outside this seat's slice and were not attacked here.
- The entry's negative sweeps re-run clean on this capture: `检索者` 0, `检索人员` 0, `[CNKI,中国知网,万方,维普,SinoMed]` = `[0, 0, 0, 0, 0]`, `paymentAmount=10` present — so the Unknown section's three checkable claims hold.
- No lsp server was consulted (plain-text/markdown corpus; no semantic code references at issue).

VERDICT: attacked Registry row S113 end to end — provenance, all six anchors, tier, scope, status/recheck, used-by, frozen binding, and counter replay all hold, but the teaches cell's "abstract to its last clause" boundary is falsified by its own capture (a further sentence follows and is the record's summary field); the row survives a non-author re-open with one Medium fix (F1) and three wording gaps.

# QuarantineS080 — hand-check of chousa round1 `S080` (`payload-absent`)

**Verdict: ABSENT-AS-WRITTEN.** The register row stands. The quoted span is
demonstrably not in the captured source under any fold, and the reason is
specific: the quote was synthesized as a `label：value` line, while the page
renders those fields as separate `<dt>`/`<dd>` elements with no colons. This
is a real misquote (punctuation/rendering the source does not contain), not a
checker artifact.

## Register row (frozen)

`/home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-48/assimilation/quarantine-slice` line 2:
`S080   payload-absent`

`/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/absent-defect-register.md` line 38:
`| chousa | round1 | S080 | payload-absent | https://std.samr.gov.cn/gb/search/gbDetailed?id=4507EFE13D37CB6AE06397BE0A0A601F | 标准号：GB/T 7714-2025 发布日期：2025-12-02 实施日期：2026-07-01 |`

Row has a locator (https URL), so it is checkable — not the S100–S103 no-locator class.

## Lane SOURCES row and gate block

Census-time file: `/home/vgpnk/Projects/shokuknow/lanes/chousa/SOURCES-PROPOSED.md`
(the lane's round1 base; `rounds_of` maps the lane dir to `round1`,
quote-lint.py:658-665). IDs drifted across renumbering commits; at census time
(`quote-lint-full-v5.json`, 2026-10-24 08:05) this was `S080`; in HEAD the same
GB/T row is `S085` (line 38), gate block `#### Gate — S085` lines 71-77:

```
URL: https://std.samr.gov.cn/gb/search/gbDetailed?id=4507EFE13D37CB6AE06397BE0A0A601F
Quote — 基础信息: "标准号：GB/T 7714-2025 发布日期：2025-12-02 实施日期：2026-07-01"   <- the flagged span
Quote — 代替了以下标准: "GB/T 7714-2015 （全部代替）"                                 <- folded/whitespace in census
Quote — 采标情况: "本标准非等效采用ISO国际标准：ISO 690:2021。"
Quote — 采标中文名称: "信息与文献 参考文献和信息资源引用指南。"
```

`git log -p` on the file: `9e91e504` shows the quote under `#### Gate — S080`;
earlier commits number it S074/S077 — consistent with the register's `S080`.

## On-disk captures (the only evidence used; no fetch)

qcache key = `sha256(url)[:24]` = `adf6ba934e813b2c326fa150`
(`/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache/`):

- `adf6ba934e813b2c326fa150.raw` — 76,252 B HTML, fetched 2026-10-23 20:33,
  sha256 `a7b868be292a4c00a6cc1f56b1bd238549a468da4b03a9935b158523654f1409`
- `adf6ba934e813b2c326fa150.txt` — 6,626 B tag-stripped text (the match
  document), sha256 `4e46154f4a841d17d858eafb5c0099257030f301daadcaa30c37f2e668fb7138`

Capture content — `.txt` lines 366-377 (the fields the quote claims):
`标准号 / GB/T 7714-2025 / 发布日期 / 2025-12-02 / 实施日期 / 2026-07-01`,
each on its own line, **no colons** (`cat -A` shows only `\r\n` + spaces).
`.raw` lines 1133-1145 confirm the DOM: `<dt …>标准号</dt><dd …>GB/T 7714-2025</dd>`,
`<dt …>发布日期</dt><dd …>2025-12-02</dd>`, `<dt …>实施日期</dt><dd …>2026-07-01</dd>`.
Char-offset scan: `.txt` contains exactly 6 fullwidth `：`, all in the 采标情况
note, the footer (主管：主办：支持电话：备案号：) — none after 标准号/发布日期/实施日期.

## Reproduced check (read-only, cache only)

```
$ python3 → ql.match(txt, '标准号：GB/T 7714-2025 发布日期：2025-12-02 实施日期：2026-07-01')
None        # all 11 folds (exact, whitespace, case, no-whitespace, markdown,
            # nfkc, typographic, c-escape, de-wrapped, html, md-link) -> False
match on RAW: None
nfkc(q): 标准号:GB/T 7714-2025 发布日期:2025-12-02 实施日期:2026-07-01
flat (\\s+→' ') source region:
 基础信息 标准号 GB/T 7714-2025 发布日期 2025-12-02 实施日期 2026-07-01 全部代替标准 ...
```

Whitespace-collapsed source reads `标准号 GB/T 7714-2025 …`; the quote needs
`标准号：GB/T …` — every fold strips whitespace/markup, none can *insert* the
missing `：` separators. Census finding (quote-lint-full-v5.json findings[83])
reproduces exactly; findings[84] shows the sibling quote `GB/T 7714-2015
（全部代替）` DID match via whitespace fold → capture is genuine, not a
truncated/error page. Companion URLs: none generated (`docs` kind, no sibling
filenames, no `_article/`); local artifacts: none named (kind≠own-work).
The two 采标 quotes present in the same block verify verbatim in the capture
(.txt lines 468, 470), including the fullwidth colon after ISO国际标准 — the
source does use `：`, just not in the 基础信息 table.

## Reason

The gate author flattened a `<dt>/<dd>` definition list into
`label：value` prose. Every datum (number, both dates) is correct; the
synthesized colons make the contiguous span unfound. Verdict
**absent-as-written** — C1 survives this row: the `payload-absent`
classification is accurate. Recommended fix direction (not applied): quote the
fields as rendered (`标准号 GB/T 7714-2025 …` on separate lines) or mark the
colon form as a paraphrase outside the quote span.

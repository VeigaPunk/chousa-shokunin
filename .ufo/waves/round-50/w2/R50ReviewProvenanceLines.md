# R50ReviewProvenanceLines — round 50 wave 2 (falsify)

ATTACKS: the provenance trio (`source:`/`verified-at:`/`recheck:`) and anchors of the
three landed entries `corpus/knowledge/istic-citation-verification-r39.md`,
`cnki-citation-check-r40.md`, `citation-matching-semantics-r41.md`, against the rule
"A new knowledge entry opens with its provenance trio" (fleet `/home/vgpnk/Projects/shokunin/CORPUS.md:163-170`
— the lane itself has no `corpus/CORPUS.md`; `find` located only the fleet file).

## DEFECTS

### D1 (medium) — r39 `recheck:` asserts an output the checker never prints
`istic-citation-verification-r39.md:5` says the on-disk half
`cd …/chousa-shokunin && python3 corpus/evidence/round50/build-spans.py --check`
"must print `SPANS_ROWS=11 STALE=0`". Verbatim run:

    $ cd /home/vgpnk/Projects/shokunin/chousa-shokunin && python3 corpus/evidence/round50/build-spans.py --check
    SPANS_ROWS=55 STALE=0   (EXIT=0)

`build-spans.py:172` prints `SPANS_ROWS={len(lines)-1}` — the whole manifest total
(55 rows over 3 ids), not this entry's count. The asserted `11` equals the entry's
11 `source:` anchors (and its `verified-at:` "eleven quotes"), a count the tool has
no mode to emit. Consequence: a future 90d re-check run to the letter reports a
false stale event. `STALE=0` and exit 0 are correct; only the pinned literal is
wrong. Fix shape: assert `STALE=0` (optionally `SPANS_ROWS=55`), or drop the row count.

### D2 (minor) — r40 `recheck:` miscounts its own sweeps
`cnki-citation-check-r40.md:5` says "re-run the four sweeps in `#### Unknown`".
`#### Unknown` (lines 26-30) carries five distinct runnable commands: the
`未收录/匹配` pair, the four-word method list, the four-capture `grep -c 引文核对`
loop, the `未找到/无结果/无匹配` list, and the `诚信档案/科研/人事` list. All five
reproduce (below); whichever four a re-checker picks is ambiguous.

### D3 (minor) — r41 `recheck:` says "the three copies"; the entry cites two
`citation-matching-semantics-r41.md:6`: "then re-download the three copies". The
entry's bound documents are S105+S106 (two copies); "three" only makes sense as the
three adopted theme captures. Harmless to a reader holding the theme, ambiguous in
isolation; the clause is a future fetch directive (no network this round, L0
`8d77e6c1` open), so nothing present-tense is mis-asserted.

## SURVIVED (attacks that found nothing, with the commands)

- **Trio order**: all three open `source:` → `verified-at:` → `recheck:` as their
  first lines after the title (r39 lines 3-5, r40 lines 3-5, r41 lines 3-6); the
  CORPUS.md rule is satisfied, incl. "S### row alongside the URL and anchor".
- **Every `char N` in every `source:` line is a true UTF-8 quote offset in the
  named capture** (`.txt` read as UTF-8), and each maps to ≥1 `spans.tsv` row of
  that id+entry. Verified by script: all 27 source-line anchors located, 0 bad;
  e.g. r41 S105 `char 30738` = `引文核对是指，以“中国知网”的文献资源为核对源内容…`
  (row spans/S105-4), S106 `char 22511` = `在创建文件夹页面中第一个选项为“仅去除第一作者本人文献”…`
  (row spans/S106-2). r40 `char 48` = `更新时间：2020 年 7 月` (row spans/S105-14).
- **spans.tsv `offset` is NOT the quote offset — by design, not a defect.**
  `build-spans.py:44` `CONTEXT=80`, `:119` `start = max(0, off - CONTEXT)`;
  docstring: "`offset` is the span's start… `QUOTE <id> char <N>`, N = offset +
  the quote's position in its span, the value a Registry `anchor` cell's `char N`
  must equal". Confirmed: `t.find(open('spans/S105-15.txt').read())` = 30581,
  quote at span index 80, sum 30661 = `t.find('第 6 章 辅助功能')`. The uniform
  −80 (heads clamped to 0) vs entry `char N` is the context window. Peer
  R50ReopenRowS105 flagged then retracted the same pattern after self-verifying.
- **r41 `recheck:` runs verbatim from any cwd and prints what it claims** (ran
  from `/tmp`):

      38174 0 4 5 0
      30937 0 0 0 0
      30727 31262 535 [0, 0, 0, 0, 0, 0, 0, 0]

  Identical to the entry's asserted outputs.
- **r40's five `#### Unknown` sweeps all reproduce exactly**: `0 0`;
  `[0, 0, 0, 0]`; `e3ca8f4fdd15420b80096a75 4` / `28750… 0` / `275c… 0` /
  `001287… 0`; `[0, 0, 0]`; `[0, 0, 0]`.
- **r40's size/hash claims**: `.txt` 83,384 bytes, sha256 `2197abe2…`;
  `.raw` 4,482,989 bytes, sha256 `d36191c7…` — both confirmed by `wc -c`/`sha256sum`
  in `.qcache`. Capture mtimes 2026-10-23 (S104, S105) match "captured 2026-10-23".
- **`adopted:` names the package** in all three (`merge/chousa/`); r41's pointer to
  the staged-to-lane id map resolves: `corpus/lessons/round-50.md` `## Gate` exists
  at line 33 with the renumber map at line 39.
- **No credential material, no `op://`, no unbound S-token.** Token scan:
  r39 uses only `S104` (14×), r40 only `S105` (10×), r41 `S105`/`S106` only; r40's
  staged rows are written bare "124, 135, 180 and 187" (no `S` prefix — invisible
  to `\bS\d{3,}\b`). `python3 corpus/evidence/round50/c2-count.py` →
  `REF_ID_UNBOUND=0`, `C2=PASS`.
- **source-line URLs equal the Registry rows** (`corpus/SOURCES.md:114-116`) —
  checked verbatim, including the S104 claim that the row is the Chinese Academy
  of Sciences centre's 引证检索 page, not an ISTIC-named document.
- **Every body `char N` also verified** (script over all three files vs bound-id
  captures): `bad_body_anchors: none` ×3. Corroborated by the frozen counter:
  `QUOTE_ROWS=55 ON_BOUND=55/55`, `QUOTES_IN_SPAN=55/55`, `QUOTES_IN_ENTRY=55/55`.
- **`verified-at:`** present in all three (2026-10-25); r39's "re-located … by
  build-spans.py" corroborated by `STALE=0`.
- Fetch halves of `recheck:` ("re-open the page", "re-download the PDF") are
  cadence directives for a networked future round, correctly not runnable now.

## Residual risk

- r40's "manual page 37 of the copy" is not verifiable from the `.txt` (41
  formfeeds precede §6.1 ≈ PDF page 42; printed folios may differ) — cosmetic.
- spans.tsv's bare `offset` header is mildly ambiguous next to the entries'
  `char N` quote positions — naming note only (peer concurs).
- Tools installed: none.

VERDICT: provenance trio + anchors of the three landed entries — 1 defect found
(r39 recheck pins unmeetable `SPANS_ROWS=11`; actual `SPANS_ROWS=55 STALE=0`),
plus 2 minors (r40 "four sweeps" vs five commands; r41 "three copies" vs two cited
documents); anchors, urls, S-id binding, adopted/package, credential hygiene all
survived.

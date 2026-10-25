# GroundIsticFee — the ISTIC 引证检索 fee block and self-citation note, re-grounded (S104)

Leaf seat, no dispatch. Re-ground the 收费标准 table, the 收费说明 and the self-citation note of
`https://chaxin.las.ac.cn/service/citation-search` from the on-disk capture, say what each fee figure attaches to,
and emit machine lines for `corpus/knowledge/istic-citation-verification-r39.md`. No network (L0 `8d77e6c1` open):
every statement is a command I ran or an offset I opened. No production file, registry row, lesson or tool written.

## 1. The capture and its two forms

    $ ls -la .qcache/001287c436f0e6b1d166ae8d.*
    -rw-r--r-- 1 vgpnk vgpnk 352066 Oct 23 20:39 ...001287c436f0e6b1d166ae8d.raw
    -rw-r--r-- 1 vgpnk vgpnk   5599 Oct 23 20:39 ...001287c436f0e6b1d166ae8d.txt
    $ sha256("https://chaxin.las.ac.cn/service/citation-search")[:24] -> 001287c436f0e6b1d166ae8d  # stem matches

- `.txt`: 5599 bytes, **2288 chars read as UTF-8**, sha256 `67f6f2df8ce96d01673d8f2f740e663f55ed8324bbf804834562bf746740a1db` — the form every quote below is copied from.
- `.raw`: 352066 bytes, sha256 `203b16907c2c953e49bb71310df2a5fd761d3f1798115ceb2ad6881cd01c17c5`, and it is **UTF-8 HTML**: it decodes cleanly as UTF-8 and holds `按合作者排除自引标准统计他引次数`, while its UTF-16LE decoding does not. `build-spans.py:57-65` decodes the `.raw` leg as UTF-16LE, so that leg is unusable here; the `.txt` leg is tried first and carries all ten quotes exactly once.
- Fetch date is the mtime `2026-10-23 20:39` (matches the entry's `page read 2026-10-23`). I opened the capture 2026-10-25; **this is not a live re-open** and no line may claim one.

## 2. Ten located quotes (machine lines)

Form: the `.txt` read as UTF-8. Each satisfies `txt.count(q)==1`, ≤25 whitespace words, ≤160 chars. Offsets in that form, in line order: 549, 422, 464, 498, 511, 524, 662, 774, 697, 594. Staged id is `S118` (`SOURCES.append.md:43`); `assemble-quotes.py` maps this URL to lane id `S104`.

```
QUOTE	S118	https://chaxin.las.ac.cn/service/citation-search	按合作者排除自引标准统计他引次数， 1 元/篇次。	corpus/knowledge/istic-citation-verification-r39.md
QUOTE	S118	https://chaxin.las.ac.cn/service/citation-search	证明费 300 元/份。提供 1 份证明，需要多份证明，增加 1 份 50 元	corpus/knowledge/istic-citation-verification-r39.md
QUOTE	S118	https://chaxin.las.ac.cn/service/citation-search	数据库检索费 10 元起，提供 10 篇以上论文，每篇 1 元	corpus/knowledge/istic-citation-verification-r39.md
QUOTE	S118	https://chaxin.las.ac.cn/service/citation-search	收录篇数 5 元/篇	corpus/knowledge/istic-citation-verification-r39.md
QUOTE	S118	https://chaxin.las.ac.cn/service/citation-search	引用篇次 5 元/次	corpus/knowledge/istic-citation-verification-r39.md
QUOTE	S118	https://chaxin.las.ac.cn/service/citation-search	期刊影响因子及分区 5 元/指标	corpus/knowledge/istic-citation-verification-r39.md
QUOTE	S118	https://chaxin.las.ac.cn/service/citation-search	1.委托5篇以内收录检索，检索费300元。	corpus/knowledge/istic-citation-verification-r39.md
QUOTE	S118	https://chaxin.las.ac.cn/service/citation-search	本次检索可免去相同数据的费用，但要收取本次检索的开库费、复核费和证明费。	corpus/knowledge/istic-citation-verification-r39.md
QUOTE	S118	https://chaxin.las.ac.cn/service/citation-search	（1）引用检索费：3元/次（1-200次），2元/次（200次以上）	corpus/knowledge/istic-citation-verification-r39.md
QUOTE	S118	https://chaxin.las.ac.cn/service/citation-search	引证检索服务收费内容包括：证明费、数据库基础费、收录费、引用费、期刊影响因子及分区费和其他费用	corpus/knowledge/istic-citation-verification-r39.md
```

## 3. What each figure attaches to (offset in the `.txt`)

| figure | clause | attaches to |
|---|---|---|
| 300 元/份, +50 元 per extra copy | 证明费 (422) | one certificate/report |
| 10 元起 | 数据库检索费 (464) | the **floor** of the database-search fee |
| 每篇 1 元 | 数据库检索费 (464) | per paper, **only** when 10+ papers are supplied |
| 5 元/篇 | 收录篇数 (498) | per included work |
| 5 元/次 | 引用篇次 (511) | per citation occurrence — the **base** citation rate |
| 5 元/指标 | 期刊影响因子及分区 (524) | per impact-factor/quartile indicator |
| 1 元/篇次 | 其他 (1) (549) | per work-occurrence of the **他引 (non-self) count** under the co-author exclusion standard — a line separate from 引用篇次 |
| 300元 | 优惠措施 1 (662) | a flat 检索费 for a **收录检索** commission of ≤5 works — a discount, 收录 only |
| 3元/次 (1–200), 2元/次 (>200) | 优惠措施 2(1) (697) | CAS users' 引用检索费 |
| 开库费、复核费、证明费 | 优惠措施 2(2) (774) | **still charged** on a ≤2-year repeat; only the same-data fee is waived |
| 100元/份 (verified, not emitted) | 优惠措施 2(4) (938) | CAS graduate thesis certificate, ≤5 papers |

The 收费说明 enumeration (594) names the table's 数据库检索费 as **数据库基础费** — one fee, two labels.

## 4. Findings against the staged r39 entry

- **F1 — the 300 元 clause merges two attachments.** Lines 53-54 read "1 元/篇次 for the non-self citation count,
  300 元 for a commission of five or fewer works". The 1 元/篇次 attachment is right (549). The 300 元 is right only
  as 优惠措施 1 (662): a flat 检索费 for a **收录检索** commission of ≤5 works; the page's other 300 is 证明费
  300 元/份 (422), per certificate. As written it reads as a total price for any ≤5-work commission, and it omits
  the `10 元起` floor (464) and the base `引用篇次 5 元/次` (511). Draft in §5.
- **F2 — a quoted string is not in the capture.** Observation line 19 prints `"03 完成并审核报告 06 出具正式报告并存档"`;
  `txt.count("03 完成并审核报告 06 出具正式报告并存档")==0`. The `.txt` slice at 380 is `03 完成并审核 报告 06 出具正式报 告并存档`, and the `.raw` DOM order is two columns interleaved (01,04,05,07 | 02,03,06) — describe the steps, or quote the exact slice.
- **F3 — the recheck waiver is overstated.** Lines 22-25 say the same data "is then not re-charged"; the page's own qualifier (774) is that 开库费、复核费 and 证明费 are still charged.
- **F4 — every Inference bullet is uncited, so C2's grounding leg cannot pass as staged.** Ran
  `python3 tools/inference-ground.py --entry <staged r39> --spans <scratch manifest> --counts /dev/null --registry
  corpus/SOURCES.md --root .` → `bullets=4 tokens=2 grounded=0`, 4×`INF_UNCITED`, `INF_TOKEN_NOT_IN_SPAN
  "counting is a property of the index's rules"`, `INF_TOKEN_NOT_IN_SPAN 300`, 2×`INF_UNGROUNDED`, `GROUND: FAIL`,
  rc 1. The token rule is hostile to Chinese: `has_two_words` (`inference-ground.py:82-85`) keeps a backticked or
  quoted phrase only with ≥2 whitespace pieces containing `[A-Za-z]`, and numerals inside backticks are scrubbed
  (line 158). Measured on three test bullets: backticked `SCI、SSCI、EI、ESI、CSCD` → `INF_UNGROUNDED`; bare `200`
  → grounded; no token → `INF_UNGROUNDED`. So each Inference bullet here needs a **bare 3+ digit numeral** in a span.
- **F5 — `source: S118` is not a lane row.** `corpus/SOURCES.md` holds S001–S103 only (row-anchored grep; `S118`
  occurs nowhere in it) and `c2-count.py:75` sets `HELD=set()`, so a surviving `S118` is `REF_ID_UNBOUND`. It must
  become `source: S104 — https://chaxin.las.ac.cn/service/citation-search`; the registry row must be new since
  `BASE_REV`, `mined`, opened `2026-10-25`, `used-by` exactly this entry, its anchor cell carrying a `char N` equal
  to a quote offset (549 and 422 are both correct).
- **F6 — span derivation constraints.** Each quote must sit on **one line** in the entry and in
  `corpus/lessons/round-50.md` (c2 tests substring over the whole file, `c2-count.py:196-197`), and the `.txt`'s
  layout spaces are part of the quote (`300 元/份`, `10 元起`, `每篇 1 元`) because the `.raw` wraps numerals in
  `<strong>` tags. None of the ten quotes is in the staged entry today (`in_entry=False` ×10).
- **F7 — the register sweep is vacuous for this theme.** `grep -c` of `chaxin.las.ac.cn`, `gs.sxu.edu.cn`,
  `rwxy.seu.edu.cn`, `bs.bnu.edu.cn` in `absent-defect-register.md` is 0 each (330 rows), so the c2 verdict leg is
  `0==0` and `blocked=0` this round. Reported as observed; no counter change proposed.

## 5. Draft for the lane (L1 integrates)

Intended lane path: `corpus/knowledge/istic-citation-verification-r39.md` (Observation bullets; one line per quote)
and `corpus/SOURCES.md` (registry row).

```
- **The service is priced line by line, and the non-self count has its own rate.** The 收费标准 lists "证明费 300 元/份。提供 1 份证明，需要多份证明，增加 1 份 50 元", "数据库检索费 10 元起，提供 10 篇以上论文，每篇 1 元", "收录篇数 5 元/篇", "引用篇次 5 元/次" and "期刊影响因子及分区 5 元/指标", and the 收费说明 names the same components: "引证检索服务收费内容包括：证明费、数据库基础费、收录费、引用费、期刊影响因子及分区费和其他费用" (`S104`). The self-citation rule is item (1) under 其他 and carries its own rate — "按合作者排除自引标准统计他引次数， 1 元/篇次。" (`S104`) — so 1 元/篇次 prices the 他引 count, while 引用篇次's 5 元/次 is the base citation rate.
- **The recheck waiver is partial.** "本次检索可免去相同数据的费用，但要收取本次检索的开库费、复核费和证明费。" (`S104`) — a repeat within two years waives the same-data fee only; 开库费、复核费 and 证明费 are still charged.
- **The 300 元 discount is 收录-only, and CAS users pay less per citation.** "1.委托5篇以内收录检索，检索费300元。" and "（1）引用检索费：3元/次（1-200次），2元/次（200次以上）" (`S104`).
```

Inference replacement for the fee bullet (measured clean: `tokens=3 grounded=2`, no bullet-4 finding):

```
- **The service is paid, and its rates attach line by line, which bounds reuse.** The 收费标准 prices each line item separately: a 证明费 of 300 元/份 per certificate, a 数据库检索费 floor of 10 元起 with 每篇 1 元 above ten papers, 收录篇数 5 元/篇, 引用篇次 5 元/次, and, as item (1) under 其他, the co-author non-self count at 1 元/篇次; a 收录检索 commission of five or fewer works pays a flat 检索费 of 300元 (`S104`). So it is an authority the lane can cite but not an open channel a lane can re-run at will.
```

Registry row (11 cells, `corpus/SOURCES.md`):

```
| S104 | 引证检索（论文收录引用检索）服务说明 — 中国科学院文献情报中心 科技查新检索服务平台 — https://chaxin.las.ac.cn/service/citation-search | docs | A | the 收费标准 table, its 收费说明 优惠措施 and the co-author self-citation note, as the institute states them | the 收费标准 table and 收费说明 (capture .txt); located quotes char 549, char 422, char 464, char 498, char 511, char 524, char 662, char 697, char 774, char 594 | 证明费, 数据库检索费 (10 元起, 每篇 1 元 above ten papers), 收录篇数, 引用篇次, 期刊影响因子及分区 and 其他 are priced separately; the co-author non-self count is 1 元/篇次; a ≤5-work 收录检索 commission is a flat 300元 检索费; a ≤2-year repeat waives only the same-data fee | mined | 2026-10-25 | 90d | corpus/knowledge/istic-citation-verification-r39.md |
```

## 6. Receipts

- `python3 corpus/evidence/round50/quote-substance-check.py <scratch spans.tsv>` → `IDS=1 QUOTES=10 FAILURES=0`, rc 0.
- Assembler-shape check of the ten lines (5 tab fields, URL→`S104`, `count==1`, ≤25 words, ≤160 chars, entry path) → `LINES 10 BAD 0`.
- Span windows (exact slice, `start=off-80`, `end=off+len+80`, longer than its quote): 549→469..654 (185), 422→342..541 (199), 464→384..575 (191), 498→418..588 (170), 511→431..601 (170), 524→444..620 (176), 662→582..763 (181), 774→694..890 (196), 697→617..811 (194), 594→514..721 (207).
- Inference-ground: staged entry `GROUND: FAIL` rc 1 (F4); drafted fee bullet `bullets=4 tokens=3 grounded=2` with no `bullet=4` finding (bullets 1–3 remain uncited — the L1's remaining work).

Scope: no install was needed or made; scratch `/dev/shm/chousa-r50-GroundIsticFee/` deleted after the receipts.

VERDICT: attacked the staged r39 fee/self-citation block against the on-disk ISTIC capture — ten quotes locate
exactly once at recorded offsets, but the 300 元 clause merges two attachments, the step-list "quote" is not
verbatim, the recheck waiver drops still-charged fees, all four Inference bullets are uncited (`GROUND: FAIL`), and
`source: S118` is not a lane row; the corrected fee bullet grounds (`tokens=3 grounded=2`).

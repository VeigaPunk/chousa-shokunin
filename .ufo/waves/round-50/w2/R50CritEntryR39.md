# R50CritEntryR39 — falsify the landed r39 entry claim by claim (S104 / 001287c436f0e6b1d166ae8d)

seat `R50CritEntryR39` (leaf, no dispatch) · lane `chousa-shokunin` tip `c5b8dca85f759c7a772225fe036e7bb9a809b91c` (read-only)
target `corpus/knowledge/istic-citation-verification-r39.md`, sha256 `a68a78925998d43a11d6c4e2f7a8995f38cd9328182c8d0b8674b2e66a281e6a` (57 lines)
capture `/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache/001287c436f0e6b1d166ae8d.txt` (5,599 B, 2,288 chars, UTF-8, sha `67f6f2df…a1db`), `.raw` HTML `203b1690…17c5`
no network, no fetch (L0 `8d77e6c1` open); every statement below is a command I ran on the on-disk capture or a file:line I opened.
Frozen file `corpus/evidence/round50/claims.md` read first: no predicate, target, counter or control is proposed for change; D1's repair is prose only because C2 freezes the entry path.

## 1. Receipts (observed output)

```
$ python3 q.py   # 12 strings the entry quotes, text.find/count in the .txt
n_quotes 12
stated/find/count/chars/ws all match=OK at 194(108/1) 1380(38/1) 1236(33/1) 380(25/6) 1784(30/1) 422(39/9)
  549(24/3) 662(21/1) 684(12/1) 735(53/1) 849(50/1) 1469(43/1)   # format: offset(chars/ws-words)
核对 0 | 匹配 0 | 查重 0 | 全文 0 | 原文 0 | 逐条 0 | CNKI 0 | 知网 0
版本 0 | 快照 0 | snapshot 0 | 更新时间 0 | 数据日期 0   (also raw: 版本 0, 快照 0; raw tailwindcss v3.4.17 ×1)
复核 3, all on line 69 | 盖章 1 @1794 | 存档 1 @403 | 报告号 1 | ISTIC 0 | 中国科学技术信息研究所 0 | 中国科学院文献情报中心 3 @989
数据库检索费 10 元起 @464 | 收录篇数 5 元/篇 @498 | 引用篇次 5 元/次 @511 | 期刊影响因子及分区 5 元/指标 @524
（1）引用检索费：3元/次（1-200次），2元/次（200次以上） @697 | 如有SCI或EI收录号，也建议提供 @1419 | 但要收取…开库费、复核费和证明费 @789
$ python3 corpus/evidence/round50/build-spans.py --check      → SPANS_ROWS=55 STALE=0   rc=0
$ python3 corpus/evidence/round50/c2-count.py                 → C2=PASS (BOUND_IDS=S104,S105,S106, QUOTES_IN_ENTRY=55/55, ANCHOR_BOUND=3/3)
$ python3 sp.py   # all 18 S104 span rows: capture[offset:offset+len(span)]==span file, quote at index 80, span>quote → BAD 0
$ awk '{print NR": "length($0)}' …r39.md → lines 4 and 5 are 188 and 405 chars
```

Flow geometry, re-derived from the `.raw` (nested step boxes, divider `y=521`, actors 委托方 `y=56` / 检索员 `y=1018`):

```
委托方 (y=175): 01 提交委托 (x=207) · 04确认报告内容 (808) · 05缴费并填写开票信息 (1140) · 07获取报告、下载发票 (1748)
检索员 (y=660): 02 确认需求并受理委托 (257) · 03 完成并审核报告 (588) · 06 出具正式报告并存档 (1439)
```

## 2. Defects (each: counterexample → evidence → axis → smallest safe correction)

**D1 — false provenance: the entry calls the page "ISTIC", its own registry row names another institute. [depth]**
Counterexample: line 6 "this entry is the ISTIC document's seat" and line 7 "re-bound by document to the ISTIC 引证检索 page", against the same file's `source:` line (S104) and `corpus/SOURCES.md:114` ("引证检索…— 中国科学院文献情报中心 科技查新检索服务平台"). Evidence: capture `ISTIC` 0, `中国科学技术信息研究所` 0, `中国科学院文献情报中心` 3 @989; `corpus/lessons/round-50.md:47` already records "ISTIC-named service page, in fact 中国科学院文献情报中心 … the path says istic" — the entry alone does not. The scoping sentence "every claim is scoped to this institute's service" then inherits the wrong owner. Fix (prose only; the path is frozen by C2):
```
ground: … this entry is the 中国科学院文献情报中心 引证检索 page's seat in that theme …
adopted: … re-bound by document to the 中国科学院文献情报中心 引证检索 page (the frozen path name says istic;
the capture names 中国科学院文献情报中心 3× at char 989 and 中国科学技术信息研究所 0×) …
```

**D2 — the published recheck receipt cannot pass as written. [operability]**
Line 5: "the on-disk half is `python3 corpus/evidence/round50/build-spans.py --check`, which must print `SPANS_ROWS=11 STALE=0`". Observed: `SPANS_ROWS=55 STALE=0`, rc 0; `build-spans.py:178` prints `len(lines) - 1`, the whole 55-row manifest (`quotes.tsv` 55 data rows). A 90d rechecker following the entry would score the recheck as failed. Fix: `must print `SPANS_ROWS=55 STALE=0``.

**D3 — "the eleven quotes below" is twelve, and line 3 omits the twelfth. [calibration]**
Body offsets, extracted: `194 380 422 549 662 684 735 849 1236 1380 1469 1784` — 12 distinct capture strings; line 3's enumeration lists 11 and drops `char 684`, which line 33 quotes ("2.针对中国科学院用户：") and `quotes.tsv`/`spans/S104-11.txt` carry. Fix: line 4 "the twelve quotes below"; line 3 add `char 684`.

**D4 — "The workflow ends in an archived, stamped report": wrong order, wrong actor, and 盖章 is not in the workflow. [depth]**
Line 23 and line 47 ("The workflow's closing steps are `03 … 06 …`"). Counterexample: 03 is step 3 of 7 and the last step is 07 获取报告、 下载发票 @352, which sits in the 委托方 row; 03 and 06 sit in the 检索员 row (boxes y=660 below the divider y=521), so review and archive are the officer's acts and the client never performs them; `盖章` occurs once, @1794, inside 用户须知(9), not in 委托流程 (`存档` 1 @403, `审核` 1). Fix:
```
- **Two workflow steps are the retrieval officer's, and the last step is the client's.** The 委托流程 block
  draws two actor rows (委托方 above the divider, 检索员 below): the client's steps are 01 提交委托,
  04 确认报告内 容, 05 缴费并填写 开票信息 and 07 获取报告、 下载发票, while 02 确认需求并 受理委托,
  03 完成并审核 报告 and 06 出具正式报 告并存档 are the officer's (`char 380` is the contiguous text-form
  slice holding 03 and 06). The default deliverable is 检索报告默认提供打印盖章文件1份，且仅打印报告正文，不含附件
  (`char 1784`) — a printed, stamped copy of the body, stated under 用户须知, not a workflow step.
- **The durable object is the report the officer reviews and archives.** 03 and 06 are the officer's acts, so
  the report outlives the session as an institute-held record while the client's last step is 07 获取报告、 下载发票.
```

**D5 — "300 元 buys the matching of a bibliography": the same 300 attaches to two lines, and the retrieval is priced separately. [depth]**
Line 45. Counterexample: `1.委托5篇以内收录检索，检索费300元。` @662 is 优惠措施 1 — a flat 检索费 for a ≤5-work **收录** commission, 收录 only; the table prices the retrieval at `数据库检索费 10 元起` @464 (`每篇 1 元` above ten papers), `收录篇数 5 元/篇` @498, `引用篇次 5 元/次` @511, `期刊影响因子及分区 5 元/指标` @524, and the certificate at `证明费 300 元/份` @422. The entry quotes both 300s and never says they are different lines, so "300 元 buys the matching" reads as a total price and silently drops the four per-item rates. Fix (tail of line 45):
```
… so a 收录检索 commission of five works or fewer pays a flat 检索费 of 300 元 (`char 662`), 收录 only, while
the table prices the rest line by line (数据库检索费 10 元起 with 每篇 1 元 above ten papers, `char 464`;
收录篇数 5 元/篇, `char 498`; 引用篇次 5 元/次, `char 511`; 期刊影响因子及分区 5 元/指标, `char 524`) and the
certificate at 证明费 300 元/份 (`char 422`): the same 300 figure attaches to two different lines, and 300 元
is not the price of the whole comparison.
```

**D6 — the CAS-only 3 元/次 is stated as the page's citation price. [depth]**
Line 48: "prices a 引用检索 at 3 元/次 for 1-200 次 and 2 元/次 above 200 次", one sentence after the entry establishes CAS scope for the reuse item. Counterexample: that price is item 2(1) @697, inside `2.针对中国科学院用户：` @684; the general rate is `引用篇次 5 元/次` @511. Fix:
```
… and prices 引用检索 for 中国科学院 users at 3 元/次 (1-200 次) and 2 元/次 (above 200 次) (item 2(1), `char 697`),
against the table's general 引用篇次 5 元/次 (`char 511`).
```

**D7 — "nothing opened here states a … self-service route" contradicts the entry's own 复核 bullet. [depth]**
Line 56 vs line 36: item 2(3) @849 lets a `科学院合法用户` run SCI、EI、ISTP on `我中心或本所网络` and bring a week-old printout for 复核 — a user-run retrieval, priced only at 复核 (`收录5元/篇`, `引用按提供论文数每篇20元`). Fix:
```
… the page states no free route; its only self-service shape is item 2(3), where a 科学院合法用户 searches
SCI、EI、ISTP on 我中心或本所网络 and brings a printout for a paid 复核 (`char 849`) — a lane outside that
user group holds neither.
```

**D8 — "The reuse provision implies results can differ between commissions" is unsupported. [calibration]**
Line 52 (inherited from the staged entry, not disclosed as carried). The provision @735 waives the same-data fee for a repeat on identical requirements; nothing in it implies differing results — if anything the retained `复核费` @789 implies re-review. Fix: drop the causal clause and keep the silence:
```
The page states no index state; whether two commissions against different index states would differ is not
stated, and the retained 复核费 on a repeat (`char 789`) is the only hint that a repeat is re-reviewed rather
than re-issued unchanged [INFERENCE].
```

**D9 — "Two documents stating a co-author boundary": only one states a boundary. [calibration]**
Line 46. This page names a standard (`按合作者排除自引标准`, @549) and defines nothing (the entry itself says so); the boundary (`任一合作者` → 自引) is stated only by the CNKI copy r37 describes (`corpus/knowledge/citation-count-semantics-r37.md:21`, quote `对于合作发文的参考文献中，如果引文出现了任一合作者，那么这条引文将被认定为自引`). Fix:
```
… this page names a 合作者排除自引 standard without defining it, and the CNKI copy described at
citation-count-semantics-r37.md states that a reference naming any one collaborator of a co-authored work
counts as a self-citation. One document states a boundary and the other names a standard; neither says the
two rules are the same rule …
```

**D10 — two word-level overclaims. [calibration]** "verdict-shaped artefact" (line 47) imports a judgment the page does not describe: its object is `第三方检索报告` @268 about 收录 and 引用 counts, and line 45 of the same entry says no claim-versus-source comparison is described — fix `a third-party report artefact outliving the session`. "an SCI or EI accession number is optional" (line 16) understates `如有SCI或EI收录号，也建议提供` @1419 — fix `recommended but not required`.

**D11 — two labelling/quote-scope defects. [calibration]** Line 3 calls 优惠措施 items "收费标准 rows": the table ends at `其他` @549, while @662/@735/@849 are `收费说明` items 1, 2(2), 2(3) — fix `the 收费标准 table and 收费说明 items (char 422, 549, 662, 684, 735, 849)`. And the 735 quote stops at `…相同数据的费用`, leaving `，但要收取本次检索的开库费、复核费和证明费` @789 paraphrased unquoted — fix: quote that 19-char clause beside the 735 slice.

## 3. What survived (attacked, not defeated)

- **All twelve quoted strings**: byte-exact, exactly once, at the stated offsets, ≤160 chars / ≤25 whitespace words (§1). The manifest agrees: 18 S104 rows, every span an exact slice with the quote at index 80, `c2-count.py` `C2=PASS`, `ANCHOR_BOUND=3/3`; the peer's span-offset alarm (`R50ReopenRowS105`) is the designed `CONTEXT=80` window, and I told that seat so before its retraction.
- **Reuse scope and modality** (lines 33-35): 684 heading + 735 item (2) + `可免去` discretionary + retained fees 789 — all as the entry says; the entry correctly refuses to call it a reuse of the report.
- **Every negative sweep reproduces**: 核对/匹配/查重/全文/原文 0; 版本/快照/snapshot/更新时间/数据日期 0 in the `.txt` (and 版本/快照 0 in the `.raw`; its only version-shaped token is `tailwindcss v3.4.17` ×1, not index state); 复核 one line, three occurrences; 逐条 0; CNKI|知网 0. The scoping to the text form holds under the raw reading.
- **The CNKI comparison's paraphrase** is accurate against r37's quote and its own Unknowns ("copy", "current?"), and the entry's one-document discipline (paths, not row ids; no cross-quote) holds.

## 4. Tooling and scratch

No install, no upgrade, no pacman transaction (host-wide pause respected); nothing to record. Scratch `/dev/shm/chousa-r50-R50CritEntryR39/` (three probe scripts, one SVG dump) deleted. Only write: this report.

VERDICT: attacked the landed r39 entry against the S104 capture — 13 defects found: D1 the page is called ISTIC in prose while the capture names 中国科学院文献情报中心 ×3 and 中国科学技术信息研究所 ×0 (and SOURCES.md:114 names the centre), D2 the entry's own recheck demands `SPANS_ROWS=11` where the tool prints `SPANS_ROWS=55`, D3 "eleven quotes" is twelve, D4 review (03) and archive (06) are the 检索员's steps (SVG y=660 vs divider y=521), 03 is not a closing step, 07 is the last and 盖章 lives in 用户须知 not the workflow, D5 the two 300 元 lines are conflated while 464/498/511/524 price the retrieval separately, D6 the CAS-only 3 元/次 is stated as the general citation price against 引用篇次 5 元/次 @511, D7 "no self-service route" contradicts item 2(3) @849, D8-D11 narrower calibration defects; the twelve quotes, the manifest, the reuse scoping and every zero-count sweep survived.

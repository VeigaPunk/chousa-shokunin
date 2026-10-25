# GroundSxuDefn — round 50 / wave 1: re-grounding CNKI 管理员 §6.1 引文核对

seat: GroundSxuDefn (scribe, leaf — no dispatch) · lane root /home/vgpnk/Projects/shokunin/chousa-shokunin
document: 知网学位论文学术不端行为检测系统使用手册（管理员）, staged S124/S135/S180/S187 (one document)
url: https://gs.sxu.edu.cn/docs/2025-03/9e5cdd215a414bf6b5694912018de4c8.pdf — no network; every byte below is from the read-only capture cache.

## Capture form and provenance (commands run, output pasted)

```
$ python3 -c "import hashlib;print(hashlib.sha256('https://gs.sxu.edu.cn/docs/2025-03/9e5cdd215a414bf6b5694912018de4c8.pdf'.encode()).hexdigest()[:24])"
e3ca8f4fdd15420b80096a75                      # == cache key, so the capture is this URL's
$ sha256sum .qcache/e3ca8f4fdd15420b80096a75.{txt,raw,pdf}
2197abe27dad4a681b33bee7a6a93a46681968bc8ee88cc0c674eaccdd84f71e  e3ca…75.txt  83384 B, 38174 chars
d36191c72a5ee007e0354b5160d207cffa9e59be86536c997a7dcff9db8ebcb6  e3ca…75.raw  4482989 B
d36191c72a5ee007e0354b5160d207cffa9e59be86536c997a7dcff9db8ebcb6  e3ca…75.pdf  4482989 B   # .raw IS the PDF
$ cp e3ca…75.raw /dev/shm/chousa-r50-GroundSxuDefn/cap.pdf && pdftotext -layout cap.pdf regen.txt && cmp regen.txt e3ca…75.txt
equal True  len 38174 38174  first diff None
```

Decode form, stated next to the offsets as round 49 required: **the `.txt` read as UTF-8** (no BOM, 0 `\r`, 57 form feeds, file ends with `\f`; `pdfinfo` on the same bytes reports `Pages: 57`). It is exactly `pdftotext -layout` of the `.raw` (byte-identical digest), so every offset below is reproducible from the capture pair. Revision stamp `更新时间：2020 年 7 月` at char 48 — supports r41's stamp claim.

## Where §6.1 sits (opened myself)

`第 6 章 辅助功能` 30661 · `6.1 引文核对` 30727 · `6.2 两两比对` 31262 · `6.3 问题库` 31606; page footers `36` 30591, `37` 30990, `38` 31534 — §6.1 body runs on pages 37–38 of 57. 引文核对 occurs exactly 4 times in the capture: 6872 (TOC), 30731, 30738, 30808 — the first body hit is itself split by a wrap (`引文核`/`对、两两比对`).

## Located quotes — form: `.txt` read as UTF-8, offsets = Python `str` index; each `text.count(q)==1`, no newline, ≤160 chars, ≤25 whitespace words

1. @30738 `引文核对是指，以“中国知网”的文献资源为核对源内容` — **the definition and the compared-against corpus in one clause**: the checking source (核对源内容) is 中国知网's own 文献资源. `文献资源`, `核对源内容`, `中国知网` each occur **exactly once**, so this document states the corpus once, with no competing statement.
2. @30773 `进行比对，以核对引文内容的正确性。` — the purpose clause: the object compared is the 引文内容 and what is checked is its correctness — not the manuscript, not a similarity ratio.
3. @30793 `把待检测文献的参考文献复制到“引文核对”文本框` — the input path: the **references** of the document to be checked are **copied** into the 引文核对 text box (this is the sentence the "pasted into a text box" wording rests on).
4. @30844 `系统会将搜索到的有关引用文献的详细情况以列表形式展示在下方` — output shape: a list of found citing records' details, not a score.
5. @30901 `该列表的第一列显示的是是否查找到该引用文献，及引文内容的正确性` — the first column conflates two questions (found? correct?), which is why the three states are not verdicts.
6. @30947 `第一类是“没找到”，表示经过核对，没有找到与输入的这条引文一一对应的文献记录` — state 1 is a one-to-one correspondence failure, not "wrong".
7. @31101 `但是引文中有某一部分的信息与源内容不同` — the middle state is a **located diff** against 源内容. The hover half is not contiguous (`会浮出文字提示具体哪部分不同` count 0: the capture wraps at `会浮出文字`/`提示具体哪部分不同`), and the label is separated from 但是 by a blank line — no single quote can span label+hover.
8. @31169 `第三类则是绿色的标识` — third state's colour word is 绿色; the middle state's is **橙色** @31063 `第二类是橙色的标识` (橙色 1, 琥珀 0).
9. @31233 `列表中的“篇名”可以点击，链接到该引用文献的详细信息。` — the list is a navigation surface into the cited work's record, not a terminal verdict.
   For the sibling seat on columns: @30880 `状态、篇名、作者和文献来源`, count 1.

## Does the text say the references are "pasted into a text box"?

**Half.** The text box is the manual's own (`文本框` 2; the §6.1 one is quote 3 @30793). The verb is not "paste": **`粘贴` occurs 0 times in the whole 38,174-character text** (`复制` 67, `参考文献` 14). The manual says the references are **copied** into the 引文核对 text box; staged r47's "pasted into the 引文核对 text box" and r41's "the pasted citation" are the lane's verb, not the vendor's.

## QUOTE machine lines

```
QUOTE	S124	https://gs.sxu.edu.cn/docs/2025-03/9e5cdd215a414bf6b5694912018de4c8.pdf	引文核对是指，以“中国知网”的文献资源为核对源内容	corpus/knowledge/cnki-citation-check-r40.md
QUOTE	S124	https://gs.sxu.edu.cn/docs/2025-03/9e5cdd215a414bf6b5694912018de4c8.pdf	进行比对，以核对引文内容的正确性。	corpus/knowledge/cnki-citation-check-r40.md
QUOTE	S135	https://gs.sxu.edu.cn/docs/2025-03/9e5cdd215a414bf6b5694912018de4c8.pdf	把待检测文献的参考文献复制到“引文核对”文本框	corpus/knowledge/citation-matching-semantics-r41.md
QUOTE	S135	https://gs.sxu.edu.cn/docs/2025-03/9e5cdd215a414bf6b5694912018de4c8.pdf	系统会将搜索到的有关引用文献的详细情况以列表形式展示在下方	corpus/knowledge/citation-matching-semantics-r41.md
QUOTE	S135	https://gs.sxu.edu.cn/docs/2025-03/9e5cdd215a414bf6b5694912018de4c8.pdf	该列表的第一列显示的是是否查找到该引用文献，及引文内容的正确性	corpus/knowledge/citation-matching-semantics-r41.md
QUOTE	S135	https://gs.sxu.edu.cn/docs/2025-03/9e5cdd215a414bf6b5694912018de4c8.pdf	第一类是“没找到”，表示经过核对，没有找到与输入的这条引文一一对应	corpus/knowledge/citation-matching-semantics-r41.md
QUOTE	S135	https://gs.sxu.edu.cn/docs/2025-03/9e5cdd215a414bf6b5694912018de4c8.pdf	但是引文中有某一部分的信息与源内容不同	corpus/knowledge/citation-matching-semantics-r41.md
QUOTE	S135	https://gs.sxu.edu.cn/docs/2025-03/9e5cdd215a414bf6b5694912018de4c8.pdf	第三类则是绿色的标识	corpus/knowledge/citation-matching-semantics-r41.md
QUOTE	S135	https://gs.sxu.edu.cn/docs/2025-03/9e5cdd215a414bf6b5694912018de4c8.pdf	列表中的“篇名”可以点击，链接到该引用文献的详细信息。	corpus/knowledge/citation-matching-semantics-r41.md
```

Staged-id column = the row each entry's current `source:` line draws (S124 for r40, S135 for r41). **All four staged ids are one document**: `staged-map.tsv` lines 44/55/100/107 (round-45 assimilation) give S124/S135/S180/S187 the same URL, the same cache key `e3ca8f4fdd15420b80096a75` and the same 38174-char count; they collapse to planned lane id S105.

## Falsifiers run against the staged entries (report only — no predicate, target or counter touched)

1. **r40's recheck anchor is not contiguous.** `状态共分为三种类型` count = **0**: the capture reads `确性。状\n态共分为三种类型：` (`状` 30933, newline 30934), so that recheck cannot be re-run by literal search as written; the contiguous slice is `态共分为三种类型：` @30935. r41's recheck anchor `引文核对是指，以“中国知网”的文献资源为核对源内容` is contiguous (count 1, @30738) and does reproduce.
2. **The middle state's colour word** is 橙色 (orange) @31063, once; 琥珀 (amber) 0; 黄色 2 — and both 黄色 hits are the 检测 view's quotation marking (@22573, @25911), a different surface. "Amber" in r40/r41 is not the vendor's word for this state.
3. **r40's Inference places the feature in the 科研·人事论文诚信档案 system, but `诚信档案` occurs 0 times in this manual** (`大学生论文管理系统` 0 too — that is the other product). Unsupported by this document; if kept it needs its own capture.
4. **r41's "查重 flow" label is not the manual's word** (`查重` 0); the substance is grounded — `仅去除第一作者本人文献` 9, `去除本人已发表文献复制比` 11.
5. **r41's negative is confirmed by me**: `匹配` count 0 — the manual publishes no matching algorithm, so "The word 匹配 occurs nowhere in the manual" holds.
6. **Cross-reference ids**: r40's Inference cites `S109`–`S111` (round-4 FEVER ids naming another document's rows) — per this round's rule these must be dropped or described by file path. r41's `S136`/`S145` are the theme's *other two* documents (东南大学 子账号 mirror, BNU 教师 mirror) and must be re-pointed to their own bound ids, not carried as-is.
7. **The claim I was asked to test holds**: §6.1 defines the feature as comparing the entered citation content against 中国知网's own 文献资源 as the 核对源内容 (quotes 1–2), stated once and unambiguously.

## Lane before-state (read-only greps, run in the lane repo)

`grep -rn 9e5cdd215a414bf6b5694912018de4c8 --include=*.md --include=*.json --include=*.tsv .` → only `.ufo/waves/round-45/assimilation/staged-map.tsv`, round-49/50 wave files and the wave spec: **no Registry row**. `grep -rln 引文核对 corpus/knowledge/` and `grep -rln 引证检索 corpus/knowledge/` → no output (both), matching C2's "no corpus/knowledge file held either term at BASE_REV".

## Not checked here / out of scope

- The 子账号 and 教师 manuals' zero-occurrence claims for 引文核对 (r41) — different captures, other seats; I did not open them.
- Whether the 学位论文 variant of the same manual differs in §6.1 (r47's open question).
- No network, no live fetch, no campaign tool from /home/vgpnk/Projects/shokuknow was run; no install or upgrade was made, so there is no tool/version/channel line to record.

VERDICT: attacked the staged r40/r41 definition claim by opening §6.1 in the pinned capture — it holds verbatim (9 unique located quotes; the corpus statement occurs once), while three calibration defects surface: r40's recheck anchor is split by a line wrap (count 0), the middle state is 橙色 not "amber", and the "pasted" verb / "诚信档案" setting / "查重" label are the lane's words, not the manual's (粘贴 0, 诚信档案 0, 查重 0).

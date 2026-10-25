# GroundSxuStates — CNKI 管理员 manual, §6.1 引文核对 result states re-grounded

Seat: leaf member, no dispatch. Lane repo `/home/vgpnk/Projects/shokunin/chousa-shokunin`; only write is this file.
Nothing installed, nothing upgraded (no install needed); no network, no live fetch — all evidence is on-disk capture.

## 1. Capture, key and decode form (round-49 defect "decode form missing next to offsets")

Capture dir `/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache/`, key `e3ca8f4fdd15420b80096a75`:

```
e3ca8f4fdd15420b80096a75.pdf   4482989  Oct 23 20:40
e3ca8f4fdd15420b80096a75.raw   4482989  Oct 23 20:40
e3ca8f4fdd15420b80096a75.txt     83384  Oct 23 20:40
```

Key derivation and byte identity checked:

```
$ python3 -c 'import hashlib;u="https://gs.sxu.edu.cn/docs/2025-03/9e5cdd215a414bf6b5694912018de4c8.pdf";print(hashlib.sha256(u.encode()).hexdigest()[:24])'
e3ca8f4fdd15420b80096a75
$ sha256sum .raw .pdf   # both -> d36191c72a5ee007...  (4482989 bytes each; .raw == .pdf, PDF 1.5, 57 pages)
```

**Decode form, stated for every offset below:** the `.txt`, read as UTF-8 (38,174 characters / 83,384 bytes), which I proved is exactly the `pdftotext -layout` rendering of the `.raw`:

```
$ pdftotext -layout cap.raw out.txt && cmp out.txt e3ca8f4fdd15420b80096a75.txt && echo "IDENTICAL: txt == pdftotext -layout(raw)"
IDENTICAL: txt == pdftotext -layout(raw)
$ pdftotext -layout cap.raw - | sha256sum
2197abe27dad4a681b33bee7a6a93a46681968bc8ee88cc0c674eaccdd84f71e  -
$ sha256sum e3ca8f4fdd15420b80096a75.txt
2197abe27dad4a681b33bee7a6a93a46681968bc8ee88cc0c674eaccdd84f71e  e3ca8f4fdd15420b80096a75.txt
```

So the text form is reproducible from the archived bytes with poppler 26.08.0; offsets are offsets into that UTF-8 string. Section 6.1 引文核对 begins at offset 30727 (`6.1 引文核对`, page 37 of the PDF).

## 2. What §6.1 actually prints — the three states

Verbatim structure (line breaks preserved in the capture; quotes below are single-line spans):

1. List introduction: `系统会将搜索到的有关引用文献的详细情况以列表形式展示在下方，展示内` / `容有状态、篇名、作者和文献来源。` (offset 30844).
2. `该列表的第一列显示的是是否查找到该引用文献，及引文内容的正确性。` then `状` / `态共分为三种类型：` (offset 30901).
3. **First state**: `第一类是“没找到”，表示经过核对，没有找到与输入的这条引文一一对应` / `的文献记录。` (offset 30947). Exact words for "not found": **“没找到”** (the manual never writes 未找到 for this state).
4. **Second (middle) state**: `第二类是橙色的标识（    ）` / `，表示系统经过核对已经找到了该条引文记录，` … `但是引文中有某一部分的信息与源内容不同，将鼠标放到该标识上，会浮出文字` / `提示具体哪部分不同，列表中对应的内容也会红色提示。` (offsets 31063, 31079, 31137). Colour word: **橙色**. Hover tip words: **会浮出文字提示具体哪部分不同** (i.e. `提示具体哪部分不同`), and the differing row content is **红色提示** — not merely "marked".
5. **Third state**: `第三类则是绿色的标识（   ）` / `，标识系统经过核对，判定该条引文与源内容` / `相同，鼠标放上去也会提示各项内容都相同。` (offsets 31169, 31209). Colour word: **绿色**; hover tip words: **提示各项内容都相同**.
6. `列表中的“篇名”可以点击，链接到该引用文献的详细信息。` (offset 31233).

Result-list columns, exact order: **状态、篇名、作者和文献来源**. The 状态 column is the first column; the middle-state marker is an inline image placeholder, hence the literal parenthesis-with-spaces `（    ）` (4 spaces) for 橙色 and `（   ）` (3 spaces) for 绿色 — those space runs are part of the capture and are reproduced byte-exact in the machine lines.

## 3. Colour-word census over the whole capture (`text.count`, 38,174 chars)

| word | count | where |
|---|---|---|
| 橙色 / 橙 | 1 / 1 | §6.1 middle citation-check state only (31063) |
| 绿色 / 绿 | 3 / 3 | 31169 (§6.1 third state); 15003 (绿色对号 提前检测 marker); 18937 (指标文字变绿) |
| 黄色 / 黄 | 2 / 2 | 22573 (§3.4 文字复制 report: 黄色文字表示引用); 25911 (§3.5.2 same) |
| 桔色 / 桔 | 1 / 1 | 14953 (桔色三角标识 = 已在本校账号内提前检测 — a *different* feature) |
| 红色 | 11 | 文字复制 highlighting, 提前检测 triangles, §6.1 红色提示 |
| 灰色 | 2 | 22573, 25911 (excluded content) |
| 蓝色 | 3 | 两两比对 similarity display (§6.2) |
| 黑色 | 3 | 18947 (灰黑色), 22656, 25922 (not-detected content) |
| **琥珀** | **0** | absent from the entire capture |

Two traps the census exposes: (a) the manual's only 黄 occurrences belong to the *similarity report's* highlighting vocabulary (引用部分), never to the citation-check status; (b) the manual does carry a second, genuinely amber-ish middle colour — 桔色 — but it marks 提前检测 time status in the 查重 report, a different feature, so it cannot supply the citation-check middle state either.

## 4. Located quotes — machine lines

`QUOTE` = first field; quote text is the `.txt`-as-UTF-8 form, copied byte-exact from the capture, one line each (no embedded newline). `staged-id` = the staged registry row the entry cites (r40 → `S124`; the same document is also staged as S135/S180/S187, planned lane document id `S105`). Entry path relative to `merge/chousa/knowledge/`.

```
QUOTE	S124	https://gs.sxu.edu.cn/docs/2025-03/9e5cdd215a414bf6b5694912018de4c8.pdf	有状态、篇名、作者和文献来源。	corpus/knowledge/cnki-citation-check-r40.md
QUOTE	S124	https://gs.sxu.edu.cn/docs/2025-03/9e5cdd215a414bf6b5694912018de4c8.pdf	该列表的第一列显示的是是否查找到该引用文献，及引文内容的正确性。	corpus/knowledge/cnki-citation-check-r40.md
QUOTE	S124	https://gs.sxu.edu.cn/docs/2025-03/9e5cdd215a414bf6b5694912018de4c8.pdf	第一类是“没找到”，表示经过核对，没有找到与输入的这条引文一一对应	corpus/knowledge/cnki-citation-check-r40.md
QUOTE	S124	https://gs.sxu.edu.cn/docs/2025-03/9e5cdd215a414bf6b5694912018de4c8.pdf	第二类是橙色的标识（    ）	corpus/knowledge/cnki-citation-check-r40.md
QUOTE	S124	https://gs.sxu.edu.cn/docs/2025-03/9e5cdd215a414bf6b5694912018de4c8.pdf	表示系统经过核对已经找到了该条引文记录，	corpus/knowledge/cnki-citation-check-r40.md
QUOTE	S124	https://gs.sxu.edu.cn/docs/2025-03/9e5cdd215a414bf6b5694912018de4c8.pdf	提示具体哪部分不同，列表中对应的内容也会红色提示。	corpus/knowledge/cnki-citation-check-r40.md
QUOTE	S124	https://gs.sxu.edu.cn/docs/2025-03/9e5cdd215a414bf6b5694912018de4c8.pdf	第三类则是绿色的标识（   ）	corpus/knowledge/cnki-citation-check-r40.md
QUOTE	S124	https://gs.sxu.edu.cn/docs/2025-03/9e5cdd215a414bf6b5694912018de4c8.pdf	鼠标放上去也会提示各项内容都相同。	corpus/knowledge/cnki-citation-check-r40.md
QUOTE	S124	https://gs.sxu.edu.cn/docs/2025-03/9e5cdd215a414bf6b5694912018de4c8.pdf	列表中的“篇名”可以点击，链接到该引用文献的详细信息。	corpus/knowledge/cnki-citation-check-r40.md
```

Each quote verified `text.count(q)==1`, `'\n' not in q`, `len(q)<=160`, `len(q.split())<=25`; offsets 30879, 30901, 30947, 31063, 31079, 31137, 31169, 31209, 31233 (`text.find`). Verification run printed `ALL OK` after the nine assertions; e.g. `第二类是橙色的标识（    ）` → count 1, offset 31063, 15 chars, 2 whitespace words.

## 5. Staged-entry comparison — conflicts verbatim

- `cnki-citation-check-r40.md` (source S124), line 18: `an **amber** marker — the record was` / `found but *part of the citation differs from the source*`. **Wrong colour word.** The PDF says 橙色. Nothing in the capture supports "amber": 琥珀 = 0, and 黄 is confined to the similarity report's 引用 highlighting.
- `citation-check-status-vocabulary-r48.md` (source S187), line 24: `- an **orange** marker — the record was found, but **some part of the` . **Correct.** Its "hovering shows a tip naming which part differs, with the differing text marked in red" matches `提示具体哪部分不同…红色提示`.
- `citation-matching-semantics-r41.md` (source S135), line 17: `record was found but some part of the citation differs from the source` preceded by `an amber state, where the`. **Wrong colour word**, same defect as r40.

So the staged corpus holds the same fact twice as "amber" (r40, r41) and once as "orange" (r48) — an internal contradiction, not a difference of emphasis. Only r48 is supportable.

Secondary wording checks on r40 that I could ground: "the states are not verdicts" and "the title links to the cited work's record" are supported (quotes 1–3, 9); r40's "marked in the list" understates `红色提示` but is not false. r40's `recheck:` line asks to confirm 6.1 still reads `状态共分为三种类型` — the string in the capture is split by a line break (`状` / `态共分为三种类型：`), so a literal single-line search for `状态共分为三种类型` returns 0; the recheck predicate should target `态共分为三种类型：` (offset 30935) or be newline-tolerant.

## 6. Gates and bounds

- Lane bar read for scope only: `corpus/QUALITY.md` (criteria 1–72), `PROVINCE.md`, `tools/inference-ground.py` — no criterion number is asserted here beyond "located quote + offset + decode form", which §1 and §4 satisfy.
- Read-only respected: no write into `/home/vgpnk/Projects/shokuknow`, no campaign tool run (`renumber-staged.py`, `merge-plan.py`, `quote-lint.py`, `absent-defect-register.py` untouched), no git/jj command, no commit, no network, no live fetch.
- Scratch `/dev/shm/chousa-r50-GroundSxuStates/` (cap.raw, out.txt) deleted before finishing; no `/tmp` use.
- Body-only cross-reference ids (S076, S109, S111, S119, S149, S170) are *not* reused here: the only staged ids named are S124/S135/S180/S187, all rows of this one document, mapped to planned lane document id S105.

## 7. Findings

1. Middle state colour word in the manual is **橙色** (offset 31063); third state is **绿色** (31169); first state is **没找到** (30947). Hover tips: `会浮出文字提示具体哪部分不同` + `红色提示`; and `提示各项内容都相同`.
2. **The wrong staged colour word is "amber"**, in `cnki-citation-check-r40.md` and `citation-matching-semantics-r41.md`; `citation-check-status-vocabulary-r48.md`'s "orange" is right. The fix is a one-word correction in two entries, not a predicate change (C2's predicate, targets and controls untouched).
3. 黄/琥珀 cannot rescue "amber": 琥珀 = 0 occurrences; 黄 = 2, both in §3.4/§3.5.2 similarity highlighting; 桔色 = 1, but it marks 提前检测 status in a different feature.
4. The capture's text form is fully reproducible (`pdftotext -layout` of the `.raw`, sha256 2197abe2…), so offsets can be re-derived by the L1 without re-downloading.
5. Minor: r40's `recheck:` predicate is line-break-fragile (see §5).

Out of scope, not attempted: the 子账号 (S106) and 教师 (S107) manuals' absence claims in r41's `recheck:` line; the ISTIC page (S104); C1's self-test and C2's counter scripts; any entry rewrite (the L1 integrates).

Artifacts: this report; capture files named in §1; scratch dir deleted.

VERDICT — Attacked the three "amber/orange" status claims against §6.1 of the 管理员 manual: the PDF says 橙色 (1 occurrence), never 琥珀 (0) and never 黄 for this feature, so r40 and r41 are wrong and r48 is right; nine single-occurrence quotes with UTF-8 offsets and a reproducible decode form recorded.

# ScoutPackageRest — staged CNKI package triage

Axes: depth, calibration, operability. Read-only triage; no candidate edits, source fetches, or installs. Scratch created under `/dev/shm/chousa-r50-ScoutPackageRest/` and removed (`test ! -e ...` → `scratch_removed=YES`).

## Evidence

The five staged headers (`merge/chousa/knowledge/corpus/knowledge/{cnki-citation-check-query-r47,citation-check-status-vocabulary-r48,cnki-comparison-basis-r46,cnki-matching-modes-r42,cnki-public-surface-r43}.md`, lines 1–4) identify URLs and source IDs S180, S187, S175, S149, S160 respectively. For each URL I computed `sha256(url)[:24]` and checked `.txt`/`.raw` with `os.path.exists` and `os.path.getsize`:

```text
r47/r48 e3ca8f4fdd15420b80096a75.txt EXISTS 83384; .raw EXISTS 4482989
r46     9c3aca545490cdfad8428e40.txt EXISTS 52741; .raw EXISTS 52741
r42     625375f640d6eb3be0990ef2.txt EXISTS 210552; .raw EXISTS 210552
r43     dd50f086f911d06fa2bbd5f9.txt EXISTS 2269; .raw EXISTS 39129
```

`SOURCES.append.md` rows observed: S119 is a SinoMed PRISMA-S record; S170 is a real-world-study quality-control paper; S175 is the CNKI privacy policy; S180/S187 and S124/S135 share the SXU administrator-manual URL; S149 is the CNKI overseas search manual; S160 is the TMLC portal. Thus r47 body references `(S170)` for the privacy policy and `(S119)` for the SXU manual point to other staged documents. r47/r48 headers’ S180/S187 identify the same document as S124/S135; the round-50 lane plan maps that document to lane S105.

Capture quotes (UTF-8 `.txt`; each listed quote is exact and occurs once, with `text.find` offset):

```text
r47 e3ca…txt @30745: 以“中国知网”的文献资源为核对源内容 (count=1)
r48 e3ca…txt @31063: 第二类是橙色的标识 (count=1); @31169: 第三类则是绿色的标识 (count=1)
r46 9c3…txt @9080: 优先出版文献库 (count=1); @9134: 比对截止日期 (count=1)
r42 625…txt @17618: 相关度匹配。采用相关度匹配的检索项为：主题、篇名、全文、摘要、参考文献、文献来源。 (count=1)
r43 dd50…txt @211: 本系统以《中国学术文献网络出版总库》为全文比对数据库 (count=1)
```

The SXU PDF uses **橙色** (orange), not 橘色; it also uses 绿色 for the third status and 红色 for the differing text (`.txt` counts: 橙色 1, 橘色 0; passage around chars 31063–31190). The entry’s English colour descriptions match.

Lane check: `git -C /home/vgpnk/Projects/shokunin/chousa-shokunin grep -n 'Q16' -- corpus/` returned no lines (rc 1); same command over the whole repo only found non-corpus wave artifacts. `git grep -n '引文核对' -- corpus/` found only the round-49 verifier lesson and round-50 counter/claims, not a knowledge entry. Lane `corpus/SOURCES.md` has 103 rows, max S103. Therefore this lane corpus does **not** hold the round-12 Q16 denial or the correction target; those are in upstream round-12 material and staged r46/r47, not adopted lane knowledge.

## Triage table

| Entry | Capture / key quote | Lane holds corrected claim? | Recommendation; flip condition |
|---|---|---|---|
| `cnki-citation-check-query-r47.md` | Present, 83,384-byte `.txt`; rule quote present at 30745. Capture continues with copied-reference/search wording at 30793. | **No.** Lane has no Q16 corpus row. Staged r46 is the denial being corrected, not lane-held knowledge. | **Admit-later**, not as an extra this round: it directly corrects the staged denial, but duplicates the same SXU manual already mapped to S105. Flip if the entry is explicitly in scope and remapped to S105, and body-only S119/S170 refs are replaced with file paths or correct bound IDs. |
| `citation-check-status-vocabulary-r48.md` | Same capture/document; 橙色 quote at 31063 and 绿色 at 31169, each once. | **No.** Same absence of lane Q16 knowledge. | **Admit-later** if status-vocabulary depth is wanted; map S187 to S105 and replace body S119 with a path/correct ID. It is an additional entry on the same manual, not another document. |
| `cnki-comparison-basis-r46.md` | Present, 52,741-byte `.txt`; library and cutoff quotes at 9080/9134. | **No.** The denial is staged/upstream, not in lane corpus. | **Refuse** as written: r47’s on-disk manual evidence contradicts its conclusion. Also its claim “比对 occurs ten times” is not reproduced: the capture `.txt` has 25 occurrences; a stripped/collapsed extraction had 13,526 chars and still 25. Flip only after replacing the false-negative conclusion and refreshing its counts from a declared text form. |
| `cnki-matching-modes-r42.md` | Present, 210,552-byte `.txt`; one-frame mode assignment quote at 17618. | **No.** No lane Q16 entry. | **Refuse** for this round: it is about the search platform, and its own claim that the citation-check query rule is unpublished is contradicted by §6.1. Its source header anchors to 一框式检索, while its exact/fuzzy definition is in the separate 高级检索 block (around 23142). Flip for a platform-matching question with that anchor split made explicit and stale Q16 wording removed. |
| `cnki-public-surface-r43.md` | Present, 2,269-byte `.txt`; comparison-database quote at 211; access quote at 283. | **No.** Lane has no such Q16 entry. | **Refuse** as written: it repeats the false claim that query formation is unpublished, contradicted by §6.1. Its sibling 科研人事 portal claim is not in this capture (`科研人事` count 0). Flip if the false negative is removed and the sibling claim is separately sourced or dropped. |

Additional checks: SXU `.txt` has `引文核对` 4 and `核对源内容` 1; the policy `.txt` has `引文核对` 0, `匹配` 0, `比对` 25 (not the entry’s ten); the TMLC `.txt` has `引文核对` 0 and both quoted portal statements once. The r42 `.txt` has the three one-frame matching assignments; the exact/fuzzy definition occurs under 高级检索, not the cited 一框式检索 section.

Commands run included the required lane `git grep -n 'Q16'`, Python SHA-256/cache-size checks, and Python `.txt` `count`/`find` checks. No source was fetched. No tool was installed.

VERDICT: Triaged five staged CNKI entries: captures and key quotes exist, but the lane holds no Q16 claim; two manual entries merit later scoped consideration, while three stale/overreaching entries should be refused as written.

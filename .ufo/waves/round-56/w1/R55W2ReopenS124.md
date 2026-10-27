# R55W2ReopenS124 — S124 reopen

Scope: re-opened frozen round-55 S124 claims only; no source fetch. Defined form is `tools/capture-text.py` stdout over the cached OLE `.raw`, not its `.txt` sidecar. Command run from lane root:

```sh
python3 tools/capture-text.py /home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache/bdff491a75c6abeda1d9c01d.raw
```

Captured stdout decoded UTF-8; observed length 13,718 chars. Evidence: entry `corpus/knowledge/grey-literature-and-chinese-search-record-r40.md:3,13-15`; Registry `corpus/SOURCES.md:134`; round-55 lesson `corpus/lessons/round-55.md:63,83-93`.

## Offsets in entry `source:` line

All four stated offsets are correct and quote the listed text:

| stated char | Actual text at offset | Result |
|---:|---|---|
| 761 | `检索策略包括检索的数据库、检索范围（如主题等）、检索词、检索式（即检索词组合方式）和时间范围等` | correct |
| 994 | `查找时应当注意收集未公开发表的文献，即“灰色文献”，如会议论文、未发表的学位论文、产业报告、咨询报告等。` | correct |
| 4625 | `文献检索策略：检索途径、检索数据库、检索时限及检索式。` | correct |
| 4652 | `应当说明是否有检索限制（如语言限制）、是否手工检索、是否检索灰色文献等关键问题。` | correct |

The line quotes these strings at the recorded offsets; each is present once in the text form. The phrase `即“灰色文献”` itself begins at char 1012, not 994; 994 is the start of its containing sentence. The entry's offset 994 identifies that sentence's quote correctly.

## Observation bullet offsets

Every additional `char N` stated in the Observation bullets is accurate: S124 char 1046 begins `灰色文献中可能包含阴性研究结果`; char 1082 begins `若文献评价中只纳入已公开发表的文献会引入发表偏倚`; char 4 begins the title; 22 begins `（试行）`; 33 begins `国家药品监督管理局《关于药品上市许可持有人直接报告不良反应事宜的公告》（2018年第66号）第四款规定`. The sweep's 2019 and 发布 counts are both zero as reported. Observation's char 5428 and char 340 references in its final bullet also point to the stated heading and Cochrane sentence.

## Registry anchor cell and lesson quote table

S124's Registry anchor cell (`SOURCES.md:134`) says chars 761, 994, 4625, 4652; all four are correct as above. The lesson table (`round-55.md:83-93`) lists S124 offsets 4625, 4652, 761, 994, 1046, 1082, 4, 22, 33, 5428, 340. Every one matches its quote's start in the defined form. In particular, the 994 row quotes the full containing sentence and is not an erroneous assertion that the embedded curly-quoted phrase begins there.

## Unknown sweep

Ran from `/home/vgpnk/Projects/shokunin/chousa-shokunin` the entry's exact command:

```sh
python3 -c "import subprocess;t=subprocess.run(['python3','tools/capture-text.py','/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache/bdff491a75c6abeda1d9c01d.raw'],capture_output=True).stdout.decode();w=('灰色文献','是否检索灰色文献','即“灰色文献”','即灰色文献','2019','发布','国家药品监督管理局','试行','PRISMA','Cochrane');print(len(t),t.count(chr(0xfffd)),[t.count(x) for x in w])"
```

Observed exit 0, stdout exactly `13718 0 [7, 1, 1, 0, 0, 0, 1, 1, 8, 5]`, stderr empty. This agrees with entry line 28 exactly.

```text
VERDICT: Re-opened round-55 S124 offsets, registry anchor, lesson quote table and Unknown sweep; all stated values survive, with the 994 sentence-start distinction confirmed.
```

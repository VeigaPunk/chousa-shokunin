## S125 reopen — source, row, entry, lesson

Source capture opened: `/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache/27d4865f201e99c1fed9f79b.txt` (UTF-8, universal newline form); relevant exact source lines: line 82 byline, line 94 notice/body, line 100 five parts, line 103 Cochrane. Frozen round-56 claims remain untouched.

Commands and observed output:

```text
python3 offset/count check on the defined .txt form
'作者：郭婷 2019-06-18 来源：中国健康传媒集团-中国食品药品网' count=1 offset=242
'6月18日，国家药品监督管理局发布通告，发布《上市药品临床安全性文献评价指导原则（试行）》' count=1 offset=371
'指导原则分为概述、方法学要点、报告撰写规范、指导原则所依据的参考文献和附录五个方面' count=1 offset=780
'引进了Cochrane系统评价规范化操作流程和全程质量控制的方法' count=1 offset=951
body_date_count 0
```

The three cited S125 anchors in the entry and registry (242, 371, 780) are correct, exact, and unique. The cited quotes are each one source line; the Cochrane statement is also exact, unique, and one line at 951, but that offset is not in the registry's anchor cell (which selects only three anchors). The registry's capture metadata says 1,673 characters; the opened capture has 1,673 characters. The date `2019-06-18` occurs in the byline only, not the body: the body says only `6月18日` before “国家药品监督管理局发布通告”. Therefore presenting the exact year as the report's byline date is grounded; presenting the body itself as saying it was issued on 2019-06-18 would not be.

S125 Registry row (`corpus/SOURCES.md:135`) title/date cell, document description, tier B and anchor-cell scope are consistent with this captured report. The `teaches` cell: (1) “the NMPA issued … by notice on 18 June” is entailed by line 94, but its year is supplied by the byline rather than the body; (2) five parts are directly entailed by line 100; (3) the Cochrane process and whole-process quality-control claim is directly entailed by line 103 (and exact phrase at offset 951). It is appropriately scoped as what the affiliated news report says, not as the guideline text itself.

Entry `grey-literature-and-chinese-search-record-r40.md:17-18` accurately reports the byline and body separately, and its five-part and Cochrane descriptions are grounded. Its wording does not wrongly state that the body contains the year. Lesson `round-55-verifier-spotcheck.md:102,106` merely says 2019 is absent from the *S124 .doc* and the date is bound to S125/S126; this remains correct. Lesson makes no specific S125 error.

Verdict: survives. No S125 quote, offset, or factual mismatch found; important precision: `2019-06-18` is byline-only, while body reports “6月18日”.

# R55GroundGcpB — S124 independent document pass

Scope: independently inspected the defined text form of S124 only; did not inspect pass A or other seats' reports. No lane files changed except this report.

## Reproduction and form identity

Command run:
```sh
python3 /home/vgpnk/Projects/shokunin/chousa-shokunin/tools/capture-text.py /home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache/bdff491a75c6abeda1d9c01d.raw > /fast/scratch/hyaku/chousa-r55/R55GroundGcpB/form.txt
```
Observed: exit 0; the raw starts `d0cf11e0a1b11ae1` (OLE compound-file signature), 243,929 bytes, SHA-256 `ac0fad62ed9a11fa3bd135e78427329be30899df90946de7ac45e153974e6c44`. `capture-text.py` SHA-256 is `2c0140bc04029c8faedc6c89a65bd657430d8b85f433406946567b70303e2573` (matches the pinned digest in claims.md). Defined form: 13,718 Unicode characters, 34,234 UTF-8 bytes, 865 LF characters/lines, U+FFFD count 0; form SHA-256 `f0b0899794420b0c10aa9d7caa75e8ccd161b8ad73d9c84e62ebf0bd9c1ef01c`.

## Identity stamp and structure

The form begins with `附件` (char 0), title `上市药品临床安全性文献评价指导原则` (char 4), and provisional status `（试行）` (char 22). Top-level headings occur at lines 5/8/44/64/75: `一、概述`, `二、方法学要点`, `三、报告撰写规范`, `四、本指导原则所依据的参考文献`, `五、附录`. Appendix subheads run from `（一）常用数据库和相关网站` (line 76) through `（六）报告撰写格式` (line 823).

The form contains `国家药品监督管理局` once, at char 33, in the line-6 title/citation of the 2018年第66号 announcement; `公告` occurs once (char 65) in that same cited title. Thus the text names the authority of its cited legal basis, but supplies no distinct self-issuer letterhead/signature stamp. It has no own issuance date visible in the form: `2019` count 0, `二〇一九` count 0, `发布` 0, `印发` 0, `落款` 0, and `年月日` 0. The sole `2018年` is in the cited announcement (char 69); bibliography years are references, not the guideline's date.

The search-record field is present, but is not among the quotes below: exact sentence `2.文献检索策略：检索途径、检索数据库、检索时限及检索式。应当说明是否有检索限制（如语言限制）、是否手工检索、是否检索灰色文献等关键问题。` occurs once at char 4623 (69 characters). The separate grey-literature discussion begins at char 1014.

## Located quotes

Each quote below was checked against the defined form: `form.count(quote) == 1`, `form[offset:offset+len(quote)] == quote`, all are single-line, at most 160 characters and at most 25 whitespace-delimited words. These are independent of the 文献检索策略 sentence.

```text
QUOTE	S124	http://www.gcpunion.org/upload/cmsfile/1703404975484107.doc	附件	corpus/knowledge/grey-literature-and-chinese-search-record-r40.md
QUOTE	S124	http://www.gcpunion.org/upload/cmsfile/1703404975484107.doc	上市药品临床安全性文献评价指导原则	corpus/knowledge/grey-literature-and-chinese-search-record-r40.md
QUOTE	S124	http://www.gcpunion.org/upload/cmsfile/1703404975484107.doc	（试行）	corpus/knowledge/grey-literature-and-chinese-search-record-r40.md
QUOTE	S124	http://www.gcpunion.org/upload/cmsfile/1703404975484107.doc	国家药品监督管理局《关于药品上市许可持有人直接报告不良反应事宜的公告》（2018年第66号）第四款规定	corpus/knowledge/grey-literature-and-chinese-search-record-r40.md
QUOTE	S124	http://www.gcpunion.org/upload/cmsfile/1703404975484107.doc	一、概述	corpus/knowledge/grey-literature-and-chinese-search-record-r40.md
QUOTE	S124	http://www.gcpunion.org/upload/cmsfile/1703404975484107.doc	二、方法学要点	corpus/knowledge/grey-literature-and-chinese-search-record-r40.md
QUOTE	S124	http://www.gcpunion.org/upload/cmsfile/1703404975484107.doc	三、报告撰写规范	corpus/knowledge/grey-literature-and-chinese-search-record-r40.md
QUOTE	S124	http://www.gcpunion.org/upload/cmsfile/1703404975484107.doc	四、本指导原则所依据的参考文献	corpus/knowledge/grey-literature-and-chinese-search-record-r40.md
QUOTE	S124	http://www.gcpunion.org/upload/cmsfile/1703404975484107.doc	五、附录	corpus/knowledge/grey-literature-and-chinese-search-record-r40.md
QUOTE	S124	http://www.gcpunion.org/upload/cmsfile/1703404975484107.doc	图2.文献筛选流程图（参考PRISMA）	corpus/knowledge/grey-literature-and-chinese-search-record-r40.md
QUOTE	S124	http://www.gcpunion.org/upload/cmsfile/1703404975484107.doc	1.安全性文献评价应当检索与研究药品有关的所有国内外文献资料	corpus/knowledge/grey-literature-and-chinese-search-record-r40.md
QUOTE	S124	http://www.gcpunion.org/upload/cmsfile/1703404975484107.doc	5.评价者、评价单位、评价日期	corpus/knowledge/grey-literature-and-chinese-search-record-r40.md
QUOTE	S124	http://www.gcpunion.org/upload/cmsfile/1703404975484107.doc	引进了Cochrane系统评价规范化操作流程和全程质量控制的方法	corpus/knowledge/grey-literature-and-chinese-search-record-r40.md
```

These QUOTE rows give the intended C2 entry path; it did not exist at the lane HEAD observed (`git cat-file -e HEAD:corpus/knowledge/grey-literature-and-chinese-search-record-r40.md` returned fatal “does not exist”), so no claim is made that it has already been integrated.

## Exact requested token sweeps

The following are Python `form.count(token)` values over the 13,718-character defined form, not the `.txt` sidecar:

| Token | Count | Finding |
|---|---:|---|
| `2019` | 0 | absent |
| `二〇一九` | 0 | absent |
| `国家药品监督管理局` | 1 | present at char 33, cited announcement context |
| `药监局` | 0 | absent |
| `NMPA` | 0 | absent |
| `灰色文献` | 7 | present |
| `即“灰色文献”` | 1 | present |
| `即灰色文献` | 0 | absent |
| `手工检索` | 3 | present |
| `语言限制` | 1 | present |
| `发表偏倚` | 4 | present |
| `Cochrane` | 5 | present |
| `系统评价` | 2 | present |
| `PRISMA` | 8 | present |
| `附录` | 8 | present |
| `参考文献` | 5 | present |

## Defined-form caution

For comparison only, the `.txt` sidecar is 323,728 bytes and its UTF-8 decode has 241,513 characters and 40,252 U+FFFD; the probe `查找时应当注意收集未公开发表的文献` occurs 0 times there but once in the defined form. A direct UTF-16LE decode of `.raw` is also not the defined form: 121,964 characters, 887 U+FFFD; it happens to contain the same grey-literature probe once, but its `灰色文献` first offset is 53,777 rather than the defined form's 1,014, and `语言限制` is at 57,484 rather than 4,665. These illustrate why occurrence in a sidecar/decode cannot substitute for the specified OLE text form or its offsets.

## Boundaries and verdict

No network access, counter run, LibreOffice run, or other seat report was used. `pgrep -u $USER -f "R55GroundGcpB"` returned no process (exit 1). Scratch was removed after copying the observed outputs and receipts into this report.

VERDICT: S124 is an identifiable provisional guideline attachment with five top-level sections and substantial grey-literature/search-record content; it names NMPA only within a cited 2018 announcement, not as a distinct self-issuer stamp, and the defined form has 13,718 characters with zero U+FFFD.
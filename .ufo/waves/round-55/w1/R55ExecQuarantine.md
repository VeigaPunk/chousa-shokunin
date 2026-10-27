# R55ExecQuarantine — S125 hand-check

Scope: only the `chousa` absent-defect-register row `S125` (register namespace, round6), using the source’s defined OLE text form. No lane predicate or target changed.

## Evidence

Commands run (all shell work from `/fast/scratch/hyaku/chousa-r55/R55ExecQuarantine`):

```text
grep -n 'round6 | S125' /home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/absent-defect-register.md
56:| `chousa` | round6 | S125 | `payload-absent` | http://www.gcpunion.org/upload/cmsfile/1703404975484107.doc | [three quoted strings] | cited source, companion URLs and local artifacts were all checked; the quote is in none of them |

python3 /home/vgpnk/Projects/shokunin/chousa-shokunin/tools/capture-text.py /home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache/bdff491a75c6abeda1d9c01d.raw > /fast/scratch/hyaku/chousa-r55/R55ExecQuarantine/form.txt
EXIT:0
865 34234 /fast/scratch/hyaku/chousa-r55/R55ExecQuarantine/form.txt
```

The captured stdout was read as UTF-8, 13,718 characters. Register strings were extracted from row 56 and counted with `form.count`; offsets below are `form.find` character offsets in that defined form. Both present strings occupy one line each.

| Register quote | Count | Defined-form evidence |
|---|---:|---|
| `文献检索策略：检索途径、检索数据库、检索时限及检索式。应当说明是否有检索限制（如语言限制）、是否手工检索、是否检索灰色文献等关键问题。` | 1 | offset 4625; line 53; within one line (form line bounds 4623–4692) |
| `检索策略包括检索的数据库、检索范围（如主题等）、检索词、检索式（即检索词组合方式）和时间范围等，应当根据不同的研究目的制定。` | 1 | offset 761; line 15; within one line (bounds 675–823) |
| `查找时应当注意收集未公开发表的文献，即灰色文献，如会议论文、未发表的学位论文、产业报告、咨询报告等。` | 0 | absent as written. Nearest exact sentence occurs once at offset 994, line 16: `查找时应当注意收集未公开发表的文献，即“灰色文献”，如会议论文、未发表的学位论文、产业报告、咨询报告等。` Removing its two curly quote characters `“` and `”` yields the register quote exactly. |

Sidecar contrast (read-only, diagnostic): the `.txt` sidecar count for Q1/Q2/Q3 was `0/0/0`; raw UTF-16LE decode was `1/1/0`; defined OLE form was `1/1/0`. The verdict above relies only on the defined form, not either alternate representation.

Theme URL census: the whole register scan for `gcpunion|cnpharm|english\.nmpa|medsci` found only line 56 (`gcpunion`). Enumerating `chousa` table rows found 24 rows and exactly one theme-URL row: `round6 | S125 | http://www.gcpunion.org/upload/cmsfile/1703404975484107.doc`. No other register row in lane `chousa` on those four theme URLs was found. This agrees with the stated C2 freeze count of one.

Required lesson-format line:

```text
- register `S125` (round6) — http://www.gcpunion.org/upload/cmsfile/1703404975484107.doc — verdict: present — Q1 count 1 at defined-form char 4625 (line 53); Q2 count 1 at char 761 (line 15); Q3 count 0 as written, but nearest wording occurs once at char 994 (line 16) and differs only by curly quotes around 灰色文献; sidecar counts Q1/Q2/Q3 = 0/0/0.
```

VERDICT: Hand-checked S125 against the defined OLE form; the `payload-absent` assertion is refuted (two quotes present, one absent only as written); no other `chousa` theme-URL register row found.
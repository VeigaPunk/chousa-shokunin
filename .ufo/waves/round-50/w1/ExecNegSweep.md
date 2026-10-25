# ExecNegSweep — negative-claim sweep, staged `citation-matching-semantics-r41.md` (r50 w1)

Seat: leaf executor. Attacked only the absence claims of the staged entry
`/home/vgpnk/Projects/shokuknow/merge/chousa/knowledge/corpus/knowledge/citation-matching-semantics-r41.md`
(read-only) against three on-disk captures. No network, no live fetch, no install (`pdftotext`
26.08.0 present). Scratch `/dev/shm/chousa-r50-ExecNegSweep/`, deleted. No production file,
index, jj state or sibling report touched.

## 1. Captures, identities, forms

| key | URL | identity read from the `.txt` head |
|---|---|---|
| `e3ca8f4fdd15420b80096a75` | `https://gs.sxu.edu.cn/docs/2025-03/9e5cdd215a414bf6b5694912018de4c8.pdf` | `知网学位论文学术不端行为检测系统 使用手册 （管理员）`, `更新时间：2020 年 7 月` |
| `28750bcdf5d36cd90a7709fb` | `https://rwxy.seu.edu.cn/_upload/article/58/cc/5a2fdc1940cfa2522e82ba8b5d81/fb75a598-a343-48f2-bb42-5c6c411506bc.pdf` | `“中国知网”大学生论文管理系统使用手册 （子账号）`, `V 5.0`, `2014-03-10` |
| `275c79d45b1e9b0fd32cef93` | `https://bs.bnu.edu.cn/docs/20160407183946745914.pdf` | `“中国知网”大学生论文管理系统使用手册 （教师）` |

Each `.raw` is byte-identical to the `.pdf` beside it (`sha256` `d36191c7…`, `0f426ea2…`,
`cbeccf3f…`): `.raw` is the PDF stream, not a text form. Text work uses the `.txt` as UTF-8;
`U+FFFD` = 0 in all three, so no decode loss can excuse a zero.

## 2. Term sweep per `.txt` (count, first offsets)

```
python3 - <<'EOF'
Q="/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache/"
for k in ["e3ca8f4fdd15420b80096a75","28750bcdf5d36cd90a7709fb","275c79d45b1e9b0fd32cef93"]:
 t=open(Q+k+".txt",encoding="utf-8").read(); acc=[]
 for w in ["引文核对","核对","匹配","引文","自引","仅去除第一作者"]:
  o=[];i=t.find(w)
  while i!=-1 and len(o)<5: o.append(i);i=t.find(w,i+1)
  acc.append("%s=%d%s"%(w,t.count(w),o))
 print("=== %s chars=%d bytes=%d CJK=%d FFFD=%d"%(k,len(t),len(t.encode()),sum(1 for c in t if '\u4e00'<=c<='\u9fff'),t.count('\ufffd')))
 print("  "+"  ".join(acc[:3])); print("  "+"  ".join(acc[3:]))
EOF
# output, verbatim:
=== e3ca8f4fdd15420b80096a75 chars=38174 bytes=83384 CJK=20192 FFFD=0
  引文核对=4[6872, 30731, 30738, 30808]  核对=11[6874, 12511, 30733, 30740, 30758]  匹配=0[]
  引文=22[4344, 6872, 23610, 23812, 24899]  自引=0[]  仅去除第一作者=11[5222, 5329, 5450, 27573, 27611]
=== 28750bcdf5d36cd90a7709fb chars=30937 bytes=63869 CJK=14639 FFFD=0
  引文核对=0[]  核对=0[]  匹配=0[]
  引文=10[3509, 13948, 19247, 20218, 21064]  自引=0[]  仅去除第一作者=9[4148, 4253, 4391, 22497, 22527]
=== 275c79d45b1e9b0fd32cef93 chars=9914 bytes=22648 CJK=5696 FFFD=0
  引文核对=0[]  核对=0[]  匹配=0[]
  引文=9[1260, 6733, 8055, 8842, 8863]  自引=0[]  仅去除第一作者=0[]
```

## 3. Independent extractor comparison

`pdftotext -layout $Q/$k.pdf -` piped into a python counter, per key:
```
e3ca… chars=38174 引文核对=4 核对=11 匹配=0 引文=22 自引=0 仅去除第一作者=11
28750… chars=30937 引文核对=0 核对=0 匹配=0 引文=10 自引=0 仅去除第一作者=9
275c7… chars=9914  引文核对=0 核对=0 匹配=0 引文=9  自引=0 仅去除第一作者=0
```
`cmp` of each fresh `-layout` file against its capture: `IDENTICAL` (83384 / 63869 / 22648
bytes). The captures *are* `pdftotext -layout` output, so this leg confirms provenance, not an
independent extractor; I added two other reading orders and recounted (`chars`, `引文核对/核对/匹配`):
```
layout  38174 4/11/0 | 30937 0/0/0 | 9914 0/0/0
raw     33163 4/11/0 | 25454 0/0/0 | 8394 0/0/0
default 33412 4/11/0 | 25801 0/0/0 | 8534 0/0/0
```
Term counts are invariant across all three modes; only the character total moves.

## 4. Which staged numbers reproduce

- `30,937` — **reproduces exactly**: `len(28750bcdf5d36cd90a7709fb.txt)` = 30937. It is the
  `.txt`/`-layout` form's length only (`-raw` 25454, default 25801): extraction-form-specific,
  and the entry does not name the form. Under-specified, not wrong.
- `zero occurrences` of `引文核对`, `核对`, `匹配` — **reproduces exactly** in the 子账号 manual
  (0/0/0 at 30,937 chars) and in the 教师 manual (0/0/0 at 9,914), stable across layout/raw/default.
- "`匹配` occurs nowhere in the manual" (管理员) — **reproduces**: 0 in `e3ca…` in all three
  modes and in all three manuals. Recheck clause "`引文核对` zero in 子账号 and 教师" — **reproduces**.

## 5. Structural corroboration beyond word counts

`辅助` (the module hosting the feature) = 5 in 管理员, **0** in 子账号, **0** in 教师. The
管理员 `第 6 章 辅助功能` opens `辅助模块主要提供了引文核对、两两比对和问题库功能。` (@30705),
while the other two document `两两比对` only as an inline button (子账号 @30626, 教师 @7531) —
a whole-module omission, which strengthens the staged sentence.

## 6. Located quotes (`.txt` as UTF-8, `text.find`, exactly once)

```
QUOTE	key	offset	chars	words
引文核对是指，以“中国知网”的文献资源为核对源内容	e3ca8f4fdd15420b80096a75	30738	25	1
将鼠标放到该标识上，会浮出文字\n提示具体哪部分不同	e3ca8f4fdd15420b80096a75	31121	25	2
在创建文件夹页面中第一个选项为“仅去除第一作者本人文献”	28750bcdf5d36cd90a7709fb	22511	28	1
将去除相似文\n献列表中第一作者为本人的相似文献	28750bcdf5d36cd90a7709fb	22574	23	2
若选择查看“全文（标明引文）报告单”，则打开的报告单标题会提示为“全	275c79d45b1e9b0fd32cef93	8852	34	1
```
The two `\n` are literal newlines: this extraction hard-wraps CJK mid-word (`状\n态共分为三种
类型`, 30939), so a quote crossing a wrap carries the newline or stays inside one line.

## 7. Defects in the staged entry (routed; nothing edited here)

1. **"an amber state"** — the capture's word is `橙色` (count 1, @31067); amber substitutes a
   colour name the source never uses. The other states are literal (`没找到` @30952, `绿色` @31174).
2. **"named on hover"** — faithful in substance, unquotable as written: `悬停` = 0; the manual
   reads `将鼠标放到该标识上，会浮出文字提示具体哪部分不同` (@31121).
3. **Over-strong term triple** — correct, but it hides that the omission is the whole `辅助`
   module (§5). `自引` = 0 in all three manuals: the manuals' term is `去除本人已发表文献复制比`.
4. **Non-unique anchors** — `6.1 引文核对` 2× in 管理员 (TOC @6868, body @30727);
   `2.6 仅去除第一作者本人文献` 2× in 子账号 (@4144, @22493); `全文（标明引文）报告单` 8× in
   教师 (first @1255): each needs an offset or a body-only tail.
5. **Staged ids** — `source:` carries `S135`, `S136`, `S145`; lane registry max is `S103`
   (`corpus/SOURCES.md:113`) and none of the three URLs appears in any lane `corpus/` record
   (`grep -rl` hits only `.ufo/waves/*`). Staged-only: renumber to 管理员→S105, 子账号→S106,
   教师→S107; no lane row exists yet — consistent with C2's "new since BASE_REV" leg.

## 8. Files changed, risks, blockers

None; this report only, scratch removed, no commits/index/jj operations. All three captures are
`pdftotext -layout` output, so no extractor independent of poppler exists on this host for the
zeros; I substituted two other poppler reading orders. Residual risk: a term present only as a
scanned image is invisible in every text form — no OCR leg was run. And `30,937` must not be
reused in the lane entry without naming the form, or a `-raw` recheck reads a 5,483-char "shrink".

VERDICT: swept the three CNKI manual captures for all six terms across three poppler reading orders and confirmed both staged numbers — `30,937` = exact `.txt` length, and `引文核对/核对/匹配` = 0/0/0 in the 子账号 manual, 0/0/0 in the 教师 manual, `匹配` = 0 in the 管理员 manual — while routing five defects (amber↔`橙色`, `悬停` = 0, over-strong term triple, three non-unique anchors, staged-only `S135/S136/S145`).

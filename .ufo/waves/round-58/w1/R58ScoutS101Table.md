# R58ScoutS101Table — S101 section 1.2.1

## Scope and evidence

Read the frozen `claims.md`, `c1-count.py`, `c2-count.py`, and `c2/quotes.tsv` before judging. Claims identify the S101 `.doc` capture and its defined text form; no live fetch was made. No counter was run (not relevant to this table-layout question).

Observed committed source pins in `claims.md` / `c2-count.py`:
- URL: `https://jc.hit.edu.cn/_upload/article/files/f7/54/711916924125a0682e3bc3ebb6ed/1f6f2731-8c87-4812-b7e2-9fad0069d508.doc`
- Raw SHA-256: `6063a3aff7a4081e93a685f2721e2cd6b477ba84a841211e298bcddd6d9fddf3`
- `tools/capture-text.py` SHA-256: `2c0140bc04029c8faedc6c89a65bd657430d8b85f433406946567b70303e2573`

Commands (all source reads were read-only; generated text was in seat scratch):
```text
sha256sum /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/captures/6dc68fd6b32ce9c8dfcebce8.raw /home/vgpnk/Projects/shokunin/chousa-shokunin/tools/capture-text.py
6063a3aff7a4081e93a685f2721e2cd6b477ba84a841211e298bcddd6d9fddf3  /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/captures/6dc68fd6b32ce9c8dfcebce8.raw
2c0140bc04029c8faedc6c89a65bd657430d8b85f433406946567b70303e2573  /home/vgpnk/Projects/shokunin/chousa-shokunin/tools/capture-text.py
python3 /home/vgpnk/Projects/shokunin/chousa-shokunin/tools/capture-text.py /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/captures/6dc68fd6b32ce9c8dfcebce8.raw > s101.txt 2>err.log; echo "exit=$?"; wc -c s101.txt; cat err.log
exit=0
47356 s101.txt
(no stderr)
awk 'NR>=14 && NR<=58 {printf "%3d|%s\n", NR, $0}' s101.txt
 14|1．2 参考文献类型及其标识
 15|1．2．1 根据GB3469规定，以单字母方式标识以下各种参考文献类型：
 16|参考文献
 17|类型
 18|普通
 19|图书
 20|会议
 21|论文
 22|报纸
 23|文章
 24|期刊
 25|文章
 26|学位
 27|论文
 28|报
 29|告
 30|标
 31|准
 32|专
 33|利
 34|汇
 35|编
 36|档
 37|案
 38|古
 39|籍
 40|参考
 41|工具
 42|
 43|文献类型
 44|标识
 45|M
 46|C
 47|N
 48|J
 49|D
 50|R
 51|S
 52|P
 53|G
 54|B
 55|O
 56|K
 57|
```

The generated form has no tabs in this region. Per `capture-text.py`'s documented defined form, OLE paragraph, cell, and row endings all emit newline; consequently, these lines do not identify which newlines are cell/row boundaries versus paragraphs within a cell. There is no explicit column separator or table grid in this text form.

## What is visible / mapping

The section heading says the reference types are identified by single letters. The visible type-text sequence is `普通 / 图书`, `会议 / 论文`, `报纸 / 文章`, `期刊 / 文章`, `学位 / 论文`, `报 / 告`, `标 / 准`, `专 / 利`, `汇 / 编`, `档 / 案`, `古 / 籍`, `参考 / 工具`; after a blank line the visible letter sequence is `M C N J D R S P G B O K`. Thus the natural positional reading yields:

| Letter | Type text as read in sequence |
|---|---|
| M | 普通图书 (ordinary book) |
| C | 会议论文 (conference paper) |
| N | 报纸文章 (newspaper article) |
| J | 期刊文章 (journal article) |
| D | 学位论文 (thesis/dissertation) |
| R | 报告 (report) |
| S | 标准 (standard) |
| P | 专利 (patent) |
| G | 汇编 (compilation) |
| B | 档案 (archive) |
| O | 古籍 (ancient/rare book) |
| K | 参考工具 (reference tool) |

This is a positional interpretation, not a directly marked association in the extracted text. It combines adjacent fragments such as `普`/`通` and `图`/`书` where visibly split across separate lines. Internal text later in the same capture is consistent for some mappings: section 1.3 examples label archive entries `[B]`, ancient-book entries `[O]`, and unspecified types `[Z]`; section 1.2.2 explicitly assigns `Z` to other unspecified types. This corroborates those examples but does not restore table geometry or prove all pairings. Section 14.3.1 contains another ordered type/letter listing, but its extracted rows are likewise flattened; it lists `M C N J D R S P G K` and not B/O.

## Layout judgment and limits

The order and counts (12 apparent type entries and 12 single-letter entries) support the mapping above as the likely intended left-to-right correspondence. **The defined text form does not preserve row/column associations**: it contains only sequential text and newlines, and it does not show cells, columns, borders, or coordinates. It cannot establish from this text alone that each letter occupied the same respective column as its mapped type, or whether line breaks inside type names are paragraph breaks or table-cell boundaries. Treat the pairing as positional/inferred, not explicit table-layout evidence. This finding concerns visible text only; it does not establish the document's semantic truth or the external standard's validity.

## Reproduction / cleanup

Scratch: `/fast/scratch/hyaku/chousa-r58/R58ScoutS101Table/`. The defined form was made only there. Scratch was removed before reporting. No installation, source edit, git/jj mutation, or live fetch.

VERDICT: The S101 defined text supports the ordered type and letter sequences and a likely 12-pair mapping, but the attack on direct row/column-association evidence survives: extracted layout is flattened and association remains positional/inferred.

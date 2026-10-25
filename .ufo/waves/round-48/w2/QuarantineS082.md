# W2 Quarantine hand-check — chousa round1 S082

Verdict: **absent-as-written** (the register's `payload-absent` classification is
correct). The quoted span is not a contiguous string anywhere in the cached
capture of the cited source, nor in the lane's own local artifacts.

## Row under test

- Register row: `~/Projects/shokuknow/.ufo/waves/corpus-expansion-1/absent-defect-register.md:39`
  `| chousa | round1 | S082 | payload-absent | https://support.nii.ac.jp/ja/cir/manual_articles_detail | 被引用文献（この論文を引用している文献）の一覧が表示されます。 随時増加していきます。 | … |`
- Census finding: `quote-lint-full-v5.json` — one ABSENT quote
  (`"verdict":"ABSENT","fold":null,"binding":"id","sweep":false`); the row's only
  other quote (`データソース種別 …`) passed under `fold:"whitespace"`.
- Lane SOURCES row: this URL is carried at `lanes/chousa/SOURCES-PROPOSED.md:40`
  under id **S087** (block 85-94 is `#### Gate — S087`; the census saw an older
  numbering, so register `S082` ≡ lane `S087`; `merge/chousa/SOURCES.append.md:12`
  also carries it as S087). The disputed gate line is
  `lanes/chousa/SOURCES-PROPOSED.md:92`:
  `Quote — section G, table row: "被引用文献（この論文を引用している文献）の一覧が表示されます。 随時増加していきます。"`

## Capture examined

`.ufo/waves/corpus-expansion-1/.qcache/09fc63de41f293d43d631c46.raw`
- sha256 `5ce63212fe0047977feabffecc9a1030e6264f7938d56084741f3d9261449ef9`
- 41,404 bytes / 758 lines, UTF-8 HTML
- Identity: `<link rel="canonical" href="https://support.nii.ac.jp/ja/cir/manual_articles_detail" />`;
  `<title>論文詳細表示画面について | 学術コンテンツサービス サポート</title>`

## Commands and observed output

```
$ grep -c "被引用文献（この論文を引用している文献）の一覧が表示されます。 随時増加していきます。" $Q
0
$ grep -c "引用している文献）の一覧" $Q
0
$ grep -c "引用されている文献" $Q
1
$ grep -bo "被引用文献（この論文が引用されている文献）の一覧が表示されます" $Q
28410:… (line 464)
$ grep -bo "現在表示している論文を引用している文献です" $Q
28825:… (line 472)
$ grep -bo "随時増加していきます" $Q
28914:… (line 473)
```

Served text at `…:464` (section G `<p>`):
`参考文献（この論文が引用している文献）、被引用文献（この論文が引用されている文献）の一覧が表示されます。`
and at `…:472-473` (table `<td>`): `現在表示している論文を引用している文献です。<br />\n                随時増加していきます。`

## Reason

The gate quote splices the section-G intro phrase `被引用文献（…文献）の一覧が
表示されます` — which the page writes in the passive `この論文が引用されている`
(this paper **is cited by**) — with the table cell's `随時増加していきます`,
changing `が`→`を` (active "papers citing this paper") and dropping the 引用文献
half of the sentence. The two fragments sit ~500 bytes apart in different
elements; no fold produces the quoted span. The checker's ABSENT verdict on the
local byte capture is confirmed by hand: this is a genuine paraphrase-drift
fabrication, not a whitespace/markup artifact and not a fetch failure.

Local artifacts concur: the deepresearch note
(`lanes/chousa/.deepresearch/20261023_172027_chousa-corpus-expansion/final_turn_001.md:49`)
paraphrases the same passage correctly and quotes only `随時増加していきます`
verbatim — the fabricated hybrid appears nowhere except the gate line itself.
No installs used; no live fetch performed (L0 `8d77e6c1` honored).

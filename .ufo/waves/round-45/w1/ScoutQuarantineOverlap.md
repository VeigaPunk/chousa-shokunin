# Scout findings: quarantine overlap

## Assignment
Confirm whether the three C3 adoption URLs (AVeriTeC README, arXiv 2305.13117v3 HTML, and AVeriTeC `data/train.json`) occur in the lane quarantine slice, using the requested slice command, operator recipe, and whole-register keyword searches.

## Commands and verbatim outputs

1. `python3 /home/vgpnk/Projects/shokunin/chousa-shokunin/tools/quarantine-check.py slice`

Output:
```
S077\tround1\tpayload-absent\thttps://doi.org/10.1186/s13643-020-01542-z\t3
S080\tround1\tpayload-absent\thttps://std.samr.gov.cn/gb/search/gbDetailed?id=4507EFE13D37CB6AE06397BE0A0A601F\t1
S082\tround1\tpayload-absent\thttps://support.nii.ac.jp/ja/cir/manual_articles_detail\t1
S084\tround1\tpayload-absent\thttps://www.jstage.jst.go.jp/static/pages/FAQs/TAB2/-char/ja\t2
S086\tround1\tpayload-absent\thttps://www.ncpssd.cn/\t2
S088\tround2\tpayload-absent\thttps://xuebaobangong.jmu.edu.cn/zkb/Upload/Park/64b9ba1b-df55-4309-87d4-0d037a497bd0.pdf\t1
S093\tround2\tpayload-absent\thttps://aclanthology.org/2026.findings-acl.19.pdf\t1
S094\tround2\tpayload-absent\thttps://ojs.aaai.org/index.php/AAAI/article/download/29825/31432\t3
S095\tround2\tpayload-absent\thttps://www.zcmu.edu.cn/__local/2/33/FC/FFA702D0F9381C8224BD74CB435_0E777725_C3A00.doc?e=.doc\t3
S096\tround2\tpayload-absent\thttps://jc.hit.edu.cn/_upload/article/files/f7/54/711916924125a0682e3bc3ebb6ed/1f6f2731-8c87-4812-b7e2-9fad0069d508.doc\t3
S104\tround3\tpayload-absent\thttps://www.jstage.jst.go.jp/article/kenkokyoiku/32/2/32_320208/_pdf/-char/ja\t1
S105\tround3\tpayload-absent\thttps://jaohfa.com/pdf/systematic_review.pdf\t3
S108\tround3\tpayload-absent\thttps://arxiv.org/html/1803.05355\t1
S110\tround3\tpayload-absent\thttps://aclanthology.org/2025.coling-main.108.pdf\t3
S111\tround4\tpayload-absent\thttps://www.slarc.org.cn/dwyx/EN/article/downloadArticleFile.do?attachType=PDF&id=5290\t1
S112\tround4\tpayload-absent\thttps://www.slarc.org.cn/dwyx/CN/article/downloadArticleFile.do?attachType=PDF&id=5237\t3
S114\tround4\tpayload-absent\thttps://www.sinomed.ac.cn/article.do?ui=2026335073\t2
S116\tround4\tpayload-absent\thttps://aclanthology.org/N18-1074.pdf\t3
S120\tround5\tpayload-absent\thttps://c2h.niph.go.jp/tools/system/Reporting_Format_Jap_202404.docx\t3
S125\tround6\tpayload-absent\thttp://www.gcpunion.org/upload/cmsfile/1703404975484107.doc\t3
S100\tround3\tthe gate block named no locator, so no quote was checked\t#### Gate — S100\t0
S101\tround3\tthe gate block named no locator, so no quote was checked\t#### Gate — S101\t0
S102\tround3\tthe gate block named no locator, so no quote was checked\t#### Gate — S102\t0
S103\tround3\tthe gate block named no locator, so no quote was checked\t#### Gate — S103\t0
```

2. `awk -F'|' -v l='chousa' '$2 ~ ("`" l "`") && $3 ~ /round[0-9]+/ && $4 ~ /S[0-9]+/ {print $4, $5}' /home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/absent-defect-register.md`

Output:
```
 S077   `payload-absent`
 S080   `payload-absent`
 S082   `payload-absent`
 S084   `payload-absent`
 S086   `payload-absent`
 S088   `payload-absent`
 S093   `payload-absent`
 S094   `payload-absent`
 S095   `payload-absent`
 S096   `payload-absent`
 S104   `payload-absent`
 S105   `payload-absent`
 S108   `payload-absent`
 S110   `payload-absent`
 S111   `payload-absent`
 S112   `payload-absent`
 S114   `payload-absent`
 S116   `payload-absent`
 S120   `payload-absent`
 S125   `payload-absent`
 S100`   the gate block named no locator, so no quote was checked
 S101`   the gate block named no locator, so no quote was checked
 S102`   the gate block named no locator, so no quote was checked
 S103`   the gate block named no locator, so no quote was checked
```

3. `grep` whole register for `AVeriTeC`, `2305\.13117`, and `MichSchli` (three independent searches).

Each output: `No matches found`.

## Verdict
**Observed:** quarantine slice/operator output lists only the above S-rows and URLs; the requested keyword searches found no register matches. The staged target URLs are not printed by the slice and the exact target URLs were not independently extracted in this assignment. **Inference:** none of the three adopted rows is quarantined: no AVeriTeC/2305.13117/MichSchli hit exists in the register, and the listed slice targets other URLs. This conclusion is high confidence for the literal requested queries; URL-equivalence variants not containing these searched strings were not tested.

## Pointers / unresolved
- Slice producer: `/home/vgpnk/Projects/shokunin/chousa-shokunin/tools/quarantine-check.py` (invoked as requested).
- Whole-register searched: `/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/absent-defect-register.md`.
- Exact line numbers were not returned by `grep` (no matches); slice command output contains no source line locations.
- No tools installed or updated.

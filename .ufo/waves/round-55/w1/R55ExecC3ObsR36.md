# R55ExecC3ObsR36 — C3 E01–E04 independent observations

Scope: independently derived the four requested observations from the two UTF-8 `.txt` captures and located unique anchors in the target. No lane production file was changed. The W2 source is `.ufo/waves/round-54/w2/R54W2CritEntailSta.md`; it reports the latent S122 string at char 1712, the S121 byline phrase at 569 (not 575), zero occurrences for the E03 terms in either form, and two occurrences of 国家标准委 in each capture (W2 report section “Observation”, O4/O7, and inference I3).

## Independent measurements

Command run (read-only):
```sh
python3 -c 'from pathlib import Path; a=Path("/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache/adf6ba934e813b2c326fa150.txt").read_text(encoding="utf-8"); b=Path("/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache/b9ca2a4fdf9455867534f144.txt").read_text(encoding="utf-8"); t=Path("/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/knowledge/source-type-taxonomy-r36.md").read_text(); x="该标准暂无全文，请等待更新"; y="主管部门为 国家标准委"; print("E01 count=%d char=%d"%(b.count(x),b.find(x))); print("E02 char=%d"%a.find(y)); print("E03 附录=%d,%d 文献类型=%d,%d"%(a.count("附录"),b.count("附录"),a.count("文献类型"),b.count("文献类型"))); print("E04 国家标准委=%d,%d"%(a.count("国家标准委"),b.count("国家标准委"))); anchors=["the stronger claim that the text is unavailable belongs to no line here","主管部门为 国家标准委 (char 575)","the document-type taxonomy the standard prescribes","count 1 each, on one line"]; [print("ANCHOR %d count=%d text=%s"%(i,t.count(q),q)) for i,q in enumerate(anchors,1)]'
```
Observed stdout:
```text
E01 count=1 char=1712
E02 char=569
E03 附录=0,0 文献类型=0,0
E04 国家标准委=2,2
ANCHOR 1 count=1 text=the stronger claim that the text is unavailable belongs to no line here
ANCHOR 2 count=1 text=主管部门为 国家标准委 (char 575)
ANCHOR 3 count=1 text=the document-type taxonomy the standard prescribes
ANCHOR 4 count=1 text=count 1 each, on one line
```

## Draft errata lines

Target path below is relative to the lane root. Each anchor was checked against the whole target with `text.count(anchor) == 1` (shown above). Observations are `name=value` strings; the capture pair order is S121 then S122. E01's offset is a zero-based Python character offset; E02 is the exact start offset of the entire phrase.

```text
erratum: E01 corpus/knowledge/source-type-taxonomy-r36.md anchor: "the stronger claim that the text is unavailable belongs to no line here" observed: "S122_latent_no_full_text_count=1;char=1712"
erratum: E02 corpus/knowledge/source-type-taxonomy-r36.md anchor: "主管部门为 国家标准委 (char 575)" observed: "S121_byline_phrase_char=569"
erratum: E03 corpus/knowledge/source-type-taxonomy-r36.md anchor: "the document-type taxonomy the standard prescribes" observed: "附录_S121=0,S122=0;文献类型_S121=0,S122=0"
erratum: E04 corpus/knowledge/source-type-taxonomy-r36.md anchor: "count 1 each, on one line" observed: "国家标准委_S121=2,S122=2"
```

These are draft lines only; the L1 integrates them append-only under the frozen SCORECARD heading. No predicate, target, counter, or control is proposed for change. No tools were installed or updated. No build, lint, test, formatter, or counter was run.

VERDICT: Independently attacked C3 E01–E04: all four observations were reproduced, with E02's phrase start at 569 rather than its cited 575.
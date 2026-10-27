# R55W2ReviewR36Corr — R36 corrections review

## Findings

No actionable falsification found in the four corrections. I reviewed the round-55 frozen-tree copy of `corpus/knowledge/source-type-taxonomy-r36.md` at lane commit `29cfb12abd70f688b48c0d17f31e636f2d81104a`; the live file has the same correction lines (38–45).

- **E01 / third inference bullet — survives.** The frozen entry’s third inference bullet is line 24; correction line 42 names that target accurately. S122’s captured universal-newline text contains `该标准暂无全文，请等待更新` exactly once, at character 1712, on one line. It occurs in the embedded `i18n` map (`b9ca2a4fdf9455867534f144.txt:64`), not as a standard-specific notice in the captured record fields. The capture therefore supports the correction that the earlier “belongs to no line here” statement missed a string in the capture.
- **E02 / fourth observation — survives.** The target observation is line 15; correction line 43 identifies it. In S121 the phrase `主管部门为 国家标准委` occurs once at character 569, while the value `国家标准委` begins at 575. S121 lines around 169–172 show the byline text; the whole-form counts confirm the value itself occurs twice.
- **E03 / last inference bullet — survives for the assigned S121/S122 test.** The last inference bullet is line 26; correction line 44 identifies it. `附录` and `文献类型` each occur zero times in both captured forms. The entry’s S123 attribution is consistent with `source-type-taxonomy-r37.md` lines 3, 20–23 and 38–40, which cite the third-party reproduction for the normative type appendix. The assigned S121/S122 captures alone do not independently verify S123’s contents.
- **E04 / verified-at line — survives.** The target verified-at line is line 5; correction line 45 identifies it. `国家标准委` occurs twice in each whole capture, consistent with the correction’s distinction between unique quoted anchors and repeating tokens.

The four C3 key anchors each occur exactly once in the entry: `belongs to no line here`; `主管部门为 国家标准委 (char 575)`; `the document-type taxonomy the standard prescribes`; `count 1 each, on one line`.

## Evidence / verification

Read the two specified captures as UTF-8 with universal-newline handling and checked full-form `count`/`find` plus line occurrence. Observed output:

```text
ANCHOR_COUNTS [('belongs to no line here', 1), ('主管部门为 国家标准委 (char 575)', 1), ('the document-type taxonomy the standard prescribes', 1), ('count 1 each, on one line', 1)]
CAPTURE_CHECKS [('E01 S122 string', 1, 1712), ('E02 S121 phrase', 1, 569), ('E02 value', 2, 575), ('E03 S121 terms', (0, 0), None), ('E03 S122 terms', (0, 0), None), ('E04 S121 token', 2, None), ('E04 S122 token', 2, None)]
LINE_CHECKS {'S121_phrase_single_line': 1, 'S122_latent_single_line': 1}
```

Ran the requested gate against the live lane paths:

```text
python3 /home/vgpnk/Projects/shokunin/chousa-shokunin/tools/inference-ground.py --entry /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/knowledge/source-type-taxonomy-r36.md --spans /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round54/spans.tsv --counts /dev/null --registry /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/SOURCES.md --root /home/vgpnk/Projects/shokunin/chousa-shokunin
GROUND entry=corpus/knowledge/source-type-taxonomy-r36.md section=1 bullets=5 tokens=6 grounded=6
GROUND: PASS
```

## Residual risk and verification gaps

The captured S122 source establishes where the latent text occurs, but no browser rendering was performed. S123’s third-party copy is cited by the entry and corroborated as a citation in r37; its captured document was outside this seat’s specified S121/S122 review set.

VERDICT: Attacked the four round-55 R36 corrections and their anchors; they survive the specified capture checks, and inference-ground passes.

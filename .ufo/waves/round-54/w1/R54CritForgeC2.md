# R54CritForgeC2 — C2 counter falsification

## Scope and method
- Attacked only frozen C2 (depth); no C1 run, production write, or counter/control change. Read `corpus/evidence/round54/claims.md:85-140` first and treated its predicate as fixed.
- Built fixtures only under `/fast/scratch/hyaku/chousa-r54/R54CritForgeC2/root-*`; exported `TMPDIR=/fast/scratch/hyaku/chousa-r54/R54CritForgeC2/work` for every counter run. Sources were the four on-disk `.qcache` captures; no fetch/network or tool install.
- Commands exercised: `python3 build.py <profile>`; `python3 /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round54/build-spans.py --root <scratch-root> --cache /home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache`; then `python3 /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round54/c2-count.py --root <scratch-root>` (also `--lane-only` where noted). The builder and counter were run only against scratch roots.

## Cheapest passing shortcuts

The following are exact, once-occurring, one-line capture quotes (UTF-8 `.txt` sidecars; offsets are `text.find`):

| Capture | Quote | char offset | count |
|---|---|---:|---:|
| SAMR `adf6ba934e813b2c326fa150.txt` | `Toggle navigation` | 166 | 1 |
| openstd `b9ca2a4fdf9455867534f144.txt` | `<title>国家标准|GB/T 7714-2025</title>` | 152 | 1 |
| JMU `0f33243fd7ac2fe88b85c1ba.txt` | `附录Ａ（规范性） 文献类型和文献载体标识代码…………………………………………………………２８` | 2512 | 1 |
| SAMR reuse | `本标准非等效采用ISO国际标准：ISO 690:2021。` | 1797 | 1 |
| openstd reuse | `该标准采用了ISO、IEC等国际国外组织的标准，由于涉及版权保护问题，本系统不提供文本阅读服务` | 15188 | 1 |

The JMU quote is the appendix-A **contents line**, not operative text. The boilerplate fixture also used unique SAMR `主要起草单位` / `执行单位`, openstd `<meta>` / HTML-comment lines, and two other full JMU TOC lines. `build-spans.py` accepted all nine exact-unique quotes: `SPANS_ROWS=9 WRITTEN=9`; after aligning the scratch anchors to its emitted quote offsets, the counter output included `CAPTURE_BOUND=9/9`, `SUBSTANCE=PASS`, `ANCHOR_BOUND=3/3`, `INFERENCE_GROUNDED=2/2`, `QUARANTINE_VERDICTS=3/3 (S080,S088,S096)`, `C2=PASS`.

The same boilerplate fixture’s inference bullets deliberately overclaim from those quotes (scratch `root-boilerplate/...r36.md:18-19` says the navigation label proves adoption basis/status and the HTML title proves full-text publication; `...r37.md:15` says a TOC line proves the operative carrier requirement). `INFERENCE_GROUNDED=2/2` still passes. These are counterexamples to semantic support, not claims about the sources.

**Duplicate quote / one-anchor shortcut:** scratch `root-reuse/.../spans.tsv:2-10` has the same quote, digest, and capture offset repeated three times per bound ID. The actual builder emitted the repeated rows and printed each same quote offset three times (`S121 char 1797`, `S122 char 15188`, `S123 char 2512`; `SPANS_ROWS=9`). Counter excerpt: `QUOTE_ROWS=9 ON_BOUND=9/9`, `SPAN_IDS=3/3 (min 3 each)`, `CAPTURE_BOUND=9/9`, `SUBSTANCE=PASS`, `ANCHOR_BOUND=3/3`, `C2=PASS`. Each Registry anchor had only one `char N`. Thus the counter counts rows, not distinct quote evidence, and a single real anchor location satisfies the row’s anchor requirement.

**Opposite inference:** scratch `root-opposite/...r36.md` quotes the captured openstd notice stating that text reading is not provided, then asserts that the portal serves the full operative text openly. Observed counter excerpt: `CAPTURE_BOUND=9/9`, `INFERENCE_GROUNDED=2/2`, `QUARANTINE_VERDICTS=3/3 (S080,S088,S096)`, `C2=PASS`. The lexical grounding/polarity check did not establish entailment.

**Held S101 wrong anchor:** scratch `root-held-anchor/corpus/SOURCES.md:111` sets S101’s anchor to `char 999999` and its `used-by` includes `corpus/knowledge/source-type-taxonomy-r37.md`. Observed `HELD_CITED=S101 HELD_BAD=0`, `ANCHOR_BOUND=3/3`, `C2=PASS`. The anchor loop is limited to bound IDs (`c2-count.py:239-243`); the held check validates citation/backlink only (`:184-197`).

**Refusing openstd:** the scratch fixture removed the S122 row and source line, and named its URL on a `refused-doc` line. Observed `BOUND=2/3 (min 2) REFUSED=1`, `CAPTURE_BOUND=6/6`, `ANCHOR_BOUND=2/2`, `QUARANTINE_VERDICTS=3/3 (S080,S088,S096)`, `C2=PASS`. This is allowed by the frozen minimum and refusal accounting (`claims.md:119-137`, `c2-count.py:167-182,291-295`), not a counter defect against that threshold.

**Mode distinction:** an invented digest yielded `CAPTURE_BOUND=8/9`, `C2=FAIL` in the ordinary run, but the same fixture with `--lane-only` yielded `CAPTURE_BOUND=skipped`, `SUBSTANCE=PASS`, `C2=PASS`. The counter documents that mode as lane-bytes-only (`c2-count.py:229-232,285`); it is not a full re-grounding result.

## Shortcuts refused by the frozen legs

| Probe | Observed output | Refusing leg |
|---|---|---|
| One-character quote `A` | `SUBSTANCE=FAIL`, `C2=FAIL` | `quote-substance-check.py:26,49-53` minimum 3 non-space chars |
| Full SAMR capture used as a span | `CAPTURE_BOUND=9/9`, `SUBSTANCE=FAIL`, `C2=FAIL` | span-width floor (`quote-substance-check.py:54-57`) |
| One invented digest, ordinary mode | `CAPTURE_BOUND=8/9`, `SUBSTANCE=PASS`, `C2=FAIL` | capture-file digest/slice check (`c2-count.py:229-232`) |
| Bound S121 anchor set to `char 999999` | `ANCHOR_BOUND=2/3`, `C2=FAIL` | anchor must match a located quote offset (`c2-count.py:239-243`) |
| Multiline quote in TSV field | `QUOTE_ROWS=10 ON_BOUND=8/10`, `QUOTES_IN_SPAN=8/10`, `SUBSTANCE=FAIL`, `C2=FAIL` | newline splits the manifest row; this was not a valid one-line quote fixture |

## What closure must still spot-check

- Hand-check claim entailment and source scope, not just capture identity: boilerplate, navigation labels and TOC headings are real capture bytes but do not establish the entry’s operative claims. Check each cited quote in context and whether the entry’s inference follows from it. `inference-ground.py` tests token presence and lexical polarity; the frozen claim explicitly says the counter does not measure entailment (`claims.md:138-140`).
- Check quote adequacy/diversity: three identical rows are three rows, not three distinct evidentiary passages. No predicate change is proposed; Gate reviewers should decide whether the repeated passage actually supports the entry’s scope.
- Re-open the held S101 anchor/backlink by hand: the counter’s S101 branch does not validate its anchor, only the `source: S101` citation and `used-by` relationship.
- Hand-adjudicate all three quarantine records: S080/SAMR, S088/JMU, S096/HIT. The scratch verdicts were synthetic `present` labels, not findings. `QUARANTINE_VERDICTS=3/3` is only a parsed-label count; the real closure must substantiate each verdict and ensure no bound document is fabricated/unverifiable.
- Run the ordinary counter for capture grounding; do not substitute `--lane-only`. Review the permitted openstd refusal in the Gate and ensure the surviving two-document coverage still supports the entry.
- Keep per-entry province, QUALITY bar and coverage-map judgment in the lesson Gate; they are expressly outside this counter (`claims.md:138-140`).

**Smallest safe correction:** leave the frozen predicate/counter untouched; require closure’s Gate spot-check to record substantive quote-to-claim entailment, duplicate-quote adequacy, the held S101 anchor, and evidence for the three quarantine verdicts. Impacted axis: C2 depth; C1 operability was not exercised.

VERDICT: C2’s ordinary counter was falsified as a semantic/coverage oracle—boilerplate, duplicate rows, opposite inference, wrong held anchor, and permitted two-of-three refusal all print PASS; structural digest, substance, and bound-anchor guards refuse their respective attacks.

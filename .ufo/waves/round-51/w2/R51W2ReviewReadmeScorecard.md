# R51W2ReviewReadmeScorecard — README appended block, SCORECARD tail, SHONEN tail

Attacked: `corpus/README.md:1085-1111` (`## Round51 coverage and frontier` → EOF), `SCORECARD.md:2622-2629` (`## Round 51 pointer corrections`), `SHONEN.md:10`. Tip `4436e27`; base
`9ec1751a…`. Read-only outside this report; scratch `/dev/shm/chousa-r51-R51W2ReviewReadmeScorecard` (symlink mirror + two file copies) deleted at the end; counters run with `env
-u ASSIMILATE_CITES`; no network, no install.

## 1. The block's own counts, re-run
```
$ env -u ASSIMILATE_CITES python3 corpus/evidence/round51/c3-count.py            # rc=0
CAP_ROWS=36 (base 36) / POINTERS=74 (base 74) / RESOLVED_BY_CORRECTION=4 / DANGLING=0 / C3=PASS
$ env -u ASSIMILATE_CITES python3 corpus/evidence/round51/c1-count.py            # rc=0
SELFTEST_DEFAULT=PASS … REGISTRY_STRUCTURE=PASS 4/4 / LEGS=5/5 / C1=PASS
$ env -u ASSIMILATE_CITES python3 corpus/evidence/round51/c2-count.py            # rc=0
ENTRIES=3/3 / BOUND=6/7 (min 5) REFUSED=1 / BOUND_IDS=S107,S108,S109,S110,S111,S112 /
QUOTE_ROWS=61 ON_BOUND=61/61 CAPTURE_BOUND=61/61 SPAN_IDS=6/6 / QUARANTINE_VERDICTS=6/6 / C2=PASS
```
`README.md:1093`'s capture loop prints a `<the six source URLs…>` placeholder; I substituted the URL cell of rows `S107`–`S112` and ran it verbatim (`[ -s "$Q/$k.txt" ]`):
`CAPTURES=6/6`. Its base claim, both halves:
```
$ git grep -l -e 検索式 -e 検索期間 -e 检索策略 9ec1751a24231e899ceea4688e21c8edf6046d35 -- corpus/knowledge; echo rc=$?
rc=1                                    # prints nothing: holds
$ git ls-tree -r --name-only 9ec1751… -- corpus/knowledge | wc -l
69
```
"each entry holds its own term — 検索式, 检索策略, 検索期間 respectively": `grep -c` per entry file gives `6 / 6 / 4` individually (not one term satisfying all three). Holds.

Six vs seven: `sed -n '1085,1111p' corpus/README.md` → `six documents` ×5, `seven`/`seventh` ×1 (the refused docx), `S107`–`S112` ×1. `SOURCES.md:295` → "opened the 7 documents …
included 6 documents (S107–S112), refused 1". Tip registry `grep -cE '^\| S[0-9]{3}' corpus/SOURCES.md` → `112`, last row `S112`, `grep -c '^| S113 '` → `0`.
`lessons/round-51.md:41` "seven rows (S107–S113, before the NIPH `.docx` was refused)" is a labelled pre-refusal scratch mirror. **No place claims seven held.** Six rows are six
documents: `SOURCES.md:119-120` are 实验动物与比较医学 45(4):496-507 and 45(1):101-111 (two rows, one journal); `:117,:118,:121,:122` four more.

## 2. SCORECARD tail (four corrections) — load-bearing, appended, semantically right
```
$ for n in 1843 2073 2074 2616; do sed -n "${n}p" SCORECARD.md | grep -o -E '`[^`]*(measure/final/|measure-l1/[^`]*|c1-supplement\.py)[^`]*`'; done   # 4× as run, one row per call
`measure/final/`   `measure-l1/c1-s36361.json`   `measure-l1/c2-s36371.json`   `c1-supplement.py`
targets: dir 9 files / 7039 B / 4069 B / 4175 B        (all non-empty)
```
Semantics, not just existence: row 2073's sibling pointer is `corpus/evidence/round36/c1-count.py` and the JSON now named carries `"label": "ENGINE_SWAP_CANARY=14/14"`; 2074's
carries `"label": "WITNESS_PER_RECORD=5/5"`. Row 1843's own sibling pointer is `corpus/evidence/round32/c1-count-v2.py`, so `round-32` — not the also-existing
`.ufo/waves/round-33/measure/final`, whose files are `c1v2-s3701.json…` — is the right directory. Append-only: `git diff 9ec1751..4436e27 -- SCORECARD.md | grep '^-'` → no lines
(same for `corpus/README.md`). Mutation test (mirror root: symlinks + copies of SCORECARD/SHONEN):
```
drop `correction: SCORECARD.md:2073 …`     → RESOLVED_BY_CORRECTION=3  DANGLING SCORECARD.md:2073 measure-l1/c1-s36361.json  C3=FAIL rc=1
also revert SHONEN:10 to the base pointer  → adds DANGLING SHONEN.md:10 round25-meta-differential.log                     C3=FAIL rc=1
```
All four corrections and the SHONEN repair are load-bearing; C3 does not pass vacuously.

## 3. SHONEN tail
`git show cf642c6 -- SHONEN.md` → `SHONEN.md | 2 +-`, one line: `round25-meta-differential.log` → `corpus/evidence/round25-meta-differential.log`, which resolves (47 B; the only
other copies are `.ufo/waves/round-4{3,5}/assimilation/validate/…` mirrors, so this is the canonical file). `git show 4436e27 -- SHONEN.md` → empty, so the adoption commit did not
touch it; `POINTERS=74 (base 74)` fits a repair, not an addition.

## 4. The S125 refusal claim and its provenance
Holds: the two text forms the frozen tools read locate nothing (`R51GroundNiphB.md:7-24`: `.txt` is the zip bytes decoded with replacement, 168952 chars / 72117 U+FFFD;
`.raw`-as-UTF-16LE 0; `R51ExecCaptureForm.md` §3-4: `.txt` 0, UTF-16LE 0, `word/document.xml` 2). Gate flip `lessons/round-51.md:56` (`## Gate`, heading line 33): "a counter and
span builder that read a zip member". `README:1106` holds: `ls .qcache/f3dbe2fe59a684b1b94cfadc*` → only the 6-byte `.fail`; the package's JPT row exists
(`merge/chousa/SOURCES.append.md:54`, S129 "**original withdrawn** … **archived at**"), so "not one of this theme's six documents" holds. Carried quotes: `README:1089`'s
hand-searching "presence and method" — `.qcache/62be15a474e866e4bef6c9d5.txt` (form: the `.txt` read as UTF-8) holds `ハンドサーチを実施した場合はその方法を記載する。` once, char 4226. `README:1105`'s searcher claim —
`検索者` 3 / 0 / 0 in the S108 / S107 / S112 captures.

## 5. "Not held at base"
`git ls-tree -r --name-only 9ec1751… corpus/knowledge | grep -Ei 'sweep|log|record|search'` → `search-log-method-r39.md`, `sweeps-rejections-r5.md`, `sweep-symlink-r19.md`,
`claim-record-fields-r33.md`, `per-record-argv-attribution-r36.md`; so `README:1099` "search-log ground has been one document (`S078`)" and `:1101` "the lane held none [non-Western
field rules]" hold (the rc=1 grep above is the same test). Pointers that resolve: `search-log-method-r39.md:6` ("The filename is the package's label, not a lane round number"),
`lessons/round-43.md:43`, `lessons/round-47.md:251` ("**refused again** … 267-byte `Client Challenge` page"), `corpus/README.md:390-391`,
`lessons/round-50-verifier-spotcheck.md:93`, `knowledge/istic-citation-verification-r39.md:6`. `README:1111` reproduces: `文献情报中心` 3, `ISTIC` 0, `中国科学技术信息研究所` 0 in
`.qcache/001287c436f0e6b1d166ae8d.txt`, and that key = `sha256(b'https://chaxin.las.ac.cn/service/citation-search')[:24]` = S104's URL, so the grep is over the right file.

## 6. Defects (lines + observed values)
**D1 — calibration, definite. `corpus/README.md:1099` and `:1101` cite `corpus/SOURCES.md:279`; line 279 is round 42.** `sed -n '279p'` → `  Identified 24 quarantined quotes over
the lane's 24 register rows, screened 24,`; `sed -n '286p'` → `Identified 3 candidate entries on the search-log theme, screened 3, included 1 (S078 … excluded 2. Rejected
search-log-fields-r36.md … Rejected search-tracking-record-r40.md: the column-allocation sentence is not a contiguous span …`. Both statements the README attributes to 279 sit on
286. Smallest fix: `:279` → `:286` twice.

**D2 — provenance, definite. `README.md:1107` "a national institute's own submission form".** `R51GroundNiphA.md:64-67` finds the opposite: `the end-of-window rule names
製造販売業者による分析提出 … Company is 厚生労働省. It governs manufacturers' submissions to the MHLW cost-effectiveness scheme, not NIPH's own assessments`; `:47` (q8) calls the document a
**reporting format + handbook** (`…記載様式と手引`), "not a bare 'submission form'". `R51GroundNiphB.md` Limits: "Whether the requirement binds applicants (MHLW programme) or only the
institute was not tested." "Not for its source quality" is supportable; "its own" asserts what the round refuted. Smallest fix: "a national institute's 記載様式 and handbook for
drug/device cost-effectiveness submissions (filled by manufacturers, filed with the MHLW)"; same descriptor at `:1091`, `:1093` ("submission form" → "format and handbook").

**D3 — calibration, definite. `README.md:1093` "it carries no id".** The refused document carries staged `S125` and quarantine row `S120`; what it lacks is a *lane* id:
`lessons/round-51.md:39` "staged S125 refused (no lane id)", `:56` "(staged S125, quarantine row S120)". Smallest fix: "it carries no lane id".

**D4 — depth/calibration, definite. `README.md:1090` headline "that China has no standard for one yet".** Carried is narrower: `.qcache/fd468a36d78ff156b6200946.txt` (form: the
`.txt` read as UTF-8) has `尚无专门针对动物实验 SR 的报告规范` once at char 17709 and `尚缺乏统一标准` once at char 9836 — neither says China lacks a standard for a search record, and the paragraph's
own detail clause already narrows it. Smallest fix: "…and that the Chinese reporting document states no dedicated reporting standard exists yet for animal-experiment systematic
reviews".

**D5 — wording risk for the wave-3 draft (not a landed defect).** The four SCORECARD lines are appended; the SHONEN change is in place (`1 insertion, 1 deletion`). Any text saying
"one appended SHONEN line" (the wave brief's phrasing) would be false; write "one SHONEN pointer repaired".

**D6 — C3's scope, named so wave 3 cannot over-claim.** `c3-count.py:63-79` reads only the third cell of `## Capabilities` rows and SHONEN's indented lines; README pointers are
outside the predicate, which is why D1 passes `C3=PASS`. "Every pointer added this round was checked" is false for the README block. Narrow but true: `README:1107` "did not reach
中国科学院文献情报中心" — the lane holds that institution's S104 page; `标准` occurs 5× there and all five are fee words (收费标准 at 408/415/644, 收费说明 646, 自引标准统计 555), so only "its guidance" is
accurate.

VERDICT: attacked the six/seven counts, the README:1090-1111 pointers, the four SCORECARD corrections by mutation, the SHONEN repair and the S125 refusal claim — every count
reproduces (CAPTURES=6/6, base rc=1 / 69 files, C1/C2/C3 PASS, corrections load-bearing, six not seven everywhere, `検索者` 3/0/0, istic 3/0/0, hand-search method carried at char
4226) and four statements break: `SOURCES.md:279` twice (should be 286), "its own submission form", "carries no id" (it lacks only a lane id), and the 1090 headline outrunning its
span; the SHONEN change is a repair, not an appended line.

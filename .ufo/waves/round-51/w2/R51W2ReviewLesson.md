# R51W2ReviewLesson — section-by-section attack on `corpus/lessons/round-51.md`

seat: R51W2ReviewLesson · 2026-10-25 · lane tip `4436e279b91d8d68fd439c9095695035fbeeab74` (HEAD `72566c8` adds only w2 spec/dispatch files; the lesson is unchanged since the tip)
form: `.txt` = `open(path, encoding="utf-8")` (universal newlines — what `build-spans.py:123` and `c2-count.py` read); DEINT = the formula at `.ufo/waves/round-51/w1/R51ExecQuarantine.md:45-47`. Nothing written but this file; no install; scratch `/dev/shm/chousa-r51-ReviewLesson` deleted at the end.

## What holds (re-ran, not re-read)

| check | observed |
|---|---|
| collision, l.37 | `wc -l` reg-ids 106 / staged-ids 114 / collisions 25; `comm -12` = 25; `diff <(seq -f 'S%03g' 1 106) <(sort reg-ids)` = 0 and S082–S195 = 0; extended to S001–S112 = 31 (S082–S112) |
| identity vs numbering | lane/staged S100–S102 URL cells identical; staged S105/S106 own-work, lane S105/S106 the CNKI manuals; guard proof pattern A `count=1` vs column-zero `count=0`, tool `COLLISIONS=1` |
| renumber map, l.39 | staged S109/S110/S116/S117/S119/S126 URLs+titles = landed S107…S112 (`SOURCES.md:117-122`); S125 has no row; S133's URL hash `453d492becd9a2f4632cb8dd` = the capture the table calls S111's document |
| decisions, l.64-70 | S082 key `01f657b3…` = "Client Challenge"; S083 `14aaa168…` 210,708; S090 landing `参照` 0, PDF `58b1b564…` char 3785; S134 27,659 / char 1334; amendment 8,804 / 6,179; S129 5,328 / char 641, `検索者` 0, `項目7` 0, `検索戦略 7` present, key `f3dbe2fe…` only a `.fail`; S142 19,352, entry 2,253 chars, 1 backtick, 0 double-quote; the PRISMA-S item-8 string 0 hits in all 2,549 `.txt`; body ids S069/S094/S114/S130 and S071/S072/S079 name the stated documents |
| quarantine verdicts | S120 `SRにおける文献検索期間について明記する。` at 39,411 in the unzipped `word/document.xml` (1,224 paras, 55,839 chars); S114 strings inside comment 9,192–9,908 and 0 in the rendered text; S105 part at 4,192; S107's sentence sits before the footer reading 122 |
| refused .docx, l.54-56 | `.txt` 168,952 chars, 72,117 U+FFFD; `文献検索期間`, the worked-example string and `PRISMA flow chart` 0; the example is two cells (`文献検索期間` \n `2015年1月から2018年10月まで`) |
| 61-quote table, l.91-157 | all 61 exact `find` offsets, count 1, ≤160 chars, ≤25 words, in the citing entry and the lesson; `quotes.tsv` = the table (0 symmetric difference). e.g. `灰色文献的检索与记录` at char 15310 in S109's `.txt` (UTF-8) |
| C1 instrument | real tool `LEGS=5/5 C1=PASS`; supplement `6/6 PASS`; forge-dirname 5/5 frozen vs 1/6 supplement; candidate1 5/5 vs 3/6; `ASSIMILATE_CITES=all` → 3/5 FAIL; `--seed 13` hangs (timeout 25 → 124); round-50 forge with REAL=ec52e632 (sha256 `bff32c11…`) → 5/5 PASS; l.16's three counters fail at tip and `--tool ec52e632` restores 3/3 and 5/5 |
| C3, l.17 + row 5 | tip `DANGLING=0 C3=PASS`; before 5; pre-erratum 8 with the two `ufo/…` false positives; tokenizer diff at `c3-count.py:54`; DOTPATH `CAP_ROWS=37 POINTERS=75 DANGLING=0 PASS` |
| Census, l.167-175 | exit 0 `ok`, exactly the five W04 (S051 S053 S073 S074 S075), 112 rows, tiers A98/B9/C5; base 106; SOURCES.md +8/−0 |
| SHONEN, names, README | four `[~]` boxes; `SHONEN.md:10` pointer resolves (47-byte file); `NAME_COLLISIONS=0 ITEMS=48`, every name `R51…`; README correction at 1,111 |

## Defects (lesson line · claim · observed · smallest safe correction)

**D1 — l.27 and l.14: the C1 after-measurement does not exist.** `ls corpus/evidence/round51/measure-after.txt` → No such file; `git log --all --oneline -- corpus/evidence/round51/measure-after.txt | wc -l` → 0; `receipt-check.py` with no argument → `CHECKS=0 OK=0 FAILS=0` / `RECEIPT_CHECK=PASS` (it passes on zero receipts), while on both landed receipts (`measure-r50-at-tip.txt`, round50/measure-after.txt) → `RECEIPT_NO_REV … FAIL` rc 1, so `RECEIPT_OK` is printed for no landed receipt at all; `grep -rl 'tool-rev:' corpus/evidence` finds only `receipt-check.py`'s docstring. C1's frozen target ("three independent runs") has no receipt at the tip. Fix: file the after-receipt, or restate l.27/row 1 as "not filed"; never let a zero-argument invocation stand as pass evidence.

**D2 — l.27 (and QUALITY 84): `--skill` cannot see the row it validates.** `SKILL.md:130` carries `tool-rev: cf642c669b73… tool: tools/assimilate-rows.py digest: sha256:6b975f91…`, yet `receipt-check.py --skill SKILL.md` → `SKILL_NO_PIN … FAIL` rc 1 because `header()` reads `splitlines()[:5]`; the same line at line 3 of a scratch copy → `SKILL_PIN_OK … rev=cf642c669b73` PASS. QUALITY 84's "shown able to fail … SKILL_NO_PIN" is a counter false negative, so the check cannot verify the pin it was written for. Fix: scan the `## Gates` table (or take a line number), and restate that QUALITY example.

**D3 — l.27: "zero differing lines against `measure-after.txt`" is false.** `diff corpus/evidence/round50/measure-after.txt corpus/evidence/round51/measure-r50-at-tip.txt | grep -c '^<'` → 68; the tip file has 4 `$` blocks against the receipt's 13, so 9 blocks were not re-run (`c2 --lane-only`, cjk-ground-check, decode-form-check, build-spans `--check` ×2, quote-substance-check, round47 `c2 --list`, census, `grep -cE rows`). `SKILL.md:135` says "five blocks"; the file has four. Fix: name the four blocks and say the other nine are not re-measured at the tip.

**D4 — l.14 row 1: the fix's own check is still red.** `head -1 corpus/evidence/round50/measure-after.txt | grep -qE '[0-9a-f]{7,40}'` → exit 1; `! grep -q 'ec52e632' SKILL.md` → exit 1 (matches :132 and :135). "both exit 0 after the fix" is unreachable with an append-only correction. Fix: `grep -q 'landed tip .1d7aba0948cf' SKILL.md` (observed true) and point the first command at a receipt that carries the header.

**D5 — l.15 row 2: no landed counter meets "a fixed counter must print `C1=FAIL` for both".** The cheat scores `LEGS=5/5 C1=PASS` on the round-50 counter (REAL=ec52e632) and again on the round-51 frozen counter (`--tool corpus/evidence/round50/controls/forge-tool.py` → `LEGS=5/5 C1=PASS` exit 0); only `c1-supplement.py` fails it (`1/6`). Fix: name the supplement as the fixed counter and cite its 1/6, or drop the sentence.

**D6 — l.17 row 4: "identical at the tip and at the base tree" is false.** Tip: `CAP_ROWS=36 POINTERS=74 RESOLVED_BY_CORRECTION=4 DANGLING=0 C3=PASS` exit 0; the `DANGLING=5 … FAIL` state exists only at the base tree (`controls/c3-before-erratum.txt`). Fix: "at the base tree", citing the before file.

**D7 — l.19 row 6: the fix's check cannot turn green.** The row's `awk` → `DRIFT_MISSING` at the tip; the note landed as `correction: corpus/README.md:1078 …` at README:1,111, which the awk never reads. The row's capture also says "`ISTIC` and `filename drift` occur 0 times in README.md"; `grep -c ISTIC corpus/README.md` → 1 (inside that correction line). Fix: check the correction line (`grep -q 'correction: corpus/README.md:1078' corpus/README.md`) and drop the zero-occurrence clause.

**D8 — l.16 row 3: pointer off by one.** `claims.md:56-58` is the antecedent; the quoted sentence "…`LEGACY_ALL` is what preserves their behaviour." is line 59 (`grep -n LEGACY_ALL` → 41,43,48,59). Fix: `:59`.

**D9 — l.20 row 7: the numbers are the round-50 tip's, unnamed.** Tip `grep -cE rows corpus/SOURCES.md` → 14; `grep -cE '^\| S[0-9]{3} '` → 112; at `1d7aba0948cf` → 13 and 106. The row reproduces the drift class it names. Fix: pin `1d7aba0948cf` or use `<rev>:corpus/SOURCES.md`.

**D10 — l.8 vs l.77/81/83: three quarantine offsets are in an undefined form.** l.8 says every `char N` is an offset into the `.txt` read as UTF-8; S104/S111/S112 say `form DEINT`. In the `.txt` the S104 quote occurs 0 times; under the DEINT formula at `R51ExecQuarantine.md:45-47` the three quotes occur once at 8497 / 3008 / 22632, not 8233 / 2882 / 21691 (the report's own probe `このプロセスに際して，誰が検索を行ったの` moves 3225 → 3452). Fix: exclude DEINT rows in l.8's sentence and re-derive the three offsets with the shipped DEINT code.

**D11 — l.181: the disclosure omits a post-freeze change to the C3 control builder.** `git diff d603f6f… 4436e27… -- corpus/evidence/round51/controls/build-c3-controls.py` adds the DOTPATH positive control and makes the three negative controls start from BASE; `controls/c3-controls-final.txt` (DOTPATH `CAP_ROWS=37 POINTERS=75 DANGLING=0 C3=PASS`) is named nowhere in the lesson, and E1 mentions only the tokenizer. Fix: one E-bullet naming the builder change and its receipt.

**D12 — l.165: the implemented check has no passing target, and the tally does not reconcile.** `open-items-age.py .ufo/waves/round-50/w2/R50ScribeReportDraft.md --round 50` → `FAIL … (8 rounds)` rc 1 (as claimed), but there is no round-51 report (`find .ufo/waves/round-51 -iname '*report*'` → `w2/R51W2DraftReportOutline.md`), and on the lesson it prints `FAIL … (9 rounds)` rc 1 — so the claimed `PASS` is unbacked. The status column gives 31 rows = 19 IMPL + 10 FMT (two FMT rows carry an OPEN remark) + 2 OPEN, not 19/9/3. Fix: name the report as the target and land the line with it; recount from the status column.

**D13 — l.167 / `SOURCES.md:117`: the S107 row's pages exclude the bound page.** Row says `32(2):120-121`; the capture's footers read 120 @9274, 122 @13779, 124 @21167, and the entry corrects the staged p.121 to "the page whose footer reads 122". Fix: re-derive the range (the capture ends on 124) instead of inheriting the staged range.

**D14 — l.64: `267 chars` is a byte count.** `01f657b3…txt` = 267 bytes, 265 UTF-8 characters (two multi-byte glyphs); the other sizes in the table are character counts. Fix: 265.

## Not falsified / unverifiable

l.37 "The staged file digest is the package's own" — no digest field in `MERGE-REPORT.json` and no command given; the 25/31/identity/clash numbers beside it hold. Row 8's supplement numbers (1/6, 3/6, 0/6) and E2–E4 hold; `c1-count.py` and `c2-count.py` are byte-unchanged from the freeze (`git diff` shows only `c3-count.py`, E1).

VERDICT — attacked all seven sections line by line (pointers, fixes, four decisions, quarantine, census, disclosure): 14 defects, worst that the C1 after-receipt cited at l.27/l.14 does not exist, `receipt-check.py` passes on zero receipts and cannot read the SKILL row it validates, and "zero differing lines" is a 68-line diff with 9 of 13 receipt blocks un-rerun; the collision/renumber/decision/quarantine substance, all 61 quote offsets, the refused-doc paragraph, C3, census and the supplement controls hold.

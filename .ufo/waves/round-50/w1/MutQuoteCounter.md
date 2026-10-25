# MutQuoteCounter — round-50 w1 mutation probe: span builder + C2 quote legs

Axes: C2's quote legs (calibration = which leg catches which mutant) and the span builder's
derivation check. C1 untouched. No tool installs (none needed; pacman paused, nothing attempted).

## Fixture (synthetic, self-labelled; scratch /dev/shm/chousa-r50-MutQuoteCounter — deleted after)
`--root` tree: quotes.tsv (6 rows), derived spans.tsv + spans/, three synthetic entries
(r40/r41/r39, each with `source:` line + one Inference bullet), synthetic lesson (6 quotes +
2 refused-doc lines for SEU/BNU), 2-row registry (S105/S104, `mined`, `2026-10-25`, anchor
cells `char 30738, char 30793` / `char 422, char 194`). Detectors ran from lane copies so
`LANE`/git resolves to the real repo (read-only `git show`/`git grep`); per tasking the three
round50 scripts + tools/ were copied into the tree (c2-count executes the scratch
quote-substance-check, byte-identical). Pre-checks: `git -C <lane> show
3c51da77…:corpus/SOURCES.md | grep -cE '^ {0,3}\|[ \t]*S10[45][ \t]*\|'` → `0`; `git grep -l
-e 引文核对 -e 引证检索 3c51da77… -- corpus/knowledge` → rc=1. Capture keys re-derived:
SXU→`e3ca8f4fdd15420b80096a75`, ISTIC→`001287c436f0e6b1d166ae8d`; both .txt LF-only.
Quotes (form: the `.txt` read as UTF-8 errors=replace; each count==1 in that form;
offset=`text.find`), byte-exact:
- S105 `引文核对是指，以“中国知网”的文献资源为核对源内容，将输入的引文内` off 30738 len 33
- S105 `把待检测文献的参考文献复制到“引文核对”文本框，点击“搜索”按钮，` off 30793 len 33
- S105 `该列表的第一列显示的是是否查找到该引用文献，及引文内容的正确性` off 30901 len 31
- S104 `证明费 300 元/份。提供 1 份证明，需要多份证明，增加 1 份 50 元` off 422 len 39
- S104 `论文收录引用检索（简称引证检索）指通过检索SCI、SSCI、EI、ESI、CSCD等国内外评价类数据库，查询个人、团队等的代表性论著收录和引用情况` off 194 len 73
- S104 `所有文章必须包括全部作者（全拼）、标题、期刊、年、卷、页码、DOI等完整信息` off 1380 len 38

## Pristine baseline — every quote leg green
- `python3 <lane>/corpus/evidence/round50/build-spans.py --root $R` → `QUOTE S105 char 30738/
  30793/30901`, `QUOTE S104 char 422/194/1380`, `SPANS_ROWS=6 WRITTEN=6`, rc=0;
  `--check` → `SPANS_ROWS=6 STALE=0` rc=0; `quote-substance-check.py $R/…/spans.tsv` →
  `IDS=2 QUOTES=6 FAILURES=0` rc=0.
- `python3 <lane>/corpus/evidence/round50/c2-count.py --root $R [--lane-only]` →
  `ENTRIES=3/3 BOUND=2/4 (min 3) REFUSED=2 BOUND_IDS=S104,S105 REF_ID_UNBOUND=0
  NEW_GROUND=3/3 QUOTE_ROWS=6 ON_BOUND=6/6 SPAN_IDS=2/2 QUOTES_IN_SPAN=6/6
  QUOTES_IN_ENTRY=6/6 QUOTES_IN_LESSON=6/6 QUOTE_SHORT=6/6 SPAN_CONTEXT=6/6
  CAPTURE_BOUND=6/6 (skipped lane-only) SUBSTANCE=PASS ANCHOR_BOUND=2/2
  INFERENCE_GROUNDED=3/3 QUARANTINE_VERDICTS=0/0` rc=1.
Declared before data: pristine `C2=FAIL` is structural scope, not a detector fault — the probe
holds two documents (tasking: two ids) and frozen MIN_BOUND=3 needs three; the bounded
behavioral detector here is the per-leg counters + substance rc + builder rc. Register has no
theme-URL rows (`grep -c 'sxu\|chaxin\|rwxy.seu\|bs.bnu'` → 0), so QUARANTINE is 0/0 trivially.

## Mutants (disposable copies; pristine tree never mutated)
| mut | smallest point | substance | c2 lane-only | c2 full | builder --check |
|---|---|---|---|---|---|
| a | S105-1 offset 30658→30659 | rc0 PASS | ANCHOR 1/2 KILL | ANCHOR 1/2 + CAPTURE 5/6 KILL | STALE=1 rc1 |
| b | S104-2 digest last char flipped | rc0 PASS | ALL GREEN **SURVIVOR** | CAPTURE 5/6 KILL | STALE=1 rc1 |
| c | S105-2.txt context char0 → 囗 (len same) | rc0 PASS | ALL GREEN **SURVIVOR** | CAPTURE 5/6 KILL | FILE_STALE rc1 |
| c′ | S105-2.txt quote char80 → 囗 | rc0 PASS | IN_SPAN 5/6 + ANCHOR 1/2 KILL | + CAPTURE 5/6 KILL | STALE=1 rc1 |
| d | S104-1 quote → `证明` (2 chars) | HOLLOW_QUOTE+OVERWIDE_SPAN rc1 | SUBSTANCE=FAIL KILL | SUBSTANCE=FAIL KILL | STALE=1 rc1 |
| e | S105-3.txt → whole 38174-char capture | OVERWIDE_SPAN rc1 | SUBSTANCE=FAIL KILL | + CAPTURE 5/6 KILL | FILE_STALE rc1 |
| f1 | 2x quote at build time | n/a | n/a | n/a | REFUSED rc1, nothing written |
| f2 | same quote as 7th hand manifest row | rc0 PASS | ALL 7/7 **SURVIVOR** | ALL 7/7 incl CAPTURE_BOUND=7/7 **SURVIVOR** | ROW_EXTRA+ORPHAN rc1 |

f1 (scratch cache copy of the 4 capture files, bytes unmodified — the chosen string occurs 2x
natively, `count==2`, first off 16853): `build-spans.py --root $R/root-f --cache $R/cache-f`
→ `build-spans: refused S105: quote not exactly once in any form (e3ca8f4fdd15420b80096a75
.txt:2x, e3ca8f4fdd15420b80096a75.raw:0x): '第 2 部分：各项检测结果，包括文字复制比结果、跨
语言检测结果、校内互'` rc=1; no spans.tsv and no spans/ created.
f2: hand row `S105 <SXU> 2197abe27dad… 16773 spans/S105-4.txt <dup> cnki-citation-check-r40.md`,
span file the exact slice txt[16773:16968] (195 chars); the synthetic entry+lesson copies got the
dup line so in_entry/in_lesson stay n/n — every counter leg revalidates it (first-occurrence
anchoring is self-consistent), including `CAPTURE_BOUND=7/7` in full mode.

## Findings (coverage, not contract changes)
1. `--lane-only` cannot see (b) digest corruption or (c) span drift — it has no capture-derived
   leg; detection there depends wholly on full-mode CAPTURE_BOUND or `build-spans --check`.
2. QUOTE_SHORT is a max-only bound: it passes (d)'s 2-char quote (6/6). The round-50 substance
   floor is the only hollow-quote leg and catches it (HOLLOW_QUOTE), plus OVERWIDE_SPAN once the
   quote shrank inside an unchanged 199-char span — the routed round-49 fix does the work.
3. (f2) is the sharpest survivor: quote uniqueness is enforced only at build time. The frozen
   counter cannot tell a derived row from a hand-written one; its legs self-validate the
   first-occurrence anchoring of a twice-occurring quote. The only guards are the build-time
   refusal (held, f1) and the derivation check SPANS_ROW_EXTRA/SPANS_FILE_ORPHAN (held, f2).
4. ANCHOR_BOUND is the only lane-only leg that caught (a): it re-derives each `char N` from the
   manifest itself, so an offset mutation breaks the registry anchor even without captures.

## Restoration evidence
After all mutants: `cd root && sha256sum -c pristine-hashes.txt` → 7×OK rc=0 (spans.tsv
`40a66e83…`, spans/S104-{1,2,3}.txt, spans/S105-{1,2,3}.txt). Mutant trees were `cp -r` copies,
deleted after their runs; the pristine tree was never written after the build. Lane repo: zero
writes (only this report); all lane/shokuknow access read-only (`git show`/`git grep`, capture
reads). No campaign tool of /home/vgpnk/Projects/shokuknow was invoked.

VERDICT: mutation-tested build-spans + the C2 quote legs with 7 probes on a synthetic
two-capture fixture — offset mutation killed by ANCHOR/CAPTURE legs, digest corruption and
context-span drift survive `--lane-only` by design, hollow/whole-capture quotes killed by the
substance floor, and a twice-occurring quote survives the counter entirely and is caught only
by the builder's uniqueness refusal and derivation check — pristine restored byte-exact
(7×sha256 OK), scratch deleted.

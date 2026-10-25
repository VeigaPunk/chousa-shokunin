# R50ExecReplay — r50 w2: replay every receipt from committed bytes
Seat R50ExecReplay (leaf; no dispatch, no installs — pacman host-paused, none needed). Lane
`/home/vgpnk/Projects/shokunin/chousa-shokunin`, HEAD `c5b8dca`, replayed `74794db07e1b383d5c3e96ad5122fd158a541271`;
`git diff 74794db HEAD -- corpus tools` is empty, so the replayed bytes are the working bytes.
Scratch `/dev/shm/chousa-r50-R50ExecReplay/` deleted at the end; no lane byte written except this report; no network.
## 1. The specified replay method cannot work, and why
Both counters and the control builder derive their root from their own path
(`LANE = pathlib.Path(__file__).resolve().parents[3]`, `c2-count.py:41`; `parents[4]`,
`controls/build-c2-controls.py:16`) and call git on that root, so the assigned method
(`git archive 74794db | tar -x` into `/dev/shm`) cannot reproduce a receipt:
```
$ cd tree && python3 corpus/evidence/round50/c2-count.py           -> NO_BASE_OR_REGISTER  rc=2
$ python3 corpus/evidence/round50/controls/build-c2-controls.py    -> ValueError: max() iterable argument is empty
$ python3 corpus/evidence/round50/c1-count.py                      -> R49_REGRESSION=FAIL rc=2, LEGS=4/5, C1=FAIL
```
The premise that C2's counter "reads git from the REAL lane" is false: it reads git from the tree
the counter sits in. Only git-free legs reproduce in an export (c1 legs 1–4, its controls,
`build-spans.py --check` → `SPANS_ROWS=55 STALE=0`). I replayed from full `git clone --no-hardlinks`
checkouts at the exact commits — same objects, git present: `clone` 74794db, `base` 3c51da77, `freeze` 6a068f2.
## 2. Receipt-by-receipt result
| receipt | replay command | result |
|---|---|---|
| `measure-after-1.txt` C1 block | `c1-count.py` | **identical**, `LEGS=5/5 C1=PASS` rc 0 |
| `measure-after-1.txt` C2 block | `c2-count.py` | **identical** (19/19 lines), `C2=PASS` rc 0 |
| `controls/c1-before.txt` tool-before | `--tool …/tool-before.py` | **identical**, `LEGS=2/5` |
| `controls/c1-before.txt` echo-tool | `--tool …/echo-tool.py` | **identical**, `LEGS=4/5` |
| `controls/c1-before.txt` const-tool | `--tool …/const-tool.py` | **identical**, `LEGS=2/5` |
| `controls/c2-before.txt` base block | `c2-count.py --root base` | **identical** (19/19), `C2=FAIL` rc 1 |
| `controls/c2-before.txt` STAGED / TOOLED | `build-c2-controls.py` | **differs** (§3) |
| — | `build-spans.py --root clone --check` | `SPANS_ROWS=55 STALE=0` rc 0 |
`diff` on C1 and C2-after is empty apart from a trailing blank line in my `awk` extraction; both frozen claims hold in place (`C1=PASS`, `C2=PASS`).
## 3. Defect D1 — the C2 do-nothing control receipt no longer reproduces
`build-c2-controls.py` at 74794db prints different blocks than the committed `c2-before.txt`:
```
--- c2-before.txt STAGED        +++ replay STAGED
-QUOTE_ROWS=0 ON_BOUND=0/0      +QUOTE_ROWS=55 ON_BOUND=0/55
-QUOTES_IN_SPAN=0/0              +QUOTES_IN_SPAN=55/55
-QUOTES_IN_LESSON=0/0            +QUOTES_IN_LESSON=0/55
-QUOTE_SHORT=0/0                 +QUOTE_SHORT=55/55
-SPAN_CONTEXT=0/0                +SPAN_CONTEXT=55/55
-CAPTURE_BOUND=0/0               +CAPTURE_BOUND=55/55
-SUBSTANCE=FAIL                  +SUBSTANCE=PASS
--- TOOLED                      +++ replay TOOLED
-BOUND=3/4 (min 3) REFUSED=0     +BOUND=4/4 (min 3) REFUSED=0
-BOUND_IDS=S106,S108,S109        +BOUND_IDS=S106,S107,S108,S109
-REF_ID_UNBOUND=8                +REF_ID_UNBOUND=3
-QUOTE_ROWS=0 ON_BOUND=0/0       +QUOTE_ROWS=55 ON_BOUND=0/55
-SPAN_IDS=0/3 (min 3 each)       +SPAN_IDS=1/4 (min 3 each)
-SUBSTANCE=FAIL                  +SUBSTANCE=PASS
```
`C2=FAIL` still holds for both, so the kill rule survives; but `claims.md` states the controls' numbers ("`BOUND=3/4`, `REF_ID_UNBOUND=8`, `QUOTE_ROWS=0`", TOOLED with "no quote, span or lesson") and the committed builder no longer produces them. Attribution:
```
$ git -C freeze checkout 6a068f2 && python3 corpus/evidence/round50/controls/build-c2-controls.py
STAGED IDENTICAL AT FREEZE / TOOLED IDENTICAL AT FREEZE      # receipt honest at the freeze
$ cd iso && rm -f corpus/evidence/round50/{quotes.tsv,spans.tsv} && rm -rf …/spans
  && python3 corpus/evidence/round50/controls/build-c2-controls.py
BOUND=0/4 … QUOTE_ROWS=0 … SUBSTANCE=FAIL                     # STAGED block restored
BOUND=4/4 … BOUND_IDS=S106,S107,S108,S109 REF_ID_UNBOUND=3    # TOOLED still 4/4
```
Cause 1: `scratch()` (`build-c2-controls.py:31`) copies `LANE/corpus/evidence/round50` wholesale (ignoring only `controls`, `c1-fixtures`), so once the candidate's `quotes.tsv`, `spans.tsv` and `spans/` landed at 74794db every control root inherits the artifact under test — 55 quotes, 55 span files, `SUBSTANCE=PASS`, `CAPTURE_BOUND=55/55` in a control advertised as carrying none.
Cause 2: the post-freeze `assimilate-rows.py` hardening (erratum item 1) binds S107, the 教师 row the erratum says was refused. Both stay `C2=FAIL` only because `ON_BOUND=0/55`, `QUOTES_IN_LESSON=0/55`, `ANCHOR_BOUND=0/4`, `INFERENCE_GROUNDED=0/3` fire.
## 4. Defect D2 — `stale-count-check.py` fails at the landed commit; its "after" receipt is absent
```
$ python3 corpus/evidence/round50/stale-count-check.py            # clone at 74794db
STALE corpus/README.md:1080 says 55, receipt 31
STALE LOG.md:1803 says 28, receipt 31
STALE_HITS=8 UNRESOLVED=2 RECEIPT_ROWS=31
STALE_COUNT=FAIL                                                  rc=1
```
(a) `corpus/QUALITY.md:783` — "after them `STALE_COUNT=PASS`, exit 0 (`stale-count-after.txt`)";
`git ls-tree -r --name-only 74794db | grep stale-count-after` → nothing (only `stale-count-before.txt` and the check exist).
(b) `corpus/lessons/round-50.md:27` (intake row 2) — "correction: lines in `corpus/QUALITY.md`, `corpus/README.md`, `LOG.md` and `corpus/lessons/round-49.md`; `stale-count-check.py` exit 1 → 0": the first three exist (`QUALITY.md:786`, `README.md:1083`, `lessons/round-49.md:220`), but `grep -n "correction:" LOG.md` finds no such line and none naming 1803, and the check exits 1.
(c) `README.md:1080` is a permanent false positive: it reads "span builder and 55-row manifest" — round 50's own manifest — and the check compares every `<n>-row manifest` in the scanned files to the round-49 receipt (31), so it cannot reach exit 0 while that row exists.
`PROSE` (`stale-count-check.py:18`) pins one receipt for four files that now carry two rounds' counts; the building seat (`.ufo/waves/round-50/w1/ExecStaleCount.md`) only ever showed PASS on a scratch copy with simulated corrections, never on the lane.
## 5. Independent byte-level check of the C2 manifest (55 rows, not the counter's code)
A standalone script re-read every row against `/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache/<key>.txt` as UTF-8:
```
stats= {'digest': 55, 'slice': 55, 'quote_in_span': 55, 'span_longer': 55,
        'quote_once_capture': 55, 'words<=25': 55, 'chars<=160': 55}   bad= [] n_bad= 0
```
Every span file is exactly `capture[offset:offset+len(span)]`, the capture digest matches, each quote occurs exactly once in its capture, inside its span, within 25 words / 160 chars. Anchors re-derived from bytes: S104 `[194,211,246,268,380,422,549,662,684,735,849,1236,1380,1469,1784]`, S105 24 offsets incl. `[48,27587,30661,30738,30745,30778,30800,31063,31101,31137,31233,31273]`, S106 `[83,22511,22549]`; every `char N` in the S104/S105/S106 anchor cells and in all five entry `source:` lines is in that set.
The `R50ReopenRowS105` flag (S105 "−80/−48") misreads the `offset` column, which is the span-block start (`CONTEXT=80`); the peer retracted it and my byte check confirms the retraction for all three ids, not just S105.
Registry legs: base at 3c51da77 has 103 rows, max id S103, no theme URL (`chaxin.las.ac.cn`, `gs.sxu.edu.cn`, `rwxy.seu.edu.cn`, `bs.bnu.edu.cn` all absent); lane rows S104/S105/S106 are `docs A/B/B`, `mined`, `opened 2026-10-25`, `used-by` exactly the citing entries; no lane row carries the 教师 URL and `corpus/lessons/round-50.md:53` carries the `refused-doc:` line naming it.
C1's fixture pin recomputed over `c1-fixtures/` → `c5c56480e9f6a08d6a2077b6a11267a4cabf0bc0d3f726408a9bb0238283cd43`, equal to `PIN`. `quote-substance-check.py spans.tsv` → `IDS=3 QUOTES=55 FAILURES=0` rc 0 (my first run on `quotes.tsv`, a 4-column source manifest, printed 55 `MALFORMED` — wrong input, not a defect). `inference-ground.py --entry … --spans spans.tsv --counts /dev/null --registry …` → rc 0 for all three entries. Register sweep independently: `grep -c` of the four theme hosts over `absent-defect-register.md` → `0`, slice rows `24`, so `QUARANTINE_VERDICTS=0/0` is vacuous as the lesson states.
## 6. Erratum verified
`git diff 6a068f2 74794db --stat -- c1-count.py c2-count.py claims.md controls c1-fixtures` is empty: predicates, counters, controls and fixtures are byte-frozen. The post-freeze tool diff is exactly the two disclosed files (`tools/assimilate-rows.py` +142/−8, `tools/inference-ground.py` +10/−1; the latter adds `CJK_RE` and `return len(CJK_RE.findall(s)) >= 4` in `has_two_words`).
`cjk-ground-check.py` → `CJK_GROUND=PASS` (cases A–C); `inference-regression-before/after.txt` differ only in the header line and one appended entry-hash line, as disclosed.
## 7. Limits
I replayed the four assigned receipts plus the control builder and `build-spans --check`; I did not mutation-test the five new checks, re-open the captures as documents, or judge entailment. D1 is a receipt/control defect, not a claim failure (the frozen C2 target and kill rule are met at 74794db); D2 is a defect in the round's Gate evidence (QUALITY 74, lesson intake row 2), not in the two frozen claims.
VERDICT: attacked the replay of every receipt from committed bytes — C1 (`LEGS=5/5 C1=PASS`), C2 (`C2=PASS`), all three C1 controls, the C2 base block, `SPANS_ROWS=55 STALE=0` and all 55 span/anchor rows reproduce exactly; defect found in two places: (D1) `controls/c2-before.txt` does not reproduce at 74794db (`QUOTE_ROWS 0→55`, `SUBSTANCE FAIL→PASS`, `BOUND 3/4→4/4` incl. the refused S107) because the builder copies the landed manifest into the control root and the post-freeze tool binds S107; (D2) `stale-count-check.py` exits 1 at 74794db while QUALITY 74 cites a non-existent `stale-count-after.txt` for `STALE_COUNT=PASS` and lesson intake row 2 claims a LOG.md correction line that does not exist; the `offset` column of `spans.tsv` (the S105 flag) is correct for all 55 rows.

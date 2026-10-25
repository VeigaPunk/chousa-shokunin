# Round 49 W1 — DraftP2Limit

## Scope and provenance

Attacked routed defect 2 from `corpus/lessons/round-48-verifier-spotcheck.md:79`: R48 P2's two-word look-back misses direct denials with a negator three positions before an affirmed phrase stem. No product or judge code changed. The only persistent write is this report. Scratch entries/copies were created under `/tmp/chousa-r49-DraftP2Limit/` and removed with `rm -rf /tmp/chousa-r49-DraftP2Limit` (no output). No installation was made. Tooling policy was read at `/home/vgpnk/.omp/agent/RULES.md:1-14`.

The frozen set supplies a05 verbatim at `corpus/evidence/round48/precision-count.py:21-23`: `("a05", "S902", "the archived copy is dated at build", "that date is not the copy's build date")`. The copied span at `corpus/fixtures/inference-ground-r47/spans/S902-1.txt:1` affirms `the archived copy is dated at build time`. `tools/inference-ground.py:317-349` describes/implements P2; line 343 uses `before[-2:]`. Current HEAD `6594092` matches R48 tool commit `671b096e`: `git -C /home/vgpnk/Projects/shokunin/chousa-shokunin diff 671b096e 6594092 -- tools/inference-ground.py | wc -l` → `0`. The preceding version was extracted with `git -C /home/vgpnk/Projects/shokunin/chousa-shokunin show 671b096e^:tools/inference-ground.py` into scratch; its P2 branch inspects all `before` words (confirmed by opening the extracted file around `polarity_flips`).

## Commands and observed outcomes

All following are from the task shell with scratch root `/tmp/chousa-r49-DraftP2Limit`; command paths omitted from this description are precisely the entries/manifests under that root.

`python3 /home/vgpnk/Projects/shokunin/chousa-shokunin/tools/inference-ground.py --entry /tmp/chousa-r49-DraftP2Limit/entry-a05.md --spans /tmp/chousa-r49-DraftP2Limit/spans.tsv --counts /tmp/chousa-r49-DraftP2Limit/counts.json --root /tmp/chousa-r49-DraftP2Limit` → stdout:

```text
GROUND entry=entry-a05.md section=1 bullets=1 tokens=1 grounded=1
GROUND: PASS
```

Then shell `echo "rc=$?"` → `rc=0`. Entry is the frozen a05 bullet; span is byte-copy of S902 fixture. The old tool from `671b096e^` on this same entry printed `GROUND entry=entry-a05.md section=1 bullets=1 tokens=1 grounded=1`, `FINDING INF_POLARITY_FLIP bullet=1 token="the archived copy is dated at build / build"`, `GROUND: FAIL`, `rc=1`.

Independent denial used a different affirmed stem: span `the archive stores each ballot; tallies are kept apart`; bullet `the stored figure is not the recorded ballot`. Token phrase grounds verbatim, and `not` is three words before `ballot` in the bullet. Current tool command, same flags with `entry-denial2.md`, printed `GROUND entry=entry-denial2.md section=1 bullets=1 tokens=1 grounded=1`, `GROUND: PASS`, `rc=0`.

Two-word boundary control used same span, bullet `the stored figure is not the ballot`; current tool with `entry-control2.md` printed `GROUND entry=entry-control2.md section=1 bullets=1 tokens=1 grounded=1`, `FINDING INF_POLARITY_FLIP bullet=1 token='the archive stores each ballot / ballot'`, `GROUND: FAIL`, `rc=1`. This shows the target stem is reached by P2 with two intervening words but not three.

Ran frozen regression command `python3 /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round48/precision-count.py` → all p01–p06 and a01–a06 `PASS rc=0`; `CORRECT_BULLETS_PASS=12/12`, `MIN_CORRECT_PASS=11/12`, `PRECISION_GATE=PASS`, shell `rc=0`. That result is evidence the false-negative class is not represented as a failing case in the frozen set; it is not evidence of general precision.

A first attempt at the independent entry used a phrase that included extra `report` and mismatched its copied span; observed `INF_TOKEN_NOT_IN_SPAN` (input error), corrected the fixture to ensure the final recorded probe above is grounded. No check was inferred from the failed intermediate.

## Draft language for next integration

(a) Suggested `corpus/QUALITY.md` Named-limit sentence after criterion 69's existing R48 window note: **“The two-word P2 look-back has an unmeasured false-negative class: a plain denial of an affirmed phrase passes when its negator is three words before the phrase stem; demonstrated by a05 and the independent denial in `.ufo/waves/round-49/w1/DraftP2Limit.md`, while `python3 corpus/evidence/round48/precision-count.py` still reports `CORRECT_BULLETS_PASS=12/12` because its frozen cases do not test that three-before denial.”**

(b) Suggested lesson sentence: **“This P2-window false-negative class is unmeasured by the frozen R48 12-case set: `python3 corpus/evidence/round48/precision-count.py` prints `CORRECT_BULLETS_PASS=12/12` and `PRECISION_GATE=PASS`, while scratch runs of `python3 tools/inference-ground.py` pass both a05 (`that date is not the copy's build date`) and a separate three-before denial (`the stored figure is not the recorded ballot`) at rc=0; a two-before boundary control is refused at rc=1.”** The exact scratch commands and outputs are transcribed above.

## Surfaces and bounds

Affected surface: R48 P2 behavior, exposed through inference-ground and described in `corpus/QUALITY.md` criterion 69 / R48 lesson routed defect 2. Out of scope: changing tool, fixture set, frozen predicates/targets/counters/controls, C1/C2 claim adjudication, any live fetch, and changes to product or judge files. No C1/C2 campaign counters run.

VERDICT: Built two scratch, grounded three-before denial probes and a boundary control; both three-before denials pass, confirming the routed P2 false-negative class is absent from frozen R48 coverage.

# w2 / RevClaimTags — QUALITY 64 tag check on the round-46 verdict table

seat: leaf reviewer (no dispatch), round 46 wave 2 (falsify)
item: `python3 corpus/evidence/round45/tag-count.py --from 46 --to 46` must print
`TAGGED=n/n` exit 0 for the round-46 verdict table; every claim row must carry
`ground`/`plumbing` consistent with what it changed (C1 plumbing, C2 plumbing, C3 ground).
target: audited landing `d09fc8e7e2972e30e5e0aaa6e404c97aa0b9f95a`; claims frozen at `c2f0e9d1`.

**Verdict: requirement MET on the round-46 verdict bytes — `TAGGED=3/3`, exit 0 — and the
three tags are correct (no untagged row, no mistag). Two reservations, neither a mistag:**
(a) those bytes are not in `d09fc8e`; the check there prints `TAGGED=0/0` exit 1 and they
first appear (byte-identical) in the closure commit `3807537`, so the green is a property
of closure, not of the audited landing (F1); (b) `TAGGED=n/n` is presence-only and its row
selector is evadable, so the PASS does not by itself prove every rendered claim row is
tagged (F2/F3 — latent, not exploited here: `n=3` matches the three frozen claims).

## Commands and verbatim output

Current tree and closure commit both carry `SCORECARD.md` sha256
`eacbc34183aef5b5ef694bf1c7b9f0c36aabfe38250e1f4223a4d909477acd26`; the three claim rows
(`2459-2461`) hash `13793f5533e6530b8a276d99ea652a3b0147ecb760c4009843df53772a393202`.

```
$ python3 corpus/evidence/round45/tag-count.py --scorecard SCORECARD.md --from 46 --to 46
TAGGED=3/3
TAG=PASS
EXIT=0
$ python3 corpus/evidence/round45/tag-count.py          # default range >= 45
TAGGED=6/6
TAG=PASS
EXIT=0
$ python3 corpus/evidence/round45/tag-count.py --scorecard <3807537:SCORECARD.md> --from 46 --to 46
TAGGED=3/3
TAG=PASS
EXIT=0
$ python3 corpus/evidence/round45/tag-count.py --scorecard <d09fc8e:SCORECARD.md> --from 46 --to 46
TAGGED=0/0
TAG=FAIL
EXIT=1
$ python3 corpus/evidence/round45/tag-count.py --scorecard <d09fc8e:SCORECARD.md> --from 45 --to 45
TAGGED=3/3
TAG=PASS
EXIT=0
$ git show d09fc8e:SCORECARD.md | grep -n "Round 46"
2439:## Planned — round 46 (not started)          # only round-46 hit in that commit
$ python3 corpus/evidence/round45/tag-count.py --scorecard /tmp/nonexistent.md --from 46 --to 46
TAG=FAIL scorecard-missing
EXIT=2
```

My first run of the assigned command (working tree before the table existed) also printed
`TAGGED=0/0 / TAG=FAIL / EXIT=1`; the section appeared while this seat was reading the file.

## Row-level result (`SCORECARD.md:2459-2461`, also `3807537:SCORECARD.md`)

| row | tag cell | expected by QUALITY 64 | verdict |
|---|---|---|---|
| C1 operability (inference-ground tool) | `plumbing` | plumbing — changes a gate, counter, fixtures | match |
| C2 calibration (registry outside the pattern) | `plumbing` | plumbing — changes a registry mechanism | match |
| C3 depth (evidence-pool entries, S085–S089) | `ground` | ground — knowledge entries on an outside subject | match |

Tags match the claims' own `Tag:` lines (`claims.md`) and the round declaration ("C1
plumbing, C2 plumbing, C3 ground"); `corpus/QUALITY.md:583-589` supports the same reading.

## Findings

**F1 — LOW (citation/state).** The verdict table is not derivable from `d09fc8e`. That
commit has only `## Planned — round 46 (not started)`; the table is inserted by closure
commit `3807537` (+46 lines, `SCORECARD.md` only), with the same sha256 I scored. So a
reader running the assigned command at the audited landing gets `TAG=FAIL`; the correct
citation for this green is `3807537`, and the verdict section's own header ("work landed
at `d09fc8e`") should not be read as placing the table there. No tag is wrong; the row
set is complete (3/3 against three frozen claims).

**F2 — MEDIUM (false pass, latent).** The row selector is `^ {0,3}\| C\d`. Emphasising the
claim id hides the row, so an untagged row can stay rendered while the gate passes:
```
$ sed -i 's/^| C3 depth:/| **C3** depth:/; s/| ground |$/|  |/' <copy>   # untag C3
TAGGED=2/2
TAG=PASS
EXIT=0
```
This contradicts QUALITY 64's binding text ("each claim row … carries a … cell",
`corpus/QUALITY.md:583-589`). Not exploited: `grep -cE '^\| \*\*C[0-9]' SCORECARD.md` = 0.

**F3 — MEDIUM/LOW (completeness).** `n` comes from the same regex, so the tool cannot tell
three claims from one. Deleting the C2 and C3 rows yields:
```
TAGGED=1/1
TAG=PASS
EXIT=0
```
Completeness for round 46 is sound only because I read `claims.md` and counted the three
rows by hand; it is not a property of `TAGGED=n/n`.

**F4 — LOW (detector asymmetry).** tag-count is fence-blind, unlike `round46/c2-count.py`.
An untagged `| C9 sample | …` row injected in a fence is counted:
`UNTAGGED round=46 | C9 sample | x | y | z |  |` → `TAGGED=3/4`, exit 1. The direction is
strict (a quoted example fails a good table); it cannot hide an untagged row.

**F5 — DECLARED LIMIT, not a defect.** Tag truth is unmeasured: flipping C3 to `plumbing`
still prints `TAGGED=3/3 TAG=PASS EXIT=0`. QUALITY 64 declares this ("A tag's truth is a
reader's check", `corpus/QUALITY.md:594`); I performed that check — all three are correct.

## Residual risk / verification gaps

- The verdict table moved under this seat (absent → present → committed at `3807537`).
  Pinned: `SCORECARD.md` sha256 `eacbc341…`, rows sha256 `13793f55…`; if those rows change,
  F2–F5 need a re-run.
- `tag-count.py` is byte-unchanged from the round-45 landing (`git diff --stat 6e2630a
  d09fc8e -- corpus/evidence/round45/tag-count.py` empty); its r35–r44 control reproduces
  `TAGGED=0/22`, exit 1.
- I did not verify the C1/C2/C3 counters or entries themselves (other wave-2 seats).
- No installs. Scratch `/tmp/chousa-r46w2-RevClaimTags` deleted after use.

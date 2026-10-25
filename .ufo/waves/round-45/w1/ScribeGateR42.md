# Round 42 Gates row — scoped findings

## Assignment
Draft one Gates row for the round-42 counter entry points `corpus/evidence/round42/c1-count.py` and `corpus/evidence/round42/c2-count.py`, using the existing table conventions and evidence. Read the counter docstrings/implementations and claims, scorecard verdict, log, and lesson; ran each counter once from the lane root without write options.

## Evidence and commands

All commands below were run with absolute paths; the counter commands' working directory was `/home/vgpnk/Projects/shokunin/chousa-shokunin`.

- Read `/home/vgpnk/Projects/shokunin/chousa-shokunin/SKILL.md`, `## Gates` rows 77 onward; `research-gate round-37 counters` is the closest row convention. It has eight cells; entry uses full repo-relative counter paths; verdict map records exact printed PASS values and exit interpretation.
- Read `/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round42/claims.md`. C1 frozen target at lines 67–79: six counts; missing-tool control; exit semantics in counter docstring. C2 target/control at lines 92–107; counter docstring lines 2–20; implementation emits its seven count values and `C2=PASS|FAIL` (counter lines 176–188). Claims freeze states base lane tip `872bf3a3507875b382313f955d15960f9638256f` (claims lines 1–4).
- Read `/home/vgpnk/Projects/shokunin/chousa-shokunin/SCORECARD.md` round-42 verdict lines 2302–2339: measured round C1/C2 results and improved verdicts, plus the round's unchanged axis/out-of-scope notes.
- Read `/home/vgpnk/Projects/shokunin/chousa-shokunin/LOG.md` lines 1494–1539: same observed results, freeze commit `dd63b6cfec5e1eafddb6662fc343e2ff6ab6aedc`, controls and receipts.
- Read `/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/lessons/round-42.md` lines 7–36, 77–101: claims/results, no adoption, control evidence, and pending outside spot-check. No later counter version is identified in the inspected round-42 materials; the two listed counters are the frozen entry points.
- Existence check: `/home/vgpnk/Projects/shokunin/chousa-shokunin/tools/quarantine-check.py` exists. Read both committed controls: C1 states missing gate tool, exit 1; C2 flipped S093 says `CLASS_CONSISTENT=23/24`, `C2=FAIL`, exit 1.

### Executed counter commands and verbatim output

Command: `cd /home/vgpnk/Projects/shokunin/chousa-shokunin && python3 corpus/evidence/round42/c1-count.py; echo "C1_EXIT=$?"`

```text
SLICE_REDERIVE_MATCH PASS  tool=24 independent=24
EXAMINE_RUNS         PASS  exit=0 
QUOTES_EXAMINED      PASS  examined=43 expected=43
NO_SKIPPED_QUOTE     PASS  every examined quote carries a status
REPRODUCIBLE         PASS  two runs identical=True
POSITIVE_CONTROL     PASS  fold=exact strict=True
NEGATIVE_CONTROL     PASS  fold=None strict=False
MUTANT_DETECTED      PASS  mutant=23 base=24
SLICE_REDERIVE_MATCH=24/24
QUOTES_EXAMINED=43/43
REPRODUCIBLE=1/1
POSITIVE_CONTROL=1/1
NEGATIVE_CONTROL=1/1
MUTANT_DETECTED=1/1
C1_EXIT=0
```

Command: `cd /home/vgpnk/Projects/shokunin/chousa-shokunin && python3 corpus/evidence/round42/c2-count.py; echo "C2_EXIT=$?"`

```text
VERDICTED=24/24
CLASS_CONSISTENT=24/24
REASON_NONEMPTY=24/24
FLIP_NONEMPTY=24/24
VOCAB_OK=24/24
DUPLICATE_ROWS=0
ROWS_OUTSIDE_SLICE=0
C2=PASS
C2_EXIT=0
```

The `echo` reports each preceding counter's status because it immediately follows the command. No receipt-writing option was passed. No tools were installed or updated.

## Draft row (verbatim)

```text
| `research-gate round-42 counters` | gate | `python3 corpus/evidence/round42/c1-count.py` · `python3 corpus/evidence/round42/c2-count.py` | C1 `SLICE_REDERIVE_MATCH=24/24 QUOTES_EXAMINED=43/43 REPRODUCIBLE=1/1 POSITIVE_CONTROL=1/1 NEGATIVE_CONTROL=1/1 MUTANT_DETECTED=1/1` and C2 `VERDICTED=24/24 CLASS_CONSISTENT=24/24 REASON_NONEMPTY=24/24 FLIP_NONEMPTY=24/24 VOCAB_OK=24/24 DUPLICATE_ROWS=0 ROWS_OUTSIDE_SLICE=0 C2=PASS`: exit `0` all counts hold; exit `1` count failure; exit `2` usage/env | C1 do-nothing control (tree without `tools/quarantine-check.py`) exits 1; C2 flipped-row control prints `CLASS_CONSISTENT=23/24`, `C2=FAIL`, exits 1 (`corpus/evidence/round42/controls/c1-control-before.txt`, `corpus/evidence/round42/controls/c2-control-before.txt`) | freeze `dd63b6cfec5e1eafddb6662fc343e2ff6ab6aedc`; C1 receipt `corpus/evidence/round42/receipts/c1-after-freeze.txt` | read-only | chousa |
```

## Verdict and scope

Both counters passed on this execution with the exact output above (exit 0). Round 42 scorecard/log call both claims improved. C1 control and C2 control fail with exit 1 per their committed receipts. The row records measured values, not claims of external validation: the lesson says the non-author spot-check is pending and discernment is not externally verified. No product, judge, counter, index, or lane production file was changed; only this scoped report was written. No external fetch, subagent dispatch, tests, build, or other verification was performed.

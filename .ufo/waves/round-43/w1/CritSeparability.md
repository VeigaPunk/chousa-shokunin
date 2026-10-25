# CritSeparability — nonempty label swap vs C1/C2

Axes: **operability** (C1, `corpus/evidence/round43/c1-count.py`) and **calibration** (C2, `corpus/evidence/round43/c2-count.py`). Depth (C3 / the S078 adoption) is not implicated. This seat does not score, admit, or edit. Counters were not edited. No install. No network.

Measured tree: `737f40b6aa8f37ffe2269db370fd6d65a720d9a8`. `git status --short` on the two counters, `claims.md`, `absent-split.tsv`, and `tools/absent-split.py` printed no lines.

## Counterexample

A class-label change that leaves both `{misquote, not-carried}` nonempty fails C2 and does not fail C1, but only on the artifact each counter actually reads. They do not read the same bytes. One shared mutation is not both kills.

**C2 kill (calibration).** `read_table` returns `(id, label)` from `corpus/evidence/round43/absent-split.tsv`. `main` optionally rewrites one row:

```text
c2-count.py:115-119
(rid, ("not-carried" if label == "misquote" else "misquote") if rid == args.flip else label)
```

Agreement is `expected.get(rid) == label`, where `expected` is `independent_labels` (which calls `nfkc_ws` and `longest_run`, bound `1/2`). `ok` is `n == 15 and agreed == 15 and vocab_ok == 15` (`c2-count.py:123-137`). There is no class-count check. Flipping S086 (`not-carried` → `misquote`) leaves 10 misquote and 5 not-carried. `main` then prints `SPLIT_AGREES=14/15` and returns 1. Exchanging S086 with S093 keeps the committed counts (9 and 6) and still fails: two ids disagree with `independent_labels`.

**C1 does not grade that swap (operability).** `absent_ids` keeps a row only when column 2 of the round-42 table is `absent` (`c1-count.py:34-42`). It never opens `absent-split.tsv` (string search: absent). `run` only captures tool stdout (`c1-count.py:45-48`). `main` binds no id to a ratio. The only label tests are:

```text
c1-count.py:79-87
labels = [row[1] for row in rows if len(row) > 1]
CLASSED: len(labels) == 15 and set(labels) <= {"misquote", "not-carried"}
BOTH_NONEMPTY: "misquote" in labels and "not-carried" in labels
```

`ABSENT_ENUMERATED` compares column 0 to `absent_ids`. `REPRODUCIBLE` compares the two stdouts. `MUTANT_DETECTED` compares `ids[:-1]` to the 15 absent ids (`c1-count.py:89-91`); it does not read labels. A deterministic in-vocab swap that keeps both names present therefore passes `main`.

**Not one artifact.** `c2-count.py` does not import `subprocess` and does not call `tools/absent-split.py` (the name occurs only in the docstring at lines 10-12). A swap inside `classify` is invisible to `read_table` / `independent_labels` / `main`. The sentence "that swap is C2's kill" (`claims.md:45-46`) over-identifies the command-output swap C1 ignores with the table swap C2 grades. The later sentence (`claims.md:72-73`) is the accurate one: C1 does not read the split table's labels; C2 does not require the command.

The empty-class boundary is load-bearing. Replacing every label with `misquote` still passes `CLASSED` and fails only `BOTH_NONEMPTY`. "Need not fail C1" is not "no label change can fail C1".

Pointing `c1.main --table` at the split TSV is not the test. `absent_ids` then sees 0 rows whose verdict is `absent`, so C1 fails on identity, while `BOTH_NONEMPTY` still passes on the unswapped command. That fail is not a label grade.

## Evidence

Fingerprints (exit 0):

```text
737f40b6aa8f37ffe2269db370fd6d65a720d9a8
54ced70767ccd20bc502504ef75d427bc760d10ebdf70a1053812ff8853289c9  corpus/evidence/round43/c1-count.py
5cbfe2f1127b50ae894bc48027ba119ca4eaf67fadc88251299512629bc9ba43  corpus/evidence/round43/c2-count.py
cc9e4822fc0115fc67a80f7d98c2efc05faaa61367b0b92c36c5379eb006a788  corpus/evidence/round43/claims.md
bba7d8b6b5165cd4d5b21c9b9c9e9275ecb26839ad8764d8db8b4ffebc001a58  corpus/evidence/round43/absent-split.tsv
c0738c7691dc6d46d6063e8013813962b8b56c4c8c319b28ea22b1c095b8e96b  tools/absent-split.py
      9 misquote
      6 not-carried
```

`read_table` plus the same comprehension `main` uses for `--flip`, executed, not edited:

```text
read_table_n 15
before {'not-carried': 6, 'misquote': 9}
after_flip_S086 {'not-carried': 5, 'misquote': 10}
S086_before [('S086', 'not-carried')]
S086_after [('S086', 'misquote')]
exchange_pair not-carried misquote
after_exchange {'not-carried': 6, 'misquote': 9}
changed_ids ['S086', 'S093']
```

`python3 corpus/evidence/round43/c2-count.py` (exit 0):

```text
SPLIT_AGREES=15/15
VOCAB_OK=15/15
MISMATCHES=0
C2=PASS
```

`python3 corpus/evidence/round43/c2-count.py --flip S086` (exit 1):

```text
SPLIT_AGREES=14/15
VOCAB_OK=15/15
MISMATCHES=1
MISMATCH S086 table=misquote independent=not-carried
C2=FAIL
```

`python3 corpus/evidence/round43/c2-count.py --table /tmp/r43-crit-separability/exchange.tsv` (exit 1). That file has 15 unique ids; S086 is `misquote` and S093 is `not-carried`; counts stay 9 and 6:

```text
SPLIT_AGREES=13/15
VOCAB_OK=15/15
MISMATCHES=2
MISMATCH S086 table=misquote independent=not-carried
MISMATCH S093 table=not-carried independent=misquote
C2=FAIL
```

`/tmp/r43-crit-separability/flip-s086.tsv` duplicated S086 (16 rows). Its `14/16` run is a probe-construction error, not the counter's flip. The `--flip` run above is the flip evidence.

`python3 corpus/evidence/round43/c1-count.py` (exit 0):

```text
TABLE_ABSENT PASS 15/15
TOOL_EXIT PASS exit=0
ABSENT_ENUMERATED PASS 15/15
CLASSED PASS 15/15
BOTH_NONEMPTY PASS misquote=9 not-carried=6
REPRODUCIBLE PASS identical=True
MUTANT_DETECTED PASS short=14 expected=15
ABSENT_ENUMERATED=15/15
CLASSED=15/15
BOTH_NONEMPTY=1/1
REPRODUCIBLE=1/1
MUTANT_DETECTED=1/1
C1=PASS
```

Tool-stdout swaps were wrappers under `/tmp/r43-crit-separability/` that ran `tools/absent-split.py` and rewrote column 2 only. Ids stayed equal to the real command. Diffs against that command:

```text
flip_diffs [('S086', 'not-carried', 'misquote')]
ex_diffs [('S086', 'not-carried', 'misquote'), ('S093', 'misquote', 'not-carried')]
flip_counts Counter({'misquote': 10, 'not-carried': 5})
ex_counts Counter({'misquote': 9, 'not-carried': 6})
```

`python3 corpus/evidence/round43/c1-count.py --tool /tmp/r43-crit-separability/tool-flip.py` (exit 0):

```text
TABLE_ABSENT PASS 15/15
TOOL_EXIT PASS exit=0
ABSENT_ENUMERATED PASS 15/15
CLASSED PASS 15/15
BOTH_NONEMPTY PASS misquote=10 not-carried=5
REPRODUCIBLE PASS identical=True
MUTANT_DETECTED PASS short=14 expected=15
ABSENT_ENUMERATED=15/15
CLASSED=15/15
BOTH_NONEMPTY=1/1
REPRODUCIBLE=1/1
MUTANT_DETECTED=1/1
C1=PASS
```

`python3 corpus/evidence/round43/c1-count.py --tool /tmp/r43-crit-separability/tool-exchange.py` (exit 0):

```text
TABLE_ABSENT PASS 15/15
TOOL_EXIT PASS exit=0
ABSENT_ENUMERATED PASS 15/15
CLASSED PASS 15/15
BOTH_NONEMPTY PASS misquote=9 not-carried=6
REPRODUCIBLE PASS identical=True
MUTANT_DETECTED PASS short=14 expected=15
ABSENT_ENUMERATED=15/15
CLASSED=15/15
BOTH_NONEMPTY=1/1
REPRODUCIBLE=1/1
MUTANT_DETECTED=1/1
C1=PASS
```

`python3 corpus/evidence/round43/c1-count.py --tool /tmp/r43-crit-separability/tool-empty.py` (exit 1). Qualifier check, not the nonempty counterexample:

```text
TABLE_ABSENT PASS 15/15
TOOL_EXIT PASS exit=0
ABSENT_ENUMERATED PASS 15/15
CLASSED PASS 15/15
BOTH_NONEMPTY FAIL misquote=15 not-carried=0
REPRODUCIBLE PASS identical=True
MUTANT_DETECTED PASS short=14 expected=15
ABSENT_ENUMERATED=15/15
CLASSED=15/15
BOTH_NONEMPTY=0/1
REPRODUCIBLE=1/1
MUTANT_DETECTED=1/1
C1=FAIL
```

`python3 corpus/evidence/round43/c1-count.py --table /tmp/r43-crit-separability/exchange.tsv` (exit 1). Wrong artifact, not a label grade:

```text
TABLE_ABSENT FAIL 0/15
TOOL_EXIT PASS exit=0
ABSENT_ENUMERATED FAIL 15/15
CLASSED PASS 15/15
BOTH_NONEMPTY PASS misquote=9 not-carried=6
REPRODUCIBLE PASS identical=True
MUTANT_DETECTED PASS short=14 expected=0
ABSENT_ENUMERATED=0/15
CLASSED=15/15
BOTH_NONEMPTY=1/1
REPRODUCIBLE=1/1
MUTANT_DETECTED=1/1
C1=FAIL
```

On that misroute the check detail `ABSENT_ENUMERATED FAIL 15/15` is `len(ids)`, not the match. The summary line `ABSENT_ENUMERATED=0/15` is the match. Do not read the detail as agreement.

## Impacted axes

- **Operability.** A nonempty in-vocab label swap is not a C1 miss. The functions that let it pass are `main`'s `CLASSED` and `BOTH_NONEMPTY`. `absent_ids` and `run` never consult the split label. Emptying a class is a C1 miss. Coupling C1 to `independent_labels` would make the nonempty swap fail operability. That is a tradeoff the frozen kill rule rejects, not a fix.
- **Calibration.** The same nonempty swap is a C2 miss when it is applied to `read_table` rows or `--flip` inside `main`. The failing functions are that comprehension, then `independent_labels` (via `nfkc_ws` and `longest_run`) compared in `main`. A swap that exists only in `tools/absent-split.py` `classify` is not this miss. Treating C2=PASS as proof the command's labels match the table is false provenance.
- **Depth.** No S078 quote, capture, or entry was an input. No depth correction.

`MUTANT_DETECTED` stayed PASS on the flip, the exchange, and the empty class. It is not the separability mechanism.

## Smallest safe correction

Do not edit either counter. Do not retune `1/2`. Do not add a per-id label comparison to `c1.main`, and do not make `c2.main` execute `tools/absent-split.py`. Those edits would collapse the two predicates.

Read the kill as two functions, not one swap:

- Command stdout, both classes nonempty: `c1.main` need not fail (`CLASSED`, `BOTH_NONEMPTY`). `c2.main` does not see it.
- Split-table label, or `c2.main --flip`: `c2.main` fails while both classes stay nonempty. `c1.main` does not see it. Do not pass `absent-split.tsv` to `c1-count.py --table`; that calls `absent_ids`, not a label check.

No predicate change follows from this review. The bound stays `1/2`.

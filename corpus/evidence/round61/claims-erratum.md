# Round 61 — erratum to the frozen claims

`claims.md` (sha256 `9afec8d493f0ba511a256f38cd5098ff508f9ed311c6c49ff5383add9ce0acec`) is not edited. It
carries three statements that do not match the files they name; wave seat `ScoutMistakesThisRound` found them
and `python3 corpus/evidence/round61/digest-ellipsis-check.py corpus/evidence/round61/claims.md` re-finds two
(`mismatched=2`, exit 1; the two tokens are those of items 1 and 2). No predicate, counter, kill rule or target
changes.

1. "Files frozen by this commit" abbreviates the sha256 of `c1-count.py` with the tail `cfff9ef`.
   The file's sha256 is `f1d8b6fde8dedd8894dfbb31aed8876434bdda61b231259069b7c168cdfff9ef` (tail `cdfff9ef`).
2. The same list abbreviates `controls/run-c1-controls.py` with the tail `b5624`. Its sha256 is
   `bcca093e4c92b0db5a7b1d081bb2c3e9ea75d79e3018ddb35c9940b2f0b5b624` (tail `5b624`), identical at the first
   and the amended freeze.
3. "14 frozen mutants M01–M14 of the reference each fail exactly the legs named in
   `controls/run-c1-controls.py`" is wrong for M08: the runner's expectation is the subset `H09`, and the
   receipt `controls/c1-controls.txt` shows `failing=H08,H09 expect=H09 KILLED`. The runner's kill test is
   "every named leg fails", not "exactly those legs"; read the sentence that way.

Also recorded here, not an error of the freeze: `c1-count.py` legs H16 and H17 test `"Traceback" not in
stderr`, which contradicts the predicate sentence ("never from searching its output", QUALITY 117); wave seat
`RevC1LegsH4` showed a correct refusal whose message contains the word fails H16 (`LEGS=19/20`). The landed
builder prints no such word; the contradiction stays in the frozen counter and is routed to the next
counter (QUALITY 121).

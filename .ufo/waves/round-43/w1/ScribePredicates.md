# ScribePredicates — round-43 predicate sentences and named counting commands

author: ScribePredicates (L2 leaf seat, chousa round 43 wave 1)
date: 2026-10-24
round: 43 (attempt 1)
measured commit: `737f40b6aa8f37ffe2269db370fd6d65a720d9a8`
claims blob: `c483f0b808ae844314081605fd18a543d13ad5aa` (4418 bytes)
mode: read-only against the lane tree. This seat wrote only this file.
counters: not executed. An unrun check has not passed.

## Axes

- operability: whether claims.md names a counting command for each predicate, and whether that named path exists as a file.
- calibration: whether "named" is the `Counting command:` line, the predicate sentence, or an executed pass. These are not the same claim.
- depth: quote the frozen sentences from the measured commit, and do not treat a counter docstring or a prompt Goal line as the predicate.

## Answer

Each counting command is named. `corpus/evidence/round43/claims.md` has exactly three lines that contain "Counting command", one under each predicate, and no fourth. The named strings are relative `python3 corpus/evidence/round43/cN-count.py` invocations. Only the R43-C1 predicate sentence also names its command inside the sentence. R43-C2 and R43-C3 name theirs on the following `Counting command:` line, not inside the sentence.

This seat did not run those commands. File existence is not `C1=PASS`, `SPLIT_AGREES=15/15`, or `C3=PASS`.

## Behavior

Read the frozen claims file and confirmed the working tree matches the measured commit. Extracted the three predicate sentences and the three counting-command lines. Checked that the three named scripts exist in that commit. Read only the opening docstrings of those scripts, enough to see that each claims to repeat "the same sentence" and does not. Did not execute a counter, did not pass `--flip`, did not retune the 1/2 bound, did not edit a production file, did not append `LOG.md`, did not touch git state, and did not open `/home/vgpnk/Projects/shokuknow`.

## Predicate sentences

Source: `corpus/evidence/round43/claims.md` at `737f40b6aa8f37ffe2269db370fd6d65a720d9a8`. Working-tree sha256 equals `git show` of that path (both `cc9e4822fc0115fc67a80f7d98c2efc05faaa61367b0b92c36c5379eb006a788`). Quotes below are the file text, including the label and the wrapped lines. Spans are 1-based.

### R43-C1 (lines 30-33)

```
Predicate R43-C1: `python3 corpus/evidence/round43/c1-count.py` executes
`tools/absent-split.py`, that command enumerates exactly the 15 absent ids of
the committed round-42 table, each id is exactly one of {misquote, not-carried},
both classes are nonempty, and two runs are byte-identical.
```

### R43-C2 (lines 54-56)

```
Predicate R43-C2: every label in `corpus/evidence/round43/absent-split.tsv`
agrees with an independent recompute of rule R43-SPLIT, and flipping one row's
label makes the agreement fail.
```

### R43-C3 (lines 77-80)

```
Predicate R43-C3: the admitted entry
`corpus/knowledge/search-log-method-r39.md` cites lane id S078, that id's
registry row names the Europe PMC full-text URL opened this round, and the
located quote is a substring of that URL's committed capture.
```

Predicate-line count in that file: 3. No other line starts with `Predicate R43-C`.

## Counting commands — named or not

| Predicate | Named in claims.md? | Line | Named string | Named inside the predicate sentence? | File at that relative path in `737f40b6`? |
|---|---|---|---|---|---|
| R43-C1 | yes | 35 | `python3 corpus/evidence/round43/c1-count.py` | yes (line 30) | yes, blob `232ea15eefa134048041635120052262acd2bfe4`, 4109 bytes |
| R43-C2 | yes | 58 | `python3 corpus/evidence/round43/c2-count.py` | no | yes, blob `77fd3a2e25de4d1eb5cd8b510fccdfbed932278d`, 4830 bytes |
| R43-C3 | yes | 82 | `python3 corpus/evidence/round43/c3-count.py` | no | yes, blob `ec59211d42a9248a9effdf13f1deeea9a518fdf3`, 2668 bytes |

Verbatim naming lines:

```
Counting command: `python3 corpus/evidence/round43/c1-count.py`
Counting command: `python3 corpus/evidence/round43/c2-count.py`
Counting command: `python3 corpus/evidence/round43/c3-count.py`
```

Grep of `claims.md` for `[Cc]ounting command` returned only those three lines (35, 58, 82). The dispatcher item for this seat does not itself name `c1-count.py`, `c2-count.py`, or `c3-count.py`. It names the claims path and asks whether each counting command is named. The answer is taken from claims.md, not invented from the item text.

The wave Goal block in this seat's prompt names the same three scripts by absolute path. That is a different naming surface. It is quoted under Conflicts. This seat did not execute either form.

## Gates

Seat gate (this item): quote the three predicate sentences and say whether each counting command is named. The quotes and the namedness table above are that gate. It is a text gate. It is not a counter score.

Wave gates, named and not run by this seat:

- C1, as named in claims.md line 35: `python3 corpus/evidence/round43/c1-count.py`. Not run. Exit status unobserved. `C1=PASS` is not evidence from this seat.
- C2, as named in claims.md line 58: `python3 corpus/evidence/round43/c2-count.py`. Not run. `--flip S086` not run. `SPLIT_AGREES=15/15` is not evidence from this seat.
- C3, as named in claims.md line 82: `python3 corpus/evidence/round43/c3-count.py`. Not run. `C3=PASS` is not evidence from this seat.

`corpus/evidence/round43/receipts/` and `controls/` filenames were listed by a directory glob. Their contents were not read. This seat does not adopt them as execution evidence.

The 1/2 bound in rule R43-SPLIT was not retuned and was not recomputed here.

## Conflicts (verbatim, for the L1)

This seat does not pick a winner and does not score either side.

### 1. Counter docstrings say "the same sentence"; the following lines are not the claims sentences

`c1-count.py` lines 4-8 at `737f40b6`:

```
Predicate R43-C1, the same sentence as corpus/evidence/round43/claims.md:
the committed command tools/absent-split.py enumerates exactly the 15 rows the
committed round-42 table labels absent, assigns each exactly one of
{misquote, not-carried}, both classes are nonempty, and two runs are
byte-identical.
```

Claims R43-C1, lines 30-33, is the sentence quoted above. It is not this text. Differences observed, not interpreted as a failed count: claims names `` `python3 corpus/evidence/round43/c1-count.py` executes `tools/absent-split.py` ``; the docstring says "the committed command tools/absent-split.py". Claims says "15 absent ids"; the docstring says "15 rows the committed round-42 table labels absent". Claims says "each id is exactly one of"; the docstring says "assigns each exactly one of".

`c2-count.py` lines 4-8 at `737f40b6`:

```
Predicate R43-C2, the same sentence as corpus/evidence/round43/claims.md:
every label in the committed split table agrees with an independent
recompute of rule R43-SPLIT (NFKC, whitespace collapse, longest contiguous
common run, row maximum ratio >= 1/2 → misquote, else not-carried), and a
one-row flip of that table does not agree.
```

Claims R43-C2 does not contain that parenthetical, and it says "flipping one row's label makes the agreement fail", not "a one-row flip of that table does not agree."

`c3-count.py` lines 4-7 at `737f40b6`:

```
Predicate R43-C3, the same sentence as corpus/evidence/round43/claims.md:
the admitted entry cites lane id S078, that row's URL is the Europe PMC
full-text URL opened this round, and the located quote is a substring of
that URL's committed capture.
```

Claims R43-C3 names `` `corpus/knowledge/search-log-method-r39.md` `` and says "that id's registry row names the Europe PMC full-text URL". The docstring says "that row's URL is the Europe PMC full-text URL" and does not name the entry path.

### 2. Prompt Goal names absolute paths and shorter print requirements; claims names relative paths and fuller targets

Prompt Goal, this seat's spawning message, not the dispatcher item:

```
C1 operability: python3 /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round43/c1-count.py must print C1=PASS and exit 0.
C2 calibration: python3 /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round43/c2-count.py must print SPLIT_AGREES=15/15 and exit 0. --flip S086 must exit 1.
C3 depth: python3 /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round43/c3-count.py must print C3=PASS and exit 0.
```

Claims targets, not executed:

```
Target, one value: `C1=PASS` with `ABSENT_ENUMERATED=15/15`, `CLASSED=15/15`,
`BOTH_NONEMPTY=1/1`, `REPRODUCIBLE=1/1`, `MUTANT_DETECTED=1/1`, exit 0.
```

```
Target: `C2=PASS` with `SPLIT_AGREES=15/15`, `VOCAB_OK=15/15`, exit 0.
The flipped-row control (`--flip S086`) must print `SPLIT_AGREES=14/15` and
exit 1.
```

```
Target: `C3=PASS` with `ENTRY_CITES=1/1`, `QUOTE_LOCATED=1/1`,
`URL_MATCH=1/1`, exit 0.
```

The Goal print requirements are not the same strings as the claims targets. In particular, the Goal's `--flip S086 must exit 1` does not state the claims requirement that the flip print `SPLIT_AGREES=14/15`. This seat did not run either form, so neither text is execution evidence.

### 3. AGENTS.md requires a LOG.md entry; the seat contract forbids it

`AGENTS.md` line 4: "Every change appends a LOG.md entry with the evidence that motivated it."

Seat contract: "Write ONLY your own report at the absolute path named in your item" and "Never modify lane production files".

This seat followed the seat contract. `LOG.md` was not appended. Whether that is a miss is for the L1.

## Touched surfaces

- Written: `.ufo/waves/round-43/w1/ScribePredicates.md` only.
- Read: `corpus/evidence/round43/claims.md` (full); `corpus/evidence/round43/c1-count.py`, `c2-count.py`, `c3-count.py` (headers; c1 through line 40, c2 through line 40, c3 through line 40, plus `git show | sed -n '1,12p'` of each); `AGENTS.md`; `/home/vgpnk/.omp/agent/RULES.md`; dispatch/spec excerpts for this item's path. No tool was installed. Pacman was not invoked.
- Not modified: lane production files, the git index, jj state, the fleet repo, sibling repos, `/home/vgpnk/Projects/shokuknow`.

## Out of scope

- Executing `c1-count.py`, `c2-count.py`, `c3-count.py`, or `--flip S086`.
- Scoring C1, C2, or C3. Receipt and control bodies were not opened.
- Retuning rule R43-SPLIT or recomputing ratios.
- Editing `tools/absent-split.py`, the split table, the knowledge entry, the lesson, `LOG.md`, or `QUALITY.md`.
- Network, fetch, or any shokuknow tool. `c2-count.py` lines 32-37 and `c3-count.py` lines 27-29 name paths under `/home/vgpnk/Projects/shokuknow`. Those paths were not opened. Naming them in source is not a runtime observation.
- Subagent dispatch, commit, push, publish, deploy.

## Findings

1. Three predicate sentences, quoted above from the measured commit's claims file. Count of `Predicate R43-C` lines: 3.
2. Each counting command is named. Count of `Counting command:` lines: 3, paired 1:1 with the predicates. Named strings are the relative `python3 corpus/evidence/round43/c1-count.py`, `c2-count.py`, and `c3-count.py` commands.
3. Inside the predicate sentence, only R43-C1 names its counting command. R43-C2 and R43-C3 do not.
4. The three named scripts exist as committed files at `737f40b6`. Existence was checked with `test -f` and `git ls-tree`. They were not executed.
5. Each counter docstring says it is "the same sentence as" claims.md. The following lines are not those sentences. Conflict 1, for the L1. Not a counter score.
6. No pass/fail of C1, C2, or C3 is claimed by this seat.

## Known limits

- Two seat-side extraction attempts failed and are not evidence about claims.md. `git show 737f40b6aa8f37ffe2269db370fd6d65a720d9a8:corpus/evidence/round43/claims.md | python3 - <<'PY'` fed the script the heredoc, not the blob, and printed `BLOB_LINES=0`. A later `python3 -c` attempt exited 1 with `SyntaxError: unexpected character after line continuation character` before reading the blob. The successful evidence is the working-tree extraction plus the sha256 match against `git show`, the empty `git status --short`, the empty `git diff --stat`, and `wc -lc` of `git show` (`101` lines, `4418` bytes, matching `git ls-tree` size).
- Header reads of the counters are not full-file audits. Line counts observed: c1 103, c2 141, c3 72.
- This report does not say the absolute Goal paths and the relative claims paths fail to resolve to the same files. It says they are written differently, and that neither form was executed.

## Provenance

Commands run in `/home/vgpnk/Projects/shokunin/chousa-shokunin` unless noted. Outputs below are the observed stdout/stderr, not a paraphrase.

`git rev-parse HEAD && git cat-file -t 737f40b6aa8f37ffe2269db370fd6d65a720d9a8 && git rev-parse 737f40b6aa8f37ffe2269db370fd6d65a720d9a8:corpus/evidence/round43/claims.md && git status --short -- corpus/evidence/round43/claims.md .ufo/waves/round-43/w1/ScribePredicates.md && git diff --stat 737f40b6aa8f37ffe2269db370fd6d65a720d9a8 -- corpus/evidence/round43/claims.md && sha256sum corpus/evidence/round43/claims.md && git show 737f40b6aa8f37ffe2269db370fd6d65a720d9a8:corpus/evidence/round43/claims.md | sha256sum`

```
737f40b6aa8f37ffe2269db370fd6d65a720d9a8
commit
c483f0b808ae844314081605fd18a543d13ad5aa
cc9e4822fc0115fc67a80f7d98c2efc05faaa61367b0b92c36c5379eb006a788  corpus/evidence/round43/claims.md
cc9e4822fc0115fc67a80f7d98c2efc05faaa61367b0b92c36c5379eb006a788  -
```

`git status --short` and `git diff --stat` produced no output.

Working-tree extraction (same bytes as the blob, by the sha256 above):

```
PATH=/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round43/claims.md
LINES=101
PREDICATE_LINE_COUNT=3
COUNTING_COMMAND_LINE_COUNT=3
---BLOCKS---
SPAN=30-33
Predicate R43-C1: `python3 corpus/evidence/round43/c1-count.py` executes
`tools/absent-split.py`, that command enumerates exactly the 15 absent ids of
the committed round-42 table, each id is exactly one of {misquote, not-carried},
both classes are nonempty, and two runs are byte-identical.
---
SPAN=35-35
Counting command: `python3 corpus/evidence/round43/c1-count.py`
---
SPAN=54-56
Predicate R43-C2: every label in `corpus/evidence/round43/absent-split.tsv`
agrees with an independent recompute of rule R43-SPLIT, and flipping one row's
label makes the agreement fail.
---
SPAN=58-58
Counting command: `python3 corpus/evidence/round43/c2-count.py`
---
SPAN=77-80
Predicate R43-C3: the admitted entry
`corpus/knowledge/search-log-method-r39.md` cites lane id S078, that id's
registry row names the Europe PMC full-text URL opened this round, and the
located quote is a substring of that URL's committed capture.
---
SPAN=82-82
Counting command: `python3 corpus/evidence/round43/c3-count.py`
---
```

`git log -1 --format='%H%n%s%n%an%n%ae%n%ci' 737f40b6aa8f37ffe2269db370fd6d65a720d9a8` then `git ls-tree -l` of the four paths, then `git status --short` of those paths plus this report, then `test -f` of the three scripts:

```
737f40b6aa8f37ffe2269db370fd6d65a720d9a8
round-43: split the absent class and adopt one locally re-opened search-log entry
chousa-shokunin
chousa@shokunin.local
2026-10-24 21:15:02 -0300
---LS-TREE---
100644 blob 232ea15eefa134048041635120052262acd2bfe4    4109	corpus/evidence/round43/c1-count.py
100644 blob 77fd3a2e25de4d1eb5cd8b510fccdfbed932278d    4830	corpus/evidence/round43/c2-count.py
100644 blob ec59211d42a9248a9effdf13f1deeea9a518fdf3    2668	corpus/evidence/round43/c3-count.py
100644 blob c483f0b808ae844314081605fd18a543d13ad5aa    4418	corpus/evidence/round43/claims.md
---STATUS---
---TEST---
EXISTS corpus/evidence/round43/c1-count.py
EXISTS corpus/evidence/round43/c2-count.py
EXISTS corpus/evidence/round43/c3-count.py
```

`git status --short` in that command produced no output. The report file did not exist yet.

`git show 737f40b6aa8f37ffe2269db370fd6d65a720d9a8:corpus/evidence/round43/claims.md | wc -lc`

```
    101    4418
```

Docstring headers were taken from `git show COMMIT:corpus/evidence/round43/cN-count.py | sed -n '1,12p'`. The "same sentence" lines are quoted in Conflict 1. That command also printed, for each file, `FILE=... LINES=103|141|72` and line 4 `Predicate R43-C*, the same sentence as corpus/evidence/round43/claims.md:`.

Grep `[Cc]ounting command` on claims.md:

```
chousa-shokunin/corpus/evidence/round43/claims.md:35:Counting command: `python3 corpus/evidence/round43/c1-count.py`
chousa-shokunin/corpus/evidence/round43/claims.md:58:Counting command: `python3 corpus/evidence/round43/c2-count.py`
chousa-shokunin/corpus/evidence/round43/claims.md:82:Counting command: `python3 corpus/evidence/round43/c3-count.py`
```

Grep `^Predicate R43-C` on claims.md:

```
chousa-shokunin/corpus/evidence/round43/claims.md:30:Predicate R43-C1: `python3 corpus/evidence/round43/c1-count.py` executes
chousa-shokunin/corpus/evidence/round43/claims.md:54:Predicate R43-C2: every label in `corpus/evidence/round43/absent-split.tsv`
chousa-shokunin/corpus/evidence/round43/claims.md:77:Predicate R43-C3: the admitted entry
```

## Artifact paths

- This report: `.ufo/waves/round-43/w1/ScribePredicates.md`
- Quoted source: `corpus/evidence/round43/claims.md` at `737f40b6aa8f37ffe2269db370fd6d65a720d9a8`

Report: .ufo/waves/round-43/w1/ScribePredicates.md

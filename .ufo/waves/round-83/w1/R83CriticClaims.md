# R83CriticClaims — adversarial review of the frozen round-83 claims

Seat: `R83CriticClaims` (leaf; no subagents, no lane/fleet mutation, no network).
Lane: `/home/vgpnk/Projects/shokunin/chousa-shokunin`.
Revisions read: base `a46534a5`, egress `8fff80ee`, prefreeze `1b9b2ff8`, freeze `3fbf8d12`,
candidate landing `81b81173` (the bytes attacked), tip `aca2a781`.
Frozen subject: `corpus/evidence/round83/claims.md` at `3fbf8d12` (blob `94eea54228a2`,
byte-identical at `81b81173` and `aca2a781`).
All receipts below are copied to `.ufo/waves/round-83/w1/R83CriticClaims/`; the scratch tree
`/fast/scratch/hyaku/chousa-r83/R83CriticClaims/` is deleted before yield.

## 1. C2 — operability (`tools/gate-records.py`)

### 1.1 K3 (harm) — FIRED: a genuine rev record whose quote begins with `"` is refused

The landed tool's own docstring defines the rev form as

```
rev  GATE-RECORD S<id> rev=<40 hex> path=<repo-relative path> line=<n> words=<n> quote=<text to end of line>
```

and defines `PARSE` as "the line fits none of the three forms (unknown/missing/duplicate key, bad value,
extra text)". It places no restriction on the first character of a rev quote. The landed parser does:

`tools/gate-records.py:114-118` (landing blob):
```python
if keys == set(REV_KEYS):
    form = "rev"
    quote = qraw.rstrip()
    if not quote or quote.startswith('"'):
        return None
```

The record below is the full text of committed line 56 of the candidate entry at the landing revision,
in the documented rev form, with every docstring check satisfied (S199 registry row; rev is a commit;
path is a blob at that rev; line 56 is in the blob; the normalized quote occurs in that line; 21 words;
1 <= 21 <= 25):

```
GATE-RECORD S199 rev=81b81173f19d175e2b2a6b409b2a496d09d0b258 path=corpus/knowledge/appraisal-judgment-records-r83.md line=56 words=21 quote="proposed judgment" of row 7 is a gate's or counter's verdict. Read that way, the rows describe practice the lane already
```

Committed line (same bytes, `git show 81b81173:corpus/knowledge/appraisal-judgment-records-r83.md | sed -n 56p`):

```
"proposed judgment" of row 7 is a gate's or counter's verdict. Read that way, the rows describe practice the lane already
```

Command and observed result (receipt `c2-k3-rev-quote-leading-dq.txt`):

```
python3 land/tools/gate-records.py verify --root land --repo /home/vgpnk/Projects/shokunin/chousa-shokunin k3/rev-quote-entry-line56.md
GATE_RECORD k3/rev-quote-entry-line56.md:1 S199 FAIL PARSE
GATE_RECORDS files=1 records=1 ok=0 fail=1
rc=1
```

Isolation (receipt `c2-k3-isolation-and-fix.txt`): the same record with the single leading `"` removed
prints `OK`, rc 0. The only difference is the first character of the quote. The tool therefore refuses a
genuine record that meets every docstring check, which is exactly C2 kill rule K3 ("a genuine record —
one that meets every docstring check — on which the landed tool prints FAIL ... → C2 falsified").

Impacted axes: C2 operability (capability acquisition), the rev record form, the closed record class.
The defect is a false refusal, not a missing check: the rev form cannot record a quote whose source line
begins with a quotation mark, including line 56 of the round's own entry.

Kill-rule status, for completeness: K1 is met (`c2-landing.txt`: `TOOL=present ... RC=3/3`,
`GATE_RECORDS_R83=PASS`, rc 0; `c2-predicate-b-tip.txt`: `records=3 ok=3 fail=0`, rc 0). K2 found no
in-class record that violates a docstring check while the tool prints `OK`; the coverage gaps are in 1.3.
K4 holds: the empty-file run exits 1 (`EMPTY_REFUSED=1/1` in `c2-landing.txt`) and the tool's `main()`
returns 0 only when `n >= 1 and ok == n`, so no `FAIL` line can accompany exit 0. K3 is the firing rule.

Smallest safe correction (tested, not applied to the lane): delete `or quote.startswith('"')` from the
rev branch. The fixed copy `gate-records-fixed.py` prints `OK` on the record above (rc 0) and the frozen
counter still prints `TOOL=present POSITIVE=15/15 FORGED_REFUSED=198/198 EXPECTED_CODE=198/198
EMPTY_REFUSED=1/1 RC=3/3`, `GATE_RECORDS_R83=PASS`, rc 0 (receipt `c2-fixed-tool-counter.txt`). No
forgery in the frozen 198 relies on the removed restriction.

### 1.2 The frozen counter is gameable by a non-implementing lookup (residual, not a frozen kill)

The counter's PASS condition is `POSITIVE=15/15`, `FORGED_REFUSED=198/198`, `EXPECTED_CODE=198/198`,
`EMPTY_REFUSED=1/1`, `RC=3/3`. The expected-code test is a subset test (`if code in v[1]`), and the
forged files are written as `f<NNN>.md` (counter `mutations()`/`main()`). Two controls cheaper than the
claimed work pass the whole battery:

- `cheap-fname.py` (54 lines): every in-class record in a file whose basename matches `^f\d{3}\.md$` gets
  `FAIL` with *all* codes; every other record gets `OK`. It reads no registry, capture, refetch or git.
  Command (receipt `c2-cheap-fname.txt`):
  ```
  python3 -B land/corpus/evidence/round83/gate-records-r83.py --root land \
    --repo /home/vgpnk/Projects/shokunin/chousa-shokunin \
    --work /fast/scratch/hyaku/chousa-r83/R83CriticClaims/c2work \
    --tool /fast/scratch/hyaku/chousa-r83/R83CriticClaims/cheap-fname.py
  TOOL=present POSITIVE=15/15 FORGED_REFUSED=198/198 EXPECTED_CODE=198/198 EMPTY_REFUSED=1/1 RC=3/3
  GATE_RECORDS_R83=PASS
  rc=0
  ```
- `cheap-whitelist.py` (68 lines): collects every in-class `GATE-RECORD` line from
  `corpus/lessons/*.md` under `--root`, accepts byte-equal lines, refuses everything else with all codes.
  It reads no registry, capture, refetch or git. The same counter command with
  `--tool .../cheap-whitelist.py` gives the identical `TOOL=present ... RC=3/3`,
  `GATE_RECORDS_R83=PASS`, `rc=0` (receipt `c2-cheap-whitelist.txt`).

Both also pass predicate (b) at the tip. Command and observed (receipt `c2-cheap-tip-b.txt`):
```
cd tip && python3 /fast/scratch/hyaku/chousa-r83/R83CriticClaims/cheap-whitelist.py verify --root . corpus/lessons/round-83.md
GATE_RECORD corpus/lessons/round-83.md:19 ? OK
GATE_RECORD corpus/lessons/round-83.md:20 ? OK
GATE_RECORD corpus/lessons/round-83.md:21 ? OK
GATE_RECORDS files=1 records=3 ok=3 fail=0
rc=0
```
`cheap-fname.py` gives the same `records=3 ok=3`, rc 0 on the same file because the lesson file is not
named `f<NNN>.md` (same receipt).

The weaker named controls behave as expected and do not pass: `cheap-zyzzyva.py` (refuse only lines
containing `Zyzzyva`) gives `FORGED_REFUSED=24/198 EXPECTED_CODE=24/198`, FAIL, rc 1
(`c2-cheap-zyzzyva.txt`); `cheap-regrefetch.py` (registry row + refetch row only) gives
`FORGED_REFUSED=41/198 EXPECTED_CODE=31/198`, FAIL, rc 1 (`c2-cheap-regrefetch.txt`).

Does the claim text still verify? The landed tool's code does implement the named checks (registry row and
tier, capture path/key/sha, refetch row, quote location and word count, rev blob line), so the claim is
true of the landed bytes; but the frozen predicate does not establish it. A 54-line lookup that checks
nothing passes both predicate (a) and (b). The counter's own `c2-f2-stub-refuse` receipt already shows the
expected-code test is not discriminative (`POSITIVE=0/15 FORGED_REFUSED=198/198 EXPECTED_CODE=198/198`);
the missing control is a whitelist or filename-keyed tool that also passes `POSITIVE`. The battery is
gameable; this is a measurement defect, out of class for K1–K4 (the landed tool is not the cheap control),
and is listed as a residual.

### 1.3 Coverage of the 198 (docstring checks without a forgery)

Receipt `c2-coverage-gaps.txt` enumerates the composition by importing the frozen counter's `mutations()`
over the 15 positives (command: `python3 - <<PY` importing
`land/corpus/evidence/round83/gate-records-r83.py` and printing the label/code counts; the receipt carries
the full output): 10 admits x 17 + 1 unreach x 4 + 4 rev x 6 = 198. Every one of the 12 codes has at
least one forgery, but the following sub-checks have none:

- `PARSE`: missing key (`M15`), duplicate key (`M16`), and one bad value (`U04`: `decision=admit` in the
  unreach form); no unknown key or extra-text forgery.
- `CAPTURE_PATH`: only `../` traversal (`M04`); no symlink or non-regular-file case.
- `CAPTURE_SHA`: only flip (`M05`) and short (`M06`); no non-hex or >64-digit case.
- `REFETCH`: only record-side changes (`M07`, `M17`, `U01`–`U03`); no tsv-side `curl_rc`/`http`/`txt_sha256`
  mismatch case (the counter cannot mutate `refetch.tsv`).
- `REGISTRY`: only an absent row (`M01`); no wrong-column-count case.

The expected-code check is a subset test, so a tool that prints all codes for every refusal scores
`EXPECTED_CODE=198/198` (the c2-f2 receipt); the counter relies on `POSITIVE` to reject blanket refusal,
which the whitelist control defeats.

### 1.4 Thinness

Not thin against the hand "Location command": that command (`corpus/lessons/round-81.md:31-38`,
`round-82.md:64-71`) checks only quote occurrence and `wc -w`; the tool adds registry/tier, capture
path/key/sha, refetch, and rev blob/line checks. `tools/quote-reopen.py` is a live re-open tool, not an
offline record verifier, so it is not a duplicate. The tool is a real capability addition; the defect in
1.1 is a fixable bug, not thinness. Command and receipt `c2-thinness-compare.txt`:
```
sed -n '31,38p' land/corpus/lessons/round-81.md; sed -n '64,71p' land/corpus/lessons/round-82.md
sed -n '1,30p' land/tools/quote-reopen.py; sed -n '20,45p' land/tools/gate-records.py
```

## 2. C1 — depth (the appraisal entry)

### 2.1 The frozen predicate is gameable by content-free rows (residual/alignment)

The counter's PASS condition is structural: `entries>=1`, every new entry passes E1–E7, where E5 only
requires each non-Warrant cell to have >=3 words and not be a placeholder. The claims.md declares the
`c1-b1-salad-boundary` PASS as the counter's limit ("the counter does not judge whether a row follows from
its quote; kill rule K3 does"). The declared B1 control has 5 rows/5 quotes and passes.

A control at the exact predicate thresholds is also content-free. `c1-b1plus-entry.md` (copied to the
receipt folder) has 7 decision rows whose Do/Never cells are `unrelated action words N` /
`unrelated prohibition words N`, 8 located quotes from S009/S212/S213, and 3 fresh sources; the registry
rows S009/S212/S213 are replaced to name it, and the candidate entry is removed. Command (receipt
`c1-b1plus-contentfree-7rows-8quotes.txt`; setup: `git -C lane archive 81b81173 | tar -x -C b1plus`,
remove `b1plus/corpus/knowledge/appraisal-judgment-records-r83.md`, write
`b1plus/corpus/knowledge/ctl-entry-r83.md`, replace the three registry rows):

```
python3 -B b1plus/corpus/evidence/round83/depth-r83.py --root b1plus
ENTRY ctl-entry-r83.md ok=yes rows=7 quotes=8/8 fails=-
DEPTH_R83 entries=1 ok_entries=1 rows=7 located_quotes=8 fresh_sources=3
DEPTH_R83=PASS
rc=0
```

That is the claim's exact predicate target (`entries=1 ok_entries=1`, `rows=` >= 7, `located_quotes=` >= 8,
`fresh_sources=3`, `DEPTH_R83=PASS`, rc 0) met by an entry that teaches nothing. The predicate therefore
does not measure "teaches how to record an appraisal judgment"; the content claim rests on K3. The actual
entry passes K3 on my read (2.2), so C1 holds, but the predicate alone is insufficient and the B1 boundary
extends to the exact thresholds.

### 2.2 K3 (warrant) — not fired on the strongest counterexample I found

The strongest candidate is row 1's Never, "record one person's judgment as though two had made it
independently", warranted by Q4/Q5 (S212). Q4 states "Risk-of-bias assessments in Cochrane reviews should
be performed independently by at least two people"; Q5 states the purpose ("ensure that the judgement is
not influenced by a single person's preconceptions"). The Never is the record-level implication of that
standard; no sentence of S212 contradicts it. The only tension in the same source is line 622, the Millard
study finding that "about one-third of articles could be assessed by just one reviewer if such a tool is
used instead of the two required reviewers" — a study finding, not a standard, and the entry's Limits
disclose it. The S213 other case (line 593: expected-reporting items, absence leads to concerns) is
likewise disclosed, and row 8 is scoped to problem-seeking questions. The other nine rows are direct
restatements of their quotes. No K3(a) or K3(b) row was found. Command and receipt `c1-k3-captures.txt`:
```
sed -n '611p;615p;620p;622p' land/corpus/captures/708022d401fd771fc59bd1d9.txt
sed -n '593p;601p;602p' land/corpus/captures/963807d173af711593fd1c45.txt
```
The observed lines are the S212 7.3.2 paragraph (611), the transparency/MECIR Box 7.3.b paragraph (615),
the C54/C55 support paragraph (620), the Millard study paragraph (622), and the S213 No-information
paragraph (593), algorithm paragraph (601), and free-text/quotation paragraph (602).

Content mapping (claim sentence to entry rows, from `land/corpus/knowledge/appraisal-judgment-records-r83.md`):
duplicate independent judgment -> row 1 (Q4/Q5); disagreement process fixed in advance -> row 2 (Q6/Q7);
support recorded -> row 3 (Q1/Q11); source location recorded -> row 5 (Q8/Q2); narrow "no information" ->
row 8 (Q15, scoped to problem-seeking questions); overriding a proposed judgment only with a stated reason
-> row 7 (Q12/Q13). Rows 4, 6, 9 and 10 add quotation, outside-document assumptions, the concern
threshold, and conflicts of interest. All ten rows are in the Decision table. This is the content the
predicate cannot see (2.1); K3 is the check that reads it.

### 2.3 K4 (ground) — holds

`grep -rniE 'S009|S212|S213|mecir-manual/standards-conduct|handbook/current/chapter-07|handbook/current/chapter-08'`
over the 94 base-list entries (excluding the new entry) returns NO HITS (`c1-k4-base-grep.txt`). The base
entries cite Cochrane Handbook chapters 2, 4, 24 and IV, not 7/8, and no base entry names S009/S212/S213.
K4 does not fire.

### 2.4 K2 (located) — committed captures pass; live-page branch unrun

The frozen counter's E3 locates all 16 declared quotes in the committed captures (`quotes=16/16` in
`c1-depth-landing.txt`). The K2 live-page branch (a non-author re-open returning HTTP 200, tag-stripped)
was **not run**: this seat's item names no re-open and the egress table allows a re-open only for a URL
named in the seat's item. An unrun check is not a pass; the C1 held verdict is for the committed-capture
and counter checks only.

## 3. Freeze discipline

`freeze-blob-compare.txt` records the blob ids at `1b9b2ff8`, `3fbf8d12`, `81b81173`, `aca2a781`:

- `depth-r83.py` `46a2f6a99e09...`, `gate-records-r83.py` `1ff810f6a5c7...`, `c2-positives.tsv`
  `11e102754032...`, `base-knowledge.txt` `ffa6a1bbb26b...`, `run-controls-r83.sh` `4b7c873d702e...`:
  identical at all four revisions.
- `claims.md` `94eea54228a2...` and `instrument-pins.txt` `f0f897ca9f6d...`: absent at prefreeze, added
  at freeze, identical at landing and tip.
- Commit times: egress `2026-11-06T17:53:00-03:00` (20:53:00Z), prefreeze `17:57:53`, freeze `17:59:58`,
  landing `18:02:56`; the first round-83 refetch rows are 20:53:06/07/08Z.
- `pins-check.txt`: the sha256 values in `instrument-pins.txt` match the landing files exactly.

No predicate or counter byte changed between the freeze and the landing. The freeze-to-landing diff adds
`tools/gate-records.py` and the entry and touches `corpus/SOURCES.md`, `SKILL.md` and `corpus/README.md`;
the tip adds the round-83 lesson and the round's integration files. The claims.md
disclosure that the tool was drafted in scratch before the freeze and run against the battery while the
counter was written is accurate and is the methodological risk the gameability finding in 1.2 confirms:
the counter and the tool share an author and were co-evolved. That is a process residual, not a byte-level
freeze violation.

## 4. Controls adequacy

The frozen prefreeze driver reproduces 8/8 (`receipts-prefreeze/summary.tsv`,
`CONTROLS_AS_EXPECTED=8/8`), including `c1-b1-salad-boundary` PASS (rows=5, quotes=5/5) and the four C2
stubs FAIL. The controls are adequate for the declared boundaries but not for the capability claims:

- C2: the missing control is a whitelist or filename-keyed tool that refuses with all codes and accepts
  the positives; it passes the frozen counter (1.2). The existing `c2-f2-stub-refuse` fails on
  `POSITIVE` and `RC` (2/3), not on the forged/expected-code checks, so it does not test this.
- C1: the missing control is a content-free entry at the exact thresholds (7 rows/8 quotes); it passes the
  frozen predicate (2.1). The existing B1 control stops at 5/5.

## 5. Residuals (out of class for the frozen kill rules)

1. C2 counter gameability by a filename-keyed or lesson-whitelist lookup (1.2); the claim's measurement
   does not establish the claimed checks.
2. C2 coverage gaps in the 198 (1.3); the expected-code test is a subset test.
3. C1 predicate gameability by content-free rows at the exact thresholds (2.1); the content claim rests
   on K3, not the counter.
4. C1 K2 live-page branch unrun (2.4); no network under this seat's item.
5. C1 row 1's Never generalizes the S212 assessment standard to the record; I read it as entailed and the
   entry's Limits disclose the study-finding tension, but a stricter reviewer could argue K3(a). Not a
   kill on this read.

## 6. Verdicts

VERDICT: R83CriticClaims C2 fired — the landed tool refuses a genuine rev record whose quote begins with a double quote (`FAIL PARSE`, rc 1) while the same record without that one character prints `OK`; the one-line parse fix restores `OK` and keeps the frozen counter `PASS`.
VERDICT: R83CriticClaims C1 held — the frozen depth counter passes at landing (rows=10, located_quotes=16, fresh_sources=3) and no base entry cites S009/S212/S213; the counter is gameable by content-free rows at the exact thresholds, so the content claim rests on K3, which I read as holding; K2's live-page branch was not run (no network).

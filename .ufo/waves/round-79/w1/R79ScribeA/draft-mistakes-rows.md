# Round 79 corpus text — `## Mistakes` rows for `corpus/lessons/round-79.md` (drafted, not landed)

Seat `R79ScribeA`, lane `chousa-shokunin`. Base `ee70e6df19fe43b1b384166cf5d360c3b99dafe2`;
prefreeze instruments, controls and repairs `e2bf2bbb5ca66f06b6571cbcaa15554d1a74a67c`; lane tip
`b58a02dbc8876dd1ad7647d88ca2c9cb2ae51ff9`.

The `## Mistakes` table header in the round-78 lesson is `| class | evidence | captured-by | fix |`
(`corpus/lessons/round-78.md:48`), and the four columns are the contract's
(`CORPUS.md` § *kaika campaign rules*: "class · evidence pointer · captured-by (the `QUALITY.md`
criterion or protocol rule that should have caught it, or `none`) · fix"). Classes come from
`mistakes.md` §5's vocabulary (`vacuous`, `survivor`, `stale-premise`, `reference-drift`,
`number-drift`, `scope`, `attribution`, `landing`, `provider`).

**The L1's lesson already exists** at `corpus/lessons/round-79.md` (untracked, 11 412 bytes, as
of this seat's read). It carries five `## Mistakes` rows. The three rows below are the ones this
seat was asked for; they are **not** already among those five, and each is independently
measured here. The first two are about the round-78 record, the third is a defect found in a
round-79 instrument while reading it.

---

## (a) The three requested rows

| class | evidence | captured-by | fix |
|---|---|---|---|
| survivor | The round-78 salt family was a normalizer away from gone, and the normalizer survived into round 79 as a shipped forger: `.ufo/waves/round-78/w1/R78L1/a8-normalizer.py` deletes the `_r78<hex>` statement family, hashes the remainder and classifies every subject against two hard-coded positive digests — its own docstring says "Scores nothing." It reached the round-78 battery's exact target line at exit 0 (`R78L1/a8-normalizer-v5.txt:113`, `BATTERY=PASS forgers_rejected=11/11 positive=2/2 oracle=REJECTED`), while the round-77 battery refused the same file (`R78L1/a8-normalizer-v4.txt:116`, `BATTERY=FAIL … positive=0/2`, exit 1). The round-79 forger set reuses that file **byte-identically**: `sha256sum .ufo/waves/round-78/w1/R78L1/a8-normalizer.py corpus/evidence/round79/forgers/a8-v5-salt-normalizer.py` prints `65f590afaa6cf88ff40807ba9f61cd5d661d6bfe98a792f2dd5d965d6373c953` for both, `diff` exit 0. | QUALITY 147 (the salt family is a per-channel measurement, not a property of the salt) — carried into round 79 as criterion 147's successor requirement; no criterion said the normalizer must be *retired*, only that the closure be re-measured | The round-79 battery re-emits the subject as a marshalled code object under a random name, so no source text is a textual derivative: `python3 -B corpus/evidence/round79/derivative-check.py --battery corpus/evidence/round79/matrix-battery-v6.py --work DIR` prints `DERIVATIVE_COPIES=0/13 MAX_WINDOW=23` exit 0 (`receipts/derivative-v6.txt`), against `13/13 MAX_WINDOW=4096` exit 1 on the round-78 battery (`receipts/derivative-v5.txt`). The surviving normalizer is now a **named, refused forger**: `FORGER a8-v5-salt-normalizer rc=1 … verdict=REFUSED` (`receipts/forge-battery-v6.txt`), and the channel it opens — the structure-identity channel, which unmarshals the payload instead of stripping text — is recorded as an open limit in the lesson, not closed |
| scope | Round 78's self-assessment counter audited only the newest `## Round-<n> addition` block, so an appended block hid every earlier criterion from pointer auditing. The receipt that shows it: `.ufo/waves/round-78/w1/R78ReviewB/atkB2-new-block-window.txt` (11 lines) prints `SELFCHECK=PASS unresolved=0/3` at exit 0 on a mirror carrying "HEAD QUALITY + empty Round-79 block; no supersedes anywhere" (its line 2) — a clean pass with the defect still present. The rule that produced it is in the counter's own source: `corpus/evidence/round78/selfcheck.py:138` `if re.match(r"^## Round-\d+ addition", line):` sets `start` to the **last** matching block, and `check_quality` iterates only `lines[start:]`. | QUALITY 146 (the successor requirement the round-78 counter's receipts produced, written as a requirement on the next counter) | The round-79 counter drops the block window entirely: `corpus/evidence/round79/selfcheck-v2.py` has no `## Round-` anchor and its `criteria()` (`selfcheck-v2.py:139-150`) parses criteria from the whole file, so the audit covers every block. Measured on a scratch mirror that appends a `## Round-80 addition` block and plants an unresolvable pointer in criterion 116 (`receipts/probeW-window.txt`): the round-78 counter prints `SELFCHECK=PASS unresolved=0/3` exit 0 (the defect hidden), the round-79 counter prints `CHECK S2-quality-pointers FAIL … unresolved=['116:corpus/evidence/round59/probeW-absent.md']` and `SELFCHECK2=FAIL unresolved=1/3` exit 1 (the defect seen). The round-79 control reproduces both halves at the lane's own bytes: `corpus/evidence/round79/controls/selfcheck-control-before.txt` prints `CONTROL=PASS cases=4 v1_false_greens=2/2 v2_refusals=2/2` |
| scope | The round-79 counter's own docstring claims the S2 check covers "**every** criterion in the file, not only the newest block" (`corpus/evidence/round79/selfcheck-v2.py:18`), but its criterion regex is three-digit-only: `selfcheck-v2.py:54` `CRITERION = re.compile(r"^(\d{3})\.\s")`. The file has 149 numbered criteria and the counter parses 50 of them — `grep -cE '^[0-9]+\. ' corpus/QUALITY.md` prints 149, and the counter's own receipt prints `criteria=50` (`corpus/evidence/round79/controls/selfcheck2-after.txt:3`). Criteria 1–99 are therefore invisible to the pointer audit, so a dead pointer planted in a two-digit criterion passes. Measured on a scratch mirror: criterion 5 gains `corpus/evidence/round59/probeN-absent.md`, and the counter still prints `CHECK S2-quality-pointers ok … unresolved=[]` and `SELFCHECK2=PASS unresolved=0/3` at exit 0 (`receipts/probeN-number-width.txt`). | no criterion: QUALITY 146 requires the audit window to cover every **block**, and the round-79 instrument satisfies that literally — the criterion-number width is a second, unnamed axis of the same gap | the frozen instrument is not amended. The gap is recorded as a limit, the successor's requirement is that the criterion regex accept any numbered criterion (`^(\d+)\.\s`) **and** that the counter report the criterion count it parsed beside the total it found, so a silent narrowing cannot read as a clean pass. Note the class this belongs to is *scope*, not *vacuous*: the three frozen classes (116, 102, 103) are all three-digit, so the frozen predicate `SELFCHECK2=PASS unresolved=0/3` is unaffected and this is a post-freeze finding, not a falsification |

---

## (b) Three corrections to the L1's landed `## Gate` — all measured, all in the lane's own bytes

The L1's `corpus/lessons/round-79.md` `## Gate` block (lines 12–33) and the registered rows
`S196`/`S197`/`S198` (`corpus/SOURCES.md:208-210`) are landed. Three of their numbers do not
match the bytes they cite. These are `number-drift` and `reference-drift` in the round's own
prose — exactly the class the round-78 closure flagged in its routed defect 11.

### Correction 1 — S196's located quote is 27 words, not 25

The lesson's Gate line 17 says the quote is "(25 words, `wc -w`)". Measured:

```
$ git show ee70e6df19fe43b1b384166cf5d360c3b99dafe2:corpus/QUALITY.md | sed -n '1056p' | grep -o 'A subject-identity salt is defeated by any normalizer that knows its marker family, so the closure is a per-channel measurement and not a property of the salt' | wc -w
27
```

The quote as printed in the lesson is the criterion 147 opening requirement; it is **27** words.
Both counts are ≤25? No — 27 is **over** the contract's 25-word bound
(`CORPUS.md` § *SOURCES.md* rule 1: "a ≤25-word quote with its location grounding `teaches`").
The quote must be shortened. Two shorter quotes from the same line 1056, both verified:

```
$ git show ee70e6df19fe43b1b384166cf5d360c3b99dafe2:corpus/QUALITY.md | sed -n '1056p' | grep -o 'A subject-identity salt is defeated by any normalizer that knows its marker family' | wc -w
13
$ git show ee70e6df19fe43b1b384166cf5d360c3b99dafe2:corpus/QUALITY.md | sed -n '1056p' | grep -o 'the closure is a per-channel measurement and not a property of the salt' | wc -w
13
```

Both alternatives are 13 words. The first is recommended (it carries the claim's subject); the
second is the tail clause and grounds `teaches` less directly.

Recommended replacement for the Gate line: `Located quote: "A subject-identity salt is defeated by
any normalizer that knows its marker family" (13 words, `wc -w`).`

### Correction 2 — S197's located quote is 25 words, not 24

The lesson's Gate line 23 says "(24 words)". Measured:

```
$ git show ee70e6df19fe43b1b384166cf5d360c3b99dafe2:corpus/QUALITY.md | sed -n '1054p' | grep -o 'A self-assessment counter validates each resolution line against the bytes it claims to repair, and its audit window covers every block rather than the newest' | wc -w
25
```

25 is exactly the contract bound, so the quote is admissible; only the stated count is wrong.
The count must read **25 words** (the r78 lesson's own precedent: `corpus/lessons/round-77.md`
records a corrected count of 11 after `R77ScribeA` re-measured it with `wc -w`).

### Correction 3 — S198's located quote is not in the file it is attributed to

The lesson's Gate line 27 gives the located quote as "the audit window is the last
`## Round-\d+ addition` block". That string does not occur in the cited receipt, nor in the
spot-check, nor anywhere in the lane's corpus:

```
$ grep -c "audit window is the last" .ufo/waves/round-78/w1/R78ReviewB/atkB2-new-block-window.txt
0
$ grep -c "audit window is the last" corpus/lessons/round-78-verifier-spotcheck.md
0
$ grep -rn "audit window is the last" corpus/ .ufo/waves/round-78/ 2>/dev/null
corpus/lessons/round-79.md:28:  Opened 2026-11-04. Located quote: "the audit window is the last `## Round-\d+ addition` block".
```

The only occurrence is in the round-79 lesson itself — the sentence the Gate line writes. The
quoted words are a paraphrase of the **predecessor's source**, not of the receipt:
`corpus/evidence/round78/selfcheck.py:138` reads
`if re.match(r"^## Round-\d+ addition", line):`. A `## Gate` located quote must be a quote of
the source it names. Two admissible quotes from the cited receipt, both verified by `sed -n`:

```
$ sed -n '2p' .ufo/waves/round-78/w1/R78ReviewB/atkB2-new-block-window.txt
# HEAD QUALITY + empty Round-79 block; no supersedes anywhere
$ sed -n '11p' .ufo/waves/round-78/w1/R78ReviewB/atkB2-new-block-window.txt
SELFCHECK=PASS unresolved=0/3
```

The file is 11 lines, so the S198 row's anchor "wave file lines 1-20" (`corpus/SOURCES.md:210`)
also overstates the span; it should read "wave file lines 1-11". The row's revision pin is
correct and verified — the file is tracked at `3eb4a3cad8febf75698a017cb6c4441f763b3454` and at
the lane tip `b58a02db`:

```
$ git ls-tree -r --name-only 3eb4a3cad8febf75698a017cb6c4441f763b3454 | grep atkB2
.ufo/waves/round-78/w1/R78ReviewB/atkB2-new-block-window.txt
$ git ls-tree -r --name-only b58a02db | grep -c atkB2-new-block-window
1
```

One more mismatch, on the S198 row's own `source` cell: it reads "round-78 hollow-mirror
**receipt**" but points at `atkB2-new-block-window.txt`, which is the **window** receipt. The
hollow-mirror receipt is a different file, `R78ReviewB/ALL-three-hollow.txt` (its line 2 reads
"row168 malformed+wrong; 142 dead pointer + gutted 144; row73 stranded — all repairs
hollow/false"). Under contract v1 rule 2 a correction is a new row, so the fix is a new row
carrying `supersedes S198 —` with the title matching the file it cites, not an in-place edit.

## (c) The three requested rows are not among the L1's five — confirmed

The L1's five rows are: the superseder criterion re-quoting the absent path; the first
all-block pointer measurement's 18 false positives; the three registry rows landing outside the
`## Registry` table; the claims file's class provenance and reach; and the control receipt
labelled `REV=worktree`. None of them is the round-78 salt normalizer, the round-78 window bug,
or a round-79 instrument defect, so the three rows above are additive rather than replacements.

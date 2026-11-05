# Round 79 corpus text — `## Gate` block for `corpus/lessons/round-79.md` (drafted, not landed)

Seat `R79ScribeA`, lane `chousa-shokunin`. Base `ee70e6df19fe43b1b384166cf5d360c3b99dafe2`;
prefreeze instruments, controls and digest-bearing repairs
`e2bf2bbb5ca66f06b6571cbcaa15554d1a74a67c`; lane tip
`b58a02dbc8876dd1ad7647d88ca2c9cb2ae51ff9`.

Landed ids S196 and S197 are already registered and are bound by the frozen claims file
(`corpus/evidence/round79/claims.md` lines 28 and 75: C1 "Sourced on S196", C2 "sourced on
S197"). Contract v1 rule 2 makes the registry append-only and forbids reusing an id. The
registry's last id is S198 (198 rows), so the next unused id is **S199** — and only **one**
new row is needed: the round-78 spot-check's routed defect 2, the closure-record source that
r78 registered as S193 and that round 79 has no row for. See `draft-sources-rows.md` for the
id-collision evidence.

**The L1's `corpus/lessons/round-79.md` already carries a `## Gate` block** (lines 12–33) with
the S196/S197/S198 admits. The block below is the **S199 admit plus the three corrections** that
`draft-mistakes-rows.md` § (b) measures — the L1 can either splice the S199 bullet into the
existing block or replace the block wholesale with this one.

Paste this block verbatim as the `## Gate` section of `corpus/lessons/round-79.md`.

```markdown
## Gate

- Admit S196, own-work B, scoped to QUALITY 147's successor requirement for the outer battery's
  subject copy. `corpus/QUALITY.md` at `ee70e6df19fe43b1b384166cf5d360c3b99dafe2`, criterion 147
  at line 1056, quote inside its opening requirement sentence. Opened 2026-11-04. Located quote:
  "A subject-identity salt is defeated by any normalizer that knows its marker family" (13
  words, `wc -w`). Grounds C1's target: it is a requirement produced by round 78's own
  falsification, not a measurement of the successor.
- Admit S197, own-work B, scoped to QUALITY 146's successor requirement for the self-assessment
  counter. `corpus/QUALITY.md` at `ee70e6df19fe43b1b384166cf5d360c3b99dafe2`, criterion 146 at
  line 1054, quote inside its opening requirement sentence. Opened 2026-11-04. Located quote:
  "A self-assessment counter validates each resolution line against the bytes it claims to repair,
  and its audit window covers every block rather than the newest" (25 words). Grounds C2's target.
- Admit S199, own-work B, scoped to the round-78 non-author spot-check's routed defect 2 — the
  r78 counter's lexical escape hatches and its newest-block-only QUALITY audit window.
  `corpus/lessons/round-78-verifier-spotcheck.md` at
  `b58a02dbc8876dd1ad7647d88ca2c9cb2ae51ff9`, routed-defect list lines 189–192, quote on line
  189. Opened 2026-11-04. Located quote: "`selfcheck.py`'s escape hatches are lexical
  (`correction:` / `supersedes:` / `erratum:`" (10 words, `wc -w`). Grounds C2's second class:
  it is the closure record that names the defect, not independent truth that the successor
  closes it — the committed counter and its receipts are.
- Reject S198, own-work C, scoped to a defect receipt offered as a source about verification
  method. `.ufo/waves/round-78/w1/R78ReviewB/atkB2-new-block-window.txt` at
  `3eb4a3cad8febf75698a017cb6c4441f763b3454`, wave file lines 1–11, quote on line 2.
  Opened 2026-11-04. Located quote: "HEAD QUALITY + empty Round-79 block; no supersedes
  anywhere" (9 words, `wc -w`). REJECTED: a receipt that demonstrates one counter's false green
  is that counter's own evidence, not a source about how self-assessment should be audited (the
  S195 class one layer out); flip: admit scoped to what a control receipt must carry if an
  admitted entry ever rests on receipt format.
- New registry rows S196/S197/S199 mined, used-by this lesson; S198 rejected, used-by `—`.
  Existing `status`/`recheck`/`used-by` cells unchanged. No URL opened or fetched: all four are
  revision-pinned committed paths.
- Non-author spot-check requested: three admits and one reject above. Dispatched wave seats are
  author-lane evidence, not independent admission or promotion reviewers.
```

## Why the S196/S197 ids are not reused (the L1 reads this before landing)

```
$ grep -nE '^\| S19[678] ' corpus/SOURCES.md          # at the lane tip b58a02db
208:| S196 | chousa QUALITY criterion 147 — corpus/QUALITY.md | ...
209:| S197 | chousa QUALITY criterion 146 — corpus/QUALITY.md | ...
210:| S198 | round-78 hollow-mirror receipt — ... | ... | rejected | ...
$ grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md
198
```

```
$ git show e2bf2bbb:corpus/evidence/round79/claims.md | grep -n 'Sourced on S196\|sourced on S197'
28:reports. Sourced on S196.
75:## C2 — calibration (sourced on S197)
```

The ids are live and the claims file is frozen; a scope change in place would break contract
v1 rule 2 (append-only, ids never reused). The drafted rows therefore take the next unused ids.

## Two independent confirmations that the S200 scope is the right one

The S200 quote's source line is the closure's own routed-defect list, and the defect it names
is the one the round-79 successor closes. Both halves are measurable:

**The lexical escape hatches are closed** — the round-79 control shows the round-78 predecessor
reaching a false green on a hollow mirror and the successor refusing it:

```
$ cat corpus/evidence/round79/controls/selfcheck-control-before.txt
CASE hollow v1 rc=0 SELFCHECK=PASS unresolved=0/3
CASE hollow v2 rc=1 SELFCHECK2=FAIL unresolved=3/3
CASE window v1 rc=0 SELFCHECK=PASS unresolved=0/3
CASE window v2 rc=1 SELFCHECK2=FAIL unresolved=3/3
CONTROL=PASS cases=4 v1_false_greens=2/2 v2_refusals=2/2
```

**The newest-block-only window is closed** — the round-78 predecessor still hides an earlier
criterion behind a newer block; the round-79 successor does not. Measured on a scratch mirror
that appends a `## Round-80 addition` block and plants an unresolvable pointer in criterion
116 (receipt: `receipts/probeW-window.txt`):

```
# --- v1 (round-78 predecessor) ---
$ python3 -B corpus/evidence/round78/selfcheck.py --lane .
CHECK S2-quality-pointers ok
SELFCHECK=PASS unresolved=0/3
# exit: 0
# --- v2 (round-79 successor) ---
$ python3 -B corpus/evidence/round79/selfcheck-v2.py --lane .
CHECK S2-quality-pointers FAIL criteria=50 missing=[116] superseders={116: [149]} unresolved=['116:corpus/evidence/round59/probeW-absent.md']
SELFCHECK2=FAIL unresolved=1/3
# exit: 1
```

Both mirrors are under `$HYAKU_SCRATCH/chousa-r79/R79ScribeA/`; the lane tree was not touched.

## The one place the successor is narrower than its own docstring — a recorded limit, not a row

`corpus/evidence/round79/selfcheck-v2.py`'s docstring (line 18) says the S2 check covers
"**every** criterion in the file, not only the newest block". Its `CRITERION` regex
(`selfcheck-v2.py:54`) is `^(\d{3})\.\s`, so it parses only three-digit criterion numbers.
Measured on the tip tree:

```
$ grep -cE '^[0-9]+\. ' corpus/QUALITY.md      # 149 numbered criteria
$ python3 -B corpus/evidence/round79/selfcheck-v2.py --lane .
CHECK S2-quality-pointers ok criteria=50 missing=[116] superseders={116: [149]} unresolved=[]
```

50 of 149 criteria are parsed; criteria 1–99 are invisible to the S2 check. Probe N
(`receipts/probeN-number-width.txt`) plants an unresolvable pointer inside criterion **5** (a
two-digit criterion) on a scratch mirror and the counter still reports a clean pass:

```
$ python3 -B corpus/evidence/round79/selfcheck-v2.py --lane .
CHECK S2-quality-pointers ok criteria=50 missing=[116] superseders={116: [149]} unresolved=[]
SELFCHECK2=PASS unresolved=0/3
# exit: 0
```

This is **not** a C2 falsification: the frozen predicate is the three named classes (116, 102
and 103), all three-digit, and the kill rule names the newest-block window and the hollow
repair line, both of which the successor closes. It is a **post-freeze finding on the
instrument**, recorded in the lesson's `## Instrument limits` section and carried to the
successor as the third `## Mistakes` row. The frozen instrument is not amended.

A wider audit over the same file (all criterion numbers, `^(\d+)\.\s`) finds ten further
criteria below 100 whose backticked path-like tokens resolve to no committed path, at both
the base and the tip:

```
$ # base ee70e6df, all criterion numbers
BASE_WIDE_COUNT= 148
BASE_WIDE_MISSING_BELOW_100= {5: ['knowledge/'], 6: ['knowledge/'], 14: ['lessons/round-<N>.md'], 31: ['controls/ChousaR31.CtlShortcutC2/v2/'], 34: ['.ufo/waves/round-32/w1/CtlC1PartialLockB/b-s3247102{1,2}.json', 'v2/mutated-b-probe-only-s3247202{1,2}.json'], 35: ['<dir>/tools/research-gate.sh'], 36: ['.ufo/waves/round-32/w2/CriticAxis32/control-metadata-s3232002{1,2}.json'], 42: ['measure/final/fz-9021{2,3,4}.json'], 89: ['word/document.xml'], 99: ['<round>/<wave>.ready.dispatched']}
```

Most of those are template or glob tokens rather than real pointers (for example
`lessons/round-<N>.md`, `<dir>/tools/research-gate.sh`), so a widened audit would need its own
exclusions before it could be a counter. That is the successor's problem, not this round's.

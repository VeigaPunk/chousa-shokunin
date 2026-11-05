# R79ScribeA — round 79 corpus prose, drafted

Seat `R79ScribeA`, lane `chousa-shokunin`, role scribe. Leaf member: no subagents, no network, no
lane or fleet git/jj mutation, no commits, no production edits. Every file written is under
`.ufo/waves/round-79/w1/R79ScribeA/`; every clone, mirror and fixture lived under
`$HYAKU_SCRATCH/chousa-r79/R79ScribeA/` and was deleted before this report was written.

Base `ee70e6df19fe43b1b384166cf5d360c3b99dafe2` (round-78 lane tip); prefreeze instruments,
controls and digest-bearing repairs `e2bf2bbb5ca66f06b6571cbcaa15554d1a74a67c`; lane tip
`b58a02dbc8876dd1ad7647d88ca2c9cb2ae51ff9`.

## Drafts (paths)

| file | what it holds |
|---|---|
| `.ufo/waves/round-79/w1/R79ScribeA/draft-sources-rows.md` | the `corpus/SOURCES.md` candidate row (**S199**), the id-collision evidence for S196/S197, the anchors, and the `wc -w` counts |
| `.ufo/waves/round-79/w1/R79ScribeA/draft-gate-block.md` | the `## Gate` block for `corpus/lessons/round-79.md`, paste-ready, plus the S198 anchor/quote correction |
| `.ufo/waves/round-79/w1/R79ScribeA/draft-mistakes-rows.md` | the three `## Mistakes` rows, plus three measured corrections to the L1's landed `## Gate` |
| `.ufo/waves/round-79/w1/R79ScribeA/receipts/` | every receipt this report cites (`probeN-number-width.txt`, `probeW-window.txt`, `derivative-v5.txt`, `derivative-v6.txt`, `forge-battery-v6.txt`, `census-validate.txt`, `s196-quote.txt`, `s197-quote.txt`) |

## The two ids this seat was asked for are already taken — and the prompt's scope assignment
## conflicts with the frozen claims file

```
$ grep -nE '^\| S19[678] ' corpus/SOURCES.md
208:| S196 | chousa QUALITY criterion 147 — corpus/QUALITY.md | own-work | B | ... | mined | 2026-11-04 | on-release | corpus/lessons/round-79.md |
209:| S197 | chousa QUALITY criterion 146 — corpus/QUALITY.md | own-work | B | ... | mined | 2026-11-04 | on-release | corpus/lessons/round-79.md |
210:| S198 | round-78 hollow-mirror receipt — .ufo/waves/round-78/w1/R78ReviewB/atkB2-new-block-window.txt | own-work | C | ... | rejected | 2026-11-04 | on-release | — |
$ grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md
198
```

```
$ git show e2bf2bbb5ca66f06b6571cbcaa15554d1a74a67c:corpus/evidence/round79/claims.md | grep -n 'Sourced on S196\|sourced on S197'
28:reports. Sourced on S196.
75:## C2 — calibration (sourced on S197)
```

The frozen claims file binds **S196 → C1** (operability: the subject copy stops being a textual
derivative) and **S197 → C2** (calibration: the counter validates its own repairs). The landed
rows satisfy that binding: S196 is criterion **147** (the salt-family requirement, which states
C1's target) and S197 is criterion **146** (the presence-only-repair-line requirement, which
states C2's target).

The prompt's assignment read literally — S196 → "QUALITY 146's successor requirement", S197 →
"the round-78 spot-check's routed defect 2" — would put the *calibration* requirement on the id
the claims file binds to *C1*, and leave criterion 147 with no row. **What the seat delivers
instead:**

- **QUALITY 146's successor requirement** — already registered as the landed **S197**
  (`corpus/SOURCES.md:209`), with the correct anchor and `teaches`. **No new row.** The only
  defect is a word count in the lesson's `## Gate` line (24 stated, 25 actual), corrected below.
- **The round-78 spot-check's routed defect 2** — **no row exists**
  (`grep -n "round-78-verifier-spotcheck" corpus/SOURCES.md` → no output). This is the
  closure-record source that round 78 registered as S193 and that round 79 is missing. It takes
  the next unused id, **S199** (the registry's last id is S198). This is the one new row.

Contract v1 (`CORPUS.md` § *SOURCES.md*, rule 2) forbids reusing an id and requires a correction
to be a new row whose `teaches` opens `supersedes S0NN —`; nothing here reuses an id.

## The `## Gate` lines the lesson needs

Both rows' gates are in `draft-gate-block.md`, paste-ready. The `sed -n <line>p` output for the
new row's quote, and its word count:

```
$ git show b58a02db:corpus/lessons/round-78-verifier-spotcheck.md | sed -n '189p'
2. **`selfcheck.py`'s escape hatches are lexical** (`correction:` / `supersedes:` / `erratum:`

$ git show b58a02db:corpus/lessons/round-78-verifier-spotcheck.md | sed -n '189p' | sed 's/^[0-9]*\. //; s/\*\*//g' | wc -w
10
```

10 words — under the contract's 25-word bound. The `## Gate` line reads:

> Admit S199, own-work B, scoped to the round-78 non-author spot-check's routed defect 2 — the
> r78 counter's lexical escape hatches and its newest-block-only QUALITY audit window.
> `corpus/lessons/round-78-verifier-spotcheck.md` at
> `b58a02dbc8876dd1ad7647d88ca2c9cb2ae51ff9`, routed-defect list lines 189–192, quote on line
> 189. Opened 2026-11-04. Located quote: "`selfcheck.py`'s escape hatches are lexical
> (`correction:` / `supersedes:` / `erratum:`" (10 words, `wc -w`).

The other three Gate lines (S196, S197, S198) are the L1's, and three corrections to them are
measured in the next section.

## The three `## Mistakes` rows

Full rows with evidence, captured-by and fix are in `draft-mistakes-rows.md`. Classes come from
`mistakes.md` §5's vocabulary; the four columns are the contract's.

**Row 1 — `survivor`: the round-78 salt normalizer that survived.** It is byte-identical in the
round-79 forger set, and it reached the round-78 battery's exact target line at exit 0.

```
$ sha256sum .ufo/waves/round-78/w1/R78L1/a8-normalizer.py corpus/evidence/round79/forgers/a8-v5-salt-normalizer.py
65f590afaa6cf88ff40807ba9f61cd5d661d6bfe98a792f2dd5d965d6373c953  .ufo/waves/round-78/w1/R78L1/a8-normalizer.py
65f590afaa6cf88ff40807ba9f61cd5d661d6bfe98a792f2dd5d965d6373c953  corpus/evidence/round79/forgers/a8-v5-salt-normalizer.py
$ diff .ufo/waves/round-78/w1/R78L1/a8-normalizer.py corpus/evidence/round79/forgers/a8-v5-salt-normalizer.py
(no output; exit 0)
$ tail -3 .ufo/waves/round-78/w1/R78L1/a8-normalizer-v5.txt
RECEIPT_LINES=113
BATTERY=PASS forgers_rejected=11/11 positive=2/2 oracle=REJECTED
# exit: 0
$ tail -3 .ufo/waves/round-78/w1/R78L1/a8-normalizer-v4.txt
forgers_rejected=11/11 positive=0/2 oracle=REJECTED
BATTERY=FAIL forgers_rejected=11/11 positive=0/2 oracle=REJECTED
# exit: 1
```

The fix is measurable both ways — the round-79 battery re-emits the subject as a marshalled code
object, so no source text is a textual derivative, and the surviving normalizer is now a named,
**refused** forger:

```
$ python3 -B corpus/evidence/round79/derivative-check.py --battery corpus/evidence/round79/matrix-battery-v6.py --work DIR
DERIVATIVE_COPIES=0/13 MAX_WINDOW=23          # exit 0   (receipts/derivative-v6.txt)
$ python3 -B corpus/evidence/round79/derivative-check.py --battery corpus/evidence/round78/matrix-battery-v5.py --work DIR
DERIVATIVE_COPIES=13/13 MAX_WINDOW=4096        # exit 1   (receipts/derivative-v5.txt)
$ python3 -B corpus/evidence/round79/forge-battery.py --battery corpus/evidence/round79/matrix-battery-v6.py --work DIR
FORGER a8-v5-salt-normalizer rc=1 receipt_lines=113 trailer=yes integrity=ok verdict=REFUSED
FORGER a9-v6-wrapper-normalizer rc=1 receipt_lines=113 trailer=yes integrity=ok verdict=REFUSED
POSITIVE legit-matrix rc=0 receipt_lines=113 integrity=ok verdict=ACCEPTED
FORGE_BATTERY=PASS forgers_handled=6/6 positive=1/1     # exit 0  (receipts/forge-battery-v6.txt)
```

**Row 2 — `scope`: the round-78 selfcheck window bug.** The receipt that shows it:
`.ufo/waves/round-78/w1/R78ReviewB/atkB2-new-block-window.txt` (11 lines) prints
`SELFCHECK=PASS unresolved=0/3` at exit 0 on a mirror carrying "HEAD QUALITY + empty Round-79
block; no supersedes anywhere". The rule that produced it is the counter's own source,
`corpus/evidence/round78/selfcheck.py:138`:

```
$ sed -n '138p' corpus/evidence/round78/selfcheck.py
        if re.match(r"^## Round-\d+ addition", line):
```

The round-79 counter drops the block window; on a scratch mirror that appends a
`## Round-80 addition` block and plants an unresolvable pointer in criterion 116, the two
counters disagree (receipt `receipts/probeW-window.txt`):

```
# v1 (round-78 predecessor)
$ python3 -B corpus/evidence/round78/selfcheck.py --lane .
CHECK S2-quality-pointers ok
SELFCHECK=PASS unresolved=0/3
# exit: 0
# v2 (round-79 successor)
$ python3 -B corpus/evidence/round79/selfcheck-v2.py --lane .
CHECK S2-quality-pointers FAIL criteria=50 missing=[116] superseders={116: [149]} unresolved=['116:corpus/evidence/round59/probeW-absent.md']
SELFCHECK2=FAIL unresolved=1/3
# exit: 1
```

and the lane's own control reproduces both halves:

```
$ cat corpus/evidence/round79/controls/selfcheck-control-before.txt
CASE hollow v1 rc=0 SELFCHECK=PASS unresolved=0/3
CASE hollow v2 rc=1 SELFCHECK2=FAIL unresolved=3/3
CASE window v1 rc=0 SELFCHECK=PASS unresolved=0/3
CASE window v2 rc=1 SELFCHECK2=FAIL unresolved=3/3
CONTROL=PASS cases=4 v1_false_greens=2/2 v2_refusals=2/2
```

**Row 3 — `scope`: a defect in a round-79 instrument, found while reading it.**
`corpus/evidence/round79/selfcheck-v2.py`'s docstring (line 18) says the S2 check covers "**every**
criterion in the file, not only the newest block", but its criterion regex is three-digit-only:

```
$ sed -n '54p' corpus/evidence/round79/selfcheck-v2.py
CRITERION = re.compile(r"^(\d{3})\.\s")
$ grep -cE '^[0-9]+\. ' corpus/QUALITY.md
149
$ grep -n 'criteria=' corpus/evidence/round79/controls/selfcheck2-after.txt
3:CHECK S2-quality-pointers ok criteria=50 missing=[116] superseders={116: [149]} unresolved=[]
```

50 of 149 criteria are parsed; criteria 1–99 are invisible to the pointer audit. A dead pointer
planted in a two-digit criterion passes (receipt `receipts/probeN-number-width.txt`):

```
$ python3 -B corpus/evidence/round79/selfcheck-v2.py --lane .
CHECK S2-quality-pointers ok criteria=50 missing=[116] superseders={116: [149]} unresolved=[]
SELFCHECK2=PASS unresolved=0/3
# exit: 0
```

(criterion 5 on the scratch mirror carries `corpus/evidence/round59/probeN-absent.md`.)

**This is not a C2 falsification.** The frozen predicate is the three named classes (116, 102,
103), all three-digit, and the kill rule names the newest-block window and the hollow repair
line — both closed, as rows 2 and the control above show. It is a post-freeze finding on the
instrument: the frozen instrument is not amended, the gap is recorded as a limit, and the
successor requirement is that the criterion regex accept any numbered criterion
(`^(\d+)\.\s`) **and** that the counter print the criterion count it parsed beside the total it
found, so a silent narrowing cannot read as a clean pass.

## Three corrections to the L1's landed `## Gate` — all measured

The L1's `corpus/lessons/round-79.md` `## Gate` block (lines 12–33) and rows `S196`/`S197`/`S198`
(`corpus/SOURCES.md:208-210`) are landed. Three of their numbers do not match the bytes they
cite. Full detail in `draft-mistakes-rows.md` § (b).

**Correction 1 — S196's located quote is 27 words, not 25, and so it breaks the contract's
25-word bound.**

```
$ git show ee70e6df:corpus/QUALITY.md | sed -n '1056p' | grep -o 'A subject-identity salt is defeated by any normalizer that knows its marker family, so the closure is a per-channel measurement and not a property of the salt' | wc -w
27
```

Two admissible replacements from the same line, both verified:

```
$ git show ee70e6df:corpus/QUALITY.md | sed -n '1056p' | grep -o 'A subject-identity salt is defeated by any normalizer that knows its marker family' | wc -w
13
$ git show ee70e6df:corpus/QUALITY.md | sed -n '1056p' | grep -o 'the closure is a per-channel measurement and not a property of the salt' | wc -w
13
```

**Correction 2 — S197's located quote is 25 words, not 24.**

```
$ git show ee70e6df:corpus/QUALITY.md | sed -n '1054p' | grep -o 'A self-assessment counter validates each resolution line against the bytes it claims to repair, and its audit window covers every block rather than the newest' | wc -w
25
```

25 is exactly the contract bound, so the quote stands; only the stated count is wrong.

**Correction 3 — S198's located quote is not in the file it is attributed to.** The lesson gives
"the audit window is the last `## Round-\d+ addition` block". That string occurs nowhere in the
cited receipt, nor in the spot-check, nor in the lane's corpus — only in the round-79 lesson
itself:

```
$ grep -c "audit window is the last" .ufo/waves/round-78/w1/R78ReviewB/atkB2-new-block-window.txt
0
$ grep -c "audit window is the last" corpus/lessons/round-78-verifier-spotcheck.md
0
$ grep -rn "audit window is the last" corpus/ .ufo/waves/round-78/ 2>/dev/null
corpus/lessons/round-79.md:28:  Opened 2026-11-04. Located quote: "the audit window is the last `## Round-\d+ addition` block".
```

The quoted words paraphrase the *predecessor's source*
(`corpus/evidence/round78/selfcheck.py:138`), not the receipt. Admissible quotes from the cited
receipt, verified by `sed -n`:

```
$ sed -n '2p' .ufo/waves/round-78/w1/R78ReviewB/atkB2-new-block-window.txt
# HEAD QUALITY + empty Round-79 block; no supersedes anywhere
$ sed -n '11p' .ufo/waves/round-78/w1/R78ReviewB/atkB2-new-block-window.txt
SELFCHECK=PASS unresolved=0/3
```

The file is 11 lines, so the S198 row's anchor "wave file lines 1-20" overstates the span; it
should read "wave file lines 1-11". The revision pin is correct — the file is tracked at
`3eb4a3cad8febf75698a017cb6c4441f763b3454` and at the tip:

```
$ git ls-tree -r --name-only 3eb4a3cad8febf75698a017cb6c4441f763b3454 | grep atkB2
.ufo/waves/round-78/w1/R78ReviewB/atkB2-new-block-window.txt
$ git ls-tree -r --name-only b58a02db | grep -c atkB2-new-block-window
1
```

One further mismatch on the S198 row: its `source` cell reads "round-78 hollow-mirror **receipt**"
but points at `atkB2-new-block-window.txt`, which is the **window** receipt. The hollow-mirror
receipt is a different file, `R78ReviewB/ALL-three-hollow.txt` (its line 2: "row168
malformed+wrong; 142 dead pointer + gutted 144; row73 stranded — all repairs hollow/false").
Under contract v1 rule 2 the fix is a new row carrying `supersedes S198 —` with a title matching
the file it cites — not an in-place edit.

## Contract check on the drafted row

Run on a **scratch copy** of the registry with S199 inserted after S198; the lane tree was not
modified. Receipt: `receipts/census-validate.txt`.

```
$ /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --file $S/census/corpus/SOURCES.md --root $S/census
file	W04	S051 duplicate url www.w3.org/TR/2017/REC-html52-20171214/syntax.html across scopes
file	W04	S053 duplicate url docs.python.org/3/library/socket.html across scopes
file	W04	S073 duplicate url www.gnu.org/software/coreutils/manual/coreutils.html across scopes
file	W04	S074 duplicate url docs.python.org/3/library/hashlib.html across scopes
file	W04	S075 duplicate url www.gnu.org/software/coreutils/manual/coreutils.html across scopes
file	ok	$S/census/corpus/SOURCES.md
# exit: 0
```

`E01` (malformed row) and `E02` (bad id) do not fire; the five `W04` warnings are the
pre-existing ones the round-78 closure already recorded. The row count goes 198 → 199. The
drafted row's 11 cells split to `NF=13` on `|`, and no cell contains a `|`.

## Gates the L1 must still cross

- The S199 row's `used-by` is `corpus/lessons/round-79.md`, which exists in the working tree but
  is untracked; the census's `E11` used-by leg resolves once it is committed.
- The three `## Gate` corrections and the S198 title/anchor mismatch are **the L1's** to land —
  this seat read-only the lane tree.
- Nothing under `corpus/` was edited by this seat. `git status --porcelain corpus/` shows only
  the L1's own pre-existing `M corpus/QUALITY.md` and `?? corpus/lessons/round-79.md`.

## Tooling

No tool was installed, upgraded or removed. The seat's measurements used only what the host
already had: `git`, `python3` (3.x, `-B` throughout), `grep`, `sed`, `awk`, `wc`, `sha256sum`,
`diff`, `tail`, `cp`, `mkdir`, `rm`, `nohup`, `timeout`, and the lane's own
`scripts/sources-census.sh`. The pacman guard was observed: no package transaction was attempted.

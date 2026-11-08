# R92ReviewerC1 — C1 wording vs code (clauses 1–9 + named limits)

Seat R92ReviewerC1, lane chousa round 92, carrier C5 `16ccf769
3c61b8ffe392fc757352304f239bfcad`, freeze F5 `42e0337822a508
208800f98faa3a63c6af9f8c27`. Scratch `/fast/scratch/hyaku/chousa-r92/
R92ReviewerC1/` (deleted at yield). Attack surface: C1 clauses 1–9 in
`corpus/evidence/round92/claims.md` (freeze `42e0337…`) against
`control-driver-r92.py` + `forgeries-r92.py` at C5. Axes: (1) clause
wording falsified by code behaviour, (2) fixtures that should be
refused but pass, (3) state the sentence reads as accepted but code
refuses, (4) exit/verdict-token mismatches.

## Baseline (not a finding)

At C5 the lane statement runs green:
`control-driver-r92.py verify --root . --repo . --rev 42e0337…
--receipts-rev 16ccf76… --work <scratch>` → `CONTROL_DRIVER_R92
=PASS`, `COMMITTED_OK=6/6 EXACT_OK=6/6 PIN_OK=6/6 FRESH_OK=6/6`
(FRESH_OK=6/6); `forgeries-r92.py --work <scratch>` →
`FORGERY_REFUSED=3/3 POSITIVE=pass`. Both commands
were run in a clone at `16ccf7693…` (exit 0 each). Receipts in this
folder: `receipt-i-del.log` (also carries the baseline PASS lines),
`receipt-r1.log`.

## Findings (by severity)

### [F1] Clause 8 `emit` exit-2 sentence is false — exit 0, writes to default

Claims C1 clause 8: “`emit` without an explicit `--receipts` exits 2
(`emit requires an explicit --receipts`)”. Code
`control-driver-r92.py:370` declares `--receipts` with
`default=DEFAULT_RECEIPTS` (= `controls/receipts/` next to the
driver); no guard checks for an explicit value in `emit`
(`:390–404`). Reproduction: `python3 -B control-driver-r92.py emit
--root <fixture> --work <scratch> --rev <40hex> --expected <fixture>
--pins <fixture>` (no `--receipts`) → exit 0,
`EMITTED=1 MISMATCH=0`, and `fx-one.txt` written into the driver’s
default receipts dir (verified: `DEFAULT_RECEIPTS` dir gained
`fx-one.txt`; cleaned afterwards — no bytes left in the lane tree).
Observed verdict token: `EMITTED=1` with `exit=0` (claimed `2`).
Receipt: `R92ReviewerC1-assets/receipt-emit-no-receipts.log`
(also `receipt-t5a.log`, scratch-driver copy run).

This is a genuine clause-code mismatch and it also weakens the K3
reading: a driver invocation that omits `--receipts` silently
overwrites lane-owned receipts instead of failing loudly. The `--work`
default (`$TMPDIR` else `/fast/scratch/hyaku`) and the `bash -c`
scrubbed-env halves of clause 8 are accurate (`:364, :200–202`).

L1 action: either wire the guard (emit exits 2 when `--receipts`
is absent) or amend clause 8 to “`emit` defaults `--receipts` to the
driver’s `controls/receipts/`; the freeze command always passes it
explicitly” — the current sentence cannot stay. Receipt-trailer
name demanded by the L1: **F1**.

### [F2] Clause 5 “EVERY file a row's command names” does not reach transitive scripts

Clause 5: “EVERY file a row's command names as its script (not just
the first)”. `instrument_rels` (`:153–162`) only tokenises the
command string itself: it splits on whitespace, takes tokens ending
`.py`/`.sh` that are absolute paths under root. A pinned `x.sh`
whose body runs `bash y.sh` contributes one token (`x.sh`); `y.sh`
is never examined, never pinned, never checked.

Fixture (receipt present, pinned `x.sh`, unpinned `y.sh`, both
otherwise well-formed): `x.sh` = `bash y.sh`, `y.sh` prints
`TOK=1 NUM=3`, pin file pins only `x.sh` + `expected.tsv` →
verdict `CONTROL_DRIVER_R92=PASS`, `COMMITTED_OK=1/1 EXACT_OK
=1/1`, exit 0. Second variant where `y.sh` is a silent no-op and
`x.sh` prints the token itself also PASSes. Receipts:
`experiments.log` T2-mutate section (T2-mutate log content is in
`experiments.log`); the primary T2 receipt was deleted with its
scratch tree — see evidence-gap note.

The driver is internally consistent (it does pin every `.sh`/`.py`
token in the command — the S4 second-script class) but the clause as
written overclaims transitive reach. Named limit (5) (“a pinned
script that reads data outside its own bytes is unseen”) is adjacent
but names *data*, not a second *script*; the clause-5 wording
does not stop the reader from thinking `y.sh` is covered.

L1 action: narrow clause 5 to “every `.py`/`.sh` token the row’s
command string names”, and add limit (7): “a pinned script that
executes a second unpinned script is unseen; only tokens in the
command string are pinned.” Receipt-trailer name: **F2**.

### [F3] Pins self-pin “sha256 of the file minus its own row” — comment/blank lines are invisible to the digest

Clause 5: “the pins file's own pin is the sha256 of the file minus
its own row (self-pin) — the minus-self digest”. Code
`pins_file_sha_minus_self` (`:179–191`) skips rows where
`ln.strip()` empty or `ln.startswith("#")` — i.e. comments and blanks
are already excluded before the self-row exclusion. And
`read_pins` (`:100–117`) likewise never sees them.

Fixture: prepend `# reviewer annotation` + blank line to a
well-formed pins file → `CONTROL_DRIVER_R92=PASS`,
`COMMITTED_OK=1/1 EXACT_OK=1/1`, exit 0. A pins file whose minus-
self bytes differ only by comment/blank lines is accepted even
though the *file oracle* — whole-file-minus-row — changes.

Conversely, changing only the self-row digest is correctly refused
(`INSTRUMENT_PIN_MISMATCH:pins.txt`, exit 1, committed counters
stay 1/1) — S5 class holds, and the S5 battery passing at C5
confirms.

So the digest is not “sha256 of the file minus its own row” but
“sha256 of the file with its self row, comments and blanks
removed”. Named limit (4) already concedes the minus-self digest
binds coherence not authority, but the live gap is narrower: a
*whole-file* rewrite that only touches comments/blanks is
invisible, which the clause-5 sentence appears to promise to
catch.

L1 action: reword clause 5 to “sha256 of the pins file’s
non-comment, non-blank rows with its own row removed”, or change
the minus-self code to include comment/blank bytes so the sentence
as written holds. Receipt-trailer name: **F3**.

### [F4] `SETUP PIN_DUPLICATE` exit code is 1, not 2

Clause 6: “a repeated pin path is `SETUP PIN_DUPLICATE` exit 2
before any receipt is scored (`read_pins` last-wins is gone)”.
`read_pins` (`:114–115`) raises `SystemExit(f"SETUP PIN_DUPLICATE
path={path}")` — a bare string argument, so Python exits 1, not 2.
Fixture with a duplicate pin row: stdout `SETUP PIN_DUPLICATE
path=fx-tool.sh`, exit 1, verdict token absent (NO_TOKEN)
(`receipt-ag-duppin.log`). Both C1 forgery runs agree
(`r92 rc=1 (PIN_DUPLICATE)`).

For comparison, the malformed `--rev` path does return 2
(`receipt-emit-no-receipts.log` neighbour, `--rev nothex`: exit 2).
The spec asserting “exit 2” for a SETUP class whose actual exit is
1 is self-inconsistent; K2/K3 phrasing leans on exit codes.

L1 action: change the raise to exit 2 explicitly (`raise
SystemExit(2)`-with-message or message+`sys.exit(2)`) and keep
clause 6 as written, or amend clause 6 to “exits nonzero”.
Receipt-trailer name: **F4**.

## Verified-strong (attempts that did NOT falsify the wording)

- **Two-space indented headers (clause 2 survives).** Receipt with
  every header indented `  # exit=0` etc. and required body token:
  `CONTROL_DRIVER_R92=PASS`, `COMMITTED_OK=1/1`, exit 0
  (`receipt-ad-indented.log`; also `receipt-t1-indented` content).
  `header_multi` (`:135–145`) strips leading whitespace and requires
  the `# ` prefix after stripping — exactly as the sentence says.
  (`#exit=0` without the space after `#` is refused:
  `receipt-t1-nospace`.)
- **Clause 2 negative direction.** `# case=WRONG` alone →
  `HEADER_CASE:WRONG`, exit 1, `COMMITTED_OK=0/1 EXACT_OK=1/1`
  (`receipt-h1.log`). All-values-must-equal-row codes fire as
  named.
- **Clause 4 (whole-token + `>=`).** Detached `TOK 1` and
  `TOK =1` → `TOKEN_MISSING:TOK`, `EXACT_OK=0/1` (`Receipt-t4a`,
  `receipt-h2`, `receipt-ab-detached.log`). Substring never
  satisfies a token; predicate floor applies.
- **Clauses 7 (self-pin prints both revs) and 1 (verify writes
  nothing under receipts).** Read-only receipt (`chmod 444`), mtime
  unchanged pre/post; `--work` outputs land in
  `work/fresh-fx-one.out` only. Full counts stay 1/1. (Earlier
  truncated logs were re-derived with byte-level logging;
  `receipt-ia.log` also shows `FRESH_OK=0/1`.)
- **Read-before-runs (clause 1’s “read first”).** Instrument that
  deletes its own receipt mid-verify: `COMMITTED_OK=1/1 EXACT_OK
  =0/1 PIN_OK=1/1 FRESH_OK=1/1`, exit 1, `CONTROL_DRIVER_R92=FAIL`
  (`receipt-i-del.log`). The committed verdict was taken from a
  read before the fresh run, and the second read (via
  missing file) is what fails exact — so “everything read before any
  fresh run” is true for the committed leg, and the exact leg’s
  post-run read is itself a correctness cost. Also:
  `committed_ok` implies `exact_ok` row-for-row in all in-place
  reads, so `FRESH_OK` full while `EXACT_OK` short cannot arise
  without mutating the receipt during verify (I-fixture above).
  `passed` requires all four per the statement (`:491–492`)
  and code agrees — the r91 exact-gate repair is present, albeit
  named-vacuous per limit (6).
- **Clause 9 battery matches at C5.** Three classes refused with
  the named codes, positive passes (see Baseline).
- **`--work` default + scrubbed env.** `--work` defaults to
  `$TMPDIR` else `/fast/scratch/hyaku` (`:364–365`); fresh legs
  run `bash -c` with PATH+HOME only (`:194–202`). Consistent with
  clause 8’s second half.

## Residual risk / verification gaps

1. The `emit` without `--receipts` run wrote `fx-one.txt` into the
   clone’s retired `controls/receipts/` (default); it was removed
   and `git status` in the clone was clean at pruned state. Cite
   `receipt-emit-no-receipts.log` for the observed exit-0/`EMITTED`
   output; the lane tree was never modified except by that
   instruction to run the command (clause 8’s own command).
2. T2’s primary receipt log was deleted with its scratch tree;
   the surviving evidence is `experiments.log` (the T2 entry
   `COMMITTED_OK=1/1 EXACT_OK=1/1 … PASS`). A blank re-derivation
   is recommended before F2 is cited.
3. The verifier is never run against `--repo` in these fixture
   experiments (self-pin `HEAD` walk needs the clone); that leg
   was exercised only by the lane’s own self-pin-battery run at
   C5, which passes.
4. No additional clauses were attacked beyond the eight assigned
   plus the clause-2/4/6/8 edges. C2/C3 untouched (n/a).

## Tools

No installs. System `git`, `bash`, `python3`, `sha256sum` only.

VERDICT: R92ReviewerC1 C1 fired — F1 (emit exit-2 false) and F4 (PIN_DUPLICATE exit-1-vs-2) contradict clauses 8 and 6 outright, and F2/F3 narrow clauses 5's 'EVERY file' and minus-self wording; two-space headers, whole-token, K3 read-first, pass gate and the 3-class battery held.

# Admission bar (probation draft)

1. Every claim falsifiable or marked opinion.
2. Every claim carries a source: a measured anchor (path:line, command, evidence id).
3. Observation, inference and unknown stay separate.
4. Errata are append-only blocks.
5. A rejection is kept, not silently dropped.

## Round-24 additions (appended 2026-10-19; criteria 1–5 unchanged)

Each criterion cites the mined mistake (`lessons/round-24.md` `## Mistakes`) or
the admitted entry that motivates it. Tier definitions live in
`corpus/SOURCES.md` (contract v1); this file holds admission only. Criteria
6–8 bind `knowledge/` entries; 9–12 bind every lane record (corpus, `SKILL.md`,
`LOG.md`, `SCORECARD.md`), because a record is admitted when it is committed.

6. **Metadata header.** A `knowledge/` entry admitted from round 24 on opens
   with `source:` (≥1 `S###` row of `corpus/SOURCES.md` whose status is
   `mined` and whose `used-by` names this entry, plus its URL or repo path and
   an exact anchor), `verified-at:` (ISO date + what was checked) and
   `recheck:` (an ISO date or a cadence — `90d`, `180d`, `365d`, `on-release` —
   optionally followed by the re-run command). A `recheck:` that is only a
   command leaves "overdue" uncomputable. — M-13.
7. **Scoped tier.** An admitted claim rests on ≥1 tier-A or tier-B
   `SOURCES.md` row whose `scope` covers that claim; a tier-C or `community`
   row is never sole support, and a source used outside its row's scope is an
   inference and labelled one. — `knowledge/contextual-source-admission-r24.md`.
8. **Support states stay distinct.** "Source exists / opens", "source is on
   topic", "source states the claim" and "the claim is true" are four
   observations; an entry never reports a claim verified from the first two,
   and never reports truth from the third alone. —
   `knowledge/claim-support-states-r24.md`.
9. **One home per number and finding.** A restated count, total or open
   finding names its owning file + revision and carries the command that
   re-derives it; closing a finding closes it in every restating file in the
   same landing, and the owning ledger gets the disposition in that landing;
   an index row lands under its own round's heading. — M-3, M-4, M-6, M-12.
10. **No unfilled template; snapshots are dated.** No placeholder ships in a
    record — `${…}`, `<…>` template slots, `TODO`, `TBD`, `[record …]` or an
    uppercase stand-in for a hash such as `LANE_HASH` (check: every hit of
    `grep -nE '\$\{[A-Z_]+\}|\bTODO\b|\bTBD\b|LANE_HASH' <file>` sits inside
    a backtick span that names the token as data, as in this criterion and
    `lessons/round-24.md` M-5). A dated reflection names the commit window it measured
    (`git log --since --until` bounds) and is re-measured, or not committed,
    when a commit has landed inside that window since. — M-5, M-7.
11. **Plan, claim and table agree.** A pre-registered wave, seat count or
    provider that is not what ran is closed by a disposition line naming what
    ran and the substitute evidence (`honest stop` is reserved for an
    unjudged exploratory claim, `AXES.md` §Working the axes); a capability a
    `LOG.md` entry claims has its `SCORECARD.md` capabilities row in the same
    landing, or the LOG line says it has none and why. — M-1, M-14.
12. **A kept score is re-derived or frozen.** A numeric axis score cited at
    a landing is re-measured there by the counting command its row names, or
    is marked `frozen at rN` with the reason and the round that will
    re-measure it. — M-11.

## Round-25 additions (appended 2026-10-21; criteria 1–12 unchanged)

13. **Runnable recheck.** A new `recheck:` command states its cwd and names
    the research root by role (`--root "$SHOKUNIN_ROOT"`, the fleet root),
    or explicitly states the checkout layout a relative root assumes. A bare
    `--root ..` is not placement-independent. — `lessons/round-25.md` R25-M2;
    `lessons/round-24-verifier-spotcheck.md:17`. Shown able to fail:
    `! grep -nE '^recheck:.*--root +"?[^/$"]' corpus/knowledge/citation-chain-fidelity-r24.md`
    exits 1 on the base line; the clone re-run with `--root ..` is DRIFT,
    with the explicit fleet root CLEAN (`.ufo/waves/round-25/build/ReviewRecheckRoot.md`).
    This syntax check sees only the `--root` argument, not command runnability;
    a reviewer checks the command in a clone outside the assumed layout.
14. **Spot-check intake.** A `lessons/round-<N>.md` landed from round 25 on
    carries `## Spot-check intake`, one row per debt or disagreement in the
    previous verifier spot-check, each fixed (pointer), carried (criterion or
    round), or refused (reason). — `lessons/round-25.md` R25-M3;
    `lessons/round-24-verifier-spotcheck.md:17`. Shown able to fail:
    `grep -qx '## Spot-check intake' corpus/lessons/round-24.md` exits 1 at
    the base; the round-25 lesson exits 0 (the per-debt rows need a reviewer).

15. **Measured bytes must be in the cited commit.** Before a report or a
    falsify wave pins a revision, the executable's digest from
    `git show "$REV":tools/research-gate.sh | sha256sum` must equal the
    measured working-tree digest (and every changed production path is in the
    helper's path list). A successful helper landing proves only its named
    paths landed. — `lessons/round-25.md` R25-M13: the first integration
    checkpoint omitted the gate, so prose said 154 cases while its gate had
    136. This check failed on `0fc037e` and matched at `d8c8cff`.

16. **An owning total must reconcile.** A disposition tuple names the row
    population, counts those rows and applies explicit addendum deltas; its
    components must sum to the row count. Queue-item counts stay separate
    from row dispositions. — lesson R25-M7 (captured-by none before this rule):
    E4's sum72 over71 fails, row-true38/22/8/0/3 sum71 passes. Re-derive with
    `python3 corpus/evidence/round25-ledger-recount.py`; an owner pointer
    alone is not validation of the owner's arithmetic.
17. **A new runnable screen needs an independent failing control.** Derive
    at least one negative fixture from the declared contract independently
    of the implementation; disable its targeted check in an isolated clone
    and show the detector fails for that reason, not a parse error. A printed
    tally without a nonzero mismatch exit is a probe, not a passing gate.
    — lesson R25-M11 (captured-by none); `FxMutateMissing.md` kills the missing
    source/recheck arms, `FxMutateRefusal.md` kills canonical/NUL guards;
    `round25-meta-differential.sh` now exits1 on any table/oracle disagreement.

## Round-26 additions (appended 2026-10-21; criteria 1–17 unchanged)

18. **A bound names its unit.** A byte-read cap is not a memory or time
    budget: downstream representations can amplify a bounded input. Before
    calling a reader resource-bounded, exercise a newline-dense input and
    record peak RSS and elapsed time against a small control. Scope the
    conclusion to the measured shapes; keep time/memory limits distinct.
    — `lessons/round-26.md` R26-M1 (captured-by none): the 8 MiB reader
    allocated over2 GiB before parsing. Shown able to fail:
    `bash corpus/evidence/round26-measure.sh <base-tree> c1` yields
    `C1_AMPLIFIED=4/4` at `ba333325`; same probe and frozen shapes evaluate
    the replacement. The probe exit0 is completion only; compare its values.

## Round27 additions (criteria1–18 unchanged)

19. **A diagnostic phrase is not a verdict record.** Test output with the
    consumer's record grammar; help prose may quote the same phrase. Keep
    expected exit, required diagnostic and forbidden-verdict checks separate.
    Negative controls must reject wrong exits, absent diagnostics and real
    verdict records, not merely accept the repaired happy path. —
    `lessons/round-27.md` R27-M1; S040; r26 shared FAIL3/187 proves the old
    predicate failed its own intended usage cases.
20. **Preserve the input representation at a verification boundary.** When
    a provenance checker crosses date-text/arithmetic, table-candidate/table,
    token/match or filesystem-path/citation-pointer boundaries, controls
    exercise the two representations separately, including finding
    multiplicity. A code-set comparison cannot detect invented duplicate
    occurrences. — `lessons/round-27.md` R27-M2–M6; S041/S042; the committed
    r26 counterexamples show each distinction able to fail. This criterion
    does not claim complete Markdown semantics or whole-parser resource bounds.

21. **A parser repair preserves positive syntax and bounded work.** Width
    assertions include escaped-pipe and mixed-outer-pipe tables, a consulted
    mined row and its queued twin. Token scans measure both id-dense and
    non-id-token-dense inputs; filtering before a shell loop must preserve
    occurrence counts. A long-line normalization names its measured size and
    timeout, rather than inferring scale safety from a small fixture. —
    `lessons/round-27.md` R27-M10/M11/M13; S043;
    `post-falsify/fc-before.stdout` shows escaped-width and 4 MiB controls
    failing at dd72641e, while the corresponding after receipt passes.
    Receipt paths are under `.ufo/waves/round-27/`.
22. **Matcher failure is not zero matches.** A verification predicate
    distinguishes the matcher's documented no-match exit from execution
    failure, and injects a matcher fault as a negative control. —
    `lessons/round-27.md` R27-M12; S043; control
    `matcher-fault-fails-closed` accepts incorrectly at dd72641e and rejects
    at cb895a2; selftest case215 preserves that distinction.

## Round-29 additions (appended 2026-10-23; criteria 1-22 unchanged)

23. **Lane prose keeps digits apart from words and carries no custody
    vocabulary.** New prose writes `all 69` and `on 2026-10-23`, never the glued
    forms, and uses only the canonical round vocabulary. Check:
    `python3 corpus/evidence/round29/prose-check.py <files>` exits 0 on the
    round's new prose. It fails (exit 1) on `lessons/round-28.md` with 9 glued
    tokens and 5 custody hits, which shows the check can fail. —
    `lessons/round-28-verifier-spotcheck.md` D1 and D2; `lessons/round-29.md`.
24. **Controls are scored before data, and a control that meets the counter
    re-designs the claim.** Before any data seat runs, the claim's frozen
    counter scores the cheapest do-nothing, all-false, junk, no-reader, and
    label- or id-keyed shortcut controls, and the receipts are committed. Any
    control that meets the counter, including one that replays committed
    receipts for a seed the caller picked, voids the design before data. A
    counter that samples at run time draws its own seed. Fails when a control
    receipt meets the counter and data still runs on that design. —
    `lessons/round-29.md`; `.ufo/waves/round-29/controls/` (v1 met 82/82 by
    label replay; v2 met 130/130 by seed replay; v3 best control 126/130).
25. **A cited web quote is re-opened, and a miss is recorded.** Before a round
    cites a located quote from a registered web source, run
    `python3 tools/quote-reopen.py verify --items <tsv>` from the lane root.
    Record every `ABSENT`, `UNREACHABLE` or `TOO_LONG` verdict with the quote.
    An `ABSENT` on a page that the extractor cannot read is a tool limit and
    must be named as one. Example: a page that omits `</head>` yields no text
    (S047). It is not evidence that the quote is false. Fails when a verdict
    other than `VERBATIM` is dropped or relabelled. — `lessons/round-29.md`;
    `knowledge/quote-reopen-r29.md`.

## Round-30 additions (appended 2026-10-23; criteria 1-25 unchanged)

26. **An adjective on a claim surface has its own evidence.** A word such as
    "live" in a capability row, claim or knowledge entry is backed by its own
    predicate or a cited receipt, or it is not written. Fails when
    `grep -nwi live <file>` finds the word in round prose that cites neither.
    Shown able to fail: the command finds 5 lines in `lessons/round-29.md`
    (routed D1) and none in `knowledge/quote-reopen-r30.md` or
    `evidence/round30/claims.md`. — `lessons/round-30.md`;
    `lessons/round-29-verifier-spotcheck.md:143-147`.
27. **A stated re-run count equals the committed receipts.** A report or
    scorecard that says N further runs names N committed receipts with distinct
    seeds. Check: `python3 corpus/evidence/round30/rerun-check.py --stated N
    <receipts>`. Shown able to fail: on the round-29 re-run evidence it prints
    `RERUN_RECEIPTS=5/6` and exits 1 against the stated 6, and exits 0 against
    5 (routed D2). — `lessons/round-30.md`; `.ufo/waves/round-30/build/ExecRerunCount.md`.
28. **A surviving mutant becomes a fixture class before data.** When a mutant
    of a landed tool survives a counter, the next design adds the class that
    breaks it before any data seat runs. Shown able to fail: the three round-29
    survivors score 76, 66 and 72 on the round-30 C1 counter, below the round-29
    tool's 78/106 (`.ufo/waves/round-30/build/CriticD3Classes.md`, routed D3). —
    `lessons/round-30.md`; `evidence/round30/claims.md`.
29. **Nothing a candidate can see reveals an item's class or label.** Item URLs,
    ids, host names, order, response heads and quote shapes are drawn so that
    they carry no class or label, and the control wave tries a shortcut keyed on
    each. Shown able to fail: on round-30 C2 design v2 a DNS- and header-keyed
    control met `QUOTE_REOPEN_FETCH_BOUND_MATCH=20/20`
    (`.ufo/waves/round-30/controls/CtlShapeKeyed/receipt-dns-header-c2-run1.json`);
    the same control scores 13/27 and 16/27 under v3 and 16/27 under v4
    (`.ufo/waves/round-30/controls/L1Rescore/`). — `lessons/round-30.md`;
    `evidence/round30/claims.md`.

30. **A Gate quote is verbatim before admission.** Every new located quote in a
    Gate row is put, exactly as printed, in a TSV item naming its `S###` source
    and re-opened from the lane root with
    `python3 tools/quote-reopen.py verify --items <tsv>`. Admit the row only
    when its result is `VERBATIM`; preserve every other verdict with the quote
    and its disposition. A tool/input error is not a match. Shown able to fail:
    the S052 input row is
    `S052q1<TAB>S052<TAB>In timeout mode, operations fail if they cannot be completed within the timeout specified for the socket.`;
    the falsify receipt records the exact command
    `timeout 120 python3 tools/quote-reopen.py verify --items /fast/scratch/hyaku/chousa-r30/w2/AttackRowS052/s052.tsv`
    from the lane root returning `QUOTE_REOPEN S052q1 ABSENT`,
    `QUOTE_REOPEN_SUMMARY verbatim=0 absent=1 too_long=0 no_source=0 unreachable=0`,
    exit 1 (`.ufo/waves/round-30/falsify/AttackRowS052.md:7-13`). The source
    capture contains `socket (they raise a timeout exception)` rather than the
    Gate's truncated `socket.` (`https://docs.python.org/3/library/socket.html#socket-timeouts`,
    opened 2026-10-23 in the round-30 evidence). —
    `lessons/round-30-verifier-spotcheck.md:190-191`;
    `lessons/round-30.md:47,77-85`;
    `.ufo/waves/round-30/falsify/AttackRowS052.md`.

31. **Every sub-variant a counter draws has a fixed count per run.** A class
    whose sub-kinds (invalid-value kinds, newline variants, CRLF files, named
    occurrences, wrong-range shapes) are drawn at random lets a tool that
    mishandles one sub-kind pass every seed that drew none of it. Fix the count
    of each sub-kind per class before data. Shown able to fail: on round-31 C2
    design v1 a whitespace-trimming validator printed
    `REVISION_BINDING_MATCH=120/120` on seed 9002
    (`.ufo/waves/round-31/controls/ChousaR31.CtlShortcutC2/`); under v2, with
    two spaced values fixed per run, the same control prints 118/120 on every
    seed (`controls/ChousaR31.CtlShortcutC2/v2/`). — `lessons/round-31.md`;
    `evidence/round31/claims.md`.
32. **A counter checks the finding the contract requires, not only the
    verdict.** When a contract names a finding for a verdict, the counter
    matches a claim only if the finding names exactly the claims with that
    verdict. Shown able to fail: under round-31 C1 v2 the no-reader control
    scores 88/120 with findings and 30/120 with its findings removed
    (`.ufo/waves/round-31/controls/CtlNoReaderC1/v2/`). — `lessons/round-31.md`;
    `evidence/round31/claims.md`.

## Round-32 additions (appended 2026-10-23; criteria 1-32 unchanged)

33. **A detector-kill sentence is receipt-backed.** A lesson sentence saying a named detector
    "killed" or "caught" a named mutant cites that detector's committed receipt for that mutant,
    and for a count-based counter the receipt shows `matched < total`; `matched == total` means
    the counter did not kill it. Shown able to fail: `python3 corpus/evidence/round32/q33-check.py` prints `FAIL` and exits 1
    on the round-31 lesson as committed at `4111607c`, and `PASS` (exit 0) on the lesson with the
    round-32 correction appended. — `lessons/round-32.md`; routed R1.
34. **A counter for an ordering or locking claim forces the window it checks.** If a wrong
    implementation's race window is shorter than the harness can observe, the counter widens it
    (delay injection, a held cooperating lock) before counting. Shown able to fail: a gate that
    locks only around the probe scored 24/24 under round-32 C1 v1 and 0/24 under v2, whose only
    change is a 300 ms delay on every write to the manifest
    (`.ufo/waves/round-32/w1/CtlC1PartialLockB/b-s3247102{1,2}.json` and `v2/mutated-b-probe-only-s3247202{1,2}.json`, gate `034f786b…`).
    — `lessons/round-32.md`; `evidence/round32/claims.md` Design v2.
35. **A control gate is scored in the gate's own layout.** The lane gate derives its lane root
    from its own path (`research-gate.sh` `LANE_ROOT`), so a control or oracle gate is placed at
    `<dir>/tools/research-gate.sh` with fixtures outside `<dir>`, and a counter that writes
    out-of-corpus fixtures refuses to run when they would fall inside that root. Shown able to
    fail: `c2-count-v2.py` with `C2_TMP` inside the gate's lane root exits 2 ("fixture dir … lies
    inside the gate's lane root"); under v1 the same layout made strict controls miss E7.
    — `lessons/round-32.md`.

## Round-33 additions (appended 2026-10-23; criteria 1-35 unchanged)

36. **Fixture metadata cannot stand in for reading.** A coverage counter's fixture assigns
    classes independently of creation order, mtime, inode and name order (shuffle writes across
    classes; draw mtimes independently). Before the counter is frozen, a metadata-order control
    and a no-reader control are scored with it and committed; each must score below total.
    Check: the committed control receipts' `matched` is below `total`. Shown able to fail: the
    round-32 counter v2 gives the metadata-order control `matched=132/132`
    (`.ufo/waves/round-32/w2/CriticAxis32/control-metadata-s3232002{1,2}.json`); the round-33 v3
    counter `corpus/evidence/round32/c2-count-v3.py` gives the same control 96/132 and 95/132 and
    the no-reader control 78/132 (`.ufo/waves/round-33/w1/ExecD1CounterV3/receipts/`). Routed
    D1, `lessons/round-32-verifier-spotcheck.md:154-158`.

37. **Every numeric tally carries its counting command.** A count in a report, lesson or
    SCORECARD row names the command that reproduces it over committed bytes. Check: run the named
    command and compare. Shown able to fail: `SCORECARD.md` round-32 row says `10f2fe12` ×18; the
    spot-check said 20; `python3 corpus/evidence/round33/d2-census.py --lane .` prints
    `C1 receipts on gate 10f2fe12: 21` (the extra receipts were written after the tally was
    taken). Routed D2, `lessons/round-32-verifier-spotcheck.md:159-162`.

38. **A battery output starts with its revision header.** Every no-harm battery output names
    `lane_revision=` and `gate_sha256=` before its first result row. Check:
    `awk '/^=== RUN/{exit} /gate_sha256=/{g=1} /lane_revision=/{r=1} END{print (g&&r)?"HEADER_OK":"HEADER_MISSING"}' <battery.out>`.
    Shown able to fail: `.ufo/waves/round-32/measure/final/battery.out` → `HEADER_MISSING`;
    `.ufo/waves/round-33/measure/battery-candidate/battery.out` → `HEADER_OK`. Routed D3,
    `lessons/round-32-verifier-spotcheck.md:163-165`.

39. **Seats signal only processes they recorded.** No seat selects processes by name or pattern
    (`pkill`, `killall`, `kill $(pgrep …)`, `pgrep … | xargs kill`) on the shared host; it kills
    the PID or process group it recorded when it started the process. Check:
    `bash corpus/evidence/round33/no-name-signals.sh <wave dir>` (exit 1 lists hits; prose that
    quotes the rule is listed as `[doc; …]` and excluded only by an explicit `--exclude`). Shown able
    to fail: on `.ufo/waves/round-32` it exits 1 with `w2/RerunC1b.md:31` (`pkill -x sleep`); on
    `tools/` it exits 0. Routed D5, `lessons/round-32-verifier-spotcheck.md:168-169`.

40. **Adversarial fixture content is not a fixed list.** A counter whose classes test "content is
    never structure" draws that content per seed (random brace/bracket/quote/backslash mixes),
    and a control that masks the counter's literal fixture strings is scored before freezing; it
    must score below total. Shown able to fail: `.ufo/waves/round-33/w2/L1ShortcutMask/mask-gate.sh`
    masks the six `CONFUSERS` of `corpus/evidence/round33/c1-count-v2.py` and scores 156/156
    (`mask-s3391.json`, `mask-s3392.json`). — `lessons/round-33.md`.

41. **Repairs are not edited into a gate that seats are scoring.** Post-falsify gate changes are
    built and tested in a scratch copy and installed after the wave settles; every receipt names
    the gate SHA-256 it measured. Check: no committed counter receipt names a gate SHA-256 that
    matches no committed revision. Shown able to fail: `.ufo/waves/round-33/w2/ReviewC1Diff/c1-v2-s4117.json`
    (gate `b808e9b5…`, 0/156, a half-written edit). — `lessons/round-33.md`.

42. **Measurements are bound to committed gate bytes.** A receipt supports a claim about a committed
    gate only when its `gate_sha256` equals the SHA-256 of a committed `tools/research-gate.sh` blob
    (or a committed control script); otherwise it is re-run on the intended bytes or labelled
    non-revision evidence. Check: `python3 .ufo/waves/round-34/w1/ExecE4Census/receipt-binding.py
    <wave dir>` lists every `UNBOUND` receipt and exits 1 when one is labelled landed/final. Shown
    able to fail: on `.ufo/waves/round-33` it exits 1 and lists `measure/final/fz-9021{2,3,4}.json`
    (`b2c07eda…`) and five wave-2 `c1-landed` receipts. Routed E1/E4,
    `lessons/round-33-verifier-spotcheck.md:157-171`. — `lessons/round-34.md`.

43. **A misrooted copy has committed byte-identity proof before deletion.** Before deleting a
    fleet-root copy moved into the lane, commit a file naming both paths with each copy's SHA-256;
    that commit precedes the deletion. Check: the deletion's round has a committed pair file; none
    fails. Shown able to fail: round 33's SentinelParser33 move has only a prose `cmp` statement
    (`lessons/round-33.md`, misroot paragraph). Routed E5. — `lessons/round-34.md`.

44. **A held control is never re-authored; its claim is declared unverified before data.** When a
    required control seat ends on a provider safety hold, nobody (the L1 included) rebuilds that
    control or a substantially equivalent one; the claim that needed it is recorded as unverified in
    the frozen design before any candidate receipt, and any artifact already re-authored is listed
    as excluded. Check: every held seat named in the round's registry has no re-authored control
    cited as evidence, and the claims file carries the exclusion record before the first candidate
    receipt. Shown able to fail: round-34 commit `ef16afb1` carried L1-built controls for the held
    CtlC1Shortcut/Windows/Halves shapes with no exclusion record (added in `f20aeaa7`, before the
    candidate receipts of `934d7cb7`). — `lessons/round-34.md`.

45. **A claim that names a mechanism carries a mechanism witness, not only output equality.** Two
    engines that implement the same contract print the same verdicts, so an output counter can never
    kill a fingerprint-and-shortcut engine (killing a correct implementation is a false negative). A
    claim whose text names a mechanism (a matcher, a routing, a code path) is met only when its
    receipt also witnesses, out of band, that the mechanism ran — and the witness separates at least
    one output-equivalent control while the landed gate passes both. Check:
    `python3 corpus/evidence/round35/c2-count.py --seed N` prints `WITNESS_SEPARATED=2/2
    OUTPUT_EQUIV=2/2 LANDED_WITNESS=pass`. Shown able to fail: the two keyed engines K1/K2 score
    9/9 output and witness-fail, while the round-34 output counter gave the same class 37/37
    (`MutC2Keyed.md`, ctl4/ctl6); a witness stub that always says pass separates 0/2, one that
    always says fail fails the landed gate. — `lessons/round-35.md`.

46. **A tool the gate executes is resolved to one absolute, verified binary.** A command resolved
    through `PATH` (or an imported shell function via `BASH_ENV`, S068) makes the gate's behaviour a
    function of the caller's environment; the substitution is invisible in output. The gate resolves
    one absolute candidate, verifies its self-reported provenance, refuses an unverifiable pin before
    reading any record (exit 2, `GREP_PROVENANCE`), and can name the pin for a receipt
    (`CHOUSA_GREP_PIN_ECHO=1` → `GATE_GREP: path=… source=… version=…`). Check:
    `python3 corpus/evidence/round35/c1-count.py --seed N` prints `GREP_PIN_MATCH=9/9`. Shown able to
    fail: the round-34 gate scores 0/9 (PATH shim and `BASH_ENV` function tripwires both fire;
    no-grep `PATH` exits 2), and a hardcoded-wrapper control without provenance/override/echo scores
    3/9. — `lessons/round-35.md`.

47. **A derived value never shares one `local` statement with the name it derives from.**
    `local a=$1 b=${#a}` expands every right-hand side before assigning any name, so `b` reads the
    caller's dynamic scope, not `$2`; `set -u` does not catch it and the public path may never
    expose it. Check: `.ufo/waves/round-35/repairs/slen-probe.sh <gate>` prints `offsets=1` for a
    repaired matcher and `offsets=0` for the coupled form. Shown able to fail: the round-34 gate
    (`a6307edf…`) prints `offsets=0` while its selftest passes 256 cases; the landed gate
    (`1f2fb4f5…`) prints `offsets=1 first=5`. Sweep: `grep -nE 'local [^#]*(\$\{[#%]|\$\(\()'` over
    the script, reading each hit. — `lessons/round-35.md`.

48. **A refusal claim asserts ordering, not only the exit code and the marker.** "Refuses before
    it reads a record" is an ordering property: a gate that opens the record and then refuses
    prints the same exit 2 and the same marker. A refusal receipt carries an open-ordering witness
    (strace/ptrace `openat` count, or a canary file the refusal must not touch) alongside the exit
    code, and the ordering is checked on the same run as the refusal. Check: every refusal scenario
    states the observed open count (0 vs the positive control's). Shown able to fail: a mutant that
    opens the record then refuses (sha256 `147ded03…`) scores `GREP_PIN_MATCH=9/9` under the round-35
    C1 counter while the strace evidence separates it (0 vs 2 opens). — `lessons/round-35.md`,
    `.ufo/waves/round-35/w2/MutPinRefusals.md`.

49. **A mechanism witness attributes per record; a global stamp sum is not coverage.** A count over
    a whole run cannot see one record answered elsewhere: the round-35 witness threshold
    (`chunk stamps >= long records`) admitted a one-record shortcut (8 stamps for 8 records, because
    the landed gate itself emits 9), a length-keyed engine whose key is constant inside a fixture,
    and a body-replaced matcher that keeps the witnessed entry line. A witness that asserts coverage
    binds stamps to record ids (or to a per-record side channel) and seeds diversity into every key
    the fixture exposes. Check: each fixture record's own witness line, not a run total. Shown able
    to fail: `.ufo/waves/round-35/w2/MutC2KeyedBattery.md` (controls C and D),
    `MutWitnessBypass2.md` (body-replaced chunk matcher, gate `3e5648b8…`, `WITNESS=pass` 9/9). —
    `lessons/round-35.md`.

50. **A tool's stated count is a claim and must trace to a committed receipt.** A docstring
    sentence like "separates only 3/5" is a measurement with no counting command, and nobody
    re-derives it because the tool's printed label excludes the before-count. Every numeric claim
    in a tool's own prose names the receipt field that yields it, or it is not evidence. Check: for
    each number in the docstring, name the receipt path + field; a number with no field is
    unverified. Shown able to fail: round-36 `c2-count.py` said the round-35 battery "separates
    only 3/5 (V3 and V5 pass it)" while `.ufo/waves/round-36/measure/c2-before-legacy-s36001.json`
    reports `matched: 2` with `V2-env-keyed`, `V3-witness-forge` and `V5-body-replaced` all
    `witness: pass`. —
    `lessons/round-36.md`.

51. **A witness channel the candidate can write to is not a witness channel.** A channel the engine
    under test can emit on (the gate's own stderr / PS4) can be forged without doing the work: the
    round-35 trace battery scored `WITNESS=pass` on 360 forged stamps and zero real chunk
    executions. A witness design names (a) who writes the channel, (b) where the per-run marker
    comes from, and (c) what a candidate that READS the harness could still forge. Check: show the
    writer and the marker source in code, and separate a forging engine. Shown able to fail:
    `V3-witness-forge` passes the round-35 battery and fails the round-36 witness
    (`corpus/evidence/round36/c2-count.py`, receipts under `.ufo/waves/round-36/measure/`). —
    `lessons/round-36.md`.

52. **A scenario's assertion must match the behaviour its name claims.** A scenario named for a
    mechanism ("the override beats an imported shim") that asserts only an echo string and a
    reference output passes without the mechanism, and its PASS inflates the count. Each scenario
    quotes the assertion that would fail if the named behaviour were absent, and a scenario whose
    assertion is a weaker proxy is renamed or re-asserted. Check: read each scenario's assertion
    assertion next to its name; a mismatch is a survivor. Shown able to fail: round-36 C1 S9 truncates the
    recorder log and never reads it again, S8 reads no matcher argv, and S7 accepts one argv
    (`.ufo/waves/round-36/w1/ScoutC1Counter.md` §Vacuity candidates); the 14/14 still holds
    because S10 requires every record attributed. — `lessons/round-36.md`.

53. **A no-harm battery's commands are re-used verbatim from their pinned record.** A battery
    re-run with a different corpus root, fixture path or flag set than the recorded pin measures
    a different invocation: refusal-class output under a drifted invocation is a signal to check
    the invocation, never itself harm. The harm verdict belongs to the recorded commands' result.
    Check: before running a pinned battery, copy the command text from its pinned record (not
    from memory or a re-derived brief) and diff the invocation. Shown able to fail: the round-37
    wave seat ran the r36 battery with `--root .` instead of `--root ..` and read the resulting
    `*_SOURCE_OUT_OF_CORPUS` refusals as harm on all six rows
    (`.ufo/waves/round-37/w1/ExecNoHarmPin.md`); the L1's verbatim re-run showed every
    observable at its pinned value (claims 17/17, chain 17/22, broken 1/2, archives 3/3). —
    `lessons/round-37.md`.

54. **A claim text's general clause must not outrun its counter's cells, and a named limit
    must enumerate every demonstrated vector class.** If the counter measures named vectors
    only, the claim text may promise no more than those vectors; if a falsifier demonstrates a
    new class (unprivileged `LD_PRELOAD` interposition into a child that inherits the caller's
    loader environment; exported functions reaching a scrubbed child through `BASH_FUNC_*`),
    a limit naming root-only mechanisms does not cover it. Check: read the claim's general
    sentence against each counter cell, and read each limit against every child process the
    gate spawns. Shown able to fail: round-37 C1's "no PATH shim" wording survived while
    `LD_PRELOAD` moved pin verdicts 4/7 and 3/7 on the landed gate
    (`.ufo/waves/round-37/residual/CritC1Kill.md`), and C2's "independent of the caller's
    `BASH_ENV`" survived while a startup-exported `date` function reached the capture child
    through `BASH_FUNC_date%%` (`.ufo/waves/round-37/residual/RevC2FreshSeed.md`). —
    `lessons/round-37.md`.
55. **A verifier's pass is a claim about provenance and truth, not about an artifact's
    agreement with itself.** A verifier that re-hashes the receipt's own fields certifies only
    self-consistency: re-sealing restores every digest, a counter hash can be swapped for a
    public digest, and an unparsed expectation table lets a doctored observation keep `ok=true`.
    A receipt-verifying gate binds (a) the counter family and the frozen predicate it claims,
    (b) the frozen expectation bytes — parsed, not only hashed — (c) the exact scenario census
    with each row's `expect` tied to the frozen table, and (d) re-derives every `ok` from (b)
    and (c). Check: mutate each of the four independently, re-seal each mutant, and require a
    named refusal. Shown able to fail: round-38's frozen `verify-receipts.py` accepted a
    re-bound legacy r37 receipt, a c1 receipt rerouted as c2 (counter hash swapped to the
    public digest), a `pin_rc` 0→99 doctoring and a zero-scenario receipt
    (`.ufo/waves/round-38/w1/CritC2Kill.md` findings 1–3); after Erratum 2 all four refuse
    by their named checks while `c2-count` stays 7/7 (`.ufo/waves/round-38/w2/W2CritLaundering.md`). —
    `lessons/round-38.md`.
56. **An attack or discrimination fixture must be shown able to fire before its cell counts.**
    A fixture that cannot fire scores its cell vacuously and the cell is not a measurement:
    identical bytes (a "doctored" copy replaced with its implicit-concatenation twin), a
    re-add the scrub un-sets again (a prefix assignment in front of a forwarded `-u` list),
    or a syntax crash where a named refusal was expected (a deleted `return` leaving an
    empty if-body). Check: run the fixture against the control bytes and require the named
    observable to move (red-before); if the control cannot be made to fail, the fixture is
    inert. Shown able to fail: all three shapes fired in round-39 drafting — the swap cell
    verified `ok` on identical bytes, the weakening cell produced empty stdout from a
    stderr-only crash, and the PATH-`env` shim was measured benign (`GATE_GREP` count 0)
    — and each rebuilt fixture fires on its control (`4/8` mutant, `7/8` base,
    `verifier-sha256-mismatch` / `subject-counter-sha256-mismatch` refusals). —
    `lessons/round-39.md`.

57. **A live-access claim carries byte evidence of the access.** "Opened", "accessed",
    "verified-at" or a re-open cited in a Gate row is attestation unless a receipt exists:
    committed response body/headers/status/digest, or a named committed capture re-read with
    its sha256. A prose access date without either is unverifiable provenance — and a seat's
    dispatch item is not operator approval for egress (the approval table is the only
    authority). Check: for each `opened`-dated claim, name the committed bytes or committed
    capture the read came from; a source check may re-read a committed capture and cite its
    hash instead of fetching. Shown able to fail: round-40's "accessed 2026-10-24" for S059
    and S074 left zero fetch receipts while the pinned body stayed dated 2026-10-23
    (`.ufo/waves/round-40/w1/SentinelFetchScope.md` F1/F2; `ScoutHashSource.md:7,32`) —
    a live GET executed under item-text "authorization" while L0 `8d77e6c1` stayed open. —
    `lessons/round-41.md`.

58. **A counter's measured revision is pinned inside its receipt.** A counter that grades
    whatever tree happens to be checked out scores worktree state, not the cited commit: a
    sibling round's in-flight edit moves the measurement without touching history. Each
    counter accepts the measured surface explicitly (`--gate PATH`, a detached tree, or a
    revision-pinned copy) and the receipt records which bytes were measured. Check: run the
    counter on the cited commit's tree and on the mutable worktree; identical results are
    required only when the worktree is clean. Shown able to fail: round-40's receipt verifier
    scored 6/6 on committed HEAD but 2/6 on a worktree carrying round-41's in-flight edits —
    the same counter, two truths, revision unpinned (`.ufo/waves/round-40/w1/
    ReviewActivePopulation.md`, `ReviewReplacementBindings.md`). —
    `lessons/round-41.md`.

## Round-42 additions (appended 2026-10-24; criteria 1–58 unchanged)

59. **A class that licenses a verdict must name the evidence it rests on.** A register,
    a registry or a checker that grades a row "fabricated" is only as strong as the
    capture behind it: a bot wall saved as a successful fetch, a binary document
    decoded as bytes, and a stale summary table are three ways to make a verdict sound
    that no source supports. Before a class is used to refuse or admit a row, name the
    committed bytes the class rests on AND the form of those bytes (a rendered text, an
    extracted PDF text, a binary decoding, an interstitial). A row whose evidence is
    not in that form is `unverifiable`, never a fabrication. Check: for each refusal,
    name the capture file and its form; if no capture of the right form exists, the row
    is unverifiable. Shown able to fail: round 42's S077 carried the campaign's
    `payload-absent` class ("every relevant source fetched cleanly") while the local
    capture of that DOI was a 265-character `Client Challenge` page; S095, S096, S120
    and S125 were binary office documents whose bytes were never rendered to text; the
    register's `## By lane` summary said 20 rows where the derived slice holds 24.
    — `lessons/round-42.md`.

60. **Every frozen counter names the cheapest gate that scores full marks without doing
    the work, and the control wave is checked against that line.** A counter is only as
    strong as the worst gate that satisfies it; a do-nothing control, a junk-row replay
    or a label-keyed program that meets the counter proves nothing. Before the counter
    is frozen, write one line naming the cheapest gate that would score full marks
    without doing the claimed work, and check that the round's controls cover it. For
    round 42: C1's cheapest gate is a script that prints the six target numbers without
    running the tool (covered by the tool-absent control and by `MUTANT_DETECTED`); C2's
    cheapest gate is a 24-row table whose verdicts are chosen to satisfy the counter
    rather than the evidence (covered by the flipped-row control, which the counter
    grades at 23/24). Check: the frozen counter's own text carries that line and the
    named gate is in the controls. Shown able to fail: round 42's C1 counter accepted
    43 identical `no-capture` status labels — the tool's own mislabel — because the
    check asserted only the field's DOMAIN, never its value. Operator proposal mined
    from `considerthese/2026-10-23.md` (2026-10-23). — `lessons/round-42.md`.

61. **A validated wave spec is not a completed dispatch.** A spec, a plan, and a
    registry whose agent ids are null are preparation. A dispatch is complete only
    when the dispatcher stayed alive until each seat settled, and the record names
    the seats that returned a report and the seats that died. Counting a prepared
    spec as a dispatched wave hides the shortfall. Check: the round report's wave
    section cites seat reports or names the dead seats with their last error; a
    registry of null ids with zero reports is a shortfall, not a completed wave.
    Shown able to fail: round 42's `w1/swarm-registry.json` has 64 members and null
    agent ids, and zero seat reports landed. Operator proposal mined from
    `considerthese/2026-10-24.md` (2026-10-24), "Track prepared-but-undispatched
    waves". — `lessons/round-43.md`.

## Round-44 additions (appended 2026-10-24; criteria 1–61 unchanged)

62. **Count claim errata in the round that froze them.** A round whose claims
    need many narrowings after freezing was frozen too broad. The count is the
    number of lines matching `^Erratum [0-9]+` in that round's claims file, not
    a prose impression. Check: `python3 corpus/evidence/round44/errata-count.py
    --file <claims>` prints the count. Shown able to fail: the two-line fixture
    `corpus/evidence/round44/controls/errata-two.txt` counts 2 and exits 0; the
    empty fixture `controls/errata-zero.txt` counts 0 and exits 1. Operator
    proposal mined from `considerthese/2026-10-24.md` (2026-10-24), "Count claim
    errata per round". The file was not edited. The operator's "round 35 needed
    nine" is that file's sentence, not a count this round re-derived. —
    `lessons/round-44.md`.

63. **A launcher's exit status is not evidence that its seats ran.** A
    dispatcher that writes its receipt and then exits 0 has certified that the
    receipt was written, not that anything was spawned. The tell is the
    receipt's own `n_spawned`/`n_reaped`, and a receipt with no
    `end parent_pid=` line is truncated, not clean. Check: read the
    launcher receipt and require `n_spawned >= 1` and an `end` line before
    counting a wave as dispatched. Shown able to fail: `tools/parent-lifetime.sh`
    given a malformed dispatch JSON writes `end … n_spawned=0 n_reaped=0` and
    exits 0 (`.ufo/waves/round-44/w3/W3ExecSelftest.md`), and the wave-2
    receipt of this round carries no `end` line at all
    (`.ufo/waves/round-44/w2-parent-lifetime.receipt`). Round-44 defect,
    named and not fixed in the round that found it. — `lessons/round-44.md`.

## Round-45 additions (appended 2026-10-25; criteria 1–63 unchanged)

64. **Every round verdict tags each claim as research ground or plumbing.** A
    claim is `ground` when it admits a source opened that round on a subject
    outside the lane's own tooling, or a knowledge entry on such a subject; it
    is `plumbing` when it changes a gate, counter, receipt pipeline or registry
    mechanism, even when sources were opened to support that work. Each claim
    row of a round's `SCORECARD.md` verdict table carries a `ground` or
    `plumbing` cell. Check: `python3 corpus/evidence/round45/tag-count.py`
    (default: rounds ≥ 45) prints `TAGGED=k/n` and exits 0 only when every
    claim row is tagged. Shown able to fail: rounds 35–44 carry no tag —
    `--from 35 --to 44` prints `TAGGED=0/22`, exit 1
    (`corpus/evidence/round45/controls/tag-control-r35-r44.txt`); history stays
    untagged and the rule binds forward. A tag's truth is a reader's check.
    Operator proposal mined from `considerthese/2026-10-24.md` (2026-10-24),
    "Tag each round as research ground or plumbing"; the file was not edited.
    The round-45 scribe's classification of rounds 35–44 found 2 of 22 claims
    `ground` (`.ufo/waves/round-45/w1/ScribeQuality64.md`). — `lessons/round-45.md`.

65. **A corpus's archive coverage is counted by value, not by field.** An entry
    that reports how much of a corpus is bound to an archived snapshot counts
    the values that are archive links, over the citations that name a source —
    not the fields that are filled. A filled field can hold a placeholder,
    another archiver or a link the corpus itself says fails; a missing key is
    not an empty field. Check: the entry's figure is re-derived by a committed
    recount over the capture (`corpus/evidence/round45/counts.json`,
    `extra_not_frozen`). Shown able to fail: the staged sentence "6,510 hold a
    non-empty archive.org URL" fails that recount — 5,959 of the 6,510 filled
    values are web.archive.org links, 429 are the literal `Metadata` — and the
    count over fields missed the 1,582 sourced answers that carry no archive
    key. — `lessons/round-45.md`.

    Note on 63 (round 45): `tools/parent-lifetime.sh` now exits 3 when its end
    line records `n_spawned=0` or a seat timed out, and requires `--timeout`
    in dispatch mode (`corpus/evidence/round45/c1-count.py`, 5/5). Criterion
    63's demonstration is the round-44 tool's behaviour and stays as history.

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
    `extra_not_frozen`). Shown able to fail: the staged entry's statement that
    6,510 evidence entries "hold a non-empty archive.org URL" (one bold
    sentence, wrapped across two lines in the staged file) fails that recount — 5,959 of the 6,510 filled
    values are web.archive.org links, 429 are the literal `Metadata` — and the
    count over fields missed the 1,582 sourced answers that carry no archive
    key. — `lessons/round-45.md`.

    Note on 63 (round 45): `tools/parent-lifetime.sh` now exits 3 when its end
    line records `n_spawned=0` or a seat timed out, and requires `--timeout`
    in dispatch mode (`corpus/evidence/round45/c1-count.py`, 5/5). Criterion
    63's demonstration is the round-44 tool's behaviour and stays as history.

    Note on 64 (round 45, wave 2): the check first matched claim rows at
    column 0 only, so an indented untagged row passed (`RevQuality64`, a forge
    scoring `TAGGED=21/21`, exit 0). It now takes 0–3 leading spaces, the
    census row rule; `controls/tag-control-indented-forge.txt` scores
    `TAGGED=1/2`, exit 1, and the r35–r44 control is unchanged.

## Round-46 addition (appended 2026-10-25; criteria 1–65 unchanged)

66. **An entry's inference must be cited and grounded, not merely plausible.**
    Every bullet under `#### Inference` names at least one `S###` source, and
    every backticked or quoted phrase and every figure in it appears verbatim in
    a span of a source that bullet cites (or is the designator of a cited
    document, `RFC 7089`). Check: `python3 tools/inference-ground.py --entry
    <entry> --spans corpus/evidence/round46/spans.tsv --counts /dev/null
    --registry corpus/SOURCES.md --root .` — exit 0 `GROUND: PASS`, exit 1 one or
    more `FINDING` lines. Shown able to fail: the three `junk-*.md` fixtures of
    `corpus/fixtures/inference-ground-r46/` each exit 1, and a "tool" that exits
    0 for names starting `positive-` fails the counter's `CANARY` leg
    (`corpus/evidence/round46/controls/c1-controls.txt`). Named limit: the check
    is lexical — correct tokens strung into an assertion of the opposite still
    pass, and 1–2 digit figures are never tokens. — `lessons/round-46.md`.

## Round-47 additions (appended 2026-10-25; criteria 1–66 unchanged)

67. **An Inference bullet must not reverse the polarity of a phrase it quotes.** A
    bullet that quotes a phrase its span negates must keep a negator next to that
    phrase's words when it reuses them, and a bullet quoting an affirmed phrase must
    not put a negator before one of its words; a counts figure whose key names a
    negation (`answers_without_key`) must be followed by one, and one whose key does
    not must not be. Check: `python3 tools/inference-ground.py --entry <entry> --spans
    <spans.tsv> --counts <counts.json|/dev/null> --registry corpus/SOURCES.md --root .`
    — a reversal prints `FINDING INF_POLARITY_FLIP`, exit 1. Shown able to fail: the
    three `junk-flip-*.md` fixtures of `corpus/fixtures/inference-ground-r47/` each exit
    1 on that code, and the round-46 tool scores them `JUNK_KILLED=0/3`
    (`corpus/evidence/round47/controls/c1-controls.txt`). Named limit: the check counts
    negators in fixed windows (three words before, two after; four after a figure) over
    words sharing a five-letter stem — it is not entailment: a flip through a different
    stem, a distant negator, or a second bullet still passes, and a correct bullet whose
    only negator sits outside the window, or whose negator binds a neighbouring word, is
    refused (wave-2 held-out sets: 4 of 12 flips killed, 2 of 12 correct bullets refused).
    — `lessons/round-47.md`.

    Note on 66 (round 47): its limit "correct tokens strung into an assertion of the
    opposite still pass" now holds only outside criterion 67's windows.

68. **A committed receipt is re-verified every round, at its measured revision and at the tip.**
    Each round, the newest committed `verify-receipts.py` is run read-only, in a `git archive`
    copy, over every receipt its active manifest names (today
    `corpus/evidence/round40/active-r39-receipts.tsv`: 6 receipts, rounds 39 and 40). Pinned leg:
    in an archive of the commit that added each receipt (`git log -1 --diff-filter=A -- <receipt>`),
    every active receipt prints `VERIFY: ok`; a refusal there means the receipt never verified as
    committed (the round-39 R1 class) and no claim may cite it. Tip leg: in an archive of `master`,
    every refusal is listed in the round lesson with its refusal name and the commit that last
    changed the bytes it binds (`git log -1 -- <path>`); a refusal with no such commit after the
    receipt's adding commit is a defect, not drift. Check: `git archive <rev> | tar -x -C <tmp> &&
    (cd <tmp> && python3 corpus/evidence/round40/c1-count.py)` — at `b173b094` (last tree before
    the round-41 gate edit) `R39_ACTIVE_RECEIPTS=6/6`, exit 0; at `a15610a5` `R39_ACTIVE_RECEIPTS=2/6`,
    exit 1, all four refusals `gate-sha256-mismatch` after `1bd9001` moved `tools/research-gate.sh`
    from `4253c187…` to `2cb04bdd…` (`lessons/round-41.md`, post-landing addendum). Shown able to
    fail: in the `b173b094` copy, change byte 676 of `c1-base-s39001-regenerated.json`
    (`"matched": 7` to `6`); the verifier refuses `receipt-self-digest` and the counter prints
    `R39_ACTIVE_RECEIPTS=5/6`, exit 1; restoring the byte returns 6/6, exit 0. Named limits: the
    pinned leg anchors on the adding commit because receipts carry no revision field; the c2
    receipts bind `subject_counter` as an absolute live-lane path, so an archive copy still reads
    that file from the live tree; a pass proves integrity against committed bytes, not authorship.
    Operator proposal mined from `considerthese/2026-10-24.md` (2026-10-24), "Spot re-verify one
    receipt a week"; the file was not edited. — `lessons/round-47.md`.

## Round-48 additions (criteria 1–68 unchanged)

69. **A polarity precision result is a bounded regression set, not a general rate.**
    A polarity counter names its correct-bullet regression population and threshold,
    keeps flip-positive and legacy no-regression controls in the composite claim, and
    records the false refusals and their cue/window classes. Do not describe a fixed
    12-case regression set as general-language precision. Check:
    `python3 corpus/evidence/round48/c1-count.py` plus
    `python3 corpus/evidence/round48/mutation-check.py`; the R47 tool control prints
    `CORRECT_BULLETS_PASS=9/12` against a frozen minimum of 11/12 and C1 fails, while
    R48 after-measurement records every leg. `precision-count.py` alone accepts an
    accept-all program; the no-read name-key lookup also passes `c1-count` alone, but
    the frozen composite rejects it when installed at the default tool path
    (`controls/name-key-control.txt`, `MUTATION_NOT_APPLIED`). The 12 texts are
    recycled R47 held-out regression cases, not a fresh estimate.
    The R48 Named limit records the current bullet-side windows (P1: 7-before/3-after; P2: 2-before); the span-side window remains 3-before. Criterion 67's 3/2 values describe the R47 behavior.
    Round-49 additions: (a) the two-word P2 look-back has an unmeasured false-negative
    class — a plain denial of an affirmed phrase passes when its negator sits three words
    before the phrase stem (a05, `that date is not the copy's build date`, and the W1
    `DraftP2Limit.md` denial both exit 0; a two-before control exits 1), while
    `python3 corpus/evidence/round48/precision-count.py` still prints
    `CORRECT_BULLETS_PASS=12/12` because no frozen case tests it; (b) the round-48
    closure ruled a05's correct label false, so the R47 tool's false refusals on this set
    are 2/12 (p03, p04); (c) pointer correction: the round-48 lesson has no Mistake 4 —
    this criterion rests on its `## Spot-check intake` rows 1–3.
    — `corpus/lessons/round-48.md` Mistake 4; S095.

70. **A control receipt preserves the observed exit/result pair.** A control is
    measured only when its stored case labels, stdout and subprocess exit agree with
    a replay of the same command on the same committed bytes; never transcribe an
    output line independently of its process status. Check: re-run the exact command
    and diff its stdout and exit against the receipt. Shown able to fail:
    `corpus/evidence/round48/controls/before.txt` recorded `FAIL wanted_rc=0
    observed_rc=0` for `/usr/bin/true`; rerunning
    `python3 corpus/evidence/round48/c1-count.py --tool /usr/bin/true --cases-only`
    shows `observed_rc=1` (the Python interpreter rejects the ELF binary), documented
    in `controls/before-erratum.txt`. — `corpus/lessons/round-48.md` Mistake 5.

71. **A round report's freshness line states the age of the newest capture the lane
    may read.** While L0 `8d77e6c1` (fetch scope) is open freshness cannot move; the
    report makes that cost visible instead of repeating "unchanged". Check:
    `python3 corpus/evidence/round49/capture-age-check.py <report>` — exit 0
    `FRESHNESS_CAPTURE_AGE=PASS` when one line names freshness, a capture and an ISO
    date; exit 1 `FAIL`. Shown able to fail: the round-48 report
    (`/home/vgpnk/Projects/shokunin/.ufo/reports/round-48/chousa.md`) prints `FAIL`,
    exit 1. — `considerthese/2026-10-25.md:55-56` (mined 2026-10-25);
    `corpus/lessons/round-49.md` `## considerthese`.

72. **A span-quote counter has a substance floor, and a capability counter has a
    perturbed-input leg.** Structural legs (quote in span, in entry, in lesson; exact
    capture slice; anchor at the quote offset) all pass a single-space quote over a
    whole-capture span; fixed-input legs all pass a replay of the real tool's outputs.
    Before freezing such a counter, score a hollow-quote control and a replay control
    with it (QUALITY 60). Check for span manifests:
    `python3 corpus/evidence/round49/quote-substance-check.py [MANIFEST]` — exit 1 on a
    quote under 3 non-space characters, an id with no quote of 12 or more, or a span
    wider than its quote plus context; exit 0 otherwise. Shown able to fail: the W1
    `CritForgeC2` shape (single-space quote, 5000-character span) prints
    `HOLLOW_QUOTE`/`OVERWIDE_SPAN`/`NO_SUBSTANTIVE_QUOTE`, exit 1; the round-49 manifest
    prints `IDS=8 QUOTES=28 FAILURES=0`, exit 0. — `corpus/lessons/round-49.md`
    Mistakes rows 2–3.

## Round-50 additions (appended 2026-10-25; criteria 1–72 unchanged)

73. **A capability's self-test compares against an expected file written from the rule,
    never one the tool emits, and is scored on perturbed copies against an echo control
    and a constant control.** A comparison with the tool's own earlier output, or with a
    file a flag regenerates, proves replay, not the rule. Check (C1):
    `python3 corpus/evidence/round50/c1-count.py` — five legs on the digest-pinned
    package `corpus/evidence/round50/c1-fixtures/` (`FIXTURES_SHA256=c5c56480…`): the
    lane default, the baseline (`SELFTEST=PASS findings=26 expected=26` and that digest),
    six perturbed copies P1–P6 (each exit 1 with its named `DIFF` line), an unparseable
    expected file (exit 2 `SELFTEST=ERROR`), and `corpus/evidence/round49/c1-count.py
    --tool <tool>` still `C1=PASS`; target `LEGS=5/5`, exit 0. The expected file is
    hand-written (`tools/assimilate-rows.py` docstring) and `selftest()` only reads it.
    Shown able to fail (`corpus/evidence/round50/controls/c1-before.txt`): the base tool
    → `BASELINE=FAIL rc=2`, `LEGS=2/5`; the echo control → `BASELINE=PASS`,
    `PERTURB_PASS=0/6`, `LEGS=4/5`, `C1=FAIL`; the constant control → `PERTURB_PASS=0/6`,
    `LEGS=2/5`, `C1=FAIL`. Named limits: the echo control passes the baseline, so only
    P1–P6 separate a real self-test from an echo; a duplicated expected line is not one of
    the six (W1 `ReviewSelftestCode` F1 found it after the freeze — the tool now compares
    multisets, `corpus/evidence/round50/selftest-duplicates-after.txt`); a pass is
    conformance on fixed fixtures, not a rate. — `corpus/lessons/round-50.md`
    `## Mistakes` row 6; round-49 spot-check defect 3.

74. **A count written in lane prose is derived from a receipt by a check, not carried
    over from an earlier report.** A manifest grows and every sentence that quoted its
    size keeps the old figure. Check:
    `python3 corpus/evidence/round50/stale-count-check.py` — the patterns `QUOTES=<n>`,
    `<n>-row manifest`, `<n> located quotes`, `CAPTURE_BOUND=<n>/<n>` in
    `corpus/QUALITY.md`, `corpus/README.md`, `LOG.md` and `corpus/lessons/round-49.md`
    against the 31 data rows of `corpus/evidence/round49/spans.tsv`; each stale hit prints
    `STALE path:line says N, receipt M`, exit 1; exit 0 when every hit agrees or a later
    line of the same file reads `correction: … superseded by …` and names the stale
    line. Shown able to fail: before the correction lines it prints four `STALE … says 28,
    receipt 31` (`corpus/evidence/round50/stale-count-before.txt`, exit 1); after them
    `STALE_COUNT=PASS`, exit 0 (`stale-count-after.txt`). Named limits: digit forms only,
    one receipt per scan. — `corpus/lessons/round-50.md` `## Mistakes` row 1; round-49
    spot-check defect 2.
    correction: corpus/QUALITY.md:746 (criterion 72, `QUOTES=28`) superseded by the receipt's 31 (`IDS=8 QUOTES=31 FAILURES=0`, `corpus/evidence/round49/measure-after.txt`).

75. **A round report is filed only after every wave seat report exists on disk.** A report
    filed mid-wave hides which seats never returned; the gate reads the wave spec, not the
    roster. Check: `python3 corpus/evidence/round50/wave-complete-check.py <wave-spec.json>
    <report-dir> [--rev REV --lane DIR]` — prints `MISSING <name>` per spec item with no
    `<name>.md` in the report dir (on disk, or in the lane tree at `--rev`), exit 1; exit 0
    when every item has a report; exit 2 on an unusable spec. Shown able to fail
    (`corpus/evidence/round50/wave-complete-before.txt`): the round-49 w2 spec at
    `5275c892` (the revision the round-49 report cited) prints eight `MISSING` names,
    `OK 27/35`, exit 1. Named limit: presence only — a stub report passes; and a report
    that exists but belongs to another round is not detected here (QUALITY 78). —
    `corpus/lessons/round-50.md` `## Mistakes` row 2; round-49 spot-check defects 1 and 4.

76. **Every `char N` offset in a lesson names the capture form it indexes.** An offset is
    meaningless without its text form: the round-49 NCPSSD help-page offsets differed by a
    constant 316 characters between two decodes of one capture (spot-check defect 5).
    Check: `python3 corpus/evidence/round50/decode-form-check.py corpus/lessons/round-<N>.md`
    — `FORM_NAMED` when the file names `.txt` read as UTF-8, `utf-8-sig`, or `.raw` decoded
    as UTF-16LE, `FORM_MISSING` (exit 1) when it has offsets and no form. Shown able to
    fail: `corpus/lessons/round-47.md` prints `FORM_MISSING`, exit 1; `round-50.md` prints
    `FORM_NAMED`. Named limit: one naming per file, not per offset; historical lessons
    stay as filed (append-only). — round-49 spot-check defect 5.

77. **An adoption run's renumbered ids are all `source:` ids of the entries, never body
    cross-references.** The adopter renumbers every staged id token an entry mentions, so a
    prose reference to another document becomes a row for that document and shifts the real
    ones. Check: `python3 corpus/evidence/round50/cited-id-check.py <renumber.tsv>
    <entry.md> [...]` — `BODY_CROSSREF staged->lane` per renumbered id no entry names at
    the start of a `source:` line, exit 1; `CITED_IDS=PASS` exit 0. Shown able to fail
    (`corpus/evidence/round50/cited-id-before.txt`): the as-staged run prints
    `BODY_CROSSREF S109->S104` and `S111->S105`, exit 1; the run on entries with body-only
    ids removed prints `CITED_IDS=PASS rows=5`. Named limit: an id the adopter does not
    renumber (a lane-registry id) passes through unseen. — `corpus/lessons/round-50.md`
    `## Mistakes` row 3.

78. **Seat names in a wave spec are unique across rounds.** The validator checks names
    inside one wave; the dispatcher resumes a parked agent that already carries the name,
    and that agent answers with its old report. Check: `python3
    corpus/evidence/round50/name-collision-check.py <wave-spec.json>` — `NAME_COLLISION name
    path` per item whose name is the basename of a report file of another round's wave
    directory, exit 1; exit 0 when none. Shown able to fail
    (`corpus/evidence/round50/name-collision-before.txt`): the round-50 wave-1 spec prints
    13 `NAME_COLLISION` lines, exit 1; those 13 seats returned round-49 reports. Run it on a
    spec before writing the `.ready` file. — `corpus/lessons/round-50.md` `## Mistakes` row 4.

79. **A grounding gate handles the script of its inputs, and says so.** `inference-ground`
    counted words by ASCII letters, so a pure-Chinese phrase was never a grounding token
    and a grounded Chinese bullet failed `INF_UNGROUNDED` (round 49 passed only on Latin
    runs). The tool now counts four CJK characters as two words; a CJK token must occur in
    a cited span, and no polarity check is made on it (`words()` stays Latin-only — a named
    limit: a CJK denial of a quoted phrase is not caught). Check: `python3
    corpus/evidence/round50/cjk-ground-check.py --old <pre-change tool>` — case A (correct
    bullet) rc 0, B (phrase absent from the span) rc 1 `INF_TOKEN_NOT_IN_SPAN`, C (no id)
    rc 1 `INF_UNCITED`, `CJK_GROUND=PASS`; the old tool prints rc 1 `INF_UNGROUNDED` on A.
    The round-46/47/48 counters give identical output before and after
    (`corpus/evidence/round50/inference-regression-before.txt`, `-after.txt`). —
    `corpus/lessons/round-50.md` `## Mistakes` row 5.

80. **A capability counter that recognises its own perturbations is paired with a nonce leg and an exclusive output set.** The frozen round-50 C1 counter searches for one `DIFF` line per fixed perturbation, so a 42-line tool that prints all six literal lines for any non-pinned digest passes it (`LEGS=5/5`, W2 `R50CritForgeC1`). Check: `python3 corpus/evidence/round50/c1-supplement.py [--tool PATH]` — P7 (a random recheck token the tool author cannot know; the DIFF set must equal exactly three lines) and four hardening probes (duplicate expected line, no entry, option clash, id-less entry); exit 0 `C1_SUPPLEMENT=PASS` for the real tool. Shown able to fail (`corpus/evidence/round50/c1-supplement-receipt.txt`): forge 1/5, echo 2/5, constant 0/5, base tool 1/5, each `C1_SUPPLEMENT=FAIL`. Named limits: a tool that reimplements the adopter passes by definition; the supplement is post-freeze and supplements, never replaces, the frozen counter. — `corpus/lessons/round-50.md` `## Wave-2 narrowing`.

74 (round-50 named limits, appended): the scan set is pinned to four files and the patterns are not vintage-aware, so a round-50 count phrased `<n>-row manifest` would be judged against the round-49 receipt; the round-50 manifest is therefore written as `67-quote manifest`, and a successor check needs a receipt per vintage (W2 `R50ReviewQuality`). 77 and 78 each have branches the round's own tables never exercise (prefix ids, case-only and non-w1 collisions; W2 `R50MutCitedId`). 76 now requires a naming line that also says `char`, offset or decode form and is not negated; a wrong form named passes.

## Round-51 additions (appended 2026-10-25; criteria 1–80 unchanged)

81. **A capability counter generates its own inputs at counting time from a nonce, and keeps its expected values in itself.** A
    counter that reads a package its tool's author can open is satisfiable without the behaviour: the frozen round-50 C1 counter
    searched for one literal `DIFF` line per fixed perturbation, so a tool printing all six lines for any input passed
    (`LEGS=5/5`, W2 `R50CritForgeC1`). The round-51 counter seeds from `os.urandom(8)` unless `--seed`, draws host and ids per run
    (`corpus/evidence/round51/c1-count.py:101,121-127`), hands the tool only
    `--staged/--knowledge/--registry/--opened/--out/--entry` and no expected file (`:77-83`), and keeps the expected relations as
    literals (`:155-157`) beside the fixtures pin (`:47`). Check: `python3 corpus/evidence/round51/c1-count.py [--seed N] [--tool
    PATH]` — five legs, exit 0 `LEGS=5/5` `C1=PASS`; exit 1 on any leg failing; exit 2 `PIN_CHANGED` when the round-50 fixture
    package no longer hashes to the pin. Shown able to fail (ran at the tip, `--tool`): `tool-before.py` `LEGS=1/5`,
    `flag-noop-tool.py` `LEGS=2/5`, each `C1=FAIL` rc 1; `corpus/evidence/round51/controls/c1-before.txt` records the same for
    `tool-before`/`echo`/`const`/`flag-noop`. Named limits: with `--tool` the SELFTEST_DEFAULT leg is skipped and counted as
    passing, so a control starts at 1/5; a tool that reimplements the adopter passes by definition; the nonce legs test the
    adopter's interface on generated packages, never the lane entries. — `corpus/lessons/round-51.md` `## Mistakes` row 2;
    `corpus/evidence/round51/claims.md` R51-C1; round-50 spot-check routed defect 2.

82. **An adopter cites only `source:` ids and lists the ids it leaves in the body.** A default that renumbers every id token turns
    a prose mention into a row for an unrelated document; round 50 answered with a check, round 51 makes the reading the default,
    so the earlier one-shot counters needed the old mode by name. The default cites the id right after `source:` on each header line above the first `####` heading (W1 `R51ReviewAdopterCode` F1/F3: ids in a line's tail, `source:` lines in the body and another entry's citations are not citations; an entry's own ids only are substituted in it), leaves a body-only
    id unchanged in the entry text and lists it in `bodyonly.tsv` with `BODYONLY=<n>`; `--cites all` (env `ASSIMILATE_CITES=all`)
    keeps the round-49/50 reading. Check: `python3 corpus/evidence/round51/c1-count.py` — the SOURCE_ONLY leg requires
    `renumber.tsv` to hold exactly the two `source:` ids (`append` to the registry maximum + 1, `held` to the row carrying the
    URL), `append.md` one row, the body-only id present in the rewritten entry, both cited ids absent from it, `bodyonly.tsv`
    equal to `[["corpus/knowledge/e.md", <body id>]]`, `BODYONLY=1`, and the `--cites all` run to renumber all three and append
    two; `LEGS=5/5` exit 0. Shown able to fail (ran at the tip): `flag-noop-tool.py` (accepts `--cites`, ignores it)
    `SOURCE_ONLY=FAIL default_rc=0 map=['S528','S784','S878'] appended=2 bodyonly=[]`, `LEGS=2/5`; `tool-before.py` `LEGS=1/5`.
    Named limits: `bodyclash.tsv` (a body-only id that is also a lane id) is reached by no leg of the FROZEN counter — its staged ids are S500–S900 and its lane ids ≤ S040, disjoint by construction — and only by the post-freeze supplement's CLASH leg (`c1-supplement.py`; `tools/assimilate-rows.py`, the `bodyclash` block after the rewritten entries are written); an id the adopter does not
    renumber still passes unseen (QUALITY 77's limit). — `corpus/lessons/round-51.md` `## Mistakes` row 3;
    `corpus/evidence/round51/claims.md` R51-C1; QUALITY 77.

83. **A self-assessment pointer resolves, or carries a `correction:` line naming a non-empty target.** Five pointers in
    `SCORECARD.md` capability rows and `SHONEN.md` evidence lines name paths the tree does not hold, and no criterion read them.
    Check: `python3 corpus/evidence/round51/c3-count.py [--root LANE]` — `CAP_ROWS=n (base 36)`, `POINTERS=n (base 74)`,
    `RESOLVED_BY_CORRECTION=n`, one `DANGLING <file>:<line> <pointer>` per unresolved pointer, `DANGLING=n`, `C3=PASS` exit 0 only
    when `DANGLING=0` and neither count fell below base. A pointer resolves when `<lane>/<pointer>` is a non-empty file or a
    directory holding a file, or a later `correction: SCORECARD.md:<row line> <pointer> -> <path>` line names that row and an
    existing non-empty `<path>`. Shown able to fail (ran at the tip): `DANGLING SCORECARD.md:1843 measure/final/`, `:2073
    measure-l1/c1-s36361.json`, `:2074 measure-l1/c2-s36371.json`, `:2616 c1-supplement.py`, `DANGLING SHONEN.md:10
    round25-meta-differential.log`, `DANGLING=5 C3=FAIL` rc 1; `controls/build-c3-controls.py` (ran) prints BLANKET `DANGLING=5`,
    DELETED `CAP_ROWS=32 POINTERS=59`, EMPTY `DANGLING=5`, all `C3=FAIL`. Correction branch (ran, scratch roots): non-empty target
    `RESOLVED_BY_CORRECTION=1 DANGLING=4`; zero-byte and missing targets `=0`. Named limits: existence, not truth; the three
    controls prove failure modes only and never a valid correction (my probe is not a round artefact); a `correction:` line names
    a line number, so an edit that shifts the row invalidates it; a correction is accepted in any line order (the word "later" above is not enforced) and only for SCORECARD rows — a dangling SHONEN pointer has no correction form; the counter's own tokenizer produced three of the first eight
    `DANGLING` lines (row 5) — extraction is part of the predicate. — `corpus/lessons/round-51.md` `## Mistakes` rows 4 and 5;
    `corpus/evidence/round51/claims.md` R51-C3; `corpus/evidence/round51/claims-erratum.md` E1.

84. **A receipt names the tool revision it was measured against, and the tip still carries that tool.** The round-50
    after-measurement opened "at the working tree before the final commit" and named no hash, and the `SKILL.md` Gates row named
    candidate `ec52e632`, not the landed tip, so neither could be tied to code. Check: `python3
    corpus/evidence/round51/receipt-check.py <receipt> [...] [--root LANE] [--tip REV] [--skill SKILL.md]` — a receipt's first
    five lines must carry `tool-rev: <40-hex> tool: <lane-relative path> [digest: sha256:<64-hex>]`; `RECEIPT_NO_REV`,
    `RECEIPT_REV_UNKNOWN`, `RECEIPT_REV_UNLANDED` (not an ancestor of the tip), `RECEIPT_TOOL_ABSENT`, `RECEIPT_TOOL_MOVED` (the
    tool's blob at the tip differs from its blob at that revision), `RECEIPT_DIGEST_MISMATCH`, else `RECEIPT_OK`; `CHECKS=n OK=n
    FAILS=n` (the skill line is a check), `RECEIPT_CHECK=PASS` exit 0, exit 1 on any failure, exit 2 when the root is not a git work tree. Shown able to fail
    (ran): the filed round-50 receipt and the current Gates row print `RECEIPT_NO_REV corpus/evidence/round50/measure-after.txt`
    and `SKILL_NO_PIN SKILL.md`, `FAILS=2` rc 1; scratch receipts print `RECEIPT_REV_UNKNOWN … rev=000…0`, `RECEIPT_REV_UNLANDED …
    rev=1fce006153ab`, `RECEIPT_TOOL_MOVED … rev=d603f6f00f78 tool=corpus/evidence/round51/c3-count.py` (the erratum changed that
    blob), `RECEIPT_DIGEST_MISMATCH recorded=000000000000 actual=94ddc7dc273c`, `RECEIPT_TOOL_ABSENT`; a header naming the tip and
    that blob's digest prints `RECEIPT_OK … rev=cfe6c9fb9b56`, `RECEIPT_CHECK=PASS` rc 0. Named limits: the header is a convention, not a signature — a receipt can name a revision it did not run at; the zero-receipt pass and the `--skill` leg that could not read the Gates table were fixed after W2 (`receipt-check.py` now needs at least one receipt and reads the first table row carrying the header); only the first five lines are read; a receipt
    measuring a tree count has no header form here; the digest leg hashes the blob, not the tool's behaviour; receipts filed
    before round 51 stay as filed (append-only) and fail this check by construction. — `corpus/lessons/round-51.md` `## Mistakes`
    row 1; `corpus/evidence/round51/claims.md` freeze section; round-50 spot-check routed defect 1.

85. **A counter's work directories carry random names, its do-nothing controls delegate to a pinned base, and a post-freeze supplement states what the frozen counter cannot see.** The frozen round-51 C1 counter names its subtests `s`, `d1`, `d2`, `renamed-heading`, so a 94-line tool that reads the name out of `--out` and prints canned shapes passes it `LEGS=5/5` (`corpus/evidence/round51/controls/forge-dirname.py`, W1 `R51CritForgeC1`); its id draws can collide and hang it (1/401 per run, `R51ExecSeedRuns`); an ambient `ASSIMILATE_CITES` flips its verdict (`R51SentScope` H5); and the shipped echo control delegated to the lane tool, so at the tip it scored `LEGS=5/5` and had stopped being a control. Check: `python3 corpus/evidence/round51/c1-supplement.py [--tool PATH]` — six legs (`SHAPE`, `MUTATION`, `CROSS_ENTRY`, `SOURCE_LINE`, `UNKNOWN_SRC`, `CLASH`) on packages in random-named directories with the variable removed from the tool's environment; exit 0 `SUPPLEMENT_LEGS=6/6` for the lane tool. Shown able to fail (`corpus/evidence/round51/controls/c1-supplement-controls.txt`): the frozen counter prints `LEGS=5/5 C1=PASS` for `forge-dirname.py` and for `tool-candidate1.py` (the first candidate, before the W1 review fixes) while the supplement prints `SUPPLEMENT_LEGS=1/6` and `3/6`; `tool-before.py`, `echo-tool.py`, `const-tool.py` 0/6, `flag-noop-tool.py` 1/6. At the tip the shipped echo control (delegating to the lane tool) had scored `LEGS=5/5`; the round-51 echo and const controls now `os.execv` to `controls/tool-before.py` (E4) — re-run at the tip they print `LEGS=2/5` and `1/5`. Named limits: the supplement is post-freeze (the frozen counter, predicate and target are unchanged — `corpus/evidence/round51/claims-erratum.md` E2–E5) and a tool that reimplements the adopter passes both by definition. — `corpus/lessons/round-51.md` `## Mistakes` rows 2 and 8. After wave 2 the supplement draws random entry names too and has ten legs (`SHAPE`, `MUTATION`, `CROSS_ENTRY`, `SOURCE_LINE`, `UNKNOWN_SRC`, `CLASH`, `OWN_WORK`, `STALE_OUT`, `HEADER`, `ENV_DEFAULT`); the 87-line `controls/forge-dual.py` (W2 `R51W2CritForgeSupplement`) passed the earlier six-leg form 6/6 and now prints `3/10`; the arms race stays open — a tool that reimplements the adopter passes by definition.

86. **A counter's tokenizer is run on a positive control seeded with the class it can mangle.** The round-51 C3 extractor stripped a leading dot, so three existing `.ufo/...` paths read as `DANGLING`; its three controls were all derived from its own `DANGLING` list and could not show that (`corpus/evidence/round51/claims-erratum.md` E1). Check: `python3 corpus/evidence/round51/controls/build-c3-controls.py` — the BLANKET, DELETED and EMPTY controls start from the BASE `SCORECARD.md`/`SHONEN.md` and print `C3=FAIL`; the DOTPATH positive control appends a capability row whose pointer is the real dot-leading path `.ufo/waves/round-51/gen-w1-spec.py` and prints `DANGLING=0 C3=PASS`, and the same row under the pre-erratum counter (`git show d603f6f0:corpus/evidence/round51/c3-count.py`) prints `DANGLING SCORECARD.md:<line> ufo/waves/round-51/gen-w1-spec.py` — red before, green after (`corpus/evidence/round51/controls/c3-controls-final.txt`). Named limit: one class (leading dot); other token shapes (a `~` or an absolute path) are not seeded. — `corpus/lessons/round-51.md` `## Mistakes` row 5.

87. **A capture is read through a defined text form before a quote is located in it or the source is refused for its form.** Round 51 refused the NIPH `.docx` "for its capture form" because no lane reader produced its text; the cache's `.txt` sidecar was the zip bytes decoded with replacement (168,953 characters decoded from its bytes with replacement, 72,117 U+FFFD), and the cheap member-strip reading is wrong on that very file (50 `w:instrText`, 60 `mc:Fallback` in its main part). Check: `python3 tools/capture-text.py <raw> --locate '<quote>'` prints `LOCATED count=1 offset=<N>` for every quote a lesson cites from an OOXML capture, and an entry's `char N` equals that offset. Shown able to fail (ran): the member-strip control `corpus/evidence/round52/controls/naive-tool.py` scores `LEGS=4/9` on `python3 corpus/evidence/round52/c1-count.py --tool …` and puts the NIPH quote at 10319 of 21,910 characters instead of 8996 of 19,682; the sidecar reading scores `LEGS=0/9`. Named limits: OOXML WordprocessingML only — an OLE `.doc` (UTF-16LE runs, round 48), a PDF and an HTML capture keep their own forms; a refusal for form is still allowed when no lane reader exists, with that reader as the flip. — `corpus/lessons/round-52.md` `## Mistakes` row 1; claim R52-C1.

88. **A capability counter varies the input's representation, not only its content and names, and a fixed-input leg pins the expected content.** The frozen round-52 C1 counter drew text, member and file names from fresh randomness (criteria 81, 85) yet always spelled the XML the same way, so an 85-line regex tool keyed to `w:` prefixes, the rels attribute order and self-closing `<w:tab/>` passed `LEGS=9/9`, and its REAL leg accepted a 21-character stub because it checked only self-consistency (`corpus/evidence/round52/controls/forge-shape.py`, W1 `R52CritForgeC1`). Check: `python3 corpus/evidence/round52/c1-supplement.py [--tool PATH]` — PREFIX, RELS_FORM, SYNTAX re-spell generated documents without changing their text form, REAL_TEXT pins the sha256 of the NIPH text form from the independent reader. Shown able to fail (ran): the forge and the naive control print `SUPPLEMENT_LEGS=0/4`, the tool `4/4`. Named limit: a tool that embeds a real XML parser passes, which is the rule implemented, not a forge; the supplement is post-freeze and reported beside the frozen counter (`corpus/evidence/round52/claims-erratum.md` E1). — `corpus/lessons/round-52.md` `## Mistakes` row 3.

89. **A verdict line's stated offset is re-located in its stated form before it is written.** The round-51 quarantine verdict for register S120 carried `char 39411` in "`.raw` unzipped → `word/document.xml` UTF-8", where the sentence does not occur contiguously (`find` → -1), and the non-author spot-check accepted the row. Check: for every `register S### … verdict:` block in a lesson, each quote line's `char N` equals the quote's offset in the named form (for `form capture-text`: `python3 tools/capture-text.py <raw> --locate '<quote>'`). Shown able to fail (ran): the round-52 S120 lines give `LOCATED count=1 offset=8996`, `9020`, `9428`; the round-51 line's form and offset give -1. Named limit: a manual check, not a counter; it binds where a quote is, not what it means. — `corpus/lessons/round-52.md` `## Mistakes` row 2.

90. **A reader of untrusted captures refuses what it cannot render faithfully: a non-target part type and an inflated part.** The C1 candidate printed an empty text form at exit 0 for two `.xlsx` captures and for the theme part an OLE `.doc` with an embedded OPC zip points at (W1 `R52ExecRealDocx`), and rendered a 524,901-byte package into 60,000,000 characters at exit 0 (W1 `R52SentCapture` H1 shape). Check: `python3 tools/capture-text.py <raw>` exits 2 with `REFUSED main part '…' is not WordprocessingML …` on `cb101e95f5f5e98d019eeca1.raw` and `REFUSED '…' inflates to <n> bytes (limit 268435456)` on a part over 256 MiB. Shown able to fail (ran): candidate `804a4537` exits 0 on both. Named limits: the bound is uncompressed bytes per part (criterion 18: a byte cap is not a time bound); entity expansion is bounded by the interpreter's expat (2.9.0 here), not by the tool. — `corpus/lessons/round-52.md` `## Mistakes` rows 5 and 6.

91. **A frozen capability counter generates representation variance inside the input's identity rule, so a forge keyed to one spelling fails.** The round-52 counter drew text and names from fresh randomness (criteria 81, 85) and still spelled every document one way, so an 85-line forge passed `LEGS=9/9` (ran: `python3 corpus/evidence/round52/c1-count.py --tool corpus/evidence/round52/controls/forge-shape.py` → `LEGS=9/9 C1=PASS`). The round-53 counter spells one URL five ways inside the census identity — http or https, upper-case host, a trailing `/` (`corpus/evidence/round53/c1-count.py:96`) — writes Registry rows at 0–3 leading spaces (`:138`) under `##` + space or tab (`:141`), and re-draws the spelling for every staged row and every entry citation. Check: `python3 corpus/evidence/round53/c1-count.py --tool <tool> --seed 53 --per-leg 1` — the landed tool gives `LEGS=8/8 C1=PASS`; the same tool with `url_of` replaced by an exact-spelling read (`re.search(r"https?://[^\s|]+", s).group(0)`) gives `LEGS=5/8` with `TWIN=FAIL HELD=FAIL MIX=FAIL map=differs`, while RECHECK/ORDER/NOENTRY/REAL/REGRESS still pass (both ran). Named limits: `spell` varies host case only — the counter's own expectation lowercases the whole URL (`:191`) while the tool's identity lowercases the host alone (`tools/assimilate-rows.py:133`), so a path-case variant would set the expectation against the tool and is not generated (reported below); the REAL leg's spellings are the campaign's own, so the spelling-keyed tool passes REAL (`CITED=6 APPEND=5 HELD=0 TWIN=1`) and only the six generated legs catch it; a tool that normalises *more* than the census identity (casefolding the path) is not exercised at all. — `corpus/lessons/round-52-verifier-spotcheck.md` section 6 item 3; `corpus/lessons/round-52.md` `## Mistakes` row 3.

92. **An adopter label names what is true of the registry: `held` only for a URL a Registry row carries, `twin` only for an id the same run minted, and the count line carries both.** At `BASE_REV` the adopter labelled staged S195 `held` — `CITED=6 APPEND=5 HELD=1`, `S195 → S118` — although no row of `corpus/SOURCES.md` at that revision carries its URL (0 rows match `url_of`; the id `S195` does not occur there): the id was minted by the run, which is `twin`. Check: `python3 corpus/evidence/round53/c1-count.py` legs TWIN, HELD, MIX, REAL — the landed tool prints `HELD=0 TWIN=1` on REAL and `LEGS=8/8 C1=PASS`; the tool at `BASE_REV` prints `HELD=1` with no `TWIN=` token at all and `LEGS=1/8` (both ran). Shown able to fail (ran): the base tool's HELD case reaches `map=ok rows=1` and still fails its leg, because its count line carries `HELD=` but no `TWIN=`; the label defect itself appears only on REAL. Named limits: the legs read `renumber.tsv`, `append.md` and the count line — right counts with wrong labels fail the map leg (observed on the spelling-keyed tool), right labels with one missing count token fail the count leg (observed on `BASE_REV`); neither leg reads the label's prose. — `corpus/lessons/round-52-verifier-spotcheck.md` section 6 item 4 (round-51 routed 2).

93. **A refusal reason is the decisive one: when a row or entry is refused on two grounds, the Gate and the tool state the ground that holds alone, and a province reason is used only for the claim's spine.** Round 52 refused the grey-literature entry with "out of province for its spine" (`corpus/lessons/round-52.md:64`) although the headline is a search-record field and so in province, and the ground that held alone was URL duplication — `SOURCES.append.md:36` and `:58` carry the same URL byte for byte (ran); the non-author closure recorded it as a disputed reason (`round-52-verifier-spotcheck.md:77`, "agree on the decision, **disagree on one reason**"). Check: for each refusal cell naming two grounds, withdraw one ground and re-test the other on the row alone; the cell's first ground must be the one that survives. Runnable legs (ran): the two campaign rows' URLs are identical; a staged row that is both ten cells and URL-less gets one line, `REFUSED S200: staged row has 10 cells, not 11`, from the `if`/`elif` at `tools/assimilate-rows.py:467-469` — the cell-count ground, not the URL ground. Named limit: the Gate side is a manual check, as 89 is; the two legs show the grounds, not the Gate's choice of one. — `corpus/lessons/round-52-verifier-spotcheck.md` section 6 item 2; the `grey-literature-and-chinese-search-record-r40.md` Gate row of round 52.

94. **A routed defect that two closures carry is landed with a test or retired with a reason in the next round, never carried a third time unlanded.** The adopter twin-label defect was routed in round 51 (`round-51-verifier-spotcheck.md` section 6 item 2, "fix with a self-test row each") and carried in round 52 (`round-52-verifier-spotcheck.md` section 6 item 4, "built in scratch and not landed"), with no commit touching the tool in that window (ran: `git log --oneline 41b4dca..5b550133 -- tools/assimilate-rows.py` → 0 lines). Round 53 landed it: `git log --oneline 5b550133..32aab5e -- tools/assimilate-rows.py` → `32aab5e round-53: C1 candidate — adopter v4 twin label, recheck pre-pass, registry-first refusal; self-test cases`, carrying `corpus/fixtures/assimilate-selftest/cases/twin-recheck` and `…/refusal-order`, and `python3 tools/assimilate-rows.py --selftest` → `SELFTEST=PASS findings=40 expected=40` (ran). Check: for every item a second closure re-lists, one of — a commit inside the round window that touches the named surface and carries the self-test case, or a lesson sentence naming why it is retired; a third carry with neither fails. Named limit: the window is read by path, so a landing that renames or moves the surface is invisible to it, and the retirement-sentence branch is unreadable mechanically; the criterion binds the queue, not the fix (the claim's counter owns that). — `round-51-verifier-spotcheck.md` section 6 item 2 (routed 2 of 4), `round-52-verifier-spotcheck.md` section 6 item 4.

95. **A polarity check covers every script a lane quotes in.** `tools/inference-ground.py` compared polarity only through Latin word stems, so a bullet quoting a CJK phrase from a span that affirms it while asserting `不要求`/`没有`/`未要求` passed `GROUND: PASS` (round-52 closure section 6 item 5; W2 `R52W2ExecInfRegression`). Round 53 adds a clause-bounded six-character CJK negator window (W1 `R53ExecCjkPolarity`). Check: `python3 corpus/evidence/round53/cjk-polarity-check.py` → `CJK_POLARITY=6/6` (four reversals flagged `INF_POLARITY_FLIP`, the positive control and a far-negator case kept). Shown able to fail (ran): the same check with the round-52 tool (`git show 5b550133:tools/inference-ground.py`) prints `CJK_POLARITY=2/6`. Named limits: a Latin negator on a CJK-quoted phrase, and a Japanese verb-final negation that rewrites the predicate, still pass (both measured by the seat). — `corpus/lessons/round-53.md` `## Spot-check intake` item 5.

96. **A counter refuses a sample size that makes its legs vacuous, and a PDF quote is checked against an independent extraction.** The frozen round-53 C1 counter printed `LEGS=8/8 C1=PASS` at `--per-leg 0` because each generated leg is `all()` over no packages (W1 `R53SentCounters` H1); and a `pdftotext -layout` sidecar of a two-column PDF pairs the columns on one line for half the JMLA body (W1 `R53ExecPdfForm`), so a one-line quote can be a glue the PDF never prints. Check: the next frozen counter exits 2 on a per-leg count below 1 and prints its case count; every quote on a PDF capture occurs, whitespace removed, in an independent extraction — `uv run --quiet --with pypdf python corpus/evidence/round53/pdf-crosscheck.py` → `PDF_QUOTES=49 NOT_IN_INDEPENDENT=0`. Shown able to fail (ran): `python3 corpus/evidence/round53/c1-count.py --per-leg 0 --seed 5` → `LEGS=8/8` with no case line; of the 85 JMLA `.txt` lines that carry two column blocks (split at 5+ spaces), 78 are absent as a whole line from the pypdf text while each block is present, so a quote spanning both blocks would fail the check. — `corpus/lessons/round-53.md` `## Mistakes` row 4; QUALITY 81.

97. **A binary capture's text form is a defined, named reading — a tool and a written rule — never a raw decode, and an anchor offset names the form it indexes.** S101's Registry row anchors six quotes in "UTF-16LE text of the raw `.doc` capture" (`corpus/SOURCES.md:111`; the same six in `corpus/lessons/round-49.md:95-100`), and that form is the container's bytes decoded as text: `6dc68fd6b32ce9c8dfcebce8.raw` gives 64,512 characters with 263 U+FFFD and 18,242 control characters, and it is not the document (the `.txt` sidecar holds none of the six phrases — `find` → −1). The defined OLE form (`tools/capture-text.py`; docstring rule: CFB sector chains, FIB wIdent/nFib, Clx piece table, cp1252/UTF-16LE pieces, main story CP 0..ccpText, field results only) gives 27,012 characters, 0 U+FFFD, 0 control characters, and the same six phrases locate exactly once at 11,972 / 12,007 / 12,963 / 12,795 / 14,049 / 25,123 against stated 11,170 / 11,205 / 11,993 / 12,161 / 13,247 / 34,374 — drift +802, +802, +970, +634, +802, −9,251, so no constant repairs an old anchor (all ran). Check: for every `char N` an entry, Registry row or lesson states for a binary capture, the stated form is a named tool+rule and `python3 tools/capture-text.py <raw> --locate '<quote>'` prints `LOCATED count=1 offset=N` with N equal to the stated `char N`; a form that decodes the file's bytes fails the check even when its number reproduces in that decode. Shown able to fail (ran): the S101 row and round-49 rows give 0/6 matches, and `corpus/evidence/round54/build-spans.py:107-113` still returns that decode for a non-zip raw, so a span built from an OLE `.doc` would index it. Named limits: a manual per-anchor check, not a counter; it binds anchors written after the criterion (the six S101 anchors stay wrong until the correction rows land, and a bound row's `anchor` cell is the counter-checked instance, not a lesson table). — `corpus/lessons/round-54.md` `## Mistakes` row 2 (anchor in an undefined form); QUALITY 87.

98. **A frozen capability counter judges real inputs against an oracle computed at counting time from the same bytes by an independent reader, and refuses a tool that delegates to that reader.** The round-54 C1 counter copies the five hash-pinned `.raw` captures to `real/*.doc` (a digest mismatch is `ENV_CHANGED` exit 2), renders them with `soffice --headless --convert-to "txt:Text (encoded):UTF8"` under a private profile at counting time (`corpus/evidence/round54/c1-count.py:244-256`), then holds the tool's whitespace-free text form to every oracle line (≥ 8 non-space characters), a 0.90-1.10 length ratio and two pinned quotes located exactly once in its own stdout (`:259-278`); every tool invocation goes through `hook.py` (`:114`), which aborts with `AUDIT_FORBIDDEN <event>` and exit 97 on `subprocess.Popen`, `os.system`, `os.exec*`, `os.posix_spawn`, `os.spawn*`, `os.fork`, `os.forkpty`, `pty.spawn`, `socket.connect` or `socket.bind` (`:70-76`). Check: `python3 corpus/evidence/round54/c1-count.py --tool <candidate> --seed N --per-leg 2` — a candidate that renders with LibreOffice fails every hooked leg while the landed tool passes REAL. Shown able to fail (ran): a forge that shells to `soffice` and prints its text (sha256 `9c8def9b…`) gives `GEN=FAIL ggen0.doc rc=97 b'AUDIT_FORBIDDEN subprocess.Popen\n'`, `REAL=FAIL … rc=97`, `LEGS=0/6 C1=FAIL` exit 1, and the SHELL control's receipt says the same (`corpus/evidence/round54/controls/c1-controls.txt`); the landed tool at `--seed 97 --per-leg 2` gives `REAL=PASS 5 captures`, `LEGS=6/6 C1=PASS` exit 0. Named limits: the hook covers Python audit events in the tool's own process, not a compiled extension that renders without one; the REGRESS leg re-runs the round-52 counter, which invokes the tool directly (`corpus/evidence/round52/c1-count.py:215`), so a delegating tool can pass REGRESS and still fail the five hooked legs; the oracle is one LibreOffice version, so an environment change fails REAL rather than skipping it (QUALITY 96's sample guard is what keeps a run from being vacuous). — round-53 closure §6 item 6 (frozen-counter forgeability, RW-1); QUALITY 90. Named limit, found in round: the frozen counter left each generated document's HTML source beside it and pinned REAL by digest, so W1 `R54CritForgeC1` passed it 6/6 with a tool that reads the sibling HTML and returns canned exports; the post-freeze supplement (`corpus/evidence/round54/c1-supplement.py`: ISOLATED, RESAVE, HELDOUT) copies every document alone under a random name and round-trips the captures to new bytes, and the rebuilt forge scores 0/3 there (`corpus/evidence/round54/controls/build-c1-forge.py`; claims-erratum E1). An oracle also has to be out of the tool's reach, not only independent of it.

99. **A wave handoff is reported as dispatched only with the dispatcher's marker (`<round>/<wave>.ready.dispatched`) or the wave's results file; otherwise it is reported as not dispatched, whatever the dispatch file, spec or seat roster says.** Round 53 wrote `.ufo/waves/round-53/w2.ready` (a readiness record naming `w2-dispatch.json`) and filed "W2: 43 seats dispatched" (`/home/vgpnk/Projects/shokunin/.ufo/reports/round-53/chousa.md:14`), while `w2.ready.dispatched` and `w2-results.json` do not exist (`ls` → both absent, ran) and the orchestrator's run file records "w2.ready orphaned - L1 exited before dispatcher marked wave" (`/home/vgpnk/Projects/shokunin/.scratch/goal-20261026-hyaku-run9.md:126`). Check: for each wave a report calls dispatched, print the marker and the results file — round-53 W1: `w1.ready.dispatched` exists (timestamp + 49 ids) and `w1-results.json` holds 49 seats / 49 results; round-53 W2: marker and results file both absent — and the report sentence must match what was printed. Shown able to fail (ran): the round-53 report line above against the two absent files. Named limits: a `<wave>.ready` record, a `<wave>-dispatch.json`, a `<wave>.ready.partial` roster or a live seat are not dispatch evidence (at draft time round-54 W1 had `w1.ready`, a 43-id `w1.ready.partial` and no marker, so its report must not call W1 dispatched unless the marker or `w1-results.json` exists at filing); the criterion checks the label, not whether the seats then ran well. — `corpus/lessons/round-54.md` `## Mistakes` row 1 (unverified handoff described as pending); round-53 closure §6 item 2; QUALITY 94.

100. **A held registry row's `used-by` is updated old→new when an admitted entry cites it, and the counter fails until it is.** S101's row carries `used-by` = `corpus/knowledge/citation-count-semantics-r37.md` (`corpus/SOURCES.md:111`), and the round-54 C2 controls show mechanical binding leaves it stale: the TOOLED control prints `BOUND=3/3 (min 2) … HELD_CITED=- HELD_BAD=1 … REF_ID_UNBOUND=3` (`corpus/evidence/round54/controls/c2-controls.txt`) with entries that cite the HIT `.doc`. Check: `python3 corpus/evidence/round54/c2-count.py [--lane-only]` prints `HELD_CITED=<id> HELD_BAD=0` only when every entry whose text carries `source: S101 — <HIT url>` is also named in the row's `used-by` cell, and the lesson records the cell's change old→new. Shown able to fail (ran): in a scratch root holding the lane's `SOURCES.md` and one such entry, `--lane-only` prints `HELD_CITED=- HELD_BAD=1 REF_ID_UNBOUND=2 C2=FAIL`; adding the entry to the cell prints `HELD_CITED=S101 HELD_BAD=0 REF_ID_UNBOUND=0`; with the cell updated but the line mis-numbered `source: S090 — <url>`, `HELD_CITED=- HELD_BAD=1 REF_ID_UNBOUND=2`. Named limits: `HELD_BAD` counts held ids cited without the update, not the lesson's sentence; an entry naming the HIT URL in prose but not on a `source:` line is not a held citation; the counter reads the row from `--root`, so a scratch copy can be probed without touching the lane registry. — round-53 closure §6 item 6 (a counter a mechanical rewrite cannot satisfy); QUALITY 92.

101. **A criterion's own numbers are re-derived before filing, each count names the set it excludes, and a mechanism claim names the events it covers — round 55 corrects 97 and 98 by appended errata, not by rewriting them.** Round-54 wave 2 re-ran the two criteria: in 97 the third and fourth located offsets are swapped (the tool prints 12795 for the phrase anchored at 11993 and 12963 for the one at 12161), so five of six anchors drift by the same +802 and only the sixth (−9251) breaks the pattern — no single constant repairs all six, but one repairs five; the "18,242" count holds only with tab, LF and CR excluded (18,451 code points below 0x20 in all), and the defined form's "0 control characters" is 469 LFs and nothing else (`.ufo/waves/round-54/w2/R54W2ReviewQuality.md` F1/F2, `R54W2CritMistakes.md` row 2). In 98, a ctypes `system()` call spawns a process under the round-54 hook with rc 0 (`R54W2CritC1Verdict.md`), so "refuses a tool that delegates" holds only for the audit events the hook lists, and the SHELL control scored 1/6, not the forge's 0/6 (`controls/c1-controls.txt`). Check: `python3 corpus/evidence/round55/c3-count.py` prints `E05 OK`, `E06 OK`, `E07 OK`, `E09 OK` and `E10 OK` only when the `SCORECARD.md` "Round 55 statement errata" lines carry the observations the counter re-derives from BASE bytes and its own ctypes probe. Shown able to fail (ran): the RESTATE control (each statement's own number as the observation) prints `WRONG` for all five and `ERRATA=0/11` (`corpus/evidence/round55/controls/c3-controls.txt`). Named limit: the counter checks the observation string, not the reading paragraph beside it.

102. **A capability counter keeps every expected value out of the judged tool's reach — not on disk, not in argv or environment — and its hook audits reads as well as spawns.** Round 54's supplement wrote its oracle exports into the work tree before running the tool, two directories above each "isolated" document, and an echo tool that never opens the `.doc` scored `SUPPLEMENT_LEGS=3/3`; the frozen round-54 REAL leg left its oracle under the inherited `TMPDIR` (`.ufo/waves/round-54/w2/R54W2SentFinal.md` F1/F2; erratum E11). The round-55 C1 counter picks held-out quotes at counting time, keeps the expected offsets in its own memory, deletes each generation tree before the run, and ends the run (exit 97) on an `open`, `os.listdir` or `os.scandir` outside the run directory, the hook file, the tool's directory, the lane's `tools/` and the Python installation, and on `ctypes.dlopen` (`corpus/evidence/round55/c1-count.py` HOOK). Check: `python3 corpus/evidence/round55/c1-count.py --tool <candidate>`; a tool that reads the work tree, `/proc` or a sibling run dies with `AUDIT_FORBIDDEN open …`. Shown able to fail (ran): the DELEGATE control (LibreOffice through ctypes) gives `AUDIT_FORBIDDEN ctypes.dlopen`, `LEGS=0/4` (`corpus/evidence/round55/controls/c1-controls.txt`); W1 `R55CritForgeEcho` (refusal-only, 1/4) and `R55CritForgeReader` (an approximate OLE reader, 0/4). Named limits (W1 `R55CritForgeHook`): the hook audits listed events, so `os.open` with `dir_fd`, a `chdir` then relative open, and unlisted events (`os.symlink`, `os.kill`) are not stopped by it; the counter's exact-slice judgement, not the hook, is what fails a delegating or approximate reader.

103. **A check's denominator is the full expected set: zero rows, a skipped id, an empty quote or a missing input tree is a failure, never a vacuous pass.** Round 54's `pdf-crosscheck.py` counted only rows whose id it recognised and passed a header-only manifest (`PDF_QUOTES=0 … rc=0`) and an empty quote; its `considerthese-ledger-check.py` passed with no `considerthese/` tree, read any absolute path the ledger named, read a 512 MiB file whole and ran a ledger regex without bound (`R54W2SentFinal.md` F5/F6). Check: `uv run --with pypdf python corpus/evidence/round55/pdf-crosscheck.py` (21 S123 rows required, PDF pinned by sha256) and `python3 corpus/evidence/round55/considerthese-ledger-check.py --root .` (pointer inside the root, 1 MiB cap before reading, regex cells over 128 characters or with nested quantifiers refused, zero proposals exit 1). Shown able to fail (ran): renamed id, empty quote, header-only and tab-in-quote manifests each exit 1 (`corpus/evidence/round55/pdf-crosscheck.txt`); an absolute pointer, `(a+)+$`, a 512 MiB target (peak RSS 15,848 kB) and a missing tree each exit 1 where the round-54 checker exits 0 on two of them (`corpus/evidence/round55/considerthese-ledger-check.txt`).

104. **A round's report is filed only after every wave it dispatched has settled, shown by that wave's committed results file.** Round 54 filed at 23:50:07 while W2 ran; W2 was killed at the orchestrator's exit and reached the lane only through a salvage commit at 00:22:58 (lesson round 55 `## Mistakes` row 1). Check: `python3 corpus/evidence/round55/wave-settled-check.py --round N --before-filing` before the report commit and without the flag after it; every `<wave>.ready.dispatched` needs a `<wave>-results.json` committed at or before the report (a first-line ` ABANDONED:` marker with no results counts as never run). Shown able to fail (ran): round 54 → `UNSETTLED w2 results=2026-10-27T00:22:58-03:00 after report=2026-10-26T23:50:07-03:00`, exit 1; round 52 → `SETTLED=2`, exit 0 (`corpus/evidence/round55/wave-settled-check.txt`).

105. **A helper that writes temporary or generated files refuses an output directory inside the lane and takes its temp root from `TMPDIR`.** Round 54's `controls/build-c1-forge.py` created its temp tree inside the caller's output argument, so a SIGKILL left four pinned campaign captures and a LibreOffice profile as untracked files in the directory named (`R54W2SentFinal.md` F3). Check: each round-55 controls builder exits 2 with `usage: OUTDIR must lie outside the lane` for an in-lane OUTDIR and writes nothing. Shown able to fail (ran): `python3 corpus/evidence/round55/controls/build-c{1,2,3}-controls.py corpus/evidence/round55/controls/tmpout` → exit 2 ×3, no directory created; the round-54 forge builder has no such guard (named, not edited: it is round-54 evidence).

## Round-56 additions (appended 2026-10-27; criteria 1–105 unchanged)

106. **A counter's kill rule cannot be satisfied by a tool that alternates its behaviour or counts its calls.** Round 56's first driver draft took any verdict-vector difference between a gate and its mutant as a kill; a tool that corrupts the first `capture_sha256` cell on odd calls only produces M3's own marker (`S901 capture_sha256`) under the gate and a pass under the M3 gate on the next call, so the clause is "killed" by a tool that never writes a bad digest (round-56 wave `R56DraftMistakes` §1(b), scratch parity-aligned run: odd call `GENOLE=FAIL S901 capture_sha256`, even call under M3 `LEGS=4/4`). The L1's own `mGmG` seed-56 instance of that kill is disclosed in `corpus/evidence/round56/claims.md` and is in no committed receipt. Check: `python3 corpus/evidence/round56/c1-count.py` counts a kill only with the clause's own reason in G's runs and a pass in three mutant runs at BOTH seeds, in a random order (a call-counting forge matches one order in 400); `python3 corpus/evidence/round56/controls/build-c1-junk.py OUT && python3 corpus/evidence/round56/c1-count.py --battery OUT` prints `KILLED=1/9` with the FLIP forge in the battery (`corpus/evidence/round56/controls/c1-controls.txt`). Shown able to fail: the parity-aligned run above.
107. **A frozen mutant set holds no equivalent mutant; a survivor is classified before the target is fixed.** The first M9 (WIN_NL) dropped one of the window filter's two newline guards and could not differ from the gate: with the second edit removed the counter prints `MUTANT M9 WIN_NL SURVIVED`, `KILLED=8/9`, `C1=FAIL` (wave `R56DraftMistakes` §1(a), seed 7, 65 runs). Check: rebuild the set with each mutant's first edit only and run the counter; a survivor the landed builder cannot kill is a mutant-set defect, never a data result. Shown able to fail: that run.
108. **A report's measurement citation names the revision its committed receipt header names.** Round 55's report said C2/C3 were "measured at `29cfb12a`" and a C2 "re-run at `53f1ce6b`"; the receipts' first lines name `5a35ebd6` and no receipt names `53f1ce6b` (closure D3; `corpus/lessons/round-55.md` `## Corrections`). Check: for every `measured at` / `re-run at` revision in a report, a receipt under the round's evidence whose first line carries that revision; wave `R56DraftMistakes` §2 ran it: round-55 report `CITES=4 UNNAMED=3`, exit 1; a copy citing `5a35ebd6` `UNNAMED=0`, exit 0.
109. **A row's table is read from the page layout, not from a multi-column text form's line order.** The round-56 entry as first committed (`99eff0ec`) placed the journal's 灰色文献 row in `表 10` because the cache `.txt` prints the right column's 表 10 title on the line above it; the row belongs to `表7    药品临床综合评价的信息来源情况` (char 20520). Check: `pdftotext <capture>.pdf OUT && python3 -c` printing the offsets of the table titles and the row in OUT — round-56 L1 run: `表7 13013 < 灰色文献 13591 < 表8 13653 < 表 10 14566` (pdftotext 26.08.0); an attribution whose table title is not the nearest preceding title in that order fails. Shown able to fail: the `99eff0ec` entry's `表 10` attribution (wave `R56GroundJournal` F1, `R56DraftGate` F1, `R56CritCurrency`).
110. **A wave item's test recipe is dry-run by the L1 before dispatch.** Round 56's spec told seats to copy the lane with `git archive` and run the gate or the driver on the copy; the copy has no history, the gate's REGRESS leg runs `git show` at its pinned base, and every run prints `ENV_CHANGED` (exit 2), so an attack seat's measurement is void (`R56CritC1Forge` printed `('ENV', 2)` and measured nothing). Check: before writing a `.ready`, run each distinct recipe the items name once (copy, then the counter on the copy) and require a non-`ENV_CHANGED` baseline. Shown able to fail: an archive copy's gate run → `ENV_CHANGED git show corpus/evidence/round54/quotes.tsv`, exit 2, while a `git clone --shared` copy ran the counter (wave `R56DraftMistakes` §6 and §1, before the cache deletion recorded in `corpus/lessons/round-56.md`).

## Round-57 additions (appended 2026-10-27; criteria 1–110 unchanged)

111. **A tool that writes derived paths resolves its repo root from its own file's location and refuses a root that is not that file's git toplevel.** Round 57's re-fetch tool derived `LANE = HERE.parents[1]` from `__file__` on its first run and wrote 86 capture files plus the fetch record into the fleet repo; the tool carried no root guard, so nothing could fire, and the defect was caught by the counter's empty-record shape, not by the tool (`corpus/lessons/round-57.md` `## Mistakes` row 1). The landed tool resolves `LANE = HERE.parent` and `root_guard()` exits 2 unless `git -C <lane> rev-parse --show-toplevel` equals the lane. Check: `python3 tools/capture-fetch.py --status` prints one line `root=<lane> record=<lane>/corpus/evidence/round57/refetch.tsv store=<lane>/corpus/captures` and exits 2 on any other root (shown able to fail: the seat's misrooted copy prints no root line and exits 0, `R57W1ScribeQuality.md` §111).

112. **A capture byte is evidence only together with its fetch-record row; the store and the record are judged as one set, in both directions.** The wrap-up commit `b022b13` added 14 capture files with no record, producing record-less orphans (`53a92273…`, `d473754a…`, `d8b4f8f8…`); the converse defect also fired — S105's record-less bytes stranded the triple as MISSING until the L1 deleted them, and two orphans later acquired all-failed records while the store holds readable PDFs (`corpus/lessons/round-57.md` row 2). Check: `python3 tools/store-record-audit.py` — classes `ORPHAN` (store bytes with no successful row), `RECORD_ONLY` (successful row with no bytes), `BYTES_STALE` (bytes ≠ last success), `STORE_BUT_RECORD_DENIES` (bytes with only failed rows); exit 1 on any non-empty class. Shown able to fail (ran): the live tree prints `ORPHAN=3` + `STORE_BUT_RECORD_DENIES=2`, `STORE_RECORD_AUDIT=FAIL`, exit 1 (the hnysfww URLs' 3-attempt caps are exhausted; the classes stand open with that reason).

113. **A commit that adds capture bytes adds their attempt rows in the same commit, and a commit that adds a successful row adds its bytes.** `b022b13` added 14 captures with zero record rows; the two later fetch commits pair 43/43 and 4/4. The pairing is what makes a counted freshness claim checkable without reconstructing history (`REPRODUCED` rests on "the last successful attempt's `raw_sha256` equals these bytes"). Check: `python3 tools/store-record-audit.py` over `git show <rev>:…` per commit (the audit's classes applied at each capture-touching revision); at round time also `--worktree` before committing in-flight fetches (shown able to fail: `b022b13 → ADDED_WITHOUT_SUCCESS_ROW=14`).
114. **A record-backed provenance counter does not treat its own writable success row as proof that a fetch occurred.** W2's C3 forge (`R57W2CritC3Forge.md` A1a/A1b) adds a self-authored success row for a new `(id,url)`, copies held capture bytes under that URL key, and reaches `C3=PASS` without fetching the URL; the frozen counter checks record-vs-bytes consistency but not record authenticity (`corpus/lessons/round-57.md` Mistakes row 6). Check: replay the two A1 fixtures; the counter must either reject the forged provenance or label it attestation-only, never claim a real fetch. Shown able to fail (ran): both A1a same-id/new-URL and A1b new-id/new-URL print `C3=PASS`, exit 0; the live five bound `(id,url)` pairs are independently re-derived as genuine in `corpus/evidence/round57/sidecar-audits.md` §4.

## Round-58 additions (appended 2026-10-27; criteria 1–114 unchanged)

115. **A frozen counter must demonstrate its positive verdict path before it binds round data; a deny-only control set cannot prove that the target is reachable.** Round 58's C1 counter had only REFUSEALL and pinned-base negative controls. A scratch builder satisfying all 11 per-leg conditions still emitted `C1=FAIL` because refusal rows were formatted `=pass(refused)` while the aggregate searched for `=PASS` (`corpus/lessons/round-58.md` `## Mistakes`; W1 `R58ScribeMistakeMine.md` lines 57–83 and `R58ReviewFrozenClaims.md` lines 25–37). Check: before a future freeze, run the counter on a positive builder that satisfies each declared leg and require its exact target token and success exit; if the positive control cannot reach the token, do not dispatch or change the claim post-data. Shown able to fail (ran): the R58 positive-leg probe prints 11 passing leg lines but `REFUSE=0/7`, `C1=FAIL`, exit 1.

## Round-59 addition (appended 2026-10-27; criteria 1–115 unchanged)

116. **A round's claims freeze is a present, nonempty, pre-dispatch artifact.** Round 59's ready context named `corpus/evidence/round59/claims.md`, but the file was absent before data and no frozen predicate existed to score (`corpus/lessons/round-59.md`, `## Mistakes` row 1). Check before writing `<wave>.ready`: require the round claims artifact to be nonempty and record its full revision in the dispatch context; refuse ready if either prerequisite fails. Shown able to fail: the observed pre-data presence check returned `CLAIMS_EXISTS=False`; a reconstructed after-data claims file cannot satisfy this criterion.

117. **A gate verdict is derived from structured leg states, never by searching untrusted child output for the target token.** The round-58 C1 refusal leg embeds builder stderr in its rendered text; W1 `R59Executor09.md` showed a builder with all seven hazard legs failing can inject `=PASS` into stderr and reach `C1=PASS` on the frozen counter (`corpus/lessons/round-59.md` `## Mistakes` row 2). Check: inject the exact target token into a failing leg's stderr and require the verdict to remain FAIL; separately require the positive builder's structured statuses to pass. Shown able to fail: the untrusted-stderr forge reaches `C1=PASS`, exit 0, with all seven hazard legs failing (W1 `R59Executor09.md`).

118. **The validated spec remains immutable after rendering; the committed spec and dispatch payload stay bound to the same digest and item bodies.** In round 59 I rewrote the persisted spec after generating dispatch/ready; `stat` showed `w1-spec.json` at 15:14:46 -0300 after `w1-dispatch.json` at 15:12:11 and `w1.ready` at 15:12:15, and current body comparison reports 0/66 equal (`corpus/lessons/round-59.md`, `## Mistakes` row 3). Check: preserve the exact validated spec bytes and digest before writing ready, then compare against dispatch before filing; any post-ready spec mutation fails. Shown able to fail: the current spec/dispatch mismatch is observable on the persisted artifacts; the original spec bytes are not reconstructed from the later file.

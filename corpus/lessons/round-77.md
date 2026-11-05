# Round 77 — the outer battery stops being passable by an invocation counter

Base: `6defa58dbdc40856f4e7dd24df98dc7ebd3459c0`; prefreeze instruments and controls
`e6fcdc4770c2fa73e5ccda99445c4311128d7e0d`; claims freeze `a9530782578723de1364e0a3a47effcde8c85c23`.
Two claims in `corpus/evidence/round77/claims.md`: C1 operability (lowest scored non-retired axis,
3/10, held) and C2 calibration. The r76 closure was admitted; this round answers
`corpus/lessons/round-76-verifier-spotcheck.md` routed defects 1, 3 and 4.

## Gate

- Admit S190, own-work B, scoped to the r76 spot-check's routed defect 1 — the outer battery's
  fixed subject order. `corpus/lessons/round-76-verifier-spotcheck.md` at
  `6defa58dbdc40856f4e7dd24df98dc7ebd3459c0`, lines 150–155, quote on line 150. Opened
  2026-11-04. Located quote: "Outer batteries score exit codes in a fixed subject order." (10
  words). Grounds C1's target: it is the closure record that names the defect, not independent
  truth that the successor closes it — the committed receipts are.
- Admit S191, own-work B, scoped to routed defect 3 — the false sentence in the frozen r76 claims
  file. Same revision and file, lines 160–164, quote on lines 163–164. Opened 2026-11-04. Located
  quote: "supersede it with an append-only correction entry naming the superseded text" (11
  words). Grounds C2's target. (The first draft said 12 words and line 163; `R77ScribeA` counted 11
  with `wc -w` and the wrap, and the count is corrected here before landing.)
- Reject S192, own-work C, scoped to this round's frozen claims file as a source row.
  `corpus/evidence/round77/claims.md` at `a9530782578723de1364e0a3a47effcde8c85c23`, line 1. Opened 2026-11-04. Located quote:
  "# Round 77 frozen claims — the outer battery's order and content legs" (a heading, contiguous
  on that line). REJECTED: a claims file is the lane's own declaration of its predicate, not
  evidence that the predicate holds — the r76 S189 precedent — and a row here would let a later
  round cite its own declaration as a source. Flip: admit scoped to the claim text if an admitted
  knowledge entry ever rests on a declaration as the only record of a prediction.
- New registry rows S190/S191 mined, used-by this lesson; S192 rejected, used-by `—`. Existing
  status/recheck/used-by cells unchanged. No URL opened or fetched: all three are revision-pinned
  committed paths.
- Non-author spot-check requested: two admits and one reject above. Dispatched wave seats are
  author-lane evidence, not independent admission or promotion reviewers.
- Assimilation: none — no package bytes adopted, so no id-collision check is run.
  `considerthese/` was opened; no proposal adopted this round (claim cap), recorded rather than
  implemented. No operator-authored consideration was edited.

## Mistakes

| class | evidence | captured-by | fix |
|---|---|---|---|
| a probe wrote its state file into the lane when invoked in place | the first C1 before-run passed `corpus/evidence/round77/forgers/forge-order-matrix.py` directly as `--matrix`; the oracle keeps its invocation count beside itself, so `corpus/evidence/round77/forgers/forge-order-matrix.state` appeared in the lane tree (observed by the L1 at 18:09 and removed before any commit; not receipted) | no rule in the round-76 battery forbade it — the lane's "no write at run time" discipline was held by the L1, not by the instrument | both oracles now call `refuse_inside_worktree()` and exit 2 when their own directory resolves inside a git worktree; the battery copies every oracle into its `--work` directory first. Shown able to fail: `python3 corpus/evidence/round77/forgers/forge-order-matrix.py --counter x --work y` → exit 2, `refusing to run inside the git worktree …`, and no `.state` file is created |
| a successor instrument named a subject root that did not exist | the first predicate run of `matrix-battery-v4.py` printed `matrix-battery-v4: missing subject …/corpus/evidence/round77/forgers/forge-constant-pass.py`, exit 2, because the eleven round-76 forgers had been copied by reference into the new directory's path instead of being referenced where they live | the battery's own missing-subject guard (exit 2, no scoring) — nothing else would have caught it before the freeze | the eleven subjects are referenced from `corpus/evidence/round76/forgers/` byte-identically and the guard is retained; receipt `controls/mutant-missing-subject.txt` reproduces the refusal on a scratch copy |

## Instrument limits (recorded, not amended after scoring)

- **The order leg is the load-bearing closure; the content leg is a shape requirement.** Measured:
  `--no-permute` turns the predicate into `BATTERY=FAIL` (`controls/twin-no-permute.txt`) because
  the block-position oracle then reaches full marks; `--no-content` leaves the predicate passing
  (`controls/twin-no-content.txt`) because a blind script cannot survive the permutation anyway.
  A matrix that prints the exact twelve-line contract table with fabricated `PASS` cells satisfies
  the content leg; what refuses it is the per-run permutation. A matrix that reads the battery's
  own source through `/proc/<ppid>/cmdline` can recover the permutation and the oracle set; that
  channel is named, not closed, and is the wave's critic target.
- **`oracle=REJECTED` is a three-subject statement.** The two round-76-style oracles are refused
  partly by the run-major iteration (their "first four PASS" script cannot satisfy both runs of
  both positives), and the block-position oracle is refused by the permutation alone. The leg does
  not prove that an arbitrary forged matrix is refused, and `forge-order-matrix.py` reaching the
  round-76 battery's target lines (`controls/before-oracle-v3.txt`) is what the round closes.
- **C2's counter is lexical.** `c3-count.py` proves presence, position, the quoted superseded
  clause, the corrected phrase and an append-only numstat — not that the corrected sentence is
  true and not that no other sentence in the frozen file is false.
- **The round-76 matrix is unchanged.** C1 supersedes the battery, not the matrix: the twelve-case
  contract, its salts and its shuffle are the r76 bytes (`b79d6441…913f`), so this round adds no
  case coverage and cannot claim one.

## Boundaries

No network, no package adoption, no host question presumed answered, no sibling repo or fleet repo
writes other than the round report and L0 appends. Frozen instruments and receipts are not amended
after any seat scores them; a post-freeze finding is reported as a limit, never as a repaired
predicate.
| a control receipt named a probe digest no committed object carries | `corpus/evidence/round77/controls/before-oracle-v3.txt` lines 4 and 7 name the oracle sha256 `9bb74e2a…248b1`; the committed `corpus/evidence/round77/forgers/forge-order-matrix.py` is `e7a12850…`, because the worktree guard was added to the oracle after that receipt was taken (`R77ScribeA` swept every object in the lane's history: one positive hit for `e7a12850…`, zero for `9bb74e2a…`; `digest-sweep.txt`) | no criterion — QUALITY 125 covers claims files only, and no rule bound a control receipt's probe digest to the committed probe | the frozen receipt is not amended; a separate re-measurement on the committed bytes is added as `controls/before-oracle-v3-committed-bytes.txt`, and the gap is recorded here. The guard adds only a refusal path, so the pre-guard run and the committed bytes differ in no scored behaviour — which the second receipt demonstrates rather than asserts |
- **The battery's `--work` contract is defective in two ways the round did not repair.** `R77SentinelA`
  measures: a `--work` that cannot be written exits 1 with a traceback instead of the documented
  could-not-evaluate 2 (S2), and the battery's `finally: shutil.rmtree(work)` deletes the caller's
  `--work` directory itself, so a caller that passes a directory holding other content loses it (S1).
  The predicate never passes such a directory, so no scored run was harmed; the defect is recorded and
  carried to QUALITY 142 rather than repaired after scoring.
- **`c3-count.py` has no lane-root guard.** It reads any `--lane` path it is given and writes nothing
  (`R77SentinelA` B3a/B3b: zero write syscalls, no `rev-parse` check). Read-only, so the exposure is a
  mis-resolution, not a write; the successor counter should resolve its root from its own file, as
  `tools/capture-fetch.py` does (QUALITY 111).
- **The seed's secrecy is an inference, not a quoted property.** `R77ScoutA` opened the installed
  `/usr/lib/python3.14/random.py` (`cf8e72f8…`) and `secrets.py` (`27700057…`): the shipped text says
  "cryptographically strong" and never "unpredictable", and neither file mentions child processes or
  same-uid visibility. What the round can state is narrower than the claim it supports: the seed is
  drawn from the OS-backed `SystemRandom` path per run and is never passed to the child (no argv, no
  environment key, seed digest only), so a blind oracle cannot recover it. A child that read the
  battery's memory would be outside these quotes. No `SOURCES.md` row was added for the two stdlib
  files: nothing admitted this round cites them, and a row without a citer is curation debt, not
  knowledge.
- **Three channels reach the predicate line without scoring anything (`R77CriticA`, exit 0 each).**
  (A1) `salted_copy()` appends `# salt <hex>` as a suffix, so stripping the trailing line recovers the
  lane file byte-for-byte and a content hash classifies every subject — 22 forgers at `11/12` and four
  positives at `12/12`, `rcpt-a1.txt`. (A2) `/proc/<ppid>/cmdline` names the battery, whose `CONTRACT`
  constant is the twelve expected cells — `rcpt-a2.txt`. (A7) the printed `ORDER` digest is
  `sha256` of the *permuted names*, not of the seed, so the permutation is recoverable by enumeration
  of 13! inside the battery's own 300 s cap (11.8 s and 59.1 s measured with an OpenMP SHA-256
  enumerator) and the matrix then answers by position — `rcpt-a7.txt`, exact predicate line, exit 0.
  What the battery does close is blind invocation-count scripting: `rcpt-a3.txt` is
  `BATTERY=FAIL forgers_rejected=7/11 positive=0/2`. The claim's first clause holds; its supporting
  sentences "the seed digest is printed, the permutation is not" and "a matrix that reads the battery's
  own source can recover the order" are falsified — the order leaks through the digest, not the source.
  Frozen bytes are not amended; the corrections are carried to QUALITY 143.
- **A child can append the predicate line to the judge's receipt after the judge exits 1.** A detached
  helper that closes the inherited pipes appends 26 copies of the exact predicate line two seconds
  after the battery's own `BATTERY=FAIL` line (`R77CriticA` A5d, `rcpt-a5d.txt`); a verifier that reads
  `tail -1` or greps for the predicate is fooled while the exit code is 1. In-band writes are destroyed
  by the judge's later writes (A5–A5c); `ptrace` is closed (`ptrace_scope=1`, A6).
## Wave integration

One v1 wave, 12 seats (3 executor, 1 scout, 1 scribe, 1 connector, 2 reviewer, 2 critic, 1
mutation-tester, 1 sentinel = 5 attack seats, 42%), L1 holding the canonical planner seat; no residual
call; no dead seat replaced. Five reports are retained: `R77ConnectorA` (sibling-overlap scan: chousa
QUALITY 139 is the only criterion that names the outer-battery boundary; `kaidoku` rows 71/95 and
`souji` Q51 are stronger as general anti-vacuity rules, and none is absorbed), `R77CriticA` (the three
forging channels above), `R77ScoutA` (the stdlib readings), `R77ScribeA` (the Gate/Mistakes drafts, the
quote-count correction and the receipt-digest slip), `R77SentinelA` (the boundary audit, the `--work`
defects, the state-file containment). Seven seats settled with no retained report: `w1-results.json`
records 12 entries with empty `output` and a note that the orchestrator kernel restarted mid-wave and
seat outputs went to the orchestrator session. That is the r76 routed defect 5 recurring — committing
the results file did not retain per-seat terminal records — and it is recorded, not glossed.

## Self-evaluation

Both frozen predicates hold on the committed bytes. The round's own slips are mined above (a probe
writing into the lane; a control receipt naming a digest no committed object carries; a quote count
off by one). The larger honesty finding is the critic's: the claim's supporting sentences were too
strong, and the round records that rather than narrowing the target after landing. What the round did
not do: close the content channels (carried as QUALITY 143), cure the settlement attestation, or add
case coverage to the matrix.

## Erratum — round 78

erratum: round-77.md:73 — the `## Mistakes` row for the control-receipt digest slip (class
"a control receipt named a probe digest no committed object carries") is stranded below
`## Boundaries` instead of inside the `## Mistakes` table at lines 40–43, so it renders as
literal text and the mined mistake is easy to miss. Routed by
`corpus/lessons/round-77-verifier-spotcheck.md` routed defect 4. The filed bytes above are not
rewritten (append-only): this line is the correction entry that names the stranded row, and
`python3 -B corpus/evidence/round78/selfcheck.py --lane .` check S3 re-derives its position.

erratum: round-77.md:73 digest=7f2d54a7eb33df54 — round-79 successor: the stranded row's exact bytes are as asserted, so this erratum is bound to the line it names and not to its position alone; `python3 -B corpus/evidence/round79/selfcheck-v2.py --lane .` check S3 re-derives the digest.

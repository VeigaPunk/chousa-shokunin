# Round 78 — the outer battery stops printing its answer key, stripping its subject identity and trusting its receipt

Base `53dbd512d0ab70055338cb44898a6db70049537f` (round-77 tip, admitted by the non-author
spot-check `53dbd512`); prefreeze instruments and controls
`93e0432eb5bb9c4492d540bc6a6358ed3f8d4392`; claims freeze
`01b444b7f8d90785515e77c7ba9db5d63361329b`. Two claims in
`corpus/evidence/round78/claims.md`: C1 operability (lowest scored non-retired axis, the
historical 3/10 held) and C2 calibration. This round answers QUALITY 143's successor
requirement and the round-77 spot-check's routed defects 1, 3 and 4.

## Gate

- Admit S193, own-work B, scoped to the r77 spot-check's routed defect 1 — the gate-registry
  row with no owner cell. `corpus/lessons/round-77-verifier-spotcheck.md` at
  `53dbd512d0ab70055338cb44898a6db70049537f`, lines 156–160, quote on line 156. Opened
  2026-11-04. Located quote: "SKILL.md registry row `round77 order-and-content battery` is
  missing its owner cell." (11 words, `wc -w`). Grounds C2's S1 class: the closure record names
  the defect, not independent truth that the successor repairs it — the committed counter is.
- Admit S194, own-work B, scoped to QUALITY 143's successor requirement for an outer battery.
  `corpus/QUALITY.md` at `53dbd512d0ab70055338cb44898a6db70049537f`, line 1046 (the criterion's
  single paragraph), quote inside its Check sentence. Opened 2026-11-04. Located quote: "An outer battery prints no invertible answer
  key, no strippable subject identity and no receipt a child can append to" (20 words). Grounds
  C1's target: it is the criterion the round-77 critic's receipts produced, and it is a
  requirement, not a measurement.
- Reject S195, own-work C, scoped to this round's own predicate receipt as a source row.
  `corpus/evidence/round78/controls/forge-battery-after-v5.txt` at
  `93e0432eb5bb9c4492d540bc6a6358ed3f8d4392`, lines 1–12, quote on line 9. Opened 2026-11-04.
  Located quote: "FORGE_BATTERY=PASS forgers_handled=4/4 positive=1/1" (a receipt line).
  REJECTED: a receipt that prints the predicate is the predicate's own evidence, not a source
  about verification method — the S192 precedent one layer out. Flip: admit scoped to what a
  receipt must carry if an admitted knowledge entry ever rests on receipt format.
- New registry rows S193/S194 mined, used-by this lesson; S195 rejected, used-by `—`. Existing
  status/recheck/used-by cells unchanged. No URL opened or fetched: all three are
  revision-pinned committed paths.
- Non-author spot-check requested: two admits and one reject above. Dispatched wave seats are
  author-lane evidence, not independent admission or promotion reviewers.
- Assimilation: none. The `merge/chousa/` package was not adopted this round: the id-collision
  check run before any append found 111 of 114 staged ids colliding with the live registry
  (192 rows), and the claim cap was already spent on C1/C2. Evidence:
  `.ufo/waves/round-78/assimilation/{reg-ids,staged-ids,collisions}`; the guard itself was
  proved able to fail once (`assimilation/guardproof/collisions` = `S002` on an indented
  scratch row). No package bytes, no campaign tool, no shokuknow write.
- `considerthese/` holds operator-authored files through 2026-10-26 and was opened; no proposal
  was adopted this round (claim cap), recorded rather than implemented. Nothing there was edited.

## Mistakes

| class | evidence | captured-by | fix |
|---|---|---|---|
| an inert salt inserted before `from __future__` broke both positives | the first v5 predicate run printed `MATRIX RUN POSITIVE successor-counter … marks=0/12/FAIL` for both positives and `FORGE_BATTERY=FAIL … positive=0/1`; the inserted statement at `ast` body line 2 landed above `from __future__ import annotations`, so every salted copy was a `SyntaxError` at compile time | nothing in the battery's own guards: the content leg and the subject loop both pass a syntactically invalid subject as "forger rejected", which is why the positive control is what caught it | `salted_copy()` now inserts only above a top-level statement that follows every `__future__` import and is not a docstring; measured on both positives at three anchor positions (`MATRIX=PASS` 12/12 each) and on the full control (`controls/forge-battery-after-v5.txt`, positive=1/1) |
| a verdict rule credited a battery with detecting an append it has no mechanism to detect | the first forge-battery run over the round-77 battery printed `FORGER a5d-detached-append … integrity=BAD verdict=DETECTED` and `forgers_handled=1/4`, though v4 prints no `RECEIPT_LINES` trailer at all — the counter's own "more than one BATTERY= line" rule was being read as the battery's integrity claim | no criterion: the receipt reader conflated "the receipt is inconsistent" with "the battery checks its receipt" | `read_receipt()` returns `None` when the battery prints no trailer, and only `integrity is False` maps to DETECTED; re-measured: v4 `handled=0/4` (`controls/forge-battery-before-v4.txt`), v5 `handled=4/4` |
| a receipt labelled `(controls)` was measured before the controls commit existed | `controls/forge-battery-after-v5.txt` and `controls/work-contract-after-v5.txt` carry `# lane rev: 53dbd512… (controls)`, but both were measured on the pre-commit worktree, so the label names a revision where the instrument they exercised does not exist (`R78SentinelA/receipt-audit.txt`, finding F2) | no criterion: QUALITY 125 binds a claims file's digests and QUALITY 133 binds a count block's revision, and neither binds a control receipt's revision label to the instrument's presence there | the receipts are frozen and not amended; the lesson records the slip, and the successor rule is that a receipt names the revision it was measured at and the instrument digest separately, never a revision the instrument does not exist at |

## Instrument limits (recorded, not amended after scoring)

- **The identity leg closes the trailing-strip class only.** The round-77 salt was an appended
  `# salt <hex>` line, so `rfind(b"\n# salt ")` recovered the source byte-for-byte
  (`R77CriticA/rcpt-a1.txt`). v5 inserts an inert *statement* above a random top-level
  statement, so no suffix strip and no single fixed-marker strip recovers a committed object —
  but a normalizer that deletes every statement it does not recognise still can, and the wave's
  `R78ExecC` measures exactly that channel rather than assuming it closed.
- **The quiet leg removes the streaming oracle, not every side channel.** No per-subject line is
  printed until the scoring loop ends and no order digest is printed at all, so
  `/proc/<ppid>/fd/1` yields no position and no permutation. What it does not hide: the work
  tree's directory count, the receipt's size growth, and `/proc/<ppid>/mem` where ptrace allows
  it. `R78CriticA` measures each.
- **`RECEIPT_LINES` exposes an append; it does not prevent one.** A child that appends after the
  battery exits changes the line count, which `forge-battery.py` reads as DETECTED rather than
  believed. A child that truncates or rewrites the receipt defeats the trailer, and the exit
  code remains the only authoritative signal.
- **The content leg is still a shape requirement.** `--no-content` does not flip the predicate;
  a blind script cannot survive the permutation anyway. The contract cells are public by design
  and the parent-cmdline channel (`rcpt-a2.txt`) still reads them; v5 does not treat the
  contract as a secrecy boundary.
- **The forge battery scores four channels at one salt family and one run per subject.** It
  proves those four forgeries are refused or detected on these bytes; it does not prove
  arbitrary-forgery freedom, and the honest answer to "can v5 be passed?" remains yes for a
  matrix that implements the checks.

## Claim outcomes — both frozen kill rules fired

- **C1 (operability): the predicate holds; the kill rule fires.** The frozen predicate line
  reproduces byte-identically at exit 0 (`controls/forge-battery-after-v5.txt`, re-run by
  `R78ReviewA` and `R78ExecB`), the positive control is ACCEPTED, and the four round-77 channels
  are REFUSED/DETECTED. But three independent seats plus the L1 built a *content normalizer* that
  deletes the salt family, hashes the remainder and answers from the two public positive digests:
  `R78L1/a8-normalizer-v5.txt` (`BATTERY=PASS forgers_rejected=11/11 positive=2/2
  oracle=REJECTED`, exit 0), `R78ExecC/v5.stdout.txt` and `R78ReviewA/v5-vs-a9-receipt.txt` reach
  the same line. The claim's own kill rule says such a forger falsifies the claim, so C1 lands
  **falsified by its own kill rule** — the instrument bytes and the four-channel closure are what
  they are, and the claim text and its kill rule contradict each other as written
  (`R78ReviewA` finding 1). QUALITY 147 carries the successor requirement.
- **C2 (calibration): the kill rule fires.** `R78ReviewB` cloned the lane, restored all three
  routed defects and wrote three *hollow* repair lines — a `correction:` line asserting 8 cells on
  a 7-cell row, a gutted `supersedes:` criterion, an `erratum:` line asserting a move that never
  happened — and the counter printed `SELFCHECK=PASS unresolved=0/3` at exit 0
  (`R78ReviewB/ALL-three-hollow.txt`), with an honest control pair per class
  (`ctrlA/ctrlB/ctrlC` each `unresolved=1/3`, exit 1) showing the PASS came from the injected
  bytes. It also showed that any newer `## Round-<n> addition` block removes every earlier
  criterion from the audited window (`atkB2-new-block-window.txt`). The lane's repairs are
  truthful and independently checkable by direct byte inspection, but the counter that was
  supposed to re-derive that does not discriminate. QUALITY 146 carries the successor requirement.
  Frozen predicate and receipts unamended.
- Neither claim is re-declared or narrowed after data. The round's admission is false on the
  frozen rules and the report says so; the operator rules.

## Additional instrument limits the wave measured (recorded, not repaired)

- **`forge-battery.py` reads each receipt once, at a caller-chosen settle time.** With
  `--settle 0` it prints the unchanged `4/4` PASS line at exit 0 while the a5d receipt on disk is
  later forged to 139 lines and 14 `BATTERY=` lines (`R78ReviewA/race-settle0.stdout`,
  `race-a5d-receipt-FORGED-ondisk.txt`); the default 26 s exceeds the forger's 20 s delay by six
  seconds, which is a wall-clock margin, not a proof.
- **A same-count in-place rewrite is invisible to `RECEIPT_LINES`.** A grandchild that rewrites
  the last `BATTERY=FAIL` line to the PASS predicate leaves a receipt that passes the trailer's
  own rule (`R78ReviewA/rw-receipt-FORGED-internallyvalid.txt`). Only the live exit code
  contradicts it.
- **The forge battery is a black-box behavioural test, not an honesty certificate.** A UUT battery
  keyed on the four forger digests passes it (`R78ReviewA/forge-vs-cheat-receipt.txt`).
- **The `--work` contract repair is real but its control's case A leaves the matrix's own exit
  unconstrained** (`R78ExecB` reading note), so `WORK_CONTRACT=PASS` speaks about survival and
  setup exits, not about the run's verdict.
- **The ORDER-line removal is decorative; the quiet leg is the closure.** `R78MutA`'s twins: M1
  (`--print-order` forced on) and M1B (the ORDER line emitted at round-77 timing, digest genuinely
  readable, `perm digest=3a472f6c1df4 secs=8.4`) both leave `forgers_handled=4/4`, because a7 derives
  its position from the count of `MATRIX RUN` lines and the quiet leg buffers those, so `seen` is
  always 0 — the digest is *necessary but not sufficient*. M4 (RUN lines emitted immediately, no
  ORDER line) also flips nothing: a visible position with no permutation to index it is not an
  answer key (`R78MutA/table.md`). What is load-bearing is the interior-statement salt (M2 flips
  a1 *and* a2 — one leg, two forgers) and the `RECEIPT_LINES` trailer (M3 flips a5d to FORGED).
  The claim's causal sentence "prints no order line at all" therefore describes a removal that the
  scored channel set cannot feel; the honest statement is the pair (quiet leg + trailer + salt).

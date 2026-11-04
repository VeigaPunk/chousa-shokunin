# Round 77 frozen claims — the outer battery's order and content legs

Base: `6defa58dbdc40856f4e7dd24df98dc7ebd3459c0` (master, Linux host, `ls-remote` = local).
Prefreeze instruments and control receipts: `e6fcdc4770c2fa73e5ccda99445c4311128d7e0d` — the controls commit strictly precedes
this freeze (r75 routed defect 3; `souji` QUALITY Q120).

Reads done before declaring: the r76 closure (admitted) and its non-author spot-check
`corpus/lessons/round-76-verifier-spotcheck.md` routed defects 1–5, and the r76 lesson's
`## Instrument limits`. Routed defects 1 (the outer order/content legs) and 3 (the false claims
sentence) are this round's two claims; 2 (the moving `--lane-rev`) is answered inside C2 by pinning
`--base` and `--rev` explicitly in the counter command; 4 (the learned-table subject) is carried as
a recorded limit, not claimed; 5 (wave settlement records) is answered by committing the wave
results file.

Two claims, distinct axes, causally separable.

## C1 — operability (lowest scored non-retired axis, 3/10; the historical 3/10 is not moved)

**Claim.** The lane's candidate-running battery can no longer be passed by a matrix that counts its
own invocations: the successor permutes the subject order per run with a fresh 64-bit seed, requires
every matrix run to print the twelve-line contract table with the battery's independently stated
`expected_rc`/`expected_failed` cells, and scores three forged matrices as a control leg.

**Predicate (one sentence, one command).**
`python3 -B corpus/evidence/round77/matrix-battery-v4.py --matrix corpus/evidence/round76/loader-matrix-v3.py --work DIR`
exits 0 and prints exactly `BATTERY=PASS forgers_rejected=11/11 positive=2/2 oracle=REJECTED`.

**Instruments (frozen at the controls commit).** `matrix-battery-v4.py` (sha256
`155fafb16b6931449abefb60575029f273959ba4e94a4db48ac22e525f106a3d`) runs the eleven round-76 forgers and two positives — byte-identical sources
under `corpus/evidence/round76/` — each salted into a random-named directory, in a per-run
permutation drawn from `secrets.randbits(64)`; the seed digest is printed, the permutation is not.
The content leg requires exactly the twelve contract lines with the battery's own contract map and a
`PASS` count equal to the summary count. The oracle leg runs three forged matrices through the same
scoring and none may reach full marks: `forgers/forge-order-matrix.py` (first four calls PASS,
summary only), `forgers/forge-order-matrix-table.py` (the same with a valid contract table) and
`forgers/forge-order-matrix-block.py` (first two positions of every thirteen-invocation block, so it
survives the run-major iteration and the content leg). `loader-matrix-v3.py` is the round-76 matrix,
unchanged (`b79d6441057a01b27eb465c6b0625cd46502114f8b622b370c2cd2805c81913f`); this round adds no
case coverage.

**Before (do-nothing state, committed before this freeze).** The round-76 battery accepts a
call-count matrix: `matrix-battery-v3.py --matrix <the first-four oracle> --work DIR` prints
`BATTERY=PASS forgers_rejected=11/11 positive=2/2`, exit 0
(`corpus/evidence/round77/controls/before-oracle-v3.txt`) — the oracle reads no input and reaches
the exact target lines. The same oracle as the matrix under test in v4 is
`BATTERY=FAIL forgers_rejected=0/11 positive=0/2`, exit 1
(`controls/forge-as-matrix-summary.txt`).

**After (pre-freeze positive control).** `BATTERY=PASS forgers_rejected=11/11 positive=2/2 oracle=REJECTED`,
exit 0 (`controls/after-battery-v4.txt`); every `ORACLE` line `REJECTED`. Closure-removal twins:
`--no-permute` → `BATTERY=FAIL` with `oracle=MISS` (`controls/twin-no-permute.txt`), so the order
leg is load-bearing; `--no-content` → still `BATTERY=PASS` (`controls/twin-no-content.txt`), so the
content leg is a shape requirement and is not claimed as the discriminating closure.

**Kill rule.** Any forger scored as not rejected in either run, any positive not accepted in both,
any oracle reaching full marks in either run, or a `BATTERY=` line that is not exactly
`PASS forgers_rejected=11/11 positive=2/2 oracle=REJECTED` → C1 unprovable/honest-stop. Matrix,
battery, oracles and predicate are frozen at the controls commit; changing a subject, a check or a
seed rule after any seat has scored it is a new claim.

**Recorded limits (QUALITY 126/135/137/139).** The battery proves these thirteen subjects and three
forged matrices at these saltings; it does not prove arbitrary-forgery freedom. The permutation is
probabilistic. A matrix that reads the battery's own source can recover the order. The content leg is
satisfied by a fabricated table. The matrix's commit graph still shows all twelve case commits.

## C2 — calibration (sourced on S190/S191, opened this round)

**Claim.** The false sentence in the frozen round-76 claims file is superseded by an append-only
correction block in that same file, and one committed counter re-derives the supersession: the
superseded clause is still present verbatim, the block quotes it, states the corrected fact, is the
last section, and the landing diff deletes nothing.

**Predicate (one sentence, one command).**
`python3 -B corpus/evidence/round77/c3-count.py --lane . --base a519fb0a80cf52c7988713c1f05b3ce8440fedda --rev <landing>`
exits 0 and prints exactly `C3=PASS checks=5/5`.

**Instrument (frozen at the controls commit).** `c3-count.py` (sha256 `32b7656515afd31524fbfc26d0674f094a442a21ee92d63c318b83097062335d`) checks five
conditions on `corpus/evidence/round76/claims.md`: C3-1 the superseded clause is still present
verbatim (whitespace-normalised, because it is split across lines 10–11), C3-2 a
`## Correction — round-76 claims prose` heading exists, C3-3 that block both quotes the superseded
clause and states the corrected fact, C3-4 the base→landing numstat deletes zero lines and adds at
least one, C3-5 the block is the last `## ` section and no unclosed HTML comment hides it.

**Before.** At the r76 tip `C3=FAIL checks=1/5`, exit 1 (`controls/before-c3.txt`): the clause is
present (C3-1) and no supersession exists.

**After.** At the landing `C3=PASS checks=5/5`, exit 0 (`controls/after-c3.txt`).

**Kill rule.** Any check failing, or a `C3=` line that is not exactly `PASS checks=5/5` → C2
honest-stop. Frozen bytes are not amended after scoring: the correction is appended and the
superseded sentence is quoted, never rewritten.

**Recorded limits.** Lexical and line-local: the counter proves presence, position, the quoted
superseded clause, the corrected phrase and an append-only numstat — not that the corrected sentence
is true, and not that no other sentence in the frozen file is false.

## Shared boundaries

No network, no package adoption, no host question presumed answered, no sibling repo or fleet repo
writes other than the round report and L0 appends. Non-author spot-check requested for the
SOURCES admit/reject set; dispatched wave seats are author-lane evidence, not promotion reviewers.
Round shape: one v1 wave of 12 seats (3 executor, 1 scout, 1 scribe, 1 connector, 2 reviewer,
2 critic, 1 mutation-tester, 1 sentinel = 5 attack seats, 42%); L1 holds the canonical planner seat;
no residual call planned; no dead seat replaced.

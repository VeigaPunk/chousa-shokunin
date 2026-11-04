# Round 75 — R75Review: independent re-measurement at freeze `43a7a0db`

Seat: R75Review (leaf; no subagents, no network, no production edits, no lane/fleet git or jj
mutation). Root `/home/vgpnk/Projects/shokunin/chousa-shokunin`, freeze A
`43a7a0db52c8aabdf32735f58e09610e05200e79`, base `8022f72c889c904b5657d52c7f29e1643392a216`
(verified `parent=8022f72c…`). Read first: `corpus/evidence/round75/claims.md`, the five committed
controls, the frozen matrix/battery/counters/forgers, `corpus/QUALITY.md:1002` (criterion 126).

Method: one read-only clone at A in scratch (`git clone --no-hardlinks` then
`checkout --detach A`; `git status --porcelain` empty), every measurement from `env -i` clean
shells against committed bytes, `TMPDIR` inside scratch. Exact commands/exits:
`R75Review/01-commands.txt`; committed-byte hashes: `R75Review/02-committed-hashes.txt`.
Environment: Linux 7.2.11-arch1-1, python 3.14.8, git 2.56.0. **No tool installed or upgraded**
(pacman paused; nothing was needed). I did not read `R75Review2.md` or any other seat draft; this
review is independent.

## 1. The two frozen predicates, re-measured

| # | Command (clean shell, cwd = clone at A) | Exit | Key output | Receipt |
|---|---|---|---|---|
| 1 | `python3 -B corpus/evidence/round75/matrix-battery.py --matrix corpus/evidence/round75/loader-matrix-v2.py --work $S/out/work-after --runs 2` | **0** | `MATRIX_SHA256=95bdd49363e475316c5f5a9e200f039fcc1611f6fbd52848af8e078be0268ee7`, `BATTERY=PASS forgers_rejected=5/5 positive=2/2` | 03 (repeated as 04, 05) |
| 2 | same battery `--matrix corpus/evidence/round74/loader-matrix.py --work $S/out/work-before` | **1** | `MATRIX_SHA256=979638251845071cfb2c5e130cd81800251c5a6cb041438deb258d8877e2ff8d`, `BATTERY=FAIL forgers_rejected=2/5 positive=2/2`; order-oracle, diff-only, naive-grep each `9/9` in both runs | 06 |
| 3 | `python3 -B corpus/evidence/round75/c2-count.py --lane . --rev 8022f72c… --base 8022f72c…` | **1** | `DERIVED=S182:16 S183:11 RECORDED=S182:18 S183:13`, `C2=FAIL checks=1/4` | 07 |
| 4 | same with `--rev 43a7a0db… --base 8022f72c…` | **1** | identical derived line; `C2=FAIL checks=1/4 rev=43a7a0db52c8 base=8022f72c889c` | 08 |

The claims predicate was also run **verbatim** (no extra flags; the battery default is `--runs 2`):
exit 0, same `MATRIX_SHA256`, same `BATTERY=PASS forgers_rejected=5/5 positive=2/2` (receipt 03b).
Repeatability: the C1 predicate ran four independent times (receipts 03/03b/04/05): exit 0, the
same `MATRIX_SHA256`, and the exact `BATTERY=` line each time. The order-oracle per-run marks
varied (4/12,5/12 · 4/12,6/12 · 5/12,5/12 · 6/12,2/12) but never approached full marks — see F9.

### Digest pinning (requested check)

`sha256(git show 43a7a0d:<path>)` over all twelve frozen instruments (receipt 02):

- `loader-matrix-v2.py` = `95bdd493…68ee7`; `round74/loader-matrix.py` = `97963825…2ff8d`.
- Both equal the digests stated in `claims.md`, and equal the `MATRIX_SHA256=` lines in the
  committed receipts (`controls/after-battery-v2-matrix.txt`, `controls/before-battery-r74-matrix.txt`).
- Each battery `SUBJECT … sha256=` prefix equals the same subject's committed full digest
  (9334721a, 909987ce, 0dbd573c, d5155850, 180d1a3d, 6691c74c, e5fc4104).

### The receipts are what they claim

- **Before** (`controls/before-battery-r74-matrix.txt`): `BATTERY=FAIL forgers_rejected=2/5
  positive=2/2`, `EXIT=1`, three forgers `9/9`. My re-run reproduced the line, the exit and the
  three `9/9` acceptances; digest matches. **Confirmed.**
- **After** (`controls/after-battery-v2-matrix.txt`): `BATTERY=PASS forgers_rejected=5/5
  positive=2/2`, `EXIT=0`, `MATRIX_SHA256=95bdd493…`. My three re-runs reproduced both.
  **Confirmed.**
- **C2 base** (`controls/before-c2.txt`): the exact `DERIVED=S182:16 S183:11 RECORDED=S182:18
  S183:13` line and `C2=FAIL checks=1/4` (Q1–Q3 FAIL, Q4 PASS removed=0). **Confirmed.**
- Independent derivation (no counter code): the S182 quote carries 16 whitespace tokens and the
  S183 quote 11; the lesson records 18 and 13. The "16 and 11" derivation is correct.
- Negative control re-run: the frozen r73 counter on v2 scores `LOADER_MATRIX=3/12`, exit 1
  (receipt 11), matching `controls/negative-r73-counter-on-v2.txt`'s 3/12 under a new seed.

## 2. Verdict per claim

| Claim | Frozen predicate met at freeze A? | Stated limit understated? |
|---|---|---|
| **C1 — operability** | **Yes.** Command 1 exits 0 with the exact line; digest equals the frozen v2 digest; the do-nothing control (command 2) is 2/5 exit 1 with the same digest as the receipt. | **No stated limit is understated.** One stated limit is *conservative* (F9), two residual limits are unstated (F4, F7), and the claim body contains one factual error about the fixture topology (F3). |
| **C2 — calibration** | **No.** No `<landing>` exists: `git log base..A -- corpus/lessons/round-74.md` is empty and `git diff --numstat` base→A for the lesson is empty; at `--rev A` the counter still prints `C2=FAIL checks=1/4` (command 4). The correction block is absent at A. | **No limits are recorded at all**, and the instrument enforces less than the claim's Q2/Q3 wording: a landing can pass 4/4 without naming the superseded 18/13 (F1), and a non-EOF insertion passes (F5). The landing control set also has no C2 "after/positive" receipt (F2). |

C1 is therefore provable at the freeze; C2 is an unlanded commitment that can only be scored at
the landing commit. Nothing in C2's predicate is met by the frozen bytes today.

## 3. Findings by severity

### F1 — High — C2's Q3 (and Q2) are substring tests; the predicate passes a block that never names the superseded 18/13

`corpus/evidence/round75/c2-count.py` implements Q3 as `str(rec_a) in block and str(rec_b) in
block` (`18` and `13`), and Q2 the same way for `16` and `11`. I built four fixture landings on
the committed base lesson (scratch repo, throwaway `fixture@invalid` identity, toplevel asserted)
and ran the frozen counter (receipt 09):

- intended block → `C2=PASS checks=4/4` (control);
- **under-enforced block** `S182 re-derives to 16 and S183 to 11; the counter scores 4/4 with 13
  net added lines.` → `C2=PASS checks=4/4`. Q3 prints `block names superseded 18/13: True`, but
  `18` only occurs inside `S182` and `13` is an unrelated line count; neither recorded value is
  named as superseded.
- **substring block** `The two located quotes total 116 characters; S182 and S183 are re-derived
  in the 13-line note.` → `C2=PASS checks=4/4`; Q2's `16`/`11` are matched inside `116`.

Consequence: the claim's kill rule "superseded values unnamed → honest-stop" cannot fire through
this instrument, and the landing can satisfy `C2=PASS checks=4/4` with a block that fails the
stated meaning. I am not editing frozen bytes (they are frozen after scoring); the landing must be
accepted only after a verifier reads the block, and the block should state explicitly that the
recorded 18-word and 13-token figures are superseded by 16 and 11.

### F2 — Medium — C2 predicate unlanded at A, with no pre-freeze positive control

`claims.md` C1 carries a committed After receipt; C2 carries only a Before receipt, and at A the
lesson bytes are untouched (`13-claim-facts.txt`). This is internally honest (the predicate names
`<landing>`), but it means the freeze contains one claim that the frozen bytes cannot satisfy and
one whose instrument has never been shown green on any committed landing. The round report must
say C2 is open at A and re-measure it at the landing commit.

### F3 — Medium — C1 claim text is wrong about the fixture topology

`claims.md` says the successor matrix "writes twelve disposable fixture repositories, one real
commit per case". The matrix calls `git init` once per run inside one `TemporaryDirectory`, then
writes twelve case commits (thirteen with the base) in that one repository, restoring `FILES`
before each case. The battery therefore creates 7×2 = 14 repositories, not 24. Direct evidence
(`13-claim-facts.txt`, `10-patch-only-counter-on-v2.txt`): all twelve cases share one `base=` sha
with twelve distinct `rev=` shas. The per-case diff is still exactly the single mutation (trees are
restored), so the measurement is unaffected — but the claim's description of the evidence is not
true as written.

### F4 — Medium-low — unstated discrimination limit: a patch-text-only counter scores 12/12

The three "content" cases are meant to defeat a diff-only reader. I wrote a counter that never
opens a protected file and never runs `git show <blob>`: it reads only the unified `git diff`
patch text (default context) plus numstat/name-only, and reconstructs the pre-image from context
lines. On `loader-matrix-v2.py` it scores **`LOADER_MATRIX=12/12 MATRIX=PASS`, exit 0**
(receipt 10; probe source `14-probe-patch-counter.py`). Root cause: each fixture file is four
lines, and git's default three-line context puts the original heading and body into the patch, so
the duplicate-heading and section-body checks need no file read. The battery's diff-only forger is
the narrower numstat/name-only shape (9/12), so this shape is untested. The claim's sentence
"decidable only from protected-file content" survives a literal reading (patch context is
protected-file content), but the matrix does not bind a candidate to opening files, and the
"source-blind vs content" framing is broader than what the battery demonstrates. Add this to the
recorded limits; it does not falsify the frozen predicate.

### F5 — Low — Q1 does not enforce "appended at the end", contrary to the counter's docstring

The docstring says the correction block is "anchored, appended at the end of the lesson"; the code
counts anchored headings anywhere and Q4 only forbids removals. A block inserted after the first
paragraph (not EOF) scores `C2=PASS checks=4/4` (receipt 09, `mid-insert`). The claims text itself
only says "appears exactly once", so the claim is not overstated — the docstring is.

### F6 — Low — `S184` is not in the registry at A

`claims.md` says C2 is "sourced on S184, opened this round", but `git show A:corpus/SOURCES.md`
contains zero `S184` rows (highest S183; receipt 13). The C2 predicate does not depend on the
registry, but the citation is unresolvable at the freeze and the row must be opened before the
landing report.

### F7 — Low — both positives are lane-authored in the same freeze commit

`ref-counter.py` is independently implemented in plumbing (`cat-file -p`, NUL-delimited numstat,
separate parser) but authored by `chousa-shokunin` in the same commit as the matrix and battery.
Positive agreement therefore proves contract-consistency between two implementations, not author
independence. QUALITY 126's own r62 precedent records the analogous limit ("the forgers were
written by the lane that wrote the counter"); the r75 limits paragraph does not.

### F8 — Low — printed `SEED` is not replayable

Both the matrix and the receipts print `SEED=…`, but `loader-matrix-v2.py` accepts only
`--counter/--work` (no `--seed`), so a verifier cannot re-derive a receipt's per-case distribution
or the quoted 5/12 oracle detail. The predicate does not require replay, but the receipts' seeds
are informational only and should not be read as a replay handle.

### F9 — Info — the stated order-randomisation limit is conservative, not understated

`claims.md` says "Order randomisation is probabilistic … a lucky permutation is not excluded".
For the frozen oracle this overstates the risk: its `SCRIPT` has 9 entries and emits `PASS`
afterwards, while the three structural cases require exit 1 with non-empty failed sets. Scoring
200 000 random permutations of the twelve cases against that script gives **max 9/12, P(full
12/12) = 0.0** (receipt 12). The frozen oracle is structurally capped below full marks on v2; the
battery's observed 2–6/12 range is consistent.

### F10 — Low — C2 predicate wording "prints exactly"

`claims.md` C2 says the command "prints exactly `C2=PASS checks=4/4`"; the counter always appends
`rev=… base=…` (`c2-count.py` final print), so an exact-line reading fails even on a correct
landing. C1's "prints exactly" is literally true for the `BATTERY=` line. Interpret C2 as a
prefix/substring match; correct the wording if the claim is restated.

## 4. Residual risk and verification gaps

- The only open predicate is C2's landing; because of F1/F5 the landing must be read by a
  verifier, not merely counted — the frozen instrument cannot distinguish the intended block from
  my under-enforced fixtures.
- C1's matrix binds content only against candidates that do not read the diff patch (F4); for
  these four-line fixtures a single `git diff` call exposes the protected content.
- I did not replay the committed receipts' seeds (F8: no `--seed`); I reproduced the predicates and
  the negative control from independent clean shells, not the exact per-case schedules.
- I did not assess the successor counter's implementation beyond its 12/12 pass on the frozen
  matrix (out of this seat's scope: claims/instruments/controls verification).
- The Windows-host question remains untouched, as the claims already state.

## 5. Receipts

`R75Review/01-commands.txt`, `02-committed-hashes.txt`,
`03b-after-battery-v2-exact-predicate.txt`, `03/04/05-after-battery-v2-run{1,2,3}.txt`,
`06-before-battery-r74-matrix.txt`, `07-c2-base.txt`, `08-c2-freezeA.txt`,
`09-c2-underenforce-probe.txt`, `10-patch-only-counter-on-v2.txt`, `11-r73-counter-on-v2.txt`,
`12-oracle-permutation-bound.txt`, `13-claim-facts.txt`, `14-probe-patch-counter.py`,
`15-probe-c2-underenforce.py`.

No production file was edited, no commit was made, no lane or fleet git/jj state was mutated. All
fixtures lived under `/fast/scratch/hyaku/chousa-r75/R75Review/` (removed after the report);
fixture toplevel was asserted before every commit and the throwaway identity was fixture-local
(`user.name=fixture`, `user.email=fixture@invalid`).

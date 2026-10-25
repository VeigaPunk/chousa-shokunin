# Attack14 — R47 C1 counter coverage: un- prefix-flip class (mut-g)

- lane: chousa-shokunin · wave: round-48 w1 · seat: Attack14 (critic) · id `L1Chousa48.Attack14`
- scope: the R47 C1 counter coverage defect for the un- prefix-flip class, mutant `g` of `.ufo/waves/round-47/w2/MutC1Refined.md`
- setup: read `corpus/evidence/round47/claims.md`, `corpus/lessons/round-47-verifier-spotcheck.md`, `corpus/evidence/round47/c1-count.py`, `tools/inference-ground.py`, `.ufo/waves/round-47/w2/MutC1Refined.md`. Read-only against the lane; every artifact under `/tmp/chousa-r48-attack14/` (removed before finish). No installs; no pacman; no lane-file modification. Milestone item covered: five surviving mutant classes → class `un-` flip (mut `g`).

## 1. Mutant reconstruction (measured)

- Pristine tool pinned to the round-47 blob: `git show 980fe43:tools/inference-ground.py` → sha256 `244a1897feec49a5a08625a0ca8d0cb3c490675678badeb3ee23d97a4329667e` (matches MutC1Refined.md line 4).
- Mutant `g` = the `un`-prefix flip branch of `polarity_flips` deleted. In the blob at 980fe43 the block sits at lines 327–330 (verified by context diff; the current working-tree tool has drifted to lines 326–329):
  1. `if pol is None:`
  2. `    return []`
  3. `negated, scope = pol`
  4. `stems = {stem(w) for w in scope}`
- Deleted exactly those four lines with a script (no `sed`-based lane edit). Reconstructed mutant sha256: `3f9c0999e6b232a5fbca21221f77f6ffe6629ccb28a6e2d8bce75ae737e976e8` — equals the R47 report's hash for `mut-g` (MutC1Refined.md line 31). Reconstruction verified byte-exact.

## 2. Frozen counter against the mutant (measured)

- Snapshot of the lane at HEAD `d4e6ef0` into `/tmp/chousa-r48-attack14/lane-snapshot` (`git archive d4e6ef0`) — the counter's own fixture set, `--root` and R46 entries intact; no lane file touched.
- `python3 corpus/evidence/round47/c1-count.py --root <lane-snapshot>` (pristine): `TOOL=present POSITIVE_PASS=3/3 JUNK_KILLED=3/3 CANARY=pass R46_COUNTER=pass R46_ENTRIES=2/2 C1=PASS` exit 0.
- Same counter with `--tool <reconstructed mut-g>`: **identical output** `TOOL=present POSITIVE_PASS=3/3 JUNK_KILLED=3/3 CANARY=pass R46_COUNTER=pass R46_ENTRIES=2/2 C1=PASS` exit 0.

**Verdict: the frozen counter does NOT catch the mutant.** The un- prefix-flip refinement is exercised by none of the six pinned fixtures or the two round-46 entries (no bullet uses an `un`-prefixed flip word), so removing it leaves every counter leg green. This reproduces and confirms the R47 coverage defect for class `un-` flip.

## 3. Minimal killer fixture (measured)

A fixture that DOES exercise the refinement, run on the counter's exact leg shape (`python3 <tool> --entry entry.md --spans spans.tsv --counts counts.json --root <k>`):

- `entry.md` Inference bullet: `Because `a frozen pool` is unfrozen at release, it drifts (S901).`
- `spans.tsv` (7 columns, same schema as `corpus/evidence/round46/spans.tsv`): `S901` row → `spans/S901-1.txt`.
- `spans/S901-1.txt`: `the release ships a frozen pool`
- `counts.json`: `{}`

Observed:
- pristine: `GROUND entry=entry.md section=1 bullets=1 tokens=1 grounded=1` + `FINDING INF_POLARITY_FLIP bullet=1 token='a frozen pool / unfrozen'` → `GROUND: FAIL` exit 1 (flip caught).
- mut-g: `GROUND: PASS` exit 0 (flip missed — `unfrozen` free of the un- branch).

So the mutation is real, minimal, and lethal to the refinement; the frozen counter cannot see it because no pinned fixture carries an `un`-prefixed flip.

## 4. Findings and smallest safe correction (measurement, not post-score proposal)

1. Measured: frozen `c1-count.py` survives mut-g (section 2). This is the same defect class routed at round-47 verifier spot-check section 6 item 2 ("add fixtures so the frozen counter kills the five surviving refinement mutants … `un-` prefix").
2. The killer fixture of section 3 is a drop-in candidate leg: pinned, minimal, and it kills mut-g (and, per MutC1Refined.md section 4, each sibling survivor has its own minimal killer — a, b, e, f). Adding the six-shaped fixture set to the counter's `PINNED`/legs would make `JUNK_KILLED` (or a new leg) discriminate.
3. No claim predicate is frozen this round; this report proposes no post-score changes — it only measures the gap.

## 5. Commands / evidence

`git show 980fe43:tools/inference-ground.py | sha256sum`; scripted 4-line deletion + `sha256sum`; `git archive d4e6ef0 | tar -x -C /tmp/chousa-r48-attack14/lane-snapshot`; two `c1-count.py` runs (`--root` snapshot; `--tool` mutated); killer-fixture runs for pristine and mutant. All outputs quoted in sections 1–3. Scratch `/tmp/chousa-r48-attack14/` removed on finish; no lane files, git/jj/index, fleet repo or sibling lanes modified.

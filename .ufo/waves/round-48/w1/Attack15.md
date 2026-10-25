# Attack15 — R47 C1 frozen-counter coverage: repeated figure occurrences (mut-e)

seat: L1Chousa48.Attack15 · lane round: 48 · wave: w1 · date: 2026-10-25
assignment: attack the R47 C1 counter coverage defect for the class of repeated
figure occurrences (`.ufo/waves/round-47/w2/MutC1Refined.md` survivor e), with
a minimal scratch mutation + fixture perturbation, scored by the frozen counter.
No lane files modified (no git/jj mutations; scratch under
`/tmp/chousa-r48-Attack15/` removed before finish).

## 1. Setup (exact)

- Pristine tool: lane tip `tools/inference-ground.py` (commit `02d95d32`
  "round-47: C1 wave-2 fixes…"; sha256 `9d789b34562cc0ce35be7e4d7ea67a9fa57eabf8794bbf096c8a8d190925149b`).
- Mutant mut-e: `/tmp/chousa-r48-Attack15/tools/inference-ground-mute.py`, a
  copy with `figure_flip` changed to first-occurrence-only (the R47 MutC1Refined
  mut-e: "figure_flip first occurrence only", lines 391–395 of the R47 tool;
  in the tip tool the function sits at lines 400–415):
  - pristine lines 411–415: `for m in re.finditer(...)` checks every
    occurrence; `if key_neg != any(is_neg(w) for w in nxt): return True`.
  - mutant lines 411–413: `for m in re.finditer(...): return False` — the
    first occurrence decides, the loop never inspects later occurrences.
  - sha256 `e5abbf27ffb0ade5d35c383a8bdc381957f842993cf5ae0fc2b125cf59199050`.
- Killer fixture: `/tmp/chousa-r48-Attack15/killer-e/` (self-contained repo):
  - `entry.md` (sha `3b78c079f131af54b655e80f5949a48edbc2fca314953c5cb7ed3d2b298f187b`):
    junk Inference bullet: "1,582 records carry no archive bucket, and 1,582
    records are bound (S902)"." — same figure twice; the FIRST occurrence is
    followed by a negator ("no"), the second is not.
  - `counts.json` (sha `0ebb4fc078f928bcc9b56e7f2a9696f67a8959f5ca5d7a0608615ab7fef96c74`):
    `{"without_archive": {"count": 1582}}` — nested counts key whose ancestor
    is negated.
  - `spans.tsv` (sha `4fca318c79093c5256b5d76286f44288eda55c9f5a9a8a3fbe0f2c2cd0cf62f4`)
    → `spans/S902-1.txt` (sha `3fb13c095d658660f48e516880652ac9e2fa5613725adb227bc793404a77134e`):
    "records carry no archive bucket; the manifest keeps them unbound" — no
    digits, so the figure grounds only via the counts leg, and the stored
    sentence does not touch the figure's polarity (the kill is pure figure
    occurrence logic; count and phrase are irrelevant to it).
  - The counts.json hash is byte-identical to the `killer f` counts.json in
    MutC1Refined §4 (`0ebb4fc0…c74`), confirming the shared counts shape.

## 2. Measured results

A. Frozen counter, pristine tool — `python3 corpus/evidence/round47/c1-count.py
--root <lane> --tool <pristine>`: `TOOL=present POSITIVE_PASS=3/3
JUNK_KILLED=3/3 CANARY=pass R46_COUNTER=pass R46_ENTRIES=2/2 C1=PASS`,
exit 0.

B. Frozen counter, mut-e — same command with `--tool <mutant>`: `TOOL=present
POSITIVE_PASS=3/3 JUNK_KILLED=3/3 CANARY=pass R46_COUNTER=pass
R46_ENTRIES=2/2 C1=PASS`, exit 0. **mut-e survives the frozen counter.**

C. Direct leg (the counter's exact fixture leg shape), pristine: `python3
<tool> --entry killer-e/entry.md --spans killer-e/spans.tsv --counts
killer-e/counts.json --root killer-e` → `GROUND entry=entry.md section=1
bullets=1 tokens=2 grounded=2`, `FINDING INF_POLARITY_FLIP bullet=1 token='1,582
/ counts key without_archive/count'` ×2, `GROUND: FAIL`, exit 1. The pristine
tool KILLS the repeated-figure bullet (both occurrences checked; the second, un-
negated occurrence flips the negated key figure).

D. Direct leg, mut-e → `GROUND: PASS`, exit 0. The mutant misses the second
occurrence: the first occurrence's negator satisfies the check and the loop
returns early.

E. Counter leg attribution: c1-count.py's coverage is the six pinned fixtures
(`corpus/fixtures/inference-ground-r47/`, pinned by sha256) + the two round-46
entries with `/dev/null` counts (no counts leg, so no figure can exercise
`figure_flip`). None of the eight contain a repeated figure with a negated
counts key ⇒ no pinned leg can see mut-e's defect. That is the measured R47
coverage gap (MutC1Refined §5's claim, confirmed on the tip tree).

## 3. Verdict

- The R47 C1 frozen counter has a real, reproduced coverage defect for the
  repeated-figure-occurrence class: the first-occurrence-only mutant survives
  unchanged (B: C1=PASS).
- The minimal perturbation is the killer fixture of C/D: one junk bullet, one
  number, two occurrences. A second occurrence without a following negator
  makes the negated-key figure flip; the current pinned set has no such shape,
  so the counter cannot score it.
- The frozen counter's fix (if the lane adopts it) is to add a repeated-figure
  fixture to the pinned set with the frame of C/D (negated ancestor key, bullet
  negator on the first occurrence only): the same counter code would then print
  `JUNK_KILLED=2/3` for mut-e (measured: its `killed()` leg is exactly the
  direct invocation of C/D).
- No post-score changes proposed; no frozen predicate touched; no operator-
  approval inferred from dispatch.

## 4. Evidence record

Commands run (decisive output above): the two frozen-counter runs (A/B),
the two direct tool runs (C/D), `sha256sum` on the mutant and every fixture
file. Scratch `/tmp/chousa-r48-Attack15/` removed before finish in no lane files modified by this seat.

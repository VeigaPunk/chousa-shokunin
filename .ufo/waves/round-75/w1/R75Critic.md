# R75Critic — W1 critic, lane chousa, round 75

Frozen revision `43a7a0db52c8aabdf32735f58e09610e05200e79` (verified with `git -C … rev-parse HEAD`).
Frozen matrix digest verified: `95bdd49363e475316c5f5a9e200f039fcc1611f6fbd52848af8e078be0268ee7`
(`sha256sum corpus/evidence/round75/loader-matrix-v2.py`). No production file was read as
authority beyond the frozen instruments and claims; nothing under `corpus/` was modified.

## Verdict

**C1's predicate reproduces exactly; C1's stated kill mechanism does not hold.**

- The frozen command prints exactly `BATTERY=PASS forgers_rejected=5/5 positive=2/2` and exits 0 on
  my own run (`logs/battery-v2.txt`). No kill-rule trigger is reachable from the frozen inputs.
- **No new source-blind forger reaches 12/12.** Three independent argv-only attempts score 4/12,
  2/12/1/12 and 2/12/1/12. The 4/12 is the combinatorial maximum for an order-invariant strategy
  (proof below), so this axis is closed for the class the claim names.
- **Four new metadata forgers reach 12/12 in both runs**, exit 0, without reading a protected file's
  payload and without implementing any check. They are not source-blind under the claim's own definition,
  so they do **not** falsify the predicate — but they falsify the sentence that justifies it:
  claims.md:52 "decidable only from protected-file content" and loader-matrix-v2.py:13/24
  "QUALITY 134: the verdict is bound to content, not to numstat". The verdict is bound to
  content **or to content-derived metadata**; `git diff --numstat` is not the only byte-free channel.
- The recorded limit at claims.md:62 ("a forge that fully re-implements the seven checks is … a
  correct counter") is incomplete: a forge that implements **nothing** and merely memorises a
  12-entry case fingerprint also passes, and is far cheaper to write.

## 1. Frozen predicate, reproduced

```
cd /home/vgpnk/Projects/shokunin/chousa-shokunin
python3 -B corpus/evidence/round75/matrix-battery.py \
  --matrix corpus/evidence/round75/loader-matrix-v2.py \
  --work /fast/scratch/hyaku/chousa-r75/R75Critic/battery/work
→ exit 0
  BATTERY=PASS forgers_rejected=5/5 positive=2/2
```

Per-subject marks from that same run (`logs/battery-v2.txt`), unchanged from the committed control:

| subject | run0 | run1 | verdict |
|---|---|---|---|
| POSITIVE successor-counter | 12/12 exit0 | 12/12 exit0 | ACCEPTED |
| POSITIVE ref-counter | 12/12 exit0 | 12/12 exit0 | ACCEPTED |
| FORGER constant-pass | 4/12 exit1 | 4/12 exit1 | REJECTED |
| FORGER constant-fail | 4/12 exit1 | 4/12 exit1 | REJECTED |
| FORGER order-oracle | 5/12 exit1 | 4/12 exit1 | REJECTED |
| FORGER diff-only | 9/12 exit1 | 9/12 exit1 | REJECTED |
| FORGER naive-grep | 9/12 exit1 | 9/12 exit1 | REJECTED |

The 5/12 and 4/12 for the order oracle are consistent with the recorded probabilistic limit
(controls/order-oracle-through-v2.txt records 5/12). Run integrity: every run emitted 12 distinct
`CASE` lines; over 18 direct runs no case occupied a fixed slot (first-case distribution
3/3/2/2/2/1/1/1/1/1/1; full position histograms in `logs/`), so the shuffle is not degenerate.

## 2. Attempts — each run twice through the frozen matrix

Command (all 18 runs): `python3 -B .ufo/waves/round-75/w1/R75Critic/run-attempts.py` → exit 0;
one log per (forger, run) under `logs/`. Sources are in this directory.

| attempt | reads at runtime | run0 | run1 |
|---|---|---|---|
| `forge-blind-const-pass.py` | argv only (ignored) | **4/12 exit1** | **4/12 exit1** |
| `forge-blind-fixed12.py` | argv + own invocation count | 2/12 exit1 | 1/12 exit1 |
| `forge-blind-revhash.py` | argv (`--base`,`--rev` digest) | 2/12 exit1 | 1/12 exit1 |
| `forge-meta-depth.py` | commit-graph depth | 4/12 exit1 | 4/12 exit1 |
| `forge-meta-mtime.py` | working-tree mtimes | 5/12 exit1 | 5/12 exit1 |
| `forge-meta-subject.py` | `git log -1 --format=%s` | **12/12 exit0** | **12/12 exit0** |
| `forge-meta-treehash-memo.py` | `git rev-parse <rev>^{tree}` | **12/12 exit0** | **12/12 exit0** |
| `forge-meta-ls-tree-delta.py` | `git ls-tree -r -l` sizes | **12/12 exit0** | **12/12 exit0** |
| `forge-meta-stat-size-memo.py` | `Path.stat().st_size` only, no git | **12/12 exit0** | **12/12 exit0** |

Content-read audit over the four winners (grep for `cat-file|git show|show|read_text|read_bytes|open(|grep`):
`content_reads=none` for all four. They read commit/tree object headers, entry types and sizes —
never a blob payload, never a diff.

### 2.1 Strongest source-blind near-miss — 4/12, and why it is the ceiling

`forge-blind-const-pass.py` answers the all-PASS contract on every invocation. It scores exactly
4/12 on every permutation, because exactly four of the twelve cases have the PASS answer
(`unchanged`, `append-0`, `append-1`, `append-2`). Exact mismatches (run0, `logs/forge-blind-const-pass-run0.txt`):

```
delete-0, delete-1, delete-2, replace-equal   want failed={C2-6}   got=none rc=0
receipt-change                                want failed={C2-7}   got=none rc=0
dup-log-heading                               want failed={C2-1,C2-2} got=none rc=0
dup-lesson-heading                            want failed={C2-3,C2-5} got=none rc=0
dup-card-heading                              want failed={C2-4}   got=none rc=0
```

Ceiling argument. The twelve expected answer shapes have multiplicities
(4, 4, 1, 1, 1, 1). For any subject whose per-invocation answer is chosen independently of the
permutation, `E[score] = Σᵢ m(aᵢ)/12 ≤ 4`, attained by always answering the modal shape; the two
identical-`4` shapes (all-PASS and all-`{C2-6}`) both give a deterministic 4/12 (constant-fail also
measures 4/12). A fixed non-constant sequence can reach 12/12 only if the permutation realises its
answer vector, which happens for `Π m! = 4!·4! = 576` of the `12! = 479 001 600` permutations
(≈1.20e-6 per run, ≈1.45e-12 across the battery's two independent runs). Deriving the answer from
`--rev` is not an escape: the 12 commit ids are distinct and per-run (measured: the same case's
`rev` differs when its chain position differs, e.g. `dup-log-heading` at position 2 in run0 and 10
in run1 of `logs/forge-meta-treehash-memo-run*.txt`).

### 2.2 Does the metadata attack count as source-blind?

**No**, under the definition the claim itself uses ("Never reads `--lane` bytes nor any repository
content", `forgers/forge-order-oracle.py:3`):

- `forge-meta-subject.py`, `forge-meta-treehash-memo.py`, `forge-meta-ls-tree-delta.py` execute git
  and therefore read repository objects (commit/tree headers, entry metadata). They are
  content-blind, not source-blind.
- `forge-meta-stat-size-memo.py` is the boundary case: five `Path.stat().st_size` calls on `--lane`,
  no subprocess, no git, no file byte. It is "argv + lane metadata", still not argv-only. If the
  round wants a binary label, this one should be called **metadata-reading**, not source-blind.

The seat's framing ("infer the case from --rev/--base plus file metadata … without opening
protected contents") is exactly realised: two of the four (sizes) need only `--base`/`--rev` plus
`ls-tree -l`, and one needs nothing but `--lane`.

### 2.3 Metadata channels that do *not* carry identity (controls)

- `--rev^{commit}` graph depth equals the **invocation index**, not the case:
  `forge-meta-depth.py` re-keys the r74 script to depth and scores 4/12, 4/12 (chance-level).
- mtimes identify the **mutated path only** (the fixture re-writes the mutated file after the reset
  pass), which is worth a deterministic 5/12 — `unchanged`, `receipt-change`, and one of the
  three append shapes per protected path. 5/12 twice. Real but insufficient; it cannot reach full
  marks.

## 3. Root cause (the counterexample, as a class)

The matrix re-randomises the **order** but not the **bytes**. Each case's tree is a pure function of
the frozen fixture plus a frozen mutation, so identity is stable across runs even though the commit
id is not. Measured in `logs/harvest.json` (fixture rebuilt twice in the seat's scratch, in opposite
case orders, from the instrument's own `FILES`/`CASES`/`mutate`):

| property | value |
|---|---|
| distinct tree ids / size vectors / commit subjects | 12 / 12 / 12 |
| trees identical across the two opposite orderings | yes, all 12 |
| `tree(unchanged) == tree(base)` | yes (`cc148693…`) |
| commit subject | literally the case name (`append-0`, `dup-log-heading`, …) |
| size deltas per case | append +21; delete −19; replace +2; dup +30/+39/+29; receipt +21 |

Three independent, stable identity keys reach the candidate through `--rev`/`--lane`:
commit subject (verbatim name), tree/blob identity (content hash, no content), byte sizes (also via
plain `stat`, no git at all). Any one of them converts the matrix into a 12-entry lookup table.
The claim's own definition of *source-blind* excludes these, which is why C1 survives as a
predicate — but its QUALITY-134 justification ("content, not numstat") is a false dichotomy, and
the recorded limits do not name the memorisation class, so a later reader would treat the axis as
closed when it is only closed for argv-only forgers.

## 4. Impacted axes

| axis | impact |
|---|---|
| C1 predicate (battery line + exit) | **unaffected**; reproduced exactly, exit 0 |
| C1 rationale sentence (claims.md:52) | **false as written** — "only from protected-file content" |
| C1 recorded limits (claims.md:62) | **incomplete** — memorised case identity is cheaper than re-implementation and is not named |
| QUALITY 126 (battery sample) | five subjects sample argv-only and content-reading shapes; **zero** metadata-reading subjects, so the battery cannot see this class |
| QUALITY 134 (attached to the content cases) | not satisfied in the stated sense; the three content cases are decided by sizes/subject as well |
| provenance sentence (claims.md:48) | "twelve disposable fixture **repositories**" is wrong; the matrix inits **one** repository and writes twelve commits chained on `base` (loader-matrix-v2.py:106-117). The single chain is why depth == invocation index and why the commit id depends on the permutation prefix |
| C2 | not measured by this seat; no claim made |

Note for reuse: the battery scores a forger as REJECTED only when both runs exit 1 with fewer than
full marks (`matrix-battery.py:116`). The four 12/12 metadata forges satisfy that criterion's
negation (exit 0, 12/12 twice), i.e. would be scored ACCEPTED if they were ever added as subjects.
This is a derivation from the frozen criterion, not a run of a modified battery.

## 5. Smallest safe correction (nothing applied — instruments are frozen)

No edit to `loader-matrix-v2.py`, `matrix-battery.py`, `ref-counter.py`, `c2-count.py` or the
committed forgers is proposed or safe under C1's kill rule ("changing a case, a check or the
battery after any seat has scored it is a new claim"). Two textual corrections and one next-round
instrument change:

1. **claims.md:52** — replace "whose verdict is decidable only from protected-file content" with
   "…decidable from protected-file content; the same verdict is also recoverable from fixture
   metadata (commit subject, tree/blob identity, byte sizes), which the battery does not sample".
2. **claims.md:62 (Recorded limits)** — add, next to the re-implementation escape: "a forge that
   memorises a per-case identity fingerprint (12-entry table keyed on the commit subject, tree id
   or size vector) also passes; the battery's five subjects do not measure this class".
   `loader-matrix-v2.py:13,24` should lose "only" / "not to numstat" on the same grounds.
3. **Next round (new claim)** — salt per run only the bytes the contract does not fix: append
   filler text with its length chosen to collide with the fixed structural deltas (+2 replace,
   +29/+30/+39 duplicate headings), commit subject suffix, receipt bodies. Measured feasibility
   on a monkeypatched probe of the frozen matrix (`probe-salted.py` — a probe of a hypothetical
   matrix, **not** the frozen one; log `logs/salt-*.txt`, 2 internal runs per subject):

   | subject | frozen matrix | salted probe |
   |---|---|---|
   | successor-counter (positive) | 12/12 ×2 | **12/12, 12/12 (exit 0)** |
   | ref-counter (positive) | 12/12 ×2 | **12/12, 12/12 (exit 0)** |
   | meta-subject | 12/12 ×2 | 4/12, 4/12 |
   | meta-treehash-memo | 12/12 ×2 | 4/12, 4/12 |
   | meta-stat-size-memo | 12/12 ×2 | 4/12, 4/12 |
   | meta-ls-tree-delta | 12/12 ×2 | 9/12, 9/12 |
   | meta-mtime | 5/12 ×2 | 5/12, 5/12 |
   | blind const-pass (control) | 4/12 ×2 | 4/12, 4/12 |

   Both declared positives stay at full marks, so the salt is contract-preserving for two
   independent implementations; all four 12/12 metadata forges collapse. Residuals to record:
   the delta oracle still gets 9/12 (its three append mismatches are exactly the collided cases —
   `logs/salt-forge-meta-ls-tree-delta.txt`), and mtime path identity is untouched at 5/12 because
   the same path is mutated in every shape; neither reaches full marks. Also add one
   metadata-reading subject to the battery; otherwise the next matrix can regress the same way
   with no battery signal.

## 6. Scope and limits of this review

- Measured: the frozen battery over the frozen v2 matrix; the nine forgers above, twice each;
  the fixture-signature harvest in two opposite orderings; a salted-probe feasibility run.
- Not measured: the r74 matrix, the C2 axis, any r72/r73 instrument, any production lane. No
  conclusion about arbitrary-forgery freedom is claimed here; the 4/12 bound applies to strategies
  that do not use per-case identity, and the 12/12 results are *fingerprint* forgeries, which fail
  on any case not in their table.
- Provenance note: `corpus/evidence/round75/__pycache__/loader-matrix-v2.cpython-314.pyc` exists in
  the lane tree, mtime 16:11:16, git-ignored (`.gitignore:3`), untracked. It is not this seat's:
  every import here ran with `-B` and a control import reproduced that `-B` writes no cache. No
  frozen instrument byte differs from the start-of-seat digests (matrix `95bdd493…`, battery
  `c35e937b…`, ref-counter `909987ce…`). Left untouched, since it is outside this seat's write scope.
- `--work` must pre-exist: the matrix does not create it and exits 2 with
  `MATRIX_SETUP: [Errno 2] No such file or directory: '…/loader-matrix-v2-…'` (run and captured
  here). The frozen battery creates it (`matrix-battery.py:90`), so the predicate is unaffected;
  worth one line in the instrument's usage text only.

## 7. Commands and exits (all executed in this seat)

| # | command | exit |
|---|---|---|
| 1 | `python3 -B corpus/evidence/round75/matrix-battery.py --matrix corpus/evidence/round75/loader-matrix-v2.py --work /fast/scratch/hyaku/chousa-r75/R75Critic/battery/work` | 0 (`BATTERY=PASS … 5/5 … 2/2`) |
| 2 | `python3 -B .ufo/waves/round-75/w1/R75Critic/harvest-fixtures.py` | 0 |
| 3 | `python3 -B .ufo/waves/round-75/w1/R75Critic/run-attempts.py` | 0 (18 matrix runs) |
| 4 | `python3 -B probe-salted.py --counter <successor-counter> --work …` | 0 |
| 5 | `python3 -B probe-salted.py --counter <ref-counter> --work …` | 0 |
| 6 | `python3 -B probe-salted.py --counter forge-meta-subject.py --work …` | 1 |
| 7 | `python3 -B probe-salted.py --counter forge-meta-treehash-memo.py --work …` | 1 |
| 8 | `python3 -B probe-salted.py --counter forge-meta-stat-size-memo.py --work …` | 1 |
| 9 | `python3 -B probe-salted.py --counter forge-meta-ls-tree-delta.py --work …` | 1 |
| 10 | `python3 -B probe-salted.py --counter forge-meta-mtime.py --work …` | 1 |
| 11 | `python3 -B probe-salted.py --counter forge-blind-const-pass.py --work …` | 1 |
| 12 | `python3 -B loader-matrix-v2.py --counter ./forge-blind-const-pass.py --work <missing dir>` | 2 |
| 13 | corpus-integrity greps/sha256sums over `logs/` (12 distinct CASE lines per run, position histograms, forger digests) | 0 |

Fixture scratch lives only under `/fast/scratch/hyaku/chousa-r75/R75Critic/`; every fixture asserted
`git rev-parse --show-toplevel` equal to its own `mktemp -d` root inside that directory before any
commit, identities were passed per-command as `fixture <fixture@invalid>`, and the scratch tree is
removed at seat close.

Tooling: nothing installed or upgraded; used the host's `python3 3.14.8` and `git 2.56.0` only.
No network, no pacman, no `~/.local/bin` writes.

## Artifacts

`forge-blind-const-pass.py` (98b9942e…), `forge-blind-fixed12.py` (1cb9c683…),
`forge-blind-revhash.py` (e4d09627…), `forge-meta-depth.py` (7a97ef8b…),
`forge-meta-ls-tree-delta.py` (d64950a9…), `forge-meta-mtime.py` (ddef2122…),
`forge-meta-stat-size-memo.py` (a2652ae8…), `forge-meta-subject.py` (b1b35efc…),
`forge-meta-treehash-memo.py` (380c4293…), plus `harvest-fixtures.py`, `gen-memo-forgers.py`,
`run-attempts.py`, `probe-salted.py`, and `logs/` (battery, harvest, 18 run logs, 8 salt logs,
summary).

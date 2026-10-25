# ReviewR2CommitTruth — R2 audited from committed bytes

- Seat: L2 reviewer, chousa round 40, wave w1 (leaf; no dispatch).
- Assigned attack: decide from committed bytes whether
  `corpus/evidence/round39/receipts/c1-mutenv-s39003.json` is tracked, compare that against the
  r39 lesson's not-committed wording, and inspect the appended erratum that names its supersession.
- Lane tip reviewed: `6bc90e04ac60307befacd554f7eee2b7284e2652` (r39 landing `6ac1007e…`,
  work `d164f88e…`). Working tree clean except `.ufo/waves/round-40/w1/swarm-registry.json`.
- Mode: read-only against the lane. No lane file, index entry, or jj state was modified. All
  counter doctoring was in memory against copies of the bytes read from disk; scratch Git repo
  lived under `/tmp/r2audit/`.

## Verdict

**R2's direction is correct and every erratum assertion I could mechanically check holds.**
`c1-mutenv-s39003.json` is tracked (added by `6d914e9`, byte-identical at `6ac1007` and `HEAD`);
the r39 lesson does say it was not committed; the r39 receipt directory held seven JSON files,
not six; the receipt binds a counter digest that is absent from the Git object database, so the
committed verifier refuses it by name and it cannot be an active receipt. The disposition
`status: corrected` is the right label for the *receipt*.

The defects are in the verification machinery and in citation/completeness, not in the finding:
the R2 cell of `c2-count.py` is the weakest of the four — its only mechanical term is index
membership, and every other term is unanchored substring presence. A forged erratum and a forged
disposition decision both still score `ok` (F1), and flipping the lesson's receipt clause to the
opposite wording still scores `ok` (F2).

## Attack (commands and outputs)

### E1 — is the receipt tracked?

```
$ git ls-tree -r --name-only 6ac1007e6a5d699d0742801026554fac1d900b5d -- corpus/evidence/round39/receipts/
corpus/evidence/round39/receipts/c1-after-s39011.json
corpus/evidence/round39/receipts/c1-after-s39111.json
corpus/evidence/round39/receipts/c1-base-s39001.json
corpus/evidence/round39/receipts/c1-mutenv-s39003.json      <-- present
corpus/evidence/round39/receipts/c1-mutenv-s39013.json
corpus/evidence/round39/receipts/c2-after-s39101.json
corpus/evidence/round39/receipts/c2-after-s39121.json
$ git ls-tree -r --name-only HEAD -- corpus/evidence/round39/receipts/   # same seven
$ git ls-tree -r --name-only 6ac1007 -- corpus/evidence/round39/receipts/ | grep -c '\.json$'
7
```

Provenance and immutability:

```
$ git log --oneline --follow -- corpus/evidence/round39/receipts/c1-mutenv-s39003.json
6d914e9 round-39: capture bash pin (C1 7/8->8/8) + verifier/subject receipt binding (C2 8/8); …
$ git diff --stat 6ac1007 HEAD -- corpus/evidence/round39/receipts/
(empty)
```

Tracked from the r39 landing onward, never rewritten in round 40 — so the erratum's "Preserve it
as superseded" is satisfied by the committed bytes, not by prose.

### E2 — the contradicted lesson wording

```
$ grep -n "not committed" corpus/lessons/round-39.md
25:| vacuous — the doctored-subject fixture … (`/tmp/chousa-r39-c2.log` — not committed) …
27:| vacuous — the PATH-`env` shim fixture … receipt `c1-mutenv-s39003.json` (superseded, not committed) …
$ awk 'NR==54' corpus/lessons/round-39.md
- Receipts (round close): six committed — `c1-after-s39011.json`,
$ awk 'NR==60' corpus/lessons/round-39.md
  c2 construction receipt and the broken-shim mutant receipt were discarded
$ git log --oneline -- corpus/lessons/round-39.md
6ac1007 round-39: knowledge x2 (S071 re-opened), lesson (4 mistakes, QUALITY 56), …
```

The receipt is named "not committed" at `:27`; the population claim ("six committed", listing six
names and excluding `c1-mutenv-s39003.json`) spans `:54-61`. The lesson was last modified in the
r39 landing, so both false statements are still live at tip.

### E3 — the appended erratum naming the supersession

`corpus/evidence/round39/claims.md:192` `## Errata (appended; the body above is frozen)`,
`:194` "Round-40 append-only erratum (2026-10-24; the frozen body above is unchanged).",
`:196` R1, `:197` **R2 — committed superseded draft.** The R2 bullet states: committed despite the
lesson's "not committed" wording; preserve as superseded; "it binds an uncommitted counter digest";
excluded from the active set; "The r39 receipt directory had seven JSON files, not six."

Append-only discipline verified mechanically — the frozen body is byte-identical and the errata
section previously held a placeholder:

```
$ git show 6d914e9:corpus/evidence/round39/claims.md | sed -n '1,190p' | sha256sum
fb4241d08bfec4d11683b8e7329af606c78f7ad2395eda18326aa4b42e862d39
$ sed -n '1,190p' corpus/evidence/round39/claims.md | sha256sum
fb4241d08bfec4d11683b8e7329af606c78f7ad2395eda18326aa4b42e862d39
$ git show d164f88 -- corpus/evidence/round39/claims.md     # 7 insertions, 1 deletion
-None yet.
+Round-40 append-only erratum … + five R-bullets
```

The single deletion is the `None yet.` placeholder under the errata heading, not body text.

### E4 — is the bound counter digest really uncommitted?

Receipt header (`c1-mutenv-s39003.json`): `counter_sha256 = 1c3b2a9e453ebfdc33993c85c758d566c806a936f414178730780a09684848da`,
`gate_sha256 = 890226590546ce7f6376a585e1e032d0eb3e6af3a962a2e42b201dbe9baf20f4`,
`expect_sha256 = 3abd2dcb1766c4…`, `predicate_holds = false`, `matched = 7 / total = 8`.

```
$ git cat-file -t 1c3b2a9e453ebfdc33993c85c758d566c806a936f414178730780a09684848da
fatal: Not a valid object name 1c3b2a9e453ebfdc33993c85c758d566c806a936f414178730780a09684848da
$ for rev in 6ac1007 HEAD; do git show $rev:corpus/evidence/round39/c1-count.py | sha256sum; done
91618e91640f748df76282244186088218d5f2b7a65364137fa6add29fea05d5  -
91618e91640f748df76282244186088218d5f2b7a65364137fa6add29fea05d5  -
$ python3 corpus/evidence/round39/verify-receipts.py \
    --receipt corpus/evidence/round39/receipts/c1-mutenv-s39003.json \
    --gate .ufo/waves/round-39/controls/mut-gate-path-env.sh \
    --counter corpus/evidence/round39/c1-count.py \
    --expectations corpus/evidence/round39/expectations.jsonl
VERIFY-FAIL: counter-sha256-mismatch
rc=1
```

The bound digest is not merely unreachable, it is not an object in the repository. Every other r39
receipt binds `91618e91…`. Exclusion is required, and the counter-level refusal is the mechanical
backstop: re-adding this row to `active-r39-receipts.tsv` would make `c1-count.py` print a miss.

### E5 — exclusion from the active set

```
$ cat corpus/evidence/round40/active-r39-receipts.tsv
# six rows: 3 round-40 regenerated + c1-after-s39111 + c2-after-s39101 + c2-after-s39121
$ grep -n "s39003" corpus/evidence/round40/c1-count.py
(no match)
```

`c1-count.py` also refuses a manifest whose row count or duplicate set is not six
(`:26-29`), so the population cannot silently grow.

### E6 — R2 cell sensitivity (in-memory doctoring, lane bytes untouched)

The predicate at `c2-count.py:60-64` was reproduced verbatim, importing the real `tracked()`
(`:37-40`) from the module:

```
baseline (real bytes)                                    -> R2=PASS
claims WITHOUT the R2 erratum bullet                     -> R2=fail
claims WITHOUT R1+R2 erratum bullets                     -> R2=fail
lesson WITHOUT receipt-level 'not committed'             -> R2=PASS   <-- F2
lesson with ALL 'not committed' removed                  -> R2=fail
erratum asserts a FALSE digest claim
  ("it binds the committed counter digest 91618e91…")    -> R2=PASS   <-- F1
disposition decision text replaced with
  "the receipt is absent from the tree"                  -> R2=PASS   <-- F1
lesson receipt clause flipped to "(superseded, committed)" -> R2=PASS <-- F2
counter reads receipt bytes? False
```

### E7 — `tracked()` primitive semantics

`tracked()` runs `git ls-files --error-unmatch` (`c2-count.py:39`), which answers about the
**index**, not about committed bytes. Demonstrated in a throwaway repo:

```
$ echo a > a.txt; git add a.txt; git commit -qm one
$ echo b > b.txt; git add b.txt            # staged, never committed
$ git ls-files --error-unmatch b.txt; echo $?          -> 0
$ git cat-file -e HEAD:b.txt; echo $?                  -> 128
$ git ls-tree HEAD -- b.txt | wc -l                    -> 0
```

At lane tip the index agrees with `HEAD` for this path, so the R2 verdict holds today; the
primitive itself cannot distinguish "staged" from "committed".

### E8 — the counter on committed bytes (container evidence)

```
$ python3 corpus/evidence/round40/c2-count.py
R2_DISPOSITION=ok
R3_DISPOSITION=ok
R4_DISPOSITION=ok
R5_DISPOSITION=ok
R39_CALIBRATION_DISPOSITIONS=4/4
rc=0
```

## Findings

### F1 — medium (calibration): the R2 disposition's content is not re-derived from the receipt

`c2-count.py:60-64`. The cell asserts only: index membership, file existence, the substring
`not committed` anywhere in the lesson, the substrings `R2` / the receipt path / `superseded`
anywhere in the r39 claims, and `dispositions["R2"]["status"] == "corrected"`. It never opens
`c1-mutenv-s39003.json`, never hashes it, and never reads `dispositions["R2"]["decision"]` or
`["evidence"]`. Proven in E6: an erratum asserting the opposite digest fact, and a disposition
decision asserting the receipt is absent from the tree, both still score `ok`.

Consequence: P2's requirement that "the counter must re-derive these states from the committed
evidence, not count prose labels alone" is met for R3 (`git ls-tree` counts, `c2-count.py:44-50`)
and R4 (`Counter` comparisons over the spec/plan JSON, `:70-78`), but for R2 the only derived fact
is index membership; the exclusion *rationale* — the one thing the erratum asserts — is unchecked
prose. This is the "unsupported by the counter's checks" limb of the C2 kill rule, at cell
granularity: a surviving-but-wrong R2 record would not be caught.

Recommended (next round, not this report's job): make the R2 cell open the receipt and assert
(a) `git cat-file -e <receipt["counter_sha256"]>` exits non-zero, (b) the same digest differs from
the committed counter, (c) the path is absent from `active-r39-receipts.tsv`. That turns the
erratum's operative sentence into a re-derivation and makes E4's evidence load-bearing.

### F2 — medium (calibration): the lesson term is unscoped and matches an unrelated sentence

`c2-count.py:62` tests `"not committed" in lesson`. `round-39.md:25` contains
"`/tmp/chousa-r39-c2.log` — not committed", which has nothing to do with the receipt. Flipping the
receipt clause at `:27` to "(superseded, committed)" — i.e. deleting the exact contradiction R2 is
about — still returns `R2=PASS` (E6). Conversely, the term also cannot detect a *repair*: the lane's
own precedent quotes the wrong text verbatim when correcting a lesson
(`round-38.md` `## Correction (D6b)`), so a corrected lesson would keep the substring alive.

Recommended: anchor the term to the receipt row, e.g. a regex over the line containing
`c1-mutenv-s39003.json` requiring `not committed`, and cite that the wording is contradicted by
`git ls-tree`.

### F3 — low/medium (consistency): the contradicted lesson is still live with no correction marker

`corpus/lessons/round-39.md` was last touched in `6ac1007`; it still asserts at `:27` that the
receipt is "not committed" and at `:54-61` that six receipts were committed. Round 40's correction
exists only outside the lesson: r39 claims Erratum R2 (`:197`), `routed-defect-dispositions.json`,
`SCORECARD.md` (round-40 section), and `corpus/lessons/round-40.md:18,27`. The round-40 lesson's own
fix column promises to "correct the r39 receipt population from six to seven", and the established
lane convention for a false prior-round lesson statement is an appended section —
`git show 6ac1007 -- corpus/lessons/round-38.md` shows exactly that (`## Correction (2026-10-24,
round 39 — routed defects D3/D6)`, +21/−2). No such section was appended to the r39 lesson, so a
reader who opens the lesson sees the false claim with no pointer to the erratum. `status:
corrected` is defensible for the receipt; it overstates the repair of the lesson that carries the
defect.

Recommended: append a one-line `## Correction (2026-10-24, round 40 — routed defect R2)` naming
`:27`/`:54-61`, the tracked path, and Erratum R2 — matching the r38 precedent.

### F4 — low (citation accuracy): the disposition cites the paragraph, not the sentence

`routed-defect-dispositions.json` R2 evidence lists `corpus/lessons/round-39.md:60`. Line 60 is
"c2 construction receipt and the broken-shim mutant receipt were discarded" — inside the
six-committed paragraph, so the citation does contradict the tracked file, but it is not the
sentence the disposition's own decision text quotes. The literal "not committed" wording is `:27`;
the population claim starts at `:54`. The round-40 lesson already cites this precisely
(`:27,54-61`, `corpus/lessons/round-40.md:18`), so the two round-40 records disagree on the same
source. Cheap fix: cite `:27` and `:54-61`.

### F5 — low (primitive strength): "tracked" is index-based, not committed-based

`c2-count.py:37-40` uses `git ls-files --error-unmatch`. E7 shows a staged-but-uncommitted file
passes that test while `HEAD` does not contain it. The frozen C2 predicate says the counter
re-derives "from the committed evidence"; the current primitive proves index membership only. The
verdict is unaffected at this tip (index == HEAD for the path), but the check is weaker than its
wording. Fix: `git ls-tree HEAD -- <path>` (non-empty = committed).

### F6 — low (completeness): the erratum names one uncommitted binding, the receipt has three stale/uncommitted ones

Erratum R2 says the receipt "binds an uncommitted counter digest" — true (E4). It omits that the
same receipt binds `gate_sha256 = 89022659…`, which is likewise not an object in the repository
(`git cat-file -t` → fatal; the committed mutant control hashes `e1251030…`; the r39 lesson `:26`
identifies `89022659…` as the EDITED working-tree copy), and the stale expectation digest
`3abd2dcb…` that round-40 Erratum R1 supersedes. The statement is not false, but it understates the
non-reproducibility that justifies exclusion; naming all three would let a reader confirm the
exclusion without running the verifier.

## What R2 gets right (confirmations)

| Assertion | Check | Result |
|---|---|---|
| receipt is tracked | `git ls-tree` at `6ac1007` and `HEAD` | yes, added by `6d914e9`, unchanged since |
| lesson says "not committed" | `round-39.md:27` | yes, verbatim |
| r39 dir had 7 JSON files, not 6 | `git ls-tree … \| grep -c '\.json$'` | 7 |
| binds an uncommitted counter digest | `git cat-file -t 1c3b2a9e…` | fatal (absent from object DB) |
| excluded from active set | manifest row count/content; `c1-count.py` | 6 rows, path absent, no reference |
| exclusion cannot regress silently | verifier on the receipt with committed counter | `VERIFY-FAIL: counter-sha256-mismatch` |
| erratum is append-only | frozen body lines 1-190 `sha256` at `6d914e9` vs `HEAD` | identical `fb4241d0…` |

## Residual risk and verification gaps

- The doctoring in E6 used a verbatim reimplementation of the `r2` boolean with the real
  `tracked()` imported from the module. It did not exercise `main()`'s control flow (the `try`
  block, `results`, exit code). A second-order risk: `main()` catches `OSError/ValueError/KeyError/
  TypeError/RuntimeError` and returns 2, so an unreadable receipt would surface as a counter error
  and never as a per-defect miss — acceptable, but it means file-removal attacks are `rc=2`, not
  `R2_DISPOSITION=missing-or-unverified`.
- I did not run the r39 `c1-count.py` or the C1 manifest end-to-end (other seats own C1 in this
  wave); the single verifier invocation in E4 is the only receipt-verification I exercised.
- `c2-count.py` reads the round-39 report from the fleet repo
  (`/home/vgpnk/Projects/shokunin/.ufo/reports/round-39/chousa.md`) at run time without pinning a
  digest. That is outside the R2 cell (it feeds R3/R4), but it means the same counter can score
  differently against an edited fleet report. Flagged for the seat that owns R3/R4, not claimed as
  an R2 defect.
- No external fetch was made; no live-target contact. `git`, `python3` only. `pacman` untouched per
  the lane's pause; nothing was installed, so there is no tool/version/channel entry to record.

## Artifact pointers

- Canonical erratum: `corpus/evidence/round39/claims.md:192-200` (R2 at `:197`).
- Contradicted lesson text: `corpus/lessons/round-39.md:27` and `:54-61`.
- Disposition record: `corpus/evidence/round40/routed-defect-dispositions.json` (`R2`).
- Counter cell under review: `corpus/evidence/round40/c2-count.py:37-40,60-64`.
- Tracked receipt: `corpus/evidence/round39/receipts/c1-mutenv-s39003.json` (blob at `HEAD`,
  introduced `6d914e9`).
- Active population: `corpus/evidence/round40/active-r39-receipts.tsv`; backstop
  `corpus/evidence/round40/c1-count.py:26-29`.
- Scratch reproduction harness (outside the lane, not committed):
  `/tmp/r2audit/sens.py`, `/tmp/r2audit/sens2.py`, `/tmp/r2audit/gitdemo/`.

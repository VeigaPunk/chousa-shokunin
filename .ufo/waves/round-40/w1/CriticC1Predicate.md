# Critic attack — C1 receipt-integrity predicate (round 40, w1)

**Seat:** CriticC1Predicate (leaf). **Scope:** attack the frozen P1 predicate — can the
six-row active manifest or its `R39_ACTIVE_RECEIPTS=6/6` success condition be satisfied by a
missing, invalid, or superseded receipt?

## Verdict

**Yes — two concrete counterexamples, plus supporting provenance gaps.** (1) A path-alias
row makes `6/6` print with only five distinct receipt files, masking a missing receipt.
(2) Observed live during this review: an uncommitted write to `tools/research-gate.sh`
flipped the counter `6/6 → 2/6` with every receipt and the manifest untouched — the
predicate resolves artifacts from mutable worktree paths and pins no revision, so its truth
value is set by external writes. Committed-tip state itself is clean (all six rows verify
against HEAD bytes); the defects are in what the predicate can accept and what moves it.

## Exact commands and observed output

Baseline (lane tip, captured before the round-41 gate write described in Counterexample 2):
```
$ cd /home/vgpnk/Projects/shokunin/chousa-shokunin && python3 corpus/evidence/round40/c1-count.py
… six rows, all "ok VERIFY: ok …"
R39_ACTIVE_RECEIPTS=6/6     EXIT=0
```
Per-receipt digest audit (all ten receipts): the six active rows bind `expect_sha256 =
01cbdc3a…` (current `expectations.jsonl`), counter/gate/verifier digests all match their
manifest columns; self-digest `receipt_sha256` valid for all. The three superseded r39
originals carry stale `expect_sha256 = 3abd2dcb…`.

### Counterexample (reproduced in a copied tree, `/tmp/r40rootA`)

Manifest row for `corpus/evidence/round39/receipts/c1-after-s39111.json` replaced by
`corpus/evidence/round40/receipts/./c1-after-s39011-regenerated.json` — a `./`-alias of the
row above it:

```
$ cd /tmp/r40rootA && python3 corpus/evidence/round40/c1-count.py
… 4th row prints "ok VERIFY: ok receipt=c1-after-s39011-regenerated.json …"
R39_ACTIVE_RECEIPTS=6/6     EXIT=0
```

**Only five distinct receipt files existed; the s39111 evidence was entirely absent from the
population, yet the frozen success string printed.** Cause: `c1-count.py:24` dedupes on
`{row[0] for row in rows}` — the raw path *string*. `ROOT / "a/./b"` never normalizes before
`open()`, so any lexical alias (`./`, `x/../`, symlink, or absolute path, which `pathlib`
lets override the join) bypasses both the population-size and uniqueness checks while
satisfying the file-existence requirement. The frozen kill rule "any active manifest row is
missing/duplicated" is enforced only at string level, so this population is semantically
duplicated while textually unique. Nothing pins the manifest's digest, so editing the TSV is
undetectable to the counter.

### Probe 2 — superseded receipt (expected behavior confirmed)

Swapping the superseded r39 original `c1-after-s39011.json` into the active row:
`fail VERIFY-FAIL: expect-sha256-mismatch` → `R39_ACTIVE_RECEIPTS=5/6`, exit 1. Stale
receipts are correctly refused; the `expect_sha256` rebinding works.

**But** "superseded" itself is not bound. `verify-receipts.py` binds artifact *bytes*, not
artifact *paths*: a byte-identical gate at an uncommitted path passes
(`--gate forged/copy-gate.sh` → `VERIFY: ok`, exit 0). A receipt declared superseded while
still byte-valid (e.g., `c1-after-s39111` demoted tomorrow) would still count if a manifest
row named it. Provenance ("the committed artifact at this path", "this is the active
receipt") is enforced only by the freeze on the TSV, not by the predicate.

### Probe 3 — invalid receipt: tamper refused, fabrication accepted

Byte-level doctoring fails (self-digest + every bound digest). **However** a fully re-sealed
*fabricated* receipt passes: took `c1-after-s39111.json`, changed `seed` to `99999` (no such
run ever occurred), recomputed `receipt_sha256` → `VERIFY: ok`, exit 0. The verifier checks
internal consistency and artifact digests, never that the run happened or that the receipt
is the one that was issued. Since manifest rows carry no expected `receipt_sha256`, *any*
file that verifies at a manifest path counts. "Invalid" in the sense of "not the issued
receipt" is therefore satisfiable; only "invalid = fails the verifier" is refused — and that
definition is circular.

### Counterexample 2 (live, observed during this review) — external write flips the predicate

`c1-count.py` resolves `tools/research-gate.sh` from the **working tree** and pins no
revision. While this report was being written, an uncommitted write (round-41 C1 block per
SentinelWriteScope W0) changed the live bytes — HEAD sha `4253c18738f84df9…`, live sha
`2cb04bddfd5601d7…` at my capture (Sentinel saw `77791864e79cf80f…` minutes earlier; the
file is being actively rewritten):

```
$ python3 corpus/evidence/round40/c1-count.py     # same receipts, same manifest, same HEAD
corpus/evidence/round40/receipts/c1-after-s39011-regenerated.json: fail VERIFY-FAIL: gate-sha256-mismatch
corpus/evidence/round39/receipts/c1-after-s39111.json: fail VERIFY-FAIL: gate-sha256-mismatch
corpus/evidence/round39/receipts/c2-after-s39101.json: fail VERIFY-FAIL: gate-sha256-mismatch
corpus/evidence/round39/receipts/c2-after-s39121.json: fail VERIFY-FAIL: gate-sha256-mismatch
R39_ACTIVE_RECEIPTS=2/6     EXIT=1
```

Every receipt is untouched and still internally valid; the frozen manifest is unchanged; yet
the predicate's truth value flipped 6/6 → 2/6 purely because a lane process edited a
mutable file the predicate reads. By symmetry a future write *restoring* HEAD bytes
re-satisfies it — the success condition is satisfiable/unsatisfiable by an external write,
independent of receipt integrity. This is a predicate-stability counterexample distinct
from any receipt defect: **P1 binds live worktree bytes at hardcoded paths, not committed
revisions.** Detail: `.ufo/waves/round-40/w1/SentinelWriteScope.md` (W0).

### Secondary gaps (same mechanism, smaller blast radius)

- `receipt["gate"]`, `receipt["counter"]`, `receipt["verifier"]` descriptive strings are
  never compared to the manifest columns — only the digests of the passed paths are bound.
  An issuer could record a false descriptive path in a sealed receipt and it still verifies.
- Receipts that record `predicate_holds: false` (the regenerated base `7/8` and mutenv
  `4/8` control runs) count toward `6/6` — correct semantics (receipt *integrity*, not
  predicate truth), but the success string reads as evidence-strength and is worth a
  footnote: `6/6` means six verifiable receipts, not six predicate-holding runs.
- A missing receipt *as such* cannot satisfy the predicate: `unreadable-receipt` →
  `VERIFY-FAIL`, rc 1, and `output.startswith("VERIFY: ok ")` cannot be forged by a refusal
  (all `fail()` prints go to stdout without that prefix, and `fail` returns before the ok
  line).

## Impacted axes

- **Operability (direct):** the 6/6 population check is lexically gameable, and the success
  condition itself is unstable — it binds live worktree bytes at hardcoded paths, not
  committed revisions, so an unrelated lane write silently flips `6/6 ↔ 2/6`.
- **Calibration:** `6/6` can overstate distinct evidence (alias row), certify a receipt no
  run produced (fabrication), or collapse to `2/6` under a dirty worktree — the score the
  frozen claim reports is not reproducible from committed state alone.
- **Depth:** the verifier itself is genuinely strict (schema, census, digest rebinding,
  re-derived `ok`/`matched`/`predicate_holds`); the weaknesses are at the manifest→file
  binding layer and the absence of any revision pin for artifacts, manifest, or receipts.

## Smallest safe correction

In `c1-count.py`, resolve before dedupe and reject non-canonical rows:

```python
resolved = [ (ROOT / r[0]).resolve() for r in rows ]
if (any(not str(p).startswith(str(ROOT)) for p in resolved)      # no escapes/absolute
        or len({p for p in resolved}) != EXPECTED_ACTIVE):       # real-file uniqueness
    → unexpected-population
```

That single change kills the alias counterexample and makes "missing" rows unmaskable.
Second-order hardening (optional but motivated by Counterexample 2): pin the manifest digest
or a `{path → receipt_sha256}` map so "superseded" and "fabricated-but-consistent" are
refused too, compare the receipt's `gate`/`counter` strings to the row's columns, and bind
artifact digests to committed revisions (e.g., verify `sha256(git show HEAD:path)`) rather
than live worktree bytes — without that, P1's result depends on whatever a lane process
last wrote. These are corrections for the canonical judge to weigh, not assertions that P1
fails at a clean checkout — against HEAD bytes the predicate is met honestly.

## Tooling

No installs; standard `python3`/`cp`/`mkdir` only. No production files modified; all probes
ran in `/tmp` copies.

**Artifacts:** copied-root repro harness `/tmp/r40rootA` (alias manifest, prints 6/6);
`/tmp/r40rootC/forged/` (fabricated receipt + uncommitted gate copy, both `VERIFY: ok`).

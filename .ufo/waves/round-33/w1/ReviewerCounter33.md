# Round-33 W1 review — frozen counter `corpus/evidence/round33/c1-count.py`

Reviewer: `ChousaR33.ReviewerCounter33`. Counter reviewed at `ab6b2ae2…229` (matches
`claims.md` pin). Base gate `tools/research-gate.sh` `f4731885…f0` (matches pin).
Contract source: `corpus/evidence/round33/claims.md` (read first, per control rule).

## What was run (control-permitted: review + one base-gate run with --keep)

```
cd /home/vgpnk/Projects/shokunin/chousa-shokunin
C1_TMP=/fast/scratch/hyaku/chousa-r33/w1/ReviewerCounter33 timeout 850 python3 \
  corpus/evidence/round33/c1-count.py --gate tools/research-gate.sh --seed 4701 \
  --receipt .ufo/waves/round-33/w1/ReviewerCounter33/receipt-base-4701.json \
  --keep /fast/scratch/hyaku/chousa-r33/w1/ReviewerCounter33/keep-base-4701
exit=1, printed TOPLEVEL_FIELD_MATCH=60/144, elapsed 2.04 s
```
Base 60/144 with the exact per-class split the contract predicts (before-decoys,
nested-only, duplicates, nested confusers miss; flat records pass) — consistent
with claims.md "Before (do-nothing control, L1)". No candidate gate was touched.
Kept fixture: `/fast/scratch/hyaku/chousa-r33/w1/ReviewerCounter33/keep-base-4701`
(scratch; `claims.jsonl` 144 lines, `src/` 160 files, `truth.json` appended by the
counter only in the keep copy). Receipt: `.ufo/waves/round-33/w1/ReviewerCounter33/receipt-base-4701.json`.

## Findings (severity order)

**No correctness defect found.** The counter's truth for every class is forced by
the claims.md contract; its matching rule implements the docstring exactly; the
one empirical run reproduced the frozen before-control count. Residual risk is
coverage-width and robustness, not truth-derivation error:

1. **LOW — Duplicate-class width.** Contract item 2 says "a read field that occurs
   more than once … makes the record invalid", but `D1_duplicate_top_level`
   (`c1-count.py:85`, build at `:233-253`) duplicates only `line`, `sha256`,
   `source`. A candidate that fails closed on duplicates of `id`, `span`,
   `expect` or `marker` but not on these three is caught; one that special-cases
   only `line`/`sha256`/`source` passes P1 while violating item 2 elsewhere.
   Frozen design accepts this width; recorded as residual risk.
2. **LOW — Finding-set coverage narrower than contract item 4.** The match
   condition (`:372-373`) requires `CLAIM_LINE_MISMATCH` iff `mislocated` and
   `CLAIM_SOURCE_REVISION_MISMATCH` iff `stale`. It does **not** require
   `CLAIM_SPAN_NOT_FOUND` for the 9 `unsupported` truths (N8, F1-unsupported) or
   `CLAIM_RECORD_INVALID` for the 12 `invalid` truths (D1). A candidate that
   prints the right `CLAIM`/`observed=` values while silently dropping those two
   findings scores 144/144. Faithful to claims.md's stated matching rule (which
   names only the two findings); the P1 it attests is narrower than the full
   contract text.
3. **LOW — Sub-variant asymmetry.** `N11` (`:226-232`) covers nested `expect`
   decoys only in position `before` and nested `marker` only as a nested-only
   member; `S2` (`:262-268`) uses `obj`/`arr` containers but never `deep`.
   Nested non-string values are exercised only for `line` (`N2`, `:195`), not
   `sha256`/`source`/`span`/`expect`. All seeded sub-variant counts are fixed
   (assert at `:91` verifies TOTAL=144; per-class counts confirmed in the run's
   `per_class`), so this is constant coverage, not flake.
4. **LOW (robustness, control-scoring side only).** `subprocess.run` captures
   stdout/stderr unboundedly (`:348`); a control gate printing unbounded output
   can OOM the counter rather than score 0 cleanly. A gate exceeding 600 s
   scores all-none (`:349-354`), as documented. A gate exiting rc ∉ {0,1}
   scores all records `none` (`:355`), consistent with the docstring — an
   honest low score, no false pass.
5. **LOW (foot-gun, operator side).** `tempfile.mkdtemp(dir=base)` returns a
   relative path when `C1_TMP` is relative (`:334-335`); `subprocess(cwd=root)`
   then makes `claims` (joined to `root`) relative to *inside* the fixture, so
   the gate finds no claims file and every record scores `none` — a false low,
   never a false pass. Absolute `C1_TMP` avoids it (used above). Similarly
   `--keep` inside the temp root would recurse `shutil.copytree` once before
   `rmtree`; callers are expected to keep it outside, as documented.
6. **INFO — Environment hygiene.** Only `CHOUSA_*` vars are stripped (`:347`)
   per docstring; `BASH_ENV`, `PATH`, `HOME` ride through to `bash <gate>`.
   Consistent with the docstring's "CHOUSA_* variables removed"; no network.

## Assignment checklist, checked

- **Truth derivation per class** (`build` `:190-286`): every class's truth is
  forced by contract items 1-4 —
  `N1/N4/N7/N9/N10` top-level-correct → `supported`;
  `N3` top-level `line` wrong → `mislocated`; `N6` top-level `sha256` stale →
  `stale`; `N8` span absent from the named `other` file → `unsupported`;
  `N2/N5` nested-only → contract item 1 `supported` (verified base reads the
  N2 *number* nested `line` as invalid — the base misses 12/12, matching the
  observed `0/12`); `D1` duplicated top-level read-key → `invalid` per item 2
  (raw lines confirmed to carry the member twice, e.g. `"source": "src/…", …,
  "source": "src/…"`); `S1`/`S2`/`F1` flat → `supported`/`mislocated` per the
  planted `line`. `F1` unsupported plants a *different* span (`:279-281`), so the
  span is genuinely absent. No class's truth is derivable from file/row order:
  `plan` is shuffled (`:302`), `files` is shuffled (`:314`), member order is
  randomized per record (`:175-181`), and `truth.json` is written only into
  `--keep` after the gate ran (`:383-386`).
- **Seeds/sub-variant counts:** `CLASS_COUNTS` (`:73-89`) fixes all counts;
  seed perturbs only placement/names. `assert TOTAL == 144` at `:91`.
- **Member placement:** `place` (`:175-181`) inserts the decoy container
  contiguously *before* or *after* the target top-level member (or alone for
  nested-only classes), at a random slot — exactly the "nested decoy … before
  and after the top-level member" the docstring promises.
- **Container builders:** `container` (`:129-138`) builds `obj`, `arr`
  (string, object, int — the decoy lands at depth 2), and `deep` (2-level
  object→array). Nested key names come from `gen.word()` which cannot emit any
  read key (`used` seeded with `READ_KEYS`, `:99-109`), so each decoy read-key
  occurs exactly once per container. Valid JSON confirmed: all 144 rows of the
  kept fixture parse as dicts (counter also self-asserts at `:318`).
- **S1/S2 confusers:** all six `CONFUSERS` (`:64-71`) serialize via `json.dumps`
  → valid JSON strings containing raw `{ } [ ] : ,`, an escaped quote, a
  trailing escaped backslash, and a fake `"line": "3"` member. Verified in the
  kept fixture (`"fake \"line\": \"3\", \"sha256\": \"x\""`). They defeat any
  parser that treats string content as structure (S1 flat, S2 inside nested
  containers). Note: the escaped `\"line\":` inside the string cannot trip the
  base gate's `"line"[[:space:]]*:` regex (needs a literal `"` after `e`), so S1
  passes on the base gate (observed `12/12`) — confusers target *structural*
  readers, matching contract item 3.
- **Regexes** (`:93-95`): `LINE_RE` `^CLAIM id=(\S+) .*?observed=(\S+)` matches
  the gate's emitted `CLAIM id=$id expected=$expect observed=$observed …`
  (gate `research-gate.sh:1637`). `FIND_LINE_RE`/`FIND_REV_RE` match the landed
  `emit_finding` shape `FINDING <id> severity=<sev> surface=<s> obs=<obs>`
  (`research-gate.sh:442-445`) with the emitted detail `id=$id …`
  (`:1545-1546`, `:1599`). `(?:\s|$)` guards `\S+` correctly. The `warn|crit`
  pin and exact `obs=id=` first-token requirement are format-fragile but keyed
  to landed behavior (contract item 4), so any deviation is a real contract
  miss, not counter noise.
- **Duplicate-id handling:** a `cid` seen on two CLAIM lines is forced to
  `none` (`:362-368`) regardless of which line printed what — matches docstring
  "An id printed on two CLAIM lines scores 'none'". N9's nested fake ids
  (`:219-222`) can't collide with real `cid`s except at ~10⁻⁹ probability
  (11-hex fake vs 40-bit space, 144 records) — negligible flake surface.
- **Receipt fields:** `gate_sha256` (`:400`, hashes the abspath'd gate file —
  `f4731885…` in the run receipt), `counter_sha256` (`:398`, hashes `__file__` —
  `ab6b2ae2…`), `predicate_holds` (`:402` = `matched == TOTAL`), plus `seed`,
  `gate_rc`, `gate_timed_out`, `per_class`, `misses` (84 entries with the
  `+finding-set` annotation rule `:374-375`). Receipt is written even for rc2
  gates/timeouts (`gate_rc:null`), so a dead gate produces an honest low
  receipt, never a false pass.
- **Temp-dir cleanup:** `shutil.rmtree(root, ignore_errors=True)` in `finally`
  (`:389`) covers generation failure, gate error, timeout, and keep-copy; the
  run left zero `chousa-r33-c1-*` dirs in `C1_TMP` (checked). `--keep` copies
  the fixture *after* the gate ran, so the truth file can never be read by the
  gate.

## Residual risk / verification gaps

- Coverage gaps in items 1-3 mean P1 (144/144 on this fixture) attests the
  contract on the *fixture's* shapes; a candidate regressing only on unexercised
  shapes (duplicated `id`/`span`, `obs=id=` ordering, `deep` confuser placement)
  is not detectable. This is inherent to a frozen finite counter, not a bug.
- Verified behaviorally only on the base gate (the one permitted run). No
  conformant-gate run was allowed in this wave, so the counter's 144/144 on a
  correct gate is established by the L1 oracle receipts (`.ufo/waves/round-33/controls/L1-design/`),
  not re-measured here.
- `obs`/`truth.json` values confirmed for all 15 classes via the kept fixture;
  no second seed exercised (per "run once with --keep" — kept to one run).

## Artifacts

- `.ufo/waves/round-33/w1/ReviewerCounter33/receipt-base-4701.json` (base-gate receipt)
- `/fast/scratch/hyaku/chousa-r33/w1/ReviewerCounter33/keep-base-4701/` (kept
  fixture + `truth.json`, scratch — not committed)
- Counter and gate untouched; no lane production files modified.

## Verdict

The frozen counter is sound for design v1: truth derivation is contract-forced
in all 15 classes, the base control reproduces 60/144, and no flakiness or
truth-leak was found. All findings are LOW coverage-width/robustness notes
(items 1-6 above) — none blocks scoring controls or candidates with this counter.

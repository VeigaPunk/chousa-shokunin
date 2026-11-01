# Round 68 claims (frozen 2026-10-31 at commit A, against base `27df950df83a2c0aea84cfe8de8ddb7b0ff432d4`)

Host: Windows/11, `python` 3.13.15 (`python -I` used throughout; no `python3` on this host), git 2.55.0.windows.3.
Fetches: public read-only only (one raw.githubusercontent.com pin this round); the standing r40/r65 fetch-scope and
L2-floor template L0 questions stay open and are routed around, never treated as answered. No wave: this host has no
batched dispatch surface (the round-63 attempt-2 precedent, disclosed every round since); every verdict rests on
committed counters, controls and receipts. Trigger: the round-67 closure routed exactly one lane defect to this
round — the pre-existing `tools/freeze-check.py --selftest` host drift (preflight G06; `.ufo/waves/round-67/preflight.txt`,
`corpus/README.md` `## Round66–67 provenance detail`) — with the instruction to repair the tool's host assumptions
with red-before/green-after receipts, or pin the refusal honestly; and to keep routing around the open L2-floor
question.

## C1 — operability (lowest-scored non-retired axis, 3/10; capability acquisition)

Repair the routed host drift in `tools/freeze-check.py --selftest`: derive the default lane root from the
instrument's own location instead of the hardcoded `/home/vgpnk` checkout, and map selftest fixture case names
through a Win32-reserved-character sanitizer (display names unchanged), instead of using case names containing `:`
as directory names. The frozen 34-case battery, its case names, expected exits and expected finding-ids are
byte-unchanged; only the tool's host assumptions change.

- Frozen before predicate (measured at the base `27df950df83a2c0aea84cfe8de8ddb7b0ff432d4`):
  1. `python -I tools/freeze-check.py --selftest` exits 1, traceback naming
     `/home/vgpnk/Projects/shokunin/chousa-shokunin\.ufo\waves\round-61\w1.ready`
     (`controls/before-freeze-default-root.txt`, `EXIT=1`).
  2. `python -I tools/freeze-check.py --selftest --lane-root .` exits 1 with
     `NotADirectoryError: [WinError 267]` at the fixture directory `M01 red: claims file empty`
     (`controls/before-freeze-colon-case.txt`, `EXIT=1`).
  3. `python -I tools/lane-preflight.py --root . --fleet <fleet> --skip G08` prints
     `GATE G06 freeze-selftest FAIL exit=1` and `PREFLIGHT=6/7 FAILED=G06`, exit 1
     (`controls/before-g06-preflight.txt`).
- Frozen after predicate (all four must hold at the landing):
  1. `python -I tools/freeze-check.py --selftest` prints `SELFTEST 34/34 pass` and
     `VERDICT: FREEZE_CHECK=34/34 red_before_exit=1`, exit 0.
  2. `python -I tools/freeze-check.py --selftest --lane-root .` prints `SELFTEST 34/34 pass`, exit 0.
  3. `python -I tools/lane-preflight.py --root . --fleet <fleet> --skip G08` prints
     `GATE G06 freeze-selftest PASS` and `PREFLIGHT=7/7 FAILED=none`, exit 0.
  4. `git diff <base>..<landing> -- tools/freeze-check.py` shows the only logic edits are (a) the
     `LANE_ROOT_DEFAULT` derivation and (b) the fixture-name sanitizer, and the 34 frozen
     `case(...)`/`mut(...)` literals are unchanged (`grep -c "case('" `, `grep -c "mut('"` unchanged vs base).
- Do-nothing control: the base bytes fail before-predicates 1–3 (receipts above); no counting command above
  reaches the after state without editing the tool.
- Capability row to enter in the same round: `portable gate selftest execution` — the freeze-check selftest
  battery runs green on a Win32/NTFS host for the first time (first-working round 68), evidence = the after
  battery receipt.

## C2 — depth (sourced on S164–S165, opened this round)

A method entry `corpus/knowledge/host-portable-gate-selftest-r68.md`: a gate selftest's default root is derived
from the instrument's own location (the lane's own prior-art rule, `tools/lane-preflight.py`-style `__file__`
arithmetic), and a fixture builder maps its display case names through a sanitizer for the Win32-reserved
characters (`< > : " / \ | ? *`), with the two named error signatures the drift produced (FileNotFoundError at a
foreign root; NotADirectoryError WinError 267 at a colon-containing fixture directory).

- Frozen before predicate: `grep -c '^| S164 |' corpus/SOURCES.md` → 0 (same for S165 → 0);
  `git show <base>:corpus/knowledge/host-portable-gate-selftest-r68.md` fails (entry absent);
  registry 163 rows, tiers A=122 B=30 C=11, mined=131.
- Frozen after predicate (all must hold at the landing):
  1. `python -I corpus/evidence/round66/c2-semantic-count.py --entry corpus/knowledge/host-portable-gate-selftest-r68.md`
     prints `SEMANTIC=9/9 C2SEM=PASS`, exit 0.
  2. `grep -c '^| S164 |' corpus/SOURCES.md` → 1; `grep -c '^| S165 |' corpus/SOURCES.md` → 1;
     registry 163 → 165 rows (A 122 → 123, B 30 → 31, C 11; mined 131 → 133); no held
     status/recheck/used-by cell of an existing row changed (SOURCES.md diff is additions-only).
  3. S164's capture re-derives: `git show <landing>:corpus/evidence/round68/captures/microsoft-naming-a-file-63e70903.md | sha256sum`
     = `bf2485c9f36d278b7d96f947869e36247ff8c56eacda6b65124ad0418d7bdcec`, the digest pinned in the S164 row.
  4. Quote re-open: `python -I tools/quote-reopen.py verify --items corpus/evidence/round68/quote-reopen.tsv`
     prints `verbatim=1` exit 0 for the S164 item (the located ≤25-word quote re-opened against the pinned live URL).
- Do-nothing control: the entry, both rows and the capture are absent at the base; the counter exits 2 and both
  greps return 0 without landing them.

## Sizing (§9) and separability

Both targets are do-nothing-unreachable (the before predicates are red at the base). C1 verifies from its own
receipts alone; C2 verifies from the counter, greps, capture digest and quote re-open alone — C2's evidence does
not depend on C1's repair having landed (the counter and quote-reopen run on the base bytes too), and C1's
receipts do not cite C2's artifacts. One exploratory claim budget: unused this round. Claim axes are distinct
(operability, depth); operability is the lowest-scored non-retired axis (SCORECARD `## Axes`: operability 3/10,
the only numerically scored axis, none retired) — the obligation is met by C1.

## Known limits, declared in advance

The sanitizer replaces the nine Win32-reserved characters with `_` in fixture directory names only; it is not a
general path-escape (reserved device names, trailing dots/spaces, path-length, and case-collision hazards stay
out of scope and are named in the entry). G08 stays skipped in the preflight receipts (minutes-long full
research-gate selftest; the same skip r66/r67 disclosed — the gate itself is untouched by this round). The
34-case count and `red_before_exit=1` are the base battery's own frozen expectations, unchanged by the repair.

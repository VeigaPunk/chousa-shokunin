# ClaimsBinding — round65 frozen-claims verification (seat note, not shipping authority)

Scope: verify the frozen claims file against its counters, controls, and freeze commit. No full tests run. No git/jj mutations. No production writes. Scratch deleted.

Freeze: `f99de3bdfaaf9b4c4fa85cc55dd37b9df2ee90fd` = HEAD, parent `d6ed8155e9b4735639a2cf0a3e479c62f2056195`, subject "round-65: freeze receipt identity claims and controls". The freeze diff adds 12 files (census, claims, both counters, six control files, reference validator). It does not add `corpus/evidence/round65/source-openings.json`, the knowledge entry, or any `tools/` file.

## Verdict per check

| Check | Result | Evidence |
|---|---|---|
| Claims file has exactly two claims | PASS | `grep -c '^## C'` = 2 (C1, C2) plus `Freeze and kill rule` section |
| Freeze commit exists and is HEAD | PASS | `rev-parse` of freeze hash = HEAD; `cat-file -t` = commit |
| Base commit and SKILL.md blob exist | PASS | `d6ed815…` resolves; `d6ed815…:SKILL.md` present (C1 reference depends on it) |
| C1 target absent at freeze | PASS | `tools/receipt-pin.py` not in freeze tree; absent in working tree too |
| C1 counter docstring vs code | PASS | Docstring: missing target fails, `--work` empty and removed on exit. Code: `missing-target` returns 1; nonempty `--work` → `p.error`; `finally: rmtree`. Matches |
| C1 case list = 20 cases, predicate `n==20` | PASS | 20 entries in `cases=[…]`; predicate `C1=PASS iff n==20`; exit 0 iff pass |
| C1 claim text vs case semantics | PASS | Each case's expected rc matches the reference validator's rules (exit range 0..255, lowercase 40/64 hex, canonical relative POSIX path, separator, nonempty body) |
| C1 before control `c1-before.txt` | PASS | Reproduced: `CASES=0/20 C1=FAIL missing-target`, exit 1 |
| C1 positive control `c1-positive.txt` (20/20 exit 0) | PASS | Reproduced via reference copy in isolated run: `CASES=20/20 C1=PASS`, exit 0; per-case lines match receipt |
| C1 always-pass control (3/20, exit 1) | PASS | Receipt shows 3/20 exit 1; `always-pass.py` prints PASS unconditionally (stub) — the receipt is consistent with the stub |
| C1 always-fail control (17/20, exit 1) | PASS | Receipt shows 17/20 exit 1; `always-fail.py` prints FAIL unconditionally — consistent |
| Reference validator blob/digest semantics | PASS | `ref-receipt-pin.py`: `git cat-file blob revision:path` + sha256 of stdout (blob, not working tree). Docstring matches code |
| C2 counter docstring vs predicate | PASS | Ten checks listed; predicate `n==10`; docstring says structural only, no entailment — code matches |
| C2 before control `c2-before.txt` (0/10 exit 1) | PASS | Reproduced in scratch from BASE `SOURCES.md` + `README.md` with no entry: `ENTRY_CHECKS=0/10 C2=FAIL`, exit 1 |
| C2 target on working tree (uncommitted) | PASS (informational) | `ENTRY_CHECKS=10/10 C2=PASS`, exit 0 against working-tree entry; not part of freeze |

## Source checks (read-only)

- S154 `/usr/share/man/man1/git-cat-file.1.gz` sha256 `8eb0bb07…5737` matches `source-openings.json`. Quote "raw (though uncompressed) contents" present (`zcat | grep -c` = 1).
- S155 `/usr/lib/python3.14/hashlib.py` sha256 `88fa6248…b1af492` matches. Quote "Return the digest of the bytes passed to the update() method" is on line 31, inside the SOURCES row's `27–34` range. The openings record's `31-32` is narrower but consistent.
- S156 `corpus/evidence/round64/controls/c1v3-before-full.txt` sha256 `ca05f579…8c9c05b` matches. File has 44 lines, matching `lines1–44`. Line 1 is `LEG CLEAN clean ok ok`.
- S157 `ref-receipt-pin.py` sha256 `0719d717…315fa2` matches. Docstring quote "Validate receipt header consistency, not execution authenticity." matches.

## Census

- BASE `corpus/SOURCES.md` has exactly 153 `| S` rows → matches claim "census start exit0,153 rows".
- Working tree has 157 rows (S154–S157 are in-flight, uncommitted integration additions). Not a freeze violation, but the count is no longer 153.

## Findings / risks for L1 (integration owner)

1. **Working tree drift (not mine to fix):** uncommitted modifications to `SKILL.md`, `SCORECARD.md`, `corpus/QUALITY.md`, `corpus/README.md`, `corpus/SOURCES.md`; untracked `corpus/knowledge/receipt-identity-r65.md`, `corpus/lessons/round-65.md`, `corpus/evidence/round65/source-openings.json`, and `.ufo/waves/round-65/w1*` files. The `source-openings.json` record is untracked and not in the freeze, so S154–S157 provenance is not pinned in committed history until integration commits it.
2. **C2 counter checks text presence, not semantics:** the 10 checks include `'authenticity' in text` and `'working tree' in text`. A boilerplate entry with those strings passes. The claim already states this limit; no semantic-quality claim rests on it.
3. **C1 cases hit only header/consistency paths.** Claim text already states this is not authentication or general parser safety. Valid cases are checked against a `REVISION` / `SHA256` pair computed from the BASE blob, so the reference and counter share the same digest semantics by construction.
4. **Stub controls are consistent with receipts** but "always-pass/fail" controls are trivially stubs; their receipts are genuine outputs of the counter against those stubs.

## Tool installs / updates

None. No installs or updates were performed by this seat.

## Scratch

`/fast/scratch/hyaku/chousa-r65/ClaimsBinding` created for probes and then removed. Probes: C1 before (absent tool), C1 positive (reference), C2 before (BASE content), C2 working tree. All read-only except counter-internal temp dirs, which were cleaned by the counter's own `finally`.

## Remaining unknowns

- Whether the working-tree C2 entry's 10/10 result survives the L1 commit and any later edits to SOURCES/README. Recheck with `python3 corpus/evidence/round65/c2-count.py` after integration.
- No check was run on C1 target (none exists at freeze); L1 must verify the target post-integration with `c1-count.py --work <fresh>`.
